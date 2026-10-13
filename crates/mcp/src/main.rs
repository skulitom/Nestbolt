//! Nestbolt's stdio MCP server: five tools over the shared native core.
//!
//! Every path is confined to the workspace (the server's working directory, or
//! `NESTBOLT_WORKSPACE`). Heavy geometry lives in files; replies stay small.
//! Outputs are written to new files only, never over existing ones. `nest` uses
//! the repeatable work budget: the same library, request, budget and seed give
//! the same layout, and every result passes the independent checker.
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, ensure};
use nestbolt_core::project::{Library, Request};
use rmcp::{
    ErrorData, Peer, RoleServer, ServerHandler, ServiceExt,
    handler::server::{router::tool::ToolRouter, wrapper::Parameters},
    model::{
        CallToolResult, Implementation, ProgressNotificationParam, RequestMetaObject,
        ServerCapabilities, ServerConfig,
    },
    schemars::{self, JsonSchema},
    tool, tool_handler, tool_router,
    transport::stdio,
};
use serde::Deserialize;
use serde_json::{Value, json};

/// Largest list returned inline; longer lists are summarised.
const LIST_LIMIT: usize = 200;

#[derive(Clone)]
struct Nestbolt {
    root: PathBuf,
    tool_router: ToolRouter<Self>,
}

#[derive(Debug, Deserialize, JsonSchema)]
struct ImportParams {
    /// SVG or DXF files, relative to the workspace or absolute inside it.
    paths: Vec<String>,
    /// Where to write the part library JSON; a new file under `nestbolt/` by default.
    library_path: Option<String>,
    /// Maximum distance between exact curves and nesting polygons, in mm (default 0.005).
    tolerance_mm: Option<f64>,
    /// Millimetres per SVG user unit when a document has no absolute size (default 25.4/96).
    svg_user_unit_mm: Option<f64>,
    /// Millimetres per DXF unit when `$INSUNITS` is missing (default 1).
    dxf_unit_mm: Option<f64>,
    /// Explicitly close gaps up to this many mm (off by default, maximum 1).
    close_gaps_mm: Option<f64>,
    /// Cut layer names; omit to prefer cut/outline/profile, then all closed contours.
    layers: Option<Vec<String>>,
    /// DXF ACI numbers as strings (e.g. "7") or RGB colours (e.g. "#000000").
    colors: Option<Vec<String>>,
}

#[derive(Debug, Deserialize, JsonSchema)]
struct NestParams {
    /// A library written by `import_parts`.
    library_path: String,
    /// Parts (ids from `import_parts`, quantities, rotations), sheets and spacing, in mm.
    request: Request,
    /// Search budget in seconds, 1 to 300 (default 10). Also the hard real-time limit.
    time_budget_s: Option<f64>,
    /// Random seed (default 0). The same inputs, budget and seed repeat exactly.
    seed: Option<u64>,
    /// New output directory; `nestbolt/runs/<name>` by default.
    out_dir: Option<String>,
}

#[derive(Debug, Deserialize, JsonSchema)]
struct LayoutParams {
    library_path: String,
    request: Request,
    /// A layout JSON file, for example `layout.json` written by `nest`.
    layout_path: String,
}

#[derive(Debug, Deserialize, JsonSchema)]
struct ExportParams {
    library_path: String,
    request: Request,
    layout_path: String,
    /// New output directory for one SVG and one DXF per sheet.
    out_dir: String,
    /// Draw sheet boundaries in their own group or layer (default false).
    sheet_outline: Option<bool>,
}

#[derive(Debug, Deserialize, JsonSchema)]
struct EstimateParams {
    library_path: String,
    request: Request,
}

fn tool_error(error: anyhow::Error) -> ErrorData {
    ErrorData::invalid_params(format!("{error:#}"), None)
}

impl Nestbolt {
    fn new(root: PathBuf) -> Self {
        Self {
            root,
            tool_router: Self::tool_router(),
        }
    }

