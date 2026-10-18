"""Record the actual seed and acceptance diagnosis, preserving all failed paths."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-free-return-observer-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
r=load(out/'results.json');v=load(out/'verification.json');g=load(out/'layout-checks.json');d=load(out/'seed-detail-checks.json');obs=load(out/'observed-exchanges.json')
assert v['valid']==4 and v['all_original_archives_verified'] and g['all_checks_passed'] and d['all_checks_passed']
assert d['reason_counts']=={'accepted':2,'material_increased':5,'source_loss_positive':17}
assert d['returned_members']==43 and d['translated_return_members']==d['lowered_return_members']==0
assert d['validated_material_trials']==7 and d['accepted_trials']==2
assert all(s['work_delta']['evaluations']>0 for s in d['sources'])
assert all(s['after_repair']['pair_violations'] for s in d['sources'] if s['reason']=='source_loss_positive')
probe=root/'output/h5-free-return-probe-20261018/candidate';caller=probe/'crates/core/src/sheets/vstrip.rs';exchange=probe/'crates/core/src/sheets/vstrip/exchange.rs'
source=caller.read_text(encoding='utf-8').split('#[cfg(test)]',1)[0];runtime=exchange.read_text(encoding='utf-8').split('#[cfg(test)]',1)[0]
assert source.count('self.directed_exchange(')==1 and 'if !filled {' in source and 'filled = true;' in source
assert 'let exchange_until = (t + 1.2).min(budget);' in source and runtime.count('return Ok(1);')==1
accepted=[t for t in d['trials'] if t['outcome']=='accepted'];reductions=[]
for t in accepted:
 baseline=next(b for b in g['baselines'] if b['job']==t['job'] and b['kerf_mm']==t['kerf_mm'] and b['invocation']==t['invocation'])
 after=next(s for s in t['sheets_with_original_height_owners'] if s['sheet']==baseline['credited_sheet'])
 change=after['used_height']-baseline['credited_height'];assert -.1<change<0
 reductions.append({'job':t['job'],'kerf_mm':t['kerf_mm'],'material_change_mm2':t['material_change'],
  'credited_height_change_mm':change,'new_height_families':sorted({p['part_id'] for p in after['owners']})})
followup=('The bounded free-space seed stage changed none of the 43 observed return poses despite charged evaluations. These four diagnostic trajectories therefore supply no successful new seed witness, and do not justify expanding its sample count blindly. '
 'The two large-plate exchanges are independently valid but save less than 0.1 mm of charged height each; a cog or another insert remains height-setting. Source review shows that the directed step is invoked once per feasible window and returns immediately after its first accepted exchange. '
 'The next distinct hypothesis is bounded continuation after a strictly material-improving exchange, using the same original absolute exchange deadline and original total search budget, with a small explicit cap and stopping on no acceptance or no strict material gain. '
 'Keep the original per-exchange independent geometry/material guards, exact quantities, filled-hole reservation, and disabled/expired behavior. Qualify authored multi-success and rollback/deadline cases before a newly committed matched pilot. '
 'This targets the observed early return after tiny gains; it does not resolve the seventeen panel source-repair failures by itself, prove that another exchange fits, or establish H5 feasibility. All original H5 limits and the complete 13-job requirement remain. Do not repeat the unchanged failed quality pilot or access reserved geometry.')
review={'diagnostic_results_sha256':digest(out/'results.json'),'detail_checks_sha256':digest(out/'seed-detail-checks.json'),
 'caller_source_sha256':digest(caller),'exchange_source_sha256':digest(exchange),'one_directed_call_per_window':True,
 'returns_after_first_acceptance':True,'same_original_exchange_cap_seconds':1.2,'accepted_height_changes':reductions,
 'lower_return_seed_witnesses':0,'panel_source_failures_remain':17,'followup':followup,'new_quality_claim':False,'production_changed':False,'H5_complete':False}
(out/'source-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
evals=[s['work_delta']['evaluations'] for s in d['sources']]
doc=f'''# Actual return seeds and exchange outcomes — 2026-10-18

**All four diagnostic outputs validate.** The added free-space seed stage
changes none of the 43 observed returned poses. This explains what happened
in these observations; it does not reconstruct the earlier pilot or measure
the seed stage's effect across all jobs and seeds.

The [committed plan](h5-free-return-observer-20261018/plan.json) fixes both
mechanical jobs, both kerfs, seed zero, 60 seconds and serial physical CCD0 CPU 8.
The failed candidate's search decisions, clock reads, work charges and guards
remain exact after removing the observation code. Logging may perturb wall
trajectories. The session takes {r['wall_seconds']:.3f} seconds.

| Job | Kerf mm | Attempts | Accepted | Positive source loss | Actual material increase |
| --- | ---: | ---: | ---: | ---: | ---: |
'''
for row in r['records']:
 reasons=row['diagnosis']['reason_counts'];doc+=f"| {row['job']} | {row['kerf_mm']} | {len(row['diagnosis']['attempt_rows'])} | {reasons.get('accepted',0)} | {reasons.get('source_loss_positive',0)} | {reasons.get('material_increased',0)} |\n"
doc+=f'''
The 24 attempts include twelve paired attempts; every attempt selects an actual
highest source copy, and twelve select all highest copies. All four final and
four baseline layouts pass original filled-outer checks over
{g['same_sheet_pairs']:,} same-sheet pairs. Original quantities, public exports,
metrics, CRCs and every archive member hash pass.

The seed stage incurs {min(evals):.0f}–{max(evals):.0f} charged evaluations per
attempt, so it was not wholly skipped. Every captured post-seed pose still
matches its contained fallback exactly. Counts are per attempt and do not
prove every individual member completed a full sampling loop. Original
rotations/reflection and unchanged source poses match their recorded baselines.

All seven material-bearing trial layouts independently validate and their
material values reconstruct exactly from original geometry. The two accepted
large-plate trials save 28.887 and 132.567 mm², respectively. Each reduces charged
height by less than 0.1 mm; a cog or another insert remains height-setting.
The five panel trials increase material by 0.0025–18.925 mm² and are correctly
rejected under the unchanged exact guard. None is classified merely as expiry.
All seventeen positive-loss source repairs retain independently observed
filled-outer violations. Their failed snapshots remain failures, not outputs
presented as valid. Snapshot inspection uses nominal stock bounds and original
filled contours; it does not reconstruct cropped proxy boundaries or loss weights.

The geometry audit initially retained the older two-case terminal assertion
after inspecting all four cases. Its failure and checker remain. Only the
expected count was corrected; all four captured CLI checks were reused without
repeating a search or validation, and geometry assertions stayed unchanged.

## Next constraint

{followup}

Production, release, reserved inputs and completed gate weights are unchanged.
**H2/H5 remain open; completed milestone weight is 60%.**

[Archive verification](h5-free-return-observer-20261018/verification.json),
[baseline/final geometry](h5-free-return-observer-20261018/layout-checks.json),
[actual seed and repair geometry](h5-free-return-observer-20261018/seed-detail-checks.json),
[source review and next hypothesis](h5-free-return-observer-20261018/source-review.json),
[preserved audit correction](h5-free-return-observer-20261018/layout-terminal-count-repair.json),
[full observations](h5-free-return-observer-20261018/results.json).
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
note='''**N4 actual return-seed diagnosis, 2026-10-18:** [four original-job outputs validate](../benchmarks/results/h5-free-return-observer-20261018.md).
The seed stage incurs work but changes none of 43 observed return poses. Of 24
attempts, two valid large-plate exchanges save only 28.887/132.567 mm², seventeen
panel source repairs retain positive loss and actual filled-outer violations,
and five valid panel trials increase material and are correctly rejected.
Four baselines/finals pass 37,119 filled-outer pair checks; all seven captured
material trials pass independent validation and exact material reconstruction.
The one-success-per-window caller motivates a bounded continuation experiment
under the same absolute deadline, after authored correctness checks. This is
not yet implemented and does not solve the panel repair failures. Original
limits, failed evidence, production and reserved inputs remain; H2/H5 stay open at 60%.
'''
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
prior=(root/'BENCHMARKS.md').read_bytes();assert prior==subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Actual return-seed and material diagnosis\n\n'+note.replace('../benchmarks/','benchmarks/')+'\n'+followup+'\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');start=s.index('**N4 actual return-seed observation preparation, 2026-10-18:**');end=s.index('**N4 free-space-return outcome, 2026-10-18:**',start)
p.write_text(s[:start]+note+'\n'+s[end:],encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record-outcome.py');shutil.copyfile(root/'output/prepare_h5_free_return_observer_finish.py',out/'prepare-finish.py')
print(json.dumps({'accepted_height_changes':reductions,'translated_return_members':0,'source_failures':17,'next':'Bounded continuation after strict material improvement within the original absolute deadline'}))
