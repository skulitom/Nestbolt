"""Archive three closed source-sliding experiments and the recovered main CI."""
from pathlib import Path
from datetime import datetime, timezone
import ast, json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-source-sliding-and-guided-penalties-20261026';OUT=ROOT/'benchmarks/results'/NAME
folders=[ROOT/'output'/n for n in ['h5-sliding-source-geometry-20261026','h5-global-sliding-source-geometry-20261026','h5-guided-sliding-source-20261026']]
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-global-short-frontier-and-eight-brackets-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head==main=='ea4f2ebfbcd7ac3e3a8ea63cb5cb037bf29588fb'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40372823229','--json','databaseId,status,conclusion,attempt,headSha,jobs,url']))
assert ci['headSha']==head and ci['status']=='completed' and ci['conclusion']=='success' and ci['attempt']==2 and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
audits={}
for label,folder,prep,result in zip(['fixed29','all53','guided53'],folders,['preflight/checks.json','preflight/checks.json','checks.json'],['result-audit/checks.json','result-audit/checks.json','result-audit-summation-repaired/checks.json']):
    audits[label+'-preflight']=folder/prep;audits[label+'-source']=folder/result
assert all(load(p)['passed'] for p in audits.values())
source=[load(audits[n+'-source']) for n in ['fixed29','all53','guided53']]
assert [s['source_pair_failures'] for s in source]==[40,52,50] and [s['source_stock_failures'] for s in source]==[5,9,10]
assert all(s['closed'] and not s['actual_source_geometry_valid'] and s['all66_originals_verified'] and s['native_calls']==0 for s in source)
assert all(s['same_sheet_source_pairs']==1456 and s['stock_edge_checks']==264 and s['cutouts_preserved']==90 and s['cutout_vertices_preserved']==10026 for s in source)
mode_evidence=[]
for folder in folders[1:]:
    modes=load(folders[1]/'modes.json');moving=load(folders[1]/'moving.json');families={r['original']:r['family'] for r in moving};changes=load(folder/'search/accepted-mode-changes.json');best=load(folder/'search/best.json')
    assert all(families[r['original']]=='cog' for r in changes)
    frame_modes=[mi for r,mi in zip(moving,best['modes']) if r['family']=='frame'];assert frame_modes==[14]*18
    mode_evidence.append({'directory':folder.relative_to(ROOT).as_posix(),'accepted_changes':len(changes),'accepted_changes_all_cogs':True,'best_frame_modes':frame_modes,'inference':'Single-part greedy mode changes did not rotate any frame from this initialization; this is not a global barrier proof.'})
