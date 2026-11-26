//! Geometry, drawing interchange, remnant extraction, job quoting and optional nesting search.
//!
//! Applications that only need drawing import/export, remnant extraction, or
//! job quoting can depend on `nestbolt-core` with `default-features = false`
//! to skip the nesting engines (`jagua-rs` and `sparrow`).
//!
//! # Example
//!
//! Compute exact curve length (without polygon flattening) and validate a
//! pricing configuration:
//!
//! ```
//! use nestbolt_core::curves::{Contour, Segment};
//! use nestbolt_core::quote::Pricing;
//!
//! let circle = Contour {
//!     start: [10.0, 0.0],
//!     segments: vec![Segment::Arc {
//!         center: [0.0, 0.0],
//!         radii: [10.0, 10.0],
//!         rotation: 0.0,
//!         start: 0.0,
//!         sweep: std::f64::consts::TAU,
//!     }],
//! };
//! assert!((circle.length() - 20.0 * std::f64::consts::PI).abs() < 1e-6);
//!
//! let pricing = Pricing {
//!     sheet_cost: Some(25.0),
//!     cut_speed_mm_per_min: Some(1200.0),
//!     machine_rate_per_hour: Some(60.0),
//!     ..Pricing::default()
//! };
//! assert!(pricing.validate().is_ok());
//! ```

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
#[cfg(not(target_arch = "wasm32"))]
pub mod lightburn_api;
pub mod offcut;
#[cfg(feature = "search")]
pub mod optimize;
#[cfg(feature = "search")]
pub mod project;
pub mod quote;
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
