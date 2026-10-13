//! First fixed-sheet constructor. Search uses jagua; the independent checker is
//! used only for source-contract preflight and final acceptance, never placement.
//! Holed exteriors and multipart hulls are conservative collision proxies. Source
//! geometry is never rewritten. This is a starting solution, not the M2 optimiser.
use std::sync::Arc;

use crate::control::Control;
use anyhow::{Context, Result, ensure};
use jagua_rs::{
    collision_detection::{CDEConfig, hazards::filter::NoFilter},
    entities::{Container, Item, Layout as SearchLayout},
    geometry::{
        DTransformation,
        fail_fast::SPSurrogateConfig,
        geo_traits::TransformableFrom,
        primitives::{Point, SPolygon},
    },
    io::{
        ext_repr::{
            ExtContainer, ExtItem, ExtOrientation, ExtQualityZone, ExtRotation, ExtSPolygon,
            ExtShape,
        },
        import::Importer,
    },
};
use nestbolt_validator::{
    RigidTransform,
    job::{Job, Layout, Mode, Part, Placement, Rotations, Sheet, Stock},
};
use serde::Serialize;

mod repair;

#[derive(Clone, Copy, Debug)]
pub struct Options {
    pub seed: u64,
    /// Per orientation, per attempted sheet region. Deterministic work quota.
    pub random_samples: u32,
    /// Initial free-angle grid; explicit/list/step permissions remain authoritative.
    pub free_rotations: u32,
}

#[cfg(test)]
mod order_tests {
    use super::*;

    #[test]
    fn diversified_anchors_preserve_constraints_and_replay_both_allowed_orientations() {
        let mut job: Job =
            serde_json::from_str(include_str!("../../../examples/validation-job.json")).unwrap();
        job.parts.truncate(1);
        let source = serde_json::to_value(&job).unwrap();
        let prepared = PreparedJob::new(&job).unwrap();
        for right in [false, true] {
            let mut seen = [false; 2];
            for seed in 0..8 {
                let run = || {
                    prepared
                        .construct_ordered(
                            Options {
                                seed,
                                random_samples: 0,
                                ..Default::default()
                            },
                            None,
                            None,
                            Refinement::Diversified { right },
                            &mut Control::unlimited(),
                        )
                        .unwrap()
                };
                let result = run();
                assert!(
                    nestbolt_validator::job::validate(&job, &result.layout)
                        .unwrap()
                        .valid
                );
                assert_eq!(
                    serde_json::to_value(&result).unwrap(),
                    serde_json::to_value(run()).unwrap()
                );
                let transform = result.layout.placements[0].transform;
                assert!(!transform.mirrored);
                assert!(
                    transform.rotation_radians == 0.0
                        || transform.rotation_radians == std::f64::consts::PI
                );
                seen[usize::from(transform.rotation_radians > 0.0)] = true;
                let bounds = nestbolt_validator::Footprint::new(
                    &job.parts[0].geometry[0],
                    job.units,
                    transform,
                )
                .unwrap()
                .bounds();
                if right {
                    assert!(bounds[0] > 530.0 && bounds[2] < 595.0);
                } else {
                    assert!(bounds[0] > 5.0 && bounds[2] < 70.0);
                }
                assert!(bounds[1] > 5.0 && bounds[3] < 50.0);
            }
            assert!(seen.into_iter().all(|value| value));
        }
        assert_eq!(serde_json::to_value(&job).unwrap(), source);
    }

    #[test]
    fn diversified_first_orientation_keeps_trying_when_an_angle_does_not_fit() {
        let mut job: Job =
            serde_json::from_str(include_str!("../../../examples/validation-job.json")).unwrap();
        job.parts.truncate(1);
        job.parts[0].rotations = Rotations::List {
            degrees: vec![0.0, 90.0],
        };
        job.stocks[0].width = 55.0;
        job.stocks[0].height = 80.0;
        let prepared = PreparedJob::new(&job).unwrap();
        for seed in 0..8 {
            let result = prepared
                .construct_ordered(
                    Options {
                        seed,
                        random_samples: 0,
                        ..Default::default()
                    },
                    None,
                    None,
                    Refinement::Diversified {
                        right: seed % 2 == 0,
                    },
                    &mut Control::unlimited(),
                )
                .unwrap();
            assert!(
                nestbolt_validator::job::validate(&job, &result.layout)
                    .unwrap()
                    .valid
            );
            assert_eq!(
                result.layout.placements[0].transform.rotation_radians,
                std::f64::consts::FRAC_PI_2
            );
        }
    }

