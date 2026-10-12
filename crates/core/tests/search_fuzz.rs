//! G1 fuzzing of the whole sheet search: random awkward jobs (duplicate and
//! collinear points, slivers, tiny features, near-touching copies, holes, arcs
//! from SVG, several stock sizes, defects) either give an independently valid
//! layout or a clean error, and never panic.
use nestbolt_core::{
    clock::Timing,
    project::{Library, Request},
    sheets::{Options, optimize},
};
use nestbolt_validator::{
    Polygon, Units,
    job::{Job, Margins, Mode, Part, Rotations, Stock, validate},
};
use proptest::prelude::*;

fn options(seed: u64) -> Options {
    Options {
        seconds: 2.0,
        seed,
        timing: Timing::Work,
        ..Options::default()
    }
}

/// A star-like ring around the origin with optional repeated and collinear
/// vertices and very short spikes, so outlines are irregular but simple.
fn ring(radii: &[f64], spike: f64, duplicate: bool, collinear: bool) -> Vec<[f64; 2]> {
    let n = radii.len();
    let mut points = vec![];
    for (i, r) in radii.iter().enumerate() {
        let a = std::f64::consts::TAU * i as f64 / n as f64;
        let p = [r * a.cos(), r * a.sin()];
        points.push(p);
        if duplicate && i == 1 {
            points.push(p);
        }
        if collinear && i == 2 {
            let b = std::f64::consts::TAU * (i + 1) as f64 / n as f64;
            let q = [radii[(i + 1) % n] * b.cos(), radii[(i + 1) % n] * b.sin()];
            points.push([(p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0]);
        }
        if i == 0 && spike > 0.0 {
            // A thin sliver spike: a very small feature on the outline.
            points.push([p[0] + spike, p[1] + 0.01]);
        }
    }
    let shift = radii.iter().cloned().fold(0.0, f64::max) + spike + 1.0;
    points.iter().map(|[x, y]| [x + shift, y + shift]).collect()
}

fn rotations(kind: u8) -> Rotations {
    match kind % 4 {
        0 => Rotations::Free,
        1 => Rotations::Step { degrees: 90.0 },
        2 => Rotations::List {
            degrees: vec![0.0, 180.0],
        },
        _ => Rotations::Step { degrees: 15.0 },
    }
}

fn check(job: &Job, seed: u64) -> Result<(), TestCaseError> {
    match optimize(job, options(seed), |_, _| {}) {
        Ok(result) => {
            if std::env::var_os("FUZZ_TRACE").is_some() {
                eprintln!("fuzz layout {} parts", result.layout.placements.len());
            }
            prop_assert!(
                result.validation.valid,
                "{:?}",
                result.validation.violations
            );
            let again = validate(job, &result.layout).unwrap();
            prop_assert!(again.valid, "{:?}", again.violations);
        }
        // Infeasible requests (a part larger than every sheet, a capped stock
        // that cannot hold every copy) must fail cleanly with a message.
        Err(error) => {
            let message = format!("{error:#}");
            if std::env::var_os("FUZZ_TRACE").is_some() {
                eprintln!("fuzz error {message}");
            }
            prop_assert!(!message.is_empty());
        }
    }
    Ok(())
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(24))]

    #[test]
    fn random_polygon_jobs_are_valid_or_clean_errors(
        shapes in proptest::collection::vec(
            (proptest::collection::vec(2.0..12.0_f64, 3..9), 0.0..3.0_f64, any::<bool>(), any::<bool>(),
             1u32..6, 0u8..4, any::<bool>(), any::<bool>()),
            1..4),
        width in 30.0..90.0_f64,
        height in 30.0..90.0_f64,
        clearance in 0.0..1.5_f64,
        second_stock in any::<bool>(),
        capped in any::<bool>(),
        defect in any::<bool>(),
        seed in 0u64..1000,
    ) {
        let parts = shapes.iter().enumerate().map(|(i, (radii, spike, dup, col, quantity, rot, mirror, hole))| {
            let outer = ring(radii, *spike, *dup, *col);
            let r = radii.iter().cloned().fold(f64::INFINITY, f64::min);
            let c = radii.iter().cloned().fold(0.0, f64::max) + spike + 1.0;
            let holes = if *hole && r > 3.0 {
                let h = r * 0.3;
                vec![vec![[c - h, c - h], [c - h, c + h], [c + h, c + h], [c + h, c - h]]]
            } else {
                vec![]
            };
            Part {
                id: format!("p{i}"),
                quantity: *quantity,
                geometry: vec![Polygon { outer, holes }],
                rotations: rotations(*rot),
                allow_mirror: *mirror,
                priority: 1.0,
            }
        }).collect();
        let margins = Margins { left: 1.0, right: 1.0, bottom: 1.0, top: 1.0 };
        let mut stocks = vec![Stock {
            id: "sheet".into(), width, height, count: capped.then_some(2), margins,
            outline: vec![],
            defects: if defect {
                vec![Polygon { outer: vec![[width / 2.0, height / 2.0], [width / 2.0 + 3.0, height / 2.0],
                                           [width / 2.0 + 3.0, height / 2.0 + 3.0], [width / 2.0, height / 2.0 + 3.0]],
                               holes: vec![] }]
            } else { vec![] },
        }];
        if second_stock {
            stocks.push(Stock { id: "large".into(), width: width * 1.5, height: height * 1.2, count: None,
                                margins, outline: vec![], defects: vec![] });
        }
        let job = Job {
            version: 1, name: "fuzz".into(), units: Units::Mm, clearance,
            edge_clearance: clearance, mode: Mode::All, parts, stocks,
        };
        check(&job, seed)?;
    }

    #[test]
    fn random_curved_svg_parts_nest_validly(
        circles in proptest::collection::vec((1.0..15.0_f64, 0.0..0.9_f64, 1u32..5), 1..4),
        rx in 2.0..20.0_f64,
        ry in 0.5..8.0_f64,
        bulge in 0.1..10.0_f64,
        seed in 0u64..1000,
    ) {
        // Circles with off-centre holes, a thin ellipse and a lens of two arcs.
        let mut elements = String::new();
        for (i, (r, offset, _)) in circles.iter().enumerate() {
            let x = 40.0 * i as f64 + 20.0;
            let h = r * 0.3;
            elements += &format!(r#"<path id="ring{i}" fill-rule="evenodd" d="M {a} 20 A {r} {r} 0 1 0 {b} 20 A {r} {r} 0 1 0 {a} 20 Z M {c} 20 A {h} {h} 0 1 0 {d} 20 A {h} {h} 0 1 0 {c} 20 Z"/>"#,
                a = x - r, b = x + r, c = x - h + offset * (r - h) * 0.9, d = x + h + offset * (r - h) * 0.9);
        }
        elements += &format!(r#"<ellipse id="tab" cx="60" cy="70" rx="{rx}" ry="{ry}"/>"#);
        elements += &format!(r#"<path id="lens" d="M 100 70 A {bulge} {bulge} 0 0 1 112 70 A {bulge} {bulge} 0 0 1 100 70 Z"/>"#);
        let svg = format!(r#"<svg xmlns="http://www.w3.org/2000/svg" width="200mm" height="100mm" viewBox="0 0 200 100">{elements}</svg>"#);
        let library = match Library::import(&[("fuzz.svg".to_owned(), svg)], &Default::default()) {
            Ok(library) => library,
            Err(error) => {
                let message = format!("{error:#}");
                prop_assert!(!message.is_empty());
                return Ok(());
            }
        };
        let quantities: Vec<u32> = circles.iter().map(|c| c.2).collect();
        let parts: Vec<_> = library.parts.iter().enumerate().map(|(i, p)| serde_json::json!({
            "id": p.id, "quantity": quantities.get(i).copied().unwrap_or(2), "rotations": {"kind": "free"}
        })).collect();
        let request: Request = serde_json::from_value(serde_json::json!({
            "parts": parts,
            "sheets": [{"width_mm": 120, "height_mm": 80, "margins_mm": {"left": 2, "right": 2, "bottom": 2, "top": 2}}],
            "spacing_mm": 0.5, "edge_spacing_mm": 0.5
        })).unwrap();
        let (job, _) = request.job(&library).unwrap();
        check(&job, seed)?;
    }
}
