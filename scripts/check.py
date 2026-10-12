"""Run the same inexpensive checks locally and in CI (Python 3.11+)."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="Also build pinned Sparrow and run two 5-second jobs")
    parser.add_argument("--web", action="store_true", help="Also build the browser app and run its Chromium and Firefox tests")
    args = parser.parse_args()
    commands = [
        ["cargo", "fmt", "--all", "--check"],
        ["cargo", "fmt", "--manifest-path", "benchmarks/sparrow-repro/Cargo.toml", "--check"],
        ["cargo", "clippy", "--workspace", "--all-targets", "--locked", "--", "-D", "warnings"],
        ["cargo", "test", "--workspace", "--locked"],
        ["cargo", "test", "--release", "--locked", "-p", "nestbolt-cli", "--test", "features"],
        ["cargo", "test", "--locked", "-p", "nestbolt-validator", "--example", "stock_adapter"],
        ["cargo", "build", "-p", "nestbolt-wasm", "--target", "wasm32-unknown-unknown", "--locked"],
        ["cargo", "build", "-p", "nestbolt-validator", "--target", "wasm32-unknown-unknown", "--locked"],
        [sys.executable, "scripts/notices.py", "--check"],
        ["node", "--test", "mcpb/mcpb.test.mjs"],
        [sys.executable, "scripts/smoke.py", "--verify-only"],
        [sys.executable, "scripts/test_m0.py"],
        [sys.executable, "scripts/schemas.py", "--check"],
        [sys.executable, "scripts/datasets.py", "--check"],
        [sys.executable, "scripts/test_datasets.py"],
        [sys.executable, "scripts/test_benchmark_io.py"],
        [sys.executable, "scripts/test_lbf_report.py"],
        [sys.executable, "scripts/test_svgnest_io.py"],
        [sys.executable, "scripts/test_svg_export_transform.py"],
        [sys.executable, "scripts/test_svgnest_report.py"],
        [sys.executable, "scripts/test_deepnest_io.py"],
        [sys.executable, "scripts/test_deepnest_report.py"],
        [sys.executable, "scripts/test_deepnest_snapshot.py"],
        [sys.executable, "scripts/test_sparrow_io.py"],
        [sys.executable, "scripts/test_sparrow_report.py"],
        [sys.executable, "scripts/test_comparator_batch_report.py"],
        [sys.executable, "scripts/test_batch_comparison_report.py"],
        [sys.executable, "scripts/test_baseline_gap.py"],
        [sys.executable, "scripts/test_strip_report.py"],
        [sys.executable, "scripts/test_construct_profile_batch.py"],
        [sys.executable, "scripts/test_search_development_report.py"],
        [sys.executable, "scripts/test_comparison_session.py"],
        [sys.executable, "scripts/test_comparison_session_report.py"],
        [sys.executable, "scripts/test_comparison_envelope.py"],
        [sys.executable, "scripts/matrix_plan.py", "--check"],
        [sys.executable, "scripts/test_matrix_plan.py"],
        [sys.executable, "scripts/maker_freeze.py", "--check"],
        [sys.executable, "scripts/test_maker_freeze.py"],
        ["cargo", "run", "--quiet", "--locked", "-p", "nestbolt-validator", "--example", "check_jobs", "--",
            *[str(path) for group in ["S", "B", "M"] for path in sorted((ROOT / "benchmarks/datasets" / group).glob("*.json"))]],
    ]
    if args.smoke:
        commands.append([sys.executable, "scripts/smoke.py"])
    if args.web:
        commands.append([sys.executable, "scripts/build_web.py", "--test"])
    for command in commands:
        print("Running:", " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
