//! Collision-guided proposals and bounded ejections. Static stock hazards are never
//! movable, and failed reinsertion restores every changed receiver region.
use super::*;
use jagua_rs::collision_detection::hazards::{BasicHazardEntity, collector::BasicHazardCollector};
use std::collections::HashMap;

#[derive(Clone)]
pub(super) struct Displacement {
    pub(super) sheet: usize,
    pub(super) region: usize,
    pub(super) candidate: Candidate,
    pub(super) victims: Vec<PItemKey>,
    area: f32,
    overlap: f64,
}

#[derive(Default)]
pub(super) struct Proposals {
    pub(super) ejections: Vec<Displacement>,
    pub(super) separation: Vec<Displacement>,
}

fn compare(a: &Displacement, b: &Displacement, separation: bool) -> std::cmp::Ordering {
    let common = || {
        a.victims
            .len()
            .cmp(&b.victims.len())
            .then(a.area.total_cmp(&b.area))
            .then(a.candidate.cost.total_cmp(&b.candidate.cost))
    };
    if separation {
        a.overlap.total_cmp(&b.overlap).then_with(common)
    } else {
        common()
    }
}

fn retain(list: &mut Vec<Displacement>, proposal: Displacement, limit: usize, separation: bool) {
    // Keep distinct blocker sets/orientations. Ejection favours a low position;
    // separation favours shallow overlap, even when it involves more blockers.
    if let Some(index) = list.iter().position(|p| {
        p.sheet == proposal.sheet
            && p.region == proposal.region
            && p.victims == proposal.victims
            && p.candidate.external.rotation_radians == proposal.candidate.external.rotation_radians
            && p.candidate.external.mirrored == proposal.candidate.external.mirrored
    }) {
        if !compare(&proposal, &list[index], separation).is_lt() {
            return;
        }
        list.remove(index);
    }
    list.push(proposal);
    list.sort_by(|a, b| compare(a, b, separation));
    list.truncate(limit);
}

