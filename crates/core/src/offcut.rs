//! Reusable offcut / remnant extraction and closed-loop SHEET-layer export.
//!
//! After nesting a job, shops often have a large clean slab (guillotine cut)
//! or usable irregular scrap left on the bed. This module computes those
//! leftover polygons with the independent Clipper2 footprint kernel, verifies
//! that no exported remnant intersects any placed part, and writes SVG/DXF
//! files on the `SHEET` layer that Nestbolt's own remnant importer reads back
//! directly for the next job.
use std::collections::BTreeMap;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::{
    Footprint, GRID, Polygon, RigidTransform, Units,
    job::{Job, Layout, Stock, rectangle, validate},
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::export::{remnant_dxf, remnant_svg};

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum OffcutMode {
    /// Clean straight-cut slab above the highest placed part (+ edge clearance + top margin).
    #[default]
    Rectangular,
    /// True-shape reusable remnant: stock outline (minus defects) minus every
    /// placed part inflated by part clearance, filtered by minimum size.
    Exact,
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(default, deny_unknown_fields)]
pub struct Options {
    pub mode: OffcutMode,
    /// Discard leftover fragments smaller than this area in mm² (default 2,500 mm² = 50 × 50 mm).
    pub min_area_mm2: f64,
    /// Discard thin slivers whose bounding-box width or height is below this limit in mm (default 25 mm).
    pub min_dimension_mm: f64,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            mode: OffcutMode::Rectangular,
            min_area_mm2: 2500.0,
            min_dimension_mm: 25.0,
        }
    }
}

impl Options {
    pub fn validate(self) -> Result<()> {
        ensure!(
            self.min_area_mm2.is_finite() && self.min_area_mm2 >= 0.0,
            "min_area_mm2 must be finite and nonnegative"
        );
        ensure!(
            self.min_dimension_mm.is_finite() && self.min_dimension_mm >= 0.0,
            "min_dimension_mm must be finite and nonnegative"
        );
        Ok(())
    }
}

/// One reusable leftover piece extracted from a nested sheet, normalized to
/// `[0, 0]` so it matches `SheetOutline` and drops straight into a new job.
#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct Remnant {
    pub id: String,
    pub sheet_id: String,
    pub stock_id: String,
    pub mode: OffcutMode,
    pub width_mm: f64,
    pub height_mm: f64,
    pub area_mm2: f64,
    /// Lower-left corner in the source sheet's mm, Y-up frame before normalization.
    pub origin_mm: [f64; 2],
    /// Normalized remnant polygons in mm, Y-up, with origin at `[0, 0]`.
    pub outline_mm: Vec<Polygon>,
}

impl Remnant {
    /// Export this remnant as an SVG on the `SHEET` layer (`#f36926`).
    pub fn to_svg(&self) -> Result<String> {
        remnant_svg(&self.id, self.width_mm, self.height_mm, &self.outline_mm)
    }

