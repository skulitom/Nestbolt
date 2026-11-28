//! jagua-rs 2.0 removes short edges from every polygon it builds, including
//! its own inflated and deflated outlines. With a separation near the
//! floating-point guard, the 1.1.0 formula left corner arcs collapsed and the
//! original outline touching its collision outline (found on `b-blaz1`, whose
//! trial layouts then failed independent validation). These tests measure the
//! margin jagua actually keeps at the separation Nestbolt requests.
use super::*;
use jagua_rs::geometry::primitives::SPolygon;
use jagua_rs::io::ext_repr::ExtContainer;
use nestbolt_validator::{
    Polygon, Units,
    job::{Margins, rectangle},
};
use sparrow::config::DEFAULT_SPARROW_CONFIG;

type P = [f64; 2];

fn point_segment(p: P, a: P, b: P) -> f64 {
    let (dx, dy) = (b[0] - a[0], b[1] - a[1]);
    let length = dx * dx + dy * dy;
    let t = if length == 0.0 {
        0.0
    } else {
        (((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / length).clamp(0.0, 1.0)
    };
    (p[0] - a[0] - t * dx).hypot(p[1] - a[1] - t * dy)
}

fn crosses(a: P, b: P, c: P, d: P) -> bool {
    let side = |p: P, q: P, r: P| (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]);
    side(a, b, c) * side(a, b, d) < 0.0 && side(c, d, a) * side(c, d, b) < 0.0
}

fn edges(points: &[P]) -> impl Iterator<Item = (P, P)> + '_ {
    (0..points.len()).map(|i| (points[i], points[(i + 1) % points.len()]))
}

/// Smallest distance between the two boundaries; zero when they cross.
fn boundary_gap(first: &[P], second: &[P]) -> f64 {
    let mut gap = f64::MAX;
    for (a, b) in edges(first) {
        for (c, d) in edges(second) {
            if crosses(a, b, c, d) {
                return 0.0;
            }
            gap = gap
                .min(point_segment(a, c, d))
                .min(point_segment(b, c, d))
                .min(point_segment(c, a, b))
                .min(point_segment(d, a, b));
        }
    }
    gap
}

fn contains(polygon: &[P], p: P) -> bool {
    edges(polygon)
        .filter(|&(a, b)| {
            (a[1] > p[1]) != (b[1] > p[1])
                && p[0] < a[0] + (p[1] - a[1]) / (b[1] - a[1]) * (b[0] - a[0])
        })
        .count()
        % 2
        == 1
}

fn points(shape: &SPolygon) -> Vec<P> {
    shape
        .vertices()
        .iter()
        .map(|p| [f64::from(p.0), f64::from(p.1)])
        .collect()
}

fn circle(radius: f64, sides: usize) -> Polygon {
    Polygon {
        outer: (0..sides)
            .map(|i| {
                let angle = std::f64::consts::TAU * i as f64 / sides as f64;
                [radius * angle.cos(), radius * angle.sin()]
            })
            .collect(),
        holes: vec![],
    }
}

fn outline(points: &[P]) -> Polygon {
    Polygon {
        outer: points.to_vec(),
        holes: vec![],
    }
}

fn job(units: Units, clearance: f64, sheet: (f64, f64), parts: Vec<Polygon>) -> Job {
    Job {
        version: 1,
        name: "separation test".into(),
        units,
        parts: parts
            .into_iter()
            .enumerate()
            .map(|(i, geometry)| Part {
                id: format!("p{i}"),
                quantity: 1,
                geometry: vec![geometry],
                rotations: Rotations::Free,
                allow_mirror: false,
                priority: 1.0,
            })
            .collect(),
        stocks: vec![Stock {
            id: "sheet".into(),
            width: sheet.0,
            height: sheet.1,
            count: None,
            margins: Margins::default(),
            outline: vec![],
            defects: vec![],
        }],
        clearance,
        edge_clearance: clearance,
        mode: Mode::All,
    }
}

fn jobs() -> Vec<Job> {
    // The scale and zero spacing of the Blazewicz benchmark.
    let small = vec![
        outline(&[
            [0.0, 0.0],
            [4.0, 0.0],
            [4.0, 1.0],
            [1.0, 1.0],
            [1.0, 3.0],
            [0.0, 3.0],
        ]),
        outline(&[[0.0, 0.0], [3.0, 0.0], [0.0, 0.4]]),
        circle(1.0, 48),
    ];
    let shop = || {
        vec![
            outline(&[
                [0.0, 0.0],
                [60.0, 0.0],
                [60.0, 15.0],
                [20.0, 15.0],
                [20.0, 40.0],
                [0.0, 40.0],
            ]),
            outline(&[[0.0, 0.0], [100.0, 0.0], [0.0, 8.0]]),
            circle(25.0, 64),
            circle(25.0, 720),
            outline(&[
                [0.0, 0.0],
                [880.0, 0.0],
                [900.0, 20.0],
                [900.0, 600.0],
                [0.0, 600.0],
            ]),
        ]
    };
    vec![
        job(Units::Unitless, 0.0, (7.5, 7.5), small),
        job(Units::Mm, 0.0, (2440.0, 1220.0), shop()),
        job(Units::Mm, 0.05, (2440.0, 1220.0), shop()),
        job(Units::Mm, 1.5, (2440.0, 1220.0), shop()),
        job(Units::Mm, 3.0, (10000.0, 1500.0), shop()),
    ]
}

