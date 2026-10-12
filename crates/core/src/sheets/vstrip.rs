//! The last few sheets laid end to end as one fixed-height strip, separated by
//! thin walls (container holes). Shrinking the last sheet is then Sparrow's
//! exploration (Algorithm 12) and compression (Algorithm 13) over the whole
//! window: parts move between sheets through ordinary sampling, and a last
//! sheet that empties is removed. Earlier sheets stay fixed outside the window.
use super::*;
use crate::separate::{COMPRESS, EXPLORE, Separator};
use jagua_rs::geometry::primitives::Rect;
use jagua_rs::{
    collision_detection::hazards::{
        BasicHazardEntity, collector::BasicHazardCollector, filter::NoFilter,
    },
    entities::{Container, Layout as JLayout, LayoutSnapshot, PItemKey},
    geometry::geo_traits::CollidesWith,
    io::ext_repr::{ExtContainer, ExtQualityZone, ExtShape},
};
use rand::seq::IteratorRandom;
use rand_distr::{Distribution, Normal};
use sparrow::sample::uniform_sampler::convert_sample_to_closest_feasible;
use sparrow::{
    eval::{
        lbf_evaluator::LBFEvaluator,
        sample_eval::{SampleEval, SampleEvaluator},
    },
    sample::uniform_sampler::UniformBBoxSampler,
};

#[derive(Clone, Copy, Debug, PartialEq)]
struct Shape {
    sheets: usize,
    /// Length of the last sheet's region along the strip.
    last: f32,
}

struct Strip<'m, 'a> {
    model: &'m Model<'a>,
    gap: f32,
    clock: crate::clock::Clock,
    /// Containers per window size: the last sheet's region is always full and
    /// its shrinking end is a pinned blocker item instead.
    containers: std::cell::RefCell<std::collections::HashMap<usize, Container>>,
}

/// Item index reserved for the blocker that ends the last sheet.
fn blocker_index(model: &Model) -> usize {
    model.instance.items.len()
}

thread_local! {
    static TIMERS: std::cell::RefCell<std::collections::BTreeMap<&'static str, f64>> = Default::default();
}

/// Accumulate real seconds per phase for `NESTBOLT_DEBUG` profiles.
fn timed<T>(label: &'static str, f: impl FnOnce() -> T) -> T {
    let started = Instant::now();
    let out = f();
    let spent = started.elapsed().as_secs_f64();
    TIMERS.with(|t| *t.borrow_mut().entry(label).or_default() += spent);
    out
}

fn shift(dt: DTransformation, du: f32) -> DTransformation {
    let (x, y) = dt.translation();
    DTransformation::new(dt.rotation(), (x + du, y)).with_reflection(dt.reflected)
}

impl Strip<'_, '_> {
    fn pitch(&self) -> f32 {
        self.model.full_width + self.gap
    }

    fn start(&self, sheet: usize) -> f32 {
        sheet as f32 * self.pitch()
    }

    fn width(&self, s: Shape) -> f32 {
        self.start(s.sheets - 1) + s.last
    }

    fn height(&self) -> f32 {
        self.model.instance.base_strip.fixed_height
    }

    /// A single sheet ends at its current length, as Sparrow's strip does; a
    /// window of several sheets keeps every region full (cached) and ends the
    /// last one with a pinned blocker, since rebuilding walls is costly.
    fn container(&self, s: Shape) -> Result<Container> {
        if s.sheets == 1 {
            return timed("container", || self.container_inner(s));
        }
        if let Some(c) = self.containers.borrow().get(&s.sheets) {
            return Ok(c.clone());
        }
        let full = Shape {
            sheets: s.sheets,
            last: self.model.full_width,
        };
        let c = timed("container", || self.container_inner(full))?;
        self.containers.borrow_mut().insert(s.sheets, c.clone());
        Ok(c)
    }

    /// Make the separator's layout end the last region at `s.last`. Callers
    /// swap in the multi-sheet container when the window size changes.
    fn apply(&self, sep: &mut Separator, s: Shape) -> Result<()> {
        self.set_blocker(&mut sep.layout, s)?;
        if s.sheets == 1 {
            sep.region = None;
            sep.swap_container(self.container(s)?);
        } else {
            // Sample only the open strip, up to the blocker.
            sep.region = Rect::try_new(0.0, 0.0, self.width(s), self.height()).ok();
            sep.rebuild();
        }
        Ok(())
    }

