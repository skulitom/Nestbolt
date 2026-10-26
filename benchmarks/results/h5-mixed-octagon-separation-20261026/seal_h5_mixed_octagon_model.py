"""Seal source-contained mixed separation, one closed search and independent audits."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-mixed-octagon-separation-20261026';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-mixed-octagon-model-20261026';GEO=ROOT/'output/h5-mixed-octagon-geometry-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-retained64-proxy-witness-and-disk-proof-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head==main=='36f162d0df3d5c88eb4145c58004890b650fba61'
assert source_digest()==previous['production_digest'] and {n:digest(ROOT/n) for n in previous['current_readmes']}==previous['current_readmes']
ci=json.loads(command(['gh','run','view','40400314122','--json','databaseId,status,conclusion,headSha,jobs,url']));assert ci['headSha']==main and len(ci['jobs'])==6
success=sum(j['conclusion']=='success' for j in ci['jobs']);ready=ci['status']=='completed' and ci['conclusion']=='success' and success==6
upstream={'sparrow_head':command(['gh','api','repos/JeroenGar/sparrow/commits/main','--jq','.sha']),
    'studio_head':command(['gh','api','repos/JeroenGar/sparrow-studio/commits/main','--jq','.sha']),
    'sparrow_release':command(['gh','api','repos/JeroenGar/sparrow/releases/latest','--jq','.tag_name']),
    'studio_latest_release':json.loads(command(['gh','api','repos/JeroenGar/sparrow-studio/releases','--jq','map(.tag_name)']))}
assert all(upstream[k]==previous[k] for k in upstream)
geometry=load(GEO/'audit/checks.json');model=load(BASE/'model-audit/checks.json');response=load(BASE/'response-audit/checks.json')
assert all(r['passed'] for r in [geometry,model,response]) and model['all66_required']
assert model['variables_verified']==5217 and model['constraints_verified']==10008 and model['all8_demonstrated_pairs_rejected']
assert response['status']=='UNKNOWN' and response['closed'] and not response['has_necessary_assignment']
OUT.mkdir()
for p,n in [(GEO/'audit/checks.json','geometry-checks.json'),(GEO/'prepared.json','geometry-summary.json'),(GEO/'demonstrated-pairs.json','demonstrated-pairs.json'),
    (BASE/'model-audit/checks.json','model-checks.json'),(BASE/'model-audit/hint-rejections.json','hint-rejections.json'),
    (BASE/'response-audit/checks.json','response-checks.json'),(BASE/'built.json','model-summary.json'),(BASE/'search/result.json','closed-result.json')]:shutil.copyfile(p,OUT/n)
write(OUT/'main-ci-36f162d0-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,'production_digest':previous['production_digest'],
    'current_readmes':previous['current_readmes'],'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,
    'main_ci':40400314122,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,'push_qualified_now':ready,
    'completion_percent':60,'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,'solver_calls':1,'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'all66_originals_required':True,'every_original_coordinate_sheet_mode_free':True,'base_model_byte_identical':True,
    'all_real_cog_rotations_covered':True,'actual_cog_angles_selected':False,'mixed_pairs_constrained':8,'mixed_pairs_not_exhaustive':True,
    'all8_bracket_variants_both_sheets_all3_components':True,'source_contained_octagon_only':True,'virtual_cog_disks_never_used_for_mixed_collisions':True,
    'advisory_hints_not_fixed':True,'old_hint_violates_new_constraints':True,'boundary_contact_allowed_as_necessary_relaxation':True,
    'solver_status':'UNKNOWN','source_layout_claimed':False,'unrestricted_exclusion_claimed':False,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'The5217-variable/10008-constraint mixed model is CLOSED UNKNOWN after one60-second call; do not repeat, extend or reseed it. The source-contained octagon rules are now independently audited and can be reused in a materially different geometric investigation. Derive all-angle cog-center free regions against the complete non-cog arrangement from the saved66 proxy construction, using all source-contained frame/insert/bracket components and original cog stock support. All15 cogs must remain mandatory. Test whether the existing non-cog arrangement can possibly admit its12 first-sheet cogs under the proven all-angle cog-pair center separation; preserve any fixed-position obstruction as local only. This can identify which frame/bracket/insert placements must move for a new coordinated construction, rather than opening another unchanged feasibility call. Full original-ring/source validity and exact material target remain required before native. H2 unchanged and22 reserved vectors unopened. Preserve main36f162d0 CI40400314122; push normally only after all6 jobs pass. No release qualifies.','completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};bindings={};queue=[]
for folder in [BASE,GEO]:
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    queue.append(folder/'plan.json')
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
helpers=[ROOT/'output'/n for n in ['prepare_h5_mixed_octagon_constraints.py','audit_h5_mixed_octagon_constraints.py','build_h5_mixed_octagon_model.py',
    'audit_h5_mixed_octagon_model.py','run_h5_mixed_octagon_model.py','audit_h5_mixed_octagon_response.py','ccd1.py','pack_h5_evidence_archive.py']];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_geometry_model_response_audits':3,'all66_required':True,'all8_demonstrated_pairs_rejected':True,
    'variables_verified':5217,'constraints_verified':10008,'status':'UNKNOWN','has_assignment':False,'native_calls':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text='All six preceding main checks pass; a normal checkpoint push is qualified.' if ready else f'{success} of six preceding main checks pass; preserve the remaining live checks before pushing.'
report=f'''# H5: all-angle mixed cog/bracket separation — 2026-10-26

**Exact source-contained geometry detects all eight demonstrated cog/bracket
collisions, but the strengthened model closes UNKNOWN without a layout.**
H2/H5 remain open at **60%**. This is neither a source witness nor an
unrestricted impossibility proof.

## Source geometry

The earlier all-angle cog disk has quantization-safe radius 109,113 µm. An
eight-vertex integer octagon lies inside that disk: cardinal reach 109,113 µm,
diagonal coordinates 77,154 µm. It therefore lies inside the original cog at
every real rotation. This is source-contained geometry, not the larger virtual
disk used only for cog/cog capacity.

Each of the eight bracket variants has three source-contained component
rectangles. Their Minkowski sums with the reflected octagon produce 24 convex
forbidden polygons, each with 12 integer facets. For relative anchor
`cog - bracket`, strict interior is forbidden; at least one inward facet must
satisfy `nx*dx + ny*dy <= rhs`. Boundary contact is retained as a necessary
relaxation, so passing does not establish the required cutting clearance.

An independent integer support certificate verifies all eight octagon vertices,
24 sums, 288 facets and 9,216 point-sum support checks. It confirms that the
octagon detects all eight physical collision pairs from the complete proxy
assignment. It also covers all 26 previously derived fixed-position bracket
anchor cells, with 1,248 exact corner/facet checks. That fixed-position result
does not exclude layouts where existing parts move.

## All originals remain movable

The new serialized model preserves every original variable/domain and all
5,016 base constraints byte for byte. For each of the eight demonstrated pairs,
it adds separation for all eight bracket variants, both sheets and all three
components. The resulting **384 conditional clauses and 4,608 facet
inequalities** yield **5,217 variables and 10,008 constraints**.

A clause activates only when the bracket selects that variant and both
originals select the same sheet. Each chosen facet enforces its outside
inequality. Inactive cases can set all their facet selectors false. All 66
originals are mandatory; no original coordinate, sheet or mode is fixed.
The prior 609-value necessary assignment is an advisory hint, and the audit
explicitly verifies that the new clauses reject it for all eight pairs. These
eight pairs do not exhaust the source collision checks required for a layout.

The independent reader verifies the entire unchanged prefix, every new Boolean,
halfplane and conditional clause, and each hint. Model SHA-256:
`{model['model_sha256']}`.

## Closed bounded search

One call requests 60 solver seconds within 90 shared seconds, with `fj`
excluded. It returns **UNKNOWN**, with **127,806 branches and 54,245 conflicts**.
Solver time is **60.056504 seconds**, returned solve **60.063253**, shared
process **61.378682**. The small soft overruns are preserved. The independent
response audit checks the saved model, parameters, raw response, log and
process boundary. There is no assignment, native call or quality run.

The call is closed without extension, retry or reseeding. A distinct next
investigation can derive cog-center free regions against all non-cog source
components in the saved arrangement, then apply the proved all-angle cog/cog
separation to locate which existing non-cog poses need coordinated movement.
Any fixed-position obstruction must stay scoped to that arrangement. The
original full-source and material requirements remain unchanged.

## Repository and evidence

At {review['utc']}, [main 36f162d0 checks](https://github.com/skulitom/Nestbolt/actions/runs/40400314122):
{ci_text} Production, READMEs and upstream heads/releases are unchanged.
All 22 reserved H2 vectors remain unopened. No new release qualifies.

[Checks]({NAME}/checks.json), [geometry audit]({NAME}/geometry-checks.json),
[model audit]({NAME}/model-checks.json), [response audit]({NAME}/response-checks.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json) and
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']} canonical files and {archive['verified_aliases']}
identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 mixed all-angle separation, 2026-10-26:** [the evidence]({link})
verifies a source-contained cog octagon and 24 exact bracket-component forbidden
polygons. They detect all eight demonstrated collisions and cover all 26 fixed
anchor cells. The strengthened all-original model leaves positions, sheets and
modes free, preserves the entire previous model, and adds 384 conditional
separation clauses/4,608 facets. All 5,217 variables/10,008 constraints and 609
advisory hints are audited; the old hint violates the new rules. The sole call
closes UNKNOWN: 127,806 branches, 54,245 conflicts, 60.063253 returned/61.378682
shared seconds, with small soft overruns preserved. Three independent audits
pass, but no source/native witness or unrestricted exclusion exists. No retry
or reseeding is permitted. H2/H5 stay open at 60%; no release qualifies and all
22 reserved vectors remain unopened. Preserve main36f162d0 CI40400314122 until
all six checks pass before the next normal push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'main_ci_successful_jobs':success,'push_qualified_now':ready})
