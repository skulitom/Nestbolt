"""Replay lowest-position relocation of the tallest last-sheet parts with exact source boxes."""
import argparse
from copy import deepcopy
import json
from math import pi
from pathlib import Path
import subprocess
from zipfile import ZipFile

import numpy as np
from replay import MATRICES, PAD, oriented, rectangles, saved


def boxes(pieces, placement):
    return np.array([oriented(box, placement["transform"], "down")
                     for box in pieces[placement["part_id"]]])


def bottom_left(fixed, moving, stock, edge, gap, top):
    """Use square kerf offsets conservatively and find a lowest feasible translation."""
    margins = stock["margins"]
    floor = margins["bottom"]+edge+PAD-min(moving[:, 2])
    left = margins["left"]+edge+PAD-min(moving[:, 0])
    right = stock["width"]-margins["right"]-edge-PAD-max(moving[:, 1])
    ceiling = min(top-PAD, stock["height"]-margins["top"]-edge-PAD)-max(moving[:, 3])
    if floor > ceiling or left > right:
        return None
    # Open translation intervals where a moving and a fixed rectangle conflict.
    obstacle = fixed[:, None, :] - moving[None, :, [1, 0, 3, 2]]
    obstacle = obstacle.reshape(-1, 4) + np.array([-gap, gap, -gap, gap])
    obstacle = obstacle[(obstacle[:, 1] > left) & (obstacle[:, 0] < right)
                        & (obstacle[:, 3] > floor) & (obstacle[:, 2] < ceiling)]
    obstacle = obstacle[np.argsort(obstacle[:, 0])]
    ys = obstacle[:, 3]
    for y in np.unique(np.r_[floor, ys[(ys >= floor) & (ys <= ceiling)]]):
        row = obstacle[(obstacle[:, 2] < y) & (obstacle[:, 3] > y)]
        x = left
        for lo, hi in row[:, :2]:
            if x <= lo or x > right:
                break
            x = max(x, hi)
        if x <= right:
            return x, y
    return None


def settle(job, trial, last):
    pieces = {p["id"]: [r for poly in p["geometry"] for r in rectangles(poly)] for p in job["parts"]}
    angles = {p["id"]: p["rotations"]["degrees"] for p in job["parts"]}
    stock, = job["stocks"]
    assert not stock["outline"] and not stock["defects"]
    sheet = [p for p in trial["placements"] if p["sheet_id"] == last]
    occupied = [boxes(pieces, p) for p in sheet]
    moves = 0
    for _ in range(2):
        order = sorted(range(len(sheet)), key=lambda i: -max(occupied[i][:, 3]))
        pass_moves = 0
        for i in order[:8]:
            p = sheet[i]
            original_top = max(occupied[i][:, 3])
            fixed = np.vstack(occupied[:i]+occupied[i+1:])
            best = None
            for degrees in angles[p["part_id"]]:
                candidate = deepcopy(p)
                trans = candidate["transform"]
                trans.update(rotation_radians=degrees*pi/180, translation=[0, 0])
                moving = boxes(pieces, candidate)
                top_cap = best[0] if best else original_top
                position = bottom_left(fixed, moving, stock, job["edge_clearance"],
                                       job["clearance"]+PAD, top_cap)
                if position:
                    trans["translation"] = list(position)
                    actual = boxes(pieces, candidate)
                    best = (max(actual[:, 3]), trans, actual)
            if best:
                _, p["transform"], occupied[i] = best
                pass_moves += 1
        moves += pass_moves
        if not pass_moves:
            break
    return moves


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
                for start in ("original", "free-down-left-down"):
                    trial = deepcopy(layout) if start == "original" else json.loads((folder/f"{start}.json").read_bytes())
                    moves = settle(job, trial, source["metrics"]["last_sheet_id"])
                    tag = f"{start}-relocate"
                    path = folder/f"{tag}.json"
                    path.write_text(json.dumps(trial), encoding="utf-8")
                    proc = subprocess.run([binary, "validate", "--library", folder/"library.json",
                                           "--request", folder/"request.json", "--layout", path], capture_output=True)
                    (folder/f"{tag}-validation.json").write_bytes(proc.stdout)
                    checked = json.loads(proc.stdout)
                    valid = proc.returncode == 0 and checked["valid"]
                    rows.append(dict(matrix=matrix, seed=seed, arm=arm, variant=tag, moves=moves,
                                     valid=valid, original=source["metrics"]["normalized_material"],
                                     material=checked["metrics"]["normalized_material"] if valid else None,
                                     original_saved_mm=saved(source), saved_mm=saved(checked) if valid else None))
    (output/"relocations.json").write_text(json.dumps(rows, indent=2)+"\n", encoding="utf-8")
    print(f"{sum(r['valid'] for r in rows)}/{len(rows)} independently validated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.binary.resolve(), Path(__file__).resolve().parents[1], args.output)
