//! Exact-output comparison against the original exhaustive distance calculation.
use super::*;
use proptest::{
    prelude::*,
    test_runner::{Config, RngSeed, TestRunner},
};

fn exhaustive(a: &Paths64, b: &Paths64) -> f64 {
    let mut minimum = f64::INFINITY;
    for (a0, a1) in a.iter().flat_map(edges) {
        for (b0, b1) in b.iter().flat_map(edges) {
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

#[test]
fn pruned_distances_equal_exhaustive_distances_at_all_supported_scales() {
    let mut runner = TestRunner::new(Config {
        cases: 3000,
        rng_seed: RngSeed::Fixed(0x44495354414e4345),
        ..Config::default()
    });
    let ring = proptest::collection::vec((-40i64..41, -40i64..41), 3..48);
    runner
        .run(
            &(
                ring.clone(),
                ring,
                -100i64..101,
                -100i64..101,
                prop_oneof![Just(1i64), Just(1_000_000i64), Just(10_000_000_000i64)],
            ),
            |(a, b, dx, dy, scale)| {
                let make = |points: Vec<(i64, i64)>, x: i64, y: i64| -> Paths64 {
                    vec![
                        points
                            .into_iter()
                            .map(|(px, py)| Point64::new((px + x) * scale, (py + y) * scale))
                            .collect(),
                    ]
                };
                let a = make(a, 0, 0);
                let b = make(b, dx, dy);
                prop_assert_eq!(boundary_distance(&a, &b), exhaustive(&a, &b));
                prop_assert_eq!(boundary_distance(&b, &a), exhaustive(&b, &a));
                Ok(())
            },
        )
        .unwrap();
}

#[test]
fn pruning_preserves_near_touching_curves_and_multiple_components() {
    let circle = |radius: f64, x: f64, y: f64| -> Path64 {
        (0..256)
            .map(|i| {
                let (s, c) = (f64::from(i) * std::f64::consts::TAU / 256.0).sin_cos();
                Point64::new(
                    (x + radius * c).round() as i64,
                    (y + radius * s).round() as i64,
                )
            })
            .collect()
    };
    for origin in [0.0, 9_000_000_000_000.0] {
        let a = vec![
            circle(1_000_000.0, origin, origin),
            circle(300_000.0, origin, origin),
        ];
        for gap in [-1.0, 0.0, 1.0, 2.0, 3.0, 1_000_000.0] {
            let b = vec![circle(1_000_000.0, origin + 2_000_000.0 + gap, origin)];
            assert_eq!(boundary_distance(&a, &b), exhaustive(&a, &b));
        }
        let nested = vec![circle(100_000.0, origin, origin)];
        assert_eq!(boundary_distance(&a, &nested), exhaustive(&a, &nested));
    }
}
