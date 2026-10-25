"""Preserve the guided search, exact selected-domain proof and repository checks."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-six-cog-guided-search-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025';CONVEX=ROOT/'output/h5-convex-domain-conflicts-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    model=load(BASE/'shared-search/solve/model-audit.json');master=load(BASE/'shared-search/solve/result.json');anchor=load(BASE/'shared-search/anchor-solve/result.json')
    timing=load(BASE/'search-audit/checks.json');proof=load(BASE/'conflict-proof-audit-completed/checks.json');tree=load(BASE/'selected-clause-tree/result.json')
    assert all(r['passed'] for r in [model,timing,proof]) and master['status']=='OPTIMAL' and anchor['status']=='INFEASIBLE'
    assert model['hints']==79 and model['conditional_selected_domain_axis_bounds']==9204 and timing['shared_budget_honored']
    assert proof['complete_selected_combination_exclusion'] and proof['tree_budget_honored'] and tree['complete_contradiction_tree']
    prior=load(ROOT/'benchmarks/results/h5-guarded-cell-search-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('372f25c6') and mainhead=='613594568fb49a71abf0248aec218a6b12f63319'
    ci=json.loads(subprocess.check_output(['gh','run','view','40242602102','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==mainhead and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
    write(BASE/'main-ci-terminal.json',ci)
    releases=json.loads(subprocess.check_output(['gh','release','list','--repo','skulitom/Nestbolt','--limit','3','--json','tagName,isLatest,isPrerelease,isDraft,publishedAt'],cwd=ROOT));write(BASE/'releases-snapshot.json',releases)
    assert next(r for r in releases if r['isLatest'])['tagName']=='v0.1.0' and next(r for r in releases if r['tagName']=='v0.2.0-alpha.1')['isPrerelease']
    action=('Keep both completed solver calls and the independent proof tree closed. The guided master now finds a candidate in 11.009201 seconds, but its full original-coordinate follow-up rejects the selected nine domains. '
        'All 1,316 proof-tree nodes, 4,851 events, 415 complete source-clause branches and 901 contradictory leaves are independently replayed. Only this exact selection is excluded; the fixed-source domain model and unrestricted packing are not declared impossible. '
        'The next structural improvement should put the two bracket anchors and insert anchor into the same full guarded model as the six cog anchors, retaining all original allowed domains, profile options, counts, area limits and native guards. '
        'Prepare compact guarded displacement representations for the remaining original profile pairs and independently prove whole-cell safety before a new bounded full search. Reuse the certified selection exclusion where applicable. '
        'Do not blindly rerun the hinted master, freeze the six-cog partial placement, waive any original, or treat these offline diagnostics as a production-budget pass. Any complete positive still needs all 66 original geometry checks, native validation, production integration and the original 13-job/two-kerf H5 matrix. '
        'Main 61359456 now has all six successful CI jobs. Preserve newer remote work, then push the saved checkpoints normally. H2 remains open under Artem\'s original-gate decision; all 22 reserved vectors remain untouched. No new release is qualified.')
    OUT.mkdir()
    copies={'shared-search/plan.json':'pipeline-plan.json','shared-search/budget.json':'shared-budget.json','shared-search/result.json':'pipeline-result.json',
        'shared-search/solve/model-audit.json':'master-model-audit.json','shared-search/solve/result.json':'master-result.json','shared-search/solve/selection.json':'selection.json',
        'shared-search/solve/necessary-cog-positions.json':'cog-positions.json','shared-search/selection-audit/checks.json':'selection-audit.json',
        'shared-search/selection-audit/full-guarded-cog-check.json':'full-guarded-cog-check.json','shared-search/anchor-solve/model-audit.json':'anchor-model-audit.json',
        'shared-search/anchor-solve/result.json':'anchor-result.json','search-audit/checks.json':'search-audit.json','selected-conflict-proofs/result.json':'interval-result.json',
        'selected-conflict-proofs/summary.json':'interval-summary.json','selected-clause-tree/plan.json':'clause-tree-plan.json','selected-clause-tree/result.json':'clause-tree-result.json',
        'conflict-proof-audit-completed/checks.json':'conflict-proof-audit.json','conflict-proof-audit-completed/certified-selected-combination-exclusion.json':'certified-selection-exclusion.json',
        'conflict-proof-audit/failure-record.json':'early-readback-failure.json','main-ci-terminal.json':'main-ci-terminal.json','releases-snapshot.json':'releases-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    correction={'source':'pipeline-plan.json method first sentence','preserved_phrase':'all66 originals movable/mandatory','correction':'All 66 originals remain mandatory; exactly nine are movable and 57 retain their verified source placements. The model fields, independent oracle and every subsequent scope statement use this actual scope.','raw_plan_unchanged':True,'model_change':False}
    write(OUT/'plan-wording-correction.json',correction)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],
        'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'full_master_solver_calls':1,'full_anchor_solver_calls':1,'proof_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
        'original_counts_material_gate_and_native_guards_unchanged':True,'pushed':False,'current_main_ci_id':40242602102,'current_main_ci_status':'completed','current_main_ci_conclusion':'success','current_main_successful_jobs':6,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        plan=load(p)
        for n,h in plan.get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
        for field,folder in [('query_hashes',SOURCE/'queries'),('mutual_hashes',SOURCE/'mutual'),('group_hashes',CONVEX/'groups')]:
            for i,h in plan.get(field,{}).items():
                q=folder/f'{int(i):03d}.json';assert digest(q)==h;members['source-inputs/'+q.relative_to(ROOT).as_posix()]=q
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for previous,names in [('h5-cog-displacement-cells-20261025',['coarse-refinement/selected-query-18.json','coarse-refinement/selected-query-19.json','audit/checks.json']),
        ('h5-guarded-cell-search-20261025',['first-sheet-four-cog-diagnostic/audit/six-cog-positions.json','first-sheet-four-cog-diagnostic/audit/checks.json','six-cog-geometry-audit/checks.json','remaining-three-candidates/audit/checks.json'])]:
        manifestpath=ROOT/'benchmarks/results'/previous/'raw-manifest.json';old=load(manifestpath);known={r['path']:r['sha256'] for r in old['files']+old['aliases']}
        for n in names:
            p=ROOT/'output'/previous/n;assert digest(p)==known[previous+'/'+n]
        members['source-inputs/'+manifestpath.relative_to(ROOT).as_posix()]=manifestpath
    names=['prepare_h5_six_cog_guided_search.py','audit_h5_six_cog_guided_master.py','solve_h5_six_cog_guided_master.py','audit_h5_six_cog_guided_selection.py','solve_h5_six_cog_guided_anchors.py','run_h5_six_cog_guided_search.py','audit_h5_six_cog_guided_search.py',
        'prove_h5_guided_selection_conflicts.py','h5_guided_conflict_oracle.py','prove_h5_guided_clause_tree.py','audit_h5_guided_conflict_proofs.py','prepare_h5_guided_completed_audit.py','audit_h5_guided_completed_conflict_proofs.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'master_and_anchor_models_independently_verified':True,'all_solver_and_proof_budgets_honored':True,'selected_combination_exclusion_independently_replayed':True,
        'early_readback_failure_and_separate_completed_audit_preserved':True,'plan_scope_wording_corrected_without_mutating_raw_record':True,'production_and_readmes_unchanged':True,
        'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: guided candidate and exact selected-domain rejection — 2026-10-25

**The verified six-cog hints let the full domain master find a candidate in
{master['seconds']:.6f}s. The original-coordinate follow-up rejects that selected
combination; a separate exact proof independently certifies the rejection.**
No complete target layout is found. H2/H5 remain open at **60%**.

## Closed guided search

All 66 original parts remain mandatory: nine movable and 57 fixed at their
verified source placements. Every one of the 9,776 domain choices, both original
area limits, all existing exclusions and the full guarded cog cells remain.
The new model adds **9,204 exact conditional domain box bounds** and **79
advisory values** from the previously verified six-cog construction. The hints
fix no placements. Independent reconstruction checks **16,775 variables /
55,587 constraints**, every hint membership and every selected cell condition.
Construction takes **{model['construction_seconds']:.6f}s** and model audit
**{model['audit_seconds']:.6f}s**.

The single 45-second-cap, eight-worker, seed-zero call returns a candidate
(`OPTIMAL` is the satisfaction-solver status). Both brackets select query 0,
domain row 190; the insert selects query 17, row 0. The six cogs retain the hinted
domain rows 3, 31, 72, 734 on the first sheet and 1, 1 on the second. Independent
selection checks confirm all nine identities, original area charges, existing
pair exclusions, regional capacities, and all 427 full guarded cog clauses.
These necessary checks do not prove the remaining parts can be placed.

The full selected-coordinate model contains **2,255 variables / 2,341
constraints**, with all 18 same-sheet pairs and 712 original forbidden faces.
Only exact complete-box proofs remove always-separated faces or impossible
directions. Its sole call returns **INFEASIBLE in {anchor['seconds']:.6f}s**.
The complete three-stage pipeline takes **{timing['actual_shared_seconds']:.6f}s**,
within the shared 60-second limit; neither call exceeds its own cap. Both calls
are closed. No native validator or quality run is opened on the rejected candidate.

The raw runner plan's phrase `all66 originals movable/mandatory` is imprecise:
the actual model has nine movable and 57 fixed originals, all mandatory.
[The explicit wording correction]({NAME}/plan-wording-correction.json) preserves
the original record; it changes no model, result or scope.

## Exact rejection proof

A separate interval diagnosis checks all 18 same-sheet pairs and the complete
nine-domain selection. All **19 traces reach fixed points**, with **1,104
integer bound deductions** and no contradiction. Exact rational replay checks
every deduction and confirms no further unit-clause or inward-bound deduction
is available. A fixed point is not a feasible placement.

A new bounded proof tree therefore branches on unresolved original separation
clauses. Every branch includes **all remaining possible source edges**; each
child enforces one edge's original inequality. Children may overlap, but their
union covers all possible solutions of their parent. Every original part and
domain stays in scope. The tree completes in **{tree['seconds']:.6f}s**, inside its
separate 60-second proof budget, with **1,316 nodes, 415 branch nodes, 901
contradictory leaves and 4,851 events**. There are no pending or open leaves.
This proof procedure invokes no solver and does not extend the completed search.

Independent rational read-back takes **{proof['seconds']:.6f}s** and reconstructs
source rules, verifies every bound update and unit clause, checks inherited
assumptions, and proves complete coverage of all branches with no orphan node.
The [certified exclusion]({NAME}/certified-selection-exclusion.json) applies only
to **these nine selected inward domains with their original source angles,
fixed 57 placements and guarded clauses**. It does not exclude other domains,
other placements or unrestricted packing.

An early read-back started before the proof process wrote its terminal files
and failed with `FileNotFoundError`. Its script, plan and failure record remain
preserved. The separate completed read-back ran after the original process
exited. No proof or solver call was restarted and no failed record overwritten.

## Next structural step and repository state

The remaining bracket/insert coordinates need to participate in the same
guarded placement search as the cog coordinates. Prepare compact guarded
displacement representations for the remaining original profile pairs, prove
whole-cell safety independently, and preserve every allowed domain and original
constraint before another bounded full search. The certified selection can be
excluded where applicable. Repeating the same hinted master is not the next step.
Any complete positive still needs all 66 original geometry checks, native
validation, production-budget integration and the original 13-job/two-kerf H5
matrix. The first-sheet cog representation's extra 0.010 mm constructive
restriction remains explicit and is not an acceptance-guard relaxation.

Main 61359456 now has **all six jobs successful** in
[CI 40242602102]({ci['url']}). Its offcut documentation is preserved. This
checkpoint is prepared for a normal push after reconciling any newer remote
changes; success of the future pushed commit's own CI is not claimed here.
Production source and all three accurate READMEs are unchanged. Preview
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged; no new release is
qualified. H2 keeps its original gate and all 22 reserved vectors untouched.

Evidence: [master audit]({NAME}/master-model-audit.json),
[search timing audit]({NAME}/search-audit.json),
[proof audit]({NAME}/conflict-proof-audit.json),
[source review]({NAME}/source-review.json), [archive]({NAME}/raw-001.zip), and
[manifest]({NAME}/raw-manifest.json). The archive preserves **{archive['archive_members']}
canonical files and {archive['verified_aliases']} exact-content aliases**, including
full models, parameters, logs, every proof node and source input, with verified
size, SHA-256 and CRC.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 guided search and exact selected-domain rejection, 2026-10-25:** [the evidence]({link})
records a candidate from the 16,775-variable / 55,587-constraint master in
11.009201s after adding 9,204 exact domain bounds and 79 advisory hints. All 66
originals remain mandatory (nine movable, 57 fixed). The full selected-coordinate
follow-up is INFEASIBLE in 0.225323s; total pipeline time is 15.872994s within 60s.
Nineteen interval traces reach fixed points, not feasibility. A separate exact
clause tree then certifies this selected combination's rejection: 1,316 nodes,
415 complete branches, 901 contradictory leaves and 4,851 independently replayed
events, with no open leaves. Its 56.946915s proof budget is separate from the
closed solver pipeline. Other domain combinations and unrestricted packing
remain open. The early read-back failure and separate completed audit are
preserved. Next integrate the bracket/insert coordinates with the guarded cog
search using independently proved compact representations for the remaining
original profile pairs. No target/native or production pass is claimed. All
six jobs of main CI 40242602102 now pass; checkpoints can be pushed normally
after preserving any newer remote work. Production, READMEs and releases are
unchanged. H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_successes':6},flush=True)
if __name__=='__main__':main()
