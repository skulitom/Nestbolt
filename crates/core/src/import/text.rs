//! Decode source bytes once, identically in native tools and the browser.
use anyhow::{Context, Result, anyhow, bail, ensure};
use encoding_rs::{Encoding, UTF_8, UTF_16BE, UTF_16LE, WINDOWS_1252};

fn header_value<'a>(lines: &[&'a str], variable: &str) -> Option<&'a str> {
    lines
        .windows(4)
        .find(|w| w[0].trim() == "9" && w[1].trim() == variable)
        .map(|w| w[3].trim())
}

fn dxf_encoding(bytes: &[u8]) -> Result<&'static Encoding> {
    // Only the ASCII header field names/values are used from this temporary view.
    let header = String::from_utf8_lossy(bytes);
    let lines = header.lines().collect::<Vec<_>>();
    let version = header_value(&lines, "$ACADVER")
        .and_then(|v| v.strip_prefix("AC"))
        .and_then(|v| v.parse::<u32>().ok());
    if version.is_some_and(|v| v >= 1021) {
        return Ok(UTF_8);
    }
    let Some(page) = header_value(&lines, "$DWGCODEPAGE") else {
        return Ok(WINDOWS_1252);
    };
    let page = page.to_ascii_uppercase();
    let label = match page.as_str() {
        "ANSI_874" => "windows-874",
        "ANSI_932" => "shift_jis",
        "ANSI_936" => "gbk",
        "ANSI_949" => "euc-kr",
        "ANSI_950" => "big5",
        "UTF-8" | "UTF8" => "utf-8",
        "ANSI_1250" => "windows-1250",
        "ANSI_1251" => "windows-1251",
        "ANSI_1252" => "windows-1252",
        "ANSI_1253" => "windows-1253",
        "ANSI_1254" => "windows-1254",
        "ANSI_1255" => "windows-1255",
        "ANSI_1256" => "windows-1256",
        "ANSI_1257" => "windows-1257",
        "ANSI_1258" => "windows-1258",
        _ => {
            bail!("unsupported DXF $DWGCODEPAGE {page:?}; re-export as a UTF-8 DXF R2007 or later")
        }
    };
    Encoding::for_label(label.as_bytes())
        .context("unknown text encoding; re-export this drawing as UTF-8")
}

fn xml_encoding(bytes: &[u8]) -> Result<&'static Encoding> {
    if bytes.starts_with(&[b'<', 0, b'?', 0]) {
        return Ok(UTF_16LE);
    }
    if bytes.starts_with(&[0, b'<', 0, b'?']) {
        return Ok(UTF_16BE);
    }
    let header = String::from_utf8_lossy(&bytes[..bytes.len().min(1024)]);
    let Some(declaration) = header
        .strip_prefix("<?xml")
        .and_then(|s| s.split_once("?>").map(|v| v.0))
    else {
        return Ok(UTF_8);
    };
    let Some((_, encoding)) = declaration.split_once("encoding") else {
        return Ok(UTF_8);
    };
    let Some(label) = encoding.trim_start().strip_prefix('=').map(str::trim_start) else {
        return Ok(UTF_8);
    };
    let quote = label.chars().next().unwrap_or(' ');
    ensure!(
        matches!(quote, '\'' | '"'),
        "invalid XML encoding declaration; re-export as UTF-8 SVG"
    );
    let label = label[1..].split(quote).next().unwrap_or("");
    Encoding::for_label(label.as_bytes())
        .with_context(|| format!("unsupported XML encoding {label:?}; re-export as UTF-8 SVG"))
}

