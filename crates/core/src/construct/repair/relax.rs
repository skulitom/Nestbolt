//! Bounded translation separation on one receiver. Overlap is private working
//! state; only a fully separated trial can escape, otherwise the region rolls back.
use super::*;
use jagua_rs::collision_detection::hazards::{
    BasicHazardEntity, HazKey, collector::BasicHazardCollector, filter::HazardFilter,
};
use jagua_rs::geometry::geo_traits::DistanceTo;
use std::collections::BTreeMap;

struct IgnoreItem(PItemKey);
impl HazardFilter<BasicHazardEntity> for IgnoreItem {
    fn is_irrelevant(&self, _: HazKey, entity: &BasicHazardEntity) -> bool {
        matches!(entity, BasicHazardEntity::PlacedItem { pk, .. } if *pk == self.0)
    }
}

// Adapted from Sparrow 0.3.0, commit 4629b22795ae6b25b3b460ccde6fb36a71292b6d,
// src/quantify/{mod.rs,overlap_proxy.rs}, Algorithms 3/4 of arXiv:2509.13329.
// Copyright (c) 2025 Jeroen Gardeyn, KU Leuven. MIT; see core/Sparrow_LICENSE.
// This is a ranking proxy only. Jagua decides collisions; the independent
// original-geometry validator decides whether a completed layout is acceptable.
pub(super) fn overlap_penalty(a: &SPolygon, b: &SPolygon) -> f32 {
    let epsilon = a.diameter().max(b.diameter()) * 0.01;
    let mut area = 0.0;
    for p in &a.surrogate().poles {
        for q in &b.surrogate().poles {
            let depth = p.radius + q.radius - p.center.distance_to(&q.center);
            let smooth = if depth >= epsilon {
                depth
            } else {
                epsilon * epsilon / (2.0 * epsilon - depth)
            };
            area += smooth * p.radius.min(q.radius);
        }
    }
    let scale =
        (a.surrogate().convex_hull_area.sqrt() * b.surrogate().convex_hull_area.sqrt()).sqrt();
    (area * std::f32::consts::PI + epsilon * epsilon).sqrt() * scale
}

type Weights = BTreeMap<(usize, usize), f32>;
fn pair(a: usize, b: usize) -> (usize, usize) {
    (a.min(b), a.max(b))
}

fn collisions(
    occupied: &Occupied,
    index: usize,
    shape: &SPolygon,
    state: &mut SearchState<'_, '_>,
) -> Result<Option<Vec<(usize, f32)>>> {
    state.before_collision()?;
    let mut collector = BasicHazardCollector::new();
    let fixed = collect_collisions(
        &occupied.region,
        shape,
        &IgnoreItem(occupied.placed[index].key),
        &mut collector,
        |h| !matches!(h, BasicHazardEntity::PlacedItem { .. }),
    );
    if fixed {
        return Ok(None);
    }
    let mut result = vec![];
    for (_, entity) in collector.iter() {
        let BasicHazardEntity::PlacedItem { pk, .. } = entity else {
            unreachable!()
        };
        let other = occupied
            .placed
            .iter()
            .position(|p| p.key == *pk)
            .context("untracked separation hazard")?;
        let penalty = overlap_penalty(shape, occupied.region.layout.placed_items()[*pk].shape());
        if !penalty.is_finite() || penalty <= 0.0 {
            return Ok(None);
        }
        result.push((other, penalty));
    }
    result.sort_by_key(|(index, _)| *index);
    Ok(Some(result))
}

fn weighted_loss(values: &[(usize, f32)], index: usize, weights: &Weights) -> f32 {
    values
        .iter()
        .map(|(other, loss)| loss * weights.get(&pair(index, *other)).unwrap_or(&1.0))
        .sum()
}

