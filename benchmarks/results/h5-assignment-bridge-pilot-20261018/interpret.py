"""Interpret the saved pilot without treating provisional moves as quality gains."""
from pathlib import Path
from hashlib import sha256
import json, shutil
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-assignment-bridge-pilot-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
r=load(out/'results.json');pairs=r['summary']['pairs']
assert len(r['records'])==72 and all(p['complete'] for p in pairs)
failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
c=[x for x in r['records'] if x['arm']=='candidate']
mechanical=[x for x in c if x['job'].startswith('m-mechanical-')]
keys=['directed_exchange_attempts','directed_exchanges','extended_exchange_attempts','extended_exchanges',
      'extended_flat_rejections','assignment_bridge_steps','assignment_bridge_flat_steps',
      'assignment_bridge_committed','assignment_bridge_rolled_back','assignment_bridge_area_rejections',
      'assignment_bridge_rollbacks']
totals=lambda rows:{k:sum(x['stats'].get(k,0) for x in rows) for k in keys}
all_counts=totals(c);mechanical_counts=totals(mechanical)
stage=load(out/'extended-counters.json');bridge=load(out/'bridge-counters.json')
assert stage['accepted']==all_counts['extended_exchanges']==all_counts['assignment_bridge_committed']
assert all(all_counts[k]==bridge[k] for k in keys if k.startswith('assignment_bridge_'))
assert all_counts['assignment_bridge_steps']==all_counts['assignment_bridge_committed']+all_counts['assignment_bridge_rolled_back']
b=load(out/'final-boundaries.json');a=load(out/'fixed-inventory-area.json')
assert b['results_sha256']==digest(out/'results.json') and b['all_saved_layout_checks_passed']
assert a['all_saved_assignment_checks_passed'] and a['final_boundaries_sha256']==digest(out/'final-boundaries.json')
bs=b['summary'];lo,hi=bs['mechanical_height_reduction_mm_range'];clo,chi=bs['mechanical_crossing_count_range']
followup=(f"Reject integration and the full 13-job gate for this candidate: {len(failed)} of eight material pairs miss the unchanged +1% limit. "
 "All four failures are mechanical. No pair has a lower median material use than its matched common baseline. This is descriptive, not a statistical ranking. "
 f"The extended phase records {all_counts['assignment_bridge_steps']} provisional/strict steps, including {all_counts['assignment_bridge_flat_steps']} flat steps; "
 f"{all_counts['assignment_bridge_committed']} steps belong to committed sequences and {all_counts['assignment_bridge_rolled_back']} roll back. "
 "A panel-hardware laser outcome records three committed extended steps including one flat step, so the intended mechanism does occur in a real development job. "
 "A committed sequence ends with strict whole-job material improvement; its intermediate steps need not each improve material, and these counters do not reveal individual gains or repair timing. "
 f"The {bs['mechanical_layouts']} final mechanical layouts require {lo:.3f}–{hi:.3f} mm less height on the currently credited sheet, "
 f"with {clo}–{chi} current copies above the conditional target. {a['same_inventory_area_failures']} current inventories exceed that target's usable rectangle area even without inter-part kerf. "
 "Those same copies cannot fit that same target sheet; this is not a whole-job infeasibility result. Area below capacity does not establish packability. "
 "Do not repeat this unchanged pilot, increase the step cap blindly or assume that longer repair or flat transitions alone address the gap. "
 "The next distinct hypothesis is joint repair of the affected two-sheet window. The current proposal repairs receiver and source separately with fixed membership; allowing an additional copy to migrate between them may unlock a final strict improvement that neither separate repair can reach. "
 "First author or capture a concrete fixed-assignment failure with a valid joint rearrangement, then test actual joint repair and independently validate geometry, quantities, orientations, frozen prefix and reserved holes. "
 "A feasible hand-authored arrangement alone does not prove the search finds it. Preserve the original short phase, total deadline, validation reserve, strict final whole-job acceptance and rollback. "
 "Qualify a changed policy before another committed matched comparison. No held-out access, limit change, quality claim or new release follows this rejected candidate.")
record={'failed_material_pairs':len(failed),'results_sha256':digest(out/'results.json'),
 'candidate_counts':all_counts,'mechanical_counts':mechanical_counts,
 'strictly_better_than_matched_common_baseline_pairs':sum(p['candidate_vs_baseline_percent']<0 for p in pairs),
 'final_boundary_analysis_sha256':digest(out/'final-boundaries.json'),'fixed_inventory_area_sha256':digest(out/'fixed-inventory-area.json'),
 'individual_repair_losses_durations_or_material_gains_observed':False,
 'quality_claim':False,'followup':followup}
with (out/'interpretation.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(record,f,indent=2);f.write('\n')
shutil.copyfile(__file__,out/'interpret.py')
print(json.dumps({'failed_pairs':len(failed),'counts':all_counts,'quality_claim':False}))
