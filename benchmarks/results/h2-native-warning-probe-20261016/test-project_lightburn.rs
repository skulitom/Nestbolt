use nestbolt_core::{
    import::Options,
    lightburn::Document,
    project::{Library, Request},
};
use nestbolt_validator::{
    RigidTransform, Units,
    job::{Layout, Placement, Sheet},
};

const SOURCE: &str = include_str!("fixtures/roundtrip.lbrn2");

fn fixture() -> (Library, Request, Layout) {
    let library = Library::import(
        &[("roundtrip.lbrn2".into(), SOURCE.into())],
        &Options::default(),
    )
    .unwrap();
    assert_eq!(library.parts.len(), 3);
    let request: Request = serde_json::from_value(serde_json::json!({
        "sheets":[{"width_mm":40,"height_mm":32}], "spacing_mm":1,"edge_spacing_mm":0.5
    }))
    .unwrap();
    let layout = Layout {
        version: 1,
        units: Units::Mm,
        sheets: (0..3)
            .map(|i| Sheet {
                id: format!("s{i}"),
                stock_id: "sheet-type-1".into(),
            })
            .collect(),
        placements: library
            .parts
            .iter()
            .enumerate()
            .map(|(i, p)| Placement {
                part_id: p.id.clone(),
                copy_index: 0,
                sheet_id: format!("s{i}"),
                transform: RigidTransform {
                    translation: [1.0 - p.bounds_mm[0], 1.0 - p.bounds_mm[1]],
                    ..Default::default()
                },
            })
            .collect(),
    };
    (library, request, layout)
}

#[test]
fn rigid_components_and_source_settings_survive_library_and_per_sheet_exports() {
    let (library, request, layout) = fixture();
    assert_eq!(library.parts[0].geometry().len(), 2);
    assert_eq!(library.parts[0].area_mm2, 200.0);
    let library: Library = serde_json::from_str(&serde_json::to_string(&library).unwrap()).unwrap();
    let project = library.lightburn.as_ref().unwrap();
    assert_eq!(project.xml, SOURCE);
    assert_eq!(project.fixed_top_level, 1);
    assert_eq!(project.layers[0].kerf_mm, 0.2);
    let (job, _) = request.job(&library).unwrap();
    assert_eq!(job.parts[0].geometry.len(), 2);
    assert!(
        nestbolt_validator::job::validate(&job, &layout)
            .unwrap()
            .valid
    );
    let files = library.export_files(&request, &layout, None, None).unwrap();
    assert_eq!(files.len(), 3);
    let source = roxmltree::Document::parse(SOURCE).unwrap();
    let settings: Vec<_> = source
        .root_element()
        .children()
        .filter(|n| {
            n.has_tag_name("CutSetting")
                || n.has_tag_name("CutSetting_Img")
                || n.has_tag_name("Unknown")
                || n.has_tag_name("Notes")
        })
        .map(|n| &SOURCE[n.range()])
        .collect();
    for (i, file) in files.iter().enumerate() {
        assert_eq!(file.name, format!("roundtrip-sheet-{}.lbrn2", i + 1));
        assert!(settings.iter().all(|s| file.text.contains(s)));
        let reread = Document::read(&file.text, 0.005).unwrap();
        assert!(reread.scene.mirror_x);
        assert!(!reread.scene.mirror_y);
        assert!(
            reread
                .scene
                .shapes
                .iter()
                .any(|s| s.fixed && s.bounds_mm == Some([-11.5, -12.0, -8.5, -8.0]))
        );
        assert!(
            reread
                .scene
                .shapes
                .iter()
                .any(|s| s.fixed && s.bounds_mm == Some([0.0, 0.0, 40.0, 32.0]))
        );
    }
    let children = source
        .descendants()
        .find(|n| n.has_tag_name("Children"))
        .unwrap();
    assert!(files[0].text.contains(&SOURCE[children.range()]));
    let backup = source
        .descendants()
        .find(|n| n.has_tag_name("BackupPath"))
        .unwrap();
    assert!(files[1].text.contains(&SOURCE[backup.range()]));
    assert!(!files[2].text.contains("Type=\"Text\""));
    let bitmap = Document::read(&files[2].text, 0.005).unwrap();
    assert!(
        bitmap
            .scene
            .shapes
            .iter()
            .any(|s| s.kind == "Bitmap" && s.bitmap_data_bytes.is_some())
    );
    let no_outline = library
        .export_sheet(&request, &layout, "s0", "lbrn2", Some(false))
        .unwrap();
    assert!(
        !Document::read(&no_outline, 0.005)
            .unwrap()
            .scene
            .shapes
            .iter()
            .any(|s| s.bounds_mm == Some([0.0, 0.0, 40.0, 32.0]))
    );
}

#[test]
fn source_xml_drives_validation_and_incomplete_or_lossy_exports_are_refused() {
    let (mut library, request, mut layout) = fixture();
    let (original, _) = request.job(&library).unwrap();
    library.parts[0].components.clear();
    library.parts[0].polygon.outer = vec![[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]];
    let (rederived, _) = request.job(&library).unwrap();
    assert_eq!(
        serde_json::to_value(original).unwrap(),
        serde_json::to_value(rederived).unwrap()
    );
    assert!(
        library
            .export_files(&request, &layout, Some("svg"), None)
            .unwrap_err()
            .to_string()
            .contains("retain its text")
    );
    layout.placements[0].transform.translation = [1000.0, 1000.0];
    assert!(
        library
            .export_files(&request, &layout, None, None)
            .unwrap_err()
            .to_string()
            .contains("independent validation")
    );
    assert!(
        Library::import(
            &[
                ("a.lbrn2".into(), SOURCE.into()),
                ("b.svg".into(), "".into())
            ],
            &Options::default()
        )
        .unwrap_err()
        .to_string()
        .contains("one LightBurn")
    );
    assert!(
        Library::import(
            &[("a.lbrn2".into(), SOURCE.into())],
            &Options {
                layers: Some(vec!["CUT".into()]),
                ..Default::default()
            }
        )
        .unwrap_err()
        .to_string()
        .contains("clear the SVG/DXF")
    );
    library.parts[1].id = library.parts[0].id.clone();
    assert!(
        request
            .job(&library)
            .unwrap_err()
            .to_string()
            .contains("unit mapping")
    );
}

#[test]
fn missing_source_and_mixed_fixed_groups_fail_before_nesting() {
    let (mut library, request, _) = fixture();
    library.lightburn = None;
    assert!(
        request
            .job(&library)
            .unwrap_err()
            .to_string()
            .contains("original LightBurn")
    );
    let source = SOURCE.replacen(
        "Type=\"Rect\" CutIndex=\"0\" W=\"10\"",
        "Type=\"Rect\" CutIndex=\"30\" W=\"10\"",
        1,
    );
    assert!(
        Library::import(&[("mixed.lbrn2".into(), source)], &Options::default())
            .unwrap_err()
            .to_string()
            .contains("group movable artwork separately")
    );
}
