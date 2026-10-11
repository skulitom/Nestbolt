use std::{
    fs,
    process::Command,
    time::{SystemTime, UNIX_EPOCH},
};

const JOB: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../../examples/validation-job.json"
);
const LAYOUT: &str = concat!(
    env!("CARGO_MANIFEST_DIR"),
    "/../../examples/validation-layout.json"
);

#[test]
fn validates_nested_example_and_prints_independently_computed_metrics() {
    let result = Command::new(env!("CARGO_BIN_EXE_nestbolt"))
        .args(["validate", "--job", JOB, "--layout", LAYOUT])
        .output()
        .unwrap();
    assert!(
        result.status.success(),
        "{}",
        String::from_utf8_lossy(&result.stderr)
    );
    let report: serde_json::Value = serde_json::from_slice(&result.stdout).unwrap();
    assert_eq!(report["valid"], true);
    assert_eq!(report["metrics"]["placed_parts"], 4);
    assert_eq!(report["metrics"]["placed_area"], 2250.0);
}

#[test]
fn invalid_layout_has_a_failing_exit_code_and_no_quality_score() {
    let mut layout: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(LAYOUT).unwrap()).unwrap();
    layout["placements"].as_array_mut().unwrap().pop();
    let unique = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let path = std::env::temp_dir().join(format!(
        "nestbolt-layout-test-{}-{unique}.json",
        std::process::id()
    ));
    let file = fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&path)
        .unwrap();
    serde_json::to_writer(file, &layout).unwrap();
    let result = Command::new(env!("CARGO_BIN_EXE_nestbolt"))
        .args(["validate", "--job", JOB, "--layout"])
        .arg(&path)
        .output()
        .unwrap();
    fs::remove_file(path).unwrap();
    assert!(!result.status.success());
    let report: serde_json::Value = serde_json::from_slice(&result.stdout).unwrap();
    assert_eq!(report["valid"], false);
    assert!(report["metrics"].is_null());
}
