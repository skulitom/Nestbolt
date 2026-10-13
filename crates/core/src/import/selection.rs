//! Shared layer/colour inventory and explicit cut selection for both readers.
use std::collections::BTreeMap;

use anyhow::{Result, bail};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::{Import, ImportReport, Options, Piece, assemble};

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct Channel {
    pub name: String,
    /// Expanded entity instances, including ignored entities; INSERT counts too.
    pub entities: usize,
    pub geometry_entities: usize,
    pub selected_entities: usize,
}

pub(super) struct DrawingEntity {
    pub layer: String,
    pub color: String,
    pub kind: String,
    pub ignored: Option<String>,
    pub pieces: Vec<Piece>,
}

#[derive(Default)]
pub(super) struct Drawing {
    pub entities: Vec<DrawingEntity>,
    pub known_layers: Vec<String>,
}

pub(super) fn cut_name(name: &str) -> bool {
    let name = name.to_ascii_lowercase();
    ["cut", "outline", "profile"]
        .iter()
        .any(|s| name.contains(s))
}

pub(super) fn ignored_layer(name: &str) -> bool {
    let name = name.to_ascii_lowercase();
    ["bend", "extent", "construction"]
        .iter()
        .any(|s| name.contains(s))
}

pub(super) fn color_key(value: &str) -> String {
    let value = value.trim();
    if let Ok(aci) = value.strip_prefix("aci:").unwrap_or(value).parse::<u16>() {
        return format!("aci:{aci}");
    }
    if let Ok(c) = value.parse::<svgtypes::Color>() {
        return format!("#{:02x}{:02x}{:02x}", c.red, c.green, c.blue);
    }
    value.to_ascii_lowercase()
}

fn channel<'a>(map: &'a mut BTreeMap<String, Channel>, name: &str) -> &'a mut Channel {
    map.entry(name.to_owned()).or_insert_with(|| Channel {
        name: name.into(),
        entities: 0,
        geometry_entities: 0,
        selected_entities: 0,
    })
}

impl Drawing {
    pub fn finish(
        self,
        options: &Options,
        mut warnings: Vec<String>,
        mut report: ImportReport,
        inspect_only: bool,
    ) -> Result<Import> {
        let mut layers = BTreeMap::new();
        let mut colors = BTreeMap::new();
        for name in self.known_layers {
            channel(&mut layers, &name);
        }
        let explicit = options.layers.is_some() || options.colors.is_some();
        let named = !explicit
            && self.entities.iter().any(|e| {
                e.ignored.is_none()
                    && !ignored_layer(&e.layer)
                    && !e.pieces.is_empty()
                    && cut_name(&e.layer)
            });
        report.selection_mode = if explicit {
            "explicit"
        } else if named {
            "named_cut_layers"
        } else {
            "closed_contours"
        }
        .into();
        let chosen_colors = options
            .colors
            .as_ref()
            .map(|v| v.iter().map(|s| color_key(s)).collect::<Vec<_>>());
        let mut skipped = BTreeMap::<String, usize>::new();
        let mut pieces = vec![];
        for e in self.entities {
            let color = color_key(&e.color);
            let ignore = e.ignored.or_else(|| {
                ignored_layer(&e.layer).then(|| "bend/extent/construction layer".into())
            });
            let selected = ignore.is_none()
                && options
                    .layers
                    .as_ref()
                    .is_none_or(|v| v.iter().any(|s| s.eq_ignore_ascii_case(&e.layer)))
                && chosen_colors.as_ref().is_none_or(|v| v.contains(&color))
                && (!named || cut_name(&e.layer));
            let geometry = !e.pieces.is_empty();
            for item in [channel(&mut layers, &e.layer), channel(&mut colors, &color)] {
                item.entities += 1;
                item.geometry_entities += usize::from(geometry);
                item.selected_entities += usize::from(selected && geometry);
            }
            if let Some(reason) = ignore {
                *skipped
                    .entry(format!("{} on layer {:?}: {reason}", e.kind, e.layer))
                    .or_default() += 1;
            } else if !selected && geometry {
                *skipped
                    .entry(format!(
                        "geometry on layer {:?}, colour {color}: excluded by cut selection",
                        e.layer
                    ))
                    .or_default() += 1;
            }
            if selected {
                pieces.extend(e.pieces);
            }
        }
        report.layers = layers.into_values().collect();
        report.colors = colors.into_values().collect();
        for (kind, count) in skipped {
            warnings.push(format!("ignored {count} {kind}"));
        }
        if !inspect_only {
            if let Some(chosen) = &options.layers {
                for name in chosen {
                    if !report
                        .layers
                        .iter()
                        .any(|l| l.name.eq_ignore_ascii_case(name))
                    {
                        bail!(
                            "unknown layer {name:?}; choose from: {}",
                            report
                                .layers
                                .iter()
                                .map(|l| l.name.as_str())
                                .collect::<Vec<_>>()
                                .join(", ")
                        );
                    }
                }
            }
            if let Some(chosen) = chosen_colors {
                for color in chosen {
                    if !report.colors.iter().any(|c| c.name == color) {
                        bail!(
                            "unknown colour {color:?}; choose from: {}",
                            report
                                .colors
                                .iter()
                                .map(|c| c.name.as_str())
                                .collect::<Vec<_>>()
                                .join(", ")
                        );
                    }
                }
            }
            if pieces.is_empty() {
                bail!(
                    "no cutting geometry selected; choose a layer/colour containing closed outlines or convert text to paths. Layers: {}; colours: {}. {}",
                    report
                        .layers
                        .iter()
                        .map(|l| l.name.as_str())
                        .collect::<Vec<_>>()
                        .join(", "),
                    report
                        .colors
                        .iter()
                        .map(|c| c.name.as_str())
                        .collect::<Vec<_>>()
                        .join(", "),
                    warnings.join("; ")
                );
            }
        }
        let parts = if inspect_only {
            vec![]
        } else {
            assemble(pieces, options, &mut warnings, &mut report)?
        };
        Ok(Import {
            parts,
            warnings,
            report,
        })
    }
}