    /// Resolve a path inside the workspace; refuse anything outside it.
    fn inside(&self, path: &str) -> Result<PathBuf> {
        let joined = if Path::new(path).is_absolute() {
            PathBuf::from(path)
        } else {
            self.root.join(path)
        };
        let parent = joined.parent().context("path has no parent directory")?;
        let base = canonical(parent)
            .or_else(|_| {
                // Not-yet-created directories: check their nearest existing ancestor.
                let mut a = parent.to_path_buf();
                while !a.exists() {
                    a = a.parent().context("no existing ancestor")?.to_path_buf();
                }
                canonical(&a).map_err(anyhow::Error::from)
            })
            .with_context(|| format!("cannot resolve {path}"))?;
        ensure!(
            base.starts_with(&self.root),
            "{path} is outside the workspace {}; use a path inside it",
            self.root.display()
        );
        ensure!(
            !joined
                .components()
                .any(|c| c == std::path::Component::ParentDir),
            "{path} must not contain '..'"
        );
        Ok(joined)
    }

    fn library(&self, path: &str) -> Result<Library> {
        let path = self.inside(path)?;
        serde_json::from_slice(
            &std::fs::read(&path).with_context(|| format!("cannot read {}", path.display()))?,
        )
        .with_context(|| {
            format!(
                "{} is not a Nestbolt part library; create one with import_parts",
                path.display()
            )
        })
    }

    fn new_dir(&self, requested: Option<&str>, name: &str) -> Result<PathBuf> {
        let dir = match requested {
            Some(d) => self
                .inside(&format!("{}/x", d.trim_end_matches(['/', '\\'])))?
                .parent()
                .expect("joined")
                .to_path_buf(),
            None => self.root.join("nestbolt").join("runs").join(name),
        };
        ensure!(
            !dir.exists() || std::fs::read_dir(&dir)?.next().is_none(),
            "{} already exists and is not empty; choose a new out_dir",
            dir.display()
        );
        std::fs::create_dir_all(&dir)?;
        Ok(dir)
    }

    fn rel(&self, path: &Path) -> String {
        path.strip_prefix(&self.root)
            .unwrap_or(path)
            .display()
            .to_string()
            .replace('\\', "/")
    }

    fn write_new(path: &Path, bytes: &[u8]) -> Result<()> {
        use std::io::Write;
        std::fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(path)
            .with_context(|| format!("{} already exists", path.display()))?
            .write_all(bytes)?;
        Ok(())
    }

    fn summary(report: &nestbolt_validator::job::Report) -> Value {
        json!({
            "valid": report.valid,
            "violation_count": report.violation_count,
            "violations": report.violations.iter().take(20).map(|v| json!({"code": v.code, "message": v.message})).collect::<Vec<_>>(),
            "metrics": report.metrics,
        })
    }

    fn exports(
        &self,
        job: &nestbolt_validator::job::Job,
        layout: &nestbolt_validator::job::Layout,
        outlines: &std::collections::HashMap<String, nestbolt_core::export::Outline>,
        dir: &Path,
        sheet_outline: bool,
    ) -> Result<Vec<String>> {
        let options = nestbolt_core::export::Options { sheet_outline };
        let mut files = vec![];
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
                let path = dir.join(format!("{}.{ext}", sheet.id));
                Self::write_new(&path, text.as_bytes())?;
                files.push(self.rel(&path));
            }
        }
        Ok(files)
    }
}

