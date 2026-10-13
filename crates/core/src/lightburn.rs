//! Lossless LightBurn document storage and geometry inspection.
//!
//! Coordinates here are the serialized project's mm, Y-up frame. Device-origin
//! MirrorX/MirrorY flags are retained separately, never applied a second time.
//! This reader does not load fonts, external bitmap files or network resources.
use std::collections::HashMap;
use std::f64::consts::{PI, TAU};

use anyhow::{Context, Result, bail, ensure};
use roxmltree::Node;
use serde::Serialize;

use crate::curves::{Affine, Contour, Point, Segment, bounds};

mod path;

#[derive(Clone, Debug, Serialize)]
pub struct Path {
    pub closed: bool,
    pub curve: Contour,
}

impl Path {
    pub fn points(&self, tolerance: f64) -> Result<Vec<Point>> {
        ensure!(
            tolerance.is_finite() && tolerance > 0.0,
            "curve tolerance must be finite and positive"
        );
        let mut points = vec![self.curve.start];
        let mut from = self.curve.start;
        for segment in &self.curve.segments {
            segment.flatten(from, tolerance, &mut points)?;
            from = segment.end();
        }
        Ok(points)
    }
}

#[derive(Clone, Debug, Serialize)]
pub struct Layer {
    pub index: u32,
    pub image: bool,
    pub name: String,
    pub mode: String,
    pub output: bool,
    pub hidden: bool,
    pub cuts: bool,
    pub kerf_mm: f64,
}

#[derive(Clone, Debug, Serialize)]
pub struct Shape {
    pub kind: String,
    /// Indices in Scene.shapes, in source order. None marks a top-level shape.
    pub parent: Option<usize>,
    pub top_level: usize,
    pub children: Vec<usize>,
    pub cut_index: u32,
    pub image_layer: bool,
    pub fixed: bool,
    pub geometry_complete: bool,
    pub local_xform: [f64; 6],
    pub world_xform: [f64; 6],
    pub paths: Vec<Path>,
    pub bitmap_corners: Option<[Point; 4]>,
    pub bitmap_data_bytes: Option<usize>,
    pub bounds_mm: Option<[f64; 4]>,
    /// Byte range in the untouched source, used by the preserving writer.
    #[serde(skip)]
    pub source_range: [usize; 2],
}

#[derive(Clone, Debug, Serialize)]
pub struct Scene {
    pub format_version: u32,
    pub mirror_x: bool,
    pub mirror_y: bool,
    pub layers: Vec<Layer>,
    pub shapes: Vec<Shape>,
    pub top_level: Vec<usize>,
    pub warnings: Vec<String>,
}

/// Keeps the entire source, including unknown XML, attribute order, whitespace,
/// settings, embedded images and comments. A no-op write is byte-identical.
pub struct Document {
    source: String,
    pub scene: Scene,
}

fn child<'a, 'input>(node: Node<'a, 'input>, name: &str) -> Option<Node<'a, 'input>> {
    node.children().find(|n| n.has_tag_name(name))
}

fn number(node: Node, attribute: &str, default: Option<f64>) -> Result<f64> {
    let value = node
        .attribute(attribute)
        .map(str::parse::<f64>)
        .transpose()
        .with_context(|| format!("invalid LightBurn {attribute}"))?
        .or(default)
        .with_context(|| format!("missing LightBurn {attribute}"))?;
    ensure!(value.is_finite(), "non-finite LightBurn {attribute}");
    Ok(value)
}

fn boolean(value: Option<&str>, default: bool) -> Result<bool> {
    match value.map(str::to_ascii_lowercase).as_deref() {
        None => Ok(default),
        Some("true" | "1") => Ok(true),
        Some("false" | "0") => Ok(false),
        _ => bail!("invalid LightBurn boolean {value:?}"),
    }
}

fn xform(node: Node) -> Result<Affine> {
    let Some(xform) = child(node, "XForm") else {
        return Ok(Affine::IDENTITY);
    };
    let values = xform
        .text()
        .unwrap_or("")
        .split_whitespace()
        .map(str::parse::<f64>)
        .collect::<std::result::Result<Vec<_>, _>>()
        .context("invalid LightBurn XForm; re-save the project")?;
    ensure!(
        values.len() == 6 && values.iter().all(|v| v.is_finite()),
        "LightBurn XForm needs six finite numbers; re-save the project"
    );
    Ok(Affine {
        m: [[values[0], values[2]], [values[1], values[3]]],
        t: [values[4], values[5]],
    })
}

fn values(m: Affine) -> [f64; 6] {
    [m.m[0][0], m.m[1][0], m.m[0][1], m.m[1][1], m.t[0], m.t[1]]
}

