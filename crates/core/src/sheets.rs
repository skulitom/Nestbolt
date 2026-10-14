//! Sparrow-style overlap minimisation for fixed rectangular sheets.
//!
//! Every physical sheet is an unmodified jagua strip of fixed width in a frame
//! rotated by -90 degrees, so the strip's variable axis is the sheet's +Y axis.
//! Parts leave the least-filled sheet one at a time: each insertion first looks
//! for a free gap, then lets Sparrow's separator resolve the overlap it causes.
//! The remaining last sheet is shortened by Sparrow's exploration and compression
//! phases. Collision proxies match the constructor (outer contours with holes
//! reserved, one hull around multipart parts). Every accepted layout passes the
//! independent original-geometry checker. This is a wall-clock benchmark search;
//! it makes no repeatability promise.

use anyhow::{Context, Result, ensure};
use jagua_rs::{
    Instant,
    geometry::{DTransformation, geo_enums::RotationRange},
    io::import::Importer,
    probs::spp::{
        entities::{SPInstance, SPPlacement, SPProblem},
        io,
    },
};
use nestbolt_validator::{
    RigidTransform,
    job::{Job, Layout, Metrics, Mode, Placement, Report, Rotations, Sheet, validate},
};
use rand::{Rng, RngExt, SeedableRng, rngs::Xoshiro256PlusPlus};
use serde::Serialize;
use serde_json::json;
use sparrow::config::DEFAULT_SPARROW_CONFIG;

use crate::clock::{Clock, Deadline, Timing, Work};
use crate::construct::{Options as ConstructOptions, conversion_guard, proxy_points};
use crate::control::{Control, StopReason};

mod native;
mod vstrip;

#[derive(Clone, Copy, Debug)]
pub struct Options {
    /// Total wall-clock budget, including the warm start and final checks.
    pub seconds: f64,
    pub seed: u64,
    /// Share of the budget given to the deterministic repacking warm start.
    pub warm_fraction: f64,
    /// Share of the separator time reserved for Sparrow's compression phase.
    pub compress_fraction: f64,
    /// Number of trailing sheets laid end to end in one virtual strip.
    pub window: usize,
    /// Wall-clock benchmarks, or repeatable work budgets.
    pub timing: Timing,
    /// Real-time limit of a repeatable work budget, at least `seconds` (default
    /// `seconds`). A slower machine than the reference PC can allow more real
    /// time so the same work still finishes; wall-clock runs ignore it.
    pub time_limit: Option<f64>,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            seconds: 60.0,
            seed: 0,
            warm_fraction: 0.1,
            compress_fraction: 0.25,
            window: 12,
            timing: Timing::Wall,
            time_limit: None,
        }
    }
}

#[derive(Clone, Copy, Debug, Serialize)]
pub struct Progress {
    pub elapsed_seconds: f64,
    pub stage: &'static str,
    pub sheets: usize,
    pub material: f64,
}

#[derive(Debug, Default, Serialize)]
pub struct Stats {
    pub direct_insertions: u64,
    pub separated_insertions: u64,
    pub failed_insertions: u64,
    pub ejections: u64,
    pub ejection_moves: u64,
    pub eliminated_sheets: u64,
    pub compressions: u64,
    pub rejected_layouts: u64,
}

#[derive(Debug, Serialize)]
pub struct SheetResult {
    pub algorithm: &'static str,
    pub seed: u64,
    pub seconds: f64,
    pub warm_start: Metrics,
    /// Why the separator was skipped; the general search then used the budget.
    pub unsupported: Option<String>,
    /// Parts placed inside the holes of other parts before the search.
    pub riders: u32,
    pub layout: Layout,
    pub validation: Report,
    pub history: Vec<Progress>,
    pub stats: Stats,
    pub accepted_at_seconds: f64,
    pub elapsed_seconds: f64,
    /// Charged deterministic work units, and whether a work budget finished
    /// before the real-time limit (wall-clock runs are never repeatable).
    pub work: f64,
    pub counts: crate::clock::Counts,
    pub repeatable: bool,
}

/// Two-dimensional affine map `p -> m p + t` in f64.
#[derive(Clone, Copy, Debug)]
struct Affine {
    m: [[f64; 2]; 2],
    t: [f64; 2],
}

impl Affine {
    fn translation(t: [f64; 2]) -> Self {
        Self {
            m: [[1.0, 0.0], [0.0, 1.0]],
            t,
        }
    }

    /// `next` applied after `self`.
    fn then(self, next: Self) -> Self {
        let m = |r: usize, c: usize| next.m[r][0] * self.m[0][c] + next.m[r][1] * self.m[1][c];
        let t = |r: usize| next.m[r][0] * self.t[0] + next.m[r][1] * self.t[1] + next.t[r];
        Self {
            m: [[m(0, 0), m(0, 1)], [m(1, 0), m(1, 1)]],
            t: [t(0), t(1)],
        }
    }

    fn apply(&self, p: [f64; 2]) -> [f64; 2] {
        [
            self.m[0][0] * p[0] + self.m[0][1] * p[1] + self.t[0],
            self.m[1][0] * p[0] + self.m[1][1] * p[1] + self.t[1],
        ]
    }

    fn reflected(&self) -> bool {
        self.m[0][0] * self.m[1][1] - self.m[0][1] * self.m[1][0] < 0.0
    }

    /// Jagua: optional reflection across X, then rotation, then translation.
    fn jagua(dt: &DTransformation) -> Self {
        let (s, c) = f64::from(dt.rotation()).sin_cos();
        let (x, y) = dt.translation();
        Self {
            m: if dt.reflected {
                [[c, s], [s, -c]]
            } else {
                [[c, -s], [s, c]]
            },
            t: [f64::from(x), f64::from(y)],
        }
    }

    /// Our contract: optional reflection across Y, then rotation, then translation.
    fn contract(rt: &RigidTransform) -> Self {
        let (s, c) = rt.rotation_radians.sin_cos();
        Self {
            m: if rt.mirrored {
                [[-c, -s], [-s, c]]
            } else {
                [[c, -s], [s, c]]
            },
            t: rt.translation,
        }
    }
}

fn circular_distance(a: f64, b: f64) -> f64 {
    let d = (a - b).rem_euclid(std::f64::consts::TAU);
    d.min(std::f64::consts::TAU - d)
}

