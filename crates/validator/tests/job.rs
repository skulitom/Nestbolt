use nestbolt_validator::{Polygon, RigidTransform, Units, job::*};

fn part(id: &str, w: f64, h: f64, quantity: u32) -> Part {
    Part {
        id: id.into(),
        quantity,
        geometry: vec![rectangle(0.0, 0.0, w, h)],
        rotations: Rotations::Step { degrees: 90.0 },
        allow_mirror: false,
        priority: 1.0,
    }
}
fn stock(id: &str, w: f64, h: f64, count: Option<u32>) -> Stock {
    Stock {
        id: id.into(),
        width: w,
        height: h,
        count,
        margins: Margins::default(),
        outline: vec![],
        defects: vec![],
    }
}
fn placement(part_id: &str, copy: u32, sheet: &str, x: f64, y: f64) -> Placement {
    Placement {
        part_id: part_id.into(),
        copy_index: copy,
        sheet_id: sheet.into(),
        transform: RigidTransform {
            translation: [x, y],
            ..Default::default()
        },
    }
}
fn fixture() -> (Job, Layout) {
    (
        Job {
            version: 1,
            name: "test".into(),
            units: Units::Mm,
            parts: vec![part("a", 10.0, 10.0, 2)],
            stocks: vec![stock("stock", 100.0, 100.0, None)],
            clearance: 0.0,
            edge_clearance: 0.0,
            mode: Mode::All,
        },
        Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![Sheet {
                id: "one".into(),
                stock_id: "stock".into(),
            }],
            placements: vec![
                placement("a", 0, "one", 0.0, 0.0),
                placement("a", 1, "one", 10.0, 0.0),
            ],
        },
    )
}
fn has(report: &Report, code: &str) -> bool {
    !report.valid && report.metrics.is_none() && report.violations.iter().any(|v| v.code == code)
}

#[test]
fn equal_stock_metric_matches_the_plan_formula() {
    let (job, mut layout) = fixture();
    layout.sheets.push(Sheet {
        id: "two".into(),
        stock_id: "stock".into(),
    });
    layout.placements[1].sheet_id = "two".into();
    layout.placements[1].transform.translation = [0.0, 40.0];
    let report = validate(&job, &layout).unwrap();
    assert!(report.valid, "{:?}", report.violations);
    let m = report.metrics.unwrap();
    // The shorter occupied sheet is selected as the final sheet, independent of order.
    assert!((m.normalized_material - (1.0 + 10.0 / 100.0)).abs() < 1e-10);
    assert_eq!(m.last_sheet_id.as_deref(), Some("one"));
    assert_eq!(m.placed_area, 200.0);
    assert_eq!(m.material_area, 11000.0);
    assert_eq!(m.trailing_offcut_area, 9000.0);
    layout.sheets.reverse();
    assert_eq!(
        validate(&job, &layout)
            .unwrap()
            .metrics
            .unwrap()
            .material_area,
        m.material_area
    );
}

#[test]
fn mixed_stock_metric_uses_actual_area_and_one_trailing_offcut() {
    let (mut job, mut layout) = fixture();
    job.stocks.push(stock("small", 20.0, 20.0, Some(1)));
    layout.sheets.push(Sheet {
        id: "two".into(),
        stock_id: "small".into(),
    });
    layout.placements[1].sheet_id = "two".into();
    layout.placements[1].transform.translation = [0.0, 0.0];
    let m = validate(&job, &layout).unwrap().metrics.unwrap();
    assert_eq!(m.full_stock_area, 10400.0);
    assert_eq!(m.material_area, 1400.0);
    assert!((m.normalized_material - 0.14).abs() < 1e-10);
    // Charging one arbitrary 'sheet unit' per differently-sized sheet would be wrong.
    assert_eq!(m.last_sheet_id.as_deref(), Some("one"));
}

#[test]
fn rejects_duplicates_missing_copies_unknown_parts_and_nonrigid_fields() {
    let (job, layout) = fixture();
    let mut duplicate = layout.clone();
    duplicate.placements[1].copy_index = 0;
    assert!(has(&validate(&job, &duplicate).unwrap(), "copy"));
    let mut missing = layout.clone();
    missing.placements.pop();
    assert!(has(&validate(&job, &missing).unwrap(), "quantity"));
    let mut unknown = layout.clone();
    unknown.placements[1].part_id = "unknown".into();
    assert!(has(&validate(&job, &unknown).unwrap(), "part_id"));
    let mut data = serde_json::to_value(&layout).unwrap();
    data["placements"][0]["transform"]["scale"] = serde_json::json!(0.5);
    assert!(serde_json::from_value::<Layout>(data).is_err());
}

