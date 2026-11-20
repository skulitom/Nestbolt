"""Assemble complete common-line layouts from intact subsets of archived sheets."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
from heapq import heappush, heappushpop
import json
from math import ceil, cos, sin
from pathlib import Path
from zipfile import ZipFile

RESULTS = Path(__file__).resolve().parents[1]
CENSUS = RESULTS / "h5-two-sheet-capacity-20261120"
SOURCE = RESULTS / "h5-common-development-20261015T142414Z"


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def archived_layouts():
    with ZipFile(CENSUS / "layout-census-replay.zip") as archive:
        names = json.loads(archive.read("output/h5-archive-layout-census-final-20261120/scope.json"))
    groups = defaultdict(dict)
    for name in names:
        with ZipFile(RESULTS / name) as archive:
            if not {"case.json", "request.json", "nested/layout.json", "validate-stdout.json"} <= set(archive.namelist()):
                continue
            case = json.loads(archive.read("case.json"))
            request = json.loads(archive.read("request.json"))
            report = json.loads(archive.read("validate-stdout.json"))
            if case.get("status") != "valid" or not request.get("common_line"):
                continue
            assert report["valid"]
            command = (case.get("validation") or case["revalidation"])["command"]
            path = command[command.index("--layout") + 1].replace(chr(92), "/")
            member = next(m for m in ("expanded-layout.json", "nested/layout.json") if path.endswith("/" + m))
            raw = archive.read(member)
            key = case["job"], case["kerf_mm"]
            digest = sha256(raw).hexdigest()
            groups[key].setdefault(digest, (name, member, json.loads(raw)))
    return groups


def height_interval(placement, ring):
    transform = placement["transform"]
    angle = transform["rotation_radians"]
    sx = -sin(angle) if transform["mirrored"] else sin(angle)
    cy = cos(angle)
    ty = transform["translation"][1]
    ys = [x * sx + y * cy + ty for x, y in ring]
    return min(ys), max(ys)


def best_band(rows, need):
    """For each upper edge, the highest eligible bottoms give its shortest band."""
    heaps = {k: [] for k in need}
    missing = sum(need.values())
    best = None
    for top, bottom, index, family in rows:
        if family not in need:
            continue
        heap = heaps[family]
        if len(heap) < need[family]:
            heappush(heap, (bottom, index))
            missing -= 1
        elif bottom > heap[0][0]:
            heappushpop(heap, (bottom, index))
        else:
            continue
        if missing:
            continue
        low = min(h[0][0] for h in heaps.values())
        height = top - low
        if best is None or height < best[0]:
            indices = sorted(i for h in heaps.values() for _, i in h)
            best = height, low, indices
    return best


def combine(case, group, canonical, out):
    job = read(RESULTS.parent / "datasets/M" / (case["job"] + ".json"))
    parts = {p["id"]: p for p in job["parts"]}
    quantity = Counter({name: p["quantity"] for name, p in parts.items()})
    assert all(len(p["geometry"]) == 1 for p in parts.values())
    assert len(group) == case["distinct_saved_layouts"]
    stock = job["stocks"][0]
    assert len(job["stocks"]) == 1 and not (stock["defects"] or stock["outline"])
    sheets, first_by_need = [], {}
    for digest, (name, member, layout) in group.items():
        positions = layout["placements"]
        assert Counter(p["part_id"] for p in positions) == quantity
        assert len(layout["sheets"]) == 2
        for sheet in layout["sheets"]:
            placed = [p for p in positions if p["sheet_id"] == sheet["id"]]
            counts = Counter(p["part_id"] for p in placed)
            inventory = tuple(sorted((quantity - counts).items()))
            assert inventory and placed
            edges = []
            for i, p in enumerate(placed):
                low, high = height_interval(p, parts[p["part_id"]]["geometry"][0]["outer"])
                edges.append((high, low, i, p["part_id"]))
            ref = dict(archive=name, member=member, sha256=digest, sheet=sheet["id"])
            first_by_need.setdefault(inventory, (ref, placed))
            sheets.append((ref, placed, counts, sorted(edges)))
    best = None
    compatible_pairs = 0
    for inventory, first in first_by_need.items():
        need = dict(inventory)
        for ref, placed, counts, rows in sheets:
            if any(counts[k] < n for k, n in inventory):
                continue
            compatible_pairs += 1
            height, low, indices = best_band(rows, need)
            if best is None or height < best[0]:
                best = height, low, first, ref, [placed[i] for i in indices]
    height, low, (first_ref, first), second_ref, second = best
    out.mkdir()
    with ZipFile(SOURCE / canonical["archive"]) as archive:
        for file in ("request.json", "library.json"):
            (out / file).write_bytes(archive.read(file))
        layout = json.loads(archive.read("nested/layout.json"))
    request = read(out / "request.json")
    assert request["common_line"]["kerf_mm"] == case["kerf_mm"]
    margin = stock["margins"]["bottom"] + request["edge_spacing_mm"]
    # Keep the translation on the validator's 1e-6 mm grid.
    dy = ceil((margin - low) * 1e6) / 1e6
    placed, indices = [], Counter()
    for sheet, source, offset in zip(layout["sheets"], (first, second), (0, dy)):
        for p in deepcopy(source):
            family = p["part_id"]
            p["sheet_id"] = sheet["id"]
            p["copy_index"] = indices[family]
            indices[family] += 1
            p["transform"]["translation"][1] += offset
            placed.append(p)
    assert indices == quantity
    layout["placements"] = placed
    write(out / "layout.json", layout)
    return dict(job=case["job"], kerf=case["kerf_mm"], target_mm2=case["target_mm2"],
                best_archived_mm2=case["best"]["material_mm2"], full_sheets=len(sheets),
                first_inventory_options=len(first_by_need), compatible_pairs=compatible_pairs,
                band_height_mm=height, band_translation_mm=dy, first=first_ref, second=second_ref,
                second_counts=dict(Counter(p["part_id"] for p in second)), canonical=canonical["archive"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    out = parser.parse_args().output
    groups = archived_layouts()
    cases = read(CENSUS / "layout-census.json")["cases"]
    source = read(SOURCE / "results.json")["rows"]
    summary = []
    assert set(groups) == {(c["job"], c["kerf_mm"]) for c in cases}
    for case in cases:
        key = case["job"], case["kerf_mm"]
        canonical = next(row for row in source if (row["job"], row["kerf_mm"]) == key
                         and row["arm"] == "bonus" and row["seed"] == 0)
        summary.append(combine(case, groups[key], canonical, out / f"{key[0]}-{key[1]}"))
    write(out / "construction.json", summary)
    print([(r["job"], r["kerf"], r["compatible_pairs"], r["band_height_mm"]) for r in summary])


if __name__ == "__main__":
    main()
