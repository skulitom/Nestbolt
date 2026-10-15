//! Cutting sidecars use original source paths, never display/collision outlines.
use super::*;
use crate::{
    curves::Contour,
    lead_in::source::{Source, Sources},
};
use nestbolt_validator::{Footprint, RigidTransform, Units};

fn classify(contours: Vec<Contour>) -> Result<Vec<Outline>> {
    let bodies = contours
        .iter()
        .map(|c| {
            let polygon = Polygon {
                outer: c.flatten(0.0001)?,
                holes: vec![],
            };
            Footprint::new(&polygon, Units::Mm, RigidTransform::default())
        })
        .collect::<Result<Vec<_>>>()?;
    let parents = bodies
        .iter()
        .enumerate()
        .map(|(i, child)| {
            let mut containing = vec![];
            for (j, parent) in bodies.iter().enumerate() {
                if i != j
                    && parent.area() > child.area()
                    && child.inside(parent, 0.0)?.outside_area == 0.0
                {
                    containing.push(j);
                }
            }
            Ok(containing.into_iter().min_by(|&a, &b| {
                bodies[a]
                    .area()
                    .total_cmp(&bodies[b].area())
                    .then(a.cmp(&b))
            }))
        })
        .collect::<Result<Vec<_>>>()?;
    let depth = |mut index: usize| {
        let mut count = 0;
        while let Some(parent) = parents[index] {
            count += 1;
            index = parent;
        }
        count
    };
    Ok((0..contours.len())
        .filter(|&i| depth(i) % 2 == 0)
        .map(|i| Outline {
            outer: contours[i].clone(),
            holes: (0..contours.len())
                .filter(|&j| parents[j] == Some(i))
                .map(|j| contours[j].clone())
                .collect(),
        })
        .collect())
}

fn protect_bounds(bounds: [f64; 4], tolerance: f64) -> Outline {
    let [mut x0, mut y0, mut x1, mut y1] = bounds;
    if x0 == x1 {
        x0 -= tolerance;
        x1 += tolerance;
    }
    if y0 == y1 {
        y0 -= tolerance;
        y1 += tolerance;
    }
    Outline::from_polygon(&nestbolt_validator::job::rectangle(
        x0,
        y0,
        x1 - x0,
        y1 - y0,
    ))
}

impl Library {
    pub(crate) fn lightburn_cut_sources(&self) -> Result<Option<Sources>> {
        let Some(project) = &self.lightburn else {
            return Ok(None);
        };
        let document = Document::read(&project.xml, self.tolerance)?;
        check_fixed_groups(&document)?;
        let nesting = document.nesting_units(self.tolerance)?;
        let mut sources = Sources::new();
        for unit in &nesting.units {
            let id = project
                .unit_ids
                .get(unit.id)
                .context("unknown LightBurn unit; re-import project")?;
            let mut source = Source {
                cutting_contours: true,
                ..Source::default()
            };
            let mut closed = vec![];
            let mut pending: Vec<_> = unit
                .members
                .iter()
                .rev()
                .map(|&top| document.scene.top_level[top])
                .collect();
            while let Some(index) = pending.pop() {
                let shape = &document.scene.shapes[index];
                if shape.kind == "Group" {
                    pending.extend(shape.children.iter().rev().copied());
                    continue;
                }
                ensure!(
                    !shape.fixed && shape.geometry_complete,
                    "cutting sidecar requires complete movable source geometry"
                );
                let cutting = document.scene.layers.iter().any(|l| {
                    l.index == shape.cut_index && l.image == shape.image_layer && l.output && l.cuts
                });
                if cutting {
                    ensure!(
                        !shape.paths.is_empty(),
                        "cutting shape has no original curves"
                    );
                    for path in &shape.paths {
                        if path.closed {
                            closed.push(path.curve.clone());
                        } else {
                            source.open.push(path.curve.clone());
                            source.extra_material.push(protect_bounds(
                                crate::curves::bounds(&path.points(self.tolerance)?),
                                self.tolerance,
                            ));
                        }
                    }
                } else {
                    source.extra_material.push(protect_bounds(
                        shape
                            .bounds_mm
                            .context("non-cutting artwork has no protected bounds")?,
                        self.tolerance,
                    ));
                }
            }
            source.components = classify(closed).with_context(|| {
                format!(
                    "{id}: cutting contours must be closed without crossing or touching themselves"
                )
            })?;
            ensure!(
                sources.insert(id.clone(), source).is_none(),
                "duplicate original cutting unit"
            );
        }
        Ok(Some(sources))
    }
}