    fn container_inner(&self, s: Shape) -> Result<Container> {
        self.clock.charge(crate::clock::Work::Container, 1.0);
        let height = self.height();
        let mut zones: Vec<_> = (0..s.sheets - 1)
            .map(|i| ExtQualityZone {
                quality: 0,
                shape: ExtShape::Rectangle {
                    x_min: self.start(i) + self.model.full_width,
                    y_min: 0.0,
                    width: self.gap,
                    height,
                },
            })
            .collect();
        for i in 0..s.sheets {
            for defect in &self.model.defects {
                let du = self.start(i);
                let points = defect.iter().map(|&(u, v)| (u + du, v)).collect();
                zones.push(ExtQualityZone {
                    quality: 0,
                    shape: ExtShape::SimplePolygon(jagua_rs::io::ext_repr::ExtSPolygon(points)),
                });
            }
        }
        // Keep quadtree cells comparable to one sheet in long strips.
        let aspect = (self.width(s) / height).max(1.0);
        let mut cde = DEFAULT_SPARROW_CONFIG.cde_config;
        cde.quadtree_depth += ((aspect / 2.0).max(1.0).log2().ceil() as u8).min(3);
        // Walls and defects are scored by bounding box, never by surrogate
        // poles, so a minimal surrogate avoids slow pole searches on thin walls.
        cde.item_surrogate_config = jagua_rs::geometry::fail_fast::SPSurrogateConfig {
            n_pole_limits: [(1, 0.0), (1, 0.75), (1, 0.90)],
            ff_pole_area_ratio: 1.0,
            n_ff_piers: 0,
        };
        Importer::new(cde, None, None)
            .with_min_item_separation(self.model.separation)?
            .import_container(&ExtContainer {
                id: 0,
                shape: ExtShape::Rectangle {
                    x_min: 0.0,
                    y_min: 0.0,
                    width: self.width(s),
                    height,
                },
                zones,
            })
    }

    fn sheet_of(&self, shape: &jagua_rs::geometry::primitives::SPolygon) -> usize {
        let b = shape.bbox();
        (((b.x_min + b.x_max) / 2.0) / self.pitch())
            .floor()
            .max(0.0) as usize
    }

    fn is_blocker(&self, p: &jagua_rs::entities::PlacedItem) -> bool {
        p.item().idx() == blocker_index(self.model)
    }

    fn clear_blocker(&self, layout: &mut JLayout) {
        let old: Vec<_> = layout
            .placed_items()
            .iter()
            .filter(|(_, p)| self.is_blocker(p))
            .map(|(k, _)| k)
            .collect();
        for k in old {
            layout.remove_item(k);
        }
    }

