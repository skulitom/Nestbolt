//! Independent geometry primitives. No jagua-rs, Sparrow or geo dependency.
//!
//! This is the kernel for the M1 validator, not yet a complete job/layout checker.
//! Inputs are f64 source polygons; transforms are rebuilt here, never accepted as
//! pre-transformed solver geometry. Clipper2 uses a one-nanometre integer grid in
//! physical jobs (1e-6 mm), or 1e-6 coordinate units for unitless benchmarks.

use anyhow::{Result, ensure};
use clipper2_rust::{
    ClipType, Clipper64, ClipperOffset, EndType, FillRule, JoinType, Path64, Paths64, Point64,
    PolyTree64,
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

pub mod job;
pub mod leads;
pub mod sparrow;

#[cfg(test)]
mod distance_tests;

const SCALE: f64 = 1_000_000.0;
pub const GRID: f64 = 1.0 / SCALE;
pub const MAX_COORDINATE: f64 = 10_000_000.0;
const MAX_VERTICES: usize = 10_000;
pub const BACKEND: &str = "clipper2-rust 1.2.0";

#[derive(Clone, Copy, Debug, Deserialize, Serialize, PartialEq, Eq, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum Units {
    Mm,
    Inch,
    Unitless,
}

impl Units {
    pub fn to_mm(self) -> f64 {
        match self {
            Self::Inch => 25.4,
            Self::Mm | Self::Unitless => 1.0,
        }
    }
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Polygon {
    pub outer: Vec<[f64; 2]>,
    #[serde(default)]
    pub holes: Vec<Vec<[f64; 2]>>,
}

/// Mirror about the local Y axis, then rotate about the origin, then translate.
/// Coordinates and translation use the caller's declared units.
#[derive(Clone, Copy, Debug, Default, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct RigidTransform {
    pub translation: [f64; 2],
    pub rotation_radians: f64,
    pub mirrored: bool,
}

#[derive(Clone, Debug)]
pub struct Footprint {
    paths: Paths64,
    area: f64,
    bounds: [f64; 4],
    units: Units,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct PairCheck {
    /// mm² for physical units; squared model units for unitless jobs.
    pub overlap_area: f64,
    /// Intersection divided by the smaller part's net area.
    pub overlap_ratio: f64,
    pub clearance_violation: bool,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct ContainmentCheck {
    pub outside_area: f64,
    pub outside_ratio: f64,
    pub clearance_violation: bool,
}

/// One immutable original footprint and clearance, reused across its neighbours.
/// The offset is created only if a close, non-overlapping pair needs it and is
/// dropped after that footprint's comparisons. It never contains solver geometry.
struct PairQuery<'a> {
    source: &'a Footprint,
    clearance: f64,
    expanded: Option<Paths64>,
}

impl PairQuery<'_> {
    fn compare(&mut self, other: &Footprint) -> Result<PairCheck> {
        let source = self.source;
        source.check_clearance(other, self.clearance)?;
        let gap = self.clearance * source.units.to_mm();
        if bounds_distance(source.bounds, other.bounds) > gap + 2.0 * GRID {
            return Ok(PairCheck {
                overlap_area: 0.0,
                overlap_ratio: 0.0,
                clearance_violation: false,
            });
        }
        let overlap_area = area(&boolean(
            &source.paths,
            &other.paths,
            ClipType::Intersection,
        )?);
        let clearance_violation = if gap > 0.0 {
            if overlap_area > 0.0 {
                true
            } else {
                if self.expanded.is_none() {
                    self.expanded = Some(clearance_envelope(&source.paths, gap)?);
                }
                let possible = !boolean(
                    self.expanded.as_ref().expect("offset prepared"),
                    &other.paths,
                    ClipType::Intersection,
                )?
                .is_empty();
                possible && boundary_distance(&source.paths, &other.paths) + 2.0 * GRID < gap
            }
        } else {
            false
        };
        Ok(PairCheck {
            overlap_area,
            overlap_ratio: overlap_area / source.area.min(other.area),
            clearance_violation,
        })
    }
}

