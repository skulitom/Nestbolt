"""Independently compare flat G6 training SVGs with placed, imported curves.

Run using the shop verification environment after h2_fidelity.py. The checker
uses svgpathtools and Shapely and reads the exported coordinates in millimetres.
"""
import argparse
from importlib.metadata import version
from hashlib import sha256
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import numpy as np
from scipy.optimize import linear_sum_assignment
from shapely.geometry import LineString
from svgpathtools import parse_path

from h3_geometry_audit import product_paths
from maker_geometry import flatten_segment

LIMIT = 0.01
TOLERANCE = 0.0005
SVG = "{http://www.w3.org/2000/svg}"


def load(path):
    return json.loads(path.read_bytes())


def line(path, transform):
    points = []
    for segment in path:
        points.extend(transform(p) for p in flatten_segment(segment, TOLERANCE)[:-1])
    points.append(transform(path.end))
    if abs(points[0] - points[-1]) > LIMIT:
        raise ValueError("Open cutting contour")
    return LineString((p.real, p.imag) for p in points)


def compare_contours(expected, actual):
    if len(actual) != len(expected) or not expected:
        raise ValueError(f"Expected {len(expected)} contours, found {len(actual)}")
    costs = np.full((len(expected), len(actual)), np.inf)
    bounds_before = [ring.bounds for ring in expected]
    bounds_after = [ring.bounds for ring in actual]
    for i, before in enumerate(expected):
        for j, after in enumerate(actual):
            if (
                max(abs(a - b) for a, b in zip(bounds_before[i], bounds_after[j]))
                <= LIMIT
            ):
                distance = before.hausdorff_distance(after)
                if math.isfinite(distance) and distance <= LIMIT:
                    costs[i, j] = distance
    try:
        rows, cols = linear_sum_assignment(costs)
    except ValueError as error:
        raise ValueError("No one-to-one contour match within 0.01 mm") from error
    return float(costs[rows, cols].max())


def measure(svg, stock, parts, placements):
    root = ET.parse(svg).getroot()
    w, h = stock["width"], stock["height"]
    if root.tag != SVG + "svg" or any(
        {"transform", "display", "visibility", "clip-path", "mask", "style"}
        & e.attrib.keys()
        for e in root.iter()
    ):
        raise ValueError("Expected a flat G6 cutting SVG")
    page = [float(v) for v in root.attrib["viewBox"].split()]
    physical = [root.attrib[k] for k in ("width", "height")]
    if len(page) != 4 or any(not v.endswith("mm") for v in physical):
        raise ValueError("Missing physical stock dimensions")
    actual = page + [float(v[:-2]) for v in physical]
    if not all(
        math.isclose(a, b, abs_tol=1e-6, rel_tol=0)
        for a, b in zip(actual, [0, 0, w, h, w, h])
    ):
        raise ValueError("Physical SVG viewport differs from the stock")
    groups = root.findall(SVG + "g")
    if (
        len(groups) != 1
        or groups[0].get("id") != "CUT"
        or groups[0].get("stroke") != "#000000"
    ):
        raise ValueError("Expected the black CUT group")
    if any(e.tag not in (SVG + "title", SVG + "g") for e in root):
        raise ValueError("Unexpected content outside CUT")
    if any(e.tag == SVG + "title" and len(e) for e in root):
        raise ValueError("Unexpected geometry inside SVG title")
    wanted = {p["part_id"] + "#" + str(p["copy_index"]): p for p in placements}
    if len(wanted) != len(placements):
        raise ValueError("Duplicate placement identifiers")
    count = 0
    maximum = 0.0
    for shape in groups[0]:
        if shape.tag != SVG + "path":
            raise ValueError("Unexpected geometry in CUT")
        stroke = shape.get("stroke", "inherit").strip().lower()
        if stroke not in ("inherit", "#000000", "#000", "black"):
            raise ValueError("Expected a black stroke on each CUT path")
        placement = wanted.pop(shape.attrib["id"])
        tx, ty = placement["transform"]["translation"]
        angle = placement["transform"]["rotation_radians"]
        rot = complex(math.cos(angle), math.sin(angle))
        mirrored = placement["transform"]["mirrored"]

        def placed(z):
            q = complex(-z.real if mirrored else z.real, z.imag) * rot + complex(tx, ty)
            return complex(q.real, h - q.imag)

        part = parts[placement["part_id"]]
        curves = [part["outer"], *part["holes"]]
        before = [
            line(p, placed)
            for p in product_paths({"paths": [{"curve": c} for c in curves]})
        ]
        commands = [
            s for s in re.split(r"(?=[Mm])", shape.attrib["d"].strip()) if s.strip()
        ]
        if any(s[0] != "M" or not s.rstrip().endswith(("z", "Z")) for s in commands):
            raise ValueError("Expected explicitly closed absolute SVG subpaths")
        after = [line(parse_path(s), lambda p: p) for s in commands]
        maximum = max(maximum, compare_contours(before, after))
        count += len(before)
    if wanted:
        raise ValueError("Missing exported placements")
    return dict(placements=len(placements), contours=count, max_hausdorff_mm=maximum)


