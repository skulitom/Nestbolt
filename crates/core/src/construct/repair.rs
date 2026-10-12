//! Remove one physical sheet while preserving the other placements. A bounded
//! displacement can unlock a blocked insertion; failed trials roll back.
use super::*;
use jagua_rs::entities::PItemKey;

mod compact;
mod compress;
mod displace;
mod relax;

#[derive(Clone)]
struct Tracked {
    key: PItemKey,
    part: usize,
    placement: Placement,
}

#[derive(Clone)]
struct Occupied {
    region: Region,
    placed: Vec<Tracked>,
}

impl Occupied {
    fn refresh(&mut self) {
        self.refresh_except(None);
    }

    fn refresh_except(&mut self, removed: Option<PItemKey>) {
        self.region.boxes.clear();
        self.region.contact_anchors.clear();
        for tracked in &self.placed {
            if removed == Some(tracked.key) {
                continue;
            }
            let shape = self.region.layout.placed_items()[tracked.key].shape();
            let b = shape.bbox();
            self.region.boxes.push([b.x_min, b.y_min, b.x_max, b.y_max]);
            self.region.contact_anchors.extend(contact_anchors(shape));
        }
    }

    fn insert(
        &mut self,
        item: &Arc<Item>,
        part: usize,
        mut placement: Placement,
        candidate: Candidate,
    ) {
        placement.transform = candidate.external;
        let key = self.region.layout.place_item(item, candidate.internal);
        let shape = self.region.layout.placed_items()[key].shape();
        let b = shape.bbox();
        self.region.boxes.push([b.x_min, b.y_min, b.x_max, b.y_max]);
        self.region.contact_anchors.extend(contact_anchors(shape));
        self.placed.push(Tracked {
            key,
            part,
            placement,
        });
    }
}

fn restore_transform(item: &Item, transform: RigidTransform) -> DTransformation {
    let (cx, cy) = item.shape_orig().pre_transform.translation();
    let (s, c) = transform.rotation_radians.sin_cos();
    let cx = f64::from(cx) * if transform.mirrored { -1.0 } else { 1.0 };
    let cy = f64::from(cy);
    DTransformation::new(
        (transform.rotation_radians
            + if transform.mirrored {
                std::f64::consts::PI
            } else {
                0.0
            }) as f32,
        (
            (transform.translation[0] - c * cx + s * cy) as f32,
            (transform.translation[1] - s * cx - c * cy) as f32,
        ),
    )
    .with_reflection(transform.mirrored)
}

