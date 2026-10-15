use nestbolt_core::{
    import::Options,
    project::{Library, Request},
};
use nestbolt_validator::{
    Footprint, RigidTransform,
    job::{Layout, Placement, Sheet},
};
use serde_json::json;

#[test]
fn final_common_starts_are_exported_from_each_copy_and_offcuts_use_reserved_space() {
    let library = Library::import(
        &[(
            "panel.svg".into(),
            include_str!("fixtures/common-panels.svg").into(),
        )],
        &Options::default(),
    )
    .unwrap();
    let request:Request=serde_json::from_value(json!({"parts":[{"id":"panel-1","quantity":2}],
        "sheets":[{"width_mm":100,"height_mm":50}],"common_line":{"kerf_mm":0.2},"lead_in":{"kerf_mm":0.2},"edge_spacing_mm":1})).unwrap();
    let prepared = request.prepare(&library).unwrap();
    let bounds = Footprint::from_polygons(
        &prepared.job.parts[0].geometry,
        prepared.job.units,
        RigidTransform::default(),
    )
    .unwrap()
    .bounds();
    let layout = Layout {
        version: 1,
        units: prepared.job.units,
        sheets: vec![Sheet {
            id: "sheet-0".into(),
            stock_id: "sheet-type-1".into(),
        }],
        placements: [0.0, 40.2]
            .iter()
            .enumerate()
            .map(|(i, x)| Placement {
                part_id: "panel-1".into(),
                copy_index: i as u32,
                sheet_id: "sheet-0".into(),
                transform: RigidTransform {
                    translation: [5.0 + x - bounds[0], 5.0 - bounds[1]],
                    ..Default::default()
                },
            })
            .collect(),
    };
    let checked = prepared.report(&layout).unwrap();
    let leads = checked.lead_in.as_ref().unwrap();
    assert_eq!(leads.reserved_contours, 2);
    assert_eq!(leads.flagged_contours, 0);
    assert!((checked.common_line.as_ref().unwrap()[0].saved_length_mm - 30.0).abs() < 0.01);
    let review = checked.review(&layout, "sheet-0").unwrap();
    assert!(!review.common.is_empty());
    let text = library
        .export_sheet(&request, &layout, "sheet-0", "svg", Some(false))
        .unwrap();
    let xml = roxmltree::Document::parse(&text).unwrap();
    for (p, lead) in layout.placements.iter().zip(&review.leadin) {
        let id = format!("{}#{}", p.part_id, p.copy_index);
        let d = xml
            .descendants()
            .find(|n| n.attribute("id") == Some(&id))
            .unwrap()
            .attribute("d")
            .unwrap();
        let svgtypes::PathSegment::MoveTo { x, y, .. } =
            svgtypes::PathParser::from(d).next().unwrap().unwrap()
        else {
            panic!("missing start")
        };
        let end = lead.end();
        assert!((x - end[0]).hypot(y - (50.0 - end[1])) < 1e-6);
    }
    assert!(text.contains("id=\"COMMON\""));
    assert!(text.contains("id=\"LEADIN\""));
    let files = library
        .export_files(&request, &layout, None, Some(false))
        .unwrap();
    assert_eq!(files[0].text, text);
    assert!(files[1].text.contains("LEADIN"));
    assert!((checked.validation.metrics.unwrap().placed_area - 2400.0).abs() < 1e-6);
}

#[test]
fn lead_request_rejects_invalid_options_and_accepts_preserved_project_sidecars() {
    let svg = Library::import(
        &[(
            "panel.svg".into(),
            include_str!("fixtures/common-panels.svg").into(),
        )],
        &Options::default(),
    )
    .unwrap();
    for lead in [
        json!({"kerf_mm":0}),
        json!({"kerf_mm":0.2,"length_mm":0.4}),
        json!({"kerf_mm":0.2,"hole_angle_degrees":91}),
    ] {
        let r: Request = serde_json::from_value(
            json!({"sheets":[{"width_mm":100,"height_mm":50}],"lead_in":lead}),
        )
        .unwrap();
        assert!(r.prepare(&svg).is_err());
    }
    let r:Request=serde_json::from_value(json!({"sheets":[{"width_mm":100,"height_mm":50}],"common_line":{"kerf_mm":0.3},"lead_in":{"kerf_mm":0.2}})).unwrap();
    assert!(
        r.prepare(&svg)
            .err()
            .unwrap()
            .to_string()
            .contains("same kerf")
    );
    let lb = Library::import(
        &[(
            "project.lbrn2".into(),
            include_str!("fixtures/roundtrip.lbrn2").into(),
        )],
        &Options::default(),
    )
    .unwrap();
    let r: Request = serde_json::from_value(
        json!({"sheets":[{"width_mm":100,"height_mm":50}],"lead_in":{"kerf_mm":0.2}}),
    )
    .unwrap();
    assert!(r.prepare(&lb).is_ok());
}
