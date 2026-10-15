//! Sparrow's overlap-minimising separator (Gardeyn et al., arXiv:2509.13329,
//! Algorithms 1, 5, 7, 8 and 9), adapted from sparrow 0.3.0 (MIT, Copyright (c)
//! Jeroen Gardeyn; see THIRD_PARTY_NOTICES) to any jagua layout. Sparrow's own
//! separator is bound to its strip problem; this one also handles container
//! holes, which represent sheet boundaries and stock defects. The exterior and
//! every hole share one static collision entry per item, quantified by bounding
//! boxes as Sparrow quantifies the exterior. A single worker moves items in the
//! master layout, so a seed and the same work give the same result.
use jagua_rs::{
    collision_detection::hazards::{
        BasicHazardEntity, HazKey,
        collector::{BasicHazardCollector, HazardCollector},
        filter::NoFilter,
    },
    entities::{Item, Layout, LayoutSnapshot, PItemKey},
    geometry::{
        DTransformation,
        geo_enums::{GeoRelation, RotationRange},
        geo_traits::{CollidesWith, TransformableFrom},
        primitives::{Rect, SPolygon},
    },
};
use rand::{SeedableRng, rngs::Xoshiro256PlusPlus, seq::SliceRandom};
use slotmap::SecondaryMap;
use sparrow::{
    consts::{GLS_WEIGHT_DECAY, GLS_WEIGHT_MAX_INC_RATIO, GLS_WEIGHT_MIN_INC_RATIO},
    consts::{
        PRE_REFINE_CD_R_STEPS, PRE_REFINE_CD_TL_RATIOS, SND_REFINE_CD_R_STEPS,
        SND_REFINE_CD_TL_RATIOS, UNIQUE_SAMPLE_THRESHOLD,
    },
    eval::sample_eval::{SampleEval, SampleEvaluator},
    quantify::{
        calc_shape_penalty, quantify_collision_poly_container, quantify_collision_poly_poly,
    },
    sample::{search::SampleConfig, uniform_sampler::UniformBBoxSampler},
};

use crate::clock::{Clock, Deadline, Work};

mod score;

/// Ceiling for guided-local-search weights. Sparrow's update has none: a pair
/// that collides on every iteration grows by up to 2x each time until f32
/// overflows, and an infinite weight never decays, so every overlap with that
/// partner then scores the same. With at most 64 poles per surrogate a loss is
/// below 80 d² for parts of diameter d (under 1e10 at 10 m in millimetres), so
/// weighted losses and their sums stay far below `f32::MAX`.
const MAX_WEIGHT: f32 = 1e20;

#[derive(Clone, Copy, Debug)]
struct Entry {
    loss: f32,
    weight: f32,
}

impl Entry {
    const CLEAR: Self = Self {
        loss: 0.0,
        weight: 1.0,
    };
    fn weighted(&self) -> f32 {
        self.loss * self.weight
    }
}

/// Bounding-box quantification of an item overlapping a static region.
fn quantify_static(shape: &SPolygon, region: Rect) -> f32 {
    let bbox = shape.bbox();
    let overlap = match Rect::intersection(bbox, region) {
        Some(r) => r.area() + 0.0001 * bbox.area(),
        None => 0.0001 * bbox.area(),
    };
    2.0 * overlap.sqrt() * calc_shape_penalty(shape, shape)
}

/// The loss of one placed shape against a static hazard (exterior or a hole).
fn static_loss(layout: &Layout, shape: &SPolygon, hazard: &BasicHazardEntity) -> f32 {
    match hazard {
        BasicHazardEntity::Exterior => {
            quantify_collision_poly_container(shape, layout.container().outer_cd().bbox())
        }
        BasicHazardEntity::Hole { idx } => {
            let zone = layout.container().quality_zones()[0]
                .as_ref()
                .expect("hole hazards come from the quality-0 zone");
            quantify_static(shape, zone.shapes_cd()[*idx].bbox())
        }
        _ => unimplemented!("items in sheet search require full-quality stock"),
    }
}

