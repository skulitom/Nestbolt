"""Replay one- and three-axis slides on saved laser layouts of orthogonal brackets."""
import argparse
from copy import deepcopy
import heapq
import json
from math import cos, hypot, sin, sqrt
from pathlib import Path
import subprocess
from zipfile import ZipFile


MATRICES = [
    "h5-common-opt-in-holes-20261120T135332Z",
    "h5-common-material-budget-pilot-20261120T142949Z",
    "h5-common-material-budget-confirmation-20261120T143452Z",
]
PAD = 0.000006


def rectangles(poly):
    """Slice an even-odd orthogonal polygon with holes into filled rectangles."""
    edges = []
    xs = set()
    for ring in [poly["outer"], *poly["holes"]]:
        for (x, y), (u, v) in zip(ring, ring[1:] + ring[:1]):
            assert x == u or y == v
            xs.add(x)
            if y == v and x != u:
                edges.append((min(x, u), max(x, u), y))
    xs = sorted(xs)
    for left, right in zip(xs, xs[1:]):
        ys = sorted(y for lo, hi, y in edges if lo <= left and right <= hi)
        assert len(ys) % 2 == 0
        for bottom, top in zip(ys[::2], ys[1::2]):
            yield left, bottom, right, top


def oriented(box, trans, axis):
    """Return cross-axis and sliding-axis intervals in increasing coordinates."""
    c, s = cos(trans["rotation_radians"]), sin(trans["rotation_radians"])
    assert abs(c-round(c)) < 1e-12 and abs(s-round(s)) < 1e-12
    x0, y0, x1, y1 = box
    tx, ty = trans["translation"]
    cross, along = [], []
    for x, y in ((x0, y0), (x1, y1)):
        if trans["mirrored"]:
            x = -x
        x, y = tx + round(c)*x - round(s)*y, ty + round(s)*x + round(c)*y
        cross.append(x if axis == "down" else y)
        along.append(y if axis == "down" else x if axis == "left" else -x)
    return min(cross), max(cross), min(along), max(along)


def slide(placements, pieces, locks, axis, floor, kerf):
    boxes = [[oriented(r, p["transform"], axis) for r in pieces[p["part_id"]]]
             for p in placements]
    travel = [max(0, min(r[2] for r in rs)-floor-PAD) for rs in boxes]
    arcs = [dict() for _ in boxes]
    for i, j in locks:
        arcs[i][j] = arcs[j][i] = 0
    for i, first in enumerate(boxes):
        for j, second in enumerate(boxes[:i]):
            for a in first:
                for b in second:
                    gap = max(0, a[0]-b[1], b[0]-a[1])
                    if gap >= kerf:
                        continue
                    if a[2] >= b[3]:
                        low, high, rise = j, i, a[2]-b[3]
                    elif b[2] >= a[3]:
                        low, high, rise = i, j, b[2]-a[3]
                    else:
                        assert gap >= kerf-1e-7
                        continue
                    assert hypot(gap, rise) >= kerf-1e-6
                    slack = max(0, rise-sqrt(kerf**2-gap**2)-PAD)
                    arcs[low][high] = min(arcs[low].get(high, float("inf")), slack)
    # For every below -> above arc, upper travel <= lower travel + slack.
    queue = [(distance, i) for i, distance in enumerate(travel)]
    heapq.heapify(queue)
    while queue:
        distance, i = heapq.heappop(queue)
        if distance != travel[i]:
            continue
        for j, slack in arcs[i].items():
            if distance + slack < travel[j]:
                travel[j] = distance + slack
                heapq.heappush(queue, (travel[j], j))
    for placement, distance in zip(placements, travel):
        placement["transform"]["translation"][int(axis == "down")] += (
            distance if axis == "right" else -distance)


def saved(report):
    return sum(s["saved_length_mm"] for s in report["common_line"])


def run(binary, results, output):
    rows = []
    for matrix in MATRICES:
        for seed in range(3):
            for arm in ("off", "bonus"):
                stem = f"c-bracket-mixed-k0.2-s{seed}-{arm}"
                folder = output / matrix / stem
                folder.mkdir(parents=True, exist_ok=True)
                with ZipFile(results / matrix / f"{stem}.zip") as archive:
                    for name in ("library.json", "request.json"):
                        (folder / name).write_bytes(archive.read(name))
                    job, layout, source = [json.loads(archive.read(name)) for name in
                                          ("nested/job.json", "nested/layout.json", "validate-stdout.json")]
                pieces = {p["id"]: [box for poly in p["geometry"] for box in rectangles(poly)]
                          for p in job["parts"]}
                last = source["metrics"]["last_sheet_id"]
                stock, = job["stocks"]
                assert not stock["outline"] and not stock["defects"]
                margin, edge = stock["margins"], job["edge_clearance"]
                floor = {"down": margin["bottom"]+edge, "left": margin["left"]+edge,
                         "right": -stock["width"]+margin["right"]+edge}
                for rigid in (True, False):
                    for sweep in (("down",), ("down", "left", "down"), ("down", "right", "down")):
                        trial = deepcopy(layout)
                        active = [p for p in trial["placements"] if p["sheet_id"] == last]
                        ids = {f"{p['part_id']}#{p['copy_index']}": i for i, p in enumerate(active)}
                        locks = [tuple(ids[o["part_copy"]] for o in e["owners"])
                                 for s in source["common_line"] if s["sheet_id"] == last
                                 for e in s["shared_edges"]] if rigid else []
                        for axis in sweep:
                            slide(active, pieces, locks, axis, floor[axis], job["clearance"])
                        tag = ("rigid-" if rigid else "free-") + "-".join(sweep)
                        path = folder / f"{tag}.json"
                        path.write_text(json.dumps(trial), encoding="utf-8")
                        p = subprocess.run([binary, "validate", "--library", folder/"library.json",
                                            "--request", folder/"request.json", "--layout", path],
                                           capture_output=True)
                        (folder/f"{tag}-validation.json").write_bytes(p.stdout)
                        checked = json.loads(p.stdout)
                        valid = p.returncode == 0 and checked["valid"]
                        rows.append(dict(matrix=matrix, seed=seed, arm=arm, variant=tag,
                                         valid=valid, original=source["metrics"]["normalized_material"],
                                         material=checked["metrics"]["normalized_material"] if valid else None,
                                         original_saved_mm=saved(source),
                                         saved_mm=saved(checked) if valid else None))
    (output/"results.json").write_text(json.dumps(rows, indent=2)+"\n", encoding="utf-8")
    print(f"{sum(r['valid'] for r in rows)}/{len(rows)} independently validated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.binary.resolve(), Path(__file__).resolve().parents[1], args.output)