/// The job translated into one fixed-width strip per sheet.
struct Model<'a> {
    job: &'a Job,
    instance: SPInstance,
    full_width: f32,
    /// Jagua's minimum separation: items inflate and strips deflate by half.
    separation: f32,
    frame: Affine,
    inverse: Affine,
    /// Per internal item: original coordinates to jagua's centred shape.
    pre: Vec<Affine>,
    part: Vec<usize>,
    /// Stock defects as outer contours in one sheet's strip frame.
    defects: Vec<Vec<(f32, f32)>>,
}

impl<'a> Model<'a> {
    fn new(job: &'a Job) -> Result<Self> {
        ensure!(
            job.mode == Mode::All,
            "sheet separation supports all-parts jobs"
        );
        ensure!(
            job.stocks.len() == 1 && job.stocks[0].outline.is_empty(),
            "sheet separation supports one rectangular stock size"
        );
        // Defects become inflated container holes, which keep the part
        // clearance; a larger edge clearance would need offset defects.
        ensure!(
            job.stocks[0].defects.is_empty() || job.edge_clearance <= job.clearance,
            "sheet separation keeps defect clearance only up to the part clearance"
        );
        let stock = &job.stocks[0];
        let guard = conversion_guard(job);
        // Jagua inflates items and deflates the strip by half the separation.
        // Round joins are inscribed, so compensate their chord deficit as the
        // constructor does. The strip rectangle is then expanded or shrunk so
        // the real edge gap still covers the requested edge clearance.
        let separation = (job.clearance + guard) / 0.05_f64.cos();
        let expand =
            (job.clearance + guard) / 2.0 + separation / 2.0 - (job.edge_clearance + guard);
        let m = stock.margins;
        let height = stock.width - m.left - m.right + 2.0 * expand;
        let full = stock.height - m.bottom - m.top + 2.0 * expand;
        ensure!(
            height > separation && full > separation,
            "sheet margins and clearances leave no usable area"
        );
        let (a, b) = (m.bottom - expand, stock.width - m.right + expand);
        let frame = Affine {
            m: [[0.0, 1.0], [-1.0, 0.0]],
            t: [-a, b],
        };
        let inverse = Affine {
            m: [[0.0, -1.0], [1.0, 0.0]],
            t: [b, a],
        };
        let mut items = vec![];
        for (id, part) in job.parts.iter().enumerate() {
            let mut points: Vec<[f64; 2]> = proxy_points(part);
            points.dedup();
            if points.len() > 1 && points.first() == points.last() {
                points.pop();
            }
            let shift = |degrees: &[f64]| degrees.iter().map(|d| d - 90.0).collect::<Vec<_>>();
            let rotation = match &part.rotations {
                Rotations::Free => json!({"mode":"continuous"}),
                Rotations::List { degrees } => json!({"mode":"discrete","angles":shift(degrees)}),
                Rotations::Step { degrees } => {
                    let count = (360.0 / degrees).ceil();
                    ensure!(count <= 65536.0, "rotation step exceeds 65,536 angles");
                    let all: Vec<_> = (0..count as u32).map(|i| f64::from(i) * degrees).collect();
                    json!({"mode":"discrete","angles":shift(&all)})
                }
            };
            // A Y-axis mirror in sheet coordinates is a reflection across the
            // strip's 90-degree axis after the frame rotation.
            items.push(json!({"id":id,"demand":part.quantity,
                "shape":{"type":"simple_polygon","data":points},
                "orientation":{"rotation":rotation,
                    "reflection_axes":if part.allow_mirror {vec![90.0]} else {vec![]}},
                "min_quality":null}));
        }
        let ext: io::ext_repr::ExtSPInstance = serde_json::from_value(json!({
            "name": job.name, "min_item_separation": separation,
            "strip_height": height, "items": items}))?;
        let config = DEFAULT_SPARROW_CONFIG;
        // Simplification would inflate shapes beyond the warm start's clearances.
        let simplify = std::env::var_os("NESTBOLT_SIMPLIFY").is_some();
        let importer = Importer::new(
            config.cde_config,
            config.poly_simpl_tolerance.filter(|_| simplify),
            config.narrow_concavity_cutoff_ratio.filter(|_| simplify),
        );
        let instance = io::import_instance(&importer, &ext)?;
        let mut pre = vec![];
        let mut part = vec![];
        for (item, _) in &instance.items {
            let p = item.shape_orig().pre_transform;
            ensure!(
                p.rotation() == 0.0 && !p.reflected,
                "unexpected pre-transform"
            );
            let (x, y) = p.translation();
            pre.push(Affine::translation([f64::from(x), f64::from(y)]));
            part.push(usize::try_from(item.external_id())?);
        }
        let defects = stock
            .defects
            .iter()
            .map(|d| {
                d.outer
                    .iter()
                    .map(|&[x, y]| {
                        let [u, v] = frame.apply([x, y]);
                        (u as f32, v as f32)
                    })
                    .collect()
            })
            .collect();
        Ok(Self {
            job,
            instance,
            defects,
            full_width: full as f32,
            separation: separation as f32,
            frame,
            inverse,
            pre,
            part,
        })
    }

    fn empty_sheet(&self) -> Result<SPProblem> {
        let mut problem = SPProblem::new(self.instance.clone())?;
        problem.change_strip_width(self.full_width)?;
        Ok(problem)
    }

    fn external(&self, item: usize, dt: &DTransformation) -> RigidTransform {
        let g = self.pre[item].then(Affine::jagua(dt)).then(self.inverse);
        let mirrored = g.reflected();
        let mut angle = if mirrored {
            (-g.m[1][0]).atan2(-g.m[0][0])
        } else {
            g.m[1][0].atan2(g.m[0][0])
        }
        .rem_euclid(std::f64::consts::TAU);
        let allowed: Vec<f64> = match &self.job.parts[self.part[item]].rotations {
            Rotations::Free => vec![],
            Rotations::List { degrees } => degrees.iter().map(|d| d.to_radians()).collect(),
            Rotations::Step { degrees } => (0..(360.0 / degrees).ceil() as u32)
                .map(|i| (f64::from(i) * degrees).to_radians())
                .collect(),
        };
        if let Some(&exact) = allowed
            .iter()
            .min_by(|a, b| circular_distance(**a, angle).total_cmp(&circular_distance(**b, angle)))
            && circular_distance(exact, angle) < 1e-3
        {
            angle = exact;
        }
        RigidTransform {
            translation: g.t,
            rotation_radians: angle,
            mirrored,
        }
    }

