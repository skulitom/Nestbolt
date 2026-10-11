//! Public API wrapper: the pinned Sparrow optimiser is an unmodified dependency.
//! A common deadline includes construction and rejects late solution callbacks.
use anyhow::{Result, ensure};
use jagua_rs::Instant;
use jagua_rs::io::import::Importer;
use jagua_rs::probs::spp::{entities::SPSolution, io};
use rand::{SeedableRng, rngs::Xoshiro256PlusPlus};
use serde_json::json;
use sparrow::config::DEFAULT_SPARROW_CONFIG;
use sparrow::optimizer::optimize;
use sparrow::util::listener::{ReportType, SolutionListener};
use sparrow::util::terminator::Terminator;
use std::fs::{self, File};
use std::io::Write;
use std::time::Duration;

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

struct Recorder {
    start: Instant,
    deadline: Instant,
    best: Option<SPSolution>,
    accepted_at: Option<f64>,
    candidates: usize,
    history: File,
}
impl SolutionListener for Recorder {
    fn report(&mut self, kind: ReportType, solution: &SPSolution) {
        let now = Instant::now();
        if now > self.deadline
            || matches!(kind, ReportType::ExplInfeas | ReportType::ExplImproving)
            || self
                .best
                .as_ref()
                .is_some_and(|b| b.strip_width() <= solution.strip_width())
        {
            return;
        }
        self.candidates += 1;
        self.accepted_at = Some(now.duration_since(self.start).as_secs_f64());
        self.best = Some(solution.clone());
        let row = json!({"elapsed_seconds": self.accepted_at, "kind": format!("{kind:?}"),
            "solution": io::export(solution, self.start)});
        writeln!(self.history, "{row}").expect("cannot retain native candidate evidence");
        self.history
            .flush()
            .expect("cannot flush candidate evidence");
    }
}

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().collect();
    ensure!(
        args.len() == 5,
        "usage: benchmark input.json seconds seed identical|upstream-default"
    );
    let seconds: u64 = args[2].parse()?;
    let seed: u64 = args[3].parse()?;
    ensure!(
        (1..=300).contains(&seconds),
        "budget must be 1..300 seconds"
    );
    ensure!(
        matches!(args[4].as_str(), "identical" | "upstream-default"),
        "unknown settings"
    );
    // Parsing, like SVG/JSON import in the other controllers, precedes the solve
    // clock. Polygon import, initial construction and both search phases count.
    let input: io::ext_repr::ExtSPInstance = serde_json::from_slice(&fs::read(&args[1])?)?;
    let mut config = DEFAULT_SPARROW_CONFIG;
    config.expl_cfg.separator_config.n_workers = 1;
    config.cmpr_cfg.separator_config.n_workers = 1;
    config.expl_cfg.time_limit = Duration::from_secs_f64(seconds as f64 * 0.9);
    config.cmpr_cfg.time_limit = Duration::from_secs_f64(seconds as f64 * 0.1);
    if args[4] == "identical" {
        config.poly_simpl_tolerance = None;
        config.narrow_concavity_cutoff_ratio = None;
    }
    let history = File::create("candidates.jsonl")?;
    let start = Instant::now();
    let deadline = start + Duration::from_secs(seconds);
    let importer = Importer::new(
        config.cde_config,
        config.poly_simpl_tolerance,
        config.narrow_concavity_cutoff_ratio,
    );
    let instance = io::import_instance(&importer, &input)?;
    let mut recorder = Recorder {
        start,
        deadline,
        best: None,
        accepted_at: None,
        candidates: 0,
        history,
    };
    let mut terminator = Deadline {
        global: deadline,
        phase: deadline,
    };
    let result = optimize(
        instance,
        Xoshiro256PlusPlus::seed_from_u64(seed),
        &mut recorder,
        &mut terminator,
        &config.expl_cfg,
        &config.cmpr_cfg,
        None,
    );
    let output = json!({"status": if recorder.best.is_some() {"completed"} else {"no_layout"},
        "seconds": seconds, "seed": seed, "workers": 1, "settings": args[4],
        "search_finished_seconds": start.elapsed().as_secs_f64(), "accepted_at_seconds": recorder.accepted_at,
        "candidates": recorder.candidates, "error": result.err().map(|e| e.to_string()),
        "solution": recorder.best.as_ref().map(|s| io::export(s, start))});
    serde_json::to_writer_pretty(File::create("solver-result.json")?, &output)?;
    println!("{output}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn phases_cannot_extend_the_global_budget() {
        let global = Instant::now() + Duration::from_secs(60);
        let mut timer = Deadline {
            global,
            phase: global,
        };
        timer.new_timeout(Duration::from_secs(300));
        assert_eq!(timer.timeout_at(), Some(global));
        timer.new_timeout(Duration::ZERO);
        assert!(timer.kill());
        timer.global = Instant::now() - Duration::from_secs(1);
        timer.new_timeout(Duration::from_secs(300));
        assert!(timer.kill());
    }
}
