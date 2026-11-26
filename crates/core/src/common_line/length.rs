//! Curve length for the cut-length report, delegating to `curves`.
use crate::curves::{Contour, Point, Segment};

pub(crate) fn segment(from: Point, s: &Segment) -> f64 {
    s.length(from)
}

pub(super) fn contour(c: &Contour) -> f64 {
    c.length()
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
