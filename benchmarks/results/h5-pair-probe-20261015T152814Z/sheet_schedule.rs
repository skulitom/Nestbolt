//! Development-only schedule probe. Uses the existing public solver with holes
//! reserved; it does not change product defaults or enable the cutting bonus.
use std::{fs, path::PathBuf};

use anyhow::{Context, Result, ensure};
use nestbolt_core::sheets;
use nestbolt_validator::job::Job;

fn main() -> Result<()> {
    let args: Vec<_> = std::env::args().collect();
    ensure!(
        args.len() == 8,
        "usage: sheet_schedule JOB OUT_DIR SECONDS SEED WARM_FRACTION COMPRESS_FRACTION WINDOW"
    );
    let job: Job = serde_json::from_slice(&fs::read(&args[1])?)?;
    let out = PathBuf::from(&args[2]);
    ensure!(!out.exists(), "output directory already exists");
    let warm_fraction: f64 = args[5].parse()?;
    let compress_fraction: f64 = args[6].parse()?;
    ensure!(
        warm_fraction.is_finite() && (0.0..1.0).contains(&warm_fraction),
        "warm fraction must be in [0, 1)"
    );
    ensure!(
        compress_fraction.is_finite() && (0.0..=1.0).contains(&compress_fraction),
        "compression fraction must be in [0, 1]"
    );
    let result = sheets::optimize_with_part_in_hole(
        &job,
        sheets::Options {
            seconds: args[3].parse()?,
            seed: args[4].parse()?,
            warm_fraction,
            compress_fraction,
            window: args[7].parse()?,
            ..Default::default()
        },
        false,
        |_, _| {},
    )?;
    ensure!(result.validation.valid, "invalid diagnostic layout");
    fs::create_dir(&out).context("create diagnostic output")?;
    fs::write(out.join("result.json"), serde_json::to_vec_pretty(&result)?)?;
    fs::write(
        out.join("layout.json"),
        serde_json::to_vec_pretty(&result.layout)?,
    )?;
    Ok(())
}
