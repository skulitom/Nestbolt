//! Curve length for the cut-length report. Lines/circles are analytic; Bézier
//! control polygons bound subdivision error, and ellipses use adaptive Simpson.
use super::distance;
use crate::curves::{Contour, Point, Segment};

const TOL: f64 = 1e-7;
fn mid(a: Point, b: Point) -> Point {
    [(a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0]
}

fn bezier(points: &[Point], tolerance: f64, depth: u8) -> f64 {
    let chord = distance(points[0], *points.last().unwrap());
    let polygon: f64 = points.windows(2).map(|p| distance(p[0], p[1])).sum();
    if polygon - chord <= 2.0 * tolerance || depth == 0 {
        return (polygon + chord) / 2.0;
    }
    let mut levels = points.to_vec();
    let mut left = vec![points[0]];
    let mut right = vec![*points.last().unwrap()];
    while levels.len() > 1 {
        levels = levels.windows(2).map(|p| mid(p[0], p[1])).collect();
        left.push(levels[0]);
        right.push(*levels.last().unwrap());
    }
    right.reverse();
    bezier(&left, tolerance / 2.0, depth - 1) + bezier(&right, tolerance / 2.0, depth - 1)
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

pub(super) fn segment(from: Point, s: &Segment) -> f64 {
    match s {
        Segment::Line { to } => distance(from, *to),
        Segment::Quad { control, to } => bezier(&[from, *control, *to], TOL, 24),
        Segment::Cubic { controls, to } => bezier(&[from, controls[0], controls[1], *to], TOL, 24),
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

pub(super) fn contour(c: &Contour) -> f64 {
    let mut from = c.start;
    let mut total = 0.0;
    for s in &c.segments {
        total += segment(from, s);
        from = s.end();
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn lengths_preserve_circles_straight_beziers_and_subdivision() {
        let line = Segment::Cubic {
            controls: [[1.0, 0.0], [2.0, 0.0]],
            to: [3.0, 0.0],
        };
        assert_eq!(segment([0.0, 0.0], &line), 3.0);
        let arc = Segment::Arc {
            center: [0.0, 0.0],
            radii: [7.0, 7.0],
            rotation: 0.2,
            start: 0.4,
            sweep: std::f64::consts::TAU,
        };
        assert!((segment([0.0, 0.0], &arc) - 14.0 * std::f64::consts::PI).abs() < 1e-12);
        let whole = Segment::Quad {
            control: [1.0, 2.0],
            to: [2.0, 0.0],
        };
        let left = Segment::Quad {
            control: [0.5, 1.0],
            to: [1.0, 1.0],
        };
        let right = Segment::Quad {
            control: [1.5, 1.0],
            to: [2.0, 0.0],
        };
        assert!(
            (segment([0.0, 0.0], &whole)
                - segment([0.0, 0.0], &left)
                - segment([1.0, 1.0], &right))
            .abs()
                < 1e-6
        );
        // Independent high-resolution midpoint quadrature of an ellipse.
        let arc = Segment::Arc {
            center: [0.0, 0.0],
            radii: [9.0, 2.0],
            rotation: 1.0,
            start: 0.0,
            sweep: std::f64::consts::TAU,
        };
        let integral: f64 = (0..100_000)
            .map(|i| {
                let a = (i as f64 + 0.5) * std::f64::consts::TAU / 100_000.0;
                (9.0 * a.sin()).hypot(2.0 * a.cos()) * std::f64::consts::TAU / 100_000.0
            })
            .sum();
        assert!((segment([0.0, 0.0], &arc) - integral).abs() < 1e-6);
    }
}
