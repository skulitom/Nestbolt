use nestbolt_core::import::{
    FailureReason, ImportEntry, ImportFailed, ImportSource, Options, SkipReason, import_dxf,
    import_svg,
};

/// A millimetre DXF whose layer table defines `layers`, all colour 7.
fn dxf(layers: &[&str], entities: &str) -> String {
    let table: String = layers
        .iter()
        .map(|name| format!("0\nLAYER\n2\n{name}\n70\n0\n62\n7\n"))
        .collect();
    format!(
        "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n\
         0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n{table}0\nENDTAB\n0\nENDSEC\n\
         0\nSECTION\n2\nENTITIES\n{entities}0\nENDSEC\n0\nEOF\n"
    )
}

fn line(layer: &str, from: [f64; 2], to: [f64; 2]) -> String {
    format!(
        "0\nLINE\n8\n{layer}\n10\n{}\n20\n{}\n11\n{}\n21\n{}\n",
        from[0], from[1], to[0], to[1]
    )
}

fn failure(result: anyhow::Result<nestbolt_core::import::Import>) -> (String, ImportFailed) {
    let error = result.unwrap_err();
    let failed = error
        .downcast_ref::<ImportFailed>()
        .expect("the error carries its import report")
        .clone();
    assert_eq!(format!("{error:#}"), error.to_string());
    (error.to_string(), failed)
}

#[test]
fn rectangle_left_open_reports_its_gap() {
    // A 100 x 50 mm rectangle whose last LINE stops 0.15 mm short of the first.
    let corners = [
        [0.0, 0.0],
        [100.0, 0.0],
        [100.0, 50.0],
        [0.0, 50.0],
        [0.0, 0.15],
    ];
    let entities: String = corners
        .windows(2)
        .map(|w| line("1 - CORTE", w[0], w[1]))
        .collect();
    let options = Options {
        close_gaps_mm: Some(0.1),
        ..Options::default()
    };
    let (message, failed) = failure(import_dxf(&dxf(&["1 - CORTE"], &entities), &options));
    let warning = "1 - CORTE:LINE: open path from (0.000000, 0.000000) to (0.000000, 0.150000); \
                   end gap 0.150000 mm; enable Close gaps up to 0.150000 mm. This contour was not imported";
    assert_eq!(
        message,
        format!(
            "no closed part outlines found; repair the cut outlines or re-export the drawing \
             with closed, nonzero-area geometry; {warning}"
        )
    );
    assert_eq!(failed.reason, FailureReason::NoClosedOutlines);
    assert_eq!(failed.warnings, [warning]);
    let report = &failed.report;
    assert_eq!(report.entries, [ImportEntry::OpenContour { contour: 0 }]);
    assert_eq!(report.close_gaps_mm, Some(0.1));
    assert!(report.closed_gaps.is_empty());
    let [open] = report.open_contours.as_slice() else {
        panic!("one open contour: {:?}", report.open_contours)
    };
    assert_eq!(open.source, "1 - CORTE:LINE");
    assert_eq!(open.start_mm, [0.0, 0.0]);
    assert_eq!(open.end_mm, [0.0, 0.15]);
    assert!((open.end_gap_mm - 0.15).abs() < 1e-12);
    assert_eq!(open.suggested_close_gaps_mm, Some(0.15));
    let [layer] = report.layers.as_slice() else {
        panic!("one layer: {:?}", report.layers)
    };
    assert_eq!(
        (layer.name.as_str(), layer.selected_entities),
        ("1 - CORTE", 4)
    );
    let units = report.units.as_ref().unwrap();
    assert!(units.declared);
    assert_eq!(units.mm_per_unit, 1.0);
    assert_eq!(units.largest_dimension_in_drawing_units, None);
}

