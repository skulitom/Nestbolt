"""Retain the complete failed joint-repair pilot and a bounded next diagnostic."""
from pathlib import Path
from hashlib import sha256
import json, shutil, subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-joint-repair-pilot-20261018'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
r=load(out/'results.json');v=load(out/'verification.json')
audit=load(out/'filled-outer-audit.json');boundaries=load(out/'final-boundaries.json')
capacity=load(out/'fixed-inventory-area.json');whole=load(out/'whole-job-area.json')
joint=load(out/'joint-counters.json');bridge=load(out/'bridge-counters.json')
assert v['valid']==v['attempts']==72 and v['all_original_archives_verified']
assert audit['cases']==48 and audit['all_holes_reserved']
assert boundaries['all_saved_layout_checks_passed'] and capacity['all_saved_assignment_checks_passed']
assert whole['all_saved_job_checks_passed'] and len(whole['records'])==8
pairs=r['summary']['pairs'];assert len(pairs)==8 and all(p['complete'] for p in pairs)
failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
assert len(failed)==5
names=['directed_exchange_attempts','directed_exchanges','paired_exchange_attempts','paired_exchanges',
    'joint_repair_attempts','joint_repair_completed','joint_repair_failed','joint_repair_expired','joint_exchanges',
    'assignment_bridge_steps','assignment_bridge_flat_steps','assignment_bridge_committed',
    'assignment_bridge_rolled_back','assignment_bridge_rollbacks','assignment_bridge_area_rejections']
def counts(rows):return {n:sum(row.get('stats',{}).get(n,0) for row in rows) for n in names}
c=counts(row for row in r['records'] if row['arm']=='candidate')
m=counts(row for row in r['records'] if row['arm']=='candidate' and row['job'].startswith('m-mechanical-'))
for name in [n for n in names if n.startswith('joint_')]:assert c[name]==joint[name]
details='; '.join(f"{p['job']} at {p['kerf_mm']} mm: {p['candidate_vs_normal_percent']:+.6f}%" for p in failed)
lo,hi=boundaries['summary']['mechanical_height_reduction_mm_range']
clo,chi=boundaries['summary']['mechanical_crossing_count_range']
followup=(
    f"Joint repair completes {c['joint_repair_completed']}/{c['joint_repair_attempts']} pair attempts and records {c['joint_exchanges']} committed steps, "
    f"including {m['joint_exchanges']} committed steps in the mechanical jobs. It is not simply unused or universally expiring. "
    "The pilot still fails, and only one pair's median is below the matched common baseline; no statistical ranking or new quality claim follows. "
    "Final snapshots and aggregate counters do not show the actual extra-member migrations, individual material gains, repair/lowering durations or rejection stage. "
    "The next step is a narrow diagnostic observer of actual joint attempts in the failed mechanical jobs: preserve canonical pair inventories before/after, "
    "additional cross-sheet migrations, whole-job material before/after, elapsed repair/lowering time, expiry/rejection reasons and provisional rollback. "
    "First verify that observation changes no decision logic, independently check saved trial geometry and frozen sheets, and commit the diagnostic plan. "
    "Use the original inputs, seeds and 60-second allowance on serial CCD0; logging may change wall-time trajectories, so this cannot be a quality comparison. "
    "Use that trace to choose a specific changed policy and require an actual independently validated witness before any further pilot. "
    "Do not repeat this unchanged pilot or increase the step cap blindly. Production, all original limits, hole reservation and the held-out split remain unchanged.")
interpretation={'failed_material_pairs':len(failed),'results_sha256':digest(out/'results.json'),
    'candidate_counts':c,'mechanical_counts':m,
    'strictly_better_than_matched_common_baseline_pairs':sum(p['candidate_vs_baseline_percent']<0 for p in pairs),
    'final_boundary_analysis_sha256':digest(out/'final-boundaries.json'),
    'fixed_inventory_area_sha256':digest(out/'fixed-inventory-area.json'),
    'whole_job_area_sha256':digest(out/'whole-job-area.json'),
    'actual_extra_member_migrations_individual_gains_and_durations_observed':False,
    'quality_claim':False,'followup':followup}
write(out/'interpretation.json',interpretation)
decision='Reject this candidate for integration; do not open the full 13-job gate for it.'
count_note=(f"There are {c['directed_exchanges']}/{c['directed_exchange_attempts']} accepted/attempted exchanges. "
    f"Joint repair attempts {c['joint_repair_attempts']} pairs: {c['joint_repair_completed']} complete, {c['joint_repair_failed']} fail and {c['joint_repair_expired']} expire. "
    f"It records {c['assignment_bridge_steps']} provisional steps, including {c['assignment_bridge_flat_steps']} flat steps; "
    f"{c['joint_exchanges']} steps commit and {c['assignment_bridge_rolled_back']} roll back across {c['assignment_bridge_rollbacks']} rollbacks. "
    "Only committed counts survive rollback. Pair completion alone does not mean whole-job acceptance or final quality improvement.")
