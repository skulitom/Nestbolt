"""Seal the stronger unresolved search and full-original construction preparation."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-circle-stock-neighborhood-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
OLD=ROOT/'output/h5-conflict-owner-neighborhood-20261025';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    generation=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');model=load(BASE/'solve/model-audit.json');solved=load(BASE/'solve/result.json')
    prep=load(BASE/'original-outline-construction/checks.json');original=load(BASE/'original-outline-construction/audit/checks.json')
    assert audit['passed'] and model['passed'] and original['passed'] and generation['queries_completed']==20 and not load(BASE/'pending.json')
    assert solved['status']=='UNKNOWN' and solved['solver_calls']==1 and not solved['incumbents'] and not solved['has_complete_66_part_necessary_proxy_solution']
    assert not (BASE/'solve/positions.json').exists()
    assert audit['reused_query_bytes_verified']==18 and model['integer_square_constraints']==30 and model['exact_moving_cog_circle_pairs']==15
    assert original['fixed_pair_native_margin_shortfalls']==9 and original['fixed_stock_guard_shortfalls']==4
    prior=load(ROOT/'benchmarks/results/h5-conflict-owner-neighborhood-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head=='94bbb68331b9adfc76985bbb9b521895777656d9' and mainhead=='51fe56c096103464379068c99e10993b5b8516bb'
    ci=load(BASE/'main-ci-snapshot.json');assert ci['databaseId']==40237436741 and ci['headSha']==mainhead
    successful=sum(j['conclusion']=='success' for j in ci['jobs']);assert len(ci['jobs'])==6
    action=('The stronger 128-vertex/exact-circle/stock-bound call ended UNKNOWN with no incumbent and is closed; do not retry, extend or merely retune it. '
            'Proceed with the distinct full-original-outline constructive preparation, which preserves every cog tooth at the known source angle, all bracket choices and all66 required originals. '
            'Before freezing the57 source originals for that construction, address the independently recorded9 pair-distance and4 stock-margin shortfalls. '
            'Prepare a separately bounded small-translation adjustment of those57 actual original shapes, keeping their original sheets, orientations, counts and target stock/material bounds; do not lower native conversion/separation guards. '
            'Declare the offset range/grid, work budget and whether any local linear approximation is only a proposal mechanism. Independently validate every original pair and every stock boundary after any candidate. '
            'A verified adjusted baseline requires fresh full-original collision domains; it is a distinct source arrangement, not evidence that either closed necessary-model search succeeded. '
            'The prepared10 full-original profiles and20 inward stock-grid queries use a finite source cog angle and1-micrometre anchor grid, so negatives are not unrestricted impossibility proofs. '
            'Then pursue all9 mandatory placements with conservative original-outline clearance geometry, retaining all66 original area charges and the material cap. '
            'Any positive must still pass native validation, production-budget implementation and the full13-job/two-kerf H5 matrix. H2 stays open with no held-out access; no release is qualified. '
            'Main51fe56c0 contains the previous six checkpoints; track CI40237436741 separately before the next periodic normal push.')
    OUT.mkdir()
    copies={'plan.json':'domain-plan.json','result.json':'domain-result.json','audit/checks.json':'domain-audit.json',
        'audit/prior-anchor-checks.json':'prior-anchor-checks.json','cog-floor-certificate.json':'cog-floor-certificate.json',
        'solver-preparation.json':'solver-preparation.json','solve/plan.json':'solver-plan.json','solve/model-audit.json':'model-audit.json',
        'solve/result.json':'solver-result.json','original-outline-construction/profiles.json':'original-profiles.json',
        'original-outline-construction/queries.json':'original-stock-queries.json','original-outline-construction/checks.json':'original-preparation.json',
        'original-outline-construction/audit/checks.json':'original-preparation-audit.json',
        'original-outline-construction/native-margin-shortfalls.json':'fixed-pair-guard-shortfalls.json',
        'original-outline-construction/audit/fixed-stock-guard-shortfalls.json':'fixed-stock-guard-shortfalls.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for name,dest in copies.items():shutil.copyfile(BASE/name,OUT/dest)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,
        'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
        'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,
        'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,
        'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,
        'current_main_ci_id':40237436741,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],
        'current_main_successful_jobs':successful,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for key in ['inputs','input_hashes','production_guard_source_hashes']:
            for name,h in load(p).get(key,{}).items():
                if name in inputs:assert inputs[name]==h
                inputs[name]=h
    for row in load(BASE/'audit/provenance.json'):
        for name,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            if name in inputs:assert inputs[name]==h
            inputs[name]=h
    for row in load(BASE/'cache-references.json'):inputs[row['source']]=row['sha256']
    for name,h in load(BASE/'solver-preparation.json')['sources'].items():inputs[name]=h
    for name,h in load(BASE/'solver-preparation.json')['generated'].items():inputs[name]=h
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name]=p
    pending=[ROOT/'output'/n for n in ['build_h5_circle_stock_neighborhood.py','audit_h5_circle_stock_neighborhood.py',
        'prepare_h5_circle_stock_solver.py','solve_h5_circle_stock_neighborhood.py','audit_h5_circle_stock_model.py',
        'prepare_h5_original_outline_construction.py','audit_h5_original_outline_construction.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'all20_mode_sheet_queries_complete':True,'all18_prior_queries_reused_unchanged':True,
        'all274_domains_and4204_outward_halfplanes_audited':True,'all512_cog_floor_error_corners_certified':True,
        'all361_minkowski_hulls_and6176_facet_normals_audited':True,'all9549_variables22313_constraints_and_parameters_reconstructed':True,
        'all15_exact_circle_pairs_and30_integer_square_constraints_audited':True,'one_bounded_call_unknown_without_incumbent':True,
        'solver_soft_time_overrun_seconds':max(0,solved['seconds']-60),'unknown_not_reported_as_infeasible':True,
        'all80_original_cog_vertices_preserved_for_distinct_construction':True,'nine_pair_and_four_stock_guard_shortfalls_preserved':True,
        'production_source_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,
        'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: stronger cog circles, stock bounds and original outlines — 2026-10-25

**The stronger nine-part model ends UNKNOWN after its one bounded call, with no
incumbent.** It remains unresolved. A separate full-original-outline construction
is prepared, and its starting arrangement is checked for native-margin shortfalls.
H2/H5 remain open at **60%** completed milestone weight.

## Stronger necessary geometry

The same 57 source originals remain fixed, with nine mandatory moving originals
and all 66 original area charges. The new cog polygon has **128 vertices**, contains
the previous 16-gon, and stays inside the original cog's certified inscribed disk
for every angle and coordinate-floor error. All **512 vertex/error-corner tests**
are exact integers; the strict squared margin is **35,535,031** geometry units.
This polygon is explicitly an approximation, distinct from the whole circle.

All 18 non-cog queries are reused byte for byte. Ten fixed-style/cog collision
entries are rebuilt; 100 other entries remain unchanged. Both fresh cog queries
start from the certified **139.2707 mm** minimum all-angle stock supports. That
convex-hull support is used only for sheet boundaries, never for collision shapes.

Construction completes in **{generation['seconds']:.6f} seconds** with all 20 queries,
**274 convex domains**, no pending work and no caps. Independent verification
takes **{audit['seconds']:.6f} seconds** and checks 29 committed source matches,
106 new triangle collision hulls, **4,204 outward halfplanes**, **85,992 rational
vertex tests**, all seven released source poses and complete stock-region coverage.
The support atlas has 19 component types and **132 normals**; all **361 exact
Minkowski hulls** and **6,176 facets** are independently verified. Both prior
fixed-conflict anchors and all three prior stock-invalid anchors are rejected.

## Fully audited bounded search

The model contains **9,549 variables and 22,313 constraints**, including 46 mode
choices, 932 complete per-part domain choices and 11,679 reified halfplanes.
All 53 cross-part component pairs use the 132-normal basis, giving 6,996 exact
projection choices. Both arms of each bracket share their part position and mode.

Each of the 15 moving-cog pairs also has an exact whole-circle condition when
both cogs occupy the same sheet. For 0.01 mm anchor units, it requires
`dx² + dy² ≥ 21820²`, corresponding to two certified **109.1 mm** circles.
Thirty integer square equalities and all sheet conditions are checked by an
independent protobuf oracle. No same-part separation, optional original part,
objective, hint or copy-order restriction is introduced. The original area
charges and complete allowed sheet/orientation inventory remain.

Model construction and the full oracle take **{model['construction_seconds']:.6f}**
and **{model['audit_seconds']:.6f} seconds** respectively. One declared 60-second,
eight-worker, seed-zero call starts search at 0.87 seconds and returns
**UNKNOWN in {solved['seconds']:.6f} seconds**. The solver's small soft-limit overrun
is preserved. It records 630,343 branches and 24,445 conflicts, with no incumbent.
The completed call is neither retried nor extended. UNKNOWN supplies no
infeasibility proof and no accepted layout.

## Full original geometry prepared for a distinct construction

Ten actual oriented profiles preserve the original outer polygons, including
**all 80 cog vertices**. Both brackets retain all eight orientations, the insert
retains its vertical orientation, and all six cogs use their shared known source
angle. Twenty inward-rounded stock-anchor rectangles use a 1-micrometre grid.
These finite angle/grid choices define a constructive search; a negative could
not establish unrestricted impossibility.

Independent checks reconstruct all seven moved source parts from those profiles,
verify every original vertex and all inward stock bounds, and retain every
recorded bracket/insert mode. No original-outline collision domains or new solver
call are made at this preparatory stage.

Checking the 57 fixed originals covers **1,246 original pairs**, all of which
meet the original 0.2 mm clearance. Their minimum gap is
**{prep['minimum_fixed_original_gap_mm']:.12f} mm**. However, **nine pairs** are below
the native engine's conservative distance of **0.211708672510 mm**, and **four
parts** lack the **0.011444091797 mm** conversion guard at a stock edge. The
thresholds are derived from the current production source and are not reduced.
All shortfalls and the source hashes are retained. This starting arrangement
is not described as native-qualified.

The next construction must first adjust the starting originals to meet these
guards while preserving their sheets, orientations, counts and target stock
bounds. Any proposed small translations must be checked against every original
pair and every boundary before freezing the adjusted source. Full-original
collision domains then need to be rebuilt for that source. This is separate
from the closed necessary-model calls; none is retroactively accepted.

Actual original geometry, native validation, production-budget implementation
and the complete 13-job/two-kerf H5 matrix remain required. No material limit,
clearance, original count or gate is changed.

## Repository and evidence

Main remains **51fe56c0**, containing the six previously pushed checkpoints.
[CI 40237436741]({ci['url']}) is **{ci['status']}**, with **{successful}/6** jobs
successful in the saved snapshot. The next periodic push will be tracked
separately. Production source, all three accurate READMEs and release versions
remain unchanged. There is no held-out evaluation, native acceptance or release.

Evidence: [domain audit]({NAME}/domain-audit.json),
[model audit]({NAME}/model-audit.json), [bounded result]({NAME}/solver-result.json),
[full-original profiles]({NAME}/original-profiles.json),
[profile and margin audit]({NAME}/original-preparation-audit.json),
[pair shortfalls]({NAME}/fixed-pair-guard-shortfalls.json),
[stock shortfalls]({NAME}/fixed-stock-guard-shortfalls.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']}** canonical members and
**{archive['verified_aliases']}** identical-content aliases retain exact bytes
with CRC/SHA-256 checks, including all domains, model/log, original profiles,
source data, guard-source code and executed helpers.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 stronger circles and full-original construction, 2026-10-25:**
[The evidence]({link}) strengthens the same 57-fixed/nine-moving neighborhood
with a certified 128-vertex cog proxy, exact circle separation for all 15 cog
pairs and the all-angle stock bounds. All 20 queries complete; 18 are reused
unchanged. Independent checks cover 274 domains, 4,204 outward halfplanes,
85,992 rational vertex tests and 361 exact component Minkowski hulls.
The fully audited 9,549-variable/22,313-constraint model returns UNKNOWN in
60.174056 seconds, with no incumbent; the completed call stays closed.
A distinct full-original preparation retains every cog tooth at its known source
angle, all bracket choices and 20 inward stock-grid queries. Its 57 starting
originals meet the 0.2 mm requested clearance, but nine pairs and four stock
margins fall below the current native conservative guards. These shortfalls
must be addressed and independently checked before that source is frozen for
an original-outline construction. No guard, material cap or count is reduced.
No accepted target or H5 qualification is claimed. Source, accurate READMEs and
releases stay unchanged; H2/H5 remain open at 60% completed milestone weight.
'''
    for name in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/name,note.format(link=('' if name=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'production_digest':source_digest(),'main_ci_status':ci['status'],'successful_jobs':successful},flush=True)

if __name__=='__main__':main()
