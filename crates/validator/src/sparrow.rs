//! Strip-output adapter. Always reads original polygons from a separate input.
use std::collections::BTreeMap;

use anyhow::{Context, Result, ensure};
use serde::{Deserialize, Serialize};

use crate::{Polygon, RigidTransform, Units, job};

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
    pub maximum_total_overlap_ratio: f64,
    pub violations: Vec<String>,
}

/// Convert a historical strip result to the same independent contract used for
/// sheet jobs. Source geometry always comes from the separate original file.
pub fn to_job(input: &str, output: &str, units: Units) -> Result<(job::Job, job::Layout)> {
    let source: Instance = serde_json::from_str(input).context("invalid original Sparrow input")?;
    let output: Output = serde_json::from_str(output).context("invalid Sparrow solution JSON")?;
    ensure!(
        source.items.len() <= 2000 && output.solution.layout.placed_items.len() <= 2000,
        "strip job/layout exceeds 2000 parts"
    );
    let mut parts = vec![];
    for item in source.items {
        let Shape::SimplePolygon(points) = item.shape;
        let rotations = match item.allowed_orientations {
            None => job::Rotations::Free,
            Some(angles) if angles.is_empty() => job::Rotations::List { degrees: vec![0.0] },
            Some(angles) => job::Rotations::List { degrees: angles },
        };
        parts.push(job::Part {
            id: item.id.to_string(),
            quantity: u32::try_from(item.demand).context("quantity exceeds u32")?,
            geometry: vec![Polygon {
                outer: points,
                holes: vec![],
            }],
            rotations,
            allow_mirror: false,
            priority: 1.0,
        });
    }
    let job = job::Job {
        version: 1,
        name: source.name,
        units,
        parts,
        stocks: vec![job::Stock {
            id: "strip".into(),
            width: output.solution.strip_width,
            height: source.strip_height,
            count: Some(1),
            margins: job::Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
        clearance: 0.0,
        edge_clearance: 0.0,
        mode: job::Mode::All,
    };
    let mut counts = BTreeMap::<u64, u32>::new();
    let placements = output
        .solution
        .layout
        .placed_items
        .into_iter()
        .map(|p| {
            let counter = counts.entry(p.item_id).or_default();
            let copy_index = *counter;
            *counter += 1;
            job::Placement {
                part_id: p.item_id.to_string(),
                copy_index,
                sheet_id: "strip-0".into(),
                transform: RigidTransform {
                    translation: p.transformation.translation,
                    rotation_radians: p.transformation.rotation,
                    mirrored: false,
                },
            }
        })
        .collect();
    let layout = job::Layout {
        version: 1,
        units,
        sheets: vec![job::Sheet {
            id: "strip-0".into(),
            stock_id: "strip".into(),
        }],
        placements,
    };
    Ok((job, layout))
}

/// Validate through the common job validator; strip scoring remains strip width.
pub fn validate(input: &str, output: &str, units: Units) -> Result<StripReport> {
    let (job, layout) = to_job(input, output, units)?;
    let report = job::validate(&job, &layout)?;
    Ok(StripReport {
        valid: report.valid,
        instance: job.name,
        backend: report.backend,
        units,
        strip_width: job.stocks[0].width,
        expected_parts: job.parts.iter().map(|p| u64::from(p.quantity)).sum(),
        placed_parts: layout.placements.len(),
        maximum_overlap_ratio: report.maximum_overlap_ratio,
        maximum_outside_ratio: report.maximum_outside_ratio,
        maximum_total_overlap_ratio: report.maximum_total_overlap_ratio,
        violations: report
            .violations
            .into_iter()
            .map(|v| format!("{}: {}", v.code, v.message))
            .collect(),
    })
}
