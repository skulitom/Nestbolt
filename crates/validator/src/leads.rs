//! Independent lead-path envelopes and checks against original placed geometry.
//! Paths are analytic local millimetres, not polygons supplied by the solver.
use std::{
    collections::{HashMap, HashSet},
    f64::consts::{PI, TAU},
};

use anyhow::{Context, Result, ensure};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::{
    ClipType, ClipperOffset, EndType, Footprint, GRID, JoinType, MAX_COORDINATE, Point64,
    RigidTransform, SCALE, Units, boolean,
    job::{Job, Layout, Metrics, Mode, Placement, Rotations, usable_stock},
};

/// Each chord/round-join error is covered by additional outward radius.
pub const ENVELOPE_TOLERANCE_MM: f64 = 0.0001;
const MAX_PATH_POINTS: usize = 10_000;

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Path {
    Line {
        from_mm: [f64; 2],
        to_mm: [f64; 2],
    },
    Arc {
        center_mm: [f64; 2],
        radius_mm: f64,
        start_radians: f64,
        sweep_radians: f64,
    },
}

impl Path {
    pub fn point(&self, t: f64) -> [f64; 2] {
        match self {
            Self::Line {
                from_mm: a,
                to_mm: b,
            } => std::array::from_fn(|k| a[k] + (b[k] - a[k]) * t),
            Self::Arc {
                center_mm: c,
                radius_mm: r,
                start_radians: a,
                sweep_radians: s,
            } => {
                // Compose rotations instead of adding a small sweep to a large
                // starting angle, which can erase meaningful physical motion.
                let (sa, ca) = a.sin_cos();
                let (sd, cd) = (s * t).sin_cos();
                [
                    c[0] + r * (ca * cd - sa * sd),
                    c[1] + r * (sa * cd + ca * sd),
                ]
            }
        }
    }

    pub fn validate(&self) -> Result<()> {
        let finite_point =
            |p: &[f64; 2]| p.iter().all(|v| v.is_finite() && v.abs() <= MAX_COORDINATE);
        match self {
            Self::Line {
                from_mm: a,
                to_mm: b,
            } => {
                ensure!(
                    finite_point(a) && finite_point(b),
                    "lead coordinates must be finite and in range"
                );
                ensure!(
                    (a[0] - b[0]).hypot(a[1] - b[1]) > GRID,
                    "lead line has no length"
                );
            }
            Self::Arc {
                center_mm: c,
                radius_mm: r,
                start_radians: a,
                sweep_radians: s,
            } => {
                ensure!(
                    finite_point(c)
                        && r.is_finite()
                        && *r > GRID
                        && *r <= MAX_COORDINATE
                        && a.is_finite()
                        && a.abs() <= 1e8
                        && s.is_finite()
                        && s.abs() > 1e-12
                        && s.abs() <= TAU,
                    "lead arc parameters must be finite and in range"
                );
                ensure!(
                    c.iter().all(|v| v.abs() + r <= MAX_COORDINATE),
                    "lead arc exceeds coordinate range"
                );
            }
        }
        Ok(())
    }

    /// Mirror/rotate paths independently of the core curve transformation code.
    /// Local path coordinates stay in mm; translations use the job's units.
    pub fn transformed(&self, transform: RigidTransform, units: Units) -> Result<Self> {
        self.validate()?;
        ensure!(
            transform.translation.iter().all(|v| v.is_finite())
                && transform.rotation_radians.is_finite()
                && transform.rotation_radians.abs() <= 1e8,
            "lead transform must be finite and in range"
        );
        let (s, c) = transform.rotation_radians.sin_cos();
        let point = |p: [f64; 2]| {
            let x = if transform.mirrored { -p[0] } else { p[0] };
            [
                c * x - s * p[1] + transform.translation[0] * units.to_mm(),
                s * x + c * p[1] + transform.translation[1] * units.to_mm(),
            ]
        };
        let path = match self {
            Self::Line { from_mm, to_mm } => Self::Line {
                from_mm: point(*from_mm),
                to_mm: point(*to_mm),
            },
            Self::Arc {
                center_mm,
                radius_mm,
                start_radians,
                sweep_radians,
            } => Self::Arc {
                center_mm: point(*center_mm),
                radius_mm: *radius_mm,
                // atan2(sin, cos) retains the original argument reduction,
                // unlike `% TAU`, before combining the two rotations.
                start_radians: s.atan2(c)
                    + if transform.mirrored {
                        PI - start_radians.sin().atan2(start_radians.cos())
                    } else {
                        start_radians.sin().atan2(start_radians.cos())
                    },
                sweep_radians: if transform.mirrored {
                    -sweep_radians
                } else {
                    *sweep_radians
                },
            },
        };
        path.validate()?;
        Ok(path)
    }

