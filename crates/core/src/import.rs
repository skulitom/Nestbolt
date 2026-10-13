//! SVG and DXF import into exact source contours and nesting polygons.
//!
//! Geometry is converted to millimetres in a Y-up frame. Each closed outer
//! contour becomes one physical part, with the contours directly inside it as
//! holes; islands inside holes are parts of their own. Open paths are chained
//! end to end; anything still open is reported and skipped. Nesting polygons
//! are chord flattenings within `tolerance` of the exact curves; callers widen
//! clearances by that tolerance so the true curves keep the requested gaps.
use std::collections::HashMap;
use std::f64::consts::{PI, TAU};

use anyhow::{Context, Result, bail, ensure};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

use crate::curves::{Affine, Contour, Point, Segment, bounds, contains, signed_area};

mod cleanup;
mod selection;
mod svg_style;
mod text;
pub use cleanup::Cleanup;
pub use selection::Channel;
use selection::{Drawing, DrawingEntity};
pub use text::decode_drawing;

#[derive(Clone, Debug, Deserialize)]
#[serde(default, deny_unknown_fields)]
pub struct Options {
    /// Maximum distance between an exact curve and its nesting polygon, in mm.
    pub tolerance: f64,
    /// Millimetres per SVG user unit when the document gives no absolute size.
    /// CSS pixels (25.4 / 96 mm) by default.
    pub svg_user_unit: f64,
    /// Millimetres per DXF drawing unit when `$INSUNITS` is absent or unitless.
    pub dxf_unit: f64,
    /// Explicit repair of larger gaps, in mm (off by default, at most 1 mm).
    /// The silent join threshold remains 0.005 mm regardless of curve precision.
    pub close_gaps_mm: Option<f64>,
    /// Explicit layer names; None uses cut/outline/profile names, then all contours.
    pub layers: Option<Vec<String>>,
    /// Explicit DXF ACI numbers ("7" or "aci:7") or SVG/DXF RGB colours.
    pub colors: Option<Vec<String>>,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            tolerance: 0.005,
            svg_user_unit: 25.4 / 96.0,
            dxf_unit: 1.0,
            close_gaps_mm: None,
            layers: None,
            colors: None,
        }
    }
}

#[derive(Clone, Debug, Serialize)]
pub struct ImportedPart {
    pub id: String,
    /// Source element id, layer or block, for the user's reference.
    pub source: String,
    pub outer: Contour,
    pub holes: Vec<Contour>,
    /// Counter-clockwise outer and clockwise holes, flattened within tolerance.
    pub polygon: nestbolt_validator::Polygon,
    pub area: f64,
    pub bounds: [f64; 4],
}

#[derive(Clone, Debug, Serialize)]
pub struct Import {
    pub parts: Vec<ImportedPart>,
    pub warnings: Vec<String>,
    pub report: ImportReport,
}

