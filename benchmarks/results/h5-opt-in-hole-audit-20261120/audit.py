"""Verify the opt-in H5 matrix against archived requests, solids, and cutting exports."""
import argparse
from collections import Counter
from io import StringIO
from itertools import combinations
import json
from math import cos, sin, dist
from pathlib import Path
import re
from statistics import median
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

import ezdxf
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from h5_cutting_report import distribution, verify_rows

EPS = 0.000003
SVG = "{http://www.w3.org/2000/svg}"


def segment_key(a, b):
    # All numbers in the two cutting formats have six decimal places in mm.
    return tuple(sorted(tuple(round(v * 1e6) for v in p[:2]) for p in (a, b)))


def audit_sheet(zipfile, sheet, stock_height, job, layout, report, straight_ring=None):
    parts = {p["id"]: p for p in job["parts"]}
    solids = {}
    owners = {}
    for p in layout["placements"]:
        if p["sheet_id"] != sheet:
            continue
        item = parts[p["part_id"]]["geometry"]
        assert len(item) == 1
        t = p["transform"]
        c, s = cos(t["rotation_radians"]), sin(t["rotation_radians"])
        dx, dy = t["translation"]
        sign = -1 if t["mirrored"] else 1
        def transform(ring):
            return [(dx + c*sign*x - s*y, dy + s*sign*x + c*y) for x,y in ring]
        solid = Polygon(transform(item[0]["outer"]), [transform(h) for h in item[0]["holes"]])
        key = f"{p['part_id']}#{p['copy_index']}"
        assert solid.is_valid and key not in solids
        solids[key] = solid
        owners[key] = Polygon(solid.exterior)
    distances = [a.distance(b) for a,b in combinations(solids.values(),2)]
    min_gap = min(distances,default=None)
    kerf = job["clearance"]
    if min_gap is not None:
        assert min_gap >= kerf - EPS, (sheet, "part gap", min_gap, kerf)
    riders, wall_gaps = set(), []
    for name, shape in solids.items():
        for ring in shape.interiors:
            void = Polygon(ring)
            for candidate, exterior in owners.items():
                if candidate != name and void.contains(exterior):
                    riders.add(candidate)
                    wall_gaps.append(void.boundary.distance(exterior))
    assert not wall_gaps or min(wall_gaps) >= kerf - EPS
    answer = dict(sheet=sheet, parts=len(solids), pair_distances=len(distances),
                  min_gap=min_gap, riders=len(riders), minimum_hole_wall_gap=min(wall_gaps,default=None))
    if report is None:
        return answer
    assert abs(sum(p.length for p in solids.values()) - report["cut_length_without_common_mm"]) < 1e-6
    assert report["contours_without_common"] == sum(1+len(p.interiors) for p in solids.values())
    # Derive offset segments for each owner's exterior only. Check the entire
    # span (both endpoints against a single segment) for each reported owner.
    from shapely.geometry import LineString, Point
    offsets = {}
    for name, exterior in owners.items():
        coords = list(orient(exterior,sign=1.0).exterior.coords)
        if straight_ring is not None:
            coords = straight_ring(coords)
        edges = []
        for a, b in zip(coords,coords[1:]):
            length = dist(a,b)
            if length < 10 - EPS:
                continue
            x, y = (b[1]-a[1])*kerf/(2*length), (a[0]-b[0])*kerf/(2*length)
            edges.append(LineString([(a[0]+x,a[1]+y),(b[0]+x,b[1]+y)]))
        offsets[name] = edges
    max_error = 0.0
    raw_shared = []
    for edge in report["shared_edges"]:
        ends = [Point(edge[k]) for k in ("from_mm","to_mm")]
        assert ends[0].distance(ends[1]) >= 10 - EPS
        raw_shared.append(LineString([edge["from_mm"],edge["to_mm"]]))
        names = [o["part_copy"] for o in edge["owners"]]
        assert len(set(names)) == 2
        for name in names:
            err = min(max(line.distance(e) for e in ends) for line in offsets[name])
            assert err <= 0.01 + EPS, (name, err, sheet, edge["from_mm"], edge["to_mm"])
            max_error = max(max_error, err)
    # Independently read the SVG and DXF. Match every emitted CUT and COMMON
    # segment including multiplicity, reversing the SVG viewBox's vertical axis.
    svg = ET.fromstring(zipfile.read(f"nested/{sheet}.svg"))
    dxf = ezdxf.read(StringIO(zipfile.read(f"nested/{sheet}.dxf").decode("utf-8")))
    assert dxf.units == 4 and svg.attrib["height"] == f"{stock_height:g}mm"
    entity_errors = dxf.audit()
    assert not entity_errors.errors and not entity_errors.fixes
    layer_sizes = {}
    seen_parts = set()
    maximum_cut_error = 0.0
    for layer in ("CUT","COMMON"):
        expected = Counter()
        group = svg.find(f"{SVG}g[@id='{layer}']")
        for path in group if group is not None else ():
            assert path.tag == SVG+"path"
            lines = re.findall(r"[A-Za-z]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", path.attrib["d"])
            i = 0
            rings = []
            while i < len(lines):
                op = lines[i]
                i += 1
                if op in ("M","L"):
                    point = (float(lines[i]),stock_height-float(lines[i+1]))
                    i += 2
                    if op == "M":
                        rings.append([])
                        start = point
                    elif last != point:
                        expected[segment_key(last,point)] += 1
                    rings[-1].append(point)
                    last = point
                else:
                    assert op == "Z"
                    if last != start:
                        expected[segment_key(last,start)] += 1
                    last = start
            if layer == "CUT":
                identity = path.attrib["id"]
                assert identity not in seen_parts
                seen_parts.add(identity)
                original = solids[identity]
                source_rings = [original.exterior, *original.interiors]
                assert len(rings) == len(source_rings)
                for points, source in zip(rings,source_rings):
                    assert len(points) == len(source.coords)
                    error = max(dist(a,b) for a,b in zip(points,source.coords))
                    assert error <= EPS, (sheet,identity,error)
                    maximum_cut_error = max(maximum_cut_error,error)
        actual = Counter()
        for e in dxf.modelspace().query(f'*[layer=="{layer}"]'):
            assert e.dxftype() == "LINE"
            actual[segment_key(tuple(e.dxf.start),tuple(e.dxf.end))] += 1
        assert expected == actual, (sheet, layer, (expected-actual).most_common(2), (actual-expected).most_common(2))
        if layer == "COMMON":
            assert all(n == 1 for n in actual.values())
            assert bool(raw_shared) == bool(actual)
            if actual:
                from shapely.ops import unary_union
                emitted = [LineString([(x/1e6,y/1e6) for x,y in edge]) for edge in actual]
                union = unary_union(emitted)
                assert abs(sum(line.length for line in emitted)-union.length) <= EPS
                assert abs(union.length-report["shared_length_mm"]) <= len(emitted)*EPS
                assert union.hausdorff_distance(unary_union(raw_shared)) <= 0.01 + EPS
        layer_sizes[layer] = sum(actual.values())
    assert seen_parts == set(solids)
    return dict(**answer, maximum_cut_vertex_error_mm=maximum_cut_error, shared_edges=len(report["shared_edges"]), largest_offset_error_mm=max_error,
                exported_segments=layer_sizes)


