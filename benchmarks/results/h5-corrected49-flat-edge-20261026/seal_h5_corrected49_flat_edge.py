"""Seal rebuilt corrected-source geometry and two closed necessary searches."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-corrected49-flat-edge-20261026';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-retained49-source-guard-repair-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head.startswith('a5ed42dc') and main==previous['remote_main']
assert source_digest()==previous['production_digest']
assert {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
 'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
 'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
 'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
ci=json.loads(command(['gh','run','view','40400314122','--json','databaseId,status,conclusion,headSha,jobs,url']))
assert ci['status']=='completed' and ci['conclusion']=='cancelled' and ci['headSha']==main
assert sum(j['conclusion']=='success' for j in ci['jobs'])==5
folders=[ROOT/'output'/n for n in ['h5-corrected49-joint-geometry-20261026','h5-corrected49-joint-model-20261026',
 'h5-corrected49-joint-model-repaired-20261026','h5-cog-flat-edge-support-20261026','h5-flat-edge-joint-model-20261026']]
G,F,B,S,M=folders
audits={'geometry':G/'audit/checks.json','base-model':B/'model-audit/checks.json','base-response':B/'response-audit/checks.json',
 'support':S/'audit/checks.json','support-mask':S/'mask/audit/checks.json','strong-model':M/'model-audit/checks.json','strong-response':M/'response-audit/checks.json'}
for p in audits.values():assert load(p)['passed']
for p in [B,M]:
    r=load(p/'response-audit/checks.json');assert r['status']=='UNKNOWN' and r['closed'] and not r['has_necessary_assignment']
    assert r['solver_calls']==1 and r['shared_process_seconds']<90 and r['native_calls']==0
assert not (F/'model.pb').exists() and (F/'failure.json').is_file()
OUT.mkdir()
for name,p in audits.items():shutil.copyfile(p,OUT/(name+'-checks.json'))
for p,n in [(S/'support-proof.json','support-proof.json'),(S/'audit/necessity-proof.json','necessity-proof.json'),
            (F/'failure.json','initial-builder-failure.json'),(B/'search/result.json','base-result.json'),(M/'search/result.json','strong-result.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-attempt2.json',ci)
write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,
 'production_digest':source_digest(),'current_readmes':previous['current_readmes'],**upstream,'upstream_heads_and_releases_unchanged':True,
 'production_and_readmes_unchanged':True,'main_ci_successful_jobs':5,'main_ci_browser_timeout_preserved':True,
 'external_solver_calls':2,'native_calls':0,'quality_runs':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,
 'reserved_H2_vectors_evaluated':0,'new_release_qualified':False})
write(OUT/'next-step.json',{'action':'Both 60-second mandatory17 searches are closed UNKNOWN; do not retry, reseed or extend. Corrected49 fixed geometry, all-angle cog support strips and complete boundary-preserving cell masks are now verified. They establish neither a full66 placement nor a fixed49 exclusion. Next use exact geometric decomposition/capacity certificates or a materially different source construction; all66 originals and current guards/material limits remain required. First repair CI checkout overhead: main36f162d0 browser attempt2 ended after 30 minutes, tests never started, with 18m07s spent checking out. Preserve both timeouts and all successful jobs. Validate a concrete sparse checkout on an isolated branch before advancing main. No gate limits or test budgets change. H2 unchanged and22 reserved vectors unopened.',
 'completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};bindings={};queue=[]
for folder in folders:
    for p in folder.rglob('*'):
        if p.is_file():
            members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
            if p.name=='plan.json':queue.append(p)
seen_plans=set()
while queue:
    plan=queue.pop()
    if plan in seen_plans:continue
    seen_plans.add(plan)
    for n,h in load(plan).get('inputs',{}).items():
        p=ROOT/n;assert digest(p)==h,n;bindings[n]=h;members['source-inputs/'+n]=p
        if p.name=='plan.json':queue.append(p)
write(OUT/'source-bindings.json',bindings)
helpers=[ROOT/'output'/n for n in ['prepare_h5_corrected49_joint_geometry.py','audit_h5_corrected49_joint_geometry.py',
 'build_h5_corrected49_joint_model.py','build_h5_corrected49_joint_model_repaired.py','audit_h5_corrected49_joint_model.py',
 'run_h5_corrected49_joint_model.py','audit_h5_corrected49_joint_response.py','prepare_h5_cog_flat_edge_support.py',
 'audit_h5_cog_flat_edge_support.py','prepare_h5_flat_edge_cog_mask.py','audit_h5_flat_edge_cog_mask.py',
 'build_h5_flat_edge_joint_model.py','audit_h5_flat_edge_joint_model.py','run_h5_flat_edge_joint_model.py',
 'audit_h5_flat_edge_joint_response.py','ccd1.py','pack_h5_evidence_archive.py']];seen=set()
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
write(OUT/'checks.json',{'passed':True,'audits_passed':len(audits),'fixed_source_valid_originals':49,'mandatory_movers':17,
 'source_support_all_real_angles':True,'new_strict_cell_exclusions':552,'boundary_center_coverage_preserved':True,
 'closed_UNKNOWN_searches':2,'initial_builder_failure_preserved':True,'full66_witness':False,'fixed49_excluded':False,
 'unrestricted_exclusion_claimed':False,'native_calls':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: corrected-source geometry and all-angle flat-edge support — 2026-10-26

**All geometry has been rebuilt for the source-valid retained 49 originals.**
The two brackets and all 15 cogs remain mandatory, with free positions and sheets,
all eight bracket variants and every real cog rotation. Neither of the two
bounded necessary searches finds an assignment or excludes this fixed subset.
H2/H5 remain open at **60%**; no source/native fit or release is claimed.

## Geometry rebuilt from corrected source transforms

The independent reader verifies 69 source-contained fixed rectangles, 1,330
integer forbidden bracket-anchor boxes and the complete union of 77 remaining
anchor rectangles across 16 variant/sheet domains. Exact set complements preserve
every integer boundary. For cogs, 69 source-inner-octagon sums provide 12 facets
each; 26,496 exact point-sum checks verify them. Of 33,275 closed grid cells,
28,175 are strictly excluded. The 5,100 remaining table rows cover all potentially
legal centers. Nine universal short-sheet count rows remain compatible.
No position-dependent certificate from the old fixed-51 arrangement is reused.

The first builder fails before model serialization because an OR-Tools method
returns `None`; its original code and failure are preserved. The repaired model
has 15,797 variables and 17,412 constraints. Its reader verifies all domains,
linked choices, optional rectangle intervals, 135 fully reified sheet equalities,
105 cog-pair clauses and 720 mixed variant/component clauses. There are no hints
or objective. Its single call ends **UNKNOWN** after 905,867 branches:
60.0538294 solver seconds / 60.0633621 returned seconds / 61.6408652 shared seconds.

## A stronger necessary rule from actual source vertices

For every real rotation, an original cog vertex attains signed-axis support of
at least 139,270 micrometers. Exact source-radius and center-flooring bounds yield
support **139,268**, radius **140,003**, and transverse bound **14,328** micrometers.
For a source-contained rectangle `[x,y,xx,yy]`, the strict center strips
`[x-h,y+L,xx+h,yy-L]` and `[x+L,y-h,xx-L,yy+h]` force an actual source collision.
The central band uses a strictly smaller source-contained disk; the outer band
uses an actual support vertex and verified rectangle-width inequalities.
The convex hull certifies vertex support only; it is never filled collision
geometry, and the cog-pair virtual disk is never applied to mixed collisions.

The exact reader checks all 80 source vertices, 40 hull edges, 80 source boundary
edges and all 186 fixed/moving support strips. Every rectangle satisfies the
strict width requirements. The stronger mask removes another **552 whole cells**,
leaving **4,548** rows (4,336 first-sheet / 212 short-sheet); all boundary centers
and all 15 previously checked cog-center cells remain represented.

The strengthened model preserves the earlier variables and constraints byte for
byte, then adds 15 mask tables, 1,440 conditional support clauses and 5,760
halfplanes. All **21,557 variables / 24,627 constraints** pass independent reading.
Its one new call ends **UNKNOWN** after **1,345,918 branches / 197,331 conflicts**:
60.097942 solver seconds / 60.1094835 returned seconds / 61.3953801 shared seconds.
Both small soft-limit overruns are retained, both calls stay inside their 90-second
shared bounds, and both searches are closed without retry or extension.

## Next work and publication checks

These are necessary models, not complete source geometry. There is no assignment,
fixed-49 exclusion, chosen cog angle, full-66 witness or native validation.
Continue through exact geometric decomposition/capacity reasoning or a materially
different source construction; preserve all originals, guards and material limits.

Main `36f162d0` has five successful checks. Its browser-only second attempt also
times out before tests: checkout alone takes **18m07s**. Both failures remain
preserved; CI checkout overhead will be repaired and validated independently before
the next main push. Production, READMEs and upstream heads/releases are unchanged.
All 22 reserved H2 vectors remain unopened.

[Checks]({NAME}/checks.json), [geometry]({NAME}/geometry-checks.json),
[support proof]({NAME}/necessity-proof.json), [mask]({NAME}/support-mask-checks.json),
[strong model]({NAME}/strong-model-checks.json), [response]({NAME}/strong-response-checks.json),
[next step]({NAME}/next-step.json), [manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 corrected49 geometry and cog flat-edge support, 2026-10-26:**
[The evidence]({link}) rebuilds all fixed-obstacle geometry from the corrected
source-valid49. All17 movers remain mandatory. Exact all-angle source-vertex
support proves186 new flat-edge forbidden strips and removes552 more whole
cog-center cells while preserving every boundary center and all15 prior cells.
Seven audits pass. The base15,797-variable and stronger21,557-variable models
both end UNKNOWN in one60-second call each; raw timing, failures and results
remain preserved and both searches are closed. There is no full66 witness,
fixed49 exclusion, native call or H5 credit. H2/H5 stay open at60%; all22 reserved
vectors remain unopened. Main36f162d0 browser attempt2 also timed out before tests,
with18m07s checkout; prepare and validate a CI checkout repair on an isolated
branch before the queued main push. Production and READMEs are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive})
