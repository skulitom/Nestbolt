//! Build a low-material candidate from repeated orthogonal parts, then let the
//! common-line search validate it on the original stock and cutting curves.
mod tiles;

use crate::clock::{Clock, Work};
use nestbolt_validator::{
    RigidTransform,
    job::{Job, Layout, Mode, Placement},
};
use std::{collections::BTreeMap, f64::consts::FRAC_PI_2, ops::Range};
use tiles::Tile;

type Point = [i64; 2];
const GRID: f64 = 1_000_000.0; // nanometres in one millimetre
const PAD: i64 = 6;
const INF: i64 = i64::MAX / 4;
const NONE: usize = usize::MAX;

fn quantize(mm: f64) -> Option<i64> {
    let n = (mm * GRID).round();
    (n.is_finite() && n.abs() < 1e14).then_some(n as i64)
}

struct Budget<'a> {
    clock: &'a Clock,
    until: f64,
}
impl Budget<'_> {
    fn charge(&self, ops: usize) -> Option<()> {
        self.clock.charge(Work::RectOperation, ops as f64);
        (self.clock.now() < self.until).then_some(())
    }
}

#[derive(Clone, Copy)]
struct Pose {
    part: usize,
    turn: u8,
    position: Point,
}

/// A mixed-radix index represents the number required from each part family.
/// Adding indices adds the inventories provided no digit exceeds its limit.
struct Inventory {
    limits: Vec<usize>,
    strides: Vec<usize>,
    states: usize,
}
impl Inventory {
    fn new(limits: Vec<usize>) -> Option<Self> {
        let mut states = 1usize;
        let mut strides = vec![];
        for &n in &limits {
            strides.push(states);
            states = states.checked_mul(n.checked_add(1)?)?;
            // Bound memory on the native and browser search paths.
            if states > 32_768 {
                return None;
            }
        }
        Some(Self {
            limits,
            strides,
            states,
        })
    }

    fn digit(&self, index: usize, part: usize) -> usize {
        (index / self.strides[part]) % (self.limits[part] + 1)
    }

    fn counts(&self, index: usize) -> Vec<usize> {
        (0..self.limits.len())
            .map(|p| self.digit(index, p))
            .collect()
    }

    fn can_add(&self, index: usize, part: usize) -> bool {
        self.digit(index, part) < self.limits[part]
    }

    /// Visit contiguous runs of states that can contain `required`, in index
    /// order. Forward iteration also permits repeating the same tile or row.
    fn ranges(&self, required: usize, mut each: impl FnMut(Range<usize>)) {
        fn visit(
            inv: &Inventory,
            lo: &[usize],
            axis: usize,
            start: usize,
            each: &mut impl FnMut(Range<usize>),
        ) {
            if axis == 0 {
                each(start + lo[0]..start + inv.limits[0] + 1);
                return;
            }
            for n in lo[axis]..=inv.limits[axis] {
                visit(inv, lo, axis - 1, start + n * inv.strides[axis], each);
            }
        }
        visit(
            self,
            &self.counts(required),
            self.limits.len() - 1,
            0,
            &mut each,
        );
    }
}

struct Row {
    height: i64,
    tiles: Vec<usize>,
}

/// Once an inventory fits across the stock, keep the tile choices at that
/// height. Later, taller tiles may make it narrower but cannot improve height.
fn rows(
    inv: &Inventory,
    tiles: &[Tile],
    gap: i64,
    width: i64,
    budget: &Budget,
) -> Option<(Vec<Row>, Vec<usize>)> {
    let mut order: Vec<_> = (0..tiles.len()).collect();
    order.sort_by_key(|&i| (tiles[i].size[1], tiles[i].inventory, tiles[i].size[0]));
    let mut widths = vec![INF; inv.states];
    let mut previous = vec![NONE; inv.states];
    let mut choice = vec![NONE; inv.states];
    let mut rows = vec![];
    let mut stored_members = 0usize;
    widths[0] = 0;
    for group in order.chunk_by(|&a, &b| tiles[a].size[1] == tiles[b].size[1]) {
        let mut first_fit = Vec::new();
        for &i in group {
            let tile = &tiles[i];
            budget.charge(inv.states)?;
            inv.ranges(tile.inventory, |range| {
                for s in range {
                    let cost = widths[s - tile.inventory] + tile.size[0] + gap;
                    if cost < widths[s] && cost <= width + gap {
                        if widths[s] == INF {
                            first_fit.push(s);
                        }
                        widths[s] = cost;
                        previous[s] = i;
                    }
                }
            });
        }
        for state in first_fit {
            let mut s = state;
            let mut members = Vec::new();
            while s > 0 {
                let i = previous[s];
                members.push(i);
                s -= tiles[i].inventory;
            }
            stored_members += members.len();
            if stored_members > 1_000_000 {
                return None;
            }
            budget.charge(members.len())?;
            members.reverse();
            choice[state] = rows.len();
            rows.push(Row {
                height: tiles[group[0]].size[1],
                tiles: members,
            });
        }
    }
    // A taller row with fewer parts is unnecessary if a shorter row can
    // supply them. Extra copies are omitted when reconstructing the layout.
    for (axis, &stride) in inv.strides.iter().enumerate() {
        budget.charge(inv.states)?;
        for s in (1..inv.states).rev() {
            if !inv.can_add(s, axis) {
                continue;
            }
            let richer = choice[s + stride];
            if richer != NONE && (choice[s] == NONE || rows[richer].height < rows[choice[s]].height)
            {
                choice[s] = richer;
            }
        }
    }
    Some((rows, choice))
}