pub const SILENT_JOIN_MM: f64 = 0.005;

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct Gap {
    pub source: String,
    pub from_mm: Point,
    pub to_mm: Point,
    pub size_mm: f64,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct OpenContour {
    pub source: String,
    pub start_mm: Point,
    pub end_mm: Point,
    pub end_gap_mm: f64,
    /// None means the endpoints exceed the 1 mm automatic repair limit.
    pub suggested_close_gaps_mm: Option<f64>,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct UnitReport {
    pub declared: bool,
    pub mm_per_unit: f64,
    pub largest_dimension_in_drawing_units: Option<f64>,
    pub possible_inches: bool,
}

#[derive(Clone, Debug, Serialize, Deserialize, JsonSchema)]
pub struct ImportReport {
    pub silent_join_mm: f64,
    pub close_gaps_mm: Option<f64>,
    pub closed_gaps: Vec<Gap>,
    pub open_contours: Vec<OpenContour>,
    #[serde(default)]
    pub layers: Vec<Channel>,
    #[serde(default)]
    pub colors: Vec<Channel>,
    #[serde(default)]
    pub selection_mode: String,
    #[serde(default)]
    pub cleanup: Cleanup,
    #[serde(default)]
    pub units: Option<UnitReport>,
}

impl ImportReport {
    fn new(options: &Options) -> Result<Self> {
        ensure!(
            options.tolerance.is_finite() && options.tolerance > 0.0,
            "curve tolerance must be a finite positive number in mm"
        );
        ensure!(
            options.svg_user_unit.is_finite()
                && options.svg_user_unit > 0.0
                && options.dxf_unit.is_finite()
                && options.dxf_unit > 0.0,
            "drawing units must be a finite positive number of mm per unit"
        );
        if let Some(gap) = options.close_gaps_mm {
            ensure!(
                gap.is_finite() && (0.0..=1.0).contains(&gap),
                "Close gaps must be between 0 and 1 mm; repair larger gaps in the source drawing"
            );
        }
        Ok(Self {
            silent_join_mm: SILENT_JOIN_MM,
            close_gaps_mm: options.close_gaps_mm,
            closed_gaps: vec![],
            open_contours: vec![],
            layers: vec![],
            colors: vec![],
            selection_mode: String::new(),
            cleanup: Cleanup::default(),
            units: None,
        })
    }
}

/// An open run of segments, or a closed loop when `start == end`.
#[derive(Clone, Debug)]
struct Piece {
    start: Point,
    segments: Vec<Segment>,
    source: String,
}

impl Piece {
    fn end(&self) -> Point {
        self.segments.last().map_or(self.start, Segment::end)
    }
}

fn dist(a: Point, b: Point) -> f64 {
    (a[0] - b[0]).hypot(a[1] - b[1])
}

/// Reverse a run: the result traverses the same curve from its end.
fn reverse(start: Point, segments: &[Segment]) -> (Point, Vec<Segment>) {
    let mut points = vec![start];
    for s in segments {
        points.push(s.end());
    }
    let mut out = Vec::with_capacity(segments.len());
    for (i, s) in segments.iter().enumerate().rev() {
        let from = points[i];
        out.push(match s {
            Segment::Line { .. } => Segment::Line { to: from },
            Segment::Quad { control, .. } => Segment::Quad {
                control: *control,
                to: from,
            },
            Segment::Cubic { controls, .. } => Segment::Cubic {
                controls: [controls[1], controls[0]],
                to: from,
            },
            Segment::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } => Segment::Arc {
                center: *center,
                radii: *radii,
                rotation: *rotation,
                start: start + sweep,
                sweep: -sweep,
            },
        });
    }
    (*points.last().expect("start point"), out)
}

/// Arcs under a non-similarity map become cubic BÃ©ziers of at most 22.5Â°,
/// whose radial error is below 1e-7 of the radius; everything else maps exactly.
fn map_segments(start: Point, segments: &[Segment], a: &Affine) -> (Point, Vec<Segment>) {
    let similar = {
        let (c0, c1) = ([a.m[0][0], a.m[1][0]], [a.m[0][1], a.m[1][1]]);
        let (n0, n1) = (c0[0].hypot(c0[1]), c1[0].hypot(c1[1]));
        (c0[0] * c1[0] + c0[1] * c1[1]).abs() <= 1e-12 * n0 * n1 && (n0 - n1).abs() <= 1e-12 * n0
    };
    let mut out = vec![];
    for s in segments {
        match s {
            Segment::Arc {
                center,
                radii,
                rotation,
                start,
                sweep,
            } if !similar => {
                let pieces = (sweep.abs() / (PI / 8.0)).ceil().max(1.0) as usize;
                let step = sweep / pieces as f64;
                let k = 4.0 / 3.0 * (step / 4.0).tan();
                let (rs, rc) = rotation.sin_cos();
                let at = |t: f64| {
                    let (x, y) = (radii[0] * t.cos(), radii[1] * t.sin());
                    [center[0] + rc * x - rs * y, center[1] + rs * x + rc * y]
                };
                let tangent = |t: f64| {
                    let (x, y) = (-radii[0] * t.sin(), radii[1] * t.cos());
                    [rc * x - rs * y, rs * x + rc * y]
                };
                for i in 0..pieces {
                    let (t0, t1) = (start + step * i as f64, start + step * (i + 1) as f64);
                    let (p0, p3) = (at(t0), at(t1));
                    let (d0, d1) = (tangent(t0), tangent(t1));
                    let c1 = [p0[0] + k * d0[0], p0[1] + k * d0[1]];
                    let c2 = [p3[0] - k * d1[0], p3[1] - k * d1[1]];
                    out.push(Segment::Cubic {
                        controls: [a.apply(c1), a.apply(c2)],
                        to: a.apply(p3),
                    });
                }
            }
            s => out.push(s.transformed(a)),
        }
    }
    (a.apply(start), out)
}

/// Join open runs whose ends meet within `tolerance`; return closed loops and
/// the number of runs left open.
/// Join pieces that follow each other in file order, as exporters write one
/// outline's entities, for as long as each starts where the chain ends. An
/// outline may pass through its own start point (a pinch) or carry relief loops
/// that close on themselves (boxes.py slot corners), so returning to the start
/// does not end it. Figures that really touch then nest together, which is
/// conservative.
fn sequential(pieces: Vec<Piece>, tolerance: f64) -> Vec<Piece> {
    let mut chains: Vec<Piece> = vec![];
    for piece in pieces.into_iter().filter(|p| !p.segments.is_empty()) {
        if let Some(current) = chains.last_mut()
            && dist(piece.start, current.end()) <= tolerance
        {
            current.segments.extend(piece.segments);
            continue;
        }
        chains.push(piece);
    }
    chains
}

fn chain(
    pieces: Vec<Piece>,
    tolerance: f64,
    report: &mut ImportReport,
) -> (Vec<Piece>, Vec<Piece>) {
    let (mut closed, mut open): (Vec<_>, Vec<_>) = sequential(pieces, SILENT_JOIN_MM)
        .into_iter()
        .partition(|p| dist(p.start, p.end()) <= SILENT_JOIN_MM);
    let mut left = vec![];
    while let Some(mut current) = open.pop() {
        loop {
            if dist(current.start, current.end()) <= tolerance {
                let start = current.start;
                bridge_gap(&mut current, start, report);
                closed.push(current);
                break;
            }
            let end = current.end();
            let next = open
                .iter()
                .enumerate()
                .map(|(i, p)| (i, dist(p.start, end).min(dist(p.end(), end))))
                .filter(|(_, gap)| *gap <= tolerance)
                .min_by(|a, b| a.1.total_cmp(&b.1))
                .map(|(i, _)| i);
            let Some(i) = next else {
                left.push(current);
                break;
            };
            let p = open.swap_remove(i);
            if dist(p.start, end) <= dist(p.end(), end) {
                bridge_gap(&mut current, p.start, report);
                current.segments.extend(p.segments);
            } else {
                let (start, reversed) = reverse(p.start, &p.segments);
                bridge_gap(&mut current, start, report);
                current.segments.extend(reversed);
            }
        }
    }
    (closed, left)
}

fn bridge_gap(piece: &mut Piece, to: Point, report: &mut ImportReport) {
    let from = piece.end();
    let size = dist(from, to);
    if size > SILENT_JOIN_MM {
        report.closed_gaps.push(Gap {
            source: piece.source.clone(),
            from_mm: from,
            to_mm: to,
            size_mm: size,
        });
        // Keep both original curve endpoints. An explicit straight bridge is
        // easier to review and does not distort a neighbouring Bezier or arc.
        piece.segments.push(Segment::Line { to });
    }
}

/// Snap a closed loop's last segment onto its start point.
fn close(mut piece: Piece) -> Contour {
    let start = piece.start;
    if let Some(last) = piece.segments.last_mut() {
        match last {
            Segment::Line { to } | Segment::Quad { to, .. } | Segment::Cubic { to, .. } => {
                *to = start
            }
            Segment::Arc { .. } => {
                if dist(last.end(), start) > 0.0 {
                    piece.segments.push(Segment::Line { to: start });
                }
            }
        }
    }
    Contour {
        start,
        segments: piece.segments,
    }
}

/// Clipper2 coordinates: nanometres, as the validator uses.
const NM: f64 = 1_000_000.0;

fn to_path(ring: &[Point]) -> clipper2_rust::Path64 {
    ring.iter()
        .map(|p| {
            clipper2_rust::Point64::new((p[0] * NM).round() as i64, (p[1] * NM).round() as i64)
        })
        .collect()
}

fn from_path(path: &clipper2_rust::Path64) -> Vec<Point> {
    path.iter()
        .map(|p| [p.x as f64 / NM, p.y as f64 / NM])
        .collect()
}

/// A conservative stand-in for an outline that touches or crosses itself, as
/// boxes.py relief loops at slot corners do: the nonzero union of its rings
/// (attached loops stay covered), then a morphological closing by `delta` that
/// fills slits and touching points narrower than `2 delta`. The result never
/// shrinks the outer outline or grows a hole; concave corners move by at most
/// `delta`. `None` if it splits into separate pieces.
fn closed_polygon(
    polygon: &nestbolt_validator::Polygon,
    delta: f64,
) -> Option<nestbolt_validator::Polygon> {
    use clipper2_rust::{ClipType, Clipper64, ClipperOffset, EndType, FillRule, JoinType, Paths64};
    let rings: Paths64 = std::iter::once(&polygon.outer)
        .chain(&polygon.holes)
        .map(|r| to_path(r))
        .collect();
    let mut union = Clipper64::new();
    union.add_subject(&rings);
    let mut merged = Paths64::new();
    let mut open = Paths64::new();
    if !union.execute(
        ClipType::Union,
        FillRule::NonZero,
        &mut merged,
        Some(&mut open),
    ) {
        return None;
    }
    let mut paths = merged;
    for (distance, join) in [(delta, JoinType::Round), (-delta, JoinType::Miter)] {
        let mut engine = ClipperOffset::new(2.0, delta * NM / 4.0, false, false);
        engine.add_paths(&paths, join, EndType::Polygon);
        let mut next = Paths64::new();
        engine.execute(distance * NM, &mut next);
        if engine.error_code() != 0 || next.is_empty() {
            return None;
        }
        paths = next;
    }
    let (outers, holes): (Vec<_>, Vec<_>) = paths
        .iter()
        .map(from_path)
        .partition(|r| signed_area(r) > 0.0);
    let [outer] = <[Vec<Point>; 1]>::try_from(outers).ok()?;
    // The validator normalises ring orientation.
    Some(nestbolt_validator::Polygon {
        outer: thin(outer),
        holes: holes.into_iter().map(thin).collect(),
    })
}

/// Drop vertices within 0.1 µm of the previous kept one, so offsets cannot
/// leave vertices that single-precision collision shapes would merge.
fn thin(ring: Vec<Point>) -> Vec<Point> {
    let mut kept: Vec<Point> = Vec::with_capacity(ring.len());
    for p in ring {
        if kept.last().is_none_or(|&q| dist(p, q) > 1e-4) {
            kept.push(p);
        }
    }
    while kept.len() > 3 && dist(kept[0], *kept.last().expect("non-empty")) <= 1e-4 {
        kept.pop();
    }
    kept
}

/// Collision shapes are single precision: distinct vertices must stay distinct.
fn simple_in_f32(ring: &[Point]) -> bool {
    let mut points: Vec<(u32, u32)> = ring
        .iter()
        .map(|p| ((p[0] as f32).to_bits(), (p[1] as f32).to_bits()))
        .collect();
    points.dedup();
    if points.len() > 1 && points.first() == points.last() {
        points.pop();
    }
    let mut seen = std::collections::HashSet::with_capacity(points.len());
    if !points.iter().all(|&p| seen.insert(p)) {
        return false;
    }
    // No two non-adjacent edges may touch once rounded to single precision.
    let v: Vec<[f64; 2]> = points
        .iter()
        .map(|&(x, y)| [f64::from(f32::from_bits(x)), f64::from(f32::from_bits(y))])
        .collect();
    let n = v.len();
    let cross = |o: [f64; 2], a: [f64; 2], b: [f64; 2]| {
        (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    };
    let on = |a: [f64; 2], b: [f64; 2], p: [f64; 2]| {
        a[0].min(b[0]) <= p[0]
            && p[0] <= a[0].max(b[0])
            && a[1].min(b[1]) <= p[1]
            && p[1] <= a[1].max(b[1])
    };
    let touch = |a: [f64; 2], b: [f64; 2], c: [f64; 2], d: [f64; 2]| {
        let (d1, d2, d3, d4) = (
            cross(c, d, a),
            cross(c, d, b),
            cross(a, b, c),
            cross(a, b, d),
        );
        ((d1 > 0.0) != (d2 > 0.0)
            && (d3 > 0.0) != (d4 > 0.0)
            && d1 != 0.0
            && d2 != 0.0
            && d3 != 0.0
            && d4 != 0.0)
            || (d1 == 0.0 && on(c, d, a))
            || (d2 == 0.0 && on(c, d, b))
            || (d3 == 0.0 && on(a, b, c))
            || (d4 == 0.0 && on(a, b, d))
    };
    let mut edges: Vec<usize> = (0..n).collect();
    let min_x = |i: usize| v[i][0].min(v[(i + 1) % n][0]);
    edges.sort_by(|&a, &b| min_x(a).total_cmp(&min_x(b)));
    for (k, &i) in edges.iter().enumerate() {
        let (a, b) = (v[i], v[(i + 1) % n]);
        let max_x = a[0].max(b[0]);
        for &j in &edges[k + 1..] {
            if min_x(j) > max_x {
                break;
            }
            if j == (i + 1) % n || i == (j + 1) % n {
                continue;
            }
            if touch(a, b, v[j], v[(j + 1) % n]) {
                return false;
            }
        }
    }
    true
}

/// The nesting polygon checked as the validator will, repaired if needed.
fn checked_polygon(
    polygon: nestbolt_validator::Polygon,
    source: &str,
    tolerance: f64,
    warnings: &mut Vec<String>,
) -> Option<nestbolt_validator::Polygon> {
    let identity = nestbolt_validator::RigidTransform {
        translation: [0.0, 0.0],
        rotation_radians: 0.0,
        mirrored: false,
    };
    let valid = |p: &nestbolt_validator::Polygon| {
        simple_in_f32(&p.outer)
            && nestbolt_validator::Footprint::new(p, nestbolt_validator::Units::Mm, identity)
                .is_ok()
    };
    if valid(&polygon) {
        return Some(polygon);
    }
    // Independent of the flattening tolerance, so a re-import repairs alike;
    // larger closings stay conservative and are tried only when needed.
    let base = tolerance.max(0.005);
    for delta in [base, 2.0 * base, 4.0 * base, 8.0 * base] {
        if let Some(p) = closed_polygon(&polygon, delta).filter(|p| valid(p)) {
            warnings.push(format!(
                "{source}: outline touches itself (for example relief loops); the nesting \
                 outline closes gaps under {:.3} mm, exports keep the exact curves",
                2.0 * delta
            ));
            return Some(p);
        }
    }
    warnings.push(format!(
        "{source}: outline crosses or touches itself; part skipped"
    ));
    None
}

fn assemble(
    pieces: Vec<Piece>,
    options: &Options,
    warnings: &mut Vec<String>,
    report: &mut ImportReport,
) -> Result<Vec<ImportedPart>> {
    let pieces = cleanup::clean(pieces, &mut report.cleanup);
    if report.cleanup != Cleanup::default() {
        warnings.push(format!("cleanup removed {} exact duplicate segment(s), {} zero-length segment(s); merged {} overlapping collinear segment(s)",
            report.cleanup.duplicate_segments_removed, report.cleanup.zero_length_segments_removed, report.cleanup.overlapping_segments_merged));
    }
    let (mut closed, mut open) = chain(pieces, SILENT_JOIN_MM, report);
    if let Some(limit) = options.close_gaps_mm.filter(|v| *v > SILENT_JOIN_MM) {
        let (repaired, remaining) = chain(open, limit, report);
        closed.extend(repaired);
        open = remaining;
    }
    for gap in &report.closed_gaps {
        warnings.push(format!("{}: closed gap {:.6} mm from ({:.6}, {:.6}) to ({:.6}, {:.6}) with explicit Close gaps",
            gap.source,gap.size_mm,gap.from_mm[0],gap.from_mm[1],gap.to_mm[0],gap.to_mm[1]));
    }
    for piece in open {
        let gap = dist(piece.start, piece.end());
        let suggested = (gap <= 1.0).then_some((gap * 1_000_000.0).ceil() / 1_000_000.0);
        let fix = if let Some(size) = suggested {
            format!("enable Close gaps up to {size:.6} mm")
        } else {
            "join these endpoints in the source drawing (automatic repair is limited to 1 mm)"
                .into()
        };
        warnings.push(format!("{}: open path from ({:.6}, {:.6}) to ({:.6}, {:.6}); end gap {:.6} mm; {fix}. This contour was not imported",
            piece.source,piece.start[0],piece.start[1],piece.end()[0],piece.end()[1],gap));
        report.open_contours.push(OpenContour {
            source: piece.source,
            start_mm: piece.start,
            end_mm: piece.segments.last().map_or(piece.start, Segment::end),
            end_gap_mm: gap,
            suggested_close_gaps_mm: suggested,
        });
    }
    let mut loops = vec![];
    for piece in closed {
        let source = piece.source.clone();
        let contour = close(piece);
        match contour.flatten(options.tolerance) {
            Ok(points) if signed_area(&points).abs() > 0.0 => loops.push((contour, points, source)),
            Ok(_) | Err(_) => warnings.push(format!("{source}: degenerate contour skipped")),
        }
    }
    // Containment depth by the smallest containing loop; even depth is an outer.
    let areas: Vec<f64> = loops.iter().map(|l| signed_area(&l.1).abs()).collect();
    let parent: Vec<Option<usize>> = (0..loops.len())
        .map(|i| {
            let probe = loops[i].1[0];
            (0..loops.len())
                .filter(|&j| j != i && areas[j] > areas[i] && contains(&loops[j].1, probe))
                .min_by(|&a, &b| areas[a].total_cmp(&areas[b]))
        })
        .collect();
    let depth = |mut i: usize| {
        let mut d = 0;
        while let Some(p) = parent[i] {
            d += 1;
            i = p;
        }
        d
    };
    let mut parts = vec![];
    for i in (0..loops.len()).filter(|&i| depth(i) % 2 == 0) {
        let (outer, points, source) = &loops[i];
        let mut outer_points = points.clone();
        if signed_area(&outer_points) < 0.0 {
            outer_points.reverse();
        }
        let mut holes = vec![];
        let mut hole_points = vec![];
        for j in (0..loops.len()).filter(|&j| parent[j] == Some(i)) {
            let mut h = loops[j].1.clone();
            if signed_area(&h) > 0.0 {
                h.reverse();
            }
            holes.push(loops[j].0.clone());
            hole_points.push(h);
        }
        let polygon = nestbolt_validator::Polygon {
            outer: outer_points,
            holes: hole_points,
        };
        let Some(polygon) = checked_polygon(polygon, source, options.tolerance, warnings) else {
            continue;
        };
        let area =
            signed_area(&polygon.outer) + polygon.holes.iter().map(|h| signed_area(h)).sum::<f64>();
        parts.push(ImportedPart {
            id: format!("part-{}", parts.len() + 1),
            source: source.clone(),
            bounds: bounds(&polygon.outer),
            outer: outer.clone(),
            holes,
            polygon,
            area,
        });
    }
    ensure!(
        !parts.is_empty(),
        "no closed part outlines found; {}",
        warnings
            .iter()
            .take(8)
            .cloned()
            .collect::<Vec<_>>()
            .join("; ")
    );
    Ok(parts)
}

// ---------------------------------------------------------------- SVG

fn length_mm(value: &str, user: f64) -> Option<f64> {
    let length: svgtypes::Length = value.parse().ok()?;
    use svgtypes::LengthUnit as U;
    let n = length.number;
    Some(match length.unit {
        U::None | U::Px => n * 25.4 / 96.0,
        U::Mm => n,
        U::Cm => n * 10.0,
        U::In => n * 25.4,
        U::Pt => n * 25.4 / 72.0,
        U::Pc => n * 25.4 / 6.0,
        U::Em | U::Ex | U::Percent => return None,
    })
    .map(|mm| {
        if length.unit == U::None && user != 25.4 / 96.0 {
            n * user
        } else {
            mm
        }
    })
}

fn svg_transform(value: Option<&str>) -> Result<Affine> {
    let Some(value) = value else {
        return Ok(Affine::IDENTITY);
    };
    let t: svgtypes::Transform = value
        .parse()
        .with_context(|| format!("invalid SVG transform {value:?}"))?;
    Ok(Affine {
        m: [[t.a, t.c], [t.b, t.d]],
        t: [t.e, t.f],
    })
}

/// SVG endpoint arc to centre form (SVG 1.1, appendix F.6.5).
#[allow(clippy::too_many_arguments)]
fn svg_arc(
    from: Point,
    rx: f64,
    ry: f64,
    phi_deg: f64,
    large: bool,
    sweep: bool,
    to: Point,
) -> Segment {
    if dist(from, to) == 0.0 {
        return Segment::Line { to };
    }
    let (mut rx, mut ry) = (rx.abs(), ry.abs());
    if rx == 0.0 || ry == 0.0 {
        return Segment::Line { to };
    }
    let phi = phi_deg.to_radians();
    let (s, c) = phi.sin_cos();
    let dx = (from[0] - to[0]) / 2.0;
    let dy = (from[1] - to[1]) / 2.0;
    let x1 = c * dx + s * dy;
    let y1 = -s * dx + c * dy;
    let lambda = (x1 * x1) / (rx * rx) + (y1 * y1) / (ry * ry);
    if lambda > 1.0 {
        rx *= lambda.sqrt();
        ry *= lambda.sqrt();
    }
    let num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1;
    let den = rx * rx * y1 * y1 + ry * ry * x1 * x1;
    let mut coef = (num / den).max(0.0).sqrt();
    if large == sweep {
        coef = -coef;
    }
    let cx1 = coef * rx * y1 / ry;
    let cy1 = -coef * ry * x1 / rx;
    let center = [
        c * cx1 - s * cy1 + (from[0] + to[0]) / 2.0,
        s * cx1 + c * cy1 + (from[1] + to[1]) / 2.0,
    ];
    let angle = |ux: f64, uy: f64, vx: f64, vy: f64| {
        let dot = ux * vx + uy * vy;
        let det = ux * vy - uy * vx;
        det.atan2(dot)
    };
    let start = angle(1.0, 0.0, (x1 - cx1) / rx, (y1 - cy1) / ry);
    let mut delta = angle(
        (x1 - cx1) / rx,
        (y1 - cy1) / ry,
        (-x1 - cx1) / rx,
        (-y1 - cy1) / ry,
    );
    if !sweep && delta > 0.0 {
        delta -= TAU;
    } else if sweep && delta < 0.0 {
        delta += TAU;
    }
    Segment::Arc {
        center,
        radii: [rx, ry],
        rotation: phi,
        start,
        sweep: delta,
    }
}

fn svg_path(d: &str, source: &str) -> Result<Vec<Piece>> {
    use svgtypes::PathSegment as P;
    let mut pieces = vec![];
    let mut current: Option<Piece> = None;
    let mut point = [0.0, 0.0];
    let mut start = [0.0, 0.0];
    let mut last_cubic: Option<Point> = None;
    let mut last_quad: Option<Point> = None;
    let finish = |current: &mut Option<Piece>, pieces: &mut Vec<Piece>| {
        if let Some(p) = current.take()
            && !p.segments.is_empty()
        {
            pieces.push(p);
        }
    };
    for segment in svgtypes::PathParser::from(d) {
        let segment = segment.with_context(|| format!("{source}: invalid path data"))?;
        let rel = |abs: bool, x: f64, y: f64| {
            if abs {
                [x, y]
            } else {
                [point[0] + x, point[1] + y]
            }
        };
        let push = |current: &mut Option<Piece>, s: Segment| {
            current
                .get_or_insert_with(|| Piece {
                    start: point,
                    segments: vec![],
                    source: source.into(),
                })
                .segments
                .push(s);
        };
        let (mut cubic, mut quad) = (None, None);
        match segment {
            P::MoveTo { abs, x, y } => {
                finish(&mut current, &mut pieces);
                point = rel(abs, x, y);
                start = point;
            }
            P::LineTo { abs, x, y } => {
                let to = rel(abs, x, y);
                push(&mut current, Segment::Line { to });
                point = to;
            }
            P::HorizontalLineTo { abs, x } => {
                let to = [if abs { x } else { point[0] + x }, point[1]];
                push(&mut current, Segment::Line { to });
                point = to;
            }
            P::VerticalLineTo { abs, y } => {
                let to = [point[0], if abs { y } else { point[1] + y }];
                push(&mut current, Segment::Line { to });
                point = to;
            }
            P::CurveTo {
                abs,
                x1,
                y1,
                x2,
                y2,
                x,
                y,
            } => {
                let (c1, c2, to) = (rel(abs, x1, y1), rel(abs, x2, y2), rel(abs, x, y));
                push(
                    &mut current,
                    Segment::Cubic {
                        controls: [c1, c2],
                        to,
                    },
                );
                cubic = Some(c2);
                point = to;
            }
            P::SmoothCurveTo { abs, x2, y2, x, y } => {
                let c1 =
                    last_cubic.map_or(point, |c| [2.0 * point[0] - c[0], 2.0 * point[1] - c[1]]);
                let (c2, to) = (rel(abs, x2, y2), rel(abs, x, y));
                push(
                    &mut current,
                    Segment::Cubic {
                        controls: [c1, c2],
                        to,
                    },
                );
                cubic = Some(c2);
                point = to;
            }
            P::Quadratic { abs, x1, y1, x, y } => {
                let (control, to) = (rel(abs, x1, y1), rel(abs, x, y));
                push(&mut current, Segment::Quad { control, to });
                quad = Some(control);
                point = to;
            }
            P::SmoothQuadratic { abs, x, y } => {
                let control =
                    last_quad.map_or(point, |c| [2.0 * point[0] - c[0], 2.0 * point[1] - c[1]]);
                let to = rel(abs, x, y);
                push(&mut current, Segment::Quad { control, to });
                quad = Some(control);
                point = to;
            }
            P::EllipticalArc {
                abs,
                rx,
                ry,
                x_axis_rotation,
                large_arc,
                sweep,
                x,
                y,
            } => {
                let to = rel(abs, x, y);
                push(
                    &mut current,
                    svg_arc(point, rx, ry, x_axis_rotation, large_arc, sweep, to),
                );
                point = to;
            }
            P::ClosePath { .. } => {
                if dist(point, start) > 0.0 {
                    push(&mut current, Segment::Line { to: start });
                }
                point = start;
                finish(&mut current, &mut pieces);
            }
        }
        last_cubic = cubic;
        last_quad = quad;
    }
    finish(&mut current, &mut pieces);
    Ok(pieces)
}

fn svg_shape(node: &roxmltree::Node, source: &str) -> Result<Vec<Piece>> {
    let num = |name: &str| node.attribute(name).and_then(|v| v.parse::<f64>().ok());
    let piece = |start: Point, segments: Vec<Segment>| Piece {
        start,
        segments,
        source: source.into(),
    };
    Ok(match node.tag_name().name() {
        "path" => svg_path(node.attribute("d").unwrap_or(""), source)?,
        "rect" => {
            let (x, y) = (num("x").unwrap_or(0.0), num("y").unwrap_or(0.0));
            let (w, h) = (num("width").unwrap_or(0.0), num("height").unwrap_or(0.0));
            if w <= 0.0 || h <= 0.0 {
                return Ok(vec![]);
            }
            let rx = num("rx").or(num("ry")).unwrap_or(0.0).clamp(0.0, w / 2.0);
            let ry = num("ry").or(num("rx")).unwrap_or(0.0).clamp(0.0, h / 2.0);
            if rx == 0.0 || ry == 0.0 {
                vec![piece(
                    [x, y],
                    vec![
                        Segment::Line { to: [x + w, y] },
                        Segment::Line { to: [x + w, y + h] },
                        Segment::Line { to: [x, y + h] },
                        Segment::Line { to: [x, y] },
                    ],
                )]
            } else {
                let arc = |cx: f64, cy: f64, a: f64| Segment::Arc {
                    center: [cx, cy],
                    radii: [rx, ry],
                    rotation: 0.0,
                    start: a,
                    sweep: PI / 2.0,
                };
                vec![piece(
                    [x + rx, y],
                    vec![
                        Segment::Line {
                            to: [x + w - rx, y],
                        },
                        arc(x + w - rx, y + ry, -PI / 2.0),
                        Segment::Line {
                            to: [x + w, y + h - ry],
                        },
                        arc(x + w - rx, y + h - ry, 0.0),
                        Segment::Line {
                            to: [x + rx, y + h],
                        },
                        arc(x + rx, y + h - ry, PI / 2.0),
                        Segment::Line { to: [x, y + ry] },
                        arc(x + rx, y + ry, PI),
                    ],
                )]
            }
        }
        "circle" | "ellipse" => {
            let (cx, cy) = (num("cx").unwrap_or(0.0), num("cy").unwrap_or(0.0));
            let (rx, ry) = if node.tag_name().name() == "circle" {
                let r = num("r").unwrap_or(0.0);
                (r, r)
            } else {
                (num("rx").unwrap_or(0.0), num("ry").unwrap_or(0.0))
            };
            if rx <= 0.0 || ry <= 0.0 {
                return Ok(vec![]);
            }
            vec![piece(
                [cx + rx, cy],
                vec![Segment::Arc {
                    center: [cx, cy],
                    radii: [rx, ry],
                    rotation: 0.0,
                    start: 0.0,
                    sweep: TAU,
                }],
            )]
        }
        "line" => {
            let a = [num("x1").unwrap_or(0.0), num("y1").unwrap_or(0.0)];
            let b = [num("x2").unwrap_or(0.0), num("y2").unwrap_or(0.0)];
            vec![piece(a, vec![Segment::Line { to: b }])]
        }
        "polygon" | "polyline" => {
            let values: Vec<f64> = node
                .attribute("points")
                .unwrap_or("")
                .split(|c: char| c == ',' || c.is_whitespace())
                .filter(|s| !s.is_empty())
                .filter_map(|s| s.parse().ok())
                .collect();
            let points: Vec<Point> = values.as_chunks::<2>().0.to_vec();
            if points.len() < 2 {
                return Ok(vec![]);
            }
            let mut segments: Vec<_> = points[1..].iter().map(|&to| Segment::Line { to }).collect();
            if node.tag_name().name() == "polygon" {
                segments.push(Segment::Line { to: points[0] });
            }
            vec![piece(points[0], segments)]
        }
        _ => vec![],
    })
}

/// Import closed outlines from an SVG document. Text and images are ignored.
pub fn import_svg(text: &str, options: &Options) -> Result<Import> {
    read_svg(text, options, false)
}

/// Inventory the document without chaining or requiring a closed part.
pub fn inspect_svg(text: &str, options: &Options) -> Result<ImportReport> {
    Ok(read_svg(text, options, true)?.report)
}

fn read_svg(text: &str, options: &Options, inspect_only: bool) -> Result<Import> {
    let report = ImportReport::new(options)?;
    let document = roxmltree::Document::parse_with_options(
        text,
        roxmltree::ParsingOptions {
            allow_dtd: true,
            nodes_limit: 1_000_000,
            entity_resolver: None,
        },
    )
    .context("invalid SVG/XML; save as plain SVG and check its XML syntax")?;
    let root = document.root_element();
    ensure!(
        root.tag_name().name() == "svg",
        "the document root is not <svg>"
    );
    let mut warnings = vec![];
    // User units to millimetres, from the outer size and viewBox when given.
    let view: Option<svgtypes::ViewBox> = root.attribute("viewBox").and_then(|v| v.parse().ok());
    let width = root
        .attribute("width")
        .and_then(|v| length_mm(v, options.svg_user_unit));
    let height = root
        .attribute("height")
        .and_then(|v| length_mm(v, options.svg_user_unit));
    let (scale, origin) = match (view, width, height) {
        (Some(v), Some(w), h) if v.w > 0.0 => {
            let sx = w / v.w;
            if let Some(h) = h
                && v.h > 0.0
                && ((h / v.h) - sx).abs() > 1e-9 * sx
            {
                warnings.push("non-uniform viewBox scaling; using the width scale".into());
            }
            (sx, [v.x, v.y])
        }
        (Some(v), None, _) => (options.svg_user_unit, [v.x, v.y]),
        _ => (options.svg_user_unit, [0.0, 0.0]),
    };
    // SVG is Y-down: flip into the Y-up sheet frame.
    let page = Affine {
        m: [[scale, 0.0], [0.0, -scale]],
        t: [-origin[0] * scale, origin[1] * scale],
    };
    let ids: HashMap<&str, roxmltree::Node> = document
        .descendants()
        .filter_map(|n| n.attribute("id").map(|id| (id, n)))
        .collect();
    let rules = svg_style::stylesheet(&document)?;
    let mut drawing = Drawing::default();
    let mut counter = 0;
    let mut stack = vec![(root, Affine::IDENTITY, 0_u32, svg_style::Style::default())];
    while let Some((node, parent, depth, parent_style)) = stack.pop() {
        if !node.is_element() {
            continue;
        }
        let name = node.tag_name().name();
        if matches!(
            name,
            "defs"
                | "clipPath"
                | "mask"
                | "symbol"
                | "pattern"
                | "marker"
                | "metadata"
                | "title"
                | "desc"
                | "style"
        ) {
            continue;
        }
        let style = parent_style.at(node, &rules);
        if node.has_tag_name("g") {
            drawing.known_layers.push(style.layer.clone());
        }
        let local = svg_transform(node.attribute("transform"))?;
        let ctm = if node == root {
            Affine::IDENTITY
        } else {
            local.then(parent)
        };
        if name == "use" {
            ensure!(depth < 16, "SVG <use> nesting is too deep");
            let href = node
                .attribute(("http://www.w3.org/1999/xlink", "href"))
                .or(node.attribute("href"))
                .unwrap_or("");
            if let Some(target) = href.strip_prefix('#').and_then(|id| ids.get(id)) {
                let x = node
                    .attribute("x")
                    .and_then(|v| v.parse().ok())
                    .unwrap_or(0.0);
                let y = node
                    .attribute("y")
                    .and_then(|v| v.parse().ok())
                    .unwrap_or(0.0);
                let shift = Affine::translation([x, y]).then(ctm);
                stack.push((*target, shift, depth + 1, style));
            } else {
                warnings.push(format!("unresolved <use> reference {href:?}"));
            }
            continue;
        }
        counter += 1;
        let source = node
            .attribute("id")
            .map_or_else(|| format!("{name}-{counter}"), str::to_owned);
        let total = ctm.then(page);
        let mut pieces = vec![];
        for piece in svg_shape(&node, &source)? {
            let (start, segments) = map_segments(piece.start, &piece.segments, &total);
            pieces.push(Piece {
                start,
                segments,
                source: piece.source,
            });
        }
        if !pieces.is_empty() || matches!(name, "text" | "image" | "foreignObject") {
            let ignored = if style.hidden {
                Some("hidden SVG entity".into())
            } else if matches!(name, "text" | "image" | "foreignObject") {
                Some("not a cut outline; convert text to paths or trace the image to cut it".into())
            } else if style.color() == "none" {
                Some("SVG has no stroke or fill".into())
            } else {
                None
            };
            drawing.entities.push(DrawingEntity {
                layer: style.layer.clone(),
                color: style.color(),
                kind: name.into(),
                ignored,
                pieces,
            });
        }
        if matches!(name, "text" | "image" | "foreignObject") {
            continue;
        }
        for child in node.children().collect::<Vec<_>>().into_iter().rev() {
            stack.push((child, ctm, depth, style.clone()));
        }
    }
    drawing.finish(options, warnings, report, inspect_only)
}

impl Affine {
    pub fn translation(t: Point) -> Self {
        Self {
            m: [[1.0, 0.0], [0.0, 1.0]],
            t,
        }
    }
}

// ---------------------------------------------------------------- DXF

/// Pairs of (group code, value) from an ASCII DXF file.
fn dxf_pairs(text: &str) -> Result<Vec<(i32, &str)>> {
    let lines: Vec<&str> = text.lines().map(str::trim).collect();
    ensure!(
        lines.len().is_multiple_of(2) || lines.last() == Some(&""),
        "truncated DXF group pairs"
    );
    let mut pairs = Vec::with_capacity(lines.len() / 2);
    for chunk in lines.chunks(2) {
        if chunk.len() < 2 {
            break;
        }
        let code: i32 = chunk[0]
            .parse()
            .with_context(|| format!("invalid DXF group code {:?}", chunk[0]))?;
        pairs.push((code, chunk[1]));
    }
    Ok(pairs)
}

#[derive(Default, Clone)]
struct Entity<'a> {
    kind: &'a str,
    codes: Vec<(i32, &'a str)>,
}

impl<'a> Entity<'a> {
    fn get(&self, code: i32) -> Option<f64> {
        self.codes
            .iter()
            .find(|c| c.0 == code)
            .and_then(|c| c.1.parse().ok())
    }
    fn text(&self, code: i32) -> Option<&'a str> {
        self.codes.iter().find(|c| c.0 == code).map(|c| c.1)
    }
    fn all(&self, code: i32) -> Vec<f64> {
        self.codes
            .iter()
            .filter(|c| c.0 == code)
            .filter_map(|c| c.1.parse().ok())
            .collect()
    }
    /// Extrusion (0, 0, -1) mirrors object coordinates across Y.
    fn ocs(&self) -> Affine {
        if self.get(230).is_some_and(|z| z < 0.0) {
            Affine {
                m: [[-1.0, 0.0], [0.0, 1.0]],
                t: [0.0, 0.0],
            }
        } else {
            Affine::IDENTITY
        }
    }
}

fn bulge_segment(from: Point, to: Point, bulge: f64) -> Segment {
    if bulge.abs() < 1e-12 {
        return Segment::Line { to };
    }
    let theta = 4.0 * bulge.atan();
    let c = [to[0] - from[0], to[1] - from[1]];
    let d = c[0].hypot(c[1]);
    let h = d / (2.0 * (theta / 2.0).tan());
    let n = [-c[1] / d, c[0] / d];
    let center = [
        (from[0] + to[0]) / 2.0 + n[0] * h,
        (from[1] + to[1]) / 2.0 + n[1] * h,
    ];
    let radius = d / (2.0 * (theta / 2.0).sin().abs());
    Segment::Arc {
        center,
        radii: [radius, radius],
        rotation: 0.0,
        start: (from[1] - center[1]).atan2(from[0] - center[0]),
        sweep: theta,
    }
}

/// Exact BÃ©zier pieces of a non-rational B-spline by Boehm knot insertion.
fn bspline(degree: usize, knots: &[f64], controls: &[Point]) -> Result<(Point, Vec<Segment>)> {
    ensure!(
        (1..=3).contains(&degree),
        "spline degree {degree} is not supported"
    );
    ensure!(
        controls.len() > degree && knots.len() == controls.len() + degree + 1,
        "inconsistent spline knots and control points"
    );
    let mut knots = knots.to_vec();
    let mut points = controls.to_vec();
    let (lo, hi) = (knots[degree], knots[knots.len() - degree - 1]);
    let insert = |knots: &mut Vec<f64>, points: &mut Vec<Point>, u: f64| {
        let k = (degree..knots.len() - degree - 1)
            .rev()
            .find(|&i| knots[i] <= u)
            .unwrap_or(degree);
        let mut next = points[..=k - degree].to_vec();
        for i in k - degree + 1..=k {
            let span = knots[i + degree] - knots[i];
            let a = if span == 0.0 {
                0.0
            } else {
                (u - knots[i]) / span
            };
            let (p, q) = (points[i - 1], points[i]);
            next.push([(1.0 - a) * p[0] + a * q[0], (1.0 - a) * p[1] + a * q[1]]);
        }
        next.extend_from_slice(&points[k..]);
        *points = next;
        knots.insert(k + 1, u);
    };
    // Raise every knot of the domain [lo, hi], ends included, to multiplicity
    // `degree`; the control polygon then splits into Bézier spans.
    let mut distinct: Vec<f64> = knots
        .iter()
        .copied()
        .filter(|&k| k >= lo && k <= hi)
        .collect();
    distinct.dedup();
    ensure!(distinct.len() >= 2, "spline has an empty parameter domain");
    for &u in &distinct {
        while knots.iter().filter(|&&k| k == u).count() < degree {
            insert(&mut knots, &mut points, u);
        }
    }
    let first = knots.iter().position(|&k| k == lo).expect("lower knot");
    let multiplicity = knots.iter().filter(|&&k| k == lo).count();
    let skip = (first + multiplicity - 1)
        .checked_sub(degree)
        .context("spline start is not representable")?;
    let spans = distinct.len() - 1;
    ensure!(
        skip + spans * degree < points.len(),
        "inconsistent spline after knot insertion"
    );
    let points = &points[skip..=skip + spans * degree];
    let mut segments = vec![];
    for chunk in 0..spans {
        let p = &points[chunk * degree..=chunk * degree + degree];
        segments.push(match degree {
            1 => Segment::Line { to: p[1] },
            2 => Segment::Quad {
                control: p[1],
                to: p[2],
            },
            _ => Segment::Cubic {
                controls: [p[1], p[2]],
                to: p[3],
            },
        });
    }
    Ok((points[0], segments))
}

fn dxf_entity(e: &Entity, warnings: &mut Vec<String>) -> Result<Vec<Piece>> {
    let layer = e.text(8).unwrap_or("0").to_owned();
    let source = format!("{}:{}", layer, e.kind);
    let point = |x: i32, y: i32| -> Option<Point> { Some([e.get(x)?, e.get(y)?]) };
    let ocs = e.ocs();
    let map = |start: Point, segments: Vec<Segment>| {
        let (start, segments) = map_segments(start, &segments, &ocs);
        Piece {
            start,
            segments,
            source: source.clone(),
        }
    };
    Ok(match e.kind {
        "LINE" => {
            let (Some(a), Some(b)) = (point(10, 20), point(11, 21)) else {
                bail!("LINE without endpoints");
            };
            vec![map(a, vec![Segment::Line { to: b }])]
        }
        "CIRCLE" | "ARC" => {
            let (Some(c), Some(r)) = (point(10, 20), e.get(40)) else {
                bail!("{} without centre or radius", e.kind);
            };
            let (start, sweep) = if e.kind == "CIRCLE" {
                (0.0, TAU)
            } else {
                let a = e.get(50).unwrap_or(0.0).to_radians();
                let b = e.get(51).unwrap_or(360.0).to_radians();
                let mut sweep = (b - a).rem_euclid(TAU);
                if sweep == 0.0 {
                    sweep = TAU;
                }
                (a, sweep)
            };
            let arc = Segment::Arc {
                center: c,
                radii: [r, r],
                rotation: 0.0,
                start,
                sweep,
            };
            let begin = [c[0] + r * start.cos(), c[1] + r * start.sin()];
            vec![map(begin, vec![arc])]
        }
        "ELLIPSE" => {
            let (Some(c), Some(m), Some(ratio)) = (point(10, 20), point(11, 21), e.get(40)) else {
                bail!("ELLIPSE without centre, axis or ratio");
            };
            let start = e.get(41).unwrap_or(0.0);
            let mut sweep = (e.get(42).unwrap_or(TAU) - start).rem_euclid(TAU);
            if sweep < 1e-12 {
                sweep = TAU;
            }
            let rx = m[0].hypot(m[1]);
            let arc = Segment::Arc {
                center: c,
                radii: [rx, rx * ratio],
                rotation: m[1].atan2(m[0]),
                start,
                sweep,
            };
            let mut probe = vec![];
            let begin = {
                let s = Segment::Arc {
                    center: c,
                    radii: [rx, rx * ratio],
                    rotation: m[1].atan2(m[0]),
                    start,
                    sweep: 0.0,
                };
                s.end()
            };
            probe.push(arc);
            vec![map(begin, probe)]
        }
        "LWPOLYLINE" => {
            let closed = e.get(70).is_some_and(|f| (f as i64) & 1 == 1);
            // Vertices and optional bulges appear in order: 10, 20, [42].
            let mut vertices: Vec<(Point, f64)> = vec![];
            let mut x = None;
            for &(code, value) in &e.codes {
                match code {
                    10 => x = value.parse::<f64>().ok(),
                    20 => {
                        if let (Some(xv), Ok(y)) = (x.take(), value.parse::<f64>()) {
                            vertices.push(([xv, y], 0.0));
                        }
                    }
                    42 => {
                        if let (Some(last), Ok(b)) = (vertices.last_mut(), value.parse::<f64>()) {
                            last.1 = b;
                        }
                    }
                    _ => {}
                }
            }
            polyline(&vertices, closed).map_or(vec![], |(s, segs)| vec![map(s, segs)])
        }
        "SPLINE" => {
            let flags = e.get(70).unwrap_or(0.0) as i64;
            let degree = e.get(71).unwrap_or(3.0) as usize;
            let knots = e.all(40);
            let xs = e.all(10);
            let ys = e.all(20);
            let controls: Vec<Point> = xs.iter().zip(&ys).map(|(&x, &y)| [x, y]).collect();
            let weights = e.all(41);
            if flags & 4 != 0 && weights.iter().any(|w| (w - 1.0).abs() > 1e-12) {
                warnings.push(format!("{source}: rational spline skipped"));
                return Ok(vec![]);
            }
            if controls.is_empty() {
                let fx = e.all(11);
                let fy = e.all(21);
                ensure!(!fx.is_empty(), "SPLINE without control or fit points");
                warnings.push(format!("{source}: fit-point spline imported as a polyline"));
                let pts: Vec<Point> = fx.iter().zip(&fy).map(|(&x, &y)| [x, y]).collect();
                let segs = pts[1..].iter().map(|&to| Segment::Line { to }).collect();
                return Ok(vec![map(pts[0], segs)]);
            }
            match bspline(degree, &knots, &controls) {
                Ok((s, segs)) => vec![map(s, segs)],
                Err(err) => {
                    warnings.push(format!("{source}: {err}"));
                    vec![]
                }
            }
        }
        "POLYLINE" | "VERTEX" | "SEQEND" | "INSERT" => unreachable!("handled by the caller"),
        other => {
            if !matches!(
                other,
                "TEXT"
                    | "MTEXT"
                    | "POINT"
                    | "DIMENSION"
                    | "HATCH"
                    | "SOLID"
                    | "ATTRIB"
                    | "ATTDEF"
                    | "VIEWPORT"
            ) {
                warnings.push(format!("{source}: unsupported entity skipped"));
            }
            vec![]
        }
    })
}

fn polyline(vertices: &[(Point, f64)], closed: bool) -> Option<(Point, Vec<Segment>)> {
    if vertices.len() < 2 {
        return None;
    }
    let mut segments = vec![];
    for i in 0..vertices.len() - 1 {
        segments.push(bulge_segment(
            vertices[i].0,
            vertices[i + 1].0,
            vertices[i].1,
        ));
    }
    if closed {
        let last = vertices[vertices.len() - 1];
        segments.push(bulge_segment(last.0, vertices[0].0, last.1));
    }
    Some((vertices[0].0, segments))
}

fn dxf_entities<'a>(pairs: &[(i32, &'a str)]) -> Vec<Entity<'a>> {
    let mut entities = vec![];
    let mut current: Option<Entity> = None;
    for &(code, value) in pairs {
        if code == 0 {
            if let Some(e) = current.take() {
                entities.push(e);
            }
            current = Some(Entity {
                kind: value,
                codes: vec![],
            });
        } else if let Some(e) = current.as_mut() {
            e.codes.push((code, value));
        }
    }
    if let Some(e) = current {
        entities.push(e);
    }
    entities
}

