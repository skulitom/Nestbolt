//! Bound-aware evaluation of Sparrow's collision score (MIT, Copyright (c)
//! 2025 Jeroen Gardeyn, KU Leuven; see crates/core/Sparrow_LICENSE and
//! THIRD_PARTY_NOTICES).
//! The pole accumulation and final arithmetic match the pinned reference.
//! Every contribution is nonnegative, so a partial score is a lower bound.
use jagua_rs::geometry::{geo_traits::DistanceTo, primitives::SPolygon};
use sparrow::{
    consts::OVERLAP_PROXY_EPSILON_DIAM_RATIO,
    quantify::{calc_shape_penalty, quantify_collision_poly_poly},
};

/// Return the exact weighted score, or stop once this candidate cannot beat
/// `bound`. Compare with the existing accumulated loss, rather than subtracting
/// it from the bound: subtraction would change rounding at the boundary.
pub(super) fn pair(
    a: &SPolygon,
    b: &SPolygon,
    weight: f32,
    previous: f32,
    bound: f32,
) -> Option<f32> {
    if !bound.is_finite() {
        return Some(quantify_collision_poly_poly(a, b) * weight);
    }
    let epsilon = a.diameter().max(b.diameter()) * OVERLAP_PROXY_EPSILON_DIAM_RATIO;
    let squared = epsilon.powi(2);
    let penalty = calc_shape_penalty(a, b);
    let finish = |sum: f32| (sum * std::f32::consts::PI + squared).sqrt() * penalty * weight;
    let mut sum = 0.0;
    for p in &a.surrogate().poles {
        for q in &b.surrogate().poles {
            let penetration = (p.radius + q.radius) - p.center.distance_to(&q.center);
            let decayed = if penetration >= epsilon {
                penetration
            } else {
                squared / (-penetration + 2.0 * epsilon)
            };
            sum += decayed * p.radius.min(q.radius);
        }
        // Check once per row, retaining the reference's summation order and
        // its exact final operations. No score approximation is accepted.
        if previous + finish(sum) > bound {
            return None;
        }
    }
    Some(finish(sum))
}

#[cfg(test)]
mod tests {
    use super::*;
    use jagua_rs::{
        geometry::{DTransformation, geo_traits::Transformable},
        io::{
            ext_repr::{ExtItem, ExtOrientation, ExtRotation, ExtSPolygon, ExtShape},
            import::Importer,
        },
    };
    use rand::{RngExt, SeedableRng, rngs::Xoshiro256PlusPlus};
    use sparrow::config::DEFAULT_SPARROW_CONFIG;

    #[test]
    fn bounded_scores_preserve_reference_bits_and_never_prune_a_tie() {
        let importer = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None);
        let outlines = [
            vec![
                (0., 0.),
                (30., 0.),
                (30., 8.),
                (8., 8.),
                (8., 22.),
                (30., 22.),
                (30., 30.),
                (0., 30.),
            ],
            (0..64)
                .map(|i| {
                    let angle = i as f32 * std::f32::consts::TAU / 64.;
                    (12. * angle.cos(), 8. * angle.sin())
                })
                .collect(),
        ];
        let shapes: Vec<_> = outlines
            .into_iter()
            .enumerate()
            .map(|(i, points)| {
                importer
                    .import_item(
                        &ExtItem {
                            id: i as u64,
                            shape: ExtShape::SimplePolygon(ExtSPolygon(points)),
                            orientation: ExtOrientation {
                                rotation: ExtRotation::Continuous {},
                                reflection_axes: vec![90.],
                            },
                            min_quality: None,
                        },
                        i,
                    )
                    .unwrap()
                    .shape_cd()
                    .as_ref()
                    .clone()
            })
            .collect();
        let mut rng = Xoshiro256PlusPlus::seed_from_u64(17);
        let mut pruned = 0;
        for i in 0..128 {
            let a = &shapes[i % 2];
            let mut b = shapes[(i / 2) % 2].clone();
            b.transform(
                &DTransformation::new(
                    rng.random_range(-3.1..3.1),
                    (rng.random_range(-40.0..40.0), rng.random_range(-40.0..40.0)),
                )
                .with_reflection(i % 3 == 0)
                .compose(),
            );
            for weight in [1., 7., 1e20] {
                let reference = quantify_collision_poly_poly(a, &b) * weight;
                for previous in [0., reference * 0.75, reference * 10000.] {
                    let total = previous + reference;
                    for bound in [0., total.next_down(), total, total.next_up(), f32::INFINITY] {
                        match pair(a, &b, weight, previous, bound) {
                            None => {
                                assert!(
                                    total > bound,
                                    "pruned a reference result at/below the bound"
                                );
                                pruned += 1;
                            }
                            Some(actual) => assert_eq!(actual.to_bits(), reference.to_bits()),
                        }
                        if total <= bound {
                            assert_eq!(pair(a, &b, weight, previous, bound), Some(reference));
                        }
                    }
                }
            }
        }
        assert!(
            pruned > 1000,
            "exercise actual pruning, not only the full-score path"
        );
    }
}
