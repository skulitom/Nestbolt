//! Authored, searched lead coupons for native verification. No corpus inputs.
use std::{collections::HashMap, fs, path::PathBuf};

use anyhow::{Context, Result, ensure};
use nestbolt_core::{
    clock::Timing,
    curves::Affine,
    export,
    lead_in::{self, Options, Style},
    project::{Library, Request},
    sheets,
};
use nestbolt_validator::{job, leads};

fn main() -> Result<()> {
    let out = PathBuf::from(
        std::env::args()
            .nth(1)
            .context("pass a new output directory")?,
    );
    ensure!(!out.exists(), "output directory already exists");
    fs::create_dir_all(&out)?;
    let panel = r#"<svg xmlns="http://www.w3.org/2000/svg" width="24mm" height="16mm" viewBox="0 0 24 16"><path d="M0 0 H24 V16 H0 Z M8 5 H16 V11 H8 Z"/></svg>"#;
    let ring = r#"<svg xmlns="http://www.w3.org/2000/svg" width="18mm" height="18mm" viewBox="0 0 18 18"><circle cx="9" cy="9" r="9"/><circle cx="9" cy="9" r="5"/></svg>"#;
    for (name, source, style, angle) in [
        ("line45", panel, Style::Line, 45.0),
        ("arc45", ring, Style::Arc, 45.0),
        ("arc90", panel, Style::Arc, 90.0),
    ] {
        let library = Library::import(
            &[(format!("{name}.svg"), source.into())],
            &Default::default(),
        )?;
        ensure!(
            library.parts.len() == 1,
            "coupon must have exactly one part"
        );
        let request: Request = serde_json::from_value(serde_json::json!({
            "parts":[{"id":library.parts[0].id,"quantity":4}],
            "sheets":[{"id":"stock","width_mm":65,"height_mm":50,"count":1}],
            "spacing_mm":0.2,"edge_spacing_mm":1.0
        }))?;
        let (job, curves) = request.job(&library)?;
        let options = Options {
            kerf_mm: 0.2,
            length_mm: 3.0,
            style,
            outer_angle_degrees: angle,
            hole_angle_degrees: angle,
        };
        let plan = lead_in::prepare(&job, &curves, options, &HashMap::new())?;
        ensure!(
            plan.parts.iter().all(|p| p.flags.is_empty()),
            "coupon has an unreserved contour"
        );
        ensure!(
            plan.parts
                .iter()
                .flat_map(|p| &p.reservations)
                .all(|r| !r.shortened),
            "coupon shortened a lead"
        );
        let result = sheets::optimize_with_part_in_hole(
            &plan.collision_job,
            sheets::Options {
                seconds: 1.0,
                time_limit: Some(30.0),
                timing: Timing::Work,
                ..Default::default()
            },
            false,
            |_, _| {},
        )?;
        ensure!(result.validation.valid, "invalid collision layout");
        let layout = &result.layout;
        ensure!(
            layout.placements.len() == 4 && layout.sheets.len() == 1,
            "coupon did not fit one sheet"
        );
        let original_validation = job::validate(&job, layout)?;
        let allowances = plan.allowances(layout)?;
        let lead_validation = leads::validate(&job, layout, &allowances)?;
        ensure!(
            original_validation.valid && lead_validation.valid,
            "independent validation failed"
        );
        let sheet_id = &layout.sheets[0].id;
        let review = plan.review(layout, sheet_id)?;
        let export_options = export::Options {
            sheet_outline: true,
        };
        let mut expected = vec![];
        for placement in &layout.placements {
            let original = &curves[&placement.part_id];
            let starts = &review.starts[&format!("{}#{}", placement.part_id, placement.copy_index)];
            for (index, c) in std::iter::once(&original.outer)
                .chain(&original.holes)
                .enumerate()
            {
                let start = starts[index].context("coupon start is missing")?;
                let transformed = c.transformed(&Affine::placement(&placement.transform));
                let restarted = transformed.restarted(start.segment, start.parameter)?;
                expected.push(serde_json::json!({
                    "part_id":placement.part_id,"copy_index":placement.copy_index,
                    "contour_index":index,"contour":restarted,
                    "attachment_mm":restarted.start
                }));
            }
        }
        fs::write(out.join(format!("{name}-source.svg")), source)?;
        fs::write(
            out.join(format!("{name}.svg")),
            export::svg_with_review_paths(
                &job,
                layout,
                sheet_id,
                &curves,
                export_options,
                &review,
            )?,
        )?;
        fs::write(
            out.join(format!("{name}.dxf")),
            export::dxf_with_review_paths(
                &job,
                layout,
                sheet_id,
                &curves,
                export_options,
                &review,
            )?,
        )?;
        fs::write(
            out.join(format!("{name}.json")),
            serde_json::to_vec_pretty(&serde_json::json!({
                "scope":"Authored searched coupon; native observation and public-surface checks still required",
                "held_out_read":false,"options":options,"parts":plan.parts,"allowances":allowances,
                "job":job,"collision_job":plan.collision_job,"layout":layout,
                "original_validation":original_validation,"lead_validation":lead_validation,
                "expected_contours":expected,"seconds":1.0,"timing":"work","time_limit":30.0,"seed":0
            }))?,
        )?;
    }
    Ok(())
}
