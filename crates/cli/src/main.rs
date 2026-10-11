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
