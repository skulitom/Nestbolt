"""Run the same inexpensive checks locally and in CI (Python 3.11+)."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="Also build pinned Sparrow and run two 5-second jobs")
    args = parser.parse_args()
    commands = [
        ["cargo", "fmt", "--all", "--check"],
        ["cargo", "fmt", "--manifest-path", "benchmarks/sparrow-repro/Cargo.toml", "--check"],
        ["cargo", "clippy", "--workspace", "--all-targets", "--locked", "--", "-D", "warnings"],
        ["cargo", "test", "--workspace", "--locked"],
        ["cargo", "build", "-p", "nestbolt-wasm", "--target", "wasm32-unknown-unknown", "--locked"],
        ["cargo", "build", "-p", "nestbolt-validator", "--target", "wasm32-unknown-unknown", "--locked"],
        [sys.executable, "scripts/notices.py", "--check"],
        [sys.executable, "scripts/smoke.py", "--verify-only"],
        [sys.executable, "scripts/test_m0.py"],
        [sys.executable, "scripts/schemas.py", "--check"],
        [sys.executable, "scripts/datasets.py", "--check"],
        [sys.executable, "scripts/test_datasets.py"],
        [sys.executable, "scripts/test_benchmark_io.py"],
        [sys.executable, "scripts/test_lbf_report.py"],
        ["cargo", "run", "--quiet", "--locked", "-p", "nestbolt-validator", "--example", "check_jobs", "--",
            *[str(path) for group in ["S", "B"] for path in sorted((ROOT / "benchmarks/datasets" / group).glob("*.json"))]],
    ]
    if args.smoke:
        commands.append([sys.executable, "scripts/smoke.py"])
    for command in commands:
        print("Running:", " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
