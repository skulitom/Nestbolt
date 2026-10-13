//! The presentation attributes and simple stylesheet rules used by shop exports.
//! Unsupported selectors fail with an editing fix instead of guessing a colour.
use anyhow::{Result, ensure};
use roxmltree::{Document, Node};

use super::selection::{color_key, cut_name, ignored_layer};

#[derive(Clone)]
pub(super) struct Style {
    pub layer: String,
    stroke: String,
    fill: String,
    current_color: String,
    pub hidden: bool,
}

impl Default for Style {
    fn default() -> Self {
        Self {
            layer: "0".into(),
            stroke: "none".into(),
            fill: "black".into(),
            current_color: "black".into(),
            hidden: false,
        }
    }
}

pub(super) struct Rule {
    selector: String,
    declarations: Vec<(String, String)>,
    specificity: u8,
}

fn declarations(text: &str) -> Vec<(String, String)> {
    text.split(';')
        .filter_map(|item| item.split_once(':'))
        .map(|(k, v)| (k.trim().to_ascii_lowercase(), v.trim().to_owned()))
        .collect()
}

pub(super) fn stylesheet(document: &Document) -> Result<Vec<Rule>> {
    let mut rules = vec![];
    for node in document.descendants().filter(|n| n.has_tag_name("style")) {
        let mut text = node.text().unwrap_or("").to_owned();
        while let Some(start) = text.find("/*") {
            let end = text[start + 2..]
                .find("*/")
                .map(|n| start + 2 + n + 2)
                .unwrap_or(text.len());
            text.replace_range(start..end, "");
        }
        for rule in text.split('}').filter(|s| !s.trim().is_empty()) {
            let Some((selectors, body)) = rule.split_once('{') else {
                continue;
            };
            for selector in selectors.split(',').map(str::trim) {
                let ident = selector.strip_prefix(['.', '#']).unwrap_or(selector);
                ensure!(
                    !ident.is_empty()
                        && ident
                            .chars()
                            .all(|c| c.is_alphanumeric() || c == '_' || c == '-')
                        || selector == "*",
                    "unsupported SVG CSS selector {selector:?}; save with presentation attributes or plain SVG before importing"
                );
                ensure!(
                    !body.contains("!important"),
                    "SVG CSS !important is unsupported; save with presentation attributes or plain SVG before importing"
                );
                rules.push(Rule {
                    selector: selector.into(),
                    declarations: declarations(body),
                    specificity: if selector.starts_with('#') {
                        3
                    } else if selector.starts_with('.') {
                        2
                    } else if selector == "*" {
                        0
                    } else {
                        1
                    },
                });
            }
        }
    }
    rules.sort_by_key(|r| r.specificity);
    Ok(rules)
}

impl Style {
    pub fn at(&self, node: Node, rules: &[Rule]) -> Self {
        let mut next = self.clone();
        let layer = node
            .attribute(("http://www.inkscape.org/namespaces/inkscape", "label"))
            .or_else(|| {
                node.attribute(("http://www.inkscape.org/namespaces/inkscape", "groupmode"))
                    .filter(|v| *v == "layer")
                    .and_then(|_| node.attribute("id"))
            })
            .or_else(|| {
                (node.has_tag_name("g"))
                    .then(|| node.attribute("id"))
                    .flatten()
                    .filter(|v| self.layer == "0" || cut_name(v) || ignored_layer(v))
            });
        if let Some(layer) = layer {
            next.layer = layer.into();
        }
        let mut properties = vec![];
        for key in [
            "stroke",
            "fill",
            "color",
            "display",
            "visibility",
            "opacity",
        ] {
            if let Some(v) = node.attribute(key) {
                properties.push((key.to_owned(), v.to_owned()));
            }
        }
        for rule in rules {
            let matched = if let Some(id) = rule.selector.strip_prefix('#') {
                node.attribute("id") == Some(id)
            } else if let Some(class) = rule.selector.strip_prefix('.') {
                node.attribute("class")
                    .unwrap_or("")
                    .split_whitespace()
                    .any(|s| s == class)
            } else {
                rule.selector == "*" || rule.selector == node.tag_name().name()
            };
            if matched {
                properties.extend(rule.declarations.iter().cloned());
            }
        }
        properties.extend(declarations(node.attribute("style").unwrap_or("")));
        // Last declaration wins on this element; a hidden ancestor stays hidden.
        let values = properties
            .into_iter()
            .collect::<std::collections::HashMap<_, _>>();
        for (key, dest) in [
            ("stroke", &mut next.stroke),
            ("fill", &mut next.fill),
            ("color", &mut next.current_color),
        ] {
            if let Some(value) = values.get(key).filter(|v| v.as_str() != "inherit") {
                *dest = value.clone();
            }
        }
        next.hidden |= values.get("display").is_some_and(|v| v == "none")
            || values
                .get("visibility")
                .is_some_and(|v| v == "hidden" || v == "collapse")
            || values
                .get("opacity")
                .and_then(|v| v.parse::<f64>().ok())
                .is_some_and(|v| v <= 0.0);
        next
    }

    pub fn color(&self) -> String {
        let paint = if self.stroke != "none" {
            &self.stroke
        } else {
            &self.fill
        };
        color_key(if paint == "currentColor" {
            &self.current_color
        } else {
            paint
        })
    }
}