struct Resources<'a, 'input> {
    vertices: HashMap<String, Node<'a, 'input>>,
    primitives: HashMap<String, Node<'a, 'input>>,
    images: HashMap<String, &'a str>,
}

impl<'a, 'input> Resources<'a, 'input> {
    fn read(root: Node<'a, 'input>) -> Result<Self> {
        let mut resources = Self {
            vertices: HashMap::new(),
            primitives: HashMap::new(),
            images: HashMap::new(),
        };
        for n in root.descendants().filter(Node::is_element) {
            for (attribute, list, map) in [
                ("VertID", "VertList", &mut resources.vertices),
                ("PrimID", "PrimList", &mut resources.primitives),
            ] {
                if let Some(id) = n.attribute(attribute)
                    && let Some(value) = child(n, list)
                    && let Some(prior) = map.insert(id.into(), value)
                {
                    ensure!(
                        prior.text() == value.text(),
                        "conflicting LightBurn {attribute} {id}; re-save shared geometry"
                    );
                }
            }
            if n.attribute("Type") == Some("Bitmap")
                && let Some(id) = n.attribute("SourceHash")
                && let Some(data) = n.attribute("Data")
                && let Some(prior) = resources.images.insert(id.into(), data)
            {
                ensure!(
                    prior == data,
                    "conflicting LightBurn bitmap SourceHash {id}; embed the images again"
                );
            }
        }
        Ok(resources)
    }
    fn list(
        &self,
        node: Node<'a, 'input>,
        name: &str,
        id: &str,
    ) -> Result<Option<Node<'a, 'input>>> {
        if let Some(list) = child(node, name) {
            return Ok(Some(list));
        }
        if let Some(reference) = node.attribute(id) {
            let map = if id == "VertID" {
                &self.vertices
            } else {
                &self.primitives
            };
            return Ok(Some(*map.get(reference).with_context(||format!("unresolved LightBurn {id} {reference}; re-save the project with shared geometry intact"))?));
        }
        Ok(None)
    }
}

fn read_layer(node: Node) -> Result<Layer> {
    let field = |name| child(node, name).and_then(|n| n.attribute("Value"));
    let mode = node
        .attribute("type")
        .or(node.attribute("Type"))
        .unwrap_or("Cut")
        .to_owned();
    let cuts = matches!(mode.as_str(), "Cut" | "Scan+Cut" | "ScanCut")
        || node.descendants().any(|n| {
            n.has_tag_name("SubLayer")
                && matches!(
                    n.attribute("type").or(n.attribute("Type")),
                    Some("Cut" | "Scan+Cut" | "ScanCut")
                )
        });
    let kerf = field("kerf")
        .unwrap_or("0")
        .parse::<f64>()
        .context("invalid LightBurn layer kerf")?;
    ensure!(kerf.is_finite(), "non-finite LightBurn layer kerf");
    Ok(Layer {
        index: field("index")
            .context("LightBurn cut setting has no index")?
            .parse()
            .context("invalid LightBurn layer index")?,
        image: node.has_tag_name("CutSetting_Img"),
        name: field("name").unwrap_or("").into(),
        mode,
        output: boolean(field("doOutput"), true)?,
        hidden: boolean(field("hide"), false)?,
        cuts,
        kerf_mm: kerf,
    })
}

fn rectangle(w: f64, h: f64, r: f64) -> Path {
    let (x, y) = (-w / 2.0, -h / 2.0);
    let points = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
    if r == 0.0 {
        return polygon(&points);
    }
    let arc = |cx, cy, start| Segment::Arc {
        center: [cx, cy],
        radii: [r, r],
        rotation: 0.0,
        start,
        sweep: PI / 2.0,
    };
    Path {
        closed: true,
        curve: Contour {
            start: [x + r, y],
            segments: vec![
                Segment::Line { to: [x + w - r, y] },
                arc(x + w - r, y + r, -PI / 2.0),
                Segment::Line {
                    to: [x + w, y + h - r],
                },
                arc(x + w - r, y + h - r, 0.0),
                Segment::Line { to: [x + r, y + h] },
                arc(x + r, y + h - r, PI / 2.0),
                Segment::Line { to: [x, y + r] },
                arc(x + r, y + r, PI),
            ],
        },
    }
}

fn polygon(points: &[Point]) -> Path {
    Path {
        closed: true,
        curve: Contour {
            start: points[0],
            segments: points
                .iter()
                .skip(1)
                .chain(&points[..1])
                .map(|&to| Segment::Line { to })
                .collect(),
        },
    }
}

