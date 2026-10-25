"""Seal complete domain incompatibilities and the independent three-cog exclusion."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-original-domain-conflicts-20261025';BASE=ROOT/'output'/NAME;SOURCE=ROOT/'output/h5-full-original-joint-prepared-20261025';OUT=ROOT/'benchmarks/results'/NAME
SYNC=ROOT/'output/h5-full-original-main-sync-20261025';load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    build=load(BASE/'result.json');audit=load(BASE/'audit/checks.json');groups=load(BASE/'groups/result.json');ga=load(BASE/'groups/audit/checks.json')
    model=load(BASE/'solve/model-audit.json');solved=load(BASE/'solve/result.json');selection=load(BASE/'selection-audit/checks.json')
    am=load(BASE/'anchor-solve/model-audit.json');ar=load(BASE/'anchor-solve/result.json');ip=load(BASE/'integer-conflict-proof/result.json');ia=load(BASE/'integer-conflict-proof/audit/checks.json')
    cm=load(BASE/'domain-core/model-audit.json');cr=load(BASE/'domain-core/result.json');cert=load(BASE/'three-cog-certificate/result.json');ca=load(BASE/'three-cog-certificate/audit/checks.json')
    assert all(r['passed'] for r in [audit,ga,model,selection,am,ia,cm,ca])
    assert build['tested_domain_pairs']==8449813 and build['certified_conflicts']==5453534 and not load(BASE/'pending-cases.json')
    assert solved['status']=='OPTIMAL' and ar['status']=='INFEASIBLE' and cr['status']=='INFEASIBLE' and cr['core_parts']==[3,4,5]
    assert ip['status']=='FIXED_POINT' and cert['excluded_domain_triples']==696 and ca['proved_three_region_occupancy_exclusion']
    prior=load(ROOT/'benchmarks/results/h5-full-original-joint-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    receipt=load(SYNC/'receipt.json');head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head==mainhead==receipt['source_head']=='4f359ff7b4c5642c92fb0df26744934395627a42' and receipt['pushed_commits']==4
    oldci=json.loads(load(SYNC/'prior-ci.json')['stdout']);assert oldci['conclusion']=='success' and len(oldci['jobs'])==6 and all(j['conclusion']=='success' for j in oldci['jobs'])
    ci=json.loads(subprocess.check_output(['gh','run','view','40240715636','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT));assert ci['headSha']==head
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('Use the complete independently audited8,449,813-entry box-conflict census and its lossless1485 row groups as necessary domain propagation. '
        'The first13,436-variable/8,257-constraint master found a domain assignment in8.0949016 seconds, but its fully audited original-coordinate model was INFEASIBLE in0.0307714 seconds. Both calls remain closed. '
        'The ordinary interval replay stopped at a fixed point and proves no contradiction; preserve that limit. A separate gated10-second diagnostic returned core parts3,4,5 (items54,57,58). '
        'The independent three-cog certificate now validates a stronger geometric reason without trusting the core: the raw original same-angle cog/cog no-fit polygon contains a strict258.082mm disk, proved against all228 finite boundary segments. '
        'The original core boxes and their outward5mm-rounded boxes cannot all contain distinct cogs: the B-C distance forces B high enough that A-B cannot separate. '
        'Certificate groups A/B/C contain12/2/29 complete query18 domains, excluding696 domain triples across all six interchangeable moving cogs. '
        'Next add this certified global three-group occupancy exclusion to the master: one occupied Boolean per group is equivalent to at least one selected cog-domain selector in that group, then require at least one of the three groups to be unoccupied. '
        'Apply it across every one of the six moving cogs, not only the labelled core copies; the certificate proves the region x intervals are disjoint. Keep all9776 domain choices, original66 counts, original area charges and other collision constraints. '
        'Independently audit the new protobuf and parameters before any separately declared bounded call. Any new region assignment still needs a complete original-coordinate solve, original polygon/stock checks and native validation. '
        'A staged master/coordinate algorithm may learn further independently justified region exclusions under a declared shared budget; never extend or silently resume a completed call. '
        'Only a validated complete positive can proceed to production-budget integration and the13-job/two-kerf H5 matrix. H2 stays open with all22 reserved vectors untouched under Artem\'s unchanged-denominator decision. '
        'Four checkpoints were normally pushed from51fe56c0 to4f359ff7 after all6 checks of40237436741 passed. New main CI40240715636 is tracked separately; do not claim its success from the older run. No new release is qualified.')
    OUT.mkdir();copies={'plan.json':'conflict-plan.json','result.json':'conflict-result.json','audit/checks.json':'conflict-audit.json','case-summary.json':'case-summary.json',
        'groups/result.json':'group-result.json','groups/audit/checks.json':'group-audit.json','solve/plan.json':'master-plan.json','solve/model-audit.json':'master-model-audit.json','solve/result.json':'master-result.json',
        'solve/selection.json':'selected-domains.json','selection-audit/checks.json':'selection-audit.json','anchor-solve/plan.json':'anchor-plan.json','anchor-solve/model-audit.json':'anchor-model-audit.json',
        'anchor-solve/result.json':'anchor-result.json','integer-conflict-proof/result.json':'interval-result.json','integer-conflict-proof/audit/checks.json':'interval-audit.json',
        'domain-core/plan.json':'core-plan.json','domain-core/model-audit.json':'core-model-audit.json','domain-core/result.json':'core-result.json','domain-core/core.json':'solver-derived-core.json',
        'three-cog-certificate/certificate.json':'three-cog-certificate.json','three-cog-certificate/result.json':'three-cog-result.json','three-cog-certificate/audit/checks.json':'three-cog-audit.json',
        'main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    shutil.copyfile(SYNC/'receipt.json',OUT/'main-push-receipt.json');write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],
        'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0',
        'master_solver_calls':1,'selected_anchor_solver_calls':1,'assumption_core_diagnostic_calls':1,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,
        'original_counts_and_material_gate_unchanged':True,'main_commits_pushed':4,'previous_main_successful_ci':40237436741,'current_main_ci_id':40240715636,
        'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,'three_region_exclusion_independently_verified':True,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for root in [BASE,SYNC]:
        for p in root.rglob('*'):
            if p.is_file():members[root.name+'/'+p.relative_to(root).as_posix()]=p
    for p in BASE.rglob('plan.json'):
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
    for p in [SOURCE/'profiles.json',SOURCE/'support-construction/atlas.json',ROOT/'output/h5-source-orientation-construction-20261025/propagation.json']:
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['build_h5_original_domain_conflicts.py','audit_h5_original_domain_conflicts.py','prepare_h5_domain_conflict_groups.py','audit_h5_domain_conflict_groups.py',
        'solve_h5_domain_selection.py','audit_h5_domain_selection_model.py','audit_h5_selected_original_domains.py','solve_h5_selected_anchors.py','audit_h5_selected_anchor_model.py',
        'prove_h5_selected_domain_conflict.py','audit_h5_selected_domain_proof.py','extract_h5_selected_domain_core.py','certify_h5_three_cog_conflict.py',
        'audit_h5_three_cog_certificate.py','push_h5_full_original_checkpoints.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'all8449813_domain_pairs_and5453534_exclusions_audited':True,'all23481818_physical_pair_exclusions_preserved_by_grouping':True,
        'master_assignment_and_full_original_anchor_model_audited':True,'selected_anchor_combination_infeasible_only':True,
        'interval_fixed_point_preserved_without_contradiction_claim':True,'solver_derived_three_domain_core_preserved':True,
        'independent228_segment_disk_and_two_complete_box_certificates_pass':True,'global12_2_29_domain_groups_exclude696_triples':True,
        'four_main_commits_pushed_after_all_six_prior_checks_passed':True,'new_main_ci_result_not_inferred':True,'production_source_and_readmes_unchanged':True,
        'full_target_witness':False,'native_full_job_qualified':False,'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: whole-domain conflicts and a three-cog exclusion — 2026-10-25

**A complete, independently checked conflict table now rules out millions of
impossible region pairs. A separate geometric certificate excludes 696 triples
of cog placement regions across all six moving cog copies.** No full original
target layout is found. H2/H5 remain open at **60%** completed milestone weight.

## Complete pair census and lossless grouping

The same adjusted 57-original source and nine mandatory moving originals retain
all original shapes, counts, source angles, stock/clearance guards and the
original material limit. Every query/domain pair needed by the 36 physical
moving-part pairs is listed before construction: **164** unique query pairs,
**394** physical uses and **8,449,813** unique domain pairs.

For each pair, the complete anchor-B-minus-anchor-A bounding rectangle expands
outward by one integer grid unit (0.001 mm). An exclusion is recorded only when
this **whole rectangle**, not just its corners, lies strictly inside a 0.0001 mm
inset of the raw original no-fit polygon. This proves collision of the actual
source-angle original shapes; no conservative outer cog hull is substituted.

Construction takes **{build['seconds']:.6f} seconds**, checking every pair and
recording **5,453,534** exclusions with no pending cases. Row-major packed bits,
their domain order, byte lengths, hashes, zero padding and full census are kept.
The independent **{audit['seconds']:.6f}-second** audit reconstructs all 82 raw
original obstacles from **9,824** unmerged triangle-pair hulls, checks every bit,
and verifies every marked whole rectangle against the independent raw geometry.
The minimum independent interior margin is **{audit['minimum_independent_raw_interior_margin_mm']:.12f} mm**.

Exactly identical conflict rows are grouped without losing any bit. The
**1,485** unique groups become **4,580** physical group constraints representing
**23,481,818** physical pair exclusions. Each group flag equals a sum of already
mutually exclusive choices for one original; at-most-one with its incompatible
partner choices is equivalent to all their binary exclusions. The independent
bitwise and Boolean audit checks every row partition, padding bit and truth table.

## Necessary region selection and full coordinate check

The necessary model retains all **9,776** domain options and **46** query options.
All nine originals are mandatory; both original sheet-area charges remain
required. Six index-order constraints remove equivalent copy-label permutations
only within identical bracket/cog inventories. The independently reconstructed
model has **13,436 variables and 8,257 constraints**, with no objective or hints.

One declared 60-second, eight-worker, seed-zero call finds a feasible domain
assignment in **{solved['seconds']:.6f} seconds**. The solver labels this OPTIMAL
because it is a satisfaction model; it is not a packing-quality optimum or an
anchor witness. The selected domains pass every stored pair exclusion. All 16
selected same-sheet pairs also receive a whole convex-difference check with
2,292 exact rational vertex/halfplane tests; those tests do not prove an
additional pair conflict.

A separate coordinate model then keeps all original geometry conditions for
this selected combination. Exact integer bounds prove 559 of its **633**
forbidden pieces always separated and 1,399 candidate directions impossible.
The remaining **74** complete disjunctions and all 33 inward domain halfplanes
produce an audited **2,045-variable/2,134-constraint** model. One declared
60-second call returns **INFEASIBLE in {ar['seconds']:.6f} seconds**. This excludes
only the chosen combination; no other region assignment is discarded by that
result alone. No invalid candidate is sent for native validation.

## An independently verified, broader three-region conflict

An exact-integer interval experiment replays **101** bound updates across 49
passes, then reaches a fixed point. Its independent replay passes, but it proves
no contradiction; that limit remains recorded.

A distinct, audited assumption-gated diagnostic preserves every original
coordinate constraint, activates selected-domain conditions only for their own
parts, and activates pair conditions only when both relevant domains are assumed.
One declared 10-second, single-worker call returns INFEASIBLE in
**{cr['seconds']:.6f} seconds**, identifying three cog domains: parts 3, 4 and 5
(items 54, 57 and 58). This solver-derived core is retained as evidence, then
checked by a separate geometric argument.

The raw original same-angle cog/cog no-fit polygon contains a strict
**258.082 mm origin-centred disk**. Exact rational distances to all **228 finite
boundary segments**, an independent interior crossing test and a downward
1-micrometre radius margin certify this fact. Two nonoverlapping original cogs
on the integer anchor grid must therefore have squared centre separation at
least `258082² + 1` in micrometre units.

For the three region boxes, B lies above C. Their maximum horizontal difference
forces a minimum B-C vertical separation. This raises B's lower bound enough
that the greatest possible A-B centre distance is too small. Both the original
boxes and boxes rounded **outward to 5 mm** pass this complete integer proof.
The enlarged case has a strict squared-distance shortfall of
**3,706,318,725 micrometre²**.

The enlarged boxes contain **12 / 2 / 29** complete source-angle cog domains.
Their x intervals are disjoint, so occupying all three groups necessarily uses
three distinct cogs. The certificate excludes **696 domain triples**, regardless
of which of the six mandatory moving cog copies occupy them. Independent replay
takes **{ca['seconds']:.6f} seconds** and relies on the geometry and arithmetic,
not the solver's unsatisfiable-core assertion.

Next add this global three-group occupancy exclusion to the necessary master,
preserving every original choice/count and all pair exclusions. Any new domain
assignment still requires a full original-coordinate solution, complete original
geometry/stock checks and native validation. Production-budget integration and
the full 13-job/two-kerf H5 matrix remain required. All completed calls stay closed.

## Main synchronization and evidence

All six jobs of [CI 40237436741](https://github.com/skulitom/Nestbolt/actions/runs/40237436741)
passed. Four committed checkpoints were then normally pushed from **51fe56c0**
to **4f359ff7**, and the remote head was verified. Its new
[CI 40240715636]({ci['url']}) is **{ci['status']}**, with **{success}/6** jobs
successful in this saved snapshot; the previous run does not prove this one passed.

Production source, the three accurate READMEs and release versions are unchanged.
No held-out evaluation, native packing call, quality run or new release is opened.
The published preview remains v0.2.0-alpha.1; stable Latest remains v0.1.0.

Evidence: [conflict audit]({NAME}/conflict-audit.json),
[group audit]({NAME}/group-audit.json), [master audit]({NAME}/master-model-audit.json),
[coordinate audit]({NAME}/anchor-model-audit.json),
[three-cog certificate]({NAME}/three-cog-certificate.json),
[independent certificate audit]({NAME}/three-cog-audit.json),
[push receipt]({NAME}/main-push-receipt.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']}** canonical members and
**{archive['verified_aliases']}** identical-content aliases retain exact bytes
with CRC/SHA-256 verification, including every tested pair bit, original source
obstacle, model, failed diagnostic limit, proof step and push capture.
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 whole-domain conflicts and three-cog exclusion, 2026-10-25:**
[The evidence]({link}) independently checks all 8,449,813 domain pairs and
5,453,534 original-shape collision exclusions. Lossless row grouping preserves
23,481,818 physical exclusions in 4,580 group constraints. A necessary-region
model finds a candidate in 8.094902 seconds; its complete original-coordinate
model is INFEASIBLE in 0.030771 seconds for that selected combination only.
The ordinary interval replay reaches a fixed point without proving a conflict.
A separate core diagnostic identifies three cog domains, then an independent
228-segment exact-rational no-fit disk certificate proves a broader three-region
exclusion. Groups containing 12/2/29 complete domains exclude 696 triples across
all six moving cogs, without changing any original count or material limit.
Next add that verified global occupancy clause before another declared search.
Four checkpoints are pushed normally to main 4f359ff7 after all six previous CI
jobs pass; new CI 40240715636 is tracked separately. No native acceptance,
quality run or new release is claimed. H2/H5 remain open at 60%.
'''
    for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'production_digest':source_digest(),'main_head':mainhead,'new_ci_status':ci['status'],'new_ci_successes':success},flush=True)
if __name__=='__main__':main()
