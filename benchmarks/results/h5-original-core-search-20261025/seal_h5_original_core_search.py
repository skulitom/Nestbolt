"""Preserve the closed core search and complete second-sheet pair classification."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-original-core-search-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025';CONVEX=ROOT/'output/h5-convex-domain-conflicts-20261025'
PAIR=BASE/'remaining-second-sheet-pairs'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    model=load(BASE/'shared-search/solve/model-audit.json');solved=load(BASE/'shared-search/solve/result.json');run=load(BASE/'shared-search/result.json');check=load(BASE/'search-audit/checks.json')
    pair=load(PAIR/'result.json');proof=load(PAIR/'exact-proofs/result.json');audit=load(PAIR/'audit/checks.json');geometry=load(PAIR/'geometry-audit-repaired/checks.json')
    assert all(load(p)['passed'] for p in [BASE/'audit/checks.json',BASE/'shared-search/solve/model-audit.json',BASE/'search-audit/checks.json',PAIR/'audit/checks.json',PAIR/'geometry-audit-repaired/checks.json'])
    assert solved['status']=='UNKNOWN' and not solved['has_necessary_domain_candidate'] and run['anchor_solver_calls']==0 and check['shared_budget_honored']
    assert pair['completed_pairs']==15 and pair['feasible_pairs']==5 and pair['infeasible_pairs']==10 and pair['pending_pairs']==0
    assert audit['excluded_pairs']==1019 and audit['feasible_pairs']==5 and audit['proof_nodes']==74 and audit['proof_events']==540
    prior=load(ROOT/'benchmarks/results/h5-full-cog-coordinates-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('b732530a') and mainhead=='613594568fb49a71abf0248aec218a6b12f63319'
    ci=json.loads(subprocess.check_output(['gh','run','view','40242602102','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Keep the original-core master closed: UNKNOWN with no incumbent in45.305899 seconds, shared pipeline47.844358 seconds within60. '
        'All71 original core pieces and130 new guarded pair exclusions were included; the independently reconstructed model has18530 variables and34068 constraints. '
        'The separate complete second-sheet diagnostic now classifies every one of1024 ordered q19 domain pairs:1019 excluded, five feasible. '
        'The last ten negative pairs have independent exact binary interval proofs,74 nodes/540 events, supplying150 new clauses across all15 physical cog pairs. '
        'Five two-cog witnesses pass exact full guarded inequalities and actual original polygon/fixed-obstacle/stock checks. They prove that the existing capacity2 is tight for this subproblem; they do not place the other seven moving originals. '
        'Next build a distinct full66-original staged model using the complete second-sheet classification and the150 new independently certified clauses. The verified two-cog coordinates may supply optional hints mapped to interchangeable copies, but must not fix these placements or omit any other original. '
        'Preserve complete domain choices, original area charges, fixed57 source, every regional constraint and the necessary original-core geometry. Independently reconstruct all new model fields and hint eligibility before one bounded call with the shared60-second budget, master45-second cap and2-second shutdown reserve. '
        'Only a positive passing full guarded all-original coordinate checks, original66-polygon/stock/native validation, production-budget integration and the complete13-job/two-kerf H5 matrix can advance H5. '
        'Main61359456 and its offcut page remain preserved; wait for terminal CI40242602102 before the next normal push so unfinished native checks are not cancelled. '
        'H2 remains open under Artem\'s unchanged gate, with22 reserved vectors untouched. No new release is qualified.')
    OUT.mkdir()
    copies={'plan.json':'core-plan.json','result.json':'core-preparation.json','audit/checks.json':'core-preparation-audit.json','added-pairs.json':'added-guarded-pairs.json',
        'shared-search/budget.json':'shared-budget.json','shared-search/result.json':'pipeline-result.json','shared-search/solve/model-audit.json':'model-audit.json','shared-search/solve/result.json':'solver-result.json','search-audit/checks.json':'search-audit.json',
        'remaining-second-sheet-pairs/plan.json':'pair-plan.json','remaining-second-sheet-pairs/result.json':'pair-result.json','remaining-second-sheet-pairs/summary.json':'pair-summary.json',
        'remaining-second-sheet-pairs/exact-proofs/plan.json':'proof-plan.json','remaining-second-sheet-pairs/exact-proofs/result.json':'proof-result.json','remaining-second-sheet-pairs/audit/checks.json':'pair-audit.json',
        'remaining-second-sheet-pairs/audit/certified-new-exclusions.json':'certified-new-exclusions.json','remaining-second-sheet-pairs/audit/complete-pair-classification.json':'complete-pair-classification.json',
        'remaining-second-sheet-pairs/audit/verified-pair-witnesses.json':'verified-pair-witnesses.json','remaining-second-sheet-pairs/geometry-audit/failure-record.json':'original-geometry-audit-failure.json',
        'remaining-second-sheet-pairs/geometry-audit-repaired/checks.json':'pair-geometry-audit.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],
        'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'master_solver_calls':1,'selected_full_anchor_solver_calls':0,'separate_pair_diagnostic_solver_calls':15,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
        'shared_master_budget_honored':True,'master_soft_limit_overshoot_seconds':check['solver_soft_limit_overshoot_seconds'],'original_counts_material_gate_and_native_guards_unchanged':True,
        'pushed':False,'current_main_ci_id':40242602102,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,
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
    for field,folder in [('query_hashes',SOURCE/'queries'),('group_hashes',CONVEX/'groups')]:
        for i,h in modelplan[field].items():
            p=folder/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_original_core_search_atlas.py','prepare_h5_original_core_search.py','audit_h5_added_guarded_pairs_master.py','audit_h5_original_core_master.py',
        'solve_h5_original_core_master.py','audit_h5_original_core_selection.py','solve_h5_original_core_anchors.py','run_h5_original_core_search.py','audit_h5_original_core_search.py',
        'solve_h5_remaining_second_sheet_pairs.py','prove_h5_remaining_second_sheet_pairs.py','audit_h5_remaining_second_sheet_pairs.py','audit_h5_second_sheet_pair_geometry.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'full_core_master_independently_reconstructed':True,'unknown_without_incumbent_preserved':True,'shared_budget_honored':True,'solver_soft_limit_overshoot_explicitly_preserved':True,
        'all1024_second_sheet_domain_pairs_classified':True,'all10_new_negative_trees_independently_replayed':True,'all5_two_cog_witnesses_checked_against_original_shapes_and_native_guards':True,
        'original_failed_geometry_audit_and_corrected_readback_preserved':True,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: original-core search and complete second-sheet cog pairs — 2026-10-25

**The full original-core master finishes UNKNOWN without a candidate. A separate
two-cog analysis now completely classifies the second-sheet domain pairs.** Five
combinations have verified placements; the remaining1,019 are excluded. This
strengthens the next full search but does not qualify a66-part target layout.
H2/H5 remain open at **60%**.

## Closed full original-core search

The staged master retains all nine mandatory moving originals, the fixed57,
all9,776 domain options, both original-area limits, existing conflict/occupancy
constraints and the130 new guarded exclusions from the previous checkpoint.
Those exclusions add1,950 physical clauses across all15 cog pairs. All six cog
anchors use the71 complete original collision-core pieces,352 necessary outside
directions per pair, with5,280 direction variables in total. Exact four-corner
checks cover2,816 projections. Positive core placements still require the full
guarded-coordinate model; this preliminary relaxation never changes acceptance.

The independent model reconstruction passes **18,530 variables /34,068 constraints**.
Construction takes **{model['construction_seconds']:.6f}s**, audit
**{model['audit_seconds']:.6f}s**. The only master call has a45-second soft cap,
eight workers and seed zero, inside a shared60-second pipeline with a two-second
shutdown reserve. It returns **UNKNOWN in {solved['seconds']:.6f}s**, with no
incumbent. The soft cap overshoots by **{check['solver_soft_limit_overshoot_seconds']:.6f}s**;
that overshoot is retained explicitly. Shared elapsed time is
**{run['elapsed_seconds']:.6f}s**, within60seconds. No selected-coordinate or native
follow-up is opened. The call is closed; no feasibility or impossibility follows.

## Complete second-sheet pair classification

The existing guarded table and earlier exact interval proofs leave15 of the
32×32 ordered domain pairs unresolved. Each receives a separate, independently
reconstructed two-cog model using its complete inward domains and all61 full
guarded original collision pieces. At most one two-second call per pair is
allowed, with all construction/audits/solves sharing a60-second diagnostic budget.
This is a separate subproblem, not additional time for the closed full search.

All15 calls finish in a combined **{pair['seconds']:.6f}s** including preparation:
five feasible and ten infeasible; no UNKNOWN or pending pair. The five feasible
ordered domain pairs are **[1,1], [1,12], [1,17], [12,1], [17,1]**. Independent
integer witness checks verify32 inward inequalities and305 full forbidden-piece
clauses. Thus the previously certified at-most-two capacity is attainable in
this fixed-source subproblem; an at-most-one restriction would be incorrect.

The ten solver-negative results are not used as unsupported exclusions. A
separate exact proof procedure applies integer interval deductions, then bisects
a remaining interval when propagation stalls. Every split covers its entire
parent interval. In **{proof['seconds']:.6f}s**, it produces **74 nodes,540 exact
bound events,32 binary splits and42 contradictory leaves**. Independent replay
rebuilds every source rule, verifies every rational floor/ceiling deduction and
unit clause, checks all split coverage, and visits every node without omissions.
All ten trees close. These yield **150 new clauses** across all15 physical cog
pairs, beyond the exclusions already included in the closed master.

Together, the earlier certificates, ten new proof trees and five positive
witnesses classify **all1,024 pairs:1,019 excluded and five feasible**. Negative
scope remains the declared source-angle, inward-domain, guarded integer
construction. No unrestricted packing impossibility is claimed.

## Original-shape and clearance read-back

Each positive pair is rebuilt from the original80-vertex cog polygon and source
rotation, then checked against the unchanged fixed obstacles and stock. All
**75 same-sheet pair checks** and **40 moving stock-edge checks** pass.
The minimum original separation is **{geometry['minimum_original_gap_mm']:.12f}mm**,
above the native requirement **{geometry['native_pair_guard_mm']:.12f}mm**.
The minimum extra stock margin is **{geometry['minimum_extra_stock_margin_mm']:.12f}mm**,
above the native guard **{geometry['native_stock_guard_mm']:.12f}mm**.
Maximum profile reconstruction error is **{geometry['maximum_original_profile_reconstruction_error_mm']:.3g}mm**.
Every mutual offset also lies outside the full raw and guarded no-fit regions.

The first geometry audit stopped with `KeyError: 'item'` while recording an
original identity; source metadata uses `index`. Its original script, plan and
observed failure are preserved. Correcting that output-field lookup in a separate
audit directory completes the read-back; no witness, guard or solver record changes.

These witnesses contain **only two moving originals against the fixed57**.
The other seven moving originals remain required. No partial layout is presented
as a full target, and no native validator is called on it.

## Next search and repository state

Use the complete second-sheet classification and150 new certified clauses in a
distinct full66-original staged model. The verified pair coordinates may provide
optional hints for interchangeable copies; they must not fix those placements
or remove other mandatory parts. Retain the shared60-second budget,45-second
master cap, shutdown reserve, original material target and all validation gates.
Any positive still needs the full guarded-coordinate and66-original/native
checks, production-budget integration and unchanged13-job/two-kerf H5 matrix.

Main61359456 and the offcut documentation remain preserved. Its own
[CI40242602102]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful jobs
at the saved snapshot; unfinished checks are not counted as passes. This
checkpoint is local. A normal push should follow terminal CI, preserving any
newer remote work and avoiding cancellation of unfinished native checks.

Production source and all three accurate READMEs are unchanged. Preview
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged; no release is qualified.
No native packing, quality run or reserved H2 vector evaluation is performed.
Artem's unchanged H2 gate remains in force, with22 reserved vectors untouched.

Evidence: [full search audit]({NAME}/search-audit.json),
[pair/model/proof audit]({NAME}/pair-audit.json),
[complete classification]({NAME}/complete-pair-classification.json),
[original-geometry audit]({NAME}/pair-geometry-audit.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
The archive preserves **{archive['archive_members']}** canonical files and
**{archive['verified_aliases']}** exact-content aliases, including original inputs,
models, actual parameters, logs, witnesses, full proof trees and failed audit.
Every stored byte length, SHA-256 and ZIP CRC is verified.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 original-core search and complete second-sheet cog pairs, 2026-10-25:**
[The evidence]({link}) preserves a full18,530-variable/34,068-constraint original-core
master UNKNOWN with no incumbent. Its single45-second call takes45.305899s;
the soft-limit overshoot is explicit, while shared47.844358s stays within60s.
No full-coordinate or native follow-up is opened. A separate bounded diagnostic
resolves all15 remaining second-sheet pairs. Five have original-shape witnesses;
ten receive independent exact proofs covering74 nodes/540 events/32 splits.
Together with prior certificates, all1,024 pairs are classified:1,019 excluded,
five feasible. All75 original pair and40 stock-edge checks pass for those five
two-cog witnesses, but seven other moving originals are absent and still required.
The first geometry audit's metadata lookup failure is preserved alongside its
corrected read-back. The ten proofs provide150 new physical pair clauses for
the next full66-original search; verified coordinates may guide optional hints.
Production source, READMEs, material/native limits and releases are unchanged.
H2/H5 remain open at60%, with all22 reserved H2 vectors untouched. Main's own
CI40242602102 remains tracked before the next normal push.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success,'production_digest':source_digest()},flush=True)
if __name__=='__main__':main()
