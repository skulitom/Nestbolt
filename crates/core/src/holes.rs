//! Part-in-part: small parts placed inside the holes of larger parts before the
//! sheet search. Each filled host copy becomes a rigid group whose collision
//! proxy is still the host's outer contour, so nothing else can reach its
//! holes; the riders keep the part clearance to the hole edges and to each
//! other. Rider rotations stay valid for every rotation the host may take, and
//! a group may be mirrored only if every member may. Layouts of the grouped job
//! expand back to the original parts and are independently checked there.
use std::collections::HashMap;
use std::sync::Arc;

use anyhow::{Context, Result};
use jagua_rs::{
    entities::{Item, Layout as JLayout},
    geometry::DTransformation,
    io::{
        ext_repr::{ExtContainer, ExtItem, ExtOrientation, ExtRotation, ExtSPolygon, ExtShape},
        import::Importer,
    },
};
use nestbolt_validator::{
    RigidTransform,
    job::{Job, Layout, Mode, Part, Placement, Rotations, Stock, validate},
};
use rand::{SeedableRng, rngs::Xoshiro256PlusPlus};
use sparrow::{
    config::DEFAULT_SPARROW_CONFIG,
    consts::LBF_SAMPLE_CONFIG,
    eval::{lbf_evaluator::LBFEvaluator, sample_eval::SampleEval},
    sample::search::search_placement,
};

use crate::clock::Clock;
use crate::construct::{conversion_guard, proxy_points};
use crate::curves::Affine;

/// A rider's collision proxy and its relative rotations (`None` is free).
type RiderItem = (Arc<Item>, Option<Vec<f64>>);

/// A rider: an original part placed in a host's local frame.
#[derive(Clone, Debug)]
struct Rider {
    part: usize,
    transform: RigidTransform,
}

/// What one part of the grouped job stands for.
#[derive(Clone, Debug)]
struct Member {
    host: usize,
    riders: Vec<Rider>,
}

/// A job whose filled hosts are rigid groups, and how to expand its layouts.
pub struct Grouped {
    pub job: Job,
    members: Vec<Member>,
    pub riders_placed: u32,
}

fn angle_set(rotations: &Rotations) -> Option<Vec<f64>> {
    match rotations {
        Rotations::Free => None,
        Rotations::List { degrees } => Some(degrees.iter().map(|d| d.rem_euclid(360.0)).collect()),
        Rotations::Step { degrees } => Some(
            (0..(360.0 / degrees).ceil() as u32)
                .map(|i| (f64::from(i) * degrees).rem_euclid(360.0))
                .collect(),
        ),
    }
}

fn has(set: &[f64], angle: f64) -> bool {
    let a = angle.rem_euclid(360.0);
    set.iter().any(|&b| {
        let d = (a - b).abs();
        d.min(360.0 - d) < 1e-9
    })
}

/// Relative rider rotations valid for every host rotation, with and without
/// a host mirror (which negates the relative rotation). `None` means free.
fn relative_rotations(host: &Part, rider: &Part) -> Option<Option<Vec<f64>>> {
    let r = angle_set(&rider.rotations);
    match (angle_set(&host.rotations), r) {
        (_, None) => Some(None),
        (None, Some(_)) => None,
        (Some(h), Some(r)) => {
            let valid: Vec<f64> = r
                .iter()
                .copied()
                .filter(|&phi| {
                    h.iter()
                        .all(|&t| has(&r, t + phi) && (!host.allow_mirror || has(&r, t - phi)))
                })
                .collect();
            (!valid.is_empty()).then_some(Some(valid))
        }
    }
}

fn shape(points: &[[f64; 2]]) -> ExtShape {
    let mut p: Vec<(f32, f32)> = points.iter().map(|q| (q[0] as f32, q[1] as f32)).collect();
    p.dedup();
    if p.len() > 1 && p.first() == p.last() {
        p.pop();
    }
    ExtShape::SimplePolygon(ExtSPolygon(p))
}

