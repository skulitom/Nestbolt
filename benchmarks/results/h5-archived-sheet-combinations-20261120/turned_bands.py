"""Price original and quarter-turned bands cut from width-limited archived windows."""
import argparse
import gzip
import json
from math import cos, floor, sin
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from bands import JOB, KERF, NAMES
from combine import RESULTS, archived_layouts, read, write


def boxes(positions, rings):
    result = []
    for p in positions:
        t = p["transform"]
        a = t["rotation_radians"]
        c, s = cos(a), sin(a)
        dx, dy = t["translation"]
        sign = -1 if t["mirrored"] else 1
        points = [(dx + c * sign * x - s * y, dy + s * sign * x + c * y) for x, y in rings[p["part_id"]]]
        xs, ys = zip(*points)
        result.append((min(xs), max(xs), min(ys), max(ys), NAMES.index(p["part_id"])))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("horizontal", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with gzip.open(args.horizontal / "catalogue.json.gz", "rt") as stream:
        original = json.load(stream)
    patterns = {tuple(k): (span, ref, low, high, None) for k, _, span, ref, low, high in original["patterns"]}
    group = archived_layouts()[JOB, KERF]
    job = read(RESULTS.parent / "datasets/M" / (JOB + ".json"))
    rings = {p["id"]: p["geometry"][0]["outer"] for p in job["parts"]}
    quantities = {p["id"]: p["quantity"] for p in job["parts"]}
    patterns_before = len(patterns)
    windows = 0
    for index, (_, _, digest, sheet) in enumerate(original["sheets"]):
        placed = [p for p in group[digest][2]["placements"] if p["sheet_id"] == sheet]
        extents = boxes(placed, rings)
        masks = set()
        for bottom in {b[2] for b in extents}:
            mask = sum(1 << i for i, (_, _, y0, y1, _) in enumerate(extents)
                       if y0 >= bottom and y1 <= bottom + 1487.000004)
            if mask:
                masks.add(mask)
        # Every omitted window is a subset of a retained window. Surplus
        # parts may be discarded when assembling any pattern from the pool.
        maximal = []
        for mask in sorted(masks, key=int.bit_count, reverse=True):
            if all(mask & other != mask for other in maximal):
                maximal.append(mask)
        windows += len(maximal)
        for mask in maximal:
            window = [b for i, b in enumerate(extents) if mask & (1 << i)]
            y0 = min(b[2] for b in window)
            window.sort(key=lambda b: (b[1], b[0], b[4]))
            for left in {b[0] for b in window}:
                counts = [0] * len(NAMES)
                actual_left = float("inf")
                for x0, x1, _, _, family in window:
                    if x0 < left:
                        continue
                    counts[family] += 1
                    actual_left = min(actual_left, x0)
                    span = x1 - actual_left
                    key = tuple(counts)
                    previous = patterns.get(key)
                    if previous is None or span < previous[0]:
                        patterns[key] = span, index, actual_left, x1, y0
    keys = sorted(patterns)
    costs = [floor(patterns[k][0] * 1000) - 2 for k in keys]
    quantities = [quantities[k] for k in NAMES]
    lp = linprog(-np.array(quantities), A_ub=keys, b_ub=costs, method="highs", options={"threads": 1})
    assert lp.success, lp.message
    weights = [max(0, floor(w * 1000)) for w in lp.x]
    assert all(sum(n*w for n, w in zip(k, weights)) <= 1000*c for k, c in zip(keys, costs))
    required = sum(n*w for n, w in zip(quantities, weights))
    capacity = read(args.horizontal / "band-verification.json")["available_stock_height_rounded_up_nm"]
    rows = [[k, *patterns[k]] for k in keys]
    with gzip.open(args.output / "turned-catalogue.json.gz", "xt", encoding="utf-8") as stream:
        json.dump({"sheets": original["sheets"], "patterns": rows}, stream, separators=(",", ":"))
    result = dict(families=NAMES, quantities=quantities, original_inventories=patterns_before,
                  total_inventories=len(keys), maximal_turned_windows=windows, integer_prices_nm=weights,
                  minimum_height_free_joins_nm=required, capacity_nm=capacity, excluded=required > capacity)
    write(args.output / "turned-prices.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
