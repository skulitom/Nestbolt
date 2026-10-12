//! The last few sheets laid end to end as one fixed-height strip, separated by
//! thin walls (container holes). Shrinking the last sheet is then Sparrow's
//! exploration (Algorithm 12) and compression (Algorithm 13) over the whole
//! window: parts move between sheets through ordinary sampling, and a last
//! sheet that empties is removed. Earlier sheets stay fixed outside the window.
use super::*;
use crate::separate::{COMPRESS, EXPLORE, Separator, Until};
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

/// At most this many trailing sheets take part in one virtual strip.
const WINDOW: usize = 6;

#[derive(Clone, Copy, Debug, PartialEq)]
struct Shape {
    sheets: usize,
    /// Length of the last sheet's region along the strip.
    last: f32,
}

struct Strip<'m, 'a> {
    model: &'m Model<'a>,
    gap: f32,
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

    fn container(&self, s: Shape) -> Result<Container> {
        let height = self.height();
        let zones = (0..s.sheets - 1)
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
        // Keep quadtree cells comparable to one sheet in long strips.
        let aspect = (self.width(s) / height).max(1.0);
        let mut cde = DEFAULT_SPARROW_CONFIG.cde_config;
        cde.quadtree_depth += ((aspect / 2.0).max(1.0).log2().ceil() as u8).min(3);
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

    fn layout(&self, window: &[SPProblem], s: Shape) -> Result<JLayout> {
        let mut layout = JLayout::new(self.container(s)?);
        for (i, sheet) in window.iter().enumerate() {
            for p in sheet.layout().placed_items().values() {
                layout.place_item(p.item(), shift(p.d_transf(), self.start(i)));
            }
        }
        Ok(layout)
    }

    /// Split a window layout back into fixed-width per-sheet problems.
    fn split(&self, layout: &JLayout, sheets: usize) -> Result<Vec<SPProblem>> {
        let mut out = (0..sheets)
            .map(|_| self.model.empty_sheet())
            .collect::<Result<Vec<_>>>()?;
        for p in layout.placed_items().values() {
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
            .filter(|(_, p)| self.sheet_of(p.shape()) >= s.sheets - 1)
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
    let large: Vec<_> = layout
        .placed_items()
        .iter()
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
                .keys()
                .filter(|&k| k != a)
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
        let layout = JLayout::from_snapshot(snapshot);
        let mut sheets = frozen.to_vec();
        sheets.extend(strip.split(&layout, s.sheets)?);
        self.accept(&sheets, stage)
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
                .filter(|(_, p)| p.shape().centroid().0 > split)
                .map(|(k, p)| (k, p.d_transf()))
                .collect();
            for (key, dt) in moving {
                let item = sep.layout.remove_item(key).item().clone();
                sep.layout.place_item(&item, shift(dt, -by));
            }
        }
        sep.swap_container(strip.container(next)?);
        Ok(next)
    }

    /// Run one window from a validated per-sheet state until `until`.
    pub(super) fn window_search(
        &mut self,
        mut order: Vec<SPProblem>,
        until: Instant,
        compress_share: f64,
    ) -> Result<()> {
        let strip = Strip {
            model: self.model,
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
        let now = Instant::now();
        let explore_until = now
            + until
                .saturating_duration_since(now)
                .mul_f64(1.0 - compress_share);
        let mut pool: Vec<(LayoutSnapshot, f32)> = vec![];
        'windows: while !order.is_empty() && Instant::now() < explore_until {
            let size = WINDOW.min(order.len());
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
            let mut sep =
                Separator::new(strip.layout(&window, shape)?, self.rng.next_u64(), EXPLORE);
            let mut best = (sep.layout.save(), shape);
            let mut pending = false;
            let mut checked = Instant::now();
            pool.clear();
            while Instant::now() < explore_until {
                let (snapshot, tracker) = sep.separate(&Until(explore_until));
                if tracker.total_loss() == 0.0 {
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
                        sep.swap_container(strip.container(shape)?);
                        best = (sep.layout.save(), shape);
                        self.stats.eliminated_sheets += 1;
                        self.accept_window(&strip, &frozen, &best.0, shape, "eliminate")?;
                        pending = false;
                        checked = Instant::now();
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
                    let next = self.shrink(&strip, &mut sep, shape, by)?;
                    if next == shape {
                        break;
                    }
                    shape = next;
                } else {
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
                    sep.rollback(&snapshot, None);
                    disrupt(&mut sep);
                }
                if pending && checked.elapsed() > Duration::from_secs(1) {
                    self.accept_window(&strip, &frozen, &best.0, best.1, "explore")?;
                    pending = false;
                    checked = Instant::now();
                }
            }
            if pending {
                self.accept_window(&strip, &frozen, &best.0, best.1, "explore")?;
            }
            // Compression: smaller, time-decaying shrinks from the best layout.
            sep.config = COMPRESS;
            let start = Instant::now();
            let span = until
                .saturating_duration_since(start)
                .as_secs_f32()
                .max(1e-3);
            let mut pending = false;
            while Instant::now() < until {
                let ratio = 0.0005 + (start.elapsed().as_secs_f32() / span) * (0.00001 - 0.0005);
                let shape = best.1;
                sep.rollback(&best.0, None);
                let by = ratio * strip.width(shape);
                if shape.last - by <= self.model.separation * 2.0 {
                    break;
                }
                let next = self.shrink(&strip, &mut sep, shape, by)?;
                let (snapshot, tracker) = sep.separate(&Until(until));
                if tracker.total_loss() == 0.0 {
                    best = (snapshot, next);
                    pending = true;
                }
                if pending && checked.elapsed() > Duration::from_secs(1) {
                    self.accept_window(&strip, &frozen, &best.0, best.1, "compress")?;
                    pending = false;
                    checked = Instant::now();
                }
            }
            if pending {
                self.accept_window(&strip, &frozen, &best.0, best.1, "compress")?;
            }
            self.stats.compressions += 1;
            break;
        }
        Ok(())
    }
}
