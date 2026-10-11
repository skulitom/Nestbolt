use std::process::Command;

#[test]
fn inspect_prints_machine_readable_json() {
    let result = Command::new(env!("CARGO_BIN_EXE_nestbolt"))
        .args([
            "inspect",
            "--input",
            concat!(env!("CARGO_MANIFEST_DIR"), "/../../examples/sheet-job.json"),
            "--units",
            "mm",
        ])
        .output()
        .unwrap();
    assert!(
        result.status.success(),
        "{}",
        String::from_utf8_lossy(&result.stderr)
    );
    let report: serde_json::Value = serde_json::from_slice(&result.stdout).unwrap();
    assert_eq!(report["total_parts"], 6);
    assert_eq!(report["units"], "mm");
}

#[test]
fn missing_input_fails_cleanly() {
    let result = Command::new(env!("CARGO_BIN_EXE_nestbolt"))
        .args(["inspect", "--input", "does-not-exist.json", "--units", "mm"])
        .output()
        .unwrap();
    assert!(!result.status.success());
    assert!(String::from_utf8_lossy(&result.stderr).contains("cannot read"));
    assert!(result.stdout.is_empty());
}
