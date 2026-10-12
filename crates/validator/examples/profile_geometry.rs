//! Development-only stage timings over an existing original job and layout.
use anyhow::{Context, Result};
use nestbolt_validator::{
    Footprint, RigidTransform,
    job::{Job, Layout, validate},
};
use serde_json::json;
use std::{fs, time::Instant};

fn main() -> Result<()> {
    let mut args = std::env::args().skip(1);
    let job: Job = serde_json::from_slice(&fs::read(args.next().context("job path")?)?)?;
    let layout: Layout = serde_json::from_slice(&fs::read(args.next().context("layout path")?)?)?;
    let start = Instant::now();
    let mut source_area = 0.0;
    for part in &job.parts {
        source_area +=
            Footprint::from_polygons(&part.geometry, job.units, RigidTransform::default())?.area();
    }
    let source_seconds = start.elapsed().as_secs_f64();
    let start = Instant::now();
    let shapes: Vec<_> = layout
        .placements
        .iter()
        .map(|placement| {
            let part = job
                .parts
                .iter()
                .find(|p| p.id == placement.part_id)
                .context("part")?;
            Footprint::from_polygons(&part.geometry, job.units, placement.transform)
        })
        .collect::<Result<_>>()?;
    let transformed_seconds = start.elapsed().as_secs_f64();
    let start = Instant::now();
    let mut overlap = 0.0;
    for (i, shape) in shapes.iter().enumerate() {
        for (j, other) in shapes.iter().enumerate().skip(i + 1) {
            if layout.placements[i].sheet_id == layout.placements[j].sheet_id {
                overlap += shape.compare(other, job.clearance)?.overlap_area;
            }
        }
    }
    let pairs_seconds = start.elapsed().as_secs_f64();
    let start = Instant::now();
    let report = validate(&job, &layout)?;
    println!(
        "{}",
        json!({"job":job.name,"source_seconds":source_seconds,
        "transformed_seconds":transformed_seconds,"pairs_seconds":pairs_seconds,
        "full_validation_seconds":start.elapsed().as_secs_f64(),"source_area":source_area,
        "total_overlap":overlap,"report":report})
    );
    Ok(())
}
