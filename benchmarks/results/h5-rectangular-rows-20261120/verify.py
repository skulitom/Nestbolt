"""Replay the CLI archives and recompute matched material and cutting results."""
import argparse
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path
from statistics import median
import sys

HERE = Path(__file__).resolve().parent
for directory in ("h5-native-interlocking-rows-20261120", "h5-opt-in-hole-audit-20261120", "h5-opt-in-material-budget-20261120"):
    sys.path.insert(0, str(HERE.parent / directory))
from audit import audit_archive, verify_rows
from check_boxes import straight_ring
from matching_requests import verify


def geometry(path):
    return dict(archive=path.name,sheets=audit_archive(path,straight_ring if path.name.startswith("m-box-") else None))


def main(folder, output, pilot, source):
    data=json.loads((folder/"results.json").read_bytes())
    plan=json.loads((HERE/"plan.json").read_bytes())
    previous=json.loads((HERE.parent/plan["previous"]/"results.json").read_bytes())
    jobs=plan["pilot"]["jobs"] if pilot else previous["jobs"]
    expected={(j,k,s,a) for j in jobs for k in (0.2,1.5) for s in (0,1,2) for a in ("normal","off","bonus")}
    rows=data["rows"]
    assert data["product_commit"] == source and data["seconds"]==60
    assert data["common_line_allow_part_in_hole"] and not data["held_out_geometry_read"]
    assert data["guards"]["manifest"]==previous["guards"]["manifest"]
    assert set(data["jobs"])==set(jobs) and data["kerfs_mm"]==[0.2,1.5] and data["seeds"]==[0,1,2]
    assert len(expected)==len(rows)==data["total"]==data["valid"]
    assert {(r["job"],r["kerf_mm"],r["seed"],r["arm"]) for r in rows}==expected
    members=verify_rows(folder,rows)
    inputs=verify(folder)
    with ProcessPoolExecutor(max_workers=3) as pool:
        cases=list(pool.map(geometry,[folder/r["archive"] for r in rows]))
    assert len({r["archive"] for r in cases})==len(rows)
    gates=[]
    for kerf in data["kerfs_mm"]:
        pairs=[]
        for job in jobs:
            arms={a:[r for r in rows if (r["job"],r["kerf_mm"],r["arm"])==(job,kerf,a)] for a in ("normal","off","bonus")}
            material={a:median(r["material"] for r in group) for a,group in arms.items()}
            cut={a:100*median(1-r["cut_with_common_mm"]/r["cut_without_common_mm"] for r in arms[a]) for a in ("off","bonus")}
            change=100*(material["bonus"]/material["normal"]-1)
            stored,=[p for p in data["pairs"] if p["job"]==job and p["kerf_mm"]==kerf]
            assert abs(change-stored["material_cost_percent"])<1e-8 and abs(cut["bonus"]-100*stored["bonus_saved_fraction"])<1e-8
            pairs.append(dict(job=job,material=material,material_change_percent=change,cut_saved_percent=cut,within_material=change<=1.0))
        saved=median(p["cut_saved_percent"]["bonus"] for p in pairs)
        gates.append(dict(kerf_mm=kerf,median_saved_percent=saved,pairs=pairs,passed=all(p["within_material"] for p in pairs) and (pilot or saved>=10)))
    sheets=[s for c in cases for s in c["sheets"]]
    cuts=[s for s in sheets if "exported_segments" in s]
    summary=dict(checked_layouts=len(cases),pair_distances=sum(s["pair_distances"] for s in sheets),
        shared_edges=sum(s["shared_edges"] for s in cuts),max_cut_vertex_error_mm=max(s["maximum_cut_vertex_error_mm"] for s in cuts),
        max_offset_difference_mm=max(s["largest_offset_error_mm"] for s in cuts))
    result=dict(source=data["product_commit"],measurement=folder.name,archive_members=members,matched_inputs=inputs,geometry=summary,
        gates=gates,passed=all(g["passed"] for g in gates),cases=cases)
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8",newline="\n")
    print("passed",result["passed"],summary,[(g["kerf_mm"],g["median_saved_percent"]) for g in gates])
    return result["passed"]


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("--pilot",action="store_true")
    parser.add_argument("--source",default="50667e906b3837c0363118229dd2e7da445c7aa6")
    args=parser.parse_args()
    sys.exit(0 if main(args.folder,args.output,args.pilot,args.source) else 1)
