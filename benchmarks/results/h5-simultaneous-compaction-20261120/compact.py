"""Compact a complete mechanical layout with simultaneous translation constraints."""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from math import cos, sin
from pathlib import Path
import subprocess
from zipfile import ZipFile

import numpy as np
import shapely
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from shapely.affinity import affine_transform
from shapely.geometry import Polygon

RESULTS = Path(__file__).resolve().parents[1]
SAVED = RESULTS / "h5-archived-sheet-combinations-20261120"
RADIUS = 150.0
PAD = 0.000005


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def execute(folder, binary, action, path, *extra):
    args = [binary, action, "--library", "library.json", "--request", "request.json", "--layout", path, *extra]
    p = subprocess.run(args, cwd=folder, capture_output=True)
    stem = f"{path.stem}-{action}"
    (folder / f"{stem}.json").write_bytes(p.stdout)
    (folder / f"{stem}.stderr").write_bytes(p.stderr)
    return json.loads(p.stdout) if p.stdout.strip() else {"valid": False, "error": p.stderr.decode(errors="replace")}


def polygon_at(shape, placement):
    t = placement["transform"]
    c, s = cos(t["rotation_radians"]), sin(t["rotation_radians"])
    sign = -1 if t["mirrored"] else 1
    return affine_transform(shape, [sign*c, -s, sign*s, c, *t["translation"]])


class Region:
    def __init__(self, convex_parts):
        self.parts = convex_parts
        self.hull = convex_parts[0] if len(convex_parts) == 1 else shapely.union_all(convex_parts).convex_hull
        self.bounds = self.hull.bounds
        self.children = None

    def split(self):
        if self.children is None:
            x0, y0, x1, y1 = self.bounds
            axis = 0 if x1-x0 > y1-y0 else 1
            parts = sorted(self.parts, key=lambda s: s.centroid.coords[0][axis])
            mid = len(parts)//2
            self.children = Region(parts[:mid]), Region(parts[mid:])
        return self.children


def separating_lines(a, b, kerf):
    x0, y0, x1, y1 = a.bounds
    u0, v0, u1, v1 = b.bounds
    # The maximum relative movement on either axis is twice the trust radius.
    if max(u0-x1, x0-u1, v0-y1, y0-v1) > 2*RADIUS + kerf + PAD:
        return
    segment = shapely.shortest_line(a.hull, b.hull)
    length = segment.length
    if length > 0 and (length >= kerf - 1e-5 or len(a.parts) == len(b.parts) == 1):
        (x, y), (u, v) = segment.coords
        yield (u-x)/length, (v-y)/length, length
    elif len(a.parts) >= len(b.parts) and len(a.parts) > 1:
        for child in a.split():
            yield from separating_lines(child, b, kerf)
    elif len(b.parts) > 1:
        for child in b.split():
            yield from separating_lines(a, child, kerf)
    else:
        raise ValueError("Intersecting convex source pieces have no positive separating distance")


def compact(active, pieces, stock, edge, kerf):
    regions = [Region([polygon_at(s, p) for s in pieces[p["part_id"]]]) for p in active]
    n = len(regions)
    h = 2*n
    rows, cols, vals, rhs = [], [], [], []
    def constraint(entries, bound):
        for col, value in entries:
            rows.append(len(rhs))
            cols.append(col)
            vals.append(value)
        rhs.append(bound)
    margins = stock["margins"]
    bounds = []
    for i, region in enumerate(regions):
        x0, y0, x1, y1 = region.bounds
        bounds.extend([(max(-RADIUS, margins["left"]+edge+PAD-x0),
                        min(RADIUS, stock["width"]-margins["right"]-edge-PAD-x1)),
                       (max(-RADIUS, margins["bottom"]+edge+PAD-y0),
                        min(RADIUS, stock["height"]-margins["top"]-edge-PAD-y1))])
        constraint([(2*i+1, 1), (h, -1)], -y1-margins["top"]-edge)
        for j in range(i):
            for nx, ny, distance in separating_lines(regions[j], region, kerf):
                constraint([(2*j,nx), (2*j+1,ny), (2*i,-nx), (2*i+1,-ny)], distance-kerf-PAD)
    bounds.extend([(0, stock["height"]), *[(0, RADIUS)]*(2*n)])
    for i in range(2*n):
        constraint([(i, 1), (h+1+i,-1)], 0)
        constraint([(i,-1), (h+1+i,-1)], 0)
    matrix = coo_matrix((vals, (rows,cols)), shape=(len(rhs),len(bounds))).tocsr()
    def solve(objective):
        cost = np.zeros(len(bounds))
        cost[objective] = 1
        return linprog(cost, A_ub=matrix, b_ub=rhs, bounds=bounds, method="highs",
                       options={"threads": 1, "time_limit": 3, "primal_feasibility_tolerance": 1e-8})
    first = solve(h)
    diagnostics = {"constraints":len(rhs), "height_status":first.message}
    if not first.success:
        return None, diagnostics
    bounds[h] = (0, first.x[h]+0.00001)
    second = solve(slice(h+1,None))
    diagnostics.update(least_movement_status=second.message, optimum_height_mm=first.x[h])
    if not second.success:
        return None, diagnostics
    return second.x[:h].reshape(n,2), diagnostics


