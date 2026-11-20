"""Check the equal-budget opt-in measurement and reconstruct the straight-sided development jobs."""
import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import median
import sys
from zipfile import ZipFile

RESULTS=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(RESULTS/"h5-opt-in-hole-audit-20261120"),str(RESULTS/"h5-opt-in-material-budget-20261120")]
from audit import audit_archive,verify_rows
from matching_requests import verify


def main(folder,out):
    d=json.loads((folder/"results.json").read_bytes())
    assert d["seconds"]==60 and d["seeds"]==[0,1,2] and d["kerfs_mm"]==[0.2,1.5]
    assert d["common_line_allow_part_in_hole"] and not d["held_out_geometry_read"]
    expected={(job,k,s,a) for job in d["jobs"] for k in d["kerfs_mm"] for s in d["seeds"] for a in ("normal","off","bonus")}
    rows=d["rows"]
    assert len(rows)==len(expected) and {(r["job"],r["kerf_mm"],r["seed"],r["arm"]) for r in rows}==expected
    assert d["product_commit"]=="e06552974048fcc4386431cf0b8b505467a850e3"
    members=verify_rows(folder,rows)
    inputs=verify(folder)
    shapes,adopted=[],[]
    for r in rows:
        if r["status"]!="valid":
            continue
        archive=folder/r["archive"]
        if r["job"].startswith("c-"):
            shapes.append(dict(archive=r["archive"],sheets=audit_archive(archive)))
        with ZipFile(archive) as z:
            stages=[json.loads(line) for line in z.read("nest-stderr.log").decode().splitlines()
                    if line.startswith("{") and '"stage":"common-line-rows"' in line]
        if stages:
            assert r["arm"]=="bonus"
            adopted.append(dict(archive=r["archive"],stages=stages))
    gates=[]
    for k in d["kerfs_mm"]:
        comparisons=[]
        for j in d["jobs"]:
            arms={a:[r for r in rows if (r["job"],r["kerf_mm"],r["arm"])==(j,k,a) and r["status"]=="valid"]
                  for a in ("normal","off","bonus")}
            if min(map(len,arms.values()))<3:
                comparisons.append(dict(job=j,complete=False))
                continue
            material={a:median(r["material"] for r in values) for a,values in arms.items()}
            change=(material["bonus"]/material["normal"]-1)*100
            savings=median(r["saved_fraction"] for r in arms["bonus"])*100
            stored,=[p for p in d["pairs"] if p["job"]==j and p["kerf_mm"]==k]
            assert abs(stored["material_cost_percent"]-change)<1e-8
            assert abs(stored["bonus_saved_fraction"]*100-savings)<1e-8
            comparisons.append(dict(job=j,complete=True,material=material,material_change_percent=change,
                                    cutting_saved_percent=savings,within_material=change<=1))
        valid=[c for c in comparisons if c["complete"]]
        gates.append(dict(kerf_mm=k,jobs=comparisons,within_material=sum(c["within_material"] for c in valid),
                          median_saved_percent=median(c["cutting_saved_percent"] for c in valid) if len(valid)==len(d["jobs"]) else None))
    out.write_text(json.dumps(dict(source=d["product_commit"],archives=len(rows),checked_members=members,
                        statuses=dict(Counter(r["status"] for r in rows)),matched_inputs=inputs,gates=gates,
                        new_rows_accepted=adopted,straight_sided_jobs=shapes),indent=2)+"\n",encoding="utf-8",newline="\n")
    print([(g["kerf_mm"],g["within_material"],g["median_saved_percent"]) for g in gates],
          len(adopted),"row layouts accepted;",len(shapes),"straight-sided layouts checked")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder",type=Path)
    parser.add_argument("out",type=Path)
    args=parser.parse_args()
    main(args.folder,args.out)
