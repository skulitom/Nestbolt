"""Compare current fixed-work outputs with the archived six pre-opt-in controls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / "h5-native-interlocking-rows-20261120" / "compatibility.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(binary, inputs, output):
    records = []
    for case in json.loads(REFERENCE.read_bytes())["cases"]:
        job, mode = case["job"], case["mode"]
        folder = output / f"{job}-{mode}"
        folder.mkdir(parents=True)
        subprocess.run([
            binary, "nest", "--library", inputs / f"{job}-library.json",
            "--request", inputs / f"{job}-{mode}.json", "--out-dir", folder,
            "--seconds", "3", "--time-limit", "90", "--seed", "0", "--repeatable",
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        report = json.loads((folder / "report.json").read_bytes())
        assert report["repeatable"] and report["validation"]["valid"]
        actual = {p.name: digest(p) for p in folder.iterdir() if p.name != "report.json"}
        assert actual == case["files"], (job, mode)
        previous = json.loads((inputs / f"{job}-{mode}-0" / "report.json").read_bytes())
        for entry in (previous, report):
            del entry["elapsed_s"]
        assert report == previous, (job, mode)
        records.append({"job": job, "mode": mode, "matching_files": actual})
    return {"binary_sha256": digest(binary), "cases": records}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("binary", "inputs", "output", "summary"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    result = compare(args.binary.resolve(), args.inputs, args.output)
    args.summary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(len(result["cases"]), "complete fixed-work controls matched")
