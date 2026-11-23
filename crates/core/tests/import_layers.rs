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
    dxf_with_layers(
        "0\nLAYER\n2\nCUT\n62\n7\n0\nLAYER\n2\nSCORE\n62\n1\n",
        entities,
        blocks,
    )
}

fn dxf_with_layers(layers: &str, entities: &str, blocks: &str) -> String {
    format!(
        "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nTABLES\n{layers}0\nENDSEC\n0\nSECTION\n2\nBLOCKS\n{blocks}0\nENDSEC\n0\nSECTION\n2\nENTITIES\n{entities}0\nENDSEC\n0\nEOF\n"
    )
}

/// A LAYER table record. A negative colour turns the layer off, and flag 1
/// freezes it.
fn layer(name: &str, color: i32, flags: u32) -> String {
    format!("0\nLAYER\n2\n{name}\n70\n{flags}\n62\n{color}\n")
}

fn rectangle(layer: &str, [x0, y0, x1, y1]: [f64; 4]) -> String {
    format!(
        "0\nLWPOLYLINE\n8\n{layer}\n90\n4\n70\n1\n10\n{x0}\n20\n{y0}\n10\n{x1}\n20\n{y0}\n10\n{x1}\n20\n{y1}\n10\n{x0}\n20\n{y1}\n"
    )
}

fn listed(layers: &[&str]) -> Options {
    Options {
        layers: Some(layers.iter().map(|&l| l.into()).collect()),
        ..Default::default()
    }
}

fn colour_7() -> Options {
    Options {
        colors: Some(vec!["7".into()]),
        ..Default::default()
    }
}

/// A layer named in `Options::layers` is read even when it is off (negative
/// colour) or frozen (flag 1). Automatic and colour-only selection still skip
/// it.
#[test]
fn listed_off_or_frozen_layer_is_imported() {
    for table in [layer("CUT", -7, 0), layer("CUT", 7, 1)] {
        let text = dxf_with_layers(&table, &rectangle("CUT", [0.0, 0.0, 100.0, 50.0]), "");
        // The list matches the layer table without case sensitivity.
        let r = import_dxf(&text, &listed(&["cut"])).unwrap();
        assert_eq!(r.parts.len(), 1, "{table:?}: {:?}", r.warnings);
        assert_eq!(r.parts[0].bounds, [0.0, 0.0, 100.0, 50.0]);
        assert!(r.warnings.is_empty(), "{:?}", r.warnings);
        assert!(r.report.entries.is_empty(), "{:?}", r.report.entries);
        let cut = r.report.layers.iter().find(|l| l.name == "CUT").unwrap();
        assert_eq!((cut.entities, cut.selected_entities), (1, 1));
        let white = r.report.colors.iter().find(|c| c.name == "aci:7").unwrap();
        assert_eq!(white.selected_entities, 1);
        for options in [Options::default(), colour_7()] {
            let e = import_dxf(&text, &options).unwrap_err().to_string();
            assert!(
                e.contains("ignored 1 LWPOLYLINE on layer \"CUT\": hidden DXF entity or layer"),
                "{table:?}: {e}"
            );
        }
    }
}

/// The 100 x 50 mm part keeps its 20 x 20 mm hole when the hole's layer is off
/// but listed. Not listed, the hole layer is still skipped with a warning.
#[test]
fn listed_hidden_hole_layer_gives_the_part_its_hole() {
    let tables = format!("{}{}", layer("CUT", 7, 0), layer("HOLES", -7, 0));
    let entities = format!(
        "{}{}",
        rectangle("CUT", [0.0, 0.0, 100.0, 50.0]),
        rectangle("HOLES", [10.0, 10.0, 30.0, 30.0])
    );
    let text = dxf_with_layers(&tables, &entities, "");
    let r = import_dxf(&text, &listed(&["CUT", "HOLES"])).unwrap();
    assert_eq!(r.parts.len(), 1, "{:?}", r.warnings);
    assert_eq!(r.parts[0].holes.len(), 1, "{:?}", r.warnings);
    let area = r.parts[0].area;
    assert!((area - 4600.0).abs() < 1e-9, "{area}");
    assert!(r.warnings.is_empty(), "{:?}", r.warnings);
    assert!(r.report.entries.is_empty(), "{:?}", r.report.entries);
    let holes = r.report.layers.iter().find(|l| l.name == "HOLES").unwrap();
    assert_eq!((holes.entities, holes.selected_entities), (1, 1));
    let white = r.report.colors.iter().find(|c| c.name == "aci:7").unwrap();
    assert_eq!((white.entities, white.selected_entities), (2, 2));
    let warning = "ignored 1 LWPOLYLINE on layer \"HOLES\": hidden DXF entity or layer";
    for options in [listed(&["CUT"]), Options::default(), colour_7()] {
        let r = import_dxf(&text, &options).unwrap();
        assert_eq!(r.parts.len(), 1, "{:?}", r.warnings);
        assert!(r.parts[0].holes.is_empty());
        assert!(r.warnings.iter().any(|w| w == warning), "{:?}", r.warnings);
        let holes = r.report.layers.iter().find(|l| l.name == "HOLES").unwrap();
        assert_eq!((holes.entities, holes.selected_entities), (1, 0));
    }
}

