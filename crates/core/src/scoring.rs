//! Original material values for searches whose collision shapes include waste.
//! Stock consumption/offcuts still use the complete reserved cutting envelope.
use std::collections::HashMap;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::{
    Footprint, RigidTransform,
    job::{Job, Layout, Metrics, Report},
};

#[cfg(test)]
mod tests;

pub(crate) struct MaterialAreas {
    areas: HashMap<String, f64>,
    total: f64,
}

impl MaterialAreas {
    pub(crate) fn new(material: &Job, collision: &Job) -> Result<Self> {
        ensure!(
            material.parts.len() == collision.parts.len(),
            "material/collision part counts differ"
        );
        let mut same = material.clone();
        for (source, enlarged) in same.parts.iter_mut().zip(&collision.parts) {
            source.geometry = enlarged.geometry.clone();
        }
        ensure!(
            serde_json::to_value(same)? == serde_json::to_value(collision)?,
            "material/collision jobs may differ only in part geometry"
        );
        let mut areas = HashMap::new();
        let mut total = 0.0;
        for (source, enlarged) in material.parts.iter().zip(&collision.parts) {
            let body = Footprint::from_polygons(
                &source.geometry,
                material.units,
                RigidTransform::default(),
            )?;
            let reserved = Footprint::from_polygons(
                &enlarged.geometry,
                collision.units,
                RigidTransform::default(),
            )?;
            ensure!(
                body.inside(&reserved, 0.0)?.outside_area == 0.0,
                "collision envelope omits original material for {}",
                source.id
            );
            ensure!(
                areas.insert(source.id.clone(), body.area()).is_none(),
                "duplicate material part id"
            );
            total += body.area() * f64::from(source.quantity);
        }
        ensure!(total.is_finite(), "non-finite material area");
        Ok(Self { areas, total })
    }

    pub(crate) fn area(&self, id: &str) -> f64 {
        self.areas[id]
    }

    fn set(metrics: &mut Metrics, area: f64) {
        metrics.placed_area = area;
        metrics.utilization = if metrics.material_area > 0.0 {
            area / metrics.material_area
        } else {
            0.0
        };
    }

    pub(crate) fn apply(&self, layout: &Layout, report: &mut Report) -> Result<()> {
        if let Some(metrics) = &mut report.metrics {
            let area = layout
                .placements
                .iter()
                .map(|p| {
                    self.areas
                        .get(&p.part_id)
                        .copied()
                        .context("placed copy has no original material area")
                })
                .sum::<Result<f64>>()?;
            Self::set(metrics, area);
        }
        Ok(())
    }

    pub(crate) fn apply_complete(&self, metrics: &mut Metrics) {
        Self::set(metrics, self.total);
    }
}