    #[test]
    fn interleaved_order_preserves_copy_identity_and_rejects_missing_or_duplicate_copies() {
        let mut job: Job =
            serde_json::from_str(include_str!("../../../examples/validation-job.json")).unwrap();
        for part in &mut job.parts {
            part.quantity = 2;
        }
        job.stocks[0].count = None;
        let original = serde_json::to_string(&job).unwrap();
        let prepared = PreparedJob::new(&job).unwrap();
        let order = [(2, 1), (0, 0), (1, 1), (2, 0), (1, 0), (0, 1)];
        let run = |order: &[(usize, u32)]| {
            prepared.construct_ordered(
                Options {
                    random_samples: 0,
                    ..Options::default()
                },
                Some(order),
                None,
                Refinement::Contacts,
                &mut Control::unlimited(),
            )
        };
        let result = run(&order).unwrap();
        assert!(result.complete);
        assert!(
            nestbolt_validator::job::validate(&job, &result.layout)
                .unwrap()
                .valid
        );
        let identities: Vec<_> = result
            .layout
            .placements
            .iter()
            .map(|p| (p.part_id.as_str(), p.copy_index))
            .collect();
        let expected: Vec<_> = order
            .iter()
            .map(|&(index, copy)| (job.parts[index].id.as_str(), copy))
            .collect();
        assert_eq!(identities, expected);
        assert_eq!(original, serde_json::to_string(&job).unwrap());
        for replacement in [(2, 1), (0, 2), (3, 0)] {
            let mut invalid = order;
            invalid[5] = replacement;
            assert!(run(&invalid).is_err());
        }
        assert!(run(&order[..5]).is_err());
    }
}

impl Default for Options {
    fn default() -> Self {
        Self {
            seed: 0,
            random_samples: 64,
            free_rotations: 4,
        }
    }
}

#[derive(Debug, Serialize)]
pub struct Construction {
    pub algorithm: &'static str,
    pub seed: u64,
    pub collision_checks: u64,
    pub surrogate_rejections: u64,
    pub proxy_notes: Vec<String>,
    pub complete: bool,
    pub unplaced: u32,
    pub layout: Layout,
}

/// A trial layout that failed its own original-geometry check. jagua's
/// single-precision collision tests can miss a crossing that falls exactly on
/// a vertex of both outlines (each adjacent edge test rounds just outside, and
/// neither interior point lies in the other part), so a trial may overlap.
/// Search loops discard such a trial and keep their checked incumbent.
#[derive(Debug)]
pub struct Rejected(pub String);

impl std::fmt::Display for Rejected {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for Rejected {}

/// Fail with [`Rejected`] unless every violation is an allowed unplaced copy
/// (`partial`) or there are none at all.
pub(crate) fn check_trial(
    report: &nestbolt_validator::job::Report,
    partial: bool,
    what: &str,
) -> Result<()> {
    let ok = if partial {
        report.violations.iter().all(|v| v.code == "quantity")
    } else {
        report.valid
    };
    if ok {
        Ok(())
    } else {
        Err(Rejected(format!(
            "{what} failed independent original-geometry validation: {:?}",
            report.violations
        ))
        .into())
    }
}

#[derive(Clone)]
struct Region {
    layout: SearchLayout,
    boxes: Vec<[f32; 4]>,
    contact_anchors: Vec<Point>,
    search_bounds: [f32; 4],
    nudge: f32,
}
struct OpenSheet {
    stock: usize,
    regions: Vec<Region>,
}
#[derive(Clone, Copy)]
struct Candidate {
    internal: DTransformation,
    external: RigidTransform,
    bounds: [f32; 4],
    cost: f32,
}

// A specified, platform-independent integer stream; no entropy or thread order.
struct Random(u64);
struct SearchState<'a, 'b> {
    random: Random,
    contact_random: Random,
    angle_random: Option<Random>,
    right: bool,
    contacts: bool,
    checks: u64,
    surrogate_rejections: u64,
    control: &'a mut Control<'b>,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub(crate) enum Refinement {
    None,
    Translation,
    Contacts,
    /// Later repacks vary the first feasible orientation and horizontal anchor.
    Diversified {
        right: bool,
    },
}
impl Random {
    fn unit(&mut self) -> f32 {
        self.0 = self.0.wrapping_add(0x9e3779b97f4a7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
        ((z ^ (z >> 31)) >> 40) as f32 / 16777216.0
    }
}

impl<'a, 'b> SearchState<'a, 'b> {
    fn new(seed: u64, contacts: bool, control: &'a mut Control<'b>) -> Self {
        Self {
            random: Random(seed),
            contact_random: Random(seed ^ 0xa0761d6478bd642f),
            angle_random: None,
            right: false,
            contacts,
            checks: 0,
            surrogate_rejections: 0,
            control,
        }
    }

    fn before_collision(&mut self) -> Result<()> {
        self.control.before_collision()?;
        self.checks += 1;
        Ok(())
    }