/// Pairwise and static collision losses with their guided-local-search weights.
#[derive(Clone, Debug)]
pub struct Tracker {
    size: usize,
    index: SecondaryMap<PItemKey, usize>,
    pairs: Vec<Entry>,
    statics: Vec<Entry>,
    /// Item index of pinned blockers, quantified like the container edge.
    pinned: Option<usize>,
}

/// Loss between two placed shapes. A pinned blocker is a static region, so it
/// is quantified by bounding boxes like the exterior, never by its large area.
fn pair_loss(layout: &Layout, a: PItemKey, b: PItemKey, pinned: Option<usize>) -> f32 {
    let (pa, pb) = (&layout.placed_items()[a], &layout.placed_items()[b]);
    if Some(pb.item().idx()) == pinned {
        quantify_static(pa.shape(), pb.shape().bbox())
    } else if Some(pa.item().idx()) == pinned {
        quantify_static(pb.shape(), pa.shape().bbox())
    } else {
        quantify_collision_poly_poly(pa.shape(), pb.shape())
    }
}

impl Tracker {
    pub fn new(layout: &Layout) -> Self {
        Self::pinned(layout, None)
    }

    pub fn pinned(layout: &Layout, pinned: Option<usize>) -> Self {
        let size = layout.placed_items().len();
        let mut tracker = Self {
            pinned,
            size,
            index: layout
                .placed_items()
                .keys()
                .enumerate()
                .map(|(i, k)| (k, i))
                .collect(),
            pairs: vec![Entry::CLEAR; size * (size + 1) / 2],
            statics: vec![Entry::CLEAR; size],
        };
        for key in layout.placed_items().keys() {
            tracker.recompute(key, layout);
        }
        tracker
    }

    fn pair(&self, a: usize, b: usize) -> usize {
        let (row, col) = if a <= b { (a, b) } else { (b, a) };
        row * self.size + col - row * (row + 1) / 2
    }

    fn recompute(&mut self, key: PItemKey, layout: &Layout) {
        let idx = self.index[key];
        for other in 0..self.size {
            let p = self.pair(idx, other);
            self.pairs[p].loss = 0.0;
        }
        self.statics[idx].loss = 0.0;
        let placed = &layout.placed_items()[key];
        let shape = placed.shape();
        let mut collector = BasicHazardCollector::with_capacity(self.size + 1);
        layout
            .cde()
            .collect_poly_collisions(shape, &NoFilter, &mut collector);
        collector.remove_by_entity(&BasicHazardEntity::from((key, placed)));
        for (_, hazard) in collector.iter() {
            match hazard {
                BasicHazardEntity::PlacedItem { pk, .. } => {
                    let p = self.pair(idx, self.index[*pk]);
                    self.pairs[p].loss = pair_loss(layout, key, *pk, self.pinned);
                }
                hazard => self.statics[idx].loss += static_loss(layout, shape, hazard),
            }
        }
    }

    /// Re-key a moved item and refresh every entry that involves it.
    pub fn register_move(&mut self, layout: &Layout, old: PItemKey, new: PItemKey) {
        let idx = self.index.remove(old).expect("tracked item");
        self.index.insert(new, idx);
        self.recompute(new, layout);
    }

    pub fn loss(&self, key: PItemKey) -> f32 {
        let idx = self.index[key];
        (0..self.size)
            .map(|i| self.pairs[self.pair(idx, i)].loss)
            .sum::<f32>()
            + self.statics[idx].loss
    }

    pub fn weighted_loss(&self, key: PItemKey) -> f32 {
        let idx = self.index[key];
        (0..self.size)
            .map(|i| self.pairs[self.pair(idx, i)].weighted())
            .sum::<f32>()
            + self.statics[idx].weighted()
    }

    pub fn total_loss(&self) -> f32 {
        self.pairs.iter().chain(&self.statics).map(|e| e.loss).sum()
    }

    pub fn total_weighted_loss(&self) -> f32 {
        self.pairs
            .iter()
            .chain(&self.statics)
            .map(Entry::weighted)
            .sum()
    }

    fn pair_weight(&self, a: PItemKey, b: PItemKey) -> f32 {
        self.pairs[self.pair(self.index[a], self.index[b])].weight
    }

