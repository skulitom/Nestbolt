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

#[path = "support/shop_habits.rs"]
mod shop_habits;

proptest! {
    #![proptest_config(shop_habits::config(17, concat!(env!("CARGO_MANIFEST_DIR"), "/tests/search_fuzz.proptest-regressions")))]
    #[test]
    fn imported_shop_habits_nest_with_original_geometry(
        habit in 0u8..17, w in 20u32..80, h in 20u32..80,
        x in -100i32..100, y in -100i32..100, seed in any::<u64>(),
        quantity in 1u32..4, mirror in any::<bool>(),
    ) {
        let library=shop_habits::checked_library(habit,w,h,x,y,seed)?;
        let request:Request=serde_json::from_value(serde_json::json!({
            "parts":[{"id":library.parts[0].id,"quantity":quantity,
                      "rotations":{"kind":"step","degrees":90},"allow_mirror":mirror}],
            "sheets":[{"width_mm":260,"height_mm":260,
                       "margins_mm":{"left":2,"right":3,"bottom":4,"top":5}}],
            "spacing_mm":1,"edge_spacing_mm":1
        })).unwrap();
        let (job,_)=request.job(&library).unwrap();
        let result=optimize(&job,Options {seconds:0.01,time_limit:Some(10.0),seed,
            timing:Timing::Work,..Options::default()},|_,_|{})
            .map_err(|e|TestCaseError::fail(format!("feasible shop fixture: {e:#}")))?;
        prop_assert_eq!(result.layout.placements.len(),quantity as usize);
        prop_assert!(validate(&job,&result.layout).unwrap().valid);
    }
}

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

#[test]
fn regression_ci_quadtree_child_edges() {
    // Exact shrunk Linux CI case; benchmark record preserves the original seed.
    let height = 87.98196658031742;
    let parts = [
        (vec![6.657948396594396, 2.0, 2.0], 0.0, true, 2, 2, true),
        (
            vec![
                2.0,
                2.0,
                9.106484315292827,
                2.0,
                2.0,
                10.49551223083212,
                2.0,
            ],
            2.8113386683023682,
            false,
            1,
            1,
            false,
        ),
    ]
    .into_iter()
    .enumerate()
    .map(
        |(i, (radii, spike, collinear, quantity, rot, mirror))| Part {
            id: format!("p{i}"),
            quantity,
            geometry: vec![Polygon {
                outer: ring(&radii, spike, false, collinear),
                holes: vec![],
            }],
            rotations: rotations(rot),
            allow_mirror: mirror,
            priority: 1.0,
        },
    )
    .collect();
    let stocks = [("sheet", 30.0, height), ("large", 45.0, height * 1.2)]
        .into_iter()
        .map(|(id, width, height)| Stock {
            id: id.into(),
            width,
            height,
            count: None,
            margins: Margins {
                left: 1.0,
                right: 1.0,
                bottom: 1.0,
                top: 1.0,
            },
            outline: vec![],
            defects: vec![],
        })
        .collect();
    let job = Job {
        version: 1,
        name: "CI quadtree child-edge regression".into(),
        units: Units::Mm,
        clearance: 0.0,
        edge_clearance: 0.0,
        mode: Mode::All,
        parts,
        stocks,
    };
    let result = optimize(&job, options(162), |_, _| {}).unwrap();
    assert!(
        result.validation.valid,
        "{:?}",
        result.validation.violations
    );
    assert_eq!(result.layout.placements.len(), 3);
    assert!(validate(&job, &result.layout).unwrap().valid);
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(128))]

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
