use super::*;

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct AttachedAllowance {
    pub allowance: Allowance,
    pub start: source::Start,
}

#[derive(Clone, Debug, Deserialize, Serialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Flag {
    pub part_id: String,
    pub copy_index: u32,
    pub contour_index: usize,
    pub reason: String,
}

#[derive(Debug, Serialize, JsonSchema)]
pub struct Coverage {
    pub expected_contours: usize,
    pub reserved_contours: usize,
    pub flagged_contours: usize,
}

impl Report {
    fn issue(&mut self, message: String) {
        self.valid = false;
        self.metrics = None;
        self.violation_count += 1;
        if self.violations.len() < 128 {
            self.violations.push(message);
        }
    }
}

/// Reconstruct coverage and material from the original job and source curves.
/// Contour indices visit each component's outer boundary followed by its holes.
/// Flags are explicit unresolved contours, not assertions that a lead is safe.
pub fn validate_complete(
    job: &Job,
    layout: &Layout,
    sources: &[source::Part],
    attached: &[AttachedAllowance],
    flags: &[Flag],
) -> Result<Report> {
    ensure!(
        crate::job::validate(job, layout)?.valid,
        "lead checks require a valid original layout"
    );
    ensure!(
        attached.len() <= 100_000 && flags.len() <= 100_000,
        "too many lead decisions"
    );
    ensure!(
        sources.len() == job.parts.len(),
        "original source part coverage differs from job"
    );
    let parts: HashMap<_, _> = job.parts.iter().map(|p| (p.id.as_str(), p)).collect();
    let mut originals = HashMap::new();
    let mut contours = HashMap::new();
    let mut counts = HashMap::new();
    let mut closed_counts = HashMap::new();
    for source in sources {
        let id = source.part_id.as_str();
        let part = parts.get(id).context("unknown original source part")?;
        ensure!(
            !originals.contains_key(id),
            "duplicate original source part"
        );
        if source.basis == source::Basis::MaterialBoundaries {
            ensure!(
                source.open_contours.is_empty() && source.extra_material.is_empty(),
                "material boundaries cannot contain extra cutting metadata"
            );
            ensure!(
                source.components.len() == part.geometry.len(),
                "original source component count differs from job"
            );
            for (component, polygon) in source.components.iter().zip(&part.geometry) {
                ensure!(
                    component.holes.len() == polygon.holes.len(),
                    "original source hole count differs from job"
                );
            }
        }
        for open in &source.open_contours {
            open.check_open(job.units)?;
        }
        let polygons = source
            .components
            .iter()
            .chain(&source.extra_material)
            .map(|c| c.polygon_mm(job.units))
            .collect::<Result<Vec<_>>>()?;
        let body = if source.basis == source::Basis::MaterialBoundaries {
            // Ordinary components must remain disjoint. Only native cutting
            // metadata can include overlapping protected artwork bounds.
            Footprint::from_polygons(&polygons, Units::Mm, RigidTransform::default())?
        } else {
            let mut body: Option<Footprint> = None;
            for polygon in &polygons {
                let next = Footprint::new(polygon, Units::Mm, RigidTransform::default())?;
                body = Some(match body {
                    Some(previous) => previous.union(&next)?,
                    None => next,
                });
            }
            body.context("original source has no protected material")?
        };
        originals.insert(id, body.polygons()?);
        let closed_count: usize = source.components.iter().map(|c| 1 + c.holes.len()).sum();
        closed_counts.insert(id, closed_count);
        counts.insert(id, closed_count + source.open_contours.len());
        contours.insert(
            id,
            source
                .components
                .iter()
                .flat_map(|c| std::iter::once(&c.outer).chain(&c.holes))
                .chain(&source.open_contours)
                .collect::<Vec<_>>(),
        );
    }
    let expected: HashSet<_> = layout
        .placements
        .iter()
        .flat_map(|p| {
            let count = counts[p.part_id.as_str()];
            (0..count).map(move |index| (p.part_id.as_str(), p.copy_index, index))
        })
        .collect();
    let allowances: Vec<_> = attached.iter().map(|a| a.allowance.clone()).collect();
    let mut report = validate_impl(job, layout, &allowances, Some(&originals), Some(&counts))?;
    report.coverage = Some(Coverage {
        expected_contours: expected.len(),
        reserved_contours: attached.len(),
        flagged_contours: flags.len(),
    });
    report.source_checked = true;
    let mut seen = HashSet::new();
    let mut owners = HashMap::new();
    for attached in attached {
        let a = &attached.allowance;
        let key = (a.part_id.as_str(), a.copy_index, a.contour_index);
        ensure!(
            expected.contains(&key),
            "lead refers to an unknown placed contour"
        );
        ensure!(seen.insert(key), "duplicate contour decision");
        ensure!(
            key.2 < closed_counts[key.0],
            "open cutting contours require an explicit flag, not a lead"
        );
        let label = format!("{}#{} contour {}", key.0, key.1, key.2);
        let point = contours[key.0][key.2].point_mm(attached.start, job.units)?;
        for path in &a.paths {
            let endpoint = path.point(1.0);
            if (point[0] - endpoint[0]).hypot(point[1] - endpoint[1]) > 8.0 * GRID {
                report.issue(format!(
                    "{label}: lead attachment differs from original contour start"
                ));
            }
        }
        let owner_key = (key.0, a.kerf_mm.to_bits());
        if let std::collections::hash_map::Entry::Vacant(entry) = owners.entry(owner_key) {
            let body =
                Footprint::from_polygons(&originals[key.0], Units::Mm, RigidTransform::default())?;
            entry.insert(Owner::new(body, a.kerf_mm)?);
        }
        if !owners[&owner_key].fits(&a.paths)? {
            report.issue(format!(
                "{label}: lead or pierce crosses its own original material"
            ));
        }
    }
    for flag in flags {
        let key = (flag.part_id.as_str(), flag.copy_index, flag.contour_index);
        ensure!(
            expected.contains(&key),
            "flag refers to an unknown placed contour"
        );
        ensure!(seen.insert(key), "duplicate contour decision");
        ensure!(
            !flag.reason.trim().is_empty(),
            "flag requires an explicit reason"
        );
    }
    // Layout order keeps diagnostics deterministic despite hash-based lookup.
    for p in &layout.placements {
        for index in 0..contours[p.part_id.as_str()].len() {
            if !seen.contains(&(p.part_id.as_str(), p.copy_index, index)) {
                report.issue(format!(
                    "{}#{} contour {index}: missing lead allowance or explicit flag",
                    p.part_id, p.copy_index
                ));
            }
        }
    }
    Ok(report)
}