impl Footprint {
    /// Multiple rigid components belonging to one part or stock outline.
    /// Components may lie inside other components' holes but cannot overlap.
    pub fn from_polygons(
        polygons: &[Polygon],
        units: Units,
        transform: RigidTransform,
    ) -> Result<Self> {
        ensure!(!polygons.is_empty(), "geometry needs at least one polygon");
        let mut components: Vec<Self> = vec![];
        for polygon in polygons {
            let next = Self::new(polygon, units, transform)?;
            for previous in &components {
                ensure!(
                    next.compare(previous, 0.0)?.overlap_area == 0.0,
                    "components of the same geometry overlap"
                );
            }
            components.push(next);
        }
        let paths = components.into_iter().flat_map(|c| c.paths).collect();
        Self::from_paths(paths, units).ok_or_else(|| anyhow::anyhow!("geometry has no area"))
    }

    /// Intersection for building a usable sheet from stock outlines and margins.
    pub fn intersection(&self, other: &Self) -> Result<Option<Self>> {
        self.check_clearance(other, 0.0)?;
        Ok(Self::from_paths(
            boolean(&self.paths, &other.paths, ClipType::Intersection)?,
            self.units,
        ))
    }

    /// Subtraction for explicitly declared sheet defects, including overlapping ones.
    pub fn subtract(&self, other: &Self) -> Result<Option<Self>> {
        self.check_clearance(other, 0.0)?;
        Ok(Self::from_paths(
            boolean(&self.paths, &other.paths, ClipType::Difference)?,
            self.units,
        ))
    }

    /// Union touching or overlapping allowance components without double-counting
    /// their area. Both operands must use the same declared coordinate units.
    pub fn union(&self, other: &Self) -> Result<Self> {
        self.check_clearance(other, 0.0)?;
        Self::from_paths(
            boolean(&self.paths, &other.paths, ClipType::Union)?,
            self.units,
        )
        .ok_or_else(|| anyhow::anyhow!("geometry union has no area"))
    }

    /// Canonical non-overlapping components, in the original declared units.
    /// Islands inside holes are separate components, retaining their own holes.
    pub fn polygons(&self) -> Result<Vec<Polygon>> {
        let mut engine = Clipper64::new();
        engine.add_subject(&self.paths);
        let mut tree = PolyTree64::new();
        ensure!(
            engine.execute_tree(ClipType::Union, FillRule::NonZero, &mut tree, &mut vec![])
                && engine.error_code() == 0,
            "geometry union topology failed"
        );
        let scale = SCALE * self.units.to_mm();
        let ring = |i: usize| {
            tree.nodes[i]
                .polygon()
                .iter()
                .map(|p| [p.x as f64 / scale, p.y as f64 / scale])
                .collect()
        };
        Ok((1..tree.nodes.len())
            .filter(|&i| !tree.is_hole(i))
            .map(|i| Polygon {
                outer: ring(i),
                holes: tree.nodes[i].children().iter().map(|&j| ring(j)).collect(),
            })
            .collect())
    }

    pub(crate) fn boundary_tolerance(&self) -> Result<Self> {
        let mut engine = ClipperOffset::new(2.0, 0.0, false, false);
        engine.add_paths(&self.paths, JoinType::Miter, EndType::Polygon);
        let mut paths = vec![];
        engine.execute(2.0, &mut paths);
        ensure!(
            engine.error_code() == 0,
            "container tolerance offset failed"
        );
        Self::from_paths(paths, self.units)
            .ok_or_else(|| anyhow::anyhow!("container tolerance offset collapsed"))
    }

    fn from_paths(paths: Paths64, units: Units) -> Option<Self> {
        let area = area(&paths);
        if area <= 0.0 {
            return None;
        }
        let mut bounds = [
            f64::INFINITY,
            f64::INFINITY,
            f64::NEG_INFINITY,
            f64::NEG_INFINITY,
        ];
        for point in paths.iter().flatten() {
            let (x, y) = (point.x as f64 / SCALE, point.y as f64 / SCALE);
            bounds[0] = bounds[0].min(x);
            bounds[1] = bounds[1].min(y);
            bounds[2] = bounds[2].max(x);
            bounds[3] = bounds[3].max(y);
        }
        Some(Self {
            paths,
            area,
            bounds,
            units,
        })
    }

