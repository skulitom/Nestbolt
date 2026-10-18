"""Separate observed extended acceptances from unmet final material requirements."""
from pathlib import Path
from hashlib import sha256
import json, shutil
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-extended-repair-pilot-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
r=load(out/'results.json');pairs=r['summary']['pairs']
failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
assert len(failed)==5 and all(p['complete'] for p in pairs)
stage=load(out/'extended-counters.json');assert (stage['attempted'],stage['accepted'],stage['flat_rejections'])==(322,20,191)
c=[x for x in r['records'] if x['arm']=='candidate'];mechanical=[x for x in c if x['job'].startswith('m-mechanical-')]
accepted=sum(x['stats'].get('directed_exchanges',0) for x in c)
assert accepted==44 and sum(x['stats'].get('extended_exchanges',0) for x in mechanical)==6
assert sum(x['stats'].get('extended_flat_rejections',0) for x in mechanical)==0
b=load(out/'final-boundaries.json');a=load(out/'fixed-inventory-area.json')
assert b['results_sha256']==digest(out/'results.json') and a['same_inventory_area_failures']==5
followup=('Reject integration and the full 13-job gate for this candidate. All four mechanical pairs and the 1.5 mm bracket pair miss the original +1% material limit. '
 'The extended phase accepts 20 of 322 attempts, including six of 55 mechanical attempts; its 191 flat rejections all belong to bracket cases. Longer repair can therefore reach valid strict improvements, but this does not yield the required final material use. The small paired median differences are descriptive, not a statistical ranking. '
 'Do not repeat this unchanged pilot, increase the exchange cap blindly or call repair time the sole remaining cause. The final mechanical layouts need 138.702–200.994 mm less height on the currently credited sheet to meet 1.01 times the matched normal median, with 6–28 current copies above the conditional target. Five of six large-plate last-sheet inventories exceed even the target usable rectangle area with original holes filled; merely rearranging those same copies on that same target sheet cannot suffice. Different assignments or another credited sheet remain possible. The remaining area checks do not prove packability, and none proves global H5 infeasibility. '
 'Next investigate assignment progress across material-flat intermediate states. The present extended policy rejects every flat trial before later compression, while source inventory may need to change before all height-setting copies can move. A distinct bounded policy may use strictly decreasing last-sheet filled area as an internal progress measure, with a retained original incumbent and a final whole-job geometry/material decision; this is a hypothesis, not established benefit. First capture or author a concrete flat area-reducing transition followed by valid whole-job improvement, together with failure/expiry rollback, no cycling, exact quantities, allowed orientations, frozen sheets and hole reservation. Preserve the original short phase, overall deadline and validation reserve. Do not weaken existing assertions or count a flat internal step as a quality improvement. Qualify before any new committed matched comparison. No reserved input access, limit change or release follows this rejected candidate.')
record={'failed_material_pairs':len(failed),'results_sha256':digest(out/'results.json'),
 'candidate_attempts':sum(x['stats'].get('directed_exchange_attempts',0) for x in c),
 'candidate_accepted_exchanges':accepted,'extended_attempts':stage['attempted'],'extended_accepts':stage['accepted'],
 'extended_flat_rejections':stage['flat_rejections'],'mechanical_extended_attempts':sum(x['stats'].get('extended_exchange_attempts',0) for x in mechanical),
 'mechanical_extended_accepts':6,'mechanical_extended_flat_rejections':0,
 'strictly_better_than_matched_common_baseline_pairs':sum(p['candidate_vs_baseline_percent']<0 for p in pairs),
 'final_boundary_analysis_sha256':digest(out/'final-boundaries.json'),'fixed_inventory_area_sha256':digest(out/'fixed-inventory-area.json'),
 'intermediate_repair_losses_durations_or_area_transitions_observed':False,
 'quality_claim':False,'followup':followup}
(out/'interpretation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'interpret.py')
print(json.dumps({k:v for k,v in record.items() if k not in ['followup'] and not k.endswith('sha256')}))
