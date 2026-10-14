//! Shared LightBurn import and preserving export for native and WASM surfaces.
use std::collections::{HashMap, HashSet};

use anyhow::{Context, Result, ensure};
use nestbolt_validator::{
    Polygon,
    job::{Job, Layout},
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::{ImportOptions, Library, LibraryPart, Request};
use crate::{
    export::Outline,
    lightburn::{Document, Layer, UnitPlacement},
};

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct LightBurnProject {
    pub file: String,
    /// Complete original XML, including editable text and embedded image data.
    pub xml: String,
    /// Unit index -> library part id. Requests choose quantities and rotations.
    pub unit_ids: Vec<String>,
    pub layers: Vec<Layer>,
    pub fixed_top_level: usize,
    pub mirror_x: bool,
    pub mirror_y: bool,
}

impl LightBurnProject {
    /// Bounded metadata for native tool replies; embedded XML stays in the library.
    pub fn summary(&self) -> serde_json::Value {
        serde_json::json!({"file":self.file,"unit_count":self.unit_ids.len(),
            "layers":self.layers.iter().take(200).collect::<Vec<_>>(),
            "layer_count":self.layers.len(),"layers_truncated":self.layers.len()>200,
            "fixed_top_level":self.fixed_top_level,
            "mirror_x":self.mirror_x,"mirror_y":self.mirror_y})
    }
}

#[derive(Debug)]
pub struct ExportFile {
    pub name: String,
    pub text: String,
}

pub(super) fn is_project(name: &str) -> bool {
    let name = name.to_ascii_lowercase();
    name.ends_with(".lbrn2") || name.ends_with(".lbrn")
}

fn check_fixed_groups(document: &Document) -> Result<()> {
    for &index in &document.scene.top_level {
        let root = &document.scene.shapes[index];
        if !root.fixed || root.kind != "Group" {
            continue;
        }
        let mut remaining = root.children.clone();
        while let Some(child) = remaining.pop() {
            let shape = &document.scene.shapes[child];
            ensure!(
                shape.kind == "Group" || shape.fixed,
                "LightBurn group {index} mixes output-enabled artwork with Tool/output-off shapes; ungroup it and group movable artwork separately before nesting. Fixed active artwork cannot yet be checked against every sheet"
            );
            remaining.extend(&shape.children);
        }
    }
    Ok(())
}

impl Library {
    /// Prepare every export before any surface writes files. An explicit format
    /// selects one; otherwise use the source format's preserving default.
    pub fn export_files(
        &self,
        request: &Request,
        layout: &Layout,
        format: Option<&str>,
        sheet_outline: Option<bool>,
    ) -> Result<Vec<ExportFile>> {
        let (job, outlines) = request.job(self)?;
        let formats = match (self.lightburn.is_some(), format) {
            (true, None | Some("lbrn2")) => vec!["lbrn2"],
            (true, _) => anyhow::bail!(
                "export this LightBurn project as lbrn2 to retain its text, images and layer settings"
            ),
            (false, None) => vec!["svg", "dxf"],
            (false, Some("svg")) => vec!["svg"],
            (false, Some("dxf")) => vec!["dxf"],
            (false, Some("lbrn2")) => {
                anyhow::bail!("lbrn2 export requires an imported LightBurn project")
            }
            _ => anyhow::bail!("format must be svg, dxf or lbrn2"),
        };
        let options = crate::export::Options {
            sheet_outline: sheet_outline.unwrap_or(self.lightburn.is_some()),
        };
        let common = request
            .common_line
            .map(|o| crate::common_line::analyze(&job, layout, &outlines, o))
            .transpose()?;
        let mut files = vec![];
        for sheet in &layout.sheets {
            let review = crate::export::ReviewPaths {
                common: common
                    .as_ref()
                    .and_then(|r| r.iter().find(|r| r.sheet_id == sheet.id))
                    .map_or_else(Vec::new, |r| r.paths.clone()),
                ..Default::default()
            };
            for format in &formats {
                let (name, text) = match *format {
                    "lbrn2" => (
                        self.lightburn_filename(layout, &sheet.id)?,
                        self.write_lightburn(&job, layout, &sheet.id, options.sheet_outline)?,
                    ),
                    "svg" => (
                        format!("{}.svg", sheet.id),
                        crate::export::svg_with_review_paths(
                            &job, layout, &sheet.id, &outlines, options, &review,
                        )?,
                    ),
                    "dxf" => (
                        format!("{}.dxf", sheet.id),
                        crate::export::dxf_with_review_paths(
                            &job, layout, &sheet.id, &outlines, options, &review,
                        )?,
                    ),
                    _ => unreachable!(),
                };
                ensure!(
                    !name.contains(['/', '\\']) && name != "." && name != "..",
                    "sheet id cannot contain a path separator"
                );
                files.push(ExportFile { name, text });
            }
        }
        Ok(files)
    }

    pub(super) fn import_lightburn(
        name: &str,
        text: &str,
        options: &ImportOptions,
    ) -> Result<Self> {
        ensure!(
            options.layers.is_none()
                && options.colors.is_none()
                && options.close_gaps_mm.is_none()
                && options.sheet_layers.is_none(),
            "LightBurn imports preserve project layers and geometry; clear the SVG/DXF layer, colour, gap and sheet-layer overrides"
        );
        let document = Document::read(text, options.tolerance)
            .with_context(|| format!("cannot import {name}"))?;
        check_fixed_groups(&document)?;
        let nesting = document.nesting_units(options.tolerance)?;
        ensure!(
            !nesting.units.is_empty(),
            "{name}: no movable nesting units; enable output for a cutting layer or choose a project with movable shapes"
        );
        let stem = std::path::Path::new(name)
            .file_stem()
            .and_then(|n| n.to_str())
            .unwrap_or("project");
        let mut parts = Vec::with_capacity(nesting.units.len());
        for unit in &nesting.units {
            let polygon = unit
                .geometry
                .first()
                .context("LightBurn unit has no collision outline")?
                .clone();
            let outline = Outline::from_polygon(&polygon);
            parts.push(LibraryPart {
                id: format!("{stem}-unit-{}", unit.id + 1),
                source: format!("{name}#unit-{}", unit.id + 1),
                // These display footprints do not replace the source curves.
                // LightBurn exports always use the retained original XML.
                outer: outline.outer,
                holes: outline.holes,
                polygon,
                components: unit.geometry.clone(),
                area_mm2: unit.area_mm2,
                bounds_mm: unit.bounds_mm,
            });
        }
        let mut warnings = document.scene.warnings.clone();
        warnings.extend(nesting.warnings.clone());
        if !nesting.fixed.is_empty() {
            warnings.push(format!("{} top-level Tool/output-off shapes stay at their original positions in every exported sheet", nesting.fixed.len()));
        }
        if document.scene.layers.iter().any(|l| l.kerf_mm != 0.0) {
            warnings.push("LightBurn layer kerf values are preserved and reported; spacing is not changed automatically".into());
        }
        Ok(Self {
            version: 1,
            tolerance: options.tolerance,
            lightburn: Some(LightBurnProject {
                file: name.into(),
                xml: text.into(),
                unit_ids: parts.iter().map(|p| p.id.clone()).collect(),
                layers: document.scene.layers.clone(),
                fixed_top_level: nesting.fixed.len(),
                mirror_x: document.scene.mirror_x,
                mirror_y: document.scene.mirror_y,
            }),
            parts,
            warnings,
            imports: vec![],
            sheet_outlines: vec![],
        })
    }

    pub(super) fn lightburn_geometry(&self) -> Result<Option<HashMap<String, Vec<Polygon>>>> {
        let Some(project) = &self.lightburn else {
            ensure!(
                self.parts.iter().all(|p| p.components.is_empty()),
                "multi-component library parts require their original LightBurn project; re-import the source file"
            );
            return Ok(None);
        };
        let document = Document::read(&project.xml, self.tolerance)?;
        check_fixed_groups(&document)?;
        let nesting = document.nesting_units(self.tolerance)?;
        let ids: HashSet<_> = project.unit_ids.iter().collect();
        ensure!(
            ids.len() == nesting.units.len()
                && project.unit_ids.len() == nesting.units.len()
                && self.parts.len() == nesting.units.len()
                && self
                    .parts
                    .iter()
                    .map(|p| &p.id)
                    .collect::<HashSet<_>>()
                    .len()
                    == ids.len()
                && self.parts.iter().all(|p| ids.contains(&p.id)),
            "LightBurn unit mapping differs from the source project; re-import it"
        );
        Ok(Some(
            nesting
                .units
                .into_iter()
                .map(|u| (project.unit_ids[u.id].clone(), u.geometry))
                .collect(),
        ))
    }

    /// Canonical filename, independent of stock ids or user-supplied paths.
    pub fn lightburn_filename(&self, layout: &Layout, sheet_id: &str) -> Result<String> {
        let project = self
            .lightburn
            .as_ref()
            .context("this library has no LightBurn project")?;
        let number = layout
            .sheets
            .iter()
            .position(|s| s.id == sheet_id)
            .context("unknown sheet")?
            + 1;
        let stem = std::path::Path::new(&project.file)
            .file_stem()
            .and_then(|n| n.to_str())
            .unwrap_or("project");
        let stem: String = stem
            .chars()
            .map(|c| {
                if c.is_ascii_alphanumeric() || c == '-' || c == '_' {
                    c
                } else {
                    '-'
                }
            })
            .collect();
        Ok(format!("{stem}-sheet-{number}.lbrn2"))
    }

    /// Export one independently valid sheet without discarding project content.
    /// None uses the format default: outline on for LightBurn, off for SVG/DXF.
    pub fn export_sheet(
        &self,
        request: &Request,
        layout: &Layout,
        sheet_id: &str,
        format: &str,
        sheet_outline: Option<bool>,
    ) -> Result<String> {
        let (job, outlines) = request.job(self)?;
        let options = crate::export::Options {
            sheet_outline: sheet_outline.unwrap_or(self.lightburn.is_some()),
        };
        let common = request
            .common_line
            .map(|o| crate::common_line::analyze(&job, layout, &outlines, o))
            .transpose()?;
        let review = crate::export::ReviewPaths {
            common: common
                .as_ref()
                .and_then(|r| r.iter().find(|r| r.sheet_id == sheet_id))
                .map_or_else(Vec::new, |r| r.paths.clone()),
            ..Default::default()
        };
        match (&self.lightburn, format) {
            (Some(_), "lbrn2") => {
                self.write_lightburn(&job, layout, sheet_id, options.sheet_outline)
            }
            (Some(_), _) => anyhow::bail!(
                "export this LightBurn project as lbrn2 to retain its text, images and layer settings"
            ),
            (None, "svg") => crate::export::svg_with_review_paths(
                &job, layout, sheet_id, &outlines, options, &review,
            ),
            (None, "dxf") => crate::export::dxf_with_review_paths(
                &job, layout, sheet_id, &outlines, options, &review,
            ),
            (None, "lbrn2") => anyhow::bail!("lbrn2 export requires an imported LightBurn project"),
            _ => anyhow::bail!("format must be svg, dxf or lbrn2"),
        }
    }

    fn write_lightburn(
        &self,
        job: &Job,
        layout: &Layout,
        sheet_id: &str,
        outline: bool,
    ) -> Result<String> {
        let report = nestbolt_validator::job::validate(job, layout)?;
        ensure!(
            report.valid,
            "layout failed independent validation: {:?}",
            report.violations
        );
        let project = self
            .lightburn
            .as_ref()
            .context("missing LightBurn source")?;
        let sheet = layout
            .sheets
            .iter()
            .find(|s| s.id == sheet_id)
            .context("unknown sheet")?;
        let stock = job
            .stocks
            .iter()
            .find(|s| s.id == sheet.stock_id)
            .context("unknown stock")?;
        let document = Document::read(&project.xml, self.tolerance)?;
        let nesting = document.nesting_units(self.tolerance)?;
        let mut placements = vec![];
        for p in layout.placements.iter().filter(|p| p.sheet_id == sheet_id) {
            let unit = project
                .unit_ids
                .iter()
                .position(|id| id == &p.part_id)
                .context("unknown LightBurn unit")?;
            placements.push(UnitPlacement {
                unit,
                transform: p.transform,
            });
        }
        nesting.write_sheet(&placements, stock.width, stock.height, outline)
    }
}
