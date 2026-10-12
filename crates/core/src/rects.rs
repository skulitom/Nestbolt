//! Bounding-rectangle packing for near-rectangular parts, such as finger-jointed
//! box panels, whose good layouts (rows and bands of upright panels) point-wise
//! constructors and local separation reach slowly. MaxRects places copies in a
//! deterministic first layout, then random orders, rules and orientations try
//! one sheet fewer, then ever shorter last sheets, until a deterministic budget
//! of operations is spent. Rectangles kept the clearance apart guarantee that
//! the outlines are, so every layout is valid by construction; callers still
//! check it independently before use.
use nestbolt_validator::{
    RigidTransform,
    job::{Job, Layout, Mode, Placement, Rotations, Sheet},
};
use rand::{RngExt, SeedableRng, rngs::Xoshiro256PlusPlus, seq::SliceRandom};

/// Quarter turns allowed by a part's rotation rule.
fn quarter_turns(rotations: &Rotations) -> Vec<f64> {
    let on_grid = |a: f64, step: f64| ((a / step).round() * step - a).abs() < 1e-9;
    [0.0, 90.0, 180.0, 270.0]
        .into_iter()
        .filter(|&a| match rotations {
            Rotations::Free => true,
            Rotations::Step { degrees } => on_grid(a, *degrees),
            Rotations::List { degrees } => degrees
                .iter()
                .any(|d| ((d - a).rem_euclid(360.0)).min((a - d).rem_euclid(360.0)) < 1e-9),
        })
        .collect()
}

/// Bounding box `[min_x, min_y, max_x, max_y]` of a part's outers rotated by `degrees`.
fn bounds(outers: &[&Vec<[f64; 2]>], degrees: f64) -> [f64; 4] {
    let (s, c) = degrees.to_radians().sin_cos();
    let mut b = [
        f64::INFINITY,
        f64::INFINITY,
        f64::NEG_INFINITY,
        f64::NEG_INFINITY,
    ];
    for &[x, y] in outers.iter().flat_map(|o| o.iter()) {
        let (u, v) = (x * c - y * s, x * s + y * c);
        b = [b[0].min(u), b[1].min(v), b[2].max(u), b[3].max(v)];
    }
    b
}

/// One part copy and its allowed orientations with distinct boxes, flattest first.
struct Item<'a> {
    part: &'a str,
    copy: u32,
    orientations: Vec<(f64, [f64; 4])>,
}

impl Item<'_> {
    fn size(&self, o: usize) -> (f64, f64) {
        let b = self.orientations[o].1;
        (b[2] - b[0], b[3] - b[1])
    }
}

/// A rectangle in a sheet's usable frame. Placed rectangles and the sheet are
/// both inflated by the gap on their top and right, so touching means apart.
#[derive(Clone, Copy, PartialEq)]
struct Rect {
    x: f64,
    y: f64,
    w: f64,
    h: f64,
}

impl Rect {
    fn contains(&self, o: &Rect) -> bool {
        self.x <= o.x
            && self.y <= o.y
            && self.x + self.w >= o.x + o.w
            && self.y + self.h >= o.y + o.h
    }

    fn overlaps(&self, o: &Rect) -> bool {
        o.x < self.x + self.w && self.x < o.x + o.w && o.y < self.y + self.h && self.y < o.y + o.h
    }
}

#[derive(Clone, Copy)]
enum Rule {
    BottomLeft,
    ShortSide,
    Area,
}

/// Per item: (sheet, orientation, x, y) in the usable frame.
type Packing = Vec<(usize, usize, f64, f64)>;

struct Packer<'a> {
    items: Vec<Item<'a>>,
    gap: f64,
    width: f64,
    operations: u64,
    budget: u64,
}

