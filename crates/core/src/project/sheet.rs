//! Stock outlines selected independently of cutting parts.
use super::{FileImportReport, ImportOptions, Library};
use anyhow::{Context, Result, ensure};
use nestbolt_validator::{Footprint, Polygon, RigidTransform, Units};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct SheetOutline {
    pub id: String,
    pub source: String,
    pub width_mm: f64,
    pub height_mm: f64,
    /// Lower-left corner in the drawing's mm, Y-up frame, before normalization.
    pub origin_mm: [f64; 2],
    pub outline_mm: Vec<Polygon>,
    pub tolerance_mm: f64,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct SheetImport {
    pub outlines: Vec<SheetOutline>,
    pub warnings: Vec<String>,
    pub imports: Vec<FileImportReport>,
}

impl SheetImport {
    /// Explicit layer/colour choices win. Otherwise prefer SHEET over the
    /// normal cutting selection, so pre-arranged cutting parts are not holes
    /// in the stock. Plain remnant files retain normal outline selection.
    pub fn read(name: &str, text: &str, options: &ImportOptions) -> Result<Self> {
        let mut options = options.clone();
        if options.layers.is_none() && options.colors.is_none() {
            let report = if name.to_ascii_lowercase().ends_with(".svg") {
                crate::import::inspect_svg(text, &options)
            } else if name.to_ascii_lowercase().ends_with(".dxf") {
                crate::import::inspect_dxf(text, &options)
            } else {
                anyhow::bail!("{name}: choose an SVG or DXF sheet outline");
            }?;
            let layers: Vec<_> = report
                .layers
                .iter()
                .filter(|l| l.name.eq_ignore_ascii_case("SHEET") && l.geometry_entities > 0)
                .map(|l| l.name.clone())
                .collect();
            if !layers.is_empty() {
                options.layers = Some(layers);
            }
        }
        let library = Library::read(&[(name.into(), text.into())], &options, false)?;
        let mut outlines = vec![];
        for (i, part) in library.parts.iter().enumerate() {
            // Part collision proxies may close self-touches outwards. Stock
            // may never gain usable material that way: validate the original
            // flattened curves instead and reject ambiguous stock geometry.
            let polygon = Polygon {
                outer: part.outer.flatten(options.tolerance)?,
                holes: part
                    .holes
                    .iter()
                    .map(|h| h.flatten(options.tolerance))
                    .collect::<Result<_>>()?,
            };
            let footprint = Footprint::new(&polygon, Units::Mm, RigidTransform::default())
                .with_context(|| format!("{name}: repair self-intersections or touching cutouts in the sheet outline; stock boundaries cannot be expanded to repair them"))?;
            let [x0, y0, x1, y1] = footprint.bounds();
            let move_ring =
                |ring: Vec<[f64; 2]>| ring.into_iter().map(|[x, y]| [x - x0, y - y0]).collect();
            let curved = std::iter::once(&part.outer).chain(&part.holes).any(|c| {
                c.segments
                    .iter()
                    .any(|s| !matches!(s, crate::curves::Segment::Line { .. }))
            });
            let stem = std::path::Path::new(name)
                .file_stem()
                .and_then(|s| s.to_str())
                .unwrap_or("drawing");
            outlines.push(SheetOutline {
                id: format!("{stem}-sheet-{}", i + 1),
                source: part.source.clone(),
                width_mm: x1 - x0,
                height_mm: y1 - y0,
                origin_mm: [x0, y0],
                outline_mm: vec![Polygon {
                    outer: move_ring(polygon.outer),
                    holes: polygon.holes.into_iter().map(move_ring).collect(),
                }],
                tolerance_mm: if curved { options.tolerance } else { 0.0 },
            });
        }
        ensure!(
            !outlines.is_empty(),
            "{name}: select a layer containing a closed sheet outline"
        );
        Ok(Self {
            outlines,
            warnings: library.warnings,
            imports: library.imports,
        })
    }
}
