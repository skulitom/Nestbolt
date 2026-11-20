"""Check the band prices directly on archived source positions using interval trigonometry."""
import argparse
from collections import Counter
from functools import lru_cache
import gzip
from hashlib import sha256
import json
from math import cos, sin
from pathlib import Path
from zipfile import ZipFile

from mpmath import iv, mp

RESULTS = Path(__file__).resolve().parents[1]
iv.dps = 40
mp.dps = 60


@lru_cache(maxsize=None)
def axes(angle, mirrored):
    a = iv.mpf(angle)
    return (-iv.sin(a) if mirrored else iv.sin(a)), iv.cos(a)


def relaxed_extent(placement, ring):
    t = placement["transform"]
    a, mirrored = t["rotation_radians"], t["mirrored"]
    sx, cy = (-sin(a) if mirrored else sin(a)), cos(a)
    bottom = min(ring, key=lambda p: p[0] * sx + p[1] * cy)
    top = max(ring, key=lambda p: p[0] * sx + p[1] * cy)
    # Any selected bottom vertex gives an upper bound on the true minimum.
    # The top vertex likewise gives a lower bound on the true maximum.
    ix, iy = axes(a, mirrored)
    ty = iv.mpf(t["translation"][1])
    y0 = ix * bottom[0] + iy * bottom[1] + ty
    y1 = ix * top[0] + iy * top[1] + ty
    low = int(mp.ceil(mp.mpf(y0.b) * 1000000))
    high = int(mp.floor(mp.mpf(y1.a) * 1000000))
    assert high > low
    return low, high


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    out = parser.parse_args().output
    prices = json.loads((out / "band-prices.json").read_bytes())
    weights = dict(zip(prices["families"], prices["integer_prices"], strict=True))
    assert min(weights.values()) >= 0 and prices["price_scale"] == 1000
    with gzip.open(out / "catalogue.json.gz", "rt", encoding="utf-8") as stream:
        sources = json.load(stream)["sheets"]
    assert len(sources) == 310 and len({(h, s) for _, _, h, s in sources}) == 310
    assert len({h for _, _, h, _ in sources}) == 155
    job_file = RESULTS.parent / "datasets/M/m-mechanical-large-plates.json"
    job = json.loads(job_file.read_bytes())
    job_sha = sha256(job_file.read_bytes()).hexdigest()
    rings = {p["id"]: p["geometry"][0]["outer"] for p in job["parts"]}
    quantity = {p["id"]: p["quantity"] for p in job["parts"]}
    prefixes = 0
    margin = None
    for filename, member, digest, sheet in sources:
        with ZipFile(RESULTS / filename) as archive:
            raw = archive.read(member)
            case = json.loads(archive.read("case.json"))
            request = json.loads(archive.read("request.json"))
            assert case["status"] == "valid" and case["job_sha256"] == job_sha
            cmd = (case.get("validation") or case["revalidation"])["command"]
            assert cmd[cmd.index("--layout") + 1].replace(chr(92), "/").endswith("/" + member)
            assert request["common_line"]["kerf_mm"] == request["spacing_mm"] == 0.2
            assert json.loads(archive.read("validate-stdout.json"))["valid"]
            assert sha256(raw).hexdigest() == digest
        placements = json.loads(raw)["placements"]
        assert Counter(p["part_id"] for p in placements) == quantity
        rows = [(*relaxed_extent(p, rings[p["part_id"]]), weights[p["part_id"]])
                for p in placements if p["sheet_id"] == sheet]
        assert rows
        # For each top, include all available parts, descending by their bottom.
        # Nonnegative weights cover every subset of each fully occupied band.
        rows.sort(reverse=True)
        for top in {high for _, high, _ in rows}:
            weight = 0
            for low, high, value in rows:
                if high <= top:
                    weight += value
                    remaining = top - low + 200000 - weight
                    assert remaining >= 0, (filename, sheet, low, top, remaining)
                    margin = remaining if margin is None else min(margin, remaining)
                    prefixes += 1
    target = json.loads((RESULTS / "h5-six-unturned-frame-construction-20261107/benchmark-target.json").read_bytes())
    # Round the available stock up. Even allowing every band to join its
    # neighbour with zero gap can refund at most one gap per original part.
    capacity = sum(int(mp.ceil((mp.mpf(y1) - y0) * 1000000))
                   for _, y0, _, y1 in target["source_stocks"].values())
    required = sum(weights[k] * n for k, n in quantity.items())
    free_join_height = required - 200000 * sum(quantity.values())
    assert free_join_height > capacity
    result = dict(source_sheets=len(sources), checked_prefixes=prefixes,
                  minimum_price_slack_nm=margin, weighted_inventory_nm=required,
                  maximum_zero_gap_refund_nm=200000 * sum(quantity.values()),
                  minimum_height_with_free_joins_nm=free_join_height,
                  available_stock_height_rounded_up_nm=capacity, deficit_nm=free_join_height - capacity)
    with (out / "band-verification.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