impl Packer<'_> {
    /// MaxRects, each item on the first sheet with room. `forced` restricts an
    /// item to one orientation when that fits anywhere. `None` when an item is
    /// left over or the budget runs out.
    fn pack(
        &mut self,
        order: &[usize],
        forced: &[Option<usize>],
        heights: &[f64],
        rule: Rule,
    ) -> Option<Packing> {
        let mut free: Vec<Vec<Rect>> = heights
            .iter()
            .map(|&h| {
                vec![Rect {
                    x: 0.0,
                    y: 0.0,
                    w: self.width + self.gap,
                    h: h + self.gap,
                }]
            })
            .collect();
        let mut placed = vec![(0, 0, 0.0, 0.0); self.items.len()];
        for &index in order {
            let item = &self.items[index];
            let all: Vec<usize> = (0..item.orientations.len()).collect();
            let mut spot = None;
            for choices in [forced[index].map(|o| vec![o]), Some(all)]
                .into_iter()
                .flatten()
            {
                for (sheet, rects) in free.iter().enumerate() {
                    let mut best: Option<((f64, f64), usize, Rect)> = None;
                    for &o in &choices {
                        let (w, h) = item.size(o);
                        let (w, h) = (w + self.gap, h + self.gap);
                        for r in rects {
                            if r.w + 1e-9 < w || r.h + 1e-9 < h {
                                continue;
                            }
                            let score = match rule {
                                Rule::BottomLeft => (r.y + h, r.x),
                                Rule::ShortSide => ((r.w - w).min(r.h - h), (r.w - w).max(r.h - h)),
                                Rule::Area => (r.w * r.h - w * h, (r.w - w).min(r.h - h)),
                            };
                            if best.is_none_or(|(s, ..)| score < s) {
                                best = Some((
                                    score,
                                    o,
                                    Rect {
                                        x: r.x,
                                        y: r.y,
                                        w,
                                        h,
                                    },
                                ));
                            }
                        }
                    }
                    self.operations += (choices.len() * rects.len()) as u64;
                    if let Some((_, o, rect)) = best {
                        spot = Some((sheet, o, rect));
                        break;
                    }
                }
                if spot.is_some() {
                    break;
                }
            }
            let (sheet, o, used) = spot?;
            placed[index] = (sheet, o, used.x, used.y);
            let rects = &mut free[sheet];
            let mut split = Vec::with_capacity(rects.len() + 4);
            for r in rects.iter() {
                if !used.overlaps(r) {
                    split.push(*r);
                    continue;
                }
                if used.x > r.x {
                    split.push(Rect {
                        w: used.x - r.x,
                        ..*r
                    });
                }
                if used.x + used.w < r.x + r.w {
                    split.push(Rect {
                        x: used.x + used.w,
                        w: r.x + r.w - used.x - used.w,
                        ..*r
                    });
                }
                if used.y > r.y {
                    split.push(Rect {
                        h: used.y - r.y,
                        ..*r
                    });
                }
                if used.y + used.h < r.y + r.h {
                    split.push(Rect {
                        y: used.y + used.h,
                        h: r.y + r.h - used.y - used.h,
                        ..*r
                    });
                }
            }
            self.operations += (split.len() * split.len()) as u64;
            if self.operations > self.budget {
                return None;
            }
            *rects = split
                .iter()
                .enumerate()
                .filter(|&(i, r)| {
                    !split
                        .iter()
                        .enumerate()
                        .any(|(j, o)| j != i && o.contains(r) && (o != r || j < i))
                })
                .map(|(_, r)| *r)
                .collect();
        }
        Some(placed)
    }

    /// Sheets used and the last sheet's content height; lower is better.
    fn score(&self, packing: &Packing) -> (usize, f64) {
        let sheets = packing.iter().map(|p| p.0).max().map_or(0, |s| s + 1);
        let top = packing
            .iter()
            .zip(&self.items)
            .filter(|(p, _)| p.0 + 1 == sheets)
            .map(|(p, item)| p.3 + item.size(p.1).1)
            .fold(0.0, f64::max);
        (sheets, top)
    }
}

fn better(a: (usize, f64), b: (usize, f64)) -> bool {
    a.0 < b.0 || (a.0 == b.0 && a.1 < b.1 - 1e-9)
}

