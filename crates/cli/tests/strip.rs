use std::{
    fs,
    process::Command,
    time::{SystemTime, UNIX_EPOCH},
};

#[test]
fn strip_cli_writes_a_valid_layout_and_preserves_existing_files() {
    let stamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let directory =
        std::env::temp_dir().join(format!("nestbolt-strip-{}-{stamp}", std::process::id()));
    fs::create_dir(&directory).unwrap();
    let job = directory.join("job.json");
    let layout = directory.join("layout.json");
    fs::write(&job,serde_json::to_vec(&serde_json::json!({
        "version":1,"name":"cli strip","units":"mm","mode":"all","clearance":0,"edge_clearance":0,
        "parts":[{"id":"square","quantity":2,"geometry":[{"outer":[[0,0],[2,0],[2,2],[0,2]],"holes":[]}],
                  "rotations":{"kind":"list","degrees":[0]},"allow_mirror":false,"priority":1}],
        "stocks":[{"id":"stock","width":100,"height":5,"count":1,
                   "margins":{"left":0,"right":0,"top":0,"bottom":0},"outline":[],"defects":[]}]
    })).unwrap()).unwrap();
    let run = || {
        Command::new(env!("CARGO_BIN_EXE_nestbolt"))
            .args(["strip", "--job"])
            .arg(&job)
            .arg("--output")
            .arg(&layout)
            .args(["--seconds", "1"])
            .env("RAYON_NUM_THREADS", "1")
            .output()
            .unwrap()
    };
    let first = run();
    assert!(
        first.status.success(),
        "{}",
        String::from_utf8_lossy(&first.stderr)
    );
    let report: serde_json::Value = serde_json::from_slice(&first.stdout).unwrap();
    assert_eq!(report["validation"]["valid"], true);
    assert!(report["accepted_at_seconds"].as_f64().unwrap() <= 1.0);
    let saved = fs::read(&layout).unwrap();
    let second = run();
    assert!(!second.status.success());
    assert_eq!(saved, fs::read(&layout).unwrap());
    let check = Command::new(env!("CARGO_BIN_EXE_nestbolt"))
        .args(["validate", "--job"])
        .arg(&job)
        .arg("--layout")
        .arg(&layout)
        .output()
        .unwrap();
    assert!(check.status.success());
    fs::remove_file(layout).unwrap();
    fs::remove_file(job).unwrap();
    fs::remove_dir(directory).unwrap();
}
