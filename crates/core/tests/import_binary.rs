//! Binary DXF files written byte by byte, compared with the same drawing as
//! ASCII text. Layout from Autodesk's "About Binary DXF Files"; value types
//! from its "Group Code Value Types" table and ezdxf's `lldxf/types.py`.
use nestbolt_core::import::{Options, decode_drawing, import_dxf};
use proptest::prelude::*;

const SENTINEL: &[u8] = b"AutoCAD Binary DXF\r\n\x1a\0";

/// A group value in the type its group code gives it.
#[derive(Clone, Copy)]
enum V<'a> {
    S(&'a [u8]),
    Bool(u8),
    I16(i16),
    I32(i32),
    I64(i64),
    F(f64),
    Chunk(&'a [u8]),
}

use V::*;

/// R12 writes one-byte group codes, with 255 before a two-byte extended data
/// code; R13 and later write every code in two bytes, least significant first.
fn binary(one_byte_codes: bool, tags: &[(u16, V)]) -> Vec<u8> {
    let mut out = SENTINEL.to_vec();
    for &(code, value) in tags {
        match u8::try_from(code) {
            Ok(code) if one_byte_codes && code != 255 => out.push(code),
            _ if one_byte_codes => {
                out.push(255);
                out.extend(code.to_le_bytes());
            }
            _ => out.extend(code.to_le_bytes()),
        }
        match value {
            S(s) => {
                out.extend(s);
                out.push(0);
            }
            Bool(b) => out.push(b),
            I16(v) => out.extend(v.to_le_bytes()),
            I32(v) => out.extend(v.to_le_bytes()),
            I64(v) => out.extend(v.to_le_bytes()),
            F(v) => out.extend(v.to_le_bytes()),
            Chunk(data) => {
                out.push(u8::try_from(data.len()).unwrap());
                out.extend(data);
            }
        }
    }
    out
}

/// The same tags as ASCII DXF, binary chunks in hex.
fn ascii(tags: &[(u16, V)]) -> Vec<u8> {
    let mut out = vec![];
    for &(code, value) in tags {
        out.extend(format!("{code}\n").bytes());
        match value {
            S(s) => out.extend(s),
            Bool(b) => out.extend(b.to_string().bytes()),
            I16(v) => out.extend(v.to_string().bytes()),
            I32(v) => out.extend(v.to_string().bytes()),
            I64(v) => out.extend(v.to_string().bytes()),
            F(v) => out.extend(v.to_string().bytes()),
            Chunk(data) => out.extend(data.iter().flat_map(|b| format!("{b:02X}").into_bytes())),
        }
        out.push(b'\n');
    }
    out
}

fn assert_same_drawing(one_byte_codes: bool, tags: &[(u16, V)]) -> String {
    assert_binary_reads_as(one_byte_codes, tags, tags)
}

/// Decoding the binary file gives the ASCII file's text, doubles parsing to
/// the same f64 bits, and both import identically.
fn assert_binary_reads_as(
    one_byte_codes: bool,
    tags: &[(u16, V)],
    ascii_tags: &[(u16, V)],
) -> String {
    let from_binary = decode_drawing("part.dxf", &binary(one_byte_codes, tags)).unwrap();
    let from_ascii = decode_drawing("part.dxf", &ascii(ascii_tags)).unwrap();
    let (b, a): (Vec<_>, Vec<_>) = (from_binary.lines().collect(), from_ascii.lines().collect());
    assert_eq!(b.len(), a.len(), "{from_binary}");
    for (i, &(code, value)) in tags.iter().enumerate() {
        assert_eq!(b[2 * i], code.to_string());
        if let F(v) = value {
            let parsed: f64 = b[2 * i + 1].parse().unwrap();
            assert_eq!(
                parsed.to_bits(),
                v.to_bits(),
                "group {code}: {}",
                b[2 * i + 1]
            );
        } else {
            assert_eq!(b[2 * i + 1], a[2 * i + 1], "group {code}");
        }
    }
    let import =
        |text: &str| serde_json::to_value(import_dxf(text, &Options::default()).unwrap()).unwrap();
    assert_eq!(import(&from_binary), import(&from_ascii));
    from_binary
}

/// A 20 x 10 mm plate with a bulged edge and a circular hole, on layer CUT,
/// with extended data on the circle (two-byte codes behind 255 in R12).
fn plate<'a>(
    version: &'a [u8],
    layer: &'a [u8],
    codepage: &'a [u8],
    r12: bool,
) -> Vec<(u16, V<'a>)> {
    let mut tags = vec![
        (0, S(b"SECTION")),
        (2, S(b"HEADER")),
        (9, S(b"$ACADVER")),
        (1, S(version)),
    ];
    if !codepage.is_empty() {
        tags.extend([(9, S(b"$DWGCODEPAGE")), (3, S(codepage))]);
    }
    tags.extend([
        (9, S(b"$INSUNITS")),
        (70, I16(4)),
        (0, S(b"ENDSEC")),
        (0, S(b"SECTION")),
        (2, S(b"ENTITIES")),
    ]);
    let corners = [
        (0.0, 0.0, 0.0),
        (20.0, 0.0, 0.5),
        (20.0, 10.0, 0.0),
        (0.0, 10.0, 1.0 / 3.0),
    ];
    if r12 {
        tags.extend([
            (0, S(b"POLYLINE")),
            (8, S(layer)),
            (66, I16(1)),
            (70, I16(1)),
        ]);
        for (x, y, bulge) in corners {
            tags.extend([
                (0, S(b"VERTEX")),
                (8, S(layer)),
                (10, F(x)),
                (20, F(y)),
                (42, F(bulge)),
            ]);
        }
        tags.push((0, S(b"SEQEND")));
    } else {
        tags.extend([
            (0, S(b"LWPOLYLINE")),
            (8, S(layer)),
            (90, I32(4)),
            (70, I16(1)),
        ]);
        for (x, y, bulge) in corners {
            tags.extend([(10, F(x)), (20, F(y)), (42, F(bulge))]);
        }
    }
    tags.extend([
        (0, S(b"CIRCLE")),
        (8, S(layer)),
        (10, F(10.1)),
        (20, F(4.9)),
        (30, F(0.0)),
        (40, F(2.5)),
        (1001, S(b"NESTBOLT")),
        (1000, S(b"note")),
        (1070, I16(-2)),
        (1071, I32(-70_000)),
        (1040, F(0.1)),
        (1010, F(1.0)),
        (1020, F(2.0)),
        (1030, F(3.0)),
        (0, S(b"ENDSEC")),
        (0, S(b"EOF")),
    ]);
    tags
}