/// Convert a flat entity list (POLYLINE/VERTEX runs and INSERTs resolved) to pieces.
struct Block<'a> {
    base: Point,
    entities: Vec<Entity<'a>>,
}

#[derive(Clone)]
struct DxfStyle {
    layer: String,
    color: String,
    hidden: bool,
}

impl Default for DxfStyle {
    fn default() -> Self {
        Self {
            layer: "0".into(),
            color: "aci:7".into(),
            hidden: false,
        }
    }
}

fn dxf_style(e: &Entity, parent: &DxfStyle, layers: &HashMap<String, DxfStyle>) -> DxfStyle {
    let own = e.text(8).unwrap_or("0");
    let layer = if own == "0" {
        parent.layer.clone()
    } else {
        own.to_owned()
    };
    let table = layers.get(&layer.to_lowercase());
    let color = if let Some(rgb) = e.get(420) {
        format!("#{:06x}", (rgb as u32) & 0xffffff)
    } else {
        match e.get(62).unwrap_or(256.0) as i32 {
            0 => parent.color.clone(),
            256 => table.map_or_else(|| "aci:7".into(), |s| s.color.clone()),
            n => format!("aci:{}", n.unsigned_abs()),
        }
    };
    DxfStyle {
        layer,
        color,
        hidden: parent.hidden
            || table.is_some_and(|l| l.hidden)
            || e.get(60) == Some(1.0)
            || e.get(62).is_some_and(|c| c < 0.0),
    }
}

