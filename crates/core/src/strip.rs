//! Native strip-parity adapter around the unmodified, pinned Sparrow library.
//! This timing-based benchmark path is distinct from deterministic sheet search.
use anyhow::{Context, Result, ensure};
use jagua_rs::{
    Instant,
    io::import::Importer,
    probs::spp::{entities::SPSolution, io},
};
use nestbolt_validator::{
    RigidTransform,
    job::{Job, Layout, Mode, Placement, Report, Rotations, Sheet, validate},
};
use rand::{SeedableRng, rngs::Xoshiro256PlusPlus};
use serde::Serialize;
use serde_json::json;
use sparrow::{
    config::DEFAULT_SPARROW_CONFIG,
    util::{
        listener::{ReportType, SolutionListener},
        terminator::Terminator,
    },
};
use std::time::Duration;

#[derive(Clone, Copy)]
pub struct Options {
    pub seconds: u64,
    pub seed: u64,
}

#[derive(Serialize)]
pub struct Progress {
    pub elapsed_seconds: f64,
    pub strip_length: f64,
}

#[derive(Serialize)]
pub struct StripResult {
    pub algorithm: &'static str,
    pub seed: u64,
    pub seconds: u64,
    pub strip_length: f64,
    pub layout: Layout,
    pub validation: Report,
    pub rejected_candidates: u64,
    pub accepted_at_seconds: f64,
    pub elapsed_seconds: f64,
}

struct Deadline {
    global: Instant,
    phase: Instant,
}
impl Terminator for Deadline {
    fn kill(&self) -> bool {
        Instant::now() >= self.phase.min(self.global)
    }
    fn new_timeout(&mut self, duration: Duration) {
        self.phase = (Instant::now() + duration).min(self.global);
    }
    fn timeout_at(&self) -> Option<Instant> {
        Some(self.phase.min(self.global))
    }
}

fn input(job: &Job) -> Result<io::ext_repr::ExtSPInstance> {
    // Validate the whole input contract before accepting this narrower adapter.
    validate(
        job,
        &Layout {
            version: 1,
            units: job.units,
            sheets: vec![],
            placements: vec![],
        },
    )?;
    ensure!(
        job.mode == Mode::All && job.stocks.len() == 1,
        "strip parity requires all-parts mode and one rectangular stock type"
    );
    let stock = &job.stocks[0];
    let m = stock.margins;
    ensure!(
        stock.count != Some(0)
            && stock.outline.is_empty()
            && stock.defects.is_empty()
            && [
                m.left,
                m.right,
                m.bottom,
                m.top,
                job.clearance,
                job.edge_clearance
            ]
            .iter()
            .all(|v| *v == 0.0),
        "strip parity requires available rectangular stock, zero margins/clearance and no defects"
    );
    let mut items = vec![];
    for (id, part) in job.parts.iter().enumerate() {
        ensure!(
            part.geometry.len() == 1 && part.geometry[0].holes.is_empty(),
            "strip parity requires one simple outline per part"
        );
        let rotation = match &part.rotations {
            Rotations::Free => json!({"mode":"continuous"}),
            Rotations::List { degrees } => json!({"mode":"discrete","angles":degrees}),
            Rotations::Step { degrees } => {
                let count = (360.0 / degrees).ceil() as usize;
                ensure!(count <= 65536, "strip rotation step exceeds 65,536 angles");
                json!({"mode":"discrete","angles":(0..count).map(|i| i as f64 * degrees).collect::<Vec<_>>()})
            }
        };
        items.push(json!({"id":id,"demand":part.quantity,
            "shape":{"type":"simple_polygon","data":part.geometry[0].outer},
            "orientation":{"rotation":rotation,"reflection_axes":if part.allow_mirror {vec![90]} else {vec![]}},
            "min_quality":null}));
    }
    Ok(serde_json::from_value(
        json!({"name":job.name,"min_item_separation":0,
        "strip_height":stock.height,"items":items}),
    )?)
}

