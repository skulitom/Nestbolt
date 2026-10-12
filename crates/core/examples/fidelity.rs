//! G6 fidelity measurement on real drawings: import each file, nest every part
//! (mirroring allowed, quarter turns), export every sheet as SVG and DXF,
//! re-import the exports finely and compare each placed contour with the
//! source curves under the same placement (Hausdorff distance, mm). Prints one
//! JSON object per input file.
use std::collections::HashMap;

use nestbolt_core::{
    clock::Timing,
    curves::{Affine, hausdorff},
    export::{Options as ExportOptions, dxf, svg},
    import::{Options as ImportOptions, import_dxf, import_svg},
    project::{Library, Request, RequestPart, RequestSheet},
    sheets::{Options, optimize},
};
use nestbolt_validator::job::{Margins, Rotations};
use serde_json::json;

type Ring = Vec<[f64; 2]>;

fn bounds(ring: &Ring) -> [f64; 4] {
    ring.iter().fold(
        [
            f64::INFINITY,
            f64::INFINITY,
            f64::NEG_INFINITY,
            f64::NEG_INFINITY,
        ],
        |b, p| {
            [
                b[0].min(p[0]),
                b[1].min(p[1]),
                b[2].max(p[0]),
                b[3].max(p[1]),
            ]
        },
    )
}

fn close(a: [f64; 4], b: [f64; 4]) -> bool {
    (0..4).all(|i| (a[i] - b[i]).abs() < 0.5)
}

