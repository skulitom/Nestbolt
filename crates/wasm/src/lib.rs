//! WebAssembly entry points for the browser app. Call them from a Web Worker:
//! `nest` runs for its whole budget on the calling thread. Inputs and outputs
//! are JSON strings; errors are thrown as JavaScript strings that say what to fix.
use std::collections::HashMap;

use nestbolt_core::{
    Units,
    project::{Library, Request},
};
use wasm_bindgen::prelude::*;

fn fail(error: impl std::fmt::Display) -> JsValue {
    JsValue::from_str(&error.to_string())
}

fn parse<T: serde::de::DeserializeOwned>(json: &str, what: &str) -> Result<T, JsValue> {
    serde_json::from_str(json).map_err(|e| fail(format!("invalid {what}: {e}")))
}

/// Same geometry inspection as the native CLI; units are explicit.
#[wasm_bindgen]
pub fn inspect_job(json: &str, units: &str) -> Result<String, JsValue> {
    let units = match units {
        "mm" => Units::Mm,
        "inch" => Units::Inch,
        "unitless" => Units::Unitless,
        _ => return Err(fail("units must be mm, inch or unitless")),
    };
    let inspection =
        nestbolt_core::inspect_json(json, units).map_err(|e| fail(format!("{e:#}")))?;
    serde_json::to_string(&inspection).map_err(fail)
}

/// Import files given as `[{"name": "a.svg", "text": "..."}]` into a library.
#[wasm_bindgen]
pub fn import_files(
    files_json: &str,
    tolerance_mm: f64,
    svg_user_unit_mm: f64,
) -> Result<String, JsValue> {
    let mut options = nestbolt_core::import::Options::default();
    if tolerance_mm > 0.0 {
        options.tolerance = tolerance_mm;
    }
    if svg_user_unit_mm > 0.0 {
        options.svg_user_unit = svg_user_unit_mm;
    }
    import_with_options(files_json, options)
}

/// Structured options shared with the native importer. The legacy entry point
/// remains available for existing integrations and published benchmark runners.
#[wasm_bindgen]
pub fn import_files_with_options(files_json: &str, options_json: &str) -> Result<String, JsValue> {
    import_with_options(files_json, parse(options_json, "import options")?)
}

/// Decode file bytes using the same DXF/XML rules as the native tools.
#[wasm_bindgen]
pub fn decode_drawing(name: &str, bytes: &[u8]) -> Result<String, JsValue> {
    nestbolt_core::import::decode_drawing(name, bytes).map_err(|e| fail(format!("{name}: {e:#}")))
}

/// Show layer/colour choices even when a drawing has no closed selected outline.
#[wasm_bindgen]
pub fn inspect_files(files_json: &str, options_json: &str) -> Result<String, JsValue> {
    #[derive(serde::Deserialize)]
    struct File {
        name: String,
        text: String,
    }
    let files: Vec<File> = parse(files_json, "file list")?;
    let options = parse(options_json, "import options")?;
    let mut reports = vec![];
    for file in files {
        let lower = file.name.to_ascii_lowercase();
        let report = if lower.ends_with(".svg") {
            nestbolt_core::import::inspect_svg(&file.text, &options)
        } else if lower.ends_with(".dxf") {
            nestbolt_core::import::inspect_dxf(&file.text, &options)
        } else {
            return Err(fail("choose an SVG or DXF drawing"));
        }
        .map_err(|e| fail(format!("{}: {e:#}", file.name)))?;
        reports.push(nestbolt_core::project::FileImportReport {
            file: file.name,
            report,
        });
    }
    serde_json::to_string(&reports).map_err(fail)
}

fn import_with_options(
    files_json: &str,
    options: nestbolt_core::import::Options,
) -> Result<String, JsValue> {
    #[derive(serde::Deserialize)]
    struct File {
        name: String,
        text: String,
    }
    let files: Vec<File> = parse(files_json, "file list")?;
    let files: Vec<(String, String)> = files.into_iter().map(|f| (f.name, f.text)).collect();
    let library = Library::import(&files, &options).map_err(|e| fail(format!("{e:#}")))?;
    serde_json::to_string(&library).map_err(fail)
}

/// Nest with a wall-clock (`repeatable = false`) or work budget. `progress` is
/// called with `(seconds, material)` whenever a better layout is checked, and
/// with that layout's JSON as a third argument at most once per
/// `live_interval_s` seconds when it is positive (for a live preview; the
/// search already pauses to check every improvement, so this costs one
/// serialisation per shown layout).
#[wasm_bindgen]
pub fn nest(
    library_json: &str,
    request_json: &str,
    seconds: f64,
    seed: u32,
    repeatable: bool,
    live_interval_s: f64,
    progress: &js_sys::Function,
) -> Result<String, JsValue> {
    let library: Library = parse(library_json, "library")?;
    let request: Request = parse(request_json, "request")?;
    let (job, _) = request.job(&library).map_err(|e| fail(format!("{e:#}")))?;
    let mut shown = f64::NEG_INFINITY;
    let result = nestbolt_core::sheets::optimize(
        &job,
        nestbolt_core::sheets::Options {
            seconds,
            seed: u64::from(seed),
            timing: if repeatable {
                nestbolt_core::clock::Timing::Work
            } else {
                nestbolt_core::clock::Timing::Wall
            },
            ..Default::default()
        },
        |p, layout| {
            let live = (live_interval_s > 0.0 && p.elapsed_seconds - shown >= live_interval_s)
                .then(layout)
                .flatten()
                .and_then(|l| serde_json::to_string(&l).ok());
            let (t, m) = (
                JsValue::from_f64(p.elapsed_seconds),
                JsValue::from_f64(p.material),
            );
            let _ = match live {
                Some(json) => {
                    shown = p.elapsed_seconds;
                    progress.call3(&JsValue::NULL, &t, &m, &JsValue::from_str(&json))
                }
                None => progress.call2(&JsValue::NULL, &t, &m),
            };
        },
    )
    .map_err(|e| fail(format!("{e:#}")))?;
    serde_json::to_string(&serde_json::json!({
        "layout": result.layout,
        "validation": result.validation,
        "seed": seed,
        "seconds": seconds,
        "repeatable": result.repeatable,
        "parts_in_holes": result.riders,
        "elapsed_seconds": result.elapsed_seconds,
    }))
    .map_err(fail)
}

