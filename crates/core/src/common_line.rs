//! Compensated common lines between straight outer edges of placed parts.
//!
//! Detection uses analytic line offsets. It does not offset with Clipper (the
//! independent tests do), change CUT contours, share holes or share sheet edges.
use std::collections::HashMap;

use anyhow::{Context, Result, ensure};
use nestbolt_validator::job::{Job, Layout, validate};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::curves::{Contour, Point, Segment, contains, signed_area};
use crate::export::{Outline, placed};

mod chains;
pub(crate) mod length;
pub(crate) mod search;

pub const COLLINEAR_MM: f64 = 0.01;
pub const MIN_SHARED_MM: f64 = 10.0;
const EPS: f64 = 1e-8;

#[derive(Clone, Copy, Debug, Serialize, Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct Options {
    pub kerf_mm: f64,
    /// Spend the last tenth of the search aligning shared cuts. Off by default.
    #[serde(default)]
    pub search_bonus: bool,
}

impl Options {
    pub fn validate(self) -> Result<()> {
        ensure!(
            self.kerf_mm.is_finite() && self.kerf_mm >= 0.05,
            "common-line cutting requires a finite kerf of at least 0.05 mm"
        );
        Ok(())
    }
}

/// Arc-length coverage on one original outer contour, for reporting and for
/// excluding future lead attachment points. Intervals may wrap around length.
#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct Coverage {
    pub part_copy: String,
    pub from_mm: f64,
    pub to_mm: f64,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct SharedEdge {
    pub from_mm: Point,
    pub to_mm: Point,
    pub owners: [Coverage; 2],
    /// Distance to the other edge's half-kerf offset, bounded by COLLINEAR_MM.
    pub maximum_offset_difference_mm: f64,
}

#[derive(Clone, Debug, Serialize, JsonSchema)]
pub struct Report {
    pub sheet_id: String,
    pub kerf_mm: f64,
    pub collinearity_tolerance_mm: f64,
    pub minimum_shared_length_mm: f64,
    pub shared_edges: Vec<SharedEdge>,
    pub paths: Vec<Contour>,
    pub shared_length_mm: f64,
    pub cut_length_without_common_mm: f64,
    pub cut_length_with_common_mm: f64,
    pub saved_length_mm: f64,
    pub saved_fraction: f64,
    pub contours_without_common: usize,
    /// Unshared source path pieces plus COMMON paths. Closed CUT reference
    /// contours remain in the export and are not an extra cutting pass.
    pub paths_with_common: usize,
}

#[derive(Clone)]
struct Edge {
    owner: usize,
    a: Point,
    b: Point,
    u: Point,
    normal: Point,
    length: f64,
    from: f64,
}

fn sub(a: Point, b: Point) -> Point {
    [a[0] - b[0], a[1] - b[1]]
}
fn add(a: Point, b: Point) -> Point {
    [a[0] + b[0], a[1] + b[1]]
}
fn mul(a: Point, s: f64) -> Point {
    [a[0] * s, a[1] * s]
}
fn dot(a: Point, b: Point) -> f64 {
    a[0] * b[0] + a[1] * b[1]
}
fn cross(a: Point, b: Point) -> f64 {
    a[0] * b[1] - a[1] * b[0]
}
fn distance(a: Point, b: Point) -> f64 {
    let p = sub(a, b);
    p[0].hypot(p[1])
}

