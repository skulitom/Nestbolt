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
fn common_line_cli_flags_override_spacing_and_export_compensated_paths() {
    let dir = temp("common-line");
    let source = dir.join("panel.svg");
    fs::write(
        &source,
        include_str!("../../core/tests/fixtures/common-panels.svg"),
    )
    .unwrap();
    let library = import(&dir, &[source]);
    let request = dir.join("request.json");
    let output = dir.join("common");
    fs::write(
        &request,
        serde_json::to_vec(&json!({"parts":[{"id":"panel-1","quantity":2}],
        "sheets":[{"width_mm":86,"height_mm":36}],"spacing_mm":5,"edge_spacing_mm":1}))
        .unwrap(),
    )
    .unwrap();
    let args: &[&std::ffi::OsStr] = &[
        "nest".as_ref(),
        "--library".as_ref(),
        library.as_os_str(),
        "--request".as_ref(),
        request.as_os_str(),
        "--out-dir".as_ref(),
        output.as_os_str(),
        "--seconds".as_ref(),
        "1".as_ref(),
        "--repeatable".as_ref(),
        "--time-limit".as_ref(),
        "15".as_ref(),
        "--common-line".as_ref(),
        "--kerf".as_ref(),
        "0.2".as_ref(),
    ];
    let run = nestbolt(args);
    assert!(
        run.status.success(),
        "{}",
        String::from_utf8_lossy(&run.stderr)
    );
    let report: Value = serde_json::from_slice(&run.stdout).unwrap();
    assert_eq!(report["validation"]["valid"], true);
    assert_eq!(report["parts_in_holes"], 0);
    assert!(
        (report["common_line"][0]["shared_length_mm"]
            .as_f64()
            .unwrap()
            - 30.0)
            .abs()
            < 0.01
    );
    let job: Value = serde_json::from_slice(&fs::read(output.join("job.json")).unwrap()).unwrap();
    assert_eq!(job["clearance"], 0.2);
    let request: Value =
        serde_json::from_slice(&fs::read(output.join("request.json")).unwrap()).unwrap();
    assert_eq!(request["common_line"]["kerf_mm"], 0.2);
    for file in report["files"].as_array().unwrap() {
        let text = fs::read_to_string(output.join(file.as_str().unwrap())).unwrap();
        assert!(text.contains("COMMON"));
    }
}

#[test]
fn lightburn_import_and_direct_nest_preserve_editable_units_and_sheet_files() {
    let dir = temp("lightburn");
    let source = dir.join("roundtrip.lbrn2");
    let original = include_str!("../../core/tests/fixtures/roundtrip.lbrn2");
    fs::write(&source, original).unwrap();
    let library = import(&dir, std::slice::from_ref(&source));
    let saved: Value = serde_json::from_slice(&fs::read(&library).unwrap()).unwrap();
    assert_eq!(saved["lightburn"]["xml"], original);
    assert_eq!(saved["parts"][0]["components"].as_array().unwrap().len(), 2);
    let request =
        json!({"sheets":[{"width_mm":34,"height_mm":24}],"spacing_mm":1,"edge_spacing_mm":0.5});
    let request_path = dir.join("lightburn-request.json");
    fs::write(&request_path, serde_json::to_vec(&request).unwrap()).unwrap();
    for input in [&library, &source] {
        let run = nest(&dir, input, request.clone(), "1");
        assert_eq!(run.metrics()["placed_parts"], 3);
        assert_eq!(run.job["parts"][0]["geometry"].as_array().unwrap().len(), 2);
        let files = run.report["files"].as_array().unwrap();
        assert!(files.len() >= 2);
        for (i, file) in files.iter().enumerate() {
            assert_eq!(
                file.as_str().unwrap(),
                format!("roundtrip-sheet-{}.lbrn2", i + 1)
            );
            let xml = fs::read_to_string(run.dir.join(file.as_str().unwrap())).unwrap();
            assert!(xml.contains("Original MIT rigid-unit integration fixture"));
            assert!(xml.contains("<kerf Value=\"0.2\""));
            let doc = nestbolt_core::lightburn::Document::read(&xml, 0.005).unwrap();
            assert!(doc.scene.mirror_x);
            assert!(
                doc.scene
                    .shapes
                    .iter()
                    .any(|s| s.fixed && s.bounds_mm == Some([0.0, 0.0, 34.0, 24.0]))
            );
        }
        let reexport = run.dir.join("without-outline");
        let output = nestbolt(&[
            "export".as_ref(),
            "--library".as_ref(),
            input.as_os_str(),
            "--request".as_ref(),
            request_path.as_os_str(),
            "--layout".as_ref(),
            run.dir.join("layout.json").as_os_str(),
            "--out-dir".as_ref(),
            reexport.as_os_str(),
            "--sheet-outline".as_ref(),
            "false".as_ref(),
        ]);
        assert!(
            output.status.success(),
            "{}",
            String::from_utf8_lossy(&output.stderr)
        );
        for file in fs::read_dir(reexport).unwrap() {
            let xml = fs::read_to_string(file.unwrap().path()).unwrap();
            let doc = nestbolt_core::lightburn::Document::read(&xml, 0.005).unwrap();
            assert!(
                !doc.scene
                    .shapes
                    .iter()
                    .any(|s| s.fixed && s.bounds_mm == Some([0.0, 0.0, 34.0, 24.0]))
            );
        }
    }
}