def measurements(report):
    cutting = report["common_line"]
    length = sum(s["cut_length_without_common_mm"] for s in cutting)
    saved = sum(s["saved_length_mm"] for s in cutting)
    m = report["metrics"]
    return dict(material_mm2=m["material_area"], last_height_mm=m["last_sheet_used_height"],
                parts=m["placed_parts"], cut_length_after_sharing_mm=length-saved,
                saved_length_mm=saved, saved_percent=100*saved/length)


def run(folder, index, binary):
    case = read(SAVED / "construction.json")[index]
    key = f"{case['job']}-{case['kerf']}"
    with ZipFile(SAVED / "layouts-and-exports.zip") as z:
        (folder / "initial.json").write_bytes(z.read(f"{key}/layout.json"))
    with ZipFile(RESULTS / "h5-common-development-20261015T142414Z" / case["canonical"]) as z:
        for f in ("library.json", "request.json"):
            (folder / f).write_bytes(z.read(f))
        job = json.loads(z.read("nested/job.json"))
    request = read(folder / "request.json")
    assert request["common_line"]["kerf_mm"] == request["spacing_mm"] == case["kerf"]
    assert len(job["stocks"]) == 1 and not (job["stocks"][0]["outline"] or job["stocks"][0]["defects"])
    pieces = {}
    for part in job["parts"]:
        assert len(part["geometry"]) == 1
        poly = Polygon(part["geometry"][0]["outer"])
        items = [poly] if poly.equals(poly.convex_hull) else list(shapely.constrained_delaunay_triangles(poly).geoms)
        assert shapely.union_all(items).equals(poly) and all(s.equals(s.convex_hull) for s in items)
        pieces[part["id"]] = items
    best_path = folder / "initial.json"
    best = read(best_path)
    report = execute(folder, binary, "validate", best_path)
    assert report["valid"] and report["metrics"]["placed_parts"] == report["metrics"]["requested_parts"]
    initial = measurements(report)
    best_metrics = initial
    sheet = report["metrics"]["last_sheet_id"]
    history = []
    for step in range(4):
        candidate = deepcopy(best)
        active = [p for p in candidate["placements"] if p["sheet_id"] == sheet]
        delta, record = compact(active, pieces, job["stocks"][0], job["edge_clearance"], case["kerf"])
        history.append(record)
        if delta is None:
            break
        for p, shift in zip(active, delta, strict=True):
            original = p["transform"]["translation"]
            p["transform"]["translation"] = [v+d for v,d in zip(original,shift)]
        path = folder / f"iteration-{step+1}.json"
        write(path, candidate)
        report = execute(folder, binary, "validate", path)
        record["native_valid"] = report["valid"]
        if not report["valid"]:
            break
        current = measurements(report)
        record.update(current)
        improvement = best_metrics["last_height_mm"] - current["last_height_mm"]
        if current["material_mm2"] < best_metrics["material_mm2"]:
            best, best_path, best_metrics = candidate, path, current
        if improvement < 0.001:
            break
    execute(folder, binary, "export", best_path, "--out-dir", "export")
    for ext in ["svg","dxf"]:
        assert {p.stem for p in (folder/"export").glob("*."+ext)} == {"sheet-0","sheet-1"}
    result = dict(job=case["job"], kerf=case["kerf"], target_mm2=case["target_mm2"],
                  initial=initial, history=history, best=best_metrics, selected=best_path.name,
                  binary_sha256=sha256(binary.read_bytes()).hexdigest())
    write(folder / "result.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("case", type=int)
    parser.add_argument("binary", type=Path)
    args = parser.parse_args()
    run(args.output.resolve(), args.case, args.binary.resolve())
