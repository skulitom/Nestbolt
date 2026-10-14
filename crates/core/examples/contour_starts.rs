//! Authored H6 export-format probe. This is not a lead allowance/search gate.
use std::{collections::HashMap, fs, path::PathBuf};

use anyhow::{Context, Result, ensure};
use nestbolt_core::{
    curves::{Affine, Contour, Segment},
    export::{self, ContourStart, ReviewPaths},
    project::{Library, Request},
};
use nestbolt_validator::{
    RigidTransform, Units,
    job::{Layout, Placement, Sheet, validate},
};

fn main() -> Result<()> {
    let out = PathBuf::from(
        std::env::args()
            .nth(1)
            .context("pass a new output directory")?,
    );
    ensure!(!out.exists(), "output directory already exists");
    let source = r#"<svg xmlns="http://www.w3.org/2000/svg" width="180mm" height="80mm" viewBox="0 0 180 80">
<rect id="rectangle" x="0" y="0" width="40" height="30"/>
<circle id="circle" cx="65" cy="15" r="10"/>
<ellipse id="ellipse" cx="105" cy="15" rx="14" ry="7"/>
<path id="cubic" d="M140 30 C140 0 175 0 175 30 Z"/>
<path id="mixed" d="M0 50 L40 50 C55 55 55 70 40 75 L0 75 Z"/>
</svg>"#;
    let library = Library::import(&[("starts.svg".into(), source.into())], &Default::default())?;
    let request: Request = serde_json::from_value(
        serde_json::json!({"sheets":[{"id":"stock","width_mm":200,"height_mm":100}]}),
    )?;
    let (job, curves) = request.job(&library)?;
    let transform = RigidTransform {
        translation: [10.0, 80.0],
        rotation_radians: 0.0,
        mirrored: false,
    };
    let layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: vec![Sheet {
            id: "sheet-0".into(),
            stock_id: "stock".into(),
        }],
        placements: library
            .parts
            .iter()
            .map(|p| Placement {
                part_id: p.id.clone(),
                copy_index: 0,
                sheet_id: "sheet-0".into(),
                transform,
            })
            .collect(),
    };
    ensure!(
        validate(&job, &layout)?.valid,
        "authored probe layout is invalid"
    );
    let mut starts = HashMap::new();
    let mut review_paths = vec![];
    let mut expected = vec![];
    for part in &library.parts {
        let position = ContourStart {
            segment: 0,
            parameter: 0.37,
        };
        let moved = part.outer.transformed(&Affine::placement(&transform));
        let restarted = moved.restarted(position.segment, position.parameter)?;
        starts.insert(format!("{}#0", part.id), vec![Some(position)]);
        // A marker ending on the selected start, only for visual inspection.
        review_paths.push(Contour {
            start: [restarted.start[0], restarted.start[1] + 3.0],
            segments: vec![Segment::Line {
                to: restarted.start,
            }],
        });
        expected.push(serde_json::json!({"part_id":part.id,"source":part.source,
            "contour":moved,"segment":position.segment,"parameter":position.parameter,
            "expected_start_mm":restarted.start}));
    }
    let review = ReviewPaths {
        starts,
        leadin: review_paths,
        ..Default::default()
    };
    let options = export::Options {
        sheet_outline: false,
    };
    fs::create_dir_all(&out)?;
    fs::write(out.join("source.svg"), source)?;
    fs::write(
        out.join("ordered.svg"),
        export::svg_with_review_paths(&job, &layout, "sheet-0", &curves, options, &review)?,
    )?;
    fs::write(
        out.join("ordered.dxf"),
        export::dxf_with_review_paths(&job, &layout, "sheet-0", &curves, options, &review)?,
    )?;
    fs::write(
        out.join("original.svg"),
        export::svg(&job, &layout, "sheet-0", &curves, options)?,
    )?;
    fs::write(
        out.join("expected.json"),
        serde_json::to_vec_pretty(&serde_json::json!({
            "scope":"Authored exact start-point format probe; marker lines are not validated lead-ins",
            "held_out_read":false,"height_mm":100,"contours":expected,"job":job,"layout":layout
        }))?,
    )?;
    Ok(())
}
