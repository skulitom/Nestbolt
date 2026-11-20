//! Join up to four source polygons at horizontal or vertical kerf contacts.
use super::{Budget, Inventory, Point, Pose, quantize};
use nestbolt_validator::job::Part;
use std::collections::BTreeMap;

#[derive(Clone, Copy)]
struct Rect {
    left: i64,
    right: i64,
    bottom: i64,
    top: i64,
}

impl Rect {
    fn shifted(self, dx: i64, dy: i64) -> Self {
        Self {
            left: self.left + dx,
            right: self.right + dx,
            bottom: self.bottom + dy,
            top: self.top + dy,
        }
    }
}

#[derive(Clone)]
pub(super) struct Tile {
    pub inventory: usize,
    pub size: Point,
    pub poses: Vec<Pose>,
    boxes: Vec<Rect>,
}

/// Slice the filled outer polygon into disjoint vertical rectangles. Reserving
/// holes while building an optional tile gives a conservative candidate.
fn rectangles(part: &Part, turn: u8, scale: f64) -> Option<Vec<Rect>> {
    let mut boxes = Vec::new();
    for polygon in &part.geometry {
        if boxes.len() > 32 {
            return None;
        }
        let ring = &polygon.outer;
        // The slice loop is quadratic in the number of distinct edge positions.
        if ring.len() > 64 || ring.len() < 3 {
            return None;
        }
        let points: Vec<_> = ring
            .iter()
            .map(|&[x, y]| {
                let x = quantize(x * scale)?;
                let y = quantize(y * scale)?;
                Some(match turn {
                    0 => [x, y],
                    1 => [-y, x],
                    2 => [-x, -y],
                    _ => [y, -x],
                })
            })
            .collect::<Option<_>>()?;
        let mut xs: Vec<_> = points.iter().map(|p| p[0]).collect();
        xs.sort_unstable();
        xs.dedup();
        let mut edges = Vec::new();
        for (a, b) in points.iter().zip(points.iter().cycle().skip(1)) {
            if a[1] == b[1] {
                edges.push((a[0].min(b[0]), a[0].max(b[0]), a[1]));
            } else if a[0] != b[0] {
                return None;
            }
        }
        for x in xs.windows(2) {
            let mut ys: Vec<_> = edges
                .iter()
                .filter(|(l, r, _)| *l <= x[0] && x[1] <= *r)
                .map(|e| e.2)
                .collect();
            ys.sort_unstable();
            if ys.len() % 2 != 0 {
                return None;
            }
            for pair in ys.as_chunks::<2>().0 {
                if pair[0] < pair[1] {
                    boxes.push(Rect {
                        left: x[0],
                        right: x[1],
                        bottom: pair[0],
                        top: pair[1],
                    });
                }
            }
        }
    }
    (!boxes.is_empty() && boxes.len() <= 32).then_some(boxes)
}

fn single(part: &Part, index: usize, inventory: usize, turn: u8, scale: f64) -> Option<Tile> {
    let boxes = rectangles(part, turn, scale)?;
    let left = boxes.iter().map(|r| r.left).min()?;
    let bottom = boxes.iter().map(|r| r.bottom).min()?;
    let size = [
        boxes.iter().map(|r| r.right).max()? - left,
        boxes.iter().map(|r| r.top).max()? - bottom,
    ];
    Some(Tile {
        inventory,
        size,
        poses: vec![Pose {
            part: index,
            turn,
            position: [-left, -bottom],
        }],
        boxes: boxes
            .into_iter()
            .map(|r| r.shifted(-left, -bottom))
            .collect(),
    })
}

type Catalogue = BTreeMap<usize, Vec<Tile>>;

fn offer(catalogue: &mut Catalogue, count: usize, size: Point, make: impl FnOnce() -> Tile) {
    let options = catalogue.entry(count).or_default();
    if options
        .iter()
        .any(|t| t.size[0] <= size[0] && t.size[1] <= size[1])
    {
        return;
    }
    options.retain(|t| size[0] > t.size[0] || size[1] > t.size[1]);
    options.push(make());
}