    fn internal(&self, item: usize, rt: &RigidTransform) -> DTransformation {
        let pre = self.pre[item];
        let undo = Affine::translation([-pre.t[0], -pre.t[1]]);
        let g = undo.then(Affine::contract(rt)).then(self.frame);
        let reflected = g.reflected();
        let mut rotation = g.m[1][0].atan2(g.m[0][0]) as f32;
        let orientations = self.instance.item(item).allowed_orientations();
        let range = if reflected {
            orientations.rotations_after_reflection()
        } else {
            Some(orientations.rotations())
        };
        match range {
            Some(RotationRange::Discrete(angles)) => {
                if let Some(&exact) = angles.iter().min_by(|a, b| {
                    circular_distance(f64::from(**a), f64::from(rotation))
                        .total_cmp(&circular_distance(f64::from(**b), f64::from(rotation)))
                }) {
                    rotation = exact;
                }
            }
            Some(RotationRange::None) => rotation = 0.0,
            _ => {}
        }
        DTransformation::new(rotation, (g.t[0] as f32, g.t[1] as f32)).with_reflection(reflected)
    }

    fn item_of_part(&self, part: usize) -> Option<usize> {
        self.part.iter().position(|&p| p == part)
    }

    fn sheets_of(&self, layout: &Layout) -> Result<Vec<SPProblem>> {
        let mut sheets = vec![];
        for sheet in &layout.sheets {
            let mut problem = self.empty_sheet()?;
            for p in layout.placements.iter().filter(|p| p.sheet_id == sheet.id) {
                let part = self
                    .job
                    .parts
                    .iter()
                    .position(|part| part.id == p.part_id)
                    .context("unknown part")?;
                let item = self.item_of_part(part).context("part without demand")?;
                problem.place_item(SPPlacement {
                    item_idx: item,
                    d_transf: self.internal(item, &p.transform),
                });
            }
            sheets.push(problem);
        }
        Ok(sheets)
    }

    fn to_layout(&self, sheets: &[SPProblem]) -> Layout {
        let mut layout = Layout {
            version: 1,
            units: self.job.units,
            sheets: vec![],
            placements: vec![],
        };
        let mut copies = vec![0_u32; self.job.parts.len()];
        for (index, problem) in sheets.iter().enumerate() {
            if problem.layout().placed_items().is_empty() {
                continue;
            }
            let id = format!("sheet-{index}");
            layout.sheets.push(Sheet {
                id: id.clone(),
                stock_id: self.job.stocks[0].id.clone(),
            });
            for (_, placed) in problem.layout().placed_items() {
                let item = placed.item().idx();
                let part = self.part[item];
                layout.placements.push(Placement {
                    part_id: self.job.parts[part].id.clone(),
                    copy_index: copies[part],
                    sheet_id: id.clone(),
                    transform: self.external(item, &placed.d_transf()),
                });
                copies[part] += 1;
            }
        }
        layout
    }
}

fn placed_area(problem: &SPProblem) -> f32 {
    problem
        .layout()
        .placed_items()
        .values()
        .map(|p| p.item().area())
        .sum()
}

fn better(candidate: &Metrics, incumbent: &Metrics) -> bool {
    candidate.sheets_used < incumbent.sheets_used
        || (candidate.sheets_used == incumbent.sheets_used
            && candidate.material_area < incumbent.material_area)
}

struct Search<'a, 'm, F> {
    model: &'m Model<'a>,
    rng: Xoshiro256PlusPlus,
    clock: Clock,
    best: (Layout, Report, f64),
    history: Vec<Progress>,
    stats: Stats,
    progress: F,
    /// Longest observed independent check (wall seconds), reserved before
    /// every wall-clock deadline.
    check_cost: f64,
    /// Minimum clock spacing of intermediate checks; removals are checked at once.
    check_every: f64,
}

impl<F: FnMut(&Progress, &dyn Fn() -> Option<Layout>)> Search<'_, '_, F> {
    fn metrics(&self) -> &Metrics {
        self.best.1.metrics.as_ref().expect("valid incumbent")
    }

    /// Validate the current state independently and keep it only if better.
    /// The latest instant at which search may start another step and still
    /// finish an independent check before `until`.
    fn last_step(&self, until: f64) -> f64 {
        match self.clock.timing() {
            Timing::Wall => until - self.check_cost * 1.5,
            Timing::Work => until,
        }
    }

    fn deadline(&self, at: f64) -> Deadline {
        Deadline {
            clock: self.clock.clone(),
            at,
        }
    }

    fn accept(&mut self, sheets: &[SPProblem], stage: &'static str) -> Result<bool> {
        let layout = self.model.to_layout(sheets);
        self.accept_layout(layout, stage)
    }

    /// Validate a layout of the whole job independently and keep it if better.
    fn accept_layout(&mut self, layout: Layout, stage: &'static str) -> Result<bool> {
        let started = Instant::now();
        let report = validate(self.model.job, &layout)?;
        self.clock.validated(self.model.job, &layout);
        self.check_cost = self.check_cost.max(started.elapsed().as_secs_f64());
        if !report.valid {
            if std::env::var_os("NESTBOLT_DEBUG").is_some() {
                eprintln!(
                    "debug reject {stage}: {:?}",
                    &report.violations[..report.violations.len().min(6)]
                );
            }
            self.stats.rejected_layouts += 1;
            return Ok(false);
        }
        let metrics = report.metrics.as_ref().expect("valid layout has metrics");
        if std::env::var_os("NESTBOLT_DEBUG").is_some() {
            eprintln!(
                "debug accept {stage}: candidate {} sheets {} vs best {}",
                metrics.normalized_material,
                metrics.sheets_used,
                self.metrics().normalized_material
            );
        }
        if !better(metrics, self.metrics()) {
            return Ok(false);
        }
        let elapsed = self.clock.now();
        let progress = Progress {
            elapsed_seconds: elapsed,
            stage,
            sheets: metrics.sheets_used,
            material: metrics.normalized_material,
        };
        (self.progress)(&progress, &|| Some(layout.clone()));
        self.history.push(progress);
        self.best = (layout, report, elapsed);
        Ok(true)
    }
}

