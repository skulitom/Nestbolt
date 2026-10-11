use std::{fs, path::PathBuf};

use anyhow::{Context, Result, ensure};
use clap::{Parser, Subcommand, ValueEnum};
use nestbolt_core::{Units, inspect_json};

#[derive(Parser)]
#[command(version, about = "Nestbolt fixed-sheet nesting groundwork")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Improve a polygon job using an explicit deterministic number of repacking passes.
    Improve {
        #[arg(long)]
        job: PathBuf,
        #[arg(long)]
        output: PathBuf,
        #[arg(long, default_value_t = 0)]
        seed: u64,
        #[arg(long, default_value_t = 4)]
        passes: u32,
        #[arg(long, default_value_t = 64)]
        samples: u32,
        #[arg(long, default_value_t = 4)]
        free_rotations: u32,
    },
    /// Build a first conservative sheet layout, optionally refining each placement.
    Construct {
        #[arg(long)]
        job: PathBuf,
        #[arg(long)]
        output: PathBuf,
        #[arg(long, default_value_t = 0)]
        seed: u64,
        #[arg(long, default_value_t = 64)]
        samples: u32,
        #[arg(long, default_value_t = 4)]
        free_rotations: u32,
        #[arg(long)]
        refine: bool,
        #[arg(long, requires = "refine")]
        contacts: bool,
    },
    /// Check a complete polygon benchmark job/layout against every declared constraint.
    Validate {
        #[arg(long)]
        job: PathBuf,
        #[arg(long)]
        layout: PathBuf,
    },
    /// Independently check a Sparrow strip layout against its original input.
    ValidateSparrow {
        #[arg(long)]
        input: PathBuf,
        #[arg(long)]
        layout: PathBuf,
        #[arg(long, value_enum)]
        units: InputUnits,
    },
    /// Inspect an upstream jagua-rs BPP JSON job (does not solve it).
    Inspect {
        #[arg(short, long)]
        input: PathBuf,
        /// Explicit coordinate units; the input format does not specify them.
        #[arg(long, value_enum)]
        units: InputUnits,
    },
}

#[derive(Clone, Copy, ValueEnum)]
enum InputUnits {
    Mm,
    Inch,
    Unitless,
}

impl From<InputUnits> for Units {
    fn from(value: InputUnits) -> Self {
        match value {
            InputUnits::Mm => Self::Mm,
            InputUnits::Inch => Self::Inch,
            InputUnits::Unitless => Self::Unitless,
        }
    }
}

fn main() -> Result<()> {
    let Cli { command } = Cli::parse();
    match command {
        Command::Improve {
            job,
            output,
            seed,
            passes,
            samples,
            free_rotations,
        } => {
            let job = serde_json::from_slice(&fs::read(&job)?)?;
            let result = nestbolt_core::optimize::optimize(
                &job,
                nestbolt_core::optimize::Options {
                    construct: nestbolt_core::construct::Options {
                        seed,
                        random_samples: samples,
                        free_rotations,
                    },
                    passes,
                },
                |progress| {
                    eprintln!(
                        "{}",
                        serde_json::to_string(progress).expect("finite search progress")
                    )
                },
            )?;
            println!("{}", serde_json::to_string_pretty(&result)?);
            ensure!(
                result.best.complete && result.validation.valid,
                "no complete validated layout found in the requested passes"
            );
            use std::io::Write;
            let mut file = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(&output)?;
            file.write_all(serde_json::to_string_pretty(&result.best.layout)?.as_bytes())?;
        }
        Command::Construct {
            job,
            output,
            seed,
            samples,
            free_rotations,
            refine,
            contacts,
        } => {
            let job = serde_json::from_slice(
                &fs::read(&job).with_context(|| format!("cannot read {}", job.display()))?,
            )?;
            let options = nestbolt_core::construct::Options {
                seed,
                random_samples: samples,
                free_rotations,
            };
            let prepared = nestbolt_core::construct::PreparedJob::new(&job)?;
            let result = if contacts {
                prepared.construct_with_contacts(options)?
            } else if refine {
                prepared.construct_refined(options)?
            } else {
                prepared.construct(options)?
            };
            let report = nestbolt_validator::job::validate(&job, &result.layout)?;
            println!(
                "{}",
                serde_json::to_string_pretty(
                    &serde_json::json!({"construction":result,"validation":report})
                )?
            );
            ensure!(
                result.complete && report.valid,
                "construction incomplete: {} copies unplaced; this does not prove infeasibility",
                result.unplaced
            );
            // Never overwrite a user's existing layout or write an invalid one.
            use std::io::Write;
            let mut file = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(&output)
                .with_context(|| format!("cannot create {}", output.display()))?;
            file.write_all(serde_json::to_string_pretty(&result.layout)?.as_bytes())?;
        }
        Command::Validate { job, layout } => {
            let source = fs::read_to_string(&job)
                .with_context(|| format!("cannot read {}", job.display()))?;
            let result = fs::read_to_string(&layout)
                .with_context(|| format!("cannot read {}", layout.display()))?;
            let job = serde_json::from_str::<nestbolt_validator::job::Job>(&source)
                .context("invalid benchmark job JSON")?;
            let layout = serde_json::from_str::<nestbolt_validator::job::Layout>(&result)
                .context("invalid benchmark layout JSON")?;
            let report = nestbolt_validator::job::validate(&job, &layout)?;
            println!("{}", serde_json::to_string_pretty(&report)?);
            ensure!(
                report.valid,
                "layout failed independent validation; see the JSON report"
            );
        }
        Command::ValidateSparrow {
            input,
            layout,
            units,
        } => {
            let input_json = fs::read_to_string(&input)
                .with_context(|| format!("cannot read {}", input.display()))?;
            let layout_json = fs::read_to_string(&layout)
                .with_context(|| format!("cannot read {}", layout.display()))?;
            let units = match units {
                InputUnits::Mm => nestbolt_validator::Units::Mm,
                InputUnits::Inch => nestbolt_validator::Units::Inch,
                InputUnits::Unitless => nestbolt_validator::Units::Unitless,
            };
            let report = nestbolt_validator::sparrow::validate(&input_json, &layout_json, units)?;
            println!("{}", serde_json::to_string_pretty(&report)?);
            ensure!(
                report.valid,
                "layout failed independent validation; see the JSON report"
            );
        }
        Command::Inspect { input, units } => {
            let json = fs::read_to_string(&input)
                .with_context(|| format!("cannot read {}", input.display()))?;
            let result = inspect_json(&json, units.into())?;
            println!("{}", serde_json::to_string_pretty(&result)?);
        }
    }
    Ok(())
}