    fn static_weight(&self, key: PItemKey) -> f32 {
        self.statics[self.index[key]].weight
    }

    /// Algorithm 8: raise the weights of current collisions, decay the others.
    fn update_weights(&mut self) {
        let max = self
            .pairs
            .iter()
            .chain(&self.statics)
            .map(|e| e.loss)
            .fold(0.0, f32::max);
        for e in self.pairs.iter_mut().chain(&mut self.statics) {
            let multiplier = if e.loss == 0.0 {
                GLS_WEIGHT_DECAY
            } else {
                GLS_WEIGHT_MIN_INC_RATIO
                    + (GLS_WEIGHT_MAX_INC_RATIO - GLS_WEIGHT_MIN_INC_RATIO) * (e.loss / max)
            };
            e.weight = (e.weight * multiplier).clamp(1.0, MAX_WEIGHT);
        }
    }

    fn restore_keep_weights(&mut self, snapshot: &Tracker) {
        self.index = snapshot.index.clone();
        for (a, b) in self.pairs.iter_mut().zip(&snapshot.pairs) {
            a.loss = b.loss;
        }
        for (a, b) in self.statics.iter_mut().zip(&snapshot.statics) {
            a.loss = b.loss;
        }
    }
}

/// Algorithm 7: weighted collision loss of one candidate transformation.
struct Evaluator<'a> {
    layout: &'a Layout,
    item: &'a Item,
    tracker: &'a Tracker,
    key: PItemKey,
    current: (HazKey, BasicHazardEntity),
    collector: BasicHazardCollector,
    buffer: SPolygon,
    evals: usize,
}

impl<'a> Evaluator<'a> {
    fn new(layout: &'a Layout, item: &'a Item, key: PItemKey, tracker: &'a Tracker) -> Self {
        let entity = BasicHazardEntity::from((key, &layout.placed_items()[key]));
        let hazard = layout
            .cde()
            .haz_key(&entity)
            .expect("placed item is registered");
        Self {
            layout,
            item,
            tracker,
            key,
            current: (hazard, entity),
            collector: BasicHazardCollector::with_capacity(layout.placed_items().len() + 1),
            buffer: item.shape_cd().as_ref().clone(),
            evals: 0,
        }
    }
}

fn weighted(
    layout: &Layout,
    tracker: &Tracker,
    key: PItemKey,
    hazard: &BasicHazardEntity,
    shape: &SPolygon,
) -> f32 {
    match hazard {
        BasicHazardEntity::PlacedItem { pk, .. } => {
            let other = &layout.placed_items()[*pk];
            let loss = if Some(other.item().idx()) == tracker.pinned {
                quantify_static(shape, other.shape().bbox())
            } else {
                quantify_collision_poly_poly(other.shape(), shape)
            };
            loss * tracker.pair_weight(key, *pk)
        }
        hazard => static_loss(layout, shape, hazard) * tracker.static_weight(key),
    }
}

impl SampleEvaluator for Evaluator<'_> {
    fn evaluate_sample(
        &mut self,
        dt: DTransformation,
        upper_bound: Option<SampleEval>,
    ) -> SampleEval {
        self.evals += 1;
        let bound = match upper_bound {
            Some(SampleEval::Collision { loss }) => loss,
            Some(SampleEval::Clear { .. }) => 0.0,
            _ => f32::INFINITY,
        };
        let Self {
            layout,
            item,
            tracker,
            key,
            current,
            collector,
            buffer,
            ..
        } = self;
        let shape = &*buffer.transform_from(item.shape_cd().as_ref(), &dt.compose());
        collector.clear();
        collector.insert(current.0, current.1);
        let ignored = collector.len();
        let mut loss = 0.0;
        let mut stop = |hazard: BasicHazardEntity| {
            // Any collision ranks below a clear placement, regardless of its
            // numerical loss. Keep checking geometry, but skip quantification.
            if matches!(upper_bound, Some(SampleEval::Clear { .. })) {
                return true;
            }
            let value = match hazard {
                BasicHazardEntity::PlacedItem { pk, .. }
                    if Some(layout.placed_items()[pk].item().idx()) != tracker.pinned =>
                {
                    score::pair(
                        layout.placed_items()[pk].shape(),
                        shape,
                        tracker.pair_weight(*key, pk),
                        loss,
                        bound,
                    )
                }
                _ => Some(weighted(layout, tracker, *key, &hazard, shape)),
            };
            let Some(value) = value else {
                return true;
            };
            loss += value;
            loss > bound
        };
        let cde = layout.cde();
        let stopped = cde
            .collect_surrogate_collisions_until(shape, &NoFilter, collector, &mut stop)
            || cde.collect_poly_collisions_until(shape, &NoFilter, collector, &mut stop);
        if stopped {
            SampleEval::Invalid
        } else if collector.len() == ignored {
            SampleEval::Clear { loss: 0.0 }
        } else {
            SampleEval::Collision { loss }
        }
    }

    fn n_evals(&self) -> usize {
        self.evals
    }
}

