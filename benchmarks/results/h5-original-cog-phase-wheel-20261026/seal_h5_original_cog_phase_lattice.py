"""Seal the closed finite phase construction and its independent local certificate."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-original-cog-phase-wheel-20261026';OUT=ROOT/'benchmarks/results'/NAME;BASE=ROOT/'output/h5-original-cog-phase-lattice-20261026';SYNC=ROOT/'output/h5-compact-joint-nine-core-main-sync-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
old=load(ROOT/'output/h5-compact-joint-nine-core-review-20261026/review.json');receipt=load(SYNC/'receipt.json');head=command(['git','rev-parse','HEAD']);remote=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head==remote==receipt['head']=='6c5bf8782a4f748eb3c184de9b9768d34756516c' and receipt['normal_fast_forward_push'] and receipt['previous_ci_successful_jobs']==6
assert source_digest()==old['production_digest'] and {n:digest(ROOT/n) for n in old['current_readmes']}==old['current_readmes']
audits=['geometry-audit/checks.json','model/checks.json','response-audit/checks.json','wheel-audit/checks.json'];assert all(load(BASE/n)['passed'] for n in audits)
response=load(BASE/'response-audit/checks.json');wheel=load(BASE/'wheel-audit/checks.json');assert response['status']=='INFEASIBLE' and response['solver_calls']==1 and response['closed'] and response['wheel_closing_states']==[0]*5 and wheel['all_complete_wheel_assignments']==0 and wheel['distance_entries_between_native_gap_and_construction_gap']==0
ci=json.loads(command(['gh','run','view','40343656177','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==head
OUT.mkdir()
for n in audits:shutil.copyfile(BASE/n,OUT/n.replace('/','-'))
for n,d in [('plan.json','construction-plan.json'),('result.json','geometry-result.json'),('search/result.json','closed-call-result.json'),('search/process.json','closed-call-process.json'),('search/solver.log','closed-call-solver.log'),('response-audit/wheel-summary.json','wheel-summary.json'),('response-audit/triangle-supports.json','triangle-supports.json')]:shutil.copyfile(BASE/n,OUT/d)
shutil.copyfile(SYNC/'receipt.json',OUT/'main-push-receipt.json');write(OUT/'main-ci-6c5bf878-observed.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':remote,'production_digest':old['production_digest'],'current_readmes':old['current_readmes'],'production_and_readmes_unchanged':True,'upstream_state_reference':'benchmarks/results/h5-compact-joint-model-and-nine-insert-core-20261026/source-review.json','upstream_rechecked_this_seal':False,'previous_main_ci':40336537934,'previous_ci_successful_jobs':6,'current_ci':40343656177,'current_ci_status':ci['status'],'current_ci_successful_jobs':sum(j['conclusion']=='success' for j in ci['jobs']),'H2_complete':False,'H5_complete':False,'completion_percent':60,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
next_action='The five declared triangular pitches260/262/264/266/268mm with36 original half-degree phases are CLOSED. No retry, reseed, extension or unreviewed phase/pitch sweep. A direct finite seven-cog wheel certificate explains the negative result; it is not an arbitrary-angle or fixed27-neighborhood exclusion. The42-original fixed27/short15 core remains available, with all six brackets18/19/20/23/24/27,three inserts47/48/49 and fifteen cogs51..65 required. The next constructive formulation should change the contact graph by allowing individual cog-center motion and couple it to all nine remaining non-cogs, using fresh current-owner source geometry. Do not assume a rigid repeated cog lattice merely because pair and triangle contacts exist. Do not claim the historical three-column/six-row wide-frame core with eleven side inserts as new: its finite search and limits are retained in h5-wide-small-selection-20261023. All earlier fixed24 compact and finite graph calls remain closed. Preserve the earlier64-original partial. Complete66 original/native/material validation, production60-second integration and fullH5 matrix remain required. Main6c5bf878 is verified pushed after all six preceding main checks passed. Queue this new evidence checkpoint while its current CI runs. H2 original gate and22 reserved vectors remain unchanged; no new release qualified.'
write(OUT/'next-step.json',{'action':next_action,'H2_complete':False,'H5_complete':False,'completion_percent':60})
write(OUT/'scope.json',{'finite_pitches_mm':[260,262,264,266,268],'finite_angles_degrees':[i/2 for i in range(36)],'construction_gap_mm':.225,'original_cogs_required_by_phase_model':15,'noncogs_not_in_phase_model_but_required_for_full_layout':{'bracket':6,'insert':3},'seven_cog_wheel_indices':[6,7,12,11,5,1,2],'unrestricted_angle_exclusion':False,'unrestricted_position_exclusion':False,'fixed27_neighborhood_excluded':False,'old64_partial_preserved':True,'full66_target_witness':False,'H5_complete':False})
members={BASE.name+'/'+p.relative_to(BASE).as_posix():p for p in BASE.rglob('*') if p.is_file()}
inputs={}
for record in [load(BASE/'plan.json'),load(BASE/'model/checks.json')]:
    for n,h in record['inputs'].items():assert digest(ROOT/n)==h;inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
for folder,names in [('h5-central-nine-insert-core-20261026',['placements.json','anchors.json','checks.json','audit/checks.json','audit/next-neighborhood.json']),('h5-compact-joint-nine-core-main-sync-20261026',['receipt.json','prior-ci.json','push.json','remote-after.json']),('h5-compact-joint-nine-core-review-20261026',['review.json'])]:
    for n in names:p=ROOT/'output'/folder/n;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
for n in ['build_h5_original_cog_phase_lattice.py','audit_h5_original_cog_phase_lattice.py','prepare_h5_original_cog_phase_lattice.py','run_h5_original_cog_phase_lattice.py','audit_h5_original_cog_phase_response.py','check_h5_finite_cog_wheel.py','push_h5_compact_joint_nine_core_checkpoint.py','ccd1.py','pack_h5_evidence_archive.py',Path(__file__).name]:members['helpers/'+n]=ROOT/'output'/n
archive,manifest=pack(ROOT,OUT,NAME,members)
checks={'passed':True,'checks_passed':4,'source_pair_reconstructions':194400,'near_pairs_verified':30,'far_pairs_verified':75,'tables_verified':15,'model_variables':16,'model_constraints':30,'closed_solver_calls':1,'status':'INFEASIBLE','solver_wall_seconds':response['solver_wall_seconds'],'returned_solve_seconds':response['returned_solve_seconds'],'shared_process_seconds':response['shared_process_seconds'],'soft_overruns':False,'triangle_assignment_counts':response['finite_triangle_counts'],'wheel_closing_states':[0]*5,'independent_enumeration_prefixes':618,'exact_reachability_records':458,'unrestricted_exclusion':False,'complete_target_witness':False,'main_push_verified':True,'production_and_readmes_unchanged':True,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: original-cog phases and a finite seven-cog obstruction — 2026-10-26

**The declared 15-cog triangular-grid construction is infeasible at all five
tested pitches and 36 tested angles.** An independent enumeration explains
the result with seven cogs: their contact constraints cannot all hold together.
This closes one finite construction, not the full placement problem. All six
remaining brackets and three inserts still require placement. H2/H5 remain
open at **60%** by completed milestone weights.

## Declared construction and source geometry

Keep the checked 27 first-sheet originals and fifteen short-sheet originals.
Require all fifteen remaining cogs in three staggered rows of five. Test
pitches 260, 262, 264, 266 and 268 mm, with each cog independently choosing an
actual original rotation from 0° through 17.5° in 0.5° increments. No exact
tooth symmetry is assumed. This phase-only preparation excludes all nine
remaining non-cogs from the model; they remain mandatory before any full-layout
claim. No old owner-dependent domains are reused.

The constructor computes **19,440 original-outline pair distances** across
fifteen pitch/direction tables. The independent audit rebuilds the actual source
vertex transforms for **194,400 near-pair angle combinations**, covering all
thirty near neighbors at all five pitches. The largest difference caused by
translating those reconstructed shapes is below 9 × 10⁻¹³ mm. The other 75
pairs have center separation greater than twice the verified 140.001 mm source
radius plus the construction clearance. All 105 cog pairs are accounted for.

The construction uses 0.225 mm clearance. No saved distance falls between the
required native guard clearance and 0.225 mm, so changing between these two
thresholds would not change these finite compatibility tables.

## One call and an independently checked explanation

The model has **16 variables and 30 compatibility constraints**: one pitch and
fifteen independent angles. A separate protobuf reconstruction verifies every
variable domain and allowed tuple, with no objective or hint.

The sole call closes **INFEASIBLE** during presolve. Internal solver time is
**{response['solver_wall_seconds']:.6f} seconds**, returned-call time
**{response['returned_solve_seconds']:.6f} seconds**, and shared-process time
**{response['shared_process_seconds']:.6f} seconds**. The declared limits are
20 solver seconds and 30 shared seconds; neither is exceeded. No retry,
reseed or extension is permitted for this closed construction.

A single triangle admits respectively **0, 0, 8, 28 and 124** phase assignments
at the five pitches. Pair or triangle feasibility therefore does not establish
feasibility of a repeated grid. For the seven-cog wheel centered on lattice node
6, every pitch has zero closing assignments. A dynamic-programming certificate
contains **458** reachability records. An independent depth-first enumeration
of **618** prefixes reproduces every record exactly and finds zero complete
wheel assignments. This also explains the 15-cog model's negative result
without relying solely on its solver status.

The certificate covers only the declared positions and finite angles. It does
not exclude continuous rotation, independent center shifts, a different contact
graph, or the fixed27 neighborhood. No original layout, native validation,
material improvement or production-budget qualification follows from it.

## Next work and repository checkpoint

The next construction must allow different cog contacts and couple them to all
six remaining brackets and three inserts. Use fresh current-owner geometry.
The 42-original core and earlier 64-original partial remain preserved. Full66
source/native/material validation, production integration and the complete H5
matrix remain required. The older wide-frame grid and eleven-insert side strip
already have retained finite-search evidence; they must not be presented as new.

Commit **6c5bf878** is verified on `main`, pushed normally after all six jobs in
[the preceding CI run](https://github.com/skulitom/Nestbolt/actions/runs/40336537934)
passed. At {review['utc']}, its
[new CI run](https://github.com/skulitom/Nestbolt/actions/runs/40343656177)
is {ci['status']}, with {review['current_ci_successful_jobs']} successful jobs.
Queue this new evidence checkpoint until that run finishes successfully.
Production and README digests are unchanged; no new release is qualified.
H2 retains its original gate and all 22 reserved vectors remain untouched.

All four audits pass. [Checks]({NAME}/checks.json),
[geometry]({NAME}/geometry-audit-checks.json),
[model]({NAME}/model-checks.json),
[response]({NAME}/response-audit-checks.json),
[independent wheel enumeration]({NAME}/wheel-audit-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json), and
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
aliases by exact bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 finite cog-phase obstruction, 2026-10-26:** [the evidence]({link})
checks all fifteen required cogs on five declared triangular pitches with36
original half-degree angles. Independent source reconstruction verifies194,400
near-pair combinations. The16-variable/30-constraint phase model closes
INFEASIBLE in0.170663 returned-call/1.124359 shared seconds, within20/30 limits.
An independent enumeration of618 prefixes reproduces458 reachability records:
the contained seven-cog wheel has no assignment at any tested pitch, although
some triangles fit. This excludes only the finite construction; arbitrary
angles, moved centers and the fixed27 neighborhood remain open. All six
brackets, three inserts and fifteen cogs stay required for the complete layout.
All four audits pass. Main6c5bf878 was pushed after all six prior checks passed;
its new CI is running, so queue this checkpoint. H2/H5 remain open at60%;
production, READMEs, releases and all22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'checks_passed':4,'current_ci_status':ci['status']},flush=True)
