"""Seal directional reductions and the necessary eight-angle family exclusion."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-necessary-direction-and-rectangle-exclusion-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'directional':'h5-directional-cog-bin-planes-20261026','compact':'h5-directional-cog-plane-probe-20261026','mix':'h5-capacity-phase-mix-probe-20261026','exploration':'h5-direction-order-bounds-20261026','source_bounds':'h5-full-source-direction-bounds-20261026','projection':'h5-necessary-direction-projection-20261026','rectangles':'h5-inner-rectangle-data-20261026','exclusion':'h5-rectangle-direction-projection-20261026','review':'h5-direction-projection-review-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']=='bc9edc2b82caa501c92052f2bcc0aa78ca068053'
assert review['main_head']=='7271cc8beb5caae3a3dced77d129ffcdcb1ec7ed' and review['main_ci_id']==40290567078 and review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6
assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('directional','audit/checks.json'),('compact','model-audit/checks.json'),('compact','response-audit/checks.json'),('mix','model-audit/checks.json'),('mix','response-audit/checks.json'),('source_bounds','audit/checks.json'),('projection','model-audit/checks.json'),('projection','response-audit/checks.json'),('rectangles','audit/checks.json'),('exclusion','model-audit/checks.json'),('exclusion','response-audit/checks.json')]
assert len(audits)==11 and all(load(base[k]/n)['passed'] for k,n in audits)
calls=[]
for k,status,limit in [('compact','UNKNOWN',60),('mix','UNKNOWN',60),('projection','OPTIMAL',30),('exclusion','INFEASIBLE',30)]:
    r=load(base[k]/'search/000/result.json');p=load(base[k]/'search/process.json');assert r['status']==status and p['exit_code']==0 and not p['timeout'] and p['seconds']<=limit and len(list(base[k].rglob('opened.json')))==1
    calls.append({'experiment':names[k],'closed':True,'status':status,'variables':load(base[k]/'inventory.json')[0]['variables'],'constraints':load(base[k]/'inventory.json')[0]['constraints'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_limit_seconds':45 if limit==60 else 20,'shared_limit_seconds':limit,'soft_overrun_seconds':r['solver_soft_overshoot_seconds'],'full_target_witness':False})
assert load(base['exclusion']/'model-audit/necessity-proof.json')['necessary_projection_of_full_source']
assert load(ROOT/'output/h5-repeated-phase-exclusion-search-20261026/audit/checks.json')['status']=='INFEASIBLE'
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
copies=[('directional','result.json','directional-geometry-summary.json'),('source_bounds','profile-bounds.json','full-source-direction-bounds.json'),('source_bounds','audit/implication.json','full-source-direction-necessity.json'),('projection','model-audit/necessity-proof.json','projection-necessity.json'),('rectangles','result.json','inner-rectangle-summary.json'),('rectangles','audit/implication.json','inner-rectangle-necessity.json'),('exclusion','model-audit/necessity-proof.json','exclusion-necessity.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-7271cc8b-success.json')]
for k,n,d in copies:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'closed-calls.json',calls)
scope={'excluded_originals':[21,22,25,26,37,53,63,64,65],'bracket_choices':'All eight quarter-turn/mirror profiles independently on each of four brackets','insert_choices':[8,10],'cog_angles_degrees':[56.25,58.5,60.75,63,65.25,67.5,69.75,72],'new_negative_requires_at_least_one_profile12_to17':True,'old_two_phase_branch_separately_closed':'h5-two-phase-band-and-spacing-exclusions-20261026','source_guard_and_micrometre_grid_only':True,'arbitrary_cog_angles_excluded':False,'alternative_sheet_compositions_excluded':False,'native_continuous_geometry_excluded':False,'full_target_witness':False,'H5_complete':False}
write(OUT/'scope.json',scope)
next_step='All four calls in this checkpoint are CLOSED; do not retry, reseed or extend them. The prior compact and full-source count-mixture UNKNOWN results exclude nothing. The necessary projection with98 inner rectangles excludes this fixed nine-original composition for the new six cog phases in combination with all eight declared phases, all independent bracket orientations and both inserts, under the conservative source guards and micrometre grid. The old two-phase branch is separately closed. Next investigate orientation-independent inner cog geometry: prove a common inscribed disk or polygon from the original20-tooth boundary, derive necessary spacing/area bounds valid for every cog rotation, and audit any complete projection before a new bounded call. Do not copy finite-angle band coefficients or stock boxes into an arbitrary-angle model. A negative remains specific to the tested stock and composition and must justify any grid/rounding scope; a positive still needs original geometric checks. Alternative sheet compositions remain open. All66 originals remain mandatory:55 checked first-sheet parts, nine second-sheet originals and pending first-sheet brackets28/29. Full native/material validation, production integration under60seconds and complete H5 matrix remain required. Main7271cc8b has all six checks passing; after staged evidence/ancestry verification, normally push queuedbc9edc2b and this checkpoint. H2 remains open under the unchanged gate, all22 reserved vectors untouched, and no new release is qualified.'
write(OUT/'next-step.json',{'action':next_step,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60})
members={};inputs={}
for folder in base.values():
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for field in ['inputs','input_hashes','additional_inputs']:
            for n,h in load(p).get(field,{}).items():
                if n in inputs:assert inputs[n]==h,n
                inputs[n]=h
for n,h in inputs.items():
    p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
for n in ['h5-compact-cog-bin-planes-20261026','h5-eight-phase-geometry-and-spacing-20261026','h5-two-phase-band-and-spacing-exclusions-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pattern in ['*h5_directional*.py','*h5_direction_order*.py','*h5_capacity_phase_mix*.py','*h5_full_source_direction*.py','*h5_necessary*projection*.py','*h5_inner_rectangle*.py','*h5_rectangle*projection*.py','*h5_direction_projection*.py'] for p in (ROOT/'output').glob(pattern)]+[Path(__file__),ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p;s=p.read_text(encoding='utf-8')
    for n in re.findall(r"['\"](?:output/)?([A-Za-z0-9_.-]+\.py)['\"]",s):
        q=ROOT/'output'/n
        if q.is_file():helpers.append(q)
    for node in ast.walk(ast.parse(s)):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
print({'archiving_members_before_deduplication':len(members)},flush=True);archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':11,'closed_solver_calls':4,'terminal_statuses':[r['status'] for r in calls],'all_shared_budgets_honored':True,'source_pair_rectangles_verified':80,'aggregate_profile_rectangles_verified':80,'necessary_projection_variables':2732,'exclusion_constraints':3779,'optional_inner_rectangles':98,'new_phase_source_family_excluded':True,'arbitrary_cog_angles_excluded':False,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
table='\n'.join(f"| {r['experiment']} | {r['variables']:,} / {r['constraints']:,} | {r['status']} | {r['solver_seconds']:.6f} / {r['shared_seconds']:.6f} |" for r in calls)
report=f'''# H5: necessary direction and inner-rectangle exclusion — 2026-10-26

**A small necessary model rules out the remaining declared eight-angle branch
for the nine-original short-sheet composition. The old two-angle branch was
closed separately. This does not exclude arbitrary cog angles, different sheet
compositions or continuous native geometry. H2/H5 remain open at60%.**

## Results and scope

| Experiment | Variables / constraints | Result | Solver / shared seconds |
|---|---:|---|---:|
{table}

All four sole calls are closed, with four workers and seed0. The first two use
45 solver /60 shared seconds; the two necessary projections use20/30. Soft
overruns of {calls[0]['soft_overrun_seconds']:.6f} and
{calls[1]['soft_overrun_seconds']:.6f} seconds are preserved. Both shared budgets
pass. Neither UNKNOWN supports a count or geometric exclusion. No retry occurs.

The excluded fixed composition contains originals21/22/25/26/37/53/63/64/65:
four brackets, one insert and four cogs. Every bracket independently chooses
all eight quarter-turn/mirror profiles; the insert has both orientations. Cog
phases are56.25°,58.5°,60.75°,63°,65.25°,67.5°,69.75°,72°. The new model requires
at least one of the six newly added phases. The previously closed9/11-only
branch is preserved in [the two-phase report](h5-two-phase-band-and-spacing-exclusions-20261026.md).
The conservative source guard and micrometre coordinate grid remain explicit.

## Earlier reductions remain inconclusive

The bidirectional compact construction covers80 profile pairs across15,680
directional1mm bins. It retains15,736 sloping requirements and accounts for
406,340 source-face implications. Both left and right alternatives are present.
Removing79,704 additional source plane flags yields8,135 variables and86,147
constraints. The independent audit proves a compact witness implies the full
source; reverse equivalence is not claimed. Its sole search returns UNKNOWN.

A separate full-source subfamily fixes only cog counts to three profile9 and
one profile15, selected by the earlier necessary area allocation. Every original
coordinate and complete vertical cell remains free. This unreduced233,773-variable
model also returns UNKNOWN. No exclusion is copied from either attempt.

An exploratory compact-only order calculation is retained, but it is not the
basis for the final necessary model and has no independent-audit claim.

## Necessary horizontal bounds from original geometry

For each of80 non-cog/cog profile cases, inspect the entire stock-allowed relative
Y interval and analytic source-boundary crossings. Prove a central rectangle
strictly inside the original guarded collision region, at every relative Y.
All integer deltaX values between the two retained endpoints are forbidden.
The resulting disjunction is therefore necessary: deltaX≤L or deltaX≥R.

For each non-cog profile, take the weakest L/R bounds across all eight cog choices
and independently check all80 aggregate rectangles again. The minimum interior
margin exceeds0.0009986mm. Consecutive x-ordered cogs have source-proven minimum
spacing256.820mm. A right-then-left side assignment would contradict
R+spacing−L>0, whose minimum margin is644.450mm. Thus15 monotone side clauses
are necessary, without fixing a nonidentical part's side.

The first projection has18 original coordinates,66 profile flags,20 side flags
and2,628 complete vertical-cell selectors:2,732 variables and3,582 constraints.
It includes272 direction inequalities,390 cog spacing bounds,66 cell/profile
equalities and63 exact area-band capacities. Independent reconstruction checks
every field,165,564 cell-band coefficients and2,614,368 covered integer Y values.
Sorting identical copies with their profiles covers98,304 bracket choice/order
cases and97,920 active cog choice/order cases. No balanced bracket count
restriction, compact sufficient guard, fixed pose or prior count cut is added.

The projection returns OPTIMAL quickly, but original geometry inspection finds
11 overlapping pairs. This is a necessary allocation only, never a valid layout.

## Inner rectangles close the branch

Each bracket is partitioned into three source-coordinate grid cells and each
insert into one. Inset each cell by1micrometre on every side. Independent checks
prove all26 profile rectangles strictly inside their actual original filled
outers, with at least0.00099999mm boundary margin. The inset weakens the test;
no sufficient clearance or enlarged bounding box is introduced.

Retain the entire necessary parent model field-for-field. Its98 physical/profile
rectangles get196 optional intervals, each present exactly when its profile is
chosen, and one global2D non-overlap constraint. Starts and ends are the original
anchor plus audited inner coordinates. No variables or fixed poses are added.
Every disjoint source placement must satisfy these inner-subset constraints.
The final2,732-variable/3,779-constraint model returns INFEASIBLE in
{calls[3]['solver_seconds']:.6f} solver seconds. All11 audits pass, including
actual import/export and independent readback of the sole response.

## Continuation and publication

Next derive an orientation-independent inner cog shape from the original
20-tooth boundary, then investigate necessary bounds for every allowed cog
rotation. Finite-angle stock boxes and band coefficients must not be reused
without proof. This remains a diagnostic branch; alternate sheet compositions
are open and any positive needs full original geometry checks.

All66 original identities remain required:55 checked first-sheet originals,
nine short-sheet originals and pending first-sheet brackets28/29. Full native
material validation, production integration under60seconds and the full H5
matrix remain open. No new release or production-quality claim is qualified.

At {review['utc']}, local HEAD isbc9edc2b and main is7271cc8b. All six jobs in
[main CI40290567078](https://github.com/skulitom/Nestbolt/actions/runs/40290567078)
pass. Queue this checkpoint withbc9edc2b for a normal push after verifying
staged evidence and ancestry. Product source, READMEs and upstream stop-rule
state are unchanged. H2 retains its original gate and all22 reserved vectors
remain untouched.

[Checks]({NAME}/checks.json), [closed calls]({NAME}/closed-calls.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). All{archive['archive_members']:,}
canonical files and{archive['verified_aliases']:,} aliases are checked by byte
length, SHA-256 and CRC across{archive['archive_parts']} archive parts.
'''
# Apply explicit prose-only corrections; never transform paths or identifiers.
for before,after in {
    'at60%':'at 60%', 'seed0':'seed 0', 'use20/30':'use 20/30',
    'contains originals21':'contains originals 21', 'are56.25':'are 56.25',
    'closed9/11':'closed 9/11', 'covers80':'covers 80', 'across15,680':'across 15,680',
    'directional1mm':'directional 1 mm', 'retains15,736':'retains 15,736',
    'Removing79,704':'Removing 79,704', 'yields8,135':'yields 8,135',
    'and86,147':'and 86,147', 'profile9':'profile 9', 'profile15':'profile 15',
    'unreduced233,773':'unreduced 233,773', 'of80':'of 80', 'all80':'all 80',
    'exceeds0.0009986mm':'exceeds 0.0009986 mm', 'spacing256.820mm':'spacing 256.820 mm',
    'is644.450mm':'is 644.450 mm', 'Thus15':'Thus 15', 'has18':'has 18',
    'coordinates,66':'coordinates, 66', 'flags,20':'flags, 20', 'and2,628':'and 2,628',
    'selectors:2,732':'selectors: 2,732', 'and3,582':'and 3,582',
    'includes272':'includes 272', 'inequalities,390':'inequalities, 390',
    'bounds,66':'bounds, 66', 'and63':'and 63', 'field,165,564':'field, 165,564',
    'and2,614,368':'and 2,614,368', 'covers98,304':'covers 98,304',
    'and97,920':'and 97,920', 'by1micrometre':'by 1 micrometre', 'all26':'all 26',
    'least0.00099999mm':'least 0.00099999 mm', 'Its98':'Its 98', 'get196':'get 196',
    'global2D':'global 2D', 'final2,732':'final 2,732', 'All11':'All 11',
    'original\n20-tooth':'original\n20-tooth', 'All66':'All 66',
    'required:55':'required: 55', 'brackets28/29':'brackets 28/29',
    'under60seconds':'under 60 seconds', 'isbc9edc2b':'is bc9edc2b',
    'is7271cc8b':'is 7271cc8b', 'CI40290567078':'CI 40290567078',
    'withbc9edc2b':'with bc9edc2b', 'all22':'all 22',
    f"All{archive['archive_members']:,}":f"All {archive['archive_members']:,}",
    f"and{archive['verified_aliases']:,}":f"and {archive['verified_aliases']:,}",
    f"across{archive['archive_parts']}":f"across {archive['archive_parts']}",
}.items():report=report.replace(before,after)
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note=f'''\n\n**N4 necessary direction/rectangle exclusion, 2026-10-26:** [the evidence]({{link}})
records two closed UNKNOWN searches and a stronger necessary geometry result.
All 80 original non-cog/cog cases support audited horizontal disjunctions;
15 necessary side-order clauses and complete area cells produce a 2,732-variable
projection. Its initial positive contains 11 overlapping pairs. Adding 98
independently verified inner rectangles closes the new-phase branch as
INFEASIBLE in {calls[3]['solver_seconds']:.6f} solver / {calls[3]['shared_seconds']:.6f} shared seconds,
with all four declared call budgets honored and all 11 audits passing.
Together with the separately closed old two-phase branch, this excludes the
fixed nine-original short-sheet composition at the eight declared cog angles,
with every bracket orientation and both inserts, under source guards and the
micrometre grid. Arbitrary cog angles and other compositions remain open.
Next derive orientation-independent inner cog geometry before another bounded
diagnostic. All 66 originals and full H5 validation remain required. Main
7271cc8b now passes all six checks; queued checkpoints can be pushed normally
after staged byte/ancestry checks. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
