"""Seal full convex pair refinement, exact clearance proofs and capacity limits."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-convex-domain-conflicts-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
THREE=ROOT/'output/h5-three-region-master-20261025';LAST=ROOT/'output/h5-second-sheet-capacity-master-20261025'
OLD=ROOT/'output/h5-original-domain-conflicts-20261025';SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    build=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');groups=load(BASE/'groups/result.json')
    pair=load(BASE/'second-sheet-pair-proofs/result.json');pa=load(BASE/'second-sheet-pair-proofs/audit/checks.json');cap=load(BASE/'second-sheet-pair-proofs/audit/capacity-certificate.json')
    assert build['unmarked_pairs_tested']==2996279 and build['new_convex_conflicts']==108041 and build['certified_conflicts']==5561575 and not load(BASE/'pending-cases.json')
    audits=[BASE/p for p in ['audit/checks.json','groups/audit/checks.json','solve/model-audit.json','selection-audit/checks.json','anchor-solve/model-audit.json','domain-core/model-audit.json','integer-conflict-proof/audit/checks.json','second-sheet-pair-proofs/audit/checks.json']]
    audits += [r/p for r in [THREE,LAST] for p in ['solve/model-audit.json','selection-audit/checks.json']]+[LAST/'anchor-solve/model-audit.json',LAST/'selection-audit/second-sheet-check.json']
    assert all(load(p)['passed'] for p in audits)
    assert load(THREE/'selection-audit/checks.json')['new_whole_convex_domain_conflicts']==1
    assert all(load(r/'solve/result.json')['status']=='OPTIMAL' for r in [THREE,BASE,LAST])
    assert all(load(r/'anchor-solve/result.json')['status']=='INFEASIBLE' for r in [BASE,LAST])
    assert load(BASE/'integer-conflict-proof/audit/checks.json')['verified_selected_domain_core_parts']==[6,8]
    assert pair['proved_conflicts']==32 and pair['fixed_points']==19 and pair['pending_pairs']==0 and cap['maximum_cog_occupancy']==2
    oldreview=load(ROOT/'benchmarks/results/h5-original-domain-conflicts-20261025/source-review.json')
    assert source_digest()==oldreview['production_digest'] and all(digest(ROOT/n)==h for n,h in oldreview['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('300a97b4') and mainhead=='4f359ff7b4c5642c92fb0df26744934395627a42'
    ci=json.loads(subprocess.check_output(['gh','run','view','40240715636','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==mainhead
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Keep every completed bounded call closed. The full refined pair table and global three-region clause are independently audited; '
        'the32 additional ordered second-sheet pair exclusions have exact independent interval replays and the global query19 occupancy is at most2. '
        'The latest master includes all480 physical uses of those pair exclusions and the capacity bound, but its selected coordinate model is still INFEASIBLE. '
        'It assigns five cogs to query18 domain row79 (raw index81) and the sixth to row190 (raw index192); pair compatibility alone cannot impose regional capacity. '
        'Next construct independently certified occupancy limits for large individual first-sheet domains and, if useful, unions of spatially overlapping domains. '
        'Use the proved original no-fit disk and exact whole-domain geometry to bound simultaneous centres; never treat sampled positions, an outer cog hull, an unchecked solver core or a fixed point as proof. '
        'Apply each certified bound to all six interchangeable cogs, preserving all9776 domain choices, original66 counts, original sheet charges and existing original-shape constraints. '
        'Independently audit every new constraint before a separately declared bounded search, preferably with a shared master/coordinate budget rather than unbounded retries. '
        'Any positive still needs full original-coordinate, polygon/stock and native validation, then production-budget integration and the full13-job/two-kerf H5 matrix. '
        'H2 remains open under Artem\'s unchanged-denominator decision; all22 reserved vectors remain untouched. Main CI40240715636 remains separately tracked before another normal push. No new release is qualified.')
    OUT.mkdir()
    copies={
        BASE:{'plan.json':'convex-plan.json','result.json':'convex-result.json','audit/checks.json':'convex-audit.json','groups/result.json':'group-result.json','groups/audit/checks.json':'group-audit.json',
            'solve/model-audit.json':'convex-master-audit.json','solve/result.json':'convex-master-result.json','selection-audit/checks.json':'convex-selection-audit.json','anchor-solve/model-audit.json':'convex-anchor-audit.json','anchor-solve/result.json':'convex-anchor-result.json',
            'domain-core/result.json':'solver-core-result.json','integer-conflict-proof/result.json':'exact-interval-result.json','integer-conflict-proof/audit/checks.json':'exact-interval-audit.json',
            'second-sheet-pair-proofs/result.json':'second-sheet-pair-result.json','second-sheet-pair-proofs/audit/checks.json':'second-sheet-pair-audit.json','second-sheet-pair-proofs/audit/certified-pair-exclusions.json':'second-sheet-pair-exclusions.json',
            'second-sheet-pair-proofs/audit/capacity-certificate.json':'second-sheet-capacity-certificate.json','main-ci-snapshot.json':'main-ci-snapshot.json'},
        THREE:{'solve/model-audit.json':'three-region-master-audit.json','solve/result.json':'three-region-master-result.json','selection-audit/checks.json':'three-region-selection-audit.json','selection-audit/new-convex-domain-conflicts.json':'three-region-failed-pair.json'},
        LAST:{'solve/model-audit.json':'capacity-master-audit.json','solve/result.json':'capacity-master-result.json','solve/selection.json':'capacity-master-selection.json','selection-audit/checks.json':'capacity-selection-audit.json','selection-audit/second-sheet-check.json':'capacity-selection-check.json','anchor-solve/model-audit.json':'capacity-anchor-audit.json','anchor-solve/result.json':'capacity-anchor-result.json'}}
    for root,names in copies.items():
        for source,dest in names.items():shutil.copyfile(root/source,OUT/dest)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),
        'current_readmes':oldreview['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,
        'master_solver_calls':3,'selected_anchor_solver_calls':2,'assumption_core_diagnostic_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
        'original_counts_material_gate_and_native_guards_unchanged':True,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'current_main_ci_id':40240715636,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for root in [THREE,BASE,LAST]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
        for p in root.rglob('plan.json'):
            for key in ['inputs','input_hashes']:
                for n,h in load(p).get(key,{}).items():
                    if n in inputs:assert inputs[n]==h
                    inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    plan=load(BASE/'plan.json')
    for key,folder in [('query_hashes','queries'),('mutual_hashes','mutual')]:
        for i,h in plan[key].items():
            p=SOURCE/folder/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for i,h in plan['source_core_hashes'].items():
        p=OLD/'cores'/f'{int(i):03d}.json';assert digest(p)==h;members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for i,hashes in plan['source_case_hashes'].items():
        for k,ext in [('metadata','json'),('packed','bin')]:
            p=OLD/'cases'/f'{int(i):03d}.{ext}';assert digest(p)==hashes[k];members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    for p in (OLD/'three-cog-certificate').rglob('*'):
        if p.is_file():members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['audit_h5_three_region_master.py','prepare_h5_three_region_master.py','solve_h5_three_region_master.py','prepare_h5_three_region_followups.py','audit_h5_three_region_selection.py',
        'build_h5_convex_domain_conflicts.py','audit_h5_convex_domain_conflicts.py','prepare_h5_convex_domain_followups.py','prepare_h5_convex_domain_groups.py','audit_h5_convex_domain_groups.py',
        'solve_h5_convex_domain_master.py','audit_h5_convex_domain_selection.py','solve_h5_convex_domain_anchors.py','prepare_h5_convex_core.py','extract_h5_convex_domain_core.py',
        'prepare_h5_convex_interval_proof.py','prove_h5_convex_selected_conflict.py','audit_h5_convex_selected_proof.py','prove_h5_second_sheet_domain_pairs.py','audit_h5_second_sheet_domain_pairs.py',
        'prepare_h5_second_sheet_master.py','audit_h5_second_sheet_master.py','solve_h5_second_sheet_master.py','audit_h5_second_sheet_selection.py','solve_h5_second_sheet_anchors.py',
        'solve_h5_domain_selection.py','audit_h5_selected_original_domains.py','solve_h5_selected_anchors.py','extract_h5_selected_domain_core.py','prove_h5_selected_domain_conflict.py','audit_h5_selected_domain_proof.py',
        'prepare_h5_domain_conflict_groups.py','audit_h5_domain_conflict_groups.py','pack_h5_evidence_archive.py','ccd1.py']
    pending=[ROOT/'output'/n for n in names];seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p);members['helpers/'+p.name]=p
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            mods=([node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [])
            for mod in mods:
                q=ROOT/'output'/(mod+'.py')
                if q.is_file():pending.append(q)
    archive,manifest=pack(ROOT,OUT,NAME,members)
    write(OUT/'checks.json',{'passed':True,'all2996279_remaining_pairs_scanned':True,'all108041_added_convex_exclusions_independently_verified':True,
        'all5561575_total_pair_exclusions_preserved':True,'all_three_master_and_two_coordinate_models_independently_reconstructed':True,
        'failed_selections_and_all_completed_solver_calls_preserved':True,'exact_selected_pair_proof_replayed':True,'all51_second_sheet_pair_proofs_replayed':True,
        'all32_constructive_pair_exclusions_and_global_capacity_two_verified':True,'production_source_and_readmes_unchanged':True,'main_ci_not_claimed_complete':ci['status']!='completed',
        'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: complete convex conflicts and second-sheet capacity — 2026-10-25

**The complete region-pair table gains 108,041 independently verified original-shape
collision exclusions. Exact integer proofs add 32 guarded-construction exclusions
on the second sheet, and a separate geometric proof limits that sheet to two moving
cogs.** All six cogs and all 66 original parts remain mandatory. No complete target
layout is found; H2/H5 remain open at **60%** completed milestone weight.

## Full refinement after the first three-region search

The previous exact three-region certificate is implemented across all six cogs,
retaining all 9,776 domain choices, original area charges and complete pair table.
Its independently reconstructed 13,439-variable/8,264-constraint master returns a
necessary assignment in **{load(THREE/'solve/result.json')['seconds']:.6f} seconds**.
The independent selected-domain check finds a whole-region bracket/cog collision
that bounding rectangles did not exclude: parts 0/8, items 28/65, query-pair case79,
domain rows 0/31. The complete convex difference lies strictly inside the original
collision core with about **0.599956 mm** interior margin. No anchor/native call
is made for this known invalid assignment.

The next construction scans **all 2,996,279 previously unmarked entries** of the
8,449,813-pair census, across all 164 unique query cases. Every difference of
actual inset-face vertices contributes to a complete convex difference hull,
which is padded by 0.00001 mm. A new exclusion requires the whole padded hull to
lie strictly inside the already verified raw-original collision core. This
adds **108,041** exclusions in **{build['seconds']:.6f} seconds**, for **5,561,575**
total exclusions, retaining every old bit and leaving no pending pairs.

The independent **{audit['seconds']:.6f}-second** audit uses a different enclosure:
exact rational coordinates become outward integer nanometre vertex boxes; all
four corners of every B-box-minus-A-box enter a complete hull. Every new positive
is checked against the certified original core. It checks **11,834** vertex boxes,
102 committed source files, all matrix hashes/order/padding and all old exclusions.
An unmarked pair is never asserted feasible.

Lossless grouping preserves **24,091,856 physical pair exclusions** in **4,491**
group constraints, using 1,444 unique row groups. The complete bitwise and Boolean
audit passes. The three-region constraint remains present.

## Complete coordinate rejection and exact replay

The refined master has **13,238 variables / 7,974 constraints**, all original
9,776 domain choices and no packing objective. One declared 60-second call finds
a necessary assignment in **{load(BASE/'solve/result.json')['seconds']:.6f} seconds**.
OPTIMAL here means satisfaction only. All 18 selected same-sheet pairs pass the
stored exclusions and 4,272 exact convex-enclosure halfplane checks.

Its full original-coordinate model keeps all 617 forbidden pieces: exact integer
bounds prove 517 already separated, leaving 100 disjunctions plus 36 inward
halfplanes. The independently rebuilt 2,799-variable/2,917-constraint model returns
**INFEASIBLE in {load(BASE/'anchor-solve/result.json')['seconds']:.6f} seconds**.

A separate audited 10-second assumption diagnostic identifies parts 7/8. An
independent exact-integer propagation proof instead establishes the equivalent
same-domain conflict for parts 6/8 (items 62/65): query19 domain rows 1/29.
Its **96** updates across 20 passes end in an empty integer interval; independent
replay reconstructs every inward inequality, all 617 complete original forbidden
clauses, each unit inference and exact rounding step. This is a proof for the
declared guarded integer construction, without relying on the solver's core.

## All unresolved second-sheet pairs and global capacity

The second-sheet raw-original table excludes 973 of 1,024 ordered domain pairs.
A separately declared shared 60-second exact-proof pass examines all **51** other
pairs using both full inward domains and every guarded original forbidden piece.
It finishes in **{pair['seconds']:.6f} seconds**, proving **32** contradictions and
retaining **19 fixed points as non-proofs**. No pair is pending or capped.
Independent rational replay verifies all **1,920** interval events.

The union of all 32 second-sheet domain boxes lies within integer anchor bounds
`{cap['whole_all32_domain_box_units1000']}` in micrometres. Its width is 258.822 mm
and height 32.949 mm. Among three sorted integer x coordinates, one adjacent gap
is at most 129.411 mm. Even using the full height, that pair's maximum squared
distance is **{cap['adjacent_pair_maximum_squared_distance_units']} micrometres²**,
strictly below **{cap['raw_original_required_squared_distance_units']}**, required by
the previously independently proved 258.082 mm original cog/cog no-fit disk.
Therefore **at most two** of the six moving cogs can select the second sheet.
This covers every domain and copy, and does not depend on a solver result.

## Latest bounded master and remaining limitation

The next independently reconstructed master retains the complete refined table,
the global three-region exclusion, all **480** physical uses of the 32 new
ordered pair exclusions, and the global second-sheet capacity of two. Its
**13,238 variables / 8,455 constraints** retain all original counts and charges.
One declared 60-second call returns a necessary assignment in
**{load(LAST/'solve/result.json')['seconds']:.6f} seconds**. It passes all new exclusions,
the capacity audit and 4,990 exact selected-domain enclosure checks.

The complete selected coordinate model has 2,105 variables / 2,242 constraints:
1,277 original forbidden pieces, 1,157 exactly proved already separated, 120
remaining complete disjunctions and 35 inward halfplanes. Its one declared call
returns **INFEASIBLE in {load(LAST/'anchor-solve/result.json')['seconds']:.6f} seconds**.
The assignment puts five cogs in first-sheet query18 domain row79 and the sixth
in row190. Pairwise compatibility does not bound simultaneous regional occupancy.
Next investigate independently certified capacities for these large domains and
useful region unions across all cog copies. Every completed call remains closed.

No unrestricted packing impossibility, complete target, native acceptance or H5
success follows from these restricted negatives. A complete valid layout still
needs original-polygon/stock checks, native validation, production-budget integration
and the full 13-job/two-kerf H5 matrix. No held-out vectors are evaluated.

## Repository and retained evidence

Production digest and all three READMEs remain unchanged and accurate. The preview
stays v0.2.0-alpha.1, stable Latest stays v0.1.0, and no new release is qualified.
Main remains **4f359ff7** after the previously documented four-commit normal push.
Its own [CI40240715636]({ci['url']}) is **{ci['status']}**, with **{success}/6** successful
jobs in the retained snapshot. This checkpoint claims no result for unfinished jobs.

Evidence includes [full convex audit]({NAME}/convex-audit.json),
[exact replay]({NAME}/exact-interval-audit.json),
[all second-sheet proofs]({NAME}/second-sheet-pair-audit.json),
[capacity certificate]({NAME}/second-sheet-capacity-certificate.json),
[latest master audit]({NAME}/capacity-master-audit.json),
[latest coordinate result]({NAME}/capacity-anchor-result.json),
[archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
The archive retains **{archive['archive_members']}** canonical files and
**{archive['verified_aliases']}** identical-content aliases with byte/hash/CRC checks,
including all matrices, original inputs, models, logs, failed selections and proof events.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 complete convex conflicts and second-sheet capacity, 2026-10-25:**
[The evidence]({link}) scans all 2,996,279 pairs left open by the box table and
independently verifies 108,041 additional whole-convex original-shape exclusions.
The complete table now has 5,561,575 exclusions, represented losslessly as
24,091,856 physical exclusions. A first three-region assignment is rejected by
a whole-convex bracket/cog collision. The refined master finds a necessary
assignment, but its full original-coordinate model is INFEASIBLE. Exact replay
then proves a second-sheet pair conflict independently of the solver core.
All 51 unresolved second-sheet pairs receive bounded exact interval checks:
32 conflicts are proved, 19 fixed points stay non-proofs, and all 1,920 events
are independently replayed. A separate original no-fit-disk argument proves
that at most two moving cogs fit the complete second-sheet region inventory.
The next master includes all 480 physical new pair clauses and this capacity;
its coordinate check still fails, having placed five cogs in one first-sheet
domain. Next derive independently certified regional occupancy limits across
all six copies. All original counts, material limits and native guards remain
unchanged; no complete target, native call, quality run or release is claimed.
Main CI40240715636 has {success}/6 successful jobs and remains {status} in the
saved snapshot. Accurate READMEs remain unchanged. H2/H5 remain open at 60%.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md',success=success,status=ci['status']))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'main_ci_status':ci['status'],'main_ci_successes':success,'production_digest':source_digest()},flush=True)
if __name__=='__main__':main()
