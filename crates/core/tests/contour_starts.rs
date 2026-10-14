use std::f64::consts::TAU;

use nestbolt_core::curves::{Affine, Contour, Point, Segment, hausdorff, signed_area};
use nestbolt_validator::RigidTransform;
use proptest::prelude::*;

fn distance(a: Point, b: Point) -> f64 {
    (a[0] - b[0]).hypot(a[1] - b[1])
}

// Independent Bernstein evaluation, deliberately not the production splitter.
fn point(from: Point, s: &Segment, t: f64) -> Point {
    let u = 1.0 - t;
    match s {
        Segment::Line { to } => std::array::from_fn(|k| from[k] * u + to[k] * t),
        Segment::Quad { control, to } => {
            std::array::from_fn(|k| from[k] * u * u + 2.0 * control[k] * u * t + to[k] * t * t)
        }
        Segment::Cubic {
            controls: [a, b],
            to,
        } => std::array::from_fn(|k| {
            from[k] * u * u * u
                + 3.0 * a[k] * u * u * t
                + 3.0 * b[k] * u * t * t
                + to[k] * t * t * t
        }),
        Segment::Arc {
            center,
            radii,
            rotation,
            start,
            sweep,
        } => {
            let angle = start + sweep * t;
            let x = radii[0] * angle.cos();
            let y = radii[1] * angle.sin();
            [
                center[0] + x * rotation.cos() - y * rotation.sin(),
                center[1] + x * rotation.sin() + y * rotation.cos(),
            ]
        }
    }
}

fn samples() -> Vec<(Point, Segment)> {
    vec![
        ([1.0, 2.0], Segment::Line { to: [8.0, -3.0] }),
        (
            [1.0, 2.0],
            Segment::Quad {
                control: [-7.0, 9.0],
                to: [8.0, -3.0],
            },
        ),
        (
            [1.0, 2.0],
            Segment::Cubic {
                controls: [[-7.0, 9.0], [11.0, 5.0]],
                to: [8.0, -3.0],
            },
        ),
        (
            [0.0, 0.0],
            Segment::Arc {
                center: [2.0, -3.0],
                radii: [8.0, 3.0],
                rotation: 0.7,
                start: 1.2,
                sweep: -5.1,
            },
        ),
    ]
    .into_iter()
    .map(|(p, s)| {
        (
            if matches!(s, Segment::Arc { .. }) {
                point(p, &s, 0.0)
            } else {
                p
            },
            s,
        )
    })
    .collect()
}

#[test]
fn each_curve_subdivides_exactly_and_derivatives_keep_direction() {
    for (from, s) in samples() {
        for t in [0.0, 0.137, 0.5, 0.901, 1.0] {
            let (a, b) = s.split_at(from, t).unwrap();
            let mid = point(from, &s, t);
            assert!(distance(a.end(), mid) < 1e-12);
            for i in 0..=32 {
                let f = f64::from(i) / 32.0;
                assert!(distance(point(from, &a, f), point(from, &s, t * f)) < 1e-11);
                assert!(distance(point(mid, &b, f), point(from, &s, t + (1.0 - t) * f)) < 1e-11);
            }
            if t > 0.0 && t < 1.0 {
                let d = s.tangent_at(from, t).unwrap();
                let left = point(from, &s, t - 1e-6);
                let right = point(from, &s, t + 1e-6);
                assert!(
                    distance(
                        d,
                        [(right[0] - left[0]) / 2e-6, (right[1] - left[1]) / 2e-6]
                    ) < 1e-7
                );
            }
        }
    }
}

#[test]
fn restarting_circle_retains_arcs_and_rejects_invalid_or_open_contours() {
    let c = Contour {
        start: [10.0, 0.0],
        segments: vec![Segment::Arc {
            center: [0.0, 0.0],
            radii: [10.0, 10.0],
            rotation: 0.0,
            start: 0.0,
            sweep: TAU,
        }],
    };
    let r = c.restarted(0, 0.25).unwrap();
    assert!(distance(r.start, [0.0, 10.0]) < 1e-12);
    assert_eq!(r.segments.len(), 2);
    assert!(r.segments.iter().all(|s| matches!(s, Segment::Arc { .. })));
    assert!(distance(r.start, r.end()) < 1e-12);
    for t in [f64::NAN, f64::INFINITY, -0.1, 1.1] {
        assert!(c.restarted(0, t).is_err());
    }
    assert!(c.restarted(1, 0.0).is_err());
    let open = Contour {
        start: [0.0, 0.0],
        segments: vec![Segment::Line { to: [3.0, 0.0] }],
    };
    assert!(open.restarted(0, 0.5).is_err());
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(64))]
    #[test]
    fn restarts_preserve_geometry_and_commute_with_rigid_transforms(t in 0.001_f64..0.999, angle in -TAU..TAU, mirrored in any::<bool>(), index in 0_usize..4) {
        let (from,s)=samples().remove(index);
        let c=Contour { start:from,segments:vec![s,Segment::Line { to:[17.0,14.0] },Segment::Line { to:from }] };
        let r=c.restarted(0,t).unwrap();
        let a=Affine::placement(&RigidTransform { translation:[123.0,-19.0],rotation_radians:angle,mirrored });
        let left=r.transformed(&a);
        let right=c.transformed(&a).restarted(0,t).unwrap();
        prop_assert!(distance(left.start,right.start)<1e-10);
        let original=c.flatten(0.0001).unwrap();
        let moved=r.flatten(0.0001).unwrap();
        prop_assert!(hausdorff(&original,&moved)<0.000201);
        prop_assert!((signed_area(&original)-signed_area(&moved)).abs()<0.02);
        for (l,r) in left.segments.iter().zip(&right.segments) { prop_assert!(distance(l.end(),r.end())<1e-9); }
    }
}