fn dxf_unicode_escapes(text: &str) -> Result<String> {
    let mut rest = text;
    let mut out = String::with_capacity(text.len());
    while let Some(i) = rest.find("\\U+") {
        out.push_str(&rest[..i]);
        rest = &rest[i..];
        let mut units = vec![];
        while let Some(hex) = rest.strip_prefix("\\U+").and_then(|s| s.get(..4)) {
            let Ok(unit) = u16::from_str_radix(hex, 16) else {
                break;
            };
            units.push(unit);
            rest = &rest[7..];
        }
        if units.is_empty() {
            out.push_str("\\U+");
            rest = &rest[3..];
        } else {
            for c in char::decode_utf16(units) {
                out.push(c.context("invalid DXF Unicode escape; repair the text/layer name or re-export as UTF-8 DXF")?);
            }
        }
    }
    out.push_str(rest);
    Ok(out)
}

/// The 22 bytes that open a binary DXF, from Autodesk's "About Binary DXF Files".
const BINARY_SENTINEL: &[u8] = b"AutoCAD Binary DXF\r\n\x1a\0";

/// How a binary DXF stores a group code's value, by code range: Autodesk's
/// "Group Code Value Types" table, extended as ezdxf's `lldxf/types.py` does.
enum BinaryValue {
    Text,
    Bool,
    Int16,
    Int32,
    Int64,
    Double,
    Chunk,
}

fn binary_value(code: u16) -> BinaryValue {
    match code {
        310..=319 | 1004 => BinaryValue::Chunk,
        290..=299 => BinaryValue::Bool,
        60..=79 | 170..=179 | 270..=289 | 370..=389 | 400..=409 | 1060..=1070 => BinaryValue::Int16,
        90..=99 | 420..=429 | 440..=459 | 1071 => BinaryValue::Int32,
        160..=169 => BinaryValue::Int64,
        10..=59 | 110..=149 | 210..=239 | 460..=469 | 1010..=1059 => BinaryValue::Double,
        _ => BinaryValue::Text,
    }
}

/// Group codes take one byte before R13 and two bytes from R13 on. Like
/// ezdxf's `binary_tags_loader`, read `$ACADVER` from the first 1024 bytes;
/// a drawing without it is R12.
fn binary_one_byte_codes(bytes: &[u8]) -> bool {
    let window = &bytes[BINARY_SENTINEL.len()..bytes.len().min(1024)];
    let Some(at) = window.windows(8).position(|w| w == b"$ACADVER") else {
        return true;
    };
    // Skip the name's terminator and a one-byte group code 1, or one more
    // byte for a two-byte group code.
    let mut start = BINARY_SENTINEL.len() + at + 10;
    if bytes.get(start).is_some_and(|&b| b != b'A') {
        start += 1;
    }
    let version = &bytes[start.min(bytes.len())..(start + 6).min(bytes.len())];
    version <= b"AC1009".as_slice()
}

fn binary_take<const N: usize>(bytes: &[u8], i: &mut usize) -> Option<[u8; N]> {
    let value = bytes.get(*i..*i + N)?.try_into().ok()?;
    *i += N;
    Some(value)
}

