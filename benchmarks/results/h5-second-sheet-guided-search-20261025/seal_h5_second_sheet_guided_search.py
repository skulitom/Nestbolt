"""Archive the closed guided original-core master without a feasibility claim."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-second-sheet-guided-search-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025';CONVEX=ROOT/'output/h5-convex-domain-conflicts-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    model=load(BASE/'shared-search/solve/model-audit.json');solved=load(BASE/'shared-search/solve/result.json');run=load(BASE/'shared-search/result.json');check=load(BASE/'search-audit/checks.json')
    assert model['passed'] and check['passed'] and check['shared_budget_honored'] and solved['status']=='UNKNOWN' and not solved['has_necessary_domain_candidate']
    assert model['hints']==14 and model['new_exact_second_sheet_pair_clauses']==150 and run['master_solver_calls']==1 and run['anchor_solver_calls']==0
    prior=load(ROOT/'benchmarks/results/h5-original-core-search-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('0c635b24') and mainhead=='613594568fb49a71abf0248aec218a6b12f63319'
    ci=json.loads(subprocess.check_output(['gh','run','view','40242602102','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Keep this guided master closed: UNKNOWN without an incumbent, actual solver45.537740 seconds and shared pipeline47.986694 seconds. '
        'The exact model audit includes all150 new physical clauses from the ten certified second-sheet exclusions and fourteen advisory values for copies7/8 from the verified [1,1] two-cog witness. Hints add no constraint and omit no original. '
        'Further unchanged-domain retries or seed changes are not the next step. Investigate a different representation of simultaneous cog separation: bounded collision-free displacement regions decomposed into convex allowed cells, rather than one disjunction for each forbidden core piece. '
        'First measure and preserve the whole original guarded complement within the exact same-sheet difference boxes. Retain every raw face and any explicitly discarded inset/grid face. Independently verify exact convexity, coordinate bounds and coefficient-error rounding, and prove that each retained allowed cell implies the complete original guarded source inequalities before using it. '
        'Any approximation or uncovered boundary remains explicit and limits negative scope; no hull/disk surrogate may qualify a positive. This alternative has not been constructed or solved in this checkpoint. '
        'A subsequent distinct model must retain all66 originals, original area and material target, fixed57 source, complete domain and occupancy constraints, and shared production budgets. Only full guarded-coordinate, original66-polygon/stock/native validation, production integration and the unchanged13-job/two-kerf matrix can close H5. '
        'Main61359456 remains preserved; await terminal CI40242602102 before normal push to avoid cancelling its Windows check. H2 remains open under the unchanged gate with all22 reserved vectors untouched. No new release is qualified.')
    OUT.mkdir()
    for a,b in {'shared-search/plan.json':'pipeline-plan.json','shared-search/budget.json':'shared-budget.json','shared-search/result.json':'pipeline-result.json',
        'shared-search/solve/model-audit.json':'model-audit.json','shared-search/solve/result.json':'solver-result.json','search-audit/checks.json':'search-audit.json','main-ci-snapshot.json':'main-ci-snapshot.json'}.items():shutil.copyfile(BASE/a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'alternative_constructed':False,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],
        'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'master_solver_calls':1,'selected_anchor_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'shared_budget_honored':True,
        'solver_soft_limit_overshoot_seconds':check['solver_soft_limit_overshoot_seconds'],'original_counts_material_gate_and_native_guards_unchanged':True,'pushed':False,
        'current_main_ci_id':40242602102,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    modelplan=load(BASE/'shared-search/solve/plan.json')
    for field,folder in [('query_hashes',SOURCE/'queries'),('group_hashes',CONVEX/'groups')]:
        for i,h in modelplan[field].items():
            p=folder/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    previous=ROOT/'benchmarks/results/h5-original-core-search-20261025/raw-manifest.json';manifest=load(previous);known={r['path']:r['sha256'] for r in manifest['files']+manifest['aliases']}
    for n in ['audit/certified-new-exclusions.json','audit/verified-pair-witnesses.json','audit/checks.json','geometry-audit-repaired/checks.json']:
        p=ROOT/'output/h5-original-core-search-20261025/remaining-second-sheet-pairs'/n
        assert digest(p)==known[p.relative_to(ROOT/'output').as_posix()]
    members['source-inputs/'+previous.relative_to(ROOT).as_posix()]=previous
    names=['prepare_h5_second_sheet_guided_search.py','audit_h5_second_sheet_guided_master.py','solve_h5_second_sheet_guided_master.py','audit_h5_second_sheet_guided_selection.py',
        'solve_h5_second_sheet_guided_anchors.py','run_h5_second_sheet_guided_search.py','audit_h5_second_sheet_guided_search.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'full_model_and_all14_hints_independently_reconstructed':True,'new_exclusion_and_witness_provenance_matches_committed_evidence':True,
        'all66_originals_required_no_hint_fixed_placements':True,'unknown_without_incumbent_preserved':True,'shared_budget_honored':True,'solver_soft_limit_overshoot_retained':True,
        'production_and_readmes_unchanged':True,'alternative_representation_not_yet_built':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: second-sheet-guided full search — 2026-10-25

**The distinct guided full master finishes UNKNOWN without an incumbent.** Its
shared runtime stays within60 seconds. The complete second-sheet classification
is now represented in the model, but it does not yet yield a full66-part layout.
H2/H5 remain open at **60%**.

The master retains all9,776 domain choices, nine mandatory moving originals,
fixed57 source, both original-area limits, all existing occupancy and conflict
constraints, and the complete original collision-core representation. The ten
new independently proved second-sheet exclusions add **150 physical clauses**.
Fourteen advisory values guide copies7 and8 toward the verified [1,1] two-cog
placement: sheet/query choices, selected domain, choice index and coordinates.
The copies share identical permitted geometry; the hints add no constraint,
fix no placement and omit no other original. All inputs match committed evidence.

Independent reconstruction verifies every field of the **18,530-variable /
34,218-constraint** model, including all14 hints. Construction takes
**{model['construction_seconds']:.6f}s**, audit **{model['audit_seconds']:.6f}s**.
The sole master call retains the45-second soft cap, eight workers and seed zero,
within the shared60-second pipeline and two-second shutdown reserve.
It returns **UNKNOWN in {solved['seconds']:.6f}s**, with no incumbent. The measured
soft-limit overshoot is **{check['solver_soft_limit_overshoot_seconds']:.6f}s**;
shared elapsed is **{run['elapsed_seconds']:.6f}s**, within60seconds.
No full-coordinate or native follow-up is opened. The terminal audit checks
the actual parameter value against the recorded remaining allowance, which
already subtracts the shutdown reserve. No call is continued or retried, and
UNKNOWN establishes neither feasibility nor impossibility.

The next investigation will measure an alternative representation: convex
allowed cells covering the bounded collision-free displacement region, instead
of a separate edge disjunction for every forbidden core piece. Before any use,
each retained cell must be independently proved sufficient for the complete
original guarded inequalities, with all raw faces, boundary losses, insets,
grid bounds and coefficient rounding preserved. This representation has not
been built or solved in this checkpoint. Original counts, clearance, stock,
material target and production/H5 budgets remain unchanged.

Main61359456 and its offcut documentation remain preserved. Its own
[CI40242602102]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful jobs
in the saved snapshot. This checkpoint is local; defer the normal push until
that run is terminal so its unfinished Windows check is not cancelled.
Production source and all three accurate READMEs are unchanged. Preview
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged; no release is qualified.
No native packing, quality run or held-out evaluation occurs. All22 reserved
H2 vectors remain untouched under Artem's unchanged-gate decision.

Evidence: [full model and hint audit]({NAME}/model-audit.json),
[terminal budget audit]({NAME}/search-audit.json), [source review]({NAME}/source-review.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
The archive retains **{archive['archive_members']}** canonical files and
**{archive['verified_aliases']}** exact-content aliases, including complete models,
inputs, parameters, logs and helper sources, with SHA-256, size and CRC checks.
'''
    replacements={'within60':'within 60','full66':'full 66','all9,776':'all 9,776','fixed57':'fixed 57','copies7 and8':'copies 7 and 8','all14':'all 14','the45':'the 45','shared60':'shared 60','60seconds':'60 seconds','Main61359456':'Main 61359456','All22':'All 22'}
    for a,b in replacements.items():report=report.replace(a,b)
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 guided full original-core search, 2026-10-25:** [the evidence]({link})
adds all 150 clauses from the ten proved second-sheet exclusions and 14 optional
values from a verified two-cog placement. The independent model audit covers
18,530 variables / 34,218 constraints, all hints and all 66 required originals;
no placement is fixed by a hint. The sole call finishes UNKNOWN without an
incumbent in 45.537740s; the 0.537740s soft-cap overshoot is preserved. Shared
47.986694s remains within 60s. No full-coordinate or native follow-up is opened.
Next investigate a different collision-free displacement-cell representation,
proving every retained cell safe against all original guarded inequalities
before use. That representation is not built yet. H2/H5 remain open at 60%;
production source, READMEs, releases, original counts, material target and guards
are unchanged. All 22 reserved H2 vectors remain untouched. Main CI40242602102
is still tracked before the next normal push.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