    fn points(&self) -> Result<Vec<Point64>> {
        self.validate()?;
        let count = match self {
            Self::Line { .. } => 1,
            Self::Arc {
                radius_mm: r,
                sweep_radians: s,
                ..
            } => {
                let step = 2.0 * (1.0 - (ENVELOPE_TOLERANCE_MM / r).min(1.0)).acos();
                let count = (s.abs() / step).ceil().max(1.0);
                ensure!(
                    count.is_finite() && count < MAX_PATH_POINTS as f64,
                    "lead arc needs too many footprint points"
                );
                count as usize
            }
        };
        let mut points: Vec<_> = (0..=count)
            .map(|i| {
                let p = self.point(i as f64 / count as f64);
                Point64::new((p[0] * SCALE).round() as i64, (p[1] * SCALE).round() as i64)
            })
            .collect();
        points.dedup();
        ensure!(points.len() >= 2, "lead collapsed at checker precision");
        Ok(points)
    }
}

/// One contour can reserve both traversal directions at a shared attachment.
/// The first path is the suggested review lead; all paths reserve physical room.
#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Allowance {
    pub part_id: String,
    pub copy_index: u32,
    pub contour_index: usize,
    pub kerf_mm: f64,
    pub paths: Vec<Path>,
}

/// Reconstruct a conservative path stroke (kerf/2) plus the pierce disc.
/// The plan's 2×kerf pierce disc is a diameter: its radius is one kerf.
/// Arc chords, round joins and nanometre-grid rounding are covered explicitly.
pub fn footprint(paths: &[Path], kerf_mm: f64) -> Result<Footprint> {
    ensure!(
        kerf_mm.is_finite() && kerf_mm > 0.0 && kerf_mm <= 1000.0,
        "lead kerf must be positive, finite and at most 1000 mm"
    );
    ensure!(
        !paths.is_empty() && paths.len() <= 2,
        "a lead allowance needs one or two paths"
    );
    let mut result = vec![];
    let target = paths[0].point(1.0);
    for path in paths {
        let points = path.points()?;
        let end = path.point(1.0);
        ensure!(
            (target[0] - end[0]).hypot(target[1] - end[1]) <= 2.0 * GRID,
            "lead alternatives must have the same attachment"
        );
        // Clipper's round joins are chord approximations; oversize by twice
        // their tolerance, plus the centreline chord error and grid rounding.
        let mut stroke = ClipperOffset::new(2.0, ENVELOPE_TOLERANCE_MM * SCALE, false, false);
        stroke.add_path(&points, JoinType::Round, EndType::Round);
        let mut outlined = vec![];
        stroke.execute(
            (kerf_mm / 2.0 + 3.0 * ENVELOPE_TOLERANCE_MM + 4.0 * GRID) * SCALE,
            &mut outlined,
        );
        ensure!(
            stroke.error_code() == 0 && !outlined.is_empty(),
            "lead stroke offset failed"
        );
        let mut pierce = ClipperOffset::new(2.0, ENVELOPE_TOLERANCE_MM * SCALE, false, false);
        pierce.add_path(&vec![points[0]], JoinType::Round, EndType::Round);
        let mut disc = vec![];
        pierce.execute(
            (kerf_mm + 2.0 * ENVELOPE_TOLERANCE_MM + 4.0 * GRID) * SCALE,
            &mut disc,
        );
        ensure!(
            pierce.error_code() == 0 && !disc.is_empty(),
            "lead pierce envelope failed"
        );
        outlined.extend(disc);
        result = boolean(&result, &outlined, ClipType::Union)?;
    }
    let shape = Footprint::from_paths(result, Units::Mm).context("lead allowance has no area")?;
    ensure!(
        shape.bounds().iter().all(|v| v.abs() <= MAX_COORDINATE),
        "lead allowance exceeds coordinate range"
    );
    Ok(shape)
}

/// Waste-side checks in local millimetres. The normal boundary cut already
/// removes a half-kerf band. A lead may join that band, but must not cut deeper
/// into the part; its piercing disc must remain wholly in waste. Source curves
/// should be flattened to ENVELOPE_TOLERANCE_MM before constructing `body`.
pub struct Owner {
    body: Footprint,
    protected: Option<Footprint>,
    centre_protected: Option<Footprint>,
    kerf_mm: f64,
}