/// The ASCII group-code text of a binary DXF, with strings left in the file's
/// own encoding and doubles written so they parse back to the same value.
/// Stops after the EOF group, which a complete file must have.
fn binary_dxf_text(bytes: &[u8]) -> Result<Vec<u8>> {
    use std::io::Write;
    if let Some(at) =
        (0..BINARY_SENTINEL.len()).find(|&i| bytes.get(i) != Some(&BINARY_SENTINEL[i]))
    {
        if at == bytes.len() {
            bail!("binary DXF is truncated in its sentinel; re-export the drawing");
        }
        bail!("binary DXF has a damaged sentinel at byte {at}; re-export the drawing");
    }
    let one_byte_codes = binary_one_byte_codes(bytes);
    // Grown as groups are written: bytes after the EOF group never count.
    let mut out = Vec::new();
    let mut i = BINARY_SENTINEL.len();
    while i < bytes.len() {
        let at = i;
        let truncated =
            || anyhow!("binary DXF is truncated in the group at byte {at}; re-export the drawing");
        let code = match bytes[i] {
            // Before R13, a 255 byte announces a two-byte extended data code.
            255 if one_byte_codes => {
                i += 1;
                u16::from_le_bytes(binary_take(bytes, &mut i).ok_or_else(truncated)?)
            }
            code if one_byte_codes => {
                i += 1;
                u16::from(code)
            }
            _ => u16::from_le_bytes(binary_take(bytes, &mut i).ok_or_else(truncated)?),
        };
        writeln!(out, "{code}")?;
        match binary_value(code) {
            BinaryValue::Text => {
                let len = bytes[i..]
                    .iter()
                    .position(|&b| b == 0)
                    .ok_or_else(truncated)?;
                let value = &bytes[i..i + len];
                i += len + 1;
                // ASCII DXF writes control characters in caret notation, such
                // as ^J for a line break; no double-byte code page uses them
                // as trail bytes. A line break must not split the pair.
                for &b in value {
                    if b < 0x20 {
                        out.extend([b'^', b + 0x40]);
                    } else {
                        out.push(b);
                    }
                }
                if code == 0 && value == b"EOF" {
                    out.push(b'\n');
                    return Ok(out);
                }
            }
            BinaryValue::Bool => write!(
                out,
                "{}",
                binary_take::<1>(bytes, &mut i).ok_or_else(truncated)?[0]
            )?,
            BinaryValue::Int16 => write!(
                out,
                "{}",
                i16::from_le_bytes(binary_take(bytes, &mut i).ok_or_else(truncated)?)
            )?,
            BinaryValue::Int32 => write!(
                out,
                "{}",
                i32::from_le_bytes(binary_take(bytes, &mut i).ok_or_else(truncated)?)
            )?,
            BinaryValue::Int64 => write!(
                out,
                "{}",
                i64::from_le_bytes(binary_take(bytes, &mut i).ok_or_else(truncated)?)
            )?,
            // Debug formatting is the shortest text that parses back to the same f64.
            BinaryValue::Double => write!(
                out,
                "{:?}",
                f64::from_le_bytes(binary_take(bytes, &mut i).ok_or_else(truncated)?)
            )?,
            // A length byte, then the data, written as hex like ASCII DXF.
            BinaryValue::Chunk => {
                let [len] = binary_take(bytes, &mut i).ok_or_else(truncated)?;
                let data = bytes.get(i..i + usize::from(len)).ok_or_else(truncated)?;
                i += data.len();
                for b in data {
                    write!(out, "{b:02X}")?;
                }
            }
        }
        out.push(b'\n');
    }
    bail!(
        "binary DXF ends at byte {} without its EOF group; re-export the drawing",
        bytes.len()
    )
}

/// R2004 and earlier use $DWGCODEPAGE (default ANSI_1252); R2007+ use UTF-8.
/// XML follows its BOM/declaration. Invalid input never gets replacement chars.
/// A binary DXF becomes its ASCII group-code text first, under the same rules.
pub fn decode_drawing(name: &str, bytes: &[u8]) -> Result<String> {
    let binary = bytes.starts_with(b"AutoCAD Binary DXF");
    let dxf = binary || name.to_ascii_lowercase().ends_with(".dxf");
    let ascii;
    let bytes = if binary {
        ascii = binary_dxf_text(bytes)?;
        ascii.as_slice()
    } else {
        bytes
    };
    let (encoding, skip) = if let Some(bom) = Encoding::for_bom(bytes) {
        bom
    } else {
        (
            if dxf {
                dxf_encoding(bytes)?
            } else {
                xml_encoding(bytes)?
            },
            0,
        )
    };
    let text = encoding
        .decode_without_bom_handling_and_without_replacement(&bytes[skip..])
        .with_context(|| {
            format!(
                "{name} has invalid {} bytes; re-export it as UTF-8 with a matching format/header",
                encoding.name()
            )
        })?;
    if dxf {
        dxf_unicode_escapes(&text)
    } else {
        Ok(text.into_owned())
    }
}
