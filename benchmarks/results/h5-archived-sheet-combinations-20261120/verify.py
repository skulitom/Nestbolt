"""Independently validate and export each candidate against the original common-line request."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile

RESULTS = Path(__file__).resolve().parents[1]
SOURCE = RESULTS / "h5-common-development-20261015T142414Z"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("binary", type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    cases = json.loads((args.output / "construction.json").read_bytes())
    assert len(cases) == 4
    records = []
    for case in cases:
        folder = args.output / f"{case['job']}-{case['kerf']}"
        with ZipFile(SOURCE / case["canonical"]) as archive:
            for member in ("library.json", "request.json"):
                assert (folder / member).read_bytes() == archive.read(member)
        for ref in (case["first"], case["second"]):
            with ZipFile(RESULTS / ref["archive"]) as archive:
                assert sha256(archive.read(ref["member"])).hexdigest() == ref["sha256"]
        inputs = ["--library", "library.json", "--request", "request.json", "--layout", "layout.json"]
        validate = subprocess.run([binary, "validate", *inputs], cwd=folder, capture_output=True)
        (folder / "validation.json").write_bytes(validate.stdout)
        (folder / "validation.stderr").write_bytes(validate.stderr)
        validate.check_returncode()
        report = json.loads(validate.stdout)
        metrics = report["metrics"]
        assert report["valid"] and report["violation_count"] == 0
        assert metrics["placed_parts"] == metrics["requested_parts"] and metrics["sheets_used"] == 2
        export = subprocess.run([binary, "export", *inputs, "--out-dir", "export"], cwd=folder, capture_output=True)
        (folder / "export.stderr").write_bytes(export.stderr)
        export.check_returncode()
        for ext in ("svg", "dxf"):
            assert {p.stem for p in (folder / "export").glob(f"*.{ext}")} == {"sheet-0", "sheet-1"}
        material = metrics["material_area"]
        records.append(dict(job=case["job"], kerf=case["kerf"], parts=metrics["placed_parts"],
                            area_mm2=material, target_mm2=case["target_mm2"], last_height_mm=metrics["last_sheet_used_height"],
                            improvement_mm2=case["best_archived_mm2"] - material,
                            above_target_percent=(material / case["target_mm2"] - 1) * 100,
                            layout_sha256=sha256((folder / "layout.json").read_bytes()).hexdigest()))
    summary = {"binary_sha256": sha256(binary.read_bytes()).hexdigest(), "validated_and_exported": records}
    with (args.output / "verified.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(summary, stream, indent=2)
        stream.write("\n")
    print([(r["job"], r["kerf"], r["area_mm2"], r["above_target_percent"]) for r in records])


if __name__ == "__main__":
    main()
