"""Archive the verified12-mover geometry and complete local partial-anchor repair."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-expanded-cog-neighborhood-20261026';OUT=ROOT/'benchmarks/results'/NAME;REG=ROOT/'output'/NAME;JOINT=ROOT/'output/h5-expanded-cog-joint-prepared-20261026';REVIEW=ROOT/'output/h5-expanded-cog-source-review-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(REVIEW/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='d1645404d65e8ce2b81a266955d8e84f4bf1b569';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
    ra=load(REG/'audit/checks.json');aa=load(REG/'anchor-repair-census/audit/checks.json');ja=load(JOINT/'audit/checks.json');assert all(c['passed'] for c in [ra,aa,ja]) and ja['all9_repaired_partial_anchors_representable'] and aa['feasible_partial_triples']==54
    OUT.mkdir()
    copies=[(REG/'result.json','region-result.json'),(REG/'query-summary.json','expanded-query-summary.json'),(REG/'audit/checks.json','region-audit.json'),(REG/'audit/query-checks.json','region-comparison.json'),(REG/'prior-partial-anchor-membership.json','original-anchor-membership.json'),(REG/'anchor-repair-census/result.json','anchor-census-result.json'),(REG/'anchor-repair-census/audit/checks.json','anchor-census-audit.json'),(REG/'anchor-repair-census/audit/three-anchor-shifts.json','verified-anchor-shifts.json'),(REG/'anchor-repair-census/audit/verified-nine-cog-anchors.json','verified-nine-cog-anchors.json'),(JOINT/'result.json','joint-domain-result.json'),(JOINT/'query-summary.json','joint-domain-summary.json'),(JOINT/'audit/checks.json','joint-domain-audit.json'),(JOINT/'audit/verified-partial-domain-membership.json','verified-partial-domain-membership.json'),(REVIEW/'review.json','source-review.json'),(REVIEW/'main-ci.json','main-ci-d1645404-snapshot.json'),(ROOT/'output/h5-compact-source-main-sync-20261026/receipt.json','prior-main-push-receipt.json')]
    for p,n in copies:shutil.copyfile(p,OUT/n)
    action=('The new54-fixed/12-mover geometry and all3716 inward domains are independently audited, with all66 original parts mandatory and all9 repaired partial cog anchors represented. Next prepare a new full12-original coordinate model from output/h5-expanded-cog-joint-prepared-20261026. It must include all24 coordinate variables,52 query-mode choices, all538 physical same-sheet query-pair relations over66 physical pairs, complete inward domains, current original count/stock/native guards and freshly recomputed global area charges. Use the verified one-sided exact shared-direction encoding, recomputing query difference bounds and live-edge eliminations from the NEW domains. Do not import fixed57 domain-conflict tables, occupancy/no-good exclusions, region-area capacities or witness locks. Any additional necessary occupancy bound must be newly certified against these54-fixed domains and the unchanged original geometric separation proof. Add only advisory hints from the independently checked9-cog partial; establish any identical-copy symmetry and hint permutation explicitly. Independent whole-model reconstruction and actual solver import/export are required before one separately declared bounded call. The partial still misses brackets28/29 and insert50, which must never become optional. A positive needs all66 original outlines/cutouts, every pair/stock/material check and native validation; production integration and the entire13-job/two-kerf matrix remain required. All earlier solver calls stay closed. Currentmain d1645404 CI40256286467 is still running; wait for its terminal result before a normal main push. H2 keeps its original gate and22 reserved vectors untouched; no release is newly qualified.')
    write(OUT/'next-step.json',{'action':action,'source_geometry':'output/h5-expanded-cog-joint-prepared-20261026','required_originals':66,'moving_originals':12,'fixed_originals':54,'full_target_witness':False,'H5_complete':False})
    bases=[REG,JOINT,REVIEW,ROOT/'output/h5-compact-source-main-sync-20261026'];members={};inputs={}
    for base in bases:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            data=load(p)
            for field in ['inputs','input_hashes','additional_inputs']:
                for n,h in data.get(field,{}).items():
                    if n in inputs:assert inputs[n]==h
                    inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-guarded-source-adjustment-20261025','h5-full-original-joint-20261025','h5-one-sided-conflict-propagation-20261026','h5-source-area-and-direction-sharing-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['build_h5_expanded_cog_regions.py','audit_h5_expanded_cog_regions.py','check_h5_expanded_cog_anchor_repair.py','audit_h5_expanded_anchor_repair.py','build_h5_expanded_cog_joint_domains.py','audit_h5_expanded_cog_joint_domains.py','review_h5_expanded_cog_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py']
    pending=[ROOT/'output'/n for n in names];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'all66_originals_mandatory':True,'fixed_originals':54,'moving_originals':12,'all20_fresh_free_regions_independently_verified':True,'complete729_anchor_census_independently_verified':True,'original_item53_constructive_anchor_exclusion_preserved':True,'old_region_exact_containment_discrepancy_preserved':True,'partial63_original_pair_and_stock_checks_pass':True,'all3716_inward_domains_independently_verified':True,'all82_reused_full_original_mutual_cases_verified':True,'all9_repaired_partial_anchors_representable':True,'no_old_fixed57_conditional_exclusion_transferred':True,'new_solver_calls':0,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: expanded cog neighborhood — 2026-10-26

**Fresh geometry for 12 mandatory movers and 54 fixed originals is verified.**
This releases neighboring original cogs **53, 56 and 61** in addition to the
previous nine movers. All 66 originals remain required. No new solver call,
complete target or native acceptance occurs. H2/H5 stay open at **60%**.

## Fresh regions and preserved inventory

The three released cogs already use the same source angle and original profile
as the six previously moving cogs. All ten profiles and 100 independently
certified fixed-style collision obstacles therefore remain reusable unchanged.
Recompute all 20 free regions using only the retained 54 original placements:
47 on sheet 1 and seven on sheet 2. Their transforms remain unchanged.
The moving inventory is two brackets, one insert and nine cogs.

Fixed area charges are recomputed to **3,681,713,590 / 249,662,718** units of
0.001 mm². The material target, native guards, 0.2125 mm construction clearance,
clearance-envelope margin and stock margins remain unchanged. No old fixed57
domain table, regional capacity, occupancy/no-good or source-area exclusion is
transferred to the expanded search space.

An independent audit reconstructs every new region by sequentially subtracting
the cached obstacles in reverse order. Its maximum Hausdorff difference from
the producer's union-subtraction result is zero. All 1,102 retained fixed-pair
checks pass. The old regions have zero recorded lost area. Exact containment
reports true for 19 queries and false for the first-sheet cog query; that
numerical boundary discrepancy remains recorded, without an exhaustive
containment claim. Sheet 2 is unchanged.

## Explicit repair of a prior partial anchor

The previous **63-original partial** is still geometrically valid under the
original native guards. But original cog 53's continuous source anchor and
nearest grid point lie outside the stronger moving-construction free region.
That original exclusion is preserved.

For each newly released cog, enumerate exactly the nine nearest-grid points
offset by −1, 0 or +1 micrometre in each direction. Keep the six prior witness
cog positions fixed for this diagnostic. Check all **27 points**, **358 source
pair cases**, **973,760 integer inequalities** and **729 triples**. Exactly
**54 triples** pass. Independently verify every result and the exact rational
minimum-shift ranking. The selected changes move an anchor axis by at most
**0.001428556 mm**, including rounding from the original continuous pose.

Reconstruct all 63 actual original outlines and their **83 cutouts / 9,172
cutout vertices**. All **1,467** same-sheet pair checks and **252** stock-edge
checks pass; minimum pair gap is **0.212500 mm**, above the unchanged native
guarded requirement **0.211709 mm**. All 22 selected moving-cog pair relations
pass the full original source clauses. The 54 fixed transforms and six earlier
witness positions remain unchanged. This remains a partial missing brackets
**28/29** and insert **50**; it is not a cutting layout or H5 result.

## Complete inward-domain preparation

The new regions produce **3,718 raw convex faces**, **3,716 inward integer
domains**, two explicitly recorded discards and **12,631 inward halfplanes**.
No merge/time/face cap fires and no positive-area raw coverage gap is recorded.
Every inset, discard, bound and rational coefficient-error rounding is independently
checked. All nine repaired partial anchors belong to at least one new domain.

The 82 original mutual profile-pair files are reused byte-for-byte, with their
committed independent geometry proof and all **27,256** outside-plane rounding
checks verified again. The fresh inventory covers **66 physical pairs** and
**538 same-sheet query-pair modes**. These are constructive finite-angle/grid
domains, not an unrestricted packing proof.

Next build and independently audit a fresh 12-original coordinate model from
these domains. Recompute all difference-bound reductions and any additional
capacity certificates; require all three missing originals. Use the checked
partial only as advisory hints. Full 66-original geometry/native validation,
production integration and the complete 13-job/two-kerf matrix remain necessary.
All earlier solver calls remain closed.

The prior two-checkpoint push to **d1645404** is retained with its receipt.
At 02:08 UTC, [its CI 40256286467](https://github.com/skulitom/Nestbolt/actions/runs/40256286467)
is running with four jobs passed. Preserve that run before another normal push.
Upstream state, production and READMEs are unchanged. No new release is qualified;
preview v0.2.0-alpha.1 and stable v0.1.0 remain appropriate. H2 retains its original
gate and all 22 reserved vectors remain untouched.

Evidence: [region audit]({NAME}/region-audit.json),
[complete local-census audit]({NAME}/anchor-census-audit.json),
[three small shifts]({NAME}/verified-anchor-shifts.json),
[joint-domain audit]({NAME}/joint-domain-audit.json),
[checks]({NAME}/checks.json), and [raw manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}**
exact-content aliases are size/SHA-256/CRC verified in **{archive['archive_parts']}**
independently readable archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 expanded cog neighborhood, 2026-10-26:** [the evidence]({link})
releases original cogs 53/56/61 for a fresh 12-mover/54-fixed construction,
retaining all 66 required originals and native guards. All 20 recomputed free
regions and 3,716 inward domains pass independent checks; no old fixed57
conditional restrictions are imported. Cog 53's original constructive-anchor
exclusion is preserved. A complete 729-triple local grid census yields 54 valid
partial repairs; the selected shifts pass all 1,467 original pair and 252 stock
checks. All nine partial cog anchors are represented in the new domains, while
brackets 28/29 and insert 50 remain missing and mandatory. The fresh geometry
covers 66 physical pairs/538 query-pair modes. Next build and audit the complete
12-part coordinate model; no solver or native call occurred here. Prior
checkpoints are on main d1645404, whose CI is running with four jobs passed at
the retained snapshot. H2/H5 stay open at 60%; production, READMEs, releases and
the 22 reserved H2 vectors remain unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