    fn cost(&self, bounds: [f32; 4]) -> f32 {
        bounds[3] + 0.001 * if self.right { -bounds[0] } else { bounds[2] }
    }
}

/// Monotone-chain hull in source f64 coordinates, before the collision copy is
/// converted to f32. This encloses every component, including their empty gaps.
fn hull(mut points: Vec<[f64; 2]>) -> Vec<[f64; 2]> {
    points.sort_by(|a, b| a[0].total_cmp(&b[0]).then(a[1].total_cmp(&b[1])));
    points.dedup();
    let cross = |a: [f64; 2], b: [f64; 2], c: [f64; 2]| {
        (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    };
    let mut result = Vec::new();
    for p in &points {
        while result.len() >= 2
            && cross(result[result.len() - 2], result[result.len() - 1], *p) <= 0.0
        {
            result.pop();
        }
        result.push(*p);
    }
    let lower = result.len();
    for p in points.iter().rev().skip(1) {
        while result.len() > lower
            && cross(result[result.len() - 2], result[result.len() - 1], *p) <= 0.0
        {
            result.pop();
        }
        result.push(*p);
    }
    result.pop();
    result
}

/// The conservative collision outline shared by every search stage: one hull
/// around multipart components, otherwise the outer contour with holes reserved.
pub(crate) fn proxy_points(part: &Part) -> Vec<[f64; 2]> {
    if part.geometry.len() > 1 {
        hull(part.geometry.iter().flat_map(|p| p.outer.clone()).collect())
    } else {
        part.geometry[0].outer.clone()
    }
}

/// Scale-dependent floating-point guard for conversion, centering, rotation and
/// source-transform reconstruction, shared by the constructor and sheet search.
pub(crate) fn conversion_guard(job: &Job) -> f64 {
    let magnitude = job
        .parts
        .iter()
        .flat_map(|p| &p.geometry)
        .flat_map(|p| &p.outer)
        .flat_map(|p| p.iter())
        .copied()
        .map(f64::abs)
        .chain(job.stocks.iter().flat_map(|s| [s.width, s.height]))
        .fold(1.0, f64::max);
    (magnitude * 32.0 * f32::EPSILON as f64).max(0.00002 / job.units.to_mm())
}

fn shape(points: &[[f64; 2]]) -> ExtShape {
    let mut points: Vec<_> = points.iter().map(|p| (p[0] as f32, p[1] as f32)).collect();
    points.dedup();
    if points.first() == points.last() {
        points.pop();
    }
    ExtShape::SimplePolygon(ExtSPolygon(points))
}

fn angles(part: &Part, options: Options) -> Result<Vec<f64>> {
    Ok(match &part.rotations {
        Rotations::Free => (0..options.free_rotations)
            .map(|i| i as f64 * 360.0 / options.free_rotations as f64)
            .collect(),
        Rotations::List { degrees } => degrees.clone(),
        Rotations::Step { degrees } => {
            let count = (360.0 / degrees).ceil();
            ensure!(
                count <= 65536.0,
                "rotation step needs more than 65,536 candidates"
            );
            (0..count as u32).map(|i| i as f64 * degrees).collect()
        }
    })
}

fn container_regions(stock: &Stock, index: usize, importer: &Importer) -> Result<Vec<Container>> {
    let mut zones: Vec<_> = stock
        .defects
        .iter()
        .map(|p| ExtQualityZone {
            quality: 0,
            shape: shape(&p.outer),
        })
        .collect();
    let m = stock.margins;
    for (x, y, w, h) in [
        (0.0, 0.0, m.left, stock.height),
        (stock.width - m.right, 0.0, m.right, stock.height),
        (0.0, 0.0, stock.width, m.bottom),
        (0.0, stock.height - m.top, stock.width, m.top),
    ] {
        if w > 0.0 && h > 0.0 {
            zones.push(ExtQualityZone {
                quality: 0,
                shape: ExtShape::Rectangle {
                    x_min: x as f32,
                    y_min: y as f32,
                    width: w as f32,
                    height: h as f32,
                },
            });
        }
    }
    let outer = if stock.outline.is_empty() {
        vec![(
            ExtShape::Rectangle {
                x_min: 0.0,
                y_min: 0.0,
                width: stock.width as f32,
                height: stock.height as f32,
            },
            vec![],
        )]
    } else {
        stock
            .outline
            .iter()
            .map(|p| {
                (
                    shape(&p.outer),
                    p.holes
                        .iter()
                        .map(|h| ExtQualityZone {
                            quality: 0,
                            shape: shape(h),
                        })
                        .collect::<Vec<_>>(),
                )
            })
            .collect()
    };
    outer
        .into_iter()
        .map(|(shape, holes)| {
            let mut zones = zones.clone();
            zones.extend(holes);
            // A region's CDE must not receive hazards wholly outside its root.
            // Other remnant islands share the physical sheet, not this tree.
            let boundary = shape_bounds(&shape);
            zones.retain(|z| {
                let b = shape_bounds(&z.shape);
                b[0] < boundary[2] && b[2] > boundary[0] && b[1] < boundary[3] && b[3] > boundary[1]
            });
            importer.import_container(&ExtContainer {
                id: index as u64,
                shape,
                zones,
            })
        })
        .collect()
}

fn shape_bounds(shape: &ExtShape) -> [f32; 4] {
    match shape {
        ExtShape::Rectangle {
            x_min,
            y_min,
            width,
            height,
        } => [*x_min, *y_min, x_min + width, y_min + height],
        ExtShape::SimplePolygon(points) => points.0.iter().fold(
            [
                f32::INFINITY,
                f32::INFINITY,
                f32::NEG_INFINITY,
                f32::NEG_INFINITY,
            ],
            |b, p| [b[0].min(p.0), b[1].min(p.1), b[2].max(p.0), b[3].max(p.1)],
        ),
        _ => unreachable!("constructor supplies only rectangles and simple zones"),
    }
}

/// Candidate contacts between sampled vertices of the inflated collision shapes.
/// This finds interlocking positions with overlapping bounding boxes. Sampling
/// is capped regardless of polygon complexity and has its own integer stream,
/// so it never consumes the ordinary random-placement quota.
fn contact_positions(region: &Region, oriented: &SPolygon, random: &mut Random) -> Vec<(f32, f32)> {
    let incoming = contact_anchors(oriented);
    let placed = &region.contact_anchors;
    let pair_limit = if region.boxes.len() <= 4 { 1024 } else { 256 };
    let pairs = incoming.len() * placed.len();
    let count = pairs.min(pair_limit);
    let b = oriented.bbox();
    let n = region.nudge * 2.0;
    let mut positions = Vec::with_capacity(count * 8);
    for i in 0..count {
        let index = if pairs <= pair_limit {
            i
        } else {
            // One sample from each stratum includes every part of the list.
            (((i as f64 + f64::from(random.unit())) * pairs as f64 / count as f64) as usize)
                .min(pairs - 1)
        };
        let a = incoming[index % incoming.len()];
        let p = placed[index / incoming.len()];
        let x = p.0 - a.0 + b.x_min;
        let y = p.1 - a.1 + b.y_min;
        for (dx, dy) in [
            (n, 0.0),
            (-n, 0.0),
            (0.0, n),
            (0.0, -n),
            (n, n),
            (n, -n),
            (-n, n),
            (-n, -n),
        ] {
            positions.push((x + dx, y + dy));
        }
    }
    positions
}

fn contact_anchors(shape: &SPolygon) -> Vec<Point> {
    let v = shape.vertices();
    let b = shape.bbox();
    // Virtual bounding corners cover a rectangular insert meeting a concave
    // corner: coinciding two rounded vertices alone can still cross both walls.
    let mut anchors = vec![
        Point(b.x_min, b.y_min),
        Point(b.x_max, b.y_min),
        Point(b.x_min, b.y_max),
        Point(b.x_max, b.y_max),
    ];
    let orientation = v
        .iter()
        .zip(v.iter().cycle().skip(1))
        .take(v.len())
        .map(|(a, b)| a.0 * b.1 - a.1 * b.0)
        .sum::<f32>()
        .signum();
    let concave: Vec<_> = (0..v.len())
        .filter(|&i| {
            let a = v[(i + v.len() - 1) % v.len()];
            let p = v[i];
            let b = v[(i + 1) % v.len()];
            let x = (p.0 - a.0, p.1 - a.1);
            let y = (b.0 - p.0, b.1 - p.1);
            let scale = (x.0 * x.0 + x.1 * x.1).sqrt() * (y.0 * y.0 + y.1 * y.1).sqrt();
            (x.0 * y.1 - x.1 * y.0) * orientation < -0.000001 * scale
        })
        .map(|i| v[i])
        .collect();
    let count = concave.len().min(16);
    anchors.extend((0..count).map(|i| concave[i * concave.len() / count]));
    let count = v.len().min(16);
    anchors.extend((0..count).map(|i| v[i * v.len() / count]));
    anchors
}

fn search(
    region: &Region,
    item: &Item,
    part: &Part,
    options: Options,
    state: &mut SearchState<'_, '_>,
) -> Result<Option<Candidate>> {
    search_bounded(region, item, part, options, state, None)
}

/// A relocation need not test positions that cannot improve its incumbent.
/// Generate random candidates first so pruning does not change the stream.
fn search_bounded(
    region: &Region,
    item: &Item,
    part: &Part,
    options: Options,
    state: &mut SearchState<'_, '_>,
    ceiling: Option<(f32, f32)>, // strict cost ceiling, inclusive top edge
) -> Result<Option<Candidate>> {
    let cde = region.layout.cde();
    let sheet = region.search_bounds;
    let nudge = region.nudge;
    let mut buffer = item.shape_cd().as_ref().clone();
    let mut best: Option<Candidate> = None;
    let mut orientations = angles(part, options)?;
    if let Some(random) = &mut state.angle_random {
        for index in (1..orientations.len()).rev() {
            let other = (random.unit() * (index + 1) as f32) as usize;
            orientations.swap(index, other);
        }
    }
    for degrees in orientations {
        state.control.checkpoint()?;
        let angle = degrees.to_radians();
        for mirrored in [false, true]
            .into_iter()
            .take(if part.allow_mirror { 2 } else { 1 })
        {
            // jagua reflects X; original contract reflects Y. Keep the exact
            // allowed f64 angle for output, rather than round-tripping f32 trig.
            let rotation = (angle + if mirrored { std::f64::consts::PI } else { 0.0 }) as f32;
            let base = DTransformation::new(rotation, (0.0, 0.0)).with_reflection(mirrored);
            buffer.transform_from(item.shape_cd(), &base.compose());
            let bounds = buffer.bbox();
            let width = bounds.x_max - bounds.x_min;
            let height = bounds.y_max - bounds.y_min;
            let min_x = sheet[0] + nudge;
            let min_y = sheet[1] + nudge;
            let max_x = sheet[2] - width - nudge;
            let max_y = sheet[3] - height - nudge;
            if min_x > max_x || min_y > max_y {
                continue;
            }
            let mut positions = vec![(min_x, min_y), (max_x, min_y), (min_x, max_y)];
            for b in &region.boxes {
                positions.extend([
                    (b[2] + nudge, min_y),
                    (min_x, b[3] + nudge),
                    (b[2] + nudge, b[1]),
                    (b[0], b[3] + nudge),
                ]);
                if state.right {
                    positions.extend([
                        (b[0] - width - nudge, min_y),
                        (max_x, b[3] + nudge),
                        (b[0] - width - nudge, b[1]),
                        (b[2] - width, b[3] + nudge),
                    ]);
                }
            }
            if state.contacts {
                positions.extend(contact_positions(
                    region,
                    &buffer,
                    &mut state.contact_random,
                ));
            }
            positions.extend((0..options.random_samples).map(|_| {
                (
                    min_x + state.random.unit() * (max_x - min_x),
                    min_y + state.random.unit() * (max_y - min_y),
                )
            }));
            // Generate the complete random stream before pruning. Stable cost
            // order preserves the original first-candidate tie rule, but lets
            // us stop at the cheapest feasible placement for this orientation.
            let mut ranked: Vec<_> = positions
                .into_iter()
                .filter(|&(x, y)| x >= min_x && y >= min_y && x <= max_x && y <= max_y)
                .map(|(x, y)| (x, y, state.cost([x, y, x + width, y + height])))
                .filter(|&(_, y, cost)| {
                    ceiling
                        .is_none_or(|(max_cost, max_top)| cost < max_cost && y + height <= max_top)
                })
                .collect();
            ranked.sort_by(|a, b| a.2.total_cmp(&b.2));
            ranked.dedup_by(|a, b| a.0 == b.0 && a.1 == b.1);
            for (x, y, cost) in ranked {
                if best.as_ref().is_some_and(|b| cost >= b.cost) {
                    break;
                }
                let internal = DTransformation::new(rotation, (x - bounds.x_min, y - bounds.y_min))
                    .with_reflection(mirrored);
                state.before_collision()?;
                let transform = internal.compose();
                if cde.detect_surrogate_collision(
                    item.shape_cd().surrogate(),
                    &transform,
                    &NoFilter,
                ) {
                    state.surrogate_rejections += 1;
                    continue;
                }
                buffer.transform_from(item.shape_cd(), &transform);
                if cde.detect_poly_collision(&buffer, &NoFilter) {
                    continue;
                }
                let (cx, cy) = item.shape_orig().pre_transform.translation();
                let (tx, ty) = internal.translation();
                let (s, c) = angle.sin_cos();
                let cx = f64::from(cx) * if mirrored { -1.0 } else { 1.0 };
                let cy = f64::from(cy);
                best = Some(Candidate {
                    internal,
                    external: RigidTransform {
                        translation: [
                            f64::from(tx) + c * cx - s * cy,
                            f64::from(ty) + s * cx + c * cy,
                        ],
                        rotation_radians: angle,
                        mirrored,
                    },
                    bounds: [x, y, x + width, y + height],
                    cost,
                });
                break;
            }
        }
        // At an empty region, keep the first feasible shuffled orientation.
        // Otherwise small trig rounding differences would consistently select
        // the same angle again. Later parts still compare every allowed angle.
        if state.angle_random.is_some() && region.boxes.is_empty() && best.is_some() {
            break;
        }
    }
    Ok(best)
}

/// A bounded pattern search from a known feasible position. It only translates;
/// exact list/step angles and reflection permissions stay unchanged. Each level
/// halves the step and admits at most 16 improvements, so even tiny source units
/// cannot turn refinement into an unbounded loop.
fn refine_translation(
    region: &Region,
    item: &Item,
    mut candidate: Candidate,
    state: &mut SearchState<'_, '_>,
) -> Result<Candidate> {
    let cde = region.layout.cde();
    let mut buffer = item.shape_cd().as_ref().clone();
    let mut step_x = (candidate.bounds[2] - candidate.bounds[0]) / 4.0;
    let mut step_y = (candidate.bounds[3] - candidate.bounds[1]) / 4.0;
    let limits = region.search_bounds;
    for _ in 0..10 {
        state.control.checkpoint()?;
        if step_x.max(step_y) < region.nudge {
            break;
        }
        for _ in 0..16 {
            let mut moved = false;
            for (mut dx, dy) in [
                (0.0, -step_y),
                (-step_x, 0.0),
                (-step_x, -step_y),
                (step_x, -step_y),
                (2.0 * step_x, -step_y),
                (4.0 * step_x, -step_y),
                (step_x, -2.0 * step_y),
                (step_x, -4.0 * step_y),
            ] {
                if state.right {
                    dx = -dx;
                }
                let old = candidate.internal.translation();
                let translation = (old.0 + dx, old.1 + dy);
                if translation == old {
                    continue;
                }
                let transform = DTransformation::new(candidate.internal.rotation(), translation)
                    .with_reflection(candidate.external.mirrored);
                let composed = transform.compose();
                buffer.transform_from(item.shape_cd(), &composed);
                let b = buffer.bbox();
                let cost = state.cost([b.x_min, b.y_min, b.x_max, b.y_max]);
                if cost >= candidate.cost
                    || b.x_min < limits[0] + region.nudge
                    || b.y_min < limits[1] + region.nudge
                    || b.x_max > limits[2] - region.nudge
                    || b.y_max > limits[3] - region.nudge
                {
                    continue;
                }
                state.before_collision()?;
                if cde.detect_surrogate_collision(item.shape_cd().surrogate(), &composed, &NoFilter)
                {
                    state.surrogate_rejections += 1;
                    continue;
                }
                if cde.detect_poly_collision(&buffer, &NoFilter) {
                    continue;
                }
                // Match the actual rounded internal displacement in f64. Using
                // the requested step would accumulate source/proxy drift.
                candidate.external.translation[0] += f64::from(translation.0) - f64::from(old.0);
                candidate.external.translation[1] += f64::from(translation.1) - f64::from(old.1);
                candidate.internal = transform;
                candidate.bounds = [b.x_min, b.y_min, b.x_max, b.y_max];
                candidate.cost = cost;
                moved = true;
                break;
            }
            if !moved {
                break;
            }
        }
        step_x *= 0.5;
        step_y *= 0.5;
    }
    Ok(candidate)
}

/// A deterministic constructive candidate. A failed construction does not prove
/// infeasibility: filled holes/hulls and a finite placement search lose options.
pub fn construct(job: &Job, options: Options) -> Result<Construction> {
    PreparedJob::new(job)?.construct(options)
}

/// Geometry prepared once for construction, repair and repeated search passes.
/// Only search state is recreated; source polygons and collision proxies persist.
pub struct PreparedJob<'a> {
    job: &'a Job,
    items: Vec<Arc<Item>>,
    containers: Vec<Vec<Container>>,
    guard: f64,
    separation: f64,
    notes: Vec<String>,
}

impl<'a> PreparedJob<'a> {
    pub fn new(job: &'a Job) -> Result<Self> {
        Self::new_controlled(job, &mut Control::unlimited())
    }