impl Owner {
    pub fn new(body: Footprint, kerf_mm: f64) -> Result<Self> {
        ensure!(body.units == Units::Mm, "lead owner must use millimetres");
        ensure!(
            kerf_mm.is_finite() && kerf_mm > 0.0 && kerf_mm <= 1000.0,
            "lead kerf must be positive, finite and at most 1000 mm"
        );
        let erode = |amount: f64| -> Result<Option<Footprint>> {
            let mut offset = ClipperOffset::new(2.0, ENVELOPE_TOLERANCE_MM * SCALE, false, false);
            offset.add_paths(&body.paths, JoinType::Round, EndType::Polygon);
            let mut paths = vec![];
            offset.execute(-amount * SCALE, &mut paths);
            ensure!(offset.error_code() == 0, "lead owner inset failed");
            Ok(Footprint::from_paths(paths, Units::Mm))
        };
        // Covers source flattening, round offsets and the conservative lead
        // envelope, without granting the whole owner an overlap exemption.
        let tolerance = 8.0 * ENVELOPE_TOLERANCE_MM + 8.0 * GRID;
        Ok(Self {
            protected: erode(kerf_mm / 2.0 + tolerance)?,
            centre_protected: erode(tolerance)?,
            body,
            kerf_mm,
        })
    }

