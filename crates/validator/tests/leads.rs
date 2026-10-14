use std::f64::consts::{PI, TAU};

use nestbolt_validator::{
    Footprint, Polygon, RigidTransform, Units,
    job::{self, Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle},
    leads::{self, Allowance, Path},
};
use proptest::prelude::*;

fn line(a: [f64; 2], b: [f64; 2]) -> Path {
    Path::Line {
        from_mm: a,
        to_mm: b,
    }
}

fn allowance(copy_index: u32, a: [f64; 2], b: [f64; 2]) -> Allowance {
    Allowance {
        part_id: "part".into(),
        copy_index,
        contour_index: 0,
        kerf_mm: 0.2,
        paths: vec![line(a, b)],
    }
}

fn fixture() -> (Job, Layout) {
    (
        Job {
            version: 1,
            name: "lead checker".into(),
            units: Units::Mm,
            parts: vec![Part {
                id: "part".into(),
                quantity: 2,
                geometry: vec![rectangle(0.0, 0.0, 10.0, 10.0)],
                rotations: Rotations::Free,
                allow_mirror: true,
                priority: 1.0,
            }],
            stocks: vec![Stock {
                id: "stock".into(),
                width: 100.0,
                height: 100.0,
                count: None,
                margins: Margins::default(),
                outline: vec![],
                defects: vec![],
            }],
            clearance: 0.0,
            edge_clearance: 0.0,
            mode: Mode::All,
        },
        Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![Sheet {
                id: "sheet".into(),
                stock_id: "stock".into(),
            }],
            placements: [20.0, 35.0]
                .into_iter()
                .enumerate()
                .map(|(i, x)| Placement {
                    part_id: "part".into(),
                    copy_index: i as u32,
                    sheet_id: "sheet".into(),
                    transform: RigidTransform {
                        translation: [x, 20.0],
                        ..Default::default()
                    },
                })
                .collect(),
        },
    )
}

fn inside_ring(p: [f64; 2], ring: &[[f64; 2]]) -> bool {
    // Independent floating-point ray crossing, not the integer clipper checker.
    let mut inside = false;
    for (a, b) in ring
        .iter()
        .zip(ring.iter().cycle().skip(1))
        .take(ring.len())
    {
        if (a[1] > p[1]) != (b[1] > p[1])
            && p[0] < a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
        {
            inside = !inside;
        }
    }
    inside
}

fn contains(polygons: &[Polygon], p: [f64; 2]) -> bool {
    polygons
        .iter()
        .any(|s| inside_ring(p, &s.outer) && !s.holes.iter().any(|h| inside_ring(p, h)))
}

#[test]
fn stroke_and_pierce_have_the_declared_physical_sizes() {
    let fp = leads::footprint(&[line([0.0, 0.0], [3.0, 0.0])], 0.2).unwrap();
    let [x0, y0, x1, y1] = fp.bounds();
    assert!((-0.2005..=-0.2).contains(&x0));
    assert!((-0.2005..=-0.2).contains(&y0));
    assert!((3.1..=3.1005).contains(&x1));
    assert!((0.2..=0.2005).contains(&y1));
    let polygons = fp.polygons().unwrap();
    // Pierce radius is kerf; the far endpoint has only the half-kerf stroke.
    assert!(contains(&polygons, [0.0, 0.1999]));
    assert!(contains(&polygons, [3.0999, 0.0]));
    assert!(!contains(&polygons, [3.15, 0.0]));
    assert!(!contains(&polygons, [1.5, 0.15]));
}

#[test]
fn both_native_traversal_directions_reserve_room() {
    let paths = [
        line([-3.0, -3.0], [0.0, 0.0]),
        line([3.0, -3.0], [0.0, 0.0]),
    ];
    let fp = leads::footprint(&paths, 0.2).unwrap();
    let polygons = fp.polygons().unwrap();
    for path in paths {
        // Test physical coverage, not exact containment of a separately rounded
        // polygon union. Intersections are quantized on the nanometre grid.
        for i in 0..=32 {
            let c = path.point(i as f64 / 32.0);
            let r = if i == 0 { 0.2 } else { 0.1 };
            for j in 0..48 {
                let a = j as f64 * TAU / 48.0;
                assert!(contains(
                    &polygons,
                    [c[0] + r * a.cos(), c[1] + r * a.sin()]
                ));
            }
        }
    }
    assert!(
        leads::footprint(
            &[line([1.0, 2.0], [0.01, 0.0]), line([3.0, 2.0], [0.0, 0.0])],
            0.2
        )
        .is_err()
    );
}