    pub(crate) fn new_controlled(job: &'a Job, control: &mut Control<'_>) -> Result<Self> {
        control.checkpoint()?;
        let layout = Layout {
            version: 1,
            units: job.units,
            sheets: vec![],
            placements: vec![],
        };
        // Existing independent model owns schema validation until public job types
        // are extracted. Collision decisions below never call that checker.
        let preflight = nestbolt_validator::job::validate(job, &layout)?;
        ensure!(
            preflight.violations.iter().all(|v| v.code == "quantity"),
            "invalid source job"
        );
        // Final validity is still checked independently.
        let guard = conversion_guard(job);
        // jagua uses 0.1-radian inscribed round joins. Compensate their chord
        // deficit as well as f32 rounding before allowing contact placements.
        let separation = (job.clearance.max(job.edge_clearance) + guard) / 0.05_f64.cos();
        let importer = Importer::new(
            CDEConfig {
                quadtree_depth: 5,
                cd_threshold: 96,
                item_surrogate_config: SPSurrogateConfig {
                    n_pole_limits: [(1, 0.0), (1, 0.75), (1, 0.90)],
                    ff_pole_area_ratio: 1.0,
                    n_ff_piers: 0,
                },
            },
            None,
            None,
        )
        .with_min_item_separation(separation as f32)?;
        let mut notes = vec![format!(
            "Conservative separation {separation}; requested part gap {}, edge gap {}. No placement inside holes yet.",
            job.clearance, job.edge_clearance
        )];
        let mut items: Vec<Arc<Item>> = Vec::new();
        for (index, part) in job.parts.iter().enumerate() {
            control.checkpoint()?;
            let multipart = part.geometry.len() > 1;
            let points = proxy_points(part);
            if multipart || part.geometry.iter().any(|p| !p.holes.is_empty()) {
                notes.push(format!(
                    "{}: {}",
                    part.id,
                    if multipart {
                        "one hull around all rigid components"
                    } else {
                        "outer contour with holes reserved"
                    }
                ));
            }
            let external = ExtItem {
                id: index as u64,
                shape: shape(&points),
                orientation: ExtOrientation {
                    rotation: ExtRotation::Continuous {},
                    reflection_axes: vec![90.0],
                },
                min_quality: None,
            };
            items.push(
                importer
                    .import_item(&external, index)
                    .with_context(|| format!("collision proxy for {}", part.id))?,
            );
        }
        let containers: Vec<_> = job
            .stocks
            .iter()
            .enumerate()
            .map(|(i, s)| {
                control.checkpoint()?;
                container_regions(s, i, &importer)
            })
            .collect::<Result<_>>()?;
        Ok(Self {
            job,
            items,
            containers,
            guard,
            separation,
            notes,
        })
    }