/// A listed DXF layer is read even when its name marks bend, extent or
/// construction lines. Automatic and colour-only selection still skip it, and
/// so does SVG import.
#[test]
fn listed_bend_extent_or_construction_layer_is_imported() {
    for name in ["Bend relief cut", "Extents", "CONSTRUCTION 2"] {
        let text = dxf_with_layers(
            &layer(name, 7, 0),
            &rectangle(name, [0.0, 0.0, 10.0, 10.0]),
            "",
        );
        let r = import_dxf(&text, &listed(&[name])).unwrap();
        assert_eq!(r.parts.len(), 1, "{name}: {:?}", r.warnings);
        assert!(r.warnings.is_empty(), "{:?}", r.warnings);
        let channel = r.report.layers.iter().find(|l| l.name == name).unwrap();
        assert_eq!((channel.entities, channel.selected_entities), (1, 1));
        for options in [Options::default(), colour_7()] {
            let e = import_dxf(&text, &options).unwrap_err().to_string();
            assert!(
                e.contains(&format!(
                    "ignored 1 LWPOLYLINE on layer {name:?}: bend/extent/construction layer"
                )),
                "{name}: {e}"
            );
        }
    }
    let svg = r#"<svg width="10mm" viewBox="0 0 10 10"><g id="BEND" stroke="black"><rect width="10" height="10"/></g></svg>"#;
    let e = import_svg(svg, &listed(&["BEND"])).unwrap_err().to_string();
    assert!(e.contains("bend/extent/construction layer"), "{e}");
}

