use std::{fs, path::PathBuf};

use anyhow::{Context, Result, ensure};
use clap::{Parser, Subcommand, ValueEnum};
use nestbolt_core::{Units, inspect_json};

#[derive(Parser)]
#[command(name = "nestbolt", version, about = "Nestbolt fixed-sheet nesting")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Import closed outlines from SVG/DXF files into a part library (mm).
    Import {
        #[arg(required = true)]
        inputs: Vec<PathBuf>,
        #[arg(long)]
        output: PathBuf,
        /// Maximum distance between exact curves and nesting polygons, in mm.
        #[arg(long, default_value_t = 0.005)]
        tolerance: f64,
        /// Millimetres per SVG user unit when a document has no absolute size.
        #[arg(long)]
        svg_user_unit_mm: Option<f64>,
        /// Millimetres per DXF unit when $INSUNITS is missing.
        #[arg(long)]
        dxf_unit_mm: Option<f64>,
        /// Close larger gaps up to this many mm (off by default, maximum 1).
        #[arg(long = "close-gaps")]
        close_gaps_mm: Option<f64>,
        /// Comma-separated cut layer names (otherwise prefer cut/outline/profile).
        #[arg(long, value_delimiter = ',')]
        layers: Option<Vec<String>>,
        /// Comma-separated DXF ACI numbers or RGB colours such as #000000.
        #[arg(long, value_delimiter = ',')]
        colors: Option<Vec<String>>,
        /// Stock-outline layers offered separately from parts (defaults to SHEET).
        /// Supply the flag without values to disable stock-outline discovery.
        #[arg(long, value_delimiter = ',', num_args = 0..)]
        sheet_layers: Option<Vec<String>>,
    },
    /// Nest library parts on sheets and write the layout, report and exports.
    Nest {
        #[arg(long)]
        library: PathBuf,
        #[arg(long)]
        request: PathBuf,
        #[arg(long)]
        out_dir: PathBuf,
        #[arg(long, default_value_t = 60.0)]
        seconds: f64,
        #[arg(long, default_value_t = 0)]
        seed: u64,
        /// Draw sheet boundaries in exports (in their own group/layer).
        #[arg(long)]
        sheet_outline: bool,
        /// Use a repeatable work budget instead of wall-clock time: the same
        /// inputs, budget and seed give the same layout.
        #[arg(long)]
        repeatable: bool,
        /// Real-time limit for a repeatable budget (default: --seconds). On a
        /// machine slower than the reference PC, allow more so the work finishes.
        #[arg(long, requires = "repeatable")]
        time_limit: Option<f64>,
    },
    /// Write per-sheet SVG and DXF files for an existing layout.
    Export {
        #[arg(long)]
        library: PathBuf,
        #[arg(long)]
        request: PathBuf,
        #[arg(long)]
        layout: PathBuf,
        #[arg(long)]
        out_dir: PathBuf,
        #[arg(long)]
        sheet_outline: bool,
    },
    /// Native strip-parity diagnostic using pinned Sparrow, timed rather than fixed-work.
    Strip {
        #[arg(long)]
        job: PathBuf,
        #[arg(long)]
        output: PathBuf,
        #[arg(long, default_value_t = 0)]
        seed: u64,
        #[arg(long, default_value_t = 60, value_parser = clap::value_parser!(u64).range(1..=300))]
        seconds: u64,
    },
    /// Timed fixed-sheet search: repacking warm start, then Sparrow-style sheet
    /// removal and last-sheet compression. Wall-clock, not repeatable.
    Sheets {
        #[arg(long)]
        job: PathBuf,
        #[arg(long)]
        output: PathBuf,
        #[arg(long, default_value_t = 0)]
        seed: u64,
        #[arg(long, default_value_t = 60.0)]
        seconds: f64,
        #[arg(long, default_value_t = 0.1)]
        warm_fraction: f64,
        #[arg(long, default_value_t = 0.25)]
        compress_fraction: f64,
        #[arg(long, default_value_t = 12)]
        window: usize,
        /// Use a repeatable work budget instead of wall-clock time.
        #[arg(long)]
        repeatable: bool,
        /// Real-time limit for a repeatable budget (default: --seconds).
        #[arg(long, requires = "repeatable")]
        time_limit: Option<f64>,
    },
    /// Compact an existing valid layout with bounded translation sweeps.
    Compact {
        #[arg(long)]
        job: PathBuf,
        #[arg(long)]
        layout: PathBuf,
        #[arg(long)]
        output: PathBuf,
        #[arg(long, default_value_t = 2)]
        sweeps: u32,
        #[arg(long)]
        max_checks: Option<u64>,
        #[arg(long)]
        relocate: bool,
    },
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
        /// Deterministic collision-query limit shared by all search passes.
        #[arg(long)]
        max_checks: Option<u64>,
        /// Cooperative safety deadline; returns the last completed valid layout.
        #[arg(long, value_parser = clap::value_parser!(u64).range(1..=300_000))]
        timeout_ms: Option<u64>,
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