#[tool_router]
impl Nestbolt {
    #[tool(
        description = "Import closed outlines from SVG or DXF files into a part library (mm). \
        Writes the library to a file and returns part ids, areas, bounds and import warnings. \
        Use the ids in nest requests."
    )]
    async fn import_parts(
        &self,
        Parameters(p): Parameters<ImportParams>,
    ) -> Result<CallToolResult, ErrorData> {
        (|| -> Result<CallToolResult> {
            ensure!(!p.paths.is_empty(), "give at least one SVG or DXF path");
            let mut options = nestbolt_core::import::Options {
                close_gaps_mm: p.close_gaps_mm,
                layers: p.layers,
                colors: p.colors,
                ..Default::default()
            };
            if let Some(t) = p.tolerance_mm {
                ensure!(t > 0.0 && t <= 1.0, "tolerance_mm must be in (0, 1]");
                options.tolerance = t;
            }
            if let Some(u) = p.svg_user_unit_mm {
                options.svg_user_unit = u;
            }
            if let Some(u) = p.dxf_unit_mm {
                options.dxf_unit = u;
            }
            let mut files = vec![];
            for path in &p.paths {
                let full = self.inside(path)?;
                let name = full
                    .file_name()
                    .and_then(|n| n.to_str())
                    .context("file name")?
                    .to_owned();
                files.push((
                    name,
                    std::fs::read_to_string(&full)
                        .with_context(|| format!("cannot read {path}"))?,
                ));
            }
            let library = Library::import(&files, &options)?;
            let out = match &p.library_path {
                Some(l) => self.inside(l)?,
                None => {
                    let dir = self.root.join("nestbolt");
                    std::fs::create_dir_all(&dir)?;
                    let stem = files[0]
                        .0
                        .rsplit_once('.')
                        .map_or(files[0].0.as_str(), |(s, _)| s);
                    (1..)
                        .map(|i| dir.join(format!("{stem}-library-{i}.json")))
                        .find(|f| !f.exists())
                        .expect("a free name")
                }
            };
            Self::write_new(&out, serde_json::to_string(&library)?.as_bytes())?;
            let parts: Vec<Value> = library
                .parts
                .iter()
                .take(LIST_LIMIT)
                .map(|q| {
                    json!({"id": q.id, "source": q.source, "area_mm2": q.area_mm2,
                    "bounds_mm": q.bounds_mm, "holes": q.holes.len()})
                })
                .collect();
            Ok(CallToolResult::structured(json!({
                "library_path": self.rel(&out),
                "part_count": library.parts.len(),
                "parts": parts,
                "parts_truncated": library.parts.len() > LIST_LIMIT,
                "warnings": library.warnings.iter().take(50).collect::<Vec<_>>(),
                "imports": library.imports,
            })))
        })()
        .map_err(tool_error)
    }

    #[tool(
        description = "Nest library parts on fixed sheets with a repeatable budget \
        (time_budget_s, at most 300). Writes job.json, layout.json, report.json and one SVG and \
        DXF per sheet; returns the independently checked metrics. Sends progress notifications."
    )]
    async fn nest(
        &self,
        meta: RequestMetaObject,
        client: Peer<RoleServer>,
        Parameters(p): Parameters<NestParams>,
    ) -> Result<CallToolResult, ErrorData> {
        let budget = p.time_budget_s.unwrap_or(10.0);
        if !(1.0..=300.0).contains(&budget) {
            return Err(tool_error(anyhow::anyhow!(
                "time_budget_s must be between 1 and 300"
            )));
        }
        let seed = p.seed.unwrap_or(0);
        let library = self.library(&p.library_path).map_err(tool_error)?;
        let (job, outlines) = p.request.job(&library).map_err(tool_error)?;
        let stamp = format!(
            "{}-seed{seed}",
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .map_or(0, |d| d.as_secs())
        );
        let dir = self
            .new_dir(p.out_dir.as_deref(), &stamp)
            .map_err(tool_error)?;
        let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<(f64, f64)>();
        let solve_job = job.clone();
        let handle = tokio::task::spawn_blocking(move || {
            nestbolt_core::sheets::optimize(
                &solve_job,
                nestbolt_core::sheets::Options {
                    seconds: budget,
                    seed,
                    timing: nestbolt_core::clock::Timing::Work,
                    ..Default::default()
                },
                |progress, _| {
                    let _ = tx.send((progress.elapsed_seconds, progress.material));
                },
            )
        });
        let token = meta.get_progress_token();
        while let Some((at, material)) = rx.recv().await {
            if let Some(token) = &token {
                let _ = client
                    .notify_progress(
                        ProgressNotificationParam::new(token.clone(), at.min(budget))
                            .with_total(budget)
                            .with_message(format!("material {material:.4} sheets")),
                    )
                    .await;
            }
        }
        let result = handle
            .await
            .map_err(|e| tool_error(anyhow::anyhow!("search task failed: {e}")))?
            .map_err(tool_error)?;
        (|| -> Result<CallToolResult> {
            ensure!(
                result.validation.valid,
                "the result failed independent validation"
            );
            Self::write_new(
                &dir.join("job.json"),
                serde_json::to_string_pretty(&job)?.as_bytes(),
            )?;
            Self::write_new(
                &dir.join("layout.json"),
                serde_json::to_string_pretty(&result.layout)?.as_bytes(),
            )?;
            let files = self.exports(&job, &result.layout, &outlines, &dir, false)?;
            let names = files
                .iter()
                .map(|f| f.rsplit('/').next().unwrap_or(f).to_owned())
                .collect();
            let repeatable = result.repeatable;
            let report = nestbolt_core::project::NestReport::new(result, budget, names);
            Self::write_new(
                &dir.join("report.json"),
                serde_json::to_string_pretty(&report)?.as_bytes(),
            )?;
            let mut reply = serde_json::to_value(&report)?;
            reply["validation"] = Self::summary(&report.validation);
            reply["out_dir"] = json!(self.rel(&dir));
            reply["layout_path"] = json!(self.rel(&dir.join("layout.json")));
            reply["files"] = json!(files);
            if !repeatable {
                reply["note"] = json!(
                    "the real-time limit was reached before the work budget; a larger \
                    time_budget_s makes the result repeatable"
                );
            }
            Ok(CallToolResult::structured(reply))
        })()
        .map_err(tool_error)
    }

    #[tool(
        description = "Check a layout file against the library parts, sheets and spacing of a \
        request with the independent validator; returns validity, violations and material metrics."
    )]
    async fn validate_layout(
        &self,
        Parameters(p): Parameters<LayoutParams>,
    ) -> Result<CallToolResult, ErrorData> {
        (|| -> Result<CallToolResult> {
            let library = self.library(&p.library_path)?;
            let (job, _) = p.request.job(&library)?;
            let path = self.inside(&p.layout_path)?;
            let layout: nestbolt_validator::job::Layout =
                serde_json::from_slice(&std::fs::read(&path)?).context("invalid layout JSON")?;
            let report = nestbolt_validator::job::validate(&job, &layout)?;
            Ok(CallToolResult::structured(Self::summary(&report)))
        })()
        .map_err(tool_error)
    }

    #[tool(
        description = "Write one SVG and one DXF per sheet for a valid layout, transforming \
        the original curves (arcs and splines stay curves). Refuses invalid layouts."
    )]
    async fn export_layout(
        &self,
        Parameters(p): Parameters<ExportParams>,
    ) -> Result<CallToolResult, ErrorData> {
        (|| -> Result<CallToolResult> {
            let library = self.library(&p.library_path)?;
            let (job, outlines) = p.request.job(&library)?;
            let layout: nestbolt_validator::job::Layout =
                serde_json::from_slice(&std::fs::read(self.inside(&p.layout_path)?)?)
                    .context("invalid layout JSON")?;
            let report = nestbolt_validator::job::validate(&job, &layout)?;
            ensure!(
                report.valid,
                "the layout does not satisfy the request; run validate_layout for details"
            );
            let dir = self.new_dir(Some(&p.out_dir), "export")?;
            let files = self.exports(
                &job,
                &layout,
                &outlines,
                &dir,
                p.sheet_outline.unwrap_or(false),
            )?;
            Ok(CallToolResult::structured(json!({"files": files})))
        })()
        .map_err(tool_error)
    }

    #[tool(
        description = "A fast lower bound on sheets for planning and quotes: net part area \
        divided by usable sheet area. Necessary, not sufficient: real layouts can need more \
        sheets. Also flags parts that fit no sheet in any allowed rotation."
    )]
    async fn estimate_sheets(
        &self,
        Parameters(p): Parameters<EstimateParams>,
    ) -> Result<CallToolResult, ErrorData> {
        (|| -> Result<CallToolResult> {
            let library = self.library(&p.library_path)?;
            let (job, _) = p.request.job(&library)?;
            let area: f64 = job
                .parts
                .iter()
                .map(|part| {
                    part.quantity as f64 * nestbolt_core::curves::polygon_area(&part.geometry[0])
                })
                .sum();
            let usable = |s: &nestbolt_validator::job::Stock| {
                (s.width - s.margins.left - s.margins.right).max(0.0)
                    * (s.height - s.margins.bottom - s.margins.top).max(0.0)
            };
            let largest = job.stocks.iter().map(usable).fold(0.0, f64::max);
            ensure!(largest > 0.0, "no sheet has usable area after margins");
            let oversized: Vec<&str> = job
                .parts
                .iter()
                .filter(|part| {
                    !job.stocks
                        .iter()
                        .any(|s| nestbolt_core::curves::fits_somehow(part, s))
                })
                .map(|part| part.id.as_str())
                .collect();
            Ok(CallToolResult::structured(json!({
                "net_part_area_mm2": area,
                "largest_usable_sheet_mm2": largest,
                "sheets_lower_bound": (area / largest - 1e-9).ceil().max(1.0),
                "kind": "necessary lower bound, not a layout or feasibility guarantee",
                "parts_fitting_no_sheet": oversized,
            })))
        })()
        .map_err(tool_error)
    }
}

