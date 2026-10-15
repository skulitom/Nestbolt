//! Original cutting boundaries, independent of the core curve implementation.
//! Coordinates use the job's units; evaluation and flattening return mm.
use anyhow::{Result, ensure};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::ENVELOPE_TOLERANCE_MM;
use crate::{GRID, MAX_COORDINATE, Polygon, Units};

const MAX_POINTS: usize = 10_000;
type Point = [f64; 2];

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Segment {
    Line {
        to: Point,
    },
    Quad {
        control: Point,
        to: Point,
    },
    Cubic {
        controls: [Point; 2],
        to: Point,
    },
    Arc {
        center: Point,
        radii: Point,
        rotation: f64,
        start: f64,
        sweep: f64,
    },
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Contour {
    pub start: Point,
    pub segments: Vec<Segment>,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Component {
    pub outer: Contour,
    pub holes: Vec<Contour>,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Part {
    pub part_id: String,
    pub components: Vec<Component>,
}

#[derive(Clone, Copy, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Start {
    pub segment: usize,
    pub parameter: f64,
}

fn distance(a: Point, b: Point) -> f64 {
    (a[0] - b[0]).hypot(a[1] - b[1])
}

fn valid_point(p: Point, scale: f64) -> bool {
    p.into_iter()
        .all(|v| v.is_finite() && (v * scale).abs() <= MAX_COORDINATE)
}

fn arc_point(center: Point, radii: Point, rotation: f64, angle: f64) -> Point {
    let (s, c) = rotation.sin_cos();
    let (sa, ca) = angle.sin_cos();
    [
        center[0] + c * radii[0] * ca - s * radii[1] * sa,
        center[1] + s * radii[0] * ca + c * radii[1] * sa,
    ]
}

impl Segment {
    fn validate(&self, from: Point, scale: f64) -> Result<()> {
        let points: &[Point] = match self {
            Self::Line { to } => std::slice::from_ref(to),
            Self::Quad { control, to } => &[*control, *to],
            Self::Cubic { controls, to } => &[controls[0], controls[1], *to],
            Self::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } => {
                ensure!(
                    valid_point(*center, scale)
                        && radii
                            .iter()
                            .all(|r| r.is_finite() && *r > 0.0 && r * scale <= MAX_COORDINATE)
                        && [rotation, start, sweep]
                            .iter()
                            .all(|a| a.is_finite() && a.abs() <= 1e8)
                        && sweep.abs() > 0.0
                        && sweep.abs() <= std::f64::consts::TAU + 1e-9,
                    "invalid original source arc"
                );
                let first = arc_point(*center, *radii, *rotation, *start);
                ensure!(
                    distance(first, from) * scale <= 8.0 * GRID,
                    "disconnected original source arc"
                );
                &[]
            }
        };
        ensure!(
            points.iter().all(|p| valid_point(*p, scale)),
            "invalid original source coordinate"
        );
        ensure!(
            valid_point(self.point(from, 1.0), scale),
            "original source endpoint exceeds range"
        );
        Ok(())
    }

    fn point(&self, from: Point, t: f64) -> Point {
        let u = 1.0 - t;
        match self {
            Self::Line { to } => std::array::from_fn(|k| u * from[k] + t * to[k]),
            Self::Quad { control, to } => {
                std::array::from_fn(|k| u * u * from[k] + 2.0 * u * t * control[k] + t * t * to[k])
            }
            Self::Cubic { controls, to } => std::array::from_fn(|k| {
                u * u * u * from[k]
                    + 3.0 * u * u * t * controls[0][k]
                    + 3.0 * u * t * t * controls[1][k]
                    + t * t * t * to[k]
            }),
            Self::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } => arc_point(*center, *radii, *rotation, start + sweep * t),
        }
    }
}

