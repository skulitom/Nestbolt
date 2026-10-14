//! Byte-range edits: keep unrelated XML verbatim, including unknown settings.
use std::collections::{BTreeMap, HashMap, HashSet};
use std::ops::Range;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::RigidTransform;
use roxmltree::Node;
use serde::{Deserialize, Serialize};

use super::{Nesting, Resources, child, number, values, xform};
use crate::curves::Affine;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct UnitPlacement {
    pub unit: usize,
    pub transform: RigidTransform,
}

struct Patch {
    range: Range<usize>,
    value: String,
}

fn patch(source: &str, offset: usize, mut changes: Vec<Patch>) -> Result<String> {
    changes.sort_by_key(|p| (p.range.start, p.range.end));
    let mut result = String::new();
    let mut end = offset;
    for change in changes {
        ensure!(
            change.range.start >= end && change.range.end <= offset + source.len(),
            "overlapping LightBurn XML edits"
        );
        result.push_str(&source[end - offset..change.range.start - offset]);
        result.push_str(&change.value);
        end = change.range.end;
    }
    result.push_str(&source[end - offset..]);
    Ok(result)
}

/// Locate the end of a parsed element's opening tag without confusing a quoted
/// greater-than sign with markup. The input has already passed XML parsing.
fn opening_end(source: &str, node: Node) -> usize {
    let mut quote = None;
    for (i, b) in source
        .as_bytes()
        .iter()
        .enumerate()
        .take(node.range().end)
        .skip(node.range().start)
    {
        match (quote, *b) {
            (None, b'\'' | b'"') => quote = Some(*b),
            (Some(q), c) if q == c => quote = None,
            (None, b'>') => return i + 1,
            _ => (),
        }
    }
    unreachable!("parsed XML element has an opening tag")
}

fn escape_attribute(value: &str) -> String {
    value
        .replace('&', "&amp;")
        .replace('"', "&quot;")
        .replace('<', "&lt;")
        .replace('\r', "&#13;")
        .replace('\n', "&#10;")
        .replace('\t', "&#9;")
}

#[derive(Default)]
struct Additions {
    attributes: String,
    children: String,
}

fn additions(source: &str, node: Node, added: Additions, changes: &mut Vec<Patch>) {
    let end = opening_end(source, node);
    if source.as_bytes()[end - 2] == b'/' {
        let value = if added.children.is_empty() {
            format!("{}/>", added.attributes)
        } else {
            format!(
                "{}>{}</{}>",
                added.attributes,
                added.children,
                node.tag_name().name()
            )
        };
        changes.push(Patch {
            range: end - 2..end,
            value,
        });
    } else {
        if !added.attributes.is_empty() {
            changes.push(Patch {
                range: end - 1..end - 1,
                value: added.attributes,
            });
        }
        if !added.children.is_empty() {
            changes.push(Patch {
                range: end..end,
                value: added.children,
            });
        }
    }
}

fn moved_fragment(
    source: &str,
    node: Node,
    transform: Affine,
    resources: &Resources,
    defined: &mut HashSet<(String, String)>,
) -> Result<String> {
    let mut changes = vec![];
    let mut added: HashMap<roxmltree::NodeId, (Node, Additions)> = HashMap::new();
    if transform != Affine::IDENTITY {
        let matrix = xform(node)?.then(transform);
        ensure!(
            values(matrix).iter().all(|v| v.is_finite()),
            "non-finite output LightBurn XForm"
        );
        let text = values(matrix)
            .iter()
            .map(ToString::to_string)
            .collect::<Vec<_>>()
            .join(" ");
        if let Some(existing) = child(node, "XForm") {
            let text_node = existing
                .children()
                .find(Node::is_text)
                .context("LightBurn XForm has no text")?;
            changes.push(Patch {
                range: text_node.range(),
                value: text,
            });
        } else {
            added
                .entry(node.id())
                .or_insert_with(|| (node, Additions::default()))
                .1
                .children
                .push_str(&format!("<XForm>{text}</XForm>"));
        }
    }
    for n in node.descendants().filter(Node::is_element) {
        for (attribute, list) in [("VertID", "VertList"), ("PrimID", "PrimList")] {
            if let Some(id) = n.attribute(attribute) {
                let key = (attribute.to_owned(), id.to_owned());
                if !defined.contains(&key) {
                    let definition = resources
                        .list(n, list, attribute)?
                        .context("missing shared list")?;
                    added
                        .entry(n.id())
                        .or_insert_with(|| (n, Additions::default()))
                        .1
                        .children
                        .push_str(&source[definition.range()]);
                    defined.insert(key);
                }
            }
        }
        if n.attribute("Type") == Some("Bitmap")
            && let Some(id) = n.attribute("SourceHash")
        {
            let key = ("SourceHash".into(), id.to_owned());
            if !defined.contains(&key) {
                let data = resources.images.get(id).context("missing shared bitmap")?;
                added
                    .entry(n.id())
                    .or_insert_with(|| (n, Additions::default()))
                    .1
                    .attributes
                    .push_str(&format!(" Data=\"{}\"", escape_attribute(data)));
                defined.insert(key);
            }
        }
    }
    for (_, (n, addition)) in added {
        additions(source, n, addition, &mut changes);
    }
    patch(&source[node.range()], node.range().start, changes)
}