#[allow(clippy::too_many_arguments)]
fn dxf_pieces(
    entities: &[Entity],
    blocks: &HashMap<String, Block>,
    transform: Affine,
    depth: u32,
    warnings: &mut Vec<String>,
    parent_style: &DxfStyle,
    layers: &HashMap<String, DxfStyle>,
    drawing: &mut Drawing,
) -> Result<()> {
    ensure!(
        depth < 16,
        "DXF block nesting is too deep; explode nested blocks in the source drawing"
    );
    let mut i = 0;
    while i < entities.len() {
        let e = &entities[i];
        let style = dxf_style(e, parent_style, layers);
        let mut pieces = vec![];
        let ignored = if style.hidden {
            Some("hidden DXF entity or layer".into())
        } else if matches!(
            e.kind,
            "TEXT"
                | "MTEXT"
                | "DIMENSION"
                | "HATCH"
                | "LEADER"
                | "MLEADER"
                | "SOLID"
                | "ATTDEF"
                | "ATTRIB"
                | "IMAGE"
        ) {
            Some("not a cut outline; explode/convert it to closed paths in the source drawing if it must be cut".into())
        } else if e.get(67) == Some(1.0) {
            Some("paper-space entity; move cut outlines to model space".into())
        } else {
            None
        };
        match e.kind {
            "POLYLINE" => {
                let closed = e.get(70).is_some_and(|f| (f as i64) & 1 == 1);
                let mut vertices = vec![];
                i += 1;
                while i < entities.len() && entities[i].kind == "VERTEX" {
                    let v = &entities[i];
                    if let (Some(x), Some(y)) = (v.get(10), v.get(20)) {
                        vertices.push(([x, y], v.get(42).unwrap_or(0.0)));
                    }
                    i += 1;
                }
                ensure!(
                    i < entities.len() && entities[i].kind == "SEQEND",
                    "POLYLINE on layer {:?} is missing its SEQEND; repair or re-export this DXF with polylines intact",
                    style.layer
                );
                if let Some((s, segs)) = polyline(&vertices, closed) {
                    let (s, segs) = map_segments(s, &segs, &e.ocs().then(transform));
                    pieces.push(Piece {
                        start: s,
                        segments: segs,
                        source: format!("{}:POLYLINE", style.layer),
                    });
                }
            }
            "SEQEND" | "VERTEX" => {
                i += 1;
                continue;
            }
            "INSERT" => {
                let name = e.text(2).unwrap_or("");
                if let Some(block) = blocks.get(name) {
                    let (sx, sy) = (e.get(41).unwrap_or(1.0), e.get(42).unwrap_or(1.0));
                    let r = e.get(50).unwrap_or(0.0).to_radians();
                    let (s, c) = r.sin_cos();
                    let at = [e.get(10).unwrap_or(0.0), e.get(20).unwrap_or(0.0)];
                    let local = Affine {
                        m: [[c * sx, -s * sy], [s * sx, c * sy]],
                        t: at,
                    };
                    dxf_pieces(
                        &block.entities,
                        blocks,
                        Affine::translation([-block.base[0], -block.base[1]])
                            .then(local)
                            .then(e.ocs())
                            .then(transform),
                        depth + 1,
                        warnings,
                        &style,
                        layers,
                        drawing,
                    )?;
                } else {
                    warnings.push(format!("unknown block {name:?} skipped"));
                }
            }
            _ => {
                for p in if ignored.is_none() {
                    dxf_entity(e, warnings)?
                } else {
                    vec![]
                } {
                    let (s, segs) = map_segments(p.start, &p.segments, &transform);
                    pieces.push(Piece {
                        start: s,
                        segments: segs,
                        source: format!("{}:{}", style.layer, e.kind),
                    });
                }
            }
        }
        drawing.entities.push(DrawingEntity {
            layer: style.layer,
            color: style.color,
            kind: e.kind.into(),
            ignored,
            pieces,
        });
        i += 1;
    }
    Ok(())
}

