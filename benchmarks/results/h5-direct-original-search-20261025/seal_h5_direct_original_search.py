"""Preserve the strict-model negative and the complete integer outer cover."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-direct-original-search-20261025';BASE=ROOT/'output'/NAME;BOXES=ROOT/'output/h5-outer-displacement-boxes-20261025';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    model=load(BASE/'shared-search/solve/model-audit.json');solved=load(BASE/'shared-search/solve/result.json');timing=load(BASE/'search-audit/checks.json');prep=load(BOXES/'result.json');boxes=load(BOXES/'audit-provenance-repaired/checks.json')
    assert all(r['passed'] for r in [model,timing,boxes]) and solved['status']=='INFEASIBLE' and not solved['has_full_original_model_candidate'] and timing['shared_budget_honored']
    assert timing['solver_soft_limit_overshoot_seconds']==0 and prep['completed_cases']==164 and not prep['pending_cases'] and prep['solver_calls']==0
    prior=load(ROOT/'benchmarks/results/h5-all-original-cell-search-20261025/source-review.json');assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();assert head=='5469e7656175a9088777a80aa0683bbd2cff9323' and mainhead=='728b2db2e86c2d123920fdceb8e3e2c1bcf1f66e'
    ci=json.loads(subprocess.check_output(['gh','run','view','40246226212','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead;write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('The distinct table-free full-coordinate call is closed INFEASIBLE in 42.634289 seconds, shared 44.271944 seconds, with no soft-cap overshoot and the declared ten-second shutdown reserve. '
        'This rejects only the fixed-57/source-angle/inward-domain construction with stricter safe cells, not unrestricted packing. No layout, native or H5 pass is claimed. '
        'An independently proved necessary outer cover now preserves every integer displacement satisfying the original full guarded pair clauses for all 164 cases / 394 physical uses. Its exact 5 mm x-slab partition removes only whole rectangles that provably fail one complete original clause. '
        'All 16,210 slabs, 22,063 removed rectangles and 6,485,956 corner inequalities are checked; 9,129 merged retained boxes remain, corresponding to 60,671 physical box flags. Retained boxes can contain invalid placements. No outer-cover solver has run. '
        'Next transform the audited table-free model by replacing ALL stricter pair-cell choices, for both cog/cog and the remaining cases, with these necessary outer boxes. Remove only the old cell flags, their cell constraints and old cell hints, retain exact pair-query activations and every original domain, area, count, coordinate, capacity and proved exclusion. '
        'Explicitly enforce each original query-difference rectangle. Independently verify every removed/replaced field and all coverage certificates before a fresh bounded call; do not leave any old stricter cell restriction behind and call the result a relaxation. '
        'A positive must be checked against every original source clause and complete original geometry, with all violations retained and no native call on invalid geometry. A negative would only concern the source inward integer domains, source angles and fixed 57; it would motivate changing that source construction rather than repeating a closed call. '
        'Use a newly declared one-call 60-second diagnostic budget, at most 45 solver seconds and ten-second shutdown reserve. Offline preparation is not production qualification; all H5 production/matrix requirements remain unchanged. '
        'H2 stays open under the original gate with all 22 reserved vectors untouched. Main 728b2db2 has its own live CI; preserve newer work and wait for terminal checks before the next normal push. No new release is qualified.')
    OUT.mkdir()
    copies={BASE/'shared-search/plan.json':'search-plan.json',BASE/'shared-search/budget.json':'search-budget.json',BASE/'shared-search/result.json':'search-result.json',BASE/'shared-search/solve/model-audit.json':'model-audit.json',BASE/'shared-search/solve/result.json':'solver-result.json',BASE/'search-audit/checks.json':'search-audit.json',BASE/'main-ci-snapshot.json':'main-ci-snapshot.json',
        BOXES/'plan.json':'outer-box-plan.json',BOXES/'result.json':'outer-box-result.json',BOXES/'summary.json':'outer-box-summary.json',BOXES/'audit-provenance-repaired/checks.json':'outer-box-audit.json',BOXES/'audit-provenance-repaired/case-checks.json':'outer-box-case-checks.json',BOXES/'audit/failure.txt':'outer-box-initial-audit-failure.txt',BOXES/'audit/repair-record.json':'outer-box-provenance-repair.json'}
    for a,b in copies.items():shutil.copyfile(a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'outer_cover_model_prepared':False,'outer_cover_solver_calls':0,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,
        'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','strict_projected_solver_calls':1,'outer_cover_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'original_counts_material_gate_and_native_guards_unchanged':True,
        'pushed':False,'current_main_ci_id':40246226212,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for base in [BASE,BOXES]:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for previous in ['h5-all-original-cell-search-20261025','h5-six-cog-guided-search-20261025']:
        p=ROOT/'benchmarks/results'/previous/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['solve_h5_direct_original_model.py','prepare_h5_direct_original_search.py','run_h5_direct_original_search.py','audit_h5_direct_original_search.py','run_h5_all_original_cell_search.py','audit_h5_all_original_cell_search.py',
        'prepare_h5_outer_displacement_boxes.py','audit_h5_outer_displacement_boxes.py','repair_h5_outer_box_provenance.py','audit_h5_outer_displacement_boxes_repaired.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'strict_model_matches_independently_audited_archived_projection':True,'strict_negative_and_limited_scope_preserved':True,'shared_and_soft_search_limits_honored':True,
        'outer_cover_full_integer_partition_independently_verified':True,'all_removed_rectangles_exactly_proved_invalid':True,'outer_cover_positive_safety_not_claimed':True,'outer_cover_solver_calls':0,'failed_provenance_lookup_and_repaired_audit_preserved':True,
        'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: closed direct-model negative and complete integer outer cover — 2026-10-25/26

**The table-free full-coordinate model reports INFEASIBLE within budget.** This
rejects its conservative fixed-source construction, not the full packing
problem. A separately verified outer cover now retains every integer pair
displacement satisfying the original guarded source clauses, enabling a wider
diagnostic next. That diagnostic model has not yet been built or solved.
All 66 originals remain mandatory; H2/H5 remain open at **60%**.

## Closed strict-model call

The archived projection has **32,074 variables / 173,814 constraints**, all
18 coordinates for nine moving originals, 57 fixed originals and all 36 direct
guarded moving-pair relations. Every original domain, area, count and capacity
constraint remains. Only the obsolete compatibility table and its private
auxiliaries were removed, as independently verified in the preceding checkpoint.

Committed archive hashes match. Loading, validation and export into the actual
solver model take **{model['construction_seconds']:.6f}s**; the new complete
protobuf equality check takes **{model['audit_seconds']:.6f}s**. This uses the
already independently audited immutable model; offline region preparation and
the earlier projection audit are not a production-budget qualification.

The distinct eight-worker, seed-zero call is capped at 45 seconds, with a
declared **10-second shutdown reserve** inside a new shared 60-second budget.
It reports **INFEASIBLE in {solved['seconds']:.6f}s**. Complete elapsed time is
**{timing['actual_shared_seconds']:.6f}s**. There is no soft-cap overrun, candidate,
restart or continuation. The saved model, parameters, source hashes and timing
pass terminal read-back. No native or quality run occurs.

This negative applies only to the **fixed 57 placements, recorded source angles,
inward integer domains and stricter pair-cell representations**. The added
conservative pair padding and inset losses are not silently treated as exhaustive
geometry. It proves neither unrestricted impossibility nor H5 completion.

## Complete necessary outer cover

To distinguish stricter pair-cell loss from the source construction itself,
prepare a necessary integer cover of the original full guarded displacement
rules. For all **164 ordered query pairs / 394 physical pair and mode uses**,
partition the complete integer anchor-difference rectangle into inclusive x
slabs of at most **5,000 micrometres**. For each original forbidden face, derive
the y interval whose entire slab rectangle satisfies every failure inequality:

`a*dx + b*dy <= outside_bound - 1`.

Exact integer floor/ceiling determines these intervals. Their union is removed;
every remaining y interval is retained. Merge adjacent slabs only when their
retained y bounds are identical. Boundary endpoints are included exactly, so
there are no missing integer points between slabs or intervals.

Preparation takes **{prep['seconds']:.6f}s**, completing all cases. It records
**16,210 slabs**, **22,063 certified inner failure rectangles**, and **9,129
merged retained boxes**. Applying them to all physical pairs would require
**60,671 box flags**. This representation is not assumed faster or safe for
cutting; its purpose is to avoid excluding a valid original integer displacement.

Independent audit takes **{boxes['seconds']:.6f}s**. It rebuilds all source cases
and difference bounds, recomputes every interval with rational floor/ceiling,
and checks **6,485,956 source inequalities at exact integer rectangle corners**.
A separate endpoint sweep verifies every y complement, and expansion of every
merged box reproduces exactly the complete retained slab intervals without
overlap, omission or extra extent. Thus **every full-guarded source-valid integer
displacement remains available**. Each removed box is proved invalid.

Retained boxes can contain invalid placements. They are a necessary relaxation,
not a safety certificate or changed clearance rule. Positive assignments must
still pass every original source inequality and full original geometry before
native validation. A future negative could only concern the original source
angles/inward integer domains/fixed 57 construction, not unrestricted packing.

The initial audit failed a provenance lookup: the newer archive contains the
remaining non-cog mutual sources, while cog source 081 is preserved in the prior
guided-search archive. The separate repaired audit resolves that one exact key
against its committed manifest. All other provenance checks and the full
integer proof remain unchanged; the failed script, plan, traceback and repair
record are retained. No geometry or solver call was repeated.

## Next action and repository state

Replace **all** stricter pair cells in the audited table-free model with these
outer boxes, including both cog/cog cases. Retain original query activation,
domains, coordinates, counts, areas, capacities and proved exclusions. Remove
only obsolete cell flags, their constraints and cell hints; explicitly impose
the original difference bounds. Independently verify this complete replacement
before a fresh bounded call. Leaving old stricter cells in place would not test
the intended relaxation. No outer-cover model or solver call exists yet.

Use a new declared 60-second diagnostic loading/verification/search budget,
at most 45 solver seconds and the ten-second reserve. Record every positive
source-rule violation; never send invalid geometry to native validation.
All production-budget, original-geometry and 13-job/two-kerf H5 requirements
remain unchanged.

Main 728b2db2 remains preserved. Its own
[CI 40246226212]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful
jobs at the snapshot. Local checkpoint 5469e765 and this new evidence wait for
terminal CI before the next normal push, with newer remote work reconciled first.
Production source, all three accurate READMEs, preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain unchanged. No new release is qualified. H2 keeps its original
gate and all 22 reserved vectors untouched.

Evidence: [closed search]({NAME}/search-audit.json),
[outer-cover plan]({NAME}/outer-box-plan.json),
[exact coverage audit]({NAME}/outer-box-audit.json),
[archive]({NAME}/raw-001.zip), and [manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']} canonical files and {archive['verified_aliases']}
exact-content aliases** retain every model, parameter, log, source file, integer
partition, failed audit and proof record with size, SHA-256 and CRC verification.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 direct-model negative and complete integer outer cover, 2026-10-26:** [the evidence]({link})
records the distinct 32,074-variable / 173,814-constraint full-coordinate model
INFEASIBLE in 42.634289s, shared 44.271944s, within its 45s cap and 60s budget
with a 10s shutdown reserve. This rejects only the fixed-57/source-angle/inward-
domain construction with stricter pair cells, not unrestricted packing. A new
necessary outer cover retains every integer displacement satisfying the original
guarded pair rules: all 164 cases / 394 physical uses, 16,210 complete slabs,
22,063 proved-invalid rectangles and 9,129 retained boxes. Independent rational
partition checks and 6,485,956 exact corner inequalities pass. Retained boxes
are not safe placements. No outer-cover model or solver has run; next replace
all stricter pair-cell constraints and audit the complete transformation before
a distinct bounded diagnostic. All originals, material/native limits and H5
production requirements remain unchanged. The provenance-lookup failure and
separate corrected audit are preserved. Main 728b2db2's own CI 40246226212 is
still tracked before pushing local checkpoints. Production, READMEs and releases
are unchanged; H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    status=ROOT/'docs/STATUS.md';s=status.read_text(encoding='utf-8');assert s.startswith('# Status — 2026-10-25\n');status.write_text(s.replace('# Status — 2026-10-25\n','# Status — 2026-10-26\n',1),encoding='utf-8',newline='\n')
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success},flush=True)
if __name__=='__main__':main()
