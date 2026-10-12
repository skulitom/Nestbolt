//! A single sheet without defects is Sparrow's own strip problem: the sheet's
//! width is the strip height and the used length is what the material score
//! measures. Unmodified Sparrow runs from its own construction within one core
//! and a deadline on our clock; every improvement it reports must pass the
//! independent validator. If its strip still does not fit the sheet by a
//! checkpoint, it stops so the caller's own search can use the rest.
use super::*;
use jagua_rs::probs::spp::entities::SPSolution;
use sparrow::util::{
    listener::{ReportType, SolutionListener},
    terminator::Terminator,
};
use std::{cell::Cell, rc::Rc, time::Duration};

/// Sparrow's phase timeouts within one overall deadline on our clock, plus an
/// early stop at `checkpoint` while no strip it found fits the sheet.
struct Phased {
    clock: Clock,
    global: f64,
    phase: f64,
    checkpoint: f64,
    fits: Rc<Cell<bool>>,
}

impl Terminator for Phased {
    fn kill(&self) -> bool {
        let now = self.clock.now();
        now >= self.phase.min(self.global) || (now >= self.checkpoint && !self.fits.get())
    }
    fn new_timeout(&mut self, duration: Duration) {
        self.phase = (self.clock.now() + duration.as_secs_f64()).min(self.global);
    }
    fn timeout_at(&self) -> Option<jagua_rs::Instant> {
        Some(self.clock.instant(self.phase.min(self.global)))
    }
}

struct Listener<'s, 'a, 'm, F> {
    search: &'s mut Search<'a, 'm, F>,
    instance: SPInstance,
    best_width: f32,
    /// The latest improvement, independently checked at most every `INTERVAL`
    /// seconds and once at the end: Sparrow reports many small steps.
    pending: Option<SPSolution>,
    checked: f64,
    /// Set once a reported strip is no longer than the sheet.
    fits: Rc<Cell<bool>>,
    error: Option<anyhow::Error>,
}

/// Seconds between independent checks of Sparrow's improvements.
const INTERVAL: f64 = 2.0;

impl<F: FnMut(&Progress, &dyn Fn() -> Option<Layout>)> Listener<'_, '_, '_, F> {
    fn flush(&mut self) {
        let Some(solution) = self.pending.take() else {
            return;
        };
        self.checked = self.search.clock.now();
        let result = (|| -> Result<bool> {
            let mut sheet = SPProblem::new(self.instance.clone())?;
            sheet.restore(&solution);
            self.search.accept(&[sheet], "sparrow")
        })();
        if let Err(error) = result {
            self.error = Some(error);
        }
    }
}

impl<F: FnMut(&Progress, &dyn Fn() -> Option<Layout>)> SolutionListener
    for Listener<'_, '_, '_, F>
{
    fn report(&mut self, kind: ReportType, solution: &SPSolution) {
        if self.error.is_some()
            || matches!(kind, ReportType::ExplInfeas | ReportType::ExplImproving)
            || solution.strip().width >= self.best_width
        {
            return;
        }
        self.best_width = solution.strip().width;
        if self.best_width <= self.search.model.full_width {
            self.fits.set(true);
        }
        self.pending = Some(solution.clone());
        if self.search.clock.now() - self.checked >= INTERVAL {
            self.flush();
        }
    }
}

impl<F: FnMut(&Progress, &dyn Fn() -> Option<Layout>)> Search<'_, '_, F> {
    /// Unmodified Sparrow (its own construction, 90/10 exploration and
    /// compression, one worker, as the frozen comparator runs it) until `until`.
    /// Returns false if it stopped at `checkpoint` without a strip that fits.
    pub(super) fn sparrow_single(&mut self, until: f64, checkpoint: f64) -> Result<bool> {
        let span = (self.last_step(until) - self.clock.now()).max(0.0);
        let mut cfg = DEFAULT_SPARROW_CONFIG;
        cfg.expl_cfg.separator_config.n_workers = 1;
        cfg.cmpr_cfg.separator_config.n_workers = 1;
        cfg.expl_cfg.time_limit = Duration::from_secs_f64(span * 0.9);
        cfg.cmpr_cfg.time_limit = Duration::from_secs_f64(span * 0.1);
        let global = self.last_step(until);
        let seed = self.rng.next_u64();
        let instance = self.model.instance.clone();
        let clock = self.clock.clone();
        let fits = Rc::new(Cell::new(false));
        let mut listener = Listener {
            search: self,
            instance: instance.clone(),
            best_width: f32::INFINITY,
            pending: None,
            checked: f64::NEG_INFINITY,
            fits: fits.clone(),
            error: None,
        };
        let outcome = sparrow::optimizer::optimize(
            instance,
            Xoshiro256PlusPlus::seed_from_u64(seed),
            &mut listener,
            &mut Phased {
                clock,
                global,
                phase: global,
                checkpoint,
                fits: fits.clone(),
            },
            &cfg.expl_cfg,
            &cfg.cmpr_cfg,
            None,
        );
        listener.flush();
        if let Some(error) = listener.error {
            return Err(error);
        }
        outcome.map(|_| fits.get())
    }
}
