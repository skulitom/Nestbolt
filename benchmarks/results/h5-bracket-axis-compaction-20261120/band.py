"""Refill a partial last sheet, also trying gaps on the first sheet, at the original kerf."""
import argparse
from copy import deepcopy
import json
from math import pi
from pathlib import Path
import subprocess
from zipfile import ZipFile

import numpy as np
from replay import MATRICES, PAD, rectangles, saved, slide
from relocate import boxes, bottom_left


def refill(job, layout, last):
    parts = {p["id"]: p for p in job["parts"]}
    pieces = {k:[r for g in p["geometry"] for r in rectangles(g)] for k,p in parts.items()}
    stock, = job["stocks"]
    assert not stock["outline"] and not stock["defects"]
    earlier, tail = layout["sheets"]
    assert tail["id"] == last and earlier["stock_id"] == tail["stock_id"] == stock["id"]
    fixed_first = np.vstack([boxes(pieces,p) for p in layout["placements"] if p["sheet_id"] == earlier["id"]])
    original = [p for p in layout["placements"] if p["sheet_id"] == last]
    original_boxes = [boxes(pieces,p) for p in original]
    peaks = [max(b[:,3]) for b in original_boxes]
    areas = {k:sum((r[2]-r[0])*(r[3]-r[1]) for r in rs) for k,rs in pieces.items()}
    templates = {k:[(d,boxes(pieces,{"part_id":k, "transform":{
        "translation":[0,0], "mirrored": False, "rotation_radians":d*pi/180}}))
        for d in p["rotations"]["degrees"]] for k,p in parts.items()}
    assert all(not p["transform"]["mirrored"] for p in original)
    # Earlier-sheet gaps rarely fit even one complete part. Cache the first such
    # placement for each shape until a transfer actually changes its obstacles.
    def place(fixed, key, cap):
        best = None
        for d, local in templates[key]:
            pos = bottom_left(fixed, local, stock, job["edge_clearance"], job["clearance"]+PAD, cap)
            if pos:
                x,y = pos
                actual = local + [x,x,y,y]
                score = (max(actual[:,3]),min(actual[:,0]),d)
                if best is None or score < best[0]:
                    best = (score, actual, pos, d)
        return best
    cache = {k:place(fixed_first,k,stock["height"]) for k in set(p["part_id"] for p in original)}
    for count in (4,8,12):
        by_top = sorted(range(len(original)), key=peaks.__getitem__, reverse=True)
        removed = by_top[:count]
        base = np.vstack([original_boxes[i] for i in by_top[count:]])
        for order_name, order in (
            ("height",list(reversed(removed))),
            ("area",sorted(removed,key=lambda i:-areas[original[i]["part_id"]]))):
            name = f"band-{count}-{order_name}"
            trial = deepcopy(layout)
            active = [p for p in trial["placements"] if p["sheet_id"] == last]
            head, tail_boxes, options = fixed_first, base, dict(cache)
            for i in order:
                p = active[i]
                part = p["part_id"]
                if part not in options:
                    options[part] = place(head,part,stock["height"])
                choice = options[part]
                if choice:
                    p["sheet_id"] = earlier["id"]
                    head = np.vstack((head,choice[1]))
                    options.clear()
                else:
                    choice = place(tail_boxes,part,stock["height"])
                    if choice is None:
                        break
                    tail_boxes = np.vstack((tail_boxes,choice[1]))
                p["transform"].update(translation=list(choice[2]),rotation_radians=choice[3]*pi/180)
            else:
                kept = [p for p in active if p["sheet_id"] == last]
                slide(kept,pieces,[],"down",stock["margins"]["bottom"]+job["edge_clearance"],job["clearance"])
                yield name, trial
                continue
            yield name, None


def run(binary, results, output):
    rows = []
    for matrix in MATRICES:
        for seed in range(3):
            for arm in ("off","bonus"):
                stem = f"c-bracket-mixed-k0.2-s{seed}-{arm}"
                folder = output / matrix / stem
                with ZipFile(results/matrix/f"{stem}.zip") as archive:
                    job, layout, source = [json.loads(archive.read(name)) for name in
                                          ("nested/job.json","nested/layout.json","validate-stdout.json")]
                for name,trial in refill(job,layout,source["metrics"]["last_sheet_id"]):
                    row = dict(matrix=matrix,seed=seed,arm=arm,variant=name,
                               original=source["metrics"]["normalized_material"],original_saved_mm=saved(source))
                    rows.append(row)
                    if trial is None:
                        row["status"] = "did not fit"
                        continue
                    path = folder/f"{name}.json"
                    path.write_text(json.dumps(trial),encoding="utf-8")
                    p = subprocess.run([binary,"validate","--library",folder/"library.json",
                                        "--request",folder/"request.json","--layout",path],capture_output=True)
                    (folder/f"{name}-validation.json").write_bytes(p.stdout)
                    checked = json.loads(p.stdout)
                    row["status"] = "valid" if p.returncode == 0 and checked["valid"] else "invalid"
                    if row["status"] == "valid":
                        row.update(material=checked["metrics"]["normalized_material"],saved_mm=saved(checked))
    (output/"bands.json").write_text(json.dumps(rows,indent=2)+"\n",encoding="utf-8")
    print(f"{sum(r['status']=='valid' for r in rows)}/{len(rows)} independently validated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.binary.resolve(), Path(__file__).resolve().parents[1], args.output)