    /// Export this remnant as an AutoCAD 2007 DXF on the `SHEET` layer (ACI 30 / `#f36926`).
    pub fn to_dxf(&self) -> Result<String> {
        remnant_dxf(&self.outline_mm)
    }
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct OffcutReport {
    pub mode: OffcutMode,
    pub min_area_mm2: f64,
    pub min_dimension_mm: f64,
    pub total_area_mm2: f64,
    pub remnants: Vec<Remnant>,
}

fn gross_minus_defects(stock: &Stock, units: Units) -> Result<Option<Footprint>> {
    let bounds = Footprint::new(
        &rectangle(0.0, 0.0, stock.width, stock.height),
        units,
        RigidTransform::default(),
    )?;
    let mut base = if stock.outline.is_empty() {
        Some(bounds)
    } else {
        Some(Footprint::from_polygons(
            &stock.outline,
            units,
            RigidTransform::default(),
        )?)
    };
    for defect in &stock.defects {
        let hole = Footprint::new(defect, units, RigidTransform::default())?;
        if let Some(current) = base {
            base = current.subtract(&hole)?;
        }
    }
    Ok(base)
}

/// Extract reusable remnants from one sheet (`sheet_id = Some(...)`) or all
/// sheets in a validated layout.
pub fn extract(
    job: &Job,
    layout: &Layout,
    sheet_id: Option<&str>,
    options: Options,
) -> Result<OffcutReport> {
    let check = validate(job, layout)?;
    extract_checked(job, layout, sheet_id, options, &check, &BTreeMap::new())
}

/// Use the finalized cutting reservations for each placed copy.
#[cfg(feature = "search")]
pub fn for_request(
    request: &crate::project::Request,
    library: &crate::project::Library,
    layout: &Layout,
    sheet_id: Option<&str>,
    options: Options,
) -> Result<OffcutReport> {
    let prepared = request.prepare(library)?;
    let report = prepared.report(layout)?;
    let mut cuts = BTreeMap::new();
    if let Some(leads) = report.lead_in {
        let placements: BTreeMap<_, _> = layout
            .placements
            .iter()
            .map(|p| ((p.part_id.as_str(), p.copy_index), p))
            .collect();
        for allowance in leads.allowances() {
            let placed = placements[&(allowance.part_id.as_str(), allowance.copy_index)];
            let paths = allowance
                .paths
                .iter()
                .map(|path| path.transformed(placed.transform, layout.units))
                .collect::<Result<Vec<_>>>()?;
            cuts.entry(placed.sheet_id.as_str())
                .or_insert_with(Vec::new)
                .push(nestbolt_validator::leads::footprint(
                    &paths,
                    allowance.kerf_mm,
                )?);
        }
    }
    extract_checked(
        &prepared.job,
        layout,
        sheet_id,
        options,
        &report.validation,
        &cuts,
    )
}

fn extract_checked(
    job: &Job,
    layout: &Layout,
    sheet_id: Option<&str>,
    options: Options,
    check: &nestbolt_validator::job::Report,
    cuts: &BTreeMap<&str, Vec<Footprint>>,
) -> Result<OffcutReport> {
    options.validate()?;
    ensure!(
        check.valid,
        "cannot extract offcuts from an invalid layout: {:?}",
        check.violations
    );
    let parts: BTreeMap<&str, _> = job.parts.iter().map(|p| (p.id.as_str(), p)).collect();
    let stocks: BTreeMap<&str, &Stock> = job.stocks.iter().map(|s| (s.id.as_str(), s)).collect();
    let scale = job.units.to_mm();

    if let Some(wanted) = sheet_id {
        ensure!(
            layout.sheets.iter().any(|s| s.id == wanted),
            "unknown sheet {wanted}"
        );
    }
    let mut remnants = Vec::new();
    for (sheet_index, sheet) in layout.sheets.iter().enumerate() {
        if sheet_id.is_some_and(|wanted| wanted != sheet.id) {
            continue;
        }
        let stock = stocks
            .get(sheet.stock_id.as_str())
            .with_context(|| format!("unknown stock {}", sheet.stock_id))?;
        let Some(base) = gross_minus_defects(stock, job.units)? else {
            continue;
        };
        let sheet_placements: Vec<_> = layout
            .placements
            .iter()
            .filter(|p| p.sheet_id == sheet.id)
            .collect();
        let mut placed_shapes = Vec::with_capacity(sheet_placements.len());
        let mut highest_mm = 0.0_f64;
        for placement in &sheet_placements {
            let part = parts
                .get(placement.part_id.as_str())
                .with_context(|| format!("unknown part {}", placement.part_id))?;
            let fp = Footprint::from_polygons(&part.geometry, job.units, placement.transform)?;
            highest_mm = highest_mm.max(fp.bounds()[3]);
            placed_shapes.push(fp);
        }

        if let Some(allowances) = cuts.get(sheet.id.as_str()) {
            for fp in allowances {
                highest_mm = highest_mm.max(fp.bounds()[3]);
                placed_shapes.push(fp.clone());
            }
        }

        let leftover = match options.mode {
            OffcutMode::Rectangular => {
                // Match `nestbolt_validator::job::validate`: round the straight cut line
                // upward to the validator grid so cutting geometry stays strictly below it.
                let grid_units = GRID / scale;
                let used = (highest_mm / scale + job.edge_clearance + stock.margins.top)
                    .clamp(0.0, stock.height);
                let used = (used / grid_units).ceil() * grid_units;
                let remaining_h = stock.height - used;
                if remaining_h <= grid_units {
                    None
                } else {
                    let slab = Footprint::new(
                        &rectangle(0.0, used, stock.width, remaining_h),
                        job.units,
                        RigidTransform::default(),
                    )?;
                    base.intersection(&slab)?
                }
            }
            OffcutMode::Exact => {
                let mut current = Some(base);
                let expand_units = job.clearance.max(0.0) + 2.0 * GRID / scale;
                for fp in &placed_shapes {
                    let Some(rem) = current else {
                        break;
                    };
                    let cut = fp.expand(expand_units)?;
                    current = rem.subtract(&cut)?;
                }
                current
            }
        };

        let Some(leftover) = leftover else {
            continue;
        };
        let mut index = 0_usize;
        for poly in leftover.polygons()? {
            let scaled_poly = Polygon {
                outer: poly
                    .outer
                    .into_iter()
                    .map(|[x, y]| [x * scale, y * scale])
                    .collect(),
                holes: poly
                    .holes
                    .into_iter()
                    .map(|h| h.into_iter().map(|[x, y]| [x * scale, y * scale]).collect())
                    .collect(),
            };
            let Ok(fp) = Footprint::new(&scaled_poly, Units::Mm, RigidTransform::default()) else {
                continue;
            };
            let area_mm2 = fp.area();
            let [x0, y0, x1, y1] = fp.bounds();
            let width_mm = x1 - x0;
            let height_mm = y1 - y0;
            if area_mm2 < options.min_area_mm2
                || width_mm < options.min_dimension_mm
                || height_mm < options.min_dimension_mm
            {
                continue;
            }
            // Shift to [0, 0] origin in mm to match `SheetOutline`.
            let shift = |ring: Vec<[f64; 2]>| {
                ring.into_iter()
                    .map(|[x, y]| [x - x0, y - y0])
                    .collect::<Vec<_>>()
            };
            let normalized = Polygon {
                outer: shift(scaled_poly.outer),
                holes: scaled_poly.holes.into_iter().map(shift).collect(),
            };
            index += 1;
            let suffix = match options.mode {
                OffcutMode::Rectangular => "offcut",
                OffcutMode::Exact => "remnant",
            };
            remnants.push(Remnant {
                id: format!("sheet-{sheet_index}-{suffix}-{index}"),
                sheet_id: sheet.id.clone(),
                stock_id: sheet.stock_id.clone(),
                mode: options.mode,
                width_mm,
                height_mm,
                area_mm2,
                origin_mm: [x0, y0],
                outline_mm: vec![normalized],
            });
        }
    }

    let total_area_mm2 = remnants.iter().map(|r| r.area_mm2).sum();
    Ok(OffcutReport {
        mode: options.mode,
        min_area_mm2: options.min_area_mm2,
        min_dimension_mm: options.min_dimension_mm,
        total_area_mm2,
        remnants,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[cfg(feature = "search")]
    use crate::import::Options as ImportOptions;
    use nestbolt_validator::job::{Margins, Mode, Part, Placement, Rotations, Sheet};

    fn sample_job_and_layout() -> (Job, Layout) {
        let job = Job {
            version: 1,
            name: "offcut-test".into(),
            units: Units::Mm,
            parts: vec![Part {
                id: "panel".into(),
                quantity: 2,
                geometry: vec![rectangle(0.0, 0.0, 120.0, 80.0)],
                rotations: Rotations::List {
                    degrees: vec![0.0, 90.0],
                },
                allow_mirror: false,
                priority: 1.0,
            }],
            stocks: vec![Stock {
                id: "ply-600x400".into(),
                width: 600.0,
                height: 400.0,
                count: None,
                margins: Margins {
                    left: 5.0,
                    right: 5.0,
                    bottom: 5.0,
                    top: 5.0,
                },
                outline: vec![],
                defects: vec![],
            }],
            clearance: 2.0,
            edge_clearance: 1.0,
            mode: Mode::All,
        };
        let layout = Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![Sheet {
                id: "sheet-0".into(),
                stock_id: "ply-600x400".into(),
            }],
            placements: vec![
                Placement {
                    part_id: "panel".into(),
                    copy_index: 0,
                    sheet_id: "sheet-0".into(),
                    transform: RigidTransform {
                        translation: [10.0, 10.0],
                        rotation_radians: 0.0,
                        mirrored: false,
                    },
                },
                Placement {
                    part_id: "panel".into(),
                    copy_index: 1,
                    sheet_id: "sheet-0".into(),
                    transform: RigidTransform {
                        translation: [140.0, 10.0],
                        rotation_radians: 0.0,
                        mirrored: false,
                    },
                },
            ],
        };
        (job, layout)
    }

    #[test]
    fn rectangular_offcut_matches_validator_trailing_area_and_roundtrips_svg_and_dxf() {
        let (job, layout) = sample_job_and_layout();
        let metrics = validate(&job, &layout).unwrap().metrics.unwrap();
        let report = extract(&job, &layout, Some("sheet-0"), Options::default()).unwrap();
        assert_eq!(report.remnants.len(), 1);
        let remnant = &report.remnants[0];
        assert!((remnant.area_mm2 - metrics.trailing_offcut_area).abs() < 1.0);
        assert!((remnant.width_mm - 600.0).abs() < 1e-3);
        assert!((remnant.height_mm - (400.0 - 96.0)).abs() < 1e-3);

        let svg = remnant.to_svg().unwrap();
        let dxf = remnant.to_dxf().unwrap();
        assert!(svg.contains(r#"id="SHEET""#));
        assert!(dxf.contains("\nSHEET\n"));

        // Closed-loop check: both exported files re-import cleanly via `SheetImport::read`.
        #[cfg(feature = "search")]
        {
            for (name, text) in [("offcut.svg", svg), ("offcut.dxf", dxf)] {
                let reimported =
                    crate::project::SheetImport::read(name, &text, &ImportOptions::default())
                        .unwrap();
                assert_eq!(reimported.outlines.len(), 1);
                assert!((reimported.outlines[0].width_mm - remnant.width_mm).abs() < 0.05);
                assert!((reimported.outlines[0].height_mm - remnant.height_mm).abs() < 0.05);
            }
        }
    }

    #[test]
    fn export_names_are_independent_of_sheet_labels() {
        let (job, mut layout) = sample_job_and_layout();
        let label = "rack A/left:panel";
        layout.sheets[0].id = label.into();
        for p in &mut layout.placements {
            p.sheet_id = label.into();
        }
        let report = extract(&job, &layout, Some(label), Options::default()).unwrap();
        assert_eq!(report.remnants[0].id, "sheet-0-offcut-1");
        assert_eq!(report.remnants[0].sheet_id, label);
    }

    #[test]
    fn exact_remnant_reclaims_side_space_and_stays_clear_of_all_placed_parts() {
        let (job, layout) = sample_job_and_layout();
        let rect_report = extract(&job, &layout, None, Options::default()).unwrap();
        let exact_report = extract(
            &job,
            &layout,
            None,
            Options {
                mode: OffcutMode::Exact,
                ..Options::default()
            },
        )
        .unwrap();
        assert_eq!(exact_report.remnants.len(), 1);
        let exact = &exact_report.remnants[0];
        // True-shape remnant reclaims the large unused right-hand L-area too!
        assert!(
            exact.area_mm2 > rect_report.total_area_mm2 + 25_000.0,
            "exact={} rect={}",
            exact.area_mm2,
            rect_report.total_area_mm2
        );
        // Independently verify zero intersection between remnant (shifted back to sheet coords) and any placed part.
        let unshifted = Footprint::from_polygons(
            &exact.outline_mm,
            Units::Mm,
            RigidTransform {
                translation: exact.origin_mm,
                rotation_radians: 0.0,
                mirrored: false,
            },
        )
        .unwrap();
        for p in &layout.placements {
            let part_fp =
                Footprint::from_polygons(&job.parts[0].geometry, Units::Mm, p.transform).unwrap();
            let pair = unshifted.compare(&part_fp, 0.0).unwrap();
            assert_eq!(pair.overlap_area, 0.0);
        }
    }
}