#[test]
fn legacy_lightburn_nests_and_exports_modern_paths() {
    let dir = temp("legacy-lightburn");
    let source = dir.join("legacy.lbrn");
    let original = include_str!("../../core/tests/fixtures/legacy.lbrn");
    fs::write(&source, original).unwrap();
    let library = import(&dir, std::slice::from_ref(&source));
    let saved: Value = serde_json::from_slice(&fs::read(library).unwrap()).unwrap();
    assert_eq!(saved["lightburn"]["xml"], original);
    let run = nest(
        &dir,
        &source,
        json!({"sheets":[{"width_mm":34,"height_mm":14}],"spacing_mm":1,"edge_spacing_mm":0.5}),
        "1",
    );
    assert_eq!(run.metrics()["placed_parts"], 1);
    assert_eq!(run.report["files"], json!(["legacy-sheet-1.lbrn2"]));
    let xml = fs::read_to_string(run.dir.join("legacy-sheet-1.lbrn2")).unwrap();
    let doc = nestbolt_core::lightburn::Document::read(&xml, 0.005).unwrap();
    assert_eq!(doc.scene.format_version, 1);
    assert_eq!(xml.matches("<VertList>").count(), 2);
    assert_eq!(xml.matches("<PrimList>").count(), 2);
    assert!(xml.contains("Future=\"a &amp; b\""));
    assert!(xml.contains("StartV=\"1\""));
}

#[test]
fn svg_page_dimensions_and_dxf_width_warnings_reach_cli_imports() {
    let dir = temp("viewport-widths");
    let svg = dir.join("viewport.svg");
    let dxf = dir.join("width.dxf");
    fs::write(&svg, include_str!("../../core/tests/fixtures/viewport.svg")).unwrap();
    fs::write(
        &dxf,
        include_str!("../../core/tests/fixtures/polyline-width.dxf"),
    )
    .unwrap();
    let path = import(&dir, &[svg, dxf]);
    let library: Value = serde_json::from_slice(&fs::read(path).unwrap()).unwrap();
    assert_eq!(library["parts"].as_array().unwrap().len(), 2);
    for (value, expected) in library["parts"][0]["bounds_mm"]
        .as_array()
        .unwrap()
        .iter()
        .zip([65.4, -62.7, 85.4, -42.7])
    {
        assert!((value.as_f64().unwrap() - expected).abs() < 1e-9);
    }
    assert_eq!(
        library["parts"][1]["bounds_mm"],
        json!([0.0, 0.0, 10.0, 5.0])
    );
    assert!(
        library["warnings"]
            .as_array()
            .unwrap()
            .iter()
            .any(|w| w.as_str().unwrap().contains("polyline widths ignored"))
    );
}

