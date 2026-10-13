//! Per-sheet SVG and DXF export of placed parts. Each placement applies its
//! rigid transform to the part's original contours, so lines, arcs, Béziers
//! and splines are written as curves, never re-polygonised. Parts without
//! source curves (polygon jobs) are written as straight segments.
use std::collections::HashMap;
use std::f64::consts::{PI, TAU};
use std::fmt::Write as _;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::job::{Job, Layout};

use crate::curves::{Affine, Contour, Segment};

/// Exact outlines of one part type: an outer contour and its holes.
#[derive(Clone, Debug)]
pub struct Outline {
    pub outer: Contour,
    pub holes: Vec<Contour>,
}

impl Outline {
    /// Straight-segment outline of a polygon part.
    pub fn from_polygon(polygon: &nestbolt_validator::Polygon) -> Self {
        let ring = |points: &[[f64; 2]]| Contour {
            start: points[0],
            segments: points[1..]
                .iter()
                .chain(std::iter::once(&points[0]))
                .map(|&to| Segment::Line { to })
                .collect(),
        };
        Self {
            outer: ring(&polygon.outer),
            holes: polygon.holes.iter().map(|h| ring(h)).collect(),
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub struct Options {
    /// Draw the sheet boundary in its own group or layer.
    pub sheet_outline: bool,
}

/// Locally verified LightBurn 2.1.01 operation colours (docs/LBRN2.md).
#[derive(Clone, Copy)]
enum Layer {
    Cut,
    Common,
    Leadin,
    Sheet,
}

impl Layer {
    const ALL: [Self; 4] = [Self::Cut, Self::Common, Self::Leadin, Self::Sheet];
    fn name(self) -> &'static str {
        match self {
            Self::Cut => "CUT",
            Self::Common => "COMMON",
            Self::Leadin => "LEADIN",
            Self::Sheet => "SHEET",
        }
    }
    fn rgb(self) -> u32 {
        match self {
            Self::Cut => 0x000000,
            Self::Common => 0x0000ff,
            Self::Leadin => 0xff0000,
            Self::Sheet => 0xf36926,
        }
    }
    fn aci(self) -> u8 {
        match self {
            Self::Cut => 7,
            Self::Common => 5,
            Self::Leadin => 1,
            Self::Sheet => 30,
        }
    }
}

/// Optional toolpaths in sheet coordinates, in millimetres. These are for
/// review only; the exporter never generates compensation, leads or cut order.
/// Open paths stay open. True-size part outlines always remain on CUT.
#[derive(Default)]
pub struct ReviewPaths {
    pub common: Vec<Contour>,
    pub leadin: Vec<Contour>,
}

fn outlines<'a>(
    job: &'a Job,
    curves: &'a HashMap<String, Outline>,
) -> Result<HashMap<&'a str, std::borrow::Cow<'a, Outline>>> {
    let mut map = HashMap::new();
    for part in &job.parts {
        let outline = match curves.get(&part.id) {
            Some(o) => std::borrow::Cow::Borrowed(o),
            None => {
                ensure!(
                    part.geometry.len() == 1,
                    "part {} has several polygons but no source curves",
                    part.id
                );
                std::borrow::Cow::Owned(Outline::from_polygon(&part.geometry[0]))
            }
        };
        map.insert(part.id.as_str(), outline);
    }
    Ok(map)
}

/// Placed contours per placement, with the sheet's width and height in mm.
type Placed = (Vec<(String, Vec<Contour>)>, f64, f64);

/// Placed contours of one sheet in sheet coordinates (Y up), with the stock.
fn placed(
    job: &Job,
    layout: &Layout,
    sheet_id: &str,
    curves: &HashMap<String, Outline>,
) -> Result<Placed> {
    let sheet = layout
        .sheets
        .iter()
        .find(|s| s.id == sheet_id)
        .with_context(|| format!("unknown sheet {sheet_id}"))?;
    let stock = job
        .stocks
        .iter()
        .find(|s| s.id == sheet.stock_id)
        .with_context(|| format!("unknown stock {}", sheet.stock_id))?;
    let outlines = outlines(job, curves)?;
    let scale = job.units.to_mm();
    let mut out = vec![];
    for p in layout.placements.iter().filter(|p| p.sheet_id == sheet_id) {
        let outline = outlines
            .get(p.part_id.as_str())
            .with_context(|| format!("unknown part {}", p.part_id))?;
        let a = Affine::placement(&p.transform).then(Affine::scale(scale));
        let mut contours = vec![outline.outer.transformed(&a)];
        contours.extend(outline.holes.iter().map(|h| h.transformed(&a)));
        out.push((format!("{}#{}", p.part_id, p.copy_index), contours));
    }
    Ok((out, stock.width * scale, stock.height * scale))
}

fn num(v: f64) -> String {
    let s = format!("{v:.6}");
    let s = s.trim_end_matches('0').trim_end_matches('.');
    if s == "-0" { "0".into() } else { s.into() }
}

fn svg_path(contour: &Contour, d: &mut String, closed: bool) {
    let p = |q: [f64; 2]| format!("{} {}", num(q[0]), num(q[1]));
    write!(d, "M {} ", p(contour.start)).expect("string write");
    for s in &contour.segments {
        match s {
            Segment::Line { to } => write!(d, "L {} ", p(*to)),
            Segment::Quad { control, to } => write!(d, "Q {} {} ", p(*control), p(*to)),
            Segment::Cubic { controls, to } => {
                write!(d, "C {} {} {} ", p(controls[0]), p(controls[1]), p(*to))
            }
            Segment::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } => {
                // One SVG arc cannot close on itself: split near-full turns.
                let pieces = if sweep.abs() > PI * 1.5 { 2 } else { 1 };
                for i in 0..pieces {
                    let part = Segment::Arc {
                        center: *center,
                        radii: *radii,
                        rotation: *rotation,
                        start: start + sweep * i as f64 / pieces as f64,
                        sweep: sweep / pieces as f64,
                    };
                    let large = (sweep / pieces as f64).abs() > PI;
                    write!(
                        d,
                        "A {} {} {} {} {} {} ",
                        num(radii[0]),
                        num(radii[1]),
                        num(rotation.to_degrees()),
                        u8::from(large),
                        u8::from(*sweep > 0.0),
                        p(part.end())
                    )
                    .expect("string write");
                }
                Ok(())
            }
        }
        .expect("string write");
    }
    if closed {
        d.push_str("Z ");
    }
}

