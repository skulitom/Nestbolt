use nestbolt_core::{construct, optimize};
use nestbolt_validator::{
    Units,
    job::{Job, Margins, Mode, Part, Rotations, Stock, rectangle, validate},
};

fn job() -> Job {
    Job {
        version: 1,
        name: "repack".into(),
        units: Units::Mm,
        clearance: 0.2,
        edge_clearance: 0.3,
        mode: Mode::All,
        parts: [(8.0, 4.0), (6.0, 6.0), (3.0, 7.0), (4.0, 4.0), (2.0, 5.0)]
            .into_iter()
            .enumerate()
            .map(|(i, (w, h))| Part {
                id: format!("p{i}"),
                quantity: 2,
                geometry: vec![rectangle(0.0, 0.0, w, h)],
                rotations: Rotations::List {
                    degrees: vec![0.0, 90.0],
                },
                allow_mirror: false,
                priority: (i + 1) as f64,
            })
            .collect(),
        stocks: vec![Stock {
            id: "sheet".into(),
            width: 16.0,
            height: 12.0,
            count: None,
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
    }
}

#[test]
fn repacking_preserves_a_valid_incumbent_and_accounts_for_every_pass() {
    let job = job();
    let options = optimize::Options {
        construct: construct::Options::default(),
        passes: 5,
    };
    let mut callbacks = vec![];
    let result = optimize::optimize(&job, options, |p| callbacks.push(p.pass)).unwrap();
    assert!(validate(&job, &result.best.layout).unwrap().valid);
    assert_eq!(callbacks, vec![0, 1, 2, 3, 4]);
    assert_eq!(result.completed_passes, 5);
    assert_eq!(
        result.history[3].sheet_limit,
        Some(
            result.history[..3]
                .iter()
                .rfind(|p| p.accepted)
                .unwrap()
                .sheets
                - 1
        )
    );
    assert_eq!(result.history[1].stage, "refine");
    assert_eq!(result.history[1].seed, result.history[0].seed);
    assert_eq!(result.history[2].stage, "contacts");
    assert_eq!(result.history[2].seed, result.history[0].seed);
    assert!(!result.history[1].contact_search);
    assert!(result.history[2].contact_search);
    assert!(result.best.layout.sheets.len() <= result.history[0].sheets);
    for pass in &result.history {
        if !pass.complete {
            assert!(!pass.accepted);
            assert!(pass.material.is_none());
        }
    }
    let repeat = optimize::optimize(&job, options, |_| {}).unwrap();
    assert_eq!(
        serde_json::to_string(&result).unwrap(),
        serde_json::to_string(&repeat).unwrap()
    );
}

#[test]
fn fill_priority_search_never_reduces_the_incumbents_priority() {
    let mut job = job();
    job.mode = Mode::FillPriority;
    job.stocks[0].count = Some(1);
    let result = optimize::optimize(
        &job,
        optimize::Options {
            construct: construct::Options::default(),
            passes: 4,
        },
        |_| {},
    )
    .unwrap();
    assert!(result.validation.valid);
    let scores: Vec<_> = result
        .history
        .iter()
        .filter(|p| p.accepted)
        .map(|p| p.placed_priority.unwrap())
        .collect();
    assert!(scores.windows(2).all(|p| p[0] <= p[1]));
    assert_eq!(result.best.layout.sheets.len(), 1);
}

#[test]
fn impossible_stock_is_not_reported_as_a_successful_improvement() {
    let mut job = job();
    job.stocks[0].width = 1.0;
    job.stocks[0].height = 1.0;
    job.stocks[0].count = Some(1);
    let result = optimize::optimize(
        &job,
        optimize::Options {
            construct: construct::Options::default(),
            passes: 3,
        },
        |_| {},
    )
    .unwrap();
    assert!(!result.validation.valid);
    assert!(!result.best.complete);
    assert!(
        result
            .history
            .iter()
            .all(|p| !p.accepted && p.material.is_none())
    );
}