def check_case(exports):
    layout = load(exports / "layout.json")
    job = load(exports / "job.json")
    parts = {p["id"]: p for p in load(exports / "library.json")["parts"]}
    stocks = {s["id"]: s for s in job["stocks"]}
    assert layout["units"] == "mm" and job["units"] == "mm"
    sheet_ids = {s["id"] for s in layout["sheets"]}
    assert len(sheet_ids) == len(layout["sheets"])
    assert all(p["sheet_id"] in sheet_ids for p in layout["placements"])
    expected = {sheet_id + ".svg" for sheet_id in sheet_ids}
    assert expected and expected == {p.name for p in exports.glob("*.svg")}
    results = []
    for sheet in layout["sheets"]:
        drawing = exports / (sheet["id"] + ".svg")
        selected = [p for p in layout["placements"] if p["sheet_id"] == sheet["id"]]
        results.append(
            dict(
                sheet=sheet["id"],
                sha256=sha256(drawing.read_bytes()).hexdigest(),
                **measure(drawing, stocks[sheet["stock_id"]], parts, selected),
            )
        )
    return results


def main():
    if not __debug__:
        raise SystemExit(
            "Run without Python -O to verify the frozen training split and all sheets."
        )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "benchmarks/datasets/shop/manifest.json",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--work-dir",
        type=Path,
        help="Location of the retained G6 output if it has moved",
    )
    args = parser.parse_args()
    report = load(args.report)
    manifest = args.manifest.read_bytes()
    assert sha256(manifest).hexdigest() == report["manifest_sha256"]
    training = {
        r["path"]
        for r in json.loads(manifest)["files"]
        if r["split"] == "training"
        and r.get("label")
        and Path(r["path"]).suffix.lower() in (".dxf", ".svg")
    }
    by_path = {r["path"]: r for r in report["rows"]}
    assert (
        by_path.keys() == training
        and len(by_path) == len(report["rows"])
        and report["only"] is None
        and report["held_out_read"] is False
    )
    seen = set()
    sheets = []
    for folder in sorted((args.work_dir or Path(report["work_directory"])).iterdir()):
        if not folder.is_dir():
            continue
        row = load(folder / "result.json")
        assert row == by_path[row["path"]] and row["path"] not in seen
        seen.add(row["path"])
        if row["status"] == "rejected":
            continue
        assert row["status"] == "passed"
        try:
            measured = check_case(folder / "exports")
        except Exception as e:
            raise RuntimeError(f"SVG verification failed on {row['path']}") from e
        sheets.extend(dict(source=row["path"], **s) for s in measured)
    assert seen == training
    comparison = {
        "method": "Symmetric vertex-to-polyline Hausdorff distance with both curves subdivided at 0.0005 mm; one-to-one matches within each saved placement",
        "limit_mm": LIMIT,
        "flatten_tolerance_mm": TOLERANCE,
        "reader_versions": {
            n: version(n) for n in ("svgpathtools", "shapely", "scipy")
        },
        "runner_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "fidelity_sha256": sha256(args.report.read_bytes()).hexdigest(),
        "sheets": len(sheets),
        "placements": sum(s["placements"] for s in sheets),
        "contours": sum(s["contours"] for s in sheets),
        "max_hausdorff_mm": max(s["max_hausdorff_mm"] for s in sheets),
        "rows": sheets,
    }
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(comparison, stream, indent=2)
        stream.write("\n")
    print({k: v for k, v in comparison.items() if k != "rows"})


if __name__ == "__main__":
    main()