/// One sheet as SVG in millimetres; Y is flipped to SVG's downward axis.
pub fn svg(
    job: &Job,
    layout: &Layout,
    sheet_id: &str,
    curves: &HashMap<String, Outline>,
    options: Options,
) -> Result<String> {
    svg_with_review_paths(
        job,
        layout,
        sheet_id,
        curves,
        options,
        &ReviewPaths::default(),
    )
}

/// Export exact outlines and already-computed review toolpaths on separate colours.
pub fn svg_with_review_paths(
    job: &Job,
    layout: &Layout,
    sheet_id: &str,
    curves: &HashMap<String, Outline>,
    options: Options,
    review: &ReviewPaths,
) -> Result<String> {
    let (parts, width, height) = placed(job, layout, sheet_id, curves)?;
    let flip = Affine {
        m: [[1.0, 0.0], [0.0, -1.0]],
        t: [0.0, height],
    };
    let mut out = String::new();
    writeln!(
        out,
        r#"<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">
<title>{name}: {sheet}</title>"#,
        w = num(width),
        h = num(height),
        name = xml_escape(&job.name),
        sheet = xml_escape(sheet_id)
    )?;
    if options.sheet_outline {
        writeln!(
            out,
            r##"<g id="SHEET" fill="none" stroke="#{:06x}" stroke-width="0.2"><rect id="sheet" x="0" y="0" width="{}" height="{}"/></g>"##,
            Layer::Sheet.rgb(),
            num(width),
            num(height)
        )?;
    }
    writeln!(
        out,
        r##"<g id="CUT" fill="none" stroke="#{:06x}" stroke-width="0.1">"##,
        Layer::Cut.rgb(),
    )?;
    for (id, contours) in parts {
        let mut d = String::new();
        for c in &contours {
            svg_path(&c.transformed(&flip), &mut d, true);
        }
        writeln!(
            out,
            r#"<path id="{}" fill-rule="evenodd" d="{}"/>"#,
            xml_escape(&id),
            d.trim_end()
        )?;
    }
    out.push_str("</g>\n");
    for (layer, paths) in [
        (Layer::Common, &review.common),
        (Layer::Leadin, &review.leadin),
    ] {
        if paths.is_empty() {
            continue;
        }
        writeln!(
            out,
            r##"<g id="{}" fill="none" stroke="#{:06x}" stroke-width="0.1">"##,
            layer.name(),
            layer.rgb()
        )?;
        for (i, path) in paths.iter().enumerate() {
            let mut d = String::new();
            svg_path(&path.transformed(&flip), &mut d, false);
            writeln!(
                out,
                r#"<path id="{}-{}" d="{}"/>"#,
                layer.name(),
                i + 1,
                d.trim_end()
            )?;
        }
        out.push_str("</g>\n");
    }
    out.push_str("</svg>\n");
    Ok(out)
}