#[test]
fn failure_keeps_every_warning_past_the_eighth() {
    let entities: String = (0..10)
        .map(|i| line("CUT", [0.0, 10.0 * i as f64], [20.0, 10.0 * i as f64]))
        .collect();
    let (message, failed) = failure(import_dxf(&dxf(&["CUT"], &entities), &Options::default()));
    assert_eq!(failed.reason, FailureReason::NoClosedOutlines);
    assert_eq!(failed.warnings.len(), 10);
    assert_eq!(failed.report.entries.len(), 10);
    assert_eq!(failed.report.open_contours.len(), 10);
    assert!(
        failed
            .warnings
            .iter()
            .all(|w| w.starts_with("CUT:LINE: open path from"))
    );
    // The message still lists only the first eight.
    assert_eq!(
        message,
        format!(
            "no closed part outlines found; repair the cut outlines or re-export the drawing \
             with closed, nonzero-area geometry; {}",
            failed.warnings[..8].join("; ")
        )
    );
}

#[test]
fn nothing_to_cut_on_the_chosen_layer_reports_why() {
    let entities = "0\nLWPOLYLINE\n8\nCUT\n90\n4\n70\n1\n\
                    10\n0\n20\n0\n10\n100\n20\n0\n10\n100\n20\n50\n10\n0\n20\n50\n\
                    0\nTEXT\n8\nNOTES\n10\n10\n20\n10\n40\n5\n1\nNote\n";
    let options = Options {
        layers: Some(vec!["NOTES".into()]),
        ..Options::default()
    };
    let (message, failed) = failure(import_dxf(&dxf(&["CUT", "NOTES"], entities), &options));
    // The TEXT warning holds "; " itself.
    let text = "ignored 1 TEXT on layer \"NOTES\": not a cut outline; explode/convert it to \
                closed paths in the source drawing if it must be cut";
    let excluded = "ignored 1 geometry on layer \"CUT\", colour aci:7: excluded by cut selection";
    assert_eq!(
        message,
        format!(
            "no cutting geometry selected; choose a layer/colour containing closed outlines or \
             convert text to paths. Layers: CUT, NOTES; colours: aci:7. {text}; {excluded}"
        )
    );
    assert_eq!(failed.reason, FailureReason::NoCuttingGeometry);
    assert_eq!(failed.warnings, [text, excluded]);
    let report = &failed.report;
    assert_eq!(
        report.entries,
        [
            ImportEntry::Skipped {
                source: ImportSource {
                    layer: "NOTES".into(),
                    entity: "TEXT".into(),
                    id: None,
                },
                reason: SkipReason::NotCutGeometry,
                count: 1,
            },
            ImportEntry::NotSelected {
                layer: "CUT".into(),
                color: "aci:7".into(),
                count: 1,
            },
        ]
    );
    assert_eq!(report.selection_mode, "explicit");
    let layers: Vec<_> = report
        .layers
        .iter()
        .map(|l| {
            (
                l.name.as_str(),
                l.entities,
                l.geometry_entities,
                l.selected_entities,
            )
        })
        .collect();
    assert_eq!(layers, [("CUT", 1, 1, 0), ("NOTES", 1, 0, 0)]);
    assert!(report.open_contours.is_empty());
    assert!(report.units.as_ref().unwrap().declared);
}

#[test]
fn svg_failures_carry_the_report_too() {
    let (message, failed) = failure(import_svg(
        r#"<svg width="30mm" height="30mm" viewBox="0 0 30 30"><path id="open" d="M0 0 H20 V20 H0"/></svg>"#,
        &Options::default(),
    ));
    assert_eq!(failed.reason, FailureReason::NoClosedOutlines);
    assert!(message.starts_with("no closed part outlines found; "));
    assert_eq!(failed.report.open_contours.len(), 1);
    assert_eq!(failed.report.open_contours[0].source, "open");
    assert_eq!(
        failed.report.entries,
        [ImportEntry::OpenContour { contour: 0 }]
    );

    let (message, failed) = failure(import_svg(
        r#"<svg width="30mm" height="30mm" viewBox="0 0 30 30"><text id="label">Note</text></svg>"#,
        &Options::default(),
    ));
    assert_eq!(failed.reason, FailureReason::NoCuttingGeometry);
    assert!(message.starts_with("no cutting geometry selected; "));
    assert_eq!(failed.warnings.len(), failed.report.entries.len());
    assert!(matches!(
        &failed.report.entries[..],
        [ImportEntry::Skipped {
            reason: SkipReason::NotCutGeometry,
            ..
        }]
    ));
}
