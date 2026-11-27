use nestbolt_core::construct::{Options, PreparedJob, Unfit, construct};
use nestbolt_core::control::Control;
use nestbolt_core::optimize;
use nestbolt_validator::{
    Polygon, Units,
    job::{Job, Margins, Mode, Part, Rotations, Stock, rectangle, validate},
};

fn part(id: &str, geometry: Vec<Polygon>, quantity: u32) -> Part {
    Part {
        id: id.into(),
        geometry,
        quantity,
        rotations: Rotations::List { degrees: vec![0.0] },
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
fn job(parts: Vec<Part>, stocks: Vec<Stock>) -> Job {
    Job {
        version: 1,
        name: "construction test".into(),
        units: Units::Mm,
        parts,
        stocks,
        clearance: 0.4,
        edge_clearance: 0.7,
        mode: Mode::All,
    }
}

#[test]
fn holed_and_disconnected_parts_preserve_source_and_repeat() {
    let mut ring = rectangle(-2.0, -3.0, 8.0, 9.0);
    ring.holes.push(rectangle(0.0, 0.0, 2.0, 2.0).outer);
    let source = job(
        vec![
            part("ring", vec![ring], 3),
            part(
                "letters",
                vec![
                    rectangle(-3.0, 0.0, 2.0, 3.0),
                    rectangle(1.0, 0.0, 2.0, 3.0),
                ],
                4,
            ),
        ],
        vec![stock("sheet", 24.0, 16.0, None)],
    );
    let before = serde_json::to_string(&source).unwrap();
    let first = construct(&source, Options::default()).unwrap();
    assert!(first.complete);
    assert!(first.layout.sheets.len() > 1);
    assert!(validate(&source, &first.layout).unwrap().valid);
    assert_eq!(before, serde_json::to_string(&source).unwrap());
    let second = construct(&source, Options::default()).unwrap();
    assert_eq!(
        serde_json::to_string(&first).unwrap(),
        serde_json::to_string(&second).unwrap()
    );
}

#[test]
fn mixed_stock_limits_and_fill_do_not_invent_sheets() {
    let mut source = job(
        vec![
            part("large", vec![rectangle(0.0, 0.0, 12.0, 9.0)], 2),
            part("small", vec![rectangle(0.0, 0.0, 3.0, 3.0)], 1),
        ],
        vec![
            stock("small", 8.0, 8.0, Some(1)),
            stock("large", 15.0, 12.0, Some(1)),
        ],
    );
    let result = construct(&source, Options::default()).unwrap();
    assert!(!result.complete);
    assert_eq!(result.unplaced, 1);
    assert_eq!(result.layout.sheets.len(), 2);
    source.mode = Mode::FillArea;
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert_eq!(result.unplaced, 1);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn exact_list_angles_and_mirror_are_rebuilt_in_source_coordinates() {
    let mut source = job(
        vec![part(
            "triangle",
            vec![Polygon {
                outer: vec![[5.0, -3.0], [12.0, -3.0], [5.0, 8.0]],
                holes: vec![],
            }],
            2,
        )],
        vec![stock("sheet", 32.0, 18.0, None)],
    );
    source.parts[0].rotations = Rotations::List {
        degrees: vec![37.0],
    };
    source.parts[0].allow_mirror = true;
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert!(validate(&source, &result.layout).unwrap().valid);
    assert!(
        result
            .layout
            .placements
            .iter()
            .all(|p| p.transform.rotation_radians == 37.0_f64.to_radians())
    );
}

#[test]
fn split_remnant_regions_share_one_stock_copy_and_avoid_defects() {
    let mut sheet = stock("remnant", 40.0, 16.0, Some(1));
    sheet.outline = vec![
        rectangle(0.0, 0.0, 16.0, 16.0),
        rectangle(24.0, 0.0, 16.0, 16.0),
    ];
    sheet.defects.push(rectangle(2.0, 2.0, 3.0, 3.0));
    sheet.margins.left = 1.0;
    let source = job(
        vec![part("block", vec![rectangle(0.0, 0.0, 7.0, 7.0)], 2)],
        vec![sheet],
    );
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert_eq!(result.layout.sheets.len(), 1);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn a_mirror_required_by_the_remnant_is_exported_as_one_rigid_transform() {
    let triangle = Polygon {
        outer: vec![[0.0, 0.0], [8.0, 0.0], [0.0, 8.0]],
        holes: vec![],
    };
    let mut sheet = stock("triangle-remnant", 10.0, 10.0, Some(1));
    sheet.outline = vec![Polygon {
        outer: vec![[0.0, 0.0], [10.0, 0.0], [10.0, 10.0]],
        holes: vec![],
    }];
    let mut source = job(vec![part("triangle", vec![triangle], 1)], vec![sheet]);
    source.clearance = 0.1;
    source.edge_clearance = 0.1;
    let unmirrored = construct(&source, Options::default()).unwrap();
    assert!(!unmirrored.complete);
    source.parts[0].allow_mirror = true;
    let result = construct(&source, Options::default()).unwrap();
    assert!(result.complete);
    assert!(result.layout.placements[0].transform.mirrored);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn narrow_margins_on_large_stock_preserve_clearance_and_source() {
    for (width, height) in [(8_000.0, 9_000.0), (9_000.0, 8_000.0)] {
        let mut sheet = stock("large", width, height, Some(1));
        sheet.margins = Margins {
            left: 5.0,
            right: 3.0,
            bottom: 4.0,
            top: 2.0,
        };
        let source = job(
            vec![part(
                "panel",
                vec![rectangle(-50.0, 10.0, 3_000.0, 3_000.0)],
                4,
            )],
            vec![sheet],
        );
        let original = serde_json::to_string(&source).unwrap();
        let result = construct(
            &source,
            Options {
                random_samples: 0,
                ..Options::default()
            },
        )
        .unwrap();
        assert!(result.complete);
        assert_eq!(result.layout.sheets.len(), 1);
        assert!(validate(&source, &result.layout).unwrap().valid);
        assert_eq!(serde_json::to_string(&source).unwrap(), original);
    }
}

#[test]
fn a_long_rectangular_sheet_uses_its_usable_edges_without_random_sampling() {
    let mut sheet = stock("long", 400.0, 20.0, Some(1));
    sheet.margins = Margins {
        left: 5.0,
        right: 5.0,
        bottom: 2.0,
        top: 2.0,
    };
    let source = job(
        vec![part("bar", vec![rectangle(0.0, 0.0, 180.0, 12.0)], 2)],
        vec![sheet],
    );
    let result = construct(
        &source,
        Options {
            random_samples: 0,
            ..Options::default()
        },
    )
    .unwrap();
    assert!(result.complete);
    assert_eq!(result.layout.sheets.len(), 1);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn refinement_keeps_a_mirrored_remnant_valid_without_changing_permissions() {
    let mut sheet = stock("triangle-remnant", 10.0, 10.0, Some(1));
    sheet.outline = vec![Polygon {
        outer: vec![[0.0, 0.0], [10.0, 0.0], [10.0, 10.0]],
        holes: vec![],
    }];
    let mut source = job(
        vec![part(
            "offset-triangle",
            vec![Polygon {
                outer: vec![[4.0, -2.0], [12.0, -2.0], [4.0, 6.0]],
                holes: vec![],
            }],
            1,
        )],
        vec![sheet],
    );
    source.clearance = 0.1;
    source.edge_clearance = 0.1;
    source.parts[0].allow_mirror = true;
    let prepared = PreparedJob::new(&source).unwrap();
    let initial = prepared.construct(Options::default()).unwrap();
    let refined = prepared.construct_refined(Options::default()).unwrap();
    let a = validate(&source, &initial.layout).unwrap();
    let b = validate(&source, &refined.layout).unwrap();
    assert!(a.valid && b.valid);
    assert!(refined.layout.placements[0].transform.mirrored);
    assert_eq!(refined.layout.placements[0].transform.rotation_radians, 0.0);
    assert!(b.metrics.unwrap().material_area <= a.metrics.unwrap().material_area);
    let repeated = prepared.construct_refined(Options::default()).unwrap();
    assert_eq!(
        serde_json::to_string(&refined).unwrap(),
        serde_json::to_string(&repeated).unwrap()
    );
}

#[test]
fn refinement_closes_a_gap_above_a_sloping_remnant_edge() {
    let mut sheet = stock("sloped-remnant", 10.0, 10.0, Some(1));
    sheet.outline = vec![Polygon {
        outer: vec![[0.0, 4.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0]],
        holes: vec![],
    }];
    let source = job(
        vec![part("square", vec![rectangle(0.0, 0.0, 4.0, 4.0)], 1)],
        vec![sheet],
    );
    let prepared = PreparedJob::new(&source).unwrap();
    let initial = prepared.construct(Options::default()).unwrap();
    let refined = prepared.construct_refined(Options::default()).unwrap();
    let a = validate(&source, &initial.layout).unwrap();
    let b = validate(&source, &refined.layout).unwrap();
    assert!(a.valid && b.valid);
    assert!(
        b.metrics.as_ref().unwrap().material_area < a.metrics.as_ref().unwrap().material_area - 0.1,
        "initial={:?}, refined={:?}; initial placement={:?}, refined placement={:?}",
        a.metrics,
        b.metrics,
        initial.layout.placements,
        refined.layout.placements
    );
}

#[test]
fn refinement_keeps_holes_components_defects_and_exact_angles_in_source_space() {
    let mut ring = rectangle(-2.0, -3.0, 8.0, 9.0);
    ring.holes.push(rectangle(0.0, 0.0, 2.0, 2.0).outer);
    let mut source = job(
        vec![
            part("ring", vec![ring], 4),
            part(
                "pair",
                vec![
                    rectangle(-3.0, 0.0, 2.0, 3.0),
                    rectangle(1.0, 0.0, 2.0, 3.0),
                ],
                5,
            ),
        ],
        vec![stock("sheet", 24.0, 26.0, None)],
    );
    source.stocks[0].defects.push(rectangle(5.0, 5.0, 3.0, 3.0));
    for part in &mut source.parts {
        part.rotations = Rotations::List {
            degrees: vec![37.0],
        };
        part.allow_mirror = true;
    }
    let original = serde_json::to_string(&source).unwrap();
    let result = PreparedJob::new(&source)
        .unwrap()
        .construct_refined(Options::default())
        .unwrap();
    assert!(result.complete);
    assert!(validate(&source, &result.layout).unwrap().valid);
    assert!(
        result
            .layout
            .placements
            .iter()
            .all(|p| p.transform.rotation_radians == 37.0_f64.to_radians())
    );
    assert_eq!(serde_json::to_string(&source).unwrap(), original);
}

#[test]
fn contact_candidates_interlock_concave_parts_without_random_sampling() {
    let mut source = job(
        vec![
            part(
                "open-frame",
                vec![Polygon {
                    outer: vec![
                        [0.0, 0.0],
                        [5.0, 0.0],
                        [5.0, 1.0],
                        [1.0, 1.0],
                        [1.0, 4.0],
                        [5.0, 4.0],
                        [5.0, 5.0],
                        [0.0, 5.0],
                    ],
                    holes: vec![],
                }],
                1,
            ),
            part("insert", vec![rectangle(0.0, 0.0, 3.0, 2.0)], 1),
        ],
        vec![stock("sheet", 6.0, 6.0, None)],
    );
    source.clearance = 0.1;
    source.edge_clearance = 0.1;
    let options = Options {
        random_samples: 0,
        ..Options::default()
    };
    let prepared = PreparedJob::new(&source).unwrap();
    let initial = prepared.construct(options).unwrap();
    let interlocked = prepared.construct_with_contacts(options).unwrap();
    assert_eq!(initial.layout.sheets.len(), 2);
    assert_eq!(interlocked.layout.sheets.len(), 1);
    assert!(validate(&source, &interlocked.layout).unwrap().valid);
    assert_eq!(
        serde_json::to_string(&interlocked).unwrap(),
        serde_json::to_string(&prepared.construct_with_contacts(options).unwrap()).unwrap()
    );
}

/// A 1020 x 10 strip with free rotation on a 1000 x 300 sheet without margins,
/// 1 mm part spacing and no edge spacing. Keeping that spacing from the edges
/// too, the constructor fits it only 12.5 to 16.4 degrees off a quarter turn.
fn strip_job(length: f64) -> Job {
    let mut strip = part("strip", vec![rectangle(0.0, 0.0, length, 10.0)], 1);
    strip.rotations = Rotations::Free;
    let mut source = job(vec![strip], vec![stock("sheet", 1000.0, 300.0, None)]);
    source.clearance = 1.0;
    source.edge_clearance = 0.0;
    source
}

#[test]
fn disabled_stock_does_not_suppress_free_rotation_on_available_stock() {
    let mut source = strip_job(1020.0);
    source
        .stocks
        .push(stock("unavailable", 1100.0, 100.0, Some(0)));
    let prepared = PreparedJob::new(&source).unwrap();
    let result = prepared.construct(Options::default()).unwrap();
    assert!(result.complete);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn unused_part_needs_no_construction_angles() {
    let mut source = strip_job(200.0);
    let mut unused = part("unused", vec![rectangle(0.0, 0.0, 10.0, 10.0)], 0);
    unused.rotations = Rotations::Step { degrees: 0.001 };
    source.parts.push(unused);
    let prepared = PreparedJob::new(&source).unwrap();
    prepared.ensure_parts_fit(Options::default()).unwrap();
    let result = prepared.construct(Options::default()).unwrap();
    assert!(result.complete);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn fit_preflight_rejects_invalid_rotation_budgets() {
    let source = strip_job(200.0);
    let prepared = PreparedJob::new(&source).unwrap();
    for free_rotations in [0, 361] {
        let error = prepared
            .ensure_parts_fit(Options {
                free_rotations,
                ..Options::default()
            })
            .unwrap_err();
        assert_eq!(error.to_string(), "invalid construction work budget");
    }
}

/// Degrees from the nearest quarter turn.
fn off_quarter_turn(radians: f64) -> f64 {
    let turns = radians / std::f64::consts::FRAC_PI_2;
    (turns - turns.round()).abs() * 90.0
}

#[test]
fn a_free_part_that_fits_only_between_quarter_turns_is_placed_with_room() {
    for mirror in [false, true] {
        let mut source = strip_job(1020.0);
        source.parts[0].allow_mirror = mirror;
        let prepared = PreparedJob::new(&source).unwrap();
        prepared.ensure_parts_fit(Options::default()).unwrap();
        let result = prepared.construct(Options::default()).unwrap();
        assert!(result.complete, "mirror {mirror}");
        assert!(validate(&source, &result.layout).unwrap().valid);
        // The middle of the fitting range, not one of its ends.
        let off = off_quarter_turn(result.layout.placements[0].transform.rotation_radians);
        assert!(
            (14.0..=15.0).contains(&off),
            "{off} degrees, mirror {mirror}"
        );
        // Refinement, contact candidates and repacking keep it placed.
        let search = optimize::optimize(
            &source,
            optimize::Options {
                construct: Options::default(),
                passes: 8,
            },
            |_| {},
        )
        .unwrap();
        assert!(search.best.complete && search.validation.valid);
    }
}

#[test]
fn a_part_that_fits_no_sheet_at_its_allowed_rotations_is_named() {
    for (length, rotations) in [
        // Longer than the sheet's 1044 mm diagonal.
        (1100.0, Rotations::Free),
        (
            1020.0,
            Rotations::List {
                degrees: vec![0.0, 90.0],
            },
        ),
        (1020.0, Rotations::Step { degrees: 30.0 }),
    ] {
        let mut source = strip_job(length);
        source.parts[0].rotations = rotations.clone();
        source.parts[0].allow_mirror = true;
        source
            .parts
            .insert(0, part("tab", vec![rectangle(0.0, 0.0, 20.0, 10.0)], 2));
        let prepared = PreparedJob::new(&source).unwrap();
        let error = prepared
            .ensure_parts_fit(Options::default())
            .expect_err(&format!("{rotations:?}"));
        assert_eq!(error.downcast_ref::<Unfit>().unwrap().part, "strip");
        let message = error.to_string();
        assert!(
            message.starts_with("part strip does not fit any sheet at its allowed rotations"),
            "{message}"
        );
        assert!(message.contains("more time will not help"), "{message}");
        // The constructor itself still returns the other parts.
        let result = prepared.construct(Options::default()).unwrap();
        assert!(!result.complete);
        assert_eq!(result.unplaced, 1);
    }
    // A 15-degree step reaches the fitting range.
    let mut source = strip_job(1020.0);
    source.parts[0].rotations = Rotations::Step { degrees: 15.0 };
    let prepared = PreparedJob::new(&source).unwrap();
    prepared.ensure_parts_fit(Options::default()).unwrap();
    let result = prepared.construct(Options::default()).unwrap();
    assert!(result.complete);
    assert!(validate(&source, &result.layout).unwrap().valid);
}

#[test]
fn free_parts_that_fit_at_a_grid_angle_search_exactly_the_grid() {
    // Free rotation and an explicit list of the grid's quarter turns must give
    // the same search, step for step, when every part fits at a quarter turn:
    // construction, refinement, contacts, sheet repair and compaction.
    let free: Job = serde_json::from_str(include_str!(
        "../../../benchmarks/datasets/B/b-fu-nest-mb-free.json"
    ))
    .unwrap();
    let mut grid = free.clone();
    for part in &mut grid.parts {
        assert!(matches!(part.rotations, Rotations::Free));
        part.rotations = Rotations::List {
            degrees: vec![0.0, 90.0, 180.0, 270.0],
        };
    }
    let run = |job: &Job| {
        let search = optimize::optimize(
            job,
            optimize::Options {
                construct: Options::default(),
                passes: 7,
            },
            |_| {},
        )
        .unwrap();
        assert!(search.validation.valid);
        assert!(search.history.iter().any(|p| p.stage == "repair-sheet"));
        let compacted = PreparedJob::new(job)
            .unwrap()
            .compact_with_relocation(
                &search.best.layout,
                2,
                Options::default(),
                &mut Control::unlimited(),
            )
            .unwrap();
        serde_json::to_string(&(search, compacted)).unwrap()
    };
    assert_eq!(run(&free), run(&grid));
}

/// Room the constructor needs around this strip beyond what it needed on
/// jagua-rs 1.1.0: twice the growth of the engine separation (0.0039 to
/// 0.0456 mm for a 1020 mm part without spacing), which keeps the collision
/// outlines' margin through jagua-rs 2.0's short-edge removal.
const ENGINE_ROOM: f64 = 0.083341;

/// The issue's strip without spacing, on a sheet `slack` larger each way than
/// the strip's bounding box at 3600/251 degrees (about 14.34).
fn narrow_strip_job(slack: f64) -> Job {
    let angle = (3600.0_f64 / 251.0).to_radians();
    let (width, height) = (
        1020.0 * angle.cos() + 10.0 * angle.sin(),
        1020.0 * angle.sin() + 10.0 * angle.cos(),
    );
    let mut source = strip_job(1020.0);
    source.stocks = vec![stock("sheet", width + slack, height + slack, None)];
    source.clearance = 0.0;
    source.edge_clearance = 0.0;
    source
}

#[test]
fn a_free_part_that_fits_between_scan_steps_is_placed() {
    // The strip fits about 0.004 degrees around 14.34 degrees, between the
    // scan's 0.1-degree steps, as `--free-rotations 251` shows.
    for mirror in [false, true] {
        let mut source = narrow_strip_job(0.03 + ENGINE_ROOM);
        source.parts[0].allow_mirror = mirror;
        let grid = Options {
            free_rotations: 251,
            ..Options::default()
        };
        let prepared = PreparedJob::new(&source).unwrap();
        let on_grid = prepared.construct(grid).unwrap();
        assert!(on_grid.complete && validate(&source, &on_grid.layout).unwrap().valid);
        prepared.ensure_parts_fit(Options::default()).unwrap();
        let result = prepared.construct(Options::default()).unwrap();
        assert!(result.complete, "mirror {mirror}");
        assert!(validate(&source, &result.layout).unwrap().valid);
        let off = off_quarter_turn(result.layout.placements[0].transform.rotation_radians);
        assert!(
            (off - 3600.0 / 251.0).abs() < 0.01,
            "{off} degrees, mirror {mirror}"
        );
    }
}

#[test]
fn a_part_that_just_misses_at_every_angle_is_named() {
    // 0.05 mm too small each way at the best angle, so no angle fits.
    let source = narrow_strip_job(-0.05);
    let error = PreparedJob::new(&source)
        .unwrap()
        .ensure_parts_fit(Options::default())
        .unwrap_err();
    assert_eq!(error.downcast_ref::<Unfit>().unwrap().part, "strip");
}

#[test]
fn a_fit_closer_than_f32_can_tell_is_left_to_the_search() {
    // With 0.01 mm slack beyond the engine's room the strip overhangs the
    // constructor's sheet bounds at every angle, but by less than f32 rounding:
    // the scan cannot rule a fit out, so it does not name the part, and
    // construction leaves it out.
    let source = narrow_strip_job(0.01 + ENGINE_ROOM);
    let prepared = PreparedJob::new(&source).unwrap();
    prepared.ensure_parts_fit(Options::default()).unwrap();
    assert!(!prepared.construct(Options::default()).unwrap().complete);
}

#[test]
fn the_fit_check_keeps_the_edge_spacing_exactly() {
    // 10 mm edge spacing, larger than the 0 mm part spacing, on a 300 mm wide
    // sheet: a strip fits if at most about 280 mm long. One 4 mm shorter fits
    // and one 4 mm longer does not, at its one allowed angle and when free on a
    // sheet too narrow to turn it.
    for (length, fits) in [(276.0, true), (284.0, false)] {
        for rotations in [Rotations::List { degrees: vec![0.0] }, Rotations::Free] {
            let mut strip = part("strip", vec![rectangle(0.0, 0.0, length, 10.0)], 1);
            strip.rotations = rotations.clone();
            let mut source = job(vec![strip], vec![stock("sheet", 300.0, 31.0, None)]);
            source.clearance = 0.0;
            source.edge_clearance = 10.0;
            let prepared = PreparedJob::new(&source).unwrap();
            let check = prepared.ensure_parts_fit(Options::default());
            assert_eq!(check.is_ok(), fits, "{length} mm, {rotations:?}");
            let result = prepared.construct(Options::default()).unwrap();
            assert_eq!(result.complete, fits, "{length} mm, {rotations:?}");
            if fits {
                assert!(validate(&source, &result.layout).unwrap().valid);
            } else {
                assert_eq!(
                    check.unwrap_err().downcast_ref::<Unfit>().unwrap().part,
                    "strip"
                );
            }
        }
    }
}
