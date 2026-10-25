"""Seal complete guarded cog search, exact pair refinements and a smaller core."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-full-cog-coordinates-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME;SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025'
CONVEX=ROOT/'output/h5-convex-domain-conflicts-20261025';REGIONAL=ROOT/'output/h5-cog-region-capacities-20261025';OLD=ROOT/'output/h5-original-domain-conflicts-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    preparation=load(BASE/'result.json');model=load(BASE/'shared-search/solve/model-audit.json');solved=load(BASE/'shared-search/solve/result.json');run=load(BASE/'shared-search/result.json');runcheck=load(BASE/'search-audit/checks.json')
    pairs=load(BASE/'guarded-cog-pairs/result.json');paircheck=load(BASE/'guarded-cog-pairs/audit/checks.json');overlap=load(BASE/'guarded-cog-pairs/prior-interval-overlap.json');core=load(BASE/'original-core-relaxation/result.json');corecheck=load(BASE/'original-core-relaxation/audit/checks.json')
    assert all(load(p)['passed'] for p in [BASE/'audit/checks.json',BASE/'shared-search/solve/model-audit.json',BASE/'search-audit/checks.json',BASE/'guarded-cog-pairs/audit/checks.json',BASE/'original-core-relaxation/audit/checks.json'])
    assert solved['status']=='UNKNOWN' and run['master_solver_calls']==1 and run['anchor_solver_calls']==0 and not runcheck['shared_budget_honored']
    assert pairs['tested_pairs']==200309 and pairs['new_guarded_conflicts']==146 and not pairs['pending_cases'] and overlap['all15_physical_cog_pair_uses']==1950
    assert core['original_core_convex_pieces']==71 and core['necessary_outside_edges']==352 and core['whole_union_equals_complete_original_core']
    prior=load(ROOT/'benchmarks/results/h5-cog-region-capacities-20261025/source-review.json');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('dff5c278') and mainhead=='613594568fb49a71abf0248aec218a6b12f63319'
    ci=json.loads(subprocess.check_output(['gh','run','view','40242602102','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Keep the complete guarded-cog shared search closed: it returned UNKNOWN without an incumbent; actual60.870843 seconds exceeds its declared60-second budget by0.870843 seconds, and the solver itself overshot its remaining limit by0.911765 seconds. '
        'All61 guarded cog pieces remain represented through exact bounds reduction to59 pieces/2636 directions per pair, but the52790-variable/66018-constraint model did not find a candidate. '
        'The complete guarded pair refinement now scans all200309 previously unmarked cog pairs and independently certifies146 extra raw-table exclusions. Sixteen second-sheet exclusions were already covered by the32 exact interval proofs; only130 ordered pairs are new to the prior master, giving1950 physical pair clauses across all15 cog pairs. '
        'A cheaper original-outline necessary relaxation is now fully prepared and independently audited: the complete committed raw-original collision core decomposes into71 convex pieces with352 edges, at most5280 physical directions. All pieces lie strictly inside the actual original cog collision region, preserving every tooth/concavity rather than replacing cogs with a hull or disk. '
        'Its edge rounding is intentionally necessary: floor(exact bound minus coefficient error), not the previous constructive ceil(bound plus error). It permits all truly outside original pairs within the signed coordinate bounds; a positive does NOT prove positive-clearance validity. '
        'Next build a distinct shared-budget staged model using all current domain/area/occupancy constraints, the130 new nonduplicate guarded pair exclusions, simultaneous cog anchors and this complete original-outline core relaxation. Audit every new protobuf field and rounding/conditional implication before one bounded call. '
        'Reserve explicit wall-clock margin for solver soft-limit overshoot instead of treating the just-recorded overrun as success. Do not extend or retry the completed full-guard run. '
        'Independently check any core-anchor witness, then solve the selected FULL guarded original-coordinate model; only all66 original polygon/stock/native validation may qualify a target. No clearance/native/material limit may be weakened in acceptance, production integration or the full13-job/two-kerf H5 matrix. '
        'Main61359456 and its scrap/offcut page remain preserved; track CI40242602102 independently before the next normal push. H2 remains open under Artem\'s unchanged gate, with all22 reserved vectors untouched. No new release is qualified.')
    OUT.mkdir();copies={'plan.json':'original-cog-plan.json','result.json':'original-cog-preparation.json','audit/checks.json':'original-cog-preparation-audit.json',
        'shared-search/budget.json':'shared-budget.json','shared-search/result.json':'pipeline-result.json','shared-search/solve/model-audit.json':'model-audit.json','shared-search/solve/result.json':'solver-result.json','search-audit/checks.json':'search-audit.json',
        'guarded-cog-pairs/plan.json':'guarded-pair-plan.json','guarded-cog-pairs/result.json':'guarded-pair-result.json','guarded-cog-pairs/audit/checks.json':'guarded-pair-audit.json','guarded-cog-pairs/audit/cases.json':'guarded-pair-cases.json',
        'guarded-cog-pairs/prior-interval-overlap.json':'guarded-pair-overlap.json','original-core-relaxation/plan.json':'core-relaxation-plan.json','original-core-relaxation/result.json':'core-relaxation-result.json',
        'original-core-relaxation/audit/checks.json':'core-relaxation-audit.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
        'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'master_solver_calls':1,'selected_anchor_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'shared_budget_honored':False,'shared_budget_overrun_seconds':runcheck['shared_overrun_seconds'],
        'original_counts_material_gate_and_native_guards_unchanged':True,'pushed':False,'current_main_ci_id':40242602102,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for key in ['inputs','input_hashes']:
            for n,h in load(p).get(key,{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    modelplan=load(BASE/'shared-search/solve/plan.json')
    for i,h in modelplan['query_hashes'].items():
        p=SOURCE/'queries'/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for i,h in modelplan['group_hashes'].items():
        p=CONVEX/'groups'/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for folder in [OLD/'three-cog-certificate',CONVEX/'second-sheet-pair-proofs/audit',REGIONAL/'audit']:
        for p in folder.rglob('*'):
            if p.is_file():members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_full_cog_constraints.py','prepare_h5_full_cog_search.py','audit_h5_full_cog_master.py','solve_h5_full_cog_master.py','audit_h5_full_cog_selection.py','solve_h5_full_cog_anchors.py','run_h5_full_cog_search.py',
        'audit_h5_full_cog_search.py','build_h5_guarded_cog_pairs.py','audit_h5_guarded_cog_pairs.py','check_h5_guarded_pair_overlap.py','prepare_h5_original_cog_core_relaxation.py','audit_h5_original_cog_core_relaxation.py',
        'solve_h5_cog_coordinate_master.py','audit_h5_cog_coordinate_selection.py','solve_h5_cog_coordinate_anchors.py','run_h5_cog_coordinate_search.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'all61_original_cog_pieces_accounted_for':True,'full_cog_protobuf_independently_reconstructed':True,'unknown_without_incumbent_preserved':True,
        'shared_and_solver_soft_limit_overruns_explicitly_retained':True,'all200309_guarded_pair_refinements_complete':True,'all146_added_raw_table_conflicts_independently_verified':True,
        'sixteen_prior_pair_exclusions_not_double_counted':True,'all71_original_core_pieces_and352_necessary_inequalities_audited':True,'core_relaxation_positive_not_claimed_valid':True,
        'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: full cog geometry and a smaller original-outline model — 2026-10-25

**The complete guarded cog model finishes UNKNOWN without a candidate. The
recorded run exceeds its declared time allowance.** A separate complete pair
check certifies more exclusions, and an independently audited representation
of the original collision core prepares a substantially smaller necessary
model. H2/H5 remain open at **60%**; no complete target layout is found.

## Complete guarded original-cog search

All previous domain choices, nine moving originals, fixed57 source, area limits,
whole-domain exclusions and occupancy limits remain present. Every one of the
six cog anchors is bound to its selected original domain. The full original
cog/cog collision region has **61 convex pieces / 2,720 outside directions**.

Exact integer projection bounds over both complete same-sheet anchor ranges
prove two pieces already separated. The remaining **59 complete disjunctions**
retain **2,636 directions per physical pair**. Independent four-corner extrema
checks cover **21,760 projections**. Forty-eight explicit query-box constraints
make the bound reductions directly implied by the model.

The independently reconstructed model has **52,790 variables / 66,018 constraints**,
including **39,540 original-cog direction variables**, **1,770 sheet-gated piece
clauses**, and all **16,170** conditional inward cog-domain halfplanes. Construction
takes **{model['construction_seconds']:.6f} seconds**, the full model audit
**{model['audit_seconds']:.6f} seconds**.

Its only call receives **{runcheck['declared_solver_seconds']:.6f} seconds** remaining
from the declared shared60-second allowance, with eight workers and seed zero.
It returns **UNKNOWN without an incumbent in {solved['seconds']:.6f} seconds**.
Actual end-to-end elapsed time is **{run['elapsed_seconds']:.6f} seconds**:
the shared allowance overruns by **{runcheck['shared_overrun_seconds']:.6f} seconds**,
and the solver's soft limit by **{runcheck['solver_soft_limit_overshoot_seconds']:.6f} seconds**.
The audit records both overruns explicitly; neither is counted as a budget pass.
No selected-domain, coordinate or native follow-up call is opened. The run stays
closed and establishes neither feasibility nor impossibility.

## Complete guarded cog-pair refinement

The existing raw-original tables leave **200,309** pairs unmarked across the
735 first-sheet and32 second-sheet domains. A separate bounded geometric pass
checks every pair using the complete convex difference of its actual inward
faces, padded outward by0.00001 mm. A new exclusion requires that whole hull
strictly inside a0.0001 mm inset of the full guarded original collision region.
The whole core is covered by the original model's61 forbidden pieces.

The check finishes in **{pairs['seconds']:.6f} seconds**, with no pending pairs:
**126** additional first-sheet and **20** second-sheet raw-table exclusions.
The independent audit reconstructs exact-rational outward nanometre vertex boxes,
checks all146 complete difference enclosures, all2,695 source vertices, every
old bit, domain order, packed hash/length/padding and whole guarded-core coverage.

Sixteen of the20 second-sheet pairs were already excluded by earlier exact
interval proofs. Therefore **130 ordered pairs are new to the prior master**,
giving **1,950** physical pair clauses across all15 cog pairs. They are not
double-counted. These are restrictions of the declared guarded construction;
an unmarked pair remains unproved, and no global packing impossibility is claimed.

## Smaller complete original collision-core representation

The large model's directions mostly come from the finely polygonized clearance
envelope. The next prepared necessary model uses the complete previously certified
raw-original collision core instead of a circular or convex-hull substitute.
It retains the original source-angle tooth geometry and concavities.

That core decomposes into **71 convex pieces with352 outside edges**. Their union
equals the entire committed core; every whole piece lies strictly inside the
actual original cog/cog collision polygon, with minimum boundary margin
**{core['minimum_original_boundary_margin_mm']:.12f} mm**. This needs at most
**5,280 physical directions**, versus39,540 in the guarded model.

The rounding is intentionally **necessary**, with exact coefficient-error bounds:
`integer_bound = floor(exact_edge_bound - coefficient_error)`. For any true
outside point, the rounded projection remains at least this bound. This differs
from the stricter constructive rounding used by final guarded separation.
Independent read-back checks verify all71 pieces, all352 inequalities and3,024
exact rational convexity relations, full core equality and strict raw containment.

This is ready for a distinct, independently audited staged model, retaining all
original counts, area/occupancy constraints and the130 new pair exclusions.
It is a necessary search relaxation: **a positive still requires the complete
guarded original-coordinate model, all66 original polygon/stock checks and native
validation**. Moving-pair clearance is omitted only from this preliminary core
test, never from acceptance, production-budget integration or the unchanged
13-job/two-kerf H5 matrix. The new model has not been run in this checkpoint.
Future shared-budget calls should reserve explicit margin for solver overshoot.

## Repository and evidence

Main61359456 and its scrap/offcut documentation remain preserved in the local
merge. Its own [CI40242602102]({ci['url']}) is **{ci['status']}**, with **{success}/6** jobs
successful in the saved snapshot. No result is inferred for unfinished jobs.
Production source and all three accurate READMEs are unchanged. Preview release
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged; no release is qualified.
No native packing, quality or held-out evaluation is run. All22 reserved H2
vectors remain untouched under Artem's unchanged-gate decision.

Evidence: [complete model audit]({NAME}/model-audit.json),
[terminal result and budget audit]({NAME}/search-audit.json),
[guarded pair audit]({NAME}/guarded-pair-audit.json),
[overlap accounting]({NAME}/guarded-pair-overlap.json),
[original-core audit]({NAME}/core-relaxation-audit.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
The archive retains **{archive['archive_members']}** canonical files and
**{archive['verified_aliases']}** identical-content aliases with exact length,
SHA-256 and CRC verification, including complete sources, models, parameters,
logs, pair matrices, negative/non-proof results and all new certificate pieces.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 complete guarded cog model and original-outline core, 2026-10-25:**
[The evidence]({link}) independently reconstructs a52,790-variable/66,018-constraint
model with all original cog collision pieces and existing domain/occupancy limits.
Its single call returns UNKNOWN without an incumbent. Shared elapsed60.870843s
exceeds the declared60s by0.870843s; the solver soft-limit overshoot is also
preserved, with no budget-pass claim, retry or follow-up coordinate call.
All200,309 remaining cog-domain pairs receive complete guarded-region checks:
146 raw-table exclusions are independently verified;16 overlap earlier proofs,
so130 ordered pairs (1,950 physical clauses) are newly available to the master.
A separately prepared complete original-outline collision core has71 convex
pieces and352 necessarily rounded edges, reducing the direction upper bound
from39,540 to5,280 while retaining tooth geometry. Its full union, strict raw
containment and exact necessary rounding are independently audited. Next use
this smaller preliminary model with the new pair exclusions; every positive
still needs full guarded-original, native and H5 validation. Main CI40242602102
is independently tracked; source, accurate READMEs, releases and all acceptance
limits are unchanged. H2/H5 remain open at60%; no reserved vectors are evaluated.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success,'production_digest':source_digest()},flush=True)
if __name__=='__main__':main()