fn least_filled(sheets: &[SPProblem]) -> Option<usize> {
    (0..sheets.len()).min_by(|&a, &b| placed_area(&sheets[a]).total_cmp(&placed_area(&sheets[b])))
}

/// Warm-start from deterministic repacking, then remove sheets and shorten the
/// last one with Sparrow's separator. Jobs outside the separator's model (mixed
/// stock, remnants, defects, fill modes) keep the general repacking search for
/// the whole budget and report why.
pub fn optimize(
    job: &Job,
    options: Options,
    mut progress: impl FnMut(&Progress, &dyn Fn() -> Option<Layout>),
) -> Result<SheetResult> {
    ensure!(
        options.seconds > 0.0 && options.seconds <= 300.0,
        "sheet budget must be in (0, 300] seconds"
    );
    ensure!(options.window >= 1, "the window needs at least one sheet");
    let limit = match options.timing {
        Timing::Work => options.time_limit.unwrap_or(options.seconds),
        Timing::Wall => options.seconds,
    };
    ensure!(
        limit >= options.seconds && limit <= 3600.0,
        "the time limit must be between the budget and 3600 seconds"
    );
    let started = Instant::now();
    let clock = Clock::new(options.timing, limit);
    // A work budget aims to finish within the real limit on the reference machine.
    let budget = match options.timing {
        Timing::Wall => options.seconds,
        Timing::Work => options.seconds * WORK_SHARE,
    };
    // Part-in-part first: filled hosts become rigid groups for the search. The
    // pre-pass stops early once every host is filled; this caps slow ones.
    let grouped = crate::holes::group(job, &clock, budget * HOLE_SHARE, options.seed)?;
    let debug = std::env::var_os("NESTBOLT_DEBUG").is_some();
    if debug {
        eprintln!(
            "debug phase group: real {:.2} clock {:.2}",
            clock.real(),
            clock.now()
        );
    }
    // Improved layouts are offered to the caller lazily, with riders expanded,
    // so callers that only log progress pay nothing.
    let live = |p: &Progress, layout: &dyn Fn() -> Option<Layout>| {
        progress(p, &|| {
            let layout = layout()?;
            if grouped.riders_placed > 0 {
                grouped.expand(job, &layout).ok()
            } else {
                Some(layout)
            }
        })
    };
    let mut result = optimize_job(&grouped.job, options, &clock, budget, live)?;
    if debug {
        eprintln!(
            "debug phase search: real {:.2} clock {:.2}",
            clock.real(),
            clock.now()
        );
    }
    if grouped.riders_placed > 0 {
        let expanded = grouped.expand(job, &result.layout)?;
        let validation = validate(job, &expanded)?;
        ensure!(
            validation.valid,
            "expanded part-in-part layout failed independent validation: {:?}",
            validation.violations
        );
        result.layout = expanded;
        result.validation = validation;
    }
    result.riders = grouped.riders_placed;
    result.elapsed_seconds = started.elapsed().as_secs_f64();
    result.work = clock.work();
    result.counts = clock.counts();
    result.repeatable = options.timing == Timing::Work && !clock.hit_hard_limit();
    Ok(result)
}

/// Largest share of the budget for the part-in-part pre-pass.
pub const HOLE_SHARE: f64 = 0.2;
/// Share of a repeatable budget's seconds converted to work, leaving headroom
/// below the real limit on the reference machine.
pub const WORK_SHARE: f64 = 0.5;
/// Constructor collision checks per reference second, for repeatable warm starts.
pub const CHECKS_PER_SECOND: f64 = 4.0e5;
/// Share of the budget for bounding-rectangle packing, and its reference speed.
pub const RECT_SHARE: f64 = 0.03;
pub const RECT_OPERATIONS_PER_SECOND: f64 = 2.0e8;