/// Minimize the sum of row heights for each possible single-sheet inventory.
fn sheets(
    inv: &Inventory,
    rows: &[Row],
    row_for: &[usize],
    height: i64,
    gap: i64,
    budget: &Budget,
) -> Option<(Vec<i64>, Vec<usize>)> {
    let mut heights = vec![INF; inv.states];
    let mut previous = vec![0; inv.states];
    heights[0] = 0;
    for (quantity, &r) in row_for.iter().enumerate().skip(1) {
        if r == NONE {
            continue;
        }
        let work: usize = inv
            .counts(quantity)
            .iter()
            .zip(&inv.limits)
            .map(|(n, limit)| limit - n + 1)
            .product();
        budget.charge(work)?;
        let rise = rows[r].height + gap;
        inv.ranges(quantity, |range| {
            for s in range {
                let h = heights[s - quantity] + rise;
                if h < heights[s] && h <= height + gap {
                    heights[s] = h;
                    previous[s] = quantity;
                }
            }
        });
    }
    Some((heights, previous))
}

/// Rebuild the sheet with the trailing offcut and at most one earlier sheet
/// of the same stock. Every other placement and physical copy ID is retained.
pub(super) fn pack(
    job: &Job,
    layout: &Layout,
    last_id: &str,
    clock: &Clock,
    until: f64,
) -> Option<Layout> {
    if job.mode != Mode::All || clock.now() >= until {
        return None;
    }
    let last = layout.sheets.iter().find(|s| s.id == last_id)?;
    let mate = layout
        .sheets
        .iter()
        .find(|s| s.id != last.id && s.stock_id == last.stock_id);
    let stock = job.stocks.iter().find(|s| s.id == last.stock_id)?;
    if !stock.outline.is_empty() || !stock.defects.is_empty() {
        return None;
    }
    let selected = |id: &str| id == last.id || mate.is_some_and(|s| s.id == id);
    let mut by_part = BTreeMap::new();
    for p in &layout.placements {
        if selected(&p.sheet_id) {
            by_part
                .entry(p.part_id.as_str())
                .or_insert_with(Vec::new)
                .push(p.copy_index);
        }
    }
    let parts: Vec<_> = job
        .parts
        .iter()
        .filter(|p| by_part.contains_key(p.id.as_str()))
        .collect();
    if parts.is_empty() {
        return None;
    }
    let mut copies: Vec<_> = parts
        .iter()
        .map(|p| by_part.remove(p.id.as_str()).unwrap())
        .collect();
    let inv = Inventory::new(copies.iter().map(Vec::len).collect())?;
    let scale = job.units.to_mm();
    let grid = GRID * scale;
    let gap = quantize(job.clearance * scale)? + PAD;
    let left = quantize((stock.margins.left + job.edge_clearance) * scale)? + PAD;
    let bottom = quantize((stock.margins.bottom + job.edge_clearance) * scale)? + PAD;
    let width =
        quantize((stock.width - stock.margins.right - job.edge_clearance) * scale)? - PAD - left;
    let height =
        quantize((stock.height - stock.margins.top - job.edge_clearance) * scale)? - PAD - bottom;
    if width <= 0 || height <= 0 {
        return None;
    }
    let budget = Budget { clock, until };
    let tiles = tiles::catalogue(&parts, &inv, scale, gap, [width, height], &budget)?;
    let (rows, row_for) = rows(&inv, &tiles, gap, width, &budget)?;
    let (heights, steps) = sheets(&inv, &rows, &row_for, height, gap, &budget)?;
    let total = inv.states - 1;
    let mut allocations = vec![];
    let mut trial = layout.clone();
    trial.placements.retain(|p| !selected(&p.sheet_id));
    if heights[total] != INF {
        if let Some(m) = mate {
            trial.sheets.retain(|s| s.id != m.id);
        }
        allocations.push((last, total));
    } else {
        let m = mate?;
        let first = (1..total)
            .filter(|&s| heights[s] != INF && heights[total - s] != INF)
            .min_by_key(|&s| (heights[total - s], heights[s]))?;
        allocations.extend([(m, first), (last, total - first)]);
    }
    for (sheet, mut state) in allocations {
        let mut y = bottom;
        while state > 0 {
            let contribution = steps[state];
            if contribution == 0 {
                return None;
            }
            let mut needs = inv.counts(contribution);
            let row = &rows[row_for[contribution]];
            let mut x = left;
            for &i in &row.tiles {
                for p in &tiles[i].poses {
                    if needs[p.part] == 0 {
                        continue;
                    }
                    trial.placements.push(Placement {
                        part_id: parts[p.part].id.clone(),
                        copy_index: copies[p.part].pop()?,
                        sheet_id: sheet.id.clone(),
                        transform: RigidTransform {
                            translation: [
                                (x + p.position[0]) as f64 / grid,
                                (y + p.position[1]) as f64 / grid,
                            ],
                            rotation_radians: f64::from(p.turn) * FRAC_PI_2,
                            mirrored: false,
                        },
                    });
                    needs[p.part] -= 1;
                }
                x += tiles[i].size[0] + gap;
            }
            if needs.iter().any(|&n| n != 0) {
                return None;
            }
            state -= contribution;
            y += row.height + gap;
        }
    }
    copies.iter().all(Vec::is_empty).then_some(trial)
}
