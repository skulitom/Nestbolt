"""Seal the continuous occupied-area audit, its failed check and core-margin census."""
from pathlib import Path
from datetime import datetime,timezone
import ast,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from pack_h5_evidence_archive import pack,digest
NAME='h5-occupied-area-relaxation-20261025';BASE=ROOT/'output'/NAME;OUT=ROOT/'benchmarks/results'/NAME
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def main():
    plan=load(BASE/'plan.json');result=load(BASE/'result.json');audit=load(BASE/'audit-verified/checks.json');margin=load(BASE/'fixed-core-margin-census/checks.json');prior=load(ROOT/'benchmarks/results/h5-small-pair-joint-20261025/source-review.json')
    assert audit['passed'] and audit['queries_reconstructed']==result['completed_queries']==168 and not load(BASE/'pending.json');assert audit['conditionally_excluded_core_groups']==[] and audit['known_compatible_original_polygon_cover_checks']==audit['known_original_translation_region_checks']==99983
    assert margin['passed'] and margin['passing_sufficient_distance_screen']==[0]
    assert source_digest()==prior['production_digest'];assert all(digest(ROOT/n)==h for n,h in prior['current_readmes'].items())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();mainhead=subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT).decode().strip();ci=json.loads(subprocess.check_output(['gh','run','view','40228140192','--json','status,conclusion,jobs,headSha,url'],cwd=ROOT));assert ci['headSha']==mainhead
    action='Build a fresh direct-coordinate feasibility model for every original small part against fixed core 0, the only saved core passing the source-derived conservative pair and stock distance screen. Keep the other cores and all four baselines preserved as evidence. Permit all original bracket rotations/reflections and all insert quarter turns, with equivalent normalized rectangle rotations explicitly accounted for. Require exactly 12 brackets and 21 inserts, together with the unchanged 18 frames and 15 cogs; no partial objective. Use a declared 0.01 mm coordinate grid, at least 0.22 mm new-part separation and 0.02 mm extra stock margin, and independently checked inward-rounded convex safe translation domains. Represent an L bracket by its two exact rectangular arms; apply directional nonoverlap only across different physical parts, never between its own arms. Inspect the earlier macro-rectangle and finite-pose exact-inventory models to preserve their failures and distinguish this model. Declare construction and one solver limit before execution; retain incomplete construction and UNKNOWN without extending or restarting completed searches. Any full witness still requires original geometry, public CLI, actual native transformed-collision checks, original production-budget qualification and the full 13-job/two-kerf matrix. This grid/subdomain model may miss placements and cannot establish unrestricted impossibility. Do not refine the completed area grid simply to seek a negative bound, resume old capped pose lists, weaken inventory or change H2.'
    write(BASE/'next-step.json',{'action':action,'full_target_witness':False})
    recovery={'original_attempt':'audit/','original_terminal_output_available':False,'original_process_observed_running_on_recovery':False,'original_checks_present':False,'diagnostic_attempt':'audit-recovered/','diagnostic_failure':'The assertion requiring at least 0.001 - 1e-7 mm inward distance fails on polygonal rounded offsets. Its traceback and original checker are preserved.','verified_attempt':'audit-verified/','changed_check':'Require the exclusion to remain a subset of the unshrunk forbidden/fixed geometry and record its actual nonnegative inward distance. Do not assume the approximate round offset has the full nominal radius at every corner. The subset condition alone makes this a relaxation; no positive-clearance acceptance is derived.','minimum_measured_inward_distance_mm':audit['minimum_forbidden_erosion_distance_mm'],'original_generation_repeated':False,'solver_calls':0,'original_result_pending_flag_preserved':True,'verification_result':'audit-verified/checks.json'}
    write(BASE/'audit-recovery.json',recovery)
    OUT.mkdir()
    for source,name in [('plan.json','plan.json'),('result.json','result.json'),('audit-verified/checks.json','audit.json'),('audit-verified/provenance.json','provenance.json'),('fixed-core-margin-census/checks.json','core-margins.json'),('audit-recovery.json','audit-recovery.json'),('next-step.json','next-step.json')]:shutil.copyfile(BASE/source,OUT/name)
    write(OUT/'main-ci-55835d7c.json',ci)
    review={'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,'main_head':mainhead,'production_digest':source_digest(),'current_readmes':prior['current_readmes'],'README_change_needed':False,'completion_percent':60,'H2_complete':False,'H5_complete':False,'new_release_qualified':False,'preview_release':'v0.2.0-alpha.1','stable_release':'v0.1.0','generation_seconds':result['seconds'],'audit_seconds':audit['seconds'],'conditionally_excluded_core_groups':[],'solver_calls':0,'native_packing_calls':0,'quality_runs':0,'held_out_files_evaluated':0,'full_target_witness':False,'native_margin_qualified':False,'stop_rule_review':'The same-day upstream review in h5-small-pair-joint-20261025 remains the recorded review; this evidence-only follow-up does not repeat it.','next_investigation':action};write(OUT/'source-review.json',review)
    members={};inputs={}
    for path in BASE.rglob('*'):
        if path.is_file():members[BASE.name+'/'+path.relative_to(BASE).as_posix()]=path
    for path in BASE.rglob('plan.json'):
        for n,h in load(path).get('inputs',{}).items():
            if n in inputs:assert inputs[n]==h
            inputs[n]=h
    for n,h in inputs.items():
        p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for row in load(BASE/'audit-verified/provenance.json')['source_members_matching_committed_evidence']:
        for n,h in [(row['source'],row['sha256']),(row['manifest'],row['manifest_sha256'])]:
            p=ROOT/n;assert digest(p)==h;members['source-inputs/'+n]=p
    for n in ['output/solve_h5_ragged_separator.py','output/solve_h5_ragged_propagation.py','output/solve_h5_contact_cpsat_cpython.py']:
        p=ROOT/n;members['reviewed-prior-models/'+p.name]=p
    pending=[ROOT/'output'/n for n in ['build_h5_occupied_area_relaxation.py','audit_h5_occupied_area_relaxation.py','recover_h5_occupied_area_audit.py','census_h5_fixed_core_margins.py','pack_h5_evidence_archive.py','ccd1.py']];seen=set()
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
    checks={'passed':True,'original_168_queries_and_all_7_aggregates_verified':True,'all_99983_known_memberships_and_translations_covered':True,'all_4_baselines_covered':True,'original_incomplete_audit_and_reproduced_failure_preserved':True,'source_and_readmes_unchanged':True,'no_fixed_core_excluded':True,'only_core_0_passes_sufficient_distance_screen':True,'native_margin_qualified':False,'full_target_witness':False,'completion_percent':60,**archive};write(OUT/'checks.json',checks);shutil.copyfile(__file__,OUT/Path(__file__).name)
    table='\n'.join(f"| {r['core_group']} | {r['combined_area_upper_mm2']:,.3f} | {r['combined_slack_mm2']:,.3f} |" for r in result['aggregates'])
    report=f'''# H5: continuous occupied-area relaxation — 2026-10-25

**The area bounds exclude none of the seven fixed arrangements.** Each bound
exceeds the 895,800 mm² needed by all 12 brackets and 21 inserts. This is
inconclusive: the pointwise union ignores competition between small parts,
so the excess area is not evidence that the inventory packs. No new layout
or solver call is produced. H2/H5 remain open at **60%** completed weight.

## Continuous coverage and independent audit

Keep each saved 18-frame/15-cog arrangement fixed. Relax positive clearance
to zero and expand stock bounds by 0.001 mm. Exact convex-piece Minkowski
sums form the original-outline forbidden translations; shrinking that union
removes only forbidden material. For every intersecting 50 mm grid cell,
an outward-padded convex hull covers the entire clipped translation region.
Minkowski sums of those hulls and the moving part cover every occupied point.
Clip to expanded stock after excluding only a subset of fixed material,
then union orientations, families and sheets. Holes remain reserved.

All **168** queries (seven cores, twelve permitted rotation/reflection classes,
two sheets) finish in **{result['seconds']:.6f} seconds**, within the declared
120 seconds. All four insert quarter turns are included. No query is pending.
The independent audit takes **{audit['seconds']:.6f} seconds** and checks:

- Eleven input files against the previous committed evidence manifest.
- All 48 cached forbidden polygons, using 1,280 convex-piece vertex sums.
- All translation domains, exclusions, 6,543 grid hulls and 8,683 swept sums.
- All seven complete family/combined aggregates.
- **99,983** compatible original-polygon memberships and the corresponding
  original translations, covering 17,481 saved variable poses.
- Both 64-part and both 63-part baselines, without changing their placements.

| Fixed core | Combined upper area (mm²) | Excess over full small inventory (mm²) |
| --- | ---: | ---: |
{table}

Both family-specific bounds also exceed their required areas. These results
do not prove that a fixed arrangement must move, that the target is impossible,
or that more finite pose sampling will succeed. No area-grid refinement or
completed solver retry is used to force a different conclusion.

## Preserved audit failure

The first audit directory contains its script and plan but no result; its
terminal output was unavailable after the interruption and no process remained.
A separately recorded diagnostic verification reproduces an assertion that
assumed a polygonal negative round offset always provides its full nominal
0.001 mm inward distance. The actual minimum is
**{audit['minimum_forbidden_erosion_distance_mm']:.12f} mm**.

The verified checker instead proves the necessary subset condition and records
the measured inward distance. Removing a subset of forbidden material enlarges
this relaxation regardless of the exact shrink distance. The saved construction
is unchanged. The failed checker, reproduced traceback and repaired checker
are all retained; the original result's pending-audit flag is preserved, with
the completed audit stored separately. This correction supplies no acceptance
clearance and makes no negative feasibility claim.

## Select a useful direct-coordinate investigation

The original-source conversion guard is 0.011444091796875 mm; the compensated
sheet-search separation is 0.21170867250963943 mm. Measuring all fixed-core
original polygons identifies **core 0 alone** as passing the sufficient pair
and stock distance screen: its minimum pair gap is 0.2126 mm and additional
stock margin is 0.0126 mm. Core 5 meets the pair screen but has only 0.0001 mm
stock margin. The other cores miss at least the pair screen. This is a geometric
screen, not an actual native transformed-collision acceptance.

{action}

## Repository and scope

Engine source and all three accurate READMEs are unchanged. The published
preview remains v0.2.0-alpha.1 and stable Latest remains v0.1.0; this audit
does not qualify another release. Main 55835d7c's hosted checks are captured
as `{ci['status']}` / `{ci['conclusion'] or 'pending'}`. No native packing,
production quality matrix, registry publication or held-out evaluation occurs.
The original 66-part count, material target, native guard, production budget
and full 13-job/two-kerf H5 requirement are retained. H2's October 20 decision
to keep its original gate open is unchanged.

Evidence: [plan]({NAME}/plan.json), [construction]({NAME}/result.json),
[independent audit]({NAME}/audit.json), [source provenance]({NAME}/provenance.json),
[failure recovery]({NAME}/audit-recovery.json), [fixed-core margins]({NAME}/core-margins.json),
[source review]({NAME}/source-review.json), [manifest]({NAME}/raw-manifest.json)
and [raw archive]({NAME}/raw-001.zip). All {archive['archive_members']} canonical
members and {archive['verified_aliases']} aliases retain their exact bytes,
with CRC and SHA-256 verification.
'''
    (OUT.parent/(NAME+'.md')).write_text(report,encoding='utf-8',newline='\n')
    note=f'''\n\n**N4 continuous occupied-area audit, 2026-10-25:** [the independent audit](../benchmarks/results/{NAME}.md)
checks all 168 queries, twelve permitted orientation/reflection classes and
seven fixed arrangements. All 99,983 known compatible polygon/translation
memberships and four prior baselines are covered. Every combined and family
area upper bound exceeds the required inventory; no core is excluded and no
packing feasibility is established. A failed round-offset assertion and its
repaired subset check are preserved without regenerating geometry. A separate
source-derived distance census finds only core 0 meets both conservative pair
and stock screens; actual native qualification remains required. Next build
an exact-count direct-coordinate model for its 12 brackets and 21 inserts,
with independently checked inward rounding, original outlines and new declared
limits. No solver retry, native packing, quality run or held-out evaluation
occurs. Engine source, accurate READMEs and releases remain unchanged; H2/H5
remain open at 60% completed milestone weight.
'''
    for n in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:append(ROOT/n,note)
    append(ROOT/'BENCHMARKS.md',note.replace('../benchmarks/results/','benchmarks/results/'));append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n');print(checks,flush=True)
if __name__=='__main__':main()
