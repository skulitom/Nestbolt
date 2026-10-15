use std::collections::HashSet;

use super::*;
use nestbolt_validator::job::{Layout, Placement};

#[derive(Debug, Serialize, JsonSchema)]
pub struct PlacedPartPlan {
    pub copy_index: u32,
    pub sheet_id: String,
    /// World-space extent of original material plus final lead footprints.
    pub bounds_mm: [f64; 4],
    #[serde(flatten)]
    pub plan: PartPlan,
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct LayoutPlan {
    pub options: Options,
    pub expected_contours: usize,
    pub reserved_contours: usize,
    pub flagged_contours: usize,
    pub parts: Vec<PlacedPartPlan>,
    pub validation: leads::Report,
}

impl LayoutPlan {
    pub fn allowances(&self) -> Vec<leads::Allowance> {
        self.parts
            .iter()
            .flat_map(|p| {
                p.plan.reservations.iter().map(|r| leads::Allowance {
                    part_id: p.plan.part_id.clone(),
                    copy_index: p.copy_index,
                    contour_index: r.contour_index,
                    kerf_mm: self.options.kerf_mm,
                    paths: r.paths.clone(),
                })
            })
            .collect()
    }

    pub fn review(&self, layout: &Layout, sheet_id: &str) -> Result<crate::export::ReviewPaths> {
        let plans: HashMap<_, _> = self
            .parts
            .iter()
            .map(|p| ((p.plan.part_id.as_str(), p.copy_index), p))
            .collect();
        let mut review = crate::export::ReviewPaths::default();
        for placement in layout.placements.iter().filter(|p| p.sheet_id == sheet_id) {
            let part = plans
                .get(&(placement.part_id.as_str(), placement.copy_index))
                .context("placed copy has no lead report")?;
            ensure!(
                part.sheet_id == placement.sheet_id,
                "lead report belongs to a different sheet"
            );
            append_review(&mut review, &part.plan, placement, layout.units)?;
        }
        Ok(review)
    }
}

fn world(paths: &[Path], placement: &Placement, units: Units, kerf: f64) -> Result<Footprint> {
    let paths = paths
        .iter()
        .map(|p| p.transformed(placement.transform, units))
        .collect::<Result<Vec<_>>>()?;
    leads::footprint(&paths, kerf)
}

/// Recheck each placed copy and avoid its actual shared segments. A newly
/// selected lead must clear stock, all other original reservation envelopes,
/// and every already selected new lead. Keeping unused original reservations
/// as obstacles is conservative and avoids changing the searched placements.
pub fn finalize(
    job: &Job,
    curves: &HashMap<String, Outline>,
    layout: &Layout,
    options: Options,
    initial: &Prepared,
    common: &[crate::common_line::Report],
) -> Result<LayoutPlan> {
    finalize_sources(
        job,
        &source::from_outlines(job, curves)?,
        layout,
        options,
        initial,
        common,
    )
}

pub fn finalize_sources(
    job: &Job,
    sources: &source::Sources,
    layout: &Layout,
    options: Options,
    initial: &Prepared,
    common: &[crate::common_line::Report],
) -> Result<LayoutPlan> {
    options.validate()?;
    crate::scoring::MaterialAreas::new(job, &initial.collision_job)?;
    ensure!(
        nestbolt_validator::job::validate(job, layout)?.valid,
        "lead report requires a valid original layout"
    );
    // An existing layout can acquire safe leads by selecting new starts or
    // reporting flags. Validate the final paths, not discarded initial leads.
    let by_id: HashMap<_, _> = job.parts.iter().map(|p| (p.id.as_str(), p)).collect();
    let enlarged: HashMap<_, _> = initial
        .collision_job
        .parts
        .iter()
        .map(|p| (p.id.as_str(), p))
        .collect();
    let obstacles = layout
        .placements
        .iter()
        .map(|p| {
            let shape = Footprint::from_polygons(
                &enlarged[p.part_id.as_str()].geometry,
                job.units,
                p.transform,
            )?
            .with_units(Units::Mm);
            Ok((p, shape))
        })
        .collect::<Result<Vec<_>>>()?;
    let mut stocks = HashMap::new();
    for sheet in &layout.sheets {
        let stock = job
            .stocks
            .iter()
            .find(|s| s.id == sheet.stock_id)
            .context("unknown lead sheet")?;
        let shape = nestbolt_validator::job::usable_stock(stock, job.units)?
            .context("lead sheet has no usable area")?
            .with_units(Units::Mm);
        stocks.insert(sheet.id.as_str(), shape);
    }
    let mut parts = vec![];
    let mut selected: Vec<(&str, Footprint)> = vec![];
    let mut expected = 0;
    let mut reserved = 0;
    let mut flagged = 0;
    for placement in &layout.placements {
        let part = by_id[placement.part_id.as_str()];
        let key = format!("{}#{}", part.id, placement.copy_index);
        let exclusions = common
            .iter()
            .filter(|r| r.sheet_id == placement.sheet_id)
            .flat_map(|r| &r.shared_edges)
            .flat_map(|e| &e.owners)
            .filter(|c| c.part_copy == key)
            .map(|c| Exclusion {
                contour_index: 0,
                from_mm: c.from_mm,
                to_mm: c.to_mm,
            })
            .collect();
        let single = Job {
            parts: vec![part.clone()],
            ..job.clone()
        };
        let prepared = prepare_filtered(
            &single,
            sources,
            options,
            &HashMap::from([(part.id.clone(), exclusions)]),
            |_, _, paths| {
                let shape = world(paths, placement, job.units, options.kerf_mm)?;
                let inside = shape.inside(
                    &stocks[placement.sheet_id.as_str()],
                    job.edge_clearance * job.units.to_mm(),
                )?;
                if inside.outside_area > 0.0 || inside.clearance_violation {
                    return Ok(false);
                }
                for (other, body) in &obstacles {
                    if other.sheet_id == placement.sheet_id
                        && (other.part_id != placement.part_id
                            || other.copy_index != placement.copy_index)
                        && shape.compare(body, 0.0)?.overlap_area > 0.0
                    {
                        return Ok(false);
                    }
                }
                for (sheet, body) in &selected {
                    if *sheet == placement.sheet_id && shape.compare(body, 0.0)?.overlap_area > 0.0
                    {
                        return Ok(false);
                    }
                }
                Ok(true)
            },
        )?;
        let plan = prepared
            .parts
            .into_iter()
            .next()
            .context("empty lead plan")?;
        let count = sources
            .get(&part.id)
            .context("part has no original cutting source")?
            .contour_count();
        let mut seen = HashSet::new();
        for index in plan
            .reservations
            .iter()
            .map(|r| r.contour_index)
            .chain(plan.flags.iter().map(|r| r.contour_index))
        {
            ensure!(
                index < count && seen.insert(index),
                "duplicate or unknown contour in lead coverage"
            );
        }
        ensure!(
            seen.len() == count && plan.contour_count == count,
            "incomplete lead contour coverage"
        );
        let mut reserved_body =
            Footprint::from_polygons(&part.geometry, job.units, placement.transform)?
                .with_units(Units::Mm);
        for lead in &plan.reservations {
            let shape = world(&lead.paths, placement, job.units, options.kerf_mm)?;
            reserved_body = reserved_body.union(&shape)?;
            selected.push((placement.sheet_id.as_str(), shape));
        }
        expected += count;
        reserved += plan.reservations.len();
        flagged += plan.flags.len();
        parts.push(PlacedPartPlan {
            copy_index: placement.copy_index,
            sheet_id: placement.sheet_id.clone(),
            bounds_mm: reserved_body.bounds(),
            plan,
        });
    }
    let allowances: Vec<_> = parts
        .iter()
        .flat_map(|p| {
            p.plan
                .reservations
                .iter()
                .map(|r| leads::AttachedAllowance {
                    allowance: leads::Allowance {
                        part_id: p.plan.part_id.clone(),
                        copy_index: p.copy_index,
                        contour_index: r.contour_index,
                        kerf_mm: options.kerf_mm,
                        paths: r.paths.clone(),
                    },
                    start: leads::source::Start {
                        segment: r.start.segment,
                        parameter: r.start.parameter,
                    },
                })
        })
        .collect();
    let flags: Vec<_> = parts
        .iter()
        .flat_map(|p| {
            p.plan.flags.iter().map(|f| leads::Flag {
                part_id: p.plan.part_id.clone(),
                copy_index: p.copy_index,
                contour_index: f.contour_index,
                reason: f.reason.clone(),
            })
        })
        .collect();
    let independent_sources: Vec<_> = job
        .parts
        .iter()
        .map(|p| sources[&p.id].independent(&p.id))
        .collect();
    let validation =
        leads::validate_complete(job, layout, &independent_sources, &allowances, &flags)?;
    ensure!(
        validation.valid,
        "final lead allowances failed independent validation: {:?}",
        validation.violations
    );
    Ok(LayoutPlan {
        options,
        expected_contours: expected,
        reserved_contours: reserved,
        flagged_contours: flagged,
        parts,
        validation,
    })
}