fn optimize_job(
    job: &Job,
    options: Options,
    clock: &Clock,
    budget: f64,
    progress: impl FnMut(&Progress, &dyn Fn() -> Option<Layout>),
) -> Result<SheetResult> {
    let finish = match clock.timing() {
        Timing::Wall => budget - 0.25,
        Timing::Work => budget,
    };
    let model = Model::new(job);
    if std::env::var_os("NESTBOLT_DEBUG").is_some() {
        eprintln!(
            "debug phase model: real {:.2} clock {:.2}",
            clock.real(),
            clock.now()
        );
    }
    // Several stock sizes or remnant outlines: the separator then works on the
    // one rectangular size the warm start used, a sub-job whose layouts stay
    // valid for the whole job.
    let restrictable = model.is_err()
        && job.stocks.len() > 1
        && job
            .stocks
            .iter()
            .any(|s| Model::new(&single_stock(job, s)).is_ok());
    let warm_until = if model.is_ok() || restrictable {
        budget * options.warm_fraction
    } else {
        finish
    };
    // Sparrow's own problem (hole-free parts whose area fits one sheet, one
    // rectangular stock without defects): the first complete repacking is kept as
    // the fallback and unmodified Sparrow gets the rest of the budget, as its
    // own command-line run would. Its layouts count only when they fit the sheet.
    let quick = model.is_ok() && sparrow_shaped(job) && clock.timing() == Timing::Wall;
    let mut warm = None;
    if quick {
        let first = warm_start(job, options.seed, clock, 0.0, finish, options.seconds)?;
        if first.best.complete && first.validation.valid {
            warm = Some(first);
        }
    }
    let delegated = warm.is_some();
    let warm = match warm {
        Some(warm) => warm,
        None => warm_start(
            job,
            options.seed,
            clock,
            warm_until,
            finish,
            options.seconds,
        )?,
    };
    ensure!(
        warm.best.complete && warm.validation.valid,
        "could not place every part in {} s: allow more time, more sheets or fewer parts",
        options.seconds
    );
    let mut warm = warm;
    // Packed bounding rectangles suit near-rectangular parts; keep them if better.
    let operations = (budget * RECT_SHARE * RECT_OPERATIONS_PER_SECOND) as u64;
    if let Some((layout, used)) = (!delegated)
        .then(|| crate::rects::pack(job, options.seed, operations))
        .flatten()
    {
        clock.charge(Work::RectOperation, used as f64);
        let report = validate(job, &layout)?;
        clock.validated(job, &layout);
        if report.valid
            && better(
                report.metrics.as_ref().expect("valid layout has metrics"),
                warm.validation.metrics.as_ref().expect("valid warm start"),
            )
        {
            warm.best.layout = layout;
            warm.validation = report;
        }
    }
    if std::env::var_os("NESTBOLT_DEBUG").is_some() {
        eprintln!(
            "debug phase warm: real {:.2} clock {:.2}",
            clock.real(),
            clock.now()
        );
    }
    let mut progress = progress;
    let restricted: Option<Job>;
    // The full job's own warm start, when a single-size start replaced it.
    let mut fallback: Option<(Layout, Report)> = None;
    let model = match model {
        Ok(model) => {
            restricted = None;
            model
        }
        Err(reason) => {
            restricted = if restrictable {
                match single_size_start(job, &warm, options, clock, budget, finish)? {
                    Some((sub, start)) => {
                        if let Some(start) = start {
                            fallback = Some((warm.best.layout.clone(), warm.validation));
                            warm.best.layout = start.best.layout;
                            warm.validation = validate(job, &warm.best.layout)?;
                        }
                        Some(sub)
                    }
                    None => None,
                }
            } else {
                None
            };
            match restricted.as_ref().map(Model::new) {
                Some(Ok(model)) => model,
                _ => {
                    if restrictable && clock.now() < finish {
                        // The warm start mixed sizes: keep repacking instead.
                        let more = warm_start(
                            job,
                            options.seed.wrapping_add(1),
                            clock,
                            finish,
                            finish,
                            options.seconds,
                        )?;
                        if more.best.complete
                            && more.validation.valid
                            && better(
                                more.validation.metrics.as_ref().expect("valid layout"),
                                warm.validation.metrics.as_ref().expect("valid warm start"),
                            )
                        {
                            warm = more;
                        }
                    }
                    let warm_metrics = warm.validation.metrics.clone().expect("valid warm start");
                    let elapsed = clock.now();
                    return Ok(SheetResult {
                        algorithm: "nestbolt-sheet-separator-v1",
                        seed: options.seed,
                        seconds: options.seconds,
                        unsupported: Some(reason.to_string()),
                        riders: 0,
                        history: vec![Progress {
                            elapsed_seconds: elapsed,
                            stage: "general",
                            sheets: warm_metrics.sheets_used,
                            material: warm_metrics.normalized_material,
                        }],
                        warm_start: warm_metrics,
                        layout: warm.best.layout,
                        validation: warm.validation,
                        stats: Stats::default(),
                        accepted_at_seconds: elapsed,
                        elapsed_seconds: elapsed,
                        work: 0.0,
                        counts: Default::default(),
                        repeatable: false,
                    });
                }
            }
        }
    };
    let warm_metrics = warm.validation.metrics.clone().expect("valid warm start");
    // A sub-job normalises material by its own stock; report the whole job's.
    let search_validation = if restricted.is_some() {
        validate(model.job, &warm.best.layout)?
    } else {
        warm.validation
    };
    let scale = warm_metrics.normalized_material
        / search_validation
            .metrics
            .as_ref()
            .expect("valid warm start")
            .normalized_material;
    let elapsed = clock.now();
    let first = Progress {
        elapsed_seconds: elapsed,
        stage: "warm",
        sheets: warm_metrics.sheets_used,
        material: warm_metrics.normalized_material,
    };
    // Offer the warm start at once, so live previews start with a layout.
    progress(&first, &|| Some(warm.best.layout.clone()));
    let mut search = Search {
        model: &model,
        rng: Xoshiro256PlusPlus::seed_from_u64(options.seed),
        clock: clock.clone(),
        best: (warm.best.layout.clone(), search_validation, elapsed),
        history: vec![first],
        stats: Stats::default(),
        progress: |p: &Progress, layout: &dyn Fn() -> Option<Layout>| {
            let scaled = Progress {
                material: p.material * scale,
                ..*p
            };
            progress(&scaled, layout)
        },
        check_cost: 0.0,
        check_every: (options.seconds * 0.1).max(5.0),
    };
    let sheets = model.sheets_of(&warm.best.layout)?;
    // Sparrow's own strip problem, where unmodified Sparrow is the state of the
    // art: it gets the rest of the budget in one run from its own construction
    // (wall clock only: its steps are not charged to repeatable work budgets).
    let mut sheets = Some(sheets);
    if delegated {
        // Sparrow keeps going only once its strip fits the sheet; otherwise our
        // search takes over from the best layout at the checkpoint.
        let now = clock.now();
        if !search.sparrow_single(finish, now + (finish - now) * 0.35)? {
            sheets = Some(model.sheets_of(&search.best.0)?);
        } else {
            sheets = None;
        }
    }
    if let Some(sheets) = sheets {
        search.window_search(sheets, finish, options.compress_fraction, options.window)?;
    }
    let Search {
        best,
        mut history,
        stats,
        ..
    } = search;
    for p in history.iter_mut().skip(1) {
        p.material *= scale;
    }
    let (mut layout, mut validation) = if restricted.is_some() {
        let report = validate(job, &best.0)?;
        ensure!(
            report.valid,
            "single-size search layout failed the whole job's check: {:?}",
            report.violations
        );
        (best.0, report)
    } else {
        (best.0, best.1)
    };
    if let Some((original, report)) = fallback
        && better(
            report.metrics.as_ref().expect("valid warm start"),
            validation.metrics.as_ref().expect("valid layout"),
        )
    {
        (layout, validation) = (original, report);
    }
    Ok(SheetResult {
        algorithm: "nestbolt-sheet-separator-v1",
        seed: options.seed,
        seconds: options.seconds,
        warm_start: warm_metrics,
        unsupported: None,
        riders: 0,
        layout,
        validation,
        history,
        stats,
        accepted_at_seconds: best.2,
        elapsed_seconds: clock.now(),
        work: 0.0,
        counts: Default::default(),
        repeatable: false,
    })
}