#[test]
fn detects_other_parts_and_crossing_leads_before_export() {
    let (job, layout) = fixture();
    let a = allowance(0, [12.0, 5.0], [10.0, 5.0]);
    let b = allowance(1, [-2.0, 5.0], [0.0, 5.0]);
    assert!(
        leads::validate(&job, &layout, &[a.clone(), b.clone()])
            .unwrap()
            .valid
    );
    let a_cross = allowance(0, [14.0, 5.0], [10.0, 5.0]);
    let report = leads::validate(&job, &layout, &[a_cross, b]).unwrap();
    assert!(
        !report.valid
            && report
                .violations
                .iter()
                .any(|v| v.contains("overlaps allowance"))
    );
    let report = leads::validate(&job, &layout, &[allowance(0, [17.0, 5.0], [10.0, 5.0])]).unwrap();
    assert!(
        !report.valid
            && report
                .violations
                .iter()
                .any(|v| v.contains("overlaps part part#1"))
    );
    // A pierce disc alone can hit a neighbour even when the line stroke clears it.
    let report =
        leads::validate(&job, &layout, &[allowance(0, [14.85, 5.0], [10.0, 5.0])]).unwrap();
    assert!(!report.valid);
}

#[test]
fn sheets_are_isolated_and_original_layout_must_be_valid() {
    let (mut job, mut layout) = fixture();
    layout.sheets.push(Sheet {
        id: "second".into(),
        stock_id: "stock".into(),
    });
    layout.placements[1].sheet_id = "second".into();
    let a = allowance(0, [17.0, 5.0], [10.0, 5.0]);
    assert!(
        leads::validate(&job, &layout, std::slice::from_ref(&a))
            .unwrap()
            .valid
    );
    job.parts[0].quantity = 3;
    assert!(leads::validate(&job, &layout, &[a]).is_err());
}

#[test]
fn stock_edges_margins_remnants_and_defects_check_the_whole_lead() {
    let (job, layout) = fixture();
    let a = allowance(0, [-3.0, 5.0], [0.0, 5.0]); // x=17..20, y=25
    assert!(
        leads::validate(&job, &layout, std::slice::from_ref(&a))
            .unwrap()
            .valid
    );
    for kind in 0..4 {
        let mut altered = job.clone();
        match kind {
            0 => altered.stocks[0].margins.left = 18.0,
            1 => altered.stocks[0].outline = vec![rectangle(18.0, 0.0, 82.0, 100.0)],
            2 => altered.stocks[0].defects = vec![rectangle(16.8, 24.9, 0.1, 0.2)],
            _ => {
                altered.stocks[0].margins.left = 16.0;
                altered.edge_clearance = 1.0;
            }
        }
        assert!(job::validate(&altered, &layout).unwrap().valid);
        let report = leads::validate(&altered, &layout, std::slice::from_ref(&a)).unwrap();
        assert!(!report.valid, "stock case {kind}");
        assert!(report.violations.iter().any(|v| v.contains("stock edge")));
    }
    let long = allowance(0, [-21.0, 5.0], [0.0, 5.0]);
    assert!(!leads::validate(&job, &layout, &[long]).unwrap().valid);
}

