"""Preserve verified coupled-sheet source necessities before opening a new solver."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-allocation-aware-geometry-20261026';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/h5-allocation-geometry-20261026';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def command(a):return subprocess.check_output(a,cwd=ROOT,text=True).strip()
previous=load(ROOT/'benchmarks/results/h5-source-capacity-profiles-20261026/source-review.json')
head=command(['git','rev-parse','HEAD']);main=command(['git','ls-remote','origin','refs/heads/main']).split()[0]
assert head.startswith('09091745') and main==previous['remote_main'] and command(['git','rev-parse','HEAD^'])==main
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
audit=load(BASE/'audit/checks.json');assert audit['passed'] and audit['all66_originals_verified'] and audit['all_cog_angles_continuous']
assert audit['short_allocations_verified']==454 and audit['solver_calls']==audit['native_calls']==0
OUT.mkdir()
for n in ['prepared.json','variants.json','domains.json','stocks.json','allowed-allocations.json','originals.json']:
    shutil.copyfile(BASE/n,OUT/n)
shutil.copyfile(BASE/'audit/checks.json',OUT/'geometry-checks.json')
write(OUT/'main-ci-ff5036af-snapshot.json',ci)
review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'remote_main':main,
    'production_digest':previous['production_digest'],'current_readmes':previous['current_readmes'],
    'production_and_readmes_unchanged':True,**upstream,'upstream_heads_and_releases_unchanged':True,
    'main_ci':40393931732,'main_ci_status':ci['status'],'main_ci_successful_jobs':success,
    'push_qualified_now':ready,'unpublished_prior_checkpoints':1,'completion_percent':60,
    'H2_complete':False,'H5_complete':False,'reserved_H2_vectors_evaluated':0,
    'solver_calls':0,'native_calls':0,'quality_runs':0,'new_release_qualified':False}
write(OUT/'source-review.json',review)
write(OUT/'scope.json',{'all66_originals_required':True,'all454_surviving_count_vectors_retained':True,
    'pareto_only_restriction':False,'fixed_short_sheet':False,'all_real_cog_rotations':True,
    'all8_bracket_modes':True,'both_frame_insert_outer_shapes':True,
    'source_disk_for_mixed_family_capacity':True,'virtual_separation_disk_for_cogs_only':True,
    'necessary_stock_relaxation_only':True,'actual_source_target_unchanged':True,
    'positive_necessary_result_not_source_fit':True,'solver_calls':0,'native_calls':0,'H5_complete':False})
write(OUT/'next-step.json',{'action':'Use this audited geometry to build a genuinely coupled two-sheet necessary model. Keep all66 originals mandatory and each exactly one legal(sheet,variant) option; allow all454 short count vectors through linked bracket/insert/cog counts. Frames have no short-sheet option. Give each original shared X/Y anchors plus a sheet indicator and optional geometry intervals selected by its variant. Non-overlap uses only source-contained coarse rectangles; source-capacity cumulative constraints use the non-cog inner rectangles and16 rotation-independent cog disk strips. Add separate cumulative constraints using16 virtual separation-disk strips ONLY among cogs: never mix those virtual strips with frames/brackets/inserts. Retain outward necessary stock domains but the actual full-source acceptance target must stay unchanged. Equivalent copies may be ordered by sheet thenY, with no fixed first-sheet positions or fixed short allocation. Independently verify every serialized variable, option, stock guard, optional interval, count-table row and capacity constraint before one declared bounded solve. Ignore the previously overlong fj worker and preserve all terminal results without unchanged retries. A necessary assignment still needs actual cog angles and full original-ring validation before any native check. No model or solver for this allocation-aware geometry has opened yet. H2 unchanged,22 reserved vectors unopened; wait for all6 main ff5036af CI40393931732 checks before pushing queued checkpoints.',
    'completion_percent':60,'H2_complete':False,'H5_complete':False})
members={};inputs=load(BASE/'plan.json')['inputs']
for p in BASE.rglob('*'):
    if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
for n,h in inputs.items():assert digest(ROOT/n)==h,n;members['source-inputs/'+n]=ROOT/n
write(OUT/'source-bindings.json',inputs)
helpers=[ROOT/'output'/n for n in ['prepare_h5_allocation_geometry.py','audit_h5_allocation_geometry.py','ccd1.py','pack_h5_evidence_archive.py']];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_geometry_audit_passed':True,'all66_originals_accounted':True,
    'source_variants':13,'verified_domain_endpoints':104,'short_allocation_vectors':454,
    'all_real_cog_rotations':True,'virtual_disk_restricted_to_cogs':True,
    'solver_calls':0,'native_calls':0,'completion_percent':60,'H2_complete':False,'H5_complete':False,**archive})
shutil.copyfile(__file__,OUT/Path(__file__).name)
ci_text=('All six checks pass; a normal checkpoint push is qualified.' if ready else f'{success} of six checks pass; preserve the remaining live checks before the next push.')
report=f'''# H5: geometry for variable two-sheet allocations — 2026-10-26

**The next model can vary the short-sheet composition while retaining all 66
originals and every real cog rotation.** Its source geometry and allocation
domains are now independently verified. No allocation-aware solver has opened
and no complete layout or exclusion is claimed. H2/H5 remain open at 60%.

## Removing the fixed short-sheet assumption

The prepared geometry retains **all 454 necessary surviving count vectors** from
the earlier full short-sheet frontier, not just its 32 Pareto vectors. Each
vector carries the exact complementary first-sheet counts. Restricting to the
Pareto vectors would not be justified by source feasibility, so no such
restriction is introduced. All 18 frames remain on the first sheet because
their minimum allowed height is 350 mm, greater than the short sheet.

Thirteen geometry variants cover all eight bracket quarter-turn/mirror modes,
both rectangular frame and insert footprints, and one cog proxy valid at every
real rotation. Half-turns of the rectangular filled outers are geometrically
equivalent; their holes remain reserved. There are 26 variant/sheet domains,
24 of them allowed. The two excluded domains are the short-sheet frame modes.

The non-cog rectangles retain two-micrometre insets to absorb coordinate
flooring. An independent reader transforms original source rings with exact
quarter turns, proves their grid-cell containment after expanding each rectangle
by one micrometre, and checks component disjointness. It verifies all 28
non-cog rectangles and every legal outline orientation.

## Two different cog bounds

The previously audited all-angle source proof supplies a **109.113 mm**
quantization-safe inscribed disk. A 153 mm coarse square and 16 horizontal strips
lie inside that disk for every rotation. The strips occupy **33,830.014276 mm²**.
These source-contained shapes may participate in necessary collision/capacity
constraints with all other part families.

A different bound comes from the independently certified **254.297 mm minimum
separation of rounded cog centers**, valid for every pair of real rotations.
Disks of radius **127.148 mm** about those centers therefore cannot overlap one
another. Their 16 inner strips occupy **45,936.033464 mm²**. These larger disks
are **not source-contained**: they may constrain cog-to-cog capacity only and
must never be used as mixed-family collision shapes.

The all-angle stock support radius is 139.270 mm, larger than the virtual disk
radius, so these virtual disks remain inside the relaxed stock for every allowed
center. The new audit checks 132 exact integer disk corners, the center-distance
inequality, all eight virtual-disk stock edges and all 104 domain endpoints.

## Necessary relaxation and acceptance remain separate

The original source short top remains **319.4269023299994 mm**. The mathematical
necessary bounds use the existing outward top **319.42699 mm** and an additional
0.020 mm outward stock relaxation for quantization. These relaxations cannot be
used to accept a layout, enlarge the material target or bypass native guards.

The geometry audit verifies all 66 unique original identities, all 454 count
vectors and their complements, all mode/stock domains and the separate uses of
the source and virtual cog disks. A future positive necessary assignment still
needs actual cog angles, full original-ring readback and native/material checks.
The current work contains **zero solver calls and zero native calls**.

The concrete next model can give each original exactly one sheet/mode option,
with optional source rectangles, source-capacity strips and a separate cog-only
virtual-capacity system. All count choices must remain linked to those options.
The serialized model must be independently checked before a bounded solve.
All prior fixed-allocation calls remain closed and are not extended or reseeded.

## Repository and evidence

At {review['utc']}, [main ff5036af checks](https://github.com/skulitom/Nestbolt/actions/runs/40393931732):
{ci_text} The preceding 09091745 checkpoint remains queued locally. Production,
READMEs and upstream heads/releases are unchanged. All 22 reserved H2 vectors
remain unopened, and no new release is qualified.

[Checks]({NAME}/checks.json), [independent geometry]({NAME}/geometry-checks.json),
[variants]({NAME}/variants.json), [stock domains]({NAME}/domains.json),
[all allocations]({NAME}/allowed-allocations.json), [scope]({NAME}/scope.json),
[next step]({NAME}/next-step.json) and [raw manifest]({NAME}/raw-manifest.json).
The archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**N4 variable-allocation geometry, 2026-10-26:** [the evidence]({link})
prepares all 66 originals for a coupled two-sheet model with all 454 surviving
short count vectors and their first-sheet complements. Thirteen source proxy
variants cover all bracket modes, both rectangular frame/insert footprints and
every real cog rotation; 24 of 26 sheet/mode domains are allowed. An independent
audit verifies 28 quantization-safe non-cog rectangles, 132 integer disk corners,
104 domain endpoints and every count vector. Cog source strips use the proved
109.113 mm inner disk. Separate 127.148 mm virtual separation disks follow from
the 254.297 mm rounded-center bound and may constrain cogs only, never mixed
families. Mathematical stock relaxations do not change the source/material
acceptance target. No allocation-aware model or solver has opened yet. Prior
calls remain closed. H2/H5 stay open at 60%; no native/full-quality run or release
qualifies and all 22 reserved H2 vectors remain unopened. Preserve main
ff5036af CI40393931732 until all six checks pass before the next normal push.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive,'main_ci_successful_jobs':success,'push_qualified_now':ready})
