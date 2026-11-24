use nestbolt_core::import::{Options, decode_drawing, import_dxf, import_svg};

fn drawing(version: &str, codepage: &str, layer: &str) -> String {
    format!(
        "0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\n{version}\n{codepage}9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n8\n{layer}\n70\n1\n90\n4\n10\n0\n20\n0\n10\n20\n20\n0\n10\n20\n20\n10\n10\n0\n20\n10\n0\nENDSEC\n0\nEOF\n"
    )
}

#[test]
fn legacy_declared_and_default_codepages_keep_unicode_layer_names() {
    for page in ["", "9\n$DWGCODEPAGE\n3\nANSI_1252\n"] {
        let original = drawing("AC1009", page, "CUT_Ø_°");
        let (encoded, _, errors) = encoding_rs::WINDOWS_1252.encode(&original);
        assert!(!errors);
        let decoded = decode_drawing("part.dxf", &encoded).unwrap();
        assert_eq!(decoded, original);
        let imported = import_dxf(
            &decoded,
            &Options {
                layers: Some(vec!["cut_ø_°".into()]),
                ..Default::default()
            },
        )
        .unwrap();
        assert_eq!(imported.parts.len(), 1);
        assert_eq!(imported.report.layers[0].name, "CUT_Ø_°");
    }
    let original = drawing("AC1015", "9\n$DWGCODEPAGE\n3\nANSI_1251\n", "CUT_Сталь");
    let (bytes, _, errors) = encoding_rs::WINDOWS_1251.encode(&original);
    assert!(!errors);
    assert_eq!(decode_drawing("part.dxf", &bytes).unwrap(), original);
}

#[test]
fn modern_utf8_ignores_legacy_codepage_and_bad_bytes_have_a_fix() {
    let original = drawing("AC1021", "9\n$DWGCODEPAGE\n3\nANSI_1252\n", "CUT_鋼");
    assert_eq!(
        decode_drawing("part.dxf", original.as_bytes()).unwrap(),
        original
    );
    let mut invalid = original.into_bytes();
    invalid.push(255);
    assert!(
        decode_drawing("part.dxf", &invalid)
            .unwrap_err()
            .to_string()
            .contains("re-export")
    );
    let unknown = drawing("AC1015", "9\n$DWGCODEPAGE\n3\nANSI_9999\n", "CUT");
    assert!(
        decode_drawing("part.dxf", unknown.as_bytes())
            .unwrap_err()
            .to_string()
            .contains("R2007")
    );
    assert!(
        decode_drawing("part.dxf", b"AutoCAD Binary DXF\r\n\x1a\0")
            .unwrap_err()
            .to_string()
            .contains("without its EOF group")
    );
}

#[test]
fn dxf_unicode_escapes_decode_surrogate_pairs_without_loss() {
    let original = drawing("AC1009", "", r"CUT_\U+00D8_\U+D83D\U+DE00");
    let decoded = decode_drawing("part.dxf", original.as_bytes()).unwrap();
    assert!(decoded.contains("CUT_Ø_😀"));
    assert!(
        decode_drawing("part.dxf", original.replace(r"\U+DE00", "").as_bytes())
            .unwrap_err()
            .to_string()
            .contains("Unicode escape")
    );
}

#[test]
fn xml_bom_and_declared_encoding_decode_without_replacement_characters() {
    let svg = r#"<?xml version="1.0" encoding="windows-1252"?><svg width="20mm" viewBox="0 0 20 20"><g id="CUT_Ø"><rect width="10" height="10"/></g></svg>"#;
    let (bytes, _, errors) = encoding_rs::WINDOWS_1252.encode(svg);
    assert!(!errors);
    assert_eq!(decode_drawing("part.svg", &bytes).unwrap(), svg);
    let decoded = decode_drawing("part.svg", &bytes).unwrap();
    assert_eq!(
        import_svg(&decoded, &Options::default())
            .unwrap()
            .parts
            .len(),
        1
    );
    let svg = svg.replace("windows-1252", "UTF-16");
    let mut utf16 = vec![0xff, 0xfe];
    for unit in svg.encode_utf16() {
        utf16.extend(unit.to_le_bytes());
    }
    assert_eq!(decode_drawing("part.svg", &utf16).unwrap(), svg);
    assert!(decode_drawing("part.svg", b"<svg>\xff</svg>").is_err());
    assert_eq!(
        decode_drawing("part.dxf", b"\xef\xbb\xbf0\nEOF\n").unwrap(),
        "0\nEOF\n"
    );
}

