"""Check the original large-plate stock target using exact area and vertical slices."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from math import floor, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
ROOT = RESULTS.parents[1]
JOB = ROOT / "benchmarks/datasets/M/m-mechanical-large-plates.json"
OLD = RESULTS / "h5-short12-exclusion-and-seven-part-readback-20261029"
STOCK = RESULTS / "h5-allocation-aware-geometry-20261026/stocks.json"
COUPLED = RESULTS / "h5-coupled-allocation-model-20261026/source-area-excluded-count-vectors.json"
NAMES = ("bracket", "insert", "cog")


def read(path):
    return json.loads(path.read_bytes())


def ring_area(points):
    return abs(sum(x * v - u * y for (x, y), (u, v) in zip(points, points[1:] + points[:1]))) / 2


def rectangle_profile(points):
    widths = Counter()
    breaks = sorted({x for x, _ in points})
    edges = list(zip(points, points[1:] + points[:1]))
    assert all(x == u or y == v for (x, y), (u, v) in edges)
    for left, right in zip(breaks, breaks[1:]):
        middle = (left + right) / 2
        crossings = sorted(y for (x, y), (u, _) in edges if min(x, u) < middle < max(x, u))
        assert len(crossings) == 2
        height = crossings[1] - crossings[0]
        assert height.denominator == (right - left).denominator == 1
        widths[int(height)] += int(right - left)
    assert sum(h * w for h, w in widths.items()) == ring_area(points)
    return dict(widths)


def geometry(plan):
    job = read(JOB)
    areas, modes, counts = {}, {}, {}
    for part in job["parts"]:
        family = part["id"]
        counts[family] = part["quantity"]
        assert len(part["geometry"]) == 1
        ring = [tuple(map(Fraction, p)) for p in part["geometry"][0]["outer"]]
        areas[family] = ring_area(ring)
        if family in ("bracket", "insert"):
            assert part["rotations"] == {"kind": "list", "degrees": [0, 90, 180, 270]}
            # Reflections and half-turns preserve the multiset of vertical slices.
            modes[family] = [rectangle_profile(ring), rectangle_profile([(-y, x) for x, y in ring])]
        elif family == "cog":
            assert part["rotations"]["kind"] == "free"
            radius = plan["cog_inner_disk_radius_mm"]
            cx, cy = [sum(p[k] for p in ring) / len(ring) for k in (0, 1)]
            crossings = 0
            for (x, y), (u, v) in zip(ring, ring[1:] + ring[:1]):
                dx, dy = u - x, v - y
                t = max(0, min(1, ((cx - x) * dx + (cy - y) * dy) / (dx**2 + dy**2)))
                assert (x + t * dx - cx)**2 + (y + t * dy - cy)**2 >= radius**2
                if (y > cy) != (v > cy):
                    crossings += x + (cy - y) * dx / dy > cx
            assert crossings % 2 == 1
            # A disk inside the original outer polygon survives every rotation.
            assert plan["cog_strip_width_mm"] == 1
            step = plan["cog_chord_height_rounding_mm"]
            disk = Counter()
            for far in range(1, radius + 1):
                height = isqrt(4 * (radius**2 - far**2)) // step * step
                if height:
                    disk[height] += 2
            modes[family] = [dict(disk)]
    assert counts == {"frame": 18, "bracket": 12, "insert": 21, "cog": 15}
    return counts, areas, modes


def patterns(heights, capacity):
    def add(index, left, row):
        if index == len(heights):
            yield tuple(row)
        else:
            h = heights[index]
            for n in range(left // h + 1):
                yield from add(index + 1, left - n * h, row + [n])
    return list(add(0, capacity, []))


def price_search(heights, modes, capacity, maxima, scale):
    # Floating-point LPs only suggest prices. All certificates are checked with integers.
    import numpy as np
    from scipy.optimize import linprog

    combinations = patterns(heights, capacity)
    n = len(heights)
    matrix = [list(p) + [0] * 3 for p in combinations]
    limits = [1] * len(matrix)
    for f, family in enumerate(NAMES):
        for costs in modes[family]:
            matrix.append([-costs.get(h, 0) for h in heights] + [int(i == f) for i in range(3)])
            limits.append(0)
    matrix = np.array(matrix)
    candidates = set()
    for counts in maxima:
        lp = linprog([0] * n + [-c for c in counts], A_ub=matrix, b_ub=limits,
                     method="highs", options={"threads": 1})
        assert lp.success, lp.message
        candidates.add(tuple(max(0, floor(v * scale)) for v in lp.x[:n]))
    return sorted(candidates)


def certified_costs(heights, prices, modes, capacity):
    # Max price of any collection of integer-height slices that can occupy one x.
    best = [0] * (capacity + 1)
    for height, price in zip(heights, prices):
        for room in range(height, capacity + 1):
            best[room] = max(best[room], best[room - height] + price)
    table = dict(zip(heights, prices))
    costs = [min(sum(table[h] * width for h, width in profile.items()) for profile in modes[name])
             for name in NAMES]
    return best[-1], costs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = read(HERE / "plan.json")
    counts, areas, modes = geometry(plan)
    bounds = [[Fraction(*p) for p in sheet["target_bounds_rational"]] for sheet in read(STOCK)]
    sizes = [(x2 - x1, y2 - y1) for x1, y1, x2, y2 in bounds]
    width, short_height = sizes[1]
    heights = sorted({h for family in modes.values() for profile in family for h in profile})
    parent = read(OLD / "updated-allocations.json")
    survivors = [r for r in parent if r["excluded_by"] is None]
    assert len(parent) == 4576 and len(survivors) == plan["starting_short_sheet_allocations"]
    maxima = read(OLD / "pareto-necessary-counts.json")
    assert len(maxima) == plan["pareto_count_vectors_for_price_search"]
    candidates = price_search(heights, modes, floor(short_height), maxima, plan["price_integer_scale"])
    prices = []
    for values in candidates:
        peak, costs = certified_costs(heights, values, modes, floor(short_height))
        prices.append(dict(values=values, column_capacity=peak, family_costs=costs))
    first_exclusions, short_exclusions, remaining = [], [], []
    for row in survivors:
        short = row["short_counts"]
        first = row["first_counts"]
        assert first == [counts["frame"]] + [counts[name] - v for name, v in zip(NAMES, short)]
        loads = [sum(q * areas[f] for q, f in zip(first, ("frame", *NAMES))),
                 sum(q * areas[f] for q, f in zip(short, NAMES))]
        if loads[0] > sizes[0][0] * sizes[0][1]:
            first_exclusions.append(short)
        assert loads[1] <= width * short_height
        for index, certificate in enumerate(prices):
            required = sum(q * p for q, p in zip(short, certificate["family_costs"]))
            limit = width * certificate["column_capacity"]
            if required > limit:
                short_exclusions.append(dict(counts=short, certificate=index, excess=int(required-limit)))
                break
        else:
            if short not in first_exclusions:
                remaining.append(short)
    assert sorted(first_exclusions) == sorted(read(COUPLED))
    paths = [JOB, STOCK, COUPLED, OLD / "updated-allocations.json", OLD / "pareto-necessary-counts.json",
             HERE / "plan.json", Path(__file__).resolve()]
    result = dict(inputs={p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest() for p in paths},
                  heights=heights, price_vectors=prices, first_sheet_area_exclusions=first_exclusions,
                  short_sheet_price_exclusions=short_exclusions, remaining_allocations=remaining,
                  remaining_count=len(remaining), layouts_produced=0)
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, separators=(",", ":"))
        stream.write("\n")
    print("first sheet", len(first_exclusions), "short sheet", len(short_exclusions), "remaining", len(remaining))


if __name__ == "__main__":
    main()
