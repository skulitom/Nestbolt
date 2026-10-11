"""Verify every recorded byte before retaining an LBF batch table/checkpoint."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from lbf import ROOT, digest, write_new


def contained_file(directory, relative):
    path = (directory / relative).resolve()
    if not path.is_relative_to(directory.resolve()) or not path.is_file():
        raise ValueError(f"Invalid evidence path: {relative}")
    return path


def audit_record(path, expected_hash):
    if digest(path) != expected_hash:
        raise ValueError(f"Run record changed: {path}")
    record = json.loads(path.read_bytes())
    for relative, expected in record["outputs"].items():
        if digest(contained_file(path.parent, relative)) != expected:
            raise ValueError(f"Recorded output changed: {path.parent.name}/{relative}")
    if digest(path.parent / "job.json") != record["job_sha256"]:
        raise ValueError("Original job differs from the run's copied source")
    if record["status"] == "valid":
        for required in ["validation.json", "layout.json", "job.json", "solver/sol_input.json"]:
            if required not in record["outputs"]:
                raise ValueError("Valid result is missing its independent evidence")
        report = json.loads((path.parent / "validation.json").read_bytes())
        if not report["valid"] or record["validator_exit_code"] != 0 or record["metrics"] != report["metrics"]:
            raise ValueError("Run score disagrees with its independent validation")
    elif record["metrics"] is not None:
        raise ValueError("Failed run must not receive a score")
    return record


def report(batch_path):
    batch = json.loads(batch_path.read_bytes())
    manifest_path = ROOT / "benchmarks/datasets/academic.json"
    if digest(manifest_path) != batch["dataset_manifest_sha256"]:
        raise ValueError("Batch dataset manifest changed")
    cases = {r["id"]: r for r in json.loads(manifest_path.read_bytes())["instances"] if r["set"] == "B"}
    expected = {(name, setting) for name in cases for setting in batch["settings"]}
    seen, rows, sources = set(), [], set()
    for entry in batch["runs"]:
        key = (entry["job"], entry["settings"])
        if key not in expected or key in seen:
            raise ValueError("Batch has an unexpected or duplicate job/setting")
        path = contained_file(ROOT, entry["record"])
        if not path.is_relative_to((ROOT / "output/lbf").resolve()):
            raise ValueError("Run record must belong to the LBF output directory")
        run = audit_record(path, entry["sha256"])
        if (run["job_name"], run["settings"]) != key or run["job_sha256"] != cases[key[0]]["sha256"]:
            raise ValueError("Run does not match its frozen job/setting")
        for name in ["batch_id", "tool", "build", "seed", "seconds_limit"]:
            if run[name] != batch[name]:
                raise ValueError(f"Run differs from batch metadata: {name}")
        if run["status"] != entry["status"]:
            raise ValueError("Batch status disagrees with the run record")
        if run["workers"] != 1 or run["rayon_threads"] != 1:
            raise ValueError("LBF batch was not configured for one worker")
        if digest(ROOT / "benchmarks/datasets" / cases[key[0]]["path"]) != run["job_sha256"]:
            raise ValueError("Frozen source job was modified")
        sources.add(json.dumps(run["adapter_sources"], sort_keys=True))
        rows.append({**entry, "metrics": run["metrics"], "error": run.get("error"),
            "solver_wall_seconds": run.get("solver_wall_seconds"),
            "validator_binary_sha256": run["validator_binary_sha256"],
            "nestbolt_commit": run["nestbolt_commit"], "dirty": run["dirty"],
            "cpu": run["cpu"], "platform": run["platform"]})
        seen.add(key)
    if not batch["complete"] or seen != expected or len(seen) != batch["expected_runs"]:
        raise ValueError("Batch is incomplete; no complete baseline table can be produced")
    if len(sources) != 1:
        raise ValueError("Adapter code changed during the batch")
    stamp = datetime.now(timezone.utc)
    checkpoint = {"recorded_at": stamp.isoformat(), "kind": "provisional_lbf_baseline",
        "scope": "One development seed, B only, one-pass LBF. Not a complete M1 baseline or a quality gate.",
        "batch_sha256": digest(batch_path), "batch_id": batch["batch_id"],
        "dataset_manifest_sha256": batch["dataset_manifest_sha256"], "tool": batch["tool"], "build": batch["build"],
        "seed": batch["seed"], "seconds_limit": batch["seconds_limit"],
        "adapter_sources": json.loads(next(iter(sources))),
        "valid_runs": sum(r["status"] == "valid" for r in rows), "required_runs": len(expected), "rows": rows}
    stem = f"lbf-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
    output = ROOT / "benchmarks/results" / stem
    write_new(output.with_suffix(".json"), checkpoint)
    lines = ["# Provisional LBF sheet baseline", "", checkpoint["scope"], "",
        f"Independent validity: **{checkpoint['valid_runs']}/{len(expected)}**. Seed {batch['seed']}, "
        f"{batch['seconds_limit']} s process limit; one pass and one worker. Actual solver time is in the JSON.", "",
        f"LBF source: `{batch['tool']['revision']}`; Rust {batch['tool']['rust_toolchain']}. "
        f"Raw batch `{batch['batch_id']}`. Every output hash was verified when this table was produced.", "",
        "Lower normalized material is better. These are LBF's results, not Nestbolt's or a comparison against other tools.", "",
        "| Job | Configuration | Status | Sheets | Material | Utilisation |", "| --- | --- | --- | ---: | ---: | ---: |"]
    for row in sorted(rows, key=lambda r: (r["job"], r["settings"])):
        metric = row["metrics"]
        if metric:
            values = f"{metric['sheets_used']} | {metric['normalized_material']:.6f} | {metric['utilization']:.2%}"
        else:
            values = "— | — | —"
        lines.append(f"| {row['job']} | {row['settings']} | {row['status']} | {values} |")
    lines.extend(["", f"[Full precision, provenance and record hashes]({stem}.json).", ""])
    with output.with_suffix(".md").open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    with (ROOT / "BENCHMARKS.md").open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"\n- {stamp.isoformat()} | verified provisional LBF batch `{batch['batch_id']}` | "
            f"{checkpoint['valid_runs']}/{len(expected)} valid, seed {batch['seed']}, B only | "
            f"[table](benchmarks/results/{stem}.md). Full M1 and quality gates remain pending.\n")
    print(f"Verified and retained {len(rows)} runs: {output.with_suffix('.md')}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", required=True, type=Path, help="Path to the completed batch.json")
    args = parser.parse_args()
    report(args.batch.resolve(strict=True))


if __name__ == "__main__":
    main()
