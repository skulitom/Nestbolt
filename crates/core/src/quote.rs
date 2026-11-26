//! Shop cutting telemetry and job quoting from exact curves and validated layouts.
//!
//! Cut lengths are computed directly from exact source contours (`Contour::length`),
//! never from flattened polygons, and deduct any verified common-line savings.
//! Material area, utilization and reusable trailing offcuts come straight from the
//! independent validator metrics.
use std::collections::{BTreeMap, HashMap};
use std::fmt::Write as _;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::job::{Job, Layout, validate};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::export::Outline;

/// Optional shop pricing and machine-rate parameters for quoting a layout.
#[derive(Clone, Debug, Default, Serialize, Deserialize, JsonSchema)]
#[serde(default, deny_unknown_fields)]
pub struct Pricing {
    /// Default cost per full sheet (used when `stock_costs` has no override for a stock id).
    pub sheet_cost: Option<f64>,
    /// Optional per-stock-id sheet cost overrides.
    #[serde(default, skip_serializing_if = "BTreeMap::is_empty")]
    pub stock_costs: BTreeMap<String, f64>,
    /// Alternative material cost per square metre of sheet area.
    pub material_cost_per_m2: Option<f64>,
    /// Credit usable trailing offcut area proportionally against material cost (default false).
    pub credit_offcut: bool,
    /// Cutting speed in mm/min (for example 1200 for plywood laser or 3000 for plasma).
    pub cut_speed_mm_per_min: Option<f64>,
    /// Pierce dwell time per cutting contour in seconds (default 0).
    pub pierce_seconds: f64,
    /// Hourly machine + operator rate (requires `cut_speed_mm_per_min` or `pierce_seconds > 0`).
    pub machine_rate_per_hour: Option<f64>,
    /// Fixed setup fee per job (default 0).
    pub setup_cost: f64,
    /// Optional currency code or symbol for display (for example "USD", "GBP", "EUR").
    pub currency: Option<String>,
}

impl Pricing {
    pub fn validate(&self) -> Result<()> {
        let nonneg = |name: &str, v: f64| -> Result<()> {
            ensure!(
                v.is_finite() && v >= 0.0,
                "{name} must be finite and nonnegative"
            );
            Ok(())
        };
        if let Some(c) = self.sheet_cost {
            nonneg("sheet_cost", c)?;
        }
        for (stock_id, &cost) in &self.stock_costs {
            nonneg(&format!("stock_costs[{stock_id}]"), cost)?;
        }
        if let Some(c) = self.material_cost_per_m2 {
            nonneg("material_cost_per_m2", c)?;
        }
        if let Some(speed) = self.cut_speed_mm_per_min {
            ensure!(
                speed.is_finite() && speed > 0.0,
                "cut_speed_mm_per_min must be finite and positive"
            );
        }
        nonneg("pierce_seconds", self.pierce_seconds)?;
        if let Some(rate) = self.machine_rate_per_hour {
            nonneg("machine_rate_per_hour", rate)?;
        }
        nonneg("setup_cost", self.setup_cost)?;
        Ok(())
    }

