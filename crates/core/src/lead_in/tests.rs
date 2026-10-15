use super::*;
use nestbolt_validator::job::{Margins, Mode, Part, Rotations, Stock, rectangle};
use proptest::prelude::*;
use std::f64::consts::{PI, TAU};

fn options() -> Options {
    Options {
        kerf_mm: 0.2,
        length_mm: 3.0,
        style: Style::Line,
        outer_angle_degrees: 45.0,
        hole_angle_degrees: 90.0,
    }
}

#[test]
fn near_zero_arc_uses_a_bounded_chord_without_a_remote_invalid_centre() {
    for angle in [0.0, 1e-12, 1e-8, 0.000001] {
        let lead = path([20.0, 5.0], [1.0, 0.0], 1.0, 3.0, angle, Style::Arc).unwrap();
        lead.validate().unwrap();
        let a = lead.point(0.0);
        assert!((a[0] - 17.0).hypot(a[1] - 5.0) < 1e-6);
        assert_eq!(lead.point(1.0), [20.0, 5.0]);
    }
}

#[test]
fn planned_search_validates_original_parts_every_allowance_and_exported_starts() {
    let mut original = job(rectangle(0.0, 0.0, 20.0, 10.0));
    original.parts[0].quantity = 4;
    original.stocks[0].width = 55.0;
    original.stocks[0].height = 35.0;
    let plan = prepare_plain(
        &original,
        Options {
            style: Style::Arc,
            ..options()
        },
    );
    assert!(plan.parts.iter().all(|p| p.flags.is_empty()));
    let result = crate::sheets::optimize_with_material(
        &plan.collision_job,
        &original,
        crate::sheets::Options {
            seconds: 1.0,
            time_limit: Some(30.0),
            timing: crate::clock::Timing::Work,
            ..Default::default()
        },
        false,
        |_, _| {},
    )
    .unwrap();
    assert!(result.validation.valid);
    assert_eq!(
        result.validation.metrics.as_ref().unwrap().placed_area,
        800.0
    );
    let validation = nestbolt_validator::job::validate(&original, &result.layout).unwrap();
    assert!(validation.valid);
    assert!((validation.metrics.unwrap().placed_area - 800.0).abs() < 1e-9);
    let allowances = plan.allowances(&result.layout).unwrap();
    assert_eq!(allowances.len(), 4);
    let checked = leads::validate(&original, &result.layout, &allowances).unwrap();
    assert!(checked.valid, "{:?}", checked.violations);
    assert_eq!(checked.checked_contours, 4);
    for sheet in &result.layout.sheets {
        let review = plan.review(&result.layout, &sheet.id).unwrap();
        let placed = crate::export::placed(&original, &result.layout, &sheet.id, &HashMap::new())
            .unwrap()
            .0;
        for ((id, contours), lead) in placed.iter().zip(&review.leadin) {
            let start = review.starts[id][0].unwrap();
            let contour = contours[0]
                .restarted(start.segment, start.parameter)
                .unwrap();
            assert!(
                sub(contour.start, lead.end())[0].hypot(sub(contour.start, lead.end())[1]) < 1e-8
            );
        }
        let svg = crate::export::svg_with_review_paths(
            &original,
            &result.layout,
            &sheet.id,
            &HashMap::new(),
            crate::export::Options {
                sheet_outline: true,
            },
            &review,
        )
        .unwrap();
        assert!(svg.contains("LEADIN"));
        let dxf = crate::export::dxf_with_review_paths(
            &original,
            &result.layout,
            &sheet.id,
            &HashMap::new(),
            crate::export::Options {
                sheet_outline: true,
            },
            &review,
        )
        .unwrap();
        assert!(dxf.contains("LEADIN"));
    }
}