fn edges(contour: &Contour, owner: usize, half_kerf: f64) -> Result<(Vec<Edge>, f64)> {
    let polygon = contour.flatten(0.0005)?;
    let area = signed_area(&polygon);
    ensure!(
        area.is_finite() && area.abs() > EPS,
        "common-line outline must enclose a nonzero area"
    );
    ensure!(
        distance(contour.start, contour.end()) < EPS,
        "common-line outlines must be closed"
    );
    let mut result: Vec<Edge> = vec![];
    let mut from = 0.0;
    let mut current = contour.start;
    for segment in &contour.segments {
        let len = length::segment(current, segment);
        ensure!(len.is_finite(), "non-finite common-line contour length");
        let end = segment.end();
        if matches!(segment, Segment::Line { .. }) && len > EPS {
            let u = mul(sub(end, current), 1.0 / len);
            let n = mul([u[1], -u[0]], area.signum());
            let edge = Edge {
                owner,
                a: add(current, mul(n, half_kerf)),
                b: add(end, mul(n, half_kerf)),
                u,
                normal: n,
                length: len,
                from,
            };
            if let Some(last) = result.last_mut()
                && distance(last.b, edge.a) < EPS
                && cross(last.u, edge.u).abs() < 1e-12
                && dot(last.u, edge.u) > 0.0
                && (last.from + last.length - from).abs() < EPS
            {
                last.b = edge.b;
                last.length += len;
            } else {
                result.push(edge);
            }
        }
        current = end;
        from += len;
    }
    // Collinear subdivisions straddling the arbitrary contour start are one
    // edge too. Its coverage continues beyond the perimeter and is wrapped later.
    if result.len() > 1 {
        let first = &result[0];
        let last = result.last().unwrap();
        if first.from < EPS
            && (last.from + last.length - from).abs() < EPS
            && distance(last.b, first.a) < EPS
            && cross(last.u, first.u).abs() < 1e-12
            && dot(last.u, first.u) > 0.0
        {
            let mut last = result.pop().unwrap();
            let first = result.remove(0);
            last.b = first.b;
            last.length += first.length;
            result.push(last);
        }
    }
    Ok((result, from))
}

fn match_edges(a: &Edge, b: &Edge, owners: &[String]) -> Option<SharedEdge> {
    if a.owner == b.owner || dot(a.normal, b.normal) > -0.999999 {
        return None;
    }
    let b0 = dot(sub(b.a, a.a), a.u);
    let b1 = dot(sub(b.b, a.a), a.u);
    let lo = 0.0_f64.max(b0.min(b1));
    let hi = a.length.min(b0.max(b1));
    if hi - lo + EPS < MIN_SHARED_MM {
        return None;
    }
    let from = add(a.a, mul(a.u, lo));
    let to = add(a.a, mul(a.u, hi));
    // Both ends of the actual overlap must be collinear, not only one endpoint
    // of a long tilted edge. The emitted line is exactly A's analytic offset.
    let error = cross(sub(from, b.a), b.u)
        .abs()
        .max(cross(sub(to, b.a), b.u).abs());
    if error > COLLINEAR_MM + EPS {
        return None;
    }
    let t0 = dot(sub(from, b.a), b.u).clamp(0.0, b.length);
    let t1 = dot(sub(to, b.a), b.u).clamp(0.0, b.length);
    Some(SharedEdge {
        from_mm: from,
        to_mm: to,
        maximum_offset_difference_mm: error,
        owners: [
            Coverage {
                part_copy: owners[a.owner].clone(),
                from_mm: a.from + lo,
                to_mm: a.from + hi,
            },
            Coverage {
                part_copy: owners[b.owner].clone(),
                from_mm: b.from + t0.min(t1),
                to_mm: b.from + t0.max(t1),
            },
        ],
    })
}

fn coverage(length: f64, spans: &[&Coverage]) -> (f64, usize) {
    let mut intervals = vec![];
    for span in spans {
        let width = (span.to_mm - span.from_mm).min(length);
        let start = span.from_mm.rem_euclid(length);
        intervals.push([start, (start + width).min(length)]);
        if start + width > length {
            intervals.push([0.0, start + width - length]);
        }
    }
    intervals.sort_by(|a, b| a[0].total_cmp(&b[0]));
    let mut merged: Vec<[f64; 2]> = vec![];
    for p in intervals {
        if let Some(last) = merged.last_mut()
            && p[0] <= last[1] + EPS
        {
            last[1] = last[1].max(p[1]);
        } else {
            merged.push(p);
        }
    }
    let removed: f64 = merged.iter().map(|p| p[1] - p[0]).sum();
    if removed >= length - EPS {
        return (length, 0);
    }
    if merged.is_empty() {
        return (0.0, 1);
    }
    let wraps =
        merged.len() > 1 && merged[0][0] <= EPS && merged.last().unwrap()[1] >= length - EPS;
    (removed, merged.len() - usize::from(wraps))
}

