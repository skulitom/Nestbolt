"""Build unmodified pinned jagua-rs LBF and independently validate bounded runs."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import time
import uuid

from benchmark_io import UnsupportedJob, jagua_input, jagua_layout
from svgnest import guard_held_out

ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "benchmarks/lbf/tool.json"
CHECKOUT = ROOT / ".cache/upstream/jagua-rs"
TARGET = ROOT / ".cache/build/lbf"
BUILD = TARGET / "build.json"
SOURCES = ['scripts/lbf.py', 'scripts/benchmark_io.py', 'scripts/dataset_selection.py',
           'scripts/svgnest.py', 'scripts/svgnest_io.py', 'scripts/svg_export_transform.py']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def lock_digest():
    return sha256((CHECKOUT / "Cargo.lock").read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def command(args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, text=True, encoding="utf-8").strip()


def write_new(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2, allow_nan=False)
        handle.write("\n")


def tool_metadata():
    return json.loads(TOOL_PATH.read_bytes())


def binary_path():
    return TARGET / "release" / ("lbf.exe" if os.name == "nt" else "lbf")


def check_checkout(tool):
    if command(["git", "rev-parse", "HEAD"], CHECKOUT) != tool["revision"]:
        raise ValueError("Cached jagua-rs is not at the pinned LBF revision")
    if command(["git", "status", "--porcelain", "--untracked-files=no"], CHECKOUT):
        raise ValueError("Cached jagua-rs has tracked changes; preserve them before using a clean checkout")
    if lock_digest() != tool["cargo_lock_sha256"]:
        raise ValueError("Upstream LBF dependency lock differs from the pinned version")


def build():
    tool = tool_metadata()
    if not CHECKOUT.exists():
        CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--no-checkout", "--filter=blob:none", tool["repository"], str(CHECKOUT)], check=True)
        subprocess.run(["git", "-C", str(CHECKOUT), "checkout", "--detach", tool["revision"]], check=True)
    check_checkout(tool)
    env = {**os.environ, "CARGO_BUILD_JOBS": "4", "CARGO_TARGET_DIR": str(TARGET), "RUSTFLAGS": tool["rustflags"]}
    subprocess.run(["cargo", "+" + tool["rust_toolchain"], "build", "--release", "--locked", "--bin", "lbf",
        "--manifest-path", str(CHECKOUT / "Cargo.toml")], cwd=ROOT, env=env, check=True)
    record = {"tool_sha256": digest(TOOL_PATH), "binary_sha256": digest(binary_path()),
        "revision": tool["revision"], "cargo_lock_sha256": lock_digest(),
        "cargo_lock_worktree_sha256": digest(CHECKOUT / "Cargo.lock"),
        "rustc": command(["rustc", "+" + tool["rust_toolchain"], "-vV"]),
        "rustflags": tool["rustflags"], "built_at": datetime.now(timezone.utc).isoformat()}
    # Build metadata is a cache. Each actual run retains a complete copy.
    BUILD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Built pinned LBF: {binary_path()}")


def built_tool():
    tool = tool_metadata()
    check_checkout(tool)
    record = json.loads(BUILD.read_bytes())
    if record["tool_sha256"] != digest(TOOL_PATH) or record["binary_sha256"] != digest(binary_path()):
        raise ValueError("LBF build cache changed; run the explicit build command")
    return tool, record


def run(job_path, seconds, seed, settings, batch_id=None, verbose=True, phase='development'):
    tool, build_record = built_tool()
    job = json.loads(job_path.read_bytes())
    guard_held_out(job, phase)
    identifier = re.sub(r"[^A-Za-z0-9_-]", "-", job["name"])[:70]
    timestamp = datetime.now(timezone.utc)
    run_id = f"{timestamp:%Y%m%dT%H%M%SZ}-{identifier}-{settings}-s{seed}-{uuid.uuid4().hex[:8]}"
    directory = ROOT / "output/lbf" / run_id
    directory.mkdir(parents=True, exist_ok=False)
    # Preserve the source even if a caller later edits or moves it.
    (directory / "job.json").write_bytes(job_path.read_bytes())
    write_new(directory / "empty-layout.json", {"version": 1, "units": job["units"], "sheets": [], "placements": []})
    validator = ROOT / "target/debug" / ("nestbolt.exe" if os.name == "nt" else "nestbolt")
    record = {"run_id": run_id, "batch_id": batch_id, "kind": "provisional_lbf_baseline", "started_at": timestamp.isoformat(),
        "job_name": job["name"], "job_sha256": digest(job_path), "job_source_path": str(job_path),
        "tool": tool, "build": build_record, "seed": seed, "seconds_limit": seconds, "settings": settings,
        "workers": 1, "rayon_threads": 1, "nestbolt_commit": command(["git", "rev-parse", "HEAD"]),
        "dirty": bool(command(["git", "status", "--porcelain"])),
        "adapter_sources": {name: digest(ROOT / name) for name in SOURCES}, "phase":phase,
        "validator_binary_sha256": digest(validator), "status": "failed", "metrics": None,
        "platform": platform.platform(), "cpu": cpu_name(), "quality_gate": "not_evaluated"}
    started = time.monotonic()
    try:
        # A normal empty-layout report has quantity failures only; an invalid
        # original job instead produces a parse/geometry error without a report.
        probe = subprocess.run([str(validator), "validate", "--job", str(directory / "job.json"),
            "--layout", str(directory / "empty-layout.json")], capture_output=True, text=True, encoding="utf-8", timeout=30)
        source_report = json.loads(probe.stdout)
        if any(v["code"] != "quantity" for v in source_report["violations"]):
            raise ValueError("Source job failed independent contract checks")
        write_new(directory / "input.json", jagua_input(job))
        config = {**tool["settings"][settings], "prng_seed": seed}
        write_new(directory / "config.json", config)
        argv = [str(binary_path()), "--input-file", str(directory / "input.json"), "--prob-var", "bpp",
            "--solution-folder", str(directory / "solver"), "--config-file", str(directory / "config.json")]
        record["command"] = argv
        write_new(directory / "start.json", record)
        solve_started = time.monotonic()
        try:
            with (directory / "stdout.log").open("wb") as out, (directory / "stderr.log").open("wb") as err:
                process = subprocess.run(argv, cwd=directory, stdout=out, stderr=err,
                    env={**os.environ, "RAYON_NUM_THREADS": "1"}, timeout=seconds)
            record["solver_exit_code"] = process.returncode
        finally:
            record["solver_wall_seconds"] = time.monotonic() - solve_started
        if process.returncode:
            raise RuntimeError(f"LBF exited with {process.returncode}; inspect stderr.log")
        output = json.loads((directory / "solver/sol_input.json").read_bytes())
        write_new(directory / "layout.json", jagua_layout(job, output))
        validation = subprocess.run([str(validator), "validate", "--job", str(directory / "job.json"),
            "--layout", str(directory / "layout.json")], capture_output=True, text=True, encoding="utf-8", timeout=60)
        report = json.loads(validation.stdout)
        write_new(directory / "validation.json", report)
        record["validator_exit_code"] = validation.returncode
        record["status"] = "valid" if report["valid"] and validation.returncode == 0 else "invalid"
        if record["status"] == "valid":
            record["metrics"] = report["metrics"]
    except UnsupportedJob as error:
        record.update(status="unsupported", error=str(error))
    except subprocess.TimeoutExpired as error:
        record.update(status="timeout", error=f"Process exceeded {error.timeout}s: {Path(error.cmd[0]).name}")
    except Exception as error:
        record["error"] = f"{type(error).__name__}: {error}"
    finally:
        record["elapsed_seconds"] = time.monotonic() - started
        record["finished_at"] = datetime.now(timezone.utc).isoformat()
        record["outputs"] = {p.relative_to(directory).as_posix(): digest(p)
            for p in sorted(directory.rglob("*")) if p.is_file()}
        write_new(directory / "run.json", record)
        with (ROOT / "BENCHMARKS.md").open("a", encoding="utf-8", newline="\n") as log:
            relative = directory.relative_to(ROOT).as_posix()
            score = record["metrics"]["normalized_material"] if record["metrics"] else "none"
            log.write(f"\n- {timestamp.isoformat()} | `{run_id}` | LBF `{tool['revision']}` | "
                f"Nestbolt `{record['nestbolt_commit']}` (dirty={record['dirty']}) | "
                f"seed {seed}, {seconds}s limit, one pass/one worker, {settings} | {record['status']}; "
                f"independent material {score} | [record]({relative}/run.json). Provisional M1 baseline, no quality-gate claim.\n")
    if verbose:
        print(json.dumps({"job": job["name"], "status": record["status"], "metrics": record["metrics"],
            "error": record.get("error"), "record": str(directory / "run.json")}, indent=2))
    else:
        print(f"{job['name']} / {settings}: {record['status']}", flush=True)
    return record


def batch(seconds, seed, settings, dataset='B'):
    from dataset_selection import development_cases
    if dataset == 'M':
        from maker_freeze import DEST, check_frozen
    else:
        from datasets import DEST, check_frozen
    check_frozen()
    manifest, rows = development_cases(ROOT, dataset)
    variants = ["identical", "upstream-default"] if settings == "both" else [settings]
    if len(rows) * len(variants) * (seconds + 90) > 3 * 3600:
        raise ValueError("Batch could exceed three hours including validation; reduce the budget or select one setting")
    tool, build_record = built_tool()
    batch_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:8]
    directory = ROOT / "output/lbf-batches" / batch_id
    directory.mkdir(parents=True, exist_ok=False)
    record = {"batch_id": batch_id, "kind": "provisional_lbf_baseline", "tool": tool, "build": build_record,
        "dataset":dataset, "cases":rows, "adapter_sources":{name:digest(ROOT/name) for name in SOURCES},
        "dataset_manifest_sha256": digest(manifest), "seed": seed, "seconds_limit": seconds,
        "settings": variants, "expected_runs": len(rows) * len(variants), "complete": False, "runs": []}
    write_new(directory / "start.json", record)
    for row in rows:
        for variant in variants:
            if any(digest(ROOT/name) != checksum for name,checksum in record['adapter_sources'].items()):
                raise ValueError('Runner changed during batch; incomplete evidence retained')
            if digest(DEST/row['path']) != row['sha256']:
                raise ValueError('Frozen source changed')
            result = run(DEST / row["path"], seconds, seed, variant, batch_id=batch_id, verbose=False)
            path = ROOT / "output/lbf" / result["run_id"] / "run.json"
            entry = {"job": row["id"], "settings": variant, "status": result["status"],
                "record": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}
            record['runs'].append(entry)
            with (directory/'runs.jsonl').open('a',encoding='utf-8',newline='\n') as f:
                f.write(json.dumps(entry)+'\n')
    record["complete"] = True  # all attempts recorded; failures are still failures
    record["valid_runs"] = sum(row["status"] == "valid" for row in record["runs"])
    write_new(directory / "batch.json", record)
    print(f"Batch complete: {record['valid_runs']}/{record['expected_runs']} valid. Evidence: {directory / 'batch.json'}")
    return record


def cpu_name():
    if os.name == "nt":
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
            return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
    return platform.processor() or "unknown"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="action", required=True)
    subs.add_parser("build")
    run_parser = subs.add_parser("run")
    run_parser.add_argument("--job", type=Path, required=True)
    run_parser.add_argument("--seconds", type=int, default=60)
    run_parser.add_argument("--seed", type=int, default=0)
    run_parser.add_argument("--settings", choices=["identical", "upstream-default"], default="identical")
    run_parser.add_argument('--phase', choices=['development','final'],default='development')
    batch_parser = subs.add_parser("batch", help="One bounded development pass over frozen B or non-held-out M jobs")
    batch_parser.add_argument("--seconds", type=int, default=60)
    batch_parser.add_argument("--seed", type=int, default=0)
    batch_parser.add_argument("--settings", choices=["identical", "upstream-default", "both"], default="both")
    batch_parser.add_argument('--dataset',choices=['B','M'],default='B')
    args = parser.parse_args()
    if args.action == "build":
        build()
    else:
        if not 1 <= args.seconds <= 300 or not 0 <= args.seed <= 2**64 - 1:
            parser.error("seconds must be in 1..300 and seed must fit u64")
        subprocess.run(["cargo", "build", "--locked", "-p", "nestbolt-cli"], cwd=ROOT, check=True)
        if args.action == "batch":
            result = batch(args.seconds, args.seed, args.settings,args.dataset)
            if result["valid_runs"] != result["expected_runs"]:
                raise SystemExit(1)
        else:
            result = run(args.job.resolve(strict=True), args.seconds, args.seed, args.settings,phase=args.phase)
            if result["status"] != "valid":
                raise SystemExit(1)


if __name__ == "__main__":
    main()
