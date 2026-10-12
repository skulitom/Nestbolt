#![cfg(not(target_arch = "wasm32"))]
use nestbolt_core::strip;
use nestbolt_validator::{
    Units,
    job::{Job, Margins, Mode, Part, Rotations, Stock, rectangle, validate},
};

fn fixture() -> Job {
    Job {
        version: 1,
        name: "strip fixture".into(),
        units: Units::Inch,
        clearance: 0.0,
        edge_clearance: 0.0,
        mode: Mode::All,
        parts: vec![Part {
            id: "offset-square".into(),
            quantity: 3,
            geometry: vec![rectangle(-1.0, -1.0, 2.0, 2.0)],
            rotations: Rotations::List {
                degrees: vec![0.0, 90.0],
            },
            allow_mirror: true,
            priority: 1.0,
        }],
        stocks: vec![Stock {
            id: "strip".into(),
            width: 20.0,
            height: 5.0,
            count: Some(1),
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
    }
}

#[test]
fn native_strip_search_returns_original_geometry_and_units_within_its_envelope() {
    let job = fixture();
    let mut progress = vec![];
    let result = strip::optimize(
        &job,
        strip::Options {
            seconds: 1,
            seed: 0,
        },
        |p| progress.push(p.strip_length),
    )
    .unwrap();
    assert!(result.validation.valid);
    assert!(validate(&job, &result.layout).unwrap().valid);
    assert_eq!(result.layout.units, Units::Inch);
    assert_eq!(result.layout.placements.len(), 3);
    assert_eq!(result.layout.sheets.len(), 1);
    assert!(result.strip_length > 0.0 && result.strip_length <= job.stocks[0].width);
    assert!(result.accepted_at_seconds <= 1.0);
    assert!(!progress.is_empty() && progress.windows(2).all(|p| p[1] < p[0]));
    assert_eq!(progress.last(), Some(&result.strip_length));
}

#[test]
fn strip_adapter_rejects_unrepresented_constraints_and_invalid_budgets() {
    let base = fixture();
    for seconds in [0, 301] {
        assert!(strip::optimize(&base, strip::Options { seconds, seed: 0 }, |_| {}).is_err());
    }
    for change in 0..5 {
        let mut job = base.clone();
        match change {
            0 => job.parts[0].geometry[0]
                .holes
                .push(rectangle(-0.2, -0.2, 0.4, 0.4).outer),
            1 => job.mode = Mode::FillArea,
            2 => job.stocks[0].defects.push(rectangle(0.0, 0.0, 1.0, 1.0)),
            3 => job.edge_clearance = 0.1,
            _ => job.stocks[0].count = Some(0),
        }
        assert!(
            strip::optimize(
                &job,
                strip::Options {
                    seconds: 1,
                    seed: 0
                },
                |_| {}
            )
            .is_err()
        );
    }
}