boundary_note=(f"The twelve mechanical final layouts need {lo:.3f}–{hi:.3f} mm less used height on their current credited sheet, "
    f"with {clo}–{chi} current copies above the conditional target. Four saved inventories exceed that target sheet's usable area "
    "even without inter-part kerf. These same inventories cannot fit those same targets; changing assignments or the credited offcut can change the conclusion. "
    "The separate whole-job filled-area bound is below the target for all eight pairs. That weak bound does not prove packability, "
    "and the conditional bounds do not prove whole-job infeasibility. All analyses use saved outputs and add no searches.")
note=f'''**N4 joint-repair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-joint-repair-pilot-20261018.md).
The independent filled-outer audit checks {audit['same_sheet_pairs']:,} same-sheet
pairs across all 48 common-mode layouts. Five of eight material pairs fail the
original +1% limit. {details}
{count_note} {decision} The isolated candidate retains its 165 passing native tests,
prior witnesses and complete qualification evidence. Production remains unchanged.
The next diagnostic will trace actual accepted joint repairs and their material
gain before choosing another policy. H2/H5 remain open at 60%.
'''
status=root/'docs/STATUS.md';old=status.read_text(encoding='utf-8')
start=old.index('**N4 joint-repair pilot plan, 2026-10-18:**')
end=old.index('**N4 assignment-bridge outcome, 2026-10-18:**',start)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
append(out.parent/(out.name+'.md'),f'''

## Independent geometry check and decision

Shapely {audit['shapely_version']} checks every original filled outer polygon in all
48 common-mode outputs: {audit['same_sheet_pairs']:,} same-sheet pairs are disjoint and
at least the requested kerf apart within the unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm
numerical tolerance. Minimum clearance slack is {audit['minimum_clearance_slack_mm']:.12g} mm.
Hole interiors remain reserved. All 72 archives pass CRC and member hashes;
the original plan, source, runner, binaries, environment and input guards match.

**{decision}** Five of eight pairs fail: {details}

{count_note}

{boundary_note}

[Final boundaries](h5-joint-repair-pilot-20261018/final-boundaries.json),
[conditional fixed inventories](h5-joint-repair-pilot-20261018/fixed-inventory-area.json),
[whole-job area check](h5-joint-repair-pilot-20261018/whole-job-area.json) and
[interpretation](h5-joint-repair-pilot-20261018/interpretation.json) retain the details.

{followup}

The published v0.2.0-alpha.1 preview and production code remain unchanged.
The English, Japanese and Chinese READMEs already describe that preview and 60%
completion accurately. There is no new qualified application build to release.
H2/H5 remain open.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Bounded joint-sheet repair comparison

[All 72 outcomes validate](benchmarks/results/h5-joint-repair-pilot-20261018.md)
in {r['wall_seconds']/60:.3f} minutes under the committed matched 60-second method.
All original ZIP/member hashes, metrics and guards pass. Independent checking
covers {audit['same_sheet_pairs']:,} same-sheet pairs across 48 common-mode layouts;
all holes stay reserved at the original numerical tolerance.

Five of eight material pairs fail +1%: {details}
{count_note} {decision}

{boundary_note}

{followup}

Production and release assets remain unchanged; the three READMEs remain accurate.
No new held-out access, H5 credit or quality claim. H2/H5 remain open at 60%.
''')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n'+note)
status.write_text(old[:start]+note+'\n'+old[end:],encoding='utf-8',newline='\n')
write(out/'source-review.json',{'pilot_material_failures':len(failed),'decision':decision,
    'candidate_counts':c,'mechanical_counts':m,'conditional_inventory_area_failures':capacity['same_inventory_area_failures'],
    'whole_job_area_obstructions':whole['whole_job_area_obstructions'],'followup':followup,
    'quality_claim':False,'integrated':False,'H5_complete':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'record-outcome.py')
shutil.copyfile(root/'benchmarks/results/h5-joint-repair-preparation-20261018/candidate-complete.patch',out/'candidate-complete.patch')
shutil.copyfile(root/'benchmarks/results/h5-joint-repair-preparation-20261018/complete-patch.json',out/'complete-patch.json')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'failed_material_pairs':len(failed),'joint_counts':{k:v for k,v in joint.items() if k!='records'},'decision':decision}))