#[derive(Clone, Copy, Debug)]
pub struct Config {
    pub iter_no_improvement_limit: usize,
    pub strike_limit: usize,
    pub sample: SampleConfig,
}

/// Sparrow's exploration separator settings.
pub const EXPLORE: Config = Config {
    iter_no_improvement_limit: 200,
    strike_limit: 3,
    sample: SampleConfig {
        n_container_samples: 50,
        n_focussed_samples: 25,
        n_coord_descents: 3,
    },
};

/// Sparrow's compression separator settings.
pub const COMPRESS: Config = Config {
    iter_no_improvement_limit: 100,
    strike_limit: 5,
    sample: EXPLORE.sample,
};

pub struct Separator {
    pub layout: Layout,
    pub tracker: Tracker,
    pub rng: Xoshiro256PlusPlus,
    pub config: Config,
    pub evals: u64,
    /// Charged with evaluations times vertices for repeatable work budgets.
    pub clock: Clock,
    /// Items with this index are fixed hazards: they keep their place.
    pub pinned: Option<usize>,
    /// Container-wide samples are drawn here (the open part of the strip)
    /// instead of the whole container.
    pub region: Option<Rect>,
}

/// Sparrow's sample search (Algorithm 6) with container-wide samples drawn
/// from `region`: focussed samples around the current placement, uniform
/// samples, then two rounds of coordinate descent on the best few.
pub fn search_placement(
    layout: &Layout,
    item: &Item,
    current: Option<PItemKey>,
    mut evaluator: impl SampleEvaluator,
    config: SampleConfig,
    rng: &mut Xoshiro256PlusPlus,
    region: Rect,
) -> (Option<(DTransformation, SampleEval)>, usize) {
    let bbox = item.shape_cd().bbox();
    let min_dim = bbox.width().min(bbox.height());
    let mut best = BestSamples::new(config.n_coord_descents, min_dim * UNIQUE_SAMPLE_THRESHOLD);
    let container = layout.container().outer_cd().bbox();
    let focussed = current.and_then(|key| {
        let dt = layout.placed_items()[key].d_transf();
        let eval = evaluator.evaluate_sample(dt, Some(best.upper_bound()));
        best.report(dt, eval);
        UniformBBoxSampler::new(layout.placed_items()[key].shape().bbox(), item, container)
    });
    if let Some(sampler) = focussed {
        for _ in 0..config.n_focussed_samples {
            let dt = sampler.sample(rng);
            let eval = evaluator.evaluate_sample(dt, Some(best.upper_bound()));
            best.report(dt, eval);
        }
    }
    if let Some(sampler) = UniformBBoxSampler::new(region, item, container) {
        for _ in 0..config.n_container_samples {
            let dt = sampler.sample(rng);
            let eval = evaluator.evaluate_sample(dt, Some(best.upper_bound()));
            best.report(dt, eval);
        }
    }
    let wiggle = item.allowed_orientations().rotations() == &RotationRange::Continuous;
    let cd = |ratios: (f32, f32), rotations: (f32, f32)| CDConfig {
        t_step_init: min_dim * ratios.0,
        t_step_limit: min_dim * ratios.1,
        r_step_init: rotations.0,
        r_step_limit: rotations.1,
        wiggle,
    };
    for start in best.samples.clone() {
        let descended = refine_coord_desc(
            start,
            &mut evaluator,
            cd(PRE_REFINE_CD_TL_RATIOS, PRE_REFINE_CD_R_STEPS),
            rng,
        );
        best.report(descended.0, descended.1);
    }
    let last = best.best().map(|s| {
        refine_coord_desc(
            s,
            &mut evaluator,
            cd(SND_REFINE_CD_TL_RATIOS, SND_REFINE_CD_R_STEPS),
            rng,
        )
    });
    (last, evaluator.n_evals())
}

