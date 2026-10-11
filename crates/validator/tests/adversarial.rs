use nestbolt_validator::{Footprint, Polygon, RigidTransform, Units};
use proptest::{
    prelude::*,
    test_runner::{Config, RngSeed, TestRunner},
};
use std::cell::Cell;

#[test]
fn seeded_adversarial_polygon_fuzz() {
    let config = Config {
        cases: 10_000,
        rng_seed: RngSeed::Fixed(0x4e455354424f4c54),
        ..Config::default()
    };
    let mut runner = TestRunner::new(config);
    let ring = proptest::collection::vec((-1000i32..1000, -1000i32..1000), 0..13);
    let accepted = Cell::new(0_u32);
    runner
        .run(&(ring.clone(), ring, 0u32..8), |(a, b, scale)| {
            let factor = 10_f64.powi(-(scale as i32));
            let make = |points: Vec<(i32, i32)>| {
                Footprint::new(
                    &Polygon {
                        outer: points
                            .into_iter()
                            .map(|(x, y)| [f64::from(x) * factor, f64::from(y) * factor])
                            .collect(),
                        holes: vec![],
                    },
                    Units::Mm,
                    RigidTransform::default(),
                )
            };
            // Invalid topologies are expected to return errors, never panic/hang.
            let (a, b) = (make(a), make(b));
            if let Ok(ref shape) = a {
                prop_assert!(shape.area().is_finite() && shape.area() > 0.0);
                accepted.set(accepted.get() + 1);
            }
            if let (Ok(a), Ok(b)) = (a, b) {
                let ab = a.compare(&b, 0.0).unwrap();
                let ba = b.compare(&a, 0.0).unwrap();
                prop_assert!(
                    (ab.overlap_area - ba.overlap_area).abs()
                        <= 1e-10 * a.area().max(b.area()).max(1.0)
                );
                prop_assert!(
                    ab.overlap_area
                        <= a.area().min(b.area()) + 1e-8 * a.area().max(b.area()).max(1.0)
                );
            }
            Ok(())
        })
        .unwrap();
    assert!(
        accepted.get() > 100,
        "fuzz corpus did not exercise enough accepted polygons"
    );
}
