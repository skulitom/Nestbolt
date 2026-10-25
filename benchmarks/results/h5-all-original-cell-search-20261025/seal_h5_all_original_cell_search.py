"""Save complete guarded cells, closed full search and audited table projection."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-all-original-cell-search-20261025';BASE=ROOT/'output'/NAME;CELLS=ROOT/'output/h5-remaining-displacement-cells-20261025';OUT=ROOT/'benchmarks/results'/NAME;SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025';CONVEX=ROOT/'output/h5-convex-domain-conflicts-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    prep=load(CELLS/'result.json');cells=load(CELLS/'audit-repaired/checks.json');model=load(BASE/'shared-search/solve/model-audit.json');solved=load(BASE/'shared-search/solve/result.json');timing=load(BASE/'search-audit/checks.json');projection=load(BASE/'direct-geometry-projection/result.json');prcheck=load(BASE/'direct-geometry-projection/audit/checks.json')
    assert all(r['passed'] for r in [cells,model,timing,prcheck]) and prep['completed_cases']==162 and not prep['pending_cases']
    assert solved['status']=='UNKNOWN' and not solved['has_full_original_model_candidate'] and timing['shared_budget_honored'] and projection['solver_calls']==0
    prior=load(ROOT/'benchmarks/results/h5-six-cog-guided-search-20261025/source-review.json');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head==mainhead=='728b2db2e86c2d123920fdceb8e3e2c1bcf1f66e'
    ci=json.loads(subprocess.check_output(['gh','run','view','40246226212','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead;write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    push=load(ROOT/'output/h5-guided-main-sync-20261025/receipt.json');assert push['source_head']==head and push['pushed_commits']==10 and push['remote_main_verified'];shutil.copyfile(ROOT/'output/h5-guided-main-sync-20261025/receipt.json',BASE/'previous-main-push.json')
    action=('The full nine-anchor guarded-cell search is closed UNKNOWN without a candidate. Its 45-second soft limit was exceeded by 7.627968 seconds; the complete 57.609353-second pipeline stayed inside 60 seconds. '
        'All 162 remaining ordered query-pair representations and all 364 physical pair/mode uses now have independently proved full guarded displacement cells: 6,174 cells, 19,329 inward planes and 38,211 exact whole-cell/failure-region certificates. '
        'The full model retains all 66 originals, nine movable and 57 fixed, with all 36 direct guarded moving-pair constraints. A separate projection removes only the obsolete 1,572,932-literal pair table and its 3,395 private auxiliaries. '
        'Independent inverse reconstruction verifies every one of the 173,814 remaining constraints and 32,074 variables, every mapping/hint and actual solver import/export. The projected model has not been solved. '
        'Next make a distinct one-call diagnostic using only that verified projection, with its own declared 60-second loading/verification/search budget, at most 45 solver seconds and a 10-second shutdown reserve informed by the observed soft overshoot. '
        'Do not repeat the previous full model or reopen a closed call. Keep the larger reserve explicit and use the actual remaining time. Offline region construction and projection audit are not a production-budget qualification. '
        'A positive still needs source-inequality read-back, every original geometry/count/stock check, native validation, general production integration and the unchanged 13-job/two-kerf H5 matrix. '
        'The 29 conservatively simplified remaining-pair representations and original first-sheet cog restriction limit negative scope; no unrestricted impossibility is claimed. '
        'H2 stays open under the original gate, with all 22 reserved vectors untouched. Main 728b2db2 contains the ten prior checkpoints; await its terminal CI before the next normal push and preserve any newer remote changes. No new release is qualified.')
    OUT.mkdir()
    copies={
        CELLS/'plan.json':'cell-preparation-plan.json',CELLS/'result.json':'cell-preparation-result.json',CELLS/'summary.json':'cell-summary.json',CELLS/'audit-repaired/checks.json':'cell-audit.json',CELLS/'audit-repaired/case-checks.json':'cell-case-checks.json',CELLS/'audit/failure.txt':'cell-initial-audit-failure.txt',CELLS/'audit/repair-record.json':'cell-audit-repair.json',
        BASE/'shared-search/plan.json':'search-plan.json',BASE/'shared-search/budget.json':'search-budget.json',BASE/'shared-search/result.json':'search-result.json',BASE/'shared-search/solve/model-audit.json':'model-audit.json',BASE/'shared-search/solve/result.json':'solver-result.json',BASE/'search-audit/checks.json':'search-audit.json',
        BASE/'direct-geometry-projection/plan.json':'projection-plan.json',BASE/'direct-geometry-projection/result.json':'projection-result.json',BASE/'direct-geometry-projection/audit/checks.json':'projection-audit.json',BASE/'main-ci-snapshot.json':'main-ci-snapshot.json',BASE/'previous-main-push.json':'previous-main-push.json'}
    for a,b in copies.items():shutil.copyfile(a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'projected_solver_calls':0,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
        'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','full_solver_calls':1,'projection_solver_calls':0,
        'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,'pushed':False,'previous_checkpoints_pushed':10,
        'current_main_ci_id':40246226212,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for base in [BASE,CELLS]:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            plan=load(p)
            for n,h in plan.get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
            for field,folder in [('query_hashes',SOURCE/'queries'),('mutual_hashes',SOURCE/'mutual'),('group_hashes',CONVEX/'groups')]:
                for i,h in plan.get(field,{}).items():
                    q=folder/f'{int(i):03d}.json';assert digest(q)==h;members['source-inputs/'+q.relative_to(ROOT).as_posix()]=q
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    manifestpath=ROOT/'benchmarks/results/h5-six-cog-guided-search-20261025/raw-manifest.json';old=load(manifestpath);known={r['path']:r['sha256'] for r in old['files']+old['aliases']}
    for p in list((SOURCE/'queries').glob('*.json'))+list((SOURCE/'mutual').glob('*.json')):assert digest(p)==known['source-inputs/'+p.relative_to(ROOT).as_posix()]
    members['source-inputs/'+manifestpath.relative_to(ROOT).as_posix()]=manifestpath
    for p in (ROOT/'output/h5-guided-main-sync-20261025').glob('*.json'):members['main-push/'+p.name]=p
    names=['prepare_h5_remaining_displacement_cells.py','audit_h5_remaining_displacement_cells.py','repair_h5_remaining_cell_audit.py','audit_h5_remaining_displacement_cells_repaired.py','prepare_h5_all_original_cell_search.py','audit_h5_all_original_cell_master.py','solve_h5_all_original_cell_master.py','run_h5_all_original_cell_search.py','audit_h5_all_original_cell_search.py','prepare_h5_direct_geometry_projection.py','audit_h5_direct_geometry_projection.py','push_h5_guided_checkpoints.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'all162_remaining_query_pair_cells_independently_proved':True,'all36_original_pair_coordinates_present':True,'full_model_independently_reconstructed':True,
        'unknown_and_actual_soft_limit_overshoot_preserved':True,'shared_search_budget_honored':True,'projection_all_retained_fields_independently_inverse_verified':True,'projection_solver_calls':0,
        'failed_audit_and_repaired_readback_preserved':True,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: complete guarded coordinates and table-free projection — 2026-10-25

**All nine moving originals now participate in one full guarded-coordinate
model. Its bounded call remains UNKNOWN. An independently checked smaller
projection removes the obsolete compatibility table and is ready for a distinct
search.** All 66 originals remain required: nine movable and 57 fixed. No full
target layout, native pass or production qualification is claimed. H2/H5 remain
open at **60%**.

## Complete remaining-pair representation

The construction covers **162 ordered same-sheet query pairs / 364 physical
pair and mode uses** outside the existing cog/cog representation. Exact rational
clipping reconstructs each full guarded source-clause failure region within the
complete anchor-difference box. Outward dyadic vertex enclosures cover those
regions; convex cells in the complement are inset and rounded inward on the
micrometre grid. Explicit complete difference bounds are required in the model.

Preparation finishes in **{prep['seconds']:.6f}s**, with no pending case. Selected
representations contain **6,174 cells / 19,329 inward halfplanes**, corresponding
to **18,324 physical cell flags**. All raw candidate faces and **11 selected
inset/grid discards** are preserved. There are **32 zero-cell query-pair cases**;
their active pair/mode conjunction is forbidden by the constructed representation.

The declared selection first tries the unsimplified failure union. Cases above
96 cells may try topology-preserving simplification at 0.001 and 0.005 mm,
each padded outward by twice its tolerance; whole failure-union coverage is
required. **29 selected cases use that stricter representation**. Every candidate
and selection is retained. Every selected raw free region is fully covered;
inset/grid losses and extra outward padding remain constructive restrictions,
not relaxed clearance or unrestricted impossibility evidence.

Independent audit takes **{cells['seconds']:.6f}s**, rebuilds all **902 source
failure polygons**, checks every retained inward plane and proves **38,211
whole-cell/failure-region separations** using exact rational projections. Each
certificate is read back. Floating calculations only nominate a candidate axis.
Thus every retained integer displacement satisfies every full guarded original
source clause, provided the explicit difference bounds hold.

The first audit failed an exact polygon-representation comparison after
reconstructing the same union from reoriented rings. Its script, plan and
traceback remain preserved. The separate repaired audit still verifies geometric
equality of the reconstructed union, then uses the recorded ring order for the
zero-tolerance reconstruction comparison. All exact cell-safety requirements
remain. No original geometry or construction was regenerated.

## Closed complete-coordinate search

The new model retains all original domain choices, counts, area charges, copy
ordering, regional capacities, cog constraints and certified exclusions. It adds
the two bracket anchors and insert anchor, every source domain's bounds and
inward halfplanes, and exact query-pair activation for the 364 remaining uses.
Active pairs choose exactly one safe cell; inactive pairs choose none. Both
complete difference bounds and each chosen cell's bounds/planes are enforced.
All **36 physical moving-original pairs** now have full guarded coordinates.
The prior independently proved nine-domain exclusion is retained.

Independent protobuf reconstruction checks **35,469 variables / 181,700
constraints**, all **18 coordinate variables**, all **9,776 domain choices**
and **79 advisory hints**. The new bracket/insert domain constraints include
**17,124 halfplanes / 10,348 conditional axis bounds**; remaining pair cells
add **59,740 conditional halfplanes**. Construction takes
**{model['construction_seconds']:.6f}s**, model audit **{model['audit_seconds']:.6f}s**.

The single eight-worker, seed-zero call has a 45-second soft limit and returns
**UNKNOWN in {solved['seconds']:.6f}s**, without a candidate. Its **{timing['solver_soft_limit_overshoot_seconds']:.6f}s
soft-limit overrun** is preserved explicitly. The complete loading/construction/
audit/search pipeline takes **{timing['actual_shared_seconds']:.6f}s**, within the
shared 60-second budget. The call is closed, with no restart or continuation.
No full original layout or native validation follows this negative outcome.
UNKNOWN proves neither feasibility nor impossibility.

## Audited removal of the obsolete pair table

The model still carried **1,572,932 literals** from an older necessary
domain-compatibility table. The direct pair geometry now establishes original
separation independently of that table. A distinct projection deletes only
**7,886 table constraints and 3,395 private group variables**. Every original
domain, count, area, coordinate, full guarded pair condition, capacity, hint and
certified exclusion remains. The result has **32,074 variables / 173,814
constraints**. It has **not been solved**.

Independent audit reconstructs every deleted definition and table constraint
from its source bitset. It inverse-maps every retained variable and complete
constraint and requires exact equality to the fully audited parent. Reinserting
the original removed block reconstructs the entire parent protobuf exactly.
The variable mapping and all 79 hints also match. Import into the actual solver
model, validation and export preserve every protobuf field. This takes
**{prcheck['seconds']:.6f}s**, with no solver call.

Next use this audited projection in a distinct bounded call, with a declared
60-second loading/verification/search budget, at most 45 solver seconds and a
**10-second shutdown reserve** informed by the observed soft overrun. Do not
repeat the closed model. Offline cell preparation and projection audit remain
separate diagnostic work, not a production-budget pass. A positive still needs
all original inequality/geometry/count/stock checks, native validation, general
production integration and the unchanged 13-job/two-kerf H5 matrix.

## Repository and evidence

The previous ten checkpoints were normally pushed from 61359456 to 728b2db2;
the remote update was verified. Current main remains 728b2db2, and its own
[CI 40246226212]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful
jobs at the saved snapshot. This new checkpoint waits for terminal CI before
another normal push, preserving any newer remote work first. Production source,
all three accurate READMEs, preview v0.2.0-alpha.1 and stable Latest v0.1.0 are
unchanged. No new release is qualified. H2 retains its original gate and all
22 reserved vectors remain untouched.

Evidence: [cell audit]({NAME}/cell-audit.json), [full model]({NAME}/model-audit.json),
[closed search audit]({NAME}/search-audit.json),
[projection audit]({NAME}/projection-audit.json), [archive]({NAME}/raw-001.zip),
and [manifest]({NAME}/raw-manifest.json). **{archive['archive_members']} canonical
files and {archive['verified_aliases']} exact-content aliases** preserve all raw
cells/candidates, exact certificates, models, mappings, parameters, logs, failures,
source inputs and push receipts, with byte length, SHA-256 and CRC verification.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 complete guarded coordinates and table projection, 2026-10-25:** [the evidence]({link})
adds all 162 remaining query-pair representations for 364 physical pair/mode
uses. Their 6,174 cells and 19,329 inward planes pass 38,211 exact separation
certificates; all 29 stricter simplifications and 11 inset/grid discards remain
explicit. The full 35,469-variable / 181,700-constraint model now includes all
nine moving originals and every one of their 36 direct guarded pair relations,
with all 66 original counts required. Its single 45-second-cap call returns
UNKNOWN in 52.627968s: the 7.627968s soft overrun is retained, while total
57.609353s stays inside the shared 60s budget. No layout/native pass is claimed.
A separately audited projection removes only the obsolete 1,572,932-literal
table and 3,395 private variables, preserving every direct geometry/count/area
constraint. All 32,074 remaining variables and 173,814 constraints inverse-map
exactly to the parent; actual solver import/export passes. That projection has
not been solved. Next use a distinct bounded call with a 10s shutdown reserve;
offline preparation is not production qualification. The prior ten checkpoints
are pushed to main 728b2db2; its own CI 40246226212 remains tracked before the
next normal push. Production, READMEs and releases are unchanged. H2/H5 remain
open at 60%, with all 22 reserved H2 vectors untouched.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
