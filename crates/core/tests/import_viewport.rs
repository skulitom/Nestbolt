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
fn polygon_and_polyline_points_preserve_the_window() {
    let source = include_str!("fixtures/compact-points.svg");
    for points in [
        "10-20 30-20 30-10 10-10",
        "+1e1-2E+1,3e1-2e1,30-10,.1e2-1e1",
        " 10 , -20\t30 -20, 30,-10\n10, -10 ",
    ] {
        for element in ["polygon", "polyline"] {
            let mut points = points.to_owned();
            if element == "polyline" {
                points.push_str(" 10-20");
            }
            let svg = source
                .replace("polygon", element)
                .replace("10-20 30-20 30-10 10-10", &points);
            let imported = import_svg(&svg, &Options::default()).unwrap();
            assert_eq!(imported.parts.len(), 1);
            let part = &imported.parts[0];
            assert!((part.area - 1000.0).abs() < 1e-9);
            for (actual, expected) in part.bounds.iter().zip([0.0, -30.0, 40.0, 0.0]) {
                assert!((actual - expected).abs() < 1e-9);
            }
            assert_eq!(part.polygon.holes.len(), 1);
            for [x, y] in [[10.0, -20.0], [30.0, -20.0], [30.0, -10.0], [10.0, -10.0]] {
                assert!(
                    part.polygon.holes[0]
                        .iter()
                        .any(|p| (p[0] - x).hypot(p[1] - y) < 1e-9)
                );
            }
        }
    }
}

#[test]
fn malformed_selected_point_lists_identify_the_element_and_repair() {
    let source = include_str!("fixtures/malformed-points.svg");
    for points in [
        "10,-20 30,-20 broken 30,-10 10,-10",
        "10,-20 30,-20 30",
        ",10,-20",
        "10,,20",
        "10,20, ",
        "10+20 30-20",
        "10.5.2",
        "10,-20-30,-20",
        "10,1e",
        "NaN,10",
        "1e999,20",
    ] {
        for element in ["polygon", "polyline"] {
            let svg = source
                .replace("polygon", element)
                .replace("10,-20 30,-20 broken 30,-10 10,-10", points);
            let message = import_svg(&svg, &Options::default())
                .unwrap_err()
                .to_string();
            assert!(
                message.contains(&format!("<{element}>"))
                    && message.contains("window")
                    && message.contains("Correct the coordinate pairs"),
                "{points}: {message}"
            );
        }
    }
}

#[test]
fn excluded_point_lists_can_be_inspected_and_empty_ones_draw_nothing() {
    let svg = r#"<svg width="20mm" viewBox="0 0 20 20">
        <g id="CUT"><rect width="10" height="10"/><polygon points=" "/><polyline/></g>
        <g id="GUIDES"><polygon id="guide" points="broken"/></g>
        <polyline visibility="hidden" points="broken"/></svg>"#;
    assert_bounds(svg, [0.0, -10.0, 10.0, 0.0]);
    let options = Options {
        layers: Some(vec!["GUIDES".into()]),
        ..Default::default()
    };
    let inventory = nestbolt_core::import::inspect_svg(svg, &options).unwrap();
    assert_eq!(
        inventory
            .layers
            .iter()
            .find(|l| l.name == "GUIDES")
            .unwrap()
            .selected_entities,
        1
    );
    assert!(
        import_svg(svg, &options)
            .unwrap_err()
            .to_string()
            .contains("guide")
    );
}

#[test]
fn physical_svg_lengths_keep_an_inch_dimensioned_hole() {
    let svg = include_str!("fixtures/inch-hole.svg");
    let import = import_svg(svg, &Options::default()).unwrap();
    assert_eq!(import.parts.len(), 1);
    let holes = &import.parts[0].holes;
    assert_eq!(holes.len(), 1);
    let nestbolt_core::curves::Segment::Arc { center, radii, .. } = &holes[0].segments[0] else {
        panic!("expected circular hole");
    };
    for (actual, expected) in center.iter().chain(radii).zip([12.7, -12.7, 3.175, 3.175]) {
        assert!((actual - expected).abs() < 1e-9);
    }
}

#[test]
fn lengths_apply_before_clone_and_viewbox_transforms() {
    let svg = r##"<svg width="192mm" height="192mm" viewBox="0 0 96 96">
        <defs><rect id="tile" x="1pc" y="12pt" width="0.25IN" height="25.4Q"/></defs>
        <g transform="scale(0.5)"><use href="#tile" x="1.27cm" y="12.7mm"/></g>
    </svg>"##;
    assert_bounds(svg, [64.0, -88.0, 88.0, -64.0]);
    let lines = r#"<svg width="96px" height="96px" stroke="black" fill="none">
        <line x2="1in"/><line x1="1in" x2="1in" y2="1in"/>
        <line x1="1in" y1="1in" y2="1in"/><line y1="1in"/>
    </svg>"#;
    assert_bounds(lines, [0.0, -25.4, 25.4, 0.0]);
}

#[test]
fn percentage_lengths_use_viewport_axes_and_the_normalized_diagonal() {
    assert_bounds(
        r#"<svg width="200mm" height="100mm" viewBox="0 0 100 100">
            <ellipse cx="50%" cy="40%" rx="10%" ry="5%"/></svg>"#,
        [90.0, -45.0, 110.0, -35.0],
    );
    let r = 0.1 * 30.0_f64.hypot(40.0) / std::f64::consts::SQRT_2;
    assert_bounds(
        r#"<svg width="30mm" height="40mm"><circle cx="50%" cy="50%" r="10%"/></svg>"#,
        [15.0 - r, -20.0 - r, 15.0 + r, -20.0 + r],
    );
}

#[test]
fn unresolvable_shape_lengths_name_the_attribute_and_repair() {
    assert_bounds(
        r#"<svg><rect x="0%" y="0em" width="96" height="96"/></svg>"#,
        [0.0, -25.4, 25.4, 0.0],
    );
    for (attributes, value) in [
        (r#"x="1em" width="10""#, "1em"),
        (r#"width="80%""#, "80%"),
        (r#"width="10" ry="invalid""#, "invalid"),
    ] {
        let svg = format!(r#"<svg><path d="M0 0h1v1h-1Z"/><rect {attributes} height="10"/></svg>"#);
        let error = import_svg(&svg, &Options::default())
            .unwrap_err()
            .to_string();
        assert!(
            error.contains("<rect>")
                && error.contains(value)
                && error.contains("convert the shape"),
            "{error}"
        );
    }
}

#[test]
fn unresolved_lengths_on_other_layers_leave_selected_cuts_available() {
    let svg = r##"<svg width="20mm" height="20mm" viewBox="0 0 20 20">
        <defs><circle id="mark" r="1"/></defs>
        <g id="CUT"><rect width="10" height="10"/></g>
        <g id="SCORE"><use href="#mark" x="2em"/><ellipse cx="1em" rx="1"/></g>
        <circle visibility="hidden" r="3em"/>
    </svg>"##;
    assert_bounds(svg, [0.0, -10.0, 10.0, 0.0]);
    let options = Options {
        layers: Some(vec!["SCORE".into()]),
        ..Default::default()
    };
    let inventory = nestbolt_core::import::inspect_svg(svg, &options).unwrap();
    assert_eq!(
        inventory
            .layers
            .iter()
            .find(|l| l.name == "SCORE")
            .unwrap()
            .selected_entities,
        2
    );
    let error = import_svg(svg, &options).unwrap_err().to_string();
    assert!(error.contains("<use>") && error.contains("2em"), "{error}");
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
