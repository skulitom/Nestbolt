"""Seal rotated-cog capacity, guarded source geometry and the cover timeout."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-aligned-cog-capacity-and-cover-limit-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'support':'h5-cog-rotation-support-20261026','profiles':'h5-aligned-cog-profiles-20261026','bands':'h5-aligned-cog-band-capacity-20261026','band_model':'h5-aligned-cog-band-model-20261026','band_search':'h5-aligned-cog-band-search-20261026','strip_source':'h5-aligned-nine-strip-source-20261026','strip_probe':'h5-aligned-nine-strip-probe-20261026','row_covers':'h5-aligned-rectangle-covers-20261026','component_covers':'h5-aligned-component-covers-20261026','cover_probe':'h5-component-cover-probe-20261026','production_review':'h5-production-choice-review-20261026','review':'h5-aligned-cog-checkpoint-review-20261026','prior_queue':'h5-eight-part-checkpoint-queue-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']=='68f82c021a0ab29cc83870ac6e738ec604d56a7b' and review['main_head']=='81cc41866306a639fa09f0db9590bb411c0c987e';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items()) and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6
audits=[('profiles','audit/checks.json'),('bands','audit/checks.json'),('band_model','audit/checks.json'),('band_search','audit/checks.json'),('strip_source','audit/checks.json'),('strip_probe','model-audit/checks.json'),('strip_probe','response-audit/checks.json'),('row_covers','audit/checks.json'),('component_covers','audit/checks.json'),('cover_probe','model-audit/checks.json'),('cover_probe','timeout-audit/checks.json')];assert len(audits)==11 and all(load(base[k]/n)['passed'] for k,n in audits)
band=load(base['band_search']/'result.json');strip=load(base['strip_probe']/'search/000/result.json');timeout=load(base['cover_probe']/'timeout-audit/checks.json');assert band['status']=='OPTIMAL' and strip['status']=='INFEASIBLE' and timeout['controller_status']=='WATCHDOG_TIMEOUT' and timeout['terminal_solver_status'] is None and not timeout['shared_budget_pass_claimed'];assert sum(len(list(base[k].rglob('opened.json'))) for k in ['band_search','strip_probe','cover_probe'])==3
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
copies=[('support','result.json','rotation-screen.json'),('support','choices.json','rotation-choices.json'),('profiles','result.json','aligned-profile.json'),('bands','result.json','band-coefficients.json'),('band_search','audit/verified-allocation.json','necessary-nine-part-allocation.json'),('strip_source','result.json','source-collision-summary.json'),('strip_probe','inventory.json','nine-part-model.json'),('row_covers','summary.json','whole-row-cover-summary.json'),('component_covers','summary.json','component-cover-summary.json'),('cover_probe','prepared.json','cover-model.json'),('cover_probe','search/process.json','cover-watchdog-result.json'),('production_review','review.json','production-policy-review.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-81cc4186-success.json'),('prior_queue','queue.json','prior-checkpoint-queue.json')]
for k,n,dest in copies:shutil.copyfile(base[k]/n,OUT/dest)
write(OUT/'closed-calls.json',{'band_capacity':{'result':band,'process':load(base['band_search']/'process.json')},'nine_part_coordinates':{'result':strip,'process':load(base['strip_probe']/'search/process.json')},'component_cover':timeout,'closed_calls':3,'all_shared_budgets_passed':False,'full_target_witness':False})
next_step='All3 calls are CLOSED, including the cover watchdog termination. No extension/reseed/retry of the old models. The56.25degree original cog profile reduces width/height by1.407411mm, and the new4bracket/1insert/4cog necessary band allocation is positive. The selected whole-stock profile pattern4/5/5/6/10/9/9/9/9 is excluded by an audited full-original guarded source model, with every coordinate free and all36 pair clauses. Next derive and independently audit a conditional profile-count exclusion in the new675-variable band master: no source layout can have bracket-profile counts p4=1,p5=2,p6=1 together with insert-profile p10=1. All four cogs retain9. Prove the permutation argument using identical complete original family copies, exact stock domains and all source pair geometry; do not exclude other profile counts or cog angles. Add exact reified equalities and a not-all clause, preserving every parent coefficient/domain/count, then at most one newly declared20second necessary call within30shared seconds. Any resulting different pattern needs its own full-original coordinate construction/audit and bounded call; no allocation alone is a layout. Avoid another large global NoOverlap2D call: the1326-rectangle model failed to return by its45second soft cap and was terminated by the60second watchdog, with0.016700second controller overhead; no solver terminal result or budget pass exists. The production review confirms no valid ordinary-hole-rider fallback under common-line part-in-hole-off requirements; changing that comparison would not close H5. All66 originals remain: checked first55, mandatory second9 IDs21/22/25/26/37/53/63/64/65, pending28/29. Full original/native/material validation, production integration and the full H5 matrix remain required. Main81cc4186 CI40273506020 passed all6 jobs; push queued68f82c02 and this checkpoint normally after staging/ancestry checks. H2 unchanged;22 reserved vectors untouched.'
write(OUT/'next-step.json',{'action':next_step,'next_call_opened':False,'pending_first_sheet_originals':[28,29],'mandatory_second_sheet_originals':[21,22,25,26,37,53,63,64,65],'H5_complete':False})
members={};inputs={}
for folder in base.values():
    for p in folder.rglob('*'):
        if p.is_file():members[folder.name+'/'+p.relative_to(folder).as_posix()]=p
    for p in folder.rglob('plan.json'):
        for field in ['inputs','input_hashes','additional_inputs']:
            for n,h in load(p).get(field,{}).items():
                if n in inputs:assert inputs[n]==h,n
                inputs[n]=h
for n,h in inputs.items():p=ROOT/n;assert digest(p)==h,n;members['source-inputs/'+n]=p
for n in ['h5-eight-part-composition-and-orientations-20261026','h5-second-strip-capacity-and-insert-exchange-20261026','h5-thirteen-part-selection-and-sheet-exclusion-20261026','h5-seven-part-obstruction-and-broader-source-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*aligned*.py','*component_cover*.py','*cog_rotation_support*.py','*production_choice_review*.py'] for p in (ROOT/'output').glob(pat)]+[ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
while helpers:
    p=helpers.pop()
    if p in seen:continue
    seen.add(p);members['helpers/'+p.name]=p;s=p.read_text(encoding='utf-8')
    for n in re.findall(r"['\"]([A-Za-z0-9_.-]+\.py)['\"]",s):
        q=ROOT/'output'/n
        if q.is_file():helpers.append(q)
    for node in ast.walk(ast.parse(s)):
        mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
        for mod in mods:
            q=ROOT/'output'/(mod+'.py')
            if q.is_file():helpers.append(q)
archive,manifest=pack(ROOT,OUT,NAME,members);write(OUT/'checks.json',{'passed':True,'independent_audits_passed':11,'closed_solver_calls':3,'terminal_solver_responses':2,'watchdog_terminations':1,'all_shared_budgets_passed':False,'controller_shutdown_overshoot_seconds':timeout['controller_shutdown_overshoot_seconds'],'all66_original_identity_obligations_preserved':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: aligned cog capacity and rectangle-cover limit — 2026-10-26

**A different allowed cog angle changes the nine-part necessary capacity test
from negative to positive. Its selected orientation pattern still fails the
full coordinate model. A conservative rectangle-cover model stalls and is
terminated by its watchdog. No full target layout is claimed; H2/H5 remain
open at 60% completed milestone weight.**

## Rotation and necessary capacity

Screen the original 80-vertex cog over the full rotation range using hull
support switches, width/height stationary points, crossings and area extrema.
This produces 105 support intervals and 251 candidate angles. Independent
original-polygon rotation recomputes every candidate and checks 315 interval
samples. The screen selects an angle near 56.25 degrees; the new profile uses
exactly 5π/16 radians. This is numeric angle selection, not a packing theorem.

The cog's width and height fall from approximately **279.949211 mm to
278.541800 mm**, a **1.407411 mm** reduction. Vertical travel inside the usable
short sheet increases from 32.977692 to 34.385103 mm before extra stock guards.
All 80 outer vertices and the original 200-vertex cutout remain required.
Ten other profiles remain unchanged; all 11 original-profile reconstructions
pass with maximum error 8.04×10⁻¹⁴ mm.

Recompute **42,525 exact band-area lower bounds** over **675** vertical cells
and **63** stock bands. A separate rational edge-integral audit verifies every
coefficient and all integer anchor coverage. The new model requires four
brackets, one insert and four cogs at the aligned angle. Its sole bounded call
returns **OPTIMAL in 0.123573 solver / 0.784745 shared seconds**. Independent
readback checks all 675 values, 66 constraints, family counts and band loads.
The result is a necessary allocation, not a coordinate witness.

All identities remain explicit: 55 checked first-sheet originals, second-sheet
originals **21/22/25/26/37/53/63/64/65**, and pending first-sheet brackets
**28/29**. The earlier current-angle negatives are not transferred.

## Full coordinate model for the selected pattern

The allocation selects profiles **4/5/5/6/10/9/9/9/9**. All 18 coordinates are
free throughout the guarded short stock, with no band-cell locks or hints.
Four unchanged bracket collision cases are reused; eight cases are rebuilt.
Independent original geometry checks reconstruct all 12 cases from 7,264
triangle-pair hulls, 191 guarded faces and 7,917 outside planes. The minimum
source guard is 0.2126 mm, above the required native 0.211709 mm.

The complete **8,561-variable / 8,738-constraint** model and actual import pass
independent reconstruction, retaining all 36 physical pairs. Its sole call
returns **INFEASIBLE in 1.767172 solver / 2.465369 shared seconds**. This excludes
only the specified profiles, guarded source and coordinate grid.

## Conservative rectangle covers and timeout

To test a different representation, dilate each original profile by a square
with half-side 0.1063 mm, then cover the guarded shape with disjoint rectangles.
Whole-row covers add 5,645.918 mm² beyond a guarded cog. Keeping disconnected
tooth-tip components separate reduces that excess to **1,467.443 mm²**.
Neither shape is substituted for the original at final acceptance.

Independent triangle-plus-square construction verifies all guarded polygons,
complete cover containment, original stock bounds and all 49,463 internal
rectangle pairs for the component covers. Twice the minimum cover-boundary
gap is **0.213651 mm**, above the native pair requirement. A non-overlapping
cover placement would therefore be sufficient, pending original verification;
a cover-model negative would not exclude original placements.

The model permits all eight bracket orientations and both insert orientations,
with shared original anchors. All **52 variables / 2,732 constraints**, including
2,652 optional intervals and one complete **1,326-rectangle NoOverlap2D**, pass
independent reconstruction and real solver import. Every original is mandatory.

The single call starts search but returns no solver response by its 45-second
soft limit. The **60-second outer watchdog terminates it**. Controller elapsed
time is **60.016700 seconds**, including **0.016700 seconds** of shutdown overhead.
The exact model, parameters, partial log and missing-result state are preserved;
a process check confirms no runner remains. This is a watchdog failure, **not
UNKNOWN or INFEASIBLE, and not a budget pass**. No retry is opened.

## Production review and next action

A read-only production review confirms that ordinary optimization enables
hole riders while common-line optimization disables them. The translation
bonus bounds material against its own starting layout; the external H5
ordinary comparison remains a separate requirement. Reusing an ordinary
hole-rider layout or changing that comparison would not close the current gate.
No production change or quality benchmark follows this review.

Next audit a conditional profile-count exclusion for the failed source pattern
in the aligned-angle band master. It must exclude exactly bracket counts
p4=1, p5=2, p6=1 with insert p10=1, using the identical-original-copy permutation
argument and full coordinate-model scope. Other patterns remain available.
Complete 66-original/native/material checks, production integration and the
full H5 matrix remain required; allocations alone earn no gate credit.

At {review['utc']}, all six checks for main **81cc4186** pass in
[CI40273506020](https://github.com/skulitom/Nestbolt/actions/runs/40273506020).
Checkpoint 68f82c02 and this evidence can be pushed normally after verification.
Production, accurate READMEs, upstream heads/releases and all 22 reserved H2
vectors remain unchanged. No new release is qualified.

[Checks]({NAME}/checks.json), [closed calls]({NAME}/closed-calls.json),
[watchdog audit]({NAME}/cover_probe-timeout-audit-checks.json),
[next step]({NAME}/next-step.json), [raw manifest]({NAME}/raw-manifest.json).
All {archive['archive_members']:,} canonical files and {archive['verified_aliases']:,}
aliases are byte/SHA-256/CRC verified in {archive['archive_parts']} archive parts.
'''
(ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
note='''

**N4 aligned cog and cover limit, 2026-10-26:** [the evidence]({link})
screens original cog rotations and verifies a 56.25-degree profile that reduces
width/height by 1.407411 mm. A newly audited 675-variable band model for four
brackets, one insert and four cogs is positive, but its selected full-coordinate
pattern is INFEASIBLE. All 66 identities remain mandatory, with first-sheet
brackets 28/29 still pending. Conservative component covers preserve original
clearance and yield a fully audited 52-variable / 2,732-constraint model with
1,326 rectangles. Its only call is stopped by the 60-second watchdog without a
solver result; 0.016700 seconds of controller overhead is retained, with no
budget pass or retry. Next audit an exact conditional profile-count exclusion
for the failed coordinate pattern. A production review finds no valid ordinary
hole-rider fallback under the existing common-line requirements. All three
calls are closed. Main 81cc4186 passes all six checks, allowing the queued
checkpoints to be pushed normally. H2/H5 stay open at 60%; production, READMEs,
releases and the 22 reserved vectors remain unchanged.
'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
