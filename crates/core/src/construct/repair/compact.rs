//! Compact a complete layout in place, retaining physical sheet/copy identities.
use super::*;

impl PreparedJob<'_> {
    /// Translate existing placements down and left in bounded sweeps. Original
    /// rotations and reflections remain exact; no additional stock is opened.
    pub fn compact_layout(&self, source: &Layout, sweeps: u32) -> Result<Construction> {
        self.compact_controlled(source, sweeps, &mut Control::unlimited())
    }

    pub fn compact_controlled(
        &self,
        source: &Layout,
        sweeps: u32,
        control: &mut Control<'_>,
    ) -> Result<Construction> {
        self.compact_impl(source, sweeps, None, control)
    }

    /// Also search new positions and permitted orientations on the same region.
    /// Every accepted move lowers its placement cost without increasing its top
    /// edge. Sheet identities and the selected part copies remain unchanged.
    pub fn compact_with_relocation(
        &self,
        source: &Layout,
        sweeps: u32,
        options: Options,
        control: &mut Control<'_>,
    ) -> Result<Construction> {
        ensure!(
            (1..=360).contains(&options.free_rotations) && options.random_samples <= 100_000,
            "invalid compaction work budget"
        );
        self.compact_impl(source, sweeps, Some(options), control)
    }

    fn compact_impl(
        &self,
        source: &Layout,
        sweeps: u32,
        relocation: Option<Options>,
        control: &mut Control<'_>,
    ) -> Result<Construction> {
        ensure!((1..=8).contains(&sweeps), "compaction needs 1..=8 sweeps");
        control.checkpoint()?;
        let before = nestbolt_validator::job::validate(self.job, source)?;
        ensure!(
            before.valid,
            "compaction requires an independently valid source layout"
        );
        let mut sheets: Vec<Vec<Occupied>> = source
            .sheets
            .iter()
            .map(|sheet| {
                let stock = self
                    .job
                    .stocks
                    .iter()
                    .position(|s| s.id == sheet.stock_id)
                    .expect("validated stock");
                self.open_sheet(stock)
                    .regions
                    .into_iter()
                    .map(|region| Occupied {
                        region,
                        placed: vec![],
                    })
                    .collect()
            })
            .collect();
        let seed = relocation.map_or(0, |options| options.seed);
        let mut state = SearchState::new(seed, relocation.is_some(), control);
        for placement in &source.placements {
            state.control.checkpoint()?;
            let part = self
                .job
                .parts
                .iter()
                .position(|p| p.id == placement.part_id)
                .expect("validated part");
            let sheet = source
                .sheets
                .iter()
                .position(|s| s.id == placement.sheet_id)
                .expect("validated sheet");
            let internal = restore_transform(&self.items[part], placement.transform);
            let mut shape = self.items[part].shape_cd().as_ref().clone();
            shape.transform_from(self.items[part].shape_cd(), &internal.compose());
            let mut matching = None;
            for (index, occupied) in sheets[sheet].iter().enumerate() {
                state.before_collision()?;
                if !occupied
                    .region
                    .layout
                    .cde()
                    .detect_poly_collision(&shape, &NoFilter)
                {
                    matching = Some(index);
                    break;
                }
            }
            let occupied = &mut sheets[sheet][matching
                .context("source layout is incompatible with conservative compaction proxies")?];
            let key = occupied
                .region
                .layout
                .place_item(&self.items[part], internal);
            occupied.placed.push(Tracked {
                key,
                part,
                placement: placement.clone(),
            });
        }
        for occupied in sheets.iter_mut().flatten() {
            // Bottom-up sweeps first move lower obstacles, then the parts above
            // them. Stable ties keep input order; no platform-dependent RNG.
            occupied.placed.sort_by(|a, b| {
                let a = occupied.region.layout.placed_items()[a.key].shape().bbox();
                let b = occupied.region.layout.placed_items()[b.key].shape().bbox();
                a.y_min
                    .total_cmp(&b.y_min)
                    .then(a.x_min.total_cmp(&b.x_min))
            });
            for _ in 0..sweeps {
                let mut changed = false;
                for index in 0..occupied.placed.len() {
                    state.control.checkpoint()?;
                    let tracked = occupied.placed[index].clone();
                    let item = &occupied.region.layout.placed_items()[tracked.key];
                    let internal = item.d_transf();
                    let b = item.shape().bbox();
                    let mut candidate = Candidate {
                        internal,
                        external: tracked.placement.transform,
                        bounds: [b.x_min, b.y_min, b.x_max, b.y_max],
                        cost: b.y_max + 0.001 * b.x_max,
                    };
                    occupied.region.layout.remove_item(tracked.key);
                    if let Some(options) = relocation {
                        occupied.refresh_except(Some(tracked.key));
                        if let Some(found) = search_bounded(
                            &occupied.region,
                            &self.items[tracked.part],
                            &self.job.parts[tracked.part],
                            options,
                            &mut state,
                            Some((candidate.cost, candidate.bounds[3])),
                        )? && found.cost < candidate.cost
                            && found.bounds[3] <= candidate.bounds[3]
                        {
                            candidate = found;
                        }
                    }
                    // Translation refinement only queries collision data. Its
                    // bounds stay fixed; contact anchors are not read here.
                    let candidate = refine_translation(
                        &occupied.region,
                        &self.items[tracked.part],
                        candidate,
                        &mut state,
                    )?;
                    changed |= candidate.external.translation
                        != tracked.placement.transform.translation
                        || candidate.external.rotation_radians
                            != tracked.placement.transform.rotation_radians
                        || candidate.external.mirrored != tracked.placement.transform.mirrored;
                    let key = occupied
                        .region
                        .layout
                        .place_item(&self.items[tracked.part], candidate.internal);
                    occupied.placed[index].key = key;
                    occupied.placed[index].placement.transform = candidate.external;
                }
                if !changed {
                    break;
                }
            }
        }
        let mut layout = source.clone();
        // Keep the source ordering as well as each sheet and copy identity.
        for tracked in sheets.iter().flatten().flat_map(|r| &r.placed) {
            let placement = layout
                .placements
                .iter_mut()
                .find(|p| {
                    p.part_id == tracked.placement.part_id
                        && p.copy_index == tracked.placement.copy_index
                })
                .expect("validated unique copy");
            placement.transform = tracked.placement.transform;
        }
        let checked = nestbolt_validator::job::validate(self.job, &layout)?;
        crate::construct::check_trial(&checked, false, "compaction")?;
        // Proxy coordinates use f32 and conservative outlines; accept quality
        // using the independent original-geometry material metric as well.
        if checked
            .metrics
            .as_ref()
            .expect("valid metrics")
            .material_area
            > before
                .metrics
                .as_ref()
                .expect("valid source metrics")
                .material_area
        {
            layout = source.clone();
        }
        Ok(Construction {
            algorithm: if relocation.is_some() {
                "nestbolt-compact-relocated-v2"
            } else {
                "nestbolt-compact-v2"
            },
            seed,
            collision_checks: state.checks,
            surrogate_rejections: state.surrogate_rejections,
            proxy_notes: self.notes.clone(),
            complete: true,
            unplaced: self.job.parts.iter().map(|p| p.quantity).sum::<u32>()
                - layout.placements.len() as u32,
            layout,
        })
    }
}