    pub fn new(polygon: &Polygon, units: Units, transform: RigidTransform) -> Result<Self> {
        ensure!(
            transform.translation.iter().all(|x| x.is_finite())
                && transform.rotation_radians.is_finite(),
            "transform must be finite"
        );
        ensure!(
            transform.rotation_radians.abs() <= 1e8,
            "rotation exceeds supported numerical range"
        );
        ensure!(
            polygon.outer.len() + polygon.holes.iter().map(Vec::len).sum::<usize>() <= MAX_VERTICES,
            "polygon exceeds {MAX_VERTICES} vertices"
        );
        let outer = make_ring(&polygon.outer, units, transform, true)?;
        let mut paths = vec![outer];
        for points in &polygon.holes {
            let hole = make_ring(points, units, transform, false)?;
            ensure!(
                area(&boolean(
                    &vec![hole.clone()],
                    &vec![paths[0].clone()],
                    ClipType::Difference
                )?) == 0.0,
                "hole extends outside its outer ring"
            );
            ensure!(
                boundary_distance(&vec![hole.clone()], &vec![paths[0].clone()]) > 0.0,
                "hole touches its outer ring"
            );
            for previous in paths.iter().skip(1) {
                ensure!(
                    area(&boolean(
                        &vec![hole.clone()],
                        &vec![previous.clone()],
                        ClipType::Intersection
                    )?) == 0.0
                        && boundary_distance(&vec![hole.clone()], &vec![previous.clone()]) > 0.0,
                    "holes overlap, touch or contain one another"
                );
            }
            paths.push(hole);
        }
        let area = area(&paths);
        ensure!(
            area > 0.0,
            "polygon has no solid area at validator precision"
        );
        let mut bounds = [
            f64::INFINITY,
            f64::INFINITY,
            f64::NEG_INFINITY,
            f64::NEG_INFINITY,
        ];
        for point in &paths[0] {
            let x = point.x as f64 / SCALE;
            let y = point.y as f64 / SCALE;
            bounds[0] = bounds[0].min(x);
            bounds[1] = bounds[1].min(y);
            bounds[2] = bounds[2].max(x);
            bounds[3] = bounds[3].max(y);
        }
        Ok(Self {
            paths,
            area,
            bounds,
            units,
        })
    }

    pub fn area(&self) -> f64 {
        self.area
    }
    pub fn bounds(&self) -> [f64; 4] {
        self.bounds
    }

    /// Clearance is in the declared input units. Contact at zero clearance is
    /// permitted. Positive clearance uses offset polygons and a segment-distance
    /// confirmation, with a two-grid-unit tolerance for integer quantisation.
    pub fn compare(&self, other: &Self, clearance: f64) -> Result<PairCheck> {
        self.pair_query(clearance).compare(other)
    }

    fn pair_query(&self, clearance: f64) -> PairQuery<'_> {
        PairQuery {
            source: self,
            clearance,
            expanded: None,
        }
    }

    /// The container polygon may include holes representing keep-out regions.
    pub fn inside(&self, container: &Self, clearance: f64) -> Result<ContainmentCheck> {
        self.check_clearance(container, clearance)?;
        let gap = clearance * self.units.to_mm();
        let outside_area = area(&boolean(
            &self.paths,
            &container.paths,
            ClipType::Difference,
        )?);
        let clearance_violation = if gap > 0.0 {
            if outside_area > 0.0 {
                true
            } else {
                let expanded = clearance_envelope(&self.paths, gap)?;
                let possible =
                    !boolean(&expanded, &container.paths, ClipType::Difference)?.is_empty();
                possible && boundary_distance(&self.paths, &container.paths) + 2.0 * GRID < gap
            }
        } else {
            false
        };
        Ok(ContainmentCheck {
            outside_area,
            outside_ratio: outside_area / self.area,
            clearance_violation,
        })
    }

    fn check_clearance(&self, other: &Self, clearance: f64) -> Result<()> {
        ensure!(
            self.units == other.units,
            "cannot compare different declared units"
        );
        ensure!(
            clearance.is_finite()
                && clearance >= 0.0
                && clearance * self.units.to_mm() <= MAX_COORDINATE,
            "clearance is outside the supported range"
        );
        Ok(())
    }
}