impl PreparedJob<'_> {
    pub(super) fn try_relaxation(
        &self,
        sheets: &mut [Vec<Occupied>],
        layout: &Layout,
        incoming: (usize, &Placement),
        proposal: displace::Displacement,
        state: &mut SearchState<'_, '_>,
    ) -> Result<bool> {
        state.control.checkpoint()?;
        let occupied = &mut sheets[proposal.sheet][proposal.region];
        let snapshot = occupied.clone();
        let mut placement = incoming.1.clone();
        placement.sheet_id = layout.sheets[proposal.sheet].id.clone();
        occupied.insert(
            &self.items[incoming.0],
            incoming.0,
            placement,
            proposal.candidate,
        );
        let result = self.separate_region(occupied, state);
        if !matches!(result, Ok(true)) {
            *occupied = snapshot;
        }
        result
    }

    pub(super) fn separate_region(
        &self,
        occupied: &mut Occupied,
        state: &mut SearchState<'_, '_>,
    ) -> Result<bool> {
        let start = state.checks;
        let exhausted = |state: &SearchState<'_, '_>| state.checks - start >= 20_000;
        let mut weights = Weights::new();
        for _ in 0..24 {
            state.control.checkpoint()?;
            let mut scores = vec![0.0_f32; occupied.placed.len()];
            let mut pairs = vec![];
            for index in 0..occupied.placed.len() {
                if exhausted(state) {
                    return Ok(false);
                }
                let shape =
                    occupied.region.layout.placed_items()[occupied.placed[index].key].shape();
                let Some(hits) = collisions(occupied, index, shape, state)? else {
                    return Ok(false);
                };
                for (other, penalty) in hits {
                    if other > index {
                        let weighted = penalty * weights.get(&pair(index, other)).unwrap_or(&1.0);
                        scores[index] += weighted;
                        scores[other] += weighted;
                        pairs.push(pair(index, other));
                    }
                }
            }
            if pairs.is_empty() {
                occupied.refresh();
                return Ok(true);
            }
            let mut order: Vec<_> = (0..scores.len()).filter(|&i| scores[i] > 0.0).collect();
            order.sort_by(|&a, &b| scores[b].total_cmp(&scores[a]).then(a.cmp(&b)));
            // Bound a crowded trial as well as an individual move. Other
            // conflicted items can be selected on a later round.
            order.truncate(16);
            let mut moved = false;
            for index in order {
                let tracked = &occupied.placed[index];
                let item = &self.items[tracked.part];
                let placed = &occupied.region.layout.placed_items()[tracked.key];
                let mut internal = placed.d_transf();
                let bounds = placed.shape().bbox();
                let mut buffer = placed.shape().as_ref().clone();
                if exhausted(state) {
                    return Ok(false);
                }
                let Some(hits) = collisions(occupied, index, &buffer, state)? else {
                    return Ok(false);
                };
                let mut loss = weighted_loss(&hits, index, &weights);
                if loss == 0.0 {
                    continue;
                }
                let mut step = (bounds.x_max - bounds.x_min).min(bounds.y_max - bounds.y_min) / 4.0;
                for _ in 0..9 {
                    if step < occupied.region.nudge {
                        break;
                    }
                    for _ in 0..4 {
                        let mut best = None;
                        for (dx, dy) in [
                            (step, 0.0),
                            (-step, 0.0),
                            (0.0, step),
                            (0.0, -step),
                            (step, step),
                            (step, -step),
                            (-step, step),
                            (-step, -step),
                        ] {
                            if exhausted(state) {
                                return Ok(false);
                            }
                            let old = internal.translation();
                            let translation = (old.0 + dx, old.1 + dy);
                            if old == translation {
                                continue;
                            }
                            let dt = DTransformation::new(internal.rotation(), translation)
                                .with_reflection(
                                    occupied.placed[index].placement.transform.mirrored,
                                );
                            buffer.transform_from(item.shape_cd(), &dt.compose());
                            let b = buffer.bbox();
                            let limits = occupied.region.search_bounds;
                            let n = occupied.region.nudge;
                            if b.x_min < limits[0] + n
                                || b.y_min < limits[1] + n
                                || b.x_max > limits[2] - n
                                || b.y_max > limits[3] - n
                            {
                                continue;
                            }
                            let Some(hits) = collisions(occupied, index, &buffer, state)? else {
                                continue;
                            };
                            let score = weighted_loss(&hits, index, &weights);
                            if score < loss {
                                loss = score;
                                best = Some(dt);
                            }
                        }
                        let Some(next) = best else { break };
                        let old = internal.translation();
                        let new = next.translation();
                        let tracked = &mut occupied.placed[index];
                        tracked.placement.transform.translation[0] +=
                            f64::from(new.0) - f64::from(old.0);
                        tracked.placement.transform.translation[1] +=
                            f64::from(new.1) - f64::from(old.1);
                        occupied.region.layout.remove_item(tracked.key);
                        tracked.key = occupied.region.layout.place_item(item, next);
                        internal = next;
                        moved = true;
                        if loss == 0.0 {
                            break;
                        }
                    }
                    if loss == 0.0 {
                        break;
                    }
                    step *= 0.5;
                }
            }
            // Penalize persistent pairs at a local minimum. Sorted pair keys
            // keep accumulation and tie-breaking deterministic across runs.
            if !moved {
                for pair in pairs {
                    let weight = weights.entry(pair).or_insert(1.0);
                    *weight = (*weight * 1.5).min(64.0);
                }
            }
        }
        Ok(false)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use nestbolt_validator::{
        Units,
        job::{Margins, Rotations, rectangle, validate},
    };

    fn job() -> Job {
        Job {
            version: 1,
            name: "translation separation".into(),
            units: Units::Mm,
            clearance: 0.1,
            edge_clearance: 0.1,
            mode: Mode::All,
            parts: vec![Part {
                id: "square".into(),
                quantity: 3,
                geometry: vec![rectangle(-1.0, -1.0, 2.0, 2.0)],
                rotations: Rotations::List {
                    degrees: vec![37.0],
                },
                allow_mirror: true,
                priority: 1.0,
            }],
            stocks: vec![Stock {
                id: "stock".into(),
                width: 12.0,
                height: 8.0,
                count: Some(1),
                margins: Margins::default(),
                outline: vec![],
                defects: vec![rectangle(9.0, 0.0, 3.0, 8.0)],
            }],
        }
    }

    fn overlapping(prepared: &PreparedJob<'_>) -> Occupied {
        let region = prepared.open_sheet(0).regions.remove(0);
        let mut occupied = Occupied {
            region,
            placed: vec![],
        };
        for (copy, x) in [3.0, 4.0, 5.0].into_iter().enumerate() {
            let external = RigidTransform {
                translation: [x, 3.0],
                rotation_radians: 37_f64.to_radians(),
                mirrored: true,
            };
            let internal = restore_transform(&prepared.items[0], external);
            let key = occupied
                .region
                .layout
                .place_item(&prepared.items[0], internal);
            occupied.placed.push(Tracked {
                key,
                part: 0,
                placement: Placement {
                    part_id: "square".into(),
                    copy_index: copy as u32,
                    sheet_id: "keep".into(),
                    transform: external,
                },
            });
        }
        occupied.refresh();
        occupied
    }

    fn result(occupied: &Occupied) -> Layout {
        Layout {
            version: 1,
            units: Units::Mm,
            sheets: vec![Sheet {
                id: "keep".into(),
                stock_id: "stock".into(),
            }],
            placements: occupied
                .placed
                .iter()
                .map(|p| p.placement.clone())
                .collect(),
        }
    }

    #[test]
    fn overlapping_group_separates_repeatably_with_exact_angles_and_defects() {
        let job = job();
        let prepared = PreparedJob::new(&job).unwrap();
        let original = overlapping(&prepared);
        assert!(!validate(&job, &result(&original)).unwrap().valid);
        let run = || {
            let mut occupied = original.clone();
            let mut control = Control::unlimited();
            let mut state = SearchState::new(0, true, &mut control);
            assert!(prepared.separate_region(&mut occupied, &mut state).unwrap());
            assert!(state.checks <= 20_000);
            let layout = result(&occupied);
            assert!(validate(&job, &layout).unwrap().valid);
            for (a, b) in original.placed.iter().zip(&layout.placements) {
                assert_eq!(a.placement.copy_index, b.copy_index);
                assert_eq!(
                    a.placement.transform.rotation_radians,
                    b.transform.rotation_radians
                );
                assert_eq!(a.placement.transform.mirrored, b.transform.mirrored);
            }
            serde_json::to_string(&layout).unwrap()
        };
        assert_eq!(run(), run());
    }

    #[test]
    fn fixed_obstacle_cannot_be_solved_as_a_movable_pair() {
        let mut job = job();
        job.stocks[0].defects.push(rectangle(2.0, 2.0, 4.0, 2.0));
        let prepared = PreparedJob::new(&job).unwrap();
        let mut occupied = overlapping(&prepared);
        let original = serde_json::to_string(&result(&occupied)).unwrap();
        let mut control = Control::unlimited();
        let mut state = SearchState::new(0, true, &mut control);
        assert!(!prepared.separate_region(&mut occupied, &mut state).unwrap());
        assert_eq!(original, serde_json::to_string(&result(&occupied)).unwrap());
    }

    #[test]
    fn interrupted_trial_restores_receiver_and_contact_cache() {
        let job = job();
        let prepared = PreparedJob::new(&job).unwrap();
        let mut occupied = overlapping(&prepared);
        let incoming = occupied.placed.pop().unwrap();
        occupied.region.layout.remove_item(incoming.key);
        occupied.refresh();
        let layout = result(&occupied);
        let original = serde_json::to_string(&layout).unwrap();
        let keys: Vec<_> = occupied.placed.iter().map(|p| p.key).collect();
        let boxes = occupied.region.boxes.clone();
        let anchors = occupied.region.contact_anchors.clone();
        let mut sheets = vec![vec![occupied]];
        let mut unlimited = Control::unlimited();
        let mut search = SearchState::new(0, true, &mut unlimited);
        let proposal = prepared
            .displacement_candidates(&sheets, 0, Options::default(), 2, 8, &mut search)
            .unwrap()
            .separation
            .remove(0);
        let mut control = Control::new(Some(0), None);
        let mut state = SearchState::new(0, true, &mut control);
        let error = prepared
            .try_relaxation(
                &mut sheets,
                &layout,
                (0, &incoming.placement),
                proposal,
                &mut state,
            )
            .unwrap_err();
        assert!(
            error
                .downcast_ref::<crate::control::Interrupted>()
                .is_some()
        );
        let restored = &sheets[0][0];
        assert_eq!(original, serde_json::to_string(&result(restored)).unwrap());
        assert_eq!(
            keys,
            restored.placed.iter().map(|p| p.key).collect::<Vec<_>>()
        );
        assert_eq!(boxes, restored.region.boxes);
        assert_eq!(anchors, restored.region.contact_anchors);
        assert_eq!(restored.region.layout.placed_items().len(), keys.len());
    }
}