    fn has_any_cost(&self) -> bool {
        self.sheet_cost.is_some()
            || !self.stock_costs.is_empty()
            || self.material_cost_per_m2.is_some()
            || self.machine_rate_per_hour.is_some()
            || self.setup_cost > 0.0
    }
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct SheetQuote {
    pub sheet_id: String,
    pub stock_id: String,
    pub width_mm: f64,
    pub height_mm: f64,
    pub placed_parts: usize,
    pub outer_contours: usize,
    pub hole_contours: usize,
    pub open_contours: usize,
    pub pierce_count: usize,
    pub gross_cut_length_mm: f64,
    pub common_line_saved_mm: f64,
    pub net_cut_length_mm: f64,
    pub placed_area_mm2: f64,
    pub sheet_area_mm2: f64,
    pub utilization: f64,
    pub trailing_offcut_area_mm2: f64,
    pub trailing_offcut_height_mm: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub estimated_cut_seconds: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub gross_material_cost: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub offcut_credit: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub net_material_cost: Option<f64>,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct CostBreakdown {
    pub currency: String,
    pub gross_material_cost: f64,
    pub offcut_credit: f64,
    pub net_material_cost: f64,
    pub machine_cost: f64,
    pub setup_cost: f64,
    pub total_cost: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cost_per_part: Option<f64>,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct JobQuote {
    pub version: u32,
    pub job_name: String,
    pub sheets_used: usize,
    pub placed_parts: usize,
    pub requested_parts: u32,
    pub outer_contours: usize,
    pub hole_contours: usize,
    pub open_contours: usize,
    pub total_pierces: usize,
    pub gross_cut_length_mm: f64,
    pub common_line_saved_mm: f64,
    pub net_cut_length_mm: f64,
    pub placed_area_mm2: f64,
    pub full_stock_area_mm2: f64,
    pub material_area_mm2: f64,
    pub trailing_offcut_area_mm2: f64,
    pub utilization: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub estimated_cut_seconds: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub costs: Option<CostBreakdown>,
    pub sheets: Vec<SheetQuote>,
}

/// Compute exact cutting lengths, pierce counts, material utilization and
/// optional shop cost breakdown for a validated layout.
///
/// `common_saved_mm` maps `sheet_id -> saved_length_mm` when common-line
/// analysis has been run.
pub fn compute(
    job: &Job,
    layout: &Layout,
    curves: &HashMap<String, Outline>,
    common_saved_mm: Option<&HashMap<String, f64>>,
    pricing: &Pricing,
) -> Result<JobQuote> {
    let report = validate(job, layout)?;
    compute_checked(
        job,
        layout,
        &report,
        |sheet| {
            (
                common_saved_mm
                    .and_then(|m| m.get(sheet))
                    .copied()
                    .unwrap_or(0.0),
                0.0,
            )
        },
        pricing,
        |part| Ok(CutMetrics::from_part(part, curves)),
    )
}

#[derive(Default)]
struct CutMetrics {
    outer: usize,
    holes: usize,
    open: usize,
    length: f64,
}

impl CutMetrics {
    fn from_part(part: &nestbolt_validator::job::Part, curves: &HashMap<String, Outline>) -> Self {
        let mut cuts = CutMetrics::default();
        if let Some(outline) = curves.get(&part.id) {
            cuts.add_outline(outline);
        } else {
            for polygon in &part.geometry {
                cuts.add_outline(&Outline::from_polygon(polygon));
            }
        }
        cuts
    }

    fn add_outline(&mut self, outline: &Outline) {
        self.outer += 1;
        self.holes += outline.holes.len();
        self.length +=
            outline.outer.length() + outline.holes.iter().map(|c| c.length()).sum::<f64>();
    }
}

fn compute_checked(
    job: &Job,
    layout: &Layout,
    report: &nestbolt_validator::job::Report,
    sheet_lengths: impl Fn(&str) -> (f64, f64),
    pricing: &Pricing,
    cuts: impl Fn(&nestbolt_validator::job::Part) -> Result<CutMetrics>,
) -> Result<JobQuote> {
    pricing.validate()?;
    ensure!(
        report.valid,
        "cannot quote an invalid layout: {:?}",
        report.violations
    );
    let metrics = report
        .metrics
        .as_ref()
        .context("valid layout missing metrics")?;
    let scale = job.units.to_mm();
    let area_scale = scale * scale;
    let mut part_metrics = HashMap::with_capacity(job.parts.len());
    for part in &job.parts {
        let area = part
            .geometry
            .iter()
            .map(crate::curves::polygon_area)
            .sum::<f64>()
            * area_scale;
        part_metrics.insert(part.id.as_str(), (cuts(part)?, area));
    }
    let stocks: HashMap<&str, _> = job.stocks.iter().map(|s| (s.id.as_str(), s)).collect();
    let mut sheets = Vec::with_capacity(layout.sheets.len());
    let mut total_outer = 0_usize;
    let mut total_open = 0;
    let mut total_holes = 0_usize;
    let mut total_gross_cut = 0.0_f64;
    let mut total_saved_cut = 0.0_f64;
    let mut total_est_seconds = 0.0_f64;
    let mut any_time = false;
    let mut total_gross_mat_cost = 0.0_f64;
    let mut total_offcut_credit = 0.0_f64;

    for sheet in &layout.sheets {
        let stock = stocks
            .get(sheet.stock_id.as_str())
            .with_context(|| format!("unknown stock {}", sheet.stock_id))?;
        let width_mm = stock.width * scale;
        let height_mm = stock.height * scale;
        let sheet_area_mm2 = if stock.outline.is_empty() {
            width_mm * height_mm
        } else {
            stock
                .outline
                .iter()
                .map(crate::curves::polygon_area)
                .sum::<f64>()
                * area_scale
        };

        let mut placed_parts = 0_usize;
        let mut outer_contours = 0_usize;
        let mut open_contours = 0;
        let mut hole_contours = 0_usize;
        let mut gross_cut = 0.0_f64;
        let mut placed_area = 0.0_f64;
        for placement in layout.placements.iter().filter(|p| p.sheet_id == sheet.id) {
            let (pm, area) = part_metrics
                .get(placement.part_id.as_str())
                .with_context(|| format!("unknown part {}", placement.part_id))?;
            placed_parts += 1;
            outer_contours += pm.outer;
            hole_contours += pm.holes;
            open_contours += pm.open;
            gross_cut += pm.length * scale;
            placed_area += area;
        }
        let pierce_count = outer_contours + hole_contours + open_contours;
        let (saved, leads) = sheet_lengths(&sheet.id);
        gross_cut += leads;
        let saved = saved.clamp(0.0, gross_cut);
        let net_cut = (gross_cut - saved).max(0.0);

        let is_last_offcut_sheet = metrics
            .last_sheet_id
            .as_deref()
            .is_some_and(|id| id == sheet.id);
        let trailing_offcut_area_mm2 = if is_last_offcut_sheet {
            metrics.trailing_offcut_area
        } else {
            0.0
        };
        let trailing_offcut_height_mm = if is_last_offcut_sheet {
            (height_mm - metrics.last_sheet_used_height * scale).max(0.0)
        } else {
            0.0
        };

        let dwell = pierce_count as f64 * pricing.pierce_seconds;
        let est_seconds = pricing
            .cut_speed_mm_per_min
            .map(|speed| net_cut / speed * 60.0 + dwell)
            .or_else(|| (pricing.pierce_seconds > 0.0).then_some(dwell));
        if let Some(s) = est_seconds {
            total_est_seconds += s;
            any_time = true;
        }

        let gross_sheet_cost = pricing
            .stock_costs
            .get(&sheet.stock_id)
            .copied()
            .or(pricing.sheet_cost)
            .or_else(|| {
                pricing
                    .material_cost_per_m2
                    .map(|per_m2| (sheet_area_mm2 / 1_000_000.0) * per_m2)
            });
        let (offcut_credit, net_sheet_cost) = match gross_sheet_cost {
            Some(gross) => {
                let credit = if pricing.credit_offcut && sheet_area_mm2 > 0.0 {
                    gross * (trailing_offcut_area_mm2 / sheet_area_mm2).clamp(0.0, 1.0)
                } else {
                    0.0
                };
                total_gross_mat_cost += gross;
                total_offcut_credit += credit;
                (Some(credit), Some((gross - credit).max(0.0)))
            }
            None => (None, None),
        };

        let utilization = if sheet_area_mm2 > 0.0 {
            placed_area / sheet_area_mm2
        } else {
            0.0
        };

        total_outer += outer_contours;
        total_open += open_contours;
        total_holes += hole_contours;
        total_gross_cut += gross_cut;
        total_saved_cut += saved;

        sheets.push(SheetQuote {
            sheet_id: sheet.id.clone(),
            stock_id: sheet.stock_id.clone(),
            width_mm,
            height_mm,
            placed_parts,
            outer_contours,
            hole_contours,
            open_contours,
            pierce_count,
            gross_cut_length_mm: gross_cut,
            common_line_saved_mm: saved,
            net_cut_length_mm: net_cut,
            placed_area_mm2: placed_area,
            sheet_area_mm2,
            utilization,
            trailing_offcut_area_mm2,
            trailing_offcut_height_mm,
            estimated_cut_seconds: est_seconds,
            gross_material_cost: gross_sheet_cost,
            offcut_credit,
            net_material_cost: net_sheet_cost,
        });
    }

    let total_net_cut = (total_gross_cut - total_saved_cut).max(0.0);
    let estimated_cut_seconds = any_time.then_some(total_est_seconds);
    let costs = if pricing.has_any_cost() {
        let net_material_cost = (total_gross_mat_cost - total_offcut_credit).max(0.0);
        let machine_cost = match (pricing.machine_rate_per_hour, estimated_cut_seconds) {
            (Some(rate), Some(secs)) => rate * (secs / 3600.0),
            _ => 0.0,
        };
        let total_cost = net_material_cost + machine_cost + pricing.setup_cost;
        let cost_per_part =
            (metrics.placed_parts > 0).then_some(total_cost / metrics.placed_parts as f64);
        Some(CostBreakdown {
            currency: pricing.currency.clone().unwrap_or_else(|| "USD".to_owned()),
            gross_material_cost: total_gross_mat_cost,
            offcut_credit: total_offcut_credit,
            net_material_cost,
            machine_cost,
            setup_cost: pricing.setup_cost,
            total_cost,
            cost_per_part,
        })
    } else {
        None
    };

    Ok(JobQuote {
        version: 1,
        job_name: job.name.clone(),
        sheets_used: metrics.sheets_used,
        placed_parts: metrics.placed_parts,
        requested_parts: metrics.requested_parts,
        outer_contours: total_outer,
        hole_contours: total_holes,
        open_contours: total_open,
        total_pierces: total_outer + total_holes + total_open,
        gross_cut_length_mm: total_gross_cut,
        common_line_saved_mm: total_saved_cut,
        net_cut_length_mm: total_net_cut,
        placed_area_mm2: metrics.placed_area,
        full_stock_area_mm2: metrics.full_stock_area,
        material_area_mm2: metrics.material_area,
        trailing_offcut_area_mm2: metrics.trailing_offcut_area,
        utilization: metrics.utilization,
        estimated_cut_seconds,
        costs,
        sheets,
    })
}

/// Quote the original cuts and recompute cutting reservations and shared edges for this layout.
#[cfg(feature = "search")]
pub fn for_request(
    request: &crate::project::Request,
    library: &crate::project::Library,
    layout: &Layout,
    pricing: &Pricing,
) -> Result<JobQuote> {
    let prepared = request.prepare(library)?;
    let report = prepared.report(layout)?;
    let saved: HashMap<String, f64> = report
        .common_line
        .as_deref()
        .unwrap_or_default()
        .iter()
        .map(|r| (r.sheet_id.clone(), r.saved_length_mm))
        .collect();
    let mut lead_lengths = HashMap::<&str, f64>::new();
    if let Some(plan) = &report.lead_in {
        for part in &plan.parts {
            let paths = part.plan.reservations.iter().flat_map(|r| &r.paths);
            let length: f64 = paths
                .map(|path| match path {
                    nestbolt_validator::leads::Path::Line { from_mm, to_mm } => {
                        (to_mm[0] - from_mm[0]).hypot(to_mm[1] - from_mm[1])
                    }
                    nestbolt_validator::leads::Path::Arc {
                        radius_mm,
                        sweep_radians,
                        ..
                    } => radius_mm * sweep_radians.abs(),
                })
                .sum();
            *lead_lengths.entry(&part.sheet_id).or_default() += length;
        }
    }
    let originals = library.lightburn_cut_sources()?;
    compute_checked(
        &prepared.job,
        layout,
        &report.validation,
        |sheet| {
            (
                saved.get(sheet).copied().unwrap_or(0.0),
                lead_lengths.get(sheet).copied().unwrap_or(0.0),
            )
        },
        pricing,
        |part| {
            let mut cuts = CutMetrics::default();
            if let Some(sources) = &originals {
                let source = sources
                    .get(&part.id)
                    .context("missing original LightBurn cutting geometry")?;
                for outline in &source.components {
                    cuts.add_outline(outline);
                }
                cuts.open = source.open.len();
                cuts.length += source.open.iter().map(|c| c.length()).sum::<f64>();
            } else {
                return Ok(CutMetrics::from_part(part, &prepared.outlines));
            }
            Ok(cuts)
        },
    )
}

impl JobQuote {
    /// RFC 4180 CSV summary with one row per sheet plus a TOTAL row.
    pub fn to_csv(&self) -> String {
        let mut out = String::from(
            "sheet_id,stock_id,width_mm,height_mm,placed_parts,pierces,gross_cut_mm,common_saved_mm,net_cut_mm,utilization_pct,offcut_area_mm2,est_cut_s,net_material_cost,machine_cost,setup_cost,total_cost,currency\n",
        );
        for s in &self.sheets {
            let _ = writeln!(
                out,
                "{},{},{:.2},{:.2},{},{},{:.2},{:.2},{:.2},{:.2},{:.1},{},{},,,,",
                csv_cell(&s.sheet_id),
                csv_cell(&s.stock_id),
                s.width_mm,
                s.height_mm,
                s.placed_parts,
                s.pierce_count,
                s.gross_cut_length_mm,
                s.common_line_saved_mm,
                s.net_cut_length_mm,
                s.utilization * 100.0,
                s.trailing_offcut_area_mm2,
                s.estimated_cut_seconds
                    .map_or_else(String::new, |v| format!("{v:.1}")),
                s.net_material_cost
                    .map_or_else(String::new, |v| format!("{v:.2}")),
            );
        }
        let cost = |field: fn(&CostBreakdown) -> f64| {
            self.costs
                .as_ref()
                .map_or_else(String::new, |c| format!("{:.2}", field(c)))
        };
        let _ = writeln!(
            out,
            "TOTAL,,0,0,{},{},{:.2},{:.2},{:.2},{:.2},{:.1},{},{},{},{},{},{}",
            self.placed_parts,
            self.total_pierces,
            self.gross_cut_length_mm,
            self.common_line_saved_mm,
            self.net_cut_length_mm,
            self.utilization * 100.0,
            self.trailing_offcut_area_mm2,
            self.estimated_cut_seconds
                .map_or_else(String::new, |v| format!("{v:.1}")),
            cost(|c| c.net_material_cost),
            cost(|c| c.machine_cost),
            cost(|c| c.setup_cost),
            cost(|c| c.total_cost),
            self.costs
                .as_ref()
                .map_or_else(String::new, |c| csv_cell(&c.currency)),
        );
        out
    }

    /// Clean Markdown summary suitable for shop job sheets, PRs or agent replies.
    pub fn to_markdown(&self) -> String {
        let mut out = String::new();
        let _ = writeln!(out, "# Nestbolt Job Quote: {}\n", self.job_name);
        let _ = writeln!(
            out,
            "- **Sheets used:** {} | **Placed parts:** {}/{} | **Utilization:** {:.1}%",
            self.sheets_used,
            self.placed_parts,
            self.requested_parts,
            self.utilization * 100.0
        );
        let _ = writeln!(
            out,
            "- **Cut length:** {:.2} m net ({:.2} m gross, {:.2} m saved via common-line) | **Pierces:** {} ({} outer, {} holes, {} open)",
            self.net_cut_length_mm / 1000.0,
            self.gross_cut_length_mm / 1000.0,
            self.common_line_saved_mm / 1000.0,
            self.total_pierces,
            self.outer_contours,
            self.hole_contours,
            self.open_contours
        );
        if self.trailing_offcut_area_mm2 > 0.0 {
            let _ = writeln!(
                out,
                "- **Reusable trailing offcut:** {:.0} cm² ({:.1}% of full stock)",
                self.trailing_offcut_area_mm2 / 100.0,
                if self.full_stock_area_mm2 > 0.0 {
                    100.0 * self.trailing_offcut_area_mm2 / self.full_stock_area_mm2
                } else {
                    0.0
                }
            );
        }
        if let Some(secs) = self.estimated_cut_seconds {
            let _ = writeln!(
                out,
                "- **Estimated cutting time:** {:.1} min ({:.0} s)",
                secs / 60.0,
                secs
            );
        }
        if let Some(c) = &self.costs {
            let _ = writeln!(
                out,
                "- **Total cost:** {} {:.2} (material {:.2} − offcut credit {:.2} + machine {:.2} + setup {:.2}){}",
                c.currency,
                c.total_cost,
                c.gross_material_cost,
                c.offcut_credit,
                c.machine_cost,
                c.setup_cost,
                c.cost_per_part
                    .map_or_else(String::new, |p| format!(" · {} {:.2}/part", c.currency, p)),
            );
        }
        out.push_str("\n| Sheet | Stock | Parts | Pierces | Net cut (m) | Utilisation |\n");
        out.push_str("| --- | --- | ---: | ---: | ---: | ---: |\n");
        for s in &self.sheets {
            let _ = writeln!(
                out,
                "| {} | {} ({:.0}×{:.0} mm) | {} | {} | {:.2} | {:.1}% |",
                s.sheet_id,
                s.stock_id,
                s.width_mm,
                s.height_mm,
                s.placed_parts,
                s.pierce_count,
                s.net_cut_length_mm / 1000.0,
                s.utilization * 100.0
            );
        }
        out
    }
}

fn csv_cell(value: &str) -> String {
    if value.contains([',', '"', '\n', '\r']) {
        format!("\"{}\"", value.replace('"', "\"\""))
    } else {
        value.to_owned()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::curves::{Contour, Segment};
    use nestbolt_validator::{
        RigidTransform, Units,
        job::{Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle},
    };
    use std::f64::consts::TAU;

    #[test]
    fn quote_computes_exact_curve_lengths_common_line_deduction_and_cost_breakdown() {
        let mut poly = rectangle(0.0, 0.0, 100.0, 50.0);
        // Add a circular hole approximated in polygon, exact circle in Outline.
        poly.holes
            .push(vec![[30.0, 15.0], [50.0, 15.0], [50.0, 35.0], [30.0, 35.0]]);
        let job = Job {
            version: 1,
            name: "quote-job".into(),
            units: Units::Mm,
            parts: vec![Part {
                id: "plate".into(),
                quantity: 2,
                geometry: vec![poly],
                rotations: Rotations::List { degrees: vec![0.0] },
                allow_mirror: false,
                priority: 1.0,
            }],
            stocks: vec![Stock {
                id: "ply".into(),
                width: 400.0,
                height: 200.0,
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
            clearance: 1.0,
            edge_clearance: 1.0,
            mode: Mode::All,
        };
        let layout = Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![Sheet {
                id: "sheet-0".into(),
                stock_id: "ply".into(),
            }],
            placements: vec![
                Placement {
                    part_id: "plate".into(),
                    copy_index: 0,
                    sheet_id: "sheet-0".into(),
                    transform: RigidTransform {
                        translation: [10.0, 10.0],
                        rotation_radians: 0.0,
                        mirrored: false,
                    },
                },
                Placement {
                    part_id: "plate".into(),
                    copy_index: 1,
                    sheet_id: "sheet-0".into(),
                    transform: RigidTransform {
                        translation: [120.0, 10.0],
                        rotation_radians: 0.0,
                        mirrored: false,
                    },
                },
            ],
        };
        let mut curves = HashMap::new();
        curves.insert(
            "plate".into(),
            Outline {
                outer: Contour {
                    start: [0.0, 0.0],
                    segments: vec![
                        Segment::Line { to: [100.0, 0.0] },
                        Segment::Line { to: [100.0, 50.0] },
                        Segment::Line { to: [0.0, 50.0] },
                        Segment::Line { to: [0.0, 0.0] },
                    ],
                },
                holes: vec![Contour {
                    start: [50.0, 25.0],
                    segments: vec![Segment::Arc {
                        center: [40.0, 25.0],
                        radii: [10.0, 10.0],
                        rotation: 0.0,
                        start: 0.0,
                        sweep: TAU,
                    }],
                }],
            },
        );
        let mut common_saved = HashMap::new();
        common_saved.insert("sheet-0".into(), 50.0);
        let pricing = Pricing {
            sheet_cost: Some(20.0),
            credit_offcut: true,
            cut_speed_mm_per_min: Some(1200.0),
            pierce_seconds: 1.5,
            machine_rate_per_hour: Some(60.0),
            setup_cost: 10.0,
            currency: Some("USD".into()),
            ..Pricing::default()
        };
        let q = compute(&job, &layout, &curves, Some(&common_saved), &pricing).unwrap();
        let expected_gross = 2.0 * (300.0 + 10.0 * TAU);
        assert!((q.gross_cut_length_mm - expected_gross).abs() < 1e-6);
        assert_eq!(q.common_line_saved_mm, 50.0);
        assert!((q.net_cut_length_mm - (expected_gross - 50.0)).abs() < 1e-6);
        assert_eq!(q.total_pierces, 4);
        assert_eq!(q.outer_contours, 2);
        assert_eq!(q.hole_contours, 2);
        let expected_secs = ((expected_gross - 50.0) / 1200.0) * 60.0 + 4.0 * 1.5;
        assert!((q.estimated_cut_seconds.unwrap() - expected_secs).abs() < 1e-6);
        let costs = q.costs.as_ref().unwrap();
        assert_eq!(costs.gross_material_cost, 20.0);
        assert!(costs.offcut_credit > 10.0 && costs.offcut_credit < 15.0);
        assert!((costs.machine_cost - (expected_secs / 3600.0) * 60.0).abs() < 1e-6);
        assert_eq!(costs.setup_cost, 10.0);
        assert!((costs.cost_per_part.unwrap() - costs.total_cost / 2.0).abs() < 1e-9);
        let csv = q.to_csv();
        assert_eq!(
            csv.lines().last().unwrap().split(',').nth(12).unwrap(),
            format!("{:.2}", costs.net_material_cost)
        );
        let dwell_only = compute(
            &job,
            &layout,
            &curves,
            None,
            &Pricing {
                pierce_seconds: 1.5,
                machine_rate_per_hour: Some(60.0),
                ..Pricing::default()
            },
        )
        .unwrap();
        assert_eq!(dwell_only.estimated_cut_seconds, Some(6.0));
        assert_eq!(dwell_only.costs.unwrap().machine_cost, 0.1);
        assert!(q.to_markdown().contains("# Nestbolt Job Quote: quote-job"));
    }

    #[test]
    fn quote_rejects_negative_or_zero_pricing_values() {
        let bad = Pricing {
            cut_speed_mm_per_min: Some(0.0),
            ..Pricing::default()
        };
        assert!(bad.validate().is_err());
        let bad_cost = Pricing {
            sheet_cost: Some(-5.0),
            ..Pricing::default()
        };
        assert!(bad_cost.validate().is_err());
    }
}
