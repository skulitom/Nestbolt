//! Shared native/browser groundwork. Inspection is not layout validation.

use std::collections::HashSet;

use anyhow::{Context, Result, ensure};
use jagua_rs::collision_detection::CDEConfig;
use jagua_rs::geometry::fail_fast::SPSurrogateConfig;
use jagua_rs::io::import::Importer;
use jagua_rs::probs::bpp::io::ext_repr::ExtBPInstance;
use serde::{Deserialize, Serialize};

pub mod construct;
pub mod control;
pub mod optimize;

/// Initial supported job size, matching the v1 target in the project plan.
pub const MAX_PARTS: u64 = 2_000;
pub const ENGINE_VERSION: &str = "jagua-rs 1.1.0";

/// Units must be declared by the caller: the upstream JSON has no unit field.
#[derive(Clone, Copy, Debug, Deserialize, Serialize, PartialEq, Eq)]
#[serde(rename_all = "snake_case")]
pub enum Units {
    Mm,
    Inch,
    Unitless,
}

#[derive(Debug, Serialize)]
pub struct Inspection {
    pub name: String,
    pub engine: &'static str,
    pub units: Units,
    pub part_types: usize,
    pub total_parts: u64,
    pub sheet_types: usize,
    pub available_sheets: u64,
    /// Original part area, including demand, in squared input units.
    pub total_part_area: f64,
    pub min_item_separation: f32,
}

/// Import an upstream jagua-rs bin-packing job and summarize its geometry.
///
/// Uses serial import explicitly so the same path works in a single browser
/// Worker without Rayon threads or SharedArrayBuffer. Zero-demand items and
/// zero-stock bins are inactive, as in upstream. Original coordinates are not
/// converted or exported. This does not solve the job, check fit, or independently
/// validate a layout. Item holes remain an explicit upstream error.
pub fn inspect_json(json: &str, units: Units) -> Result<Inspection> {
    let job: ExtBPInstance = serde_json::from_str(json).context("invalid jagua-rs BPP JSON")?;
    ensure!(!job.name.trim().is_empty(), "job name must not be empty");
    let mut ids = HashSet::new();
    ensure!(
        job.items.iter().all(|item| ids.insert(item.base.id)),
        "item IDs must be unique"
    );
    ids.clear();
    ensure!(
        job.bins.iter().all(|bin| ids.insert(bin.base.id)),
        "sheet IDs must be unique"
    );
    let total_parts = job.items.iter().try_fold(0_u64, |total, item| {
        total
            .checked_add(item.demand)
            .context("part count overflow")
    })?;
    ensure!(
        (1..=MAX_PARTS).contains(&total_parts),
        "job must request 1..={MAX_PARTS} parts"
    );
    let available_sheets = job.bins.iter().try_fold(0_u64, |total, bin| {
        // Consistent supported stock range on native and wasm32.
        ensure!(bin.stock <= u32::MAX as usize, "sheet stock exceeds u32");
        total
            .checked_add(bin.stock as u64)
            .context("sheet count overflow")
    })?;
    ensure!(available_sheets > 0, "job must have positive sheet stock");

    let config = CDEConfig {
        quadtree_depth: 5,
        cd_threshold: 96,
        item_surrogate_config: SPSurrogateConfig::none(),
    };
    let importer =
        Importer::new(config, None, None).with_min_item_separation(job.min_item_separation)?;
    let mut total_part_area = 0.0;
    let mut part_types = 0;
    for item in job.items.iter().filter(|item| item.demand > 0) {
        let imported = importer
            .import_item(&item.base, part_types)
            .with_context(|| format!("cannot import part {}", item.base.id))?;
        total_part_area += f64::from(imported.area()) * item.demand as f64;
        part_types += 1;
    }
    ensure!(total_part_area.is_finite(), "part area must be finite");
    let mut sheet_types = 0;
    for bin in job.bins.iter().filter(|bin| bin.stock > 0) {
        importer
            .import_container(&bin.base)
            .with_context(|| format!("cannot import sheet {}", bin.base.id))?;
        sheet_types += 1;
    }
    Ok(Inspection {
        name: job.name,
        engine: ENGINE_VERSION,
        units,
        part_types,
        total_parts,
        sheet_types,
        available_sheets,
        total_part_area,
        min_item_separation: job.min_item_separation,
    })
}