/// Import closed outlines from an ASCII DXF drawing (model space only).
pub fn import_dxf(text: &str, options: &Options) -> Result<Import> {
    read_dxf(text, options, false)
}

pub fn inspect_dxf(text: &str, options: &Options) -> Result<ImportReport> {
    Ok(read_dxf(text, options, true)?.report)
}

fn read_dxf(text: &str, options: &Options, inspect_only: bool) -> Result<Import> {
    let report = ImportReport::new(options)?;
    let pairs = dxf_pairs(text)?;
    let mut warnings = vec![];
    let mut unit = None;
    let mut sections: HashMap<&str, Vec<(i32, &str)>> = HashMap::new();
    let mut i = 0;
    while i + 1 < pairs.len() {
        if pairs[i] == (0, "SECTION") && pairs[i + 1].0 == 2 {
            let name = pairs[i + 1].1;
            let begin = i + 2;
            let end = (begin..pairs.len())
                .find(|&j| pairs[j] == (0, "ENDSEC"))
                .unwrap_or(pairs.len());
            sections.insert(name, pairs[begin..end].to_vec());
            i = end + 1;
        } else {
            i += 1;
        }
    }
    if let Some(header) = sections.get("HEADER")
        && let Some(pos) = header.iter().position(|p| *p == (9, "$INSUNITS"))
        && let Some(&(70, v)) = header.get(pos + 1)
    {
        unit = match v.trim() {
            "1" => Some(25.4),
            "2" => Some(304.8),
            "4" => Some(1.0),
            "5" => Some(10.0),
            "6" => Some(1000.0),
            "0" => None,
            other => {
                bail!(
                    "unsupported $INSUNITS {other}; set the source drawing to mm, cm, metres, inches or feet and re-export with its units declared"
                );
            }
        };
    }
    let scale = unit.unwrap_or_else(|| {
        warnings.push(format!(
            "no drawing units; assuming {} mm per unit",
            options.dxf_unit
        ));
        options.dxf_unit
    });
    let mut blocks = HashMap::new();
    if let Some(section) = sections.get("BLOCKS") {
        let entities = dxf_entities(section);
        let mut name = None;
        let mut base = [0.0, 0.0];
        let mut body = vec![];
        for e in entities {
            match e.kind {
                "BLOCK" => {
                    name = e.text(2).map(str::to_owned);
                    base = [e.get(10).unwrap_or(0.0), e.get(20).unwrap_or(0.0)];
                    body.clear();
                }
                "ENDBLK" => {
                    if let Some(n) = name.take() {
                        blocks.insert(
                            n,
                            Block {
                                base,
                                entities: std::mem::take(&mut body),
                            },
                        );
                    }
                }
                _ => body.push(e),
            }
        }
    }
    let entities = dxf_entities(
        sections
            .get("ENTITIES")
            .context("DXF has no ENTITIES section")?,
    );
    let mut drawing = Drawing::default();
    let mut layers = HashMap::new();
    for e in dxf_entities(sections.get("TABLES").map_or(&[], Vec::as_slice)) {
        if e.kind != "LAYER" {
            continue;
        }
        let name = e.text(2).unwrap_or("0").to_owned();
        drawing.known_layers.push(name.clone());
        layers.insert(
            name.to_lowercase(),
            DxfStyle {
                layer: name,
                color: e.get(420).map_or_else(
                    || format!("aci:{}", (e.get(62).unwrap_or(7.0) as i32).unsigned_abs()),
                    |rgb| format!("#{:06x}", (rgb as u32) & 0xffffff),
                ),
                hidden: e.get(62).is_some_and(|c| c < 0.0)
                    || e.get(70).is_some_and(|f| f as u32 & 1 != 0),
            },
        );
    }
    dxf_pieces(
        &entities,
        &blocks,
        Affine::scale(scale),
        0,
        &mut warnings,
        &DxfStyle::default(),
        &layers,
        &mut drawing,
    )?;
    let mut imported = drawing.finish(options, warnings, report, inspect_only)?;
    let extent = imported.parts.iter().map(|p| p.bounds).reduce(|a, b| {
        [
            a[0].min(b[0]),
            a[1].min(b[1]),
            a[2].max(b[2]),
            a[3].max(b[3]),
        ]
    });
    let largest = extent.map(|b| (b[2] - b[0]).max(b[3] - b[1]) / scale);
    let possible_inches = unit.is_none() && largest.is_some_and(|size| size < 60.0);
    if possible_inches {
        imported.warnings.push(format!("drawing units are missing and the largest selected dimension is {:.6} units (under 60); this may be an inches drawing. Choose inches (25.4 mm per unit) if appropriate; current scale is {scale} mm per unit. No automatic rescaling was applied",largest.unwrap()));
    }
    imported.report.units = Some(UnitReport {
        declared: unit.is_some(),
        mm_per_unit: scale,
        largest_dimension_in_drawing_units: largest,
        possible_inches,
    });
    Ok(imported)
}

