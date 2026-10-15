use std::f64::consts::TAU;

use nestbolt_validator::{
    Polygon, RigidTransform, Units,
    job::{Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock},
    leads::{
        self, Allowance, AttachedAllowance, Flag, Path,
        source::{self, Component, Contour, Segment, Start},
    },
};
use proptest::prelude::*;

fn rectangle(x: f64, y: f64, width: f64, height: f64) -> Polygon {
    Polygon {
        outer: vec![
            [x, y],
            [x + width, y],
            [x + width, y + height],
            [x, y + height],
        ],
        holes: vec![],
    }
}

fn fixture() -> (Job, Layout, Vec<source::Part>, AttachedAllowance) {
    let geometry = vec![rectangle(0.0, 0.0, 10.0, 10.0)];
    let sources = vec![source::Part {
        part_id: "part".into(),
        components: geometry
            .iter()
            .map(|p| Component::from_polygon(p).unwrap())
            .collect(),
        ..Default::default()
    }];
    let job = Job {
        version: 1,
        name: "independent source leads".into(),
        units: Units::Mm,
        parts: vec![Part {
            id: "part".into(),
            quantity: 1,
            geometry,
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
    };
    let layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: vec![Sheet {
            id: "sheet".into(),
            stock_id: "stock".into(),
        }],
        placements: vec![Placement {
            part_id: "part".into(),
            copy_index: 0,
            sheet_id: "sheet".into(),
            transform: RigidTransform {
                translation: [20.0, 20.0],
                ..Default::default()
            },
        }],
    };
    let lead = AttachedAllowance {
        allowance: Allowance {
            part_id: "part".into(),
            copy_index: 0,
            contour_index: 0,
            kerf_mm: 0.2,
            paths: vec![Path::Line {
                from_mm: [5.0, -3.0],
                to_mm: [5.0, 0.0],
            }],
        },
        start: Start {
            segment: 0,
            parameter: 0.5,
        },
    };
    (job, layout, sources, lead)
}

fn flag(id: &str, contour_index: usize) -> Flag {
    Flag {
        part_id: id.into(),
        copy_index: 0,
        contour_index,
        reason: "No safe candidate".into(),
    }
}

#[test]
fn native_cutting_coverage_uses_source_paths_instead_of_collision_proxy() {
    let (job, layout, mut sources, lead) = fixture();
    sources[0].basis = source::Basis::CuttingContours;
    sources[0]
        .components
        .push(Component::from_polygon(&rectangle(12.0, 0.0, 4.0, 4.0)).unwrap());
    sources[0].open_contours.push(Contour {
        start: [1.0, 1.0],
        segments: vec![Segment::Line { to: [2.0, 1.0] }],
    });
    let flags = [flag("part", 1), flag("part", 2)];
    let report =
        leads::validate_complete(&job, &layout, &sources, std::slice::from_ref(&lead), &flags)
            .unwrap();
    assert!(report.valid && report.source_checked);
    assert_eq!(report.coverage.unwrap().expected_contours, 3);
    assert!(
        !leads::validate_complete(
            &job,
            &layout,
            &sources,
            std::slice::from_ref(&lead),
            &flags[..1]
        )
        .unwrap()
        .valid
    );
    let mut open_lead = lead.clone();
    open_lead.allowance.contour_index = 2;
    assert!(
        leads::validate_complete(
            &job,
            &layout,
            &sources,
            &[lead.clone(), open_lead],
            &flags[..1]
        )
        .unwrap_err()
        .to_string()
        .contains("open cutting contours")
    );
    sources[0]
        .extra_material
        .push(Component::from_polygon(&rectangle(4.0, -4.0, 2.0, 2.0)).unwrap());
    let blocked = leads::validate_complete(&job, &layout, &sources, &[lead], &flags).unwrap();
    assert!(!blocked.valid);
    assert!(
        blocked
            .violations
            .iter()
            .any(|v| v.contains("own original material"))
    );
}

#[test]
fn ordinary_material_components_cannot_overlap_or_use_native_metadata() {
    let (mut job, layout, mut sources, _) = fixture();
    job.parts[0].geometry.push(rectangle(20.0, 0.0, 10.0, 10.0));
    sources[0]
        .components
        .push(Component::from_polygon(&rectangle(5.0, 0.0, 10.0, 10.0)).unwrap());
    assert!(
        leads::validate_complete(
            &job,
            &layout,
            &sources,
            &[],
            &[flag("part", 0), flag("part", 1)]
        )
        .is_err()
    );
    sources[0].components[1] = Component::from_polygon(&job.parts[0].geometry[1]).unwrap();
    let extra = sources[0].components[0].clone();
    sources[0].extra_material.push(extra);
    assert!(
        leads::validate_complete(
            &job,
            &layout,
            &sources,
            &[],
            &[flag("part", 0), flag("part", 1)]
        )
        .unwrap_err()
        .to_string()
        .contains("extra cutting metadata")
    );
}

#[test]
fn independent_coverage_requires_one_decision_for_each_placed_contour() {
    let (job, layout, sources, lead) = fixture();
    let full = leads::validate_complete(&job, &layout, &sources, std::slice::from_ref(&lead), &[])
        .unwrap();
    assert!(full.valid && full.source_checked);
    let coverage = full.coverage.unwrap();
    assert_eq!(
        (
            coverage.expected_contours,
            coverage.reserved_contours,
            coverage.flagged_contours
        ),
        (1, 1, 0)
    );
    let missing = leads::validate_complete(&job, &layout, &sources, &[], &[]).unwrap();
    assert!(!missing.valid && missing.metrics.is_none());
    assert!(missing.violations[0].contains("missing lead"));
    assert!(
        leads::validate_complete(&job, &layout, &sources, &[], &[flag("part", 0)])
            .unwrap()
            .valid
    );
    for flags in [
        vec![flag("part", 0)],
        vec![flag("part", 1)],
        vec![flag("absent", 0)],
    ] {
        assert!(
            leads::validate_complete(&job, &layout, &sources, std::slice::from_ref(&lead), &flags)
                .is_err()
        );
    }
    assert!(leads::validate_complete(&job, &layout, &sources, &[lead.clone(), lead], &[]).is_err());
    let mut empty = flag("part", 0);
    empty.reason = "  ".into();
    assert!(leads::validate_complete(&job, &layout, &sources, &[], &[empty]).is_err());
    let partial = leads::validate(&job, &layout, &[]).unwrap();
    assert!(partial.coverage.is_none() && !partial.source_checked);
}

#[test]
fn altered_start_and_inward_lead_fail_even_when_partial_checks_pass() {
    let (job, layout, sources, lead) = fixture();
    let mut wrong_start = lead.clone();
    wrong_start.start.parameter = 0.6;
    let mut detached = lead.clone();
    detached.allowance.paths = vec![Path::Line {
        from_mm: [5.0, -3.0],
        to_mm: [5.0, -0.01],
    }];
    let mut inward = lead;
    inward.allowance.paths = vec![Path::Line {
        from_mm: [5.0, 3.0],
        to_mm: [5.0, 0.0],
    }];
    for (bad, message) in [
        (wrong_start, "attachment"),
        (detached, "attachment"),
        (inward, "own original material"),
    ] {
        assert!(
            leads::validate(&job, &layout, std::slice::from_ref(&bad.allowance))
                .unwrap()
                .valid
        );
        let report = leads::validate_complete(&job, &layout, &sources, &[bad], &[]).unwrap();
        assert!(!report.valid && report.metrics.is_none());
        assert!(
            report.violations.iter().any(|v| v.contains(message)),
            "{:?}",
            report.violations
        );
    }
}

#[test]
fn component_and_hole_coverage_is_derived_from_original_job() {
    let (mut job, layout, mut sources, _) = fixture();
    job.parts[0].geometry[0]
        .holes
        .push(rectangle(3.0, 3.0, 4.0, 4.0).outer);
    job.parts[0].geometry.push(rectangle(20.0, 0.0, 5.0, 5.0));
    sources[0].components = job.parts[0]
        .geometry
        .iter()
        .map(|p| Component::from_polygon(p).unwrap())
        .collect();
    let flags = [flag("part", 0), flag("part", 1), flag("part", 2)];
    let report = leads::validate_complete(&job, &layout, &sources, &[], &flags).unwrap();
    assert!(report.valid);
    assert_eq!(report.coverage.unwrap().expected_contours, 3);
    assert!(
        !leads::validate_complete(&job, &layout, &sources, &[], &flags[..2])
            .unwrap()
            .valid
    );
    sources[0].components[0].holes.clear();
    assert!(leads::validate_complete(&job, &layout, &sources, &[], &flags).is_err());
}

#[test]
fn exact_curved_neighbour_is_checked_beyond_its_coarse_search_polygon() {
    let (mut job, mut layout, mut sources, lead) = fixture();
    let diamond = Polygon {
        outer: vec![[4.0, 0.0], [0.0, 4.0], [-4.0, 0.0], [0.0, -4.0]],
        holes: vec![],
    };
    let mut neighbour = job.parts[0].clone();
    neighbour.id = "circle".into();
    neighbour.geometry = vec![diamond];
    job.parts.push(neighbour);
    let mut placed = layout.placements[0].clone();
    placed.part_id = "circle".into();
    placed.transform.translation = [23.0, 14.0];
    layout.placements.push(placed);
    sources.push(source::Part {
        part_id: "circle".into(),
        components: vec![Component {
            outer: Contour {
                start: [4.0, 0.0],
                segments: vec![Segment::Arc {
                    center: [0.0, 0.0],
                    radii: [4.0, 4.0],
                    rotation: 0.0,
                    start: 0.0,
                    sweep: TAU,
                }],
            },
            holes: vec![],
        }],
        ..Default::default()
    });
    assert!(
        leads::validate(&job, &layout, std::slice::from_ref(&lead.allowance))
            .unwrap()
            .valid
    );
    let report =
        leads::validate_complete(&job, &layout, &sources, &[lead], &[flag("circle", 0)]).unwrap();
    assert!(!report.valid);
    assert!(
        report
            .violations
            .iter()
            .any(|v| v.contains("overlaps part circle"))
    );
}

fn segment_distance(p: [f64; 2], a: [f64; 2], b: [f64; 2]) -> f64 {
    let dx = b[0] - a[0];
    let dy = b[1] - a[1];
    let norm = dx * dx + dy * dy;
    let t = if norm == 0.0 {
        0.0
    } else {
        (((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / norm).clamp(0.0, 1.0)
    };
    (p[0] - a[0] - t * dx).hypot(p[1] - a[1] - t * dy)
}

fn boundary_distance(point: [f64; 2], ring: &[[f64; 2]]) -> f64 {
    ring.iter()
        .zip(ring.iter().cycle().skip(1))
        .take(ring.len())
        .map(|(&a, &b)| segment_distance(point, a, b))
        .fold(f64::INFINITY, f64::min)
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(64))]
    #[test]
    fn independent_bezier_samples_and_flattening_match_de_casteljau(
        controls in prop::array::uniform4(prop::array::uniform2(-20.0f64..20.0)), quadratic in any::<bool>(), inches in any::<bool>(), parameter in 0.0f64..1.0
    ) {
        let units = if inches { Units::Inch } else { Units::Mm };
        let segment = if quadratic { Segment::Quad { control: controls[1], to: controls[2] } }
            else { Segment::Cubic { controls: [controls[1],controls[2]], to: controls[3] } };
        let contour = Contour { start: controls[0], segments: vec![segment,Segment::Line { to: controls[0] }] };
        let flattened = contour.flatten_mm(units).unwrap();
        for t in (0..=64).map(|i| i as f64/64.0).chain(std::iter::once(parameter)) {
            let mut row = controls[..if quadratic {3} else {4}].to_vec();
            while row.len()>1 {
                row=row.windows(2).map(|pair| std::array::from_fn(|k| pair[0][k]+t*(pair[1][k]-pair[0][k]))).collect();
            }
            let expected = row[0].map(|v| v*units.to_mm());
            let actual = contour.point_mm(Start { segment: 0, parameter: t }, units).unwrap();
            prop_assert!((expected[0]-actual[0]).hypot(expected[1]-actual[1])<1e-9);
            prop_assert!(boundary_distance(expected,&flattened)<=leads::ENVELOPE_TOLERANCE_MM+1e-9);
        }
    }

    #[test]
    fn independent_ellipse_flattening_respects_physical_error(
        rx in 0.1f64..20.0, ry in 0.1f64..20.0, angle in -3.0f64..3.0, start in -3.0f64..3.0, reverse in any::<bool>(), inches in any::<bool>()
    ) {
        let units=if inches { Units::Inch } else { Units::Mm };
        let point=|t: f64| [rx*t.cos()*angle.cos()-ry*t.sin()*angle.sin()+2.0,rx*t.cos()*angle.sin()+ry*t.sin()*angle.cos()-3.0];
        let sweep=if reverse {-TAU} else {TAU};
        let contour=Contour { start: point(start), segments: vec![Segment::Arc { center: [2.0,-3.0], radii:[rx,ry],rotation:angle,start,sweep }] };
        let ring=contour.flatten_mm(units).unwrap();
        for i in 0..129 {
            let t=i as f64/128.0;
            let expected=point(start+sweep*t).map(|v| v*units.to_mm());
            let actual=contour.point_mm(Start { segment:0,parameter:t },units).unwrap();
            prop_assert!((expected[0]-actual[0]).hypot(expected[1]-actual[1])<1e-9);
            prop_assert!(boundary_distance(expected,&ring)<=leads::ENVELOPE_TOLERANCE_MM+1e-9);
        }
    }

    #[test]
    fn complete_checks_preserve_units_rotation_and_mirroring(angle in -std::f64::consts::PI..std::f64::consts::PI, mirror in any::<bool>(), inches in any::<bool>()) {
        let (mut job,mut layout,mut sources,lead)=fixture();
        let scale=if inches {25.4} else {1.0};
        if inches {job.units=Units::Inch;layout.units=Units::Inch;}
        for polygon in &mut job.parts[0].geometry { for p in &mut polygon.outer { *p=p.map(|v| v/scale); } }
        for stock in &mut job.stocks { stock.width/=scale;stock.height/=scale; }
        sources[0].components=job.parts[0].geometry.iter().map(|p| Component::from_polygon(p).unwrap()).collect();
        layout.placements[0].transform=RigidTransform {translation:[40.0/scale,40.0/scale],rotation_radians:angle,mirrored:mirror};
        let result=leads::validate_complete(&job,&layout,&sources,&[lead],&[]).unwrap();
        prop_assert!(result.valid,"{:?}",result.violations);
        prop_assert!((result.metrics.unwrap().placed_area-100.0).abs()<1e-8);
    }
}

#[test]
fn source_degeneracy_and_resource_limits_fail_explicitly() {
    let square = Contour::from_ring(&rectangle(0.0, 0.0, 10.0, 10.0).outer).unwrap();
    for start in [
        Start {
            segment: 4,
            parameter: 0.0,
        },
        Start {
            segment: 0,
            parameter: f64::NAN,
        },
        Start {
            segment: 0,
            parameter: -0.1,
        },
    ] {
        assert!(square.point_mm(start, Units::Mm).is_err());
    }
    let mut open = square;
    open.segments.pop();
    assert!(open.flatten_mm(Units::Mm).is_err());
    let disconnected = Contour {
        start: [4.0, 0.0],
        segments: vec![Segment::Arc {
            center: [0.0, 0.0],
            radii: [5.0, 5.0],
            rotation: 0.0,
            start: 0.0,
            sweep: TAU,
        }],
    };
    assert!(disconnected.flatten_mm(Units::Mm).is_err());
    let excessive = Contour {
        start: [1e6, 0.0],
        segments: vec![Segment::Arc {
            center: [0.0, 0.0],
            radii: [1e6, 1e6],
            rotation: 0.0,
            start: 0.0,
            sweep: TAU,
        }],
    };
    assert!(excessive.flatten_mm(Units::Mm).is_err());
    // Collinear backtracking cannot be replaced with a chord that misses it.
    let backtrack = Contour {
        start: [0.0, 0.0],
        segments: vec![
            Segment::Cubic {
                controls: [[10.0, 0.0], [-10.0, 0.0]],
                to: [0.0, 0.0],
            },
            Segment::Line { to: [0.0, -1.0] },
            Segment::Line { to: [0.0, 0.0] },
        ],
    };
    let ring = backtrack.flatten_mm(Units::Mm).unwrap();
    assert!(ring.iter().any(|p| p[0] > 2.8) && ring.iter().any(|p| p[0] < -2.8));
}

#[test]
fn collision_guard_expands_rounding_slivers_but_refuses_missing_material() {
    use nestbolt_validator::Footprint;
    let body = Footprint::new(
        &rectangle(0.0, 0.0, 10.0, 10.0),
        Units::Mm,
        RigidTransform::default(),
    )
    .unwrap();
    for missing_width in [0.0, 0.000001, 0.001] {
        let envelope = Footprint::new(
            &rectangle(0.0, 0.0, 10.0 - missing_width, 10.0),
            Units::Mm,
            RigidTransform::default(),
        )
        .unwrap();
        let guarded = leads::collision_polygons(&envelope, &body);
        if missing_width > 0.000002 {
            assert!(guarded.is_err());
        } else {
            let rebuilt =
                Footprint::from_polygons(&guarded.unwrap(), Units::Mm, RigidTransform::default())
                    .unwrap();
            assert_eq!(body.inside(&rebuilt, 0.0).unwrap().outside_area, 0.0);
            for (a, b) in rebuilt.bounds().into_iter().zip(envelope.bounds()) {
                assert!((a - b).abs() <= 0.0000021);
            }
        }
    }
}
