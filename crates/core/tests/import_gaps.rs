use nestbolt_core::import::{Options, import_svg};
use nestbolt_core::project::Library;

fn drawing(gap: f64) -> String {
    format!(
        r#"<svg width="100mm" height="100mm" viewBox="0 0 100 100">
        <path id="broken" d="M0 0 H20 V20 H0 V{gap}"/>
        <rect id="complete" x="40" width="10" height="10"/>
    </svg>"#
    )
}

#[test]
fn curve_precision_does_not_enable_gap_healing() {
    for tolerance in [0.0005, 0.005, 0.1] {
        let result = import_svg(
            &drawing(0.05),
            &Options {
                tolerance,
                ..Options::default()
            },
        )
        .unwrap();
        assert_eq!(result.parts.len(), 1);
        assert_eq!(result.report.silent_join_mm, 0.005);
        assert!(result.report.closed_gaps.is_empty());
        let open = &result.report.open_contours[0];
        assert_eq!(open.source, "broken");
        assert!((open.end_gap_mm - 0.05).abs() < 1e-10);
        assert_eq!(open.suggested_close_gaps_mm, Some(0.05));
        assert!(
            result
                .warnings
                .iter()
                .any(|w| w.contains("Close gaps up to 0.050000 mm"))
        );
    }
}

#[test]
fn explicit_gap_repair_keeps_original_curve_endpoints() {
    let result = import_svg(
        &drawing(0.05),
        &Options {
            close_gaps_mm: Some(0.05),
            ..Options::default()
        },
    )
    .unwrap();
    assert_eq!(result.parts.len(), 2);
    assert!(result.report.open_contours.is_empty());
    assert_eq!(result.report.closed_gaps.len(), 1);
    let gap = &result.report.closed_gaps[0];
    assert_eq!(gap.from_mm, [0.0, -0.05]);
    assert_eq!(gap.to_mm, [0.0, 0.0]);
    let part = result.parts.iter().find(|p| p.source == "broken").unwrap();
    assert_eq!(part.outer.segments.len(), 5);
    assert!((part.area - 400.0).abs() < 1e-8);
}

#[test]
fn repair_limit_is_one_mm_and_default_join_is_silent() {
    for limit in [-0.1, 1.0001, f64::NAN, f64::INFINITY] {
        let err = import_svg(
            &drawing(0.01),
            &Options {
                close_gaps_mm: Some(limit),
                ..Options::default()
            },
        )
        .unwrap_err();
        assert!(err.to_string().contains("between 0 and 1 mm"));
    }
    let silent = import_svg(
        &drawing(0.004),
        &Options {
            tolerance: 0.0001,
            ..Options::default()
        },
    )
    .unwrap();
    assert_eq!(silent.parts.len(), 2);
    assert!(silent.report.closed_gaps.is_empty());
    let large = import_svg(
        &drawing(1.1),
        &Options {
            close_gaps_mm: Some(1.0),
            ..Options::default()
        },
    )
    .unwrap();
    assert_eq!(large.parts.len(), 1);
    assert_eq!(large.report.open_contours[0].suggested_close_gaps_mm, None);
}

#[test]
fn empty_import_error_names_the_location_and_fix() {
    let svg = r#"<svg width="30mm" viewBox="0 0 30 30"><path id="outline" d="M0 0 H20 V20 H0 V0.2"/></svg>"#;
    let err = import_svg(svg, &Options::default())
        .unwrap_err()
        .to_string();
    assert!(
        err.contains("outline: open path from (0.000000, 0.000000)"),
        "{err}"
    );
    assert!(err.contains("Close gaps up to 0.200000 mm"), "{err}");
}

#[test]
fn library_rejects_partial_geometry_until_repaired_or_excluded() {
    let files = vec![("gap.svg".into(), drawing(0.05))];
    let err = Library::import(&files, &Options::default())
        .unwrap_err()
        .to_string();
    assert!(
        err.contains("gap.svg: 1 selected contour(s) remain open"),
        "{err}"
    );
    assert!(err.contains("no partial library was created"), "{err}");
    assert!(err.contains("Close gaps up to 0.050000 mm"), "{err}");
    let repaired = Library::import(
        &files,
        &Options {
            close_gaps_mm: Some(0.05),
            ..Options::default()
        },
    )
    .unwrap();
    assert_eq!(repaired.parts.len(), 2);
    let layered = vec![("layers.svg".into(), r#"<svg width="100mm" viewBox="0 0 100 100"><g id="CUT"><rect width="20" height="20"/></g><g id="SCORE"><path d="M40 0 H60"/></g></svg>"#.into())];
    assert_eq!(
        Library::import(&layered, &Options::default())
            .unwrap()
            .parts
            .len(),
        1
    );
    assert!(
        Library::import(
            &layered,
            &Options {
                layers: Some(vec!["CUT".into(), "SCORE".into()]),
                ..Options::default()
            }
        )
        .unwrap_err()
        .to_string()
        .contains("exclude their layer/colour")
    );
}
