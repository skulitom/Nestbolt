//! Search time. Wall mode measures real seconds for equal-budget benchmarks.
//! Work mode converts deterministic work counts to seconds with fixed,
//! versioned coefficients, so the same job, seed and budget give the same
//! layout; the real budget remains a hard limit, and hitting it is reported as
//! an incomplete, non-repeatable outcome.
use std::cell::Cell;
use std::rc::Rc;
use std::time::Duration;

use jagua_rs::Instant;
use serde::Serialize;

pub const WORK_VERSION: &str = "nestbolt-work-v1";

/// Kinds of deterministic work, with reference seconds per unit (AMD Ryzen 9
/// 7950X3D, one core). Changing a coefficient changes repeatable results.
#[derive(Clone, Copy, Debug)]
pub enum Work {
    /// One sample evaluation (collision query and loss).
    Evaluation,
    /// One vertex of an evaluated shape.
    EvaluatedVertex,
    /// One item in a collision-tracker rebuild.
    TrackedItem,
    /// One item re-registered by a container swap or snapshot rebuild.
    RegisteredItem,
    /// One container (with its static hazards) built.
    Container,
    /// One constructor collision check.
    ConstructorCheck,
    /// One vertex of a shape in a collision-tracker rebuild.
    TrackedVertex,
    /// One placed vertex checked by the independent validator.
    ValidatedVertex,
}

// Fitted on 16 development jobs (20 s wall-clock runs, `nestbolt-work-v1`):
// predicted/real time 0.72-1.23 per job.
const COEFFICIENTS: [f64; 8] = [1.8e-6, 1.9e-8, 2.0e-5, 2.0e-6, 0.05, 2.5e-6, 7.3e-7, 4.0e-6];

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Timing {
    Wall,
    Work,
}

struct Inner {
    start: Instant,
    timing: Timing,
    counts: Cell<[f64; 8]>,
    /// Real-time limit, in seconds since start.
    hard: f64,
    hit_hard: Cell<bool>,
}

/// Raw work counts behind the clock, for calibration and reports.
#[derive(Clone, Copy, Debug, Default, Serialize)]
pub struct Counts {
    pub evaluations: f64,
    pub evaluated_vertices: f64,
    pub tracked_items: f64,
    pub registered_items: f64,
    pub containers: f64,
    pub constructor_checks: f64,
    pub tracked_vertices: f64,
    pub validated_vertices: f64,
}

#[derive(Clone)]
pub struct Clock(Rc<Inner>);

impl Clock {
    pub fn new(timing: Timing, hard_limit_seconds: f64) -> Self {
        Self(Rc::new(Inner {
            start: Instant::now(),
            timing,
            counts: Cell::new([0.0; 8]),
            hard: hard_limit_seconds,
            hit_hard: Cell::new(false),
        }))
    }

    pub fn timing(&self) -> Timing {
        self.0.timing
    }

    pub fn real(&self) -> f64 {
        self.0.start.elapsed().as_secs_f64()
    }

    /// Reference seconds of the work charged so far.
    pub fn work(&self) -> f64 {
        self.0
            .counts
            .get()
            .iter()
            .zip(COEFFICIENTS)
            .map(|(n, c)| n * c)
            .sum()
    }

    /// Seconds since start: real, or charged work in reference seconds.
    pub fn now(&self) -> f64 {
        match self.0.timing {
            Timing::Wall => self.real(),
            Timing::Work => {
                if self.real() >= self.0.hard {
                    self.0.hit_hard.set(true);
                    f64::INFINITY
                } else {
                    self.work()
                }
            }
        }
    }

    /// Record deterministic work.
    pub fn charge(&self, kind: Work, amount: f64) {
        let mut c = self.0.counts.get();
        c[kind as usize] += amount;
        self.0.counts.set(c);
    }

    pub fn counts(&self) -> Counts {
        let c = self.0.counts.get();
        Counts {
            evaluations: c[0],
            evaluated_vertices: c[1],
            tracked_items: c[2],
            registered_items: c[3],
            containers: c[4],
            constructor_checks: c[5],
            tracked_vertices: c[6],
            validated_vertices: c[7],
        }
    }

    /// Charge one independent check of `layout` against `job`.
    pub fn validated(
        &self,
        job: &nestbolt_validator::job::Job,
        layout: &nestbolt_validator::job::Layout,
    ) {
        let vertices: std::collections::HashMap<&str, usize> = job
            .parts
            .iter()
            .map(|p| {
                let n = p
                    .geometry
                    .iter()
                    .map(|g| g.outer.len() + g.holes.iter().map(Vec::len).sum::<usize>())
                    .sum();
                (p.id.as_str(), n)
            })
            .collect();
        let total: usize = layout
            .placements
            .iter()
            .map(|p| vertices.get(p.part_id.as_str()).copied().unwrap_or(0))
            .sum();
        self.charge(Work::ValidatedVertex, total as f64);
    }

    /// True once work mode stopped at the real-time limit.
    pub fn hit_hard_limit(&self) -> bool {
        self.0.hit_hard.get()
    }

    /// A real instant for APIs that need one, `at` clock seconds from start.
    /// Exact in wall mode; in work mode the hard limit.
    pub fn instant(&self, at: f64) -> Instant {
        match self.0.timing {
            Timing::Wall => self.0.start + Duration::from_secs_f64(at.max(0.0)),
            Timing::Work => self.0.start + Duration::from_secs_f64(self.0.hard),
        }
    }
}

/// Stops search when the clock reaches `at`.
#[derive(Clone)]
pub struct Deadline {
    pub clock: Clock,
    pub at: f64,
}

impl Deadline {
    pub fn passed(&self) -> bool {
        self.clock.now() >= self.at
    }
}

impl sparrow::util::terminator::Terminator for Deadline {
    fn kill(&self) -> bool {
        self.passed()
    }
    fn new_timeout(&mut self, duration: Duration) {
        self.at = self.at.min(self.clock.now() + duration.as_secs_f64());
    }
    fn timeout_at(&self) -> Option<Instant> {
        Some(self.clock.instant(self.at))
    }
}
