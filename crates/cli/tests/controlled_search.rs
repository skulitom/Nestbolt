use std::{
    fs,
    path::PathBuf,
    process::Command,
    time::{SystemTime, UNIX_EPOCH},
};

fn output_path() -> PathBuf {
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    std::env::temp_dir().join(format!(
        "nestbolt-controlled-{}-{stamp}.json",
        std::process::id()
    ))
}

fn command(path: &PathBuf) -> Command {
    let mut command = Command::new(env!("CARGO_BIN_EXE_nestbolt"));
    command.args([
        "improve",
        "--job",
        concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../examples/validation-job.json"
        ),
        "--output",
    ]);
    command.arg(path);
    command
}

#[test]
fn work_limit_writes_only_the_last_valid_completed_layout() {
    let initial_path = output_path();
    let initial = command(&initial_path)
        .args(["--passes", "1"])
        .output()
        .unwrap();
    assert!(
        initial.status.success(),
        "{}",
        String::from_utf8_lossy(&initial.stderr)
    );
    let initial: serde_json::Value = serde_json::from_slice(&initial.stdout).unwrap();
    let stopped_path = output_path();
    let stopped = command(&stopped_path)
        .args([
            "--passes",
            "64",
            "--max-checks",
            &(initial["collision_checks"].as_u64().unwrap() + 1).to_string(),
        ])
        .output()
        .unwrap();
    assert!(
        stopped.status.success(),
        "{}",
        String::from_utf8_lossy(&stopped.stderr)
    );
    let stopped: serde_json::Value = serde_json::from_slice(&stopped.stdout).unwrap();
    assert_eq!(stopped["stopped"], "work_limit");
    assert_eq!(stopped["completed_passes"], 1);
    assert_eq!(stopped["validation"]["valid"], true);
    assert_eq!(
        fs::read(&initial_path).unwrap(),
        fs::read(&stopped_path).unwrap()
    );
    fs::remove_file(initial_path).unwrap();
    fs::remove_file(stopped_path).unwrap();
}

#[test]
fn stopping_before_a_layout_exists_does_not_create_an_output_file() {
    let path = output_path();
    let result = command(&path).args(["--max-checks", "0"]).output().unwrap();
    assert!(!result.status.success());
    assert!(result.stdout.is_empty());
    assert!(!path.exists());
    assert!(String::from_utf8_lossy(&result.stderr).contains("WorkLimit"));
    let result = command(&path).args(["--timeout-ms", "0"]).output().unwrap();
    assert!(!result.status.success());
    assert!(!path.exists());
}
