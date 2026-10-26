"""Preserve the fixed-noncog capacity exclusion and main browser timeout evidence."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-fixed-noncog-cog-capacity-20261026';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-fixed-noncog-center-regions-20261026';MODEL=BASE/'upper-five-model';CIROOT=ROOT/'output/h5-main36-web-timeout-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-mixed-octagon-separation-20261026/source-review.json');head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head=='76faef4cb461a77539cd2373c8b2eda18eb8ec09' and main==command(['git','rev-parse','HEAD~1'])=='36f162d0df3d5c88eb4145c58004890b650fba61'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40400314122','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and len(ci['jobs'])==6
success=sum(j['conclusion']=='success' for j in ci['jobs']);ready=ci['status']=='completed' and ci['conclusion']=='success' and success==6
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
    'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
    'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
    'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
geometry=load(BASE/'audit/checks.json');model=load(MODEL/'model-audit/checks.json');response=load(MODEL/'response-audit/checks.json')
assert all(r['passed'] for r in [geometry,model,response]) and response['fixed51_noncog_arrangement_excluded'] and response['total_cog_upper_bound_with_fixed_noncogs']==14
job=load(CIROOT/'job.json');annotations=load(CIROOT/'annotations.json');assert job['conclusion']=='cancelled' and any('maximum execution time of 30m0s' in a['message'] for a in annotations)
for name in ['job','check','annotations','logs']:
    receipt=load(CIROOT/f'{name}-receipt.json');p=CIROOT/(name+('.log' if name=='logs' else '.json'));assert receipt['exit_code']==0 and digest(p)==receipt['sha256'] and p.stat().st_size==receipt['bytes']
OUT.mkdir()
for p,n in [(BASE/'audit/checks.json','geometry-cover-graph-checks.json'),(BASE/'audit/upper-region-necessary-bounds.json','upper-region-bounds.json'),
    (BASE/'cell-capacity/result.json','coarse-cell-search-result.json'),(BASE/'refined-upper-capacity/result.json','auxiliary-refined-cell-result.json'),
    (MODEL/'model-audit/checks.json','model-checks.json'),(MODEL/'response-audit/checks.json','response-checks.json'),(MODEL/'built.json','model-summary.json'),
    (MODEL/'search/result.json','closed-result.json'),(BASE/'diagnostic-first-sheet.png','diagnostic-first-sheet.png'),
    (CIROOT/'annotations.json','main-web-timeout-annotations.json'),(CIROOT/'timing-diagnosis.json','main-web-timing-diagnosis.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-36f162d0-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],
    'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,'main_ci':40400314122,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,
    'browser_job':121844092009,'browser_job_terminal_timeout':True,'browser_job_agent_cancelled':False,'push_qualified_now':ready,'unpublished_prior_checkpoints':1,
    'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'solver_calls':1,'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'fixed_noncog_originals':51,'mandatory_cog_originals':15,'cog_centers_and_real_rotations_free':True,'cog_sheet_assignments_free_under_capacity_necessity':True,
    'first_sheet_component_upper_bounds':[6,4,1],'short_sheet_upper_bound':3,'total_upper_bound':14,'source_necessity_model_status':'INFEASIBLE',
    'at_least_one_noncog_pose_or_orientation_must_change':True,'fixed_noncog_arrangement_excluded':True,'unrestricted_job_excluded':False,
    'source_layout_found':False,'actual_angles_selected':False,'auxiliary_floating_and_refined_geometry_not_used_in_exclusion':True,
    'solver_infeasibility_not_external_formal_unsat_certificate':True,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The fixed51-noncog arrangement is now excluded for all15 cogs, at every real cog angle and any cog sheet assignment, by the audited6+4+1 first-sheet and3 short-sheet capacity bounds. Do not repeat either closed cell search or the upper-five model. A materially different construction can free the two added brackets (canonical indices20 and23, corresponding to original missing copies10/11) together with all15 cogs while retaining the other49 non-cog poses. Both bracket originals must remain mandatory with all8 orientations and legal sheets; all15 cogs remain mandatory with free centers. Use exact source-contained non-cog/cog mixed exclusions, the audited whole-stock domains and tighter64-facet necessary cog-pair separation rather than another unrestricted609-variable model. Account for each bracket/cog allocation and fixed short non-cogs; do not drop the two brackets or any cog. A positive necessary solution still needs actual original-ring positions/angles and full source/native/material validation. If that fixed49 subset is excluded, use the obstruction to free a concrete additional non-cog group rather than rerunning it. Preserve all failures and unchanged H2 decision. Main36f162d0 CI40400314122 has a terminal browser timeout after24+ minutes of Ubuntu dependency downloads; preserve its raw logs and wait for the live Windows check before a browser-only retry. Do not push while CI is live, and only push after six successful jobs. No release qualifies.','completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};bindings={};queue=[]
for folder in [BASE,CIROOT]:
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
        p=ROOT/n;assert digest(p)==h,n
        if n in bindings:assert bindings[n]==h
        bindings[n]=h;members['source-inputs/'+n]=p
        if p.name=='plan.json':queue.append(p)
write(OUT/'source-bindings.json',bindings)
helpers=[ROOT/'output'/n for n in ['prepare_h5_fixed_noncog_center_regions.py','build_h5_fixed_noncog_cell_cover.py','prove_h5_fixed_noncog_cell_capacity.py',
    'refine_h5_fixed_noncog_upper_region.py','prove_h5_refined_upper_capacity.py','audit_h5_fixed_noncog_regions.py',
    'build_h5_upper_five_center_model.py','audit_h5_upper_five_center_model.py','run_h5_upper_five_center_model.py','audit_h5_upper_five_response.py','ccd1.py','pack_h5_evidence_archive.py']];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits':3,'whole_domain_boundary_complete':True,'fixed51_noncog_arrangement_excluded':True,
    'cog_upper_bound':14,'mandatory_cogs':15,'unrestricted_exclusion_claimed':False,'source_witness':False,'native_calls':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: the saved non-cog arrangement cannot hold all 15 cogs — 2026-10-26

**At least one of the 51 non-cog poses or orientations must change.** With those
poses fixed, audited necessary geometry permits at most **14 of the 15 required
cogs**, even if every cog moves, rotates freely and changes sheet. This excludes
the saved arrangement only; it does not exclude a different complete layout.
H2/H5 remain open at **60%**.

## Whole-domain center cover

The complete proxy construction contains all 51 non-cog originals. Their 75
source-contained component rectangles are expanded by the independently proved
all-angle cog octagon, producing 75 convex integer forbidden polygons and 900
facets. An independent support reader verifies all source identities and
28,800 point-sum support checks. Cog center stock domains retain the original
audited all-angle support and its outward necessary relaxation.

Each closed stock domain is tiled by 10 mm cells. A cell is discarded only if
every corner is strictly inside one forbidden convex polygon. Convexity then
excludes every point in that cell. Remaining closed cells retain all possible
centers, including isolated legal boundary points and segments that a floating
polygon difference might omit. The audit checks **33,275 cells**, including
**30,979 strict exclusions**, **2,296 remaining cells** and **1,486,992 exact
corner/facet tests**. The first sheet has three remaining components of
1,115, 914 and 43 cells; the short sheet has one of 224 cells.

## Exact cell capacity certificates

The earlier full-circle source certificate requires rounded cog centers to be
at least **254,297 µm** apart. Each cell is smaller than that diameter. Two
cells are compatible only if their maximum possible point distance reaches the
required separation. Any placement of k cog centers therefore implies a
k-clique in this conservative graph.

The independent reader checks **1,064,175 graph vertex pairs** and **748 exact
color/branch certificate nodes**. Exhaustion proves that the lower first-sheet
component holds at most **six** cogs, the small component at most **one**, and
the short sheet at most **three**. No heuristic graph coloring is treated as
an exact answer: every excluded target has a complete branch certificate.

The upper component initially admits a five-cell clique. Its pairwise rectangle
distances can use different corners for different neighbors, so that is not a
point placement. An auxiliary rational clipping/refined graph still finds a
five-cell clique; its unverified coverage is not used in the exclusion below.
The floating plot, hex-grid scan and refined geometry are retained as
diagnostics only. The audited original closed-cell cover remains authoritative.

## Five upper centers are necessary, then excluded

Since the other regions hold at most 6 + 1 + 3 = 10 cogs, fitting all 15 requires
at least five centers in the upper component. This implication allows any cog
sheet allocation. It does not freeze the previous 12/3 allocation.

A new necessary model gives those five centers free integer coordinates in the
upper component's conservative bounding box and minimum x+y support. Each
center must remain outside the relevant source-contained forbidden polygons.
Exact domain separation makes 49 of the 61 first-sheet polygons irrelevant;
the other 12 produce 60 source clauses. Each of the ten center pairs must lie
outside a 64-vertex integer polygon strictly inside the disk of radius
254,297 µm. Every valid source center pair satisfies this necessary condition.
Only equivalent-copy X ordering is imposed; there are no hints or objective.

The independent reader verifies all **1,370 variables and 1,439 constraints**,
all source clauses, all ten pair clauses and the 64 exact radius/convexity
certificates. The single call returns **INFEASIBLE** after **12,464 branches and
2,439 conflicts**, in **0.408622 solver / 0.413757 returned / 1.759713 shared
seconds**, within the declared 60/90-second limits. Its model hash is
`{model['model_sha256']}`. The response audit binds the model, parameters,
raw response, log and process boundary. This uses the solver's infeasibility
result; it is not an external formal UNSAT certificate.

Thus the first-sheet component bounds are **6 + 4 + 1 = 11**, and the short
sheet holds at most **3**. Total capacity is **14**, below the mandatory **15**.
Moving or rotating cogs alone cannot repair these fixed non-cog poses. The next
distinct construction can free both newly added brackets together with all cogs,
retaining the other 49 non-cog poses and keeping every original mandatory.
No complete source layout, native call or H5 material pass is claimed.

![Diagnostic center regions; red crosses show old cog centers]({NAME}/diagnostic-first-sheet.png)

## Main CI and preservation

At {review['utc']}, [main 36f162d0](https://github.com/skulitom/Nestbolt/actions/runs/40400314122)
has {success} successful jobs. The browser job reached its configured 30-minute
limit after dependency setup consumed over 24 minutes. Raw logs identify long
downloads from the Ubuntu package mirror, including a 278.903-second gap while
fetching libcodec2. The browser tests started, but no full-suite pass is claimed.
The timeout was not caused by an agent cancellation or a new push. Its raw job,
annotations, logs and checksums are preserved; a Windows check was still live
when the timeout was diagnosed. Wait for that check before retrying only the
browser job, and require six successful jobs before the next normal push.
A post-capture console encoding error is also retained; all four network
captures had succeeded and no capture was repeated.

Production, READMEs and upstream heads/releases are unchanged. The 22 reserved
H2 vectors remain unopened. No new release qualifies.

[Checks]({NAME}/checks.json), [whole-domain/graph audit]({NAME}/geometry-cover-graph-checks.json),
[model audit]({NAME}/model-checks.json), [response audit]({NAME}/response-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[timeout annotations]({NAME}/main-web-timeout-annotations.json) and
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 fixed-noncog capacity, 2026-10-26:** [the evidence]({link})
excludes the saved 51 non-cog poses even when all 15 cog centers, real rotations
and sheet assignments are free. The exact whole-domain cover checks 33,275
closed cells and preserves boundary centers. Independent graph/branch readers
prove lower/small/short capacities of 6/1/3. A new necessary five-center upper
model, with all 1,370 variables/1,439 constraints audited, closes INFEASIBLE in
0.413757 returned/1.759713 shared seconds. The combined capacity is 6+4+1+3=14,
below 15: at least one non-cog pose or orientation must change. This is a fixed
arrangement exclusion, not unrestricted impossibility or a source witness.
Three audits pass; no native call, H5 credit or release follows. H2/H5 remain
open at 60% and all 22 reserved vectors are unopened. Main36f162d0 browser CI
timed out after slow Ubuntu dependency downloads; raw failure evidence is kept.
Preserve its live Windows check before retrying only the browser job, and require
all six successful jobs before pushing the queued checkpoints.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'main_ci_successful_jobs':success,'push_qualified_now':ready})