/// The margin every collision outline must keep, less the share of the guard
/// that covers measuring single-precision vertices here.
fn required_margin(job: &Job, required: f64) -> f64 {
    let guard = conversion_guard(job);
    (required + guard) / 2.0 - guard / 8.0
}

#[test]
fn part_collision_outlines_keep_half_the_spacing_and_guard() {
    for job in jobs() {
        let prepared = PreparedJob::new(&job).unwrap();
        let needed = required_margin(&job, job.clearance.max(job.edge_clearance));
        for (part, item) in job.parts.iter().zip(&prepared.items) {
            let (dx, dy) = item.shape_orig().pre_transform.translation();
            let original: Vec<P> = part.geometry[0]
                .outer
                .iter()
                .map(|p| [p[0] + f64::from(dx), p[1] + f64::from(dy)])
                .collect();
            let inflated = points(item.shape_cd());
            assert!(
                original.iter().all(|&p| contains(&inflated, p)),
                "{} {}: outline leaves its collision outline",
                job.clearance,
                part.id
            );
            let margin = boundary_gap(&inflated, &original);
            assert!(
                margin >= needed,
                "{} {}: margin {margin} below {needed}",
                job.clearance,
                part.id
            );
        }
    }
}

#[test]
fn sheet_walls_and_end_blockers_keep_half_the_spacing_and_guard() {
    for job in jobs() {
        let stock = &job.stocks[0];
        let separation = engine_separation(&job, job.clearance);
        let needed = required_margin(&job, job.clearance);
        let importer = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None)
            .with_min_item_separation(separation as f32)
            .unwrap();
        // A wall between sheets and an end blocker, the stock-scale rectangles
        // the sheet search adds, at both extremes of their proportions.
        for (width, height) in [
            (stock.height * 1e-3, stock.height),
            (stock.width * 0.4, stock.height * 0.98),
            (stock.width, stock.height * 1e-3),
        ] {
            let original = rectangle(0.0, 0.0, width, height).outer;
            let item = importer
                .import_item(
                    &ExtItem {
                        id: 0,
                        shape: shape(&original),
                        orientation: ExtOrientation {
                            rotation: ExtRotation::Discrete { angles: vec![0.0] },
                            reflection_axes: vec![],
                        },
                        min_quality: None,
                    },
                    0,
                )
                .unwrap();
            let (dx, dy) = item.shape_orig().pre_transform.translation();
            let original: Vec<P> = original
                .iter()
                .map(|p| [p[0] + f64::from(dx), p[1] + f64::from(dy)])
                .collect();
            let inflated = points(item.shape_cd());
            assert!(original.iter().all(|&p| contains(&inflated, p)));
            let margin = boundary_gap(&inflated, &original);
            assert!(
                margin >= needed,
                "{} {width} x {height}: margin {margin} below {needed}",
                job.clearance
            );
        }
    }
}

#[test]
fn drawn_stock_outlines_keep_half_the_spacing_and_guard() {
    // A remnant with a reflex corner, whose deflated outline gets a corner arc.
    let remnant = [
        [0.0, 0.0],
        [700.0, 0.0],
        [700.0, 200.0],
        [300.0, 200.0],
        [300.0, 500.0],
        [0.0, 500.0],
    ];
    for clearance in [0.0, 0.05, 1.0] {
        let mut job = job(Units::Mm, clearance, (700.0, 500.0), vec![circle(25.0, 64)]);
        job.stocks[0].outline = vec![outline(&remnant)];
        let separation = engine_separation(&job, clearance);
        let needed = required_margin(&job, clearance);
        let container = Importer::new(DEFAULT_SPARROW_CONFIG.cde_config, None, None)
            .with_min_item_separation(separation as f32)
            .unwrap()
            .import_container(&ExtContainer {
                id: 0,
                shape: shape(&remnant),
                zones: vec![],
            })
            .unwrap();
        let deflated = points(container.outer_cd());
        assert!(deflated.iter().all(|&p| contains(&remnant, p)));
        let margin = boundary_gap(&deflated, &remnant);
        assert!(
            margin >= needed,
            "{clearance}: margin {margin} below {needed}"
        );
    }
}

#[test]
fn ordinary_shop_spacing_grows_by_microns_only() {
    // 1.5 mm spacing on a full sheet: the 1.1.0 separation was 1.5114 mm.
    let job = &jobs()[3];
    let before = (job.clearance + conversion_guard(job)) / 0.05_f64.cos();
    let after = engine_separation(job, job.clearance);
    assert!(after >= before && after - before < 0.05, "{before} {after}");
}
