use nestbolt_core::{
    import::Options,
    project::{Library, Request, SheetImport},
};
use serde_json::json;

const SOURCE: &str = include_str!("fixtures/prearranged-sheet.svg");

#[test]
fn stock_cannot_gain_material_from_the_part_proxy_self_touch_repair() {
    let source = include_str!("fixtures/closed-retrace.svg")
        .replace("<path", "<g id=\"SHEET\"><path")
        .replace("</svg>", "</g></svg>");
    let error = SheetImport::read("retraced.svg", &source, &Options::default()).unwrap_err();
    assert!(format!("{error:#}").contains("stock boundaries cannot be expanded"));
}

#[test]
fn stock_selection_is_separate_and_normalizes_the_whole_sheet_with_holes() {
    let library =
        Library::import(&[("nest.svg".into(), SOURCE.into())], &Options::default()).unwrap();
    assert_eq!(library.parts.len(), 2);
    assert!(library.parts.iter().all(|p| p.holes.is_empty()));
    let [sheet] = library.sheet_outlines.as_slice() else {
        panic!("one sheet");
    };
    assert_eq!((sheet.width_mm, sheet.height_mm), (200.0, 100.0));
    assert_eq!(sheet.origin_mm, [20.0, -130.0]);
    assert_eq!(sheet.outline_mm[0].holes.len(), 1);
    assert_eq!(sheet.tolerance_mm, 0.0);
    assert!(
        library
            .warnings
            .iter()
            .any(|w| w.contains("sheet_outline_available"))
    );
    let request: Request =
        serde_json::from_value(json!({"sheets":[{"from_import":"nest-sheet-1","count":1}]}))
            .unwrap();
    let (job, _) = request.job(&library).unwrap();
    assert_eq!((job.stocks[0].width, job.stocks[0].height), (200.0, 100.0));
    let footprint = nestbolt_validator::Footprint::from_polygons(
        &job.stocks[0].outline,
        nestbolt_validator::Units::Mm,
        Default::default(),
    )
    .unwrap();
    assert_eq!(footprint.area(), 14975.0);
    assert_eq!(footprint.bounds(), [0.0, 0.0, 200.0, 100.0]);
    assert_eq!(job.parts.len(), 2);
    assert_eq!(
        job.edge_clearance,
        request.edge_spacing_mm + library.tolerance
    );
    let direct = SheetImport::read("nest.svg", SOURCE, &Options::default()).unwrap();
    assert_eq!(direct.outlines.len(), 1);
    assert_eq!(direct.outlines[0].width_mm, 200.0);
}

#[test]
fn custom_stock_layers_and_disabled_discovery_do_not_change_cut_parts() {
    let source = SOURCE.replace("id=\"SHEET\"", "id=\"MATERIAL\"");
    let options = Options {
        sheet_layers: Some(vec!["material".into()]),
        ..Default::default()
    };
    let library = Library::import(&[("nest.svg".into(), source)], &options).unwrap();
    assert_eq!(library.parts.len(), 2);
    assert_eq!(library.sheet_outlines.len(), 1);
    let disabled = Library::import(
        &[("nest.svg".into(), SOURCE.into())],
        &Options {
            sheet_layers: Some(vec![]),
            ..Default::default()
        },
    )
    .unwrap();
    assert!(disabled.sheet_outlines.is_empty());
    assert_eq!(disabled.parts.len(), 2);
}

#[test]
fn references_do_not_silently_resize_stock_or_accept_conflicting_geometry() {
    let library =
        Library::import(&[("nest.svg".into(), SOURCE.into())], &Options::default()).unwrap();
    for (stock, message) in [
        (json!({"from_import":"missing"}), "unknown sheet outline"),
        (
            json!({"from_import":"nest-sheet-1","width_mm":42}),
            "not rescaled",
        ),
        (
            json!({"from_import":"nest-sheet-1","outline_tolerance_mm":0.1}),
            "not both",
        ),
    ] {
        let request: Request = serde_json::from_value(json!({"sheets":[stock]})).unwrap();
        assert!(
            request
                .job(&library)
                .unwrap_err()
                .to_string()
                .contains(message)
        );
    }
}

#[test]
fn curved_stock_error_is_reserved_at_edges_and_explicit_gap_repair_is_required() {
    let source = r#"<svg width="200mm" viewBox="0 0 200 200"><g id="SHEET"><circle cx="100" cy="100" r="70"/><circle cx="100" cy="100" r="10"/></g><g id="CUT"><rect x="40" y="40" width="5" height="5"/></g></svg>"#;
    let library =
        Library::import(&[("ring.svg".into(), source.into())], &Options::default()).unwrap();
    let request: Request = serde_json::from_value(
        json!({"sheets":[{"from_import":"ring-sheet-1"}],"edge_spacing_mm":0.0}),
    )
    .unwrap();
    assert_eq!(request.job(&library).unwrap().0.edge_clearance, 0.01);
    let broken = r#"<svg width="100mm" viewBox="0 0 100 100"><g id="SHEET"><path d="M0 0 H100 V100 H0 V0.2"/></g><g id="CUT"><rect x="20" y="20" width="10" height="10"/></g></svg>"#;
    assert!(
        format!(
            "{:#}",
            SheetImport::read("gap.svg", broken, &Options::default()).unwrap_err()
        )
        .contains("Close gaps")
    );
    let default_parts =
        Library::import(&[("gap.svg".into(), broken.into())], &Options::default()).unwrap();
    assert_eq!(default_parts.parts.len(), 1);
    assert!(default_parts.sheet_outlines.is_empty());
    assert!(
        default_parts
            .warnings
            .iter()
            .any(|w| w.contains("SHEET outline could not"))
    );
    let repaired = SheetImport::read(
        "gap.svg",
        broken,
        &Options {
            close_gaps_mm: Some(0.2),
            ..Default::default()
        },
    )
    .unwrap();
    assert_eq!(repaired.outlines.len(), 1);
    assert_eq!(repaired.imports[0].report.closed_gaps.len(), 1);
}
