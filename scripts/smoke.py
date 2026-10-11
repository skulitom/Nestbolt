"""Reproducible Sparrow integration smoke; never a quality or validity gate."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "benchmarks/smoke.json"
TOOLCHAIN = "1.98.1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture(command, cwd=ROOT):
    return subprocess.check_output(command, cwd=cwd, text=True).strip()


def verify(manifest):
    for case in manifest["cases"]:
        path = ROOT / case["path"]
        if sha256(path) != case["sha256"]:
            raise RuntimeError(f"Fixture checksum mismatch: {case['path']}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["name"] != case["id"]:
            raise RuntimeError(f"Fixture name mismatch: {case['id']}")
    print("Smoke fixtures match their frozen checksums.", flush=True)


def prepare(tool):
    # Let rustup install the repository's pinned toolchain on a fresh machine.
    subprocess.run(["rustup", "show", "active-toolchain"], cwd=ROOT, check=True)
    checkout = ROOT / ".cache/upstream/sparrow"
    if not checkout.exists():
        checkout.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--no-checkout", "--filter=blob:none", tool["repository"], str(checkout)], check=True)
        subprocess.run(["git", "-C", str(checkout), "checkout", "--detach", tool["commit"]], check=True)
    if capture(["git", "rev-parse", "HEAD"], checkout) != tool["commit"]:
        raise RuntimeError("Cached Sparrow is at a different revision; use a fresh checkout of the pinned commit.")
    if capture(["git", "status", "--porcelain", "--untracked-files=no"], checkout):
        raise RuntimeError("Cached Sparrow has tracked changes. Preserve those changes before preparing a clean checkout.")
    lock = ROOT / "benchmarks/locks/sparrow.Cargo.lock"
    existing = checkout / "Cargo.lock"
    if existing.exists() and sha256(existing) != sha256(lock):
        raise RuntimeError("Cached Sparrow Cargo.lock differs from the benchmark lock; preserve it before restoring the pinned lock.")
    shutil.copyfile(lock, existing)
    target = ROOT / ".cache/build/sparrow"
    env = {**os.environ, "CARGO_BUILD_JOBS": "4", "CARGO_TARGET_DIR": str(target), "RUSTFLAGS": ""}
    subprocess.run([
        "cargo", f"+{TOOLCHAIN}", "build", "--release", "--locked", "--bin", "sparrow",
        "--features", "only_final_svg", "--manifest-path", str(checkout / "Cargo.toml"),
    ], cwd=ROOT, env=env, check=True)
    binary = target / "release" / ("sparrow.exe" if os.name == "nt" else "sparrow")
    return binary


def source_hash():
    digest = hashlib.sha256()
    paths = [ROOT / "Cargo.toml", ROOT / "Cargo.lock", ROOT / "rust-toolchain.toml"]
    for directory in ["crates", "scripts", "benchmarks", ".cargo"]:
        paths.extend(p for p in (ROOT / directory).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for path in sorted(paths):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return digest.hexdigest()


def run_case(binary, case, manifest, seconds, seed):
    timestamp = datetime.now(timezone.utc)
    run_id = f"{timestamp:%Y%m%dT%H%M%SZ}-{case['id']}-s{seed}-{uuid.uuid4().hex[:8]}"
    directory = ROOT / "output/runs" / run_id
    directory.mkdir(parents=True, exist_ok=False)
    input_path = ROOT / case["path"]
    command = [str(binary), "-i", str(input_path), "-t", str(seconds), "-s", str(seed), "--workers", "1"]
    commit_result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    record = {
        "run_id": run_id, "started_at_utc": timestamp.isoformat(), "kind": "integration_smoke",
        "nestbolt_commit": commit_result.stdout.strip() if commit_result.returncode == 0 else None,
        "worktree_dirty": bool(capture(["git", "status", "--porcelain"])),
        "source_sha256": source_hash(), "tool": manifest["tool"],
        "tool_lock_sha256": sha256(ROOT / "benchmarks/locks/sparrow.Cargo.lock"),
        "binary_sha256": sha256(binary), "rustc": capture(["rustc", f"+{TOOLCHAIN}", "--version"]),
        "platform": platform.platform(), "processor": platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER", "unknown"),
        "case": case, "seconds": seconds, "seed": seed, "workers": 1,
        "rayon_threads": 1, "command": command,
        "independent_validation": "not_implemented", "quality_gate": "not_evaluated",
        "status": "failed",
    }
    started = time.monotonic()
    try:
        with (directory / "process.log").open("w", encoding="utf-8") as log:
            process = subprocess.run(command, cwd=directory, env={**os.environ, "RAYON_NUM_THREADS": "1"},
                                     stdout=log, stderr=subprocess.STDOUT, timeout=seconds + 30)
        record["exit_code"] = process.returncode
        if process.returncode != 0:
            raise RuntimeError(f"Sparrow exited with {process.returncode}; see {directory / 'process.log'}")
        output = directory / "output" / f"final_{case['id']}.json"
        result = json.loads(output.read_text(encoding="utf-8"))
        width = result["solution"]["strip_width"]
        if not isinstance(width, (float, int)) or not math.isfinite(width) or width <= 0:
            raise RuntimeError("Sparrow returned an invalid strip width")
        record["strip_width_reported_by_solver"] = width
        record["solution_sha256"] = sha256(output)
        record["status"] = "completed_unvalidated"
    except Exception as error:
        record["error"] = str(error)
        raise
    finally:
        record["elapsed_s"] = time.monotonic() - started
        (directory / "run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        relative = directory.relative_to(ROOT).as_posix()
        # This runner is intentionally sequential; never replace earlier records.
        with (ROOT / "BENCHMARKS.md").open("a", encoding="utf-8") as log:
            log.write(f"\n- {timestamp.isoformat()} | `{run_id}` | Sparrow `{manifest['tool']['commit']}` | "
                      f"Nestbolt `{record['nestbolt_commit'] or 'uncommitted scaffold'}` "
                      f"(dirty={record['worktree_dirty']}) | seed {seed}, {seconds}s, 1 worker | "
                      f"{record['status']} | [record]({relative}/run.json). No independent validity/quality claim.\n")
    print(f"{case['id']}: completed (unvalidated). Record: {directory / 'run.json'}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--seconds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    if not 1 <= args.seconds <= 300 or not 0 <= args.seed <= 2**64 - 1:
        parser.error("seconds must be 1..300 and seed must be a nonnegative u64")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    verify(manifest)
    if not args.verify_only:
        binary = prepare(manifest["tool"])
        for case in manifest["cases"]:
            run_case(binary, case, manifest, args.seconds, args.seed)


if __name__ == "__main__":
    main()
