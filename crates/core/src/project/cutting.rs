//! One preparation/report path for CLI, MCP, browser and standalone exports.
use super::*;
use nestbolt_validator::job::{Layout, Report};

pub struct PreparedRequest {
    pub job: Job,
    pub outlines: HashMap<String, Outline>,
    sources: crate::lead_in::source::Sources,
    cutting_sidecars: bool,
    leads: Option<crate::lead_in::Prepared>,
    lead_options: Option<crate::lead_in::Options>,
    common_options: Option<crate::common_line::Options>,
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct CuttingReport {
    #[serde(flatten)]
    pub validation: Report,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub common_line: Option<Vec<crate::common_line::Report>>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub lead_in: Option<crate::lead_in::LayoutPlan>,
    #[serde(skip)]
    sources: Option<crate::lead_in::source::Sources>,
}

impl Request {
    pub fn prepare(&self, library: &Library) -> Result<PreparedRequest> {
        let (job, outlines) = self.job(library)?;
        let cutting_sidecars = self.lead_in.is_some() && library.lightburn.is_some();
        let sources = if cutting_sidecars {
            library
                .lightburn_cut_sources()?
                .context("missing original cutting sources")?
        } else {
            // Preserving project exports do not use proxy outlines as cuts.
            if library.lightburn.is_some() {
                HashMap::new()
            } else {
                crate::lead_in::source::from_outlines(&job, &outlines)?
            }
        };
        let leads = self
            .lead_in
            .map(|options| {
                crate::lead_in::prepare_sources(&job, &sources, options, &HashMap::new())
            })
            .transpose()?;
        Ok(PreparedRequest {
            job,
            outlines,
            sources,
            cutting_sidecars,
            leads,
            lead_options: self.lead_in,
            common_options: self.common_line,
        })
    }

    /// Recompute from source settings and placed geometry; saved reports are
    /// never used as authority for export or validation.
    pub fn cutting_report(&self, library: &Library, layout: &Layout) -> Result<CuttingReport> {
        self.prepare(library)?.report(layout)
    }
}

impl PreparedRequest {
    pub fn report(&self, layout: &Layout) -> Result<CuttingReport> {
        let mut validation = nestbolt_validator::job::validate(&self.job, layout)?;
        if !validation.valid {
            return Ok(CuttingReport {
                validation,
                common_line: None,
                lead_in: None,
                sources: None,
            });
        }
        let common_line = self
            .common_options
            .map(|o| crate::common_line::analyze(&self.job, layout, &self.outlines, o))
            .transpose()?;
        let lead_in = self
            .leads
            .as_ref()
            .zip(self.lead_options)
            .map(|(initial, options)| {
                crate::lead_in::finalize_sources(
                    &self.job,
                    &self.sources,
                    layout,
                    options,
                    initial,
                    common_line.as_deref().unwrap_or_default(),
                )
            })
            .transpose()?;
        if let Some(leads) = &lead_in {
            validation.metrics = leads.validation.metrics.clone();
        }
        Ok(CuttingReport {
            validation,
            common_line,
            lead_in,
            sources: self.cutting_sidecars.then(|| self.sources.clone()),
        })
    }

    pub fn optimize(
        &self,
        options: crate::sheets::Options,
        progress: impl FnMut(&crate::sheets::Progress, &dyn Fn() -> Option<Layout>),
    ) -> Result<(crate::sheets::SheetResult, CuttingReport)> {
        let allow_part_in_hole = self.common_options.is_none();
        let mut result = if let Some(common) = self.common_options.filter(|o| o.search_bonus) {
            crate::sheets::optimize_with_common_bonus(
                self.leads.as_ref().map_or(&self.job, |p| &p.collision_job),
                &crate::common_line::search::Bonus {
                    job: &self.job,
                    outlines: &self.outlines,
                    options: common,
                },
                options,
                progress,
            )?
        } else {
            match &self.leads {
                Some(leads) => crate::sheets::optimize_with_material(
                    &leads.collision_job,
                    &self.job,
                    options,
                    allow_part_in_hole,
                    progress,
                )?,
                None => crate::sheets::optimize_with_part_in_hole(
                    &self.job,
                    options,
                    allow_part_in_hole,
                    progress,
                )?,
            }
        };
        let report = self.report(&result.layout)?;
        ensure!(
            report.validation.valid,
            "final layout failed independent validation"
        );
        result.validation.metrics = report.validation.metrics.clone();
        Ok((result, report))
    }
}

impl CuttingReport {
    pub fn review(&self, layout: &Layout, sheet_id: &str) -> Result<crate::export::ReviewPaths> {
        ensure!(
            self.validation.valid,
            "layout failed independent validation: {:?}",
            self.validation.violations
        );
        let mut review = self
            .lead_in
            .as_ref()
            .map(|p| p.review(layout, sheet_id))
            .transpose()?
            .unwrap_or_default();
        review.common = self
            .common_line
            .as_ref()
            .and_then(|reports| reports.iter().find(|r| r.sheet_id == sheet_id))
            .map_or_else(Vec::new, |r| r.paths.clone());
        if let Some(sources) = &self.sources {
            for p in layout.placements.iter().filter(|p| p.sheet_id == sheet_id) {
                let source = sources
                    .get(&p.part_id)
                    .context("placed copy has no original cutting source")?;
                let transform = crate::curves::Affine::placement(&p.transform)
                    .then(crate::curves::Affine::scale(layout.units.to_mm()));
                review.original_cuts.insert(
                    format!("{}#{}", p.part_id, p.copy_index),
                    source
                        .contours()
                        .map(|(c, _, closed)| crate::export::CutPath {
                            curve: c.transformed(&transform),
                            closed,
                        })
                        .collect(),
                );
            }
        }
        Ok(review)
    }
}
