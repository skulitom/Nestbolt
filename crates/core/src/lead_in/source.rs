//! Original cutting contours and non-cutting artwork protected by a rigid unit.
//! Closed cutting boundaries are distinct from conservative nesting proxies.
use super::*;

#[derive(Clone, Debug, Default)]
pub struct Source {
    pub components: Vec<Outline>,
    pub open: Vec<Contour>,
    /// Original non-cutting artwork's protected footprints, never exported cuts.
    pub extra_material: Vec<Outline>,
    pub cutting_contours: bool,
}

pub type Sources = HashMap<String, Source>;

impl Source {
    pub fn contours(&self) -> impl Iterator<Item = (&Contour, bool, bool)> {
        self.components
            .iter()
            .flat_map(|c| {
                std::iter::once((&c.outer, false, true))
                    .chain(c.holes.iter().map(|h| (h, true, true)))
            })
            .chain(self.open.iter().map(|c| (c, false, false)))
    }

    pub fn contour_count(&self) -> usize {
        self.contours().count()
    }

    pub fn material_mm(&self, units: Units) -> Result<Footprint> {
        let scale = Affine::scale(units.to_mm());
        let mut combined: Option<Footprint> = None;
        for c in self.components.iter().chain(&self.extra_material) {
            let polygon = Polygon {
                outer: c
                    .outer
                    .transformed(&scale)
                    .flatten(leads::ENVELOPE_TOLERANCE_MM)?,
                holes: c
                    .holes
                    .iter()
                    .map(|h| h.transformed(&scale).flatten(leads::ENVELOPE_TOLERANCE_MM))
                    .collect::<Result<_>>()?,
            };
            let next = Footprint::new(&polygon, Units::Mm, RigidTransform::default())?;
            combined = Some(match combined {
                Some(body) => body.union(&next)?,
                None => next,
            });
        }
        combined.context("cutting source has no protected material")
    }

    pub fn independent(&self, part_id: &str) -> leads::source::Part {
        let component = |c: &Outline| leads::source::Component {
            outer: independent_contour(&c.outer),
            holes: c.holes.iter().map(independent_contour).collect(),
        };
        leads::source::Part {
            part_id: part_id.into(),
            components: self.components.iter().map(component).collect(),
            open_contours: self.open.iter().map(independent_contour).collect(),
            extra_material: self.extra_material.iter().map(component).collect(),
            basis: if self.cutting_contours {
                leads::source::Basis::CuttingContours
            } else {
                leads::source::Basis::MaterialBoundaries
            },
        }
    }
}

pub fn from_outlines(job: &Job, curves: &HashMap<String, Outline>) -> Result<Sources> {
    job.parts
        .iter()
        .map(|p| {
            let components = if let Some(outline) = curves.get(&p.id) {
                ensure!(
                    p.geometry.len() == 1,
                    "multipart source needs every exact component"
                );
                vec![outline.clone()]
            } else {
                ensure!(
                    p.geometry
                        .iter()
                        .all(|p| p.outer.len() >= 3 && p.holes.iter().all(|h| h.len() >= 3)),
                    "lead source rings need three points"
                );
                p.geometry.iter().map(Outline::from_polygon).collect()
            };
            Ok((
                p.id.clone(),
                Source {
                    components,
                    ..Source::default()
                },
            ))
        })
        .collect()
}

fn independent_contour(contour: &Contour) -> leads::source::Contour {
    use leads::source::Segment as S;
    leads::source::Contour {
        start: contour.start,
        segments: contour
            .segments
            .iter()
            .map(|segment| match *segment {
                Segment::Line { to } => S::Line { to },
                Segment::Quad { control, to } => S::Quad { control, to },
                Segment::Cubic { controls, to } => S::Cubic { controls, to },
                Segment::Arc {
                    center,
                    radii,
                    rotation,
                    start,
                    sweep,
                } => S::Arc {
                    center,
                    radii,
                    rotation,
                    start,
                    sweep,
                },
            })
            .collect(),
    }
}
