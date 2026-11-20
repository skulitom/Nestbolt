"""Rebuild the last rectangular sheet from its full inventory using bottom-left placements."""
import argparse
from copy import deepcopy
import json
from math import pi
from pathlib import Path
import subprocess
from zipfile import ZipFile

import numpy as np
from replay import MATRICES, PAD, rectangles, saved
from relocate import boxes, bottom_left


def pack(job, layout, last):
    parts = {p["id"]: p for p in job["parts"]}
    pieces = {key: [r for g in p["geometry"] for r in rectangles(g)] for key,p in parts.items()}
    active = [p for p in layout["placements"] if p["sheet_id"] == last]
    stock, = job["stocks"]
    assert not stock["outline"] and not stock["defects"]
    templates = {}
    area = {}
    for key, p in parts.items():
        area[key] = sum((x1-x0)*(y1-y0) for x0,y0,x1,y1 in pieces[key])
        assert not any(q["transform"]["mirrored"] for q in active if q["part_id"] == key)
        templates[key] = [(d, boxes(pieces, {"part_id":key, "transform":{
            "translation":[0,0], "rotation_radians": d*pi/180, "mirrored":False}}))
            for d in p["rotations"]["degrees"]]
    heights = [min(boxes(pieces, p)[:,2]) for p in active]
    orders = {
        "original-height": sorted(range(len(active)), key=heights.__getitem__),
        "decreasing-area": sorted(range(len(active)), key=lambda i: -area[active[i]["part_id"]]),
        "increasing-area": sorted(range(len(active)), key=lambda i: area[active[i]["part_id"]]),
    }
    for name, order in orders.items():
        fixed = np.empty((0, 4))
        trial = deepcopy(layout)
        current = [p for p in trial["placements"] if p["sheet_id"] == last]
        for i in order:
            best = None
            for d, template in templates[current[i]["part_id"]]:
                xy = bottom_left(fixed, template, stock, job["edge_clearance"], job["clearance"]+PAD,
                                 stock["height"])
                if xy is None:
                    continue
                x, y = xy
                actual = template + [x,x,y,y]
                score = (max(actual[:,3]), min(actual[:,0]), d)
                if best is None or score < best[0]:
                    best = score, actual, d, xy
            if best is None:
                break
            _, actual, d, xy = best
            fixed = np.vstack((fixed, actual))
            current[i]["transform"].update(translation=list(xy), rotation_radians=d*pi/180)
        else:
            yield name, trial
            continue
        yield name, None


def run(binary, results, output):
    rows = []
    for matrix in MATRICES:
        for seed in range(3):
            for arm in ("off", "bonus"):
                stem = f"c-bracket-mixed-k0.2-s{seed}-{arm}"
                folder = output / matrix / stem
                with ZipFile(results/matrix/f"{stem}.zip") as archive:
                    job, layout, source = [json.loads(archive.read(name)) for name in
                                          ("nested/job.json", "nested/layout.json", "validate-stdout.json")]
                for name, trial in pack(job, layout, source["metrics"]["last_sheet_id"]):
                    row = dict(matrix=matrix, seed=seed, arm=arm, variant=name,
                               original=source["metrics"]["normalized_material"], original_saved_mm=saved(source))
                    rows.append(row)
                    if trial is None:
                        row["status"] = "did not fit"
                        continue
                    path = folder/f"repack-{name}.json"
                    path.write_text(json.dumps(trial), encoding="utf-8")
                    proc = subprocess.run([binary, "validate", "--library", folder/"library.json",
                                           "--request", folder/"request.json", "--layout", path], capture_output=True)
                    (folder/f"repack-{name}-validation.json").write_bytes(proc.stdout)
                    check = json.loads(proc.stdout)
                    row["status"] = "valid" if proc.returncode == 0 and check["valid"] else "invalid"
                    if row["status"] == "valid":
                        row.update(material=check["metrics"]["normalized_material"], saved_mm=saved(check))
    (output/"repacks.json").write_text(json.dumps(rows, indent=2)+"\n", encoding="utf-8")
    print(f"{sum(r['status']=='valid' for r in rows)}/{len(rows)} independently validated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.binary.resolve(), Path(__file__).resolve().parents[1], args.output)
