use nestbolt_core::{
    curves::{Affine, hausdorff},
    import::{Options, import_dxf, import_svg},
    lightburn::Document,
    project::{Library, Request},
};
use nestbolt_validator::{
    RigidTransform,
    job::{Layout, Placement, Sheet},
};
use serde_json::json;

const SOURCE: &str = include_str!("fixtures/lead-group.lbrn2");

fn without_settings(source: &str, indices: &[&str], image: bool) -> String {
    let xml = roxmltree::Document::parse(source).unwrap();
    let mut output = source.to_owned();
    for node in xml.root_element().children().filter(|n| {
        n.has_tag_name(if image {
            "CutSetting_Img"
        } else {
            "CutSetting"
        }) && n.children().any(|c| {
            c.has_tag_name("index") && indices.contains(&c.attribute("Value").unwrap_or(""))
        })
    }) {
        output = output.replace(&source[node.range()], "");
    }
    output
}

#[test]
fn omitted_line_and_tool_settings_preserve_original_cutting_sidecars() {
    let missing = without_settings(SOURCE, &["0", "30"], false);
    let (reference, request, layout) = setup(SOURCE);
    let (library, _, _) = setup(&missing);
    assert_eq!(library.parts.len(), reference.parts.len());
    assert_eq!(library.lightburn.as_ref().unwrap().fixed_top_level, 1);
    let expected = request
        .cutting_report(&reference, &layout)
        .unwrap()
        .review(&layout, "sheet-0")
        .unwrap();
    let report = request.cutting_report(&library, &layout).unwrap();
    assert!(report.validation.valid);
    assert_eq!(report.lead_in.as_ref().unwrap().expected_contours, 5);
    let actual = report.review(&layout, "sheet-0").unwrap();
    assert_eq!(actual.original_cuts.len(), expected.original_cuts.len());
    for (id, paths) in &expected.original_cuts {
        let actual = &actual.original_cuts[id];
        assert_eq!(actual.len(), paths.len());
        for (a, b) in actual.iter().zip(paths) {
            assert_eq!(a.closed, b.closed);
            assert_eq!(a.curve, b.curve);
        }
    }
    let files = library
        .export_files(&request, &layout, None, Some(false))
        .unwrap();
    assert_eq!(files.len(), 3);
    assert!(!files[0].text.contains("<CutSetting type=\"Cut\""));
    for i in [1, 2] {
        assert_eq!(
            files[i].text,
            reference
                .export_files(&request, &layout, None, Some(false))
                .unwrap()[i]
                .text
        );
    }
    let missing_image = without_settings(include_str!("fixtures/roundtrip.lbrn2"), &["0"], true);
    let (library, request, layout) = setup(&missing_image);
    let report = request.cutting_report(&library, &layout).unwrap();
    assert_eq!(report.lead_in.as_ref().unwrap().expected_contours, 3);
}

fn setup(text: &str) -> (Library, Request, Layout) {
    let library = Library::import(
        &[("lead-group.lbrn2".into(), text.into())],
        &Options::default(),
    )
    .unwrap();
    let request: Request = serde_json::from_value(json!({
        "parts":library.parts.iter().map(|p|json!({"id":p.id,"allow_mirror":true,"rotations":{"kind":"free"}})).collect::<Vec<_>>(),
        "sheets":[{"width_mm":400,"height_mm":400}], "spacing_mm":0.2,
        "lead_in":{"kerf_mm":0.2}
    }))
    .unwrap();
    let layout = Layout {
        version: 1,
        units: nestbolt_validator::Units::Mm,
        sheets: vec![Sheet {
            id: "sheet-0".into(),
            stock_id: "sheet-type-1".into(),
        }],
        placements: library
            .parts
            .iter()
            .enumerate()
            .map(|(i, p)| Placement {
                part_id: p.id.clone(),
                copy_index: 0,
                sheet_id: "sheet-0".into(),
                transform: RigidTransform {
                    translation: [100.0 + 100.0 * i as f64, 100.0],
                    ..Default::default()
                },
            })
            .collect(),
    };
    (library, request, layout)
}

