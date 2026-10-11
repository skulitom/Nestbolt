"""Freeze the published Sparrow evidence, without redistributing benchmark geometry."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from statistics import mean, median, quantiles
import subprocess
import tarfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
REVISION = "7f069e9d146f5599d7ba69a47ab4e8097c56e54f"
ARCHIVE_REVISION = "4629b22795ae6b25b3b460ccde6fb36a71292b6d"
PAPER = {"albano": 89.47, "blaz1": 84.68, "dagli": 89.26, "fu": 92.24,
         "jakobs1": 89.09, "jakobs2": 84.77, "mao": 86.14, "marques": 90.93,
         "shapes0": 68.60, "shapes1": 75.69, "shirts": 89.66, "swim": 78.26,
         "trousers": 91.73}
INFLATED = {"blaz1", "fu", "jakobs1", "jakobs2", "shapes0", "shapes1"}
MANIFEST = ROOT / "benchmarks/m0-reference.json"


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def git_blob(checkout, revision, path):
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=checkout)


def render():
    published = ROOT / ".cache/upstream/sparrow-published"
    archives = ROOT / ".cache/upstream/sparrow"
    instances = []
    for name, paper_density in PAPER.items():
        source_path = f"data/input/{name}.json"
        source = git_blob(published, REVISION, source_path)
        instance = json.loads(source)
        runs = []
        archive_records = []
        for suffix in ("", " (1)"):
            filename = f"{name}-results{suffix}.zip"
            path = f"data/experiments/benchmark_runs/{filename}"
            archive = git_blob(archives, ARCHIVE_REVISION, path)
            with ZipFile(BytesIO(archive)) as z:
                nested = [n for n in z.namelist() if n.endswith(".tar.gz")]
                assert len(nested) == 1, filename
                with tarfile.open(fileobj=BytesIO(z.read(nested[0])), mode="r:gz") as tar:
                    logs = [m for m in tar.getmembers() if m.name.endswith("_bench_stdout.log")]
                    assert len(logs) == 1, filename
                    log = tar.extractfile(logs[0]).read().decode("utf-8")
            revision = re.search(r"git commit hash: ([a-f0-9]{40})", log)[1]
            assert revision == REVISION, filename
            seed = re.search(r"no seed provided, using: (\d+)", log)[1]
            widths = json.loads(re.search(r"widths:\s*(\[[^]]+\])", log)[1])
            densities = json.loads(re.search(r"usages:\s*(\[[^]]+\])", log)[1])
            assert len(widths) == len(densities) == 50, filename
            assert "1200s timelimit" in log, filename
            archive_records.append({"file": filename, "path": path,
                "sha256": sha256(archive).hexdigest(), "archive_seed": seed,
                "utc": re.search(r"system time: (\S+)", log)[1],
                "widths": widths, "density_percent": densities})
            runs.extend(widths)
        densities = [d for a in archive_records for d in a["density_percent"]]
        # Paper densities use the nominal strip height; archived logs use the
        # inflated height. Lengths themselves require no correction.
        height_factor = 1.0001 if name in INFLATED else 1.0
        corrected = mean(densities) * height_factor
        assert abs(corrected - paper_density) <= 0.0051, (name, corrected, paper_density)
        instances.append({"name": name, "paper_name": "SHAPES2" if name == "blaz1" else name.upper(),
            "input_path": source_path, "input_sha256": sha256(source).hexdigest(),
            "strip_height": instance["strip_height"], "height_factor": height_factor,
            "part_count": sum(i["demand"] for i in instance["items"]),
            "paper_mean_density_percent": paper_density,
            "reference_mean_width": mean(runs), "reference_median_width": median(runs),
            "reference_width_quartiles": quantiles(runs, n=4, method="inclusive"),
            "reference_mean_density_percent": mean(densities), "archives": archive_records})
    return {"schema_version": 1, "paper": "https://arxiv.org/html/2509.13329v1",
        "source_repository": "https://github.com/JeroenGar/sparrow.git",
        "solver_revision": REVISION, "archive_revision": ARCHIVE_REVISION,
        "toolchain": "nightly-2025-06-14-x86_64-pc-windows-msvc",
        "dependency_cutoff_utc": "2025-06-14T17:00:00Z",
        "method": {"purpose": "M0 native quality reproduction, not a full statistical replication",
            "seconds": 1200, "workers": 3, "archive_index": 0, "run_indices": [0, 1, 2],
            "comparison": "absolute relative difference of 3-run mean length from all 100 published runs",
            "maximum_relative_difference": 0.01, "all_instances_required": True,
            "missing_or_failed_runs_pass": False, "selection": "first three run indices, fixed before execution",
            "independent_validation": "M1; M0 checks quantities, finite metrics and output integrity only"},
        "dataset_licence": "Source/provenance recorded; original ESICUP redistribution rights unresolved for M1. Geometry remains in ignored cache.",
        "instances": instances}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = json.dumps(render(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        assert MANIFEST.read_text(encoding="utf-8") == text, "Published reference manifest changed"
        print("All 13 instances / 1,300 archived results match the frozen reference and paper table.")
    else:
        if MANIFEST.exists():
            raise SystemExit("Reference already frozen; use --check. Revise methodology explicitly if needed.")
        MANIFEST.write_text(text, encoding="utf-8", newline="\n")
        print("Frozen M0 reference and predeclared 39-run method.")


if __name__ == "__main__":
    main()
