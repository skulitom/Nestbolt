"""Seal the changed frame-side-strip core and its single complete finite contact search."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-staggered-frame-core-and-joint-contacts-20261026';OUT=ROOT/'benchmarks/results'/NAME;CORE=ROOT/'output/h5-staggered-frame-bracket-core-repaired-20261026';FAILED=ROOT/'output/h5-staggered-frame-bracket-core-20261026';POOL=ROOT/'output/h5-staggered-core-contact-pool-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-original-cog-phase-wheel-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0];assert head.startswith('c66b7522') and command(['git','rev-parse','HEAD^'])==main==previous['remote_main']=='6c5bf8782a4f748eb3c184de9b9768d34756516c'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes'];ci=json.loads(command(['gh','run','view','40343656177','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
audits={'core-builder':CORE/'checks.json','core-independent':CORE/'audit/checks.json','graph-independent':POOL/'audit-provenance-repaired/checks.json','model-independent':POOL/'model/checks.json','response':POOL/'response-audit-worker-table-repaired/checks.json'};assert all(load(p)['passed'] for p in audits.values());core=load(audits['core-independent']);graph=load(audits['graph-independent']);response=load(audits['response']);assert core['remaining_first_filled_demand_reduction_mm2']==40800 and response['status']=='INFEASIBLE' and response['closed'] and response['solver_calls']==1 and not response['stopped_after_presolve']
failures=[FAILED/'failure-review.json',POOL/'audit/failure-review.json',POOL/'response-audit/failure-review.json',POOL/'response-audit-worker-repaired/failure-review.json'];assert all(load(p)['failed'] for p in failures)
OUT.mkdir()
for label,p in audits.items():shutil.copyfile(p,OUT/(label+'-checks.json'))
for p,name in [(CORE/'placements.json','core41-placements.json'),(CORE/'anchors.json','core-anchors.json'),(CORE/'core.png','core.png'),(CORE/'audit/next-neighborhood.json','next-fixed26-neighborhood.json'),(POOL/'plan.json','contact-generation-plan.json'),(POOL/'result.json','contact-generation-result.json'),(POOL/'graph/result.json','source-graph-result.json'),(POOL/'search/result.json','closed-call-result.json'),(POOL/'search/process.json','closed-call-process.json'),(POOL/'search/solver.log','closed-call-solver.log'),(POOL/'response-audit-worker-table-repaired/worker-stats.json','worker-stats.json')]:shutil.copyfile(p,OUT/name)
for i,p in enumerate(failures):shutil.copyfile(p,OUT/f'failed-attempt-{i+1}.json')
write(OUT/'main-ci-6c5bf878-passed.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,'main_ci':40343656177,'main_ci_successful_jobs':6,'queued_previous_checkpoint':head,'next_push_commits':2,'upstream_state_reference':'benchmarks/results/h5-compact-joint-model-and-nine-insert-core-20261026/source-review.json','upstream_rechecked_this_seal':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
next_action='Preserve the checked staggered fixed26/short15 core: eighteen frames, three brackets and five inserts on the first sheet; all fifteen short originals unchanged. It moves40800mm2 of filled demand out of the remaining first-sheet area, with one insert extending10.45mm beyond the prior top. All25 movers remain mandatory: brackets23/24/27, inserts43..49, cogs51..65. The2000-pose joint contact model is CLOSED INFEASIBLE within its finite declared pool; no retry, reseed or extension. Every original conflict was reconstructed; solver search advanced beyond presolve and max_lp completed the finite exclusion. This is not a fixed26-neighborhood or arbitrary-position/angle exclusion. For next work, use a materially different source construction with movable coordinates or a changed frame/side-strip composition. In any future contact generator, distinguish boundary contacts from obstacle-interior representatives before applying quotas;277 of410 accepted non-cog obstacle proposals are interiors and are correctly incompatible with their generating cogs. Do not present them as boundary contacts. The frame-side-strip method may allow more complete bracket/insert subassemblies, but any changed geometry must be independently validated before new domains or search. Keep all66 quantities and the original material target. Preserve the old64 partial. Full source/native/material validation, production60-second integration and completeH5 matrix remain required. Main6c5bf878 passes all six checks, permitting a normal two-commit push of the queued wheel evidence and this checkpoint after exact staging/ancestry checks. H2 retains its original gate;22 reserved vectors remain untouched; no new release qualified.'
write(OUT/'next-step.json',{'action':next_action,'H2_complete':False,'H5_complete':False,'completion_percent':60})
write(OUT/'scope.json',{'fixed_first_originals':26,'fixed_short_originals':15,'core_originals':41,'mandatory_moving_counts':{'bracket':3,'insert':7,'cog':15},'all66_originals_required':True,'remaining_first_filled_demand_reduction_mm2':40800,'local_top_extension_mm':10.45,'old64_partial_preserved':True,'complete_finite_pool_status':'INFEASIBLE','unrestricted_neighborhood_excluded':False,'part_in_hole_used':False,'full66_target_witness':False,'H5_complete':False})
members={};inputs={}
for folder in [CORE,FAILED,POOL]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h;inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
helpers=list((ROOT/'output').glob('*h5_staggered*.py'))+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p
    for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members)
checks={'passed':True,'checks_passed':5,'failed_attempts_preserved':4,'new_core_originals':41,'core_pair_checks':430,'core_stock_edge_checks':164,'core_cutouts':59,'core_cutout_vertices':5074,'remaining_first_filled_demand_reduction_mm2':40800,'candidate_count':2000,'candidate_family_counts':graph['candidate_counts'],'fixed_pair_checks':52000,'unordered_candidate_pair_checks':1999000,'original_conflicts':573329,'verified_cliques':2855,'obstacle_interior_proposals':277,'conflicting_parent_edges_verified':277,'model_variables':2000,'model_constraints':2858,'closed_solver_calls':1,'status':'INFEASIBLE','returned_solve_seconds':response['returned_solve_seconds'],'shared_process_seconds':response['shared_process_seconds'],'stopped_after_presolve':False,'response_lp_iterations':1086,'finite_pool_only':True,'full66_target_witness':False,'production_and_readmes_unchanged':True,'native_calls':0,'quality_runs':0,'reserved_H2_vectors_evaluated':0,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: staggered frame strip and joint original contact search — 2026-10-26

**A changed frame arrangement fits three original brackets into the narrow side
strip and five inserts into adjacent gaps.** Its checked 41-original core reduces
remaining first-sheet filled demand by **40,800 mm²**, while one insert extends
10.45 mm beyond the prior core. The following joint search requires every remaining
part, but closes INFEASIBLE within its finite 2,000-pose pool. This is not a full
layout, a material-gate pass or an unrestricted exclusion. H2/H5 remain open at 60%.

## Source construction

Preserve the fifteen original short-sheet placements. Keep the first three
columns of four turned frames, then stagger the fourth column at 560.45 mm row
spacing. Each new gap holds a bracket foot and a 180 × 110 mm insert; the bracket's
75 mm stem occupies the unused side strip. Put the two unturned frames adjacent
at the upper left and two vertical inserts beside them. The first sheet fixes
eighteen frames, three brackets and five inserts.

Independent direct-vertex readback reconstructs all 26 first-sheet anchors from
rationals and verifies **430 filled-outer pairs, 164 stock edges, 59 cutouts and
5,074 cutout vertices** across both sheets. Minimum pair clearance is 0.225 mm
against 0.211708673 mm required; extra stock margin is 0.025 mm. All original
orientations and quantities are checked, holes remain reserved, and the short
sheet is unchanged. The earlier 64-original partial is preserved; this 41-original
core is a different starting arrangement, not a higher partial count.

![Checked original core]({NAME}/core.png)

## Complete finite joint search

All remaining **three brackets, seven inserts and fifteen cogs** are mandatory.
Four actual cog phases, eight bracket modes and two insert modes seed fresh
translation regions against the changed 26 owners. Cog centers then move
independently through 384 original pair-contact offsets; they are not forced into
a repeated lattice. A finite spatial quota limits near-duplicates. The pool has
1,400 cog poses, 300 bracket poses and 300 insert poses, with unfinished queues
and every generation event retained. Cog depths 0–3 contain 117, 651, 446 and 186
poses respectively.

The non-cog proposal helper supplies both obstacle-boundary points and interior
representatives. Of 410 accepted obstacle-derived non-cog proposals, **277 are
interior representatives**. They are valid alternatives against the fixed core,
but conflict with their generating cog pose. Every such conflict is independently
checked and retained. They must not be described as boundary contacts.

The independent source audit checks **52,000 fixed pairs, 8,000 stock edges and
all 1,999,000 unordered candidate pairs**. It reconstructs all **573,329** conflicts
and verifies their complete coverage by **2,855** original-graph cliques. No
candidate or required quantity is removed. The 2,000-variable, 2,858-constraint
model is independently reconstructed from the saved inventory and graph.

The sole call returns **INFEASIBLE** in **0.960597 returned-call seconds**, within
**2.098136 shared-process seconds**, against declared 60/90-second limits. There
is no overrun and no retry. Search proceeds beyond presolve: `default_lp` logs
6,127 branches and `no_lp` 11,174, while `max_lp` completes the finite exclusion
with 1,086 LP iterations. The returned worker's zero branch count does not mean
the entire search stopped during presolve. No separate formal unsat certificate
is claimed.

## Preserved failures and next action

Four failed attempts remain intact: the first core checker omitted mirrored
short-sheet transforms; the first graph audit assumed every obstacle-derived
proposal was a boundary contact; the first response audit mistook zero returned
branches for presolve termination; and its first repair read beyond the Search
stats table. Corrected audits retain the same source poses, conflict graph,
single solver call and response. No failed solver run was repeated.

The finite pool is closed. The next construction must change coordinates or the
frame-side-strip composition, keep all 25 remaining originals mandatory, and
rebuild current-owner geometry. Future contact generation must distinguish
interior representatives before consuming boundary-contact quotas. Full 66-part
source/native/material validation, production integration within 60 seconds and
the full H5 matrix remain required.

At {review['utc']}, all six jobs in
[main CI 40343656177](https://github.com/skulitom/Nestbolt/actions/runs/40343656177)
pass on 6c5bf878. This permits a normal two-commit checkpoint push after staging
and ancestry verification. Production and READMEs are unchanged; no new release
is qualified. H2 retains its original gate and all 22 reserved vectors remain
untouched.

All five audits pass. [Checks]({NAME}/checks.json),
[core]({NAME}/core-independent-checks.json),
[source graph]({NAME}/graph-independent-checks.json),
[model]({NAME}/model-independent-checks.json),
[response]({NAME}/response-checks.json), [scope]({NAME}/scope.json),
[next inventory]({NAME}/next-fixed26-neighborhood.json),
[next step]({NAME}/next-step.json), and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 staggered frame strip and joint contacts, 2026-10-26:** [the evidence]({link})
verifies a different 41-original core with three brackets in the frame-side strip
and five inserts in adjacent gaps. Remaining first-sheet filled demand falls by
40,800 mm²; one insert extends 10.45 mm beyond the prior top. Independent checks
cover 430 pairs, 164 stock edges and 59 cutouts/5,074 vertices. All three remaining
brackets, seven inserts and fifteen cogs stay mandatory. A fresh 2,000-pose pool
has all 1,999,000 source pairs and 573,329 conflicts independently verified.
Its single joint call closes INFEASIBLE in 0.960597 returned/2.098136 shared seconds.
Search advances beyond presolve; worker counters are reported separately.
The finite pool is closed, with no unrestricted exclusion. All five audits pass;
four failed checker attempts are preserved. Main 6c5bf878 passes all six checks,
allowing the queued two-commit push. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'checks_passed':5,'failed_attempts_preserved':4},flush=True)
