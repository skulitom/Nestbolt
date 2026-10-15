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

mod cutting;
mod lightburn;
pub use cutting::{CuttingReport, PreparedRequest};
mod sheet;
pub use lightburn::{ExportFile, LightBurnProject};
pub use sheet::{SheetImport, SheetOutline};

/// Imported parts in millimetres, with the tolerance of their polygons.
#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Library {
    pub version: u32,
    /// Maximum distance between each exact curve and its polygon, in mm.
    pub tolerance: f64,
    pub parts: Vec<LibraryPart>,
    pub warnings: Vec<String>,
    #[serde(default)]
    pub imports: Vec<FileImportReport>,
    /// Stock outlines are separate from cutting parts and never nested as parts
    /// merely because they were discovered on a SHEET layer.
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub sheet_outlines: Vec<SheetOutline>,
    /// Original editable project, used for preserving LightBurn exports.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub lightburn: Option<LightBurnProject>,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct FileImportReport {
    pub file: String,
    pub report: crate::import::ImportReport,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct LibraryPart {
    pub id: String,
    /// Source file and element, layer or block.
    pub source: String,
    pub outer: Contour,
    pub holes: Vec<Contour>,
    pub polygon: nestbolt_validator::Polygon,
    /// All collision components of a rigid unit. Empty for legacy single-part
    /// libraries, whose geometry is the polygon field above.
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub components: Vec<nestbolt_validator::Polygon>,
    pub area_mm2: f64,
    pub bounds_mm: [f64; 4],
}

impl Library {
    /// Import SVG and DXF files; part ids are `<file stem>-<n>`.
    pub fn import(files: &[(String, String)], options: &ImportOptions) -> Result<Self> {
        Self::read(files, options, true)
    }

    fn read(
        files: &[(String, String)],
        options: &ImportOptions,
        discover_sheets: bool,
    ) -> Result<Self> {
        if files.iter().any(|(name, _)| lightburn::is_project(name)) {
            ensure!(
                files.len() == 1,
                "open one LightBurn project at a time; its layer settings cannot be combined with another drawing"
            );
            return Self::import_lightburn(&files[0].0, &files[0].1, options);
        }
        let mut parts = vec![];
        let mut warnings = vec![];
        let mut imports = vec![];
        let mut sheet_outlines = vec![];
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
            // Low-level imports retain partial geometry for inspection. A
            // nesting library must not silently omit selected cutting paths.
            if !import.report.open_contours.is_empty() {
                let details = import.report.open_contours.iter().take(4).map(|path| {
                    let fix = path.suggested_close_gaps_mm.map_or_else(
                        || "join these endpoints in the source drawing (automatic repair is limited to 1 mm)".to_owned(),
                        |limit| format!("enable Close gaps up to {limit:.6} mm"),
                    );
                    format!("{}: open path from ({:.6}, {:.6}) to ({:.6}, {:.6}); end gap {:.6} mm; {fix}",
                        path.source, path.start_mm[0], path.start_mm[1], path.end_mm[0], path.end_mm[1], path.end_gap_mm)
                }).collect::<Vec<_>>().join("; ");
                anyhow::bail!(
                    "cannot import {name}: {} selected contour(s) remain open; no partial library was created. {details}. If these are score or construction paths, exclude their layer/colour and import again",
                    import.report.open_contours.len()
                );
            }
            let stem = std::path::Path::new(name)
                .file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("part")
                .to_owned();
            if discover_sheets {
                let layers = options.sheet_layers.clone().unwrap_or_else(|| {
                    import
                        .report
                        .layers
                        .iter()
                        .filter(|l| l.name.eq_ignore_ascii_case("SHEET") && l.geometry_entities > 0)
                        .map(|l| l.name.clone())
                        .collect()
                });
                if !layers.is_empty() {
                    let selected = ImportOptions {
                        layers: Some(layers),
                        colors: None,
                        sheet_layers: None,
                        ..options.clone()
                    };
                    match SheetImport::read(name, text, &selected) {
                        Ok(sheets) => {
                            warnings.push(format!("{name}: sheet_outline_available: {} stock outline(s) can be used as sheets; cut selection is unchanged", sheets.outlines.len()));
                            sheet_outlines.extend(sheets.outlines);
                        }
                        Err(error) if options.sheet_layers.is_some() => return Err(error),
                        Err(error) => warnings.push(format!(
                            "{name}: SHEET outline could not be used as stock: {error:#}"
                        )),
                    }
                }
            }
            warnings.extend(import.warnings.into_iter().map(|w| format!("{name}: {w}")));
            imports.push(FileImportReport {
                file: name.clone(),
                report: import.report,
            });
            for (i, p) in import.parts.into_iter().enumerate() {
                parts.push(LibraryPart {
                    id: format!("{stem}-{}", i + 1),
                    source: format!("{name}#{}", p.source),
                    outer: p.outer,
                    holes: p.holes,
                    polygon: p.polygon,
                    components: vec![],
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
            imports,
            sheet_outlines,
            lightburn: None,
        })
    }
}

impl LibraryPart {
    pub fn geometry(&self) -> &[nestbolt_validator::Polygon] {
        if self.components.is_empty() {
            std::slice::from_ref(&self.polygon)
        } else {
            &self.components
        }
    }