#[test]
fn r12_and_r13_binary_files_import_like_their_ascii_text() {
    for (version, r12) in [
        (&b"AC1009"[..], true),
        (b"AC1015", false),
        (b"AC1032", false),
    ] {
        let text = assert_same_drawing(r12, &plate(version, b"CUT", b"", r12));
        let import = import_dxf(&text, &Options::default()).unwrap();
        assert_eq!(
            import.parts.len(),
            1,
            "{}",
            String::from_utf8_lossy(version)
        );
        assert_eq!(import.parts[0].holes.len(), 1);
    }
}

#[test]
fn binary_strings_follow_the_ascii_encoding_rules() {
    // R2007 and later are UTF-8 whatever $DWGCODEPAGE says.
    let layer = "CUT_鋼".as_bytes();
    let text = assert_same_drawing(false, &plate(b"AC1021", layer, b"ANSI_1252", false));
    assert!(text.contains("\n8\nCUT_鋼\n"));
    // Earlier versions use $DWGCODEPAGE.
    let (layer, _, errors) = encoding_rs::WINDOWS_1252.encode("CUT_Ø_°");
    assert!(!errors);
    let text = assert_same_drawing(false, &plate(b"AC1018", &layer, b"ANSI_1252", false));
    let import = import_dxf(
        &text,
        &Options {
            layers: Some(vec!["cut_ø_°".into()]),
            ..Default::default()
        },
    )
    .unwrap();
    assert_eq!(import.parts.len(), 1);
    assert_eq!(import.report.layers[0].name, "CUT_Ø_°");
}

#[test]
fn binary_chunks_booleans_and_64_bit_integers_take_their_own_widths() {
    let mut tags = plate(b"AC1032", b"CUT", b"", false);
    // A boolean header variable, then proxy graphics on the circle: a 64-bit
    // size beyond f64 precision and chunks holding NUL and line-break bytes.
    // Codes at both ends of each range, so a range cut short fails too.
    tags.splice(6..6, [(9, S(b"$LWDISPLAY")), (290, Bool(1))]);
    let circle = tags
        .iter()
        .position(|t| matches!(t, (0, S(b"CIRCLE"))))
        .unwrap();
    tags.splice(
        circle + 2..circle + 2,
        [
            (160, I64(-9_007_199_254_740_993)),
            (169, I64(i64::MAX)),
            (299, Bool(1)),
            (310, Chunk(&[0x00, 0x0a, 0x0d, 0xff, 0x30])),
            (310, Chunk(&[])),
            (319, Chunk(&[0x41, 0x00])),
        ],
    );
    tags.insert(tags.len() - 2, (1004, Chunk(&[0x01, 0x00, 0x0a])));
    let text = assert_same_drawing(false, &tags);
    for pair in [
        "290\n1\n",
        "160\n-9007199254740993\n",
        "169\n9223372036854775807\n",
        "299\n1\n",
        "310\n000A0DFF30\n310\n\n",
        "319\n4100\n",
        "1004\n01000A\n",
    ] {
        assert!(text.contains(pair), "{pair:?} in {text}");
    }
}

