//! Exact segment subdivision and cyclic contour starts. No flattening is used.
use anyhow::{Result, ensure};

use super::{Contour, Point, Segment, distance, lerp};

impl Segment {
    /// Subdivide at a parameter in [0, 1], preserving the exact curve kind.
    pub fn split_at(&self, from: Point, t: f64) -> Result<(Self, Self)> {
        ensure!(
            t.is_finite() && (0.0..=1.0).contains(&t),
            "curve parameter must be in 0..=1"
        );
        Ok(match self {
            Self::Line { to } => (
                Self::Line {
                    to: lerp(from, *to, t),
                },
                self.clone(),
            ),
            Self::Quad { control, to } => {
                let a = lerp(from, *control, t);
                let b = lerp(*control, *to, t);
                (
                    Self::Quad {
                        control: a,
                        to: lerp(a, b, t),
                    },
                    Self::Quad {
                        control: b,
                        to: *to,
                    },
                )
            }
            Self::Cubic {
                controls: [c0, c1],
                to,
            } => {
                let a = lerp(from, *c0, t);
                let b = lerp(*c0, *c1, t);
                let c = lerp(*c1, *to, t);
                let d = lerp(a, b, t);
                let e = lerp(b, c, t);
                (
                    Self::Cubic {
                        controls: [a, d],
                        to: lerp(d, e, t),
                    },
                    Self::Cubic {
                        controls: [e, c],
                        to: *to,
                    },
                )
            }
            Self::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } => (
                Self::Arc {
                    center: *center,
                    radii: *radii,
                    rotation: *rotation,
                    start: *start,
                    sweep: sweep * t,
                },
                Self::Arc {
                    center: *center,
                    radii: *radii,
                    rotation: *rotation,
                    start: start + sweep * t,
                    sweep: sweep * (1.0 - t),
                },
            ),
        })
    }

    /// Derivative in the direction of this segment's traversal. Degenerate
    /// derivatives are returned as zero, so callers must handle cusps explicitly.
    pub fn tangent_at(&self, from: Point, t: f64) -> Result<Point> {
        ensure!(
            t.is_finite() && (0.0..=1.0).contains(&t),
            "curve parameter must be in 0..=1"
        );
        let delta = |a: Point, b: Point| [b[0] - a[0], b[1] - a[1]];
        Ok(match self {
            Self::Line { to } => delta(from, *to),
            Self::Quad { control, to } => {
                let d = lerp(delta(from, *control), delta(*control, *to), t);
                [2.0 * d[0], 2.0 * d[1]]
            }
            Self::Cubic {
                controls: [a, b],
                to,
            } => {
                let d = lerp(
                    lerp(delta(from, *a), delta(*a, *b), t),
                    lerp(delta(*a, *b), delta(*b, *to), t),
                    t,
                );
                [3.0 * d[0], 3.0 * d[1]]
            }
            Self::Arc {
                radii,
                rotation,
                start,
                sweep,
                ..
            } => {
                let angle = start + sweep * t;
                let (s, c) = rotation.sin_cos();
                let x = -radii[0] * angle.sin() * sweep;
                let y = radii[1] * angle.cos() * sweep;
                [c * x - s * y, s * x + c * y]
            }
        })
    }
}

impl Contour {
    /// Choose an exact point on a closed contour as its first point. Segment
    /// order/winding, dimensions and curve types are preserved. A point inside
    /// a segment introduces one exact subdivision, never an approximating line.
    pub fn restarted(&self, segment_index: usize, t: f64) -> Result<Self> {
        ensure!(
            segment_index < self.segments.len(),
            "contour start segment is out of range"
        );
        ensure!(
            t.is_finite() && (0.0..=1.0).contains(&t),
            "curve parameter must be in 0..=1"
        );
        ensure!(
            distance(self.start, self.end()) <= 1e-8,
            "only closed contours can change their start point"
        );
        let index = if t == 1.0 {
            (segment_index + 1) % self.segments.len()
        } else {
            segment_index
        };
        let from = if index == 0 {
            self.start
        } else {
            self.segments[index - 1].end()
        };
        if t == 0.0 || t == 1.0 {
            let mut segments = self.segments.clone();
            segments.rotate_left(index);
            return Ok(Self {
                start: from,
                segments,
            });
        }
        let (before, after) = self.segments[index].split_at(from, t)?;
        let start = before.end();
        let segments = std::iter::once(after)
            .chain(self.segments[index + 1..].iter().cloned())
            .chain(self.segments[..index].iter().cloned())
            .chain(std::iter::once(before))
            .collect();
        Ok(Self { start, segments })
    }
}
