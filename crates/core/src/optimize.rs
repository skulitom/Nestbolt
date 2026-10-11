//! Deterministic repacking search over the shared prepared geometry. This is the
//! first improvement stage; fixed passes are explicit experimental work budgets.
use anyhow::{Result, ensure};
use nestbolt_validator::job::{Job, Metrics, Mode, Report, validate};
use serde::Serialize;

use crate::construct::{Construction, Options as ConstructOptions, PreparedJob, Refinement};

#[derive(Clone, Copy, Debug)]
pub struct Options {
    pub construct: ConstructOptions,
    /// Includes the initial construction. Every requested pass is accounted for.
    pub passes: u32,
}

#[derive(Debug, Serialize)]
pub struct Progress {
    pub pass: u32,
    pub stage: &'static str,
    pub contact_search: bool,
    pub interleaved_copies: bool,
    pub seed: u64,
    pub sheet_limit: Option<usize>,
    pub complete: bool,
    pub accepted: bool,
    pub sheets: usize,
    pub material: Option<f64>,
    pub placed_area: Option<f64>,
    pub placed_priority: Option<f64>,
    pub collision_checks: u64,
}

#[derive(Debug, Serialize)]
pub struct SearchResult {
    pub algorithm: &'static str,
    pub seed: u64,
    pub requested_passes: u32,
    pub completed_passes: u32,
    pub best: Construction,
    pub validation: Report,
    pub history: Vec<Progress>,
}

fn seed(base: u64, pass: u32) -> u64 {
    base.wrapping_add(u64::from(pass).wrapping_mul(0x9e3779b97f4a7c15))
}

fn shuffled_order(count: usize, mut state: u64) -> Vec<usize> {
    let mut order: Vec<_> = (0..count).collect();
    for i in (1..count).rev() {
        state = state.wrapping_add(0x9e3779b97f4a7c15);
        let mut bits = state;
        bits = (bits ^ (bits >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        bits = (bits ^ (bits >> 27)).wrapping_mul(0x94d049bb133111eb);
        bits ^= bits >> 31;
        order.swap(i, (bits % (i as u64 + 1)) as usize);
    }
    order
}

fn better(candidate: &Metrics, incumbent: &Metrics, mode: Mode) -> bool {
    match mode {
        Mode::All => {
            candidate.sheets_used < incumbent.sheets_used
                || (candidate.sheets_used == incumbent.sheets_used
                    && candidate.material_area < incumbent.material_area)
        }
        Mode::FillArea => {
            candidate.placed_area > incumbent.placed_area
                || (candidate.placed_area == incumbent.placed_area
                    && candidate.material_area < incumbent.material_area)
        }
        Mode::FillPriority => {
            candidate.placed_priority > incumbent.placed_priority
                || (candidate.placed_priority == incumbent.placed_priority
                    && (candidate.placed_area > incumbent.placed_area
                        || (candidate.placed_area == incumbent.placed_area
                            && candidate.material_area < incumbent.material_area)))
        }
    }
}

/// Run every declared pass and retain the independently valid incumbent. Failed
/// attempts remain in history; a sheet-removal attempt never relaxes stock caps.
/// This API has no time-budget promise yet. Native benchmark process deadlines
/// must surround it until calibrated/cancellable work budgets are implemented.
pub fn optimize(
    job: &Job,
    options: Options,
    mut progress: impl FnMut(&Progress),
) -> Result<SearchResult> {
    ensure!(
        (1..=64).contains(&options.passes),
        "search needs 1..=64 passes"
    );
    let prepared = PreparedJob::new(job)?;
    let mut best = prepared.construct(options.construct)?;
    let mut validation = validate(job, &best.layout)?;
    let mut history = vec![];
    for pass in 0..options.passes {
        // Compare refinement to the initial constructor before changing its
        // ordering or random stream. Later passes explore new orders and caps.
        let trial_seed = seed(options.construct.seed, if pass <= 2 { 0 } else { pass });
        let sheet_limit = if pass >= 3
            && pass % 3 == 0
            && job.mode == Mode::All
            && validation.valid
            && best.layout.sheets.len() > 1
        {
            Some(best.layout.sheets.len() - 1)
        } else {
            None
        };
        let refinement = if pass == 0 {
            Refinement::None
        } else if pass % 2 == 0 {
            Refinement::Contacts
        } else {
            Refinement::Translation
        };
        let interleaved_copies = pass >= 3 && pass % 4 >= 2;
        let mut candidate = if pass == 0 {
            None
        } else {
            let grouped: Vec<_> = shuffled_order(job.parts.len(), trial_seed)
                .into_iter()
                .flat_map(|index| (0..job.parts[index].quantity).map(move |copy| (index, copy)))
                .collect();
            let order = if interleaved_copies {
                shuffled_order(grouped.len(), trial_seed ^ 0xd1b54a32d192ed03)
                    .into_iter()
                    .map(|index| grouped[index])
                    .collect()
            } else {
                grouped
            };
            Some(prepared.construct_ordered(
                ConstructOptions {
                    seed: trial_seed,
                    ..options.construct
                },
                if pass <= 2 { None } else { Some(&order) },
                sheet_limit,
                refinement,
            )?)
        };
        let checked = if let Some(ref c) = candidate {
            Some(validate(job, &c.layout)?)
        } else {
            None
        };
        let report = checked.as_ref().unwrap_or(&validation);
        let current = candidate.as_ref().unwrap_or(&best);
        let accepted = report.valid
            && (pass == 0
                || !validation.valid
                || better(
                    report.metrics.as_ref().expect("valid metrics"),
                    validation
                        .metrics
                        .as_ref()
                        .expect("valid incumbent metrics"),
                    job.mode,
                ));
        let metrics = report.metrics.as_ref();
        let entry = Progress {
            pass,
            stage: if pass == 0 {
                "construct"
            } else if pass == 1 {
                "refine"
            } else if pass == 2 {
                "contacts"
            } else if sheet_limit.is_some() {
                "remove-sheet"
            } else {
                "repack"
            },
            contact_search: refinement == Refinement::Contacts,
            interleaved_copies,
            seed: trial_seed,
            sheet_limit,
            complete: current.complete,
            accepted,
            sheets: current.layout.sheets.len(),
            material: metrics.map(|m| m.normalized_material),
            placed_area: metrics.map(|m| m.placed_area),
            placed_priority: metrics.map(|m| m.placed_priority),
            collision_checks: current.collision_checks,
        };
        if pass > 0 && accepted {
            best = candidate.take().expect("later pass has candidate");
            validation = checked.expect("candidate checked");
        }
        progress(&entry);
        history.push(entry);
    }
    Ok(SearchResult {
        algorithm: "nestbolt-repack-v5",
        seed: options.construct.seed,
        requested_passes: options.passes,
        completed_passes: options.passes,
        best,
        validation,
        history,
    })
}