#[test]
fn hole_leads_check_nested_parts_and_other_contours_of_the_owner() {
    let (mut job, mut layout) = fixture();
    job.parts[0].quantity = 1;
    job.parts[0].geometry[0] = rectangle(0.0, 0.0, 30.0, 30.0);
    job.parts[0].geometry[0]
        .holes
        .push(rectangle(5.0, 5.0, 20.0, 20.0).outer);
    job.parts.push(Part {
        id: "island".into(),
        quantity: 1,
        geometry: vec![rectangle(0.0, 0.0, 2.0, 2.0)],
        ..job.parts[0].clone()
    });
    layout.placements[1].part_id = "island".into();
    layout.placements[1].copy_index = 0;
    layout.placements[1].transform.translation = [27.0, 34.0];
    let mut hole = allowance(0, [8.0, 15.0], [5.0, 15.0]);
    hole.contour_index = 1;
    assert!(job::validate(&job, &layout).unwrap().valid);
    assert!(
        !leads::validate(&job, &layout, std::slice::from_ref(&hole))
            .unwrap()
            .valid
    );
    layout.placements[1].transform.translation = [40.0, 40.0];
    assert!(
        leads::validate(&job, &layout, std::slice::from_ref(&hole))
            .unwrap()
            .valid
    );
    // An outer lead crossing a hole lead is still caught for the same owner.
    let outer = allowance(0, [7.0, 14.0], [7.0, 16.0]);
    let report = leads::validate(&job, &layout, &[hole, outer]).unwrap();
    assert!(
        report
            .violations
            .iter()
            .any(|v| v.contains("overlaps allowance"))
    );
}

#[test]
fn inch_jobs_keep_paths_in_mm_but_translate_using_inches() {
    let (mut job, mut layout) = fixture();
    let a = allowance(0, [14.85, 5.0], [10.0, 5.0]);
    let expected = leads::validate(&job, &layout, std::slice::from_ref(&a)).unwrap();
    job.units = Units::Inch;
    layout.units = Units::Inch;
    for p in job
        .parts
        .iter_mut()
        .flat_map(|p| &mut p.geometry)
        .flat_map(|p| &mut p.outer)
    {
        p.iter_mut().for_each(|v| *v /= 25.4);
    }
    job.stocks[0].width /= 25.4;
    job.stocks[0].height /= 25.4;
    for p in &mut layout.placements {
        p.transform.translation.iter_mut().for_each(|v| *v /= 25.4);
    }
    let actual = leads::validate(&job, &layout, &[a]).unwrap();
    assert_eq!(actual.violations, expected.violations);
    assert_eq!(actual.violation_count, expected.violation_count);
}

#[test]
fn malformed_paths_and_unknown_contours_fail_explicitly() {
    for path in [
        line([0.0, 0.0], [0.0, 0.0]),
        line([f64::NAN, 0.0], [1.0, 0.0]),
        Path::Arc {
            center_mm: [0.0, 0.0],
            radius_mm: -1.0,
            start_radians: 0.0,
            sweep_radians: PI,
        },
        Path::Arc {
            center_mm: [0.0, 0.0],
            radius_mm: 1.0,
            start_radians: 0.0,
            sweep_radians: 7.0,
        },
    ] {
        assert!(leads::footprint(&[path], 0.2).is_err());
    }
    assert!(leads::footprint(&[], 0.2).is_err());
    assert!(leads::footprint(&[line([0.0, 0.0], [1.0, 0.0])], f64::INFINITY).is_err());
    let (job, layout) = fixture();
    let a = allowance(0, [-3.0, 5.0], [0.0, 5.0]);
    assert!(leads::validate(&job, &layout, &[a.clone(), a.clone()]).is_err());
    let mut unknown = a.clone();
    unknown.copy_index = 2;
    assert!(leads::validate(&job, &layout, &[unknown]).is_err());
    let mut unknown = a;
    unknown.contour_index = 1;
    assert!(leads::validate(&job, &layout, &[unknown]).is_err());
}