fn xml_escape(s: &str) -> String {
    s.replace('&', "&amp;")
        .replace('<', "&lt;")
        .replace('>', "&gt;")
        .replace('"', "&quot;")
}

struct Dxf {
    text: String,
    handle: u32,
}

impl Dxf {
    fn pair(&mut self, code: i32, value: impl std::fmt::Display) {
        writeln!(self.text, "{code}\n{value}").expect("string write");
    }
    fn entity(&mut self, kind: &str, layer: &str) {
        self.pair(0, kind);
        self.handle += 1;
        let handle = format!("{:X}", self.handle);
        self.pair(5, handle);
        self.pair(100, "AcDbEntity");
        self.pair(8, layer);
        // Explicit BYLAYER is required for LightBurn's true-colour tool-layer
        // import; an explicit ACI 30 entity is instead mapped to cutting C05.
        self.pair(62, 256);
    }
    fn point(&mut self, code: i32, p: [f64; 2]) {
        self.pair(code, num(p[0]));
        self.pair(code + 10, num(p[1]));
        self.pair(code + 20, 0);
    }
    fn spline(&mut self, layer: &str, degree: usize, points: &[[f64; 2]]) {
        self.entity("SPLINE", layer);
        self.pair(100, "AcDbSpline");
        self.pair(70, 8);
        self.pair(71, degree);
        self.pair(72, 2 * (degree + 1));
        self.pair(73, points.len());
        for k in 0..2 * (degree + 1) {
            self.pair(40, if k <= degree { 0 } else { 1 });
        }
        for &p in points {
            self.point(10, p);
        }
    }
    fn segment(&mut self, layer: &str, from: [f64; 2], s: &Segment) {
        match s {
            Segment::Line { to } => {
                self.entity("LINE", layer);
                self.pair(100, "AcDbLine");
                self.point(10, from);
                self.point(11, *to);
            }
            Segment::Quad { control, to } => self.spline(layer, 2, &[from, *control, *to]),
            Segment::Cubic { controls, to } => {
                self.spline(layer, 3, &[from, controls[0], controls[1], *to])
            }
            Segment::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } => {
                // DXF arcs run counter-clockwise: reverse clockwise sweeps.
                let (a0, a1) = if *sweep >= 0.0 {
                    (*start, start + sweep)
                } else {
                    (start + sweep, *start)
                };
                if (radii[0] - radii[1]).abs() <= 1e-9 * radii[0].max(radii[1]) {
                    let r = radii[0];
                    if sweep.abs() >= TAU - 1e-12 {
                        self.entity("CIRCLE", layer);
                        self.pair(100, "AcDbCircle");
                        self.point(10, *center);
                        self.pair(40, num(r));
                    } else {
                        self.entity("ARC", layer);
                        self.pair(100, "AcDbCircle");
                        self.point(10, *center);
                        self.pair(40, num(r));
                        self.pair(100, "AcDbArc");
                        self.pair(50, num((a0 + rotation).to_degrees().rem_euclid(360.0)));
                        self.pair(51, num((a1 + rotation).to_degrees().rem_euclid(360.0)));
                    }
                } else {
                    // DXF ellipses need the major axis; swap axes if needed.
                    let (major, ratio, rot, shift) = if radii[0] >= radii[1] {
                        (radii[0], radii[1] / radii[0], *rotation, 0.0)
                    } else {
                        (
                            radii[1],
                            radii[0] / radii[1],
                            rotation + PI / 2.0,
                            -PI / 2.0,
                        )
                    };
                    self.entity("ELLIPSE", layer);
                    self.pair(100, "AcDbEllipse");
                    self.point(10, *center);
                    self.point(11, [major * rot.cos(), major * rot.sin()]);
                    self.pair(40, num(ratio));
                    let (p0, p1) = if sweep.abs() >= TAU - 1e-12 {
                        (0.0, TAU)
                    } else {
                        (a0 + shift, a1 + shift)
                    };
                    self.pair(41, num(p0));
                    self.pair(42, num(p1));
                }
            }
        }
    }
}

