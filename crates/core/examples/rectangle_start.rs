//! Development probe of the existing rectangle packer as an early incumbent.
//! No product search/defaults change. Validate expanded original geometry.
use std::{fs, path::PathBuf, time::Instant};

use anyhow::{Context, Result, ensure};
use nestbolt_core::{
    clock::{Clock, Timing},
    holes,
    project::{Library, Request},
    rects, sheets,
};
use nestbolt_validator::job::validate;
use serde_json::json;

fn main() -> Result<()> {
    let args: Vec<_> = std::env::args().collect();
    ensure!(
        args.len() == 8,
        "usage: rectangle_start LIBRARY REQUEST OUT SECONDS SEED HOLES RECT_SHARE"
    );
    let started = Instant::now();
    let library: Library = serde_json::from_slice(&fs::read(&args[1])?)?;
    let request: Request = serde_json::from_slice(&fs::read(&args[2])?)?;
    ensure!(
        request.common_line.is_none() && request.lead_in.is_none(),
        "this probe accepts ordinary cutting jobs only"
    );
    let out = PathBuf::from(&args[3]);
    ensure!(!out.exists(), "output directory already exists");
    let seconds: f64 = args[4].parse()?;
    let seed: u64 = args[5].parse()?;
    let allow_holes: bool = args[6].parse()?;
    let share: f64 = args[7].parse()?;
    ensure!(seconds > 0.0 && seconds <= 300.0, "invalid seconds");
    ensure!(share > 0.0 && share <= 1.0, "invalid rectangle share");
    let (job, _) = request.job(&library)?;
    let prepared_seconds = started.elapsed().as_secs_f64();
    let clock = Clock::new(Timing::Wall, seconds);
    let grouped = allow_holes
        .then(|| holes::group(&job, &clock, seconds * sheets::HOLE_SHARE, seed))
        .transpose()?;
    let grouped_seconds = started.elapsed().as_secs_f64();
    let operations = (seconds * share * sheets::RECT_OPERATIONS_PER_SECOND) as u64;
    let (layout, used) =
        rects::pack(grouped.as_ref().map_or(&job, |g| &g.job), seed, operations)
            .context("no rectangle incumbent within the operation budget and stock constraints")?;
    let packed_seconds = started.elapsed().as_secs_f64();
    let layout = match &grouped {
        Some(grouped) => grouped.expand(&job, &layout)?,
        None => layout,
    };
    let expanded_seconds = started.elapsed().as_secs_f64();
    let report = validate(&job, &layout)?;
    ensure!(
        report.valid,
        "original geometry failed: {:?}",
        report.violations
    );
    let result = json!({
        "scope":"Existing rectangle packer only; not a complete solver or H4 gate",
        "seconds":seconds,"seed":seed,"holes":allow_holes,"rectangle_share":share,
        "operation_limit":operations,"operations_used":used,
        "riders":grouped.as_ref().map_or(0, |g| g.riders_placed),
        "prepared_seconds":prepared_seconds,
        "grouping_seconds":grouped_seconds-prepared_seconds,
        "packing_seconds":packed_seconds-grouped_seconds,
        "expansion_seconds":expanded_seconds-packed_seconds,
        "validation_seconds":started.elapsed().as_secs_f64()-expanded_seconds,
        "total_seconds":started.elapsed().as_secs_f64(),"validation":report
    });
    fs::create_dir(&out)?;
    for (name, value) in [("result.json", result), ("layout.json", json!(layout))] {
        fs::write(out.join(name), serde_json::to_vec_pretty(&value)?)?;
    }
    Ok(())
}