    pub fn construct(&self, options: Options) -> Result<Construction> {
        self.construct_ordered(
            options,
            None,
            None,
            Refinement::None,
            &mut Control::unlimited(),
        )
    }

    /// Construct with bounded translation refinement of each feasible placement.
    pub fn construct_refined(&self, options: Options) -> Result<Construction> {
        self.construct_ordered(
            options,
            None,
            None,
            Refinement::Translation,
            &mut Control::unlimited(),
        )
    }

    /// Include bounded outline-contact candidates before refining translations.
    pub fn construct_with_contacts(&self, options: Options) -> Result<Construction> {
        self.construct_ordered(
            options,
            None,
            None,
            Refinement::Contacts,
            &mut Control::unlimited(),
        )
    }

    fn open_sheet(&self, stock: usize) -> OpenSheet {
        OpenSheet {
            stock,
            regions: self.containers[stock]
                .iter()
                .cloned()
                .map(|c| {
                    let b = c.outer_cd().bbox();
                    let s = &self.job.stocks[stock];
                    let half = self.separation / 2.0;
                    Region {
                        nudge: self.guard as f32,
                        search_bounds: [
                            b.x_min.max((s.margins.left + half) as f32),
                            b.y_min.max((s.margins.bottom + half) as f32),
                            b.x_max.min((s.width - s.margins.right - half) as f32),
                            b.y_max.min((s.height - s.margins.top - half) as f32),
                        ],
                        layout: SearchLayout::new(c),
                        boxes: vec![],
                        contact_anchors: vec![],
                    }
                })
                .collect(),
        }
    }

