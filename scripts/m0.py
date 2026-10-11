"""Build, run bounded/resumable M0 batches, and report the frozen reproduction."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import re
from statistics import mean, median, quantiles
import subprocess
import time
import uuid

from m0_reference import ROOT, MANIFEST, REVISION, digest, git_blob

ADAPTER = ROOT / "benchmarks/sparrow-repro"
TARGET = ROOT / ".cache/build/sparrow-published"
BINARY = TARGET / "release/nestbolt-sparrow-repro.exe"
CHECKOUT = ROOT / ".cache/upstream/sparrow-published"
OUTPUT_FILES = ("output/layout.json", "output/layout.svg", "stdout.log", "stderr.log")


def utc():
    return datetime.now(timezone.utc).isoformat()


def write_new(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as f:
        json.dump(value, f, indent=2)
        f.write("\n")


def command(args, **kwargs):
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding="utf-8", **kwargs).strip()


def append_log(text):
    with (ROOT / "BENCHMARKS.md").open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n" + text + "\n")


def build():
    if platform.system() != "Windows":
        raise SystemExit("This frozen M0 environment is native Windows; use a separate experiment for other platforms.")
    env = dict(os.environ, RUSTFLAGS="-C target-cpu=native", CARGO_TARGET_DIR=str(TARGET))
    subprocess.run(["cargo", "+nightly-2025-06-14", "build", "--release", "--locked",
        "--manifest-path", str(ADAPTER / "Cargo.toml"), "-j", "4"], cwd=ROOT, env=env, check=True)
    write_path = TARGET / "build.json"
    evidence = {"built_at": utc(), "binary_sha256": digest(BINARY),
        "sources": {str(p.relative_to(ROOT)).replace("\\", "/"): digest(p) for p in
                    [ADAPTER / "src/main.rs", ADAPTER / "Cargo.toml", ADAPTER / "Cargo.lock"]},
        "compiler": command(["rustc", "+nightly-2025-06-14", "--version", "--verbose"]),
        "flags": env["RUSTFLAGS"]}
    write_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Historical build recorded.")


def verify_build():
    evidence = json.loads((TARGET / "build.json").read_text(encoding="utf-8"))
    if evidence["binary_sha256"] != digest(BINARY):
        raise ValueError("Binary changed; build again before starting an experiment")
    for path, expected in evidence["sources"].items():
        if digest(ROOT / path) != expected:
            raise ValueError(f"Build is stale: {path}; run python scripts/m0.py build")
    return evidence


def materialize_input(instance):
    content = git_blob(CHECKOUT, REVISION, instance["input_path"])
    from hashlib import sha256
    if sha256(content).hexdigest() != instance["input_sha256"]:
        raise ValueError(f"Input changed: {instance['name']}")
    path = ROOT / ".cache/m0-inputs" / (instance["name"] + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != content:
        raise ValueError(f"Cached input was modified: {path}")
    if not path.exists():
        path.write_bytes(content)
    return path


def check_output(data, instance, finished):
    """Integrity only. The separate geometry validator is an M1 requirement."""
    solution = data["solution"]
    width, density = solution["strip_width"], solution["density"]
    if not (math.isfinite(width) and width > 0 and math.isfinite(density) and 0 < density <= 1.000001):
        raise ValueError("Invalid width or density")
    if not math.isclose(width, finished["strip_width"], rel_tol=1e-6):
        raise ValueError("JSON and process metrics disagree")
    if not math.isclose(density, finished["density"], rel_tol=1e-6):
        raise ValueError("JSON and process density disagree")
    if data["name"] != instance["name"] or not math.isclose(data["strip_height"], instance["strip_height"], rel_tol=1e-6):
        raise ValueError("Output describes another instance")
    placed = solution["layout"]["placed_items"]
    source = json.loads(materialize_input(instance).read_text(encoding="utf-8"))
    demand = Counter({i["id"]: i["demand"] for i in source["items"]})
    if Counter(p["item_id"] for p in placed) != demand:
        raise ValueError("Output quantities differ from the frozen input")
    for part in placed:
        transform = part["transformation"]
        values = [transform["rotation"], *transform["translation"]]
        if len(values) != 3 or not all(math.isfinite(x) for x in values):
            raise ValueError("Nonfinite or malformed placement")
    return {"strip_width": width, "density": density, "placed_count": len(placed)}


def run_one(experiment, instance, index, seconds):
    path = experiment / f"{instance['name']}-{index}"
    path.mkdir()  # Never replace an earlier attempt, including a failed attempt.
    seed = instance["archives"][0]["archive_seed"]
    input_path = materialize_input(instance)
    argv = [str(BINARY), str(input_path), str(seconds), seed, str(index)]
    started = utc()
    begin = time.monotonic()
    record = {"started_at": started, "instance": instance["name"], "run_index": index,
        "archive_seed": seed, "seconds": seconds, "workers": 3, "command": argv,
        "input_sha256": digest(input_path), "status": "failed"}
    write_new(path / "started.json", record)
    try:
        with (path / "stdout.log").open("w", encoding="utf-8") as out, (path / "stderr.log").open("w", encoding="utf-8") as err:
            process = subprocess.run(argv, cwd=path, env=dict(os.environ, RAYON_NUM_THREADS="3"),
                stdout=out, stderr=err, timeout=seconds + 120)
        record["exit_code"] = process.returncode
        if process.returncode:
            raise ValueError(f"Solver exited {process.returncode}; see stderr.log")
        messages = [json.loads(line) for line in (path / "stdout.log").read_text(encoding="utf-8").splitlines() if line.startswith("{")]
        start = next(m for m in messages if m["phase"] == "start")
        finish = next(m for m in messages if m["phase"] == "finished")
        record["derived_run_seed"] = start["derived_run_seed"]
        data = json.loads((path / "output/layout.json").read_text(encoding="utf-8"))
        record.update(check_output(data, instance, finish))
        record["status"] = "completed_integrity_checked"
        record["independent_geometry_validated"] = False
        record["outputs"] = {p: digest(path / p) for p in OUTPUT_FILES}
    except Exception as error:
        record["error"] = str(error)
    record.update(finished_at=utc(), wall_seconds=time.monotonic() - begin)
    write_new(path / "run.json", record)
    return record, path


def run(args):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,70}", args.experiment):
        raise ValueError("Experiment name must contain only letters, numbers, dashes or underscores")
    if not 1 <= args.parallel <= 3 or not 1 <= args.max_runs <= 18:
        raise ValueError("Use 1..3 simultaneous runs and at most 18 runs per bounded session")
    reference = json.loads(MANIFEST.read_text(encoding="utf-8"))
    build_evidence = verify_build()
    path = ROOT / "output/m0" / args.experiment
    path.mkdir(parents=True, exist_ok=True)
    settings = {"reference_sha256": digest(MANIFEST), "build": build_evidence,
        "seconds": 5 if args.smoke else reference["method"]["seconds"], "smoke": args.smoke,
        "source_hashes": {p: digest(ROOT / p) for p in ("scripts/m0.py", "scripts/m0_reference.py")}}
    metadata = path / "experiment.json"
    if metadata.exists():
        existing = json.loads(metadata.read_text(encoding="utf-8"))
        if any(existing[k] != v for k, v in settings.items()):
            raise ValueError("Experiment environment changed; use a new name, preserving previous evidence")
    else:
        write_new(metadata, {**settings, "started_at": utc(), "commit": command(["git", "rev-parse", "HEAD"]),
            "dirty": bool(command(["git", "status", "--porcelain"])), "platform": platform.platform(),
            "cpu": command(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor).Name"])})
        append_log(f"- {utc()} | M0 experiment `{args.experiment}` opened | [metadata]({metadata.relative_to(ROOT).as_posix()}) | {'5s smoke only' if args.smoke else 'frozen 39-run quality reproduction; 1200s, 3 workers each'}. No pass claimed.")
    pending = []
    # Interleave datasets: every dataset gets its first seed before second seeds.
    for index in reference["method"]["run_indices"]:
        for instance in reference["instances"]:
            run_path = path / f"{instance['name']}-{index}"
            if run_path.exists():
                if not (run_path / "run.json").exists():
                    raise ValueError(f"Interrupted run preserved at {run_path}; resolve before continuing")
                continue
            pending.append((instance, index))
    # Bound the session to <3 hours including the process timeout, at any concurrency.
    capacity = max(1, int((3 * 3600 - 60) / (settings["seconds"] + 120))) * args.parallel
    pending = pending[:min(args.max_runs, capacity)]
    if not pending:
        print("No unattempted runs remain; generate a report.")
        return
    session = path / ("session-" + uuid.uuid4().hex[:10] + ".json")
    write_new(session, {"started_at": utc(), "parallel": args.parallel,
        "runs": [f"{i['name']}-{n}" for i, n in pending], "maximum_worker_count": args.parallel * 3})
    print(f"Started {len(pending)} runs, {args.parallel} at a time. Evidence: {path}", flush=True)
    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = [pool.submit(run_one, path, instance, index, settings["seconds"]) for instance, index in pending]
        for future in as_completed(futures):
            record, run_path = future.result()
            label = f"{record['instance']}-{record['run_index']}"
            append_log(f"- {record['finished_at']} | M0 `{args.experiment}/{label}` | {record['status']} | {record['seconds']}s, 3 workers | length {record.get('strip_width', 'unavailable')} | [record]({(run_path / 'run.json').relative_to(ROOT).as_posix()}). Geometry validation pending M1.")
            print(f"{label}: {record['status']}, length={record.get('strip_width', 'unavailable')}", flush=True)
    report(args)


def score_widths(widths, expected_count, reference_width, tolerance, smoke):
    if any(not math.isfinite(w) or w <= 0 for w in widths):
        raise ValueError("Cannot score nonfinite or nonpositive lengths")
    relative = mean(widths) / reference_width - 1 if widths else None
    passed = len(widths) == expected_count and not smoke and abs(relative) <= tolerance
    return relative, passed


def report(args):
    reference = json.loads(MANIFEST.read_text(encoding="utf-8"))
    path = ROOT / "output/m0" / args.experiment
    metadata = json.loads((path / "experiment.json").read_text(encoding="utf-8"))
    if metadata["reference_sha256"] != digest(MANIFEST):
        raise ValueError("Reference manifest differs from the experiment")
    rows = []
    for instance in reference["instances"]:
        records = []
        for index in reference["method"]["run_indices"]:
            record_path = path / f"{instance['name']}-{index}/run.json"
            if record_path.exists():
                record = json.loads(record_path.read_text(encoding="utf-8"))
                if (record["instance"] != instance["name"] or record["run_index"] != index
                        or record["seconds"] != metadata["seconds"] or record["workers"] != 3
                        or record["archive_seed"] != instance["archives"][0]["archive_seed"]
                        or record["input_sha256"] != instance["input_sha256"]):
                    raise ValueError(f"Run metadata differs from the experiment: {record_path}")
                if record["status"] == "completed_integrity_checked" and set(record.get("outputs", {})) != set(OUTPUT_FILES):
                    raise ValueError(f"Completed run lacks output evidence: {record_path}")
                for output, expected in record.get("outputs", {}).items():
                    if digest(record_path.parent / output) != expected:
                        raise ValueError(f"Output changed after recording: {record_path.parent / output}")
                if record["status"] == "completed_integrity_checked":
                    data = json.loads((record_path.parent / "output/layout.json").read_text(encoding="utf-8"))
                    check_output(data, instance, record)
                records.append(record)
        widths = [r["strip_width"] for r in records if r["status"] == "completed_integrity_checked"]
        relative, passed = score_widths(widths, len(reference["method"]["run_indices"]),
            instance["reference_mean_width"], reference["method"]["maximum_relative_difference"], metadata["smoke"])
        rows.append({"instance": instance["paper_name"], "completed": len(widths), "attempted": len(records),
            "reference_mean_width": instance["reference_mean_width"],
            "mean_width": mean(widths) if widths else None, "median_width": median(widths) if widths else None,
            "quartiles": quantiles(widths, n=4, method="inclusive") if len(widths) >= 2 else None,
            "relative_difference": relative,
            "pass": passed})
    result = {"generated_at": utc(), "experiment": args.experiment, "reference_sha256": digest(MANIFEST),
        "complete": all(r["completed"] == 3 for r in rows), "pass": all(r["pass"] for r in rows),
        "scope": reference["method"]["purpose"], "rows": rows}
    output = path / ("report-" + uuid.uuid4().hex[:10] + ".json")
    write_new(output, result)
    print(json.dumps({"completed_runs": sum(r["completed"] for r in rows), "required_runs": 39,
        "passing_instances": sum(r["pass"] for r in rows), "required_instances": 13,
        "pass": result["pass"], "report": str(output)}, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("build")
    for name in ("run", "report"):
        child = sub.add_parser(name)
        child.add_argument("--experiment", required=True)
        if name == "run":
            child.add_argument("--parallel", type=int, default=3)
            child.add_argument("--max-runs", type=int, default=18)
            child.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.action == "build":
        build()
    elif args.action == "run":
        lock = ROOT / ".cache/m0-active.lock"
        lock.parent.mkdir(parents=True, exist_ok=True)
        write_new(lock, {"pid": os.getpid(), "started_at": utc(), "experiment": args.experiment})
        try:
            run(args)
        finally:
            lock.unlink()
    else:
        report(args)


if __name__ == "__main__":
    main()