fn point_segment_distance(p: Point, a: Point, b: Point) -> f64 {
    let d = [b[0] - a[0], b[1] - a[1]];
    let length2 = d[0] * d[0] + d[1] * d[1];
    let t = if length2 == 0.0 {
        0.0
    } else {
        (((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / length2).clamp(0.0, 1.0)
    };
    distance(p, [a[0] + t * d[0], a[1] + t * d[1]])
}

fn append(points: &mut Vec<Point>, point: Point) -> Result<()> {
    ensure!(
        points.len() < MAX_POINTS,
        "original source needs too many independent boundary points"
    );
    ensure!(
        valid_point(point, 1.0),
        "original source boundary exceeds range"
    );
    points.push(point);
    Ok(())
}

fn bezier(points: &mut Vec<Point>, controls: Vec<Point>, depth: u8) -> Result<()> {
    let last = controls[controls.len() - 1];
    // The convex hull bounds distance from the curve to its chord. Splitting
    // also handles collinear backtracking and coincident endpoints.
    let error = controls[1..controls.len() - 1]
        .iter()
        .map(|p| point_segment_distance(*p, controls[0], last))
        .fold(0.0, f64::max);
    if error <= ENVELOPE_TOLERANCE_MM {
        return append(points, last);
    }
    ensure!(depth < 40, "original source subdivision limit exceeded");
    let mut left = vec![controls[0]];
    let mut right = vec![last];
    let mut row = controls;
    while row.len() > 1 {
        row = row
            .windows(2)
            .map(|p| [(p[0][0] + p[1][0]) / 2.0, (p[0][1] + p[1][1]) / 2.0])
            .collect();
        left.push(row[0]);
        right.push(row[row.len() - 1]);
    }
    right.reverse();
    bezier(points, left, depth + 1)?;
    bezier(points, right, depth + 1)
}

impl Contour {
    pub fn from_ring(points: &[Point]) -> Result<Self> {
        ensure!(points.len() >= 3, "original source ring needs three points");
        Ok(Self {
            start: points[0],
            segments: points[1..]
                .iter()
                .chain(std::iter::once(&points[0]))
                .map(|&to| Segment::Line { to })
                .collect(),
        })
    }

    fn check(&self, units: Units) -> Result<()> {
        let scale = units.to_mm();
        ensure!(
            valid_point(self.start, scale)
                && !self.segments.is_empty()
                && self.segments.len() < MAX_POINTS,
            "invalid original source contour"
        );
        let mut from = self.start;
        for segment in &self.segments {
            segment.validate(from, scale)?;
            from = segment.point(from, 1.0);
        }
        ensure!(
            distance(from, self.start) * scale <= 8.0 * GRID,
            "original source contour is not closed"
        );
        Ok(())
    }

    pub fn point_mm(&self, start: Start, units: Units) -> Result<Point> {
        self.check(units)?;
        ensure!(
            start.segment < self.segments.len()
                && start.parameter.is_finite()
                && (0.0..=1.0).contains(&start.parameter),
            "invalid original contour start parameter"
        );
        let mut from = self.start;
        for segment in &self.segments[..start.segment] {
            from = segment.point(from, 1.0);
        }
        Ok(self.segments[start.segment]
            .point(from, start.parameter)
            .map(|v| v * units.to_mm()))
    }

    pub fn flatten_mm(&self, units: Units) -> Result<Vec<Point>> {
        self.check(units)?;
        let scale = units.to_mm();
        let mm = |p: Point| p.map(|v| v * scale);
        let mut points = vec![mm(self.start)];
        let mut from = self.start;
        for segment in &self.segments {
            match segment {
                Segment::Line { to } => append(&mut points, mm(*to))?,
                Segment::Quad { control, to } => {
                    bezier(&mut points, vec![mm(from), mm(*control), mm(*to)], 0)?
                }
                Segment::Cubic { controls, to } => bezier(
                    &mut points,
                    vec![mm(from), mm(controls[0]), mm(controls[1]), mm(*to)],
                    0,
                )?,
                Segment::Arc { radii, sweep, .. } => {
                    // ||p''(t)|| <= max(rx,ry)*sweep²; the chord error is
                    // bounded by max ||p''|| * delta_t² / 8.
                    let count = (sweep.abs()
                        * (radii[0].max(radii[1]) * scale / (8.0 * ENVELOPE_TOLERANCE_MM)).sqrt())
                    .ceil()
                    .max(1.0);
                    ensure!(
                        count.is_finite() && count < MAX_POINTS as f64,
                        "original arc needs too many independent boundary points"
                    );
                    for i in 1..=count as usize {
                        append(&mut points, mm(segment.point(from, i as f64 / count)))?;
                    }
                }
            }
            from = segment.point(from, 1.0);
        }
        // Check above proves closure; one identical seam avoids a microscopic
        // chord caused solely by trig evaluation at a full turn.
        *points.last_mut().unwrap() = points[0];
        points.pop();
        points.dedup();
        ensure!(points.len() >= 3, "original source contour collapsed");
        Ok(points)
    }
}

impl Component {
    pub fn from_polygon(polygon: &Polygon) -> Result<Self> {
        Ok(Self {
            outer: Contour::from_ring(&polygon.outer)?,
            holes: polygon
                .holes
                .iter()
                .map(|h| Contour::from_ring(h))
                .collect::<Result<_>>()?,
        })
    }

    pub(super) fn polygon_mm(&self, units: Units) -> Result<Polygon> {
        Ok(Polygon {
            outer: self.outer.flatten_mm(units)?,
            holes: self
                .holes
                .iter()
                .map(|h| h.flatten_mm(units))
                .collect::<Result<_>>()?,
        })
    }
}