#[test]
fn prearranged_sheet_is_discovered_and_used_without_nesting_the_boundary() {
    let dir = temp("imported-sheet");
    let source = dir.join("arranged.svg");
    fs::write(
        &source,
        include_str!("../../core/tests/fixtures/prearranged-sheet.svg"),
    )
    .unwrap();
    let library = dir.join("library.json");
    let imported = nestbolt(&[
        "import".as_ref(),
        source.as_os_str(),
        "--output".as_ref(),
        library.as_os_str(),
        "--sheet-layers".as_ref(),
        "SHEET".as_ref(),
    ]);
    assert!(
        imported.status.success(),
        "{}",
        String::from_utf8_lossy(&imported.stderr)
    );
    let response: Value = serde_json::from_slice(&imported.stdout).unwrap();
    assert_eq!(response["sheet_outlines"][0]["id"], "arranged-sheet-1");
    let disabled_library = dir.join("without-stock.json");
    let disabled = nestbolt(&[
        "import".as_ref(),
        source.as_os_str(),
        "--output".as_ref(),
        disabled_library.as_os_str(),
        "--sheet-layers".as_ref(),
    ]);
    assert!(
        disabled.status.success(),
        "{}",
        String::from_utf8_lossy(&disabled.stderr)
    );
    let disabled: Value = serde_json::from_slice(&disabled.stdout).unwrap();
    assert!(disabled["sheet_outlines"].as_array().unwrap().is_empty());
    let value: Value = serde_json::from_slice(&fs::read(&library).unwrap()).unwrap();
    assert_eq!(value["parts"].as_array().unwrap().len(), 2);
    assert_eq!(value["sheet_outlines"][0]["width_mm"], 200.0);
    let run = nest(
        &dir,
        &library,
        json!({"sheets":[{"from_import":"arranged-sheet-1","count":1}],"spacing_mm":1,"edge_spacing_mm":1}),
        "1",
    );
    assert_eq!(run.metrics()["placed_parts"], 2);
    assert_eq!(run.job["stocks"][0]["width"], 200.0);
    assert_eq!(
        run.job["stocks"][0]["outline"][0]["holes"]
            .as_array()
            .unwrap()
            .len(),
        1
    );
}

