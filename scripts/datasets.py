"""Rebuild/freeze the academic benchmark jobs; check their frozen bytes offline.

The original source fetcher checks pinned raw bytes before any conversion. A freeze
is explicit and one-time. This converter must not change after quality tuning.
"""
import argparse
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from strip_sources import CACHE, ROOT

DEST = ROOT / "benchmarks/datasets"
MANIFEST = DEST / "academic.json"
PAPER = "https://doi.org/10.1016/j.ejor.2016.09.043"
PAPER_PDF = "https://eprints.whiterose.ac.uk/139290/1/BCP-EJOR.pdf"
# Table 1 / section 6.1, and the PBP results in Table 5 (N, F).
# These reported results are context, not a same-machine baseline or a BKR claim.
PUBLISHED = {
    "albano": (24, 4551, [0, 180], (3, .480), (3, .510)),
    "blaz1": (28, 7.5, [0, 180], (10, .349), (10, .350)),
    "fu": (12, 21, [0, 90, 180, 270], (4, .443), (4, .440)),
    "jakobs1": (25, 12, [0, 90, 180, 270], (4, .570), (4, .530)),
    "jakobs2": (25, 24, [0, 90, 180, 270], (4, .401), (4, .380)),
    "mao": (20, 1645.5, [0, 180], (3, .271), (3, .300)),
    "shapes0": (43, 21, [0, 90, 180, 270], (7, .271), (6, .390)),
    "shapes1": (43, 21, [0, 180], (7, .282), (6, .390)),
    "shirts": (99, 19.5, [0, 180], (8, .518), (8, .570)),
    "swim": (48, 2909.47, [0, 180], (5, .397), (5, .390)),
    "trousers": (64, 88.5, [0, 180], (3, .555), (3, .580)),
}


