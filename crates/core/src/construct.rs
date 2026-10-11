//! First fixed-sheet constructor. Search uses jagua; the independent checker is
//! used only for source-contract preflight and final acceptance, never placement.
//! Holed exteriors and multipart hulls are conservative collision proxies. Source
//! geometry is never rewritten. This is a starting solution, not the M2 optimiser.
use std::sync::Arc;

use anyhow::{Context, Result, ensure};
use jagua_rs::{
    collision_detection::{CDEConfig, hazards::filter::NoFilter},
    entities::{Container, Item, Layout as SearchLayout},
    geometry::{DTransformation, fail_fast::SPSurrogateConfig, geo_traits::TransformableFrom},
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

#[derive(Clone, Copy, Debug)]
pub struct Options {
    pub seed: u64,
    /// Per orientation, per attempted sheet region. Deterministic work quota.
    pub random_samples: u32,
    /// Initial free-angle grid; explicit/list/step permissions remain authoritative.
    pub free_rotations: u32,
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
    pub proxy_notes: Vec<String>,
    pub complete: bool,
    pub unplaced: u32,
    pub layout: Layout,
}

struct Region {
    layout: SearchLayout,
    boxes: Vec<[f32; 4]>,
    search_bounds: [f32; 4],
    nudge: f32,
}
struct OpenSheet {
    stock: usize,
    regions: Vec<Region>,
}
struct Candidate {
    internal: DTransformation,
    external: RigidTransform,
    bounds: [f32; 4],
    cost: f32,
}

// A specified, platform-independent integer stream; no entropy or thread order.
struct Random(u64);
impl Random {
    fn unit(&mut self) -> f32 {
        self.0 = self.0.wrapping_add(0x9e3779b97f4a7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
        ((z ^ (z >> 31)) >> 40) as f32 / 16777216.0
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

fn search(
    region: &Region,
    item: &Item,
    part: &Part,
    options: Options,
    random: &mut Random,
    checks: &mut u64,
) -> Result<Option<Candidate>> {
    let cde = region.layout.cde();
    let sheet = region.search_bounds;
    let nudge = region.nudge;
    let mut buffer = item.shape_cd().as_ref().clone();
    let mut best: Option<Candidate> = None;
    for degrees in angles(part, options)? {
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
            }
            positions.extend((0..options.random_samples).map(|_| {
                (
                    min_x + random.unit() * (max_x - min_x),
                    min_y + random.unit() * (max_y - min_y),
                )
            }));
            for (x, y) in positions {
                if x < min_x || y < min_y || x > max_x || y > max_y {
                    continue;
                }
                let cost = y + height + 0.001 * (x + width);
                if best.as_ref().is_some_and(|b| cost >= b.cost) {
                    continue;
                }
                let internal = DTransformation::new(rotation, (x - bounds.x_min, y - bounds.y_min))
                    .with_reflection(mirrored);
                buffer.transform_from(item.shape_cd(), &internal.compose());
                *checks += 1;
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
            }
        }
    }
    Ok(best)
}

/// A deterministic constructive candidate. A failed construction does not prove
/// infeasibility: filled holes/hulls and a finite placement search lose options.
pub fn construct(job: &Job, options: Options) -> Result<Construction> {
    ensure!(
        (1..=360).contains(&options.free_rotations) && options.random_samples <= 100_000,
        "invalid construction work budget"
    );
    let mut layout = Layout {
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
    // Reserve a scale-dependent floating-point guard for conversion, centering,
    // rotation and source-transform reconstruction. Final validity is checked.
    let guard = (magnitude * 32.0 * f32::EPSILON as f64).max(0.00002 / job.units.to_mm());
    // jagua uses 0.1-radian inscribed round joins. Compensate their chord
    // deficit as well as f32 rounding before allowing contact placements.
    let separation = (job.clearance.max(job.edge_clearance) + guard) / 0.05_f64.cos();
    let importer = Importer::new(
        CDEConfig {
            quadtree_depth: 5,
            cd_threshold: 96,
            item_surrogate_config: SPSurrogateConfig::none(),
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
        let multipart = part.geometry.len() > 1;
        let points = if multipart {
            hull(part.geometry.iter().flat_map(|p| p.outer.clone()).collect())
        } else {
            part.geometry[0].outer.clone()
        };
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
        .map(|(i, s)| container_regions(s, i, &importer))
        .collect::<Result<_>>()?;
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
    let mut stock_order: Vec<_> = (0..job.stocks.len()).collect();
    stock_order.sort_by(|&a, &b| {
        (job.stocks[a].width * job.stocks[a].height)
            .total_cmp(&(job.stocks[b].width * job.stocks[b].height))
            .then(a.cmp(&b))
    });
    let mut open: Vec<OpenSheet> = vec![];
    let mut stock_used = vec![0_u32; job.stocks.len()];
    let mut random = Random(options.seed);
    let mut checks = 0;
    for index in order {
        for copy in 0..job.parts[index].quantity {
            let mut found = None;
            for (sheet_index, sheet) in open.iter().enumerate() {
                for (region_index, region) in sheet.regions.iter().enumerate() {
                    if let Some(candidate) = search(
                        region,
                        &items[index],
                        &job.parts[index],
                        options,
                        &mut random,
                        &mut checks,
                    )? {
                        found = Some((sheet_index, region_index, candidate));
                        break;
                    }
                }
                if found.is_some() {
                    break;
                }
            }
            if found.is_none() {
                for &stock in &stock_order {
                    if job.stocks[stock]
                        .count
                        .is_some_and(|limit| stock_used[stock] >= limit)
                    {
                        continue;
                    }
                    let sheet = OpenSheet {
                        stock,
                        regions: containers[stock]
                            .iter()
                            .cloned()
                            .map(|c| {
                                // CDE's tree uses an inflated square, not the
                                // usable sheet extent. Anchor to the actual
                                // contour and margin-zone offsets instead.
                                let b = c.outer_cd().bbox();
                                let s = &job.stocks[stock];
                                let half = separation / 2.0;
                                Region {
                                    nudge: guard as f32,
                                    search_bounds: [
                                        b.x_min.max((s.margins.left + half) as f32),
                                        b.y_min.max((s.margins.bottom + half) as f32),
                                        b.x_max.min((s.width - s.margins.right - half) as f32),
                                        b.y_max.min((s.height - s.margins.top - half) as f32),
                                    ],
                                    layout: SearchLayout::new(c),
                                    boxes: vec![],
                                }
                            })
                            .collect(),
                    };
                    for (region_index, region) in sheet.regions.iter().enumerate() {
                        if let Some(candidate) = search(
                            region,
                            &items[index],
                            &job.parts[index],
                            options,
                            &mut random,
                            &mut checks,
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
            if let Some((sheet, region, candidate)) = found {
                let active = &mut open[sheet].regions[region];
                active.layout.place_item(&items[index], candidate.internal);
                active.boxes.push(candidate.bounds);
                layout.placements.push(Placement {
                    part_id: job.parts[index].id.clone(),
                    copy_index: copy,
                    sheet_id: layout.sheets[sheet].id.clone(),
                    transform: candidate.external,
                });
            }
        }
    }
    let unplaced =
        job.parts.iter().map(|p| p.quantity).sum::<u32>() - layout.placements.len() as u32;
    let final_check = nestbolt_validator::job::validate(job, &layout)?;
    ensure!(
        final_check.violations.iter().all(|v| v.code == "quantity"),
        "construction failed independent original-geometry validation: {:?}",
        final_check.violations
    );
    // Keep stock identity checked here as well as in the final independent pass.
    debug_assert!(
        open.iter()
            .enumerate()
            .all(|(i, s)| layout.sheets[i].stock_id == job.stocks[s.stock].id)
    );
    Ok(Construction {
        algorithm: "nestbolt-construct-v2",
        seed: options.seed,
        collision_checks: checks,
        proxy_notes: notes,
        complete: unplaced == 0 || job.mode != Mode::All,
        unplaced,
        layout,
    })
}