#[test]
fn cutting_sidecars_keep_disconnected_pieces_holes_islands_and_open_paths() {
    let (library, request, mut layout) = setup(SOURCE);
    assert_eq!(library.parts.len(), 1);
    let original = Document::read(SOURCE, 0.0001).unwrap();
    let paths: Vec<_> = original
        .scene
        .shapes
        .iter()
        .filter(|s| s.kind != "Group" && !s.fixed && s.cut_index == 0)
        .flat_map(|s| &s.paths)
        .collect();
    assert_eq!(paths.len(), 5);
    for (mirrored, rotation_radians) in [(false, 0.0), (true, 0.37)] {
        layout.placements[0].transform.mirrored = mirrored;
        layout.placements[0].transform.rotation_radians = rotation_radians;
        let report = request.cutting_report(&library, &layout).unwrap();
        assert!(
            report.validation.valid,
            "{:?}",
            report.validation.violations
        );
        let leads = report.lead_in.as_ref().unwrap();
        assert!(leads.validation.valid && leads.validation.source_checked);
        assert_eq!(leads.expected_contours, 5);
        assert_eq!(leads.reserved_contours, 4);
        assert_eq!(leads.flagged_contours, 1);
        assert!(
            leads.parts[0].plan.flags[0]
                .reason
                .contains("Open cutting contour")
        );
        let review = report.review(&layout, "sheet-0").unwrap();
        let cuts = &review.original_cuts["lead-group-unit-1#0"];
        assert_eq!(cuts.iter().filter(|p| p.closed).count(), 4);
        let transform = Affine::placement(&layout.placements[0].transform);
        for path in &paths {
            let expected = path.curve.transformed(&transform);
            assert!(
                cuts.iter()
                    .filter(|c| c.closed == path.closed)
                    .any(|c| c.curve == expected)
            );
        }
        let files = library
            .export_files(&request, &layout, None, Some(false))
            .unwrap();
        assert_eq!(
            files.iter().map(|f| f.name.as_str()).collect::<Vec<_>>(),
            [
                "lead-group-sheet-1.lbrn2",
                "lead-group-sheet-1-cuts.svg",
                "lead-group-sheet-1-cuts.dxf"
            ]
        );
        let mut preserving: Request =
            serde_json::from_value(serde_json::to_value(&request).unwrap()).unwrap();
        preserving.lead_in = None;
        assert_eq!(
            files[0].text,
            library
                .export_sheet(&preserving, &layout, "sheet-0", "lbrn2", Some(false))
                .unwrap()
        );
        let before = roxmltree::Document::parse(SOURCE).unwrap();
        let after = roxmltree::Document::parse(&files[0].text).unwrap();
        let children = |doc: &roxmltree::Document<'_>| {
            doc.descendants()
                .find(|n| n.has_tag_name("Children"))
                .unwrap()
                .range()
        };
        assert_eq!(&SOURCE[children(&before)], &files[0].text[children(&after)]);
        let svg = roxmltree::Document::parse(&files[1].text).unwrap();
        let d = svg
            .descendants()
            .find(|n| n.attribute("id") == Some("lead-group-unit-1#0"))
            .unwrap()
            .attribute("d")
            .unwrap();
        assert_eq!(d.matches('M').count(), 5);
        assert_eq!(d.matches('Z').count(), 4);
        assert!(files[1].text.contains("id=\"LEADIN\""));
        assert!(files[2].text.contains("LEADIN"));
        let options = Options {
            tolerance: 0.0001,
            ..Default::default()
        };
        for (format, imported) in [
            ("svg", import_svg(&files[1].text, &options)),
            ("dxf", import_dxf(&files[2].text, &options)),
        ] {
            let imported = imported.unwrap();
            assert_eq!(imported.parts.len(), 3, "{format}");
            assert_eq!(
                imported.parts.iter().map(|p| p.holes.len()).sum::<usize>(),
                1,
                "{format}"
            );
            assert_eq!(imported.report.open_contours.len(), 1, "{format}");
            let mut rings: Vec<_> = imported
                .parts
                .iter()
                .flat_map(|p| {
                    std::iter::once(p.polygon.outer.clone()).chain(p.polygon.holes.clone())
                })
                .collect();
            if format == "svg" {
                for ring in &mut rings {
                    for p in ring {
                        p[1] += 400.0;
                    }
                }
            }
            for path in paths.iter().filter(|p| p.closed) {
                let expected = path.curve.transformed(&transform).flatten(0.0001).unwrap();
                assert!(
                    rings.iter().any(|r| hausdorff(&expected, r) < 0.01),
                    "{format} changed original cut geometry"
                );
            }
        }
    }
}

#[test]
fn engraving_text_and_bitmap_bounds_never_become_cut_contours() {
    let (library, request, layout) = setup(include_str!("fixtures/roundtrip.lbrn2"));
    let report = request.cutting_report(&library, &layout).unwrap();
    assert_eq!(report.lead_in.as_ref().unwrap().expected_contours, 3);
    let review = report.review(&layout, "sheet-0").unwrap();
    assert_eq!(
        review.original_cuts.values().map(Vec::len).sum::<usize>(),
        3
    );
    assert!(review.original_cuts.values().any(Vec::is_empty));
    let output = library
        .export_sheet(&request, &layout, "sheet-0", "svg", Some(false))
        .unwrap();
    let imported = import_svg(&output, &Options::default()).unwrap();
    assert_eq!(imported.parts.len(), 3);
    assert!(imported.parts.iter().all(|p| p.holes.is_empty()));
    assert!(imported.report.open_contours.is_empty());
    let scan_only = SOURCE.replace("type=\"Cut\"", "type=\"Scan\"");
    let (library, request, layout) = setup(&scan_only);
    let report = request.cutting_report(&library, &layout).unwrap();
    assert_eq!(report.lead_in.as_ref().unwrap().expected_contours, 0);
    let output = library
        .export_sheet(&request, &layout, "sheet-0", "svg", Some(false))
        .unwrap();
    assert!(!output.contains("<path"));
}