/// Format 1 ignores legacy V/P elements. Add the equivalent compact lists while
/// retaining the original elements (including unknown attributes and comments).
/// Native 2.1.01 probes confirm that these retained elements are not extra cuts.
/// Restrict conversion to the same shape tree understood by the reader: opaque
/// project metadata must not be mistaken for path geometry.
fn modernize_legacy(source: &str) -> Result<String> {
    fn shape(source: &str, node: Node, changes: &mut Vec<Patch>) -> Result<()> {
        if node.attribute("Type") == Some("Group") {
            if let Some(children) = child(node, "Children") {
                for n in children.children().filter(|n| n.has_tag_name("Shape")) {
                    shape(source, n, changes)?;
                }
            }
            return Ok(());
        }
        let path = match node.attribute("Type") {
            Some("Path") => node,
            Some("Text") => match child(node, "BackupPath") {
                Some(backup) => backup,
                None => return Ok(()),
            },
            _ => return Ok(()),
        };
        let mut lists = String::new();
        if child(path, "VertList").is_none() && path.attribute("VertID").is_none() {
            let mut vertices = String::new();
            for v in path.children().filter(|n| n.has_tag_name("V")) {
                vertices.push_str(&format!(
                    "V{} {}",
                    number(v, "vx", None)?,
                    number(v, "vy", None)?
                ));
                // Native legacy-to-modern saves explicitly mark absent handles.
                // Keep partial coordinates and the lone x=1 sentinel as-is:
                // filling in a zero y would turn the sentinel into a real handle.
                for (x, y) in [("c0x", "c0y"), ("c1x", "c1y")] {
                    if v.attribute(x).is_none() && v.attribute(y).is_none() {
                        vertices.push_str(&format!("{x}1"));
                    } else {
                        for name in [x, y] {
                            if v.attribute(name).is_some() {
                                vertices.push_str(&format!("{name}{}", number(v, name, None)?));
                            }
                        }
                    }
                }
            }
            if !vertices.is_empty() {
                lists.push_str(&format!("<VertList>{vertices}</VertList>"));
            }
        }
        if child(path, "PrimList").is_none() && path.attribute("PrimID").is_none() {
            let mut primitives = String::new();
            for p in path.children().filter(|n| n.has_tag_name("P")) {
                let kind = p.attribute("T").context("missing legacy primitive type")?;
                ensure!(matches!(kind, "L" | "B"), "unknown legacy primitive {kind}");
                let index = |name| -> Result<usize> {
                    Ok(p.attribute(name)
                        .context("missing legacy primitive index")?
                        .parse()?)
                };
                primitives.push_str(&format!("{kind}{} {}", index("p0")?, index("p1")?));
            }
            if !primitives.is_empty() {
                lists.push_str(&format!("<PrimList>{primitives}</PrimList>"));
            }
        }
        if !lists.is_empty() {
            additions(
                source,
                path,
                Additions {
                    children: lists,
                    ..Default::default()
                },
                changes,
            );
        }
        Ok(())
    }

    let xml = roxmltree::Document::parse(source)?;
    let root = xml.root_element();
    let mut changes = vec![];
    if let Some(attribute) = root.attribute_node("FormatVersion") {
        changes.push(Patch {
            range: attribute.range_value(),
            value: "1".into(),
        });
    } else {
        additions(
            source,
            root,
            Additions {
                attributes: " FormatVersion=\"1\"".into(),
                ..Default::default()
            },
            &mut changes,
        );
    }
    for node in root.children().filter(|n| n.has_tag_name("Shape")) {
        shape(source, node, &mut changes)?;
    }
    patch(source, 0, changes)
}