/// Contract transform of a jagua placement of an item imported without a
/// frame change (holes live in the host's own coordinates).
fn contract(item: &Item, dt: &DTransformation, allowed: Option<&[f64]>) -> RigidTransform {
    let (px, py) = item.shape_orig().pre_transform.translation();
    let pre = Affine::translation([f64::from(px), f64::from(py)]);
    let (s, c) = f64::from(dt.rotation()).sin_cos();
    let (x, y) = dt.translation();
    let jagua = Affine {
        m: if dt.reflected {
            [[c, s], [s, -c]]
        } else {
            [[c, -s], [s, c]]
        },
        t: [f64::from(x), f64::from(y)],
    };
    decompose(&pre.then(jagua), allowed)
}

fn decompose(g: &Affine, allowed: Option<&[f64]>) -> RigidTransform {
    let mirrored = g.determinant() < 0.0;
    let mut angle = if mirrored {
        (-g.m[1][0]).atan2(-g.m[0][0])
    } else {
        g.m[1][0].atan2(g.m[0][0])
    }
    .to_degrees()
    .rem_euclid(360.0);
    if let Some(set) = allowed
        && let Some(&exact) = set.iter().min_by(|a, b| {
            let d = |v: f64| (v - angle).abs().min(360.0 - (v - angle).abs());
            d(**a).total_cmp(&d(**b))
        })
        && (exact - angle).abs().min(360.0 - (exact - angle).abs()) < 1e-4
    {
        angle = exact;
    }
    RigidTransform {
        translation: g.t,
        rotation_radians: angle.to_radians(),
        mirrored,
    }
}