/// Charge `evals` sample evaluations of `item`.
pub fn charge(clock: &Clock, item: &Item, evals: usize) {
    clock.charge(Work::Evaluation, evals as f64);
    clock.charge(
        Work::EvaluatedVertex,
        (evals * item.shape_cd().vertices().len()) as f64,
    );
}

impl Separator {
    pub fn new(layout: Layout, seed: u64, config: Config, clock: Clock) -> Self {
        let tracker = Tracker::new(&layout);
        charge_rebuild(&clock, &layout);
        Self {
            tracker,
            layout,
            rng: Xoshiro256PlusPlus::seed_from_u64(seed),
            config,
            evals: 0,
            clock,
            pinned: None,
            region: None,
        }
    }

    /// Algorithm 9: move colliding items until the layout is overlap-free or
    /// repeated strikes bring no substantial improvement. Returns the least
    /// overlapping layout seen and its tracker; a zero loss means feasible.
    pub fn separate(&mut self, term: &Deadline) -> (LayoutSnapshot, Tracker) {
        let mut best = (self.layout.save(), self.tracker.clone());
        let mut best_loss = self.tracker.total_loss();
        if best_loss == 0.0 {
            return best;
        }
        let mut strikes = 0;
        'outer: while strikes < self.config.strike_limit && !term.passed() {
            let mut stale = 0;
            let initial = self.tracker.total_loss();
            while stale < self.config.iter_no_improvement_limit && !term.passed() {
                self.move_items();
                let loss = self.tracker.total_loss();
                if loss == 0.0 {
                    best = (self.layout.save(), self.tracker.clone());
                    break 'outer;
                } else if loss < best_loss {
                    if loss < best_loss * 0.98 {
                        stale = 0;
                    }
                    best = (self.layout.save(), self.tracker.clone());
                    best_loss = loss;
                } else {
                    stale += 1;
                }
                self.tracker.update_weights();
            }
            if initial * 0.98 <= best_loss {
                strikes += 1;
            } else {
                strikes = 0;
            }
            self.rollback(&best.0, Some(&best.1));
        }
        best
    }

    /// Algorithm 5: give each colliding item, in random order, a better place.
    fn move_items(&mut self) {
        let mut candidates: Vec<_> = self
            .layout
            .placed_items()
            .iter()
            .filter(|(k, p)| Some(p.item().idx()) != self.pinned && self.tracker.loss(*k) > 0.0)
            .map(|(k, _)| k)
            .collect();
        candidates.shuffle(&mut self.rng);
        for key in candidates {
            if self.tracker.loss(key) == 0.0 {
                continue;
            }
            let item = self.layout.placed_items()[key].item().clone();
            let evaluator = Evaluator::new(&self.layout, &item, key, &self.tracker);
            let region = self
                .region
                .unwrap_or_else(|| self.layout.container().outer_cd().bbox());
            let (best, evals) = search_placement(
                &self.layout,
                &item,
                Some(key),
                evaluator,
                self.config.sample,
                &mut self.rng,
                region,
            );
            self.evals += evals as u64;
            charge(&self.clock, &item, evals);
            let (dt, _) = best.expect("the current placement is always a sample");
            // Coordinate descent is unbounded: when an item cannot fit, it may
            // walk off the container entirely. Keep its current position rather
            // than registering a hazard with no edges in the quadtree root.
            let mut buffer = item.shape_cd().as_ref().clone();
            let moved = buffer.transform_from(item.shape_cd().as_ref(), &dt.compose());
            if Rect::intersection(moved.bbox(), self.layout.container().outer_cd().bbox()).is_none()
            {
                continue;
            }
            // Bounding boxes can overlap at a corner while an angled or concave
            // outline misses the root completely. Fully contained bounds need
            // no edge scan; partially outside outlines must actually intersect.
            let root = self.layout.cde().bbox();
            if root.relation_to(moved.bbox()) != GeoRelation::Surrounding
                && !moved.edge_iter().any(|edge| root.collides_with(&edge))
            {
                continue;
            }
            self.move_item(key, dt);
        }
    }

    pub fn move_item(&mut self, key: PItemKey, dt: DTransformation) -> PItemKey {
        let item = self.layout.remove_item(key).item().clone();
        let new = self.layout.place_item(&item, dt);
        self.tracker.register_move(&self.layout, key, new);
        new
    }

    /// Restore a saved layout. With a tracker snapshot keep the current weights;
    /// otherwise rebuild the tracker from the layout.
    pub fn rollback(&mut self, snapshot: &LayoutSnapshot, tracker: Option<&Tracker>) {
        if self.layout.restore(snapshot).is_err() {
            self.layout = Layout::from_snapshot(snapshot);
        }
        self.clock.charge(
            Work::RegisteredItem,
            self.layout.placed_items().len() as f64,
        );
        match tracker {
            Some(t) if t.size == self.tracker.size => self.tracker.restore_keep_weights(t),
            _ => self.rebuild(),
        }
    }

    /// Replace the container and rebuild the tracker. Items are kept in place.
    pub fn swap_container(&mut self, container: jagua_rs::entities::Container) {
        self.layout.swap_container(container);
        self.clock.charge(
            Work::RegisteredItem,
            self.layout.placed_items().len() as f64,
        );
        self.rebuild();
    }

    /// Treat items with this index as fixed blockers from now on.
    pub fn pin(&mut self, item: usize) {
        self.pinned = Some(item);
        self.rebuild();
    }

    /// Insert a new item and rebuild the tracker.
    pub fn place(&mut self, item: &std::sync::Arc<Item>, dt: DTransformation) -> PItemKey {
        let key = self.layout.place_item(item, dt);
        self.rebuild();
        key
    }

    /// Recompute every collision entry, charging the work.
    pub fn rebuild(&mut self) {
        self.tracker = Tracker::pinned(&self.layout, self.pinned);
        charge_rebuild(&self.clock, &self.layout);
    }
}

