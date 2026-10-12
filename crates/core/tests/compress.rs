use nestbolt_core::{construct::PreparedJob, control::Control};
use nestbolt_validator::{
    RigidTransform, Units,
    job::{
        Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock, rectangle, validate,
    },
};

fn fixture() -> (Job, Layout) {
    let job = Job {
        version: 1,
        name: "trailing-sheet compression".into(),
        units: Units::Mm,
        clearance: 0.1,
        edge_clearance: 0.1,
        mode: Mode::All,
        parts: vec![Part {
            id: "square".into(),
            quantity: 3,
            geometry: vec![rectangle(-1.0, -1.0, 2.0, 2.0)],
            rotations: Rotations::List { degrees: vec![0.0] },
            allow_mirror: true,
            priority: 1.0,
        }],
        stocks: vec![Stock {
            id: "stock".into(),
            width: 10.0,
            height: 10.0,
            count: Some(2),
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
    };
    let layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: ["compress", "untouched"]
            .into_iter()
            .map(|id| Sheet {
                id: id.into(),
                stock_id: "stock".into(),
            })
            .collect(),
        placements: [
            ("compress", [2.0, 2.0]),
            ("compress", [2.0, 5.0]),
            ("untouched", [2.0, 8.0]),
        ]
        .into_iter()
        .enumerate()
        .map(|(i, (sheet, translation))| Placement {
            part_id: "square".into(),
            copy_index: i as u32,
            sheet_id: sheet.into(),
            transform: RigidTransform {
                translation,
                rotation_radians: 0.0,
                mirrored: true,
            },
        })
        .collect(),
    };
    (job, layout)
}

#[test]
fn compression_separates_clamped_parts_and_preserves_other_sheets() {
    let (job, source) = fixture();
    let before = validate(&job, &source).unwrap();
    assert!(before.valid);
    let prepared = PreparedJob::new(&job).unwrap();
    let run = || {
        prepared
            .compress_last_sheet(&source, 0.2, 0, &mut Control::unlimited())
            .unwrap()
            .unwrap()
    };
    let result = run();
    let report = validate(&job, &result.layout).unwrap();
    assert!(report.valid);
    assert!(report.metrics.unwrap().material_area < before.metrics.unwrap().material_area);
    assert_eq!(
        serde_json::to_string(&source.placements[2]).unwrap(),
        serde_json::to_string(&result.layout.placements[2]).unwrap()
    );
    for (a, b) in source.placements.iter().zip(&result.layout.placements) {
        assert_eq!(a.copy_index, b.copy_index);
        assert_eq!(a.sheet_id, b.sheet_id);
        assert_eq!(a.transform.rotation_radians, b.transform.rotation_radians);
        assert_eq!(a.transform.mirrored, b.transform.mirrored);
    }
    assert_eq!(
        serde_json::to_string(&result).unwrap(),
        serde_json::to_string(&run()).unwrap()
    );
}

#[test]
fn fixed_defects_or_interruption_never_modify_the_source() {
    let (mut job, source) = fixture();
    // Clamping the high part crosses this defect; it cannot be moved as a part.
    job.stocks[0].defects.push(rectangle(1.0, 3.4, 2.0, 0.3));
    assert!(validate(&job, &source).unwrap().valid);
    let original = serde_json::to_string(&source).unwrap();
    let prepared = PreparedJob::new(&job).unwrap();
    assert!(
        prepared
            .compress_last_sheet(&source, 0.2, 0, &mut Control::unlimited())
            .unwrap()
            .is_none()
    );
    let mut control = Control::new(Some(0), None);
    let error = prepared
        .compress_last_sheet(&source, 0.2, 0, &mut control)
        .unwrap_err();
    assert!(error.is::<nestbolt_core::control::Interrupted>());
    assert_eq!(original, serde_json::to_string(&source).unwrap());
}
