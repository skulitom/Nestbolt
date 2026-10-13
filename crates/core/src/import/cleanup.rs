//! Remove redundant source geometry without flattening the curves.
use super::{Piece, Point, SILENT_JOIN_MM, Segment, dist, reverse};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, JsonSchema)]
pub struct Cleanup {
    pub duplicate_segments_removed: usize,
    pub zero_length_segments_removed: usize,
    /// Each redundant line merged into the union counts once.
    pub overlapping_segments_merged: usize,
}

struct Atom {
    from: Point,
    segment: Segment,
    owner: usize,
    live: bool,
}

fn empty(from: Point, s: &Segment) -> bool {
    match s {
        Segment::Line { to } => *to == from,
        Segment::Quad { control, to } => *to == from && *control == from,
        Segment::Cubic { controls, to } => *to == from && controls.iter().all(|p| *p == from),
        Segment::Arc { radii, sweep, .. } => *sweep == 0.0 || *radii == [0.0, 0.0],
    }
}

fn key(from: Point, s: &Segment) -> Vec<u64> {
    let mut values = vec![from[0], from[1]];
    let kind = match s {
        Segment::Line { to } => {
            values.extend(to);
            0
        }
        Segment::Quad { control, to } => {
            values.extend(control);
            values.extend(to);
            1
        }
        Segment::Cubic { controls, to } => {
            values.extend(controls.iter().flatten());
            values.extend(to);
            2
        }
        Segment::Arc {
            center,
            radii,
            rotation,
            start,
            sweep,
        } => {
            values.extend(center);
            values.extend(radii);
            values.extend([*rotation, *start, *sweep]);
            3
        }
    };
    let mut bits = vec![kind];
    bits.extend(
        values
            .into_iter()
            .map(|v| if v == 0.0 { 0 } else { v.to_bits() }),
    );
    bits
}

fn duplicate_key(from: Point, s: &Segment) -> Vec<u64> {
    let forward = key(from, s);
    let (start, backward) = reverse(from, std::slice::from_ref(s));
    forward.min(key(start, &backward[0]))
}

struct LineGroup {
    anchor: Point,
    unit: Point,
    lines: Vec<usize>,
}

fn cross(a: Point, b: Point) -> f64 {
    a[0] * b[1] - a[1] * b[0]
}
fn sub(a: Point, b: Point) -> Point {
    [a[0] - b[0], a[1] - b[1]]
}
fn dot(a: Point, b: Point) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}

/// Bins are a broad phase only. Verify both endpoints against the supporting
/// line to round-off precision before merging; this never uses the gap tolerance.
fn merge_lines(atoms: &mut [Atom], report: &mut Cleanup) {
    const ANGLE_BIN: f64 = 1e-8;
    const OFFSET_BIN: f64 = 1e-6;
    const ROUND_OFF_MM: f64 = 1e-9;
    let mut bins: HashMap<(i64, i64), Vec<usize>> = HashMap::new();
    let mut groups: Vec<LineGroup> = vec![];
    for (i, a) in atoms.iter().enumerate().filter(|(_, a)| a.live) {
        let Segment::Line { to } = a.segment else {
            continue;
        };
        let delta = sub(to, a.from);
        let length = delta[0].hypot(delta[1]);
        if !length.is_finite() || length == 0.0 {
            continue;
        }
        let sign = if delta[0] < 0.0 || (delta[0] == 0.0 && delta[1] < 0.0) {
            -1.0
        } else {
            1.0
        };
        let unit = [sign * delta[0] / length, sign * delta[1] / length];
        let angle = (unit[1].atan2(unit[0]) / ANGLE_BIN).round();
        let offset = (cross(unit, a.from) / OFFSET_BIN).round();
        if angle.abs() >= i64::MAX as f64 - 4.0 || offset.abs() >= i64::MAX as f64 - 4.0 {
            continue;
        }
        let slot = (angle as i64, offset as i64);
        let mut matching = None;
        'search: for da in -1..=1 {
            for dc in -1..=1 {
                if let Some(candidates) = bins.get(&(slot.0 + da, slot.1 + dc)) {
                    for &g in candidates {
                        let group = &groups[g];
                        if cross(group.unit, unit).abs() <= 1e-12
                            && cross(group.unit, sub(a.from, group.anchor)).abs() <= ROUND_OFF_MM
                            && cross(group.unit, sub(to, group.anchor)).abs() <= ROUND_OFF_MM
                        {
                            matching = Some(g);
                            break 'search;
                        }
                    }
                }
            }
        }
        if let Some(g) = matching {
            groups[g].lines.push(i);
        } else {
            bins.entry(slot).or_default().push(groups.len());
            groups.push(LineGroup {
                anchor: a.from,
                unit,
                lines: vec![i],
            });
        }
    }
    for group in groups.into_iter().filter(|g| g.lines.len() > 1) {
        let mut intervals = group
            .lines
            .into_iter()
            .map(|i| {
                let a = &atoms[i];
                let end = a.segment.end();
                let t0 = dot(sub(a.from, group.anchor), group.unit);
                let t1 = dot(sub(end, group.anchor), group.unit);
                if t0 <= t1 {
                    (t0, t1, a.from, end, i)
                } else {
                    (t1, t0, end, a.from, i)
                }
            })
            .collect::<Vec<_>>();
        intervals.sort_by(|a, b| a.0.total_cmp(&b.0).then(a.1.total_cmp(&b.1)));
        let mut current = intervals[0];
        for next in intervals.into_iter().skip(1) {
            if next.0 < current.1 - ROUND_OFF_MM {
                let keep = current.4.min(next.4);
                let discard = current.4.max(next.4);
                let same_direction =
                    dot(sub(atoms[keep].segment.end(), atoms[keep].from), group.unit) >= 0.0;
                if next.1 > current.1 {
                    current.1 = next.1;
                    current.3 = next.3;
                }
                atoms[keep].from = if same_direction { current.2 } else { current.3 };
                atoms[keep].segment = Segment::Line {
                    to: if same_direction { current.3 } else { current.2 },
                };
                atoms[discard].live = false;
                current.4 = keep;
                report.overlapping_segments_merged += 1;
            } else {
                current = next;
            }
        }
    }
}

pub(super) fn clean(pieces: Vec<Piece>, report: &mut Cleanup) -> Vec<Piece> {
    let mut atoms = vec![];
    let mut sources = vec![];
    let mut seen = HashSet::new();
    for p in pieces {
        let owner = sources.len();
        sources.push(p.source);
        let mut from = p.start;
        for segment in p.segments {
            let end = segment.end();
            if empty(from, &segment) {
                report.zero_length_segments_removed += 1;
            } else if !seen.insert(duplicate_key(from, &segment)) {
                report.duplicate_segments_removed += 1;
            } else {
                atoms.push(Atom {
                    from,
                    segment,
                    owner,
                    live: true,
                });
            }
            from = end;
        }
    }
    merge_lines(&mut atoms, report);
    let mut output: Vec<Piece> = vec![];
    let mut previous_owner = None;
    for a in atoms.into_iter().filter(|a| a.live) {
        if previous_owner == Some(a.owner)
            && let Some(p) = output.last_mut()
            && dist(p.end(), a.from) <= SILENT_JOIN_MM
        {
            p.segments.push(a.segment);
        } else {
            output.push(Piece {
                start: a.from,
                segments: vec![a.segment],
                source: sources[a.owner].clone(),
            });
        }
        previous_owner = Some(a.owner);
    }
    output
}
