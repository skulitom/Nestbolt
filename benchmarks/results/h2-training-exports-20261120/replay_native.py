"""Compare the public CLI with the reviewed archive of 56 native training inputs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def digest(data):
    return sha256(data).hexdigest()


def replay(root, corpus, cli, out):
    baseline = root / "benchmarks/results/h2-native-warning-probe-20261016-v3"
    manifest_bytes = (corpus / "manifest.json").read_bytes()
    training = {
        r["path"]: r
        for r in json.loads(manifest_bytes)["files"]
        if r["split"] == "training"
        and Path(r["path"]).suffix.lower() in (".lbrn", ".lbrn2")
    }
    prior = json.loads((baseline / "checks.json").read_bytes())
    assert prior["held_out_geometry_read"] is False and prior["all_checks_passed"]
    assert len(training) == len(prior["rows"]) == 56
    assert training.keys() == {r["path"] for r in prior["rows"]}
    archive = baseline / "raw.zip"
    archive_hash = digest(archive.read_bytes())
    assert (
        archive_hash
        == json.loads((baseline / "archive-integrity.json").read_bytes())["sha256"]
    )
    cli_hash = digest(cli.read_bytes())
    rows = []
    with zipfile.ZipFile(archive) as z, tempfile.TemporaryDirectory() as temp:
        for index, reference in enumerate(prior["rows"]):
            item = training[reference["path"]]
            drawing = corpus / item["path"]
            assert (
                digest(drawing.read_bytes())
                == item["sha256"]
                == reference["source_sha256"]
            )
            assert (
                digest((corpus / item["label"]).read_bytes())
                == item["label_sha256"]
                == reference["label_sha256"]
            )
            output = Path(temp) / f"{index:03}.json"
            result = subprocess.run(
                [cli, "import", drawing, "--tolerance", "0.005", "--output", output],
                capture_output=True,
                timeout=180,
            )
            record = {
                "source": item["path"],
                "source_sha256": item["sha256"],
                "label_sha256": item["label_sha256"],
                "expected_exit": reference["exit_code"],
                "exit": result.returncode,
            }
            if reference["exit_code"] == 0:
                raw = z.read(
                    f"benchmarks/results/{baseline.name}/{index:03}/library.json"
                )
                assert digest(raw) == reference["library_sha256"]
                current = output.read_bytes() if output.exists() else None
                record["baseline_library_sha256"] = digest(raw)
                record["candidate_library_sha256"] = (
                    digest(current) if current is not None else None
                )
                record["library_identical"] = current is not None and json.loads(
                    current
                ) == json.loads(raw)
                record["passed"] = (
                    result.returncode == 0 and record["library_identical"]
                )
            else:
                record["error"] = result.stderr.decode("utf-8")
                record["error_identical"] = record["error"] == reference["error"]
                record["no_partial_library"] = not output.exists()
                record["passed"] = (
                    result.returncode == reference["exit_code"]
                    and record["error_identical"]
                    and record["no_partial_library"]
                )
            rows.append(record)
    assert cli_hash == digest(cli.read_bytes())
    section = {
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "binary_sha256": cli_hash,
        "baseline_archive_sha256": archive_hash,
        "manifest_sha256": digest(manifest_bytes),
        "held_out_read": False,
        "rows": rows,
    }
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(section, stream, indent=2)
        stream.write("\n")
    print(
        f"{sum(r['passed'] for r in rows)}/{len(rows)} native training outcomes matched"
    )
    return 0 if all(r["passed"] for r in rows) else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path.cwd(), help="Checkout used to build the CLI"
    )
    parser.add_argument(
        "--corpus", type=Path, help="Frozen shop directory if outside the checkout"
    )
    parser.add_argument("--cli", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(
        replay(
            args.root.resolve(),
            (args.corpus or args.root / "benchmarks/datasets/shop").resolve(),
            args.cli.resolve(),
            args.out,
        )
    )