impl PreparedJob<'_> {
    pub(super) fn displacement_candidates(
        &self,
        sheets: &[Vec<Occupied>],
        part: usize,
        options: Options,
        limit: usize,
        max_blockers: usize,
        state: &mut SearchState<'_, '_>,
    ) -> Result<Proposals> {
        let item = &self.items[part];
        let mut buffer = item.shape_cd().as_ref().clone();
        let mut collector = BasicHazardCollector::new();
        let mut proposals = Proposals::default();
        for (si, regions) in sheets.iter().enumerate() {
            for (ri, occupied) in regions.iter().enumerate() {
                let region = &occupied.region;
                let indices: HashMap<_, _> = occupied
                    .placed
                    .iter()
                    .enumerate()
                    .map(|(index, placed)| (placed.key, index))
                    .collect();
                for degrees in angles(&self.job.parts[part], options)? {
                    state.control.checkpoint()?;
                    let angle = degrees.to_radians();
                    for mirrored in
                        [false, true]
                            .into_iter()
                            .take(if self.job.parts[part].allow_mirror {
                                2
                            } else {
                                1
                            })
                    {
                        let rotation =
                            (angle + if mirrored { std::f64::consts::PI } else { 0.0 }) as f32;
                        let base =
                            DTransformation::new(rotation, (0.0, 0.0)).with_reflection(mirrored);
                        buffer.transform_from(item.shape_cd(), &base.compose());
                        let b = buffer.bbox();
                        let (width, height) = (b.x_max - b.x_min, b.y_max - b.y_min);
                        let limits = region.search_bounds;
                        let n = region.nudge;
                        let (min_x, min_y) = (limits[0] + n, limits[1] + n);
                        let (max_x, max_y) = (limits[2] - width - n, limits[3] - height - n);
                        if min_x > max_x || min_y > max_y {
                            continue;
                        }
                        let mut positions = vec![
                            (min_x, min_y),
                            (max_x, min_y),
                            (min_x, max_y),
                            (max_x, max_y),
                        ];
                        positions.extend(contact_positions(
                            region,
                            &buffer,
                            &mut state.contact_random,
                        ));
                        positions.extend((0..options.random_samples).map(|_| {
                            (
                                min_x + state.random.unit() * (max_x - min_x),
                                min_y + state.random.unit() * (max_y - min_y),
                            )
                        }));
                        positions
                            .retain(|&(x, y)| x >= min_x && y >= min_y && x <= max_x && y <= max_y);
                        positions.sort_by(|a, b| a.1.total_cmp(&b.1).then(a.0.total_cmp(&b.0)));
                        positions.dedup();
                        for (x, y) in positions {
                            state.before_collision()?;
                            let internal =
                                DTransformation::new(rotation, (x - b.x_min, y - b.y_min))
                                    .with_reflection(mirrored);
                            buffer.transform_from(item.shape_cd(), &internal.compose());
                            collector.clear();
                            let mut count = 0;
                            let stopped = region.layout.cde().collect_poly_collisions_until(
                                &buffer,
                                &NoFilter,
                                &mut collector,
                                |hazard| {
                                    count += 1;
                                    !matches!(hazard, BasicHazardEntity::PlacedItem { .. })
                                        || count > max_blockers
                                },
                            );
                            if stopped {
                                continue;
                            }
                            // Use source placement order, not tree traversal order,
                            // for deterministic ties and reinsertion.
                            let mut victim_indices = Vec::with_capacity(collector.len());
                            for (_, hazard) in collector.iter() {
                                let BasicHazardEntity::PlacedItem { pk, .. } = hazard else {
                                    unreachable!()
                                };
                                victim_indices
                                    .push(*indices.get(pk).context("untracked repair hazard")?);
                            }
                            victim_indices.sort_unstable();
                            let victims: Vec<_> = victim_indices
                                .into_iter()
                                .map(|index| &occupied.placed[index])
                                .collect();
                            ensure!(victims.len() == collector.len(), "untracked repair hazard");
                            let area = victims.iter().map(|p| self.items[p.part].area()).sum();
                            // Sum in source order, independent of collision-tree
                            // traversal. A low blocker count alone can conceal a
                            // deep intersection that translation cannot resolve.
                            let overlap = victims
                                .iter()
                                .map(|p| {
                                    f64::from(relax::overlap_penalty(
                                        &buffer,
                                        region.layout.placed_items()[p.key].shape(),
                                    ))
                                })
                                .sum();
                            let keys: Vec<_> = victims.iter().map(|p| p.key).collect();
                            let cost = y + height + 0.001 * (x + width);
                            let (cx, cy) = item.shape_orig().pre_transform.translation();
                            let (tx, ty) = internal.translation();
                            let (s, c) = angle.sin_cos();
                            let cx = f64::from(cx) * if mirrored { -1.0 } else { 1.0 };
                            let cy = f64::from(cy);
                            let proposal = Displacement {
                                sheet: si,
                                region: ri,
                                area,
                                overlap,
                                victims: keys,
                                candidate: Candidate {
                                    internal,
                                    external: RigidTransform {
                                        translation: [
                                            f64::from(tx) + c * cx - s * cy,
                                            f64::from(ty) + s * cx + c * cy,
                                        ],
                                        rotation_radians: angle,
                                        mirrored,
                                    },
                                    bounds: [x, y, x + width, y + height],
                                    cost,
                                },
                            };
                            if proposal.victims.len() <= 2 {
                                retain(&mut proposals.ejections, proposal.clone(), limit, false);
                            }
                            retain(&mut proposals.separation, proposal, limit.min(2), true);
                        }
                    }
                }
            }
        }
        Ok(proposals)
    }

    pub(super) fn try_displacement(
        &self,
        sheets: &mut [Vec<Occupied>],
        layout: &Layout,
        incoming: (usize, &Placement),
        proposal: Displacement,
        options: Options,
        state: &mut SearchState<'_, '_>,
    ) -> Result<bool> {
        state.control.checkpoint()?;
        let Displacement {
            sheet,
            region,
            candidate,
            victims,
            ..
        } = proposal;
        let mut snapshots = vec![(sheet, region, sheets[sheet][region].clone())];
        let occupied = &mut sheets[sheet][region];
        let mut removed: Vec<_> = occupied
            .placed
            .iter()
            .filter(|p| victims.contains(&p.key))
            .cloned()
            .collect();
        for victim in &removed {
            occupied.region.layout.remove_item(victim.key);
        }
        occupied.placed.retain(|p| !victims.contains(&p.key));
        occupied.refresh();
        // A complete collision collection guaranteed feasibility once these
        // items were removed. Refinement still checks all static hazards.
        let candidate =
            refine_translation(&occupied.region, &self.items[incoming.0], candidate, state)?;
        let mut placed = incoming.1.clone();
        placed.sheet_id = layout.sheets[sheet].id.clone();
        occupied.insert(&self.items[incoming.0], incoming.0, placed, candidate);
        removed.sort_by(|a, b| {
            self.items[b.part]
                .area()
                .total_cmp(&self.items[a.part].area())
        });
        for victim in removed {
            let Some((si, ri, candidate)) =
                self.repair_position(sheets, victim.part, options, state)?
            else {
                for (si, ri, original) in snapshots {
                    sheets[si][ri] = original;
                }
                return Ok(false);
            };
            if !snapshots.iter().any(|(s, r, _)| *s == si && *r == ri) {
                snapshots.push((si, ri, sheets[si][ri].clone()));
            }
            let mut placed = victim.placement;
            placed.sheet_id = layout.sheets[si].id.clone();
            sheets[si][ri].insert(&self.items[victim.part], victim.part, placed, candidate);
        }
        Ok(true)
    }
}
