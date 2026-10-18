"""Record observed constraints without inferring impossibility or changing any gate."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-productive-stage-20261018'
load=lambda p:json.loads(p.read_bytes());write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json');data=load(out/'observed-exchanges.json');s=data['summary'];allocation=load(out/'observed-allocations.json')
assert v['all_original_archives_verified'] and v['all_traces_verified'] and v['valid']==4
assert audit['all_holes_reserved'] and audit['cases']==4
attempts=data['attempts'];singles=[a for a in attempts if not a['proposal']['paired']];paired=[a for a in attempts if a['proposal']['paired']]
assert len(singles)==20 and all(a['proposal']['returned_area']>a['proposal']['incoming_area'] for a in singles)
assert len(paired)==8 and all(a['neutral_inventory'] for a in paired)
assert s['outcomes']=={'accepted':1,'material_guard_failed':1,'source_repair_failed':18,'neutral_inventory_rejected':7,'expired_after_repairs':1}
assert s['accepted_material_decreases']==s['accepted_extent_decreases']==0
large=[r for r in allocation['records'] if r['job']=='m-mechanical-large-plates']
assert len(large)==2
for r in large:
    assert r['source_inventories']==[{'1':1,'0':12,'3':6}]
    assert all(1 not in p for choices in r['pair_choices'] for p in choices)
rows=[a for a in attempts if a['source_remaining'] is not None]
minimum=min(a['source_remaining'] for a in rows);maximum=max(a['source_remaining'] for a in rows)
expired=sum(a['source_remaining']<=0 for a in rows)
source=root/'output/h5-productive-exchange-probe-20261018/candidate/crates/core/src/sheets/vstrip/exchange.rs';text=source.read_text(encoding='utf-8')
start=text.index('fn incoming_pairs(');end=text.index('\nfn same_original_inventory(',start)
fragment=text[start:end];assert 'groups.retain(|group| group.len() >= 2)' in fragment and 'std::sync::Arc::ptr_eq' in fragment
callsite=root/'output/h5-productive-exchange-probe-20261018/candidate/crates/core/src/sheets/vstrip.rs';calltext=callsite.read_text(encoding='utf-8')
caps=['let budget = t + (explore_until - t).max(0.0) * 0.1;','let exchange_until = (t + 1.2).min(budget);']
assert all(calltext.count(x)==1 for x in caps)
paircap='let pair_end = now + ((self.last_step(exchange_until) - now) * 0.5).min(0.4);';assert text.count(paircap)==1
followup='''All twenty single-part attempts return more recorded item area to the source
sheet than they remove. All eight paired attempts preserve the same original
inventory; seven are rejected as neutral and one expires after repair. In both
large-plate cases, the largest remaining item (ID 1) has only one copy, so the
same-original-item pair selector excludes it. Its six choices instead use
IDs 0 and 3. Panel cases consider four original item families, but their
attempted pairs still preserve inventory. This is a proposal/assignment gap
as well as an incomplete-repair observation.

The next isolated change should test bounded pairs of different original
items, with authored witnesses using different dimensions and allowed-pose
checks. Keep the existing whole-job time budget, complete obstruction sets,
pair returned-area bound, geometry/material guards and normal-mode behavior.
This is a new hypothesis, not a claim that mixed pairs will meet H5. The
earlier repair-feasibility timings are not minimum required times; simply
enlarging repair windows is not justified as the sole remedy by these traces.
'''
review={'source':source.relative_to(root).as_posix(),'source_sha256':sha256(source.read_bytes()).hexdigest(),'pair_selector_line':text[:start].count('\n')+1,'exact_pair_selector':fragment,'caller_source':callsite.relative_to(root).as_posix(),'caller_sha256':sha256(callsite.read_bytes()).hexdigest(),'caller_budget_fragments':caps,'pair_budget_fragment':paircap,'single_attempts':len(singles),'single_attempts_returning_larger_item_area':len(singles),'paired_attempts':len(paired),'paired_attempts_with_unchanged_inventory':len(paired),'large_plate_singleton_item_id':1,'source_requested_remaining_range_seconds':[minimum,maximum],'nonpositive_source_windows':expired,'inference':followup,'production_changed':False,'new_searches':0}
assert not (out/'source-review.json').exists();write(out/'source-review.json',review)
note=f'''**N4 productive-exchange diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-productive-stage-20261018.md).
Of {s['attempts']} attempts, 18 fail source repair, seven reject unchanged
inventory, one expires after repair, one fails the material guard and one
is accepted without immediate material/extent reduction. All eight paired
attempts preserve inventory; all twenty single attempts return more recorded
item area than they remove. The large-plate source's largest item has only
one copy, excluding it from the same-item pair selector. Requested source
windows range from {minimum:.6f} to {maximum:.6f} seconds, with {expired} already
nonpositive. Timings do not prove minimum repair time or impossibility.
The independent outer audit checks {audit['same_sheet_pairs']:,} pairs. The
next hypothesis is bounded mixed-item pairs with authored correctness checks;
budgets and every geometry/material limit remain. No integration or H5 credit;
H2/H5 remain open at 60%.
'''
marker='**N4 productive-exchange diagnosis, 2026-10-18:**';paths=[root/n for n in ['docs/STATUS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']]
assert all(marker not in p.read_text(encoding='utf-8') for p in paths)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=paths[0];old=p.read_text(encoding='utf-8');at=old.index('**N4 productive-exchange outcome, 2026-10-18:**');p.write_text(old[:at]+note+'\n'+old[at:],encoding='utf-8',newline='\n')
for p in paths[1:]:append(p,'\n\n'+note)
append(out.parent/(out.name+'.md'),f'''

## Independent audit and next hypothesis

The filled-outer audit independently checks all {audit['same_sheet_pairs']:,}
same-sheet pairs across four layouts. Minimum clearance slack is
{audit['minimum_clearance_slack_mm']:.12g} mm at the unchanged 1e-7 mm tolerance.
Original hole interiors remain reserved. All archives, trace references, five
solver counters, quantities, metrics and source/binary/input guards verify.

{followup}
The [source review](h5-productive-stage-20261018/source-review.json) retains the
exact selector, deadline fragments and hashes. No production change or
repeated quality run; H2/H5 remain open at 60%.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Productive-exchange choice and repair diagnosis

[All four diagnostic layouts validate](benchmarks/results/h5-productive-stage-20261018.md).
Twenty-eight attempts produce eighteen source-repair failures, seven neutral
rejections, one post-repair expiry, one strict material rejection and one
accepted exchange with no immediate material/extent improvement. All eight
paired attempts preserve inventory. Every one of twenty single attempts
returns more recorded item area to the source than it removes.

Both large-plate source inventories contain only one copy of their largest
item, which the same-item pair selector excludes. Four nonpositive source
windows and a requested-time range of {minimum:.6f} to {maximum:.6f} seconds
are recorded; these do not prove the time necessary for successful repair.
All original archives, five counters, validation/export results and guards
verify. The independent filled-outer audit checks {audit['same_sheet_pairs']:,}
pairs at unchanged tolerance. Bounded mixed-item pairs are the next hypothesis;
full correctness and quality gates remain. Production, original failures and
reserved inputs are unchanged. H2/H5 remain open at 60%.
''')
shutil.copyfile(__file__,out/'record-outcome.py');assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'attempts':len(attempts),'source_failures':18,'paired_inventory_preserving':len(paired),'singles_returning_more_area':len(singles),'nonpositive_source_windows':expired,'next_hypothesis':'bounded mixed-original-item pairs'}))
