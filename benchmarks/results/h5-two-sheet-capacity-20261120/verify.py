"""Independent integer replay of every certified whole-allocation exclusion. No LP dependency."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import pairwise
import json
from math import isqrt
from pathlib import Path
from sys import argv

base = Path(__file__).resolve().parent
root = base.parents[2]
result = json.loads(Path(argv[1]).read_bytes())
for name, expected in result["inputs"].items():
    assert sha256((root / name).read_bytes()).hexdigest() == expected, name


def source(suffix):
    name, = [name for name in result["inputs"] if name.endswith(suffix)]
    return json.loads((root / name).read_bytes())


def cross(a, b, c):
    return (b[0]-a[0]) * (c[1]-a[1]) - (b[1]-a[1]) * (c[0]-a[0])


def profiles(points, mirrored):
    variants = set()
    for sign in ((1, -1) if mirrored else (1,)):
        pts = [(x * sign, y) for x, y in points]
        for _ in range(4):
            assert all(int(x) == x and int(y) == y for x, y in pts)
            spans = Counter()
            for x in range(int(min(p[0] for p in pts)), int(max(p[0] for p in pts))):
                ys = [p[1] for p, q in pairwise(pts + pts[:1])
                      if min(2*p[0], 2*q[0]) < 2*x+1 < max(2*p[0], 2*q[0])]
                assert len(ys) == 2
                spans[int(max(ys) - min(ys))] += 1
            variants.add(tuple(sorted(spans.items())))
            pts = [(y, -x) for x, y in pts]
    return [dict(v) for v in variants]


def disk_profile(pts):
    r = 109
    center = tuple((max(p[k] for p in pts) + min(p[k] for p in pts)) / 2 for k in (0, 1))
    edges = list(pairwise(pts + pts[:1]))
    winding = 0
    for i, (a, b) in enumerate(edges):
        for j, (c, d) in enumerate(edges[:i]):
            if i - j == 1 or (i == len(pts) - 1 and j == 0):
                continue
            disjoint_box = any(max(a[k], b[k]) < min(c[k], d[k]) or
                               max(c[k], d[k]) < min(a[k], b[k]) for k in (0, 1))
            assert disjoint_box or cross(a, b, c)*cross(a, b, d) > 0 or cross(c, d, a)*cross(c, d, b) > 0
        side = cross(a, b, center)
        winding += int(a[1] <= center[1] < b[1] and side > 0)
        winding -= int(b[1] <= center[1] < a[1] and side < 0)
        at_a = sum((center[k]-a[k]) * (b[k]-a[k]) for k in (0, 1))
        at_b = sum((center[k]-b[k]) * (a[k]-b[k]) for k in (0, 1))
        if min(at_a, at_b) >= 0:
            assert side**2 >= r*r*sum((a[k]-b[k])**2 for k in (0, 1))
        else:
            nearest = a if at_a < 0 else b
            assert sum((center[k]-nearest[k])**2 for k in (0, 1)) >= r*r
    assert abs(winding) == 1
    # Total width guaranteed to contain at least a given height; difference
    # adjacent levels to recover each disjoint class of one-mm columns.
    widths = {h: 2 * (isqrt(4*r*r - h*h)//2) for h in range(25, 2*r+1, 25)}
    return [{h: w - widths.get(h+25, 0) for h, w in widths.items()}]


def max_column(heights, prices, capacity, index=0):
    if index == len(heights):
        return 0
    h, p = heights[index], prices[index]
    return max(n*p + max_column(heights, prices, capacity-n*h, index+1)
               for n in range(capacity//h+1))


modes, areas = {}, {}
job = source("m-mechanical-large-plates.json")
for part in job["parts"]:
    name = part["id"]
    pts = [tuple(map(Fraction, p)) for p in part["geometry"][0]["outer"]]
    # Fan triangulation about the first vertex gives signed occupied outer area.
    areas[name] = abs(sum(cross(pts[0], a, b) for a, b in pairwise(pts[1:]))) / 2
    if name in ("bracket", "insert"):
        assert set(part["rotations"]["degrees"]) == {0, 90, 180, 270}
        modes[name] = profiles(pts, part["allow_mirror"])
    elif name == "cog":
        modes[name] = disk_profile(pts)
width = 1487
sizes = [(width, 2987), (width, Fraction(31942699, 100000) - Fraction(13, 2))]
for size, stock in zip(sizes, source("stocks.json"), strict=True):
    x, y, u, v = [Fraction(*q) for q in stock["target_bounds_rational"]]
    assert size == (u-x, v-y)
names = ["bracket", "insert", "cog"]
heights = result["heights"]
assert heights == sorted({k for variants in modes.values() for v in variants for k in v})
tables = []
for certificate in result["price_vectors"]:
    values = certificate["values"]
    assert len(values) == len(heights) and all(isinstance(p, int) and p >= 0 for p in values)
    prices = dict(zip(heights, values))
    peak = max_column(heights, values, int(sizes[1][1]))
    costs = [min(sum(w * prices[h] for h, w in v.items()) for v in modes[name]) for name in names]
    assert costs == certificate["family_costs"] and peak == certificate["column_capacity"]
    tables.append((peak, costs))
old = source("updated-allocations.json")
active = [r for r in old if r["excluded_by"] is None]
assert len(active) == len({tuple(r["short_counts"]) for r in active}) == 440
first, short, remaining = [], [], []
for row in active:
    counts = row["short_counts"]
    assert row["first_counts"] == [18, 12-counts[0], 21-counts[1], 15-counts[2]]
    first_area = sum(areas[name] * q for name, q in zip(["frame", *names], row["first_counts"]))
    if first_area > width * sizes[0][1]:
        first.append(counts)
    for i, (peak, costs) in enumerate(tables):
        excess = sum(p*q for p, q in zip(costs, counts)) - peak * width
        if excess > 0:
            short.append(dict(counts=counts, certificate=i, excess=excess))
            break
    else:
        if counts not in first:
            remaining.append(counts)
assert result["first_sheet_area_exclusions"] == first
assert sorted(first) == sorted(source("source-area-excluded-count-vectors.json"))
assert result["short_sheet_price_exclusions"] == short
assert result["remaining_allocations"] == remaining and result["remaining_count"] == len(remaining)
print(json.dumps(dict(passed=True, checked_allocations=len(active), area_exclusions=len(first),
                      slice_exclusions=len(short), remaining=len(remaining),
                      verified_price_vectors=len(tables), solver_calls=0)))

if len(argv) > 2:
    cog_result = json.loads(Path(argv[2]).read_bytes())
    for name, expected in cog_result["inputs"].items():
        assert sha256((base / name).read_bytes()).hexdigest() == expected
    points = next(p for p in job["parts"] if p["id"] == "cog")["geometry"][0]["outer"]
    center = [(max(Fraction(p[k]) for p in points) + min(Fraction(p[k]) for p in points))/2 for k in (0, 1)]
    assert all(sum((Fraction(p[k])-center[k])**2 for k in (0, 1)) <= 141**2 for p in points)
    heights = sorted({h for name in names[:2] for v in modes[name] for h in v})
    assert cog_result["heights"] == heights and 312 < sizes[1][1] < 313
    costs_and_caps = []
    for certificate in cog_result["certificates"]:
        payments = certificate["weights"]
        m, b = certificate["slope"], certificate["offset"]
        assert len(payments) == len(heights) and all(isinstance(v, int) and v >= 0 for v in (*payments, m, b))
        # For each exact total of non-cog height, find the maximum price.
        dp = [0] + [None] * 313
        for t in range(1, 314):
            attainable = [dp[t-h] + pay for h, pay in zip(heights, payments) if t >= h and dp[t-h] is not None]
            if attainable:
                dp[t] = max(attainable)
        # Consider every possible number of cogs, including more than two.
        peak = max(v + min(313-t, 282*k)*m-k*b for t, v in enumerate(dp) if v is not None for k in range(16))
        w = dict(zip(heights, payments))
        costs = [min(sum(w[h]*n for h, n in v.items()) for v in modes[name]) for name in names[:2]]
        costs.append(int(areas["cog"])*m - 282*b)
        assert costs == certificate["costs"] and peak == certificate["peak"]
        costs_and_caps.append((costs, peak))
    new, final = [], []
    for q in remaining:
        for index, (costs, peak) in enumerate(costs_and_caps):
            excess = sum(p*n for p, n in zip(costs, q)) - 1487*peak
            if excess > 0:
                new.append(dict(counts=q, certificate=index, excess=excess))
                break
        else:
            final.append(q)
    assert new == cog_result["exclusions"] and final == cog_result["remaining"]
    print(json.dumps(dict(passed=True, checked_allocations=len(remaining), cog_exclusions=len(new),
                          remaining=len(final), verified_price_vectors=len(costs_and_caps), solver_calls=0)))
