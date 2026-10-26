"""Seal the fully required17-mover joint model and its sole closed response."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-paired-strip-joint-geometry-20261026';OUT=ROOT/'benchmarks/results'/NAME;GEO=ROOT/'output/h5-paired-strip-joint-geometry-20261026';MODEL=ROOT/'output/h5-paired-strip-joint-model-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-paired-strip-clearance-capacity-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head=='183a160a3249a01a556f572c7f495c216825b3e6' and command(['git','rev-parse','HEAD^'])==main=='cb7f7b1f414c9ebeccc61873f7046bae8b024f66'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40359411459','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))};assert all(upstream[k]==previous[k] for k in upstream)
audits={'joint-geometry':GEO/'audit/checks.json','joint-model':MODEL/'model-audit/checks.json','joint-response':MODEL/'response-audit/checks.json'};assert all(load(p)['passed'] for p in audits.values());response=load(audits['joint-response']);assert response['status']=='UNKNOWN' and response['closed'] and response['all17_required'] and response['solver_calls']==1
OUT.mkdir()
for label,p in audits.items():shutil.copyfile(p,OUT/(label+'-checks.json'))
for p,name in [(GEO/'inventory.json','all66-inventory.json'),(GEO/'domains.json','29-current-cog-domains.json'),(GEO/'domain-capacities.json','domain-capacities.json'),(GEO/'unit-domain-conflicts.json','unit-domain-conflicts.json'),(GEO/'audit/necessity-proof.json','geometry-necessity-proof.json'),(MODEL/'model-audit/necessity-proof.json','model-necessity-proof.json'),(MODEL/'prepared.json','prepared-model.json'),(MODEL/'search/result.json','closed-call-result.json'),(MODEL/'search/process.json','closed-call-process.json'),(MODEL/'search/solver.log','closed-call-solver.log'),(MODEL/'response-audit/worker-stats.json','worker-stats.json')]:shutil.copyfile(p,OUT/name)
write(OUT/'main-ci-cb7f7b1f-passed.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'upstream_rechecked_this_seal':True,'main_ci':40359411459,'main_ci_successful_jobs':6,'queued_previous_checkpoint':head,'next_push_commits':2,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
next_action='The full17-mover necessary model is CLOSED UNKNOWN after60.0601769000059 returned-call seconds and60.99909879988991 shared seconds. Do not rerun, reseed, extend or treat it as a negative. It jointly requires inserts48/49 and cogs51..65 against the same34 first-sheet/15 short-sheet originals, with all original modes, complete29 cog domains, current clearance regions, source support boxes and separation necessities. No source positions or angles were found. Preserve the49 core as an optional alternative and the older64 partial. The next useful work must materially move the frame/bracket arrangement or introduce original-shape joint geometry that changes this relaxation; merely repeating necessary occupancy or timing changes will not establish a fit. Any positive must include every66 original and pass source/native/material checks before production integration in the60-second budget and the completeH5 matrix. Maincb7f7b1f now passes all six checks, allowing a normal two-commit push of queued183a160a and this evidence after staging/ancestry verification. H2 retains the original gate,22 reserved vectors remain unopened, and no new release qualifies.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'fixed_first_originals':34,'fixed_short_originals':15,'mandatory_moving_originals':[48,49,*range(51,66)],'mandatory_counts':{'insert':2,'cog':15},'all17_required':True,'all66_accounted_once':True,'all_original_insert_modes':True,'continuous_positions_and_free_cog_angles_relaxed':True,'necessary_only':True,'status':'UNKNOWN','fixed34_neighborhood_excluded':False,'source_witness_found':False,'full66_target_witness':False,'H5_complete':False})
members={};inputs={}
for folder in [GEO,MODEL]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
helpers=list((ROOT/'output').glob('*h5_paired_strip_joint*.py'))+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
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
checks={'passed':True,'audits_passed':3,'failed_checker_attempts':0,'merged_domains':29,'input_lattice_rectangles':1067,'integer_union_atoms':3632,'insert_modes':4,'fractional_anchor_corners':16,'exact_interval_edge_tests':64,'fixed_clearance_boxes':24,'domain_conflicts':85,'model_variables':8440,'model_constraints':10044,'mandatory_inserts':2,'mandatory_cogs':15,'all17_required':True,'all66_accounted_once':True,'cog_pairs':105,'cog_insert_circle_pairs':30,'support_strips':60,'support_vertex_boxes':840,'solver_calls':1,'status':'UNKNOWN','returned_solve_seconds':response['returned_solve_seconds'],'shared_process_seconds':response['shared_process_seconds'],'returned_soft_overrun_seconds':response['returned_soft_overrun_seconds'],'returned_worker_branches':response['returned_worker_branches'],'returned_worker_conflicts':response['returned_worker_conflicts'],'full66_target_witness':False,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: joint insert/cog geometry for the paired strip — 2026-10-26

**The joint model now requires both remaining inserts and all fifteen cogs.**
Its full geometry and model audits pass, but the single bounded call closes
UNKNOWN after search. It provides no source placement or neighborhood exclusion.
H2/H5 remain open at 60% by completed milestone weights.

## Complete current-owner geometry

Keep the checked 34-original first-sheet core and all fifteen short-sheet
originals. Inserts48/49 and cogs51..65 remain mandatory, accounting for every
one of the 66 originals once. No previously fixed owner is silently moved.

The prior exact clipped footprints contain 1,067 integer rectangles. Coalescing
only matching transverse intervals with overlapping or adjacent integer extents
reduces these to **29 domains**. Independent partitioning verifies **3,632 integer
atoms**, proving exact coverage of each assigned union. No possible floor-rounded
cog center is lost. Integer tiles with diagonal below the certified 254.297 mm
separation give valid domain capacities, while exact farthest corners prove
**85 conflicts** among capacity-one domains.

Each insert may use all four original quarter turns and a continuous ideal
anchor represented by its integer floor. Fresh exact trigonometric intervals
check **16 corners and 64 source edges** across every fractional anchor in
closed [0,1]² micrometres. A 4-micrometre inset keeps each model rectangle inside
its true filled outer; a 20-micrometre outward stock relaxation covers rounding
and angle error. The two moving inner rectangles and **24 current required-clearance
regions** obey global two-dimensional nonoverlap. Only intrinsic shape certificates
are reused; older fixed-owner coordinates are not transferred.

Each insert inner rectangle contains a circle of radius 54.996 mm. Together with
the cog's certified 109.115 mm inner disk and rounding allowance, this requires
at least 164.109 mm between the rounded cog center and the insert's model-circle
center. Exact scaling and downward facet rounding keep a 32-gon inside that
forbidden disk. The original certified 32-gon supplies the 254.297 mm cog/cog
necessity. Both are permissive bounds, not substitute source shapes.

## Full joint model audit

| Required relation | Count |
| --- | ---: |
| Mandatory inserts / cogs | 2 / 15 |
| Cog choices among complete domains | 435 |
| Cog/cog separation pairs | 105 |
| Cog/insert inner-circle pairs | 30 |
| Cog/insert support strips | 60 |
| Exact rational support-vertex boxes | 840 |

The model has **8,440 variables and 10,044 constraints**, with no objective or
hints. The independent auditor reconstructs every variable domain, mode table,
interval, stock row, occupancy count, conflict and outside-box/facet choice by
semantic name, without trusting the saved mapping. It checks integer arithmetic
bounds and the solver's actual import/export. Equal copies may be relabelled in
nondecreasing X, preserving feasible source geometry. All seventeen movers are
required throughout; the inserts are no longer omitted from this necessary test.

## One closed call

The sole 60-second solver call, inside 90 shared seconds, returns **UNKNOWN**.
Internal solver time is **60.052053 seconds**, returned-call time **60.060177
seconds**, and total shared-process time **60.999099 seconds**. Internal/returned
soft overruns of 0.052053/0.060177 seconds are preserved; the shared limit is
honored. Search advances beyond presolve, with all three primary workers
recording branches. The returned worker reports **1,526,058 branches and 250,475
conflicts**. Separate worker counters and the original response remain archived.

There is no solution assignment, source witness or formal unsat certificate.
The call is closed: no retry, reseed or extension. A future positive necessary
result would still need actual original cog angles, guarded source geometry,
full66 native/material validation, production integration within 60 seconds and
the complete H5 matrix. The next useful construction must change the core or
introduce materially different original-shape joint geometry. Preserve the
earlier 64-original partial and the alternative 49-original core.

## Repository and evidence

All three audits pass, with no failed checker attempts. At {review['utc']},
[all six checks on main cb7f7b1f](https://github.com/skulitom/Nestbolt/actions/runs/40359411459)
pass. This permits a normal two-commit push of the queued 183a160a checkpoint and
this evidence after staging and ancestry checks. Upstream heads and releases
remain unchanged. Production and READMEs are unchanged; no new release qualifies.
H2 retains its original gate and all 22 reserved vectors remain untouched.

[Checks]({NAME}/checks.json), [geometry]({NAME}/joint-geometry-checks.json),
[model]({NAME}/joint-model-checks.json), [response]({NAME}/joint-response-checks.json),
[geometry proof]({NAME}/geometry-necessity-proof.json),
[model proof]({NAME}/model-necessity-proof.json), [scope]({NAME}/scope.json),
[inventory]({NAME}/all66-inventory.json), [next step]({NAME}/next-step.json),
and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 complete joint insert/cog necessities, 2026-10-26:** [the evidence]({link})
retains every source cog center in29 exact merged domains, independently checking
3,632 integer atoms. All four insert modes pass16 corner and64 exact edge tests.
Both remaining inserts and all fifteen cogs are mandatory in the independently
reconstructed8,440-variable/10,044-constraint model. Current clearance regions,
105 cog pairs,30 cog/insert circle pairs,60 support strips and840 support-vertex
boxes supply necessary geometry. The sole call closes UNKNOWN after search in
60.060177 returned/60.999099 shared seconds, with its0.060177-second soft overrun
preserved. The returned worker records1,526,058 branches and250,475 conflicts.
No source witness or exclusion is claimed; the call is closed. All three audits
pass. Maincb7f7b1f now passes all six checks, allowing a normal two-commit push.
H2/H5 remain open at60%; production, READMEs, releases and all22 reserved H2
vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'audits_passed':3,'previous_main_ci_successful_jobs':6,'next_push_commits':2})