#[cfg(test)]
mod tests {
    use super::*;

    /// boxes.py draws burn-relief loops that start and end on a slot corner.
    /// The nesting outline covers them; exports keep the exact curves.
    #[test]
    fn self_touching_relief_loops_get_a_covering_nesting_outline() {
        let svg = r#"<svg xmlns="http://www.w3.org/2000/svg" width="100mm" height="50mm" viewBox="0 0 100 50">
            <path id="relief" d="M 0 0 H 20 C 19.9 0 20 0.1 20 0 V 20 H 0 Z M 5 5 V 15 H 15 V 5 H 10 C 10 4.9 10.1 5 10 5 Z"/>
            <path id="outward" d="M 40 0 H 60 C 60.1 0 60 -0.1 60 0 V 20 H 40 Z"/>
        </svg>"#;
        let import = import_svg(svg, &Options::default()).unwrap();
        assert_eq!(import.parts.len(), 2, "{:?}", import.warnings);
        let identity = nestbolt_validator::RigidTransform {
            translation: [0.0, 0.0],
            rotation_radians: 0.0,
            mirrored: false,
        };
        for part in &import.parts {
            nestbolt_validator::Footprint::new(
                &part.polygon,
                nestbolt_validator::Units::Mm,
                identity,
            )
            .unwrap();
            // The exact contours keep the loops for cutting.
            assert!(
                part.outer
                    .segments
                    .iter()
                    .any(|s| matches!(s, Segment::Cubic { .. }))
            );
        }
        let relief = &import.parts[0];
        assert_eq!((relief.source.as_str(), relief.holes.len()), ("relief", 1));
        assert!((relief.area - 300.0).abs() < 0.05, "{}", relief.area);
        // An outward loop is a cut outside the square: the outline covers it.
        let outward = &import.parts[1];
        assert!(outward.bounds[2] > 60.02, "{:?}", outward.bounds);
        assert_eq!(import.warnings.len(), 2);
        assert!(
            import
                .warnings
                .iter()
                .all(|w| w.contains("touches itself") && !w.contains("skipped"))
        );
    }

