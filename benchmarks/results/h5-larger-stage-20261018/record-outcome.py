"""Record phase costs and independently checked exchange/fill states."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-larger-stage-20261018'
load=lambda p:json.loads(p.read_bytes())
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json');mid=load(out/'intermediate-layout-checks.json');phase=load(out/'phase-timings.json');ex=load(out/'observed-exchanges.json');r=load(out/'results.json')
assert v['all_original_archives_verified'] and v['all_traces_verified'] and v['valid']==4
assert audit['all_holes_reserved'] and audit['cases']==4 and mid['all_checks_passed'] and mid['layouts']==4
assert ex['summary']['outcomes']=={'accepted':2,'source_repair_failed':14,'neutral_inventory_rejected':7}
assert len(phase['records'])==4
panel=[p for p in phase['records'] if p['job']=='m-mechanical-panel-hardware'];large=[p for p in phase['records'] if p['job']=='m-mechanical-large-plates']
assert len(panel)==len(large)==2
neutral=[a for a in ex['attempts'] if a['outcome']=='neutral_inventory_rejected']
assert len(neutral)==7 and all(a['receiver_initial_loss']==a['source_initial_loss']==0 for a in neutral)
assert all(a['receiver_elapsed']<.0001 and a['source_elapsed']<.0001 for a in neutral)
assert all(p['immediate_material']['fill_delta']==0 for p in large)
assert abs(large[0]['immediate_material']['exchange_delta']+86.418)<1e-6
assert abs(large[1]['immediate_material']['exchange_delta']+40.2735)<1e-6
generations=load(out/'observed-generations.json')['records'];assert len(generations)==4
assert all(not g['mixed'] and g['area_rejected']==0 and not g['deadline_reached'] for g in generations)
source=root/'output/h5-larger-return-probe-20261018/candidate/crates/core/src/sheets/vstrip/exchange.rs'
text=source.read_text(encoding='utf-8');start=text.index('                    let mut trial = JLayout::from_snapshot');end=text.index('                    sep.layout = trial;',start)
next_step='''Panel hardware retains six proposals for the first same-item pair at each
kerf. Seven attempted paired proposals have zero initial repair loss, repair
durations below 0.0001 seconds, and unchanged inventory/material. Their full
validations cost 0.3666222 and 0.2986677 seconds in aggregate. The group phase
then has insufficient reserved time for the later pair choices; no mixed pair
is generated. Later single proposals spend 0.5481800 and 0.5911573 seconds in
failed source repairs. Construction and paired sampling each take only a few
milliseconds here. These are observed durations with logging, not minimum
time requirements or speed comparisons.

The next narrow check is whether any expensive neutral trial is exactly the
same physical state as its validated incumbent: the same original item index,
full transform (including reflection), multiplicity and sheet location. Same
inventory or equal material alone is insufficient. First observe exact state
equivalence on these rejected trials and cover key-order changes, distinct
original identities, changed poses and duplicate counts in authored tests.
Only a proven identical state could be rejected before repeated validation;
every changed state and every accepted exchange must retain the full original
geometry/material checks. Do not use geometric tolerances, rounded poses or
an unchecked material estimate to bypass those checks.

Large-plate acceptances leave 0.9653642 and 0.5524092 seconds of their original
exchange opportunity after filling, while immediate material improves by only
86.4180 and 40.2735 mm2. Filling does not change those material totals. This
identifies unused time after acceptance, but does not prove another useful
swap exists. Any later consecutive-exchange experiment must retain the shared
budget, valid incumbent and cycle protection. The original five failed pilot
material comparisons remain authoritative; neither observation is a quality
gain or justification for integration.
'''
write(out/'source-review.json',{'source':str(source.relative_to(root)),'source_sha256':sha256(source.read_bytes()).hexdigest(),
 'trial_validation_and_neutral_guard':text[start:end],'line':text[:start].count('\n')+1,'next_step':next_step,
 'exact_neutral_geometry_observed':False,'production_changed':False,'new_searches':0,'quality_claim':False})
lines=['\n\n## Observed phase costs and intermediate geometry','',
 f"All four final layouts and four intermediate layouts independently validate. Filled-outer audits check {audit['same_sheet_pairs']+mid['same_sheet_pairs']:,} same-sheet pairs with the unchanged 1e-7 mm clearance tolerance.",'',
 '| Job | Kerf mm | Invocation s | Initial validation s | Choice construction s | Pair generation s | Attempt setup s | Source repair s | Trial validation s |',
 '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
for p in phase['records']:
    s=p['seconds'];lines.append(f"| {p['job']} | {p['kerf_mm']} | {p['total_elapsed_seconds']:.6f} | {s['baseline_validation']:.6f} | {s['choice_construction']:.6f} | {s['paired_generation']:.6f} | {s['attempt_setup']:.6f} | {s['source_repair']:.6f} | {s['proposal_validation']:.6f} |")
lines += ['','The [complete timing record](h5-larger-stage-20261018/phase-timings.json) also retains receiver repair, trial reconstruction and unassigned/observation overhead. Recorded scopes are disjoint and reconcile with each invocation duration.','',
 '| Kerf mm | Before exchange, mm2 | After exchange, mm2 | After fill, mm2 | Remaining after fill, s |',
 '| --- | ---: | ---: | ---: | ---: |']
for p in large:
    m=p['immediate_material'];remaining=next(x['remaining'] for x in mid['records'] if x['job']==p['job'] and x['kerf_mm']==p['kerf_mm'] and x['stage']=='after_fill')
    lines.append(f"| {p['kerf_mm']} | {m['before_exchange']:.4f} | {m['after_exchange']:.4f} | {m['after_fill']:.4f} | {remaining:.7f} |")
lines += ['','[Every saved intermediate layout and independent check](h5-larger-stage-20261018/intermediate-layout-checks.json) is retained. Material change during filling was measured without assuming nonincrease.','',next_step,
 '[Source review and next check](h5-larger-stage-20261018/source-review.json). H2/H5 remain open at 60%.','']
append(out.parent/(out.name+'.md'),'\n'.join(lines))
note='''**N4 larger-return diagnosis, 2026-10-18:** [all four final and four intermediate layouts validate](../benchmarks/results/h5-larger-stage-20261018.md).
The filled-outer audits check 23,542 same-sheet pairs. Of 23 attempts, two
accept, fourteen fail source repair and seven are neutral inventory rejections.
Panel paired repairs start with zero loss; repeated validation costs 0.367 /
0.299 seconds, and no mixed pair is generated. Large-plate exchanges save only
86.418 / 40.2735 mm2 immediately; filling changes neither total and leaves
0.965 / 0.552 seconds of the original exchange opportunity. Next verify whether
neutral trials preserve exact original-item poses before considering an early
rejection. Equal inventory/material alone cannot justify skipping validation.
These instrumented observations do not replace the five failed pilot pairs;
no integration or H5 credit, and completion remains 60%.
'''
status=root/'docs/STATUS.md';old=status.read_text(encoding='utf-8');begin=old.index('**N4 larger-return diagnosis preparation, 2026-10-18:**');end=old.index('**N4 larger-return outcome, 2026-10-18:**',begin)
status.write_text(old[:begin]+note+'\n'+old[end:],encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Observe larger-return validation costs and unused time\n\n'+note.replace('../benchmarks/','benchmarks/')+f'\nThe four serial observations take {r["wall_seconds"]/60:.3f} minutes. Original archives, source/runner/input guards, all counters, and independent metrics/quantities verify. Full phase timings and every saved intermediate layout remain available. The original compiler failure is retained. No unchanged quality rerun, gate change or reserved access.\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-outcome.py')
print(json.dumps({'final_layouts_valid':4,'intermediate_layouts_valid':4,'filled_outer_pairs':audit['same_sheet_pairs']+mid['same_sheet_pairs'],'next':'verify exact state equivalence before any early rejection'}))
