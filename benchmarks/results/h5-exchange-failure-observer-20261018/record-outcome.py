"""Record reviewed exchange failure causes and independently checked trial geometry."""
from pathlib import Path
from hashlib import sha256
import json, shutil, subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-exchange-failure-observer-20261018'
load=lambda p:json.loads(p.read_bytes())
v=load(out/'verification.json');a=load(out/'layout-checks.json');d=load(out/'failure-detail-checks.json')
r=load(out/'results.json');observed=load(out/'observed-exchanges.json')['summary']
assert v['valid']==2 and v['all_traces_verified'] and v['all_original_archives_verified']
assert a['all_checks_passed'] and d['all_checks_passed'] and d['all_trial_metrics_exact'] and d['all_trial_material_reconstructed']
interpretation=load(out/'interpretation.json')
assert interpretation['failure_detail_checks_sha256']==sha256((out/'failure-detail-checks.json').read_bytes()).hexdigest()
assert interpretation['failure_reason_counts']==d['failure_reason_counts'] and interpretation['quality_claim'] is False
followup=interpretation['followup']
reasons=d['failure_reason_counts']
finding=', '.join(f'{count} {reason.replace("_"," ")}' for reason,count in sorted(reasons.items()))
lines=['# Exchange failure reasons — 2026-10-18','',f'**Observed failure causes: {finding}.**','',
    'Two serial panel-hardware diagnostics retain both kerfs, seed zero,',
    '60 seconds and physical CCD0 CPU 8. The observer only adds data after',
    'the original rejection decisions; every condition, clock read, work',
    'charge and original test remains. Logging can change wall trajectories,',
    'so this is not a quality or speed comparison.','',
    f"Both final layouts and {a['baseline_layouts']} baselines independently validate.",
    f"All {d['validated_material_trials']} captured material/deadline trials also validate,",
    'reproduce their original metrics exactly, reserve all filled outer contours,',
    'and reproduce material by a separate rectangular-stock height calculation.',
    f"The original/final audit checks {a['same_sheet_pairs']:,} filled-outer pairs;",
    f"captured trial checks add {sum(x['same_sheet_pairs'] for x in d['trials']):,} pairs.",
    'Quantities, exact selected physical poses, original archives, all member',
    'hashes and source/binary guards pass. The 72-run quality pilot remains',
    'failed and is not replaced by these observations.','',
    '| Kerf mm | Choice | Failure reason | Before material mm² | Trial material mm² | Change mm² |',
    '| --- | ---: | --- | ---: | ---: | ---: |']
for row in d['trials']:
    lines.append(f"| {row['kerf_mm']} | {row['choice_index']} | {row['reason']} | {row['baseline_material']:.6f} | {row['trial_material']:.6f} | {row['material_change']:+.6f} |")
lines+=['',f"The {d['source_failures_inspected']} saved failed sources are diagnostic intermediate states.",
    'Their original-part inventory is checked independently. Original filled',
    'polygons are inspected before and after repair for overlaps, clearance',
    'and nominal stock bounds. This does not reconstruct the cropped separator',
    'boundary or its weighted proxy loss. Positive recorded loss proves that',
    'the source repair condition failed; it neither proves global infeasibility',
    'nor excludes a concurrent deadline expiry. Zero recorded loss would identify',
    'the deadline side of that original short-circuit condition.','',followup,'',
    '[Committed scope](h5-exchange-failure-observer-20261018/plan.json),',
    '[archive verification](h5-exchange-failure-observer-20261018/verification.json),',
    '[baseline and final audit](h5-exchange-failure-observer-20261018/layout-checks.json),',
    '[independent failed-trial and source audit](h5-exchange-failure-observer-20261018/failure-detail-checks.json).','',
    '**H2/H5 remain open; completed milestone weight is 60%.** No production',
    'integration, reserved-input access, changed threshold or release.','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
note=f'''**N4 exchange-failure diagnosis, 2026-10-18:** [the focused cause audit is complete](../benchmarks/results/h5-exchange-failure-observer-20261018.md).
Recorded causes are {finding}. All {d['validated_material_trials']} captured final-trial
layouts validate independently, with exact metrics and independently rebuilt
material. Original/final geometry and every selected physical pose also pass.
Failed source snapshots remain diagnostic states. No quality rerun or
integration follows from these observations; H2/H5 remain open at 60%.
'''
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8')
start=s.index('**N4 exchange-failure observation, 2026-10-18:**');end=s.index('**N4 boundary-pair diagnosis, 2026-10-18:**',start)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
p.write_text(s[:start]+note+'\n'+s[end:],encoding='utf-8',newline='\n')
def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as stream:stream.write(text)
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Distinguish exchange rejection causes\n\n'+note.replace('../benchmarks/','benchmarks/')+'\n'+followup+'\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-outcome.py')
print(json.dumps({'causes':reasons,'validated_material_trials':len(d['trials']),'source_failures_inspected':len(d['sources'])}))
