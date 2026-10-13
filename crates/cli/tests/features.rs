//! End-to-end tests of every v1 feature through the CLI: `import` real SVG/DXF
//! drawings, `nest` a request with a repeatable work budget, then check the
//! written layout with the separate `validate` command. One test per plan item.
use std::{
    f64::consts::PI,
    fs,
    path::{Path, PathBuf},
    process::Command,
    time::{SystemTime, UNIX_EPOCH},
};

use serde_json::{Value, json};

fn example(name: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../examples")
        .join(name)
}

fn temp(name: &str) -> PathBuf {
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let dir = std::env::temp_dir().join(format!(
        "nestbolt-feature-{name}-{}-{stamp}",
        std::process::id()
    ));
    fs::create_dir_all(&dir).unwrap();
    dir
}

fn nestbolt(args: &[&std::ffi::OsStr]) -> std::process::Output {
    Command::new(env!("CARGO_BIN_EXE_nestbolt"))
        .args(args)
        .env("RAYON_NUM_THREADS", "1")
        .output()
        .unwrap()
}

fn import(dir: &Path, inputs: &[PathBuf]) -> PathBuf {
    let library = dir.join("library.json");
    let mut args: Vec<&std::ffi::OsStr> = vec!["import".as_ref()];
    args.extend(inputs.iter().map(|p| p.as_os_str()));
    args.extend(["--output".as_ref(), library.as_os_str()]);
    let out = nestbolt(&args);
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    library
}