#[tool_handler(router = self.tool_router)]
impl ServerHandler for Nestbolt {
    fn get_info(&self) -> ServerConfig {
        ServerConfig::new(ServerCapabilities::builder().enable_tools().build())
            .with_server_info(Implementation::new("nestbolt", env!("CARGO_PKG_VERSION")))
            .with_instructions(format!(
                "Nestbolt nests parts on fixed sheets for laser, CNC and fabric cutting. \
                 1) import_parts with SVG/DXF paths inside the workspace ({}). \
                 2) nest with the library_path, a request (parts by id with quantities, sheets in mm, \
                 spacing_mm) and time_budget_s. 3) Use the returned SVG/DXF files. validate_layout and \
                 export_layout work on layout files; estimate_sheets gives a lower bound only. \
                 Lengths are millimetres. Results always pass an independent geometry check.",
                self.root.display()
            ))
    }
}

/// `fs::canonicalize` without Windows' verbatim prefix on drive paths, so joined
/// relative paths with `/` still resolve and messages stay readable.
fn canonical(path: &Path) -> std::io::Result<PathBuf> {
    let full = std::fs::canonicalize(path)?;
    let text = full.to_string_lossy();
    Ok(match text.strip_prefix(r"\\?\") {
        Some(rest) if rest.as_bytes().get(1) == Some(&b':') => PathBuf::from(rest),
        _ => full.clone(),
    })
}

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<()> {
    // stdout belongs exclusively to the MCP transport. Errors go to stderr.
    let root = match std::env::var_os("NESTBOLT_WORKSPACE") {
        Some(r) => PathBuf::from(r),
        None => std::env::current_dir()?,
    };
    let root = canonical(&root).context("workspace directory")?;
    let service = Nestbolt::new(root).serve(stdio()).await?;
    service.waiting().await?;
    Ok(())
}
