use nestbolt_core::import::{Options, import_dxf, import_svg};

fn assert_bounds(svg: &str, expected: [f64; 4]) {
    let imported = import_svg(svg, &Options::default()).unwrap();
    assert_eq!(imported.parts.len(), 1);
    for (got, want) in imported.parts[0].bounds.iter().zip(expected) {
        assert!(
            (got - want).abs() < 0.005,
            "{:?} != {expected:?}",
            imported.parts[0].bounds
        );
    }
}

#[test]
fn aspect_ratio_meet_slice_none_and_alignment_keep_physical_dimensions() {
    let page = |aspect| {
        format!(
            r#"<svg width="200mm" height="100mm" viewBox="10 20 100 100" {aspect}><rect x="30" y="50" width="10" height="20"/></svg>"#
        )
    };
    for (aspect, bounds) in [
        ("", [70.0, -50.0, 80.0, -30.0]),
        (
            r#"preserveAspectRatio="xMaxYMin meet""#,
            [120.0, -50.0, 130.0, -30.0],
        ),
        (r#"preserveAspectRatio="none""#, [40.0, -50.0, 60.0, -30.0]),
        (
            r#"preserveAspectRatio="xMidYMid slice""#,
            [40.0, -50.0, 60.0, -10.0],
        ),
        (
            r#"preserveAspectRatio="xMaxYMax slice""#,
            [40.0, 0.0, 60.0, 40.0],
        ),
    ] {
        assert_bounds(&page(aspect), bounds);
    }
    let sliced = import_svg(
        &page(r#"preserveAspectRatio="xMidYMid slice""#),
        &Options::default(),
    )
    .unwrap();
    assert!(
        sliced
            .warnings
            .iter()
            .any(|w| w.contains("without viewport clipping") && w.contains("closed paths"))
    );
    assert_bounds(
        r#"<svg width="100mm" height="200mm" viewBox="0 0 100 100" preserveAspectRatio="xMinYMax"><rect x="20" y="30" width="10" height="20"/></svg>"#,
        [20.0, -150.0, 30.0, -130.0],
    );
}

#[test]
fn either_absolute_dimension_sets_the_scale_and_missing_dimensions_use_user_units() {
    for dimensions in [r#"height="100mm""#, r#"width="200mm""#] {
        assert_bounds(
            &format!(
                r#"<svg {dimensions} viewBox="0 0 200 100"><rect x="20" y="30" width="10" height="20"/></svg>"#
            ),
            [20.0, -50.0, 30.0, -30.0],
        );
    }
    let source =
        r#"<svg viewBox="10 20 200 100"><rect x="30" y="50" width="10" height="20"/></svg>"#;
    let options = Options {
        svg_user_unit: 1.0,
        ..Default::default()
    };
    assert_eq!(
        import_svg(source, &options).unwrap().parts[0].bounds,
        [20.0, -50.0, 30.0, -30.0]
    );
}

#[test]
fn root_transform_acts_outside_viewbox_in_viewport_units() {
    assert_bounds(
        include_str!("fixtures/viewport.svg"),
        [65.4, -62.7, 85.4, -42.7],
    );
    assert_bounds(
        r#"<svg width="200mm" height="100mm" viewBox="0 0 100 100" transform="scale(2)"><g transform="translate(10 0)"><rect x="20" y="30" width="10" height="20"/></g></svg>"#,
        [160.0, -100.0, 180.0, -60.0],
    );
}

#[test]
fn nonuniform_page_mapping_retains_curved_boundaries() {
    let source = r#"<svg width="200mm" height="100mm" viewBox="0 0 100 100" preserveAspectRatio="none"><circle cx="25" cy="40" r="5"/></svg>"#;
    assert_bounds(source, [40.0, -45.0, 60.0, -35.0]);
    let imported = import_svg(source, &Options::default()).unwrap();
    assert!(imported.parts[0].outer.segments.iter().any(|s| matches!(
        s,
        nestbolt_core::curves::Segment::Cubic { .. } | nestbolt_core::curves::Segment::Arc { .. }
    )));
    assert!((imported.parts[0].area - 50.0 * std::f64::consts::PI).abs() < 0.2);
}

#[test]
fn ambiguous_or_invalid_pages_name_the_repair_instead_of_guessing_a_size() {
    for attributes in [
        r#"viewBox="bad""#,
        r#"viewBox="0 0 0 100""#,
        r#"width="100%""#,
        r#"height="0""#,
        r#"width="NaN""#,
        r#"viewBox="0 0 100 100" preserveAspectRatio="invalid""#,
        r#"transform="scale(0)""#,
    ] {
        let error = import_svg(
            &format!(r#"<svg {attributes}><rect width="10" height="10"/></svg>"#),
            &Options::default(),
        )
        .unwrap_err();
        let error = format!("{error:#}");
        assert!(
            error.contains("SVG")
                && (error.contains("set")
                    || error.contains("repair")
                    || error.contains("apply")
                    || error.contains("use")),
            "{error}"
        );
    }
    let error = import_svg(
        r#"<svg><svg width="50" viewBox="0 0 100 100"><rect width="10" height="10"/></svg></svg>"#,
        &Options::default(),
    )
    .unwrap_err();
    assert!(error.to_string().contains("single page"));
}

#[test]
fn modern_and_legacy_polyline_widths_warn_without_expanding_cut_centrelines() {
    let constant = include_str!("fixtures/polyline-width.dxf");
    let variable = constant
        .replace("43\n0.4\n", "")
        .replace("20\n0\n", "20\n0\n40\n0.1\n41\n0.3\n");
    let legacy = "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nPOLYLINE\n8\nCUT\n70\n1\n40\n0.1\n0\nVERTEX\n10\n0\n20\n0\n41\n0.3\n0\nVERTEX\n10\n10\n20\n0\n0\nVERTEX\n10\n10\n20\n5\n0\nVERTEX\n10\n0\n20\n5\n0\nSEQEND\n0\nENDSEC\n0\nEOF\n";
    for source in [constant, variable.as_str(), legacy] {
        let imported = import_dxf(source, &Options::default()).unwrap();
        assert_eq!(imported.parts.len(), 1);
        assert_eq!(imported.parts[0].bounds, [0.0, 0.0, 10.0, 5.0]);
        assert_eq!(imported.parts[0].area, 50.0);
        assert_eq!(
            imported
                .warnings
                .iter()
                .filter(|w| w.contains("polyline widths ignored") && w.contains("Convert widths"))
                .count(),
            1
        );
    }
    let zero = import_dxf(
        &constant.replace("43\n0.4\n", "43\n0\n"),
        &Options::default(),
    )
    .unwrap();
    assert!(
        !zero
            .warnings
            .iter()
            .any(|w| w.contains("polyline widths ignored"))
    );
}