    /// Collision shapes are single precision: vertices or edges that only
    /// merge there must count as touching.
    #[test]
    fn rings_must_stay_simple_in_single_precision() {
        let square = [[0.0, 0.0], [300.0, 0.0], [300.0, 200.0], [0.0, 200.0]];
        assert!(simple_in_f32(&square));
        // Two distinct vertices 1e-6 mm apart (but not neighbours) merge in f32.
        let pinch = [
            [0.0, 0.0],
            [150.0, 100.0],
            [300.0, 0.0],
            [300.0, 200.0],
            [150.000_001, 100.0],
            [0.0, 200.0],
        ];
        assert!(!simple_in_f32(&pinch));
        // A vertex 1e-6 mm from a non-adjacent edge touches it in f32 (whose
        // spacing near 150 is 1.5e-5).
        let near = [
            [0.0, 0.0],
            [300.0, 0.0],
            [300.0, 100.0],
            [150.0, 149.999_999],
            [100.0, 150.0],
            [300.0, 150.0],
            [300.0, 200.0],
            [0.0, 200.0],
        ];
        assert!(!simple_in_f32(&near));
        assert_eq!(
            thin(vec![[0.0, 0.0], [5e-5, 0.0], [10.0, 0.0], [10.0, 10.0]]).len(),
            3
        );
    }

