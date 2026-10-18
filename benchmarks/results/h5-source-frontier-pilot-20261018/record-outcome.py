"""Retain the failed source-frontier pilot and select a saved-layout gap diagnosis."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-source-frontier-pilot-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
r=load(out/'results.json');v=load(out/'verification.json');g=load(out/'filled-outer-audit.json')
b=load(out/'final-boundaries.json');a=load(out/'fixed-inventory-area.json');w=load(out/'whole-job-area.json')
assert v['attempts']==v['valid']==72 and v['all_original_archives_verified']
assert g['cases']==48 and g['all_holes_reserved'] and g['same_sheet_pairs']==132966
assert b['all_saved_layout_checks_passed'] and a['all_saved_assignment_checks_passed'] and w['all_saved_job_checks_passed']
assert digest(out/'final-boundaries.json')==load(out/'analysis-environment-recovery.json')['completed_boundary_sha256']
pairs=r['summary']['pairs'];failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
assert len(failed)==5 and all(p['complete'] for p in pairs)
names=['directed_exchange_attempts','directed_exchanges','paired_exchange_attempts','paired_exchanges',
    'joint_repair_attempts','joint_repair_completed','joint_repair_failed','joint_repair_expired','joint_exchanges',
    'source_frontier_attempts','assignment_bridge_steps','assignment_bridge_flat_steps','assignment_bridge_committed',
    'assignment_bridge_rolled_back','assignment_bridge_rollbacks','assignment_bridge_area_rejections']
def counts(rows):
    rows=list(rows);return {name:sum(x['stats'].get(name,0) for x in rows) for name in names}
c=counts(x for x in r['records'] if x['arm']=='candidate')
m=counts(x for x in r['records'] if x['arm']=='candidate' and x['job'].startswith('m-mechanical'))
for name in [n for n in names if n.startswith('joint_')]:assert c[name]==load(out/'joint-counters.json')[name]
assert c['source_frontier_attempts']==load(out/'frontier-counters.json')['attempted']
followup=("Reject this candidate for integration; do not repeat its unchanged pilot or open the full 13-job gate. "
    "The 44 mechanical targeted calls include 23 completed repairs and 22 committed steps, with 20 expiries and one failed repair. "
    "Targets are being used; aggregate counters still do not identify their individual gains or time cost. "
    "Before changing crop policy or budgets again, inspect the saved final mechanical layouts for zero-victim transfers into earlier sheets. "
    "The current fill_gaps method draws 1000 uniform samples per part for a two-sheet window; it does not exhaustively represent narrow feasible translation regions. "
    "Use an independent conservative geometric construction of those regions, with original allowed orientations, filled outer contours and the original clearance. "
    "Keep every other placement fixed, retain each attempted layout, and validate any constructed transfer through the frozen public CLI and independent filled-outer checks. "
    "An actual material-reducing sequence would witness a missed geometric opportunity; no result under a conservative convex-hull check would not prove no true placement exists. "
    "This is post-hoc mechanism diagnosis, not a quality comparison or proof that the +1% target is feasible. "
    "Only a concrete useful witness should motivate a bounded implementation and another qualified pilot. "
    "Preserve all budgets, the four-step cap, strict final material guard, original failures, hole reservation and held-out isolation.")
interpretation={'failed_material_pairs':5,'results_sha256':digest(out/'results.json'),'candidate_counts':c,'mechanical_counts':m,
    'strictly_better_than_matched_common_baseline_pairs':sum(p['candidate_vs_baseline_percent']<0 for p in pairs),
    'final_boundary_sha256':digest(out/'final-boundaries.json'),'fixed_inventory_area_sha256':digest(out/'fixed-inventory-area.json'),
    'whole_job_area_sha256':digest(out/'whole-job-area.json'),'individual_target_gains_or_durations_observed':False,
    'gap_sampler_source':'output/h5-frontier-probe-20261018/candidate/crates/core/src/sheets/vstrip.rs',
    'gap_sampler_source_sha256':digest(root/'output/h5-frontier-probe-20261018/candidate/crates/core/src/sheets/vstrip.rs'),
    'quality_claim':False,'integrated':False,'H5_complete':False,'completed_weight_percent':60,'followup':followup}
write(out/'interpretation.json',interpretation);write(out/'source-review.json',interpretation)
details='; '.join(f"{p['job']} at {p['kerf_mm']} mm: {p['candidate_vs_normal_percent']:+.6f}%" for p in failed)
lo,hi=b['summary']['mechanical_height_reduction_mm_range'];clo,chi=b['summary']['mechanical_crossing_count_range']
count_note=(f"The candidate records {c['directed_exchanges']}/{c['directed_exchange_attempts']} accepted/attempted exchanges. "
    f"Joint repair has {c['joint_repair_attempts']} attempts: {c['joint_repair_completed']} complete, {c['joint_repair_failed']} fail and {c['joint_repair_expired']} expire. "
    f"There are {c['source_frontier_attempts']} proposed calls with tighter source crops, {c['joint_exchanges']} committed joint steps "
    f"and {c['assignment_bridge_rolled_back']} rolled-back steps. All accepted counts exclude rolled-back steps.")
boundary_note=(f"The twelve mechanical final layouts need {lo:.3f}–{hi:.3f} mm less used height on their currently credited sheet, "
    f"with {clo}–{chi} current copies above that conditional target. Four saved source inventories exceed their target's usable area even without inter-part kerf. "
    "These are conditional obstacles to the existing assignments, not whole-job impossibility proofs. "
    "The weak whole-job filled-area bound remains below the original target in all eight pairs; this does not prove packability.")
append(out.parent/(out.name+'.md'),f'''

## Verified outcome and next investigation

All 72 original archives, CRCs, member hashes, metrics, counters and guards verify.
The independent filled-outer audit checks all 48 common outputs and {g['same_sheet_pairs']:,}
same-sheet pairs at the unchanged 1e-7 mm tolerance. No hole interior is used.
The session takes {r['wall_seconds']/60:.3f} minutes. The completed boundary audit
was retained when the next area audit initially used a Python environment without
Shapely. Only the two missing audits were then run with the configured geometry
environment; no search or completed analysis was repeated.

**Reject for integration.** Five pairs fail the original +1% limit: {details}
No candidate pair has a lower median than its matched common baseline. This is
a descriptive pilot result, not a statistical ranking across old experiments.

{count_note}

{boundary_note}

[Independent geometry](h5-source-frontier-pilot-20261018/filled-outer-audit.json),
[final boundaries](h5-source-frontier-pilot-20261018/final-boundaries.json),
[conditional areas](h5-source-frontier-pilot-20261018/fixed-inventory-area.json),
[whole-job area bound](h5-source-frontier-pilot-20261018/whole-job-area.json) and
[interpretation](h5-source-frontier-pilot-20261018/interpretation.json).

{followup}

Production and the published preview remain unchanged. All three READMEs remain
accurate at 60%; no new qualified application build is ready to release.
H2/H5 remain open.
''')
note=f'''**N4 source-frontier outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-source-frontier-pilot-20261018.md),
but five of eight material pairs fail the original +1% limit: {details}
Independent checking covers all 48 common layouts and {g['same_sheet_pairs']:,} filled-outer
pairs. {count_note} No candidate pair beats its matched common-baseline median.
Reject this candidate for integration. The next investigation checks saved layouts
for geometrically constructed transfers into narrow gaps missed by uniform sampling;
it must produce actual validated layouts before another policy is justified.
All limits and production remain unchanged; H2/H5 remain open at 60%.
'''
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/')+'\n'+boundary_note+'\n\n'+followup+'\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n'+note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');a0=s.index('**N4 source-frontier pilot plan, 2026-10-18:**');a1=s.index('**N4 source-frontier qualification, 2026-10-18:**',a0)
p.write_text(s[:a0]+note+'\n'+s[a1:],encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-outcome.py')
print(json.dumps({'pilot_valid':72,'material_pairs_failed':5,'targeted_calls':c['source_frontier_attempts'],'committed_joint_steps':c['joint_exchanges'],'next':'Independent saved-layout feasible-translation check','integrated':False}))
