//! Decode source bytes once, identically in native tools and the browser.
use anyhow::{Context, Result, bail, ensure};
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

/// R2004 and earlier use $DWGCODEPAGE (default ANSI_1252); R2007+ use UTF-8.
/// XML follows its BOM/declaration. Invalid input never gets replacement chars.
pub fn decode_drawing(name: &str, bytes: &[u8]) -> Result<String> {
    let dxf = name.to_ascii_lowercase().ends_with(".dxf");
    ensure!(
        !bytes.starts_with(b"AutoCAD Binary DXF"),
        "binary DXF is not supported; export an ASCII DXF drawing"
    );
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
