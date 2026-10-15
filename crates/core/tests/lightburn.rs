use nestbolt_core::lightburn::Document;

const PROJECT: &str = r#"<?xml version="1.0" encoding="UTF-8"?>
<!-- Original Nestbolt fixture, MIT; unusual whitespace/unknown XML is intentional. -->
<LightBurnProject FormatVersion="1" MirrorX="True" MirrorY="False" Future="retain">
  <CutSetting type="Cut"><index Value="0"/><name Value="CUT"/><kerf Value="0.2"/><future Value="keep"/></CutSetting>
  <CutSetting_Img type="Image"><index Value="0"/><doOutput Value="1"/></CutSetting_Img>
  <CutSetting type="Scan"><index Value="1"/><SubLayer type="Cut" index="1"/></CutSetting>
  <CutSetting type="Tool"><index Value="30"/></CutSetting>
  <Shape Type="Path" CutIndex="0" VertID="3" PrimID="4" StartV="2"><XForm>1 0 0 1 100 50</XForm></Shape>
  <Shape Type="Group"><XForm>0 1 -1 0 40 20</XForm><Children>
    <Shape Type="Path" CutIndex="0" VertID="3"><XForm>1 0 0 1 0 0</XForm><VertList>V0 0c0x1c1x1V1e1 0SV10 5V0 5</VertList><PrimList>LineClosed</PrimList></Shape>
    <Shape Type="Text" CutIndex="1" Str="cached"><XForm>1 0 0 1 2 3</XForm><BackupPath Type="Path"><XForm>0 1 -1 0 37 22</XForm><VertList>V0 0V1 0V1 2V0 2</VertList><PrimList>LineClosed</PrimList></BackupPath></Shape>
  </Children></Shape>
  <Shape Type="Path" CutIndex="1" PrimID="4"><XForm>1 0 0 1 0 0</XForm><VertList>V0 0V5 0V5 5V0 5</VertList><PrimList>LineClosed</PrimList></Shape>
  <Shape Type="Bitmap" CutIndex="0" SourceHash="0" W="8" H="6"><XForm>1 0 0 1 60 30</XForm></Shape>
  <Shape Type="Bitmap" CutIndex="0" SourceHash="0" Data="aW1hZ2U=" W="8" H="6"><XForm>1 0 0 1 70 30</XForm></Shape>
  <Shape Type="Group"><Children><Shape Type="Rect" CutIndex="30" W="3" H="4"/><Shape Type="Rect" CutIndex="30" W="1" H="2"/></Children></Shape>
  <Unknown><Value escaped="&amp;&quot;">opaque</Value></Unknown>
</LightBurnProject>"#;

fn close(actual: [f64; 4], expected: [f64; 4]) {
    for (a, b) in actual.into_iter().zip(expected) {
        assert!((a - b).abs() < 0.0005, "{actual:?} != {expected:?}");
    }
}