fn measure(path: &str) -> serde_json::Value {
    let name = std::path::Path::new(path)
        .file_name()
        .unwrap()
        .to_string_lossy()
        .into_owned();
    let text = match std::fs::read_to_string(path) {
        Ok(t) => t,
        Err(e) => return json!({"file": name, "error": e.to_string()}),
    };
    let library = match Library::import(&[(name.clone(), text)], &ImportOptions::default()) {
        Ok(l) if !l.parts.is_empty() => l,
        Ok(_) => return json!({"file": name, "skipped": "no closed outlines"}),
        Err(e) => return json!({"file": name, "skipped": format!("{e:#}")}),
    };
    let side = library
        .parts
        .iter()
        .map(|p| (p.bounds_mm[2] - p.bounds_mm[0]).max(p.bounds_mm[3] - p.bounds_mm[1]))
        .fold(0.0, f64::max);
    let request = Request {
        name: Some(name.clone()),
        parts: library
            .parts
            .iter()
            .take(300)
            .map(|p| RequestPart {
                id: p.id.clone(),
                quantity: 1,
                rotations: Rotations::List {
                    degrees: vec![0.0, 90.0, 180.0, 270.0],
                },
                allow_mirror: true,
                priority: 1.0,
            })
            .collect(),
        sheets: vec![RequestSheet {
            id: None,
            width_mm: (side * 1.5 + 20.0).max(600.0),
            height_mm: (side * 1.5 + 20.0).max(400.0),
            count: None,
            margins_mm: Margins {
                left: 5.0,
                right: 5.0,
                bottom: 5.0,
                top: 5.0,
            },
            defects_mm: vec![],
            outline_mm: vec![],
        }],
        spacing_mm: 1.0,
        edge_spacing_mm: 1.0,
        mode: nestbolt_validator::job::Mode::All,
    };
    let (job, outlines) = match request.job(&library) {
        Ok(j) => j,
        Err(e) => return json!({"file": name, "skipped": format!("{e:#}")}),
    };
    let result = match optimize(
        &job,
        Options {
            seconds: 4.0,
            timing: Timing::Work,
            ..Options::default()
        },
        |_| {},
    ) {
        Ok(r) if r.validation.valid => r,
        Ok(_) => return json!({"file": name, "error": "invalid layout"}),
        Err(e) => return json!({"file": name, "error": format!("{e:#}")}),
    };
    // Re-import as a user would; the comparison flattens the exact re-imported
    // curves at 0.0005 mm, so the import tolerance does not limit it.
    let fine = ImportOptions::default();
    let height = job.stocks[0].height;
    let mut worst: HashMap<&str, f64> = HashMap::new();
    let mut rings = 0;
    let mut unmatched = 0;
    let mut kinds: HashMap<String, usize> = HashMap::new();
    for sheet in &result.layout.sheets {
        let mut expected: Vec<Ring> = vec![];
        for p in result
            .layout
            .placements
            .iter()
            .filter(|p| p.sheet_id == sheet.id)
        {
            let o = &outlines[&p.part_id];
            let a = Affine::placement(&p.transform);
            for c in std::iter::once(&o.outer).chain(&o.holes) {
                expected.push(c.transformed(&a).flatten(0.0005).unwrap());
                for s in &c.segments {
                    let kind = serde_json::to_value(s).unwrap()["kind"]
                        .as_str()
                        .unwrap()
                        .to_owned();
                    *kinds.entry(kind).or_default() += 1;
                }
            }
        }
        let options = ExportOptions {
            sheet_outline: false,
        };
        let exports = [
            (
                "svg",
                svg(&job, &result.layout, &sheet.id, &outlines, options)
                    .map(|t| import_svg(&t, &fine)),
            ),
            (
                "dxf",
                dxf(&job, &result.layout, &sheet.id, &outlines, options)
                    .map(|t| import_dxf(&t, &fine)),
            ),
        ];
        for (format, imported) in exports {
            let imported = match imported {
                Ok(Ok(i)) => i,
                Ok(Err(e)) | Err(e) => {
                    return json!({"file": name, "error": format!("{format}: {e:#}")});
                }
            };
            if std::env::var_os("FIDELITY_DEBUG").is_some() {
                for w in imported
                    .warnings
                    .iter()
                    .filter(|w| !w.contains("corner loop"))
                    .take(5)
                {
                    eprintln!("{format} re-import: {w}");
                }
            }
            // Compare the exact re-imported curves: nesting polygons may leave
            // out relief loops that the exports (and the cuts) keep.
            let mut got: Vec<Ring> = imported
                .parts
                .iter()
                .flat_map(|p| std::iter::once(&p.outer).chain(&p.holes))
                .map(|c| c.flatten(0.0005).unwrap())
                .collect();
            if format == "svg" {
                // The SVG export flips Y; map the re-import back into the sheet frame.
                for ring in &mut got {
                    for q in ring.iter_mut() {
                        q[1] += height;
                    }
                }
            }
            let boxes: Vec<_> = got.iter().map(bounds).collect();
            for e in &expected {
                let b = bounds(e);
                let best = got
                    .iter()
                    .zip(&boxes)
                    .filter(|(_, g)| close(b, **g))
                    .map(|(g, _)| hausdorff(e, g))
                    .fold(f64::INFINITY, f64::min);
                if best.is_infinite() {
                    unmatched += 1;
                    if std::env::var_os("FIDELITY_DEBUG").is_some() && unmatched <= 3 {
                        let nearest = boxes
                            .iter()
                            .min_by(|x, y| {
                                let d = |g: &[f64; 4]| {
                                    (0..4).map(|i| (g[i] - b[i]).abs()).fold(0.0, f64::max)
                                };
                                d(x).total_cmp(&d(y))
                            })
                            .unwrap();
                        eprintln!(
                            "{format} unmatched {b:?} nearest {nearest:?} of {} got",
                            got.len()
                        );
                    }
                }
                let w = worst.entry(format).or_default();
                *w = w.max(best);
                rings += 1;
            }
        }
    }
    json!({"file": name, "parts": job.parts.len(), "sheets": result.layout.sheets.len(),
           "rings_compared": rings, "unmatched": unmatched, "segments": kinds,
           "max_hausdorff_mm": worst, "warnings": library.warnings.len()})
}

fn main() {
    for path in std::env::args().skip(1) {
        println!("{}", measure(&path));
    }
}