fn adapt(job: &Job, ext: io::ext_repr::ExtSPSolution) -> Result<Layout> {
    ensure!(ext.layout.container_id == 0, "unexpected strip container");
    ensure!(
        ext.layout.placed_items.len() <= 2000,
        "too many strip placements"
    );
    let mut layout = Layout {
        version: 1,
        units: job.units,
        sheets: vec![Sheet {
            id: "strip".into(),
            stock_id: job.stocks[0].id.clone(),
        }],
        placements: vec![],
    };
    let mut copies = vec![0; job.parts.len()];
    for p in ext.layout.placed_items {
        let index = usize::try_from(p.item_id)?;
        let part = job.parts.get(index).context("unknown strip item")?;
        let t = p.transformation;
        // Jagua exports an X-axis reflection; our contract reflects across Y.
        let rotation = (f64::from(t.rotation) - if t.reflected { 180.0 } else { 0.0 })
            .rem_euclid(360.0)
            .to_radians();
        layout.placements.push(Placement {
            part_id: part.id.clone(),
            copy_index: copies[index],
            sheet_id: "strip".into(),
            transform: RigidTransform {
                translation: [f64::from(t.translation.0), f64::from(t.translation.1)],
                rotation_radians: rotation,
                mirrored: t.reflected,
            },
        });
        copies[index] += 1;
    }
    Ok(layout)
}

/// Measure the original transformed outlines, never Sparrow's reported width.
fn strip_length(job: &Job, layout: &Layout) -> f64 {
    let mut length = 0.0_f64;
    for p in &layout.placements {
        let part = job
            .parts
            .iter()
            .find(|part| part.id == p.part_id)
            .expect("validated part");
        let (s, c) = p.transform.rotation_radians.sin_cos();
        for [x, y] in part.geometry.iter().flat_map(|shape| &shape.outer) {
            let x = if p.transform.mirrored { -x } else { *x };
            length = length.max(x * c - y * s + p.transform.translation[0]);
        }
    }
    length
}

struct Recorder<'a, F> {
    job: &'a Job,
    start: Instant,
    deadline: Instant,
    best: Option<(Layout, Report, f64, f64)>,
    rejected: u64,
    error: Option<anyhow::Error>,
    progress: F,
}
impl<F: FnMut(&Progress)> SolutionListener for Recorder<'_, F> {
    fn report(&mut self, kind: ReportType, solution: &SPSolution) {
        if Instant::now() > self.deadline
            || matches!(kind, ReportType::ExplInfeas | ReportType::ExplImproving)
        {
            return;
        }
        let candidate = (|| -> Result<_> {
            let layout = adapt(self.job, io::export(solution, self.start))?;
            let checked = validate(self.job, &layout)?;
            let length = if checked.valid {
                strip_length(self.job, &layout)
            } else {
                f64::INFINITY
            };
            Ok((layout, checked, length))
        })();
        match candidate {
            Err(error) => {
                self.error = Some(error);
            }
            Ok((layout, checked, length)) => {
                if !checked.valid {
                    self.rejected += 1;
                    return;
                }
                let now = Instant::now();
                if now > self.deadline || self.best.as_ref().is_some_and(|b| b.2 <= length) {
                    return;
                }
                let elapsed = now.duration_since(self.start).as_secs_f64();
                (self.progress)(&Progress {
                    elapsed_seconds: elapsed,
                    strip_length: length,
                });
                self.best = Some((layout, checked, length, elapsed));
            }
        }
    }
}