fn job(polygon: Polygon) -> Job {
    Job {
        version: 1,
        name: "lead fixture".into(),
        units: Units::Mm,
        parts: vec![Part {
            id: "plate".into(),
            quantity: 2,
            geometry: vec![polygon],
            rotations: Rotations::Free,
            allow_mirror: true,
            priority: 1.0,
        }],
        stocks: vec![Stock {
            id: "sheet".into(),
            width: 100.0,
            height: 100.0,
            count: None,
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
        clearance: 0.2,
        edge_clearance: 1.0,
        mode: Mode::All,
    }
}

fn prepare_plain(job: &Job, options: Options) -> Prepared {
    prepare(job, &HashMap::new(), options, &HashMap::new()).unwrap()
}

#[test]
fn native_tenth_mm_setting_is_the_actual_reserved_path_length() {
    for style in [Style::Line, Style::Arc] {
        let result = prepare_plain(
            &job(rectangle(0.0, 0.0, 20.0, 10.0)),
            Options {
                length_mm: 1.2349,
                style,
                ..options()
            },
        );
        let reservation = &result.parts[0].reservations[0];
        assert_eq!(reservation.length_mm, 1.2);
        assert!(reservation.shortened);
        for path in &reservation.paths {
            let length = match path {
                Path::Line {
                    from_mm: a,
                    to_mm: b,
                } => (a[0] - b[0]).hypot(a[1] - b[1]),
                Path::Arc {
                    radius_mm,
                    sweep_radians,
                    ..
                } => radius_mm * sweep_radians.abs(),
            };
            assert!((length - reservation.length_mm).abs() < 1e-9);
        }
    }
}

#[test]
fn angles_require_native_hundredth_degree_precision() {
    for angle in [0.0, 0.01, 45.12, 89.99, 90.0] {
        assert!(
            Options {
                outer_angle_degrees: angle,
                hole_angle_degrees: angle,
                ..options()
            }
            .validate()
            .is_ok()
        );
    }
    for (outer, hole) in [(45.001, 90.0), (45.0, 89.999)] {
        let error = Options {
            outer_angle_degrees: outer,
            hole_angle_degrees: hole,
            ..options()
        }
        .validate()
        .unwrap_err();
        assert!(error.to_string().contains("two decimal places"));
    }
}

#[test]
fn invalid_source_and_exclusion_inputs_fail_clearly() {
    let empty = job(Polygon {
        outer: vec![],
        holes: vec![],
    });
    assert!(prepare(&empty, &HashMap::new(), options(), &HashMap::new()).is_err());
    let valid = job(rectangle(0.0, 0.0, 20.0, 10.0));
    let unknown = HashMap::from([("missing".into(), vec![])]);
    assert!(prepare(&valid, &HashMap::new(), options(), &unknown).is_err());
    let inverted = HashMap::from([(
        "plate".into(),
        vec![Exclusion {
            contour_index: 0,
            from_mm: 10.0,
            to_mm: 2.0,
        }],
    )]);
    assert!(prepare(&valid, &HashMap::new(), options(), &inverted).is_err());
}

#[test]
fn final_validation_rebuilds_mixed_curves_in_physical_units() {
    use nestbolt_validator::job::{Layout, Placement, Sheet};
    let outer = Contour {
        start: [0.0, 0.0],
        segments: vec![
            Segment::Line { to: [20.0, 0.0] },
            Segment::Cubic {
                controls: [[25.0, 0.0], [25.0, 20.0]],
                to: [20.0, 20.0],
            },
            Segment::Quad {
                control: [10.0, 25.0],
                to: [0.0, 20.0],
            },
            Segment::Arc {
                center: [0.0, 10.0],
                radii: [10.0, 10.0],
                rotation: 0.0,
                start: PI / 2.0,
                sweep: PI,
            },
        ],
    };
    for units in [Units::Mm, Units::Inch] {
        let outer = outer.transformed(&Affine::scale(1.0 / units.to_mm()));
        let mut original = job(Polygon {
            outer: outer.flatten(0.005 / units.to_mm()).unwrap(),
            holes: vec![],
        });
        original.parts[0].quantity = 1;
        original.units = units;
        original.clearance /= units.to_mm();
        original.edge_clearance /= units.to_mm();
        original.stocks[0].width /= units.to_mm();
        original.stocks[0].height /= units.to_mm();
        let curves = HashMap::from([(
            "plate".into(),
            Outline {
                outer,
                holes: vec![],
            },
        )]);
        let layout = Layout {
            version: 1,
            units,
            sheets: vec![Sheet {
                id: "sheet-0".into(),
                stock_id: "sheet".into(),
            }],
            placements: vec![Placement {
                part_id: "plate".into(),
                copy_index: 0,
                sheet_id: "sheet-0".into(),
                transform: RigidTransform {
                    translation: [40.0 / units.to_mm(), 40.0 / units.to_mm()],
                    rotation_radians: 0.3,
                    mirrored: true,
                },
            }],
        };
        let initial = prepare(&original, &curves, options(), &HashMap::new()).unwrap();
        let report = finalize(&original, &curves, &layout, options(), &initial, &[]).unwrap();
        assert!(report.validation.valid && report.validation.source_checked);
        assert_eq!(report.reserved_contours, 1);
        assert_eq!(report.validation.coverage.unwrap().expected_contours, 1);
    }
}

#[test]
fn final_common_line_exclusions_choose_starts_per_copy_in_mm_and_inches() {
    use nestbolt_validator::job::{Layout, Placement, Sheet};
    for units in [Units::Mm, Units::Inch] {
        let mut original = job(rectangle(0.0, 0.0, 20.0, 10.0));
        let scale = units.to_mm();
        original.units = units;
        original.clearance /= scale;
        original.edge_clearance /= scale;
        original.stocks[0].width /= scale;
        original.stocks[0].height /= scale;
        for p in &mut original.parts[0].geometry[0].outer {
            p[0] /= scale;
            p[1] /= scale;
        }
        let layout = Layout {
            version: 1,
            units,
            sheets: vec![Sheet {
                id: "sheet-0".into(),
                stock_id: "sheet".into(),
            }],
            placements: [5.0, 25.2]
                .iter()
                .enumerate()
                .map(|(i, x)| Placement {
                    part_id: "plate".into(),
                    copy_index: i as u32,
                    sheet_id: "sheet-0".into(),
                    transform: RigidTransform {
                        translation: [x / scale, 5.0 / scale],
                        ..Default::default()
                    },
                })
                .collect(),
        };
        let initial = prepare_plain(&original, options());
        let common = crate::common_line::analyze(
            &original,
            &layout,
            &HashMap::new(),
            crate::common_line::Options { kerf_mm: 0.2 },
        )
        .unwrap();
        assert_eq!(common[0].shared_edges.len(), 1);
        let report = finalize(
            &original,
            &HashMap::new(),
            &layout,
            options(),
            &initial,
            &common,
        )
        .unwrap();
        assert_eq!(
            (
                report.expected_contours,
                report.reserved_contours,
                report.flagged_contours
            ),
            (2, 2, 0)
        );
        assert_eq!(report.parts[0].plan.reservations[0].start.segment, 0);
        assert!(report.validation.source_checked);
        let coverage = report.validation.coverage.as_ref().unwrap();
        assert_eq!(
            (
                coverage.expected_contours,
                coverage.reserved_contours,
                coverage.flagged_contours
            ),
            (2, 2, 0)
        );
        assert_eq!(report.parts[1].plan.reservations[0].start.segment, 1);
        assert_eq!(
            report.validation.metrics.as_ref().unwrap().placed_area,
            400.0
        );
        let review = report.review(&layout, "sheet-0").unwrap();
        assert_eq!(review.starts["plate#0"][0].unwrap().segment, 0);
        assert_eq!(review.starts["plate#1"][0].unwrap().segment, 1);
        assert_eq!(review.leadin.len(), 2);
        assert!(
            leads::validate(&original, &layout, &report.allowances())
                .unwrap()
                .valid
        );
    }
}

#[test]
fn final_report_accounts_for_flags_reselects_near_edges_and_refuses_invalid_layouts() {
    use nestbolt_validator::job::{Layout, Placement, Sheet};
    let mut polygon = rectangle(0.0, 0.0, 20.0, 10.0);
    polygon.holes.push(rectangle(10.0, 4.0, 0.4, 0.4).outer);
    let mut original = job(polygon);
    original.parts[0].quantity = 1;
    let mut layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: vec![Sheet {
            id: "sheet-0".into(),
            stock_id: "sheet".into(),
        }],
        placements: vec![Placement {
            part_id: "plate".into(),
            copy_index: 0,
            sheet_id: "sheet-0".into(),
            transform: RigidTransform {
                translation: [10.0, 10.0],
                ..Default::default()
            },
        }],
    };
    let initial = prepare_plain(&original, options());
    let report = finalize(
        &original,
        &HashMap::new(),
        &layout,
        options(),
        &initial,
        &[],
    )
    .unwrap();
    assert_eq!(
        (
            report.expected_contours,
            report.reserved_contours,
            report.flagged_contours
        ),
        (2, 1, 1)
    );
    assert_eq!(report.parts[0].plan.flags[0].contour_index, 1);
    layout.placements[0].transform.translation = [1.0, 1.0];
    assert!(
        nestbolt_validator::job::validate(&original, &layout)
            .unwrap()
            .valid
    );
    let revised = finalize(
        &original,
        &HashMap::new(),
        &layout,
        options(),
        &initial,
        &[],
    )
    .unwrap();
    assert!(revised.validation.valid);
    assert_eq!(revised.reserved_contours + revised.flagged_contours, 2);
    assert_ne!(revised.parts[0].plan.reservations[0].start.segment, 0);
    layout.placements[0].transform.translation = [-1.0, -1.0];
    assert!(
        finalize(
            &original,
            &HashMap::new(),
            &layout,
            options(),
            &initial,
            &[]
        )
        .is_err()
    );
}

#[test]
fn native_line_and_arc_calibrations_have_the_expected_length_radius_and_tangent() {
    let line = path([0.0, 0.0], [1.0, 0.0], 1.0, 3.0, 45.0, Style::Line).unwrap();
    let start = line.point(0.0);
    assert!((start[0] + 3.0 / 2_f64.sqrt()).abs() < 1e-12);
    assert!((start[1] - 3.0 / 2_f64.sqrt()).abs() < 1e-12);
    for degrees in [45.0, 90.0] {
        let arc = path([0.0, 0.0], [1.0, 0.0], 1.0, 3.0, degrees, Style::Arc).unwrap();
        let Path::Arc {
            radius_mm,
            sweep_radians,
            ..
        } = arc
        else {
            panic!("expected arc")
        };
        assert!((radius_mm - 3.0 / degrees.to_radians()).abs() < 1e-12);
        assert!((radius_mm * sweep_radians.abs() - 3.0).abs() < 1e-12);
        let end = arc.point(1.0);
        assert!(end[0].hypot(end[1]) < 1e-12);
        assert!(arc.point(0.999)[0] < 0.0);
        assert!(arc.point(0.999)[1] >= 0.0);
    }
}

#[test]
fn rectangle_uses_a_convex_corner_and_retains_original_job_and_physical_envelope() {
    let original = job(rectangle(0.0, 0.0, 20.0, 10.0));
    let before = serde_json::to_value(&original).unwrap();
    let result = prepare_plain(&original, options());
    assert_eq!(serde_json::to_value(&original).unwrap(), before);
    let plan = &result.parts[0];
    assert!(plan.flags.is_empty());
    assert_eq!(plan.reservations.len(), 1);
    let lead = &plan.reservations[0];
    assert_eq!((lead.start.segment, lead.start.parameter), (0, 0.0));
    assert_eq!(lead.length_mm, 3.0);
    assert_eq!(lead.paths.len(), 2);
    let combined = Footprint::from_polygons(
        &result.collision_job.parts[0].geometry,
        Units::Mm,
        RigidTransform::default(),
    )
    .unwrap();
    let physical = leads::footprint(&lead.paths, options().kerf_mm).unwrap();
    assert_eq!(physical.inside(&combined, 0.0).unwrap().outside_area, 0.0);
    assert!(combined.area() > 200.0);
    assert_eq!(result.collision_job.parts[0].quantity, 2);
}

#[test]
fn narrow_hole_shortens_and_tiny_hole_is_flagged_without_losing_coverage() {
    for (size, expected) in [(2.0, true), (0.4, false)] {
        let mut polygon = rectangle(0.0, 0.0, 20.0, 20.0);
        polygon.holes.push(rectangle(9.0, 9.0, size, size).outer);
        let result = prepare_plain(&job(polygon), options());
        let plan = &result.parts[0];
        assert_eq!(plan.contour_count, 2);
        assert_eq!(plan.reservations.len() + plan.flags.len(), 2);
        if expected {
            let hole = plan
                .reservations
                .iter()
                .find(|l| l.contour_index == 1)
                .unwrap();
            assert!(hole.shortened);
            assert!((0.5..1.8).contains(&hole.length_mm));
        } else {
            assert_eq!(plan.flags.len(), 1);
            assert_eq!(plan.flags[0].contour_index, 1);
        }
    }
}

#[test]
fn owner_rejects_interior_path_and_pierce_but_allows_a_tangent_arc_join() {
    let body = Footprint::new(
        &rectangle(0.0, -10.0, 20.0, 10.0),
        Units::Mm,
        RigidTransform::default(),
    )
    .unwrap();
    let owner = leads::Owner::new(body, 0.2).unwrap();
    let outside = path([10.0, 0.0], [1.0, 0.0], 1.0, 3.0, 45.0, Style::Arc).unwrap();
    assert!(owner.fits(&[outside]).unwrap());
    let inside = path([10.0, 0.0], [1.0, 0.0], -1.0, 3.0, 45.0, Style::Line).unwrap();
    assert!(!owner.fits(&[inside]).unwrap());
    let tangent = path([10.0, 0.0], [1.0, 0.0], 1.0, 3.0, 0.0, Style::Line).unwrap();
    assert!(
        !owner.fits(&[tangent]).unwrap(),
        "piercing on the material boundary is not waste-side"
    );
    let crossing = Path::Line {
        from_mm: [-3.0, -5.0],
        to_mm: [10.0, 0.0],
    };
    assert!(!owner.fits(&[crossing]).unwrap());
}

#[test]
fn exclusions_wrap_the_source_seam_and_all_excluded_contours_are_flagged() {
    let original = job(rectangle(0.0, 0.0, 20.0, 10.0));
    let exclusions = HashMap::from([(
        "plate".into(),
        vec![Exclusion {
            contour_index: 0,
            from_mm: 50.0,
            to_mm: 65.0,
        }],
    )]);
    let result = prepare(&original, &HashMap::new(), options(), &exclusions).unwrap();
    assert_ne!(result.parts[0].reservations[0].start.segment, 0);
    let exclusions = HashMap::from([(
        "plate".into(),
        vec![Exclusion {
            contour_index: 0,
            from_mm: 0.0,
            to_mm: 60.0,
        }],
    )]);
    let result = prepare(&original, &HashMap::new(), options(), &exclusions).unwrap();
    assert_eq!(result.parts[0].flags.len(), 1);
    assert!(result.parts[0].reservations.is_empty());
}

#[test]
fn smooth_round_hole_starts_towards_its_centre_and_keeps_exact_curve_start() {
    let circle = Contour {
        start: [12.0, 10.0],
        segments: vec![Segment::Arc {
            center: [10.0, 10.0],
            radii: [2.0, 2.0],
            rotation: 0.0,
            start: 0.0,
            sweep: TAU,
        }],
    };
    let mut polygon = rectangle(0.0, 0.0, 20.0, 20.0);
    polygon.holes.push(circle.flatten(0.01).unwrap());
    let original = job(polygon.clone());
    let mut outline = Outline::from_polygon(&polygon);
    outline.holes = vec![circle.clone()];
    let result = prepare(
        &original,
        &HashMap::from([("plate".into(), outline)]),
        options(),
        &HashMap::new(),
    )
    .unwrap();
    let lead = result.parts[0]
        .reservations
        .iter()
        .find(|l| l.contour_index == 1)
        .unwrap();
    assert!((lead.length_mm - 2.0).abs() < 0.0001);
    for path in &lead.paths {
        let p = path.point(0.0);
        assert!((p[0] - 10.0).hypot(p[1] - 10.0) < 0.0001);
    }
    let restarted = circle
        .restarted(lead.start.segment, lead.start.parameter)
        .unwrap();
    let end = lead.paths[0].point(1.0);
    assert!((end[0] - restarted.start[0]).hypot(end[1] - restarted.start[1]) < 1e-8);
}

#[test]
fn subdivided_hole_edge_is_chosen_by_its_full_length() {
    let mut polygon = rectangle(0.0, 0.0, 30.0, 30.0);
    polygon.holes.push(vec![
        [15.0, 10.0],
        [20.0, 10.0],
        [20.0, 14.0],
        [10.0, 14.0],
        [10.0, 10.0],
    ]);
    let original = job(polygon);
    let result = prepare_plain(&original, options());
    let lead = result.parts[0]
        .reservations
        .iter()
        .find(|l| l.contour_index == 1)
        .unwrap();
    let endpoint = lead.paths[0].point(1.0);
    assert!((endpoint[0] - 15.0).abs() < 1e-8);
    assert!((endpoint[1] - 10.0).abs() < 1e-8 || (endpoint[1] - 14.0).abs() < 1e-8);
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(64))]
    #[test]
    fn path_length_attachment_and_waste_side_survive_arbitrary_heading(
        theta in -PI..PI, angle in 1.0f64..90.0, length in 0.5f64..20.0, reverse in any::<bool>()
    ) {
        let t=[theta.cos(),theta.sin()];
        let side=if reverse {-1.0} else {1.0};
        let a=[13.0,-7.0];
        let curve=path(a,t,side,length,angle,Style::Arc).unwrap();
        let Path::Arc{radius_mm,sweep_radians,..}=curve else {unreachable!()};
        prop_assert!((radius_mm*sweep_radians.abs()-length).abs()<1e-10);
        let end=curve.point(1.0);
        prop_assert!(sub(a,end)[0].hypot(sub(a,end)[1])<1e-9);
        for i in 0..=16 {
            let d=sub(curve.point(i as f64/16.0),a);
            prop_assert!(side*cross(t,d)>=-1e-9);
        }
    }
    #[test]
    fn mm_and_inch_jobs_reserve_the_same_physical_geometry(width in 10.0f64..50.0,height in 10.0f64..50.0) {
        let mm=job(rectangle(0.0,0.0,width,height));
        let mut inch=mm.clone();inch.units=Units::Inch;
        for p in &mut inch.parts[0].geometry[0].outer {*p=mul(*p,1.0/25.4);}
        let a=prepare_plain(&mm,options());let b=prepare_plain(&inch,options());
        let make=|result:&Prepared,units|Footprint::from_polygons(&result.collision_job.parts[0].geometry,units,RigidTransform::default()).unwrap();
        let (a,b)=(make(&a,Units::Mm),make(&b,Units::Inch));
        prop_assert!((a.area()-b.area()).abs()<1e-5);
        for (x,y) in a.bounds().iter().zip(b.bounds()) {prop_assert!((x-y).abs()<1e-6);}
    }
}
