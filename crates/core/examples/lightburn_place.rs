//! Controlled placements for native writer probes, not a search interface.
use anyhow::{Context, Result};
use nestbolt_core::lightburn::{Document, UnitPlacement};
use serde::Deserialize;

#[derive(Deserialize)]
struct Request {
    width_mm: f64,
    height_mm: f64,
    outline: bool,
    placements: Vec<UnitPlacement>,
}

fn main() -> Result<()> {
    let mut args = std::env::args().skip(1);
    let file = args.next().context("provide a LightBurn project")?;
    let request = args.next().context("provide a placement JSON file")?;
    let source = std::fs::read_to_string(file)?;
    let request: Request = serde_json::from_str(&std::fs::read_to_string(request)?)?;
    let document = Document::read(&source, 0.0005)?;
    let nesting = document.nesting_units(0.0005)?;
    let xml = nesting.write_sheet(
        &request.placements,
        request.width_mm,
        request.height_mm,
        request.outline,
    )?;
    println!("{xml}");
    Ok(())
}