/// Use one native worker and the same 90/10 exploration/compression split as the
/// frozen comparator. Import, construction, candidate checking and search share
/// the wall-clock budget. A late candidate is never accepted. Results may vary
/// with machine scheduling; this is not the deterministic MCP `nest` interface.
pub fn optimize(
    job: &Job,
    options: Options,
    progress: impl FnMut(&Progress),
) -> Result<StripResult> {
    ensure!(
        (1..=300).contains(&options.seconds),
        "strip budget must be 1..300 seconds"
    );
    let start = Instant::now();
    let deadline = start + Duration::from_secs(options.seconds);
    let ext = input(job)?;
    let mut cfg = DEFAULT_SPARROW_CONFIG;
    cfg.poly_simpl_tolerance = None;
    cfg.narrow_concavity_cutoff_ratio = None;
    cfg.expl_cfg.separator_config.n_workers = 1;
    cfg.cmpr_cfg.separator_config.n_workers = 1;
    cfg.expl_cfg.time_limit = Duration::from_secs_f64(options.seconds as f64 * 0.9);
    cfg.cmpr_cfg.time_limit = Duration::from_secs_f64(options.seconds as f64 * 0.1);
    let importer = Importer::new(cfg.cde_config, None, None);
    let instance = io::import_instance(&importer, &ext)?;
    let mut recorder = Recorder {
        job,
        start,
        deadline,
        best: None,
        rejected: 0,
        error: None,
        progress,
    };
    let outcome = sparrow::optimizer::optimize(
        instance,
        Xoshiro256PlusPlus::seed_from_u64(options.seed),
        &mut recorder,
        &mut Deadline {
            global: deadline,
            phase: deadline,
        },
        &cfg.expl_cfg,
        &cfg.cmpr_cfg,
        None,
    );
    if let Some(error) = recorder.error {
        return Err(error);
    }
    if recorder.best.is_none() {
        outcome?;
    }
    let (layout, validation, length, accepted_at) = recorder
        .best
        .context("no independently valid strip layout within the budget")?;
    Ok(StripResult {
        algorithm: "nestbolt-sparrow-strip-v1",
        seed: options.seed,
        seconds: options.seconds,
        strip_length: length,
        layout,
        validation,
        rejected_candidates: recorder.rejected,
        accepted_at_seconds: accepted_at,
        elapsed_seconds: start.elapsed().as_secs_f64(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use nestbolt_validator::{
        Units,
        job::{Margins, Part, Stock, rectangle},
    };

    #[test]
    fn exported_reflection_preserves_copy_ids_and_scores_original_vertices() {
        let job = Job {
            version: 1,
            name: "mapped strip".into(),
            units: Units::Mm,
            clearance: 0.0,
            edge_clearance: 0.0,
            mode: Mode::All,
            parts: vec![Part {
                id: "original-id".into(),
                quantity: 3,
                geometry: vec![rectangle(-1.0, -1.0, 2.0, 2.0)],
                rotations: Rotations::List { degrees: vec![0.0] },
                allow_mirror: true,
                priority: 1.0,
            }],
            stocks: vec![Stock {
                id: "original-stock".into(),
                width: 20.0,
                height: 5.0,
                count: Some(1),
                margins: Margins::default(),
                outline: vec![],
                defects: vec![],
            }],
        };
        let ext =
            serde_json::from_value(json!({"strip_width":999.0,"density":0.0,"run_time_sec":0,
            "layout":{"container_id":0,"density":0.0,"placed_items":(0..3).map(|i|
                json!({"item_id":0,"transformation":{"rotation":180.0,"reflected":true,
                    "translation":[2.0+4.0*f64::from(i),2.0]}})).collect::<Vec<_>>()}}))
            .unwrap();
        let layout = adapt(&job, ext).unwrap();
        assert!(validate(&job, &layout).unwrap().valid);
        assert_eq!(strip_length(&job, &layout), 11.0);
        for (i, p) in layout.placements.iter().enumerate() {
            assert_eq!(p.part_id, "original-id");
            assert_eq!(p.copy_index, i as u32);
            assert!(p.transform.mirrored);
            assert_eq!(p.transform.rotation_radians, 0.0);
        }
        let mut denied = job;
        denied.parts[0].allow_mirror = false;
        assert!(!validate(&denied, &layout).unwrap().valid);
    }

    #[test]
    fn phase_timeouts_never_extend_the_global_budget() {
        let global = Instant::now() + Duration::from_secs(1);
        let mut timer = Deadline {
            global,
            phase: global,
        };
        timer.new_timeout(Duration::from_secs(300));
        assert_eq!(timer.timeout_at(), Some(global));
        timer.new_timeout(Duration::ZERO);
        assert!(timer.kill());
    }
}