/// The best rectangle layout found within `budget` operations, and the
/// operations used. Single-stock, all-parts jobs on full rectangles only; `None`
/// when the job is outside this model, a part fits no sheet, stock runs out, or
/// the budget cannot finish even the first layout.
pub fn pack(job: &Job, seed: u64, budget: u64) -> Option<(Layout, u64)> {
    if job.mode != Mode::All || job.stocks.len() != 1 {
        return None;
    }
    let stock = &job.stocks[0];
    if !stock.outline.is_empty() || !stock.defects.is_empty() {
        return None;
    }
    let m = stock.margins;
    let scale = stock.width.max(stock.height);
    let gap = job.clearance + 1e-7 * scale;
    let edge = job.edge_clearance + 1e-7 * scale;
    let (x0, y0) = (m.left + edge, m.bottom + edge);
    let (width, height) = (
        stock.width - m.right - edge - x0,
        stock.height - m.top - edge - y0,
    );
    if width <= 0.0 || height <= 0.0 {
        return None;
    }
    let mut items = vec![];
    for part in &job.parts {
        let outers: Vec<_> = part.geometry.iter().map(|g| &g.outer).collect();
        let mut orientations: Vec<(f64, [f64; 4])> = vec![];
        for a in quarter_turns(&part.rotations) {
            let b = bounds(&outers, a);
            let (w, h) = (b[2] - b[0], b[3] - b[1]);
            let same = |o: &(f64, [f64; 4])| {
                ((o.1[2] - o.1[0]) - w).abs() < 1e-9 && ((o.1[3] - o.1[1]) - h).abs() < 1e-9
            };
            if w <= width && h <= height && !orientations.iter().any(same) {
                orientations.push((a, b));
            }
        }
        if orientations.is_empty() {
            return None;
        }
        orientations.sort_by(|a, b| (a.1[3] - a.1[1]).total_cmp(&(b.1[3] - b.1[1])));
        for copy in 0..part.quantity {
            items.push(Item {
                part: &part.id,
                copy,
                orientations: orientations.clone(),
            });
        }
    }
    let n = items.len();
    let area: f64 = items.iter().map(|i| i.size(0).0 * i.size(0).1).sum();
    let mut packer = Packer {
        items,
        gap,
        width,
        operations: 0,
        budget,
    };
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by(|&a, &b| {
        let (wa, ha) = packer.items[a].size(0);
        let (wb, hb) = packer.items[b].size(0);
        (wb * hb).total_cmp(&(wa * ha)).then(a.cmp(&b))
    });
    let limit = stock.count.map_or(n, |c| (c as usize).min(n));
    let unforced = vec![None; n];
    let first = packer.pack(&order, &unforced, &vec![height; limit], Rule::BottomLeft)?;
    let mut best = (packer.score(&first), first);
    let lower = ((area / (width * height)).ceil() as usize).max(1);
    let mut reducing = best.0.0 > lower;
    let mut step = 0.05_f64;
    let mut misses = 0;
    let patience = 1000 + 100 * n.min(50);
    let mut rng = Xoshiro256PlusPlus::seed_from_u64(seed);
    let mut forced = unforced.clone();
    while packer.operations < packer.budget && step >= 0.002 {
        let (sheets, top) = best.0;
        let heights = if reducing {
            vec![height; sheets - 1]
        } else {
            let mut h = vec![height; sheets];
            h[sheets - 1] = top * (1.0 - step);
            h
        };
        order.shuffle(&mut rng);
        for (f, item) in forced.iter_mut().zip(&packer.items) {
            *f = (item.orientations.len() > 1 && rng.random_bool(0.2))
                .then(|| rng.random_range(0..item.orientations.len()));
        }
        // Short-side fit packs tight targets best; the others add variety.
        let rule = [
            Rule::ShortSide,
            Rule::ShortSide,
            Rule::ShortSide,
            Rule::Area,
            Rule::BottomLeft,
        ][rng.random_range(0..5)];
        match packer.pack(&order, &forced, &heights, rule) {
            Some(found) if better(packer.score(&found), best.0) => {
                best = (packer.score(&found), found);
                reducing &= best.0.0 > lower;
                misses = 0;
            }
            _ => {
                misses += 1;
                if misses >= patience {
                    misses = 0;
                    if reducing {
                        reducing = false;
                    } else {
                        step /= 2.0;
                    }
                }
            }
        }
    }
    let layout = Layout {
        version: 1,
        units: job.units,
        sheets: (0..best.0.0)
            .map(|i| Sheet {
                id: format!("sheet-{i}"),
                stock_id: stock.id.clone(),
            })
            .collect(),
        placements: packer
            .items
            .iter()
            .zip(&best.1)
            .map(|(item, &(sheet, o, x, y))| {
                let (degrees, b) = item.orientations[o];
                Placement {
                    part_id: item.part.to_owned(),
                    copy_index: item.copy,
                    sheet_id: format!("sheet-{sheet}"),
                    transform: RigidTransform {
                        translation: [x0 + x - b[0], y0 + y - b[1]],
                        rotation_radians: degrees.to_radians(),
                        mirrored: false,
                    },
                }
            })
            .collect(),
    };
    Some((layout, packer.operations))
}