impl Document {
    pub fn read(source: &str, tolerance_mm: f64) -> Result<Self> {
        ensure!(
            tolerance_mm.is_finite() && tolerance_mm > 0.0 && tolerance_mm <= 0.01,
            "LightBurn geometry tolerance must be positive and no more than 0.01 mm"
        );
        let xml = roxmltree::Document::parse_with_options(
            source,
            roxmltree::ParsingOptions {
                nodes_limit: 1_000_000,
                ..Default::default()
            },
        )
        .context("invalid LightBurn XML; re-save as .lbrn or .lbrn2")?;
        let root = xml.root_element();
        ensure!(
            root.has_tag_name("LightBurnProject"),
            "not a LightBurnProject document"
        );
        let version = root
            .attribute("FormatVersion")
            .unwrap_or("0")
            .parse::<u32>()
            .context("invalid LightBurn FormatVersion")?;
        ensure!(
            version <= 1,
            "unsupported LightBurn FormatVersion {version}; save a single-page .lbrn2 project compatible with LightBurn 2.1"
        );
        let resources = Resources::read(root)?;
        let mut scene = Scene {
            format_version: version,
            mirror_x: boolean(root.attribute("MirrorX"), false)?,
            mirror_y: boolean(root.attribute("MirrorY"), false)?,
            layers: vec![],
            shapes: vec![],
            top_level: vec![],
            warnings: vec![],
        };
        for node in root
            .children()
            .filter(|n| n.has_tag_name("CutSetting") || n.has_tag_name("CutSetting_Img"))
        {
            let layer = read_layer(node)?;
            ensure!(
                !scene
                    .layers
                    .iter()
                    .any(|l| l.index == layer.index && l.image == layer.image),
                "duplicate LightBurn layer index {} in the same setting family; repair the cut settings",
                layer.index
            );
            scene.layers.push(layer);
        }
        for (top, node) in root
            .children()
            .filter(|n| n.has_tag_name("Shape"))
            .enumerate()
        {
            let index = read_shape(
                node,
                None,
                top,
                Affine::IDENTITY,
                &resources,
                &mut scene,
                tolerance_mm,
                0,
            )?;
            scene.top_level.push(index);
        }
        Ok(Self {
            source: source.to_owned(),
            scene,
        })
    }
    pub fn original_xml(&self) -> &str {
        &self.source
    }
}