#[test]
fn extreme_arc_sizes_keep_physical_coverage_or_fail_with_a_bounded_cost() {
    for radius in [0.000002, 0.05, 1.0, 30.0] {
        for kerf in [0.000002, 0.01, 0.05, 1000.0] {
            let path = Path::Arc {
                center_mm: [0.0, 0.0],
                radius_mm: radius,
                start_radians: 0.0,
                sweep_radians: TAU,
            };
            let polygons = leads::footprint(&[path], kerf).unwrap().polygons().unwrap();
            for i in 0..96 {
                let a = TAU * i as f64 / 96.0;
                // Outside of the analytic torus and of the pierce disc.
                assert!(contains(
                    &polygons,
                    [
                        (radius + kerf / 2.0) * a.cos(),
                        (radius + kerf / 2.0) * a.sin()
                    ]
                ));
                assert!(contains(
                    &polygons,
                    [radius + kerf * a.cos(), kerf * a.sin()]
                ));
            }
        }
    }
    let giant = Path::Arc {
        center_mm: [0.0, 0.0],
        radius_mm: 1e7,
        start_radians: 0.0,
        sweep_radians: TAU,
    };
    assert!(
        leads::footprint(&[giant], 0.2)
            .unwrap_err()
            .to_string()
            .contains("too many")
    );
    let edge = line([1e7 - 1.0, 0.0], [1e7, 0.0]);
    assert!(
        leads::footprint(&[edge], 0.2)
            .unwrap_err()
            .to_string()
            .contains("coordinate range")
    );
}

#[test]
fn large_start_angles_do_not_erase_short_sweeps_or_rigid_rotations() {
    let angle: f64 = 1e8;
    let sweep: f64 = 0.000123;
    let radius: f64 = 1e6;
    let path = Path::Arc {
        center_mm: [0.0, 0.0],
        radius_mm: radius,
        start_radians: angle,
        sweep_radians: sweep,
    };
    // Independently compose the two rotation matrices; adding the angles first
    // loses 0.0058 mm here, despite every parameter being inside its limits.
    let expected = [
        radius * (angle.cos() * sweep.cos() - angle.sin() * sweep.sin()),
        radius * (angle.sin() * sweep.cos() + angle.cos() * sweep.sin()),
    ];
    let p = path.point(1.0);
    assert!((p[0] - expected[0]).hypot(p[1] - expected[1]) < 1e-7);
    for mirrored in [false, true] {
        let transform = RigidTransform {
            mirrored,
            rotation_radians: angle,
            ..Default::default()
        };
        let transformed = path.transformed(transform, Units::Mm).unwrap();
        let x = p[0] * if mirrored { -1.0 } else { 1.0 };
        let q = [
            x * angle.cos() - p[1] * angle.sin(),
            x * angle.sin() + p[1] * angle.cos(),
        ];
        let actual = transformed.point(1.0);
        assert!((actual[0] - q[0]).hypot(actual[1] - q[1]) < 1e-7);
    }
    let polygons = leads::footprint(&[path], 0.05).unwrap().polygons().unwrap();
    for i in 0..48 {
        let a = TAU * i as f64 / 48.0;
        assert!(contains(
            &polygons,
            [expected[0] + 0.025 * a.cos(), expected[1] + 0.025 * a.sin()]
        ));
    }
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(64))]

    #[test]
    fn analytic_swept_discs_are_contained(
        arc in any::<bool>(), radius in 0.05f64..30.0, kerf in 0.05f64..2.0,
        angle in -PI..PI, sweep in 0.05f64..TAU, reverse in any::<bool>(),
        x in -100.0f64..100.0, y in -100.0f64..100.0,
    ) {
        let sweep = if reverse { -sweep } else { sweep };
        let center = |t: f64| if arc {
            [x + radius * (angle + sweep * t).cos(), y + radius * (angle + sweep * t).sin()]
        } else { [x + radius * t * angle.cos(), y + radius * t * angle.sin()] };
        let path = if arc { Path::Arc { center_mm: [x, y], radius_mm: radius, start_radians: angle, sweep_radians: sweep } }
            else { line(center(0.0), center(1.0)) };
        let polygons = leads::footprint(&[path], kerf).unwrap().polygons().unwrap();
        // Discs swept along the exact analytic path, including both round caps;
        // separate full-radius pierce disc. No solver flattening is reused.
        for i in 0..=32 {
            let c = center(i as f64 / 32.0);
            let r = if i == 0 { kerf } else { kerf / 2.0 };
            for j in 0..48 {
                let a = j as f64 * TAU / 48.0;
                prop_assert!(contains(&polygons, [c[0] + r * a.cos(), c[1] + r * a.sin()]));
            }
        }
    }

    #[test]
    fn transformation_matches_independent_matrix_at_every_sample(
        angle in -1e8f64..1e8, rotation in -1e8f64..1e8, radius in 0.05f64..30.0,
        sweep in -TAU..TAU, mirrored in any::<bool>(), inch in any::<bool>(),
    ) {
        prop_assume!(sweep.abs() > 1e-6);
        let t = RigidTransform { translation: [3.0, 5.0], rotation_radians: rotation, mirrored };
        let units = if inch { Units::Inch } else { Units::Mm };
        let k = if inch { 25.4 } else { 1.0 };
        for path in [line([1.0, 2.0], [4.0, 6.0]), Path::Arc {
            center_mm: [2.0, 4.0], radius_mm: radius, start_radians: angle, sweep_radians: sweep,
        }] {
            let transformed = path.transformed(t, units).unwrap();
            for i in 0..=16 {
                let p = path.point(i as f64 / 16.0);
                let x = p[0] * if mirrored { -1.0 } else { 1.0 };
                let expected = [x * rotation.cos() - p[1] * rotation.sin() + 3.0 * k,
                    x * rotation.sin() + p[1] * rotation.cos() + 5.0 * k];
                let actual = transformed.point(i as f64 / 16.0);
                prop_assert!((actual[0]-expected[0]).hypot(actual[1]-expected[1]) < 1e-10);
            }
        }
    }
}