fn join(
    a: &Tile,
    b: &Tile,
    gap: i64,
    stock: Point,
    catalogue: &mut Catalogue,
    budget: &Budget,
) -> Option<()> {
    let mut obstacles = Vec::new();
    let mut xs = vec![0, a.size[0] - b.size[0]];
    let mut ys = vec![0, a.size[1] - b.size[1]];
    for p in &a.boxes {
        for q in &b.boxes {
            // Open intervals of translations where the square clearance
            // envelopes intersect. Their boundaries are safe contact points.
            let r = Rect {
                left: p.left - q.right - gap,
                right: p.right - q.left + gap,
                bottom: p.bottom - q.top - gap,
                top: p.top - q.bottom + gap,
            };
            xs.extend([r.left, r.right]);
            ys.extend([r.bottom, r.top]);
            obstacles.push(r);
        }
    }
    xs.sort_unstable();
    xs.dedup();
    ys.sort_unstable();
    ys.dedup();
    let count = a.inventory + b.inventory;
    for x in xs {
        let width = a.size[0].max(x + b.size[0]) - x.min(0);
        if width > stock[0] {
            continue;
        }
        budget.charge(obstacles.len() + ys.len())?;
        let active: Vec<_> = obstacles
            .iter()
            .filter(|r| r.left < x && x < r.right)
            .collect();
        for &y in &ys {
            let height = a.size[1].max(y + b.size[1]) - y.min(0);
            if height > stock[1] || active.iter().any(|r| r.bottom < y && y < r.top) {
                continue;
            }
            let size = [width, height];
            offer(catalogue, count, size, || {
                let mut poses = Vec::with_capacity(a.poses.len() + b.poses.len());
                let mut boxes = Vec::with_capacity(a.boxes.len() + b.boxes.len());
                for (tile, dx, dy) in [(a, -x.min(0), -y.min(0)), (b, x.max(0), y.max(0))] {
                    poses.extend(tile.poses.iter().map(|p| Pose {
                        position: [p.position[0] + dx, p.position[1] + dy],
                        ..*p
                    }));
                    boxes.extend(tile.boxes.iter().map(|r| r.shifted(dx, dy)));
                }
                Tile {
                    inventory: count,
                    size,
                    poses,
                    boxes,
                }
            });
        }
    }
    Some(())
}

pub(super) fn catalogue(
    parts: &[&Part],
    inventory: &Inventory,
    scale: f64,
    gap: i64,
    stock: Point,
    budget: &Budget,
) -> Option<Vec<Tile>> {
    let mut singles = Vec::new();
    let mut all = Catalogue::new();
    for (i, part) in parts.iter().enumerate() {
        let first = singles.len();
        for turn in crate::rects::quarter_turns(&part.rotations) {
            let tile = single(part, i, inventory.strides[i], (turn / 90.0) as u8, scale)?;
            if tile.size[0] <= stock[0] && tile.size[1] <= stock[1] {
                offer(&mut all, tile.inventory, tile.size, || tile.clone());
                singles.push(tile);
            }
        }
        if singles.len() == first {
            return None;
        }
    }
    // A group of rectangles can fill a strip that no single rectangle spans.
    // Use the same row inventory and source-validation rules for these groups.
    for (i, a) in singles.iter().enumerate() {
        for b in &singles[i..] {
            if inventory.can_add(a.inventory, b.poses[0].part) {
                join(a, b, gap, stock, &mut all, budget)?;
            }
        }
    }
    for n in 2..4 {
        let parents: Vec<_> = all
            .values()
            .flatten()
            .filter(|t| t.poses.len() == n)
            .cloned()
            .collect();
        for a in &parents {
            for b in &singles {
                if inventory.can_add(a.inventory, b.poses[0].part) {
                    join(a, b, gap, stock, &mut all, budget)?;
                }
            }
        }
    }
    Some(all.into_values().flatten().collect())
}