OUT.mkdir()
for name,p in audits.items():shutil.copyfile(p,OUT/(name+'-checks.json'))
write(OUT/'mode-change-audit.json',mode_evidence);write(OUT/'main-ci-ea4f2ebf-passed.json',ci)
shutil.copyfile(folders[2]/'result-audit/failure.json',OUT/'preserved-summation-checker-failure.json')
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40372823229,'main_ci_attempt':2,'main_ci_successful_jobs':6,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'next-step.json',{'action':'All three source-sliding searches are CLOSED; do not extend or reseed them. Revisit the preserved 64-original layout at output/h5-latest-wide-joint-20261023/layout-audit/layout-final.json as a materially different allocation: retain its 9-part short sheet (4 brackets,2 inserts,3 cogs), release all57 required first originals including the two missing brackets, and retain actual source angles without a symmetry assumption. Its old .2001mm gap is below the present native guard; independently check/rebuild the short sheet at current clearance before opening a search. A full66 source/native/material witness remains necessary before integration and the complete H5 matrix. H2 stays open under the original gate;22 reserved vectors stay unopened.','old_searches_closed':True,'completion_percent':60,'H2_complete':False,'H5_complete':False})
write(OUT/'scope.json',{'searches':3,'all_searches_closed':True,'all66_originals_preserved_each':True,'source_valid_results':0,'native_calls':0,'quality_runs':0,'penalty_reduction_is_material_improvement':False,'source_partial_count_improvement_claimed':False,'unrestricted_exclusion':False,'H5_complete':False})
members={};inputs={}
for folder in folders+[ROOT/'output/ci-ea4f2ebf-web-timeout-20261026']:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=list((ROOT/'output').glob('*h5*sliding*.py'))+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
write(OUT/'checks.json',{'passed':True,'preflight_audits_passed':3,'independent_original_geometry_readbacks_passed':3,'source_valid_results':0,'failed_checker_attempts_preserved':1,'searches_closed':3,'all66_originals_verified_each':True,'source_pair_failures':[40,52,50],'source_stock_failures':[5,9,10],'native_calls':0,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: source sliding and guided penalties — 2026-10-26

**Three bounded searches retain all 66 originals but produce no valid layout.**
The best returned positions still violate source pair or stock clearances.
All three searches are closed. Lower overlap penalties are not material savings,
higher valid part counts, or evidence that H5 passes. H2/H5 remain open at 60%
by completed gate weights.

## Source geometry and bounded searches

The starting allocation uses the verified eight-bracket/five-insert short sheet.
The first experiment fixes 18 frames and 11 inserts on the full sheet and moves
all remaining four brackets, five inserts and fifteen cogs jointly. A source
checkerboard of fifteen cogs at alternating 0°/13.5° and 261.25 mm pitch is
initially valid: 105 cog pairs and 435 fixed-core pairs pass, with a minimum cog
gap of 0.22859487 mm. This is only a 57-part source partial; the older 64-part
partials remain stronger and are preserved.

Configuration obstacles come from original filled outlines. Four cog phases,
eight bracket modes and two insert orientations are allowed. The second search
adds both frame orientations and releases every first-sheet part: 53 mandatory
originals, 106 continuous coordinates, and only 13 short-sheet originals fixed.
All 16 stock domains are rebuilt, retaining no former fixed-owner exclusions.
The 105 identical intrinsic obstacles are hash-checked; 31 frame pairs are new.

The third search uses a different adaptive objective starting from the second
search's saved best positions. All 1,378 pair terms and 53 stock terms remain
strictly positive. Before each stage, the top quarter of violated terms ranked
by squared depth divided by weight ratio receive a 1.5× weight increase (ratio
capped at one million). There are at most 100 stages, with legal mode sweeps
every fourth stage. Best poses are compared using the unweighted geometric
penalty, since scores with changing weights are not comparable.

| Search | Moving first parts | Returned status | Optimization / shared seconds | Source pair failures | Stock failures |
| --- | ---: | --- | ---: | ---: | ---: |
| Fixed 29 first parts | 24 | LOCAL_STATIONARY | 0.268804 / 7.809760 | 40 | 5 |
| All first parts | 53 | LOCAL_STATIONARY | 0.701100 / 5.011996 | 52 | 9 |
| Adaptive positive penalties | 53 | ITERATION_LIMIT | 14.120617 / 15.284898 | 50 | 10 |

Each search starts once, without random restarts, within its declared 60-second
search / 90-second shared limit. Respectively they make 473, 526 and 14,243
objective evaluations. Best unweighted penalties are 8,434.111700, 6,083.424728
and 5,004.590670 mm²; these are overlap diagnostics, not usable layout scores.
Neither all-part search accepts a frame turn: every accepted mode change is a
cog phase change, and all 18 best frames retain the unturned mode. This suggests
a limitation of single-part greedy turns from this initialization; it does not
prove that a coordinated rearrangement or any source layout is impossible.

## Independent acceptance and preserved failures

Three preflight checks cover source mode reconstruction, sampled obstacle/stock
geometry and numerical gradients (36, 60 and 60 checks). Geometry samples are
not continuous proofs. Each independent final reader reconstructs all original
rings directly from the job and verifies identities, legal transformations,
1,456 same-sheet pairs, 264 stock edges, and all 90 cutouts/10,026 hole vertices.
Pair guard is 0.21170867250963943 mm; extra stock guard is 0.011444091796875 mm.
Every returned layout fails these source conditions. No native validator is
called, no full quality run occurs, and no unrestricted exclusion is claimed.

The first guided reader rejected a diagnostic sum differing by one floating
point unit (9.094947017729282e-13). That failed checker and its result remain
preserved. A repaired reader allows 32 units only for diagnostic sum comparison;
physical source thresholds are unchanged. It replays all 100 positive weight
updates without rerunning the search and confirms the same invalid geometry.

## Repository checks and next evidence

Main ea4f2ebf's first browser job exhausted its 30-minute limit downloading
Ubuntu dependencies; browser tests had not started. Its log, terminal result
and retry request are preserved. After the other five jobs had completed,
only that browser job was rerun on the same commit. At {review['utc']},
[all six main checks pass](https://github.com/skulitom/Nestbolt/actions/runs/40372823229)
on attempt 2. No live main job was cancelled and no application changes were
made to obtain the pass.

The next distinct hypothesis uses the preserved 64-part allocation with three
cogs on the short sheet and adds its two missing brackets while releasing all
57 required first originals. It must first address the old partial's clearance
below the current native guard, use its actual source rotations, and validate
the changed short sheet. It is not a continuation of any closed 53-part run.

Production, READMEs, upstream heads/releases and all 22 reserved H2 vectors are
unchanged. No new release is qualified. [Checks]({NAME}/checks.json),
[scope]({NAME}/scope.json), [mode evidence]({NAME}/mode-change-audit.json),
[next step]({NAME}/next-step.json) and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 bounded source sliding, 2026-10-26:** [the evidence]({link})
records three closed searches: 24 movers with 29 fixed first parts, all 53 first
parts movable, and adaptive positive penalties on all 53. Independent original
geometry readers retain all 66 identities, 90 cutouts and 10,026 hole vertices,
but find 40/52/50 pair failures and 5/9/10 stock failures respectively. Lower
overlap penalties are not material or valid part-count improvements. Neither
all-part search accepts a frame turn; no global impossibility is claimed.
Three preflight and three final checks pass; one diagnostic-summation checker
failure is preserved and repaired without changing physical tolerances or
rerunning a search. All six main ea4f2ebf checks now pass after the browser-only
retry of a dependency-download timeout. The failed attempt is preserved.
H2/H5 remain open at 60%; no native/full-quality run or new release qualifies.
The next distinct allocation must first repair the older 64-part partial's
short-sheet clearance; all 22 reserved H2 vectors remain unopened.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'source_valid_results':0,'main_ci_successful_jobs':6})