#[allow(clippy::too_many_arguments)]
fn read_shape(
    node: Node,
    parent: Option<usize>,
    top_level: usize,
    parent_transform: Affine,
    resources: &Resources,
    scene: &mut Scene,
    tolerance: f64,
    depth: usize,
) -> Result<usize> {
    ensure!(
        depth < 128,
        "LightBurn groups are too deeply nested; ungroup some levels before importing"
    );
    let kind = node
        .attribute("Type")
        .context("LightBurn Shape has no Type")?
        .to_owned();
    let local = xform(node)?;
    let world = local.then(parent_transform);
    let index = scene.shapes.len();
    let cut_index = node
        .attribute("CutIndex")
        .unwrap_or("0")
        .parse::<u32>()
        .context("invalid LightBurn CutIndex")?;
    let image_layer = kind == "Bitmap";
    let layer = scene
        .layers
        .iter()
        .find(|l| l.index == cut_index && l.image == image_layer);
    let fixed = layer.is_some_and(|l| !l.output || l.mode == "Tool");
    let mut shape = Shape {
        kind: kind.clone(),
        parent,
        top_level,
        children: vec![],
        cut_index,
        image_layer,
        fixed,
        geometry_complete: true,
        local_xform: values(local),
        world_xform: values(world),
        paths: vec![],
        bitmap_corners: None,
        bitmap_data_bytes: None,
        bounds_mm: None,
        source_range: [node.range().start, node.range().end],
    };
    if layer.is_none() && kind != "Group" {
        scene.warnings.push(format!(
            "shape {index}: no {} setting for CutIndex {cut_index}; source settings are preserved",
            if image_layer { "image" } else { "vector" }
        ));
    }
    let mut paths = match kind.as_str() {
        "Group" => vec![],
        "Path" => {
            path::read(node, resources).with_context(|| format!("LightBurn Path shape {index}"))?
        }
        "Rect" | "Bitmap" => {
            let (w, h) = (number(node, "W", None)?, number(node, "H", None)?);
            ensure!(
                w > 0.0 && h > 0.0,
                "LightBurn {kind} shape {index} needs positive W and H; repair its size"
            );
            if image_layer {
                shape.bitmap_corners = Some(
                    [
                        [-w / 2.0, -h / 2.0],
                        [w / 2.0, -h / 2.0],
                        [w / 2.0, h / 2.0],
                        [-w / 2.0, h / 2.0],
                    ]
                    .map(|p| world.apply(p)),
                );
                let data=node.attribute("Data").or_else(||node.attribute("SourceHash").and_then(|id|resources.images.get(id).copied()))
                    .with_context(||format!("Bitmap shape {index} has unresolved image data; embed the bitmap in LightBurn and save again"))?;
                shape.bitmap_data_bytes = Some(data.len());
                vec![]
            } else {
                let radius = number(node, "Cr", Some(0.0))?;
                ensure!(radius >= 0.0, "negative LightBurn rectangle corner radius");
                vec![rectangle(w, h, radius.min(w / 2.0).min(h / 2.0))]
            }
        }
        "Ellipse" | "Polygon" => {
            let (rx, ry) = (number(node, "Rx", None)?, number(node, "Ry", None)?);
            ensure!(
                rx > 0.0 && ry > 0.0,
                "LightBurn {kind} shape {index} needs positive radii"
            );
            if kind == "Ellipse" {
                vec![Path {
                    closed: true,
                    curve: Contour {
                        start: [rx, 0.0],
                        segments: vec![Segment::Arc {
                            center: [0.0, 0.0],
                            radii: [rx, ry],
                            rotation: 0.0,
                            start: 0.0,
                            sweep: TAU,
                        }],
                    },
                }]
            } else {
                let n = node
                    .attribute("N")
                    .context("LightBurn Polygon has no side count")?
                    .parse::<usize>()?;
                ensure!(
                    (3..=100_000).contains(&n),
                    "invalid LightBurn Polygon side count"
                );
                vec![polygon(
                    &(0..n)
                        .map(|i| {
                            let a = TAU * i as f64 / n as f64;
                            [rx * a.cos(), ry * a.sin()]
                        })
                        .collect::<Vec<_>>(),
                )]
            }
        }
        "Text" => {
            if let Some(backup) = child(node, "BackupPath") {
                // Cached paths are in text-local coordinates. Backup XForm is a
                // redundant world-space cache in native saves; using the Text
                // chain also keeps geometry correct after moving its group.
                path::read(backup, resources)
                    .with_context(|| format!("Text shape {index} BackupPath"))?
            } else {
                shape.geometry_complete = false;
                scene.warnings.push(format!("Text shape {index} has no BackupPath; open and re-save in LightBurn to cache its exact font outlines before nesting"));
                vec![]
            }
        }
        _ => {
            shape.geometry_complete = false;
            scene.warnings.push(format!("unsupported LightBurn Shape Type {kind:?} at {index}; convert it to paths before nesting; its original XML is retained"));
            vec![]
        }
    };
    for path in &mut paths {
        let (start, segments) =
            crate::import::map_segments(path.curve.start, &path.curve.segments, &world);
        path.curve = Contour { start, segments };
    }
    shape.paths = paths;
    let mut points = vec![];
    for path in &shape.paths {
        points.extend(path.points(tolerance)?);
    }
    if let Some(corners) = shape.bitmap_corners {
        points.extend(corners);
    }
    ensure!(
        points.iter().flatten().all(|v| v.is_finite()),
        "non-finite transformed LightBurn geometry at shape {index}"
    );
    if !points.is_empty() {
        shape.bounds_mm = Some(bounds(&points));
    }
    scene.shapes.push(shape);
    if kind == "Group"
        && let Some(children) = child(node, "Children")
    {
        let mut child_indices = vec![];
        for child in children.children().filter(|n| n.has_tag_name("Shape")) {
            child_indices.push(read_shape(
                child,
                Some(index),
                top_level,
                world,
                resources,
                scene,
                tolerance,
                depth + 1,
            )?);
        }
        let mut corners = vec![];
        for &child in &child_indices {
            if let Some([x0, y0, x1, y1]) = scene.shapes[child].bounds_mm {
                corners.extend([[x0, y0], [x1, y1]]);
            }
        }
        let any_fixed = child_indices.iter().any(|&i| scene.shapes[i].fixed);
        if any_fixed && child_indices.iter().any(|&i| !scene.shapes[i].fixed) {
            scene.warnings.push(format!("Group shape {index} contains both fixed and movable children; keep the whole rigid group fixed"));
        }
        let complete = child_indices
            .iter()
            .all(|&i| scene.shapes[i].geometry_complete);
        let shape = &mut scene.shapes[index];
        if !corners.is_empty() {
            shape.bounds_mm = Some(bounds(&corners));
        }
        shape.fixed = any_fixed;
        shape.geometry_complete = complete;
        shape.children = child_indices;
    }
    Ok(index)
}