    /// Replace the blocker that ends the last region at `s.last`. It stays
    /// inside the deflated container even after its own inflation.
    fn set_blocker(&self, layout: &mut JLayout, s: Shape) -> Result<()> {
        let old: Vec<_> = layout
            .placed_items()
            .iter()
            .filter(|(_, p)| self.is_blocker(p))
            .map(|(k, _)| k)
            .collect();
        for k in old {
            layout.remove_item(k);
        }
        if s.sheets == 1 {
            return Ok(());
        }
        let margin = self.model.separation * 1.1 + self.height() * 1e-5;
        let start = self.start(s.sheets - 1) + s.last;
        let end = self.start(s.sheets - 1) + self.model.full_width - margin;
        let (low, high) = (margin, self.height() - margin);
        // A sliver adds no useful pressure and has no stable surrogate poles.
        if end - start <= (2.0 * margin).max(0.01 * self.height()) || high <= low {
            return Ok(());
        }
        let points = vec![(start, low), (end, low), (end, high), (start, high)];
        let imported = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None)
            .with_min_item_separation(self.model.separation)?
            .import_item(
                &jagua_rs::io::ext_repr::ExtItem {
                    id: u64::MAX,
                    shape: ExtShape::SimplePolygon(jagua_rs::io::ext_repr::ExtSPolygon(points)),
                    orientation: jagua_rs::io::ext_repr::ExtOrientation {
                        rotation: jagua_rs::io::ext_repr::ExtRotation::Discrete {
                            angles: vec![0.0],
                        },
                        reflection_axes: vec![],
                    },
                    min_quality: None,
                },
                blocker_index(self.model),
            );
        // Without a blocker the search simply has no end pressure this step.
        let Ok(item) = imported else {
            return Ok(());
        };
        let (px, py) = item.shape_orig().pre_transform.translation();
        layout.place_item(&item, DTransformation::new(0.0, (-px, -py)));
        Ok(())
    }

    fn layout(&self, window: &[SPProblem], s: Shape) -> Result<JLayout> {
        let mut layout = JLayout::new(self.container(s)?);
        let items: usize = window.iter().map(|w| w.layout().placed_items().len()).sum();
        self.clock
            .charge(crate::clock::Work::RegisteredItem, items as f64);
        for (i, sheet) in window.iter().enumerate() {
            for p in sheet.layout().placed_items().values() {
                layout.place_item(p.item(), shift(p.d_transf(), self.start(i)));
            }
        }
        self.set_blocker(&mut layout, s)?;
        Ok(layout)
    }

    /// Split a window layout back into fixed-width per-sheet problems.
    fn split(&self, layout: &JLayout, sheets: usize) -> Result<Vec<SPProblem>> {
        let mut out = (0..sheets)
            .map(|_| self.model.empty_sheet())
            .collect::<Result<Vec<_>>>()?;
        for p in layout
            .placed_items()
            .values()
            .filter(|p| !self.is_blocker(p))
        {
            let i = self.sheet_of(p.shape()).min(sheets - 1);
            out[i].place_item(SPPlacement {
                item_idx: p.item().idx(),
                d_transf: shift(p.d_transf(), -self.start(i)),
            });
        }
        Ok(out)
    }

    fn in_last(&self, layout: &JLayout, s: Shape) -> Vec<PItemKey> {
        layout
            .placed_items()
            .iter()
            .filter(|(_, p)| !self.is_blocker(p) && self.sheet_of(p.shape()) >= s.sheets - 1)
            .map(|(k, _)| k)
            .collect()
    }

    /// Shortest last region holding every part currently in it.
    fn fit_last(&self, layout: &JLayout, s: Shape) -> f32 {
        let start = self.start(s.sheets - 1);
        let end = self
            .in_last(layout, s)
            .into_iter()
            .map(|k| layout.placed_items()[k].shape().bbox().x_max)
            .fold(start, f32::max);
        let offset = self.model.separation / 2.0;
        ((end - start) * 1.00001 + offset).min(self.model.full_width)
    }
}

/// Collects items whose point of inaccessibility lies inside `key`'s shape.
fn contained(layout: &JLayout, key: PItemKey) -> Vec<PItemKey> {
    let outer = &layout.placed_items()[key];
    let mut collector = BasicHazardCollector::new();
    layout
        .cde()
        .collect_poly_collisions(outer.shape(), &NoFilter, &mut collector);
    collector
        .iter()
        .filter_map(|(_, h)| match h {
            BasicHazardEntity::PlacedItem { pk, .. } if *pk != key => Some(*pk),
            _ => None,
        })
        .filter(|pk| {
            let poi = layout.placed_items()[*pk].shape().poi();
            outer.shape().collides_with(&poi.center)
        })
        .collect()
}