/// A full tracker rebuild queries every placed shape once.
fn charge_rebuild(clock: &Clock, layout: &Layout) {
    clock.charge(Work::TrackedItem, layout.placed_items().len() as f64);
    let vertices: usize = layout
        .placed_items()
        .values()
        .map(|p| p.shape().vertices().len())
        .sum();
    clock.charge(Work::TrackedVertex, vertices as f64);
}

/// The best few distinct samples, sorted by evaluation (sparrow's
/// `BestSamples`, which sparrow does not export).
#[derive(Clone, Debug)]
struct BestSamples {
    size: usize,
    samples: Vec<(DTransformation, SampleEval)>,
    unique: f32,
}

fn similar(a: DTransformation, b: DTransformation, threshold: f32) -> bool {
    let (ta, tb) = (a.translation(), b.translation());
    (ta.0 - tb.0).abs() < threshold
        && (ta.1 - tb.1).abs() < threshold
        && ((a.rotation() % std::f32::consts::TAU) - (b.rotation() % std::f32::consts::TAU)).abs()
            < 1.0_f32.to_radians()
        && a.reflected == b.reflected
}

impl BestSamples {
    fn new(size: usize, unique: f32) -> Self {
        Self {
            size,
            samples: vec![],
            unique,
        }
    }

    fn report(&mut self, dt: DTransformation, eval: SampleEval) {
        if eval >= self.upper_bound() {
            return;
        }
        let mut close = self
            .samples
            .iter()
            .filter(|(d, _)| similar(*d, dt, self.unique))
            .peekable();
        if close.peek().is_some() {
            if !close.all(|(_, e)| eval < *e) {
                return;
            }
            let unique = self.unique;
            self.samples.retain(|(d, _)| !similar(*d, dt, unique));
        } else if self.samples.len() == self.size {
            self.samples.pop();
        }
        self.samples.push((dt, eval));
        self.samples.sort_by_key(|(_, e)| *e);
    }

