//! Read-only N2 diagnostic; never alters the source project or renders fonts.
use anyhow::{Context, Result};
use nestbolt_core::lightburn::Document;

fn main() -> Result<()> {
    let file = std::env::args()
        .nth(1)
        .context("pass a .lbrn/.lbrn2 file")?;
    let source = std::fs::read_to_string(&file)?;
    let document = Document::read(&source, 0.0005)?;
    println!(
        "{}",
        serde_json::to_string(
            &serde_json::json!({"scene":document.scene,"noop_byte_identical":document.original_xml()==source})
        )?
    );
    Ok(())
}