#[test]
fn enforces_stock_limits_and_rejects_empty_or_duplicate_sheets() {
    let (mut job, mut layout) = fixture();
    job.stocks[0].count = Some(1);
    layout.sheets.push(Sheet {
        id: "two".into(),
        stock_id: "stock".into(),
    });
    layout.placements[1].sheet_id = "two".into();
    assert!(has(&validate(&job, &layout).unwrap(), "stock_limit"));
    job.stocks[0].count = None;
    assert!(validate(&job, &layout).unwrap().valid);
    layout.sheets.push(Sheet {
        id: "empty".into(),
        stock_id: "stock".into(),
    });
    assert!(has(&validate(&job, &layout).unwrap(), "empty_sheet"));
    layout.sheets.pop();
    layout.sheets[1].id = "one".into();
    assert!(has(&validate(&job, &layout).unwrap(), "sheet_id"));
}

#[test]
fn step_list_free_and_mirror_rules_are_checked() {
    let (mut job, mut layout) = fixture();
    layout.placements[1].transform = RigidTransform {
        rotation_radians: std::f64::consts::FRAC_PI_4,
        translation: [40.0, 40.0],
        mirrored: false,
    };
    assert!(has(&validate(&job, &layout).unwrap(), "rotation"));
    job.parts[0].rotations = Rotations::List {
        degrees: vec![0.0, 45.0],
    };
    assert!(validate(&job, &layout).unwrap().valid);
    job.parts[0].rotations = Rotations::Free;
    layout.placements[1].transform.rotation_radians = 0.123;
    assert!(validate(&job, &layout).unwrap().valid);
    layout.placements[1].transform.mirrored = true;
    assert!(has(&validate(&job, &layout).unwrap(), "mirror"));
    job.parts[0].allow_mirror = true;
    assert!(validate(&job, &layout).unwrap().valid);
}

#[test]
fn margins_edges_defects_and_interpart_clearance_are_separate() {
    let (mut job, mut layout) = fixture();
    job.stocks[0].margins = Margins {
        left: 2.0,
        right: 2.0,
        bottom: 2.0,
        top: 2.0,
    };
    assert!(has(&validate(&job, &layout).unwrap(), "containment"));
    layout.placements[0].transform.translation = [2.0, 2.0];
    layout.placements[1].transform.translation = [12.0, 2.0];
    assert!(validate(&job, &layout).unwrap().valid);
    job.edge_clearance = 1.0;
    assert!(has(&validate(&job, &layout).unwrap(), "edge_clearance"));
    layout.placements[0].transform.translation = [3.0, 3.0];
    layout.placements[1].transform.translation = [13.0, 3.0];
    assert!(validate(&job, &layout).unwrap().valid);
    job.clearance = 0.5;
    assert!(has(&validate(&job, &layout).unwrap(), "clearance"));
    layout.placements[1].transform.translation = [14.0, 3.0];
    assert!(validate(&job, &layout).unwrap().valid);
    job.stocks[0].defects.push(rectangle(5.0, 5.0, 2.0, 2.0));
    assert!(has(&validate(&job, &layout).unwrap(), "containment"));
}

#[test]
fn parts_can_nest_in_holes_and_disconnected_components_stay_rigid() {
    let (mut job, mut layout) = fixture();
    job.parts = vec![part("frame", 30.0, 30.0, 1), part("inside", 5.0, 5.0, 1)];
    job.parts[0].geometry[0]
        .holes
        .push(rectangle(5.0, 5.0, 20.0, 20.0).outer);
    layout.placements = vec![
        placement("frame", 0, "one", 0.0, 0.0),
        placement("inside", 0, "one", 10.0, 10.0),
    ];
    job.clearance = 2.0;
    assert!(validate(&job, &layout).unwrap().valid);
    job.parts[1].geometry.push(rectangle(7.0, 0.0, 2.0, 2.0));
    assert!(validate(&job, &layout).unwrap().valid);
    job.parts[1].geometry.push(rectangle(1.0, 1.0, 1.0, 1.0));
    assert!(validate(&job, &layout).is_err());
}

