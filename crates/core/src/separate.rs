//! Sparrow's overlap-minimising separator (Gardeyn et al., arXiv:2509.13329,
//! Algorithms 1, 5, 7, 8 and 9), adapted from sparrow 0.3.0 (MIT, Copyright (c)
//! Jeroen Gardeyn; see THIRD_PARTY_NOTICES) to any jagua layout. Sparrow's own
//! separator is bound to its strip problem; this one also handles container
//! holes, which represent sheet boundaries and stock defects. The exterior and
//! every hole share one static collision entry per item, quantified by bounding
//! boxes as Sparrow quantifies the exterior. A single worker moves items in the
//! master layout, so a seed and the same work give the same result.
use jagua_rs::{
    Instant,
    collision_detection::hazards::{
        BasicHazardEntity, HazKey,
        collector::{BasicHazardCollector, HazardCollector},
        filter::NoFilter,
    },
    entities::{Item, Layout, LayoutSnapshot, PItemKey},
    geometry::{
        DTransformation,
        geo_traits::TransformableFrom,
        primitives::{Rect, SPolygon},
    },
};
use rand::{SeedableRng, rngs::Xoshiro256PlusPlus, seq::SliceRandom};
use slotmap::SecondaryMap;
use sparrow::{
    consts::{GLS_WEIGHT_DECAY, GLS_WEIGHT_MAX_INC_RATIO, GLS_WEIGHT_MIN_INC_RATIO},
    eval::sample_eval::{SampleEval, SampleEvaluator},
    quantify::{
        calc_shape_penalty, quantify_collision_poly_container, quantify_collision_poly_poly,
    },
    sample::search::{SampleConfig, search_placement},
    util::terminator::Terminator,
};

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
}

impl Tracker {
    pub fn new(layout: &Layout) -> Self {
        let size = layout.placed_items().len();
        let mut tracker = Self {
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
                    let other = layout.placed_items()[*pk].shape();
                    let p = self.pair(idx, self.index[*pk]);
                    self.pairs[p].loss = quantify_collision_poly_poly(shape, other);
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
            e.weight = (e.weight * multiplier).max(1.0);
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
            quantify_collision_poly_poly(layout.placed_items()[*pk].shape(), shape)
                * tracker.pair_weight(key, *pk)
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
            loss += weighted(layout, tracker, *key, &hazard, shape);
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
}

impl Separator {
    pub fn new(layout: Layout, seed: u64, config: Config) -> Self {
        Self {
            tracker: Tracker::new(&layout),
            layout,
            rng: Xoshiro256PlusPlus::seed_from_u64(seed),
            config,
            evals: 0,
        }
    }

    /// Algorithm 9: move colliding items until the layout is overlap-free or
    /// repeated strikes bring no substantial improvement. Returns the least
    /// overlapping layout seen and its tracker; a zero loss means feasible.
    pub fn separate(&mut self, term: &impl Terminator) -> (LayoutSnapshot, Tracker) {
        let mut best = (self.layout.save(), self.tracker.clone());
        let mut best_loss = self.tracker.total_loss();
        if best_loss == 0.0 {
            return best;
        }
        let mut strikes = 0;
        'outer: while strikes < self.config.strike_limit && !term.kill() {
            let mut stale = 0;
            let initial = self.tracker.total_loss();
            while stale < self.config.iter_no_improvement_limit && !term.kill() {
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
            .keys()
            .filter(|&k| self.tracker.loss(k) > 0.0)
            .collect();
        candidates.shuffle(&mut self.rng);
        for key in candidates {
            if self.tracker.loss(key) == 0.0 {
                continue;
            }
            let item = self.layout.placed_items()[key].item().clone();
            let evaluator = Evaluator::new(&self.layout, &item, key, &self.tracker);
            let (best, evals) = search_placement(
                &self.layout,
                &item,
                Some(key),
                evaluator,
                self.config.sample,
                &mut self.rng,
            );
            self.evals += evals as u64;
            let (dt, _) = best.expect("the current placement is always a sample");
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
        match tracker {
            Some(t) if t.size == self.tracker.size => self.tracker.restore_keep_weights(t),
            _ => self.tracker = Tracker::new(&self.layout),
        }
    }

    /// Replace the container and rebuild the tracker. Items are kept in place.
    pub fn swap_container(&mut self, container: jagua_rs::entities::Container) {
        self.layout.swap_container(container);
        self.tracker = Tracker::new(&self.layout);
    }

    /// Insert a new item and rebuild the tracker.
    pub fn place(&mut self, item: &std::sync::Arc<Item>, dt: DTransformation) -> PItemKey {
        let key = self.layout.place_item(item, dt);
        self.tracker = Tracker::new(&self.layout);
        key
    }
}

/// A terminator that also stops when `limit` is reached.
pub struct Until(pub Instant);

impl Terminator for Until {
    fn kill(&self) -> bool {
        Instant::now() >= self.0
    }
    fn new_timeout(&mut self, duration: std::time::Duration) {
        self.0 = self.0.min(Instant::now() + duration);
    }
    fn timeout_at(&self) -> Option<Instant> {
        Some(self.0)
    }
}
