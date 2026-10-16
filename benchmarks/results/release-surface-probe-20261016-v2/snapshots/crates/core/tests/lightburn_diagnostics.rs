use nestbolt_core::{
    curves::Segment,
    lightburn::{Document, UnitPlacement},
};
use nestbolt_validator::RigidTransform;

#[test]
fn missing_handles_explain_native_fallback_without_changing_paths() {
    for (body, controls, straight) in [
        (
            r#"<VertList>V10 0c0x1V15 5c1x1</VertList><PrimList>B0 1</PrimList>"#,
            [[10.0, 0.0], [15.0, 5.0]],
            1,
        ),
        (
            r#"<V vx="10" vy="0"/><V vx="15" vy="5"/><P T="B" p0="0" p1="1"/>"#,
            [[10.0, 0.0], [15.0, 5.0]],
            1,
        ),
        (
            r#"<VertList>V10 0c0x12V15 5c1x1</VertList><PrimList>B0 1</PrimList>"#,
            [[12.0, 0.0], [15.0, 5.0]],
            0,
        ),
        (
            r#"<V vx="10" vy="0" c0x="12"/><V vx="15" vy="5"/><P T="B" p0="0" p1="1"/>"#,
            [[12.0, 0.0], [15.0, 5.0]],
            0,
        ),
    ] {
        let xml = format!(
            r#"<LightBurnProject><CutSetting type="Cut"><index Value="0"/></CutSetting><Shape Type="Path" CutIndex="0">{body}</Shape></LightBurnProject>"#
        );
        let document = Document::read(&xml, 0.0005).unwrap();
        assert_eq!(document.original_xml(), xml);
        assert_eq!(
            document.scene.shapes[0].paths[0].curve.segments[0],
            Segment::Cubic {
                controls,
                to: [15.0, 5.0]
            }
        );
        assert_eq!(document.scene.warnings.len(), 1);
        let warning = &document.scene.warnings[0];
        assert!(
            warning.contains("shape 0")
                && warning.contains("native endpoint fallback")
                && warning.contains("missing Bezier control points")
        );
        assert!(warning.contains("affected segments: 1"));
        assert!(warning.contains(&format!(
            "straight line segments with both controls absent: {straight}"
        )));
    }
}

#[test]
fn proxy_messages_describe_only_artwork_that_uses_rectangles() {
    let source = r#"<LightBurnProject FormatVersion="1">
      <CutSetting type="Cut"><index Value="0"/></CutSetting>
      <CutSetting type="Tool"><index Value="30"/></CutSetting>
      <CutSetting_Img type="Image"><index Value="0"/></CutSetting_Img>
      <Shape Type="Rect" CutIndex="0" W="40" H="30"/>
      <Shape Type="Text" CutIndex="0" Str="attached"><BackupPath Type="Path"><VertList>V0 0V2 0V0 2</VertList><PrimList>LineClosed</PrimList></BackupPath></Shape>
      <Shape Type="Path" CutIndex="0"><XForm>1 0 0 1 100 0</XForm><VertList>V0 0V2 3</VertList><PrimList>LineOpen</PrimList></Shape>
      <Shape Type="Path" CutIndex="30"><VertList>V0 0V2 3</VertList><PrimList>LineOpen</PrimList></Shape>
      <Shape Type="Group"><XForm>1 0 0 1 200 0</XForm><Children>
        <Shape Type="Text" CutIndex="0" Str="grouped"><BackupPath Type="Path"><VertList>V0 0V2 0V0 2</VertList><PrimList>LineClosed</PrimList></BackupPath></Shape>
        <Shape Type="Rect" CutIndex="0" W="40" H="30"/>
      </Children></Shape>
      <Shape Type="Bitmap" CutIndex="0" W="2" H="2" Data="aW1hZ2U="><XForm>1 0 0 1 300 0</XForm></Shape>
    </LightBurnProject>"#;
    let document = Document::read(source, 0.0005).unwrap();
    assert_eq!(document.original_xml(), source);
    let nesting = document.nesting_units(0.0005).unwrap();
    assert_eq!(nesting.units.len(), 4);
    assert_eq!(nesting.units[0].members, [0, 1]);
    assert_eq!(nesting.fixed, [3]);
    let proxies: Vec<_> = nesting
        .warnings
        .iter()
        .filter(|w| w.contains("bounding rectangle"))
        .collect();
    assert_eq!(proxies.len(), 3);
    for index in [2, 5, 7] {
        assert!(
            proxies
                .iter()
                .any(|w| w.starts_with(&format!("LightBurn shape {index} ("))),
            "{proxies:?}"
        );
    }
    let cached: Vec<_> = nesting
        .warnings
        .iter()
        .filter(|w| w.contains("embedded cached font outlines"))
        .collect();
    assert_eq!(cached.len(), 2);
    for index in [1, 5] {
        assert!(
            cached
                .iter()
                .any(|w| w.starts_with(&format!("Text shape {index}:")))
        );
    }
    assert!(
        cached
            .iter()
            .all(|w| w.contains("local fonts are not consulted")
                && w.contains("editable text is preserved"))
    );
    let placements: Vec<_> = nesting
        .units
        .iter()
        .map(|unit| UnitPlacement {
            unit: unit.id,
            transform: RigidTransform::default(),
        })
        .collect();
    assert_eq!(
        nesting
            .write_sheet(&placements, 1000.0, 1000.0, false)
            .unwrap(),
        source
    );
}
