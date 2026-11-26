//! Exact source curves for import and export. Nesting works on flattened
//! polygons; exports transform these original segments instead, so arcs,
//! Béziers and splines survive a layout unchanged apart from the rigid move.
use std::f64::consts::{PI, TAU};

use anyhow::{Result, ensure};
use nestbolt_validator::RigidTransform;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

mod starts;

pub type Point = [f64; 2];

/// One boundary segment, always in millimetres or the job's declared units.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Segment {
    Line {
        to: Point,
    },
    /// Elliptical arc in centre form: `center + R(rotation) (rx cos t, ry sin t)`
    /// for `t` from `start` to `start + sweep` (radians; positive is
    /// counter-clockwise in a Y-up frame).
    Arc {
        center: Point,
        radii: [f64; 2],
        rotation: f64,
        start: f64,
        sweep: f64,
    },
    Quad {
        control: Point,
        to: Point,
    },
    Cubic {
        controls: [Point; 2],
        to: Point,
    },
}

/// A closed boundary: a start point and segments that end where it began.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize, JsonSchema)]
pub struct Contour {
    pub start: Point,
    pub segments: Vec<Segment>,
}

/// A rigid or reflecting affine map used for exports and unit scaling.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Affine {
    pub m: [[f64; 2]; 2],
    pub t: Point,
}

impl Affine {
    pub const IDENTITY: Self = Self {
        m: [[1.0, 0.0], [0.0, 1.0]],
        t: [0.0, 0.0],
    };

    pub fn scale(s: f64) -> Self {
        Self {
            m: [[s, 0.0], [0.0, s]],
            t: [0.0, 0.0],
        }
    }

    /// The placement contract: optional mirror across Y, rotation, translation.
    pub fn placement(transform: &RigidTransform) -> Self {
        let (s, c) = transform.rotation_radians.sin_cos();
        let m = if transform.mirrored {
            [[-c, -s], [-s, c]]
        } else {
            [[c, -s], [s, c]]
        };
        Self {
            m,
            t: transform.translation,
        }
    }

    /// `next` applied after `self`.
    pub fn then(self, next: Self) -> Self {
        let m = |r: usize, c: usize| next.m[r][0] * self.m[0][c] + next.m[r][1] * self.m[1][c];
        Self {
            m: [[m(0, 0), m(0, 1)], [m(1, 0), m(1, 1)]],
            t: next.apply(self.t),
        }
    }

    pub fn apply(&self, p: Point) -> Point {
        [
            self.m[0][0] * p[0] + self.m[0][1] * p[1] + self.t[0],
            self.m[1][0] * p[0] + self.m[1][1] * p[1] + self.t[1],
        ]
    }

    pub fn determinant(&self) -> f64 {
        self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0]
    }
}

fn lerp(a: Point, b: Point, t: f64) -> Point {
    [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]
}

fn distance(a: Point, b: Point) -> f64 {
    (a[0] - b[0]).hypot(a[1] - b[1])
}