    pub(crate) fn construct_ordered(
        &self,
        options: Options,
        copy_order: Option<&[(usize, u32)]>,
        max_sheets: Option<usize>,
        refinement: Refinement,
        control: &mut Control<'_>,
    ) -> Result<Construction> {
        ensure!(
            (1..=360).contains(&options.free_rotations) && options.random_samples <= 100_000,
            "invalid construction work budget"
        );
        let job = self.job;
        let items = &self.items;
        let mut layout = Layout {
            version: 1,
            units: job.units,
            sheets: vec![],
            placements: vec![],
        };
        let mut order: Vec<_> = (0..items.len()).collect();
        order.sort_by(|&a, &b| {
            let priority = if job.mode == Mode::FillPriority {
                job.parts[b].priority.total_cmp(&job.parts[a].priority)
            } else {
                std::cmp::Ordering::Equal
            };
            priority
                .then(items[b].area().total_cmp(&items[a].area()))
                .then(a.cmp(&b))
        });
        let mut copies: Vec<_> = order
            .into_iter()
            .flat_map(|index| (0..job.parts[index].quantity).map(move |copy| (index, copy)))
            .collect();
        if let Some(requested) = copy_order {
            let unique: std::collections::BTreeSet<_> = requested.iter().copied().collect();
            ensure!(
                requested.len() == copies.len()
                    && unique.len() == copies.len()
                    && unique.iter().all(|&(index, copy)| {
                        job.parts
                            .get(index)
                            .is_some_and(|part| copy < part.quantity)
                    }),
                "search order must contain every requested part copy exactly once"
            );
            copies = requested.to_vec();
        }
        let mut stock_order: Vec<_> = (0..job.stocks.len()).collect();
        stock_order.sort_by(|&a, &b| {
            (job.stocks[a].width * job.stocks[a].height)
                .total_cmp(&(job.stocks[b].width * job.stocks[b].height))
                .then(a.cmp(&b))
        });
        let mut open: Vec<OpenSheet> = vec![];
        let mut stock_used = vec![0_u32; job.stocks.len()];
        let contacts = matches!(
            refinement,
            Refinement::Contacts | Refinement::Diversified { .. }
        );
        let mut state = SearchState::new(options.seed, contacts, control);
        if let Refinement::Diversified { right } = refinement {
            state.right = right;
            state.angle_random = Some(Random(options.seed ^ 0xe7037ed1a0b428db));
        }
        for (index, copy) in copies {
            state.control.checkpoint()?;
            let mut found = None;
            for (sheet_index, sheet) in open.iter().enumerate() {
                for (region_index, region) in sheet.regions.iter().enumerate() {
                    if let Some(candidate) = search(
                        region,
                        &items[index],
                        &job.parts[index],
                        options,
                        &mut state,
                    )? {
                        found = Some((sheet_index, region_index, candidate));
                        break;
                    }
                }
                if found.is_some() {
                    break;
                }
            }
            if found.is_none() && max_sheets.is_none_or(|limit| open.len() < limit) {
                for &stock in &stock_order {
                    if job.stocks[stock]
                        .count
                        .is_some_and(|limit| stock_used[stock] >= limit)
                    {
                        continue;
                    }
                    let sheet = self.open_sheet(stock);
                    for (region_index, region) in sheet.regions.iter().enumerate() {
                        if let Some(candidate) = search(
                            region,
                            &items[index],
                            &job.parts[index],
                            options,
                            &mut state,
                        )? {
                            found = Some((open.len(), region_index, candidate));
                            break;
                        }
                    }
                    if found.is_some() {
                        layout.sheets.push(Sheet {
                            id: format!("sheet-{}", open.len()),
                            stock_id: job.stocks[stock].id.clone(),
                        });
                        stock_used[stock] += 1;
                        open.push(sheet);
                        break;
                    }
                }
            }
            if let Some((sheet, region, mut candidate)) = found {
                let active = &mut open[sheet].regions[region];
                if refinement != Refinement::None {
                    candidate = refine_translation(active, &items[index], candidate, &mut state)?;
                }
                let key = active.layout.place_item(&items[index], candidate.internal);
                if contacts {
                    active
                        .contact_anchors
                        .extend(contact_anchors(active.layout.placed_items()[key].shape()));
                }
                active.boxes.push(candidate.bounds);
                layout.placements.push(Placement {
                    part_id: job.parts[index].id.clone(),
                    copy_index: copy,
                    sheet_id: layout.sheets[sheet].id.clone(),
                    transform: candidate.external,
                });
            } else if max_sheets.is_some() && job.mode == Mode::All {
                // A capped reconstruction does not retry missing copies. Stop
                // this failed sheet-removal trial; fill mode must keep looking
                // for later parts that may still fit.
                break;
            }
        }
        let unplaced =
            job.parts.iter().map(|p| p.quantity).sum::<u32>() - layout.placements.len() as u32;
        let final_check = nestbolt_validator::job::validate(job, &layout)?;
        check_trial(&final_check, true, "construction")?;
        // Keep stock identity checked here as well as in the final independent pass.
        debug_assert!(
            open.iter()
                .enumerate()
                .all(|(i, s)| layout.sheets[i].stock_id == job.stocks[s.stock].id)
        );
        Ok(Construction {
            algorithm: match refinement {
                Refinement::None => "nestbolt-construct-v3",
                Refinement::Translation => "nestbolt-construct-refined-v1",
                Refinement::Contacts => "nestbolt-construct-refined-v2",
                Refinement::Diversified { .. } => "nestbolt-construct-diverse-v1",
            },
            seed: options.seed,
            collision_checks: state.checks,
            surrogate_rejections: state.surrogate_rejections,
            proxy_notes: self.notes.clone(),
            complete: unplaced == 0 || job.mode != Mode::All,
            unplaced,
            layout,
        })
    }
}
