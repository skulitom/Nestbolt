//! Deterministic diagnostic placement for independent writer audits, not a
//! quality benchmark or the public nesting interface. Source XML stays intact.
use anyhow::{Context, Result};
use nestbolt_core::lightburn::{Document, UnitPlacement};
use nestbolt_validator::job::{
    Job, Layout, Margins, Mode, Part, Placement, Rotations, Sheet, Stock,
};
use nestbolt_validator::{RigidTransform, Units};
use serde_json::json;

fn main() -> Result<()> {
    let file = std::env::args()
        .nth(1)
        .context("provide a LightBurn project")?;
    let text = std::fs::read_to_string(&file)?;
    let doc = Document::read(&text, 0.0005)?;
    let nesting = match doc.nesting_units(0.0005) {
        Ok(nesting) => nesting,
        Err(error) => {
            println!(
                "{}",
                json!({"status":"unit_error", "error":format!("{error:#}")})
            );
            return Ok(());
        }
    };
    let identity: Vec<_> = nesting
        .units
        .iter()
        .map(|u| UnitPlacement {
            unit: u.id,
            transform: RigidTransform::default(),
        })
        .collect();
    let noop = nesting.write_sheet(&identity, 100.0, 100.0, false)?;
    let cell = nesting
        .units
        .iter()
        .map(|u| (u.bounds_mm[2] - u.bounds_mm[0]).max(u.bounds_mm[3] - u.bounds_mm[1]))
        .fold(1.0_f64, f64::max)
        + 10.0;
    let columns = (nesting.units.len().max(1) as f64).sqrt().ceil() as usize;
    let rows = nesting.units.len().max(1).div_ceil(columns);
    let width = cell * columns as f64;
    let height = cell * rows as f64;
    let mut files = vec![];
    let mut layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: vec![],
        placements: vec![],
    };
    for sheet in 0..2 {
        let selected: Vec<_> = nesting
            .units
            .iter()
            .filter(|u| u.id % 2 == sheet)
            .map(|u| {
                let mut transform = RigidTransform {
                    translation: [0.0, 0.0],
                    rotation_radians: (u.id % 4) as f64 * std::f64::consts::FRAC_PI_2,
                    mirrored: u.id % 3 == 1,
                };
                let affine = nestbolt_core::curves::Affine::placement(&transform);
                let points: Vec<_> = u
                    .geometry
                    .iter()
                    .flat_map(|p| p.outer.iter())
                    .map(|&p| affine.apply(p))
                    .collect();
                let bounds = nestbolt_core::curves::bounds(&points);
                transform.translation = [
                    cell * (u.id % columns) as f64 + 5.0 - bounds[0],
                    cell * (u.id / columns) as f64 + 5.0 - bounds[1],
                ];
                UnitPlacement {
                    unit: u.id,
                    transform,
                }
            })
            .collect();
        let output = nesting.write_sheet(&selected, width, height, true)?;
        if !selected.is_empty() {
            let sheet_id = format!("sheet-{sheet}");
            layout.sheets.push(Sheet {
                id: sheet_id.clone(),
                stock_id: "diagnostic".into(),
            });
            layout.placements.extend(selected.iter().map(|p| Placement {
                part_id: format!("unit-{}", p.unit),
                copy_index: 0,
                sheet_id: sheet_id.clone(),
                transform: p.transform,
            }));
        }
        files.push(json!({"sheet":sheet, "placements":selected, "xml":output}));
    }
    let job = Job {
        version: 1,
        name: "LightBurn deterministic writer audit".into(),
        units: Units::Mm,
        parts: nesting
            .units
            .iter()
            .map(|u| Part {
                id: format!("unit-{}", u.id),
                quantity: 1,
                geometry: u.geometry.clone(),
                rotations: Rotations::List {
                    degrees: vec![0.0, 90.0, 180.0, 270.0],
                },
                allow_mirror: true,
                priority: 1.0,
            })
            .collect(),
        stocks: vec![Stock {
            id: "diagnostic".into(),
            width,
            height,
            count: None,
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
        clearance: 0.001,
        edge_clearance: 0.0005,
        mode: Mode::All,
    };
    let validation = if job.parts.is_empty() {
        None
    } else {
        Some(nestbolt_validator::job::validate(&job, &layout)?)
    };
    println!(
        "{}",
        json!({"status":"written", "nesting":nesting, "identity_byte_equal":noop == text,
        "width_mm":width,"height_mm":height,"files":files,"validation":validation})
    );
    Ok(())
}