    pub fn hole_count(&self) -> usize {
        self.geometry().iter().map(|p| p.holes.len()).sum()
    }
}

/// The `report.json` written beside `job.json` and `layout.json` by the CLI and
/// the MCP server's `nest`.
#[derive(Debug, Serialize, JsonSchema)]
pub struct NestReport {
    pub version: u32,
    pub algorithm: String,
    pub seed: u64,
    pub time_budget_s: f64,
    pub elapsed_s: f64,
    /// Whether the same inputs and seed reproduce this layout exactly: true
    /// only for a deterministic work budget that finished before the real-time
    /// limit.
    pub repeatable: bool,
    pub work_version: String,
    /// Copies placed inside the holes of other parts.
    pub parts_in_holes: u32,
    /// Why the fixed-sheet search did not apply; the general search ran instead.
    pub unsupported: Option<String>,
    /// Exported sheets, relative to the report's directory.
    pub files: Vec<String>,
    pub validation: nestbolt_validator::job::Report,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub common_line: Option<Vec<crate::common_line::Report>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub lead_in: Option<crate::lead_in::LayoutPlan>,
}

impl NestReport {
    pub fn new(result: crate::sheets::SheetResult, time_budget_s: f64, files: Vec<String>) -> Self {
        Self {
            version: 1,
            algorithm: result.algorithm.to_owned(),
            seed: result.seed,
            time_budget_s,
            elapsed_s: result.elapsed_seconds,
            repeatable: result.repeatable,
            work_version: crate::clock::WORK_VERSION.to_owned(),
            parts_in_holes: result.riders,
            unsupported: result.unsupported,
            files,
            validation: result.validation,
            common_line: None,
            lead_in: None,
        }
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
    /// An imported stock-outline id from Library.sheet_outlines. Omit dimensions
    /// to use its measured size, or supply those same dimensions explicitly.
    #[serde(default)]
    pub from_import: Option<String>,
    #[serde(default)]
    pub width_mm: f64,
    #[serde(default)]
    pub height_mm: f64,
    /// Available sheets of this size; absent means unlimited.
    pub count: Option<u32>,
    #[serde(default)]
    pub margins_mm: Margins,
    /// Areas that must stay clear (knots, damage, clamps), in sheet coordinates.
    #[serde(default)]
    pub defects_mm: Vec<nestbolt_validator::Polygon>,
    /// A remnant's usable outline inside its width × height; empty means the
    /// whole rectangle.
    #[serde(default)]
    pub outline_mm: Vec<nestbolt_validator::Polygon>,
    /// Curve-to-polygon error of an imported stock outline. Edge clearance is
    /// increased by this error as well as the part-library curve tolerance.
    #[serde(default)]
    pub outline_tolerance_mm: f64,
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
    /// Optional compensated common-line cutting. Its kerf replaces part spacing.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub common_line: Option<crate::common_line::Options>,
    /// Reserve cutting leads, choose contour starts and export LEADIN for review.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub lead_in: Option<crate::lead_in::Options>,
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
    pub fn common_line_reports(
        &self,
        library: &Library,
        layout: &nestbolt_validator::job::Layout,
    ) -> Result<Option<Vec<crate::common_line::Report>>> {
        self.common_line
            .map(|options| {
                let (job, curves) = self.job(library)?;
                crate::common_line::analyze(&job, layout, &curves, options)
            })
            .transpose()
    }

    /// Derive the polygon job and the exact outlines for export. Clearances
    /// grow by the library tolerance so the true curves keep the requested gaps.
    pub fn job(&self, library: &Library) -> Result<(Job, HashMap<String, Outline>)> {
        if let Some(options) = self.lead_in {
            options.validate()?;
            if let Some(common) = self.common_line {
                ensure!(
                    (common.kerf_mm - options.kerf_mm).abs() < 1e-9,
                    "common-line and lead allowances must use the same kerf"
                );
            }
        }
        if let Some(options) = self.common_line {
            options.validate()?;
            ensure!(
                library.lightburn.is_none(),
                "common-line toolpaths use SVG/DXF cutting outlines; export the cuts from LightBurn as SVG/DXF and import them here. Editable project exports retain their original layers and settings"
            );
        }
        ensure!(!self.sheets.is_empty(), "add at least one sheet size");
        ensure!(
            self.spacing_mm >= 0.0 && self.edge_spacing_mm >= 0.0,
            "spacing must be zero or positive"
        );
        let by_id: HashMap<&str, &LibraryPart> =
            library.parts.iter().map(|p| (p.id.as_str(), p)).collect();
        // Original project XML is authoritative for both solver geometry and
        // preserving exports, even when a library JSON has been edited.
        let lightburn_geometry = library.lightburn_geometry()?;
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
                geometry: match &lightburn_geometry {
                    Some(geometry) => geometry
                        .get(&w.id)
                        .context("unknown LightBurn unit; re-import the project")?
                        .clone(),
                    None => p.geometry().to_vec(),
                },
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
        let mut stock_tolerance = 0.0_f64;
        let stocks = self
            .sheets
            .iter()
            .enumerate()
            .map(|(i, s)| {
                let (width, height, outline, tolerance) = if let Some(id) = &s.from_import {
                    let imported = library.sheet_outlines.iter().find(|p| &p.id == id)
                        .with_context(|| format!("unknown sheet outline {id:?}; use an id from the library's sheet_outlines"))?;
                    ensure!(s.outline_mm.is_empty() && s.outline_tolerance_mm == 0.0,
                        "sheet {id}: use from_import or an explicit outline, not both");
                    ensure!((s.width_mm == 0.0 || s.width_mm == imported.width_mm)
                        && (s.height_mm == 0.0 || s.height_mm == imported.height_mm),
                        "sheet {id}: omit width_mm/height_mm or use the imported dimensions; imported outlines are not rescaled");
                    (imported.width_mm, imported.height_mm, imported.outline_mm.clone(), imported.tolerance_mm)
                } else {
                    (s.width_mm, s.height_mm, s.outline_mm.clone(), s.outline_tolerance_mm)
                };
                ensure!(tolerance.is_finite() && (0.0..=1.0).contains(&tolerance),
                    "sheet outline tolerance must be between 0 and 1 mm");
                stock_tolerance = stock_tolerance.max(tolerance);
                Ok(Stock {
                id: s
                    .id
                    .clone()
                    .unwrap_or_else(|| format!("sheet-type-{}", i + 1)),
                width,
                height,
                count: s.count,
                margins: s.margins_mm,
                outline,
                defects: s.defects_mm.clone(),
            })})
            .collect::<Result<Vec<_>>>()?;
        // Straight source segments have no flattening error. In common mode
        // they can meet at exactly one kerf, without a fictitious curve guard.
        // Curved drawings retain the original conservative error allowance.
        let tolerance = if self.common_line.is_some()
            && outlines.values().all(|o| {
                std::iter::once(&o.outer).chain(&o.holes).all(|c| {
                    c.segments
                        .iter()
                        .all(|s| matches!(s, crate::curves::Segment::Line { .. }))
                })
            }) {
            0.0
        } else {
            library.tolerance
        };
        Ok((
            Job {
                version: 1,
                name: self.name.clone().unwrap_or_else(|| "nestbolt job".into()),
                units: Units::Mm,
                parts,
                stocks,
                clearance: self.common_line.map_or(self.spacing_mm, |o| o.kerf_mm)
                    + 2.0 * tolerance,
                edge_clearance: self.edge_spacing_mm + tolerance + stock_tolerance,
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