/// Validate a layout and derive all compensated shared edges in millimetres.
/// The independent validator still sees the caller's original job and spacing.
pub fn analyze(
    job: &Job,
    layout: &Layout,
    curves: &HashMap<String, Outline>,
    options: Options,
) -> Result<Vec<Report>> {
    options.validate()?;
    ensure!(
        job.parts.iter().all(|p| p.geometry.len() == 1),
        "common-line cutting requires one outer component per part"
    );
    ensure!(
        job.units != nestbolt_validator::Units::Unitless,
        "common-line kerf needs physical mm or inch units"
    );
    ensure!(
        job.clearance * job.units.to_mm() + EPS >= options.kerf_mm,
        "common-line parts must be spaced by at least the kerf; nest again with spacing = kerf"
    );
    let checked = validate(job, layout)?;
    ensure!(
        checked.valid,
        "common-line paths require an independently valid layout: {:?}",
        checked.violations
    );
    let mut reports = vec![];
    for sheet in &layout.sheets {
        let (mut parts, _, _) = placed(job, layout, &sheet.id, curves)?;
        // Stable ownership makes the chosen exact offset independent of layout
        // vector order (the opposing edge may differ by up to 0.01 mm).
        parts.sort_by(|a, b| a.0.cmp(&b.0));
        let owners: Vec<String> = parts.iter().map(|p| p.0.clone()).collect();
        let mut all_edges = vec![];
        let mut lengths = vec![];
        let mut total_length = 0.0;
        let mut contour_count = 0;
        let mut holes = 0;
        for (owner, (_, contours)) in parts.iter().enumerate() {
            let outer = contours.first().context("part has no outer contour")?;
            let (e, len) = edges(outer, owner, options.kerf_mm / 2.0)?;
            all_edges.extend(e);
            lengths.push(len);
            total_length += len;
            for hole in &contours[1..] {
                let ring = hole.flatten(0.0005)?;
                ensure!(
                    !parts
                        .iter()
                        .enumerate()
                        .any(|(i, (_, other))| i != owner && contains(&ring, other[0].start)),
                    "common-line mode does not allow parts inside holes; nest again with part-in-hole disabled"
                );
                total_length += length::contour(hole);
                holes += 1;
            }
            contour_count += contours.len();
        }
        // Sweep edge bounds: finger-joint jobs have many short, distant edges.
        // Avoid comparing every one with every other edge in those jobs.
        all_edges.retain(|e| e.length + EPS >= MIN_SHARED_MM);
        all_edges.sort_by(|a, b| a.a[0].min(a.b[0]).total_cmp(&b.a[0].min(b.b[0])));
        let mut shared = vec![];
        for (i, a) in all_edges.iter().enumerate() {
            for b in &all_edges[i + 1..] {
                if b.a[0].min(b.b[0]) > a.a[0].max(a.b[0]) + COLLINEAR_MM {
                    break;
                }
                if b.a[1].min(b.b[1]) > a.a[1].max(a.b[1]) + COLLINEAR_MM
                    || b.a[1].max(b.b[1]) < a.a[1].min(a.b[1]) - COLLINEAR_MM
                {
                    continue;
                }
                // Owner order, not the sweep's endpoint order, selects the
                // analytic source line when offsets differ within tolerance.
                let pair = if a.owner < b.owner { (a, b) } else { (b, a) };
                if let Some(edge) = match_edges(pair.0, pair.1, &owners) {
                    shared.push(edge);
                }
            }
        }
        let paths = chains::paths(shared.iter().map(|s| [s.from_mm, s.to_mm]).collect());
        let shared_length: f64 = paths.iter().map(length::contour).sum();
        let mut removed = 0.0;
        let mut unshared_count = holes;
        for (owner, len) in owners.iter().zip(lengths) {
            let spans: Vec<_> = shared
                .iter()
                .flat_map(|s| &s.owners)
                .filter(|s| &s.part_copy == owner)
                .collect();
            let (amount, pieces) = coverage(len, &spans);
            removed += amount;
            unshared_count += pieces;
        }
        let with_common = (total_length - removed + shared_length).max(0.0);
        let saved = total_length - with_common;
        reports.push(Report {
            sheet_id: sheet.id.clone(),
            kerf_mm: options.kerf_mm,
            collinearity_tolerance_mm: COLLINEAR_MM,
            minimum_shared_length_mm: MIN_SHARED_MM,
            shared_edges: shared,
            paths_with_common: unshared_count + paths.len(),
            paths,
            shared_length_mm: shared_length,
            cut_length_without_common_mm: total_length,
            cut_length_with_common_mm: with_common,
            saved_length_mm: saved,
            saved_fraction: if total_length > 0.0 {
                saved / total_length
            } else {
                0.0
            },
            contours_without_common: contour_count,
        });
    }
    Ok(reports)
}
