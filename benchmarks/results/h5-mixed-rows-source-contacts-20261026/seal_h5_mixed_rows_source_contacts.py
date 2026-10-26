"""Seal a changed source arrangement and its closed all-required joint search."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,math,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-mixed-rows-source-contacts-20261026';OUT=ROOT/'benchmarks/results'/NAME;CORE=ROOT/'output/h5-mixed-rows-core-20261026';POOL=ROOT/'output/h5-mixed-rows-contact-pool-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-paired-strip-joint-geometry-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head==main=='e158daa2b8f0c51399a26769cd05f6d470d664ec'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40365489221','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and len(ci['jobs'])==6 and all(j['conclusion'] in ['', 'success'] for j in ci['jobs']);ci_success=sum(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))};assert all(upstream[k]==previous[k] for k in upstream)
audits={'core':CORE/'audit/checks.json','source-graph':POOL/'audit/checks.json','model':POOL/'model/checks.json','response':POOL/'response-audit-log-precision-repaired/checks.json'};assert all(load(p)['passed'] for p in audits.values());response=load(audits['response']);assert response['status']=='UNKNOWN' and response['closed'] and response['all33_movers_required'] and response['solver_calls']==1
shortplan=ROOT/'output/h5-nine-insert-short-sheet-20261026/plan.json';sp=load(shortplan);source_names=['output/h5-source-orientation-construction-20261025/items.json','output/h5-source-orientation-construction-20261025/geometry.json'];assert all(digest(ROOT/n)==sp['inputs'][n] for n in source_names)
OUT.mkdir()
for label,p in audits.items():shutil.copyfile(p,OUT/(label+'-checks.json'))
for p,name in [(CORE/'audit/next-neighborhood.json','all66-inventory.json'),(CORE/'audit/historical-comparison.json','historical-frame-comparison.json'),(CORE/'visual/core.png','core.png'),(POOL/'plan.json','candidate-plan.json'),(POOL/'result.json','candidate-result.json'),(POOL/'graph/result.json','initial-graph-result.json'),(POOL/'fast-cover/checks.json','fast-cover-checks.json'),(POOL/'search/result.json','closed-call-result.json'),(POOL/'search/process.json','closed-call-process.json'),(POOL/'search/solver.log','closed-call-solver.log'),(POOL/'response-audit-log-precision-repaired/worker-stats.json','worker-stats.json'),(POOL/'response-audit/failure.json','preserved-auditor-failure.json')]:shutil.copyfile(p,OUT/name)
write(OUT/'main-ci-e158daa2-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40365489221,'main_ci_successful_jobs_at_seal':ci_success,'push_waits_for_all_six_success':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False};write(OUT/'source-review.json',review)
next_action='The changed mixed-row18-frame/short15 core and complete finite4200-pose joint model are CLOSED UNKNOWN, not excluded. Do not retry, reseed or extend this call. Preserve the33-core alternative, both older64-original partials and all failed or unresolved evidence. Future work needs a materially different construction or a demonstrated source-geometric mechanism for completing the original66, rather than another unchanged finite pool or occupancy retry. The mixed-row core exposes a lower top but narrows the lower side strip; neither greater usable capacity nor a better partial score has been established. A valid full66 source/native/material witness must precede production integration within60 seconds and the complete H5 matrix. Keep the current main CI running; push the next checkpoint only after all six checks succeed. H2 retains its original gate and22 reserved vectors stay unopened. No new release is qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'fixed_first_originals':18,'fixed_short_originals':15,'mandatory_counts':{'bracket':6,'insert':12,'cog':15},'all33_movers_required':True,'all66_accounted_once':True,'cog_phases_degrees':[0,4.5,9,13.5],'bracket_modes':8,'insert_outer_orientation_classes':2,'finite_source_pool':True,'status':'UNKNOWN','unrestricted_source_exclusion':False,'source_witness_found':False,'H5_complete':False})
members={};inputs={}
for folder in [CORE,POOL]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n,h in load(CORE/'audit/historical-comparison.json')['inputs'].items():assert digest(ROOT/n)==h;inputs[n]=h
for n in source_names:inputs[n]=sp['inputs'][n]
inputs[shortplan.relative_to(ROOT).as_posix()]=digest(shortplan)
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=list((ROOT/'output').glob('*h5_mixed_rows*.py'))+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',ROOT/'output/build_h5_staggered_core_contact_pool.py',ROOT/'output/build_h5_staggered_contact_graph.py',ROOT/'output/audit_h5_staggered_contact_graph_repaired.py',ROOT/'output/prepare_h5_staggered_contact_selection.py',ROOT/'output/run_h5_staggered_contact_selection.py',ROOT/'output/plot_h5_paired_strip_core.py'];seen=set()
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
core=load(audits['core']);graph=load(audits['source-graph']);model=load(audits['model']);generated=load(POOL/'result.json');cover=load(POOL/'fast-cover/checks.json')
checks={'passed':True,'independent_audits_passed':4,'failed_checker_attempts_preserved':1,'core_originals':33,'core_pairs':258,'core_stock_edges':132,'core_cutouts':45,'core_cutout_vertices':3366,'candidate_counts':generated['candidate_counts'],'candidate_source_pair_checks':graph['unordered_original_pair_checks'],'conflicts_verified':graph['conflicts_verified'],'fixed_original_pair_checks':graph['fixed_original_pair_checks'],'candidate_stock_edges':graph['stock_edge_checks'],'accepted_obstacle_interior_representatives':0,'rejected_obstacle_interior_proposals':generated['event_counts']['obstacle_interior'],'cliques_verified':graph['cliques_verified'],'model_variables':model['variables'],'model_constraints':model['constraints'],'all33_movers_required':True,'all66_accounted_once':True,'solver_calls':1,'status':'UNKNOWN','returned_solve_seconds':response['returned_solve_seconds'],'shared_process_seconds':response['shared_process_seconds'],'returned_soft_overrun_seconds':response['returned_soft_overrun_seconds'],'source_witness_found':False,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: mixed frame rows and complete source contacts — 2026-10-26

**A changed frame arrangement and a fresh joint search remain unresolved.**
The original geometry, complete conflict graph and exact required quantities
pass independent audits. The one bounded call returns UNKNOWN; there is no
complete layout, exclusion or new release qualification. H2/H5 remain open
at 60% by completed gate weights.

## Changed core

Twelve quarter-turned frames occupy four columns by three rows, followed by
six unturned frames in three columns by two rows. Their top is 2,057.425 mm.
Keep the checked short sheet's six brackets and nine inserts exactly. The
remaining **six brackets, twelve inserts and fifteen cogs** are all mandatory
on the first sheet. No quantity is dropped and no old fixed-owner exclusion
is transferred.

The independent readback verifies all 33 fixed originals, **258 same-sheet
pairs, 132 stock edges and 45 cutouts with 3,366 vertices**. Minimum pair gap is
0.225 mm; minimum extra stock margin is 0.025 mm. All eighteen first-sheet
anchors are checked against rational construction formulas. A comparison with
29 historical frame groups finds no identical sorted sheet/bounds arrangement
at 0.000001 mm precision. This does not establish a globally new topology or
an improved partial score. The lower side strip is narrower than the wide-row
alternative. Both older 64-original partials remain preserved.

![Checked alternative core; 33 other originals still required]({NAME}/core.png)

## Actual-source contact pool

The new pool has **2,200 cog, 1,000 bracket and 1,000 insert poses**. Its declared
finite orientations are four cog phases (0°, 4.5°, 9°, 13.5°), all eight allowed
bracket rotation/mirror modes, and two insert outer-orientation classes.

Fourteen fixed-obstacle queries seed placements. A table of 384 checked
source-cog contacts extends independent centers to depth three. Forty contact
queries around 64 spatially spread cog parents provide noncog poses; a separate
100-query stage around 64 stratified bracket/insert parents adds mutual contacts.
This permits bracket pairs and inserts to touch without requiring common cog
rows, pitch or phase. Generation takes **5.437320 seconds**.

Before counting a contact toward any quota, the generator rejects obstacle
interior representatives and checks actual distance from the generating parent.
It rejects **1,280 interior proposals**. All accepted contact-parent links pass
the independent source check. The resulting provenance counts are 247 fixed
seeds, 2,139 cog contacts, 714 contacts around cogs and 1,100 mutual contacts.
Finite caps, 25 mm spatial bins, omitted proposals and unfinished queues remain
recorded; no continuous or arbitrary-angle coverage is asserted.

## Complete graph and exact model

Independent reconstruction checks **75,600 fixed-original pairs, 16,800 stock
edges and all 8,817,900 candidate pairs**, reproducing **1,998,405 conflicts**.
The minimum candidate/fixed gap is 0.221851 mm and extra stock margin 0.012600 mm,
both above their native guards.

The initial graph builder takes 64.856107 seconds. Its reported cover stage,
including saved residual bookkeeping, takes 22.961423 seconds against a
20-second loop allowance; this overrun is retained. It leaves 794,682 explicit
edges after 112 cliques. A separate first-bit bitset extension compresses the
same graph into **25,736 verified cliques**, with zero residual edges, in
0.862628 seconds of cover work and 1.371304 seconds including output. No candidate
or conflict is removed. The original cover and graph bytes remain archived.

The model contains **4,200 Boolean variables and 25,739 constraints**: exact
family counts 6/12/15 plus the complete conflict cover, with no objective or
hints. Independent protocol reconstruction and solver import/export pass.

## Closed result and evidence

The sole 60-second call, inside 90 shared seconds, returns **UNKNOWN** after
search. Internal time is **60.066062 seconds**, returned-call time **60.071975
seconds**, and shared time **61.044539 seconds**. The 0.071975-second returned
soft overrun is preserved. The returned worker reports 175,799 branches and
1,184 conflicts; separate worker statistics are archived. No assignment is
returned. The call is closed, without retry, reseeding or extension.

All four independent audits pass. One initial response-checker failure is kept:
it assumed finer precision than the solver's printed walltime. The repaired
reader uses the printed decimal precision and verifies the unchanged response;
the search is not rerun. No native call or full quality run is justified by
this unresolved result.

At {review['utc']}, **{ci_success} of six** checks on
[main e158daa2](https://github.com/skulitom/Nestbolt/actions/runs/40365489221)
have succeeded. The next push must wait for all six. Production, READMEs,
upstream heads/releases and all 22 reserved H2 vectors remain unchanged.
H2 retains its original gate. A complete 66-original source/native/material
witness is still required before integration and the complete H5 matrix.

[Checks]({NAME}/checks.json), [core]({NAME}/core-checks.json),
[source graph]({NAME}/source-graph-checks.json), [model]({NAME}/model-checks.json),
[response]({NAME}/response-checks.json), [inventory]({NAME}/all66-inventory.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 mixed frame rows and source contacts, 2026-10-26:** [the evidence]({link})
checks a changed 18-frame core and the preserved 15-part short sheet against
258 pairs, 132 stock edges and all 45 cutouts. Every remaining bracket, insert
and cog stays mandatory (6/12/15). A fresh 4,200-pose pool adds mutual bracket/
insert contacts and rejects 1,280 obstacle-interior proposals before quotas.
Independent checks reproduce all 8,817,900 candidate pairs and 1,998,405 conflicts;
25,736 verified cliques preserve the complete graph. The exact 4,200-variable,
25,739-constraint model closes UNKNOWN after search in 60.071975 returned/
61.044539 shared seconds. Its soft overrun and initial cover overrun remain
recorded. All four independent audits pass; a failed log-precision checker is
preserved and repaired without rerunning the search. No source witness or
exclusion is claimed. H2/H5 remain open at 60%; production, READMEs, releases
and all 22 reserved H2 vectors are unchanged. Wait for all six checks on main
e158daa2 before the next push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'independent_audits_passed':4,'main_ci_successful_jobs_at_seal':ci_success})
