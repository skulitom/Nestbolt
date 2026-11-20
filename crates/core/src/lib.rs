//! Geometry, drawing interchange and optional nesting search.

#[cfg(feature = "search")]
pub mod clock;
#[cfg(feature = "search")]
pub mod common_line;
#[cfg(feature = "search")]
pub mod construct;
#[cfg(feature = "search")]
pub mod control;
pub mod curves;
pub mod export;
#[cfg(feature = "search")]
pub mod holes;
pub mod import;
#[cfg(feature = "search")]
pub mod lead_in;
pub mod lightburn;
#[cfg(feature = "search")]
pub mod optimize;
#[cfg(feature = "search")]
pub mod project;
#[cfg(feature = "search")]
pub mod rects;
#[cfg(feature = "search")]
mod scoring;
#[cfg(feature = "search")]
pub mod separate;
#[cfg(feature = "search")]
pub mod sheets;
#[cfg(all(feature = "search", not(target_arch = "wasm32")))]
pub mod strip;

#[cfg(feature = "search")]
mod inspection;
#[cfg(feature = "search")]
pub use inspection::{ENGINE_VERSION, Inspection, MAX_PARTS, Units, inspect_json};
