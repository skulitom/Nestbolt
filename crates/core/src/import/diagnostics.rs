use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use std::fmt;

/// Drawing entity associated with an import diagnostic. Layer names are resolved
/// through block and group inheritance. SVG IDs are present when available.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize, JsonSchema)]
pub struct ImportSource {
    pub layer: String,
    pub entity: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub id: Option<String>,
}

impl ImportSource {
    pub(super) fn new(layer: &str, entity: &str, id: Option<&str>) -> Self {
        Self {
            layer: layer.into(),
            entity: entity.into(),
            id: id.map(str::to_owned),
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
#[non_exhaustive]
pub enum SkipReason {
    Unsupported,
    RationalSpline,
    InvalidSpline,
    Hidden,
    NotCutGeometry,
    PaperSpace,
    NoStrokeOrFill,
    IgnoredLayer,
}

/// Structured counterpart to one entry in the ordered warning list.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize, JsonSchema)]
#[serde(tag = "kind", rename_all = "snake_case")]
#[non_exhaustive]
pub enum ImportEntry {
    Skipped {
        source: ImportSource,
        reason: SkipReason,
        count: usize,
    },
    NotSelected {
        layer: String,
        color: String,
        count: usize,
    },
    UnknownBlock {
        source: ImportSource,
        block: String,
    },
    UnresolvedUse {
        source: ImportSource,
        href: String,
    },
    FitPointSpline {
        source: ImportSource,
    },
    PolylineWidth {
        source: ImportSource,
    },
    OutlineTouches {
        source: ImportSource,
        closed_under_mm: f64,
    },
    OutlineCrosses {
        source: ImportSource,
    },
    DegenerateContour {
        source: ImportSource,
    },
    OverlapsKept {
        sources: Vec<ImportSource>,
    },
    Cleanup,
    GapClosed {
        gap: usize,
    },
    OpenContour {
        contour: usize,
    },
    DuplicateHandle {
        handle: String,
        count: usize,
    },
    UndefinedLayer {
        layer: String,
        count: usize,
    },
    UnitsMissing,
    PossibleInches,
    SvgSliceNotClipped,
}

// The historic display label is part of the public warning and part output.
// In particular an unnamed SVG element receives a generated label, not an ID.
#[derive(Clone, Debug)]
pub(super) struct Origin {
    pub label: String,
    pub location: ImportSource,
}

impl Origin {
    pub fn dxf(layer: &str, entity: &str) -> Self {
        Self {
            label: format!("{layer}:{entity}"),
            location: ImportSource::new(layer, entity, None),
        }
    }
}
impl fmt::Display for Origin {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.label)
    }
}

#[derive(Default)]
pub(super) struct Diagnostics {
    pub messages: Vec<String>,
    pub entries: Vec<ImportEntry>,
}

impl Diagnostics {
    pub fn push(&mut self, entry: ImportEntry, message: String) {
        self.messages.push(message);
        self.entries.push(entry);
    }
}
