use super::*;
use nestbolt_validator::{
    Units,
    job::{Margins, Mode, Part, Rotations, Stock, rectangle, validate},
};

fn job(mode: Mode) -> Job {
    Job {
        version: 1,
        name: "material scores".into(),
        units: Units::Mm,
        parts: vec![
            Part {
                id: "more-waste".into(),
                quantity: 1,
                geometry: vec![rectangle(0.0, 0.0, 5.0, 10.0)],
                rotations: Rotations::List { degrees: vec![0.0] },
                allow_mirror: false,
                priority: 1.0,
            },
            Part {
                id: "more-material".into(),
                quantity: 1,
                geometry: vec![rectangle(0.0, 0.0, 9.0, 8.0)],
                rotations: Rotations::List { degrees: vec![0.0] },
                allow_mirror: false,
                priority: 1.0,
            },
        ],
        stocks: vec![Stock {
            id: "stock".into(),
            width: 11.0,
            height: 11.0,
            count: Some(1),
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
        clearance: 0.1,
        edge_clearance: 0.1,
        mode,
    }
}

fn options() -> crate::sheets::Options {
    crate::sheets::Options {
        seconds: 0.1,
        time_limit: Some(30.0),
        timing: crate::clock::Timing::Work,
        ..Default::default()
    }
}

#[test]
fn fill_modes_value_parts_not_reserved_waste_and_keep_priority_primary() {
    for (mode, priority, expected, area) in [
        (Mode::FillArea, 1.0, "more-material", 72.0),
        (Mode::FillPriority, 1.0, "more-material", 72.0),
        (Mode::FillPriority, 2.0, "more-waste", 50.0),
    ] {
        let mut material = job(mode);
        material.parts[0].priority = priority;
        let mut collision = material.clone();
        collision.parts[0].geometry = vec![rectangle(0.0, 0.0, 10.0, 10.0)];
        let result = crate::sheets::optimize_with_material(
            &collision,
            &material,
            options(),
            false,
            |_, _| {},
        )
        .unwrap();
        assert!(result.validation.valid);
        assert_eq!(result.layout.placements.len(), 1);
        assert_eq!(result.layout.placements[0].part_id, expected);
        let metrics = result.validation.metrics.as_ref().unwrap();
        assert!((metrics.placed_area - area).abs() < 1e-9);
        assert!((metrics.placed_priority - priority).abs() < 1e-9);
        assert!((metrics.utilization - area / metrics.material_area).abs() < 1e-12);
        assert_eq!(result.warm_start.placed_area, metrics.placed_area);
        assert!(validate(&material, &result.layout).unwrap().valid);
        assert!(validate(&collision, &result.layout).unwrap().valid);
    }
}

#[test]
fn reserved_cutting_space_stays_out_of_the_reported_offcut() {
    let mut material = job(Mode::All);
    material.parts.truncate(1);
    material.parts[0].geometry = vec![rectangle(0.0, 0.0, 10.0, 10.0)];
    material.stocks[0].width = 20.0;
    material.stocks[0].height = 30.0;
    let mut collision = material.clone();
    collision.parts[0].geometry = vec![rectangle(0.0, 0.0, 10.0, 13.0)];
    let result =
        crate::sheets::optimize_with_material(&collision, &material, options(), false, |_, _| {})
            .unwrap();
    let source = validate(&material, &result.layout)
        .unwrap()
        .metrics
        .unwrap();
    let reserved = validate(&collision, &result.layout)
        .unwrap()
        .metrics
        .unwrap();
    let report = result.validation.metrics.unwrap();
    assert_eq!(report.placed_area, 100.0);
    assert_eq!(report.material_area, reserved.material_area);
    assert_eq!(report.trailing_offcut_area, reserved.trailing_offcut_area);
    assert_eq!(
        report.last_sheet_used_height,
        reserved.last_sheet_used_height
    );
    assert!(report.last_sheet_used_height > source.last_sheet_used_height + 2.99);
    assert_eq!(result.warm_start.placed_area, 100.0);
}

#[test]
fn source_material_must_match_metadata_and_fit_the_reserved_geometry() {
    let source = job(Mode::All);
    let mut changed = source.clone();
    changed.parts[0].priority = 2.0;
    assert!(MaterialAreas::new(&source, &changed).is_err());
    changed = source.clone();
    changed.parts[0].geometry = vec![rectangle(0.0, 0.0, 4.9, 10.0)];
    assert!(MaterialAreas::new(&source, &changed).is_err());
    changed = source.clone();
    changed.parts[0].geometry[0]
        .holes
        .push(rectangle(1.0, 1.0, 1.0, 1.0).outer);
    assert!(MaterialAreas::new(&source, &changed).is_err());
    assert!(MaterialAreas::new(&source, &source).is_ok());
}
