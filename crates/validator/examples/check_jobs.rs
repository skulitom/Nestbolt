//! Dataset authoring check: validates source contracts without claiming a layout.
use anyhow::{Context, Result, ensure};
use nestbolt_validator::job::{Job, Layout, validate};

fn main() -> Result<()> {
    let paths: Vec<_> = std::env::args().skip(1).collect();
    ensure!(!paths.is_empty(), "provide one or more benchmark job paths");
    for path in &paths {
        let job: Job = serde_json::from_str(&std::fs::read_to_string(path)?)
            .with_context(|| format!("invalid job JSON in {path}"))?;
        let report = validate(
            &job,
            &Layout {
                version: 1,
                units: job.units,
                sheets: vec![],
                placements: vec![],
            },
        )
        .with_context(|| format!("invalid source geometry or constraints in {path}"))?;
        ensure!(
            report.violations.iter().all(|v| v.code == "quantity"),
            "unexpected empty-layout report for {path}: {:?}",
            report.violations
        );
    }
    println!(
        "Checked {} job source contracts (no solve or feasible-layout claim).",
        paths.len()
    );
    Ok(())
}
