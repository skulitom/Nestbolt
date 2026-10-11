"""Fetch the pinned, MIT-declared OR-Datasets strip sources and verify provenance."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REVISION = "e2e151cf241ab97d860f657cbfe515232e7096d7"
BASE = f"https://raw.githubusercontent.com/Oscar-Oliveira/OR-Datasets/{REVISION}/"
MANIFEST = ROOT / "benchmarks/sources/strip-sources.json"
CACHE = ROOT / ".cache/or-datasets"
FAMILIES = {"albano": "ALBANO", "blaz1": "BLAZ", "dagli": "DAGLI", "fu": "FU",
    "jakobs1": "JAKOBS", "jakobs2": "JAKOBS", "mao": "MAO", "marques": "MARQUES",
    "shapes0": "SHAPES", "shapes1": "SHAPES", "shirts": "SHIRTS", "swim": "SWIM", "trousers": "TROUSERS"}


def fetch(path, destination, expected=None):
    url = BASE + quote(path, safe="/")
    if destination.exists():
        content = destination.read_bytes()
    else:
        with urlopen(Request(url, headers={"User-Agent": "Nestbolt-benchmark-provenance/0.1"}), timeout=60) as response:
            content = response.read()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
    actual = sha256(content).hexdigest()
    if expected and expected != actual:
        raise ValueError(f"Source checksum mismatch: {destination}")
    return content, actual, url


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true", help="First freeze only; refuses to overwrite an existing manifest")
    parser.add_argument("--verify-m0", action="store_true", help="Also compare geometry to the frozen historical Sparrow source")
    args = parser.parse_args()
    if args.freeze and MANIFEST.exists():
        raise SystemExit("Source manifest already frozen; run without --freeze to verify/download")
    if not args.freeze and not MANIFEST.exists():
        raise SystemExit("No frozen source manifest; initial authoring requires --freeze")
    frozen = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else None
    rows = []
    for name, family in FAMILIES.items():
        previous = next((r for r in frozen["instances"] if r["name"] == name), None) if frozen else None
        path = f"Cutting-and-Packing/2D-Irregular/Datasets/{family}/json/{name}.json"
        content, checksum, url = fetch(path, CACHE / f"{name}.json", previous["sha256"] if previous else None)
        job = json.loads(content)
        assert job["name"] == name
        quantities = sum(i["demand"] for i in job["items"])
        assert 1 <= quantities <= 2000
        assert all(i["shape"]["type"] == "simple_polygon" for i in job["items"])
        rows.append({"name": name, "family": family, "source_url": url, "sha256": checksum,
            "declared_licence": "MIT", "licence_scope": "OR-Datasets converted collection",
            "units": "unitless", "strip_height": job["strip_height"], "part_count": quantities,
            "original_publication_index": BASE + "Cutting-and-Packing/2D-Irregular/README.md"})
    licence_path = ROOT / "benchmarks/sources/OR_DATASETS_LICENSE"
    licence, licence_hash, licence_url = fetch("LICENSE", CACHE / "SOURCE_LICENSE", frozen["licence_sha256"] if frozen else None)
    assert licence.decode("utf-8").startswith("MIT License")
    notice = licence.decode("utf-8").replace("\r\n", "\n")
    if args.freeze:
        licence_path.parent.mkdir(parents=True, exist_ok=True)
        licence_path.write_text(notice, encoding="utf-8", newline="\n")
    else:
        assert licence_path.read_text(encoding="utf-8") == notice, "Retained licence text differs from source"
    _, provenance_hash, provenance_url = fetch("Cutting-and-Packing/2D-Irregular/README.md",
        CACHE / "PROVENANCE.md", frozen["provenance_sha256"] if frozen else None)
    result = {"schema_version": 1, "repository": "https://github.com/Oscar-Oliveira/OR-Datasets",
        "revision": REVISION, "licence_url": licence_url, "licence_sha256": licence_hash,
        "provenance_url": provenance_url, "provenance_sha256": provenance_hash,
        "note": "Original publication attributions are retained in the pinned provenance index. This freezes source bytes; canonical S/B job conversion and benchmark constraints are separate work.",
        "instances": rows}
    if args.freeze:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print("Frozen all 13 strip-source checksums, declared MIT licence and publication provenance.")
    else:
        assert result == frozen, "Source provenance changed"
        print("All 13 strip sources and their licence/provenance match the frozen manifest.")
    if args.verify_m0:
        reference = json.loads((ROOT / "benchmarks/m0-reference.json").read_text(encoding="utf-8"))
        for instance in reference["instances"]:
            original = json.loads((CACHE / (instance["name"] + ".json")).read_text(encoding="utf-8"))
            historical = json.loads(subprocess.check_output(["git", "show",
                reference["solver_revision"] + ":" + instance["input_path"]], cwd=ROOT / ".cache/upstream/sparrow-published"))
            def geometry(job):
                return [(i["id"], i["demand"], i.get("allowed_orientations"), i["shape"]) for i in job["items"]]
            assert geometry(original) == geometry(historical), f"Geometry differs: {instance['name']}"
            assert abs(original["strip_height"] * instance["height_factor"] - historical["strip_height"]) < 1e-9
        print("All original polygons, quantities and rotations equal the M0 historical inputs; only the six declared strip-height adjustments differ.")


if __name__ == "__main__":
    main()