def audit_archive(path, straight_ring=None):
    with ZipFile(path) as archive:
        job, layout, report = [json.loads(archive.read("nested/"+n+".json")) for n in ("job","layout","report")]
        assert job["units"] == "mm" and report["validation"]["valid"]
        stocks = {s["id"]:s for s in job["stocks"]}
        reports = {s["sheet_id"]:s for s in report.get("common_line",[])}
        sheets = [audit_sheet(archive,s["id"],stocks[s["stock_id"]]["height"],job,layout,reports.get(s["id"]),straight_ring)
                  for s in layout["sheets"]]
        assert sum(s["riders"] for s in sheets) == report["parts_in_holes"]
        return sheets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("measurement",type=Path)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    raw = json.loads((args.measurement/"results.json").read_bytes())
    assert raw["seconds"]==60 and raw["seeds"]==[0,1,2] and raw["kerfs_mm"]==[0.2,1.5]
    assert raw["common_line_allow_part_in_hole"] and not raw["held_out_geometry_read"]
    assert len(set(raw["jobs"]))==13 and raw["total"]==234
    expected = {(j,k,s,a) for j in raw["jobs"] for k in raw["kerfs_mm"] for s in raw["seeds"] for a in ("normal","off","bonus")}
    assert len(raw["rows"])==234 and {(r["job"],r["kerf_mm"],r["seed"],r["arm"]) for r in raw["rows"]}==expected
    members = verify_rows(args.measurement,raw["rows"])
    original = json.loads((args.measurement.parent / "h5-common-development-20261015T142414Z/results.json").read_bytes())
    assert original["guards"]["manifest"] == raw["guards"]["manifest"]
    historical_normal = {(p["job"],p["kerf_mm"]): p["normal_material"] for p in original["pairs"]}
    mechanical, arms, gates = [], [], []
    for r in raw["rows"]:
        if r["status"]=="valid" and r["job"].startswith("m-mechanical"):
            mechanical.append(dict(archive=r["archive"],sheets=audit_archive(args.measurement/r["archive"])))
    for k in raw["kerfs_mm"]:
        savings, costs, historical_costs = [], {}, {}
        for j in raw["jobs"]:
            matched = {}
            for a in ("normal","off","bonus"):
                rows = [r for r in raw["rows"] if (r["job"],r["kerf_mm"],r["arm"])==(j,k,a)]
                item = dict(job=j,kerf_mm=k,arm=a,statuses=dict(Counter(r["status"] for r in rows)))
                if all(r["status"]=="valid" for r in rows):
                    item["material"] = distribution([r["material"] for r in rows])
                    item["riders"] = distribution([r["parts_in_holes"] for r in rows])
                    if a!="normal":
                        item["saved_fraction"] = distribution([1-r["cut_with_common_mm"]/r["cut_without_common_mm"] for r in rows])
                        item["saved_mm"] = distribution([r["cut_without_common_mm"]-r["cut_with_common_mm"] for r in rows])
                    matched[a] = item
                arms.append(item)
            if len(matched)==3:
                savings.append(matched["bonus"]["saved_fraction"]["median"])
                used = matched["bonus"]["material"]["median"]
                costs[j] = 100*(used/matched["normal"]["material"]["median"]-1)
                historical_costs[j] = 100*(used/historical_normal[(j,k)]-1)
        gates.append(dict(kerf_mm=k,complete_jobs=len(costs),median_saved_fraction=median(savings) if savings else None,
                          material_cost_percent=costs,material_vs_october_normal_percent=historical_costs,passed=len(costs)==13 and median(savings)>=0.10 and max(costs.values())<=1.0))
    output = dict(source=raw["product_commit"],verified_archives=len(raw["rows"]),verified_members=members,
                  statuses=dict(Counter(r["status"] for r in raw["rows"])),gates=gates,arms=arms,mechanical=mechanical)
    args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(gates))


if __name__=="__main__":
    main()
