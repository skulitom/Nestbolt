//! End-to-end shop CAD torture tests covering real-world DXF/SVG quirks
//! (units, negative extrusion, nested MINSERT + paper space, duplicate/gap
//! cleanup, SVG physical lengths) through closed-loop remnant nesting and quoting.
use nestbolt_core::{
    import::{Options as ImportOptions, decode_drawing, import_dxf, import_svg},
    offcut::{OffcutMode, Options as OffcutOptions, extract},
    project::{Library, Request, SheetImport},
    quote::{Pricing, from_cutting_report},
    sheets::{Options as SheetOptions, optimize},
};
use nestbolt_validator::job::validate;

#[test]
fn dxf_insunits_inches_cm_and_mm_scale_to_exact_millimetres() {
    let make_square = |insunits: i32, size: f64| {
        format!(
            "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n{insunits}\n0\nENDSEC\n\
             0\nSECTION\n2\nENTITIES\n\
             0\nLWPOLYLINE\n8\nCUT\n90\n4\n70\n1\n\
             10\n0\n20\n0\n10\n{size}\n20\n0\n10\n{size}\n20\n{size}\n10\n0\n20\n{size}\n\
             0\nENDSEC\n0\nEOF\n"
        )
    };
    // 1 = inches (2 in = 50.8 mm), 4 = mm (50 mm), 5 = cm (5 cm = 50 mm), 6 = m (0.05 m = 50 mm).
    for (code, dim, expected_mm) in [
        (1, 2.0, 50.8),
        (4, 50.0, 50.0),
        (5, 5.0, 50.0),
        (6, 0.05, 50.0),
    ] {
        let imported = import_dxf(&make_square(code, dim), &ImportOptions::default()).unwrap();
        assert_eq!(imported.parts.len(), 1);
        let [x0, y0, x1, y1] = imported.parts[0].bounds;
        assert!(
            ((x1 - x0) - expected_mm).abs() < 1e-4,
            "code={code} w={}",
            x1 - x0
        );
        assert!(
            ((y1 - y0) - expected_mm).abs() < 1e-4,
            "code={code} h={}",
            y1 - y0
        );
    }
}

#[test]
fn messy_dxf_with_duplicates_gap_repair_paper_space_and_minsert_imports_cleanly() {
    // Combines four classic shop DXF headaches in one file:
    // 1. A 2x1 MINSERT grid of 40x30 brackets in model space (2 parts)
    // 2. A paper-space INSERT (67=1) that must NOT become a part
    // 3. A closed rectangle with duplicate line segments + a 0.08 mm gap repaired by close_gaps_mm
    let dxf = "\
0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n\
0\nSECTION\n2\nBLOCKS\n\
0\nBLOCK\n8\n0\n2\nBRACKET\n70\n0\n10\n0\n20\n0\n30\n0\n\
0\nLWPOLYLINE\n8\nCUT\n90\n4\n70\n1\n10\n0\n20\n0\n10\n40\n20\n0\n10\n40\n20\n30\n10\n0\n20\n30\n\
0\nENDBLK\n\
0\nBLOCK\n8\n0\n2\nTITLEBLOCK\n70\n0\n10\n0\n20\n0\n30\n0\n\
0\nLWPOLYLINE\n8\nCUT\n90\n4\n70\n1\n10\n0\n20\n0\n10\n500\n20\n0\n10\n500\n20\n300\n10\n0\n20\n300\n\
0\nENDBLK\n\
0\nENDSEC\n\
0\nSECTION\n2\nENTITIES\n\
0\nINSERT\n8\nCUT\n2\nBRACKET\n10\n0\n20\n0\n70\n2\n71\n1\n44\n60\n45\n0\n\
0\nINSERT\n67\n1\n8\nCUT\n2\nTITLEBLOCK\n10\n0\n20\n0\n\
0\nLINE\n8\nCUT\n10\n200\n20\n0\n11\n250\n21\n0\n\
0\nLINE\n8\nCUT\n10\n200\n20\n0\n11\n250\n21\n0\n\
0\nLINE\n8\nCUT\n10\n250\n20\n0\n11\n250\n21\n40\n\
0\nLINE\n8\nCUT\n10\n250\n20\n40\n11\n200\n21\n40\n\
0\nLINE\n8\nCUT\n10\n200\n20\n40\n11\n200\n21\n0.08\n\
0\nENDSEC\n0\nEOF\n";

    // Default import (no gap healing) must flag the 0.08 mm open contour instead of silently dropping it.
    let raw = import_dxf(dxf, &ImportOptions::default()).unwrap();
    assert_eq!(raw.report.open_contours.len(), 1);
    assert!((raw.report.open_contours[0].end_gap_mm - 0.08).abs() < 1e-3);

    // Explicit close_gaps_mm heals the 0.08 mm gap, strips the duplicate line, keeps both MINSERT copies, and skips paper space.
    let healed = import_dxf(
        dxf,
        &ImportOptions {
            close_gaps_mm: Some(0.1),
            ..ImportOptions::default()
        },
    )
    .unwrap();
    assert!(healed.report.open_contours.is_empty());
    assert_eq!(healed.report.closed_gaps.len(), 1);
    assert!(healed.report.cleanup.duplicate_segments_removed >= 1);
    assert_eq!(
        healed.parts.len(),
        3,
        "expected 2 MINSERT brackets + 1 healed plate"
    );
}

