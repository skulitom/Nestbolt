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
    #[derive(serde::Deserialize)]
    struct File {
        name: String,
        text: String,
    }
    let files: Vec<File> = parse(files_json, "file list")?;
    let mut options = nestbolt_core::import::Options::default();
    if tolerance_mm > 0.0 {
        options.tolerance = tolerance_mm;
    }
    if svg_user_unit_mm > 0.0 {
        options.svg_user_unit = svg_user_unit_mm;
    }
    let files: Vec<(String, String)> = files.into_iter().map(|f| (f.name, f.text)).collect();
    let library = Library::import(&files, &options).map_err(|e| fail(format!("{e:#}")))?;
    serde_json::to_string(&library).map_err(fail)
}

/// Nest with a wall-clock (`repeatable = false`) or work budget. `progress` is
/// called with `(seconds, material)` whenever a better layout is checked.
#[wasm_bindgen]
pub fn nest(
    library_json: &str,
    request_json: &str,
    seconds: f64,
    seed: u32,
    repeatable: bool,
    progress: &js_sys::Function,
) -> Result<String, JsValue> {
    let library: Library = parse(library_json, "library")?;
    let request: Request = parse(request_json, "request")?;
    let (job, _) = request.job(&library).map_err(|e| fail(format!("{e:#}")))?;
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
        |p| {
            let _ = progress.call2(
                &JsValue::NULL,
                &JsValue::from_f64(p.elapsed_seconds),
                &JsValue::from_f64(p.material),
            );
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