/// For several stock sizes: the sub-job of the one rectangular size the
/// separator will search, and a new warm start on it when the full job's warm
/// start mixed sizes (`None` keeps that warm start). Sizes that cannot hold
/// every part by area, or whose start fails, are skipped.
fn single_size_start(
    job: &Job,
    warm: &crate::optimize::SearchResult,
    options: Options,
    clock: &Clock,
    budget: f64,
    finish: f64,
) -> Result<Option<(Job, Option<crate::optimize::SearchResult>)>> {
    if let Some(stock) = used_stock(job, &warm.best.layout)
        && stock.outline.is_empty()
    {
        return Ok(Some((single_stock(job, stock), None)));
    }
    let parts: f64 = job
        .parts
        .iter()
        .map(|p| {
            f64::from(p.quantity)
                * p.geometry
                    .iter()
                    .map(crate::curves::polygon_area)
                    .sum::<f64>()
        })
        .sum();
    let sizes: Vec<_> = job
        .stocks
        .iter()
        .filter(|s| {
            let m = s.margins;
            let usable = (s.width - m.left - m.right) * (s.height - m.bottom - m.top);
            s.outline.is_empty() && s.count.is_none_or(|c| f64::from(c) * usable >= parts)
        })
        .collect();
    let share = budget * options.warm_fraction / sizes.len().max(1) as f64;
    let mut best: Option<(Job, crate::optimize::SearchResult, Metrics)> = None;
    for stock in sizes {
        let sub = single_stock(job, stock);
        let now = clock.now();
        if Model::new(&sub).is_err() || now >= finish {
            continue;
        }
        let Ok(start) = warm_start(
            &sub,
            options.seed,
            clock,
            now + share,
            (now + 2.0 * share).min(finish),
            options.seconds,
        ) else {
            continue;
        };
        if !start.best.complete || !start.validation.valid {
            continue;
        }
        let report = validate(job, &start.best.layout)?;
        let Some(metrics) = report.metrics.filter(|_| report.valid) else {
            continue;
        };
        if best.as_ref().is_none_or(|(_, _, b)| better(&metrics, b)) {
            best = Some((sub, start, metrics));
        }
    }
    Ok(best.map(|(sub, start, _)| (sub, Some(start))))
}

/// Hole-free parts whose net area fits one sheet's usable area, on one
/// rectangular stock without defects: the shape of Sparrow's strip problem.
fn sparrow_shaped(job: &Job) -> bool {
    let [stock] = job.stocks.as_slice() else {
        return false;
    };
    let m = stock.margins;
    let usable = (stock.width - m.left - m.right) * (stock.height - m.bottom - m.top);
    let area: f64 = job
        .parts
        .iter()
        .map(|p| {
            f64::from(p.quantity)
                * p.geometry
                    .iter()
                    .map(crate::curves::polygon_area)
                    .sum::<f64>()
        })
        .sum();
    stock.outline.is_empty()
        && stock.defects.is_empty()
        && job
            .parts
            .iter()
            .all(|p| p.geometry.iter().all(|g| g.holes.is_empty()))
        && area <= usable
}

/// The job with only `stock` available.
fn single_stock(job: &Job, stock: &nestbolt_validator::job::Stock) -> Job {
    Job {
        stocks: vec![stock.clone()],
        ..job.clone()
    }
}

/// The one stock size every sheet of `layout` uses, if there is one.
fn used_stock<'j>(job: &'j Job, layout: &Layout) -> Option<&'j nestbolt_validator::job::Stock> {
    let first = &layout.sheets.first()?.stock_id;
    layout
        .sheets
        .iter()
        .all(|s| &s.stock_id == first)
        .then(|| job.stocks.iter().find(|s| &s.id == first))
        .flatten()
}

