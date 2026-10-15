use std::collections::HashMap;

use clipper2_rust::{ClipperOffset, EndType, JoinType, Path64, Point64};
use nestbolt_core::{
    common_line::{self, Options},
    curves::{Contour, Segment},
    export::{self, Outline, ReviewPaths},
};
use nestbolt_validator::{
    Polygon, RigidTransform, Units,
    job::{Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle},
};
use proptest::prelude::*;

fn fixture(
    width: f64,
    height: f64,
    kerf: f64,
    angle: f64,
    mirror: bool,
    y_offset: f64,
) -> (Job, Layout) {
    let job = Job {
        version: 1,
        name: "compensated pair".into(),
        units: Units::Mm,
        parts: vec![Part {
            id: "panel".into(),
            quantity: 2,
            geometry: vec![rectangle(0.0, 0.0, width, height)],
            rotations: Rotations::Free,
            allow_mirror: true,
            priority: 1.0,
        }],
        stocks: vec![Stock {
            id: "stock".into(),
            width: 500.0,
            height: 500.0,
            count: None,
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
        clearance: kerf,
        edge_clearance: 0.0,
        mode: Mode::All,
    };
    let r = angle.to_radians();
    let (s, c) = r.sin_cos();
    let dx = (width + kerf) * if mirror { -1.0 } else { 1.0 };
    let layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: vec![Sheet {
            id: "sheet".into(),
            stock_id: "stock".into(),
        }],
        placements: vec![
            Placement {
                part_id: "panel".into(),
                copy_index: 0,
                sheet_id: "sheet".into(),
                transform: RigidTransform {
                    translation: [200.0, 200.0],
                    rotation_radians: r,
                    mirrored: mirror,
                },
            },
            Placement {
                part_id: "panel".into(),
                copy_index: 1,
                sheet_id: "sheet".into(),
                transform: RigidTransform {
                    translation: [200.0 + c * dx - s * y_offset, 200.0 + s * dx + c * y_offset],
                    rotation_radians: r,
                    mirrored: mirror,
                },
            },
        ],
    };
    (job, layout)
}

fn report(job: &Job, layout: &Layout, kerf: f64) -> common_line::Report {
    common_line::analyze(
        job,
        layout,
        &HashMap::new(),
        Options {
            kerf_mm: kerf,
            search_bonus: false,
        },
    )
    .unwrap()
    .remove(0)
}

/// Independent offset oracle: direct Clipper2 integer miter offset of the
/// original polygon, transformed here without the product's export helpers.
fn offset_boundary(
    polygon: &Polygon,
    transform: &RigidTransform,
    delta: f64,
) -> Vec<Vec<[f64; 2]>> {
    let (s, c) = transform.rotation_radians.sin_cos();
    let mut points: Vec<_> = polygon
        .outer
        .iter()
        .map(|&[x, y]| {
            let x = if transform.mirrored { -x } else { x };
            [
                c * x - s * y + transform.translation[0],
                s * x + c * y + transform.translation[1],
            ]
        })
        .collect();
    let area: f64 = points
        .iter()
        .zip(points.iter().cycle().skip(1))
        .take(points.len())
        .map(|(a, b)| a[0] * b[1] - a[1] * b[0])
        .sum();
    if area < 0.0 {
        points.reverse();
    }
    let path: Path64 = points
        .iter()
        .map(|p| Point64::new((p[0] * 1e6).round() as i64, (p[1] * 1e6).round() as i64))
        .collect();
    let mut engine = ClipperOffset::new(2.0, 0.0, false, false);
    engine.add_path(&path, JoinType::Miter, EndType::Polygon);
    let mut result = vec![];
    engine.execute(delta * 1e6, &mut result);
    result
        .iter()
        .map(|ring| {
            ring.iter()
                .map(|p| [p.x as f64 / 1e6, p.y as f64 / 1e6])
                .collect()
        })
        .collect()
}

fn point_distance(p: [f64; 2], rings: &[Vec<[f64; 2]>]) -> f64 {
    rings
        .iter()
        .flat_map(|ring| {
            ring.iter()
                .zip(ring.iter().cycle().skip(1))
                .take(ring.len())
        })
        .map(|(a, b)| {
            let d = [b[0] - a[0], b[1] - a[1]];
            let len = d[0] * d[0] + d[1] * d[1];
            let t = (((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / len).clamp(0.0, 1.0);
            (p[0] - a[0] - t * d[0]).hypot(p[1] - a[1] - t * d[1])
        })
        .fold(f64::INFINITY, f64::min)
}

fn check_offset(job: &Job, layout: &Layout, report: &common_line::Report) {
    let boundaries: Vec<_> = layout
        .placements
        .iter()
        .map(|p| {
            offset_boundary(
                &job.parts[0].geometry[0],
                &p.transform,
                report.kerf_mm / 2.0,
            )
        })
        .collect();
    assert_eq!(report.paths.len(), 1);
    let mut from = report.paths[0].start;
    for segment in &report.paths[0].segments {
        let to = segment.end();
        for i in 0..=32 {
            let t = i as f64 / 32.0;
            let p = [
                from[0] + t * (to[0] - from[0]),
                from[1] + t * (to[1] - from[1]),
            ];
            for boundary in &boundaries {
                assert!(point_distance(p, boundary) < 0.000003, "point {p:?}");
            }
        }
        from = to;
    }
}

#[test]
fn compensated_pair_preserves_cut_size_and_exports_one_shared_path() {
    for kerf in [0.2, 1.5] {
        let (job, layout) = fixture(40.0, 30.0, kerf, 0.0, false, 0.0);
        let r = report(&job, &layout, kerf);
        assert_eq!(r.shared_edges.len(), 1);
        assert!((r.shared_length_mm - 30.0).abs() < 1e-8);
        assert!((r.cut_length_without_common_mm - 280.0).abs() < 1e-8);
        assert!((r.cut_length_with_common_mm - 250.0).abs() < 1e-8);
        assert_eq!((r.contours_without_common, r.paths_with_common), (2, 3));
        check_offset(&job, &layout, &r);
        let review = ReviewPaths {
            common: r.paths.clone(),
            ..Default::default()
        };
        let options = export::Options {
            sheet_outline: true,
        };
        let svg = export::svg_with_review_paths(
            &job,
            &layout,
            "sheet",
            &HashMap::new(),
            options,
            &review,
        )
        .unwrap();
        assert!(svg.contains("id=\"COMMON\""));
        assert!(svg.contains("stroke=\"#0000ff\""));
        let source =
            nestbolt_core::import::import_svg(&svg, &nestbolt_core::import::Options::default())
                .unwrap();
        assert_eq!(source.parts.len(), 2);
        for p in source.parts {
            assert!((p.bounds[2] - p.bounds[0] - 40.0).abs() < 1e-6);
            assert!((p.bounds[3] - p.bounds[1] - 30.0).abs() < 1e-6);
        }
        let dxf = export::dxf_with_review_paths(
            &job,
            &layout,
            "sheet",
            &HashMap::new(),
            options,
            &review,
        )
        .unwrap();
        let source = nestbolt_core::import::import_dxf(&dxf, &Default::default()).unwrap();
        assert_eq!(source.parts.len(), 2);
        assert!(
            source
                .report
                .layers
                .iter()
                .any(|l| l.name == "COMMON" && l.geometry_entities == 1)
        );
    }
}

#[test]
fn partial_matches_subdivisions_and_layout_order_preserve_shared_length() {
    let (mut job, mut layout) = fixture(40.0, 30.0, 0.2, 0.0, false, 10.0);
    let p = &mut job.parts[0].geometry[0].outer;
    *p = vec![
        [0.0, 5.0],
        [0.0, 0.0],
        [40.0, 0.0],
        [40.0, 5.0],
        [40.0, 10.0],
        [40.0, 15.0],
        [40.0, 20.0],
        [40.0, 25.0],
        [40.0, 30.0],
        [0.0, 30.0],
        [0.0, 25.0],
        [0.0, 20.0],
        [0.0, 15.0],
        [0.0, 10.0],
    ];
    let r = report(&job, &layout, 0.2);
    assert!((r.shared_length_mm - 20.0).abs() < 1e-8);
    assert_eq!(r.paths_with_common, 3);
    layout.placements.reverse();
    let replay = report(&job, &layout, 0.2);
    assert_eq!(r.paths, replay.paths);
}

#[test]
fn minimum_length_spacing_and_physical_units_are_enforced() {
    let (job, layout) = fixture(40.0, 9.9, 0.2, 0.0, false, 0.0);
    assert!(report(&job, &layout, 0.2).paths.is_empty());
    let (mut job, layout) = fixture(40.0, 10.0, 0.2, 0.0, false, 0.0);
    assert!((report(&job, &layout, 0.2).shared_length_mm - 10.0).abs() < 1e-8);
    for kerf in [0.0, 0.049, f64::INFINITY, f64::NAN] {
        assert!(
            Options {
                kerf_mm: kerf,
                search_bonus: false
            }
            .validate()
            .is_err()
        );
    }
    job.clearance = 0.1;
    assert!(
        common_line::analyze(
            &job,
            &layout,
            &HashMap::new(),
            Options {
                kerf_mm: 0.2,
                search_bonus: false
            }
        )
        .unwrap_err()
        .to_string()
        .contains("spacing = kerf")
    );
    job.clearance = 0.2;
    job.units = Units::Unitless;
    assert!(
        common_line::analyze(
            &job,
            &layout,
            &HashMap::new(),
            Options {
                kerf_mm: 0.2,
                search_bonus: false
            }
        )
        .is_err()
    );
}

#[test]
fn holes_sheet_edges_and_other_sheets_are_not_shared() {
    let (mut job, mut layout) = fixture(40.0, 30.0, 0.2, 0.0, false, 0.0);
    job.parts[0].geometry[0]
        .holes
        .push(rectangle(10.0, 10.0, 10.0, 10.0).outer);
    let r = report(&job, &layout, 0.2);
    assert!((r.shared_length_mm - 30.0).abs() < 1e-8);
    assert_eq!(r.contours_without_common, 4);
    layout.sheets.push(Sheet {
        id: "other".into(),
        stock_id: "stock".into(),
    });
    layout.placements[1].sheet_id = "other".into();
    let r = common_line::analyze(
        &job,
        &layout,
        &HashMap::new(),
        Options {
            kerf_mm: 0.2,
            search_bonus: false,
        },
    )
    .unwrap();
    assert!(r.iter().all(|r| r.paths.is_empty()));
    // A valid part inside a host hole is rejected for common-line mode.
    job.parts[0].quantity = 1;
    job.parts.push(Part {
        id: "small".into(),
        quantity: 1,
        geometry: vec![rectangle(0.0, 0.0, 5.0, 5.0)],
        rotations: Rotations::Free,
        allow_mirror: false,
        priority: 1.0,
    });
    layout.sheets.pop();
    layout.placements[1] = Placement {
        part_id: "small".into(),
        copy_index: 0,
        sheet_id: "sheet".into(),
        transform: RigidTransform {
            translation: [211.0, 211.0],
            ..Default::default()
        },
    };
    assert!(
        common_line::analyze(
            &job,
            &layout,
            &HashMap::new(),
            Options {
                kerf_mm: 0.2,
                search_bonus: false
            }
        )
        .unwrap_err()
        .to_string()
        .contains("part-in-hole disabled")
    );
}

#[test]
fn curved_portions_are_counted_but_never_polygonized_into_common_lines() {
    let (job, layout) = fixture(40.0, 30.0, 0.2, 0.0, false, 0.0);
    // Round the top inward; the common vertical edge still ends at y=30.
    let contour = Contour {
        start: [0.0, 0.0],
        segments: vec![
            Segment::Line { to: [40.0, 0.0] },
            Segment::Line { to: [40.0, 30.0] },
            Segment::Cubic {
                controls: [[30.0, 20.0], [10.0, 20.0]],
                to: [0.0, 30.0],
            },
            Segment::Line { to: [0.0, 0.0] },
        ],
    };
    let curves = HashMap::from([(
        "panel".into(),
        Outline {
            outer: contour,
            holes: vec![],
        },
    )]);
    let r = common_line::analyze(
        &job,
        &layout,
        &curves,
        Options {
            kerf_mm: 0.2,
            search_bonus: false,
        },
    )
    .unwrap()
    .remove(0);
    assert!((r.shared_length_mm - 30.0).abs() < 1e-8);
    assert!(r.cut_length_without_common_mm > 280.0);
    assert!((r.saved_length_mm - 30.0).abs() < 1e-8);
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(64))]
    #[test]
    fn analytic_common_offsets_match_independent_clipper(
        w in 12.0..80.0_f64,h in 12.0..80.0_f64,kerf in 0.05..2.0_f64,
        angle in 0.0..360.0_f64,mirror in any::<bool>(),
    ) {
        let (job,layout)=fixture(w,h,kerf,angle,mirror,0.0);
        let r=report(&job,&layout,kerf);
        prop_assert!((r.shared_length_mm-h).abs()<1e-7);
        check_offset(&job,&layout,&r);
    }
}