#[test]
fn fill_modes_allow_missing_parts_but_never_extra_copies() {
    let (mut job, mut layout) = fixture();
    layout.placements.pop();
    job.mode = Mode::FillArea;
    let m = validate(&job, &layout).unwrap().metrics.unwrap();
    assert_eq!(m.placed_area, 100.0);
    assert_eq!(m.requested_parts, 2);
    job.mode = Mode::FillPriority;
    job.parts[0].priority = 7.0;
    assert_eq!(
        validate(&job, &layout)
            .unwrap()
            .metrics
            .unwrap()
            .placed_priority,
        7.0
    );
    layout.placements[0].copy_index = 2;
    assert!(has(&validate(&job, &layout).unwrap(), "copy"));
    layout.placements.clear();
    layout.sheets.clear();
    let m = validate(&job, &layout).unwrap().metrics.unwrap();
    assert_eq!(m.placed_area, 0.0);
    assert_eq!(m.material_area, 0.0);
}

#[test]
fn unit_mismatch_invalid_inputs_and_excessive_demand_are_rejected() {
    let (mut job, mut layout) = fixture();
    layout.units = Units::Inch;
    assert!(has(&validate(&job, &layout).unwrap(), "units"));
    layout.units = Units::Mm;
    job.parts[0].quantity = 2001;
    assert!(validate(&job, &layout).is_err());
    job.parts[0].quantity = 2;
    job.parts[0].rotations = Rotations::Step { degrees: 0.0 };
    assert!(validate(&job, &layout).is_err());
}

#[test]
fn remnant_outline_and_overlapping_defects_are_supported() {
    let (mut job, mut layout) = fixture();
    job.stocks[0].outline = vec![Polygon {
        outer: vec![
            [0.0, 0.0],
            [100.0, 0.0],
            [100.0, 40.0],
            [40.0, 40.0],
            [40.0, 100.0],
            [0.0, 100.0],
        ],
        holes: vec![],
    }];
    job.stocks[0].defects = vec![
        rectangle(50.0, 10.0, 10.0, 10.0),
        rectangle(55.0, 15.0, 10.0, 10.0),
    ];
    assert!(validate(&job, &layout).unwrap().valid);
    layout.placements[1].transform.translation = [70.0, 70.0];
    assert!(has(&validate(&job, &layout).unwrap(), "containment"));
}

#[test]
fn tiny_pair_overlaps_are_accumulated_per_part() {
    let (mut job, mut layout) = fixture();
    job.parts = vec![part("center", 10.0, 10.0, 1), part("edge", 10.0, 10.0, 2)];
    layout.placements = vec![
        placement("center", 0, "one", 20.0, 20.0),
        placement("edge", 0, "one", 10.000006, 20.0),
        placement("edge", 1, "one", 29.999994, 20.0),
    ];
    let report = validate(&job, &layout).unwrap();
    assert!(report.maximum_overlap_ratio < 1e-6);
    assert!(has(&report, "total_overlap"));
}

#[test]
fn validates_two_thousand_distinct_copies() {
    let (mut job, mut layout) = fixture();
    job.parts[0].quantity = 2000;
    job.stocks[0].width = 500.0;
    job.stocks[0].height = 400.0;
    layout.placements = (0..2000)
        .map(|n| {
            placement(
                "a",
                n,
                "one",
                f64::from(n % 50) * 10.0,
                f64::from(n / 50) * 10.0,
            )
        })
        .collect();
    let report = validate(&job, &layout).unwrap();
    assert!(report.valid, "{:?}", report.violations);
    let metrics = report.metrics.unwrap();
    assert_eq!(metrics.placed_parts, 2000);
    assert_eq!(metrics.utilization, 1.0);
}

#[test]
fn a_completely_defective_sheet_allows_only_an_empty_fill_result() {
    let (mut job, mut layout) = fixture();
    job.stocks[0]
        .defects
        .push(rectangle(0.0, 0.0, 100.0, 100.0));
    assert!(has(&validate(&job, &layout).unwrap(), "containment"));
    job.mode = Mode::FillArea;
    layout.sheets.clear();
    layout.placements.clear();
    assert!(validate(&job, &layout).unwrap().valid);
}