/// Create a new file; never overwrite a user's existing output.
fn write_new(path: &std::path::Path, bytes: &[u8]) -> Result<()> {
    use std::io::Write;
    let mut file = fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(path)
        .with_context(|| format!("cannot create {} (it may already exist)", path.display()))?;
    file.write_all(bytes)?;
    Ok(())
}

fn exports(
    job: &nestbolt_validator::job::Job,
    layout: &nestbolt_validator::job::Layout,
    outlines: &std::collections::HashMap<String, nestbolt_core::export::Outline>,
    out_dir: &std::path::Path,
    sheet_outline: bool,
) -> Result<Vec<String>> {
    let options = nestbolt_core::export::Options { sheet_outline };
    let mut written = vec![];
    for sheet in &layout.sheets {
        for (ext, text) in [
            (
                "svg",
                nestbolt_core::export::svg(job, layout, &sheet.id, outlines, options)?,
            ),
            (
                "dxf",
                nestbolt_core::export::dxf(job, layout, &sheet.id, outlines, options)?,
            ),
        ] {
            let path = out_dir.join(format!("{}.{ext}", sheet.id));
            write_new(&path, text.as_bytes())?;
            written.push(path.display().to_string());
        }
    }
    Ok(written)
}

fn main() -> Result<()> {
    let Cli { command } = Cli::parse();
    match command {
        Command::Import {
            inputs,
            output,
            tolerance,
            svg_user_unit_mm,
            dxf_unit_mm,
            close_gaps_mm,
            layers,
            colors,
            sheet_layers,
        } => {
            let mut options = nestbolt_core::import::Options {
                tolerance,
                close_gaps_mm,
                layers,
                colors,
                sheet_layers,
                ..Default::default()
            };
            if let Some(u) = svg_user_unit_mm {
                options.svg_user_unit = u;
            }
            if let Some(u) = dxf_unit_mm {
                options.dxf_unit = u;
            }
            let files = inputs
                .iter()
                .map(|p| {
                    let name = p
                        .file_name()
                        .and_then(|n| n.to_str())
                        .context("input file name")?
                        .to_owned();
                    let bytes =
                        fs::read(p).with_context(|| format!("cannot read {}", p.display()))?;
                    let text = nestbolt_core::import::decode_drawing(&name, &bytes)
                        .with_context(|| format!("cannot decode {}", p.display()))?;
                    Ok((name, text))
                })
                .collect::<Result<Vec<_>>>()?;
            let library = nestbolt_core::project::Library::import(&files, &options)?;
            write_new(&output, serde_json::to_string_pretty(&library)?.as_bytes())?;
            let summary: Vec<_> = library
                .parts
                .iter()
                .map(|p| {
                    serde_json::json!({"id": p.id, "source": p.source, "area_mm2": p.area_mm2,
                    "bounds_mm": p.bounds_mm, "holes": p.holes.len()})
                })
                .collect();
            println!(
                "{}",
                serde_json::to_string_pretty(
                    &serde_json::json!({"library": output, "parts": summary,
                    "warnings": library.warnings,"imports":library.imports,
                    "sheet_outlines": library.sheet_outlines.iter().map(|s| serde_json::json!({
                        "id":s.id,"source":s.source,"width_mm":s.width_mm,"height_mm":s.height_mm,
                        "origin_mm":s.origin_mm,"tolerance_mm":s.tolerance_mm})).collect::<Vec<_>>()})
                )?
            );
        }
        Command::Nest {
            library,
            request,
            out_dir,
            seconds,
            seed,
            sheet_outline,
            repeatable,
            time_limit,
        } => {
            let library: nestbolt_core::project::Library =
                serde_json::from_slice(&fs::read(&library)?)
                    .context("invalid part library JSON")?;
            let request: nestbolt_core::project::Request =
                serde_json::from_slice(&fs::read(&request)?)
                    .context("invalid nest request JSON")?;
            let (job, outlines) = request.job(&library)?;
            fs::create_dir_all(&out_dir)?;
            let result = nestbolt_core::sheets::optimize(
                &job,
                nestbolt_core::sheets::Options {
                    seconds,
                    seed,
                    timing: if repeatable {
                        nestbolt_core::clock::Timing::Work
                    } else {
                        nestbolt_core::clock::Timing::Wall
                    },
                    time_limit,
                    ..Default::default()
                },
                |p, _| eprintln!("{}", serde_json::to_string(p).expect("finite progress")),
            )?;
            ensure!(
                result.validation.valid,
                "result failed independent validation"
            );
            write_new(
                &out_dir.join("job.json"),
                serde_json::to_string_pretty(&job)?.as_bytes(),
            )?;
            write_new(
                &out_dir.join("layout.json"),
                serde_json::to_string_pretty(&result.layout)?.as_bytes(),
            )?;
            let files = exports(&job, &result.layout, &outlines, &out_dir, sheet_outline)?;
            let names = files
                .iter()
                .filter_map(|f| std::path::Path::new(f).file_name())
                .map(|f| f.to_string_lossy().into_owned())
                .collect();
            let report = nestbolt_core::project::NestReport::new(result, seconds, names);
            write_new(
                &out_dir.join("report.json"),
                serde_json::to_string_pretty(&report)?.as_bytes(),
            )?;
            println!("{}", serde_json::to_string_pretty(&report)?);
        }
        Command::Export {
            library,
            request,
            layout,
            out_dir,
            sheet_outline,
        } => {
            let library: nestbolt_core::project::Library =
                serde_json::from_slice(&fs::read(&library)?)?;
            let request: nestbolt_core::project::Request =
                serde_json::from_slice(&fs::read(&request)?)?;
            let layout: nestbolt_validator::job::Layout =
                serde_json::from_slice(&fs::read(&layout)?)?;
            let (job, outlines) = request.job(&library)?;
            let report = nestbolt_validator::job::validate(&job, &layout)?;
            ensure!(
                report.valid,
                "the layout does not satisfy the request: {:?}",
                report.violations
            );
            fs::create_dir_all(&out_dir)?;
            let files = exports(&job, &layout, &outlines, &out_dir, sheet_outline)?;
            println!(
                "{}",
                serde_json::to_string_pretty(&serde_json::json!({"files": files}))?
            );
        }
        Command::Strip {
            job,
            output,
            seed,
            seconds,
        } => {
            let job = serde_json::from_slice(&fs::read(job)?)?;
            let result = nestbolt_core::strip::optimize(
                &job,
                nestbolt_core::strip::Options { seconds, seed },
                |p| {
                    eprintln!(
                        "{}",
                        serde_json::to_string(p).expect("finite strip progress")
                    )
                },
            )?;
            ensure!(
                result.validation.valid,
                "strip result failed independent validation"
            );
            use std::io::Write;
            let mut file = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(output)?;
            file.write_all(serde_json::to_string_pretty(&result.layout)?.as_bytes())?;
            println!("{}", serde_json::to_string_pretty(&result)?);
        }
        Command::Sheets {
            job,
            output,
            seed,
            seconds,
            warm_fraction,
            compress_fraction,
            window,
            repeatable,
            time_limit,
        } => {
            let job = serde_json::from_slice(&fs::read(&job)?)?;
            let result = nestbolt_core::sheets::optimize(
                &job,
                nestbolt_core::sheets::Options {
                    seconds,
                    seed,
                    warm_fraction,
                    compress_fraction,
                    window,
                    timing: if repeatable {
                        nestbolt_core::clock::Timing::Work
                    } else {
                        nestbolt_core::clock::Timing::Wall
                    },
                    time_limit,
                },
                |p, _| {
                    eprintln!(
                        "{}",
                        serde_json::to_string(p).expect("finite sheet progress")
                    )
                },
            )?;
            println!("{}", serde_json::to_string_pretty(&result)?);
            ensure!(
                result.validation.valid,
                "sheet result failed independent validation"
            );
            use std::io::Write;
            let mut file = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(&output)?;
            file.write_all(serde_json::to_string_pretty(&result.layout)?.as_bytes())?;
        }
        Command::Compact {
            job,
            layout,
            output,
            sweeps,
            max_checks,
            relocate,
        } => {
            let job = serde_json::from_slice(&fs::read(job)?)?;
            let source = serde_json::from_slice(&fs::read(layout)?)?;
            let prepared = nestbolt_core::construct::PreparedJob::new(&job)?;
            let mut control = nestbolt_core::control::Control::new(max_checks, None);
            let construction = if relocate {
                prepared.compact_with_relocation(
                    &source,
                    sweeps,
                    nestbolt_core::construct::Options::default(),
                    &mut control,
                )?
            } else {
                prepared.compact_controlled(&source, sweeps, &mut control)?
            };
            let validation = nestbolt_validator::job::validate(&job, &construction.layout)?;
            ensure!(
                validation.valid,
                "compacted layout failed independent validation"
            );
            println!(
                "{}",
                serde_json::to_string_pretty(
                    &serde_json::json!({"construction": construction, "validation": validation})
                )?
            );
            use std::io::Write;
            let mut file = fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(output)?;
            file.write_all(serde_json::to_string_pretty(&construction.layout)?.as_bytes())?;
        }
        Command::Improve {
            job,
            output,
            seed,
            passes,
            samples,
            free_rotations,
            max_checks,
            timeout_ms,
        } => {
            let job = serde_json::from_slice(&fs::read(&job)?)?;
            use nestbolt_core::control::{Control, StopReason};
            let started = std::time::Instant::now();
            let mut deadline = || {
                timeout_ms
                    .filter(|&limit| started.elapsed().as_millis() >= u128::from(limit))
                    .map(|_| StopReason::Deadline)
            };
            let mut control = Control::new(
                max_checks,
                if timeout_ms.is_some() {
                    Some(&mut deadline)
                } else {
                    None
                },
            );
            let result = nestbolt_core::optimize::optimize_controlled(
                &job,
                nestbolt_core::optimize::Options {
                    construct: nestbolt_core::construct::Options {
                        seed,
                        random_samples: samples,
                        free_rotations,
                    },
                    passes,
                },
                &mut control,
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
