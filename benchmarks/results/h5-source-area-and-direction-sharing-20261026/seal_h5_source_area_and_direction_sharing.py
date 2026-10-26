"""Archive two closed complete-source searches and the exact representation proof."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-source-area-and-direction-sharing-20261026';OUT=ROOT/'benchmarks/results'/NAME
REVIEW=ROOT/'output/h5-shared-direction-source-review-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(REVIEW/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==review['source_head']=='68c82ae1dd88c4486dbccb09d8e92a6879c2199e'
    assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
    OUT.mkdir();rows=[];bases=[REVIEW,ROOT/'output/h5-first-sheet-main-sync-20261026']
    for label in ['area-constrained','shared-direction']:
        model=ROOT/f'output/h5-{label}-source-model-20261026';run=ROOT/f'output/h5-{label}-source-search-20261026';bases.extend([model,run]);mr=load(model/'result.json');ma=load(model/'audit/checks.json');sa=load(run/'search-audit/checks.json')
        assert ma['passed'] and ma['all_original_full_guarded_source_clauses_retained'] and sa['passed'] and sa['terminal_status']=='UNKNOWN' and sa['solver_calls']==1 and sa['shared_budget_honored'] and not sa['full_guarded_source_candidate']
        dest=OUT/label;dest.mkdir()
        for p,n in [(model/'result.json','model-result.json'),(model/'audit/checks.json','model-audit.json'),(run/'shared-search/result.json','shared-search-result.json'),(run/'shared-search/solve/model-audit.json','actual-model-audit.json'),(run/'shared-search/solve/result.json','solver-result.json'),(run/'search-audit/checks.json','closed-search-audit.json')]:shutil.copyfile(p,dest/n)
        rows.append({'representation':label,'variables':mr['variables'],'constraints':mr['constraints'],'model_sha256':mr['model_sha256'],'model_preparation_seconds':mr['seconds'],'model_audit_seconds':ma['seconds'],'terminal_status':'UNKNOWN','solver_seconds':sa['actual_solver_seconds'],'shared_seconds':sa['actual_shared_seconds'],'soft_limit_overshoot_seconds':sa['solver_soft_limit_overshoot_seconds'],'all66_originals_required':True})
    area=load(bases[2]/'audit/checks.json');shared=load(bases[4]/'audit/checks.json')
    assert area['entire_original_parent_restored'] and area['newly_excluded_beyond_original_global_area']==9 and shared['shared_direction_equivalence_verified'] and shared['old_flags_verified']==156789 and shared['shared_direction_flags']==101455
    write(OUT/'comparison.json',rows)
    copies=[(bases[2]/'area-additions.json','area-additions.json'),(bases[2]/'audit/allocation-propagation-comparison.json','allocation-propagation-comparison.json'),(bases[4]/'audit/equivalence-proof.json','equivalence-proof.json'),(REVIEW/'review.json','source-review.json'),(REVIEW/'main-ci.json','main-ci-snapshot.json'),(ROOT/'output/h5-first-sheet-main-sync-20261026/receipt.json','prior-main-push-receipt.json'),(ROOT/'output/h5-source-direction-reuse-20261026.json','direction-reuse-survey.json'),(ROOT/'output/h5-source-model-timing-20261026.json','closed-log-timing.json')]
    for p,n in copies:shutil.copyfile(p,OUT/n)
    timing=load(ROOT/'output/h5-source-model-timing-20261026.json');write(OUT/'next-step.json',{'action':timing['next_structural_question'],'predicted_variables':111710,'predicted_constraints':164254,'previous_calls_closed':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False})
    members={};inputs={}
    for base in bases:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
    for name in ['h5-bounded-source-search-20261026','h5-first-sheet-cog-neighborhoods-20261026']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    extras=['h5-source-direction-reuse-20261026.json','h5-shared-direction-search-helper-generation-20261026.json','h5-source-model-timing-20261026.json']
    for n in extras:members['extra/'+n]=ROOT/'output'/n
    names=['prepare_h5_area_constrained_source_model.py','audit_h5_area_constrained_source_model.py','prepare_h5_area_constrained_search_helpers.py','run_h5_area_constrained_source_search.py','audit_h5_area_constrained_source_search.py','survey_h5_source_direction_reuse.py','prepare_h5_shared_direction_source_model.py','audit_h5_shared_direction_source_model.py','prepare_h5_shared_direction_search_helpers.py','run_h5_shared_direction_source_search.py','audit_h5_shared_direction_source_search.py','review_h5_shared_direction_checkpoint.py','summarize_h5_source_model_timing.py','run_h5_bounded_source_search.py','audit_h5_bounded_source_search.py','pack_h5_evidence_archive.py','ccd1.py']
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
    checks={'passed':True,'area_model_preserves_entire_original_parent':True,'all14_area_rules_independently_reconstructed':True,'newly_excluded_original_area_allocations':9,'shared_direction_projection_equivalence_verified':True,'old_and_new_auxiliary_constraints_fully_accounted_for':True,'both_actual_solver_imports_verified':True,'two_distinct_single_calls_closed':True,'both_unknown_not_infeasible':True,'both_soft_limit_overshoots_preserved':True,'both_total_budgets_honored':True,'required_originals':66,'moving_originals':9,'fixed_originals':57,'native_packing_calls':0,'quality_runs':0,'reserved_H2_files_evaluated':0,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    table='\n'.join(f"| {r['representation']} | {r['variables']:,} | {r['constraints']:,} | {r['terminal_status']} | {r['solver_seconds']:.6f} / {r['shared_seconds']:.6f} |" for r in rows)
    report=f'''# H5: source area propagation and shared directions — 2026-10-26

**Both distinct bounded searches return UNKNOWN.** No layout or impossibility
proof is obtained. H2/H5 remain open at **60%** completed milestone weight.
All 66 originals remain required, with nine movable and 57 fixed in the
original source construction. No witness cog coordinates are locked.

| Representation | Variables | Constraints | Result | Solver / total seconds |
|---|---:|---:|---|---:|
{table}

## Verified area propagation

The first model preserves every original variable, constraint and all 72 hints,
then appends exactly 14 independently proved source-region area inequalities.
The independent reader reconstructs all 184 sheet-mode coefficients and
activations and restores the complete parent protobuf. Across all 42 count
allocations, the original global-area rules admit 23; the new necessary bounds
exclude another nine. The 14 remaining allocations are not proved feasible.

## Exact reduction in auxiliary variables

The second model replaces 156,789 mode-specific direction flags with 101,455
shared flags. Sharing is restricted to identical normalized integer inequalities
for the same ordered physical pair. Positive-gcd division and an exact ceiling
preserve every integer boundary. Each shared flag is defined by a plane and its
complement. All 394 source pair modes, active face clauses, displacement bounds,
the original base, the 14 area rules and the 72 hints are retained.

An independent audit verifies both complete auxiliary-constraint multisets,
all 158,777 direction uses and the two-way assignment proof. From a shared
assignment, each old flag becomes active-mode AND shared truth. From an old
assignment, evaluate every shared plane at the original coordinates. This
proves equal feasible projections within the original source construction.
It removes **55,334 variables (33.1%)** and **110,668 constraints (29.4%)**.
Actual solver import/export matches both audited models.

## Closed calls and limits

Each call uses eight workers, seed zero, a 45-second soft solver limit and a
60-second shared loading/audit/search budget with a ten-second shutdown reserve.
The actual soft-limit overruns are **1.532948s** and **3.508436s**; both total
budgets pass. Both calls are closed and must not be restarted, extended or
reseeded. There is no candidate for original-geometry or native validation.

The logs start search at 18.27s and 15.05s respectively. These single diagnostics
do not establish a production speed or packing improvement. Next investigate
whether the exact existential projection needs only shared flag-implies-plane
constraints, allowing removal of 101,455 complement clauses. This needs its
own independent assignment proof and actual import check before any new call.

The construction remains conditional on the recorded orientations, inward
integer domains, copy-order restrictions and fixed 57 placements. It does not
prove unrestricted packing impossible. A full original-geometry/native-valid
target, production integration and the complete 13-job/two-kerf H5 matrix remain
required. Offline work is not production-budget qualification.

## Repository and release state

The prior four-checkpoint push to main **68c82ae1** is retained with its verified
receipt. At the fresh 01:27 UTC snapshot, five of its six CI jobs have passed;
Windows checks are still running. Wait for terminal main CI before another
push so its result is preserved. Upstream Sparrow/Studio heads and release
state are unchanged. Production code and READMEs are unchanged; preview
v0.2.0-alpha.1 and stable v0.1.0 remain appropriate. No new release is qualified.
H2 retains its original gate and all 22 reserved vectors remain untouched.

Evidence: [comparison]({NAME}/comparison.json),
[area audit]({NAME}/area-constrained/model-audit.json),
[equivalence proof]({NAME}/equivalence-proof.json),
[shared-model audit]({NAME}/shared-direction/model-audit.json),
[prior push receipt]({NAME}/prior-main-push-receipt.json),
[checks]({NAME}/checks.json), and [raw manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}**
exact-content aliases are size/SHA-256/CRC verified in
**{archive['archive_parts']}** independently readable archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 source area propagation and shared directions, 2026-10-26:** [the evidence]({link})
retains two closed full nine-mover searches, both UNKNOWN. Fourteen verified
area rules exclude nine allocations beyond the original global-area bounds.
An independently verified equivalent representation shares exact direction
predicates across modes, removing 55,334 variables and 110,668 constraints;
all 66 originals, 394 source pair modes and original guards remain required.
The calls finish in 49.698399s and 51.313156s within their shared 60 seconds;
their 1.532948s/3.508436s soft solver overruns are preserved. Neither result
proves impossibility or supplies a native-valid target. Next independently
verify whether complement clauses can be removed under an exact existential
assignment proof before any distinct bounded call. All earlier calls remain
closed. Prior checkpoints are on main 68c82ae1; five CI jobs pass and Windows
checks are still running at the retained snapshot. Production, READMEs,
releases and the 22 reserved H2 vectors remain unchanged. H2/H5 stay open at 60%.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
if __name__=='__main__':main()
