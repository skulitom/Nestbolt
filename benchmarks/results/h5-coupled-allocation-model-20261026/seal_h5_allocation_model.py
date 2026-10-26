"""Preserve the first fully coupled all-original necessary model and closed response."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-coupled-allocation-model-20261026';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-allocation-model-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-allocation-aware-geometry-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head.startswith('1cc9300c') and main==previous['remote_main'] and command(['git','rev-parse','HEAD~2'])==main
assert source_digest()==previous['production_digest']
assert {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40393931732','--json','databaseId,status,conclusion,headSha,jobs,url']))
assert ci['headSha']==main and len(ci['jobs'])==6
success=sum(j['conclusion']=='success' for j in ci['jobs']);ready=ci['status']=='completed' and ci['conclusion']=='success' and success==6
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
    'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
    'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
    'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
model=load(BASE/'model-audit/checks.json');response=load(BASE/'response-audit/checks.json')
assert model['passed'] and response['passed'] and model['all66_required']
assert model['variables_verified']==609 and model['constraints_verified']==5016
assert response['status']=='UNKNOWN' and response['closed'] and not response['has_necessary_assignment']
OUT.mkdir()
for p,n in [(BASE/'model-audit/checks.json','model-checks.json'),(BASE/'response-audit/checks.json','response-checks.json'),
            (BASE/'built.json','model-summary.json'),(BASE/'source-area-coefficients.json','source-area-coefficients.json'),
            (BASE/'model-audit/source-area-excluded-count-vectors.json','source-area-excluded-count-vectors.json'),
            (BASE/'search/result.json','closed-result.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-ff5036af-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,
    'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],
    'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,
    'main_ci':40393931732,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,
    'push_qualified_now':ready,'unpublished_prior_checkpoints':2,'completion_percent':60,
    'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,
    'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'all66_originals_required':True,'exactly_one_sheet_and_variant_per_original':True,
    'fixed_short_sheet':False,'all_real_cog_rotations_covered_by_necessary_proxy':True,
    'actual_cog_angles_selected':False,'all454_count_rows_linked':True,'source_area_constraints_additional':True,
    'source_only_nonoverlap':True,'virtual_capacity_cogs_only':True,'solver_status':'UNKNOWN',
    'has_assignment':False,'unrestricted_exclusion_claimed':False,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The609-variable/5016-constraint coupled model is CLOSED UNKNOWN after one60-second call; do not extend, repeat or reseed it. All66 originals, variable allocation and every real cog angle remain covered by its necessary geometry. There is no assignment or infeasibility proof. A different constructive investigation can map the preserved source-valid64-original layout at output/h5-latest-wide-joint-20261023/layout-audit/layout-final.json and repaired9-part short sheet into these exact necessary proxies, preserving both missing bracket copies as mandatory. First independently determine which proxy constraints those fixed originals satisfy; if they do, derive deterministic feasible-anchor regions for the two missing bracket source modes against the coarse shapes, then check both source and virtual cumulative capacities for each proposed pair. Do not reopen any old fixed-source neighborhood solver or call a proxy placement a complete source fit. A useful necessary assignment must lead to actual original-ring collision analysis and a materially different source-aware construction, not an unchanged coupled-model retry. All prior partials and failed calls stay preserved. H2 unchanged and22 reserved vectors unopened. Await all6 main ff5036af CI40393931732 checks before the next normal push. No release qualifies.',
    'completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs=load(BASE/'plan.json')['inputs']
for p in BASE.rglob('*'):
    if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
for n,h in inputs.items():assert digest(ROOT/n)==h,n;members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=[ROOT/'output'/n for n in ['build_h5_allocation_model.py','audit_h5_allocation_model.py',
    'run_h5_allocation_model.py','audit_h5_allocation_response.py','ccd1.py','pack_h5_evidence_archive.py']];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_model_and_response_audits_passed':True,
    'all66_originals_required':True,'variables_verified':609,'constraints_verified':5016,
    'sheet_variant_choices_verified':342,'optional_rectangles_verified':1686,
    'source_area_count_exclusions':4,'status':'UNKNOWN','has_assignment':False,'native_calls':0,
    'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text=('All six checks pass; a normal checkpoint push is qualified.' if ready else f'{success} of six checks pass; preserve the remaining live checks before the next push.')
report=f'''# H5: fully coupled two-sheet necessary model — 2026-10-26

**The new model allows each of the 66 originals to choose its sheet and geometry
variant, but its one bounded search returns UNKNOWN without an assignment.**
There is no source layout or impossibility proof. H2/H5 remain open at 60%.

## Every original, linked to both sheets

The model has **609 variables and 5,016 constraints**. Each original chooses
exactly one of its legal sheet/variant options; there are **342 options** in
total. A shared X/Y anchor is bounded by four guards for the selected option.
The sheet bit is linked to that same choice. A sheet/Y key orders identical
copies without fixing positions or the short-sheet allocation.

The three short-sheet counts are sums of the original sheet bits and are linked
to all **454 surviving count vectors**. The model also checks filled original
source area on both sheets, using downward-rounded integer square-micrometre
coefficients and the original target stock areas. Proxy areas are not used for
these two constraints. They rule out four further short vectors `[bracket,
insert,cog]`: `[0,0,0]`, `[0,1,0]`, `[0,2,0]` and `[1,0,0]`.

These count exclusions do not exclude the full job. The mathematical stock
relaxations used by geometry never enlarge the source/material acceptance
target. All frames stay on the first sheet, and all 15 cogs remain represented
by the previously proved all-angle necessities.

## Optional source geometry and separate cog capacity

The selected source-contained coarse rectangles participate in one NoOverlap2D
per sheet. There are 381 optional coarse rectangles for the first sheet and 345
for the short sheet. Only rectangles belonging to selected options are active.
Four source-capacity constraints use the non-cog rectangles and the 16 source
inner-disk strips per cog: 606/570 optional rectangles by sheet.

Four different capacity constraints use the virtual separation disks **only
among cogs**, with 240 optional rectangles per sheet. Those virtual disks never
enter mixed-family collision or source-capacity constraints. All 1,686 optional
rectangles use the same selected sheet/variant literal as their parent original.
Actual cog angles are not chosen by this necessary model.

An independent protobuf reader checks every variable and all 5,016 constraints,
including 1,368 stock guards, 3,372 optional intervals, all 62 copy orders, the
linked table, both source-area bounds and every capacity membership. It verifies
that every original is mandatory, every option activates only its own geometry,
no short allocation is fixed, and there are no hints or objective. The model
SHA-256 is `1027dd1d8bf01231e52b0fe4d5ff9ac42832a07e77ce1eae0b8e8317dd0585b2`.

## One closed search

The sole call requests 60 solver seconds within 90 shared seconds, with the
previously overlong `fj` worker excluded. It starts real search and returns
**UNKNOWN**, recording **87,096 branches and 62,265 conflicts**. Solver time is
**60.054159 seconds**, returned solve **60.056339**, shared process **61.456279**.
The 0.054159/0.056339 second soft overruns are preserved. No assignment, source
candidate, native call or full quality run is produced.

The response audit verifies the model hash, parameters, raw solver response,
log and closed process boundary. The call is CLOSED without extension,
reseeding or retry. These checks do not establish infeasibility of this necessary
model or the complete source job.

The next distinct investigation can map the earlier preserved 64-original
source layout into these necessary geometries and construct explicit proxy
anchor regions for its two missing bracket copies. Both missing originals must
remain mandatory. Any resulting proxy assignment still needs actual original
collision analysis; it must not be presented as a source layout or used merely
to rerun this unchanged coupled solver.

## Repository and evidence

At {review['utc']}, [main ff5036af checks](https://github.com/skulitom/Nestbolt/actions/runs/40393931732):
{ci_text} Checkpoints 09091745 and 1cc9300c remain queued locally. Production,
READMEs and upstream heads/releases are unchanged. All 22 reserved H2 vectors
remain unopened, and no new release is qualified.

[Checks]({NAME}/checks.json), [full model audit]({NAME}/model-checks.json),
[response]({NAME}/response-checks.json), [source-area exclusions]({NAME}/source-area-excluded-count-vectors.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json) and
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 coupled two-sheet model, 2026-10-26:** [the evidence]({link})
links every one of the 66 originals to exactly one sheet/mode choice, with 342
options, all 454 short count rows, no fixed short allocation and all-angle cog
necessities. The independent reader verifies all 609 variables/5,016 constraints,
1,368 stock guards, 1,686 optional rectangles, both source-area constraints and
separate source/cog-only virtual capacities. Filled source area excludes four
further count vectors, without excluding the job. The sole call closes UNKNOWN:
87,096 branches, 62,265 conflicts, 60.056339 returned/61.456279 shared seconds.
Small soft overruns are preserved; no assignment or source/native witness exists.
The model and response audits pass, and the closed call cannot be extended or
reseeded. H2/H5 remain open at 60%; no full-quality run or new release qualifies,
and all 22 reserved H2 vectors remain unopened. Preserve main ff5036af
CI40393931732 until all six checks pass before the next normal push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'main_ci_successful_jobs':success,'push_qualified_now':ready})