fn boolean(subject: &Paths64, clip: &Paths64, operation: ClipType) -> Result<Paths64> {
    let mut engine = Clipper64::new();
    engine.add_subject(subject);
    engine.add_clip(clip);
    let mut output = vec![];
    let success = engine.execute(operation, FillRule::NonZero, &mut output, None);
    ensure!(
        success && engine.error_code() == 0,
        "independent polygon operation failed ({})",
        engine.error_code()
    );
    Ok(output)
}

fn clearance_envelope(paths: &Paths64, gap: f64) -> Result<Paths64> {
    // A conservative polygonal envelope is sufficient: exact segment distance
    // confirms every candidate. Relative arc tolerance bounds corner complexity
    // even for very large spacing, while the extra radius covers chord error.
    let arc_tolerance = (gap * SCALE / 1000.0).max(10.0);
    let distance = gap * SCALE + 2.0 * arc_tolerance + 2.0;
    let mut engine = ClipperOffset::new(2.0, arc_tolerance, false, false);
    engine.add_paths(paths, JoinType::Round, EndType::Polygon);
    let mut output = vec![];
    engine.execute(distance, &mut output);
    ensure!(
        engine.error_code() == 0 && !output.is_empty(),
        "independent polygon offset failed ({})",
        engine.error_code()
    );
    Ok(output)
}

fn signed_twice_area(path: &Path64) -> i128 {
    edges(path)
        .map(|(a, b)| i128::from(a.x) * i128::from(b.y) - i128::from(b.x) * i128::from(a.y))
        .sum()
}

fn area(paths: &Paths64) -> f64 {
    paths.iter().map(signed_twice_area).sum::<i128>().abs() as f64 / (2.0 * SCALE * SCALE)
}

fn make_ring(
    points: &[[f64; 2]],
    units: Units,
    transform: RigidTransform,
    positive: bool,
) -> Result<Path64> {
    ensure!(points.len() >= 3, "ring needs at least three points");
    let (sin, cos) = transform.rotation_radians.sin_cos();
    let mut path = vec![];
    for &[x, y] in points {
        ensure!(
            x.is_finite()
                && y.is_finite()
                && x.abs().max(y.abs()) * units.to_mm() <= MAX_COORDINATE,
            "ring coordinates must be finite and within the validator range"
        );
        let x = if transform.mirrored { -x } else { x };
        let x_out = (x * cos - y * sin + transform.translation[0]) * units.to_mm();
        let y_out = (x * sin + y * cos + transform.translation[1]) * units.to_mm();
        ensure!(
            x_out.is_finite()
                && y_out.is_finite()
                && x_out.abs().max(y_out.abs()) <= MAX_COORDINATE,
            "coordinate exceeds validator range"
        );
        let point = Point64::new(
            (x_out * SCALE).round() as i64,
            (y_out * SCALE).round() as i64,
        );
        if path.last() != Some(&point) {
            path.push(point);
        }
    }
    if path.first() == path.last() {
        path.pop();
    }
    ensure!(path.len() >= 3, "ring collapsed at validator precision");
    // Remove redundant points on straight edges, but reject a doubled-back edge.
    loop {
        let mut remove = None;
        for i in 0..path.len() {
            let a = path[(i + path.len() - 1) % path.len()];
            let b = path[i];
            let c = path[(i + 1) % path.len()];
            if cross(a, b, c) == 0 {
                ensure!(between(a, c, b), "ring doubles back along an edge");
                remove = Some(i);
                break;
            }
        }
        match remove {
            Some(i) => {
                path.remove(i);
                ensure!(path.len() >= 3, "ring is collinear");
            }
            None => break,
        }
    }
    let segments: Vec<_> = edges(&path).collect();
    for (i, &(a, b)) in segments.iter().enumerate() {
        for (j, &(c, d)) in segments.iter().enumerate().skip(i + 1) {
            if j == i + 1 || (i == 0 && j == path.len() - 1) {
                continue;
            }
            ensure!(
                !segments_touch(a, b, c, d),
                "ring self-intersects or touches itself"
            );
        }
    }
    let signed = signed_twice_area(&path);
    ensure!(signed != 0, "ring has zero area");
    if (signed > 0) != positive {
        path.reverse();
    }
    Ok(path)
}