    fn best(&self) -> Option<(DTransformation, SampleEval)> {
        self.samples.first().copied()
    }

    fn upper_bound(&self) -> SampleEval {
        self.samples
            .get(self.size - 1)
            .map_or(SampleEval::Invalid, |(_, e)| *e)
    }
}

#[derive(Clone, Copy, Debug)]
struct CDConfig {
    t_step_init: f32,
    t_step_limit: f32,
    r_step_init: f32,
    r_step_limit: f32,
    wiggle: bool,
}

/// Coordinate descent to a local minimum (sparrow's `refine_coord_desc`).
/// Unlike sparrow, candidates keep the reflection of the start position.
fn refine_coord_desc(
    (start, eval): (DTransformation, SampleEval),
    evaluator: &mut impl SampleEvaluator,
    config: CDConfig,
    rng: &mut Xoshiro256PlusPlus,
) -> (DTransformation, SampleEval) {
    use rand::RngExt;
    use sparrow::consts::{CD_STEP_FAIL, CD_STEP_SUCCESS};
    let axes = if config.wiggle { 6 } else { 4 };
    let (mut pos, mut best) = (start, eval);
    let mut axis = rng.random_range(0..axes);
    let (mut sx, mut sy, mut sr) = (config.t_step_init, config.t_step_init, config.r_step_init);
    while !(sx < config.t_step_limit
        && sy < config.t_step_limit
        && (sr < config.r_step_limit || !config.wiggle))
    {
        let (tx, ty) = pos.translation();
        let r = pos.rotation();
        let candidates = match axis {
            0 => [(tx + sx, ty, r), (tx - sx, ty, r)],
            1 => [(tx, ty + sy, r), (tx, ty - sy, r)],
            2 => [(tx + sx, ty + sy, r), (tx - sx, ty - sy, r)],
            3 => [(tx - sx, ty + sy, r), (tx + sx, ty - sy, r)],
            _ => [(tx, ty, r + sr), (tx, ty, r - sr)],
        }
        .map(|(x, y, r)| DTransformation::new(r, (x, y)).with_reflection(pos.reflected));
        let (dt, e) = candidates
            .into_iter()
            .map(|c| (c, evaluator.evaluate_sample(c, Some(best))))
            .min_by_key(|(_, e)| *e)
            .expect("two candidates");
        let better = e < best;
        if e <= best {
            (pos, best) = (dt, e);
        }
        let m = if better {
            CD_STEP_SUCCESS
        } else {
            CD_STEP_FAIL
        };
        match axis {
            0 => sx *= m,
            1 => sy *= m,
            2 | 3 => {
                sx *= m.sqrt();
                sy *= m.sqrt();
            }
            _ => sr *= m,
        }
        if !better {
            axis = rng.random_range(0..axes);
        }
    }
    (pos, best)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::clock::Timing;
    use jagua_rs::io::{
        ext_repr::{ExtContainer, ExtItem, ExtOrientation, ExtRotation, ExtShape},
        import::Importer,
    };
    use sparrow::config::DEFAULT_SPARROW_CONFIG;

    fn square(side: f32) -> ExtShape {
        ExtShape::Rectangle {
            x_min: 0.0,
            y_min: 0.0,
            width: side,
            height: side,
        }
    }

    #[test]
    fn bounded_samples_match_full_scores_for_items_blockers_and_exterior() {
        let importer = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None);
        let container = importer
            .import_container(&ExtContainer {
                id: 0,
                shape: square(80.0),
                zones: vec![],
            })
            .unwrap();
        let items: Vec<_> = [10.0, 24.0]
            .into_iter()
            .enumerate()
            .map(|(i, side)| {
                importer
                    .import_item(
                        &ExtItem {
                            id: i as u64,
                            shape: square(side),
                            orientation: ExtOrientation {
                                rotation: ExtRotation::Continuous {},
                                reflection_axes: vec![90.0],
                            },
                            min_quality: None,
                        },
                        i,
                    )
                    .unwrap()
            })
            .collect();
        let mut layout = Layout::new(container);
        let key = layout.place_item(&items[0], DTransformation::new(0.0, (12.0, 12.0)));
        layout.place_item(&items[0], DTransformation::new(0.0, (18.0, 12.0)));
        layout.place_item(&items[1], DTransformation::new(0.0, (32.0, 32.0)));
        let tracker = Tracker::pinned(&layout, Some(1));
        let (mut clear, mut collisions) = (0, 0);
        for position in [
            (-15.0, -15.0),
            (12.0, 12.0),
            (18.0, 12.0),
            (32.0, 32.0),
            (65.0, 65.0),
            (90.0, 30.0),
        ] {
            for reflected in [false, true] {
                for rotation in [0.0, 0.37, 1.57] {
                    let dt = DTransformation::new(rotation, position).with_reflection(reflected);
                    let full =
                        Evaluator::new(&layout, &items[0], key, &tracker).evaluate_sample(dt, None);
                    let score = match full {
                        SampleEval::Clear { loss } => {
                            clear += 1;
                            loss
                        }
                        SampleEval::Collision { loss } => {
                            collisions += 1;
                            loss
                        }
                        SampleEval::Invalid => panic!("unbounded sample cannot be pruned"),
                    };
                    for bound in [
                        SampleEval::Clear { loss: 0.0 },
                        SampleEval::Collision {
                            loss: score.next_down().max(0.0),
                        },
                        SampleEval::Collision { loss: score },
                        SampleEval::Collision {
                            loss: score.next_up(),
                        },
                        SampleEval::Invalid,
                    ] {
                        let expected = match (full, bound) {
                            (SampleEval::Collision { .. }, SampleEval::Clear { .. }) => {
                                SampleEval::Invalid
                            }
                            (
                                SampleEval::Collision { loss },
                                SampleEval::Collision { loss: limit },
                            ) if loss > limit => SampleEval::Invalid,
                            _ => full,
                        };
                        assert_eq!(
                            Evaluator::new(&layout, &items[0], key, &tracker)
                                .evaluate_sample(dt, Some(bound)),
                            expected
                        );
                    }
                }
            }
        }
        assert!(clear > 0 && collisions > 0);
    }

    #[test]
    fn weights_stay_finite_when_a_collision_never_clears() {
        // Two sheet-sized squares can never separate: the same pair collides on
        // every iteration, so its weight grows by up to 2x each time.
        let importer = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None);
        let container = importer
            .import_container(&ExtContainer {
                id: 0,
                shape: square(10.0),
                zones: vec![],
            })
            .unwrap();
        let item = importer
            .import_item(
                &ExtItem {
                    id: 0,
                    orientation: ExtOrientation {
                        rotation: ExtRotation::Discrete { angles: vec![0.0] },
                        reflection_axes: vec![],
                    },
                    shape: square(10.0),
                    min_quality: None,
                },
                0,
            )
            .unwrap();
        let mut layout = Layout::new(container);
        let (px, py) = item.shape_orig().pre_transform.translation();
        for _ in 0..2 {
            layout.place_item(&item, DTransformation::new(0.0, (-px, -py)));
        }
        let clock = Clock::new(Timing::Work, 600.0);
        let mut sep = Separator::new(layout, 0, EXPLORE, clock.clone());
        let (_, best) = sep.separate(&Deadline {
            clock,
            at: f64::INFINITY,
        });
        assert!(best.total_loss() > 0.0, "the squares cannot separate");
        let max = |tracker: &Tracker| {
            tracker
                .pairs
                .iter()
                .chain(&tracker.statics)
                .map(|e| e.weight)
                .fold(0.0, f32::max)
        };
        // Without the ceiling this weight overflows to infinity.
        assert_eq!(max(&sep.tracker), MAX_WEIGHT);
        for tracker in [&best, &sep.tracker] {
            assert!(max(tracker) <= MAX_WEIGHT);
            assert!(tracker.total_weighted_loss().is_finite());
        }
    }
}