#[test]
fn explicit_gap_repair_reports_its_size_and_location() {
    let dir = temp("gap-repair");
    let source = dir.join("gap.svg");
    let library = dir.join("library.json");
    fs::write(&source,r#"<svg width="50mm" viewBox="0 0 50 50"><path id="outline" d="M0 0 H20 V20 H0 V0.2"/><rect x="30" width="10" height="10"/></svg>"#).unwrap();
    let failed = nestbolt(&[
        "import".as_ref(),
        source.as_os_str(),
        "--output".as_ref(),
        library.as_os_str(),
    ]);
    assert!(!failed.status.success());
    assert!(String::from_utf8_lossy(&failed.stderr).contains("Close gaps up to 0.200000 mm"));
    assert!(String::from_utf8_lossy(&failed.stderr).contains("no partial library was created"));
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
    assert_eq!(response["parts"].as_array().unwrap().len(), 2);
    assert_eq!(
        response["imports"][0]["report"]["closed_gaps"][0]["size_mm"],
        0.2
    );
    assert_eq!(
        response["imports"][0]["report"]["closed_gaps"][0]["from_mm"],
        json!([0.0, -0.2])
    );
}

#[test]
fn layers_and_colors_select_cuts_and_report_ignored_entities() {
    let dir = temp("layers");
    let source = dir.join("layers.svg");
    fs::write(&source,r##"<svg width="100mm" viewBox="0 0 100 100"><g id="CUT" stroke="black"><rect width="20" height="20"/></g><g id="SCORE" stroke="red"><rect x="40" width="10" height="10"/><text>label</text></g></svg>"##).unwrap();
    for (flag, value, expected_x) in [("--layers", "SCORE", 40.0), ("--colors", "#000000", 0.0)] {
        let out = dir.join(format!("{flag}.json"));
        let result = nestbolt(&[
            "import".as_ref(),
            source.as_os_str(),
            "--output".as_ref(),
            out.as_os_str(),
            flag.as_ref(),
            value.as_ref(),
        ]);
        assert!(
            result.status.success(),
            "{}",
            String::from_utf8_lossy(&result.stderr)
        );
        let library: Value = serde_json::from_slice(&fs::read(out).unwrap()).unwrap();
        assert_eq!(library["parts"][0]["bounds_mm"][0], expected_x);
        assert_eq!(library["parts"].as_array().unwrap().len(), 1);
        assert_eq!(
            library["imports"][0]["report"]["layers"]
                .as_array()
                .unwrap()
                .len(),
            2
        );
        assert!(
            library["warnings"]
                .as_array()
                .unwrap()
                .iter()
                .any(|w| w.as_str().unwrap().contains("text"))
        );
    }
}

#[test]
fn cleanup_counts_are_in_the_import_report() {
    let dir = temp("cleanup");
    let source = dir.join("cleanup.svg");
    fs::write(&source,r#"<svg width="100mm" viewBox="0 0 100 100"><path d="M0 0 H12 M8 0 H20 V20 H0 V0 M20 0 V20 M0 0 L0 0"/></svg>"#).unwrap();
    let library = import(&dir, &[source]);
    let value: Value = serde_json::from_slice(&fs::read(library).unwrap()).unwrap();
    assert_eq!(value["parts"].as_array().unwrap().len(), 1);
    assert_eq!(
        value["imports"][0]["report"]["cleanup"],
        json!({"duplicate_segments_removed":1,"zero_length_segments_removed":1,"overlapping_segments_merged":1})
    );
}

#[test]
fn closed_retraces_keep_holes_and_report_preserved_overlaps() {
    let dir = temp("closed-retrace");
    let source = dir.join("closed.svg");
    fs::write(
        &source,
        include_str!("../../core/tests/fixtures/closed-retrace.svg"),
    )
    .unwrap();
    let library = import(&dir, &[source]);
    let value: Value = serde_json::from_slice(&fs::read(library).unwrap()).unwrap();
    assert_eq!(value["parts"].as_array().unwrap().len(), 1);
    assert_eq!(value["parts"][0]["holes"].as_array().unwrap().len(), 1);
    assert_eq!(
        value["imports"][0]["report"]["cleanup"]["closed_path_overlaps_preserved"],
        2
    );
    assert!(
        value["warnings"]
            .as_array()
            .unwrap()
            .iter()
            .any(|w| w.as_str().unwrap().contains("keep closed paths connected"))
    );
}

#[test]
fn legacy_dxf_bytes_and_missing_units_are_explicit() {
    let dir = temp("encoding-units");
    let source = dir.join("legacy.dxf");
    let drawing = "0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n8\nCUT_Ø\n70\n1\n90\n4\n10\n0\n20\n0\n10\n20\n20\n0\n10\n20\n20\n10\n10\n0\n20\n10\n0\nENDSEC\n0\nEOF\n";
    fs::write(
        &source,
        drawing.chars().map(|c| c as u8).collect::<Vec<_>>(),
    )
    .unwrap();
    for (unit, width) in [("1", 20.0), ("25.4", 508.0)] {
        let out = dir.join(format!("units-{unit}.json"));
        let result = nestbolt(&[
            "import".as_ref(),
            source.as_os_str(),
            "--output".as_ref(),
            out.as_os_str(),
            "--layers".as_ref(),
            "CUT_Ø".as_ref(),
            "--dxf-unit-mm".as_ref(),
            unit.as_ref(),
        ]);
        assert!(
            result.status.success(),
            "{}",
            String::from_utf8_lossy(&result.stderr)
        );
        let library: Value = serde_json::from_slice(&fs::read(out).unwrap()).unwrap();
        assert_eq!(library["parts"][0]["bounds_mm"][2], width);
        assert_eq!(library["imports"][0]["report"]["units"]["declared"], false);
        assert_eq!(
            library["imports"][0]["report"]["units"]["possible_inches"],
            true
        );
    }
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
    assert!(svg.contains(r##"<g id="CUT" fill="none" stroke="#000000""##));
    assert!(dxf.contains("2\nCUT\n70\n0\n62\n7\n420\n0\n"));
    assert!(dxf.contains("\n8\nCUT\n62\n256\n"));
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