fn edges(path: &Path64) -> impl Iterator<Item = (Point64, Point64)> + '_ {
    path.iter()
        .copied()
        .zip(path.iter().copied().cycle().skip(1))
        .take(path.len())
}

fn cross(a: Point64, b: Point64, c: Point64) -> i128 {
    i128::from(b.x - a.x) * i128::from(c.y - a.y) - i128::from(b.y - a.y) * i128::from(c.x - a.x)
}

fn between(a: Point64, b: Point64, p: Point64) -> bool {
    a.x.min(b.x) <= p.x && p.x <= a.x.max(b.x) && a.y.min(b.y) <= p.y && p.y <= a.y.max(b.y)
}

fn segments_touch(a: Point64, b: Point64, c: Point64, d: Point64) -> bool {
    if a.x.max(b.x) < c.x.min(d.x)
        || c.x.max(d.x) < a.x.min(b.x)
        || a.y.max(b.y) < c.y.min(d.y)
        || c.y.max(d.y) < a.y.min(b.y)
    {
        return false;
    }
    let (ab_c, ab_d, cd_a, cd_b) = (
        cross(a, b, c),
        cross(a, b, d),
        cross(c, d, a),
        cross(c, d, b),
    );
    (ab_c == 0 && between(a, b, c))
        || (ab_d == 0 && between(a, b, d))
        || (cd_a == 0 && between(c, d, a))
        || (cd_b == 0 && between(c, d, b))
        || (ab_c.signum() * ab_d.signum() < 0 && cd_a.signum() * cd_b.signum() < 0)
}

fn point_segment_distance(p: Point64, a: Point64, b: Point64) -> f64 {
    let dx = (b.x - a.x) as f64;
    let dy = (b.y - a.y) as f64;
    let px = (p.x - a.x) as f64;
    let py = (p.y - a.y) as f64;
    let t = ((px * dx + py * dy) / (dx * dx + dy * dy)).clamp(0.0, 1.0);
    (px - t * dx).hypot(py - t * dy) / SCALE
}

fn boundary_distance(a: &Paths64, b: &Paths64) -> f64 {
    let mut minimum = f64::INFINITY;
    for (a0, a1) in a.iter().flat_map(edges) {
        for (b0, b1) in b.iter().flat_map(edges) {
            // A segment pair cannot improve the incumbent if its bounding boxes
            // are farther apart on either axis. Coordinates are exact integers;
            // keep two extra grid units to conservatively cover f64 distance
            // rounding within MAX_COORDINATE. Never prune touching boxes.
            let limit = minimum * SCALE + 2.0;
            let dx = (a0.x.min(a1.x) - b0.x.max(b1.x)).max(b0.x.min(b1.x) - a0.x.max(a1.x));
            let dy = (a0.y.min(a1.y) - b0.y.max(b1.y)).max(b0.y.min(b1.y) - a0.y.max(a1.y));
            if dx as f64 > limit || dy as f64 > limit {
                continue;
            }
            if segments_touch(a0, a1, b0, b1) {
                return 0.0;
            }
            minimum = minimum
                .min(point_segment_distance(a0, b0, b1))
                .min(point_segment_distance(a1, b0, b1))
                .min(point_segment_distance(b0, a0, a1))
                .min(point_segment_distance(b1, a0, a1));
        }
    }
    minimum
}

fn bounds_distance(a: [f64; 4], b: [f64; 4]) -> f64 {
    let dx = (a[0] - b[2]).max(b[0] - a[2]).max(0.0);
    let dy = (a[1] - b[3]).max(b[1] - a[3]).max(0.0);
    dx.hypot(dy)
}
