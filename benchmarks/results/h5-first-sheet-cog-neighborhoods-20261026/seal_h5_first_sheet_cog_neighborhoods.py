"""Preserve three closed first-sheet neighborhoods and global source area bounds."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-first-sheet-cog-neighborhoods-20261026';OUT=ROOT/'benchmarks/results'/NAME;CAP=ROOT/'output/h5-source-area-caps-20261026';REVIEW=ROOT/'output/h5-first-sheet-source-review-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    review=load(REVIEW/'review.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();assert head==review['source_head']=='336440d57a2bac912b81efa432a62bd7834817c6'
    assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items()) and review['main_ci_successful_jobs']==6 and review['main_ci_conclusion']=='success'
    cases=[];bases=[];OUT.mkdir()
    for name,suffix,status in [('pair','4-5','INFEASIBLE'),('three','4-5-6','INFEASIBLE'),('four','3-4-5-6','UNKNOWN')]:
        root=ROOT/f'output/h5-first-{name}-regions-20261026';reg=root/f'release-{suffix}';model=ROOT/f'output/h5-first-{name}-source-model-20261026';run=ROOT/f'output/h5-first-{name}-source-search-20261026';bases.extend([root,model,run])
        region=load(reg/'result.json');ra=load(reg/'audit/checks.json');mr=load(model/'result.json');ma=load(model/'audit/checks.json');sa=load(run/'search-audit/checks.json')
        assert region['planned_domains']==3523 and region['pending_domains']==0 and not region['cap_reached'] and ra['passed'] and ma['passed'] and ma['exact_parent_restored'] and sa['passed'] and sa['terminal_status']==status and sa['solver_calls']==1 and sa['shared_budget_honored']
        dest=OUT/name;dest.mkdir()
        copies={reg/'result.json':'region-result.json',reg/'summary.json':'region-queries.json',reg/'audit/checks.json':'region-audit.json',reg/'audit/conditional-region-summary.json':'conditional-regions.json',model/'result.json':'model-result.json',model/'audit/checks.json':'model-audit.json',run/'shared-search/result.json':'shared-search-result.json',run/'shared-search/solve/result.json':'solver-result.json',run/'shared-search/solve/model-audit.json':'actual-model-audit.json',run/'search-audit/checks.json':'closed-search-audit.json'}
        for a,b in copies.items():shutil.copyfile(a,dest/b)
        cases.append({'case':name,'released_parts':region['released_cog_parts'],'movers':ma['moving_originals'],'fixed':ma['fixed_originals'],'region_seconds':region['seconds'],'region_audit_seconds':ra['seconds'],'residual_domains':region['residual_domains'],'residual_fragments':region['residual_fragments'],'lower_dimensional_fragments':region['lower_dimensional_residuals'],'model_constraints':mr['constraints'],'fixed_coordinate_equalities':mr['appended_coordinate_equalities'],'empty_domain_exclusions':mr['appended_empty_domain_exclusions'],'nonempty_physical_domains_retained':mr['retained_domain_flags'],'terminal_status':status,'solver_seconds':sa['actual_solver_seconds'],'shared_seconds':sa['actual_shared_seconds'],'soft_limit_overshoot_seconds':sa['solver_soft_limit_overshoot_seconds']})
    ca=load(CAP/'audit-provenance-repaired/checks.json');assert ca['passed'] and ca['excluded_all_nine_allocations']==28 and ca['no_cog_witness_pose_assumed'];bases.extend([CAP,REVIEW]);write(OUT/'case-comparison.json',cases)
    for a,b in [(CAP/'result.json','area-result.json'),(CAP/'audit-provenance-repaired/checks.json','area-audit.json'),(CAP/'audit-provenance-repaired/verified-capacity-inequalities.json','verified-area-inequalities.json'),(CAP/'audit-provenance-repaired/all-nine-sheet-allocations.json','all-nine-sheet-allocations.json'),(CAP/'audit/provenance-repair.json','area-provenance-repair.json'),(REVIEW/'review.json','repository-review.json'),(REVIEW/'main-ci.json','prior-main-ci.json')]:shutil.copyfile(a,OUT/b)
    action=('All three distinct first-sheet focus calls are closed: original57/58 is INFEASIBLE;57/58/62 is INFEASIBLE; all54/57/58/62 is UNKNOWN, not impossible. The last call exceeded its45-second soft solver limit by0.682462s but stayed within60 shared seconds. Never restart, extend or reseed any of them. The source-area audit independently verifies14 necessary family-subset area inequalities conditional only on all recorded source domains/profiles and fixed57, without any witness cog pose. They reject28 of42 all-nine sheet allocations by area alone; remaining allocations are not proved feasible. Two brackets plus two cogs on sheet2 demand at least180124mm2 against an upper174476mm2. The seven-first-sheet case remains area-possible (300048 versus342722mm2). Next build a distinct full nine-mover model from the original output/h5-bounded-source-model-20261026 parent, not any focused model: preserve all167044 variables,376363 constraints and72 hints, append exactly the14 verified integer area inequalities using every matching part/query sheet-mode activation. Do not add fixed witness coordinates or focused conditional domain exclusions. Verify all coefficients, units, activations, source provenance and complete parent restoration, then actual solver import/export, before a separately budgeted one-shot bounded call. This is added global source-region propagation, not continuation of a completed search. If a candidate exists, require all66 original shapes/cutouts/counts, native-clearance/material checks and native validation; production integration and the full13-job/two-kerf H5 matrix remain necessary. Offline preparation is not production qualification. H2 retains its original gate and22 reserved vectors untouched. Prior main822a5f67 CI40248595273 has all6 jobs successful; commit this checkpoint and normally push all4 local checkpoints with fresh ancestry/remote verification. No new release is qualified.')
    write(OUT/'next-step.json',{'action':action,'source_parent':'output/h5-bounded-source-model-20261026','new_verified_inequalities':14,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),**review,'new_solver_calls':3,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'README_change_needed':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for base in bases:
        for p in base.rglob('*'):
            if p.is_file():members[base.name+'/'+p.relative_to(base).as_posix()]=p
        for p in base.rglob('plan.json'):
            for n,h in load(p).get('inputs',{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in load(ROOT/'output/h5-single-cog-release-20261026/audit-recovered/witness-source-provenance.json')['inputs'].items():inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for name in ['h5-bounded-source-search-20261026','h5-fixed-six-completion-20261026','h5-guarded-cell-search-20261025','h5-guarded-source-adjustment-20261025']:
        p=ROOT/'benchmarks/results'/name/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    p=ROOT/'output/h5-fixed-six-completion-20261026/audit/provenance-repair.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['prepare_h5_first_pair_regions.py','prove_h5_first_pair_regions.py','audit_h5_first_pair_regions.py','prepare_h5_first_pair_model_helpers.py','prepare_h5_first_pair_source_model.py','audit_h5_first_pair_source_model.py','prepare_h5_first_pair_search_runner.py','run_h5_first_pair_source_search.py','prepare_h5_first_pair_search_audit.py','audit_h5_first_pair_source_search.py','certify_h5_source_area_caps.py','audit_h5_source_area_caps.py','repair_h5_source_area_cap_provenance.py','audit_h5_source_area_caps_repaired.py','prepare_h5_first_sheet_checkpoint_review.py','retain_h5_stop_rule_metadata.py','prove_h5_two_cog_regions.py','audit_h5_two_cog_regions.py','prepare_h5_two_cog_fixed_source_model.py','audit_h5_two_cog_fixed_source_model.py','run_h5_two_cog_fixed_source_search.py','audit_h5_bounded_source_search.py','pack_h5_evidence_archive.py','ccd1.py']
    for name in ['three','four']:names += [f'prepare_h5_first_{name}_helpers.py',f'prove_h5_first_{name}_regions.py',f'audit_h5_first_{name}_regions.py',f'prepare_h5_first_{name}_source_model.py',f'audit_h5_first_{name}_source_model.py',f'prepare_h5_first_{name}_search_helpers.py',f'run_h5_first_{name}_source_search.py',f'audit_h5_first_{name}_source_search.py']
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
    write(OUT/'checks.json',{'passed':True,'all10569_region_domain_cases_independently_replayed':True,'all_three_complete_parent_models_preserved':True,'three_distinct_single_calls_closed':True,'all_actual_models_parameters_and_timing_verified':True,'unknown_not_claimed_infeasible':True,'soft_limit_overrun_preserved':True,'all14_source_area_inequalities_independently_verified':True,'exact_area_proof_uses_no_witness_cog_position':True,'area_provenance_lookup_failure_and_repair_preserved':True,'all_six_prior_main_ci_jobs_passed':True,'production_and_readmes_unchanged':True,'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
    table='\n'.join(f"| {label} | {r['movers']} / {r['fixed']} | {r['residual_domains']:,} / {r['residual_fragments']:,} | {r['terminal_status']} | {r['solver_seconds']:.6f} / {r['shared_seconds']:.6f} |" for label,r in zip(['57, 58','57, 58, 62','54, 57, 58, 62'],cases))
    report=f'''# H5: first-sheet neighborhoods and source area capacities — 2026-10-26

**Two focused cases returned INFEASIBLE; freeing all four first-sheet cogs
remains unresolved (UNKNOWN).** Separately, 14 independently verified area
bounds exclude 28 of 42 sheet allocations for all nine moving originals,
without fixing any witness cog position. No full target layout is obtained.
H2/H5 remain open at **60%** completed milestone weight.

## Three distinct neighborhoods, all originals retained

Each case keeps the two second-sheet cog witnesses and progressively releases
two, three and all four first-sheet cogs. Both brackets 28/29, insert 50 and
every released cog remain mandatory. All 66 original parts, shapes, source
orientations/domains, native guards and material target remain unchanged.

| Released original cogs | Movers / fixed | Residual domains / fragments | Status | Solver / total seconds |
|---|---:|---:|---|---:|
{table}

Each region census examines all 20 queries and 3,523 source domains, for
**10,569 complete cases**. Separate rational clipping audits verify every
source clause, domain and boundary, including 114/74/0 line or point fragments
respectively. All moving parts must use the first sheet under these fixed
witness poses. The four-cog case retains every original first-sheet domain.

Each focused model preserves the entire previously audited parent: 167,044
variables, 376,363 constraints and 72 advisory hints. Only exact fixed-cog
coordinates and independently proved empty-domain flags are appended. The
three cases add 8/6/4 coordinate equalities and 5,964/3,524/407 domain exclusions.
Independent audits reconstruct every addition and recover the full parent
exactly; actual solver import/export matches. Parent copy-order restrictions
remain, so solver negatives are conditional construction results, not
independent unrestricted geometry proofs. No earlier focused exclusion is
transferred to a case that moves its fixed witness.

Each distinct call has eight workers, seed zero, a 45-second solver limit and
a 60-second total import/audit/search budget with a ten-second shutdown reserve.
All calls are closed. The last call reports **UNKNOWN**, exceeds its soft
solver limit by **0.682462s**, and finishes within the shared budget at
**48.884638s**. That overrun is retained. No candidate, native validation or
quality run occurs; no call is restarted, extended or reseeded.

## Necessary area bounds independent of cog witnesses

For each sheet and each nonempty subset of bracket/insert/cog families,
enclose every source-domain anchor box plus every profile vertex. Round the
combined bounds outward to whole millimetres and pad another millimetre on
every side. All corresponding filled outer profiles lie inside this rectangle.
Subtract only **floored exact clipped areas** of the disjoint 57 fixed original
polygons. Use conservative family area lower bounds of **40,000 / 19,800 /
50,062 mm²**. Part-in-hole remains off.

The producer clips signed polygon-fan triangles with rational arithmetic.
The independent reader clips whole polygons directly, with no producer
clipping code, and obtains exactly the same rational areas. GEOS cross-checks
399 clipped areas (maximum difference **1.10e-11 mm²**); all 1,246 fixed-pair
clearance checks pass. All 3,523 domains and 77,220 translated profile vertices
are checked against committed source bytes.

The resulting **14 necessary inequalities** exclude **28 of 82** individual
sheet count cases and **28 of 42** complementary allocations of all nine
moving originals. The remaining allocations are not proved feasible.
Two brackets plus two cogs on sheet 2 require at least **180,124 mm²**, exceeding
their **174,476 mm²** available upper bound by **5,648 mm²**. The seven-mover
first-sheet case is not excluded by area: demand **300,048 mm²**, upper capacity
**342,722 mm²**. Thus the UNKNOWN result stays unresolved.

The initial area audit stopped at a provenance lookup for the fixed-geometry
audit. A separate repair resolves that exact file in its original committed
archive and preserves the initial source/plan/failure record. No completed
area computation or solver is repeated.

## Next construction and repository state

Build a distinct **full nine-mover** model from the original complete-source
parent, adding exactly these 14 verified count inequalities. Keep all 66
originals and 57 source placements, and leave every cog movable. Do not inherit
fixed witness coordinates or focused domain exclusions. Independently verify
coefficients, units, sheet activations and complete parent restoration before
another separately budgeted call. This adds source-region propagation to the
global construction; it does not continue a closed search.

A full original-geometry/native-valid target, production integration and the
complete 13-job/two-kerf H5 matrix remain required. Offline preparation is not
production-budget qualification. H2 retains its original gate and all 22 reserved
vectors untouched. Source code, READMEs, preview v0.2.0-alpha.1 and stable Latest
v0.1.0 remain unchanged; no new release is qualified.

Fresh repository/upstream checks preserve main 822a5f67 and unchanged Sparrow
and Studio heads; Studio has no published release. All **six** jobs in
[main CI 40248595273](https://github.com/skulitom/Nestbolt/actions/runs/40248595273)
have passed. This checkpoint is ready for a normal main push with the three
queued checkpoints, after fresh ancestry and remote-ref verification.

Evidence: [case comparison]({NAME}/case-comparison.json),
[area audit]({NAME}/area-audit.json),
[verified inequalities]({NAME}/verified-area-inequalities.json),
[42 complete allocations]({NAME}/all-nine-sheet-allocations.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
**{archive['archive_members']:,}** canonical files and **{archive['verified_aliases']:,}**
exact-content aliases are size/SHA-256/CRC verified across
**{archive['archive_parts']}** independently readable archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 first-sheet neighborhoods and area capacities, 2026-10-26:** [the evidence]({link})
retains three distinct original-part searches: cogs 57/58 and 57/58/62 return
INFEASIBLE; all four first-sheet cogs return UNKNOWN. Every region and focused
model is independently audited, with all 66 originals retained. The UNKNOWN
call's 0.682462s soft-limit overrun is preserved; total time is 48.884638s within
the shared 60 seconds. All calls are closed. Separate exact area proofs yield
14 necessary source-region inequalities, independent of cog witness poses,
excluding 28 of 42 all-nine sheet allocations. Two brackets plus two cogs
cannot share sheet 2 in these source domains (180,124 versus 174,476 mm²);
the seven-part first-sheet case remains unresolved. Next add the verified
inequalities to the full nine-mover source model, with no focused witness locks
or exclusions. Original/native target, production integration and the complete
H5 matrix remain required. All six prior main checks pass; the queued batch is
ready for a normal push. H2/H5 remain open at 60%; original limits, production,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'prior_main_ci_successes':6},flush=True)
if __name__=='__main__':main()
