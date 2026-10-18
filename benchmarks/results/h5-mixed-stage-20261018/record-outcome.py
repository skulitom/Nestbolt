"""Record observed pair selection barriers and the separate larger-return witness."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-mixed-stage-20261018'
load=lambda p:json.loads(p.read_bytes())
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json');ex=load(out/'observed-exchanges.json');gens=load(out/'observed-generations.json')['records']
assert v['all_original_archives_verified'] and v['all_traces_verified'] and v['valid']==4
assert audit['all_holes_reserved'] and audit['cases']==4
s=ex['summary'];assert s['outcomes']=={'source_repair_failed':19,'material_guard_failed':1,'accepted':1,'neutral_inventory_rejected':7}
large=[g for g in gens if g['job']=='m-mechanical-large-plates'];panel=[g for g in gens if g['job']=='m-mechanical-panel-hardware']
assert len(large)==24 and all(g['seen']==g['sample_total'] and not g['deadline_reached'] and g['retained']==0 for g in large)
assert sum(g['seen'] for g in large)==4764 and sum(g['area_rejected'] for g in large)==1721
assert sum(g['area_rejected'] for g in large if g['mixed'])==575
assert len(panel)==2 and all(not g['mixed'] and g['retained']==6 for g in panel)
paired=[a for a in ex['attempts'] if a['proposal']['paired']]
assert len(paired)==7 and all(a['neutral_inventory'] and a['outcome']=='neutral_inventory_rejected' for a in paired)
assert all(a['receiver_initial_loss']==a['source_initial_loss']==0 for a in paired)
assert all(a['receiver_elapsed']<.0001 and a['source_elapsed']<.0001 for a in paired)
accepted=[a for a in ex['attempts'] if a['outcome']=='accepted'];assert len(accepted)==1 and not accepted[0]['proposal']['paired']
gain=accepted[0]['before_material']-accepted[0]['after_material'];assert abs(gain-18.669)<1e-6
witness=root/'benchmarks/results/h5-larger-return-witness-20261018';w=load(witness/'checks.json')
assert w['both_layouts_valid'] and w['all_metrics_identical'] and w['material_mm2']==19700
assert w['returned_group_area_mm2']==2790>w['incoming_group_area_mm2']==2700 and w['optimizer_runs']==0
for name,r in load(witness/'integrity.json')['members'].items():assert sha256((witness/name).read_bytes()).hexdigest()==r['sha256']
source=root/w['current_filter_source'];text=source.read_text(encoding='utf-8');assert sha256(source.read_bytes()).hexdigest()==w['current_filter_source_sha256']
start=text.index('        let same_pairs = incoming_pairs');end=text.index('            let incoming_key = selected[0];',start)
neutral_start=text.index('                    // Same inventory');neutral_end=text.index('                    sep.layout = trial;',neutral_start)
followup='''Both large-plate traces reach all twelve planned pairs and every generated
sample. The paired returned-area filter alone discards 1,721 otherwise eligible
samples, including 575 mixed samples, after pose/boundary/obstruction-count checks.
This identifies a search filter, not the feasibility of those rejected layouts.
The independently checked larger-return witness demonstrates that this area
inequality is not necessary for a valid material-nonincreasing pair exchange.
The next isolated candidate should first reproduce a failing runtime regression
for that witness, then test removing this proposal-area filter while retaining
complete obstruction sets, pose rules, both repairs, strict whole-job geometry
and material guards, all existing budgets and normal-mode behavior.

Panel traces expose a separate scheduling limitation: only the first same-item
pair is generated, retaining six proposals per kerf; seven attempted paired
swaps are rejected as unchanged-inventory without material gain. No mixed pair
is generated there. The recorded repairs already have zero loss and each takes
less than 0.0001 seconds. The trace does not allocate the remaining time among
construction, conversion and independent validation, so it does not establish
which of those dominates. Do not infer that longer repair windows alone solve
either workload, or that lifting the area filter will meet the quality gate.
'''
write(out/'source-review.json',{'source':w['current_filter_source'],'source_sha256':w['current_filter_source_sha256'],
    'pair_filter':w['current_filter_fragment'],'pair_filter_line':w['current_filter_line'],
    'exact_pair_schedule_and_deadline_check':text[start:end],'exact_post_validation_neutral_guard':text[neutral_start:neutral_end],
    'large_generation_calls':24,'large_samples':4764,'large_area_rejections':1721,'large_mixed_area_rejections':575,
    'panel_generation_calls':2,'panel_mixed_generation_calls':0,'panel_neutral_pair_attempts':7,
    'neutral_repairs_zero_initial_loss':True,'neutral_repair_elapsed_each_below_seconds':.0001,
    'accepted_single_material_decrease_mm2':gain,'next_hypothesis':followup,'production_changed':False,'quality_claim':False})
note=f'''**N4 mixed-pair diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-mixed-stage-20261018.md).
The two large-plate traces examine all 24 pair calls and 4,764 samples without
sample truncation, but retain no paired proposal. The area filter rejects
1,721 otherwise eligible samples, including 575 mixed samples. Panel traces
generate only the first same-item pair per kerf; all seven attempted paired
swaps reject unchanged inventory, and no mixed pair is generated. Their
repairs already have zero loss and each takes less than 0.0001 seconds;
remaining construction/validation time is not separately measured.
Overall, 28 attempts yield 19 failed source repairs, seven neutral rejections,
one material rejection and one accepted single swap saving {gain:.3f} mm2
immediately. The filled-outer audit checks {audit['same_sheet_pairs']:,} pairs.
The next hypothesis targets the proposal-area filter with an authored runtime
regression; it is not a quality claim. H2/H5 remain open at 60%.
'''
witness_note='''**N4 larger-return witness, 2026-10-18:** [a valid mixed pair exchange](../benchmarks/results/h5-larger-return-witness-20261018.md)
returns 2,790 mm2 of parts after removing 2,700 mm2, while keeping all seven
parts and every material metric unchanged at 19,700 mm2. Frozen CLI and
independent filled-outer checks validate both authored layouts. Eight
conservative height bounds exclude either selected incoming part moving
alone while one filler stays on each sheet. The current pair-area filter
excludes this complete return set. This proves a limitation of that filter,
with zero optimizer runs; an actual runtime regression and full candidate
checks remain necessary. It does not establish mechanical quality or H5.
'''
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
p=root/'docs/STATUS.md';old=p.read_text(encoding='utf-8');start=old.index('**N4 mixed-pair diagnosis preparation, 2026-10-18:**');end=old.index('**N4 mixed-exchange outcome, 2026-10-18:**',start)
p.write_text(old[:start]+note+'\n'+witness_note+'\n'+old[end:],encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note+'\n'+witness_note)
append(out.parent/(out.name+'.md'),f'''

## Independent audit and next hypothesis

All {audit['same_sheet_pairs']:,} same-sheet pairs in the four saved layouts
pass the independent filled-outer audit. Minimum clearance slack is
{audit['minimum_clearance_slack_mm']:.12g} mm under the unchanged 1e-7 mm tolerance.
The one accepted single swap decreases immediate material by {gain:.3f} mm2;
this small local change does not replace the failed pilot comparison.

{followup}
[The source review](h5-mixed-stage-20261018/source-review.json) preserves the
exact filter, schedule, neutral guard and source hash. The
[larger-return witness](h5-larger-return-witness-20261018.md) remains authored
geometry evidence only. Production, limits, reserved inputs and 60% completion
are unchanged.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Mixed-pair sampling and repair diagnosis

[Four diagnostic layouts validate](benchmarks/results/h5-mixed-stage-20261018.md),
including all {audit['same_sheet_pairs']:,} independently checked filled-outer
pairs. The two large-plate searches examine all 4,764 samples from 24 pair
calls. None truncate; none retain a paired proposal. The area filter rejects
1,721 otherwise eligible samples, of which 575 are mixed. Panel searches
generate only their first same-item pair; seven attempted pairs reject neutral
inventory and none reaches a mixed generation call. The recorded repairs have
zero initial loss and each takes under 0.0001 s; other stages are not timed
separately. Overall, 28 attempts yield 19 source failures, seven neutral
rejections, one material failure and one accepted single saving {gain:.3f} mm2.

The reader reconciles sampling partitions and all seven solver counters;
archives, quantities, metrics, exports and source/binary/input hashes verify.
Instrumentation can perturb trajectories. No quality repeat, integration,
gate change or H5 credit; completed milestone weight stays 60%.

## 2026-10-18 — Author a larger-return-area pair witness

[Both authored layouts independently validate](benchmarks/results/h5-larger-return-witness-20261018.md).
The incoming 30x40 and 30x50 rectangles total 2,700 mm2; the three 30x31
returns total 2,790 mm2. All seven parts and every metric remain identical,
including 19,700 mm2 charged material. Eight conservative height bounds rule
out either chosen incoming part alone under the stated filler constraint.
The complete returned set violates the current proposal-area inequality,
showing that inequality is not necessary for a valid nonincreasing-material
exchange. No optimizer run occurs. A failing original-runtime regression,
complete correctness checks and unchanged quality gates are still required.
Production and reserved inputs are unchanged; H2/H5 remain open at 60%.
''')
append(root/'.gitattributes','\nbenchmarks/results/h5-larger-return-witness-20261018/** -text -whitespace\n')
shutil.copyfile(__file__,out/'record-outcome.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'valid':4,'sample_area_rejections':1721,'mixed_area_rejections':575,'neutral_paired_attempts':7,'witness_valid':True,'production_changed':False}))
