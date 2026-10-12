use nestbolt_core::control::{Control, Interrupted, StopReason};
use nestbolt_core::{construct, optimize};
use nestbolt_validator::{
    Units,
    job::{Job, Margins, Mode, Part, Rotations, Stock, rectangle, validate},
};
use std::cell::Cell;

#[test]
fn shallow_overlap_repair_keeps_the_blaz1_development_quality_gain() {
    // This is a frozen development job, never a held-out case. The original
    // blocker-count ranking needed eleven sheets at the same four-pass budget.
    let job: Job = serde_json::from_str(include_str!(
        "../../../benchmarks/datasets/B/b-blaz1-nest-mb-free.json"
    ))
    .unwrap();
    let result = optimize::optimize(
        &job,
        optimize::Options {
            construct: construct::Options {
                seed: 0,
                random_samples: 64,
                ..construct::Options::default()
            },
            passes: 4,
        },
        |_| {},
    )
    .unwrap();
    assert!(result.validation.valid);
    assert!(result.best.layout.sheets.len() <= 10);
    assert!(result.validation.metrics.unwrap().normalized_material < 9.81);
}

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
    assert_eq!(result.history[3].stage, "repair-sheet");
    assert!(!result.history[3].interleaved_copies);
    assert!(!result.history[4].interleaved_copies);
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

#[test]
fn collision_limit_stops_mid_pass_and_preserves_the_valid_incumbent_deterministically() {
    let job = job();
    let options = optimize::Options {
        construct: construct::Options::default(),
        passes: 1,
    };
    let initial = optimize::optimize(&job, options, |_| {}).unwrap();
    let limit = initial.collision_checks + 1;
    let run = || {
        optimize::optimize_controlled(
            &job,
            optimize::Options {
                passes: 8,
                ..options
            },
            &mut Control::new(Some(limit), None),
            |_| {},
        )
        .unwrap()
    };
    let stopped = run();
    assert_eq!(stopped.stopped, Some(StopReason::WorkLimit));
    assert_eq!(stopped.completed_passes, 1);
    assert_eq!(stopped.requested_passes, 8);
    assert_eq!(stopped.collision_checks, limit);
    assert!(stopped.validation.valid);
    assert_eq!(
        serde_json::to_string(&stopped.best.layout).unwrap(),
        serde_json::to_string(&initial.best.layout).unwrap()
    );
    assert_eq!(
        serde_json::to_string(&stopped).unwrap(),
        serde_json::to_string(&run()).unwrap()
    );
}

#[test]
fn cancellation_before_initial_layout_is_typed_and_after_progress_keeps_the_layout() {
    let job = job();
    let options = optimize::Options {
        construct: construct::Options::default(),
        passes: 4,
    };
    let mut already_cancelled = || Some(StopReason::Cancelled);
    let error = optimize::optimize_controlled(
        &job,
        options,
        &mut Control::new(None, Some(&mut already_cancelled)),
        |_| {},
    )
    .unwrap_err();
    assert_eq!(
        error.downcast_ref::<Interrupted>().unwrap().0,
        StopReason::Cancelled
    );
    let error =
        optimize::optimize_controlled(&job, options, &mut Control::new(Some(0), None), |_| {})
            .unwrap_err();
    assert_eq!(
        error.downcast_ref::<Interrupted>().unwrap().0,
        StopReason::WorkLimit
    );

    let cancel = Cell::new(false);
    let mut probe = || cancel.get().then_some(StopReason::Cancelled);
    let result = optimize::optimize_controlled(
        &job,
        options,
        &mut Control::new(None, Some(&mut probe)),
        |_| cancel.set(true),
    )
    .unwrap();
    assert_eq!(result.stopped, Some(StopReason::Cancelled));
    assert_eq!(result.completed_passes, 1);
    assert!(result.validation.valid && result.best.complete);
}

#[test]
fn interrupted_sheet_repair_cannot_leak_removed_or_displaced_parts() {
    let job = job();
    let options = optimize::Options {
        construct: construct::Options::default(),
        passes: 3,
    };
    let initial = optimize::optimize(&job, options, |_| {}).unwrap();
    assert!(initial.best.layout.sheets.len() > 1);
    let options = optimize::Options {
        passes: 4,
        ..options
    };
    let full = optimize::optimize(&job, options, |_| {}).unwrap();
    let repair_work = full.collision_checks - initial.collision_checks;
    assert!(repair_work > 2);
    for extra in [1, repair_work / 2, repair_work - 1] {
        let result = optimize::optimize_controlled(
            &job,
            options,
            &mut Control::new(Some(initial.collision_checks + extra), None),
            |_| {},
        )
        .unwrap();
        assert_eq!(result.stopped, Some(StopReason::WorkLimit));
        assert_eq!(result.completed_passes, 3);
        assert!(result.validation.valid);
        assert_eq!(
            serde_json::to_string(&result.best.layout).unwrap(),
            serde_json::to_string(&initial.best.layout).unwrap()
        );
    }
}
