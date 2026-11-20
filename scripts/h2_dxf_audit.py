"""Audit the actual DXF sheets from a completed training-vector fidelity run with ezdxf."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import ezdxf

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "benchmarks/datasets/shop"
EXPECTED_PALETTE = {"CUT": 0, "COMMON": 255, "LEADIN": 16711680, "SHEET": 15952166}


def read(path):
    return json.loads(path.read_bytes())


def audit_file(path):
    doc = ezdxf.readfile(path)
    model = list(doc.modelspace())
    types = Counter(e.dxftype() for e in model)
    collapsed = [e.dxf.handle for e in model if e.dxftype() == "LINE" and e.dxf.start == e.dxf.end]
    palette = {name: doc.layers.get(name).dxf.true_color for name in EXPECTED_PALETTE}
    audit = doc.audit()
    return {
        "name": path.name, "sha256": sha256(path.read_bytes()).hexdigest(),
        "version": doc.dxfversion, "units": doc.units, "entities": dict(types), "palette": palette,
        "zero_length_lines": collapsed, "errors": [e.message for e in audit.errors],
        "fixes": [e.message for e in audit.fixes],
        "passed": (bool(model) and doc.dxfversion == "AC1021" and doc.units == 4
                   and palette == EXPECTED_PALETTE and not (audit.errors or audit.fixes or collapsed)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fidelity", type=Path)
    parser.add_argument("--work-dir", type=Path, help="Location of the fidelity output when moved to another host")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = read(args.fidelity)
    manifest_path = CORPUS / "manifest.json"
    assert sha256(manifest_path.read_bytes()).hexdigest() == report["manifest_sha256"]
    training = {r["path"] for r in read(manifest_path)["files"] if r["split"] == "training"
                and r.get("label") and Path(r["path"]).suffix.lower() in (".svg", ".dxf")}
    assert report["only"] is None and report["held_out_read"] is False
    assert len(report["rows"]) == len(training) and {r["path"] for r in report["rows"]} == training
    indexed = {r["path"]: r for r in report["rows"]}
    work = args.work_dir or ROOT / report["work_directory"]
    files, seen = [], set()
    for folder in sorted(work.iterdir()):
        if not folder.is_dir():
            continue
        row = read(folder / "result.json")
        assert row == indexed[row["path"]] and row["path"] not in seen
        seen.add(row["path"])
        if row["status"] == "rejected":
            continue
        assert row["pass"], row["path"]
        exports = folder / "exports"
        expected = {s["id"] + ".dxf" for s in read(exports / "layout.json")["sheets"]}
        drawings = sorted(exports.glob("*.dxf"))
        assert expected and {d.name for d in drawings} == expected
        for drawing in drawings:
            try:
                result = audit_file(drawing)
            except (OSError, ValueError, ezdxf.DXFError) as exc:
                result = {"name": drawing.name, "passed": False, "error": str(exc)}
            files.append({"source": row["path"], **result})
    assert seen == training
    result = {
        "ezdxf": ezdxf.__version__,
        "runner_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "fidelity_report_sha256": sha256(args.fidelity.read_bytes()).hexdigest(),
        "passed": bool(files) and all(r["passed"] for r in files),
        "sheets": len(files),
        "files": files,
    }
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(f"{sum(r['passed'] for r in files)}/{len(files)} DXF sheets passed")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