def serialized(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def source_parts(source):
    parts = []
    for item in source["items"]:
        if item["shape"]["type"] != "simple_polygon":
            raise ValueError("Academic converter only accepts simple source polygons")
        angles = item["allowed_orientations"]
        parts.append({"id": str(item["id"]), "quantity": item["demand"],
            "geometry": [{"outer": deepcopy(item["shape"]["data"]), "holes": []}],
            "rotations": {"kind": "free"} if angles is None else
                {"kind": "list", "degrees": angles or [0]},
            "allow_mirror": False, "priority": 1.0})
    return parts


def extent(points, axis):
    coordinates = [Decimal(str(p[axis])) for p in points]
    return max(coordinates) - min(coordinates)


def dimensions(parts):
    return [(extent(p["geometry"][0]["outer"], 0),
             extent(p["geometry"][0]["outer"], 1)) for p in parts]


def make_job(name, parts, width, height, count=None):
    return {"version": 1, "name": name, "units": "unitless", "parts": deepcopy(parts),
        "stocks": [{"id": "stock", "width": float(width), "height": float(height),
            "count": count, "margins": {"left": 0, "right": 0, "bottom": 0, "top": 0},
            "outline": [], "defects": []}],
        "clearance": 0, "edge_clearance": 0, "mode": "all"}


def build(sources):
    jobs, rows = {}, []
    for row in sources["instances"]:
        name = row["name"]
        path = CACHE / f"{name}.json"
        if digest(path) != row["sha256"]:
            raise ValueError(f"Original source checksum mismatch: {name}")
        source = json.loads(path.read_bytes())
        parts = source_parts(source)
        dims = dimensions(parts)
        md = max(max(pair) for pair in dims)
        count = sum(p["quantity"] for p in parts)
        height = Decimal(str(source["strip_height"]))
        # A finite envelope large enough for every part placed consecutively at 0°.
        # S is scored by the actual occupied X extent, never by this envelope.
        upper = sum(w * p["quantity"] for (w, _), p in zip(dims, parts)) + 1
        if any(h > height for _, h in dims):
            raise ValueError(f"Source {name} needs a different strip envelope proof")

        def add(group, variant, job, method, **extra):
            identifier = f"{group.lower()}-{name}-{variant}"
            job["name"] = identifier
            relative = f"{group}/{identifier}.json"
            data = serialized(job)
            jobs[relative] = data
            rows.append({"id": identifier, "set": group, "path": relative,
                "sha256": sha256(data).hexdigest(), "source": name,
                "source_sha256": row["sha256"], "source_url": row["source_url"],
                "declared_licence": row["declared_licence"],
                "licence_scope": row["licence_scope"], "units": "unitless",
                "part_count": count, "held_out": False, "construction": method, **extra})

        add("S", "strip", make_job("", parts, upper, height, 1),
            "Original source polygons, quantities, angles and strip Y extent. The finite X envelope is sum(quantity * initial bbox width) + 1. No M0 0.01% height adjustment.",
            metric="strip_used_width", strip_height=float(height), envelope_width=float(upper))

        # A stated length independent of solver results, with original strip height.
        length = md * Decimal("2")
        add("B", "strip-sheet", make_job("", parts, length, height),
            "Nestbolt-derived fixed sheets: X length = twice the maximum initial part bbox dimension; Y height = original strip height. Original rotations, unlimited identical stock.",
            metric="normalized_material", published_instance=False,
            sheet_length=float(length), strip_height=float(height))

        if name in PUBLISHED:
            expected_count, printed_side, angles, fixed_result, free_result = PUBLISHED[name]
            side = md * Decimal("1.5")
            if count != expected_count or abs(float(side) - printed_side) > .005:
                raise ValueError(f"Source does not match paper Table 1: {name}")
            for variant, rotations, result in [
                ("nest-mb-given", {"kind": "list", "degrees": angles}, fixed_result),
                ("nest-mb-free", {"kind": "free"}, free_result),
            ]:
                job = make_job("", parts, side, side)
                for part in job["parts"]:
                    part["rotations"] = deepcopy(rotations)
                changes = sorted(p["id"] for p in parts if p["rotations"] != rotations)
                add("B", variant, job,
                    "Reconstruction of Martinez-Sykora et al. (2017), section 6.1 Nest-MB: square side = 1.5 * maximum initial part bbox dimension, using pinned OR-Datasets contours. Rotation rule follows Table 1 / Table 5. No scaling, simplification or sheet rounding.",
                    metric="normalized_material", published_instance="reconstructed",
                    publication=PAPER, publication_table=5, sheet_side=float(side),
                    printed_table_1_side=printed_side, rotation_overrides=changes,
                    published_name={"blaz1": "shapes2", "swim": "swimm"}.get(name, name),
                    published_result={"algorithm": "PBP", "bins": result[0],
                        "mean_squared_utilization": result[1],
                        "kind": "reported context; not a verified global best-known result",
                        "comparable_to_nestbolt_material": False})
    return jobs, rows


def check_frozen():
    manifest = json.loads(MANIFEST.read_bytes())
    if manifest["converter_sha256"] != digest(Path(__file__)):
        raise ValueError("Frozen converter changed; do not silently alter a benchmark")
    if manifest["source_manifest_sha256"] != digest(ROOT / "benchmarks/sources/strip-sources.json"):
        raise ValueError("Frozen source manifest changed")
    expected = set()
    for row in manifest["instances"]:
        path = DEST / row["path"]
        if path.resolve().parent not in [(DEST / "S").resolve(), (DEST / "B").resolve()]:
            raise ValueError("Unsafe dataset path")
        if digest(path) != row["sha256"]:
            raise ValueError(f"Frozen job changed: {row['id']}")
        expected.add(path.resolve())
    actual = {p.resolve() for group in ["S", "B"] for p in (DEST / group).glob("*.json")}
    if actual != expected:
        raise ValueError("Missing or unlisted academic jobs")
    print(f"Verified {len(expected)} frozen academic jobs offline.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true", help="One-time freeze; refuses an existing manifest")
    parser.add_argument("--check", action="store_true", help="Verify frozen files without network/source cache")
    args = parser.parse_args()
    if args.check:
        if args.freeze:
            parser.error("--check and --freeze are mutually exclusive")
        check_frozen()
        return
    if args.freeze and MANIFEST.exists():
        raise SystemExit("Academic benchmark already frozen; do not overwrite it")
    if not args.freeze and not MANIFEST.exists():
        raise SystemExit("Use --freeze once after reviewing source and construction rules")
    subprocess.run([sys.executable, "scripts/strip_sources.py"], cwd=ROOT, check=True)
    source_path = ROOT / "benchmarks/sources/strip-sources.json"
    jobs, rows = build(json.loads(source_path.read_bytes()))
    manifest = {"version": 1, "converter_sha256": digest(Path(__file__)),
        "source_manifest_sha256": digest(source_path),
        "licence_notice": "../sources/OR_DATASETS_LICENSE", "instances": rows,
        "paper": {"doi": PAPER, "author_manuscript": PAPER_PDF,
            "reviewed_pdf_sha256": "3cdad63b0922d436c3d2750cbf9f6c2e7aa9aeed205df2ee8b238c724c27e0e8",
            "relevant_sections": "6.1, Tables 1 and 5",
            "note": "PDF is a research reference only and is not redistributed. Source shapes come from the separately MIT-declared collection. This recreates the 11 overlapping Nest-MB families, not all 23 paper families. Exact original paper geometry hashes and current global BKRs are unavailable; reported scores are context only."}}
    if args.freeze:
        for relative in jobs:
            if (DEST / relative).exists():
                raise SystemExit(f"Refusing to overwrite existing candidate: {relative}")
        for relative, data in jobs.items():
            path = DEST / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        MANIFEST.write_bytes(serialized(manifest))
        print(f"Froze {len(jobs)} academic jobs: 13 S and 35 B.")
    else:
        if json.loads(MANIFEST.read_bytes()) != manifest:
            raise ValueError("Rebuilt manifest differs from frozen benchmark")
        for relative, data in jobs.items():
            path = DEST / relative
            if path.exists() and path.read_bytes() != data:
                raise ValueError(f"Refusing to overwrite changed job: {relative}")
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        print("Rebuilt original sources produce exactly the frozen academic jobs.")
    check_frozen()


if __name__ == "__main__":
    main()
