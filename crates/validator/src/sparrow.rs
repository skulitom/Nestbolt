//! Strip-output adapter. Always reads original polygons from a separate input.
use std::collections::{BTreeMap, BTreeSet};

use anyhow::{Context, Result, ensure};
use serde::{Deserialize, Serialize};

use crate::{BACKEND, Footprint, GRID, Polygon, RigidTransform, Units};

#[derive(Deserialize)]
struct Instance {
    name: String,
    strip_height: f64,
    items: Vec<Item>,
}

#[derive(Deserialize)]
struct Item {
    id: u64,
    demand: u64,
    allowed_orientations: Option<Vec<f64>>,
    shape: Shape,
}

#[derive(Deserialize)]
#[serde(tag = "type", content = "data", rename_all = "snake_case")]
enum Shape {
    SimplePolygon(Vec<[f64; 2]>),
}

#[derive(Deserialize)]
struct Output {
    solution: Solution,
}

#[derive(Deserialize)]
struct Solution {
    strip_width: f64,
    layout: Layout,
}

#[derive(Deserialize)]
struct Layout {
    placed_items: Vec<Placed>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Placed {
    item_id: u64,
    transformation: Transform,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Transform {
    translation: [f64; 2],
    rotation: f64,
}

#[derive(Debug, Serialize)]
pub struct StripReport {
    pub valid: bool,
    pub instance: String,
    pub backend: &'static str,
    pub units: Units,
    pub strip_width: f64,
    pub expected_parts: u64,
    pub placed_parts: usize,
    pub maximum_overlap_ratio: f64,
    pub maximum_outside_ratio: f64,
    pub violations: Vec<String>,
}

/// Validate original simple polygons, quantities, rigid transforms, rotations,
/// containment and pairwise overlap independently of Sparrow's own geometry.
/// The historical strip instances have zero inter-part clearance.
pub fn validate(input: &str, output: &str, units: Units) -> Result<StripReport> {
    let source: Instance = serde_json::from_str(input).context("invalid original Sparrow input")?;
    let output: Output = serde_json::from_str(output).context("invalid Sparrow solution JSON")?;
    ensure!(
        source.strip_height.is_finite() && source.strip_height > 0.0,
        "strip height must be positive and finite"
    );
    let width = output.solution.strip_width;
    ensure!(
        width.is_finite() && width > 0.0,
        "strip width must be positive and finite"
    );
    let mut ids = BTreeSet::new();
    let mut expected = 0_u64;
    for item in &source.items {
        ensure!(ids.insert(item.id), "duplicate source item ID {}", item.id);
        expected = expected
            .checked_add(item.demand)
            .context("part count overflow")?;
        if let Some(angles) = &item.allowed_orientations {
            ensure!(
                angles.iter().all(|a| a.is_finite()),
                "source orientations must be finite"
            );
        }
        let Shape::SimplePolygon(ref points) = item.shape;
        Footprint::new(
            &Polygon {
                outer: points.clone(),
                holes: vec![],
            },
            units,
            RigidTransform::default(),
        )
        .with_context(|| format!("invalid original part {}", item.id))?;
    }
    ensure!((1..=2000).contains(&expected), "job requires 1..2000 parts");
    let placed = output.solution.layout.placed_items;
    ensure!(placed.len() <= 2000, "layout exceeds 2000 parts");
    // Only integer-grid rounding is tolerated at the container boundary.
    let epsilon = 2.0 * GRID / units.to_mm();
    let container = Footprint::new(
        &Polygon {
            outer: vec![
                [-epsilon, -epsilon],
                [width + epsilon, -epsilon],
                [width + epsilon, source.strip_height + epsilon],
                [-epsilon, source.strip_height + epsilon],
            ],
            holes: vec![],
        },
        units,
        RigidTransform::default(),
    )?;
    let mut report = StripReport {
        valid: false,
        instance: source.name,
        backend: BACKEND,
        units,
        strip_width: width,
        expected_parts: expected,
        placed_parts: placed.len(),
        maximum_overlap_ratio: 0.0,
        maximum_outside_ratio: 0.0,
        violations: vec![],
    };
    let by_id: BTreeMap<_, _> = source.items.iter().map(|i| (i.id, i)).collect();
    let mut counts = BTreeMap::<u64, u64>::new();
    let mut shapes = vec![];
    for (index, part) in placed.iter().enumerate() {
        *counts.entry(part.item_id).or_default() += 1;
        let Some(item) = by_id.get(&part.item_id) else {
            report
                .violations
                .push(format!("placement {index}: unknown item {}", part.item_id));
            continue;
        };
        let degrees = part.transformation.rotation.to_degrees().rem_euclid(360.0);
        if let Some(angles) = &item.allowed_orientations {
            // Historical jagua-rs treats an empty list as no rotation; null is free.
            let permitted = if angles.is_empty() {
                degrees.min(360.0 - degrees) <= 0.00001
            } else {
                angles
                    .iter()
                    .any(|a| ((degrees - a + 180.0).rem_euclid(360.0) - 180.0).abs() <= 0.00001)
            };
            if !permitted {
                report.violations.push(format!(
                    "placement {index}: rotation {degrees} is not allowed"
                ));
            }
        }
        let Shape::SimplePolygon(ref points) = item.shape;
        let shape = Footprint::new(
            &Polygon {
                outer: points.clone(),
                holes: vec![],
            },
            units,
            RigidTransform {
                translation: part.transformation.translation,
                rotation_radians: part.transformation.rotation,
                mirrored: false,
            },
        );
        match shape {
            Ok(shape) => {
                let containment = shape.inside(&container, 0.0)?;
                report.maximum_outside_ratio =
                    report.maximum_outside_ratio.max(containment.outside_ratio);
                if containment.outside_area > 0.0 {
                    report.violations.push(format!(
                        "placement {index}: outside strip (area {})",
                        containment.outside_area
                    ));
                }
                shapes.push((index, shape));
            }
            Err(error) => report
                .violations
                .push(format!("placement {index}: {error:#}")),
        }
    }
    for item in &source.items {
        let actual = counts.get(&item.id).copied().unwrap_or(0);
        if actual != item.demand {
            report.violations.push(format!(
                "item {}: expected {}, found {actual}",
                item.id, item.demand
            ));
        }
    }
    for (i, (index, shape)) in shapes.iter().enumerate() {
        for (other_index, other) in shapes.iter().skip(i + 1) {
            let comparison = shape.compare(other, 0.0)?;
            report.maximum_overlap_ratio =
                report.maximum_overlap_ratio.max(comparison.overlap_ratio);
            if comparison.overlap_ratio > 1e-6 {
                report.violations.push(format!(
                    "placements {index} and {other_index}: overlap ratio {} exceeds 1e-6",
                    comparison.overlap_ratio
                ));
            }
        }
    }
    report.valid = report.violations.is_empty();
    Ok(report)
}