/// Sparrow's disruption: swap two large, dissimilar parts (possibly on
/// different sheets) and carry along the parts their old positions contained.
fn disrupt(sep: &mut Separator) {
    let layout = &sep.layout;
    if layout.placed_items().len() < 2 {
        return;
    }
    let mut areas: Vec<f32> = layout
        .placed_items()
        .values()
        .filter(|p| Some(p.item().idx()) != sep.pinned)
        .map(|p| p.shape().surrogate().convex_hull_area)
        .collect();
    areas.sort_by(|a, b| b.total_cmp(a));
    let total: f32 = areas.iter().sum();
    let mut cumulative = 0.0;
    let cutoff = areas
        .iter()
        .copied()
        .find(|a| {
            cumulative += a;
            cumulative > total * 0.75
        })
        .unwrap_or(0.0);
    let pinned = sep.pinned;
    let large: Vec<_> = layout
        .placed_items()
        .iter()
        .filter(|(_, p)| Some(p.item().idx()) != pinned)
        .filter(|(_, p)| p.shape().surrogate().convex_hull_area >= cutoff)
        .map(|(k, _)| k)
        .collect();
    let Some(&a) = large.iter().choose(&mut sep.rng) else {
        return;
    };
    let pa = &layout.placed_items()[a];
    let (area, diameter) = (pa.shape().area(), pa.shape().diameter());
    let b = large
        .iter()
        .copied()
        .filter(|&k| {
            let p = layout.placed_items()[k].shape();
            (p.area() - area).abs() > area * 0.01
                && (p.diameter() - diameter).abs() > diameter * 0.01
        })
        .choose(&mut sep.rng)
        .or_else(|| {
            layout
                .placed_items()
                .iter()
                .filter(|(k, p)| *k != a && Some(p.item().idx()) != pinned)
                .map(|(k, _)| k)
                .choose(&mut sep.rng)
        });
    let Some(b) = b else {
        return;
    };
    let (dta, dtb) = (
        layout.placed_items()[a].d_transf(),
        layout.placed_items()[b].d_transf(),
    );
    let ia = layout.placed_items()[a].item().clone();
    let ib = layout.placed_items()[b].item().clone();
    let na = convert_sample_to_closest_feasible(dtb, &ia);
    let nb = convert_sample_to_closest_feasible(dta, &ib);
    let a = sep.move_item(a, na);
    let b = sep.move_item(b, nb);
    for (key, other, old, new) in [(a, b, dta, na), (b, a, dtb, nb)] {
        let convert = new.compose().inverse().transform(&old.compose());
        for c in contained(&sep.layout, key)
            .into_iter()
            .filter(|&c| c != other)
        {
            let p = &sep.layout.placed_items()[c];
            let dt = p.d_transf().compose().transform(&convert).decompose();
            let dt = convert_sample_to_closest_feasible(dt, p.item());
            sep.move_item(c, dt);
        }
    }
}

impl<F: FnMut(&Progress)> Search<'_, '_, F> {
    /// Validate a window snapshot with the frozen sheets and keep it if better.
    fn accept_window(
        &mut self,
        strip: &Strip,
        frozen: &[SPProblem],
        snapshot: &LayoutSnapshot,
        s: Shape,
        stage: &'static str,
    ) -> Result<bool> {
        let started = Instant::now();
        let layout = JLayout::from_snapshot(snapshot);
        let mut sheets = frozen.to_vec();
        sheets.extend(strip.split(&layout, s.sheets)?);
        let accepted = timed("accept", || self.accept(&sheets, stage));
        if std::env::var_os("NESTBOLT_DEBUG").is_some() {
            eprintln!("debug accept_window {stage}: {:?}", started.elapsed());
        }
        accepted
    }

    /// Shrink (or, at zero length, remove) the last sheet at a random split.
    fn shrink(
        &mut self,
        strip: &Strip,
        sep: &mut Separator,
        from: Shape,
        by: f32,
    ) -> Result<Shape> {
        let mut next = Shape {
            last: from.last - by,
            ..from
        };
        if next.last <= self.model.separation * 2.0 {
            if from.sheets == 1 {
                return Ok(from);
            }
            next = Shape {
                sheets: from.sheets - 1,
                last: self.model.full_width,
            };
        } else {
            let start = strip.start(from.sheets - 1);
            let split = start + self.rng.random_range(0.0..from.last);
            let moving: Vec<_> = sep
                .layout
                .placed_items()
                .iter()
                .filter(|(_, p)| !strip.is_blocker(p) && p.shape().centroid().0 > split)
                .map(|(k, p)| (k, p.d_transf()))
                .collect();
            for (key, dt) in moving {
                let item = sep.layout.remove_item(key).item().clone();
                sep.layout.place_item(&item, shift(dt, -by));
            }
        }
        if next.sheets != from.sheets {
            // Every hazard must lie inside the smaller container's quadtree:
            // drop the blocker and move the dropped sheet's parts onto the new
            // last sheet at the same local position, overlapping as they may.
            strip.clear_blocker(&mut sep.layout);
            let moving: Vec<_> = strip
                .in_last(&sep.layout, from)
                .into_iter()
                .map(|k| (k, sep.layout.placed_items()[k].d_transf()))
                .collect();
            for (key, dt) in moving {
                let item = sep.layout.remove_item(key).item().clone();
                sep.layout.place_item(&item, shift(dt, -strip.pitch()));
            }
            sep.layout.swap_container(strip.container(next)?);
        }
        strip.apply(sep, next)?;
        Ok(next)
    }

