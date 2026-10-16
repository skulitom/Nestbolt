//! Rigid nesting membership and collision geometry, separate from the source XML.
use std::collections::HashSet;

use anyhow::{Context, Result, ensure};
use clipper2_rust::{ClipType, Clipper64, FillRule, Paths64, Point64, PolyTree64};
use nestbolt_validator::{Footprint, GRID, Polygon, RigidTransform, Units};
use serde::Serialize;

use super::{Document, Scene, Shape};
use crate::curves::{Point, signed_area};

const SCALE: f64 = 1_000_000.0;

#[derive(Clone, Debug, Serialize)]
pub struct Unit {
    pub id: usize,
    /// Top-level ordinals, not indices into the flattened scene's shapes.
    pub members: Vec<usize>,
    /// Millimetres in the original document's Y-up coordinate frame. The same
    /// placement applies to these polygons and to the members' original XForms.
    pub geometry: Vec<Polygon>,
    pub bounds_mm: [f64; 4],
    pub area_mm2: f64,
}

#[derive(Serialize)]
pub struct Nesting<'a> {
    #[serde(skip)]
    pub(super) document: &'a Document,
    pub units: Vec<Unit>,
    pub fixed: Vec<usize>,
    pub tolerance_mm: f64,
    pub warnings: Vec<String>,
}

fn paths(polygons: &[Polygon]) -> Paths64 {
    polygons
        .iter()
        .flat_map(|p| std::iter::once((&p.outer, true)).chain(p.holes.iter().map(|h| (h, false))))
        .map(|(ring, outer)| {
            let mut points: Vec<_> = ring
                .iter()
                .map(|p| Point64::new((p[0] * SCALE).round() as i64, (p[1] * SCALE).round() as i64))
                .collect();
            if (signed_area(ring) > 0.0) != outer {
                points.reverse();
            }
            points
        })
        .collect()
}

fn union(input: &Paths64, rule: FillRule) -> Result<Vec<Polygon>> {
    let mut engine = Clipper64::new();
    engine.add_subject(input);
    let mut tree = PolyTree64::new();
    ensure!(
        engine.execute_tree(ClipType::Union, rule, &mut tree, &mut vec![]),
        "LightBurn outline union failed; repair the source outlines"
    );
    let ring = |i: usize| -> Vec<Point> {
        tree.nodes[i]
            .polygon()
            .iter()
            .map(|p| [p.x as f64 / SCALE, p.y as f64 / SCALE])
            .collect()
    };
    Ok((1..tree.nodes.len())
        .filter(|&i| !tree.is_hole(i))
        .map(|i| Polygon {
            outer: ring(i),
            holes: tree.nodes[i].children().iter().map(|&j| ring(j)).collect(),
        })
        .collect())
}

fn closed(shape: &Shape) -> bool {
    matches!(shape.kind.as_str(), "Path" | "Rect" | "Ellipse" | "Polygon")
        && !shape.paths.is_empty()
        && shape.paths.iter().all(|p| p.closed)
}

fn box_polygon(bounds: [f64; 4]) -> Polygon {
    let [x0, y0, x1, y1] = bounds;
    nestbolt_validator::job::rectangle(x0, y0, x1 - x0, y1 - y0)
}

fn nesting_bounds(mut bounds: [f64; 4], tolerance: f64) -> [f64; 4] {
    // Open strokes need a nonzero collision footprint, whether grouped or not.
    // Almost-axis-aligned strokes can also collapse in the solver's floating
    // point representation. Reserve at least two curve tolerances on each
    // axis, adding at most one on each side. Stored/exported paths stay exact.
    let padding = tolerance.max(GRID);
    for axis in 0..2 {
        let extra = (2.0 * padding - (bounds[axis + 2] - bounds[axis])) * 0.5;
        if extra > 0.0 {
            bounds[axis] -= extra;
            bounds[axis + 2] += extra;
        }
    }
    bounds
}

fn geometry(
    scene: &Scene,
    index: usize,
    tolerance: f64,
    warnings: &mut Vec<String>,
) -> Result<Vec<Polygon>> {
    let shape = &scene.shapes[index];
    ensure!(
        shape.geometry_complete,
        "LightBurn shape {index} ({}) has incomplete geometry; open and re-save text in LightBurn to cache its outlines, or convert unsupported shapes to paths before nesting",
        shape.kind
    );
    let polygons = if shape.kind == "Group" {
        let mut components = vec![];
        for &child in &shape.children {
            components.extend(geometry(scene, child, tolerance, warnings)?);
        }
        union(&paths(&components), FillRule::NonZero)?
    } else if closed(shape) {
        let rings = shape
            .paths
            .iter()
            .map(|p| p.points(tolerance))
            .collect::<Result<Vec<_>>>()?;
        ensure!(
            rings.iter().flatten().flatten().all(|v| v.abs() <= 1e8),
            "LightBurn shape {index} exceeds the supported coordinate range; move it nearer the origin"
        );
        let input = rings
            .iter()
            .map(|r| {
                r.iter()
                    .map(|p| {
                        Point64::new((p[0] * SCALE).round() as i64, (p[1] * SCALE).round() as i64)
                    })
                    .collect()
            })
            .collect();
        // Each multi-contour closed shape follows containment parity. Different
        // children in a rigid group are then unioned, never XORed against text
        // or an engraving that occupies the same material.
        union(&input, FillRule::EvenOdd)?
    } else {
        let bounds = shape.bounds_mm.with_context(||
            format!("LightBurn shape {index} has no measurable bounds; group it with a closed outline before nesting"))?;
        let [x0, y0, x1, y1] = nesting_bounds(bounds, tolerance);
        ensure!(
            x1 > x0 && y1 > y0,
            "LightBurn shape {index} has a zero-width or zero-height bounding rectangle; group it with a closed outline before nesting"
        );
        warnings.push(format!(
            "LightBurn shape {index} ({}): nesting uses a bounding rectangle around this artwork; original artwork is preserved in the editable project",
            shape.kind
        ));
        vec![box_polygon([x0, y0, x1, y1])]
    };
    ensure!(
        !polygons.is_empty(),
        "LightBurn shape {index} has no solid nesting outline; repair its contours or group it with a closed outline"
    );
    Footprint::from_polygons(&polygons, Units::Mm, RigidTransform::default())
        .with_context(|| format!("LightBurn shape {index} has invalid nesting geometry; repair crossing or touching contours"))?;
    Ok(polygons)
}