/// Fill the holes of host parts with smaller parts, largest first. Returns the
/// original job unchanged (as one-member groups) when nothing fits or the job
/// asks for fill mode. `until` bounds the whole pre-pass.
pub fn group(job: &Job, clock: &Clock, until: f64, seed: u64) -> Result<Grouped> {
    let plain = || Grouped {
        job: job.clone(),
        members: (0..job.parts.len())
            .map(|host| Member {
                host,
                riders: vec![],
            })
            .collect(),
        riders_placed: 0,
    };
    if job.mode != Mode::All
        || !job
            .parts
            .iter()
            .any(|p| p.geometry.len() == 1 && !p.geometry[0].holes.is_empty())
    {
        return Ok(plain());
    }
    let guard = conversion_guard(job);
    let separation = ((job.clearance + guard) / 0.05_f64.cos()) as f32;
    let importer = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None)
        .with_min_item_separation(separation)?;
    let mut rng = Xoshiro256PlusPlus::seed_from_u64(seed);
    let mut remaining: Vec<u32> = job.parts.iter().map(|p| p.quantity).collect();
    // Item proxies per (host, rider) pair, keyed by the allowed relative set.
    let mut items: HashMap<(usize, usize), Option<RiderItem>> = HashMap::new();
    let area = |p: &Part| {
        let g = &p.geometry[0];
        crate::curves::signed_area(&g.outer).abs()
    };
    let mut order: Vec<usize> = (0..job.parts.len()).collect();
    order.sort_by(|&a, &b| area(&job.parts[b]).total_cmp(&area(&job.parts[a])));
    let mut members = vec![];
    let mut patterns: Vec<(usize, Vec<Rider>, u32)> = vec![];
    for &host in &order {
        let part = &job.parts[host];
        if part.geometry.len() != 1 || part.geometry[0].holes.is_empty() {
            continue;
        }
        // Fill one host copy at a time; identical consecutive patterns merge.
        // The first copy of each host is always tried, however late: on a slow
        // or busy machine a short budget could otherwise end the pre-pass before
        // any rider, and a sheet that fits only the filled host has no layout.
        let mut first = true;
        while remaining[host] > 0 && (first || clock.now() < until) {
            let forced = std::mem::replace(&mut first, false);
            // Another copy of the same host takes the last checked pattern
            // again while its riders last: same group, no new search.
            if let Some((h, pattern, n)) = patterns.last_mut()
                && *h == host
                && (0..job.parts.len()).all(|part| {
                    pattern.iter().filter(|r| r.part == part).count() as u32 <= remaining[part]
                })
            {
                for r in pattern.iter() {
                    remaining[r.part] -= 1;
                }
                remaining[host] -= 1;
                *n += 1;
                continue;
            }
            let mut riders = vec![];
            for hole in &part.geometry[0].holes {
                let container = importer.import_container(&ExtContainer {
                    id: 0,
                    shape: shape(hole),
                    zones: vec![],
                });
                let Ok(container) = container else {
                    continue;
                };
                let hole_area = crate::curves::signed_area(hole).abs();
                let mut layout = JLayout::new(container);
                for &rider in &order {
                    if rider == host || area(&job.parts[rider]) >= hole_area {
                        continue;
                    }
                    let entry = items.entry((host, rider)).or_insert_with(|| {
                        let r = &job.parts[rider];
                        let rel = relative_rotations(part, r)?;
                        let rotation = match &rel {
                            None => ExtRotation::Continuous {},
                            Some(v) => ExtRotation::Discrete {
                                angles: v.iter().map(|&d| d as f32).collect(),
                            },
                        };
                        let item = importer
                            .import_item(
                                &ExtItem {
                                    id: rider as u64,
                                    shape: shape(&proxy_points(r)),
                                    orientation: ExtOrientation {
                                        rotation,
                                        reflection_axes: vec![],
                                    },
                                    min_quality: None,
                                },
                                0,
                            )
                            .ok()?;
                        Some((item, rel))
                    });
                    let Some((item, rel)) = entry.clone() else {
                        continue;
                    };
                    let available = |riders: &Vec<Rider>| {
                        remaining[rider]
                            > riders.iter().filter(|r| r.part == rider).count() as u32
                                + u32::from(rider == host)
                    };
                    while available(&riders) && (forced || clock.now() < until) {
                        let (sample, evals) = search_placement(
                            &layout,
                            &item,
                            None,
                            LBFEvaluator::new(&layout, &item),
                            LBF_SAMPLE_CONFIG,
                            &mut rng,
                        );
                        crate::separate::charge(clock, &item, evals);
                        let Some((dt, SampleEval::Clear { .. })) = sample else {
                            break;
                        };
                        layout.place_item(&item, dt);
                        riders.push(Rider {
                            part: rider,
                            transform: contract(&item, &dt, rel.as_deref()),
                        });
                    }
                }
            }
            if riders.is_empty() {
                break;
            }
            // Confirm the group independently before using it.
            if !pattern_valid(job, host, &riders, clock)? {
                break;
            }
            for r in &riders {
                remaining[r.part] -= 1;
            }
            remaining[host] -= 1;
            match patterns.last_mut() {
                Some((h, p, n)) if *h == host && same(p, &riders) => *n += 1,
                _ => patterns.push((host, riders, 1)),
            }
        }
    }
    if patterns.is_empty() {
        return Ok(plain());
    }
    let mut parts = vec![];
    let mut placed = 0;
    for (index, part) in job.parts.iter().enumerate() {
        if remaining[index] > 0 {
            let mut p = part.clone();
            p.quantity = remaining[index];
            parts.push(p);
            members.push(Member {
                host: index,
                riders: vec![],
            });
        }
    }
    for (k, (host, riders, count)) in patterns.into_iter().enumerate() {
        let mut p = job.parts[host].clone();
        p.id = format!("{}+riders-{}", p.id, k + 1);
        p.quantity = count;
        p.allow_mirror = p.allow_mirror && riders.iter().all(|r| job.parts[r.part].allow_mirror);
        placed += riders.len() as u32 * count;
        parts.push(p);
        members.push(Member { host, riders });
    }
    let mut grouped = job.clone();
    grouped.parts = parts;
    Ok(Grouped {
        job: grouped,
        members,
        riders_placed: placed,
    })
}

fn same(a: &[Rider], b: &[Rider]) -> bool {
    a.len() == b.len()
        && a.iter().zip(b).all(|(x, y)| {
            x.part == y.part
                && x.transform.mirrored == y.transform.mirrored
                && (x.transform.rotation_radians - y.transform.rotation_radians).abs() < 1e-12
                && (0..2)
                    .all(|i| (x.transform.translation[i] - y.transform.translation[i]).abs() < 1e-9)
        })
}

