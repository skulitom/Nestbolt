"""Distinguish observed continuation from final quality; select the next bounded repair hypothesis."""
from pathlib import Path
from hashlib import sha256
import json,shutil
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exchange-chain-pilot-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
r=load(out/'results.json');pairs=r['summary']['pairs'];failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
assert len(failed)==4 and all(p['complete'] for p in pairs) and all(p['job'].startswith('m-mechanical-') for p in failed)
c=[x for x in r['records'] if x['arm']=='candidate'];multi=[x for x in c if x['stats'].get('directed_exchanges',0)>x['stats'].get('post_exchange_fill_calls',0)]
accepted=sum(x['stats'].get('directed_exchanges',0) for x in c);windows=sum(x['stats'].get('post_exchange_fill_calls',0) for x in c)
assert accepted==28 and windows==14 and len(multi)==7
assert all(p['candidate_vs_baseline_percent']>=0 for p in pairs)
probe=root/'output/h5-exchange-chain-probe-20261018/candidate';caller=probe/'crates/core/src/sheets/vstrip.rs';exchange=probe/'crates/core/src/sheets/vstrip/exchange.rs'
caller_text=caller.read_text(encoding='utf-8');step_text=exchange.read_text(encoding='utf-8')
assert 'let budget = t + (explore_until - t).max(0.0) * 0.1;' in caller_text
assert 'let exchange_until = (t + 1.2).min(budget);' in caller_text
assert 'let pair_end = now + ((self.last_step(exchange_until) - now) * 0.5).min(0.4);' in step_text
assert 'let middle = (now + pair_end) / 2.0;' in step_text
assert 'let mut source_sep = Separator::new(' in step_text
followup=('Reject integration and a full H5 run for this candidate. All four mechanical medians remain above the original +1% material limit. '
 'Seven candidate runs accept more exchanges than successful windows, proving actual continuation; 28 accepted exchanges across 14 successful windows still yield no lower final material median than the matched common baseline on any pair. This single matched pilot is descriptive, not a statistical ranking of small differences. '
 'Do not increase the chain cap blindly or repeat this unchanged pilot. Return to the source-repair constraint: the current caller still caps the exchange window at 1.2 seconds, within an existing ten-percent relocation allowance, and each receiver/source repair pair is capped at 0.4 seconds and half the remaining exchange time. Each proposal creates a fresh source separator. '
 'The preserved fixed-assignment diagnostic supplies three feasible source packings, observed in 1.05, 2.29 and 6.16 seconds, while the previous source traces retain positive repair loss. Those older assignments and timings are evidence of feasibility and incomplete short repairs, not proof that this candidate needs those durations or that extra repair time will satisfy H5. '
 'Next qualify a distinct continuous-source-repair allocation using the already available relocation allowance, within the unchanged whole-search wall budget. Preserve independent whole-job geometry and material acceptance, exact quantities, filled holes, allowed orientations, frozen sheets and rollback; author failure/deadline and useful repair witnesses before a new precommitted matched pilot. Record exact changes to the 1.2-second and per-pair caps rather than calling internal allocation unchanged. No full 13-job gate or reserved-input access is justified yet.')
record={'failed_material_pairs':len(failed),'results_sha256':digest(out/'results.json'),'candidate_accepted_exchanges':accepted,'successful_windows':windows,'runs_with_continuation':len(multi),'strictly_better_than_matched_common_baseline_pairs':0,'caller_source_sha256':digest(caller),'exchange_source_sha256':digest(exchange),'existing_relocation_fraction':0.1,'current_exchange_cap_seconds':1.2,'current_repair_pair_cap_seconds':0.4,'current_repair_pair_remaining_fraction':0.5,'older_feasibility_evidence':'benchmarks/results/h5-assignment-repack-20261018/verification.json','older_feasibility_sha256':digest(root/'benchmarks/results/h5-assignment-repack-20261018/verification.json'),'current_rejection_causes_observed':False,'quality_claim':False,'followup':followup}
(out/'interpretation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');shutil.copyfile(__file__,out/'interpret.py')
print(json.dumps({k:record[k] for k in ['failed_material_pairs','candidate_accepted_exchanges','successful_windows','runs_with_continuation','strictly_better_than_matched_common_baseline_pairs']}))