impl Document {
    fn check_fixed_groups(&self) -> Result<()> {
        for &index in &self.scene.top_level {
            let root = &self.scene.shapes[index];
            if !root.fixed || root.kind != "Group" {
                continue;
            }
            let mut remaining = root.children.clone();
            while let Some(child) = remaining.pop() {
                let shape = &self.scene.shapes[child];
                ensure!(
                    shape.kind == "Group" || shape.fixed,
                    "LightBurn group {index} mixes output-enabled artwork with Tool/output-off shapes; ungroup it in LightBurn and group movable artwork separately before nesting"
                );
                remaining.extend(&shape.children);
            }
        }
        Ok(())
    }

    /// Assemble the plan's rigid units. Incomplete movable geometry fails the
    /// whole operation; fixed XML may remain without measurable geometry.
    pub fn nesting_units(&self, tolerance_mm: f64) -> Result<Nesting<'_>> {
        ensure!(
            tolerance_mm.is_finite() && tolerance_mm > 0.0 && tolerance_mm <= 0.01,
            "LightBurn nesting tolerance must be positive and no more than 0.01 mm"
        );
        self.check_fixed_groups()?;
        let scene = &self.scene;
        let mut warnings = scene.warnings.clone();
        let mut fixed = vec![];
        let mut footprints = vec![];
        let mut geometries = vec![];
        for (top, &i) in scene.top_level.iter().enumerate() {
            if scene.shapes[i].fixed {
                fixed.push(top);
                geometries.push(vec![]);
                footprints.push(None);
            } else {
                ensure!(
                    scene.shapes[i].geometry_complete,
                    "LightBurn top-level shape {top} has incomplete geometry; re-save text in LightBurn to cache its outlines, or convert unsupported shapes to paths before nesting"
                );
                if closed(&scene.shapes[i]) && scene.is_cutting(&scene.shapes[i]) {
                    let g = geometry(scene, i, tolerance_mm, &mut warnings)?;
                    footprints.push(Some(Footprint::from_polygons(
                        &g,
                        Units::Mm,
                        RigidTransform::default(),
                    )?));
                    geometries.push(g);
                } else {
                    footprints.push(None);
                    geometries.push(vec![]);
                }
            }
        }
        let candidates: Vec<_> = scene
            .top_level
            .iter()
            .enumerate()
            .filter_map(|(top, &i)| {
                let shape = &scene.shapes[i];
                (!shape.fixed && closed(shape) && scene.is_cutting(shape)).then_some(top)
            })
            .collect();
        let mut attachments = vec![vec![]; scene.top_level.len()];
        let mut attached = HashSet::new();
        for (top, &i) in scene.top_level.iter().enumerate() {
            let shape = &scene.shapes[i];
            if shape.fixed
                || shape.kind == "Group"
                || (scene.is_cutting(shape) && shape.kind != "Text")
            {
                continue;
            }
            // Containment of the entire rectangle catches concavities and holes;
            // testing only its corners would attach engravings across a notch.
            let Some(b) = shape.bounds_mm else {
                continue;
            };
            let b = nesting_bounds(b, tolerance_mm);
            let bounds = Footprint::new(&box_polygon(b), Units::Mm, RigidTransform::default())?;
            let mut containing = vec![];
            for &parent in &candidates {
                if parent == top {
                    continue;
                }
                let footprint = footprints[parent].as_ref().expect("movable candidate");
                let relation = bounds.inside(footprint, tolerance_mm)?;
                if relation.outside_area == 0.0 && !relation.clearance_violation {
                    containing.push(parent);
                }
            }
            containing.sort_by(|&a, &b| {
                footprints[a]
                    .as_ref()
                    .unwrap()
                    .area()
                    .total_cmp(&footprints[b].as_ref().unwrap().area())
                    .then(a.cmp(&b))
            });
            if let Some(&parent) = containing.first() {
                attachments[parent].push(top);
                attached.insert(top);
                if containing.len() > 1 {
                    warnings.push(format!("top-level shape {top} lies inside several cutting outlines; attached to the smallest, shape {parent}; group explicitly to choose another"));
                }
            }
        }
        let mut units = vec![];
        for (top, mut polygons) in geometries.into_iter().enumerate() {
            if fixed.contains(&top) || attached.contains(&top) {
                continue;
            }
            if polygons.is_empty() {
                polygons = geometry(scene, scene.top_level[top], tolerance_mm, &mut warnings)?;
            }
            let mut members = vec![top];
            members.extend(&attachments[top]);
            members.sort_unstable();
            let footprint =
                Footprint::from_polygons(&polygons, Units::Mm, RigidTransform::default())?;
            units.push(Unit {
                id: units.len(),
                members,
                geometry: polygons,
                bounds_mm: footprint.bounds(),
                area_mm2: footprint.area(),
            });
        }
        Ok(Nesting {
            document: self,
            units,
            fixed,
            tolerance_mm,
            warnings,
        })
    }
}