/// One sheet as an AutoCAD 2007 (AC1021) DXF in millimetres, with true-colour layers.
pub fn dxf(
    job: &Job,
    layout: &Layout,
    sheet_id: &str,
    curves: &HashMap<String, Outline>,
    options: Options,
) -> Result<String> {
    dxf_with_review_paths(
        job,
        layout,
        sheet_id,
        curves,
        options,
        &ReviewPaths::default(),
    )
}

/// Export exact outlines and already-computed review toolpaths on separate colours.
pub fn dxf_with_review_paths(
    job: &Job,
    layout: &Layout,
    sheet_id: &str,
    curves: &HashMap<String, Outline>,
    options: Options,
    review: &ReviewPaths,
) -> Result<String> {
    let (parts, width, height) = placed(job, layout, sheet_id, curves)?;
    let mut w = Dxf {
        text: String::new(),
        handle: 0x100,
    };
    for (code, value) in [
        (0, "SECTION"),
        (2, "HEADER"),
        (9, "$ACADVER"),
        (1, "AC1021"),
        (9, "$INSUNITS"),
        (70, "4"),
        (0, "ENDSEC"),
        (0, "SECTION"),
        (2, "TABLES"),
        (0, "TABLE"),
        (2, "LAYER"),
        (5, "100"),
        (330, "0"),
        (100, "AcDbSymbolTable"),
        (70, "4"),
    ] {
        w.pair(code, value);
    }
    for layer in Layer::ALL {
        w.pair(0, "LAYER");
        w.handle += 1;
        w.pair(5, format!("{:X}", w.handle));
        w.pair(330, "100");
        w.pair(100, "AcDbSymbolTableRecord");
        w.pair(100, "AcDbLayerTableRecord");
        w.pair(2, layer.name());
        w.pair(70, 0);
        w.pair(62, layer.aci());
        w.pair(420, layer.rgb());
        w.pair(6, "CONTINUOUS");
    }
    for (code, value) in [
        (0, "ENDTAB"),
        (0, "ENDSEC"),
        (0, "SECTION"),
        (2, "ENTITIES"),
    ] {
        w.pair(code, value);
    }
    if options.sheet_outline {
        let corners = [[0.0, 0.0], [width, 0.0], [width, height], [0.0, height]];
        for i in 0..4 {
            w.segment(
                "SHEET",
                corners[i],
                &Segment::Line {
                    to: corners[(i + 1) % 4],
                },
            );
        }
    }
    for (_, contours) in parts {
        for c in &contours {
            let mut from = c.start;
            for s in &c.segments {
                w.segment("CUT", from, s);
                from = s.end();
            }
        }
    }
    for (layer, paths) in [
        (Layer::Common, &review.common),
        (Layer::Leadin, &review.leadin),
    ] {
        for path in paths {
            let mut from = path.start;
            for segment in &path.segments {
                w.segment(layer.name(), from, segment);
                from = segment.end();
            }
        }
    }
    for (code, value) in [(0, "ENDSEC"), (0, "EOF")] {
        w.pair(code, value);
    }
    Ok(w.text)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::curves::hausdorff;
    use crate::import::{Options as ImportOptions, import_dxf, import_svg};
    use nestbolt_validator::{
        RigidTransform, Units,
        job::{Margins, Mode, Part, Placement, Rotations, Sheet, Stock},
    };

    const SOURCE: &str = r#"<svg xmlns="http://www.w3.org/2000/svg" width="120mm" height="80mm" viewBox="0 0 120 80">
        <path id="bracket" d="M 0 0 L 40 0 A 10 10 0 0 1 50 10 L 50 30 C 50 40 40 45 30 40 Q 10 35 0 30 Z M 15 10 A 5 3 20 1 0 25 12 A 5 3 20 1 0 15 10 Z"/>
        <circle id="washer" cx="80" cy="20" r="8"/>
    </svg>"#;

    #[test]
    fn exploded_dxf_retraces_keep_closed_curves_after_cleanup() {
        let imported = import_svg(
            include_str!("../tests/fixtures/closed-retrace.svg"),
            &ImportOptions::default(),
        )
        .unwrap();
        for (mirrored, rotation_radians) in [(false, 0.0), (true, 0.0), (false, 0.37), (true, 0.37)]
        {
            let transform = Affine::placement(&RigidTransform {
                translation: [120.0, 100.0],
                rotation_radians,
                mirrored,
            });
            let original = &imported.parts[0];
            let contours: Vec<_> = std::iter::once(&original.outer)
                .chain(&original.holes)
                .map(|c| c.transformed(&transform))
                .collect();
            let mut w = Dxf { text: "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n".into(), handle: 0x100 };
            for contour in &contours {
                let mut from = contour.start;
                for segment in &contour.segments {
                    w.segment("CUT", from, segment);
                    from = segment.end();
                }
            }
            w.text.push_str("0\nENDSEC\n0\nEOF\n");
            let got = import_dxf(&w.text, &ImportOptions::default()).unwrap();
            assert!(got.report.open_contours.is_empty());
            assert_eq!(got.parts.len(), 1);
            assert_eq!(got.parts[0].holes.len(), 1);
            assert_eq!(got.report.cleanup.overlapping_segments_merged, 0);
            if rotation_radians == 0.0 {
                assert_eq!(got.report.cleanup.closed_path_overlaps_preserved, 2);
            }
            for (expected, actual) in contours
                .iter()
                .zip(std::iter::once(&got.parts[0].outer).chain(&got.parts[0].holes))
            {
                assert!(
                    hausdorff(
                        &expected.flatten(0.0005).unwrap(),
                        &actual.flatten(0.0005).unwrap()
                    ) <= 0.001
                );
            }
        }
    }

    #[test]
    fn palette_separates_review_paths_and_keeps_them_open() {
        let (job, layout, curves) = placed_job();
        let review = ReviewPaths {
            common: vec![Contour {
                start: [10.0, 10.0],
                segments: vec![Segment::Line { to: [30.0, 10.0] }],
            }],
            leadin: vec![Contour {
                start: [50.0, 10.0],
                segments: vec![Segment::Line { to: [50.0, 20.0] }],
            }],
        };
        let opts = Options {
            sheet_outline: true,
        };
        let svg = svg_with_review_paths(&job, &layout, "sheet-0", &curves, opts, &review).unwrap();
        let dxf = dxf_with_review_paths(&job, &layout, "sheet-0", &curves, opts, &review).unwrap();
        let doc = roxmltree::Document::parse(&svg).unwrap();
        for (name, rgb, aci) in [
            ("CUT", "#000000", 7),
            ("COMMON", "#0000ff", 5),
            ("LEADIN", "#ff0000", 1),
            ("SHEET", "#f36926", 30),
        ] {
            let g = doc
                .descendants()
                .find(|n| n.attribute("id") == Some(name))
                .unwrap();
            assert_eq!(g.attribute("stroke"), Some(rgb));
            let packed = u32::from_str_radix(&rgb[1..], 16).unwrap();
            assert!(dxf.contains(&format!(
                "2\n{name}\n70\n0\n62\n{aci}\n420\n{packed}\n6\nCONTINUOUS\n"
            )));
        }
        for name in ["COMMON", "LEADIN"] {
            let path = doc
                .descendants()
                .find(|n| n.attribute("id") == Some(&format!("{name}-1")))
                .unwrap();
            assert!(!path.attribute("d").unwrap().contains('Z'));
            let selected = ImportOptions {
                layers: Some(vec![name.into()]),
                ..ImportOptions::default()
            };
            for error in [
                import_svg(&svg, &selected).unwrap_err(),
                import_dxf(&dxf, &selected).unwrap_err(),
            ] {
                assert!(error.to_string().contains("open path"));
            }
        }
        let entities = dxf.split("2\nENTITIES\n").nth(1).unwrap();
        assert!(!entities.contains("\n420\n"));
        assert!(entities.contains("\n8\nSHEET\n62\n256\n"));
        for imported in [
            import_svg(&svg, &ImportOptions::default()),
            import_dxf(&dxf, &ImportOptions::default()),
        ] {
            let imported = imported.unwrap();
            assert_eq!(imported.parts.len(), 2);
            assert!(imported.report.open_contours.is_empty());
            assert_eq!(imported.report.selection_mode, "named_cut_layers");
        }
    }

    fn placed_job() -> (Job, Layout, HashMap<String, Outline>) {
        let import = import_svg(SOURCE, &ImportOptions::default()).unwrap();
        let mut curves = HashMap::new();
        let parts = import
            .parts
            .iter()
            .map(|p| {
                curves.insert(
                    p.source.clone(),
                    Outline {
                        outer: p.outer.clone(),
                        holes: p.holes.clone(),
                    },
                );
                Part {
                    id: p.source.clone(),
                    quantity: 1,
                    geometry: vec![p.polygon.clone()],
                    rotations: Rotations::Free,
                    allow_mirror: true,
                    priority: 1.0,
                }
            })
            .collect();
        let job = Job {
            version: 1,
            name: "export".into(),
            units: Units::Mm,
            parts,
            stocks: vec![Stock {
                id: "s".into(),
                width: 300.0,
                height: 200.0,
                count: None,
                margins: Margins::default(),
                outline: vec![],
                defects: vec![],
            }],
            clearance: 0.0,
            edge_clearance: 0.0,
            mode: Mode::All,
        };
        let layout = Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![Sheet {
                id: "sheet-0".into(),
                stock_id: "s".into(),
            }],
            placements: vec![
                Placement {
                    part_id: "bracket".into(),
                    copy_index: 0,
                    sheet_id: "sheet-0".into(),
                    transform: RigidTransform {
                        translation: [120.0, 150.0],
                        rotation_radians: 2.3,
                        mirrored: true,
                    },
                },
                Placement {
                    part_id: "washer".into(),
                    copy_index: 0,
                    sheet_id: "sheet-0".into(),
                    transform: RigidTransform {
                        translation: [150.0, 80.0],
                        rotation_radians: 0.4,
                        mirrored: false,
                    },
                },
            ],
        };
        (job, layout, curves)
    }

    /// Re-imported exports must match the transformed source within 0.01 mm.
    #[test]
    fn exported_sheets_round_trip_within_hundredth_of_a_millimetre() {
        let (job, layout, curves) = placed_job();
        let options = ImportOptions {
            tolerance: 0.0005,
            ..ImportOptions::default()
        };
        let mut expected: Vec<Vec<[f64; 2]>> = vec![];
        for p in &layout.placements {
            let o = &curves[&p.part_id];
            let a = Affine::placement(&p.transform);
            for c in std::iter::once(&o.outer).chain(&o.holes) {
                expected.push(c.transformed(&a).flatten(0.0005).unwrap());
            }
        }
        let svg = svg(
            &job,
            &layout,
            "sheet-0",
            &curves,
            Options {
                sheet_outline: false,
            },
        )
        .unwrap();
        let dxf = dxf(
            &job,
            &layout,
            "sheet-0",
            &curves,
            Options {
                sheet_outline: false,
            },
        )
        .unwrap();
        for (format, import) in [
            ("svg", import_svg(&svg, &options)),
            ("dxf", import_dxf(&dxf, &options)),
        ] {
            let import = import.unwrap();
            let mut got: Vec<Vec<[f64; 2]>> = vec![];
            for p in &import.parts {
                got.push(p.polygon.outer.clone());
                got.extend(p.polygon.holes.iter().cloned());
            }
            // SVG export flips Y; map the re-import back into the sheet frame.
            if format == "svg" {
                for ring in &mut got {
                    for q in ring.iter_mut() {
                        q[1] += 200.0;
                    }
                }
            }
            assert_eq!(got.len(), expected.len(), "{format}");
            for e in &expected {
                let best = got
                    .iter()
                    .map(|g| hausdorff(e, g))
                    .fold(f64::INFINITY, f64::min);
                assert!(best < 0.01, "{format}: Hausdorff {best}");
            }
        }
        assert!(svg.contains(" A ") && svg.contains(" C ") && svg.contains(" Q "));
        assert!(
            dxf.contains("ARC")
                && dxf.contains("ELLIPSE")
                && dxf.contains("SPLINE")
                && dxf.contains("CIRCLE")
        );
    }
}
