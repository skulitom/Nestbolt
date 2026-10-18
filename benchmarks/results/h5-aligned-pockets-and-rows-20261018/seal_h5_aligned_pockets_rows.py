from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,shutil,subprocess,zipfile,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));from h2_import_audit import source_digest
OUT=ROOT/'benchmarks/results/h5-aligned-pockets-and-rows-20261018';PREFIX='h5-aligned-pockets-and-rows-20261018'
NAMES=['h5-aligned-stagger-20261018','h5-aligned-aspect-cpsat-20261018','h5-aligned-aspect-rectangles-20261018','h5-aligned-aspect-backfill-20261018','h5-aligned-truncated-20261018','h5-aligned-pockets-20261018','h5-pocket-aspect-rectangles-20261018','h5-pocket-aspect-backfill-20261018','h5-five-row-shelves-20261018','h5-five-row-backfill-20261018']
RUNS={n:ROOT/'output'/n for n in NAMES};load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    OUT.mkdir();source=source_digest();assert source=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88';readmes={n:digest(ROOT/n) for n in ['README.md','README.ja.md','README.zh-CN.md']};previous=load(ROOT/'benchmarks/results/h5-outline-contact-direction-20261018/source-review.json');assert readmes==previous['readmes_unchanged']
    stagger=load(RUNS[NAMES[0]]/'audit.json');model=load(RUNS[NAMES[1]]/'model-audit.json');solver=load(RUNS[NAMES[1]]/'result.json');modelgeometry=load(RUNS[NAMES[1]]/'geometry-audit.json');pockets=load(RUNS[NAMES[5]]/'audit/checks.json');novelty=load(RUNS[NAMES[8]]/'pose-novelty.json')
    searches=[load(RUNS[NAMES[i]]/'result.json') for i in [2,6,8]];traces=[load(RUNS[NAMES[i]]/'trace-audit.json') for i in [2,6,8]];fills=[load(RUNS[NAMES[i]]/'results.json') for i in [3,7,9]];audits=[load(RUNS[NAMES[i]]/'audit/checks.json') for i in [3,7,9]]
    assert stagger['original_pair_checks']==3080 and pockets['pocket_pair_checks']==29724 and pockets['pocket_candidate_checks']==5511;assert solver['status']=='UNKNOWN' and not solver['feasible'] and model['all_variable_domains_and_constraints_verified'];assert not modelgeometry['full_target_witness']
    assert all(not r['complete'] for r in searches) and [r['attempts'] for r in searches]==[109200,1573800,1028981];assert [r['expired'] for r in searches]==[False,False,True] and traces[-1]['unattempted_after_limit']==60583
    assert all(r['no_complete_witness'] for r in audits) and sum(r['filled_outer_pairs'] for r in audits)==27954 and sum(r['candidate_additions_independently_verified'] for r in audits)==54;assert all(not r['full_witness'] and not r['expired'] for r in fills);assert novelty['new_signatures_total']==261
    ci=json.loads(subprocess.check_output(['gh','run','view','39146239813','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']=='f825cab1cbdcea9854a2e987eb8f4e36ddb72bdb' and ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs']);write(OUT/'main-ci-f825cab.json',ci)
    live=json.loads(subprocess.check_output(['gh','run','view','39149585692','--json','status,conclusion,headSha,jobs,url'],cwd=ROOT));assert live['headSha']=='c9b01762f0163ac8167a8a02ac7e27ff1c7f2701'
    next_step=('The coordinated original geometry now supplies materially different positions for a finite placement-selection model. The new best partial has all frames, brackets and cogs but lacks eight inserts; its filled area is 4,323,340.784069745 mm2, still 8,211.84318605 mm2 below the earlier 63-part partial missing three cogs. Do not rerun the UNKNOWN shared-coordinate model, completed column sweeps or timed-out row suffix, and do not extend their limits. Next prepare a fresh extension of the previously audited 8,798-pose contact-selection pool from the 24 retained layouts in h5-aligned-aspect-backfill-20261018, h5-pocket-aspect-backfill-20261018 and h5-five-row-backfill-20261018, plus the 24 verified frame-only row allocations in h5-five-row-shelves-20261018. A diagnostic 0.0001 mm vertex-signature census identifies 261 additional signatures: 97 frame, 63 bracket, 66 insert and 35 cog; the row-run retained layouts add no signatures beyond the column layouts, while its frame-only allocations add 55. This census is not a pool mutation and its rounding must not change original stored coordinates or establish tolerance-based acceptance. Declare exact deduplication, source lists and one finite full-inventory selection limit before running. Preserve every old candidate, graph, failure and model; verify new candidates against original geometry/rotations/target bounds and audit all added old-new/new-new conflicts, reusing old graph evidence only under exact hashes. Keep a reproducible feasible partial hint without treating it as a complete solution. This combines different arrangements rather than committing an entire layout greedily. Any full 66-copy result must pass frozen original CLI and independent filled-outer checks; native margin qualification, original repair budgets/four-step cap and full H5 comparison remain required before integration. Older bracket patterns still have only about 0.2011 mm physical separation and are not native-margin qualified. No restricted failure proves the unrestricted original job impossible.')
    write(OUT/'source-review.json',{'next_investigation':next_step,'production_digest':source,'readmes_unchanged':readmes,'runtime_changed':False,'native_packing_calls':0,'quality_runs':0,'frozen_cli_calls':24,'full_target_witnesses':0,'all_failures_and_expirations_preserved':True,'old_bracket_native_margin_unqualified':True,'previous_63_part_partial_still_greater_filled_area':True,'all_six_f825cab_checks_pass':True,'pushed_checkpoint':'c9b01762f0163ac8167a8a02ac7e27ff1c7f2701','current_main_CI_snapshot':live,'H5_complete':False,'completion_percent':60})
    shutil.copyfile(RUNS[NAMES[5]]/'comparison.png',OUT/'comparison.png');members={}
    for root in RUNS.values():
        for p in sorted(root.rglob('*')):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    helpers=['construct_h5_aligned_stagger.py','audit_h5_aligned_stagger.py','prepare_h5_aligned_aspect_model.py','audit_h5_aligned_aspect_model.py','solve_h5_aligned_aspects.py','audit_h5_aligned_aspect_geometry.py','construct_h5_aligned_aspect_rectangles.py','prepare_h5_aligned_aspect_backfill.py','backfill_h5_aligned_aspects.py','audit_h5_aligned_aspect_backfill.py','audit_h5_aligned_rectangle_trace.py','construct_h5_aligned_truncated.py','prepare_h5_aligned_pockets.py','fill_h5_aligned_pockets.py','prepare_h5_aligned_pocket_audit.py','audit_h5_aligned_pockets.py','plot_h5_aligned_pockets.py','construct_h5_pocket_aspect_rectangles.py','prepare_h5_pocket_aspect_checks.py','backfill_h5_pocket_aspects.py','audit_h5_pocket_aspect_backfill.py','audit_h5_pocket_rectangle_trace.py','prepare_h5_row_shelves.py','construct_h5_five_row_shelves.py','prepare_h5_row_shelf_checks.py','audit_h5_row_shelf_trace.py','backfill_h5_row_shelves.py','audit_h5_row_shelf_backfill.py','inspect_h5_coordinated_pose_novelty.py','construct_h5_pattern_layouts.py','construct_h5_outline_beam.py','diagnose_h5_concave_gaps.py','audit_h5_cog_lattices.py','fill_h5_ragged_pockets.py','audit_h5_ragged_geometry.py','backfill_h5_cog_lattices.py','audit_h5_lattice_backfill.py']
    for n in helpers:members['helpers/'+n]=ROOT/'output'/n
    inputs=[ROOT/'output/h5-cog-lattices-20261018/all-patterns.json',*[ROOT/'output/h5-minimum-contact-grids-20261018'/n for n in ['plan.json','phases.json','audit.json','obstacles/0.0.json']],ROOT/'output/h5-contact-placement-selection-20261018/candidates.json']
    for p in inputs:members['source-inputs/'+p.relative_to(ROOT/'output').as_posix()]=p
    manifest=[];archive=OUT/'raw.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(members.items()):z.write(p,name);manifest.append({'path':name,'bytes':p.stat().st_size,'sha256':digest(p)})
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==len(manifest)
        for row in manifest:assert sha256(z.read(row['path'])).hexdigest()==row['sha256']
    write(OUT/'raw-manifest.json',{'archive_sha256':digest(archive),'files':manifest});write(OUT/'checks.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'staggered_component_audit':stagger,'shared_coordinate_model_audit':model,'solver_result':solver,'model_geometry':modelgeometry,'pocket_audit':pockets,'rectangle_searches':searches,'rectangle_trace_audits':traces,'original_outline_continuations':fills,'continuation_audits':audits,'pose_novelty_census':novelty,'archive_members':len(manifest),'archive_sha256':digest(archive),'production_digest':source,'H5_complete':False,'completion_percent':60});shutil.copyfile(__file__,OUT/'seal_h5_aligned_pockets_rows.py')
    rows='\n'.join(f"| {name} | {r['attempts']:,} | {r['seconds']:.6f} | {'expired' if r['expired'] else 'finished'} | {r['best_count']}/66 | {r['best_filled_area_mm2']:.3f} |" for name,r in zip(['Aligned components, fixed columns','Filled pockets, fixed columns','Same filled recipes, five frame rows'],searches))
    doc=f'''# H5: aligned pockets, independent bracket aspects and frame rows — 2026-10-18

**The component geometry improves; no full target layout is qualified.** The
strongest new retained layout has every frame, cog and bracket, but is missing
eight inserts. Its filled area, **4,323,340.784070 mm²**, remains **8,211.843186 mm²**
below the earlier 63-part partial missing three cogs. H2/H5 remain open at **60%**.

The [contact-direction study](h5-outline-contact-direction-20261018.md) supplies
the original cog angle and horizontal pitch. The original 66-copy job, stock,
reserved holes and 0.2 mm clearance stay unchanged. The last-sheet used-height
limit remains **325.92690233 mm**, corresponding to **4,988,890.353495 mm²** of
charged material. These are offline constructions, not native quality runs.

![Original square and staggered components with inserts]({PREFIX}/comparison.png)

## Actual contact geometry and filled pockets

Eight declared row-offset fractions and nine patch sizes produce **72** valid
components. Their **3,080** original pair checks pass at minimum
**0.225123442 mm**. Independent rays in the unrotated exclusion polygon recover
vertical pitches within **8.6×10⁻¹⁴ mm**; all member transforms and nondominated
bounding choices are verified. The half-offset fifteen-cog group is
**1,444.523309 × 767.082326 mm**, 30.455373 mm shorter than the square group,
while remaining inside the original usable stock width.

Using those same audited pitches, a finite follow-up forms **28** patches with
9–15 cogs, four or five columns, and square or half-offset rows. All **1,904**
original pair checks pass. Two filler-family orders and four corner priorities
give **224** mixed components in **18.317621 seconds**. All cog poses and group
bounds remain exact. Independent checks cover **5,511** proposed additions and
**29,724** final component pairs; the minimum distance is about **0.2251 mm**.
There are 993 accepted additions across these alternative components, not within
one job. Every implied remainder still contains exactly the original inventory.
The fifteen-cog staggered component holds **three inserts** in its side pockets.
Component checks alone establish neither full-job savings nor native acceptance.

## Whole-inventory construction

One new exact-count model allows all eighteen frame rectangles to translate,
six bracket-pair slots to independently choose any of the three retained aspects,
fifteen remaining inserts, and one of five complete cog decompositions. Shared
position/size variables and two non-crossable stock strips avoid duplicated
coordinates per alternative. Independent protobuf review verifies all **465**
variable domains, **393** constraints and **136** choices, including all inventory,
area bounds and interchangeable-copy ordering. The first auditor has a false
empty-slot assertion; its original source and failure remain. A corrected
inventory comparison passes without changing model bytes or inputs.

The unchanged seed 0, eight offline workers and 120-second ceiling return
**UNKNOWN after 120.160022 seconds**, with no full selection. This is not an
infeasibility result. Its 20 source components also pass 766 original pair checks.
The older bracket patterns have only about **0.2011 mm** spacing: they satisfy
the original physical condition but are **not native-margin qualified**.

Separate deterministic rectangle sweeps use the audited components, all three
bracket aspects and original quantities. A complete 364-recipe sweep tries the
new unfilled cog shapes. The filled-pocket sweep retains 93 distinct rectangle/
inventory combinations from 224 components, records 131 rectangle-equivalent
omissions, and expands all 5,246 remaining-inventory recipes. It includes actual
aligned cog prefixes whose additional 66 pair checks pass. These equivalences
apply only to rectangle packing, not to arbitrary outline placement.

| Construction | Attempted arrangements | Seconds | Outcome | Greatest-filled-area partial | Filled area, mm² |
| --- | ---: | ---: | --- | ---: | ---: |
{rows}

The row study enumerates all 32 five-row orientation sequences and retains
**24** distinct valid count allocations. Five is the minimum possible shelf-row
count for eighteen frames at this width; higher row counts and unrestricted frame
positions remain outside this sweep. Its original patterns and 5,246 recipes
are byte-identical to the filled-pocket column study. **35,107** recipe/frame
prefixes are skipped because their mandatory component rectangle fits none of
the saved free rectangles. Every filter is independently checked, as are **3,672**
fixed-frame pairs and the exact free-space union (maximum area discrepancy
**6.8×10⁻¹⁰ mm²**). The 120-second cap leaves **60,583** arrangements unattempted;
the measured 120.018964-second soft overrun is retained. No suffix retry occurs.

All **2,711,981** attempted inventory records, missing counts and filled areas
recompute. Geometry of every rejected arrangement is not claimed to be audited.
Eight retained partials from each sweep receive one original-outline gap-fill
continuation. All 24 finish without expiry, adding 18 parts across their separate
layouts. Independent audits verify **54** proposed additions and **27,954**
retained-layout pairs, preserve every initial placement, and check original stock,
rotations, quantities and material target. The frozen CLI rejects all 24 for
missing quantities. No partial is relabelled as valid, and no full witness emerges.

## Next evidence to use

A geometry-signature census against the earlier 8,798-entry contact pool finds
**261** additional signatures: 97 frame, 63 bracket, 66 insert and 35 cog. Of
these, 55 come from the verified frame-only row allocations. The row run's
retained layouts add no signatures beyond the column results. Rounding to
0.0001 mm is used only for this diagnostic census; original coordinates are
unchanged and no candidate graph or new selection run is claimed.

{next_step}

[Checks]({PREFIX}/checks.json), [all raw inputs, models, failures, searches and
audits]({PREFIX}/raw.zip), [verified manifest]({PREFIX}/raw-manifest.json),
[source review]({PREFIX}/source-review.json). All **{len(manifest)}** archive members,
CRCs and byte hashes verify; the component figure has been visually reviewed.

All six hosted checks on [main f825cab]({PREFIX}/main-ci-f825cab.json) pass.
The preceding contact-direction checkpoint is pushed to main as **c9b0176**;
its ongoing check snapshot is recorded accurately in source review. Production,
gate limits, preview assets and all three accurate READMEs remain unchanged.
No runtime integration, new release qualification or gate credit is claimed.
'''
    (OUT.parent/(PREFIX+'.md')).write_text(doc,encoding='utf-8',newline='\n')
    note=f'''**N4 aligned pockets and frame rows, 2026-10-18:** [verified contact-aligned components](../benchmarks/results/{PREFIX}.md)
include a fifteen-cog group with three inserts, preserving every original outline
and all group bounds. Checks cover 224 filled alternatives, 5,511 proposed
additions and 29,724 component pairs. The independent-bracket-aspect model remains
UNKNOWN. Column and row constructions retain 2,711,981 attempted arrangements;
the row cap leaves 60,583 unattempted. Twenty-four outline continuations preserve
27,954 checked pairs, but all remain incomplete. The best new 58-part layout lacks
eight inserts and still has less filled area than the earlier 63-part partial.
A diagnostic census supplies 261 new geometric signatures for the next exact-count
placement-selection pool; original coordinates remain untouched. All six f825cab
checks pass, and c9b0176 is pushed to main. Original failures, native-margin caveats
and all gate limits remain; no runtime/release/README change or gate credit. 60%.
'''
    old=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=ROOT);assert (ROOT/'BENCHMARKS.md').read_bytes()==old;append(ROOT/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(ROOT/n,'\n'+note)
    p=ROOT/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 contact direction and outline construction, 2026-10-18:**';assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n');append(ROOT/'.gitattributes',f'\nbenchmarks/results/{PREFIX}/** -text -whitespace\n')
    print(json.dumps({'sealed':True,'archive_members':len(manifest),'archive_bytes':archive.stat().st_size,'all_f825cab_checks':'success','c9b0176_status':live['status'],'completion_percent':60}),flush=True)
if __name__=='__main__':main()
