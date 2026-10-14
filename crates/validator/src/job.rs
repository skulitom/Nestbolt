//! Engine-neutral benchmark contract. This is not yet the public project/curve format.
use std::collections::{BTreeMap, BTreeSet};

use anyhow::{Context, Result, ensure};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::{BACKEND, Footprint, GRID, Polygon, RigidTransform, Units};

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Job {
    pub version: u32,
    pub name: String,
    pub units: Units,
    pub parts: Vec<Part>,
    pub stocks: Vec<Stock>,
    pub clearance: f64,
    pub edge_clearance: f64,
    pub mode: Mode,
}

#[derive(Clone, Copy, Debug, Deserialize, Serialize, PartialEq, Eq, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum Mode {
    All,
    FillArea,
    FillPriority,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Part {
    pub id: String,
    pub quantity: u32,
    pub geometry: Vec<Polygon>,
    pub rotations: Rotations,
    pub allow_mirror: bool,
    pub priority: f64,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Rotations {
    Free,
    Step { degrees: f64 },
    List { degrees: Vec<f64> },
}

#[derive(Clone, Copy, Debug, Default, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Margins {
    pub left: f64,
    pub right: f64,
    pub bottom: f64,
    pub top: f64,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Stock {
    pub id: String,
    pub width: f64,
    pub height: f64,
    /// null is unlimited; zero makes this stock unavailable.
    pub count: Option<u32>,
    pub margins: Margins,
    /// Empty means the complete rectangular sheet; otherwise a remnant outline.
    pub outline: Vec<Polygon>,
    pub defects: Vec<Polygon>,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Layout {
    pub version: u32,
    pub units: Units,
    pub sheets: Vec<Sheet>,
    pub placements: Vec<Placement>,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Sheet {
    pub id: String,
    pub stock_id: String,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Placement {
    pub part_id: String,
    /// Zero-based physical copy within the source quantity.
    pub copy_index: u32,
    pub sheet_id: String,
    pub transform: RigidTransform,
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct Violation {
    pub code: &'static str,
    pub message: String,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct Metrics {
    pub sheets_used: usize,
    pub placed_parts: usize,
    pub requested_parts: u32,
    /// Area is mm² for physical jobs, squared model units for unitless jobs.
    pub placed_area: f64,
    /// Sum of per-copy priorities, not an area-weighted score.
    pub placed_priority: f64,
    pub full_stock_area: f64,
    pub material_area: f64,
    /// Material area divided by the largest available stock outline's area.
    pub normalized_material: f64,
    pub utilization: f64,
    pub trailing_offcut_area: f64,
    pub last_sheet_id: Option<String>,
    /// In the job's declared coordinate units; measured in the +Y direction.
    pub last_sheet_used_height: f64,
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct Report {
    pub valid: bool,
    pub backend: &'static str,
    pub units: Units,
    pub maximum_overlap_ratio: f64,
    pub maximum_total_overlap_ratio: f64,
    pub maximum_outside_ratio: f64,
    pub violation_count: u32,
    /// At most 128 diagnostics; violation_count includes every detected failure.
    pub violations: Vec<Violation>,
    /// Invalid layouts are never assigned a usable score.
    pub metrics: Option<Metrics>,
}

impl Report {
    fn issue(&mut self, code: &'static str, message: String) {
        self.violation_count += 1;
        if self.violations.len() < 128 {
            self.violations.push(Violation { code, message });
        }
    }
}

pub fn rectangle(x: f64, y: f64, width: f64, height: f64) -> Polygon {
    Polygon {
        outer: vec![
            [x, y],
            [x + width, y],
            [x + width, y + height],
            [x, y + height],
        ],
        holes: vec![],
    }
}

struct PreparedStock {
    gross: Footprint,
    usable: Option<Footprint>,
    tolerant: Option<Footprint>,
}

fn prepare_stock(stock: &Stock, units: Units) -> Result<PreparedStock> {
    ensure!(
        stock.width.is_finite()
            && stock.height.is_finite()
            && stock.width > 0.0
            && stock.height > 0.0,
        "stock dimensions must be positive and finite"
    );
    let m = stock.margins;
    ensure!(
        [m.left, m.right, m.bottom, m.top]
            .iter()
            .all(|v| v.is_finite() && *v >= 0.0),
        "margins must be finite and nonnegative"
    );
    ensure!(
        m.left + m.right < stock.width && m.bottom + m.top < stock.height,
        "margins consume the entire stock"
    );
    let bounds = Footprint::new(
        &rectangle(0.0, 0.0, stock.width, stock.height),
        units,
        RigidTransform::default(),
    )?;
    let gross = if stock.outline.is_empty() {
        bounds.clone()
    } else {
        let outline = Footprint::from_polygons(&stock.outline, units, RigidTransform::default())?;
        ensure!(
            outline.inside(&bounds, 0.0)?.outside_area == 0.0,
            "stock outline exceeds its dimensions"
        );
        outline
    };
    let margins = Footprint::new(
        &rectangle(
            m.left,
            m.bottom,
            stock.width - m.left - m.right,
            stock.height - m.bottom - m.top,
        ),
        units,
        RigidTransform::default(),
    )?;
    let mut usable = gross.intersection(&margins)?;
    for defect in &stock.defects {
        let hole = Footprint::new(defect, units, RigidTransform::default())?;
        if let Some(remaining) = usable {
            usable = remaining.subtract(&hole)?;
        }
    }
    let tolerant = usable
        .as_ref()
        .map(Footprint::boundary_tolerance)
        .transpose()?;
    Ok(PreparedStock {
        gross,
        usable,
        tolerant,
    })
}

/// The lead checker uses the identical stock/margin/defect contract, while it
/// independently rebuilds every lead footprint from analytic path parameters.
pub(crate) fn usable_stock(stock: &Stock, units: Units) -> Result<Option<Footprint>> {
    Ok(prepare_stock(stock, units)?.usable)
}

fn validate_rotations(rotations: &Rotations) -> Result<()> {
    match rotations {
        Rotations::Free => Ok(()),
        Rotations::Step { degrees } => {
            ensure!(
                degrees.is_finite() && *degrees > 0.0 && *degrees <= 360.0,
                "rotation step must be in (0,360]"
            );
            Ok(())
        }
        Rotations::List { degrees } => {
            ensure!(
                !degrees.is_empty()
                    && degrees.len() <= 3600
                    && degrees.iter().all(|d| d.is_finite() && d.abs() <= 360.0),
                "rotation list needs finite angles between -360 and 360"
            );
            Ok(())
        }
    }
}

fn rotation_allowed(rotations: &Rotations, radians: f64) -> bool {
    if !radians.is_finite() {
        return false;
    }
    let degrees = radians.to_degrees().rem_euclid(360.0);
    let close = |a: f64| ((degrees - a + 180.0).rem_euclid(360.0) - 180.0).abs() <= 0.00001;
    match rotations {
        Rotations::Free => true,
        Rotations::Step { degrees: step } => {
            let multiple = (degrees / step).round() * step;
            close(0.0) || (multiple < 360.0 && close(multiple))
        }
        Rotations::List { degrees } => degrees.iter().any(|a| close(*a)),
    }
}

/// Validate a complete benchmark job independently of the engine. Invalid input
/// contracts return an error; invalid placements return a report with no metrics.
pub fn validate(job: &Job, layout: &Layout) -> Result<Report> {
    ensure!(
        job.version == 1 && layout.version == 1,
        "unsupported benchmark contract version"
    );
    ensure!(!job.name.trim().is_empty(), "job name is required");
    ensure!(
        !job.parts.is_empty()
            && !job.stocks.is_empty()
            && job.parts.len() <= 2000
            && job.stocks.len() <= 2000,
        "job requires 1..2000 part and stock types"
    );
    ensure!(
        [job.clearance, job.edge_clearance]
            .iter()
            .all(|v| v.is_finite() && *v >= 0.0 && *v * job.units.to_mm() <= crate::MAX_COORDINATE),
        "clearances must be finite, nonnegative and within the coordinate range"
    );
    ensure!(
        layout.placements.len() <= 2000 && layout.sheets.len() <= 2000,
        "layout exceeds 2000 parts or sheets"
    );
    let mut parts = BTreeMap::new();
    let mut source_shapes = BTreeMap::new();
    let mut requested = 0_u32;
    for part in &job.parts {
        ensure!(
            !part.id.trim().is_empty() && parts.insert(part.id.as_str(), part).is_none(),
            "part IDs must be nonempty and unique"
        );
        requested = requested
            .checked_add(part.quantity)
            .context("quantity overflow")?;
        ensure!(
            part.priority.is_finite() && part.priority >= 0.0 && part.priority <= 1e12,
            "priority must be in 0..=1e12"
        );
        validate_rotations(&part.rotations)?;
        source_shapes.insert(
            part.id.as_str(),
            Footprint::from_polygons(&part.geometry, job.units, RigidTransform::default())
                .with_context(|| format!("invalid part {}", part.id))?,
        );
    }
    ensure!(
        (1..=2000).contains(&requested),
        "job requires 1..2000 copies"
    );
    let mut stocks = BTreeMap::new();
    let mut prepared = BTreeMap::new();
    for stock in &job.stocks {
        ensure!(
            !stock.id.trim().is_empty() && stocks.insert(stock.id.as_str(), stock).is_none(),
            "stock IDs must be nonempty and unique"
        );
        prepared.insert(
            stock.id.as_str(),
            prepare_stock(stock, job.units)
                .with_context(|| format!("invalid stock {}", stock.id))?,
        );
    }
    ensure!(
        job.stocks.iter().any(|s| s.count != Some(0)),
        "job has no available stock"
    );
    let mut report = Report {
        valid: false,
        backend: BACKEND,
        units: job.units,
        maximum_overlap_ratio: 0.0,
        maximum_total_overlap_ratio: 0.0,
        maximum_outside_ratio: 0.0,
        violation_count: 0,
        violations: vec![],
        metrics: None,
    };
    if layout.units != job.units {
        report.issue("units", "layout units differ from original job".into());
        return Ok(report);
    }
    let mut sheets = BTreeMap::new();
    let mut stock_counts = BTreeMap::<&str, u32>::new();
    for sheet in &layout.sheets {
        if sheet.id.trim().is_empty() || sheets.insert(sheet.id.as_str(), sheet).is_some() {
            report.issue(
                "sheet_id",
                format!("duplicate or empty sheet ID {}", sheet.id),
            );
        }
        if !stocks.contains_key(sheet.stock_id.as_str()) {
            report.issue(
                "stock_id",
                format!(
                    "sheet {} references unknown stock {}",
                    sheet.id, sheet.stock_id
                ),
            );
        }
        *stock_counts.entry(&sheet.stock_id).or_default() += 1;
    }
    for (id, count) in stock_counts {
        if let Some(stock) = stocks.get(id)
            && stock.count.is_some_and(|limit| count > limit)
        {
            report.issue(
                "stock_limit",
                format!("stock {id}: {count} sheets exceed its limit"),
            );
        }
    }
    let mut copies = BTreeSet::new();
    let mut occupied = BTreeSet::new();
    let mut placed = vec![];
    let mut highest = BTreeMap::<&str, f64>::new();
    let mut placed_area = 0.0;
    let mut placed_priority = 0.0;
    for (index, p) in layout.placements.iter().enumerate() {
        let Some(part) = parts.get(p.part_id.as_str()) else {
            report.issue(
                "part_id",
                format!("placement {index}: unknown part {}", p.part_id),
            );
            continue;
        };
        if p.copy_index >= part.quantity || !copies.insert((p.part_id.as_str(), p.copy_index)) {
            report.issue(
                "copy",
                format!(
                    "placement {index}: invalid or duplicate copy {} of {}",
                    p.copy_index, p.part_id
                ),
            );
        }
        let Some(sheet) = sheets.get(p.sheet_id.as_str()) else {
            report.issue(
                "sheet_id",
                format!("placement {index}: unknown sheet {}", p.sheet_id),
            );
            continue;
        };
        let Some(stock) = prepared.get(sheet.stock_id.as_str()) else {
            continue;
        };
        occupied.insert(p.sheet_id.as_str());
        if p.transform.mirrored && !part.allow_mirror {
            report.issue(
                "mirror",
                format!("placement {index}: mirroring is prohibited"),
            );
        }
        if !rotation_allowed(&part.rotations, p.transform.rotation_radians) {
            report.issue(
                "rotation",
                format!("placement {index}: rotation is not allowed"),
            );
        }
        let shape = match Footprint::from_polygons(&part.geometry, job.units, p.transform) {
            Ok(shape) => shape,
            Err(error) => {
                report.issue("transform", format!("placement {index}: {error:#}"));
                continue;
            }
        };
        if let (Some(tolerant), Some(usable)) = (&stock.tolerant, &stock.usable) {
            let containment = shape.inside(tolerant, 0.0)?;
            report.maximum_outside_ratio =
                report.maximum_outside_ratio.max(containment.outside_ratio);
            if containment.outside_area > 0.0 {
                report.issue(
                    "containment",
                    format!(
                        "placement {index}: outside usable sheet (area {})",
                        containment.outside_area
                    ),
                );
            }
            if job.edge_clearance > 0.0
                && shape
                    .inside(usable, job.edge_clearance)?
                    .clearance_violation
            {
                report.issue(
                    "edge_clearance",
                    format!("placement {index}: edge/defect clearance is too small"),
                );
            }
        } else {
            report.issue(
                "containment",
                format!("placement {index}: sheet has no usable area"),
            );
        }
        highest
            .entry(&p.sheet_id)
            .and_modify(|y| *y = y.max(shape.bounds()[3]))
            .or_insert(shape.bounds()[3]);
        placed_area += source_shapes[p.part_id.as_str()].area();
        placed_priority += part.priority;
        placed.push((index, p.sheet_id.as_str(), shape));
    }
    if job.mode == Mode::All {
        for part in &job.parts {
            let count = copies.iter().filter(|(id, _)| *id == part.id).count();
            if count != part.quantity as usize {
                report.issue(
                    "quantity",
                    format!(
                        "part {}: expected {}, found {count}",
                        part.id, part.quantity
                    ),
                );
            }
        }
    }
    for sheet in &layout.sheets {
        if !occupied.contains(sheet.id.as_str()) {
            report.issue(
                "empty_sheet",
                format!("sheet {} has no placements", sheet.id),
            );
        }
    }
    let mut total_overlap = vec![0.0; placed.len()];
    for (i, (index, sheet, shape)) in placed.iter().enumerate() {
        let mut comparisons = shape.pair_query(job.clearance);
        for (j, (other_index, other_sheet, other)) in placed.iter().enumerate().skip(i + 1) {
            if sheet != other_sheet {
                continue;
            }
            let pair = comparisons.compare(other)?;
            report.maximum_overlap_ratio = report.maximum_overlap_ratio.max(pair.overlap_ratio);
            total_overlap[i] += pair.overlap_area;
            total_overlap[j] += pair.overlap_area;
            if pair.overlap_ratio > 1e-6 {
                report.issue(
                    "overlap",
                    format!(
                        "placements {index}/{other_index}: overlap ratio {}",
                        pair.overlap_ratio
                    ),
                );
            }
            if pair.clearance_violation {
                report.issue(
                    "clearance",
                    format!("placements {index}/{other_index}: insufficient clearance"),
                );
            }
        }
    }
    for (i, (index, _, shape)) in placed.iter().enumerate() {
        let ratio = total_overlap[i] / shape.area();
        report.maximum_total_overlap_ratio = report.maximum_total_overlap_ratio.max(ratio);
        if ratio > 1e-6 {
            report.issue(
                "total_overlap",
                format!("placement {index}: cumulative overlap ratio {ratio}"),
            );
        }
    }
    if report.violation_count > 0 {
        return Ok(report);
    }
    let mut full_area = 0.0;
    let mut offcut = 0.0;
    let mut last = None;
    let mut last_height = 0.0;
    for (sheet_id, sheet) in &sheets {
        let stock = stocks[sheet.stock_id.as_str()];
        let geometry = &prepared[sheet.stock_id.as_str()].gross;
        full_area += geometry.area();
        let used = (highest[sheet_id] / job.units.to_mm() + job.edge_clearance + stock.margins.top)
            .clamp(0.0, stock.height);
        // Rounding upward prevents the saved offcut from including cutting geometry.
        let used = (used / (GRID / job.units.to_mm())).ceil() * (GRID / job.units.to_mm());
        let prefix = Footprint::new(
            &rectangle(0.0, 0.0, stock.width, used.min(stock.height)),
            job.units,
            RigidTransform::default(),
        )?;
        let prefix_area = geometry.intersection(&prefix)?.map_or(0.0, |f| f.area());
        let saving = (geometry.area() - prefix_area).max(0.0);
        if last.is_none() || saving > offcut {
            offcut = saving;
            last = Some((*sheet_id).to_string());
            last_height = used.min(stock.height);
        }
    }
    let reference_area = job
        .stocks
        .iter()
        .filter(|s| s.count != Some(0))
        .map(|s| prepared[s.id.as_str()].gross.area())
        .fold(0.0_f64, f64::max);
    let material_area = (full_area - offcut).max(0.0);
    report.valid = true;
    report.metrics = Some(Metrics {
        sheets_used: sheets.len(),
        placed_parts: layout.placements.len(),
        requested_parts: requested,
        placed_area,
        placed_priority,
        full_stock_area: full_area,
        material_area,
        normalized_material: material_area / reference_area,
        utilization: if material_area > 0.0 {
            placed_area / material_area
        } else {
            0.0
        },
        trailing_offcut_area: offcut,
        last_sheet_id: last,
        last_sheet_used_height: last_height,
    });
    Ok(report)
}
