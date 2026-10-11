"""Attach independent, immutable geometry reports to completed M0 attempts."""
import argparse
from datetime import datetime, timezone
import json
import re
import subprocess
import uuid

from m0 import ROOT, MANIFEST, append_log, command, materialize_input, write_new
from m0_reference import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,70}", args.experiment):
        raise SystemExit("Invalid experiment name")
    root = ROOT / "output/m0" / args.experiment
    reference = json.loads(MANIFEST.read_text(encoding="utf-8"))
    metadata = json.loads((root / "experiment.json").read_text(encoding="utf-8"))
    if metadata["reference_sha256"] != digest(MANIFEST):
        raise SystemExit("Frozen reference differs from experiment")
    subprocess.run(["cargo", "build", "--locked", "-p", "nestbolt-cli"], cwd=ROOT, check=True)
    binary = ROOT / "target/debug/nestbolt.exe"
    common = {"validator_binary_sha256": digest(binary), "validator_commit": command(["git", "rev-parse", "HEAD"]),
        "validator_dirty": bool(command(["git", "status", "--porcelain"])),
        "validator_sources": {p.relative_to(ROOT).as_posix(): digest(p) for p in
            sorted((ROOT / "crates/validator/src").glob("*.rs")) + [ROOT / "Cargo.lock"]}}
    results = []
    for instance in reference["instances"]:
        for index in reference["method"]["run_indices"]:
            run_path = root / f"{instance['name']}-{index}"
            record_path = run_path / "run.json"
            if not record_path.exists():
                continue
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if record["status"] != "completed_integrity_checked":
                continue
            layout = run_path / "output/layout.json"
            if digest(layout) != record["outputs"]["output/layout.json"]:
                raise SystemExit(f"Layout changed since run completion: {layout}")
            source = materialize_input(instance)
            process = subprocess.run([str(binary), "validate-sparrow", "--input", str(source),
                "--layout", str(layout), "--units", "unitless"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
            try:
                report = json.loads(process.stdout)
            except json.JSONDecodeError:
                report = {"valid": False, "error": process.stderr.strip() or "validator produced no JSON"}
            valid = bool(report["valid"] and process.returncode == 0)
            output = run_path / ("validation-" + uuid.uuid4().hex[:10] + ".json")
            write_new(output, {**common, "validated_at": datetime.now(timezone.utc).isoformat(),
                "input_sha256": digest(source), "layout_sha256": digest(layout), "exit_code": process.returncode,
                "valid": valid, "report": report})
            results.append(valid)
            print(f"{run_path.name}: {'valid' if valid else 'INVALID'}; report {output.relative_to(ROOT)}", flush=True)
            append_log(f"- {datetime.now(timezone.utc).isoformat()} | independent geometry check `{args.experiment}/{run_path.name}` | {'valid' if valid else 'INVALID'} | [report]({output.relative_to(ROOT).as_posix()}). Original polygons; Clipper2 path; this does not establish full M1/G1.")
    print(f"Independently valid: {sum(results)}/{len(results)} completed attempts. Unfinished runs excluded from this snapshot.")
    if results and not all(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
