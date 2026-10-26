"""Seal complete composition selection and rotation-independent support bounds."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-complete-composition-selection-and-support-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'resources':'h5-composition-resources-20261026','selector':'h5-complete-composition-selector-20261026','support':'h5-all-angle-support-bounds-20261026','strengthened':'h5-support-composition-selector-20261026','decision':'h5-nine-short-decision-20261026','geometry_only':'h5-geometric-nine-decision-20261026','stem_plan':'h5-stem-order-reduction-plan-20261026','review':'h5-composition-selection-review-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']=='5025ace18886dfa503fd74572a7e4dc1715f3b94';assert review['main_head']=='6246967c2962095d78b15693ae34550fbe163743' and review['main_ci_id']==40298314725 and review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6;assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('resources','checks.json'),('selector','model-audit/checks.json'),('selector','response-audit/checks.json'),('support','audit/checks.json'),('strengthened','model-audit/checks.json'),('strengthened','response-audit/checks.json'),('decision','model-audit/checks.json'),('decision','response-audit/checks.json'),('geometry_only','model-audit/checks.json'),('geometry_only','response-audit/checks.json'),('stem_plan','checks.json')];assert len(audits)==11 and all(load(base[k]/n)['passed'] for k,n in audits)
calls=[]
for k,status in [('selector','FEASIBLE'),('strengthened','FEASIBLE'),('decision','UNKNOWN'),('geometry_only','UNKNOWN')]:
    r=load(base[k]/'search/000/result.json');p=load(base[k]/'search/process.json');assert r['status']==status and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and len(list(base[k].rglob('opened.json')))==1
    calls.append({'experiment':names[k],'closed':True,'status':r['status'],'variables':load(base[k]/'inventory.json')[0]['variables'],'constraints':load(base[k]/'inventory.json')[0]['constraints'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_limit_seconds':20,'shared_limit_seconds':30,'soft_overrun_seconds':r['solver_soft_overshoot_seconds'],'full_target_witness':False})
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('resources','resources.json','complete-area-resources.json'),('resources','necessity-proof.json','resource-necessity.json'),('selector','model-audit/necessity-proof.json','selector-necessity.json'),('selector','response-audit/verified-necessary-allocation.json','initial-necessary-allocation.json'),('support','cog-spacing-proof.json','original-tip-spacing-proof.json'),('support','bracket-direction-bounds.json','bracket-stem-bounds.json'),('support','audit/necessity-proof.json','support-necessity.json'),('strengthened','response-audit/verified-necessary-allocation.json','strengthened-necessary-allocation.json'),('geometry_only','model-audit/necessity-proof.json','geometry-projection-necessity.json'),('stem_plan','reduction-plan.json','next-stem-order-formulation.json'),('stem_plan','necessity-proof.json','stem-order-necessity.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-6246967c-success.json')]:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'closed-calls.json',calls)
write(OUT/'scope.json',{'all11_remaining_originals_required':True,'every_unselected_short_part_mandatory_on_first':True,'all_real_cog_angles_and_continuous_source_anchors_covered':True,'initial_and_strengthened_selections_only_necessary':True,'lexicographic_optimality_proved':False,'maximum_short_count_proved':False,'nine_or_more_excluded':False,'actual_new_full_geometry_witness':False,'original_support_bounds_necessary':True,'first_sheet_partial_scope':'Continuation of checked55 with11 remaining originals, same relaxed two-sheet target','H5_complete':False})
next_action='All four20solver/30shared calls are CLOSED: two FEASIBLE eight-part necessary selections and two UNKNOWN nine-or-more decisions. Neither optimization is optimal; no9/10-part count exclusion follows. Do not retry, reseed or extend them. New original-tip support proves continuous cog centers need247.444mm separation and rounded X gaps245.034mm; full-height stems strengthen192 bracket/cog endpoints. Next implement the separately audited stem-order formulation from h5-stem-order-reduction-plan-20261026: start from the116-variable/859-constraint geometry-only necessary decision; REMOVE exactly its five bracket bounding-box-anchor order constraints120/122/124/126/128. Relabel selected identical brackets by full-height stem starts. Add6 conditional stem-start variables,48 affine profile channels and40 adjacent profile-dependent stem-width separations, retaining presence prefixes and every other source/identity/resource/cardinality rule. Expected122 variables/942 constraints. Do not impose both old and new bracket orders. Independently verify retained field remapping, all optional interval references, common160mm line coverage, source relabelling and actual import before one separately declared bounded call. A negative would exclude9-or-more only for this checked55 continuation; positives still need omitted band checks and original geometry on both sheets. All66 originals remain mandatory; no full native call until every original has a valid placement. Production integration under60seconds and the full H5 matrix remain. Main6246967c CI40298314725 now passes all six jobs; normally push queued5025ace1 and this checkpoint after staged-byte/ancestry checks. H2 original gate remains open and22 reserved vectors untouched. No new release is qualified.'
write(OUT/'next-step.json',{'action':next_action,'new_stem_model_prepared':False,'completion_percent':60,'H2_complete':False,'H5_complete':False})
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
for n in ['h5-all-angle-continuous-composition-exclusion-20261026','h5-necessary-direction-and-rectangle-exclusion-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*h5_composition*.py','*h5_complete_composition*.py','*h5_support*selector*.py','*h5_all_angle_support*.py','*h5_nine_short*.py','*h5_geometric_nine*.py','*h5_stem_order*.py'] for p in (ROOT/'output').glob(pat)]+[Path(__file__),ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':11,'closed_solver_calls':4,'terminal_statuses':[r['status'] for r in calls],'all_shared_budgets_honored':True,'soft_overruns_seconds':[r['soft_overrun_seconds'] for r in calls],'initial_selected_short_count':8,'strengthened_selected_short_count':8,'selection_optimality_proved':False,'nine_or_more_excluded':False,'original_center_spacing_units1000':247444,'rounded_x_spacing_units1000':245034,'strengthened_direction_endpoints':192,'geometry_only_variables':116,'geometry_only_constraints':859,'next_stem_formulation_prepared':False,'all66_originals_required':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
table='\n'.join(f"| {r['experiment']} | {r['variables']:,} / {r['constraints']:,} | {r['status']} | {r['solver_seconds']:.6f} / {r['shared_seconds']:.6f} |" for r in calls)
report=f'''# H5: complete composition selection and original support — 2026-10-26

**A complete necessary selector accounts for all eleven remaining originals
and finds two eight-part short-sheet allocations. Neither is proved optimal
or an original geometric layout. New all-angle support bounds strengthen cog
spacing and bracket separation. Nine-or-more decisions remain UNKNOWN;
no count exclusion follows. H2/H5 remain open at 60%.**

## Complete sheet obligations and first-sheet resource

The checked first-sheet partial has 55 originals. The remaining originals are
**21/22/25/26/28/29/37/53/63/64/65**: six brackets, one insert and four cogs.
Every selector flag means either a selected short-sheet part or a mandatory
first-sheet addition. No original disappears and absent proxy coordinates
do not assert a first-sheet pose.

Recompute each family filled-outer area exactly using both shoelace and anchored
triangle formulas. With part-in-part off, cutouts do not reduce occupied area.
The first-sheet area capacity uses its actual dimensions, margins and edge
clearance, relaxed outward by 0.020 mm. Total original area minus that capacity
requires at least **39,892,822 area units** on the short sheet (1,000 units/mm²).
Ceil each selected family coefficient and floor the lower bound, weakening the
integer constraint conservatively. This area condition cannot prove a fit.

The objective ranks selected short-sheet count before rounded original area.
A count weight of 1,000,000,000 exceeds the maximum secondary area term of
460,050,876. Both selections preserve the exact complement of all 66 identities.

## Models and closed calls

| Experiment | Variables / constraints | Result | Solver / shared seconds |
|---|---:|---|---:|
{table}

All four sole calls use 20 solver / 30 shared seconds, four workers and seed 0.
The shared limits pass. Their soft overruns are preserved as
**{calls[0]['soft_overrun_seconds']:.6f} / {calls[1]['soft_overrun_seconds']:.6f} /
{calls[2]['soft_overrun_seconds']:.6f} / {calls[3]['soft_overrun_seconds']:.6f} seconds**.
Every call is closed; no restart, reseed or extension occurs.

The complete selector has 11 presence flags, 54 profile choices, 2,300 complete
vertical-cell flags, 63 fresh band bounds, 146 optional inner rectangles,
conditional original spacing rules and the previously proved composition cut.
Selected identical copies form a prefix and are ordered with their profiles;
every pair condition is inactive for absent parts. Independent reconstruction
checks every field, 144,900 cell-band coefficients, 46,080 bracket and 384 cog
presence/rank permutations, exact objective and actual solver import/export.

The first FEASIBLE selection has **three brackets, one insert and four cogs**,
leaving originals **26/28/29** mandatory on the first sheet. Its objective is
8,340,050,876, with upper bound 10,409,988,157. The strengthened FEASIBLE selection
has **four brackets, one insert and three cogs**, leaving **28/29/65** mandatory
on the first sheet. Its objective is 8,329,988,157 with the same upper bound.
Neither proves maximum selected count, original clearance or first-sheet fit.

## All-angle original-tip support

The original cog contains a centered disk of radius **109.115 mm**. Its convex
hull contains a centered disk of radius **139.270 mm**, while every original
vertex lies within radius **140.001 mm**. Thus in any direction some original
vertex has projection at least h=139.270 mm and norm at most R=140.001 mm.
At center distance d from another cog, that vertex's squared distance from the
other center is at most **d² - 2hd + R²**.

Exact integer arithmetic proves this is strictly less than r² throughout
**[2r, 247.444 mm]**: the quadratic is convex and both endpoint values are
negative. Smaller distances collide by the two original inner disks. Therefore
original cog centers need at least **247.444 mm** separation at every real
rotation. After a conservative 3-micrometre anchor-rounding loss and the full
relative-Y range, the necessary X gap increases from **215.446 to 245.034 mm**.

Every bracket has an inset full-height vertical stem. The transverse component
of the cog support vertex is at most 15 mm, and the whole allowed relative-Y
range places that vertex inside each stem's height. The stem width plus inner
disk radius exceeds the outer radius, so the disk/stem and support-tip/stem
forbidden X intervals overlap. Their union extends a necessary directional
endpoint for each of the eight bracket profiles. Account for relative anchor
rounding and merge only overlapping, already proved forbidden intervals.

The strengthened selector changes exactly **192 bracket/cog endpoints and six
cog gaps**. Independent restoration proves every other parent field and the
objective unchanged. These bounds apply to actual original geometry for every
angle and continuous anchor; earlier proxy-only solutions need not survive.

## Nine-or-more remains open

A distinct decision removes the objective and requires at least nine short-sheet
parts, retaining every other constraint and original obligation. Complete parent
restoration and import pass, but the sole call is UNKNOWN.

A separate necessary projection removes all 2,300 vertical-cell variables,
their 2,300 implications, 54 cell/profile sums and 63 band bounds. Every other
field is retained, including the first-sheet resource, nine-part requirement,
source support and optional rectangle constraints; interval references are
remapped and audited. This weaker **116-variable / 859-constraint** geometry
model also returns UNKNOWN. No nine/ten-part exclusion is inferred.

## Verified next formulation

All eight quantization-safe bracket stems span a common Y interval,
**69.448–256.478 mm**, at every allowed anchor. At the shared line **Y=160 mm**,
disjoint original brackets require disjoint stem X intervals. This suggests
ordering identical selected brackets by stem starts instead of bounding-box
anchors, making adjacent stem separation explicit.

The five old bracket anchor-order constraints are identified exactly and must
be removed before adding the new order. Retain presence-prefix symmetry, add
six stem-start variables, 48 conditional affine profile channels and 40
conditional adjacent width inequalities. The expected model has **122 variables
/ 942 constraints**. Imposing both orders would be unsound. The common-line
proof and source relabelling are audited; no new model or call is prepared yet.
Require complete field/reference and import audits before a bounded call.

Full original geometry on both sheets, all 66 native/material checks, production
integration within 60 seconds and the complete H5 matrix remain required.

## Repository and evidence

At **{review['utc']}**, local HEAD is **5025ace1**, queued above main **6246967c**.
All six jobs in [main CI40298314725](https://github.com/skulitom/Nestbolt/actions/runs/40298314725)
now pass. Normally push both queued checkpoints after staged-byte and ancestry
checks. Production, READMEs, upstream stop-rule state and all 22 reserved H2
vectors remain unchanged. H2 retains its original gate; no release is qualified.

All **eleven audits pass**. [Checks]({NAME}/checks.json),
[closed calls]({NAME}/closed-calls.json), [scope]({NAME}/scope.json),
[next step]({NAME}/next-step.json), [raw manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']:,} canonical files and {archive['verified_aliases']:,}
aliases are byte/SHA-256/CRC verified across {archive['archive_parts']} archive parts.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note=f'''\n\n**N4 complete composition selection and original support, 2026-10-26:** [the evidence]({{link}})
accounts for all eleven remaining originals with explicit first-sheet complements.
Two complete necessary selectors find eight-part allocations without proving
optimality or original geometry. Exact original-tip support raises the all-angle
continuous cog-center lower bound to 247.444 mm and rounded X spacing to 245.034 mm;
full-height stems strengthen 192 bracket/cog endpoints. The nine-or-more decision
and its 116-variable geometry-only relaxation both remain UNKNOWN. All four
20/30-second calls are closed, all shared limits and eleven audits pass, and
soft overruns are preserved. No maximum selected count or new count exclusion
is claimed. A common Y=160 mm stem-line proof supports the next audited
formulation: replace the five old bracket anchor-order constraints before adding
conditional stem ordering, never impose both. All 66 originals and full H5
validation remain required. Main 6246967c now passes all six checks, enabling
a normal push of queued checkpoints after staged-byte/ancestry checks.
H2/H5 remain open at 60%; production, READMEs, releases and reserved vectors
are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
