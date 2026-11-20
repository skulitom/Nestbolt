use nestbolt_core::import::{ImportEntry, ImportReport, Options, import_dxf, import_svg};
use serde_json::{Value, json};

#[test]
fn grouped_svg_warnings_keep_order_and_source_ids() {
    let svg = r##"<svg width="30mm" height="20mm" viewBox="0 0 30 20">
      <use id="broken-use" href="#missing"/>
      <rect width="20" height="10"/>
      <g id="GUIDES" visibility="hidden"><path id="a" d="M0 0h5"/><path id="b" d="M0 1h5"/></g>
      <text id="label">Note</text></svg>"##;
    let import = import_svg(svg, &Options::default()).unwrap();
    let data = serde_json::to_value(&import.report.entries).unwrap();
    assert_eq!(data.as_array().unwrap().len(), import.warnings.len());
    assert_eq!(
        data[0],
        json!({"kind":"unresolved_use","source":{"layer":"0","entity":"use","id":"broken-use"},"href":"#missing"})
    );
    let hidden = data
        .as_array()
        .unwrap()
        .iter()
        .position(|d| d["reason"] == "hidden")
        .unwrap();
    assert_eq!(
        data[hidden],
        json!({"kind":"skipped","source":{"layer":"GUIDES","entity":"path"},"reason":"hidden","count":2})
    );
    assert!(import.warnings[hidden].contains("ignored 2 path"));
    let text = data
        .as_array()
        .unwrap()
        .iter()
        .find(|d| d["reason"] == "not_cut_geometry")
        .unwrap();
    assert_eq!(text["source"]["id"], "label");
    let mut old = serde_json::to_value(&import.report).unwrap();
    old.as_object_mut().unwrap().remove("entries");
    assert!(
        serde_json::from_value::<ImportReport>(old)
            .unwrap()
            .entries
            .is_empty()
    );
}

#[test]
fn dxf_diagnostic_uses_resolved_layer_and_preserves_the_original_sentence() {
    let dxf = "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n\
    0\nSECTION\n2\nBLOCKS\n0\nBLOCK\n2\nplate\n0\nCIRCLE\n10\n0\n20\n0\n40\n5\n\
    0\nSPLINE\n70\n4\n41\n2\n0\nENDBLK\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n\
    0\nINSERT\n8\nCUT:front\n2\nplate\n0\nENDSEC\n0\nEOF\n";
    let import = import_dxf(dxf, &Options::default()).unwrap();
    assert_eq!(import.parts.len(), 1);
    assert_eq!(import.report.entries.len(), import.warnings.len());
    let i = import
        .warnings
        .iter()
        .position(|w| w == "0:SPLINE: rational spline skipped")
        .unwrap();
    assert_eq!(
        serde_json::to_value(&import.report.entries[i]).unwrap(),
        json!({"kind":"skipped","source":{"layer":"CUT:front","entity":"SPLINE"},"reason":"rational_spline","count":1})
    );
}

#[test]
fn preserved_overlap_pairs_identify_their_source_path() {
    let import = import_svg(
        include_str!("fixtures/closed-retrace.svg"),
        &Options::default(),
    )
    .unwrap();
    let i = import
        .warnings
        .iter()
        .position(|w| w.contains("overlapping segment pair"))
        .unwrap();
    let ImportEntry::OverlapsKept { sources } = &import.report.entries[i] else {
        panic!("missing retained-overlap diagnostic")
    };
    assert_eq!(
        sources.len(),
        import.report.cleanup.closed_path_overlaps_preserved
    );
    assert!(
        sources
            .iter()
            .all(|s| s.layer == "0" && s.entity == "path" && s.id.is_none())
    );
    let serialized: Value = serde_json::to_value(&import.report).unwrap();
    let round_trip: ImportReport = serde_json::from_value(serialized).unwrap();
    assert_eq!(round_trip.entries, import.report.entries);
}
