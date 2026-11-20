"""Check complete compaction proposals against original filled rings and stock."""
import argparse
from collections import defaultdict
import itertools
import json
from math import cos, sin
from pathlib import Path
from zipfile import ZipFile

from shapely.geometry import Polygon

RESULTS = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_bytes())


def geometry_check(layout, previous, job, request, last, metrics):
    parts = {p["id"]: p for p in job["parts"]}
    expected = {(k, i) for k, part in parts.items() for i in range(part["quantity"])}
    previous = {(p["part_id"], p["copy_index"]): p for p in previous["placements"]}
    ids = [(p["part_id"], p["copy_index"]) for p in layout["placements"]]
    assert set(ids) == set(previous) == expected and len(ids) == len(expected)
    assert len(layout["sheets"]) == 2 and len(job["stocks"]) == 1
    stock = job["stocks"][0]
    margin = stock["margins"]
    edge = request["edge_spacing_mm"]
    shapes = defaultdict(list)
    edge_slack = float("inf")
    moved = 0
    for p, identity in zip(layout["placements"], ids, strict=True):
        old = previous[identity]
        sheet = p["sheet_id"]
        assert old["sheet_id"] == sheet
        if sheet != last:
            assert old == p
        t = p["transform"]
        assert all(t[k] == old["transform"][k] for k in ("rotation_radians","mirrored"))
        moved += t["translation"] != old["transform"]["translation"]
        part = parts[p["part_id"]]
        ring = part["geometry"][0]["outer"]
        assert len(part["geometry"]) == 1 and (not t["mirrored"] or part["allow_mirror"])
        c,s = cos(t["rotation_radians"]),sin(t["rotation_radians"])
        sign = -1 if t["mirrored"] else 1
        dx,dy = t["translation"]
        shape = Polygon([(dx+sign*x*c-y*s,dy+sign*x*s+y*c) for x,y in ring])
        assert shape.is_valid and not shape.interiors
        x0,y0,x1,y1 = shape.bounds
        edge_slack = min(edge_slack, x0-margin["left"]-edge,y0-margin["bottom"]-edge,
                         stock["width"]-margin["right"]-edge-x1,stock["height"]-margin["top"]-edge-y1)
        shapes[sheet].append(shape)
    pairs = 0
    shortest = float("inf")
    top = []
    for sheet in shapes.values():
        for a,b in itertools.combinations(sheet, 2):
            shortest = min(shortest,a.distance(b))
            pairs += 1
        top.append(max(s.bounds[3] for s in sheet)+edge+margin["top"])
    used = min(top)
    calculated_area = stock["width"] * (stock["height"]+used)
    height_difference = abs(calculated_area-metrics["material_area"])/stock["width"]
    return dict(parts=len(ids), moved=moved, pairs=pairs, shortest_distance_mm=shortest,
                minimum_edge_slack_mm=edge_slack, material_height_difference_mm=height_difference,
                meets_source_tolerance=(shortest >= request["spacing_mm"]-1e-7 and edge_slack >= -1e-7
                                        and height_difference <= 2e-6))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    cases = read(RESULTS/"h5-archived-sheet-combinations-20261120/construction.json")
    valid = []
    for i,case in enumerate(cases):
        folder = args.output/f"case{i}"
        initial = read(folder/"initial.json")
        request = read(folder/"request.json")
        job = read(RESULTS.parent/"datasets/M"/(case["job"]+".json"))
        with ZipFile(RESULTS/"h5-common-development-20261015T142414Z"/case["canonical"]) as archive:
            assert archive.read("library.json") == (folder/"library.json").read_bytes()
            assert archive.read("request.json") == (folder/"request.json").read_bytes()
            assert [p["geometry"][0]["outer"] for p in json.loads(archive.read("nested/job.json"))["parts"]] == [
                p["geometry"][0]["outer"] for p in job["parts"]]
        row = read(folder/"result.json")
        reports = []
        last = read(folder/"initial-validate.json")["metrics"]["last_sheet_id"]
        for path in [folder/"initial.json",*sorted(folder.glob("iteration-?.json"))]:
            native = read(folder/(path.stem+"-validate.json"))
            if not native["valid"]:
                reports.append(dict(layout=path.name, native_valid=False))
                continue
            g = geometry_check(read(path), initial, job, request, last, native["metrics"])
            reports.append(dict(layout=path.name, native_valid=True, **g))
        valid.append(dict(job=case["job"],kerf=case["kerf"], selected=row["selected"], checks=reports))
    with (args.output/"geometry-audit.json").open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(valid,stream,indent=2)
        stream.write("\n")
    print([(r["job"],r["kerf"],len(r["checks"]),min(v["minimum_edge_slack_mm"] for v in r["checks"] if v["native_valid"]))
           for r in valid])
    if not all(not v["native_valid"] or v["meets_source_tolerance"] for r in valid for v in r["checks"]):
        raise SystemExit("At least one native-valid layout exceeded the independent source tolerance")


if __name__ == "__main__":
    main()