/// Check a host with its riders on an ample sheet with the original rules.
fn pattern_valid(job: &Job, host: usize, riders: &[Rider], clock: &Clock) -> Result<bool> {
    let mut probe = job.clone();
    probe.mode = Mode::FillArea;
    let extent = job
        .parts
        .iter()
        .flat_map(|p| &p.geometry)
        .flat_map(|g| &g.outer)
        .map(|q| q[0].abs().max(q[1].abs()))
        .fold(1.0, f64::max);
    probe.stocks = vec![Stock {
        id: "probe".into(),
        width: extent * 8.0,
        height: extent * 8.0,
        count: Some(1),
        margins: Default::default(),
        outline: vec![],
        defects: vec![],
    }];
    let at = [extent * 4.0, extent * 4.0];
    let host_t = RigidTransform {
        translation: at,
        rotation_radians: 0.0,
        mirrored: false,
    };
    let mut layout = Layout {
        version: 1,
        units: job.units,
        sheets: vec![nestbolt_validator::job::Sheet {
            id: "probe".into(),
            stock_id: "probe".into(),
        }],
        placements: vec![Placement {
            part_id: job.parts[host].id.clone(),
            copy_index: 0,
            sheet_id: "probe".into(),
            transform: host_t,
        }],
    };
    let mut copies: HashMap<usize, u32> = HashMap::from([(host, 1)]);
    for r in riders {
        let copy = copies.entry(r.part).or_insert(0);
        layout.placements.push(Placement {
            part_id: job.parts[r.part].id.clone(),
            copy_index: *copy,
            sheet_id: "probe".into(),
            transform: compose(&host_t, &r.transform, &job.parts[r.part].rotations),
        });
        *copy += 1;
    }
    clock.validated(&probe, &layout);
    Ok(validate(&probe, &layout)?.valid)
}

fn compose(host: &RigidTransform, rider: &RigidTransform, rotations: &Rotations) -> RigidTransform {
    let g = Affine::placement(rider).then(Affine::placement(host));
    decompose(&g, angle_set(rotations).as_deref())
}

impl Grouped {
    /// Expand a layout of the grouped job into one of the original job.
    pub fn expand(&self, original: &Job, layout: &Layout) -> Result<Layout> {
        let index: HashMap<&str, usize> = self
            .job
            .parts
            .iter()
            .enumerate()
            .map(|(i, p)| (p.id.as_str(), i))
            .collect();
        let mut copies = vec![0_u32; original.parts.len()];
        let mut placements = vec![];
        for p in &layout.placements {
            let member = &self.members[*index
                .get(p.part_id.as_str())
                .with_context(|| format!("unknown grouped part {}", p.part_id))?];
            let mut push = |part: usize, transform: RigidTransform| {
                placements.push(Placement {
                    part_id: original.parts[part].id.clone(),
                    copy_index: copies[part],
                    sheet_id: p.sheet_id.clone(),
                    transform,
                });
                copies[part] += 1;
            };
            push(member.host, p.transform);
            for r in &member.riders {
                push(
                    r.part,
                    compose(
                        &p.transform,
                        &r.transform,
                        &original.parts[r.part].rotations,
                    ),
                );
            }
        }
        Ok(Layout {
            version: layout.version,
            units: layout.units,
            sheets: layout.sheets.clone(),
            placements,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn inserts_ride_inside_frames_and_expand_validly() {
        let mut job: Job =
            serde_json::from_str(include_str!("../../../examples/validation-job.json")).unwrap();
        job.parts.iter_mut().for_each(|p| p.quantity *= 3);
        let clock = Clock::new(crate::clock::Timing::Wall, 10.0);
        let grouped = group(&job, &clock, 10.0, 0).unwrap();
        assert!(grouped.riders_placed > 0);
        let original: u32 = job.parts.iter().map(|p| p.quantity).sum();
        let left: u32 = grouped.job.parts.iter().map(|p| p.quantity).sum();
        assert_eq!(left + grouped.riders_placed, original);
        let construction = crate::construct::construct(&grouped.job, Default::default()).unwrap();
        assert!(construction.complete);
        let expanded = grouped.expand(&job, &construction.layout).unwrap();
        let report = validate(&job, &expanded).unwrap();
        assert!(report.valid, "{:?}", report.violations);
    }

    #[test]
    fn the_first_host_is_filled_even_when_the_share_has_run_out() {
        // Found by the browser tests on a busy CI runner: a 3 s budget, the
        // pre-pass deadline already past, and a sheet only the filled frame fits.
        let job: Job =
            serde_json::from_str(include_str!("../../../examples/validation-job.json")).unwrap();
        let clock = Clock::new(crate::clock::Timing::Wall, 10.0);
        let grouped = group(&job, &clock, 0.0, 0).unwrap();
        assert!(grouped.riders_placed > 0);
    }
}
