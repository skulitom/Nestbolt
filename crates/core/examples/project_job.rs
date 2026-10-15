//! Emit the exact polygon job used by a public library/request pair.
//! Diagnostic only: preserves all components and curve-clearance allowances.
use anyhow::{Context, Result};
use nestbolt_core::project::{Library, Request};

fn main() -> Result<()> {
    let mut args = std::env::args().skip(1);
    let library: Library = serde_json::from_slice(&std::fs::read(
        args.next().context("pass library.json and request.json")?,
    )?)?;
    let request: Request = serde_json::from_slice(&std::fs::read(
        args.next().context("pass library.json and request.json")?,
    )?)?;
    let (job, _) = request.job(&library)?;
    println!("{}", serde_json::to_string_pretty(&job)?);
    Ok(())
}