/// The repacking warm start: stops at `warm_until` once it has a complete
/// layout, and at `finish` regardless.
fn warm_start(
    job: &Job,
    seed: u64,
    clock: &Clock,
    warm_until: f64,
    finish: f64,
    seconds: f64,
) -> Result<crate::optimize::SearchResult> {
    let explain_interruption = |e: anyhow::Error| {
        if e.is::<crate::control::Interrupted>() {
            anyhow::anyhow!(
                "no complete layout within {} s: these parts are many or detailed; allow more time",
                seconds
            )
        } else {
            e
        }
    };
    let construct = crate::optimize::Options {
        construct: ConstructOptions {
            seed,
            ..ConstructOptions::default()
        },
        passes: 1024,
    };
    Ok(match clock.timing() {
        Timing::Wall => {
            // Never interrupt the warm start before its first complete layout,
            // except at the overall deadline.
            let complete = std::cell::Cell::new(false);
            let mut probe = || {
                let now = clock.now();
                (now >= finish || (complete.get() && now >= warm_until))
                    .then_some(StopReason::Deadline)
            };
            let mut control = Control::new(None, Some(&mut probe));
            crate::optimize::optimize_controlled(job, construct, &mut control, |p| {
                if p.complete && (p.accepted || p.pass > 0) {
                    complete.set(true);
                }
            })
            .map_err(explain_interruption)?
        }
        Timing::Work => {
            // A deterministic collision-check quota; if it cannot finish the
            // first construction, construct once without a quota, still subject
            // to the real deadline. Checks on detailed outlines cost more:
            // weight by the root vertex count.
            let vertices = job
                .parts
                .iter()
                .map(|p| proxy_points(p).len())
                .sum::<usize>() as f64
                / job.parts.len().max(1) as f64;
            let weight = (vertices / 16.0).sqrt().max(1.0);
            let quota = ((warm_until - clock.now()).max(0.0) * CHECKS_PER_SECOND / weight) as u64;
            let mut deadline = || clock.now().is_infinite().then_some(StopReason::Deadline);
            let mut control = Control::new(Some(quota.max(1)), Some(&mut deadline));
            let warm =
                match crate::optimize::optimize_controlled(job, construct, &mut control, |_| {}) {
                    Err(e)
                        if matches!(
                            e.downcast_ref::<crate::control::Interrupted>(),
                            Some(crate::control::Interrupted(StopReason::WorkLimit))
                        ) =>
                    {
                        let mut deadline =
                            || clock.now().is_infinite().then_some(StopReason::Deadline);
                        let mut once_control = Control::new(None, Some(&mut deadline));
                        let once = crate::optimize::Options {
                            passes: 1,
                            ..construct
                        };
                        let warm = crate::optimize::optimize_controlled(
                            job,
                            once,
                            &mut once_control,
                            |_| {},
                        )
                        .map_err(explain_interruption)?;
                        clock.charge(
                            Work::ConstructorCheck,
                            once_control.collision_checks() as f64 * weight,
                        );
                        warm
                    }
                    other => other.map_err(explain_interruption)?,
                };
            clock.charge(
                Work::ConstructorCheck,
                control.collision_checks() as f64 * weight,
            );
            warm
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use nestbolt_validator::{
        Units,
        job::{Margins, Part, Stock},
    };

    fn job(rotations: Rotations, allow_mirror: bool) -> Job {
        Job {
            version: 1,
            name: "frame test".into(),
            units: Units::Mm,
            clearance: 1.5,
            edge_clearance: 2.5,
            mode: Mode::All,
            parts: vec![Part {
                id: "l".into(),
                quantity: 6,
                geometry: vec![nestbolt_validator::Polygon {
                    outer: vec![
                        [0.0, 0.0],
                        [30.0, 0.0],
                        [30.0, 8.0],
                        [9.0, 8.0],
                        [9.0, 20.0],
                        [0.0, 20.0],
                    ],
                    holes: vec![],
                }],
                rotations,
                allow_mirror,
                priority: 1.0,
            }],
            stocks: vec![Stock {
                id: "sheet".into(),
                width: 70.0,
                height: 50.0,
                count: None,
                margins: Margins {
                    left: 3.0,
                    right: 1.0,
                    bottom: 2.0,
                    top: 4.0,
                },
                outline: vec![],
                defects: vec![],
            }],
        }
    }

    #[test]
    fn strip_frame_round_trips_contract_transforms() {
        for (rotations, mirror) in [
            (Rotations::Free, true),
            (
                Rotations::List {
                    degrees: vec![0.0, 90.0, 180.0, 270.0],
                },
                true,
            ),
            (
                Rotations::List {
                    degrees: vec![0.0, 180.0],
                },
                false,
            ),
            (Rotations::Step { degrees: 45.0 }, true),
        ] {
            let job = job(rotations, mirror);
            let model = Model::new(&job).unwrap();
            let allowed: Vec<f64> = match &job.parts[0].rotations {
                Rotations::Free => vec![0.3, 1.9, 4.0],
                Rotations::List { degrees } => degrees.iter().map(|d| d.to_radians()).collect(),
                Rotations::Step { degrees } => (0..8)
                    .map(|i| (f64::from(i) * degrees).to_radians())
                    .collect(),
            };
            for &angle in &allowed {
                for mirrored in [false, true].into_iter().take(if mirror { 2 } else { 1 }) {
                    let rt = RigidTransform {
                        translation: [21.25, 17.5],
                        rotation_radians: angle,
                        mirrored,
                    };
                    let dt = model.internal(0, &rt);
                    assert!(model.instance.item(0).allowed_orientations().allows(&dt));
                    let back = model.external(0, &dt);
                    assert_eq!(back.mirrored, mirrored);
                    assert!(circular_distance(back.rotation_radians, angle) < 1e-6);
                    for i in 0..2 {
                        assert!((back.translation[i] - rt.translation[i]).abs() < 1e-4);
                    }
                }
            }
        }
    }

    #[test]
    fn expired_repeatable_warm_start_does_not_retry_without_a_deadline() {
        let job = job(
            Rotations::List {
                degrees: vec![0.0, 90.0],
            },
            false,
        );
        let clock = Clock::new(Timing::Work, 0.0);
        let result = warm_start(&job, 0, &clock, 0.1, 1.0, 1.0);
        assert!(clock.hit_hard_limit());
        let error = result.expect_err("an expired deadline must stop the initial construction");
        assert!(error.to_string().contains("allow more time"), "{error:#}");
    }

    #[test]
    fn short_sheet_searches_are_independently_valid() {
        for (rotations, mirror) in [
            (
                Rotations::List {
                    degrees: vec![0.0, 90.0, 180.0, 270.0],
                },
                true,
            ),
            (Rotations::Free, false),
        ] {
            let mut job = job(rotations, mirror);
            job.parts[0].quantity = 14;
            let result = optimize(
                &job,
                Options {
                    seconds: 3.0,
                    // Work budgets finish the warm start on any machine speed.
                    timing: Timing::Work,
                    ..Options::default()
                },
                |_, _| {},
            )
            .unwrap();
            assert!(result.validation.valid);
            assert!(validate(&job, &result.layout).unwrap().valid);
            let warm = result.warm_start.normalized_material;
            assert!(result.validation.metrics.unwrap().normalized_material <= warm);
        }
    }

    proptest::proptest! {
        #![proptest_config(proptest::prelude::ProptestConfig::with_cases(64))]
        #[test]
        fn strip_frame_round_trips_random_jobs(
            width in 20.0..3000.0_f64,
            height in 20.0..3000.0_f64,
            margin in 0.0..0.1_f64,
            clearance in 0.0..2.0_f64,
            edge in 0.0..2.0_f64,
            angles in proptest::collection::vec(0u32..360, 1..6),
            mirror in proptest::prelude::any::<bool>(),
            pick in 0usize..6,
            x in 0.0..1.0_f64,
            y in 0.0..1.0_f64,
        ) {
            let mut job = job(Rotations::List { degrees: angles.iter().map(|&a| f64::from(a)).collect() }, mirror);
            let scale = width.min(height) / 200.0;
            for point in &mut job.parts[0].geometry[0].outer {
                *point = [point[0] * scale, point[1] * scale];
            }
            job.clearance = clearance * scale;
            job.edge_clearance = edge * scale;
            job.stocks[0].width = width;
            job.stocks[0].height = height;
            job.stocks[0].margins = Margins {
                left: margin * width,
                right: margin * width / 2.0,
                bottom: margin * height,
                top: margin * height / 3.0,
            };
            let model = Model::new(&job).unwrap();
            let angle = f64::from(angles[pick % angles.len()]).to_radians();
            for mirrored in [false, true].into_iter().take(if mirror { 2 } else { 1 }) {
                let rt = RigidTransform {
                    translation: [x * width, y * height],
                    rotation_radians: angle,
                    mirrored,
                };
                let dt = model.internal(0, &rt);
                proptest::prop_assert!(model.instance.item(0).allowed_orientations().allows(&dt));
                let back = model.external(0, &dt);
                proptest::prop_assert_eq!(back.mirrored, mirrored);
                proptest::prop_assert!(circular_distance(back.rotation_radians, angle) < 1e-6);
                for i in 0..2 {
                    proptest::prop_assert!((back.translation[i] - rt.translation[i]).abs() < 1e-6 * width.max(height));
                }
            }
        }
    }

    #[test]
    fn defects_stay_clear_in_sheet_search() {
        let mut job = job(
            Rotations::List {
                degrees: vec![0.0, 90.0, 180.0, 270.0],
            },
            false,
        );
        job.parts[0].quantity = 10;
        job.edge_clearance = job.clearance;
        job.stocks[0].defects = vec![nestbolt_validator::Polygon {
            outer: vec![[30.0, 18.0], [42.0, 18.0], [42.0, 30.0], [30.0, 30.0]],
            holes: vec![],
        }];
        let result = optimize(
            &job,
            Options {
                seconds: 4.0,
                // Work budgets finish the warm start on any machine speed.
                timing: Timing::Work,
                ..Options::default()
            },
            |_, _| {},
        )
        .unwrap();
        assert!(result.unsupported.is_none());
        assert!(validate(&job, &result.layout).unwrap().valid);
        // A larger edge clearance cannot be kept around defects yet.
        job.edge_clearance = job.clearance + 0.5;
        assert!(Model::new(&job).is_err());
    }

    #[test]
    fn several_stock_sizes_search_one_size() {
        let mut job = job(Rotations::Free, false);
        job.parts[0].quantity = 10;
        // A small capped offcut that cannot hold every part, then the sheet.
        job.stocks.insert(
            0,
            Stock {
                id: "offcut".into(),
                width: 40.0,
                height: 30.0,
                count: Some(1),
                ..job.stocks[0].clone()
            },
        );
        let mut shown = 0;
        let result = optimize(
            &job,
            Options {
                seconds: 6.0,
                // Work budgets finish the warm start on any machine speed.
                timing: Timing::Work,
                ..Options::default()
            },
            |_, layout| {
                if let Some(layout) = layout() {
                    assert!(validate(&job, &layout).unwrap().valid);
                    shown += 1;
                }
            },
        )
        .unwrap();
        assert!(result.unsupported.is_none(), "{:?}", result.unsupported);
        assert!(validate(&job, &result.layout).unwrap().valid);
        assert!(result.validation.valid);
        let metrics = result.validation.metrics.unwrap();
        assert!(metrics.normalized_material <= result.warm_start.normalized_material);
        // Progress material is the whole job's, as in the final report.
        assert!((result.history[0].material - result.warm_start.normalized_material).abs() < 1e-12);
        assert!(shown >= 1, "the warm start is offered to live previews");
    }

    #[test]
    fn sparrow_takes_one_sheet_of_hole_free_parts() {
        let mut job = job(
            Rotations::List {
                degrees: vec![0.0, 90.0, 180.0, 270.0],
            },
            false,
        );
        job.parts[0].quantity = 3;
        assert!(sparrow_shaped(&job));
        let result = optimize(
            &job,
            Options {
                seconds: 4.0,
                ..Options::default()
            },
            |_, _| {},
        )
        .unwrap();
        assert!(validate(&job, &result.layout).unwrap().valid);
        assert_eq!(result.validation.metrics.as_ref().unwrap().sheets_used, 1);
        assert!(
            result.history.iter().any(|p| p.stage == "sparrow"),
            "{:?}",
            result.history
        );
        // Holes, defects or several sheets' worth of parts keep our own search.
        let mut holed = job.clone();
        holed.parts[0].geometry[0].holes =
            vec![vec![[2.0, 2.0], [2.0, 5.0], [5.0, 5.0], [5.0, 2.0]]];
        assert!(!sparrow_shaped(&holed));
        let mut many = job.clone();
        many.parts[0].quantity = 40;
        assert!(!sparrow_shaped(&many));
    }

    #[test]
    // Stopped mid-search on a strip that can never fit, unmodified Sparrow trips
    // its own debug assertion on a NaN loss; release builds have no such check and
    // our search resumes from the last validated layout. check.py runs it in release.
    #[cfg_attr(debug_assertions, ignore = "upstream Sparrow debug assertion")]
    fn sparrow_hands_back_when_its_strip_cannot_fit_the_sheet() {
        // Two fixed 40 x 22 plates pass the area test (1,760 of 2,904 mm2 usable)
        // but with 1 mm spacing cannot share one 66 x 44 sheet, so Sparrow
        // never fits and our search finishes the job on two sheets.
        let mut job = job(Rotations::List { degrees: vec![0.0] }, false);
        job.clearance = 1.0;
        job.edge_clearance = 1.0;
        job.parts[0].quantity = 2;
        job.parts[0].geometry[0].outer = vec![[0.0, 0.0], [40.0, 0.0], [40.0, 22.0], [0.0, 22.0]];
        assert!(sparrow_shaped(&job));
        let result = optimize(
            &job,
            Options {
                seconds: 4.0,
                ..Options::default()
            },
            |_, _| {},
        )
        .unwrap();
        assert!(validate(&job, &result.layout).unwrap().valid);
        assert_eq!(result.validation.metrics.as_ref().unwrap().sheets_used, 2);
        assert!(result.elapsed_seconds < 4.5, "{}", result.elapsed_seconds);
    }

    #[test]
    fn remnant_outline_keeps_the_general_search() {
        let mut job = job(Rotations::Free, false);
        job.stocks[0].outline = vec![nestbolt_validator::Polygon {
            outer: vec![
                [0.0, 0.0],
                [70.0, 0.0],
                [70.0, 25.0],
                [35.0, 25.0],
                [35.0, 50.0],
                [0.0, 50.0],
            ],
            holes: vec![],
        }];
        job.parts[0].quantity = 3;
        let result = optimize(
            &job,
            Options {
                seconds: 6.0,
                timing: Timing::Work,
                ..Options::default()
            },
            |_, _| {},
        )
        .unwrap();
        assert!(result.unsupported.is_some());
        assert!(result.validation.valid);
    }
}