/// Listing a layer overrides only that layer's own off or frozen state. An
/// entity hidden on its own (60=1), or inside an INSERT that is hidden on its
/// own or sits on a hidden layer that isn't listed, stays hidden.
#[test]
fn listed_layer_keeps_entities_hidden_on_their_own_or_by_their_insert() {
    let tables = format!(
        "{}{}{}",
        layer("CUT", 7, 0),
        layer("PARTS", -7, 0),
        layer("OFF", -7, 0)
    );
    // A layer-0 circle that takes the INSERT's layer and a circle on CUT.
    let blocks = "0\nBLOCK\n2\nA\n10\n0\n20\n0\n0\nCIRCLE\n8\n0\n10\n0\n20\n0\n40\n5\n\
        0\nCIRCLE\n8\nCUT\n10\n0\n20\n20\n40\n5\n0\nENDBLK\n";
    let entities = "0\nCIRCLE\n8\nPARTS\n60\n1\n10\n0\n20\n0\n40\n5\n\
        0\nINSERT\n8\nOFF\n2\nA\n10\n100\n20\n0\n\
        0\nINSERT\n8\nPARTS\n2\nA\n10\n200\n20\n0\n\
        0\nINSERT\n8\nCUT\n60\n1\n2\nA\n10\n300\n20\n0\n";
    let text = dxf_with_layers(&tables, entities, blocks);
    let r = import_dxf(&text, &listed(&["CUT", "PARTS"])).unwrap();
    let mut centers: Vec<_> = r
        .parts
        .iter()
        .map(|p| {
            let nestbolt_core::curves::Segment::Arc { center, .. } = p.outer.segments[0] else {
                panic!("exact circle lost")
            };
            center
        })
        .collect();
    centers.sort_by(|a, b| a.partial_cmp(b).unwrap());
    // Only the INSERT on the listed PARTS layer places its circles.
    assert_eq!(centers, [[200.0, 0.0], [200.0, 20.0]], "{:?}", r.warnings);
    for (count, layer) in [(3, "CUT"), (1, "OFF"), (1, "PARTS")] {
        let warning =
            format!("ignored {count} CIRCLE on layer {layer:?}: hidden DXF entity or layer");
        assert!(r.warnings.contains(&warning), "{warning}: {:?}", r.warnings);
    }
    for (name, entities, selected) in [("CUT", 5, 1), ("PARTS", 3, 1), ("OFF", 2, 0)] {
        let channel = r.report.layers.iter().find(|l| l.name == name).unwrap();
        assert_eq!(
            (channel.entities, channel.selected_entities),
            (entities, selected),
            "{name}"
        );
    }
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

/// A paper-space INSERT places its block in paper space too, as GDAL reports
/// it, so neither the INSERT nor the block's entities are cut.
#[test]
fn paper_space_insert_ignores_its_block() {
    let blocks = "0\nBLOCK\n2\nA\n10\n0\n20\n0\n0\nCIRCLE\n8\n0\n10\n0\n20\n0\n40\n5\n0\nENDBLK\n";
    let entities =
        "0\nINSERT\n8\nCUT\n2\nA\n10\n20\n20\n0\n0\nINSERT\n8\nCUT\n67\n1\n2\nA\n10\n50\n20\n0\n";
    let r = import_dxf(&dxf(entities, blocks), &Options::default()).unwrap();
    assert_eq!(r.parts.len(), 1, "{:?}", r.warnings);
    let nestbolt_core::curves::Segment::Arc { center, .. } = r.parts[0].outer.segments[0] else {
        panic!("exact circle lost")
    };
    assert_eq!(center, [20.0, 0.0]);
    for kind in ["INSERT", "CIRCLE"] {
        let warning = format!(
            "ignored 1 {kind} on layer \"CUT\": paper-space entity; move cut outlines to model space"
        );
        assert!(r.warnings.contains(&warning), "{:?}", r.warnings);
    }
    let cut = r.report.layers.iter().find(|l| l.name == "CUT").unwrap();
    assert_eq!((cut.entities, cut.selected_entities), (4, 1));
}

/// A MINSERT places a copy of its block at every row and column, spaced along
/// its rotated axes without scaling, as in ezdxf's `Insert.multi_insert` and
/// GDAL's `additional-entities.dxf` test. A count of 0 reads as 1, and a
/// spacing of 0 keeps one copy along its axis.
#[test]
fn minsert_places_a_copy_at_every_grid_position() {
    let blocks = "0\nBLOCK\n2\nA\n10\n0\n20\n0\n0\nCIRCLE\n8\n0\n10\n0\n20\n0\n40\n5\n0\nENDBLK\n";
    // 3 columns 30 apart and 2 rows 40 apart, turned 90 degrees: columns run
    // along +Y and rows along -X.
    let grid = "0\nINSERT\n8\nCUT\n2\nA\n10\n100\n20\n50\n41\n2\n42\n2\n50\n90\n\
        70\n3\n71\n2\n44\n30\n45\n40\n";
    // No columns, and 3 rows with no spacing between them: one copy.
    let single = "0\nINSERT\n8\nCUT\n2\nA\n10\n300\n20\n0\n70\n0\n71\n3\n44\n30\n45\n0\n";
    let r = import_dxf(
        &dxf(&format!("{grid}{single}"), blocks),
        &Options::default(),
    )
    .unwrap();
    let circles: Vec<_> = r
        .parts
        .iter()
        .map(|p| {
            let nestbolt_core::curves::Segment::Arc { center, radii, .. } = p.outer.segments[0]
            else {
                panic!("exact circle lost")
            };
            (center, radii[0])
        })
        .collect();
    let expected = [
        ([100.0, 50.0], 10.0),
        ([100.0, 80.0], 10.0),
        ([100.0, 110.0], 10.0),
        ([60.0, 50.0], 10.0),
        ([60.0, 80.0], 10.0),
        ([60.0, 110.0], 10.0),
        ([300.0, 0.0], 5.0),
    ];
    assert_eq!(circles.len(), expected.len(), "{:?}", r.warnings);
    for (center, radius) in expected {
        assert!(
            circles
                .iter()
                .any(|(c, rad)| (c[0] - center[0]).abs() < 1e-9
                    && (c[1] - center[1]).abs() < 1e-9
                    && (rad - radius).abs() < 1e-9),
            "{center:?} missing from {circles:?}"
        );
    }
    let cut = r.report.layers.iter().find(|l| l.name == "CUT").unwrap();
    assert_eq!(cut.entities, 2 + expected.len());
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

#[test]
fn incomplete_polyline_in_paper_block_keeps_model_geometry() {
    let block = "0\nBLOCK\n2\nPAGE\n0\nPOLYLINE\n8\n0\n0\nVERTEX\n10\n12\n20\n5\n0\nENDBLK\n";
    let entities = "0\nCIRCLE\n8\nCUT\n10\n5\n20\n5\n40\n3\n0\nINSERT\n8\nLAYOUT\n67\n1\n2\nPAGE\n";
    let import = import_dxf(&dxf(entities, block), &Options::default()).unwrap();
    assert_eq!(import.parts.len(), 1);
    assert!(
        import
            .warnings
            .iter()
            .any(|w| w.contains("POLYLINE") && w.contains("paper-space"))
    );
}
