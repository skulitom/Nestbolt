"""Catalogue stacks of horizontal bands from the archived 0.2 mm large-plate sheets."""
import argparse
from gzip import open as gzip_open
import json
from math import ceil, floor
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from combine import RESULTS, archived_layouts, height_interval, read, write

JOB = "m-mechanical-large-plates"
KERF = 0.2
NAMES = ("bracket", "cog", "frame", "insert")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    out = parser.parse_args().output
    job = read(RESULTS.parent / "datasets/M" / (JOB + ".json"))
    parts = {p["id"]: p for p in job["parts"]}
    quantity = [parts[k]["quantity"] for k in NAMES]
    group = archived_layouts()[JOB, KERF]
    assert len(group) == 155
    patterns, sheets = {}, []
    for digest, (archive, member, layout) in group.items():
        for sheet in layout["sheets"]:
            sheet_index = len(sheets)
            sheets.append([archive, member, digest, sheet["id"]])
            edges = []
            for placement in layout["placements"]:
                if placement["sheet_id"] == sheet["id"]:
                    part = parts[placement["part_id"]]
                    low, high = height_interval(placement, part["geometry"][0]["outer"])
                    edges.append((high, low, NAMES.index(part["id"])))
            edges.sort()
            for lower in sorted({low for _, low, _ in edges}):
                counts = [0] * len(NAMES)
                actual_low = float("inf")
                for upper, bottom, family in edges:
                    if bottom < lower:
                        continue
                    counts[family] += 1
                    actual_low = min(actual_low, bottom)
                    span = upper - actual_low
                    key = tuple(counts)
                    previous = patterns.get(key)
                    if previous is None or span < previous[0]:
                        patterns[key] = span, sheet_index, actual_low, upper
    keys = sorted(patterns)
    # Each shelf pays one gap. Adding one gap to each sheet's capacity refunds
    # the unused gap above its top shelf. Round down for the price test.
    lower_costs = [max(0, floor(patterns[k][0] * 1000) - 1) + 200 for k in keys]
    target = read(RESULTS / "h5-six-unturned-frame-construction-20261107/benchmark-target.json")
    bounds = target["source_stocks"]
    capacities = [ceil((bounds[s][3] - bounds[s][1]) * 1000) + 200 for s in sorted(bounds)]
    prices = linprog(-np.array(quantity), A_ub=keys, b_ub=lower_costs, method="highs", options={"threads": 1})
    assert prices.success, prices.message
    # All reported inequalities are checked using integers, including the slack
    # which a subsequent integer assignment may use for pattern filtering.
    scale = 1000
    weights = [max(0, floor(w * scale)) for w in prices.x]
    assert all(sum(p * w for p, w in zip(k, weights)) <= cost * scale for k, cost in zip(keys, lower_costs))
    needed = sum(c * w for c, w in zip(quantity, weights))
    rows = [[k, lower_cost, *patterns[k]] for k, lower_cost in zip(keys, lower_costs)]
    with gzip_open(out / "catalogue.json.gz", "xt", encoding="utf-8") as stream:
        json.dump({"sheets": sheets, "patterns": rows}, stream, separators=(",", ":"))
    result = dict(families=NAMES, quantities=quantity, source_sheets=len(sheets), inventories=len(keys),
                  price_scale=scale, integer_prices=weights, required_weight=needed,
                  available_weight=sum(capacities) * scale, capacity_um_including_end_gap=capacities,
                  excluded=needed > sum(capacities) * scale)
    write(out / "band-prices.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