#[test]
fn explicit_gap_repair_reports_its_size_and_location() {
    let dir = temp("gap-repair");
    let source = dir.join("gap.svg");
    let library = dir.join("library.json");
    fs::write(&source,r#"<svg width="30mm" viewBox="0 0 30 30"><path id="outline" d="M0 0 H20 V20 H0 V0.2"/></svg>"#).unwrap();
    let failed = nestbolt(&[
        "import".as_ref(),
        source.as_os_str(),
        "--output".as_ref(),
        library.as_os_str(),
    ]);
    assert!(!failed.status.success());
    assert!(String::from_utf8_lossy(&failed.stderr).contains("Close gaps up to 0.200000 mm"));
    assert!(!library.exists());
    let repaired = nestbolt(&[
        "import".as_ref(),
        source.as_os_str(),
        "--output".as_ref(),
        library.as_os_str(),
        "--close-gaps".as_ref(),
        "0.2".as_ref(),
    ]);
    assert!(
        repaired.status.success(),
        "{}",
        String::from_utf8_lossy(&repaired.stderr)
    );
    let response: Value = serde_json::from_slice(&repaired.stdout).unwrap();
    assert_eq!(response["parts"].as_array().unwrap().len(), 1);
    assert_eq!(
        response["imports"][0]["report"]["closed_gaps"][0]["size_mm"],
        0.2
    );
    assert_eq!(
        response["imports"][0]["report"]["closed_gaps"][0]["from_mm"],
        json!([0.0, -0.2])
    );
}

struct Nested {
    dir: PathBuf,
    report: Value,
    layout: Value,
    job: Value,
}

impl Nested {
    fn metrics(&self) -> &Value {
        &self.report["validation"]["metrics"]
    }

    /// The separate checker's verdict on the written job and layout.
    fn validate(&self) -> Value {
        let out = nestbolt(&[
            "validate".as_ref(),
            "--job".as_ref(),
            self.dir.join("job.json").as_os_str(),
            "--layout".as_ref(),
            self.dir.join("layout.json").as_os_str(),
        ]);
        let report: Value = serde_json::from_slice(&out.stdout).unwrap();
        assert_eq!(out.status.success(), report["valid"] == true);
        report
    }

    fn placements(&self, part: &str) -> Vec<&Value> {
        self.layout["placements"]
            .as_array()
            .unwrap()
            .iter()
            .filter(|p| p["part_id"] == part)
            .collect()
    }
}

fn nest(dir: &Path, library: &Path, request: Value, seconds: &str) -> Nested {
    let request_path = dir.join(format!(
        "request-{}.json",
        fs::read_dir(dir).unwrap().count()
    ));
    fs::write(&request_path, serde_json::to_vec_pretty(&request).unwrap()).unwrap();
    let out_dir = dir.join(format!("run-{}", fs::read_dir(dir).unwrap().count()));
    let out = nestbolt(&[
        "nest".as_ref(),
        "--library".as_ref(),
        library.as_os_str(),
        "--request".as_ref(),
        request_path.as_os_str(),
        "--out-dir".as_ref(),
        out_dir.as_os_str(),
        "--seconds".as_ref(),
        seconds.as_ref(),
        "--repeatable".as_ref(),
        // CI runners can be more than twice as slow as the reference PC; the
        // work budget stays the same, so the layout does too.
        "--time-limit".as_ref(),
        "120".as_ref(),
    ]);
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    let read = |name: &str| -> Value {
        serde_json::from_slice(&fs::read(out_dir.join(name)).unwrap()).unwrap()
    };
    let nested = Nested {
        report: read("report.json"),
        layout: read("layout.json"),
        job: read("job.json"),
        dir: out_dir,
    };
    assert_eq!(nested.report["validation"]["valid"], true);
    assert_eq!(nested.validate()["valid"], true, "the separate check fails");
    nested
}

fn sheet(w: f64, h: f64, margin: f64) -> Value {
    json!({"width_mm": w, "height_mm": h,
           "margins_mm": {"left": margin, "right": margin, "bottom": margin, "top": margin}})
}

// examples/parts.svg imports as parts-1 frame (80 x 60, 60 x 40 window),
// parts-2 washer (24 mm, 10 mm hole), parts-3 bracket, parts-4 elliptical tab.
const FRAME: &str = "parts-1";
const WASHER: &str = "parts-2";
const BRACKET: &str = "parts-3";
const TAB: &str = "parts-4";

#[test]
fn several_sheet_sizes_margins_and_capped_counts() {
    let dir = temp("sheets");
    let library = import(&dir, &[example("parts.svg")]);
    let mut small = sheet(120.0, 120.0, 10.0);
    small["id"] = json!("small");
    small["count"] = json!(1);
    let mut large = sheet(200.0, 150.0, 5.0);
    large["id"] = json!("large");
    let run = nest(
        &dir,
        &library,
        json!({"parts": [{"id": BRACKET, "quantity": 14}], "sheets": [small, large],
               "spacing_mm": 1, "edge_spacing_mm": 1}),
        "3",
    );
    assert_eq!(run.metrics()["placed_parts"], 14);
    let stocks: Vec<_> = run.layout["sheets"]
        .as_array()
        .unwrap()
        .iter()
        .map(|s| s["stock_id"].as_str().unwrap().to_owned())
        .collect();
    assert!(stocks.iter().filter(|s| *s == "small").count() <= 1);
    assert!(stocks.len() >= 2, "14 brackets need more than one sheet");
    let job_stocks = run.job["stocks"].as_array().unwrap();
    assert_eq!(job_stocks[0]["count"], 1);
    assert_eq!(job_stocks[0]["margins"]["left"], 10.0);
    assert!(
        job_stocks[1]["count"].is_null(),
        "unlimited stays unlimited"
    );
}

#[test]
fn fewest_sheets_with_the_offcut_at_one_end() {
    let dir = temp("multi");
    let library = import(&dir, &[example("parts.svg")]);
    // 16 washers fit a 100 mm square in a 4 x 4 grid, so 20 need two sheets.
    let run = nest(
        &dir,
        &library,
        json!({"parts": [{"id": WASHER, "quantity": 20}], "sheets": [sheet(105.0, 105.0, 2.5)],
               "spacing_mm": 1, "edge_spacing_mm": 0}),
        "4",
    );
    let m = run.metrics();
    assert_eq!(m["placed_parts"], 20);
    assert_eq!(m["sheets_used"], 2);
    // Material is (sheets - 1) + used fraction of the last sheet: the leftover
    // washers are pushed together, leaving one offcut.
    assert!(m["normalized_material"].as_f64().unwrap() < 1.5, "{m}");
    assert!(m["trailing_offcut_area"].as_f64().unwrap() > 0.5 * 105.0 * 105.0);
}

#[test]
fn small_parts_go_inside_holes() {
    let dir = temp("holes");
    let library = import(&dir, &[example("parts.svg")]);
    // The frame nearly fills the one sheet; the washers fit only in its window.
    let mut only = sheet(90.0, 70.0, 0.0);
    only["count"] = json!(1);
    let run = nest(
        &dir,
        &library,
        json!({"parts": [{"id": FRAME, "quantity": 1}, {"id": WASHER, "quantity": 2}],
               "sheets": [only], "spacing_mm": 1, "edge_spacing_mm": 1}),
        "2",
    );
    assert_eq!(run.metrics()["placed_parts"], 3);
    assert!(run.report["parts_in_holes"].as_u64().unwrap() >= 2);
}

#[test]
fn defects_and_remnant_outlines_stay_clear() {
    let dir = temp("defects");
    let library = import(&dir, &[example("parts.svg")]);
    let mut damaged = sheet(200.0, 100.0, 2.0);
    damaged["defects_mm"] =
        json!([{"outer": [[80, 30], [120, 30], [120, 70], [80, 70]], "holes": []}]);
    let mut remnant = sheet(150.0, 150.0, 0.0);
    // An L-shaped offcut: the top-right quarter is gone.
    remnant["outline_mm"] = json!([{"outer": [[0, 0], [150, 0], [150, 75], [75, 75], [75, 150], [0, 150]], "holes": []}]);
    remnant["count"] = json!(1);
    let run = nest(
        &dir,
        &library,
        json!({"parts": [{"id": TAB, "quantity": 30}], "sheets": [remnant, damaged],
               "spacing_mm": 1, "edge_spacing_mm": 1}),
        "3",
    );
    assert_eq!(run.metrics()["placed_parts"], 30);
    let stocks = run.job["stocks"].as_array().unwrap();
    assert_eq!(stocks[0]["outline"].as_array().unwrap().len(), 1);
    assert_eq!(stocks[1]["defects"].as_array().unwrap().len(), 1);
}

#[test]
fn part_and_edge_spacing_are_kept() {
    let dir = temp("spacing");
    let library = import(&dir, &[example("parts.svg")]);
    let run = nest(
        &dir,
        &library,
        json!({"parts": [{"id": BRACKET, "quantity": 6}, {"id": TAB, "quantity": 6}],
               "sheets": [sheet(200.0, 150.0, 0.0)], "spacing_mm": 3, "edge_spacing_mm": 4}),
        "3",
    );
    // The checked job adds the curve tolerance, so exact curves keep the gaps too.
    let gap = |k: &str| run.job[k].as_f64().unwrap();
    assert!(
        (3.0..3.05).contains(&gap("clearance")),
        "{}",
        run.job["clearance"]
    );
    assert!(
        (4.0..4.05).contains(&gap("edge_clearance")),
        "{}",
        run.job["edge_clearance"]
    );
    // The same layout fails a check that asks for far more spacing.
    let mut strict = run.job.clone();
    strict["clearance"] = json!(30.0);
    let strict_path = run.dir.join("strict-job.json");
    fs::write(&strict_path, serde_json::to_vec(&strict).unwrap()).unwrap();
    let out = nestbolt(&[
        "validate".as_ref(),
        "--job".as_ref(),
        strict_path.as_os_str(),
        "--layout".as_ref(),
        run.dir.join("layout.json").as_os_str(),
    ]);
    assert!(!out.status.success());
    let report: Value = serde_json::from_slice(&out.stdout).unwrap();
    assert_eq!(report["valid"], false);
}

#[test]
fn rotation_lists_steps_free_and_mirroring() {
    let dir = temp("rotation");
    let library = import(&dir, &[example("parts.svg")]);
    let run = nest(
        &dir,
        &library,
        json!({"parts": [
                  {"id": TAB, "quantity": 6, "rotations": {"kind": "list", "degrees": [0, 180]}},
                  {"id": BRACKET, "quantity": 4, "rotations": {"kind": "step", "degrees": 90}, "allow_mirror": true},
                  {"id": WASHER, "quantity": 4, "rotations": {"kind": "free"}},
                  {"id": FRAME, "quantity": 1, "rotations": {"kind": "list", "degrees": [0]}}],
               "sheets": [sheet(250.0, 200.0, 2.0)], "spacing_mm": 1, "edge_spacing_mm": 1}),
        "3",
    );
    let turns = |p: &Value| {
        let r = p["transform"]["rotation_radians"].as_f64().unwrap() / (PI / 2.0);
        r.rem_euclid(4.0)
    };
    let near = |x: f64, y: f64| (x - y).abs() < 1e-6 || (x - y).abs() > 4.0 - 1e-6;
    for p in run.placements(TAB) {
        assert!(near(turns(p), 0.0) || near(turns(p), 2.0), "{p}");
        assert_eq!(p["transform"]["mirrored"], false);
    }
    for p in run.placements(BRACKET) {
        assert!(near(turns(p), turns(p).round()), "{p}");
    }
    for p in run.placements(FRAME) {
        assert!(near(turns(p), 0.0), "{p}");
    }
    for p in run.placements(WASHER) {
        assert_eq!(p["transform"]["mirrored"], false);
    }
    assert_eq!(run.metrics()["placed_parts"], 15);
}

#[test]
fn quantities_from_one_to_hundreds() {
    let dir = temp("quantity");
    let library = import(&dir, &[example("parts.svg")]);
    let run = nest(
        &dir,
        &library,
        json!({"parts": [{"id": FRAME, "quantity": 1}, {"id": TAB, "quantity": 200}],
               "sheets": [sheet(600.0, 400.0, 5.0)], "spacing_mm": 1, "edge_spacing_mm": 1}),
        "5",
    );
    assert_eq!(run.metrics()["placed_parts"], 201);
    assert_eq!(run.placements(FRAME).len(), 1);
    assert_eq!(run.placements(TAB).len(), 200);
}

#[test]
fn fill_modes_place_the_most_area_or_priority() {
    let dir = temp("fill");
    let library = import(&dir, &[example("parts.svg")]);
    let mut one = sheet(100.0, 100.0, 0.0);
    one["count"] = json!(1);
    let area = nest(
        &dir,
        &library,
        json!({"parts": [{"id": WASHER, "quantity": 40}], "sheets": [one.clone()],
               "spacing_mm": 1, "edge_spacing_mm": 0, "mode": "fill_area"}),
        "3",
    );
    let placed = area.metrics()["placed_parts"].as_u64().unwrap();
    assert!((10..40).contains(&placed), "{placed}");
    let priority = nest(
        &dir,
        &library,
        json!({"parts": [{"id": BRACKET, "quantity": 2, "priority": 10},
                         {"id": WASHER, "quantity": 40, "priority": 1}],
               "sheets": [one], "spacing_mm": 1, "edge_spacing_mm": 0, "mode": "fill_priority"}),
        "3",
    );
    assert_eq!(priority.placements(BRACKET).len(), 2);
    assert!(priority.metrics()["placed_priority"].as_f64().unwrap() >= 20.0);
}

#[test]
fn svg_and_dxf_in_curves_out_and_re_export() {
    let dir = temp("formats");
    let library = import(
        &dir,
        &[
            example("fidelity/curves-mm.svg"),
            example("fidelity/plate-in.dxf"),
        ],
    );
    let parts: Value = serde_json::from_slice(&fs::read(&library).unwrap()).unwrap();
    let ids: Vec<_> = parts["parts"]
        .as_array()
        .unwrap()
        .iter()
        .map(|p| p["id"].as_str().unwrap().to_owned())
        .collect();
    assert!(ids.iter().any(|i| i.starts_with("plate-in")));
    assert!(ids.iter().any(|i| i.starts_with("curves-mm")));
    let request = json!({"parts": [], "sheets": [sheet(400.0, 300.0, 5.0)],
                         "spacing_mm": 1, "edge_spacing_mm": 1});
    let run = nest(&dir, &library, request.clone(), "3");
    let svg = fs::read_to_string(run.dir.join("sheet-0.svg")).unwrap();
    let dxf = fs::read_to_string(run.dir.join("sheet-0.dxf")).unwrap();
    // Curves are transformed, not re-polygonised: SVG arcs/Béziers and DXF arcs.
    assert!(
        svg.contains(" A ") || svg.contains(" C "),
        "no curves in SVG"
    );
    assert!(
        dxf.contains("\nARC\n") || dxf.contains("\nELLIPSE\n"),
        "no arcs in DXF"
    );
    // `export` re-writes the same files from the layout.
    let again = dir.join("export");
    let request_path = dir.join("export-request.json");
    fs::write(&request_path, serde_json::to_vec(&request).unwrap()).unwrap();
    let out = nestbolt(&[
        "export".as_ref(),
        "--library".as_ref(),
        library.as_os_str(),
        "--request".as_ref(),
        request_path.as_os_str(),
        "--layout".as_ref(),
        run.dir.join("layout.json").as_os_str(),
        "--out-dir".as_ref(),
        again.as_os_str(),
    ]);
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    assert_eq!(fs::read_to_string(again.join("sheet-0.svg")).unwrap(), svg);
    assert_eq!(fs::read_to_string(again.join("sheet-0.dxf")).unwrap(), dxf);
    // The exported drawing imports again with every part.
    let back = import(&temp("formats-back"), &[run.dir.join("sheet-0.svg")]);
    let back: Value = serde_json::from_slice(&fs::read(back).unwrap()).unwrap();
    assert_eq!(
        back["parts"].as_array().unwrap().len() as u64,
        run.metrics()["placed_parts"].as_u64().unwrap()
    );
}

#[test]
fn repeatable_budgets_give_the_same_layout() {
    let dir = temp("repeat");
    let library = import(&dir, &[example("parts.svg")]);
    let request: Value =
        serde_json::from_slice(&fs::read(example("nest-request.json")).unwrap()).unwrap();
    let first = nest(&dir, &library, request.clone(), "2");
    let second = nest(&dir, &library, request, "2");
    assert_eq!(first.report["repeatable"], true);
    assert_eq!(first.layout, second.layout);
}

#[test]
fn version_names_the_command() {
    let out = nestbolt(&["--version".as_ref()]);
    assert!(out.status.success());
    assert_eq!(
        String::from_utf8(out.stdout).unwrap().trim(),
        format!("nestbolt {}", env!("CARGO_PKG_VERSION"))
    );
}