#[cfg(test)]
mod tests {
    use super::*;
    use nestbolt_validator::{
        Polygon, Units,
        job::{Margins, Part, Stock, validate},
    };

    fn rectangle(id: &str, w: f64, h: f64, quantity: u32, rotations: Rotations) -> Part {
        Part {
            id: id.into(),
            quantity,
            geometry: vec![Polygon {
                outer: vec![[0.0, 0.0], [w, 0.0], [w, h], [0.0, h]],
                holes: vec![],
            }],
            rotations,
            allow_mirror: false,
            priority: 1.0,
        }
    }

    fn job(parts: Vec<Part>, count: Option<u32>) -> Job {
        Job {
            version: 1,
            name: "rectangles".into(),
            units: Units::Mm,
            clearance: 0.8,
            edge_clearance: 0.8,
            mode: Mode::All,
            parts,
            stocks: vec![Stock {
                id: "sheet".into(),
                width: 300.0,
                height: 200.0,
                count,
                margins: Margins {
                    left: 5.0,
                    right: 5.0,
                    bottom: 5.0,
                    top: 5.0,
                },
                outline: vec![],
                defects: vec![],
            }],
        }
    }

    fn quarters() -> Rotations {
        Rotations::List {
            degrees: vec![0.0, 90.0, 180.0, 270.0],
        }
    }

    /// Box panels whose best layout stands some panels upright: shelves and a
    /// tall-sheet MaxRects stop at 0.72; a shorter target finds 0.667.
    #[test]
    fn shorter_targets_find_upright_bands() {
        let job = job(
            vec![
                rectangle("a", 60.0, 30.0, 8, quarters()),
                rectangle("b", 60.0, 40.0, 4, quarters()),
                rectangle("c", 40.0, 30.0, 8, quarters()),
            ],
            None,
        );
        let (layout, used) = pack(&job, 0, 50_000_000).unwrap();
        let report = validate(&job, &layout).unwrap();
        assert!(report.valid, "{:?}", report.violations);
        let metrics = report.metrics.unwrap();
        assert_eq!(metrics.sheets_used, 1);
        assert!(
            metrics.normalized_material < 0.70,
            "{}",
            metrics.normalized_material
        );
        // Deterministic for a seed and budget.
        assert_eq!(
            serde_json::to_value(pack(&job, 0, 50_000_000).unwrap().0).unwrap(),
            serde_json::to_value(&layout).unwrap()
        );
        assert!(used <= 50_000_000 + 1_000_000);
    }

    #[test]
    fn rules_limits_and_budgets_are_respected() {
        let fixed = Rotations::List { degrees: vec![0.0] };
        let many = job(
            vec![rectangle("p", 140.0, 90.0, 20, fixed.clone())],
            Some(2),
        );
        assert!(pack(&many, 0, 1_000_000).is_none());
        let few = job(vec![rectangle("p", 140.0, 90.0, 4, fixed)], Some(1));
        let (layout, _) = pack(&few, 0, 1_000_000).unwrap();
        assert!(
            layout
                .placements
                .iter()
                .all(|p| p.transform.rotation_radians == 0.0)
        );
        assert!(validate(&few, &layout).unwrap().valid);
        let wide = job(vec![rectangle("p", 400.0, 20.0, 1, Rotations::Free)], None);
        assert!(pack(&wide, 0, 1_000_000).is_none());
        let several = job(vec![rectangle("p", 100.0, 90.0, 9, quarters())], None);
        let (layout, _) = pack(&several, 3, 2_000_000).unwrap();
        let report = validate(&several, &layout).unwrap();
        assert!(report.valid, "{:?}", report.violations);
        // Four fit a sheet in any orientation mix, so nine need three.
        assert_eq!(report.metrics.unwrap().sheets_used, 3);
        assert!(pack(&several, 3, 10).is_none());
    }
}
