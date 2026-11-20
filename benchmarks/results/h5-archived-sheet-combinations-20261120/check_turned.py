"""Verify zero-gap prices for every original and quarter-turned source window."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from math import cos, sin
from pathlib import Path
from zipfile import ZipFile

from mpmath import iv, mp

from check_bands import RESULTS, axes, relaxed_extent


def relaxed_x(placement, ring):
    transform = placement["transform"]
    angle = transform["rotation_radians"]
    mirror = -1 if transform["mirrored"] else 1
    c, s = cos(angle) * mirror, sin(angle)
    left = min(ring, key=lambda p: c*p[0] - s*p[1])
    right = max(ring, key=lambda p: c*p[0] - s*p[1])
    iy, ix = axes(angle, transform["mirrored"])
    tx = iv.mpf(transform["translation"][0])
    left_bound = tx + mirror * (ix*left[0] - iy*left[1])
    right_bound = tx + mirror * (ix*right[0] - iy*right[1])
    lo = int(mp.ceil(mp.mpf(left_bound.b) * 1000000))
    hi = int(mp.floor(mp.mpf(right_bound.a) * 1000000))
    assert hi > lo
    return lo, hi


def verify_intervals(intervals):
    """Largest total price below each upper endpoint for each possible lower endpoint."""
    descending = sorted(intervals, reverse=True)
    count = 0
    slack = None
    for top in {hi for _, hi, _ in descending}:
        weight = 0
        for lo, hi, value in descending:
            if hi <= top:
                weight += value
                remaining = top - lo - weight
                assert remaining >= 0, (lo, top, weight)
                slack = remaining if slack is None else min(slack, remaining)
                count += 1
    return count, slack


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("horizontal", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    out = args.output
    prices = json.loads((out / "turned-prices.json").read_bytes())
    weights = dict(zip(prices["families"], prices["integer_prices_nm"], strict=True))
    assert min(weights.values()) >= 0
    with gzip.open(args.horizontal / "catalogue.json.gz", "rt") as stream:
        sources = json.load(stream)["sheets"]
    assert len(sources) == len({(d, s) for _, _, d, s in sources}) == 310
    data = (RESULTS.parent / "datasets/M/m-mechanical-large-plates.json").read_bytes()
    job = json.loads(data)
    rings = {p["id"]: p["geometry"][0]["outer"] for p in job["parts"]}
    quantity = {p["id"]: p["quantity"] for p in job["parts"]}
    stock = job["stocks"][0]
    target = json.loads((RESULTS / "h5-six-unturned-frame-construction-20261107/benchmark-target.json").read_bytes())
    counts = Counter()
    min_slack = None
    for name, member, digest, sheet in sources:
        with ZipFile(RESULTS / name) as archive:
            case = json.loads(archive.read("case.json"))
            request = json.loads(archive.read("request.json"))
            cmd = (case.get("validation") or case["revalidation"])["command"]
            assert cmd[cmd.index("--layout") + 1].replace(chr(92), "/").endswith("/" + member)
            assert case["status"] == "valid" and case["job_sha256"] == sha256(data).hexdigest()
            assert request["spacing_mm"] == request["common_line"]["kerf_mm"] == 0.2
            width = stock["width"] - stock["margins"]["left"] - stock["margins"]["right"] - 2*request["edge_spacing_mm"]
            assert width == 1487 and json.loads(archive.read("validate-stdout.json"))["valid"]
            raw = archive.read(member)
            assert sha256(raw).hexdigest() == digest
            layout = json.loads(raw)
        assert Counter(p["part_id"] for p in layout["placements"]) == quantity
        rows = []
        for p in layout["placements"]:
            if p["sheet_id"] == sheet:
                ring = rings[p["part_id"]]
                rows.append((*relaxed_x(p, ring), *relaxed_extent(p, ring), weights[p["part_id"]]))
        n, slack = verify_intervals([(yl, yh, w) for _, _, yl, yh, w in rows])
        counts["horizontal_prefixes"] += n
        min_slack = slack if min_slack is None else min(min_slack, slack)
        # Anchor at each possible far edge on the original Y axis. Include all
        # shrunken intervals that could fit in the stock width after rotation.
        for end in {r[3] for r in rows}:
            window = [(xl, xh, w) for xl, xh, yl, yh, w in rows
                      if end - width*1000000 <= yl and yh <= end]
            if window:
                n, slack = verify_intervals(window)
                counts["turned_windows"] += 1
                counts["turned_prefixes"] += n
                min_slack = min(min_slack, slack)
    capacity = sum(int(mp.ceil((mp.mpf(y1) - y0) * 1000000))
                   for _, y0, _, y1 in target["source_stocks"].values())
    required = sum(weights[k] * quantity[k] for k in weights)
    assert required == prices["minimum_height_free_joins_nm"] and required > capacity
    result = dict(checked=dict(counts), minimum_slack_nm=min_slack, required_height_nm=required,
                  stock_height_rounded_up_nm=capacity, deficit_nm=required-capacity)
    with (out / "turned-verification.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
