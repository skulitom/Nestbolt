"""Identify one-transfer receivers and validate the original-source partial construction."""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from zipfile import ZipFile

RESULTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESULTS / "h5-archived-sheet-combinations-20261120"))
from combine import archived_layouts, read, write
sys.path.insert(0, str(RESULTS / "h5-simultaneous-compaction-20261120"))
from audit import geometry_check

JOB = "m-mechanical-large-plates"
NAMES = ("bracket", "insert", "cog", "frame")


def validate(binary, folder, request, layout, name):
    proc = subprocess.run([binary, "validate", "--library", "library.json", "--request", request,
                           "--layout", layout], cwd=folder, capture_output=True)
    (folder / (name+".json")).write_bytes(proc.stdout)
    (folder / (name+".stderr")).write_bytes(proc.stderr)
    report = json.loads(proc.stdout)
    assert (proc.returncode == 0) == report["valid"]
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("binary", type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    binary = args.binary.resolve()
    group = archived_layouts()[JOB,0.2]
    assert len(group) == 155
    frontier = {(*v,0) for v in read(RESULTS/"h5-two-sheet-capacity-20261120/cog-results.json")["remaining"]}
    assert len(frontier) == 418
    short_file = RESULTS/"h5-short-cog-transfer-20261028/short-source12.json"
    short = read(short_file)
    short_counts = Counter(p["part_id"] for p in short)
    target_vector = tuple(short_counts[k] for k in NAMES)
    assert target_vector == (7,4,1,0) and target_vector in frontier
    job = read(RESULTS.parent/"datasets/M"/(JOB+".json"))
    targets = read(RESULTS/"h5-six-unturned-frame-construction-20261107/benchmark-target.json")
    canonical = read(RESULTS/"h5-archived-sheet-combinations-20261120/construction.json")[0]
    assert (canonical["job"],canonical["kerf"]) == (JOB,0.2)
    donors, histogram, nearest = [], Counter(), []
    for digest,(name,member,layout) in group.items():
        distances = []
        for sheet in layout["sheets"]:
            counts = Counter(p["part_id"] for p in layout["placements"] if p["sheet_id"] == sheet["id"])
            v = tuple(counts[k] for k in NAMES)
            d = min(sum(abs(a-b) for a,b in zip(v,q)) for q in frontier)
            distances.append(d)
            if d == 1:
                neighbours = sorted(q for q in frontier if sum(abs(a-b) for a,b in zip(v,q)) == 1)
                nearest.append(dict(archive=name, member=member, sha256=digest, short_sheet=sheet["id"],
                                    old_short=v, reachable_vectors=neighbours))
                if v == (7,4,2,0) and target_vector in neighbours:
                    donors.append((name, member, digest, sheet["id"], layout))
        histogram[min(distances)] += 1
    summaries = []
    for n,(archive,member,digest,short_id,layout) in enumerate(donors):
        folder = out/f"receiver{n}"
        folder.mkdir()
        with ZipFile(RESULTS/"h5-common-development-20261015T142414Z"/canonical["canonical"]) as ref:
            for member_name in ("library.json","request.json"):
                (folder/member_name).write_bytes(ref.read(member_name))
        request = read(folder/"request.json")
        subset_request = deepcopy(request)
        next(p for p in subset_request["parts"] if p["id"] == "cog")["quantity"] -= 1
        subset_job = deepcopy(job)
        next(p for p in subset_job["parts"] if p["id"] == "cog")["quantity"] -= 1
        write(folder/"request65.json",subset_request)
        first = [deepcopy(p) for p in layout["placements"] if p["sheet_id"] != short_id]
        placed = first + deepcopy(short)
        ids = Counter()
        for i,p in enumerate(placed):
            p["sheet_id"] = "sheet-0" if i < len(first) else "sheet-1"
            p["copy_index"] = ids[p["part_id"]]
            ids[p["part_id"]] += 1
        assert len(first) == 53 and ids == {"frame":18,"bracket":12,"insert":21,"cog":14}
        assembly = {**layout, "placements":placed}
        write(folder/"partial.json",assembly)
        full = validate(binary,folder,"request.json","partial.json","full-quantity-check")
        reduced = validate(binary,folder,"request65.json","partial.json","partial-geometry-check")
        assert not full["valid"] and reduced["valid"] and reduced["metrics"]["placed_parts"] == 65
        independent = geometry_check(assembly,assembly,subset_job,request,"sheet-1",reduced["metrics"])
        assert independent["meets_source_tolerance"] and reduced["metrics"]["material_area"] <= targets["target_material_mm2"]
        summaries.append(dict(archive=archive,member=member,sha256=digest,source_short_sheet=short_id,
                              partial_metrics=reduced["metrics"], full_violations=full["violations"],
                              independent=independent, missing_family="cog",missing_copy_index=14))
    result = dict(layout_count=len(group),minimum_transfers=dict(sorted(histogram.items())),one_transfer=nearest,
                  checked_short_sha256=sha256(short_file.read_bytes()).hexdigest(),target_mm2=targets["target_material_mm2"],
                  constructions=summaries)
    write(out/"inventory.json",result)
    print(json.dumps({"minimum_transfers":result["minimum_transfers"],"receivers":len(summaries),
                      "65_part_material":[s["partial_metrics"]["material_area"] for s in summaries]}))


if __name__ == "__main__":
    main()
