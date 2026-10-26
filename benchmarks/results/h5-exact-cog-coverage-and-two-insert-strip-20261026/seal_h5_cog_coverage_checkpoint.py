"""Seal exact first-sheet collision coverage and the revised64-original branch."""
from pathlib import Path
import ast,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-exact-cog-coverage-and-two-insert-strip-20261026';OUT=ROOT/'benchmarks/results'/NAME
names={'fixed55_screen':'h5-first-three-cog-space-20261026','fixed44_screen':'h5-first-fourteen-cog-space-20261026','coverage':'h5-fixed55-cog-coverage-20261026','partial':'h5-two-insert-short-sheet-20261026','fixed43_screen':'h5-released-twelve-cog-space-20261026','screens_audit':'h5-cog-space-screen-audit-20261026','review':'h5-cog-coverage-review-20261026'}
base={k:ROOT/'output'/n for k,n in names.items()};load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
review=load(base['review']/'review.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==review['source_head']=='2274a7a1396bf5d0e4832ee5ae8cdbdbf9ac394f' and review['main_head']=='9842e4c1d5953970a8698d7f9600a713f154554b' and review['main_ci_id']==40305808059 and review['main_ci_status']=='completed' and review['main_ci_conclusion']=='success' and review['main_ci_successful_jobs']==6;assert source_digest()==review['production_digest'] and all(digest(ROOT/n)==h for n,h in review['current_readmes'].items())
audits=[('coverage','audit/checks.json'),('partial','checks.json'),('partial','audit/checks.json'),('partial','fixed-first-coverage-audit/checks.json'),('screens_audit','checks.json')];assert all(load(base[k]/n)['passed'] for k,n in audits)
coverage=load(base['coverage']/'audit/checks.json');partial=load(base['partial']/'audit/checks.json');inventory=load(base['screens_audit']/'next-neighborhood.json');assert coverage['additional_original_cog_excluded'] and partial['originals_verified']==64 and inventory['all66_originals_accounted_once'] and inventory['moving_count']==14
OUT.mkdir()
for k,n in audits:shutil.copyfile(base[k]/n,OUT/(k+'-'+n.replace('/','-')))
for k,n,d in [('coverage','audit/necessity-proof.json','exact-fixed55-exclusion.json'),('coverage','cover-tree.json','continuous-center-cover.json'),('coverage','audit/exact-source-center-certificates.json','exact-transform-certificates.json'),('coverage','audit/leaf-owner-counts.json','cover-owners.json'),('partial','partial64-placements.json','partial64-placements.json'),('partial','short-sheet-placements.json','original-short-nine.json'),('partial','mandatory-first-additions.json','mandatory-first-additions.json'),('partial','fixed-first-coverage-audit/insert-corner-certificates.json','exact-insert-in-cog-certificates.json'),('screens_audit','verified-screens.json','diagnostic-screen-comparison.json'),('screens_audit','next-neighborhood.json','released-cog-neighborhood.json'),('review','review.json','source-review.json'),('review','main-ci.json','main-ci-9842e4c1-success.json')]:shutil.copyfile(base[k]/n,OUT/d)
write(OUT/'scope.json',{'old_fixed55_no_additional_original_cog':True,'proof_uses_exact_source_membership_trig_intervals_and_continuous_cover':True,'new_fixed55_no_additional_original_cog':True,'revised_originals_placed':64,'revised_short_sheet_originals':9,'old_eight_part_bound_not_transferred_to_changed_allocation':True,'mandatory_unplaced_first_cogs':[63,64],'first_sheet_rearrangement_required_for_current_branch':True,'rearranged_first_sheet_excluded':False,'next_fixed_first_count':43,'next_mandatory_moving_cogs':14,'fixed_short_count':9,'all66_originals_required':True,'solver_calls':0,'native_calls':0,'H5_complete':False})
next_action='All previous solver calls remain CLOSED; this checkpoint makes zero solver calls. Exact rational source-point/cog-disk coverage proves no additional cog fits the former fixed55. Restoring cog53 in place of insert36 only enlarges the fixed filled union, so the no-extra-cog proof also applies to the revised fixed55. The new verified64-original partial puts six brackets21/22/25/26/28/29, two inserts36/37 and cog65 on the short sheet; cogs63/64 remain mandatory first additions. Do not apply the old eight-part count bound to this changed allocation. To make progress, use the explicitly audited next inventory:43 non-cog first originals fixed, all14 first-sheet cogs mandatory and freely movable without mirrors,9 short originals fixed, all66 identities covered exactly once. Twelve prior cog poses are diagnostic seeds only. The disk-only free-center map has area474313.726959mm2 but is not a full-source feasible region or an exclusion certificate. Next construct independently audited all-angle necessary center domains against these43 fixed non-cog originals, strengthening collision constraints with original support where valid; preserve all regions and boundaries before any new separately declared bounded model. Positive necessary placements require actual angles and every original mutual clearance. If the43-fixed neighborhood is excluded, release/rearrange non-cog originals; do not retry closed calls. Full66 native/material validation, production integration under60seconds and complete H5 matrix remain. Main9842e4c1 CI40305808059 passes all six jobs; normally push queued2274a7a1 and this checkpoint after staged-byte/ancestry checks. H2 original gate remains open,22 reserved vectors untouched, no new release qualified.'
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
p=ROOT/'benchmarks/results/h5-short-sheet-count-bound-and-original-eight-20261026/raw-manifest.json';members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
helpers=[ROOT/'output'/n for n in ['screen_h5_first_three_cog_space.py','make_h5_fourteen_cog_screen.py','screen_h5_first_fourteen_cog_space.py','certify_h5_fixed55_cog_coverage.py','audit_h5_fixed55_cog_coverage.py','build_h5_two_insert_short_sheet.py','make_h5_two_insert_audit.py','audit_h5_two_insert_short_sheet.py','audit_h5_restored_cog_coverage.py','make_h5_released_twelve_cog_screen.py','screen_h5_released_twelve_cog_space.py','audit_h5_cog_space_screens.py','make_h5_cog_coverage_review.py','review_h5_cog_coverage_checkpoint.py','ccd1.py','pack_h5_evidence_archive.py']]+[Path(__file__)];seen=set()
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
write(OUT/'checks.json',{'passed':True,'audits_passed':5,'diagnostic_maps_replayed':3,'diagnostic_obstacles_replayed':142,'exact_continuous_cover_nodes':483,'exact_covered_cells':242,'exact_source_centers_checked':222,'exact_trig_angles_checked':3,'old_and_revised_fixed55_exclude_additional_cog':True,'new_originals_placed':64,'new_short_originals':9,'original_pair_checks':1521,'stock_edges_checked':256,'original_cutouts_preserved':88,'original_cutout_vertices_preserved':9626,'remaining_first_cogs':[63,64],'next_fixed_first_originals':43,'next_mandatory_first_cogs':14,'all66_originals_required':True,'solver_calls':0,'native_calls':0,'quality_runs':0,'previous_main_all6_ci_passed':True,'production_and_readmes_unchanged':True,'reserved_H2_vectors_evaluated':0,'full66_target_witness':False,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive});shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# H5: exact cog coverage and a two-insert short sheet — 2026-10-26

**An exact continuous coverage proof shows that no additional cog fits while
the former first-sheet 55 placements stay fixed. A revised allocation stacks
both inserts on the short sheet and restores a first-sheet cog, producing a
verified 64-part partial. Two cogs still require a first-sheet rearrangement.
H2/H5 remain open at 60%; there is no complete target witness.**

## A diagnostic screen, then an exact proof

First compute a diagnostic center map using a 109.10 mm moving disk against
all 55 original filled outers, zero pair clearance and stock relaxed outward
by 0.020 mm. The disk lies inside every original cog. All-angle stock support
of 139.270 mm bounds the center domain. The floating map is empty, but that
result alone is not accepted as a formal exclusion.

The independent certificate covers the entire continuous rectangle
**[145.750, 1354.250] × [145.750, 2854.250] mm** with **242 leaf rectangles**
in a **483-node binary partition**. Each leaf's four corners are strictly
inside one conservative collision disk. Convexity then covers its whole
continuous interior and boundary; every split is checked exactly, with no gaps.

The construction seeds 7,403 collision disks and uses **222** in the final
cover. A 109.10 mm disk is centered near an exact point of a fixed original
filled outer; a 218.20 mm disk is centered near a fixed cog's inscribed-disk
center. The moving cog has an independently certified 109.115 mm inscribed
radius. Fixed cogs have the same radius. Thus the reserved radius losses are
0.015 mm and 0.030 mm, respectively.

The auditor uses exact rational winding/boundary tests for source-point
membership. For each of three stored rotation angles it bounds sine and
cosine by a Taylor polynomial through degree 59, with rigorous remainder
|angle|^60 / 60!. It propagates these intervals through the source transform
and proves the rounded center error fits the reserved radius loss. Exact
integer squared-distance checks certify every leaf corner; the smallest
strict squared margin is **51,526,014 square micrometres**.

No floating polygon buffer, sampled cog angle, finite center grid, or solver
timeout establishes this negative. It covers every real cog angle and every
continuous center within the relaxed stock domain. Filled outers are the
occupied geometry because part-in-hole is disabled. Moving any fixed original
changes the problem and is not excluded by this certificate.

## Revised 64-part allocation

Move insert **36** from the first sheet to the short sheet, stacked above
insert **37** with a 0.225 mm gap. Restore cog **53** at its earlier verified
first-sheet pose, and replace the identical short-sheet cog copy with **65**.
The other **54 first-sheet placements** remain exactly unchanged.

The short sheet now contains **nine originals**: six brackets
**21/22/25/26/28/29**, inserts **36/37**, and cog **65**. The old eight-part
bound concerned a different first-sheet allocation and is not transferred.
The new partial places **64 originals**, with cogs **63/64** explicitly
required on the first sheet. All 66 identities are accounted for exactly once.

All **1,521 same-sheet original filled-outer pairs and 256 stock edges** pass.
The **88 cutouts and 9,626 cutout vertices** are preserved. Minimum pair
distance is 0.212500 mm against the required native guarded distance of
0.211708673 mm; minimum extra stock margin is 0.012500 mm. A separate auditor
directly transforms every original vertex, checks allowed rotations/mirrors,
cutout coordinates and areas, and repeats the pair and stock checks.

The new fixed55 still cannot accept an extra cog. Four exact corner checks
prove the removed insert's whole rectangular outer lies inside the restored
cog53 inscribed disk. The new fixed filled union therefore contains the old
one, so the exact collision cover transfers. The remaining two cogs require
moving first-sheet originals; a complete native job is not run on this partial.

## The next rearrangement retains all originals

Release all **12 existing first-sheet cogs**, retaining **43 non-cog first
originals** and the **nine short-sheet originals**. Together with the two
unplaced cogs, all **14 first-sheet cogs** are mandatory movers with their
original free-rotation/no-mirror rules. The 12 saved poses are diagnostic seeds,
not locks or a completeness claim. The inventory independently accounts for
all 66 originals exactly once.

The disk-only screen for those 43 fixed originals has one component of area
**474,313.726959 mm²**, bounded by X=370.125555–1354.250 mm and
Y=2216.737600–2784.387400 mm. A preceding 44-fixed diagnostic map had area
429,417.482877 mm². All three maps and **142 fixed obstacles** are replayed,
but the maps remain screening data, not original-cog feasible regions or
exact exclusions. Original-support constraints and complete domain audits
should precede a new bounded search. A positive necessary placement still
needs actual cog angles and every original mutual clearance.

This checkpoint makes **zero solver calls** and does not reopen any closed
call. Full66 native/material validation, production integration within 60
seconds and the complete H5 matrix remain required.

## Repository and evidence

At **{review['utc']}**, local HEAD **2274a7a1** is queued above main **9842e4c1**.
All six jobs in [CI40305808059](https://github.com/skulitom/Nestbolt/actions/runs/40305808059)
have passed, permitting a normal push of both checkpoints after staged-byte
and ancestry checks. Production and README digests, upstream stop-rule state
and the 22 reserved H2 vectors remain unchanged. H2 retains its original gate;
no new release is qualified.

All **five audits pass**. [Checks]({NAME}/checks.json),
[exact exclusion]({NAME}/exact-fixed55-exclusion.json),
[partial64]({NAME}/partial64-placements.json),
[next inventory]({NAME}/released-cog-neighborhood.json),
[scope]({NAME}/scope.json), [next step]({NAME}/next-step.json),
[raw manifest]({NAME}/raw-manifest.json). The archive verifies
{archive['archive_members']:,} canonical files and {archive['verified_aliases']:,}
aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note=f'''\n\n**N4 exact cog coverage and two-insert strip, 2026-10-26:** [the evidence]({{link}})
proves no additional cog fits the former fixed 55 first-sheet placements at
any angle or continuous center. An exact 483-node partition covers the full
center-stock rectangle with 242 cells; 222 source points/disks and three
rotation angles pass rational membership, Taylor-interval and corner checks.
A revised allocation stacks inserts 36/37 on the short sheet with six brackets
and cog 65, restores cog 53 first, and independently verifies 64 originals,
1,521 pairs, 256 stock edges and 88 cutouts/9,626 hole vertices. The old eight-part
bound is not applied after this allocation change. Cogs 63/64 remain mandatory.
Exact insert-in-cog containment transfers the no-extra-cog result to the new
fixed 55, requiring a first-sheet rearrangement. The next audited inventory
fixes 43 non-cog first originals and nine short originals, with all 14 first-sheet
cogs mandatory movers. Three diagnostic maps are replayed but do not prove
source feasibility. All five audits pass, with zero new solver calls. Main
9842e4c1 now passes all six checks, permitting a normal push of queued
checkpoints. H2/H5 remain open at 60%; production, READMEs, releases and all
22 reserved H2 vectors are unchanged.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print({'sealed':NAME,**archive},flush=True)
