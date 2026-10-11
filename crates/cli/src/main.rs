use std::{fs, path::PathBuf};

use anyhow::{Context, Result};
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
        Command::Inspect { input, units } => {
            let json = fs::read_to_string(&input)
                .with_context(|| format!("cannot read {}", input.display()))?;
            let result = inspect_json(&json, units.into())?;
            println!("{}", serde_json::to_string_pretty(&result)?);
        }
    }
    Ok(())
}
