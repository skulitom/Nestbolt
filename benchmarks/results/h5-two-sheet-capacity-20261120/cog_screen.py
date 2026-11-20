"""Use the complete gear area at all angles to bound short-sheet assignments."""
from fractions import Fraction
from math import ceil, floor
import argparse
import json
from hashlib import sha256
from pathlib import Path

from scipy.optimize import linprog
from screen import HERE, JOB, geometry, patterns, read


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    output = parser.parse_args().output
    old = read(HERE / "results.json")["remaining_allocations"]
    plan = read(HERE / "cog-plan.json")
    assert len(old) == plan["parent_remaining_allocations"]
    maxima = [q for q in old if not any(q != r and all(a <= b for a, b in zip(q, r)) for r in old)]
    _, areas, modes = geometry(read(HERE / "plan.json"))
    cog = next(p for p in read(JOB)["parts"] if p["id"] == "cog")
    ring = [tuple(map(Fraction, p)) for p in cog["geometry"][0]["outer"]]
    center = [sum(p[k] for p in ring)/len(ring) for k in (0, 1)]
    assert all(sum((v - c)**2 for v, c in zip(point, center)) <= 141**2 for point in ring)
    diameter = 282
    area = floor(areas["cog"])
    names = ["bracket", "insert"]
    heights = sorted({h for name in names for profile in modes[name] for h in profile})
    combinations = patterns(heights, 313)
    n = len(heights)
    matrix, limits = [], []
    for combo in combinations:
        space = 313 - sum(k * h for k, h in zip(combo, heights))
        for cogs in (0, 1, 2):
            matrix.append([*combo, min(diameter*cogs, space), -cogs, 0, 0, 0])
            limits.append(1)
    for family, name in enumerate(names):
        for mode in modes[name]:
            matrix.append([-mode.get(h, 0) for h in heights] + [0, 0, int(family == 0), int(family == 1), 0])
            limits.append(0)
    matrix.append([0]*n + [-area, diameter, 0, 0, 1])
    limits.append(0)
    vectors = set()
    scale = plan["price_integer_scale"]
    for q in maxima:
        lp = linprog([0]*(n+2) + [-v for v in q], A_ub=matrix, b_ub=limits,
                     method="highs", options={"threads": 1})
        assert lp.success, lp.message
        slope, offset = lp.x[n:n+2]
        vectors.add((*[max(0, floor(v*scale)) for v in lp.x[:n]], max(0, floor(slope*scale)),
                     max(0, ceil(offset*scale))))
    certificates = []
    for vector in sorted(vectors):
        weights = dict(zip(heights, vector[:n]))
        slope, offset = vector[n:]
        peak = 0
        for combo in combinations:
            reward = sum(p*k for p, k in zip(vector[:n], combo))
            space = 313 - sum(k*h for k, h in zip(combo, heights))
            peak = max(peak, reward, reward+slope*min(space, diameter)-offset, reward+slope*space-2*offset)
        costs = [min(sum(w*weights[h] for h, w in profile.items()) for profile in modes[name]) for name in names]
        costs.append(area*slope - diameter*offset)
        certificates.append(dict(weights=vector[:n], slope=slope, offset=offset, peak=peak, costs=costs))
    excluded, remaining = [], []
    for q in old:
        for i, c in enumerate(certificates):
            excess = sum(k*p for k, p in zip(q, c["costs"])) - 1487*c["peak"]
            if excess > 0:
                excluded.append(dict(counts=q, certificate=i, excess=excess))
                break
        else:
            remaining.append(q)
    pins = {name: sha256((HERE/name).read_bytes()).hexdigest()
            for name in ["cog-plan.json", "results.json", "screen.py", "cog_screen.py"]}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(dict(inputs=pins, heights=heights, maximal_vectors=len(maxima), certificates=certificates,
                       exclusions=excluded, remaining=remaining), stream, separators=(",", ":"))
        stream.write("\n")
    print("additional exclusions", len(excluded), "remaining", len(remaining))


if __name__ == "__main__":
    main()