#[test]
fn doubles_parse_back_to_the_same_f64() {
    let mut tags = plate(b"AC1015", b"CUT", b"", false);
    let tricky = [0.1, 1.0 / 3.0, -0.0, 5e-324, f64::MAX, -123_456.789, 1e-7];
    let at = tags.len() - 2;
    for v in tricky {
        tags.insert(at, (1040, F(v)));
    }
    assert_same_drawing(false, &tags);
}

#[test]
fn truncated_or_malformed_binary_files_give_errors() {
    for r12 in [true, false] {
        let tags = plate(if r12 { b"AC1009" } else { b"AC1027" }, b"CUT", b"", r12);
        let bytes = binary(r12, &tags);
        for cut in b"AutoCAD Binary DXF".len()..bytes.len() {
            let error = decode_drawing("part.dxf", &bytes[..cut])
                .unwrap_err()
                .to_string();
            assert!(error.contains("re-export"), "{cut}: {error}");
        }
        // Bytes after the EOF group are not part of the drawing.
        let mut padded = bytes.clone();
        padded.extend(b"\0\0\x01");
        assert_eq!(
            decode_drawing("part.dxf", &padded).unwrap(),
            decode_drawing("part.dxf", &bytes).unwrap()
        );
    }
    let mut damaged = binary(false, &plate(b"AC1015", b"CUT", b"", false));
    damaged[21] = b'!';
    let error = decode_drawing("part.dxf", &damaged)
        .unwrap_err()
        .to_string();
    assert!(error.contains("damaged sentinel at byte 21"), "{error}");
}

#[test]
fn only_a_group_0_eof_ends_a_binary_file() {
    // An unknown entity whose name starts with EOF, and EOF as extended data
    // text, are ordinary groups; the drawing goes on after them.
    for r12 in [true, false] {
        let version: &[u8] = if r12 { b"AC1009" } else { b"AC1032" };
        let mut tags = plate(version, b"CUT", b"", r12);
        let circle = tags
            .iter()
            .position(|t| matches!(t, (0, S(b"CIRCLE"))))
            .unwrap();
        tags.splice(circle..circle, [(0, S(b"EOFX")), (8, S(b"CUT"))]);
        tags.insert(tags.len() - 2, (1000, S(b"EOF")));
        let text = assert_same_drawing(r12, &tags);
        let import = import_dxf(&text, &Options::default()).unwrap();
        assert_eq!(import.parts[0].holes.len(), 1);
    }
}

#[test]
fn control_characters_in_binary_strings_take_caret_notation() {
    // A TOLERANCE text's line breaks are raw bytes in binary DXF and ^J in
    // ASCII DXF. A caret stays as it is: the importer decodes neither form.
    for r12 in [true, false] {
        let version: &[u8] = if r12 { b"AC1009" } else { b"AC1024" };
        let mut tags = plate(version, b"CUT", b"", r12);
        let mut ascii_tags = tags.clone();
        let at = tags.len() - 2;
        tags.insert(at, (1000, S(b"{\\Fgdt;j}\n.5\r\n\x1f\ttab ^J")));
        ascii_tags.insert(at, (1000, S(b"{\\Fgdt;j}^J.5^M^J^_^Itab ^J")));
        let text = assert_binary_reads_as(r12, &tags, &ascii_tags);
        assert!(text.contains("\n1000\n{\\Fgdt;j}^J.5^M^J^_^Itab ^J\n"));
    }
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(512))]
    /// Arbitrary bytes after the sentinel give an error or a drawing, never a
    /// panic or an endless loop, with one- and two-byte group codes alike.
    #[test]
    fn arbitrary_binary_dxf_never_panics(r13 in any::<bool>(), body in proptest::collection::vec(any::<u8>(), 0..400)) {
        let mut bytes = SENTINEL.to_vec();
        if r13 {
            bytes.extend(b"\0\0SECTION\0\x02\0HEADER\0\x09\0$ACADVER\0\x01\0AC1032\0");
        }
        bytes.extend(body);
        if let Ok(text) = decode_drawing("part.dxf", &bytes) {
            let _ = import_dxf(&text, &Options::default());
        }
    }

    /// Truncated or byte-damaged valid binary files must not panic either.
    #[test]
    fn damaged_binary_dxf_never_panics(r12 in any::<bool>(), cut in 0usize..2000, at in 0usize..2000, byte in any::<u8>()) {
        let version: &[u8] = if r12 { b"AC1009" } else { b"AC1032" };
        let mut bytes = binary(r12, &plate(version, b"CUT", b"", r12));
        bytes.truncate(cut.max(SENTINEL.len()));
        let i = SENTINEL.len() + at % (bytes.len() - SENTINEL.len() + 1);
        if i < bytes.len() {
            bytes[i] = byte;
        }
        if let Ok(text) = decode_drawing("part.dxf", &bytes) {
            let _ = import_dxf(&text, &Options::default());
        }
    }
}
