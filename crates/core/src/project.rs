//! The user-facing job description shared by the CLI, MCP server and browser:
//! a library of imported parts with exact curves, and a request naming the
//! parts, quantities, sheets and spacing. Polygon jobs for the solver and the
//! independent checker are derived from it; exports use the exact curves.
use std::collections::HashMap;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::{
    Units,
    job::{Job, Margins, Mode, Part, Rotations, Stock},
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::curves::Contour;
use crate::export::Outline;
use crate::import::{Import, Options as ImportOptions, import_dxf, import_svg};

/// Imported parts in millimetres, with the tolerance of their polygons.
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Library {
    pub version: u32,
    /// Maximum distance between each exact curve and its polygon, in mm.
    pub tolerance: f64,
    pub parts: Vec<LibraryPart>,
    pub warnings: Vec<String>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LibraryPart {
    pub id: String,
    /// Source file and element, layer or block.
    pub source: String,
    pub outer: Contour,
    pub holes: Vec<Contour>,
    pub polygon: nestbolt_validator::Polygon,
    pub area_mm2: f64,
    pub bounds_mm: [f64; 4],
}

impl Library {
    /// Import SVG and DXF files; part ids are `<file stem>-<n>`.
    pub fn import(files: &[(String, String)], options: &ImportOptions) -> Result<Self> {
        let mut parts = vec![];
        let mut warnings = vec![];
        for (name, text) in files {
            let lower = name.to_ascii_lowercase();
            let import: Import = if lower.ends_with(".svg") {
                import_svg(text, options)
            } else if lower.ends_with(".dxf") {
                import_dxf(text, options)
            } else {
                anyhow::bail!("{name}: only .svg and .dxf files can be imported")
            }
            .with_context(|| format!("cannot import {name}"))?;
            let stem = std::path::Path::new(name)
                .file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("part")
                .to_owned();
            warnings.extend(import.warnings.into_iter().map(|w| format!("{name}: {w}")));
            for (i, p) in import.parts.into_iter().enumerate() {
                parts.push(LibraryPart {
                    id: format!("{stem}-{}", i + 1),
                    source: format!("{name}#{}", p.source),
                    outer: p.outer,
                    holes: p.holes,
                    polygon: p.polygon,
                    area_mm2: p.area,
                    bounds_mm: p.bounds,
                });
            }
        }
        let mut seen = std::collections::HashSet::new();
        ensure!(
            parts.iter().all(|p| seen.insert(p.id.clone())),
            "two imported files share a name; rename one so part ids are unique"
        );
        Ok(Self {
            version: 1,
            tolerance: options.tolerance,
            parts,
            warnings,
        })
    }
}

fn default_quantity() -> u32 {
    1
}

fn default_rotations() -> Rotations {
    Rotations::List {
        degrees: vec![0.0, 90.0, 180.0, 270.0],
    }
}

fn default_priority() -> f64 {
    1.0
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct RequestPart {
    /// A library part id.
    pub id: String,
    #[serde(default = "default_quantity")]
    pub quantity: u32,
    #[serde(default = "default_rotations")]
    pub rotations: Rotations,
    #[serde(default)]
    pub allow_mirror: bool,
    #[serde(default = "default_priority")]
    pub priority: f64,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct RequestSheet {
    pub id: Option<String>,
    pub width_mm: f64,
    pub height_mm: f64,
    /// Available sheets of this size; absent means unlimited.
    pub count: Option<u32>,
    #[serde(default)]
    pub margins_mm: Margins,
}

/// What to nest. Lengths are millimetres.
#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Request {
    pub name: Option<String>,
    /// Parts to place; all library parts with default settings when empty.
    #[serde(default)]
    pub parts: Vec<RequestPart>,
    pub sheets: Vec<RequestSheet>,
    /// Minimum gap between parts (kerf plus margin).
    #[serde(default)]
    pub spacing_mm: f64,
    /// Minimum gap between parts and the sheet edge or a defect.
    #[serde(default)]
    pub edge_spacing_mm: f64,
    #[serde(default = "default_mode")]
    pub mode: Mode,
}

fn default_mode() -> Mode {
    Mode::All
}

impl Request {
    /// Derive the polygon job and the exact outlines for export. Clearances
    /// grow by the library tolerance so the true curves keep the requested gaps.
    pub fn job(&self, library: &Library) -> Result<(Job, HashMap<String, Outline>)> {
        ensure!(!self.sheets.is_empty(), "add at least one sheet size");
        ensure!(
            self.spacing_mm >= 0.0 && self.edge_spacing_mm >= 0.0,
            "spacing must be zero or positive"
        );
        let by_id: HashMap<&str, &LibraryPart> =
            library.parts.iter().map(|p| (p.id.as_str(), p)).collect();
        let wanted: Vec<RequestPart> = if self.parts.is_empty() {
            library
                .parts
                .iter()
                .map(|p| RequestPart {
                    id: p.id.clone(),
                    quantity: 1,
                    rotations: default_rotations(),
                    allow_mirror: false,
                    priority: 1.0,
                })
                .collect()
        } else {
            self.parts.clone()
        };
        let mut parts = vec![];
        let mut outlines = HashMap::new();
        for w in &wanted {
            let p = by_id.get(w.id.as_str()).with_context(|| {
                format!(
                    "unknown part id {:?}; use one returned by import_parts",
                    w.id
                )
            })?;
            ensure!(
                w.quantity >= 1,
                "part {} needs a quantity of at least 1",
                w.id
            );
            parts.push(Part {
                id: w.id.clone(),
                quantity: w.quantity,
                geometry: vec![p.polygon.clone()],
                rotations: w.rotations.clone(),
                allow_mirror: w.allow_mirror,
                priority: w.priority,
            });
            outlines.insert(
                w.id.clone(),
                Outline {
                    outer: p.outer.clone(),
                    holes: p.holes.clone(),
                },
            );
        }
        let stocks = self
            .sheets
            .iter()
            .enumerate()
            .map(|(i, s)| Stock {
                id: s
                    .id
                    .clone()
                    .unwrap_or_else(|| format!("sheet-type-{}", i + 1)),
                width: s.width_mm,
                height: s.height_mm,
                count: s.count,
                margins: s.margins_mm,
                outline: vec![],
                defects: vec![],
            })
            .collect();
        let tolerance = library.tolerance;
        Ok((
            Job {
                version: 1,
                name: self.name.clone().unwrap_or_else(|| "nestbolt job".into()),
                units: Units::Mm,
                parts,
                stocks,
                clearance: self.spacing_mm + 2.0 * tolerance,
                edge_clearance: self.edge_spacing_mm + tolerance,
                mode: self.mode,
            },
            outlines,
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn request_builds_a_checked_job_with_widened_clearances() {
        let svg = r#"<svg xmlns="http://www.w3.org/2000/svg" width="40mm" height="20mm" viewBox="0 0 40 20">
            <rect x="0" y="0" width="10" height="10"/><circle cx="30" cy="10" r="5"/></svg>"#;
        let library = Library::import(
            &[("tabs.svg".into(), svg.into())],
            &ImportOptions::default(),
        )
        .unwrap();
        assert_eq!(library.parts.len(), 2);
        let request: Request = serde_json::from_value(serde_json::json!({
            "parts": [{"id": "tabs-1", "quantity": 3}, {"id": "tabs-2", "rotations": {"kind": "free"}}],
            "sheets": [{"width_mm": 100, "height_mm": 50, "margins_mm": {"left": 2, "right": 2, "bottom": 2, "top": 2}}],
            "spacing_mm": 1.0
        }))
        .unwrap();
        let (job, outlines) = request.job(&library).unwrap();
        assert_eq!(job.parts[0].quantity, 3);
        assert!((job.clearance - 1.01).abs() < 1e-12);
        assert_eq!(outlines.len(), 2);
        let empty = nestbolt_validator::job::Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![],
            placements: vec![],
        };
        // Only missing copies are reported for an empty layout.
        let report = nestbolt_validator::job::validate(&job, &empty).unwrap();
        assert!(report.violations.iter().all(|v| v.code == "quantity"));
        let bad: Request = serde_json::from_value(serde_json::json!({
            "parts": [{"id": "nope"}], "sheets": [{"width_mm": 1, "height_mm": 1}]}))
        .unwrap();
        assert!(
            bad.job(&library)
                .unwrap_err()
                .to_string()
                .contains("unknown part id")
        );
    }
}
