"""Seal all-rotation/continuous-position necessary exclusions and composition cut."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-all-angle-continuous-composition-exclusion-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'geometry':'h5-rotation-independent-geometry-20261026','bands':'h5-rotation-independent-bands-20261026','nine':'h5-all-angle-projection-20261026','eight':'h5-all-angle-eight-projection-20261026','cut':'h5-all-angle-composition-cut-20261026','review':'h5-all-angle-checkpoint-review-20261026','previous_sync':'h5-direction-projection-main-sync-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==review['source_head']==review['main_head']=='6246967c2962095d78b15693ae34550fbe163743';assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items());assert review['main_ci_id']==40298314725 and review['main_ci_status']=='in_progress' and review['main_ci_successful_jobs']==5
audits=[('geometry','audit/checks.json'),('bands','audit/checks.json'),('nine','model-audit/checks.json'),('nine','response-audit/checks.json'),('eight','model-audit/checks.json'),('eight','response-audit/checks.json'),('cut','checks.json')];assert all(load(base[k]/n)['passed'] for k,n in audits)
calls=[]
for k in ['nine','eight']:
    r=load(base[k]/'search/000/result.json');p=load(base[k]/'search/process.json');assert r['status']=='INFEASIBLE' and p['exit_code']==0 and not p['timeout'] and p['seconds']<=30 and r['solver_soft_overshoot_seconds']==0 and len(list(base[k].rglob('opened.json')))==1
    calls.append({'experiment':names[k],'closed':True,'status':r['status'],'variables':load(base[k]/'inventory.json')[0]['variables'],'constraints':load(base[k]/'inventory.json')[0]['constraints'],'solver_seconds':r['seconds'],'shared_seconds':p['seconds'],'solver_limit_seconds':20,'shared_limit_seconds':30,'soft_overrun_seconds':0,'full_target_witness':False})
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('geometry','result.json','all-angle-geometry-summary.json'),('geometry','original-cog-proof.json','original-cog-radius-proof.json'),('geometry','audit/necessity-proof.json','continuous-subset-necessity.json'),('geometry','audit/exact-forbidden-coverage.json','exact-forbidden-rectangle-coverage.json'),('bands','audit/necessity-proof.json','all-angle-band-necessity.json'),('nine','model-audit/necessity-proof.json','nine-original-necessity.json'),('eight','model-audit/necessity-proof.json','eight-original-necessity.json'),('cut','implication.json','composition-cut.json'),('cut','identities.json','full-job-identities.json'),('cut','remaining-count-allocations.json','remaining-count-allocations.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-6246967c-in-progress.json'),('previous_sync','receipt.json','previous-main-sync.json')]:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'closed-calls.json',calls)
write(OUT/'scope.json',{'fixed_target':'Original 1487mm-wide usable short sheet, usable Y6.5..319.42690233mm, relaxed outward by0.020mm on every edge','excluded_minimum_family_counts':{'bracket':4,'cog':4},'insert_count_irrelevant':True,'bracket_choices':'Every allowed quarter-turn and mirror','cog_choices':'Every real rotation','original_anchor_positions':'Every continuous position contained in the relaxed stock','proxy_grid_is_a_relaxation_not_source_restriction':True,'filled_outer_pair_disjointness_required':True,'part_in_part':False,'other_short_sheet_compositions_excluded':False,'other_material_or_sheet_targets_excluded':False,'native_or_full_job_acceptance_claimed':False,'H5_complete':False})
next_step='Both20solver/30shared second calls are CLOSED INFEASIBLE with no overruns. Do not retry, reseed or extend them. The all-angle continuous inner-subset proof excludes any short-sheet arrangement containing at least4 brackets and4 cogs at this target, irrespective of inserts. For this two-sheet target, first-sheet totals must therefore include at least9 brackets OR12 cogs. The checked55 contains6 brackets and11 cogs, so its continuation must add at least3 brackets OR1 cog. All11 remaining originals21/22/25/26/28/29/37/53/63/64/65 stay mandatory. Next prepare a complete necessary short-sheet composition selector over those6 brackets,1 insert and4 cogs, with unselected identities explicitly required on the first sheet. Use only fresh all-angle proxy stock/band/direction data. Add presence-conditional geometry, complete family symmetry and any separately justified first-sheet area bound; audit that every whole-job continuation maps to it before one new bounded call. A necessary selected composition is not a source layout: validate actual full-original geometry on both sheets, preserve every cutout, then run the full66 native/material validator. Product integration under60seconds and the complete H5 matrix remain required. Current main6246967c CI40298314725 has5successful jobs and Windows checks live; queue this checkpoint until all six pass, then normally push after ancestry and staged-byte checks. H2 retains its original gate;22 reserved vectors untouched. No new release is qualified.'
write(OUT/'next-step.json',{'action':next_step,'mandatory_remaining_originals':[21,22,25,26,28,29,37,53,63,64,65],'completion_percent':60,'H2_complete':False,'H5_complete':False})
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
for n in ['h5-necessary-direction-and-rectangle-exclusion-20261026','h5-eight-part-composition-and-orientations-20261026','h5-second-strip-capacity-and-insert-exchange-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*h5_rotation_independent*.py','*h5_all_angle*.py'] for p in (ROOT/'output').glob(pat)]+[Path(__file__),ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py'];seen=set()
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
write(OUT/'checks.json',{'passed':True,'independent_audits_passed':7,'closed_solver_calls':2,'terminal_statuses':['INFEASIBLE','INFEASIBLE'],'all_shared_budgets_honored':True,'soft_overrun_seconds':0,'original_cog_edges_checked':80,'convex_hull_edges_checked':40,'exact_expanded_forbidden_rectangles':11,'fresh_band_coefficients_checked':42525,'all_real_cog_angles_covered':True,'continuous_original_positions_covered':True,'monotone_family_count_cut_verified':True,'remaining_count_allocations':70,'excluded_count_allocations':6,'remaining_unproved_allocations':64,'all66_originals_accounted_once':True,'native_calls':0,'quality_runs':0,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: all-angle continuous composition exclusion — 2026-10-26

**Four brackets and four cogs cannot fit the current short-sheet target,
even with arbitrary cog rotations, continuous positions and stock enlarged
outward by 0.020 mm. Adding an insert or more parts cannot fix that subset.
For this two-sheet target, the first sheet must contain at least nine brackets
or twelve cogs. Other compositions remain open; H2/H5 remain open at 60%.**

## Rotation-independent geometry and continuous positions

Reconstruct the original 80-vertex, 20-tooth cog from the frozen job. Exact
rational distances to every edge, together with an exact origin winding check,
prove a centered disk of radius **109.115 mm** lies in its filled outer.
The disk is preserved under every real rotation; this uses no angle sample.
Part-in-part remains disabled, so holes do not reduce the occupied filled outer.

Floor each continuous anchor coordinate to the micrometre grid. Its displacement
is less than sqrt(2) micrometres. Reduce the common disk radius by 2 micrometres
to **109.113 mm**, then inscribe a rational 128-gon. Every vertex's squared norm
is checked exactly. The shifted polygon remains inside the original shape at
every rotation and continuous position. Likewise, rebuild all 26 bracket/insert
inner rectangles with **2-micrometre insets**, whose whole-boundary margins
exceed the possible anchor displacement.

A separate exact convex-hull proof checks all 40 hull edges and every original
vertex. Its centered **139.270 mm** disk establishes necessary stock support in
every direction. This larger disk is used only for stock bounds, not collisions.
Relax the original usable stock outward by **0.020 mm** on every side and floor
the resulting necessary anchor bounds. The mapping covers continuous source
positions; the proxy grid does not restrict source positions. Old sampled-angle
stock padding, angle flags and exclusions are not transferred.

For each of ten non-cog profiles against the common cog polygon, and for the
cog pair, construct exact integer-coordinate Minkowski hulls. Independently
verify hull convexity, every hull vertex's provenance and containment of all
**21,505** generated sum points. Prove each complete central forbidden rectangle,
expanded by **0.1 micrometre**, is covered by its hull union using exact rational
polygon subtraction. No sample-only containment inference is used. This yields
necessary left/right disjunctions and a common cog X gap of **215.446 mm**.

## Fresh area and complete model checks

Recompute all area bounds from the rational inner subsets and the new stock
domains. Exact slice integration includes every translated vertex breakpoint
and interior quadratic minimum. A separate edge-integral implementation checks
all **42,525 coefficients**, **675 complete vertical cells**, and **63 bands**.
No finite-angle coefficient is reused. Disjoint mapped inner subsets obey
these band capacities, so the inequalities remain necessary for original
continuous placements.

The nine-original model has **1,768 variables / 2,374 constraints**. It retains
all eight bracket choices independently, both insert profiles, the common cog
proxy, complete stock and cell constraints, necessary side/order bounds, and
98 optional inner rectangles. The audit reconstructs every field, checks
106,596 physical cell-band coefficients, verifies copy/profile relabelling and
round-trips the model through the actual solver importer.

Its sole 20-second, four-worker, seed-0 call returns **INFEASIBLE** after
**{calls[0]['solver_seconds']:.6f} solver / {calls[0]['shared_seconds']:.6f} shared seconds**.
The declared 30-second shared limit is honored without a soft overrun.

Removing the insert from the short-sheet inventory is a distinct composition;
insert37 remains mandatory on the first sheet alongside brackets28/29. The
eight-original model contains **1,424 variables / 2,008 constraints**, including
96 optional inner rectangles. Every field and import is independently checked.
Its sole call also returns **INFEASIBLE**, after
**{calls[1]['solver_seconds']:.6f} solver / {calls[1]['shared_seconds']:.6f} shared seconds**,
again within its 20/30-second limits. Both calls are closed and independently
read back; neither is retried, reseeded or extended.

## Consequence for the complete job

The job defines identical copies within each family. Any valid larger short-sheet
arrangement containing at least four brackets and four cogs would contain a valid
eight-part subset, contradicting the necessary-model result. Therefore:

**Short sheet: brackets <= 3 OR cogs <= 3.**

With all 12 brackets and 15 cogs required in this two-sheet target, the equivalent
first-sheet condition is **brackets >= 9 OR cogs >= 12**. This does not claim the
surviving compositions fit, or exclude another sheet/material target.

The checked first-sheet partial contains **55 originals**: 18 frames, six
brackets, 20 inserts and 11 cogs. All **11** remaining originals are still
mandatory: **21/22/25/26/28/29/37/53/63/64/65** (six brackets, one insert, four cogs).
Thus continuing that partial requires adding at least three brackets or one cog
to the first sheet. Exact enumeration covers all **70** remaining family-count
allocations; the new subset cut excludes **six**, leaving **64 unproved**.
Every one of the 66 identities is accounted for exactly once.

Next prepare a complete necessary composition selector over these remaining
originals. A part unselected for the short sheet must remain an explicit
first-sheet obligation. Audit presence-conditional geometry and any new area
bound before another bounded call. A selected composition still needs actual
original geometry on both sheets, complete native/material validation,
production integration within 60 seconds and the full H5 matrix.

## Repository and evidence

At **{review['utc']}**, local HEAD and main are **6246967c**. The previous two
checkpoints were pushed normally after all six checks on 7271cc8b passed.
[Current CI40298314725](https://github.com/skulitom/Nestbolt/actions/runs/40298314725)
has five successful jobs and Windows checks remain live. Queue this checkpoint
until the existing run completes successfully; do not cancel it with a push.
Production, READMEs, upstream stop-rule state and all 22 reserved H2 vectors
remain unchanged. H2 retains its original gate and no new release is qualified.

All **seven audits pass**. [Checks]({NAME}/checks.json),
[closed calls]({NAME}/closed-calls.json), [scope]({NAME}/scope.json),
[composition cut]({NAME}/composition-cut.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). All {archive['archive_members']:,}
canonical files and {archive['verified_aliases']:,} aliases are byte/SHA-256/CRC
verified across {archive['archive_parts']} archive parts.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note=f'''\n\n**N4 all-angle continuous composition exclusion, 2026-10-26:** [the evidence]({{link}})
proves an inner cog polygon valid at every real rotation and maps every
continuous original anchor to quantization-safe inner subsets. Exact stock
support, 11 expanded forbidden-rectangle proofs and 42,525 fresh band coefficients
support two independently audited necessary models. The nine-original model
is INFEASIBLE in {calls[0]['solver_seconds']:.6f} solver / {calls[0]['shared_seconds']:.6f} shared seconds;
removing the insert gives a separate eight-original INFEASIBLE result in
{calls[1]['solver_seconds']:.6f} / {calls[1]['shared_seconds']:.6f} seconds. All seven audits pass,
both 20/30-second calls are closed, and no overruns occur. Four brackets and
four cogs are excluded at this short-sheet target even with continuous positions,
all cog angles and 0.020 mm outward stock relaxation. Therefore the two-sheet
target requires at least nine brackets or twelve cogs on the first sheet.
All 66 identities remain mandatory; six of 70 remaining family-count allocations
are excluded and 64 remain unproved. Next select a different complete sheet
composition, preserving every unselected short-sheet part as a first-sheet
obligation. Main 6246967c has five successful checks and Windows remains live;
queue this checkpoint for a later normal push. H2/H5 remain open at 60%; no
production, README, release or reserved-vector change is claimed.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
