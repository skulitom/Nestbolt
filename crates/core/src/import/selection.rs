//! Shared layer/colour inventory and explicit cut selection for both readers.
use std::collections::BTreeMap;

use anyhow::{Result, bail};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use super::{
    Diagnostics, FailureReason, Import, ImportEntry, ImportFailed, ImportReport, ImportSource,
    Options, Piece, SkipReason, assemble,
};

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
    pub id: Option<String>,
    pub ignored: Option<(SkipReason, &'static str)>,
    /// Includes unreadable geometry and hidden outlines counted without keeping their curves.
    pub has_geometry: bool,
    pub pieces: Result<Vec<Piece>>,
}

#[derive(Default)]
pub(super) struct Drawing {
    pub entities: Vec<DrawingEntity>,
    pub known_layers: Vec<String>,
    /// Read a layer named in `Options::layers` even when its name marks bend,
    /// extent or construction lines. Only the DXF reader sets this.
    pub listed_layers_override_names: bool,
}

/// Whether `Options::layers` names this layer, ignoring case.
pub(super) fn listed_layer(options: &Options, name: &str) -> bool {
    options
        .layers
        .as_ref()
        .is_some_and(|v| v.iter().any(|s| s.to_lowercase() == name.to_lowercase()))
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

enum Exclusion {
    Ignored(ImportSource, SkipReason),
    NotSelected { layer: String, color: String },
}

impl Exclusion {
    fn diagnostic(self, count: usize) -> ImportEntry {
        match self {
            Self::Ignored(mut source, reason) => {
                if count > 1 {
                    source.id = None;
                }
                ImportEntry::Skipped {
                    source,
                    reason,
                    count,
                }
            }
            Self::NotSelected { layer, color } => ImportEntry::NotSelected {
                layer,
                color,
                count,
            },
        }
    }
}

impl Drawing {
    pub fn finish(
        self,
        options: &Options,
        mut warnings: Diagnostics,
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
                    && e.has_geometry
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
        let mut skipped = BTreeMap::<String, (usize, Exclusion)>::new();
        let mut pieces = vec![];
        for e in self.entities {
            let geometry = e.has_geometry;
            let color = color_key(&e.color);
            let listed = listed_layer(options, &e.layer);
            let ignore = e.ignored.or_else(|| {
                (ignored_layer(&e.layer) && !(self.listed_layers_override_names && listed))
                    .then_some((SkipReason::IgnoredLayer, "bend/extent/construction layer"))
            });
            let selected = ignore.is_none()
                && (options.layers.is_none() || listed)
                && chosen_colors.as_ref().is_none_or(|v| v.contains(&color))
                && (!named || cut_name(&e.layer));
            for item in [channel(&mut layers, &e.layer), channel(&mut colors, &color)] {
                item.entities += 1;
                item.geometry_entities += usize::from(geometry);
                item.selected_entities += usize::from(selected && geometry);
            }
            if let Some((reason, message)) = ignore {
                let group = format!("{} on layer {:?}: {message}", e.kind, e.layer);
                let (count, _) = skipped.entry(group).or_insert_with(|| {
                    let source = ImportSource::new(&e.layer, &e.kind, e.id.as_deref());
                    (0, Exclusion::Ignored(source, reason))
                });
                *count += 1;
            } else if !selected && geometry {
                let group = format!(
                    "geometry on layer {:?}, colour {color}: excluded by cut selection",
                    e.layer
                );
                let (count, _) = skipped.entry(group).or_insert_with(|| {
                    (
                        0,
                        Exclusion::NotSelected {
                            layer: e.layer.clone(),
                            color,
                        },
                    )
                });
                *count += 1;
            }
            if selected && !inspect_only {
                pieces.extend(e.pieces?);
            }
        }
        report.layers = layers.into_values().collect();
        report.colors = colors.into_values().collect();
        for (description, (count, reason)) in skipped {
            warnings.push(
                reason.diagnostic(count),
                format!("ignored {count} {description}"),
            );
        }
        if !inspect_only {
            if let Some(chosen) = &options.layers {
                for name in chosen {
                    if !report
                        .layers
                        .iter()
                        .any(|l| l.name.to_lowercase() == name.to_lowercase())
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
                report.entries = warnings.entries;
                return Err(ImportFailed {
                    reason: FailureReason::NoCuttingGeometry,
                    warnings: warnings.messages,
                    report,
                }
                .into());
            }
        }
        let parts = if inspect_only {
            vec![]
        } else {
            assemble(pieces, options, &mut warnings, &mut report)?
        };
        report.entries = warnings.entries;
        if parts.is_empty() && !inspect_only {
            return Err(ImportFailed {
                reason: FailureReason::NoClosedOutlines,
                warnings: warnings.messages,
                report,
            }
            .into());
        }
        Ok(Import {
            parts,
            warnings: warnings.messages,
            report,
        })
    }
}
