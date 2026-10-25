"""Seal full-original joint geometry, closed bounded calls and all failed proposals."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-full-original-joint-20261025';BASE=ROOT/'output/h5-full-original-joint-prepared-20261025';OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    build=load(BASE/'result.json');geometry=load(BASE/'audit/checks.json');fullmodel=load(BASE/'solve/model-audit.json');full=load(BASE/'solve/result.json')
    sup=BASE/'support-construction';support=load(sup/'result.json');sa=load(sup/'audit/checks.json');sm=load(sup/'solve/model-audit.json');ss=load(sup/'solve/result.json')
    lazy=BASE/'lazy-full-original';lr=load(lazy/'result.json');la=load(lazy/'audit/checks.json');original=load(lazy/'original-proposal-audit/checks.json')
    assert all(r['passed'] for r in [geometry,fullmodel,sa,sm,la,original])
    assert full['status']=='UNKNOWN' and full['solver_calls']==1 and ss['status']=='INFEASIBLE' and ss['solver_calls']==1
    assert lr['status']=='UNKNOWN' and lr['solver_calls']==8 and la['complete_original_proposals_replayed']==7 and original['originally_valid_proposals']==0
    assert not load(BASE/'pending-queries.json') and not load(BASE/'pending-mutual.json') and build['queries_completed']==20 and build['mutual_cases_completed']==82
    prior=load(ROOT/'benchmarks/results/h5-guarded-source-adjustment-20261025/source-review.json')
    assert source_digest()==prior['production_digest'] and all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip()
    assert head.startswith('c627d494') and mainhead=='51fe56c096103464379068c99e10993b5b8516bb'
    ci=json.loads(subprocess.check_output(['gh','run','view','40237436741','--json','databaseId,status,conclusion,headSha,jobs,url'],cwd=ROOT))
    assert ci['headSha']==mainhead and len(ci['jobs'])==6
    write(BASE/'main-ci-snapshot.json',ci);success=sum(j['conclusion']=='success' for j in ci['jobs'])
    action=('All three recorded formulations are closed: full-original convex-forbidden model UNKNOWN, conservative moving-cog-hull model INFEASIBLE only for its stronger finite construction, and a separate full-original lazy separation experiment UNKNOWN after8 calls sharing60 seconds. '
        'Do not repeat these searches, change seeds or extend their caps. No66-original proposal is valid; round05 has the lowest retained overlap but still7 moving-pair overlaps totalling50480.2754985761mm2. '
        'The validated57-original adjusted source,20 full-original allowed regions and82 full-original mutual obstacles remain reusable evidence. '
        'Next investigate whole-domain incompatibility propagation: enumerate the complete same-sheet query/domain-pair census for the9 mandatory originals, including interchangeable copy groups. '
        'For each pair of inward-grid domain boxes form the complete signed difference rectangle, and certify a domain-pair conflict only when that whole rectangle lies strictly inside a full-original mutual forbidden region with an explicit inward numerical margin. '
        'Independent geometry coverage must justify every excluded pair; no sampled corner-only or centre-only conflict proof. Preserve complete census, untested cases and caps. '
        'A complete conflict table could supply direct binary domain exclusions and capacity/clique bounds, addressing the current weak propagation without restarting an unchanged search. Alternatively use the original-failure geometry to justify a genuinely larger source neighborhood, preserving all66 identities/counts and the original material limit. '
        'Every new model and bound needs an independent audit and separately declared budget before execution. Negatives remain source-angle/grid/fixed-source conditional; only a full positive can proceed to original geometry/native validation, production-budget integration and the13-job/two-kerf H5 matrix. '
        'H2 stays open under Artem\'s explicit unchanged-denominator decision, without reading the22 reserved vectors. Main51fe56c0 still has the prior six checkpoints; inspect CI40237436741 before the next normal fast-forward push, preserving any new remote commits. No new release is qualified.')
    OUT.mkdir();copies={'plan.json':'geometry-plan.json','result.json':'geometry-result.json','audit/checks.json':'geometry-audit.json',
        'query-summary.json':'query-summary.json','mutual-summary.json':'mutual-summary.json','solve/plan.json':'full-model-plan.json','solve/model-audit.json':'full-model-audit.json','solve/result.json':'full-model-result.json',
        'support-construction/plan.json':'support-plan.json','support-construction/result.json':'support-preparation.json','support-construction/audit/checks.json':'support-audit.json',
        'support-construction/solve/model-audit.json':'support-model-audit.json','support-construction/solve/result.json':'support-model-result.json',
        'lazy-full-original/plan.json':'lazy-plan.json','lazy-full-original/result.json':'lazy-result.json','lazy-full-original/audit/checks.json':'lazy-run-audit.json',
        'lazy-full-original/audit/round-checks.json':'lazy-round-checks.json','lazy-full-original/original-proposal-audit/checks.json':'original-proposal-audit.json',
        'lazy-full-original/original-proposal-audit/ranked-proposals.json':'original-proposal-ranking.json','main-ci-snapshot.json':'main-ci-snapshot.json'}
    for a,b in copies.items():shutil.copyfile(BASE/a,OUT/b)
    write(OUT/'next-step.json',{'action':action,'full_target_witness':False,'H5_complete':False})
    write(OUT/'source-review.json',{'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),
        'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,
        'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','full_model_solver_calls':1,'support_model_solver_calls':1,
        'shared_budget_lazy_solver_calls':8,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'originally_valid_proposals':0,
        'current_main_ci_id':40237436741,'current_main_ci_status':ci['status'],'current_main_ci_conclusion':ci['conclusion'],'current_main_successful_jobs':success,
        'full_target_witness':False,'native_full_job_qualified':False,'next_investigation':action})
    members={};inputs={}
    for p in BASE.rglob('*'):
        if p.is_file():members[BASE.name+'/'+p.relative_to(BASE).as_posix()]=p
    for p in BASE.rglob('plan.json'):
        for key in ['inputs','input_hashes']:
            for n,h in load(p).get(key,{}).items():
                if n in inputs:assert inputs[n]==h
                inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    # Preserve the original regions referenced by hash, not merely the new face records.
    for i,h in load(BASE/'plan.json')['original_query_hashes'].items():
        p=ROOT/'output/h5-guarded-source-adjustment-20261025/original-regions/queries'/f'{int(i):03d}.json';assert digest(p)==h
        members['source-inputs/'+p.relative_to(ROOT).as_posix()]=p
    names=['build_h5_full_original_joint_domains.py','audit_h5_full_original_joint_domains.py','solve_h5_full_original_joint.py',
        'audit_h5_full_original_joint_model.py','prepare_h5_full_original_supports.py','audit_h5_full_original_supports.py','prepare_h5_full_original_support_model.py',
        'solve_h5_full_original_supports.py','audit_h5_full_original_support_model.py','prepare_h5_lazy_original_helpers.py','build_h5_lazy_original_model.py',
        'audit_h5_lazy_original_model.py','solve_h5_lazy_original.py','audit_h5_lazy_original_run.py','diagnose_h5_lazy_original_proposals.py','pack_h5_evidence_archive.py','ccd1.py']
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
    write(OUT/'checks.json',{'passed':True,'all20_original_regions_and82_mutual_cases_complete_and_audited':True,
        'all3525_raw_allowed_faces_and_two_discarded_faces_recorded':True,'all512_forbidden_pieces_and27256_sufficient_outside_halfplanes_audited':True,
        'all_three_formulations_and_every_lazy_model_audited':True,'all_seven_failed66_original_proposals_preserved':True,'all11191_original_pair_and1848_stock_checks_retained':True,
        'all_bounded_calls_closed_without_extensions':True,'full_model_soft_time_overrun_seconds':max(0,full['seconds']-60),'lazy_soft_time_overrun_seconds':max(0,lr['seconds']-60),
        'convex_cog_hull_negative_is_conditional':True,'production_source_and_readmes_unchanged':True,'native_full_job_qualified':False,'full_target_witness':False,
        'H5_complete':False,'completion_percent':60,**archive})
    shutil.copyfile(__file__,OUT/Path(__file__).name)
    report=f'''# H5: complete original-shape joint searches — 2026-10-25

**All original-shape placement regions and moving-pair collision regions are
prepared and independently audited. No valid 66-original target layout was
found.** The full model and a distinct bounded constraint-generation experiment
return UNKNOWN; a smaller conservative cog-hull construction is conditionally
infeasible. H2/H5 stay open at **60%** completed milestone weight.

## Complete constructive geometry

The adjusted 57-original source from the preceding checkpoint is unchanged.
All nine other originals remain mandatory: items 28, 29, 50, 54, 57, 58, 62, 64
and 65. Counts remain 18 frames, 12 brackets, 21 inserts and 15 cogs. The original
material limit, stock bounds, native clearance guards and original area charges
are unchanged. Cogs retain all 80 vertices at their recorded source angle.

All **20** mode/sheet regions yield **3,525** raw convex faces; **3,523** remain
after conservative 0.000001 mm insets and inward 1-micrometre grid bounds. The
two discarded faces are explicitly retained with their reason. No raw region
has uncovered area. This remains a constructive subset because of the insets,
grid and finite orientation inventory; it is not an exhaustive relaxation.

All **82** required ordered profile pairs yield **512** convex forbidden pieces
and **27,256** sufficient outside halfplanes. Each forbidden piece expands by
a 0.000001 mm square; their union covers the whole collision region. Exact
rational coefficient-error bounds make allowed inequalities round inward and
outside inequalities round outward over the full signed difference domain.
Construction takes **{build['seconds']:.6f} seconds**, with no pending cases or caps.

Independent auditing takes **{geometry['seconds']:.6f} seconds** and checks 26
source files against the committed prior manifest, all 11,834 inward halfplanes,
**9,824** unmerged original triangle-pair hulls, and **1,862** independently
expanded raw-obstacle triangles. Every independently reconstructed whole
forbidden region is covered. Maximum raw/expanded geometric disagreement is
**{geometry['maximum_raw_hausdorff_error_mm']:.3g} / {geometry['maximum_expanded_hausdorff_error_mm']:.3g} mm**.

## Three distinct, closed formulations

| Formulation | Audited model | Declared limit | Outcome |
|---|---|---|---|
| Full original forbidden-piece disjunctions | 181,160 variables; 228,434 constraints | One 60 s call | UNKNOWN in {full['seconds']:.6f} s; no incumbent |
| Conservative moving-cog hull projections | 12,701 variables; 55,915 constraints | One 60 s call | INFEASIBLE in {ss['seconds']:.6f} s, conditional on this stronger construction |
| Full-original constraint generation | Eight successively audited models | 60 s shared across construction, audits and calls; at most 12 calls | UNKNOWN in {lr['seconds']:.6f} s after eight calls |

All calls use eight workers and seed zero. Full-model build/audit times are
{fullmodel['construction_seconds']:.6f}/{fullmodel['audit_seconds']:.6f} seconds;
the support-model times are {sm['construction_seconds']:.6f}/{sm['audit_seconds']:.6f} seconds.
The complete 46 mode choices and 9,776 physical-part convex domain options remain
mandatory, with both original area constraints and no partial-count objective.
The small soft timing overruns are retained, not presented as production-budget
passes. No completed call is repeated or extended.

The support construction covers each moving cog by its 40-vertex convex hull
only for mutual collision checks. Each bracket stays the exact union of two
rectangles. An independent certificate checks all **3,200** original-cog
vertex/halfplane relationships, **792** upward rational support ceilings, and
44 upward Euclidean-normal clearance bounds. Six x-order inequalities remove
equivalent permutations only within identical bracket/cog copy groups. Its
negative result does not exclude arrangements using the actual concave cogs.

The constraint-generation experiment returns to the complete original mutual
regions. Each provisional layout is checked against **every** forbidden piece
for every selected same-sheet profile pair. Every violated piece becomes a
complete, profile/sheet-conditional separation constraint in the next model.
It finds seven relaxed proposals, adds **83** independently replayed face cuts,
and checks **5,209** forbidden faces. The eighth call returns UNKNOWN. All eight
models, parameters, limits, proposals and cuts are preserved; no proposal is
treated as a completed target.

## Actual-original diagnosis

A separate audit reconstructs all **66 original polygons and copy identities**
in each of the seven proposals, checking **11,191** same-sheet original pairs and
**1,848** stock edges. Maximum profile reconstruction disagreement is
**{original['maximum_original_profile_reconstruction_error_mm']:.3g} mm**. All
fixed-part clearances and stock margins pass the unchanged native guards.
Every remaining failure is between mandatory moving originals.

None of the seven proposals passes. The lowest-overlap recorded proposal,
round 05, still has **seven** overlapping pairs totalling
**50,480.275499 mm²**. This is not a small numerical-clearance problem or a
native-validation candidate. Every original layout and all pair/stock checks
remain in the archive. No native packing or H5 quality run is opened.

Next, investigate complete whole-domain incompatibility propagation: prove
domain-pair exclusions only when the entire signed difference rectangle lies
strictly inside a full original forbidden region with a numerical margin.
Preserve the full pair census, tested/untested cases and caps; independently
verify each exclusion. Such exclusions may strengthen propagation or yield
capacity bounds. A larger source neighborhood is another option if justified
by the actual conflict geometry. The three completed searches stay closed.

## Repository and evidence

Main remains **51fe56c0**. [CI 40237436741]({ci['url']}) is **{ci['status']}**
with **{success}/6** successful jobs in this saved snapshot. A normal push of
the local checkpoints follows its terminal outcome, preserving remote changes.
Production source and all three accurate READMEs remain unchanged. The published
preview remains v0.2.0-alpha.1 and stable Latest remains v0.1.0; no new release is
qualified. H2's explicit unchanged-denominator decision and all held-out limits
remain intact. Production-budget integration and the full 13-job/two-kerf H5
matrix remain required.

Evidence: [geometry audit]({NAME}/geometry-audit.json),
[full-model audit]({NAME}/full-model-audit.json),
[support-model audit]({NAME}/support-model-audit.json),
[lazy-run audit]({NAME}/lazy-run-audit.json),
[original-proposal audit]({NAME}/original-proposal-audit.json),
[proposal ranking]({NAME}/original-proposal-ranking.json),
[raw archive]({NAME}/raw-001.zip) and [manifest]({NAME}/raw-manifest.json).
All **{archive['archive_members']}** canonical members and
**{archive['verified_aliases']}** identical-content aliases retain exact bytes,
verified by member count, CRC and SHA-256 across {archive['archive_parts']} archive part(s).
'''
    (ROOT/'benchmarks/results'/f'{NAME}.md').write_text(report,encoding='utf-8',newline='\n')
    note='''

**N4 complete original-shape joint searches, 2026-10-25:**
[The evidence]({link}) audits all 20 actual-original placement regions, 82 mutual
collision cases, 3,525 raw allowed faces and 512 forbidden pieces. All nine
moving originals remain mandatory alongside the adjusted 57-part source.
The full-original joint model returns UNKNOWN in 60.875060 seconds; a smaller
conservative moving-cog-hull model is conditionally INFEASIBLE in 8.862555 seconds.
A distinct original-shape constraint-generation experiment shares 60 seconds
across construction, audits and eight calls, ending UNKNOWN in 60.102165 seconds.
All seven relaxed 66-original proposals are independently reconstructed: 11,191
pair checks and 1,848 stock-edge checks preserve every failure. Fixed clearances
and stock margins pass; none passes moving-part collisions. The best recorded
overlap diagnosis still has seven overlapping pairs, so no native call is made.
All bounded searches stay closed. Next investigate certified whole-domain pair
exclusions or a structurally larger neighborhood, without relaxing counts,
material limits, clearance guards or H5. Source, accurate READMEs and releases
are unchanged; H2/H5 remain open at 60%.
'''
    for name in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
        append(ROOT/name,note.format(link=('' if name=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
    append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
    print({'sealed':NAME,**archive,'production_digest':source_digest(),'main_ci_status':ci['status'],'successful_jobs':success},flush=True)
if __name__=='__main__':main()
