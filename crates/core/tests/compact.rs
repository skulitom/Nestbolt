use nestbolt_core::{
    construct::PreparedJob,
    control::{Control, Interrupted, StopReason},
};
use nestbolt_validator::{
    RigidTransform, Units,
    job::{
        Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle, validate,
    },
};

fn fixture() -> (Job, Layout) {
    let job = Job {
        version: 1,
        name: "compact separated stacked parts".into(),
        units: Units::Mm,
        clearance: 0.1,
        edge_clearance: 0.1,
        mode: Mode::All,
        parts: vec![Part {
            id: "part".into(),
            quantity: 2,
            geometry: vec![rectangle(0.0, 0.0, 2.0, 2.0)],
            rotations: Rotations::List { degrees: vec![0.0] },
            allow_mirror: false,
            priority: 1.0,
        }],
        stocks: vec![Stock {
            id: "stock".into(),
            width: 15.0,
            height: 15.0,
            count: Some(1),
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
    };
    let source = Layout {
        version: 1,
        units: Units::Mm,
        sheets: vec![Sheet {
            id: "physical-sheet".into(),
            stock_id: "stock".into(),
        }],
        placements: [5.0, 9.0]
            .into_iter()
            .enumerate()
            .map(|(index, y)| Placement {
                part_id: "part".into(),
                copy_index: index as u32,
                sheet_id: "physical-sheet".into(),
                transform: RigidTransform {
                    translation: [4.0, y],
                    rotation_radians: 0.0,
                    mirrored: false,
                },
            })
            .collect(),
    };
    (job, source)
}

#[test]
fn compaction_reduces_material_preserves_copies_and_repeats() {
    let (job, source) = fixture();
    let original = serde_json::to_string(&source).unwrap();
    let before = validate(&job, &source).unwrap().metrics.unwrap();
    let prepared = PreparedJob::new(&job).unwrap();
    let result = prepared.compact_layout(&source, 3).unwrap();
    let checked = validate(&job, &result.layout).unwrap();
    assert!(checked.valid);
    let after = checked.metrics.unwrap();
    assert!(after.material_area < before.material_area * 0.6);
    assert_eq!(after.placed_parts, 2);
    assert_eq!(after.sheets_used, 1);
    assert_eq!(result.layout.sheets[0].id, "physical-sheet");
    assert_eq!(
        result
            .layout
            .placements
            .iter()
            .map(|p| p.copy_index)
            .collect::<Vec<_>>(),
        vec![0, 1]
    );
    assert_eq!(
        serde_json::to_string(&result).unwrap(),
        serde_json::to_string(&prepared.compact_layout(&source, 3).unwrap()).unwrap()
    );
    assert_eq!(serde_json::to_string(&source).unwrap(), original);
}

#[test]
fn interruption_and_invalid_inputs_do_not_change_the_source() {
    let (job, source) = fixture();
    let original = serde_json::to_string(&source).unwrap();
    let prepared = PreparedJob::new(&job).unwrap();
    let all = prepared.compact_layout(&source, 2).unwrap();
    for limit in [0, 1, all.collision_checks / 2] {
        let mut control = Control::new(Some(limit), None);
        let error = prepared
            .compact_controlled(&source, 2, &mut control)
            .unwrap_err();
        assert_eq!(
            error.downcast_ref::<Interrupted>().unwrap().0,
            StopReason::WorkLimit
        );
        assert_eq!(control.collision_checks(), limit);
        assert_eq!(serde_json::to_string(&source).unwrap(), original);
    }
    for sweeps in [0, 9] {
        assert!(prepared.compact_layout(&source, sweeps).is_err());
    }
    let mut invalid = source.clone();
    invalid.placements[1].transform = invalid.placements[0].transform;
    assert!(prepared.compact_layout(&invalid, 2).is_err());
}

#[test]
fn fill_compaction_keeps_the_original_selection() {
    let (mut job, source) = fixture();
    job.mode = Mode::FillArea;
    job.parts[0].quantity = 4;
    let result = PreparedJob::new(&job)
        .unwrap()
        .compact_layout(&source, 2)
        .unwrap();
    assert!(result.complete);
    assert_eq!(result.unplaced, 2);
    let report = validate(&job, &result.layout).unwrap();
    assert!(report.valid);
    assert_eq!(report.metrics.unwrap().placed_parts, 2);
}

#[test]
fn relocation_can_choose_a_shorter_permitted_orientation_and_repeats() {
    let (mut job, mut source) = fixture();
    job.parts[0].quantity = 1;
    job.parts[0].geometry = vec![rectangle(0.0, 0.0, 4.0, 2.0)];
    job.parts[0].rotations = Rotations::List {
        degrees: vec![0.0, 90.0],
    };
    source.placements.truncate(1);
    source.placements[0].transform.translation = [6.0, 5.0];
    source.placements[0].transform.rotation_radians = 90_f64.to_radians();
    let prepared = PreparedJob::new(&job).unwrap();
    let slides = prepared.compact_layout(&source, 2).unwrap();
    let relocated = || {
        prepared
            .compact_with_relocation(
                &source,
                2,
                nestbolt_core::construct::Options::default(),
                &mut Control::unlimited(),
            )
            .unwrap()
    };
    let result = relocated();
    let checked = validate(&job, &result.layout).unwrap();
    assert!(checked.valid);
    assert!(
        checked.metrics.unwrap().material_area
            < validate(&job, &slides.layout)
                .unwrap()
                .metrics
                .unwrap()
                .material_area
                * 0.6
    );
    assert_eq!(result.layout.placements[0].transform.rotation_radians, 0.0);
    assert_eq!(
        serde_json::to_string(&result).unwrap(),
        serde_json::to_string(&relocated()).unwrap()
    );
    let mut control = Control::new(Some(result.collision_checks - 1), None);
    let error = prepared
        .compact_with_relocation(
            &source,
            2,
            nestbolt_core::construct::Options::default(),
            &mut control,
        )
        .unwrap_err();
    assert_eq!(
        error.downcast_ref::<Interrupted>().unwrap().0,
        StopReason::WorkLimit
    );
    assert_eq!(
        source.placements[0].transform.rotation_radians,
        90_f64.to_radians()
    );
}
