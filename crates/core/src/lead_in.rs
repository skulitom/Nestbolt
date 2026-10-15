//! Local lead planning. Source curves and material metrics remain separate from
//! the enlarged collision job. Every contour has either a reservation or an
//! explicit flag; exported starts refer to the original segment parameters.
use std::collections::HashMap;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::{
    Footprint, Polygon, RigidTransform, Units,
    job::Job,
    leads::{self, Path},
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::{
    common_line::length,
    curves::{Affine, Contour, Point, Segment, signed_area},
    export::{ContourStart, Outline},
};

const MIN_LENGTH_MM: f64 = 0.5;
const EPS: f64 = 1e-9;

mod layout;
#[cfg(test)]
mod tests;
pub use layout::{LayoutPlan, PlacedPartPlan, finalize};

#[derive(Clone, Copy, Debug, Default, Deserialize, Serialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum Style {
    #[default]
    Line,
    Arc,
}

#[derive(Clone, Copy, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Options {
    pub kerf_mm: f64,
    #[serde(default = "default_length")]
    pub length_mm: f64,
    #[serde(default)]
    pub style: Style,
    #[serde(default = "default_outer_angle")]
    pub outer_angle_degrees: f64,
    #[serde(default = "default_hole_angle")]
    pub hole_angle_degrees: f64,
}

fn default_length() -> f64 {
    3.0
}
fn default_outer_angle() -> f64 {
    45.0
}
fn default_hole_angle() -> f64 {
    90.0
}

