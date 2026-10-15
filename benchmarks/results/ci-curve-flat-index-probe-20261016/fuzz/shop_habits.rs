//! Analytic, independently authored DXFs covering the N0 generator's 17 habits.
//! No corpus geometry or labels are loaded. Expectations come from a rectangle
//! with a circular hole, or a cubic cap whose area is 3*w*d/5.
use nestbolt_core::{import::Options, project::Library};
use proptest::prelude::*;

pub const HABITS: [&str; 17] = [
    "exploded-shuffled",
    "gap-0.001",
    "gap-0.05",
    "gap-0.5",
    "overlap-0.001",
    "overlap-0.5",
    "duplicates-zero",
    "fusion-splines-extrusion",
    "bulges-widths",
    "nested-mirrored-blocks",
    "single-block-insert",
    "missing-header-inches",
    "missing-units-inches",
    "centimetres",
    "annotations-construction",
    "operation-colours",
    "existing-nest",
];

pub fn config(default_cases: u32, regression_file: &'static str) -> ProptestConfig {
    // An explicit override avoids with_cases silently masking PROPTEST_CASES.
    let cases = std::env::var("NESTBOLT_HABIT_CASES")
        .map(|s| s.parse::<u32>().expect("positive NESTBOLT_HABIT_CASES"))
        .unwrap_or(default_cases);
    assert!(cases > 0);
    ProptestConfig {
        cases,
        failure_persistence: Some(Box::new(
            proptest::test_runner::FileFailurePersistence::Direct(regression_file),
        )),
        ..ProptestConfig::default()
    }
}

fn line(a: [f64; 2], b: [f64; 2], layer: &str, scale: f64) -> String {
    format!(
        "0\nLINE\n8\n{layer}\n10\n{}\n20\n{}\n11\n{}\n21\n{}\n",
        a[0] / scale,
        a[1] / scale,
        b[0] / scale,
        b[1] / scale
    )
}

fn poly(points: &[[f64; 2]], layer: &str, scale: f64, width: f64) -> String {
    let mut s = format!(
        "0\nLWPOLYLINE\n8\n{layer}\n90\n{}\n70\n1\n43\n{width}\n",
        points.len()
    );
    for p in points {
        s += &format!("10\n{}\n20\n{}\n", p[0] / scale, p[1] / scale);
    }
    s
}

