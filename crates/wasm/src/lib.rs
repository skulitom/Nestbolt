//! Call from a Web Worker. No global thread pool or browser main-thread work.

use nestbolt_core::Units;
use wasm_bindgen::prelude::*;

/// Same geometry inspection as the native CLI; units are explicit.
#[wasm_bindgen]
pub fn inspect_job(json: &str, units: &str) -> Result<String, JsValue> {
    let units = match units {
        "mm" => Units::Mm,
        "inch" => Units::Inch,
        "unitless" => Units::Unitless,
        _ => return Err(JsValue::from_str("units must be mm, inch or unitless")),
    };
    let inspection = nestbolt_core::inspect_json(json, units)
        .map_err(|error| JsValue::from_str(&format!("{error:#}")))?;
    serde_json::to_string(&inspection).map_err(|error| JsValue::from_str(&error.to_string()))
}
