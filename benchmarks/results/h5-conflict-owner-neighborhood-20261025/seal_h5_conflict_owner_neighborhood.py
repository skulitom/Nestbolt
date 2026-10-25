"""Seal the complete nine-part search, rejected lift and stronger cog proof."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-conflict-owner-neighborhood-20261025';BASE=ROOT/'output'/NAME
OUT=ROOT/'benchmarks/results'/NAME;SYNC=ROOT/'output/h5-strong-pair-main-sync-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    generation=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');model=load(BASE/'solve/model-audit.json')
    solved=load(BASE/'solve/result.json');lift=load(BASE/'solution-audit/checks.json');strong=load(BASE/'stronger-cog-conditions/audit/checks.json')
    assert audit['passed'] and model['passed'] and lift['passed'] and strong['passed']
    assert generation['queries_completed']==generation['queries_planned']==20 and not load(BASE/'pending.json')
    assert generation['convex_domains']==199 and not any(generation[k] for k in ['merge_cap_queries','merge_time_queries','domain_cap_reached'])
    assert solved['status']=='OPTIMAL' and solved['solver_calls']==1 and len(solved['incumbents'])==1
    assert solved['has_complete_66_part_necessary_proxy_solution'] and lift['necessary_model_solution_verified']
    assert lift['original_outline_trial_pair_failures']==17 and lift['original_outline_trial_stock_failures']==3 and not lift['original_outline_trial_valid']
    assert [strong[k] for k in ['selected_cog_pair_exclusions','selected_fixed_pair_exclusions','selected_stock_exclusions']]==[3,2,3]
    prior=load(ROOT/'benchmarks/results/h5-strong-pair-relocation-exclusion-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head==mainhead=='51fe56c096103464379068c99e10993b5b8516bb'
    receipt=load(SYNC/'receipt.json');assert receipt['source_head']==head and receipt['pushed_commits']==6 and receipt['normal_fast_forward_push'] and receipt['remote_main_verified']
    ci=load(BASE/'main-ci-final-snapshot.json');assert ci['headSha']==head and ci['databaseId']==40237436741
    success=sum(j['conclusion']=='success' for j in ci['jobs']);assert len(ci['jobs'])==6
    action=('Use the independently certified whole-circle radius of 109.1 mm and all-angle stock support of 139.2707 mm to strengthen this same nine-part construction. '
            'Keep all 57 fixed originals, all nine mandatory moving originals, the complete source orientation inventory, both allowed sheets and all 66 original area charges. '
            'Build fresh cog domains against the fixed original outlines using a separately declared, audited conservative representation of the certified whole circle; '
            'a higher-resolution inscribed polygon may supply linear fixed-obstacle conditions, but must not be called the exact circle. '
            'Add exact squared-distance conditions for moving cog circles where practical, and use the certified stock bounds for every cog mode. '
            'The convex-hull support disk is valid only for sheet-boundary constraints and must never replace the concave cog in collision checks. '
            'Independently audit the new model before a separately declared bounded call. Do not retry or extend the completed 16-gon call, merely change its seed, or release more fixed owners to evade the newly proved conflicts. '
            'Any positive still requires actual original outlines and angles, clearance and native guards, the production budget and the full 13-job/two-kerf matrix. '
            'H2 remains open without held-out access; this diagnostic does not qualify a release. The six accumulated checkpoints are already on main; follow CI 40237436741 separately before the next periodic push.')
    OUT.mkdir()
    copies={'plan.json':'domain-plan.json','result.json':'domain-result.json','audit/checks.json':'domain-audit.json',
        'solve/plan.json':'solver-plan.json','solve/model-audit.json':'model-audit.json','solve/result.json':'solver-result.json',
        'solve/positions.json':'selected-positions.json','solution-audit/checks.json':'solution-audit.json',
        'solution-audit/original-pair-failures.json':'original-pair-failures.json','solution-audit/original-stock-failures.json':'original-stock-failures.json',
        'solution-audit/angle-independent-cog-conflicts.json':'angle-independent-cog-conflicts.json',
        'stronger-cog-conditions/certificate.json':'stronger-cog-certificate.json',
        'stronger-cog-conditions/audit/checks.json':'stronger-cog-audit.json','main-ci-final-snapshot.json':'main-ci-snapshot.json'}
    for name,dest in copies.items():shutil.copyfile(BASE/name,OUT/dest)
    shutil.copyfile(SYNC/'receipt.json',OUT/'main-push-receipt.json')
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,
        'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
        'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,
        'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,
        'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,
        'normal_pushed_checkpoints':6,'current_main_ci_id':40237436741,'current_main_ci_status':ci['status'],
        'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'next_investigation':action})
    members={};inputs={}
    for root in [BASE,SYNC]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for key in ['inputs','input_hashes']:
            for name,h in load(p).get(key,{}).items():
                if name in inputs:assert inputs[name]==h
                inputs[name]=h
    for row in load(BASE/'audit/provenance.json'):
        for name,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            if name in inputs:assert inputs[name]==h
            inputs[name]=h
    for row in load(BASE/'cache-references.json'):inputs[row['source']]=row['sha256']
    for name,h in inputs.items():
        p=ROOT/name;assert digest(p)==h;members['source-inputs/'+name]=p
    pending=[ROOT/'output'/n for n in ['build_h5_conflict_owner_neighborhood.py','audit_h5_conflict_owner_neighborhood.py',
        'solve_h5_conflict_owner_neighborhood.py','audit_h5_conflict_owner_model.py','audit_h5_conflict_owner_solution.py',
        'prepare_h5_exact_disk_and_stock_bounds.py','audit_h5_exact_disk_and_stock_bounds.py',
        'push_h5_strong_pair_checkpoint.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
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
    write(OUT/'checks.json',{'passed':True,'all20_original_stock_queries_complete':True,'all199_convex_domains_and3638_halfplanes_audited':True,
        'all361_component_minkowski_hulls_and2032_facets_verified':True,'all1871_variables_and10774_constraints_reconstructed':True,
        'all66_required_originals_retained':True,'one_bounded_necessary_model_solution_independently_checked':True,
        'invalid_original_trial_and_all_failures_preserved':True,'five_angle_independent_pair_conflicts_and_three_stock_anchors_rejected':True,
        'all15_source_cog_centers_preserved_by_stronger_stock_bounds':True,'six_previous_checkpoints_normal_pushed_to_main':True,
        'new_main_ci_success_claimed':ci['conclusion']=='success','production_source_and_readmes_unchanged':True,
        'full_target_witness':False,'native_margin_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: nine-part conflict-owner neighborhood — 2026-10-25

**The broader search finds all 66 required parts in its necessary geometric
model, but the original-outline trial fails.** Independent checks identify five
cog-pair conflicts that no angle can repair at the selected anchors. Stronger
whole-circle and sheet-boundary conditions are now certified for the next model.
H2/H5 remain open at **60%** completed milestone weight.

## Fresh complete geometry

The released originals are items **50, 54, 57, 58, 62, 64 and 65**: one vertical
insert and six cogs. With both missing brackets, the model moves nine mandatory
parts and preserves 57 original source transforms. Counts remain 18 frames,
12 brackets, 21 inserts and 15 cogs. Every allowed orientation and sheet from
the recorded source inventory remains available.

All **20 mode/sheet queries** start from full original stock anchor bounds.
None uses the earlier two-core free cells. The construction reuses 100 immutable
collision-cache entries and adds 10 for the vertical insert. Only strict
interior collision regions are excluded. Complete free regions, including
boundary cases, receive outward padding before complete convex decomposition
and rational outward inequality rounding.

Construction takes **{generation['seconds']:.6f} seconds**, producing **199 convex
domains** without pending work or caps. Independent verification takes
**{audit['seconds']:.6f} seconds** and checks:

- 112 inputs against committed evidence, all 57 fixed transforms and all counts.
- 16 exact insert floor-error corner tests and 106 independently built triangle
  collision hulls for its 10 new cache entries.
- Whole-stock coverage for every query, **3,638 outward halfplanes** and
  **82,650 rational vertex tests**.
- All seven released source poses, and **361 exact component Minkowski hulls**
  with all **2,032 facets** represented by the 20-normal separation basis.

The minimum new exclusion margin is {audit['minimum_new_exclusion_interior_margin_mm']:.12f} mm;
the nominal 0.001 mm erosion is not claimed as its exact realized margin.

## One bounded search and a rejected original trial

The joint model contains **1,871 variables and 10,774 constraints**: 46 mode
choices, 482 complete per-part domain choices, 8,283 reified halfplanes,
36 physical pairs and 53 convex-component pairs. All 1,060 exact projection
separation choices are present. Original area charges and original outward
stock bounds remain. There is no objective, hint, copy ordering or optional
original part. A separate protobuf oracle checks every variable, constraint
and solver parameter before search.

One declared 60-second, eight-worker, seed-zero call returns **OPTIMAL in
{solved['seconds']:.6f} seconds**, with an incumbent at
{solved['incumbents'][0]['seconds']:.6f} seconds. Here OPTIMAL means a feasible
necessary-model arrangement; there is no packing objective. The completed call
is not retried or extended.

An independent solution audit verifies all 66 copies, nine selected domains,
25 same-sheet moving-component separations and original area charges of
**4,091,952,616 / 389,788,154** units across the two sheets (1,000 units/mm²).
The outward fixed-obstacle relaxation permits two tiny proxy intersections;
these are recorded explicitly, not described as physical feasibility.

The full original-outline trial preserves all 57 fixed transforms, uses the
selected bracket/insert orientations and each restored cog's source angle.
Checking all **1,585 original pairs** finds **17 clearance failures** and
**three stock-boundary failures**. Its three largest stock overruns are about
28.97, 30.87 and 23.12 mm. The rejected file and every failure remain preserved.
It is not sent to native packing as an accepted candidate.

## Stronger cog conditions, independently certified

The original cog contains a disk of radius **109.1157 mm** at every angle.
A whole circle of radius **109.1 mm** about its floored center remains inside
that disk for every floor error: in 0.0001 mm units,
`(1091157 − 1091000)² > 2 × 100²`. Exact circle distances reject three selected
moving-cog pairs; rational point-to-original distances reject two further
moving-cog/fixed-original pairs. These account for all five robust conflicts.

Separately, the original's convex hull has **40 vertices**. All 3,200 original
point/halfplane checks establish a centered hull disk with radius
**139.2707 mm**. This supplies a necessary minimum stock-boundary support at
every angle. It is used **only for sheet boundaries**, never as a filled
collision proxy for the concave cog.

The stronger stock-center bounds are `[14576, 14576, 135424, 285424]` and
`[14576, 14576, 135424, 18017]` in 0.01 mm units. They preserve **all 15 known
valid source cog centers** and reject all three out-of-bounds selected cog
anchors at every angle. Preparation and independent verification take
{load(BASE/'stronger-cog-conditions/checks.json')['seconds']:.6f} and
{strong['seconds']:.6f} seconds respectively. No further solver call occurs in
this checkpoint.

Next, strengthen the nine-part model using these certified conditions while
preserving its complete original counts, material cap and allowed modes. Any
linear approximation of the whole circle must be identified and audited as
such. A positive still needs actual original outlines and angles, clearance
and native guards, the production budget and the full 13-job/two-kerf matrix.
Neither this rejected trial nor a conditional negative proves unrestricted
packing impossibility.

## Repository and evidence

The previous six checkpoints were normally pushed to main **51fe56c0**, and
the remote head was verified. New [CI 40237436741]({ci['url']}) is
**{ci['status']}**, with **{success}/6** jobs successful in the saved snapshot.
Its status is separate from the older six-job successful run. Production source,
all three accurate READMEs and release versions remain unchanged. There is no
held-out evaluation, full quality rerun, native acceptance or new release.

Evidence: [domain audit]({NAME}/domain-audit.json),
[model audit]({NAME}/model-audit.json), [bounded result]({NAME}/solver-result.json),
[solution audit]({NAME}/solution-audit.json),
[stronger certificate]({NAME}/stronger-cog-certificate.json),
[independent certificate audit]({NAME}/stronger-cog-audit.json),
[push receipt]({NAME}/main-push-receipt.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']}** canonical members and
**{archive['verified_aliases']}** identical-content aliases retain exact bytes
with CRC/SHA-256 verification, including all domains, model/log, rejected trial,
source inputs, certificates and executed helpers.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 complete conflict-owner neighborhood, 2026-10-25:**
[The evidence]({link}) restores seven originals and both missing brackets with
57 source transforms fixed, retaining all 66 required parts. All 20 original-stock
queries complete with 199 convex domains; independent checks cover 3,638 outward
halfplanes, 82,650 rational vertex tests and 361 component Minkowski hulls.
The fully audited 1,871-variable/10,774-constraint model finds a necessary-model
arrangement in 1.133719 seconds. Its original-outline trial fails 17 clearance
checks and three stock bounds; all failures are preserved. Exact 109.1 mm whole
circles reject five selected cog conflicts, and a separately certified 139.2707 mm
all-angle stock support rejects three anchors while retaining all 15 valid source
cog centers. The hull support is not used as filled collision geometry. These
conditions prepare the next stronger model; no completed call is retried.
The previous six checkpoints are on main 51fe56c0; its new CI remains separate
from the prior successful run. No accepted target, native qualification or H5
completion is claimed. Source, accurate READMEs and releases stay unchanged;
H2/H5 remain open at 60% completed milestone weight.
'''
    for name in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/name,note.format(link=('' if name=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'production_digest':source_digest(),'main_ci_status':ci['status'],'main_ci_successful_jobs':success},flush=True)

if __name__=='__main__':main()
