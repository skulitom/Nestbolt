use nestbolt_core::construct::{Options, PreparedJob};
use nestbolt_validator::{
    RigidTransform, Units,
    job::{
        Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle, validate,
    },
};

fn fixture() -> (Job, Layout) {
    let job = Job {
        version: 1,
        name: "one-item displacement".into(),
        units: Units::Mm,
        clearance: 0.1,
        edge_clearance: 0.1,
        mode: Mode::All,
        parts: [("small", 2.0), ("large", 4.0)]
            .into_iter()
            .map(|(id, size)| Part {
                id: id.into(),
                quantity: 1,
                geometry: vec![rectangle(0.0, 0.0, size, size)],
                rotations: Rotations::List { degrees: vec![0.0] },
                allow_mirror: false,
                priority: 1.0,
            })
            .collect(),
        stocks: vec![Stock {
            id: "stock".into(),
            width: 6.4,
            height: 6.4,
            count: Some(2),
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
    };
    let layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: ["keep", "donor"]
            .into_iter()
            .map(|id| Sheet {
                id: id.into(),
                stock_id: "stock".into(),
            })
            .collect(),
        placements: [
            ("small", "keep", [2.2, 2.2]),
            ("large", "donor", [0.2, 0.2]),
        ]
        .into_iter()
        .map(|(part, sheet, translation)| Placement {
            part_id: part.into(),
            copy_index: 0,
            sheet_id: sheet.into(),
            transform: RigidTransform {
                translation,
                rotation_radians: 0.0,
                mirrored: false,
            },
        })
        .collect(),
    };
    (job, layout)
}

fn options() -> Options {
    Options {
        random_samples: 0,
        ..Options::default()
    }
}

#[test]
fn moving_a_blocker_fits_both_parts_on_one_sheet_and_repeats() {
    let (job, source) = fixture();
    assert!(
        validate(&job, &source).unwrap().valid,
        "{:?}",
        validate(&job, &source).unwrap()
    );
    let before = serde_json::to_string(&source).unwrap();
    let prepared = PreparedJob::new(&job).unwrap();
    let blocked = prepared.repair_sheet(&source, 1, options(), 0).unwrap();
    assert!(!blocked.complete);
    assert_eq!(blocked.unplaced, 1);
    let repaired = prepared.repair_sheet(&source, 1, options(), 1).unwrap();
    assert!(repaired.complete);
    assert_eq!(repaired.layout.sheets.len(), 1);
    assert!(validate(&job, &repaired.layout).unwrap().valid);
    assert_eq!(repaired.layout.sheets[0].id, "keep");
    assert_eq!(before, serde_json::to_string(&source).unwrap());
    let again = prepared.repair_sheet(&source, 1, options(), 1).unwrap();
    assert_eq!(
        serde_json::to_string(&repaired).unwrap(),
        serde_json::to_string(&again).unwrap()
    );
}

#[test]
fn failed_ejection_restores_the_unchanged_receiver_and_never_opens_stock() {
    let (mut job, mut source) = fixture();
    job.stocks[0].width = 4.0;
    job.stocks[0].height = 4.0;
    for part in &mut job.parts {
        part.geometry = vec![rectangle(0.0, 0.0, 3.0, 3.0)];
    }
    for placed in &mut source.placements {
        placed.transform.translation = [0.3, 0.3];
    }
    let before = serde_json::to_string(&source).unwrap();
    let repaired = PreparedJob::new(&job)
        .unwrap()
        .repair_sheet(&source, 1, options(), 8)
        .unwrap();
    assert!(!repaired.complete);
    assert_eq!(repaired.unplaced, 1);
    assert_eq!(repaired.layout.sheets.len(), 1);
    assert_eq!(
        serde_json::to_string(&repaired.layout.placements[0]).unwrap(),
        serde_json::to_string(&source.placements[0]).unwrap()
    );
    let checked = validate(&job, &repaired.layout).unwrap();
    assert!(!checked.valid);
    assert!(checked.metrics.is_none());
    assert!(checked.violations.iter().all(|v| v.code == "quantity"));
    assert_eq!(before, serde_json::to_string(&source).unwrap());
}

#[test]
fn repair_keeps_mirrored_off_origin_geometry_and_split_remnant_identity() {
    let (mut job, mut source) = fixture();
    job.parts.truncate(1);
    let mut ring = rectangle(-3.0, -4.0, 2.0, 1.0);
    ring.holes.push(rectangle(-2.5, -3.8, 0.3, 0.2).outer);
    job.parts[0].geometry = vec![ring, rectangle(-0.5, -4.0, 1.0, 1.0)];
    job.parts[0].quantity = 2;
    job.parts[0].rotations = Rotations::List {
        degrees: vec![37.0],
    };
    job.parts[0].allow_mirror = true;
    job.stocks[0].width = 20.0;
    job.stocks[0].height = 20.0;
    job.stocks[0].outline = vec![
        rectangle(0.0, 0.0, 9.0, 20.0),
        rectangle(11.0, 0.0, 9.0, 20.0),
    ];
    job.stocks[0].defects = vec![rectangle(2.0, 17.0, 4.0, 2.0)];
    for (copy, placed) in source.placements.iter_mut().enumerate() {
        placed.part_id = "small".into();
        placed.copy_index = copy as u32;
        placed.transform = RigidTransform {
            translation: [3.0, 7.0],
            rotation_radians: 37_f64.to_radians(),
            mirrored: true,
        };
    }
    assert!(
        validate(&job, &source).unwrap().valid,
        "{:?}",
        validate(&job, &source).unwrap()
    );
    let repaired = PreparedJob::new(&job)
        .unwrap()
        .repair_sheet(&source, 1, options(), 0)
        .unwrap();
    assert!(repaired.complete);
    assert_eq!(repaired.layout.sheets.len(), 1);
    assert!(validate(&job, &repaired.layout).unwrap().valid);
    let preserved = repaired
        .layout
        .placements
        .iter()
        .find(|p| p.copy_index == 0)
        .unwrap();
    assert_eq!(
        serde_json::to_string(preserved).unwrap(),
        serde_json::to_string(&source.placements[0]).unwrap()
    );
}

#[test]
fn repair_rejects_invalid_sources_donors_and_excess_work() {
    let (job, mut source) = fixture();
    let prepared = PreparedJob::new(&job).unwrap();
    assert!(prepared.repair_sheet(&source, 2, options(), 1).is_err());
    assert!(prepared.repair_sheet(&source, 1, options(), 9).is_err());
    source.placements[0].transform.translation = [-20.0, 0.0];
    assert!(prepared.repair_sheet(&source, 1, options(), 1).is_err());
}