#[test]
fn missing_units_suggest_inches_without_rescaling_and_headers_take_precedence() {
    let no_units = drawing("AC1009", "", "CUT").replace("9\n$INSUNITS\n70\n4\n", "");
    let normal = import_dxf(&no_units, &Options::default()).unwrap();
    assert_eq!(normal.parts[0].bounds, [0.0, 0.0, 20.0, 10.0]);
    assert!(normal.report.units.unwrap().possible_inches);
    assert!(normal.warnings.iter().any(|s| s.contains("Choose inches")));
    let inches = import_dxf(
        &no_units,
        &Options {
            dxf_unit: 25.4,
            ..Default::default()
        },
    )
    .unwrap();
    assert_eq!(inches.parts[0].bounds, [0.0, 0.0, 508.0, 254.0]);
    let centimetres =
        drawing("AC1015", "", "CUT").replace("9\n$INSUNITS\n70\n4\n", "9\n$INSUNITS\n70\n5\n");
    let declared = import_dxf(
        &centimetres,
        &Options {
            dxf_unit: 25.4,
            ..Default::default()
        },
    )
    .unwrap();
    assert_eq!(declared.parts[0].bounds, [0.0, 0.0, 200.0, 100.0]);
    let report = declared.report.units.unwrap();
    assert!(report.declared);
    assert!(!report.possible_inches);
    assert_eq!(report.mm_per_unit, 10.0);
}

#[test]
fn every_insunits_length_code_converts_to_millimetres() {
    // Exact definitions: international inch, US survey foot of 1200/3937 m,
    // IAU astronomical unit, Julian light year and parsec of 648000/π au.
    let inch = 25.4;
    let au = 149_597_870_700.0 * 1000.0;
    let expected = [
        (1, inch),
        (2, 12.0 * inch),
        (3, 5280.0 * 12.0 * inch),
        (4, 1.0),
        (5, 10.0),
        (6, 1000.0),
        (7, 1e6),
        (8, inch / 1e6),
        (9, inch / 1000.0),
        (10, 36.0 * inch),
        (11, 1e-7),
        (12, 1e-6),
        (13, 1e-3),
        (14, 100.0),
        (15, 1e4),
        (16, 1e5),
        (17, 1e12),
        (18, au),
        (19, 299_792_458_000.0 * 86_400.0 * 365.25),
        (20, au * 180.0 * 3600.0 / std::f64::consts::PI),
        (21, 1200.0 / 3937.0 * 1000.0),
    ];
    let close = |a: f64, b: f64| (a - b).abs() <= 4.0 * f64::EPSILON * b.abs();
    for (code, mm) in expected {
        // A 20 x 10 mm rectangle drawn in this unit.
        let (w, h) = (20.0 / mm, 10.0 / mm);
        let dxf = format!(
            "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n{code}\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n8\nCUT\n70\n1\n90\n4\n10\n0\n20\n0\n10\n{w:?}\n20\n0\n10\n{w:?}\n20\n{h:?}\n10\n0\n20\n{h:?}\n0\nENDSEC\n0\nEOF\n"
        );
        let import = import_dxf(&dxf, &Options::default()).unwrap();
        let units = import.report.units.unwrap();
        assert!(units.declared);
        assert!(
            close(units.mm_per_unit, mm),
            "{code}: {} mm",
            units.mm_per_unit
        );
        let [x0, y0, x1, y1] = import.parts[0].bounds;
        assert!(x0.abs() < 1e-9 && y0.abs() < 1e-9, "{code}");
        assert!(
            (x1 - 20.0).abs() < 1e-6 && (y1 - 10.0).abs() < 1e-6,
            "{code}: {x1} x {y1}"
        );
    }
    for code in ["22", "-1", "4.5", "mm"] {
        let dxf = drawing("AC1015", "", "CUT")
            .replace("$INSUNITS\n70\n4\n", &format!("$INSUNITS\n70\n{code}\n"));
        let error = import_dxf(&dxf, &Options::default())
            .unwrap_err()
            .to_string();
        assert!(
            error.contains(&format!("unsupported $INSUNITS {code}")),
            "{error}"
        );
        assert!(error.contains("codes 1 to 21"), "{error}");
    }
}