    /// Move parts of the last sheet into free gaps of earlier window sheets,
    /// largest first, by Sparrow's left-bottom sampling within each sheet.
    /// Earlier sheets are tried first. Returns the number of moved parts.
    fn fill_gaps(&mut self, strip: &Strip, sep: &mut Separator, shape: Shape) -> usize {
        if shape.sheets < 2 {
            return 0;
        }
        let mut keys = strip.in_last(&sep.layout, shape);
        keys.sort_by(|&a, &b| {
            let area = |k| sep.layout.placed_items()[k].item().area();
            area(b).total_cmp(&area(a))
        });
        let bounds = sep.layout.container().outer_cd().bbox();
        let samples = (1000 / (shape.sheets - 1)).max(200);
        let mut moved = 0;
        for key in keys {
            let placed = sep.layout.remove_item(key);
            let item = placed.item().clone();
            let mut best: Option<(DTransformation, SampleEval)> = None;
            for sheet in 0..shape.sheets - 1 {
                let start = strip.start(sheet);
                let Ok(region) =
                    Rect::try_new(start, 0.0, start + self.model.full_width, strip.height())
                else {
                    continue;
                };
                let Some(sampler) = UniformBBoxSampler::new(region, &item, bounds) else {
                    continue;
                };
                let mut evaluator = LBFEvaluator::new(&sep.layout, &item);
                for _ in 0..samples {
                    let dt = sampler.sample(&mut self.rng);
                    let eval = evaluator.evaluate_sample(dt, None);
                    if matches!(eval, SampleEval::Clear { .. })
                        && best.as_ref().is_none_or(|b| eval < b.1)
                    {
                        best = Some((dt, eval));
                    }
                }
                crate::separate::charge(&self.clock, &item, samples);
                if best.is_some() {
                    break;
                }
            }
            sep.layout
                .place_item(&item, best.as_ref().map_or(placed.d_transf(), |b| b.0));
            moved += usize::from(best.is_some());
        }
        if moved > 0 {
            sep.rebuild();
            self.stats.direct_insertions += moved as u64;
        }
        moved
    }

    /// Move each part of the last sheet, largest first, into one of the three
    /// emptiest other sheets: the receiver alone becomes a one-sheet layout, the
    /// part is dropped at a random position and the separator must resolve every
    /// overlap within that sheet. Successful receivers are written back.
    fn relocate(
        &mut self,
        strip: &Strip,
        sep: &mut Separator,
        shape: Shape,
        until: f64,
    ) -> Result<usize> {
        if shape.sheets < 2 {
            return Ok(0);
        }
        let single = strip.container(Shape {
            sheets: 1,
            last: self.model.full_width,
        })?;
        let bounds = single.outer_cd().bbox();
        let mut items: Vec<_> = strip
            .in_last(&sep.layout, shape)
            .into_iter()
            .map(|k| sep.layout.placed_items()[k].item().clone())
            .collect();
        items.sort_by(|a, b| b.area().total_cmp(&a.area()));
        let mut moved = 0;
        for item in items {
            let mut fill = vec![0.0_f32; shape.sheets - 1];
            for p in sep.layout.placed_items().values() {
                let i = strip.sheet_of(p.shape());
                if i < shape.sheets - 1 {
                    fill[i] += p.item().area();
                }
            }
            let mut targets: Vec<_> = (0..shape.sheets - 1).collect();
            targets.sort_by(|&a, &b| fill[a].total_cmp(&fill[b]));
            for target in targets.into_iter().take(3) {
                if self.clock.now() >= until {
                    return Ok(moved);
                }
                let Some(sampler) = UniformBBoxSampler::new(bounds, &item, bounds) else {
                    break;
                };
                let offset = strip.start(target);
                let members: Vec<_> = sep
                    .layout
                    .placed_items()
                    .iter()
                    .filter(|(_, p)| strip.sheet_of(p.shape()) == target)
                    .map(|(k, p)| (k, p.item().clone(), p.d_transf()))
                    .collect();
                let mut layout = JLayout::new(single.clone());
                for (_, it, dt) in &members {
                    layout.place_item(it, shift(*dt, -offset));
                }
                layout.place_item(&item, sampler.sample(&mut self.rng));
                let now = self.clock.now();
                let slice = now + ((until - now) * 0.25).min(2.0);
                let mut local =
                    Separator::new(layout, self.rng.next_u64(), EXPLORE, self.clock.clone());
                let (snapshot, tracker) = local.separate(&self.deadline(slice));
                if tracker.total_loss() > 0.0 {
                    self.stats.failed_insertions += 1;
                    continue;
                }
                let Some(&key) = strip
                    .in_last(&sep.layout, shape)
                    .iter()
                    .find(|&&k| sep.layout.placed_items()[k].item().idx() == item.idx())
                else {
                    break;
                };
                sep.layout.remove_item(key);
                for (k, _, _) in &members {
                    sep.layout.remove_item(*k);
                }
                for p in JLayout::from_snapshot(&snapshot).placed_items().values() {
                    sep.layout.place_item(p.item(), shift(p.d_transf(), offset));
                }
                sep.rebuild();
                moved += 1;
                self.stats.separated_insertions += 1;
                break;
            }
        }
        Ok(moved)
    }

