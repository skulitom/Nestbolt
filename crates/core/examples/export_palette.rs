//! Reproducible native colour-check coupon; not a common-line or lead generator.
use anyhow::{Context, Result, ensure};
use nestbolt_core::{
    curves::{Contour, Segment},
    export::{self, Options, ReviewPaths},
    project::{Library, Request},
};
use nestbolt_validator::{
    RigidTransform, Units,
    job::{Layout, Placement, Sheet, validate},
};
use std::{fs, path::PathBuf};

fn main() -> Result<()> {
    let out = PathBuf::from(
        std::env::args()
            .nth(1)
            .context("pass a new output directory")?,
    );
    ensure!(!out.exists(), "output directory already exists");
    let library = Library::import(&[("coupon.svg".into(),
        r#"<svg width="50mm" viewBox="0 0 50 50"><rect width="20" height="10"/><circle cx="5" cy="5" r="1"/></svg>"#.into())], &Default::default())?;
    let request: Request = serde_json::from_value(
        serde_json::json!({"sheets":[{"id":"stock","width_mm":100,"height_mm":70}]}),
    )?;
    let (job, curves) = request.job(&library)?;
    let layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: vec![Sheet {
            id: "sheet-0".into(),
            stock_id: "stock".into(),
        }],
        placements: vec![Placement {
            part_id: library.parts[0].id.clone(),
            copy_index: 0,
            sheet_id: "sheet-0".into(),
            transform: RigidTransform {
                translation: [10.0, 20.0],
                rotation_radians: 0.0,
                mirrored: false,
            },
        }],
    };
    ensure!(validate(&job, &layout)?.valid, "invalid coupon layout");
    let rectangle = |x: f64| Contour {
        start: [x, 10.0],
        segments: vec![
            Segment::Line {
                to: [x + 20.0, 10.0],
            },
            Segment::Line {
                to: [x + 20.0, 20.0],
            },
            Segment::Line { to: [x, 20.0] },
            Segment::Line { to: [x, 10.0] },
        ],
    };
    let review = ReviewPaths {
        common: vec![rectangle(40.0)],
        leadin: vec![rectangle(70.0)],
    };
    let options = Options {
        sheet_outline: true,
    };
    let svg = export::svg_with_review_paths(&job, &layout, "sheet-0", &curves, options, &review)?;
    let dxf = export::dxf_with_review_paths(&job, &layout, "sheet-0", &curves, options, &review)?;
    fs::create_dir_all(&out)?;
    fs::write(out.join("palette.svg"), svg)?;
    fs::write(out.join("palette.dxf"), dxf)?;
    fs::write(
        out.join("expected.json"),
        serde_json::to_vec_pretty(&serde_json::json!({
            "purpose":"Palette coupon only: COMMON/LEADIN rectangles are authored review geometry, not generated machining paths",
            "sheet_mm":[100,70],"all_cuts_bounds_mm":[10,10,90,20],
            "layers":{"CUT":{"lightburn":"00","rgb":"#000000","aci":7},"COMMON":{"lightburn":"01","rgb":"#0000ff","aci":5},
                      "LEADIN":{"lightburn":"02","rgb":"#ff0000","aci":1},"SHEET":{"lightburn":"T1","rgb":"#f36926","aci":30}},
            "lightburn_setting":"Allow Importing to Tool Layers must be enabled for T1"
        }))?,
    )?;
    Ok(())
}
