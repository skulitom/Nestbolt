"""Seal exact regional capacities, bounded coordinate relaxations and main merge."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-cog-region-capacities-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025';OLD=ROOT/'output/h5-original-domain-conflicts-20261025';CONVEX=ROOT/'output/h5-convex-domain-conflicts-20261025'
MERGE=ROOT/'output/h5-offcut-main-reconciliation-20261025';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    build=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');searchaudit=load(BASE/'search-audit/checks.json');diagnosis=load(BASE/'cog-witness-diagnosis/result.json')
    assert audit['passed'] and searchaudit['passed'] and load(BASE/'disk-relaxation/checks.json')['passed']
    assert build['retained_constraints']==35 and build['candidate_boxes_certified']==1215 and diagnosis['raw_original_collision_pairs']==4
    for name in ['shared-search','disk-search']:
        p=BASE/name;assert load(p/'result.json')['status']=='ANCHORS_INFEASIBLE' and load(p/'result.json')['elapsed_seconds']<60
        assert all(load(p/q)['passed'] for q in ['solve/model-audit.json','anchor-solve/model-audit.json','selection-audit/checks.json','selection-audit/regional-capacity-check.json'])
    prior=load(ROOT/'benchmarks/results/h5-convex-domain-conflicts-20261025/source-review.json');receipt=load(MERGE/'receipt.json')
    assert source_digest()==prior['production_digest']==receipt['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head==receipt['merge_head']=='da4ced0f80a504a4931f321701e61fbe1fae390a' and mainhead==receipt['remote_main']=='613594568fb49a71abf0248aec218a6b12f63319'
    for n,h in receipt['preserved_file_sha256'].items():assert digest(ROOT/n)==h
    oldci=json.loads((MERGE/'cancelled-prior-ci.stdout').read_bytes());assert oldci['conclusion']=='cancelled' and sum(j['conclusion']=='success' for j in oldci['jobs'])==5
    ci=json.loads(subprocess.check_output(['gh','run','view','40242602102','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Preserve both closed shared60-second pipelines and all earlier calls. All35 regional capacities are independently certified from1215 whole integer boxes; '
        'their30 capacity-one and5 capacity-two sums count all six source-angle cogs. The simultaneous-cog necessary master now binds all4602 physical cog-domain choices to12 anchors and uses a certified inner32-gon of the original258.082mm collision disk. '
        'It finds a necessary simultaneous-anchor assignment in38.615079 seconds, but4 of7 same-sheet cog pairs collide in the actual original geometry; the full original-coordinate selection is INFEASIBLE. '
        'The disk is therefore too weak for this remaining obstruction. Next strengthen simultaneous cog geometry using the complete independently audited original cog/cog forbidden polygon (case81,61 pieces,2720 edge inequalities), retaining every original cog tooth and the full guarded envelope. '
        'A staged exact-cog model can keep the refined whole-domain table, global triple exclusion, all32 additional second-sheet pair exclusions, capacity-two sheet bound and35 regional capacities, all9 mandatory domain selections and both original area constraints. '
        'Add full original mutual separation for every same-sheet cog pair, or a separately declared shared-budget generation of complete violated pieces; audit every bound reduction and conditional constraint before a new bounded call. '
        'Do not resume or extend a closed run, change seeds, loosen native guards or original material limits, or mistake inner-polygon feasibility for an original-shape witness. '
        'Any complete positive still requires all66 original polygons/stock, native validation, production-budget integration and the full13-job/two-kerf H5 matrix. '
        'Main61359456 adds15 public scrap/offcut documentation files. Merge da4ced0f preserves all15 and73 local evidence files byte-for-byte; production digest and READMEs are unchanged. '
        'Prior CI40240715636 was cancelled after5 passes, including no Windows pass; track new main CI40242602102 independently and preserve newer remote work before any normal push. '
        'H2 remains open under Artem\'s unchanged gate with all22 reserved vectors untouched. No new release is qualified.')
    OUT.mkdir();copies={'plan.json':'capacity-plan.json','result.json':'capacity-result.json','capacities.json':'capacities.json','audit/checks.json':'capacity-audit.json',
        'previous-selection-violations.json':'previous-selection-violations.json','disk-relaxation/polygon.json':'inner-disk-polygon.json','disk-relaxation/checks.json':'inner-disk-audit.json',
        'shared-search/result.json':'capacity-pipeline-result.json','shared-search/solve/model-audit.json':'capacity-master-audit.json','shared-search/solve/result.json':'capacity-master-result.json',
        'shared-search/anchor-solve/model-audit.json':'capacity-anchor-audit.json','shared-search/anchor-solve/result.json':'capacity-anchor-result.json',
        'disk-search/result.json':'coordinate-pipeline-result.json','disk-search/solve/model-audit.json':'coordinate-master-audit.json','disk-search/solve/result.json':'coordinate-master-result.json',
        'disk-search/solve/selection.json':'coordinate-selection.json','disk-search/solve/necessary-cog-positions.json':'necessary-cog-positions.json','disk-search/anchor-solve/model-audit.json':'coordinate-anchor-audit.json',
        'disk-search/anchor-solve/result.json':'coordinate-anchor-result.json','search-audit/checks.json':'search-audit.json','search-audit/pipeline-checks.json':'shared-budget-checks.json',
        'cog-witness-diagnosis/result.json':'original-cog-diagnosis.json','cog-witness-diagnosis/pairs.json':'original-cog-pairs.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    shutil.copyfile(MERGE/'receipt.json',OUT/'main-merge-receipt.json');write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],
        'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'master_solver_calls':2,'selected_anchor_solver_calls':2,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_limit_and_native_guards_unchanged':True,
        'remote_documentation_files_preserved':15,'local_evidence_files_preserved':73,'merge_commit':head,'pushed':False,'prior_main_ci_id':40240715636,'prior_main_ci_conclusion':'cancelled','prior_main_successful_jobs':5,
        'current_main_ci_id':40242602102,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for root in [BASE,MERGE]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for key in ['inputs','input_hashes']:
                for n,h in load(p).get(key,{}).items():
                    if n in inputs:assert inputs[n]==h
                    inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    plan=load(CONVEX/'plan.json')
    for key,folder in [('query_hashes','queries'),('mutual_hashes','mutual')]:
        for i,h in plan[key].items():
            p=SOURCE/folder/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder in [CONVEX/'groups',CONVEX/'cases',OLD/'cores',OLD/'three-cog-certificate',CONVEX/'second-sheet-pair-proofs/audit']:
        for p in folder.rglob('*'):
            if p.is_file():members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['build_h5_cog_region_capacities.py','audit_h5_cog_region_capacities.py','prepare_h5_cog_capacity_search.py','solve_h5_cog_capacity_master.py','audit_h5_cog_capacity_master.py',
        'audit_h5_cog_capacity_selection.py','solve_h5_cog_capacity_anchors.py','run_h5_cog_capacity_search.py','build_h5_cog_disk_relaxation.py','audit_h5_cog_coordinate_master.py',
        'prepare_h5_cog_coordinate_search.py','solve_h5_cog_coordinate_master.py','audit_h5_cog_coordinate_selection.py','solve_h5_cog_coordinate_anchors.py','run_h5_cog_coordinate_search.py',
        'audit_h5_capacity_searches.py','diagnose_h5_cog_coordinate_witness.py','reconcile_h5_offcut_main.py','solve_h5_second_sheet_master.py','audit_h5_second_sheet_selection.py',
        'solve_h5_selected_anchors.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'all1215_box_membership_and_dominance_proofs_checked':True,'all35_capacity_constraints_include_all_six_cogs':True,
        'strict_inner_original_collision_polygon_algebraically_checked':True,'all_four_search_models_independently_reconstructed':True,'both_pipelines_finish_within_shared60_seconds':True,
        'necessary_cog_anchor_witness_independently_checked':True,'all_four_original_cog_collision_failures_retained':True,'both_selected_coordinate_negatives_retained':True,
        'remote15_and_local73_files_preserved_byte_exact':True,'production_and_readmes_unchanged':True,'old_ci_cancelled_without_windows_pass_claim':True,'new_ci_independently_tracked':True,
        'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    first=load(BASE/'shared-search/result.json');second=load(BASE/'disk-search/result.json');master=load(BASE/'disk-search/solve/result.json')
    report=f'''# H5: regional cog capacity and simultaneous anchors — 2026-10-25

**Thirty-five independently certified regional occupancy limits now prevent
overcrowding of placement regions. A stronger necessary model also places all
six cog anchors simultaneously. Its resulting assignment still collides in the
actual original geometry.** Both original-coordinate checks fail; no complete
target layout is found. H2/H5 remain open at **60%** completed milestone weight.

## Whole-region capacity certificates

The same fixed57-source construction retains all nine moving originals and all
9,776 choices. Each original cog-domain integer box is considered at its exact
size and rounded outward to 1, 5, 10 and 25 mm. For each box, all domains wholly
contained in it form an occupancy group across all six mandatory cog copies.

A box's integer coordinates are partitioned into consecutive x/y bins. Every
cell's full diagonal must be shorter than the previously exact-rational proved
258.082 mm original cog/cog collision-disk separation. A cell holds at most one
cog, so its cover bounds the group's total occupancy. This uses whole regions
and exact integer inequalities, not sample positions or substituted cog hulls.

Construction certifies **1,215 boxes** in **{build['seconds']:.6f} seconds**.
Equal-domain-set deduplication and explicit superset dominance reduce them to
**35 constraints: 30 capacity-one and five capacity-two**. They contain 1,850
domain memberships and 11,100 physical selector uses across the six copies.
The prior assignment's five cogs in one narrow long region violate its new
capacity-two bound.

The independent **{audit['seconds']:.6f}-second** audit reconstructs all rounded
boxes and contained-domain sets, explicitly builds complete disjoint integer
bin intervals, checks **1,249 cell diagonals**, and verifies all **1,215** dominance
witnesses. Every original domain remains available; each group constrains only
the number of selected cog domains inside its certified box.

## First shared-budget pipeline

The full refined domain table, global three-region exclusion, 480 additional
second-sheet pair clauses, global second-sheet capacity of two and all 35
regional capacities remain together. The independently reconstructed master has
**13,238 variables / 8,490 constraints**. It finds a necessary assignment in
7.761160 seconds, which passes every capacity and selected-domain check.

The full selected original-coordinate model has **2,346 variables / 2,440
constraints**, including all 651 forbidden pieces, 575 exactly proved already
separated pieces, 76 remaining complete disjunctions and 36 inward halfplanes.
It returns **INFEASIBLE in 0.024988 seconds** for that selected combination only.
Construction, independent model audits, both calls and selected-domain checking
share one declared60-second allowance and finish in **{first['elapsed_seconds']:.6f} seconds**.

## Simultaneous-cog necessary geometry

The second pipeline binds **12 cog anchor coordinates** to all **16,170** physical
inward halfplanes for their selected original domains. It additionally requires
each same-sheet cog pair to separate outside a strict inner32-gon of the verified
original no-fit disk. All32 integer vertices are strictly inside the disk; exact
cross products verify convexity and every edge, including **1,024** vertex/edge
checks. The pair disjunction has480 directions and30 sheet-gating clauses, whose
complete truth tables are checked. The polygon is a necessary relaxation only.

Every inherited and added constraint is independently reconstructed. The resulting
**13,730-variable / 25,170-constraint** master finds an assignment in
**{master['seconds']:.6f} seconds**. Independent exact checks verify all six reported
anchors against their selected inward planes and stock bounds, and every one of
the seven same-sheet pair separations against the necessary inner polygon.

The full original-coordinate model then checks the selected domains using all
755 original forbidden pieces. Exact interval filtering leaves95 complete
disjunctions and31 inward planes, giving **2,645 variables / 2,753 constraints**.
It returns **INFEASIBLE in 0.716578 seconds**. This second complete pipeline uses
**{second['elapsed_seconds']:.6f} seconds** of its separate shared60-second allowance.
Both pipelines make exactly one master and one coordinate call, with each call
receiving only the remaining time; all completed calls remain closed.

A follow-up diagnosis checks the necessary cog coordinates against the complete
original cog/cog obstacle. **Four of seven same-sheet pairs collide**, both in
the raw original shapes and guarded geometry; the corresponding exact original
separation inequalities also fail. Thus the inner disk leaves a real obstruction,
not just a formatting or numerical issue. This six-anchor witness is not a
complete66-part proposal and is not submitted for native acceptance.

Next strengthen the simultaneous cog geometry using the complete original
cog/cog obstacle: **61 convex pieces and2,720 separating edges per pair**, while
retaining the domain exclusions, all occupancy constraints, original counts and
area limits. Independently audit any conditional/bounds reductions before a
separately bounded search. Only a fully validated original66-part target could
advance to native validation, production integration and the unchanged H5 matrix.

## New main documentation preserved

Remote main advanced to **61359456**, adding the scrap/offcut example page and
associated assets. Its 15 changed files are all under `web/public/`; there is
no source, test, dependency or workflow change. The examples distinguish a
31-of32 fill-area result from an8-of8 traced-render result and identify their
source build and limits. These documentation examples do not qualify H5.

Merge **da4ced0f** preserves all **15 remote files and73 local evidence files**
byte-for-byte. Both prior heads remain ancestors. Production digest and all three
accurate READMEs are unchanged. No new release or registry publication is made;
preview v0.2.0-alpha.1 and stable Latest v0.1.0 remain in place.

The older [CI40240715636](https://github.com/skulitom/Nestbolt/actions/runs/40240715636)
finished **cancelled after five passes**; its Windows check did not pass.
The workflow cancels superseded runs for the same branch. New main's
[CI40242602102]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful jobs
in the saved snapshot. This evidence and merge are not yet pushed, preserving
the current main run while it finishes. H2's gate and22 reserved vectors remain
unchanged under Artem's decision.

Evidence: [capacity audit]({NAME}/capacity-audit.json),
[certified groups]({NAME}/capacities.json),
[inner-polygon audit]({NAME}/inner-disk-audit.json),
[shared-budget audit]({NAME}/search-audit.json),
[original collision diagnosis]({NAME}/original-cog-pairs.json),
[merge receipt]({NAME}/main-merge-receipt.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']}** canonical files and
**{archive['verified_aliases']}** identical-content aliases retain exact bytes with
CRC/SHA verification, including each certificate, matrix, model, parameter,
failed result, source input and remote-reconciliation capture.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 regional cog capacity and simultaneous anchors, 2026-10-25:**
[The evidence]({link}) certifies 1,215 whole integer boxes and independently
checks every membership, cell diagonal and dominance witness. Thirty-five
retained bounds (30 capacity-one, five capacity-two) count all six cogs and
eliminate the prior five-in-one-region assignment. A first master/coordinate
pipeline finishes within 11.416324 seconds of a shared60-second allowance; its
selected original-coordinate model is INFEASIBLE. A second pipeline adds all
six simultaneous cog anchors and a certified strict inner32-gon of the original
collision disk, finishing in43.440899 seconds. Its necessary assignment still
has four actual original cog collisions, and the full selected-coordinate model
is INFEASIBLE. Next strengthen simultaneous geometry with the complete original
cog obstacle (61 pieces/2,720 edges), retaining all counts, guards and material
limits. Both bounded pipelines stay closed; no full target or native acceptance
is claimed. Main's new15-file scrap/offcut documentation change is merged as
da4ced0f, preserving all15 remote and73 local evidence files byte-exact. The older
CI was cancelled after five passes; new main CI40242602102 is independently
tracked. Production and accurate READMEs are unchanged. H2/H5 remain open at60%.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'source_head':head,'main_head':mainhead,'new_main_ci_status':ci['status'],'new_main_ci_successful_jobs':success,'production_digest':source_digest()},flush=True)
if __name__=='__main__':main()