    /// Run one window from a validated per-sheet state until `until`.
    pub(super) fn window_search(
        &mut self,
        mut order: Vec<SPProblem>,
        until: f64,
        compress_share: f64,
        window: usize,
    ) -> Result<()> {
        let strip = Strip {
            model: self.model,
            clock: self.clock.clone(),
            containers: Default::default(),
            gap: (self
                .model
                .full_width
                .max(self.model.instance.base_strip.fixed_height))
                * 0.02,
        };
        if let Some(victim) = least_filled(&order) {
            let last = order.remove(victim);
            order.push(last);
        }
        let now = self.clock.now();
        let explore_until = now + (until - now).max(0.0) * (1.0 - compress_share);
        let mut pool: Vec<(LayoutSnapshot, f32)> = vec![];
        let mut relocating = 0.0;
        'windows: while !order.is_empty() && self.clock.now() < explore_until {
            let size = window.min(order.len());
            let frozen = order[..order.len() - size].to_vec();
            let window = order[order.len() - size..].to_vec();
            let empty = strip.layout(
                &window,
                Shape {
                    sheets: size,
                    last: self.model.full_width,
                },
            )?;
            let mut shape = Shape {
                sheets: size,
                last: strip.fit_last(
                    &empty,
                    Shape {
                        sheets: size,
                        last: self.model.full_width,
                    },
                ),
            };
            let mut sep = Separator::new(
                strip.layout(&window, shape)?,
                self.rng.next_u64(),
                EXPLORE,
                self.clock.clone(),
            );
            sep.pin(blocker_index(self.model));
            if shape.sheets > 1 {
                sep.region = Rect::try_new(0.0, 0.0, strip.width(shape), strip.height()).ok();
            }
            if std::env::var_os("NESTBOLT_DEBUG").is_some() {
                let counts: Vec<_> = order
                    .iter()
                    .map(|s| s.layout().placed_items().len())
                    .collect();
                eprintln!(
                    "debug window: frozen {} window {} shape {:?} counts {:?} loss {}",
                    frozen.len(),
                    size,
                    shape,
                    counts,
                    sep.tracker.total_loss()
                );
            }
            let mut best = (sep.layout.save(), shape);
            let mut pending = false;
            let mut checked = self.clock.now();
            let mut filled = false;
            let mut stalled = 0;
            pool.clear();
            while self.clock.now() < explore_until {
                let deadline = self.deadline(explore_until);
                let before = sep.tracker.total_loss();
                let (snapshot, tracker) = timed("separate", || sep.separate(&deadline));
                if std::env::var_os("NESTBOLT_TRACE").is_some() {
                    eprintln!(
                        "trace shape {:?} loss before {} after {}",
                        shape,
                        before,
                        tracker.total_loss()
                    );
                }
                if tracker.total_loss() == 0.0 {
                    stalled = 0;
                    if !filled {
                        // Cheap direct moves into free gaps and a bounded
                        // number of one-sheet relocations, once per window.
                        filled = true;
                        let t = self.clock.now();
                        let budget = t + (explore_until - t).max(0.0) * 0.1;
                        let gaps = std::env::var_os("NESTBOLT_NO_FILL").is_none();
                        if (gaps && timed("fill", || self.fill_gaps(&strip, &mut sep, shape)) > 0)
                            || timed("relocate", || {
                                self.relocate(&strip, &mut sep, shape, budget)
                            })? > 0
                        {
                            shape.last = strip.fit_last(&sep.layout, shape);
                            strip.apply(&mut sep, shape)?;
                        }
                    }
                    let snapshot = sep.layout.save();
                    best = (snapshot, shape);
                    pending = true;
                    pool.clear();
                    if shape.sheets > 1 && strip.in_last(&sep.layout, shape).is_empty() {
                        // The last sheet emptied: remove it and its wall.
                        shape = Shape {
                            sheets: shape.sheets - 1,
                            ..shape
                        };
                        shape.last = strip.fit_last(&sep.layout, shape);
                        strip.clear_blocker(&mut sep.layout);
                        sep.layout.swap_container(strip.container(shape)?);
                        strip.apply(&mut sep, shape)?;
                        best = (sep.layout.save(), shape);
                        self.stats.eliminated_sheets += 1;
                        self.accept_window(&strip, &frozen, &best.0, shape, "eliminate")?;
                        pending = false;
                        checked = self.clock.now();
                        filled = false;
                        if !frozen.is_empty() && shape.sheets < size {
                            // Pull the next fixed sheet into the window.
                            let layout = JLayout::from_snapshot(&best.0);
                            order = frozen.clone();
                            order.extend(strip.split(&layout, shape.sheets)?);
                            continue 'windows;
                        }
                        continue;
                    }
                    let by = 0.001 * strip.width(shape);
                    let next = timed("shrink", || self.shrink(&strip, &mut sep, shape, by))?;
                    if next == shape {
                        break;
                    }
                    shape = next;
                } else {
                    stalled += 1;
                    let elapsed = self.clock.now() - now;
                    if stalled >= 3 && best.1.sheets > 1 && relocating < elapsed * 0.15 {
                        // The last sheet cannot shrink: from the best feasible
                        // layout, try to move one of its parts elsewhere.
                        stalled = 0;
                        let started = self.clock.now();
                        sep.rollback(&best.0, None);
                        shape = best.1;
                        let budget = (started + 2.0).min(explore_until);
                        if timed("relocate", || {
                            self.relocate(&strip, &mut sep, shape, budget)
                        })? > 0
                        {
                            shape.last = strip.fit_last(&sep.layout, shape);
                            strip.apply(&mut sep, shape)?;
                            best = (sep.layout.save(), shape);
                            pending = true;
                        }
                        pool.clear();
                        relocating += self.clock.now() - started;
                        continue;
                    }
                    let loss = tracker.total_loss();
                    let at = pool.partition_point(|(_, l)| *l < loss);
                    pool.insert(at, (snapshot, loss));
                    let sample = Normal::new(0.0, 0.25_f32)
                        .expect("valid normal")
                        .sample(&mut self.rng)
                        .abs()
                        .min(0.999);
                    let chosen = (sample * pool.len() as f32) as usize;
                    let snapshot = pool[chosen].0.clone();
                    timed("rollback", || sep.rollback(&snapshot, None));
                    timed("disrupt", || disrupt(&mut sep));
                }
                if pending && self.clock.now() - checked > self.check_every {
                    self.accept_window(&strip, &frozen, &best.0, best.1, "explore")?;
                    pending = false;
                    checked = self.clock.now();
                }
            }
            if pending {
                self.accept_window(&strip, &frozen, &best.0, best.1, "explore")?;
            }
            // Compression: smaller, time-decaying shrinks from the best layout.
            sep.config = COMPRESS;
            let start = self.clock.now();
            let span = ((until - start) as f32).max(1e-3);
            let mut pending = false;
            while self.clock.now() < self.last_step(until) {
                let ratio =
                    0.0005 + (((self.clock.now() - start) as f32) / span) * (0.00001 - 0.0005);
                let shape = best.1;
                sep.rollback(&best.0, None);
                let by = ratio * strip.width(shape);
                if shape.last - by <= self.model.separation * 2.0 {
                    break;
                }
                let next = timed("shrink", || self.shrink(&strip, &mut sep, shape, by))?;
                let deadline = self.deadline(self.last_step(until));
                let (snapshot, tracker) = timed("separate-c", || sep.separate(&deadline));
                if tracker.total_loss() == 0.0 {
                    best = (snapshot, next);
                    pending = true;
                }
                if pending && self.clock.now() - checked > self.check_every {
                    self.accept_window(&strip, &frozen, &best.0, best.1, "compress")?;
                    pending = false;
                    checked = self.clock.now();
                }
            }
            if pending {
                self.accept_window(&strip, &frozen, &best.0, best.1, "compress")?;
            }
            self.stats.compressions += 1;
            break;
        }
        if std::env::var_os("NESTBOLT_DEBUG").is_some() {
            TIMERS.with(|t| eprintln!("debug timers {:?}", t.borrow()));
        }
        Ok(())
    }
}
