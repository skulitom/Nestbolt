"""Preserve the failed small repair, diagnosed stack correction and source-valid49."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-retained49-source-guard-repair-20261026';OUT=ROOT/'benchmarks/results'/NAME
OLD=ROOT/'output/h5-retained49-guard-repair-20261026';BASE=ROOT/'output/h5-retained49-stack-repair-20261026';RETRY=ROOT/'output/h5-main36-web-retry-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-fixed-noncog-cog-capacity-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head.startswith('4bbd47f4') and main==command(['git','rev-parse','HEAD~2'])=='36f162d0df3d5c88eb4145c58004890b650fba61'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40400314122','--json','databaseId,status,conclusion,headSha,jobs,url']));attempt=json.loads(command(['gh','api','repos/skulitom/Nestbolt/actions/runs/40400314122','--jq','{status,conclusion,run_attempt,head_sha,html_url}']))
assert ci['headSha']==main and len(ci['jobs'])==6 and attempt['run_attempt']==2
success=sum(j['conclusion']=='success' for j in ci['jobs']);ready=ci['status']=='completed' and ci['conclusion']=='success' and success==6
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
    'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
    'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
    'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
failure=load(OLD/'audit/checks.json');good=load(BASE/'audit/checks.json');assert failure['passed'] and good['passed'] and not failure['source_repair_excluded'] and good['source_pair_failures']==good['source_stock_failures']==0
assert good['retained_source_originals_verified']==49 and good['mandatory_movers_preserved']==17 and good['maximum_absolute_axis_shift_um']==79
OUT.mkdir()
for p,n in [(OLD/'result.json','failed50um-result.json'),(OLD/'audit/checks.json','failure-audit.json'),(OLD/'audit/negative-cycle.json','negative-cycle.json'),
    (BASE/'result.json','repair-result.json'),(BASE/'audit/checks.json','source-checks.json'),(BASE/'corrected49-source.json','corrected49-source.json'),
    (BASE/'mandatory17-movers.json','mandatory17-movers.json'),(RETRY/'retry-web-only.json','browser-retry-receipt.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-36f162d0-attempt2.json',ci);write(OUT/'main-attempt2-state.json',attempt)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],
    'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40400314122,'main_attempt':2,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,
    'browser_only_retry_after_other5_success':True,'push_qualified_now':ready,'unpublished_prior_checkpoints':2,'completion_percent':60,'H2_complete':False,'H5_complete':False,
    'reserved_H2_vectors_evaluated':0,'external_solver_calls':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'corrected_source_valid_originals':49,'mandatory_unplaced_originals':17,'mandatory_movers':{'cog':15,'bracket':2},'orientations_sheets_identities_unchanged':True,
    'original_guard_thresholds_unchanged':True,'225um_conservative_component_spacing_unchanged':True,'maximum_axis_shift_um':79,'old50um_failure_preserved':True,
    'seven_insert_positiveY_domains_changed_from_certificate':True,'all_pair_range_bounds_rebuilt':True,'old_fixed51_exclusion_not_transferred_to_changed_geometry':True,'full66_witness':False,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'Use output/h5-retained49-stack-repair-20261026/corrected49-source.json as the independently source-valid retained49. All17 originals in mandatory17-movers.json remain required: canonical bracket copies2 and5 (original missing10/11) plus all15 cogs. Rebuild exact fixed-obstacle geometry from the corrected source transforms before a new coordinated placement investigation; none of the old fixed51 capacity/exclusion certificates transfers to these changed poses. Free both brackets in all8 orientations and legal sheets, and every cog center/real rotation. Retain original short-stock/material targets, source clearances and native guards; universal all-angle cog pair separation and global allocation necessities may be reused, but old position-dependent center regions may not. The49-part source pass is not a66-part target witness. No old feasibility call may be extended, reseeded or repeated. H2 unchanged;22 reserved vectors unopened. Main36f162d0 CI40400314122 browser-only attempt2 is live or must be checked by handle; preserve its successful other5 jobs and wait for all6 success before the normal queued checkpoint push. No release qualifies.','completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};bindings={};queue=[]
for folder in [OLD,BASE,RETRY]:
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
helpers=[ROOT/'output'/n for n in ['repair_h5_retained49_guards.py','audit_h5_retained49_guard_failure.py','construct_h5_retained49_stack_repair.py','audit_h5_retained49_stack_repair.py','ccd1.py','pack_h5_evidence_archive.py']];seen=set()
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
write(OUT/'checks.json',{'passed':True,'failed_repair_and_negative_cycle_preserved':True,'independent_repaired_original_ring_audit_passed':True,'source_valid_originals':49,'mandatory_movers':17,
    'source_pairs_verified':918,'stock_edges_verified':196,'source_cutouts_preserved':69,'source_hole_vertices_preserved':6294,'source_pair_failures':0,'source_stock_failures':0,
    'full66_witness':False,'native_calls':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text='All six checks now pass; a normal checkpoint push is qualified.' if ready else f'{success} of six checks pass; the browser-only retry remains in progress and must not be interrupted.'
report=f'''# H5: source guards repaired for the retained 49 originals — 2026-10-26

**The retained 49 non-cog originals now pass every current source-clearance and
stock guard.** All two bracket movers and 15 cogs remain mandatory. This prepares
the next coordinated construction; it is not a complete 66-part fit. H2/H5 stay
open at **60%**.

## The failed small repair is preserved

The previous retained source readback had six pair-clearance and three stock
failures. The first construction enclosed the fixed-orientation filled outlines
in outward integer component rectangles, required 225 µm component gaps and
allowed translations of at most 50 µm per axis. An exact integer difference
constraint pass found the construction inconsistent. Its independent reader
preserves an eight-edge negative cycle with sum **−29 µm**, involving inserts
0 through 6. This excludes that sufficient construction model, not source
repair in general.

The cycle identifies the needed correction: insert 0 requires at least 13 µm
upward movement for stock clearance; the seven-insert stack then requires
insert 6 to move at least **79 µm**. A separate deterministic construction
therefore permits those seven inserts up to 79 µm in positive Y. Every other
coordinate bound, orientation, sheet and source identity stays as before.
The 225 µm construction gap and actual source/native requirements are unchanged.
All component-pair bounds are recalculated for the changed ranges, including
1,458 far pairs; an old 50 µm far-pair claim is never reused unsafely.

The new 98-variable, 284-constraint system has an explicit integer assignment.
It takes one exact pass sequence, without random seeds, an external solver or
time-budget extension. All 49 originals receive translations; the maximum
absolute axis change is **0.079 mm**. The previous failure remains frozen.

## Full original-ring readback of the retained subset

The independent reader verifies all 98 shifts, every constraint, 88 near and
1,458 far component pairs, source identity, sheet and orientation preservation,
and the complete partition into 49 retained originals plus 17 mandatory movers.
It then transforms the original source rings directly, reserving filled outers
with part-in-hole off. All **918 same-sheet source pairs** and **196 stock
edges** pass. All **69 cutouts and 6,294 hole vertices** are preserved.

Minimum source gap is **0.2256789543045 mm**, above the unchanged
**0.2117086725096 mm** requirement. Minimum extra stock margin is
**0.0131000000000 mm**, above **0.0114440917969 mm**. There are zero retained
source pair or stock failures. No native call is made for this partial layout.

The next geometry must be rebuilt from these corrected source transforms.
The older fixed-51-pose capacity exclusion remains valid for its original input;
it cannot be transferred to this changed arrangement. The remaining mandatory
originals are bracket copies 2 and 5 in canonical labeling (the original missing
copies 10 and 11) and all 15 cogs. All must fit and pass full source, native and
material checks before any H5 or release claim.

## Main CI and evidence

The Windows check completed successfully after the preserved browser timeout,
leaving five successful jobs. Only the browser job was retried, after the first
attempt had fully stopped. [Main 36f162d0 attempt 2](https://github.com/skulitom/Nestbolt/actions/runs/40400314122)
at {review['utc']}: {ci_text} Production, READMEs and upstream heads/releases
are unchanged. No held-out vectors or new release are involved.

[Checks]({NAME}/checks.json), [source audit]({NAME}/source-checks.json),
[corrected 49 placements]({NAME}/corrected49-source.json),
[mandatory 17 movers]({NAME}/mandatory17-movers.json),
[failed repair]({NAME}/failed50um-result.json), [negative cycle]({NAME}/negative-cycle.json),
[next step]({NAME}/next-step.json) and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 retained49 source-guard repair, 2026-10-26:** [the evidence]({link})
repairs all six retained pair-clearance and three stock failures. The first
50 µm construction stays preserved with its exact −29 µm, seven-insert cycle.
A separately bounded correction derived from that cycle allows only those
seven inserts up to79 µm in positive Y; all source thresholds stay unchanged.
The independent reader verifies all49 originals, 918 source pairs, 196 stock
edges, 69 cutouts and6,294 hole vertices: zero failures, minimum gap0.2256789543 mm,
extra stock0.0131 mm. All17 remaining originals (two brackets and15 cogs) are
still mandatory. Rebuild geometry from the corrected poses; the old fixed51
capacity exclusion does not transfer. This is not a66-part witness, native
pass or H5 credit; H2/H5 remain open at60%. All22 reserved vectors stay unopened.
Main36f162d0's other five jobs passed before its browser-only attempt2 retry;
preserve that live retry and require all six successes before the queued push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'main_ci_successful_jobs':success,'push_qualified_now':ready})