    pub fn fits(&self, paths: &[Path]) -> Result<bool> {
        let envelope = footprint(paths, self.kerf_mm)?;
        let Some(protected) = &self.protected else {
            // The ordinary kerf consumes this entire part; do not call a lead
            // safe merely because the protected set is empty.
            return Ok(false);
        };
        if envelope.compare(protected, 0.0)?.overlap_area > 0.0 {
            return Ok(false);
        }
        if let Some(interior) = &self.centre_protected
            && footprint(paths, 2.0 * GRID)?
                .compare(interior, 0.0)?
                .overlap_area
                > 0.0
        {
            return Ok(false);
        }
        for path in paths {
            let p = path.point(0.0);
            let mut offset = ClipperOffset::new(2.0, ENVELOPE_TOLERANCE_MM * SCALE, false, false);
            offset.add_path(
                &vec![Point64::new(
                    (p[0] * SCALE).round() as i64,
                    (p[1] * SCALE).round() as i64,
                )],
                JoinType::Round,
                EndType::Round,
            );
            let mut paths = vec![];
            offset.execute(
                (self.kerf_mm + 2.0 * ENVELOPE_TOLERANCE_MM + 4.0 * GRID) * SCALE,
                &mut paths,
            );
            ensure!(offset.error_code() == 0, "lead pierce check failed");
            let disc =
                Footprint::from_paths(paths, Units::Mm).context("lead pierce check collapsed")?;
            if disc.compare(&self.body, 0.0)?.overlap_area > 0.0 {
                return Ok(false);
            }
        }
        Ok(true)
    }
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct Report {
    pub valid: bool,
    pub checked_contours: usize,
    pub violation_count: usize,
    pub violations: Vec<String>,
    /// Original placed area, with stock consumption/offcuts enclosing the
    /// independently rebuilt lead envelopes as well as the original parts.
    pub metrics: Option<Metrics>,
}

/// Check every supplied allowance against original parts on its sheet, other
/// contours' allowances (including the same part), margins, remnants and defects.
/// Coverage/flagging of contours without a lead is reported by the lead planner.
pub fn validate(job: &Job, layout: &Layout, allowances: &[Allowance]) -> Result<Report> {
    let original_report = crate::job::validate(job, layout)?;
    ensure!(
        original_report.valid,
        "lead checks require a valid original layout"
    );
    ensure!(allowances.len() <= 100_000, "too many lead allowances");
    let mut report = Report {
        valid: true,
        checked_contours: allowances.len(),
        violation_count: 0,
        violations: vec![],
        metrics: None,
    };
    let mut issue = |text: String| {
        report.valid = false;
        report.violation_count += 1;
        if report.violations.len() < 128 {
            report.violations.push(text);
        }
    };
    let parts: HashMap<_, _> = job.parts.iter().map(|p| (p.id.as_str(), p)).collect();
    let placements: HashMap<_, _> = layout
        .placements
        .iter()
        .map(|p| ((p.part_id.as_str(), p.copy_index), p))
        .collect();
    let originals = layout
        .placements
        .iter()
        .map(|p| {
            let mut shape = Footprint::from_polygons(
                &parts[p.part_id.as_str()].geometry,
                job.units,
                p.transform,
            )?;
            shape.units = Units::Mm; // Internal coordinates are already physical mm.
            Ok((p, shape))
        })
        .collect::<Result<Vec<_>>>()?;
    let mut stocks = HashMap::new();
    for sheet in &layout.sheets {
        let stock = job
            .stocks
            .iter()
            .find(|s| s.id == sheet.stock_id)
            .context("unknown lead sheet stock")?;
        let mut shape = usable_stock(stock, job.units)?.context("lead sheet has no usable area")?;
        shape.units = Units::Mm;
        stocks.insert(sheet.id.as_str(), shape);
    }
    let mut seen = HashSet::new();
    let mut built: Vec<(&Allowance, &str, Footprint)> = vec![];
    for allowance in allowances {
        let key = (allowance.part_id.as_str(), allowance.copy_index);
        let placement = placements
            .get(&key)
            .context("lead refers to an unplaced part copy")?;
        ensure!(
            seen.insert((key, allowance.contour_index)),
            "duplicate contour allowance"
        );
        let count: usize = parts[key.0]
            .geometry
            .iter()
            .map(|p| 1 + p.holes.len())
            .sum();
        ensure!(
            allowance.contour_index < count,
            "lead contour index is out of range"
        );
        let paths = allowance
            .paths
            .iter()
            .map(|p| p.transformed(placement.transform, job.units))
            .collect::<Result<Vec<_>>>()?;
        let shape = footprint(&paths, allowance.kerf_mm)?;
        let owner = format!("{}#{} contour {}", key.0, key.1, allowance.contour_index);
        let sheet = placement.sheet_id.as_str();
        let inside = shape.inside(&stocks[sheet], job.edge_clearance * job.units.to_mm())?;
        if inside.outside_area > 0.0 || inside.clearance_violation {
            issue(format!(
                "{owner}: lead crosses a stock edge, margin, remnant boundary or defect"
            ));
        }
        for (other, body) in &originals {
            if other.sheet_id == sheet
                && (other.part_id.as_str(), other.copy_index) != key
                && shape.compare(body, 0.0)?.overlap_area > 0.0
            {
                issue(format!(
                    "{owner}: lead overlaps part {}#{}",
                    other.part_id, other.copy_index
                ));
            }
        }
        for (other, other_sheet, body) in &built {
            if *other_sheet == sheet && shape.compare(body, 0.0)?.overlap_area > 0.0 {
                issue(format!(
                    "{owner}: lead overlaps allowance {}#{} contour {}",
                    other.part_id, other.copy_index, other.contour_index
                ));
            }
        }
        built.push((allowance, sheet, shape));
    }
    if report.valid {
        report.metrics = Some(reserved_metrics(
            job,
            layout,
            &originals,
            &built,
            original_report
                .metrics
                .as_ref()
                .context("original layout has no metrics")?,
        )?);
    }
    Ok(report)
}

fn reserved_metrics(
    job: &Job,
    layout: &Layout,
    originals: &[(&Placement, Footprint)],
    built: &[(&Allowance, &str, Footprint)],
    original_metrics: &Metrics,
) -> Result<Metrics> {
    if originals.is_empty() {
        return Ok(original_metrics.clone());
    }
    // Each placed copy can have a different start/length after common-line
    // exclusions. Build independent per-copy geometry in world coordinates.
    let mut physical = job.clone();
    physical.parts.clear();
    physical.mode = Mode::FillArea;
    physical.clearance = 0.0; // Original spacing and strict lead overlap were checked above.
    let mut positioned = layout.clone();
    positioned.placements.clear();
    let by_id: HashMap<_, _> = job.parts.iter().map(|p| (p.id.as_str(), p)).collect();
    for (index, (placement, original)) in originals.iter().enumerate() {
        let mut combined = original.clone();
        for (lead, _, shape) in built {
            if lead.part_id == placement.part_id && lead.copy_index == placement.copy_index {
                combined = combined.union(shape)?;
            }
        }
        let mut part = by_id[placement.part_id.as_str()].clone();
        part.id = format!("reserved-copy-{index}");
        part.quantity = 1;
        part.rotations = Rotations::List { degrees: vec![0.0] };
        part.allow_mirror = false;
        part.geometry = combined.polygons()?;
        for polygon in &mut part.geometry {
            for point in polygon
                .outer
                .iter_mut()
                .chain(polygon.holes.iter_mut().flatten())
            {
                for value in point {
                    *value /= job.units.to_mm();
                }
            }
        }
        positioned.placements.push(Placement {
            part_id: part.id.clone(),
            copy_index: 0,
            sheet_id: placement.sheet_id.clone(),
            transform: RigidTransform::default(),
        });
        physical.parts.push(part);
    }
    let checked = crate::job::validate(&physical, &positioned)?;
    ensure!(
        checked.valid,
        "reserved lead geometry failed independent stock accounting: {:?}",
        checked.violations
    );
    let mut metrics = checked
        .metrics
        .context("reserved lead geometry has no metrics")?;
    metrics.requested_parts = original_metrics.requested_parts;
    metrics.placed_area = original_metrics.placed_area;
    metrics.utilization = if metrics.material_area > 0.0 {
        metrics.placed_area / metrics.material_area
    } else {
        0.0
    };
    Ok(metrics)
}
