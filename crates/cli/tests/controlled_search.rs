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

#[test]
fn incomplete_stopped_search_skips_the_followup_fit_scan() {
    let mut job: serde_json::Value =
        serde_json::from_str(include_str!("../../../examples/validation-job.json")).unwrap();
    job["parts"][0]["geometry"] = serde_json::json!([{
        "outer": [[0, 0], [10000, 0], [10000, 10], [0, 10]], "holes": []
    }]);
    let job_path = output_path();
    let layout_path = output_path();
    fs::write(&job_path, serde_json::to_vec(&job).unwrap()).unwrap();
    let run = |args: &[&str]| {
        Command::new(env!("CARGO_BIN_EXE_nestbolt"))
            .args(["improve", "--job"])
            .arg(&job_path)
            .arg("--output")
            .arg(&layout_path)
            .args(args)
            .output()
            .unwrap()
    };
    let initial = run(&["--passes", "1"]);
    assert!(!initial.status.success());
    assert!(String::from_utf8_lossy(&initial.stderr).contains("part frame does not fit"));
    let report: serde_json::Value = serde_json::from_slice(&initial.stdout).unwrap();
    let checks = report["collision_checks"].as_u64().unwrap().to_string();
    let stopped = run(&["--passes", "2", "--max-checks", &checks]);
    assert!(!stopped.status.success());
    let report: serde_json::Value = serde_json::from_slice(&stopped.stdout).unwrap();
    assert_eq!(report["stopped"], "work_limit");
    assert!(String::from_utf8_lossy(&stopped.stderr).contains("no complete validated layout"));
    assert!(!layout_path.exists());
    fs::remove_file(job_path).unwrap();
}