/// Benchmark entry: the same search as `nestbolt sheets` on a polygon job
/// (validator job JSON), with default search options. Returns the full sheet
/// result, so browser and native runs are scored identically.
#[wasm_bindgen]
pub fn nest_job(
    job_json: &str,
    seconds: f64,
    seed: u32,
    repeatable: bool,
    progress: &js_sys::Function,
) -> Result<String, JsValue> {
    let job: nestbolt_validator::job::Job = parse(job_json, "job")?;
    let result = nestbolt_core::sheets::optimize(
        &job,
        nestbolt_core::sheets::Options {
            seconds,
            seed: u64::from(seed),
            timing: if repeatable {
                nestbolt_core::clock::Timing::Work
            } else {
                nestbolt_core::clock::Timing::Wall
            },
            ..Default::default()
        },
        |p, _| {
            let _ = progress.call2(
                &JsValue::NULL,
                &JsValue::from_f64(p.elapsed_seconds),
                &JsValue::from_f64(p.material),
            );
        },
    )
    .map_err(|e| fail(format!("{e:#}")))?;
    serde_json::to_string(&result).map_err(fail)
}

/// Bytes of WebAssembly linear memory this engine instance has reserved.
#[wasm_bindgen]
pub fn memory_bytes() -> f64 {
    #[cfg(target_arch = "wasm32")]
    return (core::arch::wasm32::memory_size(0) * 65536) as f64;
    #[cfg(not(target_arch = "wasm32"))]
    0.0
}

/// Independent check of a layout against a request.
#[wasm_bindgen]
pub fn validate(
    library_json: &str,
    request_json: &str,
    layout_json: &str,
) -> Result<String, JsValue> {
    let library: Library = parse(library_json, "library")?;
    let request: Request = parse(request_json, "request")?;
    let layout: nestbolt_validator::job::Layout = parse(layout_json, "layout")?;
    let (job, _) = request.job(&library).map_err(|e| fail(format!("{e:#}")))?;
    let report =
        nestbolt_validator::job::validate(&job, &layout).map_err(|e| fail(format!("{e:#}")))?;
    serde_json::to_string(&report).map_err(fail)
}

/// One sheet of a valid layout as `"svg"` or `"dxf"` text.
#[wasm_bindgen]
pub fn export_sheet(
    library_json: &str,
    request_json: &str,
    layout_json: &str,
    sheet_id: &str,
    format: &str,
    sheet_outline: bool,
) -> Result<String, JsValue> {
    let library: Library = parse(library_json, "library")?;
    let request: Request = parse(request_json, "request")?;
    let layout: nestbolt_validator::job::Layout = parse(layout_json, "layout")?;
    let (job, outlines): (_, HashMap<_, _>) =
        request.job(&library).map_err(|e| fail(format!("{e:#}")))?;
    let options = nestbolt_core::export::Options { sheet_outline };
    match format {
        "svg" => nestbolt_core::export::svg(&job, &layout, sheet_id, &outlines, options),
        "dxf" => nestbolt_core::export::dxf(&job, &layout, sheet_id, &outlines, options),
        _ => return Err(fail("format must be svg or dxf")),
    }
    .map_err(|e| fail(format!("{e:#}")))
}

/// Net part area over usable sheet area: a necessary lower bound only.
#[wasm_bindgen]
pub fn estimate_sheets(library_json: &str, request_json: &str) -> Result<String, JsValue> {
    let library: Library = parse(library_json, "library")?;
    let request: Request = parse(request_json, "request")?;
    let (job, _) = request.job(&library).map_err(|e| fail(format!("{e:#}")))?;
    let area: f64 = job
        .parts
        .iter()
        .map(|p| p.quantity as f64 * nestbolt_core::curves::polygon_area(&p.geometry[0]))
        .sum();
    let largest = job
        .stocks
        .iter()
        .map(|s| {
            (s.width - s.margins.left - s.margins.right).max(0.0)
                * (s.height - s.margins.bottom - s.margins.top).max(0.0)
        })
        .fold(0.0, f64::max);
    if largest <= 0.0 {
        return Err(fail("no sheet has usable area after margins"));
    }
    serde_json::to_string(&serde_json::json!({
        "net_part_area_mm2": area,
        "sheets_lower_bound": (area / largest - 1e-9).ceil().max(1.0),
        "kind": "necessary lower bound, not a layout",
    }))
    .map_err(fail)
}