#[test]
fn union_preserves_holes_islands_and_units_without_double_counting() {
    for units in [Units::Mm, Units::Inch] {
        let mut ring = rectangle(0.0, 0.0, 10.0, 10.0);
        ring.holes.push(rectangle(2.0, 2.0, 6.0, 6.0).outer);
        let mut island = rectangle(3.0, 3.0, 4.0, 4.0);
        island.holes.push(rectangle(4.0, 4.0, 2.0, 2.0).outer);
        let a = Footprint::new(&ring, units, RigidTransform::default()).unwrap();
        let b = Footprint::new(&island, units, RigidTransform::default()).unwrap();
        let union = a.union(&b).unwrap();
        let polygons = union.polygons().unwrap();
        assert_eq!(polygons.len(), 2);
        assert!(polygons.iter().all(|p| p.holes.len() == 1));
        let rebuilt =
            Footprint::from_polygons(&polygons, units, RigidTransform::default()).unwrap();
        assert!((rebuilt.area() - 76.0 * units.to_mm().powi(2)).abs() < 1e-8);
        assert_eq!(rebuilt.inside(&union, 0.0).unwrap().outside_area, 0.0);
        assert_eq!(union.inside(&rebuilt, 0.0).unwrap().outside_area, 0.0);
    }
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(64))]
    #[test]
    fn union_roundtrip_matches_analytic_overlapping_rectangles(
        w in 1.0f64..100.0, h in 1.0f64..100.0, fraction in 0.0f64..2.0,
        mirrored in any::<bool>(), rotation in -PI..PI,
    ) {
        let t = RigidTransform { translation: [10.0, -20.0], mirrored, rotation_radians: rotation };
        let a = Footprint::new(&rectangle(0.0, 0.0, w, h), Units::Mm, t).unwrap();
        let b = Footprint::new(&rectangle(w * fraction, 0.0, w, h), Units::Mm, t).unwrap();
        let union = a.union(&b).unwrap();
        let expected = w * h * (1.0 + fraction.min(1.0));
        prop_assert!((union.area() - expected).abs() < (w + h) * 0.00001);
        let rebuilt = Footprint::from_polygons(&union.polygons().unwrap(), Units::Mm, RigidTransform::default()).unwrap();
        prop_assert!((rebuilt.area() - union.area()).abs() < 1e-8);
        // Clipped intersections are rounded to the integer grid. A two-grid
        // strip around either original boundary bounds the possible area loss.
        let quantization_area = 4.0 * (w + h) * nestbolt_validator::GRID;
        prop_assert!(a.inside(&rebuilt, 0.0).unwrap().outside_area <= quantization_area);
        prop_assert!(b.inside(&rebuilt, 0.0).unwrap().outside_area <= quantization_area);
    }
}
