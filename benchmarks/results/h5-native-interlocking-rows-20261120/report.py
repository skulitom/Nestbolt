"""Render the H5 development comparison from its separately verified measurements."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from statistics import median


HERE=Path(__file__).resolve().parent
RESULTS=HERE.parent
PILOT="h5-common-native-row-pilot-20261120T154338Z"


def read(path):
    return json.loads(path.read_bytes())


def main(folder,out):
    raw=read(folder/"results.json")
    audit=read(HERE/"confirmation-audit.json")
    replay=read(HERE/"confirmation-replay.json")
    jobs=raw["jobs"]
    assert len(jobs)==13 and len(raw["rows"])==234 and audit["source"]==replay["source"]==raw["product_commit"]
    assert audit["verified_archives"]==replay["archives"] and audit["verified_members"]==replay["checked_members"]
    gates=replay["gates"]
    complete=raw["valid"]==234
    pairs={(j["job"],g["kerf_mm"]):j for g in gates for j in g["jobs"]}
    assert all(j["complete"] for j in pairs.values())
    for g,a in zip(gates,audit["gates"],strict=True):
        assert abs(g["median_saved_percent"]-100*a["median_saved_fraction"])<1e-8
        assert a["passed"]==(g["within_material"]==13 and g["median_saved_percent"]>=10)
    passed=complete and all(g["within_material"]==13 and g["median_saved_percent"]>=10 for g in gates)
    headline=("The opt-in configuration met the cutting and material limits at both kerfs."
              if passed else "H5 remains open. The opt-in configuration missed one or more original limits.")
    text=["# Interlocking common-line rows in the 13-job development comparison","",headline+" "
          f"All {raw['valid']} complete layouts passed the public validator. The comparison used ordinary nesting at matching spacing, "
          "the same 13 frozen development jobs, 60 seconds on one physical core per run, and seeds 0, 1 and 2. "
          "The two common-line arms allowed parts inside holes. Only the bonus arm searched for interlocking rows and shared edges.","",
          "| Kerf | Median cutting distance saved | Worst material change vs ordinary | Jobs within +1% material |",
          "| --- | ---: | ---: | ---: |"]
    for g in gates:
        worst=max(g["jobs"],key=lambda j:j["material_change_percent"])
        text.append(f"| {g['kerf_mm']} mm | {g['median_saved_percent']:.3f}% | {worst['material_change_percent']:+.3f}% ({worst['job']}) | {g['within_material']}/13 |")
    text+=["","Each job uses three-seed medians. The material comparison divides the bonus median by the ordinary median. "
           "The cut-length gate requires the median across jobs to reach 10% separately at each kerf. The material ceiling applies to every job.",
           "",f"All 36 layouts passed the [two-job pilot]({PILOT}/README.md) before the full comparison. "
           "The [source construction](h5-repeated-bands-20261120.md) groups up to four right-angled parts, then chooses rows that fit across the available stock. "
           "The product uses a portion of the existing common-line time allowance and checks each proposed layout against the source geometry, current material use and shared cutting length. "
           "The default common-line policy reserves holes.","","## Per-job results","",
           "| Job | Laser cut saved | Laser material | Plasma cut saved | Plasma material |",
           "| --- | ---: | ---: | ---: | ---: |"]
    for j in jobs:
        l,p=pairs[j,0.2],pairs[j,1.5]
        text.append(f"| {j} | {l['cutting_saved_percent']:.3f}% | {l['material_change_percent']:+.3f}% | "
                    f"{p['cutting_saved_percent']:.3f}% | {p['material_change_percent']:+.3f}% |")
    if not passed:
        for (j,k),r in pairs.items():
            if not r["within_material"]:
                text+=["",f"The {j} job at {k} mm exceeded the +1% ceiling. Its material change was {r['material_change_percent']:+.3f}%."]
    text+=["",f"[All three arms, including the bonus-off results]({folder.name}/README.md). "
           "The [original hole-reserving comparison](h5-cutting-development-20261015.md), "
           "[first opt-in measurement](h5-opt-in-holes-20261120.md), and [experimental scheduler](h5-opt-in-material-budget-20261120.md) retain their original failures.","",
           "## Independent checks","",
           f"SHA-256 verification covered {replay['archives']} archives and {replay['checked_members']:,} members. "
           f"The {replay['matched_inputs']['identical_triples']} matched triples used identical source jobs and libraries. "
           "A second reading of the validated outputs reproduced the gate arithmetic. The checked product commit was "
           f"`{raw['product_commit'][:8]}`. [Inputs and scores]({HERE.name}/confirmation-replay.json).",""]
    boxes=read(HERE/"confirmation-boxes.json")
    groups=audit["mechanical"]+replay["straight_sided_jobs"]+boxes
    assert len(groups)==234 and {c["archive"] for c in groups}=={r["archive"] for r in raw["rows"]}
    sheets=[s for case in groups for s in case["sheets"]]
    cuts=[s for s in sheets if "exported_segments" in s]
    text+= [f"Independent geometry reconstruction covered all {len(groups)} layouts, "
           f"{sum(s['pair_distances'] for s in sheets):,} part-pair distances, and {sum(s['shared_edges'] for s in cuts):,} shared edges. "
           f"The maximum original-to-exported CUT vertex error was {max(s['maximum_cut_vertex_error_mm'] for s in cuts):.9f} mm. "
           f"The largest shared-edge offset difference was {max(s['largest_offset_error_mm'] for s in cuts):.6f} mm against 0.01 mm. "
           "Every tested SVG CUT and COMMON segment matched its DXF counterpart. "
           f"[Mechanical geometry and arm distributions]({HERE.name}/confirmation-audit.json).","",
           "The first box check flagged a 3 mm discrepancy. Its source contour divided a straight 160 mm side into three segments of 3, 154 and 3 mm. "
           "The exported offset coincides exactly with the full side. The box check now verifies continuous collinear source sections across the contour start. "
           f"The 10 mm minimum overlap and 0.01 mm offset tolerance apply throughout. [Original rejection]({HERE.name}/box-offset-first-rejection.json). "
           f"[All 108 box layouts]({HERE.name}/confirmation-boxes.json).","",
           "The CLI, stdio MCP, Chrome and Firefox produced the same 80-copy mixed-bracket layout. CLI and MCP also produced byte-identical SVGs and DXFs. "
           "Chrome’s first fixed-work run reached its 30-second wall limit and returned a valid earlier layout. Its isolated replay finished the work budget. "
           f"Both browsers returned the reference layout in 15-second wall-timed runs. [Surface results]({HERE.name}/surfaces.json). "
           f"[Six fixed-work compatibility comparisons]({HERE.name}/compatibility.json) cover ordinary nesting and the default hole policy.","",
           "The October laser SVG and plasma DXF were opened in LightBurn 2.1.01. Re-exporting both coupons with the current executable produced the same four "
           "SVG and R2007 DXF files as the earlier opt-in build. The current DXFs match the native-checked originals in units, layers and all nine cutting entities. "
           f"[Current export hashes]({HERE.name}/native-fixtures.json) and [native measurements and screenshots](h5-commonline-checkpoint-20261014.md#native-lightburn-evidence). "
           f"The combined line and arc lead fixtures retain the same six validated reservations each. [Lead results]({HERE.name}/combined-leads.json). "
           f"[Build and test results]({HERE.name}/functional-tests.json).","",
           "## Deepnest comparison","",
           "Deepnest used its required zero spacing. Its native merged-length report and measured SVG saving are separate quantities. "
           "The 39 historical runs yielded 35 layouts and four no-layout outcomes. Distances below are three-seed medians in millimetres. "
           "[Original archive verification](h5-opt-in-hole-audit-20261120/deepnest-replay.json).","",
           "| Job | Nestbolt laser saved | Nestbolt plasma saved | Deepnest native merged | Deepnest SVG saved |",
           "| --- | ---: | ---: | ---: | ---: |"]
    deep=read(RESULTS/"h5-opt-in-hole-audit-20261120/deepnest-replay.json")
    assert sha256((RESULTS/"h5-cutting-development-20261015.json").read_bytes()).hexdigest()==deep["sha256"]
    for j in jobs:
        lengths=[median(r["cut_without_common_mm"]-r["cut_with_common_mm"] for r in raw["rows"]
                        if r["job"]==j and r["kerf_mm"]==k and r["arm"]=="bonus") for k in (0.2,1.5)]
        v=deep["jobs"][j]
        other=[f"{v[key]['median']:,.1f}" if v["valid"]==3 else f"{v['valid']}/3 valid"
               for key in ("native_merged_length_mm","export_saved_length_mm")]
        text.append(f"| {j} | {lengths[0]:,.1f} | {lengths[1]:,.1f} | {other[0]} | {other[1]} |")
    out.write_text("\n".join(text)+"\n",encoding="utf-8",newline="\n")
    print("Original numerical gates:",passed)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder",type=Path)
    parser.add_argument("out",type=Path)
    args=parser.parse_args()
    main(args.folder,args.out)