#[test]
fn standalone_open_strokes_have_protected_footprints_and_keep_exact_paths() {
    use nestbolt_core::{curves::Affine, lightburn::UnitPlacement};
    use nestbolt_validator::{Footprint, RigidTransform, Units};
    let source = include_str!("fixtures/open-lines.lbrn2");
    let doc = Document::read(source, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    assert_eq!(nesting.units.len(), 4);
    close(nesting.units[0].bounds_mm, [9.9995, 10.0, 10.0005, 30.0]);
    close(
        nesting.units[1].bounds_mm,
        [20.0, 214.9995095, 40.0, 215.0005095],
    );
    close(nesting.units[2].bounds_mm, [-0.0005, 10.0, 0.0005, 30.0]);
    close(nesting.units[3].bounds_mm, [60.0, 10.0, 72.0, 26.0]);
    for (index, unit) in nesting.units.iter().enumerate() {
        assert_eq!(unit.members, vec![index]);
        assert!(
            Footprint::from_polygons(&unit.geometry, Units::Mm, RigidTransform::default())
                .unwrap()
                .area()
                > 0.0
        );
        let original = &doc.scene.shapes[doc.scene.top_level[index]];
        for mirrored in [false, true] {
            for rotation_radians in [0.0, std::f64::consts::FRAC_PI_2, 0.37] {
                let transform = RigidTransform {
                    translation: [100.0, 80.0],
                    rotation_radians,
                    mirrored,
                };
                let output = nesting
                    .write_sheet(
                        &[UnitPlacement {
                            unit: index,
                            transform,
                        }],
                        300.0,
                        200.0,
                        false,
                    )
                    .unwrap();
                let reread = Document::read(&output, 0.0005).unwrap();
                assert_eq!(reread.scene.top_level.len(), 1);
                let actual = &reread.scene.shapes[0];
                assert_eq!(actual.paths.len(), 1);
                assert!(!actual.paths[0].closed);
                let expected: Vec<_> = original.paths[0]
                    .points(0.0005)
                    .unwrap()
                    .into_iter()
                    .map(|point| Affine::placement(&transform).apply(point))
                    .collect();
                let actual = actual.paths[0].points(0.0005).unwrap();
                assert_eq!(actual.len(), expected.len());
                for (a, b) in actual.iter().zip(expected) {
                    assert!((a[0] - b[0]).hypot(a[1] - b[1]) < 1e-10);
                }
                let xml = roxmltree::Document::parse(source).unwrap();
                let shape = xml
                    .root_element()
                    .children()
                    .filter(|n| n.has_tag_name("Shape"))
                    .nth(index)
                    .unwrap();
                for node in shape
                    .children()
                    .filter(|n| n.has_tag_name("VertList") || n.has_tag_name("PrimList"))
                {
                    assert!(output.contains(&source[node.range()]));
                }
                assert!(!output.contains("Type=\"Rect\""));
            }
        }
    }
    let identity: Vec<_> = nesting
        .units
        .iter()
        .map(|u| UnitPlacement {
            unit: u.id,
            transform: RigidTransform::default(),
        })
        .collect();
    assert_eq!(
        nesting.write_sheet(&identity, 100.0, 100.0, false).unwrap(),
        source
    );
    // The minimum validator-grid padding also protects very small tolerances.
    assert!(doc.nesting_units(1e-9).is_ok());
    let grouped = source.replace("  <Shape Type=\"Path\" CutIndex=\"0\" Label=\"vertical\">", "  <Shape Type=\"Group\"><Children><Shape Type=\"Path\" CutIndex=\"0\" Label=\"vertical\">")
        .replacen("</PrimList></Shape>", "</PrimList></Shape></Children></Shape>", 1);
    let grouped = Document::read(&grouped, 0.0005).unwrap();
    let grouped = grouped.nesting_units(0.0005).unwrap();
    assert_eq!(grouped.units[0].bounds_mm, nesting.units[0].bounds_mm);
    assert_eq!(grouped.units[0].area_mm2, nesting.units[0].area_mm2);
}

#[test]
fn no_op_preserves_every_byte_and_sharing_resolves_independently() {
    let doc = Document::read(PROJECT, 0.0005).unwrap();
    assert_eq!(doc.original_xml().as_bytes(), PROJECT.as_bytes());
    assert_eq!(doc.scene.top_level.len(), 6);
    assert!(doc.scene.mirror_x);
    assert!(!doc.scene.mirror_y);
    assert_eq!(doc.scene.layers.iter().filter(|l| l.index == 0).count(), 2);
    assert!(doc.scene.layers.iter().find(|l| l.index == 1).unwrap().cuts);
    assert_eq!(doc.scene.layers[0].kerf_mm, 0.2);
    let p = &doc.scene.shapes[0];
    close(p.bounds_mm.unwrap(), [100.0, 50.0, 110.0, 55.0]);
    assert_eq!(
        p.paths[0].curve.start,
        [110.0, 55.0],
        "StartV must be honoured"
    );
    let bitmaps: Vec<_> = doc
        .scene
        .shapes
        .iter()
        .filter(|s| s.kind == "Bitmap")
        .collect();
    assert_eq!(bitmaps.len(), 2);
    assert_eq!(bitmaps[0].bitmap_data_bytes, Some(8));
    assert!(bitmaps.iter().all(|s| s.image_layer && !s.fixed));
    close(bitmaps[0].bounds_mm.unwrap(), [56.0, 27.0, 64.0, 33.0]);
    let group = &doc.scene.shapes[*doc.scene.top_level.last().unwrap()];
    assert!(group.fixed);
    assert!(doc.scene.warnings.is_empty());
}

#[test]
fn mixed_fixed_groups_require_regrouping_even_for_the_low_level_writer() {
    let source = include_str!("fixtures/mixed-fixed.lbrn2");
    for xml in [source.to_owned(), source.replace("type=\"Tool\"", "type=\"Cut\"").replace(
        "<index Value=\"30\"/>", "<index Value=\"30\"/><doOutput Value=\"0\"/>"),
        source.replace("<Shape Type=\"Rect\" CutIndex=\"0\" W=\"20\" H=\"10\"/>",
            "<Shape Type=\"Group\"><Children><Shape Type=\"Rect\" CutIndex=\"0\" W=\"20\" H=\"10\"/></Children></Shape>")]
    {
        let doc = Document::read(&xml, 0.0005).unwrap();
        assert_eq!(doc.original_xml(), xml);
        assert!(doc.scene.warnings.iter().any(|w| w.contains("group movable artwork separately")));
        let error = doc.nesting_units(0.0005).err().expect("mixed group must fail");
        assert!(error.to_string().contains("ungroup it in LightBurn"));
    }
    let fixed = source.replace("CutIndex=\"0\" W=\"20\"", "CutIndex=\"30\" W=\"20\"");
    let doc = Document::read(&fixed, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    assert!(nesting.units.is_empty());
    assert_eq!(nesting.fixed, vec![0]);
    assert_eq!(
        nesting.write_sheet(&[], 100.0, 100.0, false).unwrap(),
        fixed
    );
}

#[test]
fn group_transform_and_text_cache_apply_once_and_text_moves_with_its_group() {
    let doc = Document::read(PROJECT, 0.0005).unwrap();
    let text = doc.scene.shapes.iter().find(|s| s.kind == "Text").unwrap();
    close(text.bounds_mm.unwrap(), [35.0, 22.0, 37.0, 23.0]);
    let moved = Document::read(
        &PROJECT.replace("0 1 -1 0 40 20", "0 1 -1 0 140 70"),
        0.0005,
    )
    .unwrap();
    let text = moved
        .scene
        .shapes
        .iter()
        .find(|s| s.kind == "Text")
        .unwrap();
    close(text.bounds_mm.unwrap(), [135.0, 72.0, 137.0, 73.0]);
    assert!(
        moved
            .original_xml()
            .contains("<XForm>0 1 -1 0 37 22</XForm>"),
        "cached XML remains untouched"
    );
}

#[test]
fn legacy_and_compact_cubic_multicontours_have_the_same_geometry() {
    let legacy = r#"<LightBurnProject FormatVersion="0"><Shape Type="Path"><XForm>1 0 0 1 0 0</XForm><V vx="0" vy="0" c0x="2" c0y="3"/><V vx="10" vy="0" c1x="8" c1y="3"/><V vx="20" vy="0"/><V vx="25" vy="0"/><P T="B" p0="0" p1="1"/><P T="L" p0="1" p1="0"/><P T="L" p0="2" p1="3"/></Shape></LightBurnProject>"#;
    let compact = r#"<LightBurnProject FormatVersion="1"><Shape Type="Path"><VertList>V0 0c0x2c0y3V10 0c1x8c1y3V20 0V25 0</VertList><PrimList>B0 1L1 0L2 3</PrimList></Shape></LightBurnProject>"#;
    let a = Document::read(legacy, 0.0005).unwrap();
    let b = Document::read(compact, 0.0005).unwrap();
    assert_eq!(a.scene.shapes[0].paths.len(), 2);
    for (a, b) in a.scene.shapes[0].paths.iter().zip(&b.scene.shapes[0].paths) {
        assert_eq!(a.curve, b.curve);
        assert_eq!(a.closed, b.closed);
    }
    assert!(a.scene.shapes[0].paths[0].closed);
    assert!(!a.scene.shapes[0].paths[1].closed);
    close(a.scene.shapes[0].bounds_mm.unwrap(), [0.0, 0.0, 25.0, 2.25]);
}

#[test]
fn legacy_sheet_conversion_keeps_original_xml_and_only_adds_compact_geometry() {
    use nestbolt_core::lightburn::UnitPlacement;
    use nestbolt_validator::RigidTransform;
    let legacy = include_str!("fixtures/legacy.lbrn");
    for source in [legacy.to_owned(), legacy.replace(" FormatVersion='0'", "")] {
        let doc = Document::read(&source, 0.0005).unwrap();
        assert_eq!(doc.original_xml(), source);
        let nesting = doc.nesting_units(0.0005).unwrap();
        assert_eq!(nesting.units.len(), 1);
        assert_eq!(nesting.units[0].geometry.len(), 2);
        let placement = UnitPlacement {
            unit: 0,
            transform: RigidTransform::default(),
        };
        let output = nesting
            .write_sheet(std::slice::from_ref(&placement), 100.0, 100.0, false)
            .unwrap();
        let modern = Document::read(&output, 0.0005).unwrap();
        assert_eq!(modern.scene.format_version, 1);
        assert_eq!(modern.scene.shapes.len(), doc.scene.shapes.len());
        for (before, after) in doc.scene.shapes.iter().zip(&modern.scene.shapes) {
            assert_eq!(before.bounds_mm, after.bounds_mm);
            assert_eq!(before.paths.len(), after.paths.len());
            for (a, b) in before.paths.iter().zip(&after.paths) {
                assert_eq!(a.curve, b.curve);
                assert_eq!(a.closed, b.closed);
            }
        }
        let xml = roxmltree::Document::parse(&source).unwrap();
        for node in xml.descendants().filter(|n| {
            n.is_element()
                && matches!(
                    n.tag_name().name(),
                    "V" | "P" | "Unknown" | "Notes" | "CutSetting"
                )
        }) {
            assert!(output.contains(&source[node.range()]), "source data lost");
        }
        assert!(output.contains("<!-- keep this comment -->"));
        assert_eq!(output.matches("<VertList>").count(), 2);
        assert_eq!(output.matches("<PrimList>").count(), 2);
        assert_eq!(
            modern
                .nesting_units(0.0005)
                .unwrap()
                .write_sheet(&[placement], 100.0, 100.0, false)
                .unwrap(),
            output,
            "conversion must be idempotent"
        );
    }
}

#[test]
fn legacy_conversion_includes_text_backups_fixed_paths_and_partial_handles() {
    use nestbolt_core::lightburn::UnitPlacement;
    use nestbolt_validator::RigidTransform;
    let legacy = r#"<LightBurnProject FormatVersion="0"><CutSetting type="Tool"><index Value="30"/></CutSetting><Shape Type="Group"><Children><Shape Type="Text" Str="cache" H="2"><BackupPath Type="Path"><V vx="10" vy="0" c0x="12"/><V vx="15" vy="5" c1y="2"/><P T="B" p0="0" p1="1"/><P T="L" p0="1" p1="0"/></BackupPath></Shape></Children></Shape><Shape Type="Path" CutIndex="30"><V vx="0" vy="0" c0x="1"/><V vx="4" vy="4" c1x="1"/><P T="B" p0="0" p1="1"/></Shape></LightBurnProject>"#;
    let doc = Document::read(legacy, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    let transform = RigidTransform {
        translation: [20.0, 40.0],
        rotation_radians: std::f64::consts::FRAC_PI_2,
        mirrored: true,
    };
    let output = nesting
        .write_sheet(&[UnitPlacement { unit: 0, transform }], 100.0, 100.0, false)
        .unwrap();
    let modern = Document::read(&output, 0.0005).unwrap();
    assert_eq!(modern.scene.format_version, 1);
    assert_eq!(output.matches("<VertList>").count(), 2);
    let moved = doc.scene.shapes[1].paths[0]
        .curve
        .transformed(&nestbolt_core::curves::Affine::placement(&transform));
    assert_eq!(modern.scene.shapes[1].paths[0].curve, moved);
    assert_eq!(
        modern.scene.shapes[2].paths[0].curve,
        doc.scene.shapes[2].paths[0].curve
    );
    assert!(output.contains("V0 0c0x1c1x1V4 4c0x1c1x1"));
    assert!(output.contains("V10 0c0x12c1x1V15 5c0x1c1y2"));
}

#[test]
fn circles_rounded_rectangles_polygons_and_open_paths_keep_their_shape() {
    let xml = r#"<LightBurnProject><Shape Type="Ellipse" Rx="10" Ry="5"><XForm>0 1 -1 0 20 30</XForm></Shape><Shape Type="Rect" W="20" H="10" Cr="2"/><Shape Type="Polygon" Rx="10" Ry="10" N="4"/><Shape Type="Path"><VertList>V0 0V10 0V10 10</VertList><PrimList>LineOpen</PrimList></Shape></LightBurnProject>"#;
    let doc = Document::read(xml, 0.0001).unwrap();
    close(
        doc.scene.shapes[0].bounds_mm.unwrap(),
        [15.0, 20.0, 25.0, 40.0],
    );
    close(
        doc.scene.shapes[1].bounds_mm.unwrap(),
        [-10.0, -5.0, 10.0, 5.0],
    );
    close(
        doc.scene.shapes[2].bounds_mm.unwrap(),
        [-10.0, -10.0, 10.0, 10.0],
    );
    assert!(!doc.scene.shapes[3].paths[0].closed);
}

#[test]
fn uncached_text_and_unknown_shapes_are_retained_without_inventing_bounds() {
    let xml = r#"<LightBurnProject><Shape Type="Text" Str="No font dependency" Font="missing"/><Shape Type="FutureShape" Payload="retain"/></LightBurnProject>"#;
    let doc = Document::read(xml, 0.0005).unwrap();
    assert!(
        doc.scene
            .shapes
            .iter()
            .all(|s| !s.geometry_complete && s.bounds_mm.is_none())
    );
    assert!(
        doc.scene
            .warnings
            .iter()
            .any(|w| w.contains("re-save in LightBurn"))
    );
    assert!(
        doc.scene
            .warnings
            .iter()
            .any(|w| w.contains("convert it to paths"))
    );
    assert_eq!(doc.original_xml(), xml);
}

#[test]
fn omitted_zero_handle_coordinates_are_not_missing_handles() {
    use nestbolt_core::curves::Segment;
    let compact = r#"<LightBurnProject><Shape Type="Path"><VertList>V10 0c0x12c1x1V15 5c0x1c1y2</VertList><PrimList>B0 1L1 0</PrimList></Shape></LightBurnProject>"#;
    let legacy = r#"<LightBurnProject><Shape Type="Path"><V vx="10" vy="0" c0x="12"/><V vx="15" vy="5" c1y="2"/><P T="B" p0="0" p1="1"/><P T="L" p0="1" p1="0"/></Shape></LightBurnProject>"#;
    for xml in [compact, legacy] {
        let document = Document::read(xml, 0.0005).unwrap();
        assert_eq!(
            document.scene.shapes[0].paths[0].curve.segments[0],
            Segment::Cubic {
                controls: [[12.0, 0.0], [0.0, 2.0]],
                to: [15.0, 5.0]
            }
        );
    }
}

#[test]
fn corrupt_shared_lists_and_nonfinite_geometry_fail_with_context() {
    for (body, expected) in [
        (
            r#"<Shape Type="Path" VertID="7"/>"#,
            "unresolved LightBurn VertID 7",
        ),
        (
            r#"<Shape Type="Path"><VertList>V0 0V1 0</VertList><PrimList>L0 4</PrimList></Shape>"#,
            "missing vertex",
        ),
        (
            r#"<Shape Type="Bitmap" W="1" H="1" SourceHash="0"/>"#,
            "embed the bitmap",
        ),
        (r#"<Shape Type="Rect" W="NaN" H="1"/>"#, "non-finite"),
        (
            r#"<Shape Type="Path"><VertList>V1e 0</VertList><PrimList>LineClosed</PrimList></Shape>"#,
            "invalid exponent",
        ),
    ] {
        let error = Document::read(
            &format!("<LightBurnProject>{body}</LightBurnProject>"),
            0.0005,
        )
        .err()
        .expect("reject");
        assert!(format!("{error:#}").contains(expected), "{error:#}");
    }
}

#[test]
fn nesting_units_attach_contents_but_preserve_groups_and_fixed_shapes() {
    let xml = r#"<LightBurnProject FormatVersion="1">
      <CutSetting type="Cut"><index Value="0"/></CutSetting>
      <CutSetting type="Scan"><index Value="1"/></CutSetting>
      <CutSetting type="Cut"><index Value="2"/><doOutput Value="0"/></CutSetting>
      <CutSetting_Img type="Image"><index Value="0"/></CutSetting_Img>
      <Shape Type="Rect" CutIndex="0" W="40" H="30"/>
      <Shape Type="Rect" CutIndex="1" W="8" H="6"/>
      <Shape Type="Bitmap" CutIndex="0" W="2" H="2" Data="aW1hZ2U="/>
      <Shape Type="Path" CutIndex="1"><VertList>V-5 0V5 0</VertList><PrimList>LineOpen</PrimList></Shape>
      <Shape Type="Group"><Children><Shape Type="Rect" CutIndex="0" W="4" H="2"/><Shape Type="Rect" CutIndex="0" W="4" H="2"><XForm>1 0 0 1 10 0</XForm></Shape></Children></Shape>
      <Shape Type="Text" CutIndex="2" Str="uncached fixed content"/>
    </LightBurnProject>"#;
    let doc = Document::read(xml, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    assert_eq!(nesting.units.len(), 2);
    assert_eq!(nesting.units[0].members, vec![0, 1, 2, 3]);
    assert_eq!(nesting.units[0].area_mm2, 1200.0);
    assert_eq!(nesting.units[1].members, vec![4]);
    assert_eq!(nesting.units[1].geometry.len(), 2);
    assert_eq!(nesting.units[1].area_mm2, 16.0);
    assert_eq!(nesting.fixed, vec![5]);
    let movable = xml.replace("doOutput Value=\"0\"", "doOutput Value=\"1\"");
    assert!(
        Document::read(&movable, 0.0005)
            .unwrap()
            .nesting_units(0.0005)
            .is_err()
    );
}

#[test]
fn containment_checks_the_whole_rectangle_and_chooses_the_smallest_cut() {
    let xml = r#"<LightBurnProject FormatVersion="1">
      <CutSetting type="Cut"><index Value="0"/></CutSetting>
      <CutSetting type="Scan"><index Value="1"/></CutSetting>
      <Shape Type="Path" CutIndex="0"><VertList>V0 0V10 0V10 10V6 10V6 3V4 3V4 10V0 10</VertList><PrimList>LineClosed</PrimList></Shape>
      <Shape Type="Rect" CutIndex="1" W="8" H="2"><XForm>1 0 0 1 5 6</XForm></Shape>
      <Shape Type="Rect" CutIndex="0" W="6" H="6"><XForm>1 0 0 1 20 10</XForm></Shape>
      <Shape Type="Rect" CutIndex="0" W="8" H="8"><XForm>1 0 0 1 20 10</XForm></Shape>
      <Shape Type="Rect" CutIndex="1" W="2" H="2"><XForm>1 0 0 1 20 10</XForm></Shape>
      <Shape Type="Path" CutIndex="0"><XForm>1 0 0 1 30 0</XForm><VertList>V0 0V10 0V10 10V0 10V3 3V7 3V7 7V3 7</VertList><PrimList>L0 1L1 2L2 3L3 0L4 5L5 6L6 7L7 4</PrimList></Shape>
      <Shape Type="Rect" CutIndex="1" W="2" H="2"><XForm>1 0 0 1 35 5</XForm></Shape>
    </LightBurnProject>"#;
    let doc = Document::read(xml, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    assert_eq!(
        nesting
            .units
            .iter()
            .map(|u| u.members.clone())
            .collect::<Vec<_>>(),
        vec![vec![0], vec![1], vec![2, 4], vec![3], vec![5], vec![6]]
    );
    assert_eq!(nesting.units[4].geometry[0].holes.len(), 1);
    assert!(nesting.warnings.iter().any(|w| w.contains("smallest")));
}

#[test]
fn per_sheet_writer_rehomes_independent_resources_and_keeps_fixed_xml() {
    use nestbolt_core::lightburn::UnitPlacement;
    use nestbolt_validator::RigidTransform;
    let doc = Document::read(PROJECT, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    let t = RigidTransform {
        translation: [200.0, 100.0],
        rotation_radians: std::f64::consts::FRAC_PI_2,
        mirrored: true,
    };
    let output = nesting
        .write_sheet(
            &[
                UnitPlacement {
                    unit: 0,
                    transform: t,
                },
                UnitPlacement {
                    unit: 3,
                    transform: RigidTransform::default(),
                },
            ],
            300.0,
            200.0,
            true,
        )
        .unwrap();
    let reread = Document::read(&output, 0.0005).unwrap();
    assert_eq!(reread.scene.top_level.len(), 4); // two units, fixed group, T1
    let moved = &reread.scene.shapes[0];
    let transform = nestbolt_core::curves::Affine::placement(&t);
    let expected = doc.scene.shapes[0].paths[0].curve.transformed(&transform);
    for (a, b) in moved.paths[0]
        .curve
        .flatten(0.0005)
        .unwrap()
        .iter()
        .zip(expected.flatten(0.0005).unwrap())
    {
        assert!((a[0] - b[0]).hypot(a[1] - b[1]) < 1e-10);
    }
    assert_eq!(reread.scene.shapes[1].bitmap_data_bytes, Some(8));
    assert!(output.contains("VertID=\"3\" PrimID=\"4\" StartV=\"2\""));
    assert!(output.contains("<VertList>V0 0c0x1c1x1V1e1 0SV10 5V0 5</VertList>"));
    assert!(output.contains("<PrimList>LineClosed</PrimList>"));
    assert!(output.contains("SourceHash=\"0\" W=\"8\" H=\"6\" Data=\"aW1hZ2U=\""));
    let fixed = &doc.scene.shapes[*doc.scene.top_level.last().unwrap()];
    assert!(output.contains(&PROJECT[fixed.source_range[0]..fixed.source_range[1]]));
    assert!(output.contains("<Unknown><Value escaped=\"&amp;&quot;\">opaque</Value></Unknown>"));
    let before = roxmltree::Document::parse(PROJECT).unwrap();
    for node in before
        .root_element()
        .children()
        .filter(|n| n.has_tag_name("CutSetting") || n.has_tag_name("CutSetting_Img"))
    {
        assert!(output.contains(&PROJECT[node.range()]));
    }
    assert_eq!(reread.scene.layers.len(), doc.scene.layers.len());
    assert!(reread.scene.mirror_x && !reread.scene.mirror_y);
}

#[test]
fn identity_sheet_is_byte_identical_and_group_children_never_get_transformed() {
    use nestbolt_core::lightburn::UnitPlacement;
    use nestbolt_validator::RigidTransform;
    let doc = Document::read(PROJECT, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    let all: Vec<_> = nesting
        .units
        .iter()
        .map(|u| UnitPlacement {
            unit: u.id,
            transform: RigidTransform::default(),
        })
        .collect();
    assert_eq!(
        nesting.write_sheet(&all, 300.0, 200.0, false).unwrap(),
        PROJECT
    );
    let transform = RigidTransform {
        translation: [100.0, 50.0],
        rotation_radians: 0.0,
        mirrored: false,
    };
    let output = nesting
        .write_sheet(&[UnitPlacement { unit: 1, transform }], 300.0, 200.0, false)
        .unwrap();
    let xml = roxmltree::Document::parse(PROJECT).unwrap();
    let group = xml
        .root_element()
        .children()
        .filter(|n| n.has_tag_name("Shape"))
        .nth(1)
        .unwrap();
    let children = group
        .children()
        .find(|n| n.has_tag_name("Children"))
        .unwrap();
    assert!(output.contains(&PROJECT[children.range()]));
    let reread = Document::read(&output, 0.0005).unwrap();
    close(
        reread
            .scene
            .shapes
            .iter()
            .find(|s| s.kind == "Text")
            .unwrap()
            .bounds_mm
            .unwrap(),
        [135.0, 72.0, 137.0, 73.0],
    );
}

#[test]
fn writer_handles_self_closing_shapes_copies_and_tool_setting_conflicts() {
    use nestbolt_core::lightburn::UnitPlacement;
    use nestbolt_validator::RigidTransform;
    let xml = r#"<LightBurnProject FormatVersion="1"><CutSetting type="Cut"><index Value="0"/></CutSetting><Shape Type="Rect" W="10" H="5" Unknown="a > b &amp; c" /></LightBurnProject>"#;
    let doc = Document::read(xml, 0.0005).unwrap();
    let nesting = doc.nesting_units(0.0005).unwrap();
    let placements: Vec<_> = [20.0, 40.0]
        .map(|x| UnitPlacement {
            unit: 0,
            transform: RigidTransform {
                translation: [x, 20.0],
                ..Default::default()
            },
        })
        .into();
    let output = nesting.write_sheet(&placements, 100.0, 50.0, true).unwrap();
    assert_eq!(output.matches("Unknown=\"a > b &amp; c\"").count(), 2);
    let reread = Document::read(&output, 0.0005).unwrap();
    assert_eq!(reread.scene.top_level.len(), 3);
    assert_eq!(
        reread
            .scene
            .layers
            .iter()
            .find(|l| l.index == 30)
            .unwrap()
            .mode,
        "Tool"
    );
    close(
        reread.scene.shapes[0].bounds_mm.unwrap(),
        [15.0, 17.5, 25.0, 22.5],
    );
    let bad = xml.replace(
        "</LightBurnProject>",
        "<CutSetting type=\"Cut\"><index Value=\"30\"/></CutSetting></LightBurnProject>",
    );
    let bad = Document::read(&bad, 0.0005).unwrap();
    assert!(
        bad.nesting_units(0.0005)
            .unwrap()
            .write_sheet(&[], 100.0, 50.0, true)
            .is_err()
    );
    assert!(
        nesting
            .write_sheet(
                &[UnitPlacement {
                    unit: 99,
                    transform: RigidTransform::default()
                }],
                100.0,
                50.0,
                false
            )
            .is_err()
    );
}

#[test]
fn tool_setting_precedes_shapes_and_outline_precedes_trailing_notes() {
    use nestbolt_core::lightburn::UnitPlacement;
    use nestbolt_validator::RigidTransform;
    for xml in [
        r#"<LightBurnProject FormatVersion="1"><Shape Type="Rect" W="10" H="5"/><Notes Notes="keep"/><Future/></LightBurnProject>"#,
        r#"<LightBurnProject FormatVersion="1"><Notes Notes="keep"/><Future/></LightBurnProject>"#,
        r#"<LightBurnProject FormatVersion="1"><CutSetting type="Cut"><index Value="0"/></CutSetting><Notes Notes="keep"/><Future/></LightBurnProject>"#,
        r#"<LightBurnProject FormatVersion="1"/>"#,
    ] {
        let doc = Document::read(xml, 0.0005).unwrap();
        let nesting = doc.nesting_units(0.0005).unwrap();
        let placements: Vec<_> = nesting
            .units
            .iter()
            .map(|u| UnitPlacement {
                unit: u.id,
                transform: RigidTransform::default(),
            })
            .collect();
        let output = nesting.write_sheet(&placements, 100.0, 50.0, true).unwrap();
        let tree = roxmltree::Document::parse(&output).unwrap();
        let children: Vec<_> = tree
            .root_element()
            .children()
            .filter(|n| n.is_element())
            .collect();
        let setting = children
            .iter()
            .position(|n| n.has_tag_name("CutSetting"))
            .unwrap();
        let first_shape = children
            .iter()
            .position(|n| n.has_tag_name("Shape"))
            .unwrap();
        let outline = children
            .iter()
            .position(|n| n.attribute("CutIndex") == Some("30"))
            .unwrap();
        assert!(setting < first_shape);
        assert!(
            children
                .iter()
                .enumerate()
                .filter(|(_, n)| n.has_tag_name("CutSetting"))
                .all(|(i, _)| i < first_shape)
        );
        if let Some(notes) = children.iter().position(|n| n.has_tag_name("Notes")) {
            assert!(outline < notes);
            assert!(output.contains("<Notes Notes=\"keep\"/><Future/>"));
        }
    }
}