fn point_segment_distance(p: Point, a: Point, b: Point) -> f64 {
    let d = [b[0] - a[0], b[1] - a[1]];
    let len2 = d[0] * d[0] + d[1] * d[1];
    if len2 == 0.0 {
        return distance(p, a);
    }
    let t = (((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / len2).clamp(0.0, 1.0);
    distance(p, lerp(a, b, t))
}

fn mid(a: Point, b: Point) -> Point {
    [(a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0]
}

fn bezier_length(points: &[Point], tolerance: f64, depth: u8) -> f64 {
    let chord = distance(points[0], *points.last().expect("bezier points"));
    let polygon: f64 = points.windows(2).map(|p| distance(p[0], p[1])).sum();
    if polygon - chord <= 2.0 * tolerance || depth == 0 {
        return (polygon + chord) / 2.0;
    }
    let mut levels = points.to_vec();
    let mut left = vec![points[0]];
    let mut right = vec![*points.last().expect("bezier points")];
    while levels.len() > 1 {
        levels = levels.windows(2).map(|p| mid(p[0], p[1])).collect();
        left.push(levels[0]);
        right.push(*levels.last().expect("bezier levels"));
    }
    right.reverse();
    bezier_length(&left, tolerance / 2.0, depth - 1)
        + bezier_length(&right, tolerance / 2.0, depth - 1)
}

fn simpson(f: &impl Fn(f64) -> f64, a: f64, b: f64, tolerance: f64, depth: u8) -> f64 {
    let m = (a + b) / 2.0;
    let l = (a + m) / 2.0;
    let r = (m + b) / 2.0;
    let (fa, fm, fb) = (f(a), f(m), f(b));
    let whole = (b - a) * (fa + 4.0 * fm + fb) / 6.0;
    let halves = (b - a) * (fa + 4.0 * f(l) + 2.0 * fm + 4.0 * f(r) + fb) / 12.0;
    if (halves - whole).abs() <= 15.0 * tolerance || depth == 0 {
        halves + (halves - whole) / 15.0
    } else {
        simpson(f, a, m, tolerance / 2.0, depth - 1) + simpson(f, m, b, tolerance / 2.0, depth - 1)
    }
}

impl Segment {
    /// Exact arc length of this segment starting at `from`. Lines and circular
    /// arcs are analytic; Béziers use adaptive de Casteljau bounds, and
    /// elliptical arcs use adaptive Simpson quadrature.
    pub fn length(&self, from: Point) -> f64 {
        const TOL: f64 = 1e-7;
        match self {
            Segment::Line { to } => distance(from, *to),
            Segment::Quad { control, to } => bezier_length(&[from, *control, *to], TOL, 24),
            Segment::Cubic { controls, to } => {
                bezier_length(&[from, controls[0], controls[1], *to], TOL, 24)
            }
            Segment::Arc {
                radii,
                start,
                sweep,
                ..
            } => {
                if (radii[0] - radii[1]).abs() < 1e-12 {
                    return radii[0].abs() * sweep.abs();
                }
                let speed = |t: f64| {
                    let a = start + sweep * t;
                    (radii[0] * a.sin()).hypot(radii[1] * a.cos()) * sweep.abs()
                };
                (0..8)
                    .map(|i| simpson(&speed, i as f64 / 8.0, (i + 1) as f64 / 8.0, TOL / 8.0, 24))
                    .sum()
            }
        }
    }

    pub fn end(&self) -> Point {
        match self {
            Segment::Line { to } | Segment::Quad { to, .. } | Segment::Cubic { to, .. } => *to,
            Segment::Arc { .. } => self.arc_point(1.0),
        }
    }

    fn arc_point(&self, f: f64) -> Point {
        let Segment::Arc {
            center,
            radii,
            rotation,
            start,
            sweep,
        } = self
        else {
            unreachable!("arc_point on a non-arc")
        };
        let t = start + sweep * f;
        let (s, c) = rotation.sin_cos();
        let (x, y) = (radii[0] * t.cos(), radii[1] * t.sin());
        [center[0] + c * x - s * y, center[1] + s * x + c * y]
    }

    /// Transform exactly. Line and Bézier control points map directly; an
    /// elliptical arc keeps its centre form, with the parameter direction
    /// reversed under reflection.
    pub fn transformed(&self, a: &Affine) -> Segment {
        match self {
            Segment::Line { to } => Segment::Line { to: a.apply(*to) },
            Segment::Quad { control, to } => Segment::Quad {
                control: a.apply(*control),
                to: a.apply(*to),
            },
            Segment::Cubic { controls, to } => Segment::Cubic {
                controls: [a.apply(controls[0]), a.apply(controls[1])],
                to: a.apply(*to),
            },
            Segment::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } => {
                // Map the ellipse axes; similarity transforms keep them orthogonal.
                let (s, c) = rotation.sin_cos();
                let ax = [a.m[0][0] * c + a.m[0][1] * s, a.m[1][0] * c + a.m[1][1] * s];
                let ay = [
                    -a.m[0][0] * s + a.m[0][1] * c,
                    -a.m[1][0] * s + a.m[1][1] * c,
                ];
                let sx = ax[0].hypot(ax[1]);
                let sy = ay[0].hypot(ay[1]);
                let new_rotation = ax[1].atan2(ax[0]);
                let flip = a.determinant() < 0.0;
                Segment::Arc {
                    center: a.apply(*center),
                    radii: [radii[0] * sx, radii[1] * sy],
                    rotation: new_rotation,
                    start: if flip { -start } else { *start },
                    sweep: if flip { -sweep } else { *sweep },
                }
            }
        }
    }

    /// Points after `from` (excluding it) within `tolerance` of the curve.
    pub fn flatten(&self, from: Point, tolerance: f64, out: &mut Vec<Point>) -> Result<()> {
        ensure!(tolerance > 0.0, "flattening tolerance must be positive");
        match self {
            Segment::Line { to } => out.push(*to),
            Segment::Arc { radii, sweep, .. } => {
                let radius = radii[0].abs().max(radii[1].abs());
                let step = if radius <= tolerance {
                    PI
                } else {
                    2.0 * (1.0 - tolerance / radius).clamp(-1.0, 1.0).acos()
                };
                let count = (sweep.abs() / step).ceil().max(1.0);
                ensure!(count <= 100_000.0, "arc needs too many subdivisions");
                let count = count as usize;
                for i in 1..=count {
                    out.push(self.arc_point(i as f64 / count as f64));
                }
            }
            Segment::Quad { control, to } => {
                let c1 = lerp(from, *control, 2.0 / 3.0);
                let c2 = lerp(*to, *control, 2.0 / 3.0);
                flatten_cubic([from, c1, c2, *to], tolerance, 0, out)?;
            }
            Segment::Cubic { controls, to } => {
                flatten_cubic([from, controls[0], controls[1], *to], tolerance, 0, out)?;
            }
        }
        Ok(())
    }
}

/// Subdivide until every control point lies within `tolerance` of the chord;
/// convexity then bounds the curve within the same capsule.
fn flatten_cubic(p: [Point; 4], tolerance: f64, depth: u32, out: &mut Vec<Point>) -> Result<()> {
    if point_segment_distance(p[1], p[0], p[3]).max(point_segment_distance(p[2], p[0], p[3]))
        <= tolerance
    {
        out.push(p[3]);
        return Ok(());
    }
    ensure!(depth < 40, "curve subdivision did not converge");
    let ab = lerp(p[0], p[1], 0.5);
    let bc = lerp(p[1], p[2], 0.5);
    let cd = lerp(p[2], p[3], 0.5);
    let abc = lerp(ab, bc, 0.5);
    let bcd = lerp(bc, cd, 0.5);
    let mid = lerp(abc, bcd, 0.5);
    flatten_cubic([p[0], ab, abc, mid], tolerance, depth + 1, out)?;
    flatten_cubic([mid, bcd, cd, p[3]], tolerance, depth + 1, out)
}

impl Contour {
    pub fn transformed(&self, a: &Affine) -> Contour {
        Contour {
            start: a.apply(self.start),
            segments: self.segments.iter().map(|s| s.transformed(a)).collect(),
        }
    }

    /// Closed polygon (without a repeated last point) within `tolerance`.
    pub fn flatten(&self, tolerance: f64) -> Result<Vec<Point>> {
        let mut points = vec![self.start];
        let mut from = self.start;
        for segment in &self.segments {
            segment.flatten(from, tolerance, &mut points)?;
            from = segment.end();
        }
        if points.len() > 1 && distance(points[0], *points.last().expect("points")) <= tolerance {
            points.pop();
        }
        points.dedup_by(|a, b| distance(*a, *b) == 0.0);
        ensure!(
            points.len() >= 3,
            "contour has fewer than three distinct points"
        );
        Ok(points)
    }

    pub fn end(&self) -> Point {
        self.segments.last().map_or(self.start, Segment::end)
    }

    /// Total exact arc length along all segments of this contour.
    pub fn length(&self) -> f64 {
        let mut from = self.start;
        let mut total = 0.0;
        for segment in &self.segments {
            total += segment.length(from);
            from = segment.end();
        }
        total
    }
}

/// Signed shoelace area; positive is counter-clockwise in a Y-up frame.
pub fn signed_area(points: &[Point]) -> f64 {
    let mut area = 0.0;
    for i in 0..points.len() {
        let a = points[i];
        let b = points[(i + 1) % points.len()];
        area += a[0] * b[1] - b[0] * a[1];
    }
    area / 2.0
}

pub fn bounds(points: &[Point]) -> [f64; 4] {
    points.iter().fold(
        [
            f64::INFINITY,
            f64::INFINITY,
            f64::NEG_INFINITY,
            f64::NEG_INFINITY,
        ],
        |b, p| {
            [
                b[0].min(p[0]),
                b[1].min(p[1]),
                b[2].max(p[0]),
                b[3].max(p[1]),
            ]
        },
    )
}

/// Even-odd point-in-polygon test.
pub fn contains(polygon: &[Point], p: Point) -> bool {
    let mut inside = false;
    let mut j = polygon.len() - 1;
    for i in 0..polygon.len() {
        let (a, b) = (polygon[i], polygon[j]);
        if (a[1] > p[1]) != (b[1] > p[1])
            && p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]
        {
            inside = !inside;
        }
        j = i;
    }
    inside
}

/// Net area of a polygon with holes.
pub fn polygon_area(polygon: &nestbolt_validator::Polygon) -> f64 {
    signed_area(&polygon.outer).abs()
        - polygon
            .holes
            .iter()
            .map(|h| signed_area(h).abs())
            .sum::<f64>()
}

/// Whether the part's bounding box fits the stock's usable rectangle at some
/// allowed rotation (free rotation sampled every half degree). Used only to
/// warn about impossible parts; a fit here is no placement guarantee.
pub fn fits_somehow(
    part: &nestbolt_validator::job::Part,
    stock: &nestbolt_validator::job::Stock,
) -> bool {
    use nestbolt_validator::job::Rotations;
    let w = stock.width - stock.margins.left - stock.margins.right;
    let h = stock.height - stock.margins.bottom - stock.margins.top;
    let angles: Vec<f64> = match &part.rotations {
        Rotations::Free => (0..720).map(|i| f64::from(i) * 0.5).collect(),
        Rotations::List { degrees } => degrees.clone(),
        Rotations::Step { degrees } => (0..(360.0 / degrees).ceil() as u32)
            .map(|i| f64::from(i) * degrees)
            .collect(),
    };
    let points: Vec<Point> = part
        .geometry
        .iter()
        .flat_map(|g| g.outer.iter().copied())
        .collect();
    angles.iter().any(|a| {
        let (s, c) = a.to_radians().sin_cos();
        let rotated: Vec<Point> = points
            .iter()
            .map(|p| [c * p[0] - s * p[1], s * p[0] + c * p[1]])
            .collect();
        let b = bounds(&rotated);
        b[2] - b[0] <= w * 1.000001 && b[3] - b[1] <= h * 1.000001
    })
}

/// Normalise an angle to [0, 2π).
pub fn normalize(angle: f64) -> f64 {
    angle.rem_euclid(TAU)
}

/// Symmetric Hausdorff distance between two dense point samples, by brute
/// force over segments. Used by the import/export fidelity tests.
pub fn hausdorff(a: &[Point], b: &[Point]) -> f64 {
    let directed = |from: &[Point], to: &[Point]| {
        from.iter()
            .map(|&p| {
                (0..to.len())
                    .map(|i| point_segment_distance(p, to[i], to[(i + 1) % to.len()]))
                    .fold(f64::INFINITY, f64::min)
            })
            .fold(0.0, f64::max)
    };
    directed(a, b).max(directed(b, a))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn circle() -> Contour {
        Contour {
            start: [12.0, 2.0],
            segments: vec![Segment::Arc {
                center: [2.0, 2.0],
                radii: [10.0, 10.0],
                rotation: 0.0,
                start: 0.0,
                sweep: TAU,
            }],
        }
    }

    #[test]
    fn flattened_circle_stays_within_tolerance() {
        let points = circle().flatten(0.001).unwrap();
        for p in &points {
            assert!((distance(*p, [2.0, 2.0]) - 10.0).abs() < 1e-9);
        }
        // Chord midpoints sag by at most the tolerance.
        for i in 0..points.len() {
            let m = lerp(points[i], points[(i + 1) % points.len()], 0.5);
            assert!(10.0 - distance(m, [2.0, 2.0]) <= 0.001 + 1e-12);
        }
        assert!((signed_area(&points) - PI * 100.0).abs() < 0.05);
    }

    #[test]
    fn transformed_arcs_match_transformed_samples() {
        let arc = Segment::Arc {
            center: [1.0, -2.0],
            radii: [6.0, 3.0],
            rotation: 0.4,
            start: 0.3,
            sweep: -2.1,
        };
        for transform in [
            RigidTransform {
                translation: [5.0, 7.0],
                rotation_radians: 1.1,
                mirrored: false,
            },
            RigidTransform {
                translation: [-3.0, 2.0],
                rotation_radians: 2.7,
                mirrored: true,
            },
        ] {
            let a = Affine::placement(&transform);
            let moved = arc.transformed(&a);
            for i in 0..=8 {
                let f = f64::from(i) / 8.0;
                let expected = a.apply(arc.arc_point(f));
                let actual = moved.arc_point(f);
                assert!(distance(expected, actual) < 1e-9, "{expected:?} {actual:?}");
            }
        }
    }

    #[test]
    fn cubic_flattening_converges_and_bounds_error() {
        let contour = Contour {
            start: [0.0, 0.0],
            segments: vec![
                Segment::Cubic {
                    controls: [[0.0, 10.0], [10.0, 10.0]],
                    to: [10.0, 0.0],
                },
                Segment::Line { to: [0.0, 0.0] },
            ],
        };
        let coarse = contour.flatten(0.01).unwrap();
        let fine = contour.flatten(0.0001).unwrap();
        assert!(hausdorff(&coarse, &fine) <= 0.0101);
    }
}
