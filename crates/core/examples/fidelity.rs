//! G6 fidelity measurement on real drawings: import each file, nest every part
//! (mirroring allowed, quarter turns), export every sheet as SVG and DXF,
//! re-import the exports finely and compare each placed contour with the
//! source curves under the same placement (Hausdorff distance, mm). Prints one
//! JSON object per input file.
use std::collections::{HashMap, VecDeque};
use std::path::{Path, PathBuf};

use anyhow::{Context, Result, ensure};
use serde::Deserialize;

use nestbolt_core::{
    clock::Timing,
    curves::{Affine, hausdorff},
    export::{Options as ExportOptions, dxf, svg},
    import::{Options as ImportOptions, decode_drawing, import_dxf, import_svg},
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

/// Optional per-file settings for H2; ordinary G6 positional inputs still work.
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Task {
    path: String,
    #[serde(default)]
    options: ImportOptions,
    seconds: f64,
    time_limit: Option<f64>,
    output: Option<PathBuf>,
}

fn save(folder: Option<&Path>, name: &str, value: &[u8]) -> Result<()> {
    if let Some(folder) = folder {
        std::fs::write(folder.join(name), value)?;
    }
    Ok(())
}

/// A full matching prevents duplicate/extra exports from reusing a single
/// expected contour. Iterative augmenting paths keep large drawings off the stack.
fn matched_contours(edges: &[Vec<usize>], got_count: usize) -> usize {
    let mut left: Vec<Option<usize>> = vec![None; edges.len()];
    let mut right: Vec<Option<usize>> = vec![None; got_count];
    let mut matched = 0;
    for root in 0..edges.len() {
        let mut pending = VecDeque::from([root]);
        let mut seen = vec![false; edges.len()];
        seen[root] = true;
        let mut previous = vec![None; got_count];
        let mut free = None;
        'search: while let Some(i) = pending.pop_front() {
            for &j in &edges[i] {
                if previous[j].is_some() {
                    continue;
                }
                previous[j] = Some(i);
                if let Some(owner) = right[j] {
                    if !seen[owner] {
                        seen[owner] = true;
                        pending.push_back(owner);
                    }
                } else {
                    free = Some(j);
                    break 'search;
                }
            }
        }
        if let Some(mut j) = free {
            loop {
                let i = previous[j].expect("discovered edge");
                let old = left[i];
                left[i] = Some(j);
                right[j] = Some(i);
                if let Some(old) = old {
                    j = old;
                } else {
                    break;
                }
            }
            matched += 1;
        }
    }
    matched
}

