//! Compress the trailing sheet into a shorter prefix, then separate overlaps.
use super::*;

impl PreparedJob<'_> {
    /// Preserve physical sheets, copies and exact orientations while shrinking
    /// the used vertical span on the sheet with the largest trailing offcut.
    /// A failed separation returns no candidate. Source and other sheets are
    /// immutable; only an independently valid material improvement is returned.
    pub fn compress_last_sheet(
        &self,
        source: &Layout,
        shrink_fraction: f64,
        seed: u64,
        control: &mut Control<'_>,
    ) -> Result<Option<Construction>> {
        ensure!(
            shrink_fraction.is_finite() && shrink_fraction > 0.0 && shrink_fraction <= 0.5,
            "compression fraction must be in (0, 0.5]"
        );
        control.checkpoint()?;
        let before = nestbolt_validator::job::validate(self.job, source)?;
        ensure!(before.valid, "compression requires a valid source layout");
        let metrics = before.metrics.as_ref().expect("valid metrics");
        let Some(last_id) = &metrics.last_sheet_id else {
            return Ok(None);
        };
        let sheet = source.sheets.iter().find(|s| &s.id == last_id).unwrap();
        let stock = self
            .job
            .stocks
            .iter()
            .position(|s| s.id == sheet.stock_id)
            .unwrap();
        let mut regions: Vec<_> = self
            .open_sheet(stock)
            .regions
            .into_iter()
            .map(|region| Occupied {
                region,
                placed: vec![],
            })
            .collect();
        let mut state = SearchState::new(seed, true, control);
        for placement in source.placements.iter().filter(|p| &p.sheet_id == last_id) {
            state.control.checkpoint()?;
            let part = self
                .job
                .parts
                .iter()
                .position(|p| p.id == placement.part_id)
                .unwrap();
            let item = &self.items[part];
            let internal = restore_transform(item, placement.transform);
            let mut shape = item.shape_cd().as_ref().clone();
            shape.transform_from(item.shape_cd(), &internal.compose());
            let mut matching = None;
            for (i, occupied) in regions.iter().enumerate() {
                state.before_collision()?;
                if !occupied
                    .region
                    .layout
                    .cde()
                    .detect_poly_collision(&shape, &NoFilter)
                {
                    matching = Some(i);
                    break;
                }
            }
            let Some(index) = matching else {
                // An externally supplied valid layout may not fit conservative
                // search proxies. It remains valid, but this trial is unavailable.
                return Ok(None);
            };
            let occupied = &mut regions[index];
            let key = occupied.region.layout.place_item(item, internal);
            occupied.placed.push(Tracked {
                key,
                part,
                placement: placement.clone(),
            });
        }

        for occupied in &mut regions {
            if occupied.placed.is_empty() {
                continue;
            }
            let n = occupied.region.nudge;
            let floor = occupied.region.search_bounds[1] + n;
            let top = occupied
                .placed
                .iter()
                .map(|p| {
                    occupied.region.layout.placed_items()[p.key]
                        .shape()
                        .bbox()
                        .y_max
                })
                .fold(f32::NEG_INFINITY, f32::max);
            let ceiling = floor + (top - floor) * (1.0 - shrink_fraction as f32);
            if !ceiling.is_finite() || ceiling <= floor + 2.0 * n {
                return Ok(None);
            }
            occupied.region.search_bounds[3] = ceiling;
            for tracked in &mut occupied.placed {
                state.control.checkpoint()?;
                let placed = &occupied.region.layout.placed_items()[tracked.key];
                let bounds = placed.shape().bbox();
                if bounds.y_max - bounds.y_min > ceiling - floor - 2.0 * n {
                    return Ok(None);
                }
                let old = placed.d_transf();
                let (x, y) = old.translation();
                let dy = (ceiling - 2.0 * n - bounds.y_max).min(0.0);
                let next = DTransformation::new(old.rotation(), (x, y + dy))
                    .with_reflection(tracked.placement.transform.mirrored);
                tracked.placement.transform.translation[1] +=
                    f64::from(next.translation().1) - f64::from(y);
                occupied.region.layout.remove_item(tracked.key);
                tracked.key = occupied
                    .region
                    .layout
                    .place_item(&self.items[tracked.part], next);
                // Only this trial's added ceiling is new. Existing stock-side
                // clearance remains governed by the collision tree, whose valid
                // restored placements can sit within one rounding unit of the
                // constructor's extra search nudge.
                if occupied.region.layout.placed_items()[tracked.key]
                    .shape()
                    .bbox()
                    .y_max
                    > ceiling - n
                {
                    return Ok(None);
                }
            }
            // Clamping can create part overlaps. Defects and stock boundaries
            // remain fixed hazards, and every translation stays below the ceiling.
            if !self.separate_region(occupied, &mut state)? {
                return Ok(None);
            }
        }
        let mut layout = source.clone();
        for tracked in regions.iter().flat_map(|r| &r.placed) {
            let target = layout
                .placements
                .iter_mut()
                .find(|p| {
                    p.part_id == tracked.placement.part_id
                        && p.copy_index == tracked.placement.copy_index
                })
                .unwrap();
            target.transform = tracked.placement.transform;
        }
        let checked = nestbolt_validator::job::validate(self.job, &layout)?;
        ensure!(
            checked.valid,
            "compression failed independent validation: {:?}",
            checked.violations
        );
        if checked.metrics.as_ref().unwrap().material_area >= metrics.material_area {
            return Ok(None);
        }
        Ok(Some(Construction {
            algorithm: "nestbolt-compress-v1",
            seed,
            collision_checks: state.checks,
            surrogate_rejections: state.surrogate_rejections,
            proxy_notes: self.notes.clone(),
            complete: true,
            unplaced: self.job.parts.iter().map(|p| p.quantity).sum::<u32>()
                - layout.placements.len() as u32,
            layout,
        }))
    }
}