pub fn checked_library(
    habit: u8,
    w: u32,
    h: u32,
    x: i32,
    y: i32,
    seed: u64,
) -> Result<Library, TestCaseError> {
    let habit = habit as usize;
    let name = HABITS[habit];
    let (w, h, tx, ty) = (w as f64, h as f64, x as f64, y as f64);
    let scale = match habit {
        11 | 12 => 25.4,
        13 => 10.0,
        _ => 1.0,
    };
    let (ox, oy) = if habit == 9 || habit == 10 {
        (3.0, 7.0)
    } else {
        (tx, ty)
    };
    let p = [[ox, oy], [ox + w, oy], [ox + w, oy + h], [ox, oy + h]];
    let radius = w.min(h) / 8.0;
    let cx = ox + w * 0.4;
    let cy = oy + h * 0.6;
    let layer = if habit == 15 {
        "OP"
    } else if habit == 9 || habit == 10 {
        "0"
    } else {
        "CUT"
    };
    let mut edges = vec![(p[0], p[1]), (p[1], p[2]), (p[2], p[3]), (p[3], p[0])];
    let mut options = Options {
        dxf_unit: scale,
        ..Options::default()
    };
    if (1..=5).contains(&habit) {
        let gap = match habit {
            1 => 0.001,
            2 => 0.05,
            3 => 0.5,
            4 => -0.001,
            _ => -0.5,
        };
        edges[0] = (p[0], [ox + w / 2.0, oy]);
        edges.push(([ox + w / 2.0 + gap, oy], p[1]));
        if gap > 0.005 {
            options.close_gaps_mm = Some(gap + 1e-8);
        }
    }
    if habit == 6 {
        edges.extend([(p[1], p[0]), (p[0], p[0])]);
    }
    let cap = if habit == 7 { h / 5.0 } else { 0.0 };
    if habit == 7 {
        edges.remove(2);
    }
    let mut state = seed;
    for i in (1..edges.len()).rev() {
        state = state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        edges.swap(i, state as usize % (i + 1));
        if state & 128 != 0 {
            edges[i] = (edges[i].1, edges[i].0);
        }
    }
    let mut body = if habit == 8 {
        poly(&p, layer, scale, 0.8)
    } else {
        edges
            .iter()
            .map(|(a, b)| line(*a, *b, layer, scale))
            .collect::<String>()
    };
    if habit == 7 {
        body += &format!(
            "0\nSPLINE\n8\n{layer}\n70\n8\n71\n3\n72\n8\n73\n4\n40\n0\n40\n0\n40\n0\n40\n0\n40\n1\n40\n1\n40\n1\n40\n1\n"
        );
        for q in [p[2], [ox + w, oy + h + cap], [ox, oy + h + cap], p[3]] {
            body += &format!("10\n{}\n20\n{}\n30\n0\n", q[0], q[1]);
        }
        for (a, b) in [(0, 180), (180, 360)] {
            body += &format!(
                "0\nARC\n8\n{layer}\n10\n{}\n20\n{cy}\n40\n{radius}\n50\n{a}\n51\n{b}\n210\n0\n220\n0\n230\n-1\n",
                -cx
            );
        }
    } else if habit == 8 {
        body += &format!(
            "0\nLWPOLYLINE\n8\n{layer}\n90\n2\n70\n1\n43\n0.3\n10\n{}\n20\n{cy}\n42\n1\n10\n{}\n20\n{cy}\n42\n1\n",
            cx - radius,
            cx + radius
        );
    } else {
        body += &format!(
            "0\nCIRCLE\n8\n{layer}\n10\n{}\n20\n{}\n40\n{}\n",
            cx / scale,
            cy / scale,
            radius / scale
        );
    }
    let mut blocks = String::new();
    let mut expected = [tx, ty, tx + w, ty + h + 0.75 * cap];
    if habit == 9 || habit == 10 {
        blocks = format!("0\nSECTION\n2\nBLOCKS\n0\nBLOCK\n2\nP\n10\n3\n20\n7\n{body}0\nENDBLK\n");
        if habit == 9 {
            blocks += "0\nBLOCK\n2\nQ\n10\n2\n20\n4\n0\nINSERT\n2\nP\n8\n0\n10\n2\n20\n4\n41\n-1\n42\n1\n50\n90\n0\nENDBLK\n";
            body = format!("0\nINSERT\n2\nQ\n8\nCUT\n10\n{tx}\n20\n{ty}\n");
            expected = [tx - h, ty - w, tx, ty];
        } else {
            body = format!("0\nINSERT\n2\nP\n8\nCUT\n10\n{tx}\n20\n{ty}\n41\n-1\n42\n1\n");
            expected = [tx - w, ty, tx, ty + h];
        }
        blocks += "0\nENDSEC\n";
    }
    if habit == 14 {
        for kind in ["TEXT", "MTEXT", "DIMENSION", "HATCH", "LEADER", "SOLID"] {
            body += &format!("0\n{kind}\n8\nCUT\n10\n{tx}\n20\n{ty}\n1\nannotation\n");
        }
        body += &poly(
            &[
                [tx - 20.0, ty],
                [tx - 10.0, ty],
                [tx - 10.0, ty + 10.0],
                [tx - 20.0, ty + 10.0],
            ],
            "BEND",
            scale,
            0.0,
        );
    }
    if habit == 15 {
        options.colors = Some(vec!["7".into()]);
        body += &poly(
            &[
                [tx - 20.0, ty],
                [tx - 10.0, ty],
                [tx - 10.0, ty + 10.0],
                [tx - 20.0, ty + 10.0],
            ],
            "SCORE",
            scale,
            0.0,
        );
    }
    if habit == 16 {
        body += &poly(
            &[
                [tx - 10.0, ty - 10.0],
                [tx + w + 10.0, ty - 10.0],
                [tx + w + 10.0, ty + h + 10.0],
                [tx - 10.0, ty + h + 10.0],
            ],
            "SHEET",
            scale,
            0.0,
        );
    }
    let header = match habit {
        11 => String::new(),
        12 => "0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1027\n0\nENDSEC\n".into(),
        _ => format!(
            "0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n{}\n0\nENDSEC\n",
            if habit == 13 { 5 } else { 4 }
        ),
    };
    let mut table = "0\nSECTION\n2\nTABLES\n".to_string();
    for (layer, color) in [
        ("CUT", 7),
        ("OP", 7),
        ("SCORE", 1),
        ("BEND", 5),
        ("SHEET", 30),
    ] {
        table += &format!("0\nLAYER\n2\n{layer}\n62\n{color}\n");
    }
    table += "0\nENDSEC\n";
    let source =
        format!("{header}{table}{blocks}0\nSECTION\n2\nENTITIES\n{body}0\nENDSEC\n0\nEOF\n");
    let library = Library::import(&[(format!("{name}.dxf"), source)], &options)
        .map_err(|e| TestCaseError::fail(format!("{name}: {e:#}")))?;
    prop_assert_eq!(library.parts.len(), 1, "{}", name);
    let part = &library.parts[0];
    prop_assert_eq!(part.holes.len(), 1, "{}", name);
    // Off-centre hole detects a wrong reflection or missing block-base offset,
    // which the outer rectangle and total area alone cannot reveal.
    let hole_center = match habit {
        9 => [tx - h * 0.6, ty - w * 0.4],
        10 => [tx - w * 0.4, ty + h * 0.6],
        _ => [cx, cy],
    };
    let hole_points = part.holes[0].flatten(0.0001).unwrap();
    for point in hole_points {
        let distance = (point[0] - hole_center[0]).hypot(point[1] - hole_center[1]);
        prop_assert!(
            (distance - radius).abs() < 0.0002,
            "{name}: hole radius {distance} != {radius}"
        );
    }
    for (actual, expected) in part.bounds_mm.into_iter().zip(expected) {
        prop_assert!(
            (actual - expected).abs() < 1e-7,
            "{name}: bound {actual} != {expected}"
        );
    }
    // Polygon area differs only by the documented flattening error. This bound
    // derives from the original perimeter; it is independent of import code.
    let exact_area = w * h + 0.6 * w * cap - std::f64::consts::PI * radius * radius;
    let area_bound =
        (2.0 * (w + h) + 4.0 * cap + std::f64::consts::TAU * radius) * options.tolerance;
    prop_assert!(
        (part.area_mm2 - exact_area).abs() < area_bound,
        "{name}: area {} vs {exact_area}",
        part.area_mm2
    );
    let report = &library.imports[0].report;
    prop_assert!(report.open_contours.is_empty(), "{}", name);
    match habit {
        2 | 3 => prop_assert_eq!(report.closed_gaps.len(), 1),
        4 | 5 => prop_assert!(report.cleanup.overlapping_segments_merged > 0),
        6 => {
            prop_assert!(report.cleanup.duplicate_segments_removed > 0);
            prop_assert!(report.cleanup.zero_length_segments_removed > 0);
        }
        8 => prop_assert!(
            library
                .warnings
                .iter()
                .any(|w| w.contains("widths ignored"))
        ),
        11 | 12 => prop_assert!(report.units.as_ref().unwrap().possible_inches),
        13 => prop_assert_eq!(report.units.as_ref().unwrap().mm_per_unit, 10.0),
        14 => prop_assert!(
            library
                .warnings
                .iter()
                .any(|w| w.contains("ignored") && w.contains("TEXT"))
        ),
        15 => prop_assert_eq!(&report.selection_mode, "explicit"),
        16 => {
            prop_assert_eq!(library.sheet_outlines.len(), 1);
            prop_assert!((library.sheet_outlines[0].width_mm - (w + 20.0)).abs() < 1e-8);
        }
        _ => {}
    }
    if std::env::var_os("NESTBOLT_HABIT_TRACE").is_some() {
        eprintln!("habit-pass {name}");
    }
    Ok(library)
}