    /// Exported DXF writes each segment as an entity: the relief SPLINE that
    /// closes on a corner must stay in its outline, not become a tiny part.
    #[test]
    fn dxf_relief_loops_in_file_order_stay_in_their_outline() {
        let line = |a: [f64; 2], b: [f64; 2]| {
            format!(
                "0\nLINE\n8\nCUT\n10\n{}\n20\n{}\n11\n{}\n21\n{}\n",
                a[0], a[1], b[0], b[1]
            )
        };
        let relief = "0\nSPLINE\n8\nCUT\n70\n8\n71\n3\n72\n8\n73\n4\n40\n0\n40\n0\n40\n0\n40\n0\n40\n1\n40\n1\n40\n1\n40\n1\n\
            10\n20\n20\n0\n10\n19.9\n20\n0\n10\n20\n20\n0.1\n10\n20\n20\n0\n";
        let dxf = format!(
            "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n{}{}{}{}{}{}0\nENDSEC\n0\nEOF\n",
            line([0.0, 0.0], [20.0, 0.0]),
            relief,
            line([20.0, 0.0], [20.0, 20.0]),
            line([20.0, 20.0], [0.0, 20.0]),
            line([0.0, 20.0], [0.0, 0.0]),
            line([40.0, 0.0], [50.0, 0.0]),
        );
        let import = import_dxf(&dxf, &Options::default()).unwrap();
        assert_eq!(import.parts.len(), 1, "{:?}", import.warnings);
        assert!((import.parts[0].area - 400.0).abs() < 0.05);
        assert!(
            import.parts[0]
                .outer
                .segments
                .iter()
                .any(|s| matches!(s, Segment::Cubic { .. }))
        );
        assert!(import.warnings.iter().any(|w| w.contains("touches itself")));
    }

    #[test]
    fn svg_frame_with_hole_and_rounded_rectangle() {
        let svg = r#"<svg xmlns="http://www.w3.org/2000/svg" width="100mm" height="50mm" viewBox="0 0 100 50">
            <path id="frame" d="M 0 0 H 60 V 40 H 0 Z M 10 10 V 30 H 50 V 10 Z"/>
            <rect id="tab" x="70" y="5" width="20" height="10" rx="2"/>
            <circle cx="80" cy="35" r="5" transform="translate(1,1)"/>
            <g transform="scale(2)"><line x1="0" y1="0" x2="5" y2="5"/></g>
        </svg>"#;
        let import = import_svg(svg, &Options::default()).unwrap();
        assert_eq!(import.parts.len(), 3);
        let frame = import.parts.iter().find(|p| p.source == "frame").unwrap();
        assert_eq!(frame.holes.len(), 1);
        assert!((frame.area - (2400.0 - 800.0)).abs() < 1e-6);
        let circle = import
            .parts
            .iter()
            .find(|p| p.holes.is_empty() && p.source != "tab")
            .unwrap();
        assert!((circle.area - PI * 25.0).abs() < 0.15);
        // Y-up: the circle centre (81, 36) in SVG maps to y = -36; polygon
        // vertices lie on the circle, so the bounds are within the tolerance.
        assert!((circle.bounds[1] + 41.0).abs() < 0.01 && (circle.bounds[0] - 76.0).abs() < 0.01);
        assert!(
            import.warnings.iter().any(|w| w.contains("open path")),
            "{:?}",
            import.warnings
        );
    }

    #[test]
    fn svg_arcs_match_the_endpoint_definition() {
        for (large, sweep) in [(false, false), (false, true), (true, false), (true, true)] {
            let s = svg_arc([0.0, 0.0], 10.0, 6.0, 30.0, large, sweep, [8.0, 3.0]);
            assert!(dist(s.end(), [8.0, 3.0]) < 1e-9);
            if let Segment::Arc { sweep: d, .. } = s {
                assert_eq!(d > 0.0, sweep);
                assert_eq!(d.abs() > PI, large);
            }
        }
    }

    #[test]
    fn dxf_lines_arcs_bulges_and_splines_close_into_parts() {
        let dxf = "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n1\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n\
            0\nLINE\n8\nCUT\n10\n0\n20\n0\n11\n2\n21\n0\n\
            0\nARC\n8\nCUT\n10\n2\n20\n1\n40\n1\n50\n270\n51\n90\n\
            0\nLINE\n8\nCUT\n10\n2\n20\n2\n11\n0\n21\n2\n\
            0\nLINE\n8\nCUT\n10\n0\n20\n2\n11\n0\n21\n0\n\
            0\nLWPOLYLINE\n8\nCUT\n90\n2\n70\n1\n10\n10\n20\n0\n42\n1\n10\n12\n20\n0\n42\n1\n\
            0\nSPLINE\n8\nCUT\n70\n8\n71\n3\n72\n8\n73\n4\n40\n0\n40\n0\n40\n0\n40\n0\n40\n1\n40\n1\n40\n1\n40\n1\n\
            10\n20\n20\n0\n10\n20\n20\n2\n10\n22\n20\n2\n10\n22\n20\n0\n\
            0\nLINE\n8\nCUT\n10\n22\n20\n0\n11\n20\n21\n0\n\
            0\nENDSEC\n0\nEOF\n";
        let import = import_dxf(dxf, &Options::default()).unwrap();
        assert_eq!(import.parts.len(), 3, "{:?}", import.warnings);
        // Inches to millimetres.
        let stadium = import.parts.iter().find(|p| p.bounds[0] < 1.0).unwrap();
        let expected = (4.0 + PI / 2.0) * 25.4 * 25.4;
        assert!((stadium.area - expected).abs() / expected < 1e-4);
        let disc = import
            .parts
            .iter()
            .find(|p| (p.bounds[0] - 254.0).abs() < 1e-6)
            .unwrap();
        // Chords sit inside the arc by at most the 0.005 mm tolerance.
        assert!((disc.area - PI * 25.4 * 25.4).abs() / (PI * 645.16) < 1e-3);
    }

    #[test]
    fn bspline_knot_insertion_reproduces_the_curve() {
        // A clamped cubic with one interior knot: compare against de Boor.
        let knots = [0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0];
        let controls = [[0.0, 0.0], [1.0, 3.0], [3.0, 4.0], [5.0, 1.0], [6.0, 0.0]];
        let (start, segments) = bspline(3, &knots, &controls).unwrap();
        assert_eq!(segments.len(), 2);
        let de_boor = |u: f64| {
            let k = if u >= 0.5 { 4 } else { 3 };
            let mut d: Vec<Point> = (0..=3).map(|j| controls[j + k - 3]).collect();
            for r in 1..=3 {
                for j in (r..=3).rev() {
                    let i = j + k - 3;
                    let a = (u - knots[i]) / (knots[i + 4 - r] - knots[i]);
                    d[j] = [
                        (1.0 - a) * d[j - 1][0] + a * d[j][0],
                        (1.0 - a) * d[j - 1][1] + a * d[j][1],
                    ];
                }
            }
            d[3]
        };
        let bezier = |p: [Point; 4], t: f64| {
            let s = 1.0 - t;
            let w = [s * s * s, 3.0 * s * s * t, 3.0 * s * t * t, t * t * t];
            [
                (0..4).map(|i| w[i] * p[i][0]).sum::<f64>(),
                (0..4).map(|i| w[i] * p[i][1]).sum::<f64>(),
            ]
        };
        let mut from = start;
        for (i, s) in segments.iter().enumerate() {
            let Segment::Cubic { controls: c, to } = s else {
                panic!("cubic")
            };
            for step in 0..=10 {
                let t = f64::from(step) / 10.0;
                let u = 0.5 * (i as f64 + t);
                let expected = de_boor(u.min(0.999_999_999));
                assert!(dist(bezier([from, c[0], c[1], *to], t), expected) < 1e-6);
            }
            from = *to;
        }
    }
}

#[cfg(test)]
mod fuzz {
    use super::*;
    use proptest::prelude::*;

    const SVG: &str = r#"<svg xmlns="http://www.w3.org/2000/svg" width="40mm" height="20mm" viewBox="0 0 40 20"><path d="M 0 0 L 10 0 A 5 5 0 0 1 10 10 Z"/><circle cx="30" cy="10" r="4"/></svg>"#;
    const DXF: &str = "0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n8\n0\n90\n3\n70\n1\n10\n0\n20\n0\n10\n5\n20\n0\n42\n0.5\n10\n5\n20\n5\n0\nENDSEC\n0\nEOF\n";

    proptest! {
        #![proptest_config(ProptestConfig::with_cases(256))]
        /// Arbitrary text must give an error or parts, never a panic.
        #[test]
        fn arbitrary_text_never_panics(text in ".{0,400}") {
            let _ = import_svg(&text, &Options::default());
            let _ = import_dxf(&text, &Options::default());
        }

        /// Truncated or byte-damaged valid files must not panic either.
        #[test]
        fn damaged_files_never_panic(cut in 0usize..400, at in 0usize..400, byte in 32u8..127) {
            for source in [SVG, DXF] {
                let mut bytes = source.as_bytes().to_vec();
                bytes.truncate(cut.min(bytes.len()));
                if !bytes.is_empty() {
                    let i = at % bytes.len();
                    bytes[i] = byte;
                }
                let text = String::from_utf8_lossy(&bytes);
                let _ = import_svg(&text, &Options::default());
                let _ = import_dxf(&text, &Options::default());
            }
        }

        /// Random path data stays finite and bounded when it imports.
        #[test]
        fn random_paths_import_finite_parts(points in proptest::collection::vec((-50.0..50.0f64, -50.0..50.0f64), 3..12)) {
            let d: String = points.iter().enumerate().map(|(i, (x, y))| {
                format!("{} {x:.3} {y:.3} ", if i == 0 { "M" } else { "L" })
            }).collect::<String>() + "Z";
            let svg = format!(r#"<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -60 120 120" width="120mm"><path d="{d}"/></svg>"#);
            if let Ok(import) = import_svg(&svg, &Options::default()) {
                for p in import.parts {
                    prop_assert!(p.area.is_finite() && p.area >= 0.0);
                    prop_assert!(p.bounds.iter().all(|v| v.is_finite() && v.abs() <= 200.0));
                }
            }
        }
    }
}
