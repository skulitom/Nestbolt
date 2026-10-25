"""Seal complete pair coverage, full proxy solution and rejected original lift."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-pair-core-relocation-and-outline-diagnosis-20261025'
OUT=ROOT/'benchmarks/results'/NAME;BASE=ROOT/'output/h5-pair-core-relocation-regions-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)

def main():
    generation=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');model=load(BASE/'solve/model-audit.json')
    solved=load(BASE/'solve/result.json');lift=load(BASE/'solution-audit/checks.json')
    assert all(x['passed'] for x in [audit,model,lift])
    assert generation['cases_completed']==528 and generation['queries_completed']==9984
    assert not generation['stop_reason'] and not generation['cell_cap_reached'] and not load(BASE/'pending.json')
    assert (audit['excluded_cases'],audit['surviving_cases'],audit['surviving_allocations'])==(299,229,424)
    assert solved['status']=='OPTIMAL' and solved['solver_calls']==1 and len(solved['incumbents'])==1 and solved['has_full_proxy_solution']
    assert lift['full_proxy_solution_verified'] and lift['proxy_original_parts']==66 and not lift['original_outline_trial_valid']
    assert (lift['original_outline_trial_pair_failures'],lift['original_outline_trial_stock_failures'],lift['robust_angle_independent_cog_conflicts'])==(7,2,2)
    prior=load(ROOT/'benchmarks/results/h5-single-core-relocation-exclusion-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('c584bc7c') and mainhead.startswith('247e823a')
    ci=load(BASE/'repository-sync/main-ci.json');assert ci['headSha']==mainhead
    action='The complete pair census and its one bounded solver call are finished. Preserve the full 66-part proxy solution and rejected original-outline lift; do not rerun or extend that unchanged model. The two robust disk conflicts show the five-rectangle proxy omits necessary collision geometry. Next audit a stronger necessary geometry construction around the same 62 fixed original transforms: actual filled outer polygons for fixed parts, existing floor-safe rectangle components for movable brackets/frames, and an independently certified floor-safe inscribed polygon for each movable cog, valid at every cog angle and every coordinate-floor error. First independently prove each proxy is a subset of its original over the full floor-error square, and verify it rejects the selected false anchors. Then declare bounded complete zero-clearance configuration-space regions for all 229 area-surviving pairs, retaining all 424 allowed allocations and all 66 parts. Any forbidden-region approximation must be inward/conservative and its free-region cover outward. Preserve caps and pending cases rather than infer negatives from unfinished work. Independently audit coverage before a separately declared new bounded model. A positive still needs complete original shapes, original clearance/native guards, production budget and the full 13-job/two-kerf matrix. H2 stays open; no reserved vectors or new release. Poll main CI40233299884 and push accumulated evidence normally after it is terminal.'
    OUT.mkdir()
    copies={'plan.json':'region-plan.json','result.json':'region-result.json','audit/checks.json':'region-audit.json',
            'audit/surviving-neighborhoods.json':'surviving-neighborhoods.json','solve/plan.json':'solver-plan.json',
            'solve/model-audit.json':'model-audit.json','solve/result.json':'solver-result.json','solve/positions.json':'proxy-solution.json',
            'solution-audit/checks.json':'solution-audit.json','solution-audit/original-pair-failures.json':'original-pair-failures.json',
            'solution-audit/original-stock-failures.json':'original-stock-failures.json',
            'solution-audit/angle-independent-cog-conflicts.json':'angle-independent-cog-conflicts.json'}
    for rel,name in copies.items():shutil.copyfile(BASE/rel,OUT/name)
    write(OUT/'main-ci.json',ci);write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,
          'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,
          'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,
          'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','solver_calls':1,'native_packing_calls':0,
          'quality_runs':0,'held_out_files_evaluated':0,'full_proxy_solution_verified':True,
          'full_target_witness':False,'native_margin_qualified':False,'current_main_ci_id':40233299884,'next_investigation':action})
    members={BASE.name+'/'+p.relative_to(BASE).as_posix():p for p in BASE.rglob('*') if p.is_file()};inputs={}
    for p in BASE.rglob('plan.json'):
        for n,h in load(p).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    provenance=load(BASE/'audit/provenance.json')['source_members_matching_committed_evidence']
    manifestpath=ROOT/'benchmarks/results/h5-source-inventory-and-proxy-slot-coverage-20261025/raw-manifest.json'
    mf=load(manifestpath);files=mf['files']+mf['aliases']
    sourcepath=ROOT/load(ROOT/'output/h5-source-orientation-construction-20261025/plan.json')['hint_source']
    for p in [sourcepath,ROOT/'output/h5-coordinated-placement-selection-20261018/job.json',ROOT/'output/h5-cog-center-capacity-20261020/disk.json']:
        matches=[r for r in files if r['sha256']==digest(p)];assert matches,p
        provenance.append({'source':p.relative_to(ROOT).as_posix(),'sha256':digest(p),'manifest':manifestpath.relative_to(ROOT).as_posix(),
                           'manifest_sha256':digest(manifestpath),'member':matches[0]['path']})
    for row in provenance:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    write(OUT/'source-provenance.json',provenance)
    pending=[ROOT/'output'/n for n in ['build_h5_pair_core_relocation_regions.py','audit_h5_pair_core_relocation_regions.py',
             'solve_h5_pair_core_neighborhoods.py','audit_h5_pair_core_model.py','audit_h5_pair_core_solution.py','prepare_h5_pair_ci_snapshot.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
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
    checks={'passed':True,'all528_pairs_and9984_queries_complete':True,'nothing_capped_or_pending':True,
            'all130183_integer_cells_and53424_allocation_inequalities_audited':True,
            'all229_survivors_and424_allocations_in_one_audited_model':True,
            'all73266_variables141477_constraints_and_parameters_reconstructed':True,
            'one_bounded_call_found_full66_proxy_solution':True,'full66_proxy_solution_independently_verified':True,
            'original_outline_lift_failed_and_preserved':True,'two_angle_independent_cog_conflicts_verified':True,
            'only_selected_false_anchors_rejected_not_entire_cells':True,'unrestricted_infeasibility_claimed':False,
            'production_source_and_readmes_unchanged':True,'full_target_witness':False,'native_margin_qualified':False,
            'H5_complete':False,'completion_percent':60,**archive}
    write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: pair relocation and original-outline diagnosis — 2026-10-25

**Moving two cogs yields all 66 parts in the simplified proxy model, but the
original-outline lift fails.** Two collisions remain unavoidable at the selected
cog-center coordinates even allowing every angle and the full coordinate-floor
uncertainty. Stronger necessary collision geometry is required. H2/H5 remain
open at **60%** completed milestone weight; no original target witness is claimed.

## Complete pair census

All 528 unordered pairs of the 18 frames and 15 cogs are considered. Each case
keeps 62 source poses fixed, restores both released originals, and adds both
missing brackets: all 66 counts remain mandatory. Frames retain their finite
source horizontal-orientation inventory. Cogs use the all-angle five-rectangle
inner proxy; both extra brackets keep every original orientation/reflection.
Material bounds and full original area charges remain unchanged.

All 9,984 queries complete in **{generation['seconds']:.6f} seconds** under the
declared 120-second limit and 500,000-cell cap. There are 130,183 complete
inclusive integer free cells, including touching boundaries and isolated grid
rows, with nothing capped or pending. Swept component rectangles give outward
occupied covers. Exact union-area bounds apply to all seven nonempty role
subsets on each sheet for every allowed allocation, alongside original-area
capacity. Proxy coordinate-squared areas and original area units stay separate.

The independent audit takes **{audit['seconds']:.6f} seconds** and verifies:

| Check | Count |
| --- | ---: |
| Independently reconstructed integer collision rectangles | 1,320,690 |
| Critical cells checked with two-dimensional difference arrays | 115,212,526 |
| Mode/anchor combinations covered | 173,927,689,353,312 |
| Free mode/anchor combinations | 943,680,836,601 |
| Reconstructed outward occupied rectangles | 339,163 |
| Original released source poses still covered | 1,056 |
| Exact allocation inequalities | 53,424 |

The area oracle uses two-dimensional arrays independently of construction's
interval sweep. Necessary bounds exclude **299 cases**, leaving **229 cases
and 424 sheet allocations**. Area survival alone is not a layout.

## Joint model and independently verified proxy solution

One model includes every surviving case and allocation. Four shared part
positions represent both restored originals and both extra brackets. Each
selects a complete free cell from the same chosen case. Sheet links enforce
the allocation; all components share their part's position and orientation.
Up to 14 inner rectangles use two NoOverlap2D constraints and 56 optional
intervals. Absent frame arms have no active intervals. There are no optional
original parts, hints, objectives, copy orders or sampled candidate subsets.

Construction takes **{model['construction_seconds']:.6f} seconds**. A separate
protobuf oracle reconstructs every field of **73,266 variables and 141,477
constraints**, all 4,770 role/mode options and 67,649 complete-cell options,
component/sheet presence, intervals, original-area bounds and parameters in
**{model['audit_seconds']:.6f} seconds**. It also checks 8,300 within-part
component pairs and the complete presence/sheet truth tables.

One declared 60-second, eight-worker, seed-zero call starts search at 4.26
seconds. It finds an arrangement at **7.658665 seconds** and returns
**OPTIMAL in {solved['seconds']:.6f} seconds**, with 2,842 branches and 92
conflicts. This is feasibility without an objective; OPTIMAL does not mean
optimal material use or cutting performance.

Case **506** moves cog items **58 and 65**, restoring one cog and adding one
bracket to each sheet. Independent reconstruction verifies all 66 unique copies,
62 unchanged source transforms, four selected cells, 138 inner rectangles and
6,456 same-sheet component pairs. Original area charges are 4,091,952,616 and
389,788,154 in the audited 1,000-units/mm² system, both within capacity. The
solution audit and diagnosis take **{lift['seconds']:.6f} seconds**.

## Rejected original-outline lift

One explicit trial preserves all 62 source transforms, uses the selected
bracket orientations at grid lower-corner anchors, and restores cogs at their
selected center anchors with source angles. Only copy labels are reassigned
to the complete inventory. All 1,585 same-sheet original polygon pairs and
every stock boundary are checked. **Seven overlapping part pairs and two stock
failures** involve moved/added parts. The complete trial and failures remain.

This trial does not exhaust cog angles or floor phases. A separate necessary
disk check finds cog 65's center anchor 82.025650 mm from fixed cog 57 and
60.638928 mm from fixed cog 62. Every original cog angle contains the previously
certified disk of radius 109.1157 mm. A floor-cell center shift is at most
sqrt(2) × 0.01 mm. Even after that entire uncertainty, collision margins remain
**27.075908 mm and 48.462630 mm**. Changing the angle or floor phase cannot fix
these selected coordinates. Other coordinates in these cells and other
neighborhoods remain unresolved.

No native call is made on an already invalid original-outline trial. There is
no native-margin qualification, production-budget result or full H5 matrix.

## Next work and evidence

{action}

Production source, accurate READMEs and release versions remain unchanged.
Main 247e823a's existing CI40233299884 is captured as `{ci['status']}` /
`{ci['conclusion'] or 'pending'}`; unfinished checks are not passes. This
checkpoint starts at {head[:8]}. No held-out file or new release is involved.

The first archival attempt stopped before creating its destination because a
read of this existing CI run hit a transient GitHub connection error. The same
run was re-read successfully and captured separately: five jobs passed while
Windows remained in progress. The failure record, original sealer and recovered
snapshot are preserved. No geometry, audit or solver call was repeated.

Evidence: [region plan]({NAME}/region-plan.json), [complete census]({NAME}/region-result.json),
[region audit]({NAME}/region-audit.json), [model audit]({NAME}/model-audit.json),
[solver result]({NAME}/solver-result.json), [proxy solution]({NAME}/proxy-solution.json),
[solution audit]({NAME}/solution-audit.json), [robust conflicts]({NAME}/angle-independent-cog-conflicts.json),
[source provenance]({NAME}/source-provenance.json), [raw archive]({NAME}/raw-001.zip)
and [manifest]({NAME}/raw-manifest.json). All **{archive['archive_members']}**
canonical members and **{archive['verified_aliases']}** identical-content aliases
retain exact bytes with CRC/SHA-256 verification, including every query,
allocation, complete model/log, original-outline trial and failure.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 complete pair relocation census and outline diagnosis, 2026-10-25:**
[The evidence](../benchmarks/results/{NAME}.md) completes all 528 core-pair
releases and 9,984 mode queries. Independent coverage and 53,424 allocation
inequalities exclude 299 cases; all 229 survivors and 424 allocations enter
one fully audited 73,266-variable/141,477-constraint model. One bounded call
finds a complete 66-part proxy arrangement in 7.952451 seconds. Independent
reconstruction verifies all copies, 138 inner rectangles and 6,456 component
pairs. The original-outline lift fails seven pair and two stock checks. Two
certified-disk conflicts remain after every cog angle and full floor-center
uncertainty, rejecting those selected coordinates. Broader cells and
neighborhoods remain unresolved. Next strengthen necessary collision geometry
against actual fixed original outlines; no unchanged retry or acceptance
reduction. Source, accurate READMEs and releases stay unchanged. No original
target witness or H5 qualification; H2/H5 remain open at 60%.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)

if __name__=='__main__':main()