impl Nesting<'_> {
    /// Write a single sheet. Placements may repeat a unit to request additional
    /// copies. Fixed top-level shapes survive once, at their original transform.
    /// Placement transforms operate directly on the original scene coordinates.
    /// Layout validity is checked by the caller before this preserving writer.
    pub fn write_sheet(
        &self,
        placements: &[UnitPlacement],
        width_mm: f64,
        height_mm: f64,
        sheet_outline: bool,
    ) -> Result<String> {
        ensure!(
            width_mm.is_finite() && height_mm.is_finite() && width_mm > 0.0 && height_mm > 0.0,
            "LightBurn sheet width and height must be finite and positive"
        );
        let source = &self.document.source;
        let xml = roxmltree::Document::parse(source)?;
        let root = xml.root_element();
        let resources = Resources::read(root)?;
        let top: Vec<_> = root
            .children()
            .filter(|n| n.has_tag_name("Shape"))
            .collect();
        let mut moves: BTreeMap<usize, Vec<Affine>> = self
            .fixed
            .iter()
            .map(|&i| (i, vec![Affine::IDENTITY]))
            .collect();
        for placement in placements {
            ensure!(
                placement
                    .transform
                    .translation
                    .iter()
                    .all(|v| v.is_finite())
                    && placement.transform.rotation_radians.is_finite()
                    && placement.transform.rotation_radians.abs() <= 1e8,
                "LightBurn placement must be finite and within the supported rotation range"
            );
            let unit = self
                .units
                .get(placement.unit)
                .context("unknown LightBurn nesting unit")?;
            let transform = Affine::placement(&placement.transform);
            for &member in &unit.members {
                ensure!(
                    member < top.len() && !self.fixed.contains(&member),
                    "invalid LightBurn unit membership"
                );
                moves.entry(member).or_default().push(transform);
            }
        }
        // Definitions can occur later than their references, or deep in groups.
        // Re-home only if every original defining owner is absent from the sheet.
        let mut defined = HashSet::new();
        for &i in moves.keys() {
            for n in top[i].descendants().filter(Node::is_element) {
                for (attribute, list) in [("VertID", "VertList"), ("PrimID", "PrimList")] {
                    if child(n, list).is_some()
                        && let Some(id) = n.attribute(attribute)
                    {
                        defined.insert((attribute.to_owned(), id.to_owned()));
                    }
                }
                if n.attribute("Type") == Some("Bitmap")
                    && n.attribute("Data").is_some()
                    && let Some(id) = n.attribute("SourceHash")
                {
                    defined.insert(("SourceHash".into(), id.to_owned()));
                }
            }
        }
        let mut changes = vec![];
        for (i, node) in top.iter().copied().enumerate() {
            let mut value = String::new();
            if let Some(transforms) = moves.get(&i) {
                for &transform in transforms {
                    value.push_str(&moved_fragment(
                        source,
                        node,
                        transform,
                        &resources,
                        &mut defined,
                    )?);
                }
            }
            if value != source[node.range()] {
                changes.push(Patch {
                    range: node.range(),
                    value,
                });
            }
        }
        if sheet_outline {
            let setting = self
                .document
                .scene
                .layers
                .iter()
                .find(|l| !l.image && l.index == 30);
            ensure!(
                setting.is_none_or(|l| l.mode == "Tool"),
                "LightBurn index 30 already has a non-Tool setting; disable the sheet outline or repair T1 in the source project"
            );
            let mut setting_xml = String::new();
            if setting.is_none() {
                setting_xml.push_str("<CutSetting type=\"Tool\"><index Value=\"30\"/><name Value=\"SHEET\"/></CutSetting>");
            }
            let outline = format!(
                "<Shape Type=\"Rect\" CutIndex=\"30\" W=\"{width_mm}\" H=\"{height_mm}\"><XForm>1 0 0 1 {} {}</XForm></Shape>",
                width_mm / 2.0,
                height_mm / 2.0
            );
            // Native 2.1.01 stops loading geometry after Notes. Keep the new
            // setting ahead of shapes and the outline beside the existing
            // shapes, before trailing metadata. Root-end insertion loses T1.
            if let (Some(first), Some(last)) = (top.first(), top.last()) {
                if !setting_xml.is_empty() {
                    let start = first.range().start;
                    changes.push(Patch {
                        range: start..start,
                        value: setting_xml,
                    });
                }
                let end = last.range().end;
                changes.push(Patch {
                    range: end..end,
                    value: outline,
                });
            } else if source.as_bytes()[opening_end(source, root) - 2] == b'/' {
                additions(
                    source,
                    root,
                    Additions {
                        attributes: String::new(),
                        children: setting_xml + &outline,
                    },
                    &mut changes,
                );
            } else {
                // With no original shapes, keep existing layer settings ahead
                // of the first new shape too, and do not put it after Notes.
                let at = root
                    .children()
                    .rfind(|n| n.has_tag_name("CutSetting") || n.has_tag_name("CutSetting_Img"))
                    .map(|n| n.range().end)
                    .or_else(|| child(root, "Notes").map(|n| n.range().start))
                    .unwrap_or(
                        source[..root.range().end]
                            .rfind("</")
                            .context("missing project closing tag")?,
                    );
                changes.push(Patch {
                    range: at..at,
                    value: setting_xml + &outline,
                });
            }
        }
        let result = patch(source, 0, changes)?;
        let result = if self.document.scene.format_version == 0 {
            modernize_legacy(&result)?
        } else {
            result
        };
        // Catch malformed range edits or unresolved references before exporting.
        super::Document::read(&result, self.tolerance_mm)?;
        Ok(result)
    }
}
