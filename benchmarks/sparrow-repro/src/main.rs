// SPDX-License-Identifier: MPL-2.0
// Benchmark orchestration adapted from Sparrow's src/bench.rs at 7f069e9.
// Copyright (c) Jeroen Gardeyn and contributors. See UPSTREAM_LICENSE.
//! Adapter around the unmodified published Sparrow library. No search changes.
use std::{fs::File, path::Path, time::Duration};

use anyhow::{Context, Result, ensure};
use jagua_rs::{io::import::Importer, io::svg::s_layout_to_svg};
use rand::{Rng, RngCore, SeedableRng, rngs::SmallRng};
use sparrow::{
    EPOCH, config,
    optimizer::{
        Terminator, compression_phase, exploration_phase, lbf::LBFBuilder, separator::Separator,
    },
    util::io::{self, SPOutput},
};

fn main() -> Result<()> {
    let _started = *EPOCH;
    let args: Vec<String> = std::env::args().skip(1).collect();
    ensure!(
        args.len() == 4,
        "usage: nestbolt-sparrow-repro INPUT SECONDS ARCHIVE_SEED RUN_INDEX"
    );
    let seconds: u64 = args[1].parse().context("invalid time budget")?;
    let master_seed: u64 = args[2].parse().context("invalid archive seed")?;
    let run_index: usize = args[3].parse().context("invalid run index")?;
    ensure!(
        (1..=1200).contains(&seconds),
        "budget must be 1..1200 seconds"
    );
    ensure!(run_index < 100, "run index must be below 100");

    // Match bench.rs's master-to-run seed derivation in published run order.
    let mut master = SmallRng::seed_from_u64(master_seed);
    let mut run_seed = 0_u64;
    for _ in 0..=run_index {
        run_seed = master.random();
    }
    let external = io::read_spp_instance_json(Path::new(&args[0]))?;
    let importer = Importer::new(
        config::CDE_CONFIG,
        config::SIMPL_TOLERANCE,
        config::MIN_ITEM_SEPARATION,
    );
    let instance = jagua_rs::probs::spp::io::import(&importer, &external)?;
    println!(
        "{}",
        serde_json::json!({"phase": "start", "instance": external.name,
        "archive_seed": master_seed.to_string(), "run_index": run_index,
        "derived_run_seed": run_seed.to_string(), "seconds": seconds,
        "workers": config::SEP_CFG_EXPLORE.n_workers})
    );

    std::fs::create_dir_all("output")?;
    let budget = Duration::from_secs(seconds);
    let mut rng = SmallRng::seed_from_u64(run_seed);
    let mut next_rng = || SmallRng::seed_from_u64(rng.next_u64());
    let builder =
        LBFBuilder::new(instance.clone(), next_rng(), config::LBF_SAMPLE_CONFIG).construct();
    let mut explore = Separator::new(
        builder.instance,
        builder.prob,
        next_rng(),
        "output/intermediate".into(),
        0,
        config::SEP_CFG_EXPLORE,
    );
    let mut terminator = Terminator::new_with_ctrlc_handler();
    terminator.set_timeout_from_now(budget.mul_f32(config::EXPLORE_TIME_RATIO));
    let solutions = exploration_phase(&instance, &mut explore, &terminator);
    let final_explore = solutions.last().context("no exploration solution")?;
    terminator
        .set_timeout_from_now(budget.mul_f32(config::COMPRESS_TIME_RATIO))
        .reset_ctrlc();
    let mut compress = Separator::new(
        explore.instance,
        explore.prob,
        next_rng(),
        explore.output_svg_folder,
        explore.svg_counter,
        config::SEP_CFG_COMPRESS,
    );
    let solution = compression_phase(&instance, &mut compress, final_explore, &terminator);
    let width = solution.strip_width();
    let density = solution.density(&instance);
    let svg = s_layout_to_svg(
        &solution.layout_snapshot,
        &instance,
        config::DRAW_OPTIONS,
        "reproduced",
    );
    std::fs::write("output/layout.svg", svg.to_string())?;
    let output = SPOutput {
        instance: external,
        solution: jagua_rs::probs::spp::io::export(&instance, &solution, *EPOCH),
    };
    serde_json::to_writer_pretty(File::create("output/layout.json")?, &output)?;
    println!(
        "{}",
        serde_json::json!({"phase": "finished", "strip_width": width, "density": density})
    );
    Ok(())
}
