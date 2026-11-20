"""Independently check each proposed layout against straight source paths and matched controls."""
from collections import Counter, defaultdict
import argparse
import json
from math import cos, sin
from pathlib import Path
from statistics import median
from zipfile import ZipFile

import numpy as np
import shapely
from shapely.affinity import affine_transform
from shapely.geometry import Polygon
from replay import MATRICES


def read(path):
    return json.loads(path.read_bytes())


def ring(outline):
    assert all(s["kind"] == "line" for s in outline["segments"])
    return [outline["start"],*[s["to"] for s in outline["segments"]]]


def check(layout,baseline,source,request,validation):
    def ids(l):
        return Counter((p["part_id"],p["copy_index"]) for p in l["placements"])
    assert ids(layout) == ids(baseline) and layout["sheets"] == baseline["sheets"]
    assert len(layout["placements"]) == sum(p["quantity"] for p in request["parts"]) == 80
    shapes = {p["id"]:Polygon(ring(p["outer"]),[ring(h) for h in p["holes"]]) for p in source["parts"]}
    limits = {p["id"]:p for p in request["parts"]}
    edge = request["edge_spacing_mm"]
    stock, = request["sheets"]
    assert stock["margins_mm"] == dict(top=0,bottom=0,left=0,right=0)
    assert not stock["defects_mm"] and not stock["outline_mm"]
    sheets = defaultdict(list)
    for p in layout["placements"]:
        trans = p["transform"]
        angle = trans["rotation_radians"]
        assert not trans["mirrored"] and not limits[p["part_id"]]["allow_mirror"]
        assert any(abs((angle - np.deg2rad(d) + np.pi)%(2*np.pi)-np.pi) < 1e-7
                   for d in limits[p["part_id"]]["rotations"]["degrees"])
        shape = affine_transform(shapes[p["part_id"]],[cos(angle),-sin(angle),sin(angle),cos(angle),
                                                       *trans["translation"]])
        l,b,r,t = shape.bounds
        assert min(l,b,stock["width_mm"]-r,stock["height_mm"]-t) >= edge-0.000003
        sheets[p["sheet_id"]].append(shape)
    distances = []
    for solids in sheets.values():
        i,j = np.triu_indices(len(solids),1)
        arr = np.array(solids,dtype=object)
        distances.extend(shapely.distance(arr[i],arr[j]).tolist())
    assert min(distances) >= request["spacing_mm"]-0.000003
    last = layout["sheets"][-1]["id"]
    top = max(s.bounds[3] for s in sheets[last])+edge
    material = (len(sheets)-1) + top/stock["height_mm"]
    assert abs(validation["metrics"]["normalized_material"]-material) < 0.00000004
    length = sum(s.length for solids in sheets.values() for s in solids)
    assert abs(length-sum(c["cut_length_without_common_mm"] for c in validation["common_line"])) < 1e-6
    return len(distances),min(distances)


def main(root,dest):
    checks = []
    sets = []
    for matrix in MATRICES:
        result = Path(__file__).resolve().parents[1]/matrix
        control, = [p["normal_material"] for p in read(result/"results.json")["pairs"]
                    if p["job"]=="c-bracket-mixed" and p["kerf_mm"]==0.2]
        per_method = defaultdict(list)
        for seed in range(3):
            for arm in ("off","bonus"):
                stem = f"c-bracket-mixed-k0.2-s{seed}-{arm}"
                folder = root/matrix/stem
                with ZipFile(result/f"{stem}.zip") as z:
                    source, request, layout, original = [json.loads(z.read(n)) for n in
                        ("library.json","request.json","nested/layout.json","validate-stdout.json")]
                candidates = []
                for path in sorted(folder.glob("*-validation.json")):
                    name = path.name.removesuffix("-validation.json")
                    validation = read(path)
                    if not validation["valid"]:
                        continue
                    trial = read(folder/f"{name}.json")
                    comparisons,gap = check(trial,layout,source,request,validation)
                    amount = validation["metrics"]["normalized_material"]
                    cut = sum(r["saved_length_mm"] for r in validation["common_line"])
                    checks.append(dict(matrix=matrix,seed=seed,arm=arm,method=name,pairs=comparisons,
                                       minimum_gap_mm=gap,material=amount,saved_mm=cut))
                    if arm=="bonus":
                        per_method[name].append((seed,amount))
                    candidates.append((amount,cut,name))
                if arm == "bonus":
                    before = original["metrics"]["normalized_material"]
                    cut_before = sum(r["saved_length_mm"] for r in original["common_line"])
                    candidates.append((before,cut_before,"original"))
                    per_method["original"].append((seed,before))
                    for key,choices in [("best_observed",candidates),("best_with_all_original_cut_savings",
                                        [r for r in candidates if r[1]>=cut_before-1e-7])]:
                        per_method[key].append((seed,min(choices)[0]))
        summary = {}
        for k,rows in per_method.items():
            if len(rows) == 3:
                med = median(v for _,v in rows)
                summary[k] = dict(median=med,change_percent=100*(med/control-1))
        sets.append(dict(matrix=matrix,ordinary=control,maximum=1.01*control,methods=summary))
    report = dict(valid_candidates=len(checks),same_sheet_distances=sum(r["pairs"] for r in checks),
                  closest_mm=min(r["minimum_gap_mm"] for r in checks),geos=shapely.geos_version_string,
                  measurements=sets,rows=checks)
    dest.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    for s in sets:
        print(s["matrix"],{k:round(s["methods"][k]["change_percent"],4) for k in
                           ("original","free-down-left-down","best_observed","best_with_all_original_cut_savings")})
    print(report["valid_candidates"],report["same_sheet_distances"],report["closest_mm"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work",type=Path)
    parser.add_argument("report",type=Path)
    args = parser.parse_args()
    main(args.work,args.report)