impl Options {
    pub fn validate(self) -> Result<()> {
        ensure!(
            self.kerf_mm.is_finite() && self.kerf_mm > 0.0 && self.kerf_mm <= 1000.0,
            "lead kerf must be positive and at most 1000 mm"
        );
        ensure!(
            self.length_mm.is_finite() && (MIN_LENGTH_MM..=50.0).contains(&self.length_mm),
            "lead length must be between 0.5 and 50 mm"
        );
        ensure!(
            [self.outer_angle_degrees, self.hole_angle_degrees]
                .iter()
                .all(|a| a.is_finite() && (0.0..=90.0).contains(a)),
            "lead angle magnitudes must be between 0 and 90 degrees"
        );
        ensure!(
            [self.outer_angle_degrees, self.hole_angle_degrees]
                .iter()
                .all(|a| (a * 100.0 - (a * 100.0).round()).abs() <= EPS),
            "lead angles must use at most two decimal places to match LightBurn settings"
        );
        Ok(())
    }
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct Reservation {
    pub contour_index: usize,
    pub start: ContourStart,
    pub length_mm: f64,
    pub shortened: bool,
    pub paths: Vec<Path>,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct Flag {
    pub contour_index: usize,
    pub reason: String,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct PartPlan {
    pub part_id: String,
    pub contour_count: usize,
    pub reservations: Vec<Reservation>,
    pub flags: Vec<Flag>,
}

pub struct Prepared {
    /// Use only for collision search; score/report material against the original job.
    pub collision_job: Job,
    pub parts: Vec<PartPlan>,
    kerf_mm: f64,
}

impl Prepared {
    /// Expand the local plan for the copies actually placed by the search.
    pub fn allowances(
        &self,
        layout: &nestbolt_validator::job::Layout,
    ) -> Result<Vec<leads::Allowance>> {
        let plans: HashMap<_, _> = self.parts.iter().map(|p| (p.part_id.as_str(), p)).collect();
        let mut allowances = vec![];
        for placement in &layout.placements {
            let plan = plans
                .get(placement.part_id.as_str())
                .context("placement has no lead plan")?;
            allowances.extend(plan.reservations.iter().map(|r| leads::Allowance {
                part_id: placement.part_id.clone(),
                copy_index: placement.copy_index,
                contour_index: r.contour_index,
                kerf_mm: self.kerf_mm,
                paths: r.paths.clone(),
            }));
        }
        Ok(allowances)
    }

    /// Sheet coordinates for review, with original segment start overrides.
    /// The first direction is drawn; both directions remain reserved and checked.
    pub fn review(
        &self,
        layout: &nestbolt_validator::job::Layout,
        sheet_id: &str,
    ) -> Result<crate::export::ReviewPaths> {
        let plans: HashMap<_, _> = self.parts.iter().map(|p| (p.part_id.as_str(), p)).collect();
        let mut review = crate::export::ReviewPaths::default();
        for placement in layout.placements.iter().filter(|p| p.sheet_id == sheet_id) {
            let plan = plans
                .get(placement.part_id.as_str())
                .context("placement has no lead plan")?;
            append_review(&mut review, plan, placement, layout.units)?;
        }
        Ok(review)
    }
}

fn append_review(
    review: &mut crate::export::ReviewPaths,
    plan: &PartPlan,
    placement: &nestbolt_validator::job::Placement,
    units: Units,
) -> Result<()> {
    let mut starts = vec![None; plan.contour_count];
    for lead in &plan.reservations {
        starts[lead.contour_index] = Some(lead.start);
        let path = lead.paths[0].transformed(placement.transform, units)?;
        let start = path.point(0.0);
        let segment = match path {
            Path::Line { to_mm, .. } => Segment::Line { to: to_mm },
            Path::Arc {
                center_mm,
                radius_mm,
                start_radians,
                sweep_radians,
            } => Segment::Arc {
                center: center_mm,
                radii: [radius_mm, radius_mm],
                rotation: 0.0,
                start: start_radians,
                sweep: sweep_radians,
            },
        };
        review.leadin.push(Contour {
            start,
            segments: vec![segment],
        });
    }
    review.starts.insert(
        format!("{}#{}", placement.part_id, placement.copy_index),
        starts,
    );
    Ok(())
}

/// Disallowed attachment intervals on local contours, measured in millimetres
/// from the source start. A wrap may have to_mm greater than the perimeter.
#[derive(Clone, Copy, Debug)]
pub struct Exclusion {
    pub contour_index: usize,
    pub from_mm: f64,
    pub to_mm: f64,
}

fn sub(a: Point, b: Point) -> Point {
    [a[0] - b[0], a[1] - b[1]]
}
fn add(a: Point, b: Point) -> Point {
    [a[0] + b[0], a[1] + b[1]]
}
fn mul(a: Point, n: f64) -> Point {
    [a[0] * n, a[1] * n]
}
fn dot(a: Point, b: Point) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}
fn cross(a: Point, b: Point) -> f64 {
    a[0] * b[1] - a[1] * b[0]
}
fn unit(p: Point) -> Option<Point> {
    let d = p[0].hypot(p[1]);
    (d.is_finite() && d > EPS).then(|| mul(p, 1.0 / d))
}

/// `side` is +1 for waste left of traversal, -1 for waste right of traversal.
/// Arc length follows the native LightBurn calibration (plan decision 3).
pub fn path(
    attachment: Point,
    tangent: Point,
    side: f64,
    length_mm: f64,
    angle_degrees: f64,
    style: Style,
) -> Result<Path> {
    ensure!(
        side == 1.0 || side == -1.0,
        "lead waste side must be -1 or +1"
    );
    ensure!(
        length_mm.is_finite() && (MIN_LENGTH_MM..=50.0).contains(&length_mm),
        "lead length must be between 0.5 and 50 mm"
    );
    ensure!(
        angle_degrees.is_finite() && (0.0..=90.0).contains(&angle_degrees),
        "lead angle must be between 0 and 90 degrees"
    );
    let t = unit(tangent).context("lead attachment has no tangent")?;
    let n = mul([-t[1], t[0]], side);
    let angle = angle_degrees.to_radians();
    let result = if matches!(style, Style::Line) || angle == 0.0 {
        Path::Line {
            from_mm: add(
                attachment,
                add(
                    mul(t, -length_mm * angle.cos()),
                    mul(n, length_mm * angle.sin()),
                ),
            ),
            to_mm: attachment,
        }
    } else if length_mm / angle > nestbolt_validator::MAX_COORDINATE / 4.0
        && length_mm * angle / 8.0 < leads::ENVELOPE_TOLERANCE_MM
    {
        // Near zero angle, the remote centre loses precision or exceeds the
        // coordinate range. Use the chord only when its sagitta is covered by
        // the independent envelope's explicit chord-error allowance.
        Path::Line {
            from_mm: add(
                attachment,
                add(
                    mul(t, -length_mm * angle.sin() / angle),
                    mul(n, length_mm * 2.0 * (angle / 2.0).sin().powi(2) / angle),
                ),
            ),
            to_mm: attachment,
        }
    } else {
        let radius = length_mm / angle;
        let center = add(attachment, mul(n, radius));
        let end_angle = (-n[1]).atan2(-n[0]);
        Path::Arc {
            center_mm: center,
            radius_mm: radius,
            start_radians: end_angle - side * angle,
            sweep_radians: side * angle,
        }
    };
    result.validate()?;
    Ok(result)
}

#[derive(Clone)]
struct Candidate {
    start: ContourStart,
    cap: f64,
    distance: f64,
}

fn from(c: &Contour, i: usize) -> Point {
    if i == 0 {
        c.start
    } else {
        c.segments[i - 1].end()
    }
}

fn tangent(c: &Contour, i: usize, t: f64) -> Result<Point> {
    for p in [
        t,
        if t == 0.0 {
            1e-6
        } else if t == 1.0 {
            1.0 - 1e-6
        } else {
            t
        },
    ] {
        if let Some(v) = unit(c.segments[i].tangent_at(from(c, i), p)?) {
            return Ok(v);
        }
    }
    anyhow::bail!("contour attachment has a degenerate tangent")
}

fn candidates(c: &Contour, hole: bool, winding: f64) -> Result<Vec<Candidate>> {
    let lengths: Vec<_> = c
        .segments
        .iter()
        .enumerate()
        .map(|(i, s)| length::segment(from(c, i), s))
        .collect();
    ensure!(
        lengths.iter().all(|l| l.is_finite()),
        "non-finite contour length"
    );
    let mut cumulative = vec![0.0];
    for l in &lengths {
        cumulative.push(cumulative.last().unwrap() + l);
    }
    let mut result = vec![];
    if !hole {
        let mut corners = vec![];
        for i in 0..c.segments.len() {
            let prev = (i + c.segments.len() - 1) % c.segments.len();
            if let (Ok(a), Ok(b)) = (tangent(c, prev, 1.0), tangent(c, i, 0.0)) {
                let turn = winding * cross(a, b).atan2(dot(a, b));
                if turn > 1e-5 {
                    corners.push((i, turn));
                }
            }
        }
        corners.sort_by(|a, b| b.1.total_cmp(&a.1).then(a.0.cmp(&b.0)));
        result.extend(corners.into_iter().map(|(i, _)| Candidate {
            start: ContourStart {
                segment: i,
                parameter: 0.0,
            },
            cap: f64::INFINITY,
            distance: cumulative[i],
        }));
    }
    // Merge collinear line subdivisions, including across the arbitrary seam.
    let mut edges: Vec<Vec<usize>> = vec![];
    for (i, s) in c.segments.iter().enumerate() {
        if !matches!(s, Segment::Line { .. }) || lengths[i] <= EPS {
            continue;
        }
        let current = unit(sub(s.end(), from(c, i))).unwrap();
        let merge = edges.last().is_some_and(|e| {
            let j = *e.last().unwrap();
            let previous = unit(sub(c.segments[j].end(), from(c, j))).unwrap();
            j + 1 == i && cross(previous, current).abs() < 1e-12 && dot(previous, current) > 0.0
        });
        if merge {
            edges.last_mut().unwrap().push(i);
        } else {
            edges.push(vec![i]);
        }
    }
    if edges.len() > 1
        && edges[0][0] == 0
        && *edges.last().unwrap().last().unwrap() == c.segments.len() - 1
    {
        let first = tangent(c, 0, 0.0)?;
        let last = tangent(c, c.segments.len() - 1, 1.0)?;
        if cross(first, last).abs() < 1e-12 && dot(first, last) > 0.0 {
            let first = edges.remove(0);
            edges.last_mut().unwrap().extend(first);
        }
    }
    let total = |e: &Vec<usize>| -> f64 { e.iter().map(|&i| lengths[i]).sum() };
    edges.sort_by(|a, b| total(b).total_cmp(&total(a)).then(a[0].cmp(&b[0])));
    for edge in edges {
        let mut remaining = total(&edge) / 2.0;
        for i in edge {
            if remaining <= lengths[i] {
                let t = remaining / lengths[i];
                let (segment, parameter) = if t == 1.0 {
                    ((i + 1) % c.segments.len(), 0.0)
                } else {
                    (i, t)
                };
                result.push(Candidate {
                    start: ContourStart { segment, parameter },
                    cap: f64::INFINITY,
                    distance: (cumulative[i] + remaining) % cumulative.last().unwrap(),
                });
                break;
            }
            remaining -= lengths[i];
        }
    }
    if result.is_empty() && !hole {
        let i = (0..lengths.len())
            .max_by(|a, b| lengths[*a].total_cmp(&lengths[*b]))
            .unwrap();
        let (mut lo, mut hi) = (0.0, 1.0);
        for _ in 0..40 {
            let t = (lo + hi) / 2.0;
            let partial = length::segment(from(c, i), &c.segments[i].split_at(from(c, i), t)?.0);
            if partial < lengths[i] / 2.0 {
                lo = t;
            } else {
                hi = t;
            }
        }
        result.push(Candidate {
            start: ContourStart {
                segment: i,
                parameter: (lo + hi) / 2.0,
            },
            cap: f64::INFINITY,
            distance: cumulative[i] + lengths[i] / 2.0,
        });
    }
    if result.is_empty() {
        // Smooth contours have no corners/straight edges. For holes, choose
        // the boundary point nearest the area centroid; at a smooth minimum
        // the normal points towards that centre. Cap a radial line at it.
        let flat = c.flatten(leads::ENVELOPE_TOLERANCE_MM)?;
        let area = signed_area(&flat);
        let mut center = [0.0; 2];
        for i in 0..flat.len() {
            let a = flat[i];
            let b = flat[(i + 1) % flat.len()];
            let w = cross(a, b);
            center = add(center, mul(add(a, b), w / (6.0 * area)));
        }
        let mut choices = vec![];
        for (i, s) in c.segments.iter().enumerate() {
            // Search each of sixteen parameter intervals; ellipses and
            // Beziers can have several distinct minima against the centroid.
            for k in 0..16 {
                let (mut lo, mut hi) = (k as f64 / 16.0, (k + 1) as f64 / 16.0);
                let point = |t| -> Result<Point> { Ok(s.split_at(from(c, i), t)?.0.end()) };
                for _ in 0..36 {
                    let (a, b) = (lo + (hi - lo) / 3.0, hi - (hi - lo) / 3.0);
                    let (da, db) = (sub(point(a)?, center), sub(point(b)?, center));
                    if dot(da, da) < dot(db, db) {
                        hi = b;
                    } else {
                        lo = a;
                    }
                }
                let t = (lo + hi) / 2.0;
                let d = sub(point(t)?, center);
                let d = d[0].hypot(d[1]);
                choices.push((d, i, t));
            }
        }
        choices.sort_by(|a, b| {
            a.0.total_cmp(&b.0)
                .then(a.1.cmp(&b.1))
                .then(a.2.total_cmp(&b.2))
        });
        let (d, i, t) = choices[0];
        result.push(Candidate {
            start: ContourStart {
                segment: i,
                parameter: t,
            },
            cap: d,
            distance: cumulative[i]
                + length::segment(from(c, i), &c.segments[i].split_at(from(c, i), t)?.0),
        });
    }

    Ok(result)
}

/// Plan every contour before nesting. Shared-edge exclusions are optional local
/// intervals; per-copy post-search reselection is a separate integration step.
pub fn prepare(
    job: &Job,
    curves: &HashMap<String, Outline>,
    options: Options,
    exclusions: &HashMap<String, Vec<Exclusion>>,
) -> Result<Prepared> {
    prepare_filtered(job, curves, options, exclusions, |_, _, _| Ok(true))
}

fn prepare_filtered(
    job: &Job,
    curves: &HashMap<String, Outline>,
    options: Options,
    exclusions: &HashMap<String, Vec<Exclusion>>,
    mut accept: impl FnMut(&str, usize, &[Path]) -> Result<bool>,
) -> Result<Prepared> {
    options.validate()?;
    ensure!(
        exclusions
            .keys()
            .all(|id| job.parts.iter().any(|part| &part.id == id)),
        "lead attachment exclusions refer to an unknown part"
    );
    let mut collision_job = job.clone();
    let mut plans = vec![];
    for (part, enlarged) in job.parts.iter().zip(&mut collision_job.parts) {
        ensure!(
            part.geometry.len() == 1,
            "lead planning needs exact cutting contours for a multi-component rigid unit"
        );
        ensure!(
            part.geometry[0].outer.len() >= 3
                && part.geometry[0].holes.iter().all(|ring| ring.len() >= 3),
            "lead source rings need at least three points"
        );
        let outline = curves
            .get(&part.id)
            .cloned()
            .unwrap_or_else(|| Outline::from_polygon(&part.geometry[0]));
        let scale = Affine::scale(job.units.to_mm());
        let contours: Vec<_> = std::iter::once(&outline.outer)
            .chain(&outline.holes)
            .map(|c| c.transformed(&scale))
            .collect();
        ensure!(
            contours.len() == 1 + part.geometry[0].holes.len(),
            "source contour count differs from the part geometry"
        );
        let polygon = Polygon {
            outer: contours[0].flatten(leads::ENVELOPE_TOLERANCE_MM)?,
            holes: contours[1..]
                .iter()
                .map(|c| c.flatten(leads::ENVELOPE_TOLERANCE_MM))
                .collect::<Result<_>>()?,
        };
        let body = Footprint::new(&polygon, Units::Mm, RigidTransform::default())?;
        let owner = leads::Owner::new(body.clone(), options.kerf_mm)?;
        let mut original = part.geometry[0].clone();
        for p in original
            .outer
            .iter_mut()
            .chain(original.holes.iter_mut().flatten())
        {
            *p = mul(*p, job.units.to_mm());
        }
        let mut combined = body.union(&Footprint::new(
            &original,
            Units::Mm,
            RigidTransform::default(),
        )?)?;
        let mut previous: Vec<Footprint> = vec![];
        let mut plan = PartPlan {
            part_id: part.id.clone(),
            contour_count: contours.len(),
            reservations: vec![],
            flags: vec![],
        };
        for (index, c) in contours.iter().enumerate() {
            ensure!(
                sub(c.start, c.end()).iter().all(|v| v.abs() <= 1e-8),
                "lead contours must be closed"
            );
            let area = signed_area(&c.flatten(leads::ENVELOPE_TOLERANCE_MM)?);
            ensure!(
                area.is_finite() && area.abs() > EPS,
                "lead contour has no area"
            );
            let winding = area.signum();
            let hole = index > 0;
            let side = if hole { winding } else { -winding };
            let angle = if hole {
                options.hole_angle_degrees
            } else {
                options.outer_angle_degrees
            };
            let perimeter: f64 = c
                .segments
                .iter()
                .enumerate()
                .map(|(i, s)| length::segment(from(c, i), s))
                .sum();
            if let Some(spans) = exclusions.get(&part.id) {
                ensure!(
                    spans.iter().all(|s| s.contour_index < contours.len()
                        && s.from_mm.is_finite()
                        && s.to_mm.is_finite()
                        && s.from_mm >= 0.0
                        && s.to_mm >= s.from_mm),
                    "invalid lead attachment exclusion"
                );
            }
            let mut reservation = None;
            for candidate in candidates(c, hole, winding)? {
                if exclusions.get(&part.id).is_some_and(|spans| {
                    spans.iter().any(|span| {
                        span.contour_index == index
                            && ((candidate.distance + crate::common_line::COLLINEAR_MM
                                >= span.from_mm
                                && candidate.distance
                                    <= span.to_mm + crate::common_line::COLLINEAR_MM)
                                || (candidate.distance
                                    + perimeter
                                    + crate::common_line::COLLINEAR_MM
                                    >= span.from_mm
                                    && candidate.distance + perimeter
                                        <= span.to_mm + crate::common_line::COLLINEAR_MM))
                    })
                }) {
                    continue;
                }
                let start = candidate.start;
                let attachment = c.segments[start.segment]
                    .split_at(from(c, start.segment), start.parameter)?
                    .0
                    .end();
                let forward = tangent(c, start.segment, start.parameter)?;
                let reverse = if start.parameter == 0.0 {
                    mul(
                        tangent(
                            c,
                            (start.segment + c.segments.len() - 1) % c.segments.len(),
                            1.0,
                        )?,
                        -1.0,
                    )
                } else {
                    mul(forward, -1.0)
                };
                let mut len = if matches!(options.style, Style::Line) {
                    options.length_mm.min(candidate.cap)
                } else {
                    options.length_mm
                };
                while len + EPS >= MIN_LENGTH_MM {
                    // LightBurn 2.1.01 accepts tenths of a millimetre here.
                    // Round down before constructing either direction, so its
                    // native setting cannot round up beyond the reservation.
                    let actual = (len * 10.0 + EPS).floor() / 10.0;
                    if actual < MIN_LENGTH_MM {
                        break;
                    }
                    let paths = vec![
                        path(attachment, forward, side, actual, angle, options.style)?,
                        path(attachment, reverse, -side, actual, angle, options.style)?,
                    ];
                    let shape = leads::footprint(&paths, options.kerf_mm)?;
                    if owner.fits(&paths)?
                        && previous
                            .iter()
                            .map(|p| shape.compare(p, 0.0))
                            .collect::<Result<Vec<_>>>()?
                            .iter()
                            .all(|p| p.overlap_area == 0.0)
                        && accept(&part.id, index, &paths)?
                    {
                        reservation = Some((
                            Reservation {
                                contour_index: index,
                                start,
                                length_mm: actual,
                                shortened: actual < options.length_mm - EPS,
                                paths,
                            },
                            shape,
                        ));
                        break;
                    }
                    if len <= MIN_LENGTH_MM + EPS {
                        break;
                    }
                    len = (len * 0.9).max(MIN_LENGTH_MM);
                }
                if reservation.is_some() {
                    break;
                }
            }
            if let Some((lead, shape)) = reservation {
                combined = combined.union(&shape)?;
                previous.push(shape);
                plan.reservations.push(lead);
            } else {
                plan.flags.push(Flag {
                    contour_index: index,
                    reason: "Could not reserve a waste-side lead of at least 0.5 mm at the candidate starts; check the geometry, kerf, neighbouring leads and shared-edge exclusions".into(),
                });
            }
        }
        enlarged.geometry = combined
            .polygons()?
            .into_iter()
            .map(|mut polygon| {
                for p in polygon
                    .outer
                    .iter_mut()
                    .chain(polygon.holes.iter_mut().flatten())
                {
                    *p = mul(*p, 1.0 / job.units.to_mm());
                }
                polygon
            })
            .collect();
        plans.push(plan);
    }
    Ok(Prepared {
        collision_job,
        parts: plans,
        kerf_mm: options.kerf_mm,
    })
}
