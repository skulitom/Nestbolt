"""Seal the all-angle fourteen-cog exclusion and repaired twelve-original strip."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-fourteen-cog-exclusion-and-twelve-part-strip-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'support':'h5-fixed43-support-domains-20261026','combined':'h5-fixed43-combined-domains-20261026','model':'h5-fourteen-cog-necessary-model-20261026','capacity':'h5-fixed43-conflict-soundness-20261026','failed':'h5-five-insert-short-sheet-20261026','repaired':'h5-five-insert-short-sheet-repaired-20261026','next':'h5-fixed40-cog-neighborhood-20261026','screen':'h5-fixed40-cog-space-20261026','review':'h5-fixed43-review-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==review['source_head']==review['main_head']=='5928270da59f7ce2c1bbd804ddf985d441490533' and review['main_ci_id']==40312752008 and review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6;assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('support','audit/checks.json'),('combined','audit/checks.json'),('model','model-audit/checks.json'),('model','response-audit/checks.json'),('capacity','checks.json'),('repaired','checks.json'),('repaired','audit/checks.json'),('next','checks.json')];assert len(audits)==8 and all(load(base[k]/n)['passed'] for k,n in audits)
call=load(base['model']/'search/000/result.json');proc=load(base['model']/'search/process.json');assert call['status']=='INFEASIBLE' and call['solver_calls']==1 and proc['exit_code']==0 and not proc['timeout'] and proc['seconds']<=30 and len(list((base['model']/'search').rglob('opened.json')))==1;partial=load(base['repaired']/'audit/checks.json');assert partial['originals_verified']==64 and partial['short_originals_verified']==12 and partial['mandatory_first_sheet_additions']==[63,64];assert load(base['failed']/'failure-review.json')['construction_exit_code']==1 and not (base['failed']/'checks.json').exists()
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('support','audit/necessity-proof.json','support-necessity.json'),('combined','audit/necessity-proof.json','combined-domain-necessity.json'),('combined','audit/cell-capacities.json','verified-cell-capacities.json'),('combined','audit/incompatible-cell-pairs.json','verified-cell-conflicts.json'),('combined','audit/existing-seed-domain-checks.json','twelve-existing-cog-seeds-preserved.json'),('model','model-audit/necessity-proof.json','fourteen-cog-model-necessity.json'),('model','search/000/result.json','closed-solver-result.json'),('model','search/process.json','closed-shared-process.json'),('failed','failure-review.json','preserved-construction-failure.json'),('repaired','partial64-placements.json','partial64-placements.json'),('repaired','short-sheet-placements.json','original-short-twelve.json'),('repaired','short-sheet-anchors.json','short-sheet-anchors.json'),('next','next-neighborhood.json','next-fixed40-neighborhood.json'),('screen','result.json','next-diagnostic-screen.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-5928270d-success.json')]:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'scope.json',{'prior_fixed43_and_short9_neighborhood_excluded':True,'all14_first_cogs_required_in_negative_model':True,'negative_covers_all_real_cog_angles_and_continuous_centers':True,'new_short_originals':12,'new_short_family_counts':{'bracket':6,'insert':5,'cog':1},'new_first_originals_placed':52,'new_originals_placed':64,'mandatory_first_cogs_unplaced':[63,64],'new_fixed_first_noncogs':40,'new_moving_first_cogs':14,'old_fixed43_negative_transferred':False,'part_in_hole_used':False,'all66_originals_required':True,'new_full66_target_witness':False,'H5_complete':False})
next_action='The only fixed43/short9 necessary14-cog call is CLOSED INFEASIBLE (8.613519500solver/9.451583200shared seconds), with no retry. Exact source support, collision-disk coverage and all91 pair distances prove this neighborhood impossible at every real angle and continuous center, but do not exclude changed fixed geometry. A repaired original short strip now contains12: six brackets21/22/25/26/28/29, inserts32/34/35/36/37 and cog65. Inserts32/34 sit between separate bracket filled outers;36/37 stand side by side with35 above. The first52 plus short12 form a validated64-original partial, with cogs63/64 mandatory. The failed first construction raised the wrong bracket arm and failed original-pair checks; failed plan/scripts and follow-on missing-file audit are preserved separately. The repaired copy raises profile5 and passes independent direct-vertex validation. Next use h5-fixed40-cog-neighborhood-20261026/next-neighborhood.json:40 fixed first non-cogs,14 mandatory free-angle first cogs,12 fixed short originals. Recompute complete support/collision domains and all capacities/conflicts for the changed owner set; only per-owner source geometry may be reused after hash/transform equality checks. No old43-fixed cell restriction or negative may transfer. Recheck all12 existing seed centers without locking them. IMPORTANT: an incompatible cell-pair countA+countB<=1 row is valid only when each domain independently has capacity1; otherwise use occupancy-presence logic or omit it. This side condition holds for all2409 old rows but must be checked afresh. After full domain/model/import audits, a new separately declared bounded14-cog necessary decision is permitted. Positive centers require actual original cog angles and every mutual/fixed clearance. Full66 native/material validation, production integration under60seconds and the full H5 matrix remain. Main5928270d CI40312752008 now passes all6 jobs, enabling a normal push after staged-byte/ancestry checks. H2 stays at its original gate,22 reserved vectors untouched; no new release qualified.'
write(OUT/'next-step.json',{'action':next_action,'completion_percent':60,'H2_complete':False,'H5_complete':False})
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
for n in ['h5-exact-cog-coverage-and-two-insert-strip-20261026','h5-short-sheet-count-bound-and-original-eight-20261026']:
    p=ROOT/'benchmarks/results'/n/'raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[p for pat in ['*h5_fixed43*.py','*h5_fixed40*.py','*h5_fourteen_cog*.py','*h5_five_insert*.py'] for p in (ROOT/'output').glob(pat)]+[ROOT/'output/h5_rational_geometry_helpers.py',ROOT/'output/ccd1.py',ROOT/'output/pack_h5_evidence_archive.py',Path(__file__)];seen=set()
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
print({'archive_input_members':len(members)},flush=True);archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'audits_passed':8,'closed_solver_calls':1,'terminal_status':'INFEASIBLE','solver_seconds':call['seconds'],'shared_seconds':proc['seconds'],'shared_budget_honored':True,'soft_overrun_seconds':call['solver_soft_overshoot_seconds'],'fixed43_source_rectangles':55,'exact_world_corner_checks':220,'exact_interval_edge_checks':880,'source_support_boxes':80,'complete_support_grid_cells':3612,'combined_refinement_nodes':2127,'certified_source_disks_used':57,'merged_necessary_domains':135,'exact_aggregate_conflict_rows':2409,'all_conflict_endpoints_capacity1':True,'all91_cog_pairs_required':True,'preserved_failed_construction':True,'repaired_originals_placed':64,'repaired_short_originals':12,'original_pair_checks':1392,'stock_edge_checks':256,'cutouts_preserved':88,'cutout_vertices_preserved':9626,'remaining_first_cogs':[63,64],'next_fixed_first_noncogs':40,'next_mandatory_first_cogs':14,'all66_originals_required':True,'native_calls':0,'quality_runs':0,'previous_main_all6_ci_passed':True,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full66_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: fourteen-cog exclusion and a twelve-part short sheet — 2026-10-26

**Fourteen cogs cannot fit while the previous 43 non-cog first-sheet originals
and nine short-sheet originals stay fixed. The audited necessary model is
INFEASIBLE for all real cog angles and continuous centers. A changed short-sheet
construction fits twelve originals, moving three more inserts off the first
sheet. The new partial still places 64 of 66 originals, with two cogs pending.
H2/H5 remain open at 60%.**

## Certified first-sheet center domains

Decompose all 43 fixed non-cog filled outers into **55 source rectangles**.
Each transformed world rectangle is rounded inward and inset by two micrometres.
Exact rational trigonometric intervals prove **220 candidate corners** strictly
inside all true source edges, using **880 interval cross-product checks**.

An original cog contains a disk of radius r=109.115 mm, has hull support
h=139.270 mm and vertex radius at most R=140.001 mm. A supporting vertex's
transverse component is at most beta=15 mm. For each fixed rectangle, its
width/height plus r exceeds R. The inner-disk collision interval therefore
overlaps both original-support-tip collision intervals. With the center at
least beta inside the transverse sides, their union forbids longitudinal
positions from low-h to high+h. Inset these strict exclusions by one micrometre
to obtain **80 entirely forbidden closed rectangles** after stock clipping.

Partition the entire center-stock rectangle at every exclusion edge. Audit
all **3,612 grid cells**, retaining **747** whole closed cells and every
possible boundary. Refine those cells with conservative collision disks
centered at source points of the same 43 fixed originals. Exact source-point
membership and transform-error bounds verify all **57 disks** used for deletion.
The **2,127-node refinement** removes 354 leaves and retains 1,083 atomic leaves,
including every unresolved boundary cell. Exact containment, area and single-use
membership certify their merger into **135 rectangles**.

All twelve previously valid original cog centers remain representable, including
every possible one-micrometre floor implied by exact transform intervals. Their
poses are diagnostic seeds only; no pose is locked in the search.

## One complete, closed fourteen-cog decision

The model keeps all **14 first-sheet cogs mandatory**, along with the fixed 43
first-sheet non-cogs and nine short-sheet originals: all 66 identities remain.
Every cog selects one certified center rectangle. Occupancy counts enforce
135 cell capacities and **2,409 incompatible-cell rows**. All **91 cog pairs**
have exact integer squared-distance constraints at 247.441 mm, conservatively
weakened from the original all-angle 247.444 mm center-distance bound to cover
coordinate flooring. Relabel identical copies by X; no objective or hint is used.

Independent reconstruction checks every field of the **2,417-variable /
6,793-constraint** model, all 182 integer square operations, complete identity
obligations and actual solver import/export. A separate capacity soundness
audit verifies that both endpoints of every aggregate incompatible-cell row
have capacity one. None of the 18 larger-capacity cells occurs in those rows.
This side condition must be checked afresh after any domain change; cross-cell
incompatibility alone does not justify countA+countB<=1 for larger capacities.

The only call returns **INFEASIBLE in {call['seconds']:.6f} solver seconds /
{proc['seconds']:.6f} shared seconds**, within its declared 20/30-second limits,
with four workers, seed zero and no soft overrun. Actual input, parameters,
terminal response and timing are audited. The call is closed and is not retried.
This excludes the fixed43/short9 neighborhood, not arrangements that move its
non-cog originals or change the short-sheet allocation.

## A twelve-original short sheet

Move first-sheet inserts **32/34/35** onto the short sheet. Two fit between
separate bracket pairs: keep each lower-arm profile7 bracket at Y=6.525 mm,
raise its upper-arm profile5 partner to Y=19 mm, and widen the pair to provide
0.225 mm clearance around a 180 × 110 mm insert. These gaps are outside both
filled bracket outers; part-in-hole remains disabled. Keep the third bracket
pair compact. Beside cog65, place two rotated 110 × 180 mm inserts side by side,
then a horizontal 180 × 110 mm insert above them.

The first attempt raised the wrong bracket arm and failed original-pair checks.
Its dependent audit could not read the absent candidate file. The failed scripts,
plans and diagnosis remain preserved. A distinct repaired construction raises
profile5 instead; the corrected candidate and independent direct-vertex audit pass.

The short sheet contains **six brackets 21/22/25/26/28/29**, **five inserts
32/34/35/36/37**, and **cog65**. Its outer geometry reaches X=1493.222484 mm and
Y=319.000000 mm, inside the guarded target. The remaining **52 first-sheet
placements are unchanged**. All **64 placed originals**, **1,392 same-sheet
filled-outer pairs**, **256 stock edges**, **88 cutouts** and **9,626 hole vertices**
pass both construction and independent direct-transform checks. Minimum pair
distance remains 0.212500 mm against the required 0.211708673 mm; minimum extra
stock margin remains 0.012500 mm. Cogs **63/64** still need first-sheet placements.

## Changed neighborhood and remaining work

The next audited inventory fixes **40 first-sheet non-cogs** (18 frames, six
brackets, 16 inserts) and **12 short-sheet originals**, with all **14 first-sheet
cogs mandatory movers**. All 66 identities are accounted for; the 12 old cog
poses remain available only as diagnostic seeds. The previous fixed43 negative
does not apply after removing inserts32/34/35 from its fixed owner set.

The new disk-only diagnostic map has area 510,879.805073 mm² and reaches
Y=2854.250 mm. It is not an audited original-cog feasible domain. Rebuild complete
support/disk domains, capacities and incompatibilities for the changed owner set
before another separately declared bounded call. Positive necessary centers
still need actual original cog angles and every original mutual/fixed clearance.
Full66 native/material validation, production integration within 60 seconds and
the complete H5 matrix remain required.

## Repository and evidence

At **{review['utc']}**, local HEAD and main are **5928270d**. All six jobs in
[CI40312752008](https://github.com/skulitom/Nestbolt/actions/runs/40312752008)
have passed, permitting a normal checkpoint push after staged-byte/ancestry
checks. Production/README digests and upstream stop-rule state remain unchanged.
H2 retains its original gate and the 22 reserved vectors remain untouched.
No new release is qualified.

All **eight audits pass**, with the initial construction failure separately
preserved. [Checks]({NAME}/checks.json), [closed call]({NAME}/closed-solver-result.json),
[failure record]({NAME}/preserved-construction-failure.json),
[original short twelve]({NAME}/original-short-twelve.json),
[partial64]({NAME}/partial64-placements.json),
[next inventory]({NAME}/next-fixed40-neighborhood.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']:,} canonical files and {archive['verified_aliases']:,}
aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note=f'''\n\n**N4 fourteen-cog exclusion and twelve-part strip, 2026-10-26:** [the evidence]({{link}})
excludes the previous 43-fixed/non-cog and nine-short-original neighborhood:
all fourteen first-sheet cogs are mandatory in an audited all-angle necessary
model, which returns INFEASIBLE in 8.613520 solver / 9.451583 shared seconds.
The sole call is closed. Exact support rectangles and source-point disks cover
all continuous centers with 135 conservative domains; all 91 cog pairs and
2,409 capacity-one conflicts are verified. A changed original short-sheet
construction fits twelve parts: six brackets, five inserts and one cog.
The initial wrong-arm construction and dependent audit failure are preserved;
the repaired copy passes independent checks of 64 originals, 1,392 pairs,
256 stock edges and 88 cutouts/9,626 hole vertices. Inserts 32/34/35 move off
the first sheet. Cogs 63/64 remain mandatory; the next inventory has 40 fixed
first non-cogs, fourteen moving cogs and twelve fixed short originals.
The old exclusion and domain constraints are not transferred. All eight audits
pass. Main 5928270d now passes all six checks, permitting a normal checkpoint
push. H2/H5 remain open at 60%; production, READMEs, releases and all 22
reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