#[test]
fn svg_physical_units_closed_loop_remnant_reuse_and_quote() {
    // 2 in × 1 in plate with a 0.25 in radius hole (50.8 × 25.4 mm, hole Ø12.7 mm).
    let svg = r#"<svg xmlns="http://www.w3.org/2000/svg" width="4in" height="2in" viewBox="0 0 4 2">
        <rect x="0" y="0" width="2" height="1"/>
        <circle cx="1" cy="0.5" r="0.25"/>
    </svg>"#;
    let decoded = decode_drawing("inch-plate.svg", svg.as_bytes()).unwrap();
    let check = import_svg(&decoded, &ImportOptions::default()).unwrap();
    assert_eq!(check.parts.len(), 1);
    assert_eq!(check.parts[0].holes.len(), 1);
    let [x0, y0, x1, y1] = check.parts[0].bounds;
    assert!(((x1 - x0) - 50.8).abs() < 1e-3);
    assert!(((y1 - y0) - 25.4).abs() < 1e-3);

    // Batch 1: nest 4 plates on a 300 × 200 mm sheet.
    let lib = Library::import(
        &[("inch-plate.svg".into(), decoded)],
        &ImportOptions::default(),
    )
    .unwrap();
    let req1: Request = serde_json::from_value(serde_json::json!({
        "name": "batch-1",
        "parts": [{"id": "inch-plate-1", "quantity": 4}],
        "sheets": [{"width_mm": 300.0, "height_mm": 200.0, "margins_mm": {"left": 5.0, "right": 5.0, "bottom": 5.0, "top": 5.0}}],
        "spacing_mm": 1.0,
        "edge_spacing_mm": 1.0
    }))
    .unwrap();
    let prepared1 = req1.prepare(&lib).unwrap();
    let (res1, cut1) = prepared1
        .optimize(
            SheetOptions {
                seconds: 1.0,
                seed: 1,
                timing: nestbolt_core::clock::Timing::Work,
                time_limit: Some(30.0),
                ..SheetOptions::default()
            },
            |_, _| {},
        )
        .unwrap();
    assert!(validate(&prepared1.job, &res1.layout).unwrap().valid);

    // Quote Batch 1 and verify exact perimeter (outer 152.4 mm + circle 12.7*pi mm) × 4 parts.
    let quote1 = from_cutting_report(
        &prepared1,
        &res1.layout,
        &cut1,
        &Pricing {
            sheet_cost: Some(15.0),
            credit_offcut: true,
            cut_speed_mm_per_min: Some(1000.0),
            pierce_seconds: 0.5,
            machine_rate_per_hour: Some(60.0),
            setup_cost: 2.0,
            currency: Some("USD".into()),
            ..Pricing::default()
        },
    )
    .unwrap();
    let expected_cut = 4.0 * (2.0 * (50.8 + 25.4) + std::f64::consts::PI * 12.7);
    assert!((quote1.net_cut_length_mm - expected_cut).abs() < 0.05);
    assert_eq!(quote1.total_pierces, 8);

    // Extract reusable exact remnant from Batch 1 -> export as DXF -> re-import -> nest Batch 2 onto it!
    let offcuts = extract(
        &prepared1.job,
        &res1.layout,
        None,
        OffcutOptions {
            mode: OffcutMode::Exact,
            ..OffcutOptions::default()
        },
    )
    .unwrap();
    assert!(!offcuts.remnants.is_empty());
    let remnant_dxf = offcuts.remnants[0].to_dxf().unwrap();
    let sheet_import =
        SheetImport::read("remnant.dxf", &remnant_dxf, &ImportOptions::default()).unwrap();
    assert_eq!(sheet_import.outlines.len(), 1);
    let outline = &sheet_import.outlines[0];

    let req2: Request = serde_json::from_value(serde_json::json!({
        "name": "batch-2-on-remnant",
        "parts": [{"id": "inch-plate-1", "quantity": 4}],
        "sheets": [{
            "width_mm": outline.width_mm,
            "height_mm": outline.height_mm,
            "margins_mm": {"left": 2.0, "right": 2.0, "bottom": 2.0, "top": 2.0},
            "outline_mm": outline.outline_mm,
            "outline_tolerance_mm": outline.tolerance_mm,
            "count": 1
        }],
        "spacing_mm": 1.0,
        "edge_spacing_mm": 1.0
    }))
    .unwrap();
    let (job2, _) = req2.job(&lib).unwrap();
    let res2 = optimize(
        &job2,
        SheetOptions {
            seconds: 1.0,
            seed: 1,
            timing: nestbolt_core::clock::Timing::Work,
            time_limit: Some(30.0),
            ..SheetOptions::default()
        },
        |_, _| {},
    )
    .unwrap();
    assert!(validate(&job2, &res2.layout).unwrap().valid);
    assert_eq!(res2.layout.placements.len(), 4);
}
