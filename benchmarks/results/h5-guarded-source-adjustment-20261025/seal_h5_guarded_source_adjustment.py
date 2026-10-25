"""Seal verified original-source guard corrections and complete actual free regions."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-guarded-source-adjustment-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    prep=load(BASE/'preparation.json');pa=load(BASE/'preparation-audit/checks.json');model=load(BASE/'solve/model-audit.json');solved=load(BASE/'solve/result.json');audit=load(BASE/'audit/checks.json')
    regions=load(BASE/'original-regions/result.json');ra=load(BASE/'original-regions/audit/checks.json')
    assert pa['passed'] and model['passed'] and audit['passed'] and ra['passed']
    assert solved['status']=='OPTIMAL' and solved['solver_calls']==1 and solved['objective_units']==2563
    assert audit['changed_parts']==15 and audit['maximum_absolute_axis_translation_mm']==.023 and audit['nine_prior_pair_shortfalls_resolved'] and audit['four_prior_stock_shortfalls_resolved']
    assert regions['cache_cases_completed']==100 and regions['queries_completed']==20 and not load(BASE/'original-regions/pending-caches.json') and not load(BASE/'original-regions/pending-queries.json')
    prior=load(ROOT/'benchmarks/results/h5-circle-stock-neighborhood-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('f11eb97a') and mainhead=='51fe56c096103464379068c99e10993b5b8516bb'
    ci=load(BASE/'main-ci-snapshot.json');assert ci['databaseId']==40237436741 and ci['headSha']==mainhead;success=sum(j['conclusion']=='success' for j in ci['jobs']);assert len(ci['jobs'])==6
    action=('The adjusted57-original baseline now passes all1246 original pair checks and all228 stock-edge checks above the unchanged native conservative guards. '
            'Use audit/adjusted-fixed-originals.json as a distinct fixed source for the full-original construction; retain all original identities, orientations, sheets and the same material target. '
            'All20 full-original fixed-obstacle free regions are complete and independently audited under original-regions/. They use actual outlines including all80 cog vertices, the recorded source cog angle, all8 bracket orientations and the vertical insert. '
            'Next build full-original mutual collision obstacles for the moving profiles with the same conservative polygonal clearance envelope. '
            'Prepare complete convex decompositions of the free regions and mutual forbidden regions under declared budgets, retaining all components and caps. '
            'The constructive anchor grid is1000 units/mm. Use conservative inward rounding for allowed-domain inequalities and sufficient outward separation inequalities for avoiding every convex forbidden piece; do not reuse the outward necessary-relaxation rounding blindly. '
            'A joint model must place all9 mandatory originals (items28,29,50,54,57,58,62,64,65), preserve all66 original area charges, and retain every allowed mode/sheet in this constructive inventory. '
            'Independently audit actual geometry coverage, every protobuf constraint and parameters before one separately declared bounded call. '
            'A positive requires complete original66-part pair/stock checks and native validation; the57-part baseline alone is not a full target witness. '
            'Finite source cog angle, anchor grid and construction margins make any negative conditional, not unrestricted impossibility. All completed earlier calls remain closed. '
            'Production-budget implementation and the full13-job/two-kerf H5 matrix remain required. H2 stays open without held-out access or release. '
            'Main51fe56c0 already contains six previous checkpoints; CI40237436741 has5/6 successes in this snapshot, with Windows still running. Perform the next normal push after its outcome is known, preserving any newer remote work.')
    OUT.mkdir();copies={'plan.json':'adjustment-plan.json','preparation.json':'adjustment-preparation.json','preparation-audit/checks.json':'preparation-audit.json',
        'solve/plan.json':'solver-plan.json','solve/model-audit.json':'model-audit.json','solve/result.json':'solver-result.json','solve/offsets.json':'offsets.json',
        'audit/checks.json':'original-geometry-audit.json','audit/changes.json':'changes.json','audit/adjusted-fixed-originals.json':'adjusted-fixed-originals.json',
        'original-regions/plan.json':'original-region-plan.json','original-regions/result.json':'original-region-result.json',
        'original-regions/audit/checks.json':'original-region-audit.json','original-regions/query-summary.json':'original-query-summary.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for name,dest in copies.items():shutil.copyfile(BASE/name,OUT/dest)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,
        'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,
        'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'baseline_adjustment_solver_calls':1,'full_original_joint_solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
        'baseline_geometrically_clears_native_guards':True,'full_target_witness':False,'native_full_job_qualified':False,
        'current_main_ci_id':40237436741,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],
        'current_main_successful_jobs':success,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for key in ['inputs','input_hashes']:
            for name,h in load(p).get(key,{}).items():
                if name in inputs:assert inputs[name]==h
                inputs[name]=h
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name]=p
    pending=[ROOT/'output'/n for n in ['prepare_h5_guarded_source_adjustment.py','audit_h5_guarded_source_preparation.py',
        'solve_h5_guarded_source_adjustment.py','audit_h5_guarded_source_solution.py','build_h5_guarded_original_regions.py',
        'audit_h5_guarded_original_regions.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                other=ROOT/'output'/(mod+'.py')
                if other.is_file():pending.append(other)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'all57_originals_preserved_with_bounded_translations':True,'all467_local_constraints_and228_variables695_constraints_audited':True,
        'one_bounded_adjustment_call_optimal':True,'all1246_original_pairs_and228_stock_edges_independently_checked':True,
        'all_nine_prior_pair_and_four_stock_guard_shortfalls_resolved':True,'fifteen_parts_moved_at_most0_023mm_per_axis':True,
        'all100_full_original_obstacles_and20_regions_complete':True,'all11872_raw_triangle_hulls_and2491_expanded_hulls_audited':True,
        'actual_cog_teeth_preserved_and_no_outward_region_padding':True,'production_source_and_readmes_unchanged':True,
        'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: corrected source clearances and original-outline regions — 2026-10-25

**The 57-original starting arrangement now clears the unchanged native
conservative distance and stock guards in independent geometry checks.** Fifteen
parts move by at most **0.023 mm per axis**. Complete clearance regions for all
nine remaining mandatory originals are built from their actual outlines,
including every cog tooth. No full 66-part target layout is claimed; H2/H5 remain
open at **60%** completed milestone weight.

## Small, bounded source adjustment

Every source part keeps its original shape, copy, orientation and sheet. Axis
offsets are bounded to ±0.05 mm on a 0.0001 mm grid. Stock bounds round inward
and require 0.0125 mm beyond the original stock clearances. The pair-gap target
is 0.2125 mm, above the native conservative 0.211708672510 mm requirement.

All **1,246** same-sheet pairs are examined. For 92 near pairs, all **60,404**
boundary-segment pairs are checked, producing **467** projection constraints.
Integer normals, exact rational segment projections and ceiling bounds preserve
the intended gap. These constraints propose a candidate; the subsequent full
original-geometry audit decides whether it is usable.

Preparation takes **{prep['seconds']:.6f} seconds** and its independent audit
**{pa['seconds']:.6f} seconds**. A separate protobuf oracle checks every variable,
constraint, objective and parameter in the **228-variable/695-constraint** model.
One declared 10-second, eight-worker, seed-zero call returns **OPTIMAL in
{solved['seconds']:.6f} seconds**, minimizing the total absolute axis translation
on this bounded grid. All three incumbent records are preserved.

The final total absolute axis translation is **0.2563 mm** across 15 parts:
one frame, five brackets and nine inserts. No cog changes position. The maximum
single-axis change is **0.023 mm**, below the declared 0.05 mm limit.

## Independent full-original checks

Every adjusted polygon is reconstructed from the source job and new transform,
with maximum disagreement of **{audit['maximum_original_reconstruction_error_mm']:.3g} mm**
against an independent translation of the original polygon. All identities,
orientations, mirror flags, sheets and area charges remain unchanged.

All **1,246 original pairs** have zero intersection area and meet the requested
gap. The minimum gap is **{audit['minimum_pair_gap_mm']:.12f} mm**, exceeding the
native conservative distance by **{audit['minimum_pair_excess_above_native_mm']:.12f} mm**.
All **228 stock-edge checks** pass: the minimum extra margin is
**{audit['minimum_extra_stock_margin_mm']:.12f} mm**, exceeding the conversion guard
by **{audit['minimum_stock_excess_above_native_mm']:.12f} mm**. All nine prior pair
shortfalls and all four prior stock shortfalls are resolved.

The preserved partial layout still contains only 57 originals. Its independent
geometry checks do not claim a native full-job validation or a completed target.
The other nine originals remain mandatory, so final counts stay 18 frames,
12 brackets, 21 inserts and 15 cogs. Fixed-original area charges remain
3,831,901,744 / 249,662,718 units across the sheets (1,000 units/mm²).

## Complete full-original clearance regions

All ten moving profiles use actual outer polygons. Both brackets retain every
recorded orientation, the insert remains vertical, and all six cogs use their
known source angle with all **80 original vertices** preserved. This finite
construction inventory does not exhaust all possible cog angles.

All **100** fixed-style/moving-profile collision obstacles are rebuilt. Each
zero-clearance Minkowski obstacle receives an explicit circumscribed 128-gon
clearance envelope, assembled from boundary-segment sums rather than a rounded
buffer substitute. The nominal envelope support is 0.2126 mm; exact rational
halfplane checks certify that it contains the required 0.2125 mm disk.

Each of the **20** mode/sheet queries starts from inward 1-micrometre anchor
bounds with 0.0125 mm extra stock margin, and subtracts every applicable adjusted
fixed-original obstacle. Whole free geometries are retained with **no outward
padding or sampled pose list**. All queries are nonempty. Construction takes
**{regions['seconds']:.6f} seconds**, with no pending cases or caps and
**{regions['region_vertices']:,}** output vertices.

The independent audit takes **{ra['seconds']:.6f} seconds**. It reconstructs raw
obstacles from **11,872 unmerged triangle-pair hulls**, then checks positive
clearance using a different decomposition: **2,491 raw-obstacle triangles**
Minkowski-summed with the complete envelope. It verifies all 128 rational support
lines and 16,384 convexity checks. Maximum raw/expanded obstacle disagreement is
**{ra['maximum_raw_hausdorff_error_mm']:.3g} / {ra['maximum_expanded_hausdorff_error_mm']:.3g} mm**;
maximum free-region disagreement is **{ra['maximum_free_region_hausdorff_error_mm']:.3g} mm**.
Every whole-stock partition is checked against all applicable fixed originals.

Next, construct full-original mutual collision conditions and a joint model for
all nine mandatory moving parts. Allowed-region rounding must stay conservative
inward for this constructive search; the older outward necessary-relaxation
rounding is not a substitute. Every resulting 66-part candidate still needs
original-pair/stock checks, native validation, production-budget implementation
and the full 13-job/two-kerf H5 matrix. Previous completed solver calls stay closed.

## Repository and evidence

Main **51fe56c0** contains the six previously pushed checkpoints and has no new
remote commits after this checkpoint's fetch. [CI 40237436741]({ci['url']}) is
**{ci['status']}**, with **{success}/6** jobs successful in the saved snapshot.
Production source, all three accurate READMEs and release versions remain
unchanged. There is no held-out evaluation, full-job native acceptance or release.

Evidence: [source changes]({NAME}/changes.json),
[original-geometry audit]({NAME}/original-geometry-audit.json),
[model audit]({NAME}/model-audit.json), [bounded result]({NAME}/solver-result.json),
[original-region audit]({NAME}/original-region-audit.json),
[query summary]({NAME}/original-query-summary.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']}** canonical members and
**{archive['verified_aliases']}** identical-content aliases retain exact bytes
with CRC/SHA-256 verification, including all source transforms, proposals,
pair/stock checks, full-original obstacles, free regions and executed helpers.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 corrected source guards and original-outline regions, 2026-10-25:**
[The evidence]({link}) corrects all nine pair and four stock-margin shortfalls
without changing original shapes, counts, orientations, sheets or the material
target. One audited 228-variable/695-constraint bounded adjustment finishes in
0.027011 seconds. Fifteen originals move by at most 0.023 mm per axis. Independent
checks cover all 1,246 original pairs and 228 stock edges; the minimum gap is
0.2125 mm and extra stock margin 0.0125 mm, both above unchanged native guards.
The baseline still contains only 57 originals; all nine others remain mandatory.
All 100 full-original collision obstacles and 20 free-region queries are rebuilt
and independently checked using 11,872 raw triangle hulls and 2,491 expanded
triangle hulls. Every cog tooth is preserved, with no outward region padding.
Next is a joint full-original nine-part model using this adjusted source.
No complete target, native full-job validation or H5 qualification is claimed.
Source, accurate READMEs and releases stay unchanged; H2/H5 remain open at 60%.
'''
    for name in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/name,note.format(link=('' if name=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'production_digest':source_digest(),'main_ci_status':ci['status'],'successful_jobs':success},flush=True)

if __name__=='__main__':main()
