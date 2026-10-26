"""Preserve current-guard short-sheet repair and the closed complete first-sheet search."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-retained64-allocation-source-search-20261026';OUT=ROOT/'benchmarks/results'/NAME;OLD=ROOT/'output/h5-legacy64-sliding-geometry-20261026';GEO=ROOT/'output/h5-legacy57-sliding-source-20261026';RUN=ROOT/'output/h5-legacy57-guided-search-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-source-sliding-and-guided-penalties-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head.startswith('7a37f3da') and command(['git','rev-parse','HEAD^'])==main==previous['remote_main']
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40372823229','--json','databaseId,status,conclusion,attempt,headSha,jobs,url']));assert ci['headSha']==main and ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
pre=load(RUN/'preflight/checks.json');result=load(RUN/'result-audit/checks.json');short=load(RUN/'preflight/short-source-readback.json');assert pre['passed'] and result['passed'] and short['valid'] and short['originals']==9 and result['closed'] and result['all66_originals_verified'] and not result['actual_source_geometry_valid'] and result['source_pair_failures']==60 and result['source_stock_failures']==10
moving=load(GEO/'moving.json');families={r['original']:r['family'] for r in moving};changes=load(RUN/'search/accepted-mode-changes.json');counts=dict(Counter(families[r['original']] for r in changes));best=load(RUN/'search/best.json');frames=[mi for r,mi in zip(moving,best['modes']) if r['family']=='frame'];assert counts=={'cog':9,'insert':7,'bracket':1} and frames==[14]*18
OUT.mkdir()
for p,n in [(RUN/'preflight/checks.json','preflight-checks.json'),(RUN/'preflight/short-source-readback.json','short-source-readback.json'),(OLD/'short-repair/before-source.json','short-original-failed-guard.json'),(OLD/'short-repair/result.json','short-repair-result.json'),(OLD/'short-repair/placements.json','short-repaired-placements.json'),(RUN/'chosen-insertions.json','chosen-insertions.json'),(RUN/'result-audit/checks.json','result-checks.json'),(RUN/'result-audit/all66-placements.json','all66-invalid-placements.json'),(RUN/'search/result.json','closed-search-result.json')]:shutil.copyfile(p,OUT/n)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40372823229,'main_ci_successful_jobs':6,'queued_previous_checkpoint':head,'next_push_commits':2,'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False};write(OUT/'source-review.json',review);write(OUT/'main-ci-ea4f2ebf-passed.json',ci)
write(OUT/'scope.json',{'short_source_originals':9,'short_current_guard_valid':True,'first_required_originals':57,'all66_preserved':True,'first_search_closed':True,'source_witness_complete':False,'native_calls':0,'quality_runs':0,'unrestricted_exclusion':False,'lower_penalty_is_material_improvement':False,'accepted_mode_changes_by_family':counts,'all18_frames_remain_unturned':True,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The repaired four-bracket/two-insert/three-cog short sheet is valid at current guards and can be retained as an allocation option. The57-first-part adaptive run is CLOSED after100 updates; no time extension, reseed or continuation. Its remaining60 source pair failures and10 stock failures require a materially different geometric mechanism. Single-part greedy mode changes have still not rotated any frame; investigate coordinated multi-part orientation/position changes or genuinely continuous source cog rotations, with source-grounded preflight and a new declared bounded hypothesis before any search. Preserve both earlier64 partials and every failed result. No complete source/native/material witness exists; production integration/fullH5 matrix and release remain unqualified. H2 keeps the original gate and22 reserved vectors remain unopened. Push this and the queued7a37f3da checkpoint normally after stage/ancestry checks; preceding main ea4f2ebf has all6 CI checks successful.','completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs={}
for folder in [OLD,GEO,RUN]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():assert digest(ROOT/n)==h,(p,n);inputs[n]=h
for n in inputs:members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=list((ROOT/'output').glob('*h5_legacy*.py'))+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_preflight_and_source_audits_passed':2,'short_originals_repaired_and_verified':9,'short_source_pairs':36,'short_stock_edges':36,'short_cutouts':17,'short_hole_vertices':2308,'source_modes_verified':18,'original55_first_seed_poses_preserved':True,'deterministic_insertion_proposals':22640,'all66_final_originals_verified':True,'final_source_pairs':1632,'final_stock_edges':264,'final_cutouts':90,'final_hole_vertices':10026,'final_pair_failures':60,'final_stock_failures':10,'source_witness_complete':False,'native_calls':0,'production_and_readmes_unchanged':True,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: retained 64-part allocation with all first parts movable — 2026-10-26

**The older nine-part short sheet now passes current source clearances, but a
new search for all 57 required first-sheet parts still fails.** All 66 original
identities and cutouts remain present. There is no complete target witness;
H2/H5 remain open at 60% by completed gate weights.

## Repair the distinct short allocation first

The preserved 64-part result has four brackets, two inserts and three cogs on
the short sheet. Its first sheet has 18 frames, six brackets, 19 inserts and
12 cogs; bracket copies10/11 are missing. This allocation differs from the prior
53/13 experiments, which remain closed. Original evidence is retained unchanged.

Original source rotation is preserved exactly: cogs use
**-2.2428996024478143 radians**, and horizontal reversed inserts use pi. Both
are added to the mode table by transforming the original rings, with no tooth
symmetry assumption. There are now 18 source modes and 171 unordered pair
obstacles: 136 unchanged intrinsic obstacles are hash-verified and 35 are new.
Geometry preparation takes 4.979303 seconds.

Before repair, the short sheet fails three pair guards and one stock guard.
Its minimum pair gap is 0.2011 mm and extra stock margin is 0.0001 mm. A single
fixed-mode translation repair takes 21 evaluations / 0.007894 seconds within
its declared 10-second/2,500-evaluation limit. Independent original-ring readback
then passes all **36 pairs, 36 stock edges, 17 cutouts and 2,308 hole vertices**.
Minimum pair gap becomes **0.2243086724868379 mm** and extra stock margin
**0.012600000000188238 mm**, above the unchanged native guards. Angles, mirror
attributes and original geometry are preserved; only positions change.

## One full first-sheet search

All 55 original first poses are preserved in the seed. The two missing brackets
are inserted using a deterministic 50 mm stock grid including stock boundaries
and all eight bracket modes. The second insertion accounts for the first.
All **22,640 proposals** are retained. The selected initial anchors are
[1150,2650] mm in mode6 for original28 and [200,2550] mm in mode4 for original29.
Insertion preparation takes 1.712307 seconds. This is one seed, not a valid fit.

The new inventory keeps all **57 first originals movable**: 18 frames, eight
brackets, 19 inserts and 12 cogs. The repaired short9 stays fixed. Preflight
reconstructs all18 modes, verifies 108 stock samples, 4,275 obstacle samples
(2,896 outside-source checks), and 60 weighted gradient checks. Samples are
not a continuous geometry proof. Every 1,596 pair term and 57 stock term stays
strictly positive; 100 adaptive updates and legal mode sweeps use the same
declared algorithm as the earlier guided experiment on this different inventory.

The sole call closes **ITERATION_LIMIT** after **29.220400 optimization /
30.492711 shared seconds**, within 60/90 seconds. It performs 21,787 objective
evaluations, 100 returned stages, 4,000 mode trials and 17 accepted changes
(nine cog, seven insert and one bracket changes). All18 frames remain unturned.
No retry, extension or random restart occurs.

Best unweighted overlap penalty falls from 8,880.895434 to 1,278.391832 mm².
This is not a material saving or a valid part-count improvement. The independent
final reader checks **all66 identities, 1,632 same-sheet pairs, 264 stock edges,
90 cutouts and 10,026 hole vertices**, finding **60 pair failures and 10 stock
failures**. It replays all100 weight updates and confirms no constraint was
removed. Therefore no native call or full quality run is qualified. Neither
this local failure nor the finite modes prove unrestricted impossibility.

## Checkpoint and remaining work

At {review['utc']}, [all six main ea4f2ebf checks pass](https://github.com/skulitom/Nestbolt/actions/runs/40372823229),
allowing a normal two-commit push with the queued7a37f3da evidence. Production,
READMEs, upstream heads/releases and all22 reserved H2 vectors remain unchanged.
No new release qualifies. The next search needs a materially different source
geometry mechanism, such as coordinated orientation/position changes; these
closed runs must not be extended or reseeded. A full66 source/native/material
witness remains required before integration and the full H5 matrix.

[Checks]({NAME}/checks.json), [short repair]({NAME}/short-repair-result.json),
[preflight]({NAME}/preflight-checks.json), [full result]({NAME}/result-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 retained-64 allocation and full first-sheet search, 2026-10-26:** [the evidence]({link})
repairs the older four-bracket/two-insert/three-cog short sheet to current
clearances, independently passing 36 pairs, 36 edges and all17 cutouts.
Its exact cog angle is reconstructed from source, without a symmetry assumption.
All57 first originals remain mandatory and movable; the two missing brackets
are seeded from 22,640 deterministic proposals. The sole guided call closes
ITERATION_LIMIT in29.220400 optimization/30.492711 shared seconds. All66 source
identities, 90 cutouts and10,026 hole vertices are retained, but final readback
finds60 pair failures and10 stock failures. Lower overlap penalty is not a
material improvement. No native/full-quality run or release is qualified.
Both independent audits pass; all6 main ea4f2ebf checks pass, permitting a
normal two-commit checkpoint push. H2/H5 stay open at60%; all22 reserved H2
vectors stay unopened. Closed searches will not be extended or reseeded.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive,'source_witness_complete':False,'next_push_commits':2})