fn measure(task: &Task) -> Result<serde_json::Value> {
    let path = &task.path;
    let name = Path::new(path)
        .file_name()
        .context("input has no filename")?
        .to_string_lossy()
        .into_owned();
    let text = match std::fs::read(path)
        .map_err(anyhow::Error::from)
        .and_then(|bytes| decode_drawing(&name, &bytes))
    {
        Ok(t) => t,
        Err(e) => return Ok(json!({"file": name, "skipped": format!("{e:#}"), "stage":"decode"})),
    };
    let library = match Library::import(&[(name.clone(), text)], &task.options) {
        Ok(l) if !l.parts.is_empty() => l,
        Ok(_) => {
            return Ok(json!({"file": name, "skipped": "no closed outlines", "stage":"import"}));
        }
        Err(e) => return Ok(json!({"file": name, "skipped": format!("{e:#}"), "stage":"import"})),
    };
    let output = task.output.as_deref();
    if let Some(folder) = output {
        std::fs::create_dir(folder).context("fidelity output must be a new directory")?;
    }
    save(output, "library.json", &serde_json::to_vec(&library)?)?;
    let side = library
        .parts
        .iter()
        .map(|p| (p.bounds_mm[2] - p.bounds_mm[0]).max(p.bounds_mm[3] - p.bounds_mm[1]))
        .fold(0.0, f64::max);
    let request = Request {
        lead_in: None,
        name: Some(name.clone()),
        parts: library
            .parts
            .iter()
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
            from_import: None,
            outline_tolerance_mm: 0.0,
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
        common_line: None,
        edge_spacing_mm: 1.0,
        mode: nestbolt_validator::job::Mode::All,
    };
    let (job, outlines) = match request.job(&library) {
        Ok(j) => j,
        Err(e) => return Ok(json!({"file": name, "error": format!("{e:#}"), "stage":"job"})),
    };
    let result = match optimize(
        &job,
        Options {
            seconds: task.seconds,
            time_limit: task.time_limit,
            timing: Timing::Work,
            ..Options::default()
        },
        |_, _| {},
    ) {
        Ok(r) if r.validation.valid => r,
        Ok(_) => return Ok(json!({"file": name, "error": "invalid layout", "stage":"nest"})),
        Err(e) => return Ok(json!({"file": name, "error": format!("{e:#}"), "stage":"nest"})),
    };
    ensure!(
        result.layout.placements.len() == library.parts.len(),
        "nest omitted an imported part"
    );
    save(output, "job.json", &serde_json::to_vec(&job)?)?;
    save(output, "layout.json", &serde_json::to_vec(&result.layout)?)?;
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
        let mut labels: Vec<String> = vec![];
        for p in result
            .layout
            .placements
            .iter()
            .filter(|p| p.sheet_id == sheet.id)
        {
            let o = &outlines[&p.part_id];
            let a = Affine::placement(&p.transform);
            for c in std::iter::once(&o.outer).chain(&o.holes) {
                expected.push(c.transformed(&a).flatten(0.0005)?);
                labels.push(format!(
                    "{} mirrored {} rotation {:.4}",
                    p.part_id, p.transform.mirrored, p.transform.rotation_radians
                ));
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
                svg(&job, &result.layout, &sheet.id, &outlines, options)?,
            ),
            (
                "dxf",
                dxf(&job, &result.layout, &sheet.id, &outlines, options)?,
            ),
        ];
        for (format, text) in exports {
            save(output, &format!("{}.{format}", sheet.id), text.as_bytes())?;
            let imported = if format == "svg" {
                import_svg(&text, &fine)
            } else {
                import_dxf(&text, &fine)
            }
            .with_context(|| format!("{format} re-import"))?;
            ensure!(
                imported.report.open_contours.is_empty(),
                "{format} re-import contains open paths"
            );
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
                .map(|c| c.flatten(0.0005))
                .collect::<Result<_>>()?;
            if format == "svg" {
                // The SVG export flips Y; map the re-import back into the sheet frame.
                for ring in &mut got {
                    for q in ring.iter_mut() {
                        q[1] += height;
                    }
                }
            }
            let boxes: Vec<_> = got.iter().map(bounds).collect();
            let mut edges = vec![];
            for (k, e) in expected.iter().enumerate() {
                let b = bounds(e);
                let distances: Vec<_> = got
                    .iter()
                    .zip(&boxes)
                    .enumerate()
                    .filter(|(_, (_, g))| close(b, **g))
                    .map(|(j, (g, _))| (j, hausdorff(e, g)))
                    .collect();
                let best = distances
                    .iter()
                    .map(|(_, d)| *d)
                    .fold(f64::INFINITY, f64::min);
                edges.push(
                    distances
                        .iter()
                        .filter(|(_, d)| *d <= 0.01)
                        .map(|(j, _)| *j)
                        .collect(),
                );
                if best > 0.01 && std::env::var_os("FIDELITY_DEBUG").is_some() {
                    eprintln!("{format} distance {best:.6} for {}", labels[k]);
                }
                let w = worst.entry(format).or_default();
                *w = w.max(best);
                rings += 1;
            }
            unmatched += expected.len().max(got.len()) - matched_contours(&edges, got.len());
        }
    }
    Ok(
        json!({"file": name, "parts": job.parts.len(), "sheets": result.layout.sheets.len(),
           "nest_elapsed_s": result.elapsed_seconds, "repeatable": result.repeatable, "all_parts_measured":true,
           "rings_compared": rings, "unmatched": unmatched, "segments": kinds,
           "max_hausdorff_mm": worst, "warnings": library.warnings, "imports": library.imports}),
    )
}

fn main() -> Result<()> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    let tasks: Vec<Task> = if args.first().is_some_and(|a| a == "--task") {
        ensure!(args.len() == 2, "--task requires one JSON task file");
        vec![serde_json::from_slice(&std::fs::read(&args[1])?)?]
    } else {
        args.into_iter()
            .map(|path| Task {
                path,
                options: ImportOptions::default(),
                seconds: 4.0,
                time_limit: None,
                output: None,
            })
            .collect()
    };
    for task in tasks {
        let row =
            measure(&task).unwrap_or_else(|e| json!({"file":task.path,"error":format!("{e:#}")}));
        println!("{row}");
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::matched_contours;
    #[test]
    fn contour_matching_rejects_reuse_and_finds_augmenting_paths() {
        assert_eq!(matched_contours(&[vec![0], vec![0]], 2), 1);
        assert_eq!(matched_contours(&[vec![0, 1], vec![0]], 2), 2);
        assert_eq!(matched_contours(&[vec![], vec![0]], 1), 1);
        assert_eq!(matched_contours(&[], 1), 0);
    }
}