impl PreparedJob<'_> {
    pub(crate) fn repair_ranked(
        &self,
        source: &Layout,
        rank: usize,
        options: Options,
        control: &mut Control<'_>,
    ) -> Result<Construction> {
        let mut loads: Vec<_> = source
            .sheets
            .iter()
            .enumerate()
            .map(|(i, sheet)| {
                let area: f32 = source
                    .placements
                    .iter()
                    .filter(|p| p.sheet_id == sheet.id)
                    .map(|p| {
                        let part = self
                            .job
                            .parts
                            .iter()
                            .position(|part| part.id == p.part_id)
                            .expect("validated part");
                        self.items[part].area()
                    })
                    .sum();
                (i, area)
            })
            .collect();
        loads.sort_by(|a, b| a.1.total_cmp(&b.1).then(a.0.cmp(&b.0)));
        ensure!(!loads.is_empty(), "repair requires sheets");
        self.repair_sheet_controlled(source, loads[rank % loads.len()].0, options, 8, control)
    }

    /// Try to remove a physical sheet from a valid all-parts layout compatible
    /// with these conservative proxies. No stock is opened. Failed insertions
    /// produce an explicitly incomplete trial; the supplied layout is immutable.
    /// `ejections` caps each of the single-victim and collision-guided trial
    /// lists per insertion. A guided trial moves at most two actual blockers.
    /// Up to two later separation trials admit eight initial blockers and use
    /// at most 20,000 collision queries each; only a valid separated trial survives.
    pub fn repair_sheet(
        &self,
        source: &Layout,
        donor: usize,
        options: Options,
        ejections: usize,
    ) -> Result<Construction> {
        self.repair_sheet_controlled(source, donor, options, ejections, &mut Control::unlimited())
    }

    fn repair_sheet_controlled(
        &self,
        source: &Layout,
        donor: usize,
        options: Options,
        ejections: usize,
        control: &mut Control<'_>,
    ) -> Result<Construction> {
        control.checkpoint()?;
        ensure!(
            self.job.mode == Mode::All,
            "sheet repair requires all-parts mode"
        );
        ensure!(
            donor < source.sheets.len() && source.sheets.len() > 1,
            "invalid donor sheet"
        );
        ensure!(
            (1..=360).contains(&options.free_rotations)
                && options.random_samples <= 100_000
                && ejections <= 8,
            "invalid repair work budget"
        );
        ensure!(
            nestbolt_validator::job::validate(self.job, source)?.valid,
            "repair requires an independently valid source layout"
        );
        let mut layout = Layout {
            sheets: source
                .sheets
                .iter()
                .enumerate()
                .filter(|(i, _)| *i != donor)
                .map(|(_, sheet)| sheet.clone())
                .collect(),
            placements: vec![],
            version: source.version,
            units: source.units,
        };
        let mut sheets: Vec<Vec<Occupied>> = layout
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
        let mut pending = vec![];
        let mut state = SearchState::new(options.seed, true, control);
        for placement in &source.placements {
            state.control.checkpoint()?;
            let part = self
                .job
                .parts
                .iter()
                .position(|p| p.id == placement.part_id)
                .expect("validated part");
            if placement.sheet_id == source.sheets[donor].id {
                pending.push((part, placement.clone()));
                continue;
            }
            let sheet = layout
                .sheets
                .iter()
                .position(|s| s.id == placement.sheet_id)
                .expect("validated sheet");
            let internal = restore_transform(&self.items[part], placement.transform);
            let mut shape = self.items[part].shape_cd().as_ref().clone();
            shape.transform_from(self.items[part].shape_cd(), &internal.compose());
            let mut matching = None;
            for (index, region) in sheets[sheet].iter().enumerate() {
                state.before_collision()?;
                if !region
                    .region
                    .layout
                    .cde()
                    .detect_poly_collision(&shape, &NoFilter)
                {
                    matching = Some(index);
                    break;
                }
            }
            let index = matching
                .context("source layout is incompatible with conservative repair proxies")?;
            let region = &mut sheets[sheet][index];
            let key = region.region.layout.place_item(&self.items[part], internal);
            region.placed.push(Tracked {
                key,
                part,
                placement: placement.clone(),
            });
        }
        for region in sheets.iter_mut().flatten() {
            region.refresh();
        }
        pending.sort_by(|(a, pa), (b, pb)| {
            self.items[*b]
                .area()
                .total_cmp(&self.items[*a].area())
                .then(a.cmp(b))
                .then(pa.copy_index.cmp(&pb.copy_index))
        });
        'pending: for (part, placement) in pending {
            state.control.checkpoint()?;
            if let Some((sheet, region, candidate)) =
                self.repair_position(&sheets, part, options, &mut state)?
            {
                let mut placed = placement.clone();
                placed.sheet_id = layout.sheets[sheet].id.clone();
                sheets[sheet][region].insert(&self.items[part], part, placed, candidate);
                continue;
            }
            // Search a fixed, bounded list of victims, starting with the smallest
            // movable shapes. A snapshot restores both collision and contact data.
            let mut victims: Vec<_> = sheets
                .iter()
                .enumerate()
                .flat_map(|(si, regions)| {
                    regions.iter().enumerate().flat_map(move |(ri, region)| {
                        region.placed.iter().map(move |p| (si, ri, p.key, p.part))
                    })
                })
                .collect();
            victims.sort_by(|a, b| self.items[a.3].area().total_cmp(&self.items[b.3].area()));
            for (sheet, region, key, victim_part) in victims.into_iter().take(ejections) {
                state.control.checkpoint()?;
                let snapshot = sheets[sheet][region].clone();
                let occupied = &mut sheets[sheet][region];
                let victim = occupied
                    .placed
                    .iter()
                    .find(|p| p.key == key)
                    .expect("live victim")
                    .clone();
                occupied.region.layout.remove_item(key);
                occupied.placed.retain(|p| p.key != key);
                occupied.refresh();
                if let Some(candidate) = search(
                    &occupied.region,
                    &self.items[part],
                    &self.job.parts[part],
                    options,
                    &mut state,
                )? {
                    let candidate = refine_translation(
                        &occupied.region,
                        &self.items[part],
                        candidate,
                        &mut state,
                    )?;
                    let mut placed = placement.clone();
                    placed.sheet_id = layout.sheets[sheet].id.clone();
                    occupied.insert(&self.items[part], part, placed, candidate);
                    if let Some((target_sheet, target_region, candidate)) =
                        self.repair_position(&sheets, victim_part, options, &mut state)?
                    {
                        let mut placed = victim.placement;
                        placed.sheet_id = layout.sheets[target_sheet].id.clone();
                        sheets[target_sheet][target_region].insert(
                            &self.items[victim_part],
                            victim_part,
                            placed,
                            candidate,
                        );
                        continue 'pending;
                    }
                }
                sheets[sheet][region] = snapshot;
            }
            if ejections > 0 {
                let proposals = self.displacement_candidates(
                    &sheets,
                    part,
                    options,
                    ejections.max(2),
                    8,
                    &mut state,
                )?;
                for proposal in proposals.ejections.into_iter().take(ejections) {
                    if self.try_displacement(
                        &mut sheets,
                        &layout,
                        (part, &placement),
                        proposal,
                        options,
                        &mut state,
                    )? {
                        continue 'pending;
                    }
                }
                for proposal in proposals.separation.into_iter().take(ejections.min(2)) {
                    if self.try_relaxation(
                        &mut sheets,
                        &layout,
                        (part, &placement),
                        proposal,
                        &mut state,
                    )? {
                        continue 'pending;
                    }
                }
            }
            // This trial never revisits an unplaced donor copy. Once direct
            // insertion and every ejection fail, adding later copies cannot
            // make the trial complete. Preserve the incumbent in the caller.
            break;
        }
        layout.placements = sheets
            .into_iter()
            .flatten()
            .flat_map(|region| region.placed.into_iter().map(|p| p.placement))
            .collect();
        layout
            .sheets
            .retain(|sheet| layout.placements.iter().any(|p| p.sheet_id == sheet.id));
        let unplaced =
            self.job.parts.iter().map(|p| p.quantity).sum::<u32>() - layout.placements.len() as u32;
        let checked = nestbolt_validator::job::validate(self.job, &layout)?;
        ensure!(
            checked.violations.iter().all(|v| v.code == "quantity"),
            "repair failed independent validation: {:?}",
            checked.violations
        );
        Ok(Construction {
            algorithm: "nestbolt-repair-v5",
            seed: options.seed,
            collision_checks: state.checks,
            surrogate_rejections: state.surrogate_rejections,
            proxy_notes: self.notes.clone(),
            complete: unplaced == 0,
            unplaced,
            layout,
        })
    }

    fn repair_position(
        &self,
        sheets: &[Vec<Occupied>],
        part: usize,
        options: Options,
        state: &mut SearchState<'_, '_>,
    ) -> Result<Option<(usize, usize, Candidate)>> {
        for (sheet, regions) in sheets.iter().enumerate() {
            for (region, occupied) in regions.iter().enumerate() {
                if let Some(candidate) = search(
                    &occupied.region,
                    &self.items[part],
                    &self.job.parts[part],
                    options,
                    state,
                )? {
                    return Ok(Some((
                        sheet,
                        region,
                        refine_translation(&occupied.region, &self.items[part], candidate, state)?,
                    )));
                }
            }
        }
        Ok(None)
    }
}
