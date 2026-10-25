"""Preserve guarded search, six-cog witness and the failed fixed-witness completion."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-guarded-cell-search-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME;SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025';CONVEX=ROOT/'output/h5-convex-domain-conflicts-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    model=load(BASE/'shared-search/solve/model-audit.json');solved=load(BASE/'shared-search/solve/result.json');run=load(BASE/'shared-search/result.json');budget=load(BASE/'search-audit/checks.json')
    four=load(BASE/'first-sheet-four-cog-diagnostic/result.json');fourmodel=load(BASE/'first-sheet-four-cog-diagnostic/model-audit.json');fourcheck=load(BASE/'first-sheet-four-cog-diagnostic/audit/checks.json');geometry=load(BASE/'six-cog-geometry-audit/checks.json');sample=load(BASE/'remaining-three-candidates/result.json');samplecheck=load(BASE/'remaining-three-candidates/audit/checks.json')
    assert all(r['passed'] for r in [model,budget,fourmodel,fourcheck,geometry,samplecheck])
    assert solved['status']=='UNKNOWN' and not solved['has_necessary_domain_candidate'] and budget['shared_budget_honored'] and run['anchor_solver_calls']==0
    assert four['status']=='OPTIMAL' and four['total_seconds']<60 and geometry['placed_originals']==63 and geometry['missing_original_items']==[28,29,50]
    assert samplecheck['accepted_bracket_points']==0 and samplecheck['accepted_insert_points']==8 and samplecheck['rejected_points_with_exact_failure_certificates']==103028
    prior=load(ROOT/'benchmarks/results/h5-cog-displacement-cells-20261025/source-review.json');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head.startswith('ba78688a') and mainhead=='613594568fb49a71abf0248aec218a6b12f63319'
    ci=json.loads(subprocess.check_output(['gh','run','view','40242602102','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead;write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Keep the full guarded-cell master closed: UNKNOWN without an incumbent, solver45.666246 seconds, shared48.579203 seconds. '
        'The new model was independently reconstructed with16775 variables,46383 constraints,3495 cell flags,30 exact sheet-activation flags and16 advisory hints; all66 originals remained mandatory. '
        'A distinct first-sheet four-cog diagnostic solved once in7.753828 seconds (shared8.201210), using all735 original domains per cog and all229 guarded cells per pair. '
        'It yields a fully checked six-cog witness when combined with the previously verified second-sheet pair. All63 currently placed originals pass1467 original pair checks and252 stock-edge checks against unchanged native guards. The two brackets28/29 and insert50 remain missing. '
        'The complete declared finite completion sample regenerated162863 grid points,103036 unique source-valid poses. Exact rejection certificates cover103028 poses; zero bracket and eight insert poses survive the fixed six cogs. This excludes only that finite sample, not continuous completion or another six-cog arrangement. '
        'Next keep all six cogs movable in a distinct full original model. Use the six-cog positions only as advisory hints, with source-choice and proved cell memberships checked. Add redundant but exact selected-domain integer bounding boxes for each of the6x767 cog-domain choices (9204 conditional bounds), as used by the successful smaller diagnostic. '
        'Retain every full domain, all original counts, area charges, pair and occupancy constraints, original stock/material target and full guarded displacement cells. Audit every new field and hint; do not freeze the63-part partial layout or waive the missing brackets. '
        'Keep one45-second master call within the shared60-second pipeline and2-second shutdown reserve. A positive still needs the full original-coordinate follow-up, all66 original geometry/native checks, production-budget integration and unchanged13-job/two-kerf H5 matrix. No closed call is retried or extended. '
        'Main61359456 remains preserved; await terminal CI40242602102 before normal push and reconcile any newer remote work first. H2 remains open under the unchanged gate with22 reserved vectors untouched. No release is qualified.')
    OUT.mkdir()
    copies={'shared-search/plan.json':'pipeline-plan.json','shared-search/budget.json':'shared-budget.json','shared-search/result.json':'pipeline-result.json','shared-search/solve/model-audit.json':'model-audit.json','shared-search/solve/result.json':'solver-result.json','search-audit/checks.json':'search-audit.json',
        'first-sheet-four-cog-diagnostic/plan.json':'four-cog-plan.json','first-sheet-four-cog-diagnostic/model-audit.json':'four-cog-model-audit.json','first-sheet-four-cog-diagnostic/result.json':'four-cog-result.json',
        'first-sheet-four-cog-diagnostic/audit/checks.json':'four-cog-audit.json','first-sheet-four-cog-diagnostic/audit/six-cog-positions.json':'six-cog-positions.json','first-sheet-four-cog-diagnostic/audit/six-cog-pair-checks.json':'six-cog-pair-checks.json',
        'six-cog-geometry-audit/checks.json':'original63-geometry-audit.json','six-cog-geometry-audit/missing-originals.json':'missing-originals.json','remaining-three-candidates/plan.json':'completion-sample-plan.json',
        'remaining-three-candidates/result.json':'completion-sample-result.json','remaining-three-candidates/summary.json':'completion-sample-summary.json','remaining-three-candidates/audit/checks.json':'completion-sample-audit.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
        'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','full_master_solver_calls':1,'full_anchor_solver_calls':0,
        'separate_four_cog_solver_calls':1,'sample_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,
        'pushed':False,'current_main_ci_id':40242602102,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    mp=load(BASE/'shared-search/solve/plan.json')
    for field,folder in [('query_hashes',SOURCE/'queries'),('group_hashes',CONVEX/'groups')]:
        for i,h in mp[field].items():
            p=folder/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    manifestpath=ROOT/'benchmarks/results/h5-cog-displacement-cells-20261025/raw-manifest.json';old=load(manifestpath);known={r['path']:r['sha256'] for r in old['files']+old['aliases']}
    for n in ['coarse-refinement/selected-query-18.json','coarse-refinement/selected-query-19.json','audit/checks.json']:
        p=ROOT/'output/h5-cog-displacement-cells-20261025'/n;assert digest(p)==known[p.relative_to(ROOT/'output').as_posix()]
    members['source-inputs/'+manifestpath.relative_to(ROOT).as_posix()]=manifestpath
    names=['prepare_h5_guarded_cell_search.py','audit_h5_guarded_cell_master.py','solve_h5_guarded_cell_master.py','audit_h5_guarded_cell_selection.py','solve_h5_guarded_cell_anchors.py','run_h5_guarded_cell_search.py','audit_h5_guarded_cell_search.py',
        'audit_h5_four_cog_model.py','solve_h5_first_sheet_four_cogs.py','audit_h5_four_cog_solution.py','audit_h5_six_cog_geometry.py','prepare_h5_remaining_three_candidates.py','audit_h5_remaining_three_candidates.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'full_guarded_model_reconstructed':True,'unknown_without_incumbent_and_soft_overshoot_preserved':True,'both_shared_search_budgets_honored':True,
        'four_cog_model_and_six_cog_witness_independently_verified':True,'all63_original_geometry_checked_missing_three_explicit':True,'all_sample_accepts_and_rejects_independently_certified':True,
        'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: guarded full search and a verified six-cog construction — 2026-10-25

**The full guarded-cell master remains UNKNOWN. A smaller diagnostic finds four
first-sheet cog placements, giving a verified six-cog construction with the
known second-sheet pair.** Together with the fixed57, all63 placed originals
clear the original native guards. Two brackets and one insert remain required.
No full target layout is claimed; H2/H5 remain open at **60%**.

## Full guarded-cell search, closed

The master retains all66 originals, all9,776 domain options, both original-area
limits and every existing occupancy/pair exclusion. It replaces the necessary
raw-core cog conditions with the independently proved229+4 guarded displacement
cells. Every same-sheet pair chooses one cell for that sheet; different-sheet
pairs activate none. Independent reconstruction verifies all16,775 variables /
46,383 constraints, including30 sheet-activation flags,3,495 cell flags,6,990
chosen-cell box bounds,12,465 cell halfplanes and16 advisory hints. Boolean
activation truth tables are exhausted. No hint fixes a placement or removes a part.

Construction takes **{model['construction_seconds']:.6f}s**, model audit
**{model['audit_seconds']:.6f}s**. The single45-second/eight-worker/seed-zero call
returns **UNKNOWN in {solved['seconds']:.6f}s** without an incumbent. Its soft-cap
overshoot is **{budget['solver_soft_limit_overshoot_seconds']:.6f}s**, explicitly retained.
Shared pipeline time **{run['elapsed_seconds']:.6f}s** stays within60 seconds.
No full-coordinate or native follow-up is opened. This closed call proves neither
feasibility nor impossibility. The extra0.010 mm first-sheet construction
restriction from the cell preparation remains explicit.

## Four first-sheet cogs and six-cog read-back

The existing exact second-sheet capacity is at most two cogs. A full placement
of six moving cogs therefore needs at least four on the first sheet. A separate
diagnostic keeps **four mandatory original cogs, all735 first-sheet domains per
cog, every domain's integer box and inward halfplanes, applicable regional
limits, the global three-region exclusion and all229 guarded pair cells**.
The other five moving originals are absent only from this subproblem and remain
mandatory for the full job. No partial acceptance or objective is introduced.

Its independent oracle verifies **4,329 variables /23,991 constraints**, with
no hints. The sole45-second-cap call returns a feasible assignment (`OPTIMAL`
is the satisfaction-solver status) in **{four['solver_seconds']:.6f}s**; complete
elapsed time is **{four['total_seconds']:.6f}s**, inside the separate60-second budget.
The call is closed. The four domain rows are **3,31,72,734**; every chosen domain,
cell, regional bound and original guarded inequality passes read-back.

Combining those positions with the previous second-sheet [1,1] witness assigns
all six interchangeable original copies without changing their source angle.
All **seven same-sheet cog pairs /427 complete original guarded clauses** pass.
The six positions are available as advisory hints; they are not fixed in the
next full search.

## Original geometry and failed sampled completion

Rebuilding the six cogs and all57 fixed originals from actual job polygons
verifies **63 distinct original identities**, **1,467 same-sheet pair checks**
and **252 stock-edge checks**. Minimum original separation is
**{geometry['minimum_original_gap_mm']:.12f}mm**, above the native requirement
**{geometry['native_required_gap_mm']:.12f}mm**. Minimum extra stock margin is
**{geometry['minimum_extra_stock_margin_mm']:.12f}mm**, above the native guard
**{geometry['native_stock_guard_mm']:.12f}mm**. Maximum reconstruction error is
**{geometry['maximum_original_reconstruction_error_mm']:.3g}mm**. Missing items
**28,29,50** (two brackets and one insert) are recorded explicitly; no native
validator is called on the partial layout.

A separate deterministic completion sample tests all18 allowed bracket/insert
queries. Rational vertex-to-mean interpolation and floor/ceil micrometre
neighbours generate **162,863 points**, yielding **103,036 unique source-valid
poses**. Every point is tested against all fixed cogs on its sheet using the full
guarded original inequalities. **Zero bracket poses and eight insert poses**
survive. The sampler finishes in **{sample['seconds']:.6f}s**, with no pending query.

Independent read-back regenerates the complete declared sample and supplies a
failed source-clause certificate for every one of the **103,028 rejected poses**.
It verifies **4,858,271 failed inequalities with arbitrary-precision integers**,
and all **672** full clauses for the eight accepted poses. This proves the
finite sample cannot complete the fixed six-cog arrangement. It does **not**
exclude unsampled positions, other cog arrangements or unrestricted packing.

Next keep all six cogs movable and use the verified positions only as hints.
Add explicit selected-domain integer boxes for all6×767 cog-domain choices,
as in the successful smaller diagnostic:9,204 redundant conditional bounds.
These bounds preserve every allowed integer position. Independently audit the
new full model and hints before a distinct bounded call. All66 originals, the
material target, native guards, full-coordinate follow-up and complete H5
requirements remain unchanged. A positive must still reach production-budget
integration and the original13-job/two-kerf matrix.

## Repository and evidence

Main61359456 and its offcut documentation remain preserved. Its own
[CI40242602102]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful jobs
at the saved snapshot. This checkpoint remains local pending terminal CI, so
the Windows check is not cancelled by a push. Production source, all three
accurate READMEs, preview v0.2.0-alpha.1 and stable Latest v0.1.0 are unchanged.
No new release is qualified. No native packing, quality run or held-out
evaluation occurs; all22 reserved H2 vectors remain untouched.

Evidence: [full model audit]({NAME}/model-audit.json),
[terminal budget audit]({NAME}/search-audit.json), [four-cog audit]({NAME}/four-cog-audit.json),
[63-original geometry audit]({NAME}/original63-geometry-audit.json),
[sample audit]({NAME}/completion-sample-audit.json), [archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). The archive retains
**{archive['archive_members']}** canonical files and **{archive['verified_aliases']}**
exact-content aliases, including complete models, parameters, logs, original
layouts, every sampled point and rejection certificate, with size/SHA-256/CRC verification.
'''
    replacements={'fixed57':'fixed 57','all63':'all 63','all66':'all 66','all9,776':'all 9,776','proved229':'proved 229','all16,775':'all 16,775','including30':'including 30','flags,3,495':'flags, 3,495','flags,6,990':'flags, 6,990','bounds,12,465':'bounds, 12,465','and16':'and 16','single45':'single 45','within60':'within 60','extra0.010':'extra 0.010','all735':'all 735','all229':'all 229','/23,991':'/ 23,991','sole45':'sole 45','separate60':'separate 60','3,31,72,734':'3, 31, 72, 734','/427':'/ 427','all57':'all 57','28,29,50':'28, 29, 50','all18':'all 18','all6×767':'all 6×767','diagnostic:9,204':'diagnostic: 9,204','All66':'All 66','original13':'original 13','Main61359456':'Main 61359456','all22':'all 22'}
    for a,b in replacements.items():report=report.replace(a,b)
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 guarded cell search and six-cog witness, 2026-10-25:** [the evidence]({link})
preserves a full 16,775-variable / 46,383-constraint guarded master UNKNOWN,
without an incumbent. Shared48.579203s is within60s; the45-second soft-cap
overshoot is retained. A distinct four-cog first-sheet diagnostic succeeds in
7.753828s (shared8.201210s), with every domain, bound, cell and full original
guarded clause independently verified. Combined with the known second-sheet
pair, all63 currently placed originals pass1,467 pair and252 stock-edge checks.
Two brackets28/29 and insert50 are explicitly missing, so no full target/native
pass is claimed. A complete declared finite sample regenerates162,863 points;
103,028 exact rejection certificates leave zero bracket and eight insert poses.
This does not prove continuous impossibility. Next keep all six cogs movable,
use their verified positions only as hints, and add9,204 exact selected-domain
box bounds to the full model. All66 parts, material/native limits and H5 gates
remain required. Production source, READMEs and releases are unchanged; H2/H5
remain open at60%, with22 reserved H2 vectors untouched. Main CI40242602102
is tracked before normal push.
'''
    for a,b in {'Shared48':'Shared 48','within60':'within 60','the45':'the 45','shared8':'shared 8','all63':'all 63','pass1,467':'pass 1,467','and252':'and 252','brackets28/29':'brackets 28/29','insert50':'insert 50','regenerates162':'regenerates 162','add9,204':'add 9,204','All66':'All 66','at60%':'at 60%','with22':'with 22'}.items():note=note.replace(a,b)
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
