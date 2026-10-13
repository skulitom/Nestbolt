use nestbolt_core::import::{Options, import_dxf, import_svg, inspect_svg};

const SVG: &str = r##"<?xml version="1.0"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="100mm" viewBox="0 0 100 100">
<style>.cut { fill:none;stroke:#000 } .score {stroke:rgb(255,0,0);fill:none}</style>
<g inkscape:groupmode="layer" inkscape:label="CUT" class="cut"><rect width="20" height="20"/><circle cx="10" cy="10" r="2"/></g>
<g id="score" class="score"><rect x="40" width="8" height="8"/><text x="60">label</text></g>
<g id="BEND" stroke="blue"><rect x="60" width="8" height="8"/></g>
<g id="hidden" style="display:none;stroke:green"><rect x="80" width="8" height="8"/></g>
</svg>"##;

#[test]
fn svg_defaults_and_explicit_filters_preserve_inventory() {
    let r = import_svg(SVG, &Options::default()).unwrap();
    assert_eq!(r.parts.len(), 1);
    assert_eq!(r.parts[0].holes.len(), 1);
    assert_eq!(r.report.selection_mode, "named_cut_layers");
    assert_eq!(
        r.report
            .layers
            .iter()
            .find(|l| l.name == "score")
            .unwrap()
            .entities,
        2
    );
    assert_eq!(
        r.report
            .layers
            .iter()
            .find(|l| l.name == "hidden")
            .unwrap()
            .entities,
        1
    );
    assert!(r.warnings.iter().any(|s| s.contains("BEND")));
    assert!(
        r.warnings
            .iter()
            .any(|s| s.contains("text") && s.contains("convert"))
    );
    let r = import_svg(
        SVG,
        &Options {
            colors: Some(vec!["red".into()]),
            ..Default::default()
        },
    )
    .unwrap();
    assert_eq!(r.parts.len(), 1);
    assert!(r.parts[0].holes.is_empty());
    assert_eq!(r.parts[0].bounds, [40.0, -8.0, 48.0, 0.0]);
    assert_eq!(
        r.report
            .colors
            .iter()
            .find(|c| c.name == "#ff0000")
            .unwrap()
            .selected_entities,
        1
    );
    let e = import_svg(
        SVG,
        &Options {
            layers: Some(vec!["CUT".into()]),
            colors: Some(vec!["red".into()]),
            ..Default::default()
        },
    )
    .unwrap_err();
    assert!(e.to_string().contains("choose a layer/colour"));
    let e = import_svg(
        SVG,
        &Options {
            layers: Some(vec!["misspelled".into()]),
            ..Default::default()
        },
    )
    .unwrap_err();
    assert!(e.to_string().contains("unknown layer"));
    assert!(e.to_string().contains("CUT"));
}

#[test]
fn inventory_is_available_for_open_only_drawings() {
    let svg = r#"<svg><g id="cut"><path stroke="red" d="M0 0 L10 10"/></g></svg>"#;
    assert!(import_svg(svg, &Options::default()).is_err());
    let r = inspect_svg(svg, &Options::default()).unwrap();
    assert_eq!(
        r.layers.iter().find(|l| l.name == "cut").unwrap().entities,
        1
    );
    assert_eq!(r.colors[0].name, "#ff0000");
}

#[test]
fn svg_css_specificity_and_use_inheritance_choose_the_right_colour() {
    let svg = r##"<svg width="50mm" viewBox="0 0 50 50"><style>#r {stroke:blue}.x {stroke:red}rect {stroke:green}* {stroke:purple}</style>
        <defs><rect id="symbol" width="10" height="10"/></defs>
        <g id="cut" stroke="purple"><use href="#symbol" x="20"/></g>
        <rect id="r" class="x" width="10" height="10" stroke="black" style="stroke:orange"/>
        </svg>"##;
    let r = import_svg(
        svg,
        &Options {
            colors: Some(vec!["orange".into()]),
            ..Default::default()
        },
    )
    .unwrap();
    assert_eq!(r.parts.len(), 1);
    assert_eq!(r.parts[0].bounds, [0.0, -10.0, 10.0, 0.0]);
    // An element's tag stylesheet rule overrides inherited <use> stroke.
    assert_eq!(
        r.report
            .colors
            .iter()
            .find(|c| c.name == "#008000")
            .unwrap()
            .entities,
        1
    );
    let bad = svg.replace("rect {stroke:green}", "g rect {stroke:green}");
    assert!(
        import_svg(&bad, &Options::default())
            .unwrap_err()
            .to_string()
            .contains("presentation attributes")
    );
}

fn dxf(entities: &str, blocks: &str) -> String {
    format!(
        "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nTABLES\n0\nLAYER\n2\nCUT\n62\n7\n0\nLAYER\n2\nSCORE\n62\n1\n0\nENDSEC\n0\nSECTION\n2\nBLOCKS\n{blocks}0\nENDSEC\n0\nSECTION\n2\nENTITIES\n{entities}0\nENDSEC\n0\nEOF\n"
    )
}

#[test]
fn dxf_layer_and_color_inherit_through_blocks_with_base_points() {
    let blocks = "0\nBLOCK\n2\nA\n10\n10\n20\n20\n0\nCIRCLE\n8\n0\n62\n0\n10\n12\n20\n23\n40\n2\n0\nENDBLK\n";
    let entities = "0\nINSERT\n8\nCUT\n62\n1\n2\nA\n10\n100\n20\n200\n0\nCIRCLE\n8\nSCORE\n10\n20\n20\n20\n40\n1\n0\nTEXT\n8\nSCORE\n1\nlabel\n";
    let text = dxf(entities, blocks);
    let r = import_dxf(&text, &Options::default()).unwrap();
    assert_eq!(r.parts.len(), 1);
    let nestbolt_core::curves::Segment::Arc { center, radii, .. } = r.parts[0].outer.segments[0]
    else {
        panic!("exact circle lost")
    };
    assert_eq!(center, [102.0, 203.0]);
    assert_eq!(radii, [2.0, 2.0]);
    assert_eq!(
        r.report
            .layers
            .iter()
            .find(|l| l.name == "CUT")
            .unwrap()
            .entities,
        2
    );
    assert_eq!(
        r.report
            .colors
            .iter()
            .find(|c| c.name == "aci:1")
            .unwrap()
            .entities,
        4
    );
    let r = import_dxf(
        &text,
        &Options {
            colors: Some(vec!["1".into()]),
            ..Default::default()
        },
    )
    .unwrap();
    assert_eq!(r.parts.len(), 2);
    let r = import_dxf(
        &text,
        &Options {
            layers: Some(vec!["score".into()]),
            ..Default::default()
        },
    )
    .unwrap();
    let nestbolt_core::curves::Segment::Arc { center, .. } = r.parts[0].outer.segments[0] else {
        panic!("exact circle lost")
    };
    assert_eq!(center, [20.0, 20.0]);
}

#[test]
fn insert_extrusion_mirrors_its_position_after_local_scale_and_rotation() {
    let blocks =
        "0\nBLOCK\n2\nA\n10\n10\n20\n20\n0\nCIRCLE\n8\n0\n10\n12\n20\n23\n40\n2\n0\nENDBLK\n";
    let entity = "0\nINSERT\n8\nCUT\n2\nA\n10\n100\n20\n200\n41\n2\n42\n2\n50\n90\n210\n0\n220\n0\n230\n-1\n";
    let r = import_dxf(&dxf(entity, blocks), &Options::default()).unwrap();
    let nestbolt_core::curves::Segment::Arc { center, radii, .. } = r.parts[0].outer.segments[0]
    else {
        panic!("exact circle lost")
    };
    assert_eq!(center, [-94.0, 204.0]);
    assert_eq!(radii, [4.0, 4.0]);
    for (a, b) in r.parts[0].bounds.iter().zip([-98.0, 200.0, -90.0, 208.0]) {
        assert!((a - b).abs() <= 0.005, "{:?}", r.parts[0].bounds);
    }
}

#[test]
fn malformed_polyline_has_a_reexport_fix() {
    let entity = "0\nPOLYLINE\n8\nCUT\n70\n1\n0\nVERTEX\n10\n0\n20\n0\n";
    assert!(
        import_dxf(&dxf(entity, ""), &Options::default())
            .unwrap_err()
            .to_string()
            .contains("re-export")
    );
}
