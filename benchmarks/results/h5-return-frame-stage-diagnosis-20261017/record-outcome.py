from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-return-frame-stage-diagnosis-20261017'
load=lambda p:json.loads(p.read_bytes())
result=load(out/'results.json');verification=load(out/'verification.json');frames=load(out/'observed-frames.json')
assert result['all_valid'] and verification['all_original_archives_and_traces_verified'] and verification['valid']==4
attempts=[a for row in result['records'] for t in row['diagnosis']['traces'] for a in t['attempts']]
assert len(attempts)==23 and frames['frame_modes']=={'reciprocal':23}
assert all(a['outcome']=='source_repair_failed' and a['receiver_loss']==0 and a['source_loss']>0 and a['after_material'] is None for a in attempts)
assert all(a['victims']==a['blockers'] and all(m['actual_allowed'] and m['hypothetical_allowed'] for m in a['frame']['members']) for a in attempts)
ratios=[a['returned_area']/a['incoming_area'] for a in attempts]
assert min(ratios)>1
review={'attempts':len(attempts),'all_complete_sets':True,'all_reciprocal_frames_allowed':True,
    'all_receiver_repairs_succeed':True,'all_source_repairs_fail':True,'none_reach_trial_geometry_or_material_guard':True,
    'returned_to_incoming_area_ratio_range':[min(ratios),max(ratios)],
    'available_source_capacity_recorded':False,'larger_return_area_proves_infeasibility':False,
    'next_scope':'Inspect source capacity and initial placement of the larger returned group. Consider balanced groups in both directions only after an independent authored feasibility example; do not infer mechanical feasibility from area ratios.',
    'original_quality_pilot_repeated':False,'production_changed':False,'H5_complete':False}
(out/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
append(out.parent/(out.name+'.md'),f'''

## Reviewed result and next question

All **23 complete-set attempts use a permitted reciprocal frame**, with every
hypothetical and actual return orientation allowed. All receiving-sheet repairs
succeed; all return-sheet repairs fail. There are no orientation fallbacks,
partial attempts, accepted exchanges or trials reaching final independent
geometry/material acceptance in these observations. The previously demonstrated
0.0007 mm² guard rejection is not the failure stage here.

Returned area is {min(ratios):.6f}–{max(ratios):.6f} times incoming area. That helps
explain why mapping a group into one vacated part's frame may give repair a hard
starting point, but **does not prove the assignment impossible**: available
source-sheet capacity and every other source pose were not recorded. The next
scope is source capacity and group placement. A balanced exchange of several
parts in both directions needs an independent authored feasibility example
before any new heuristic or performance trial. Original limits remain unchanged.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-17 — Return-frame diagnostics isolate return-sheet repair again

[All four recorded outcomes validate](benchmarks/results/h5-return-frame-stage-diagnosis-20261017.md),
with original metrics/quantities, public exports, source/input guards, immutable
archive CRC/member hashes and matching solver/trace counters. The serial session
took {result['wall_seconds']:.3f} seconds. All 23 attempts are complete sets and
use permitted reciprocal frames; every receiver repair succeeds, then every
return-sheet repair fails. No partial set, orientation fallback or final trial
geometry/material check is reached. These observations rule out orientation
legality/fallback and the final material guard as their immediate failure stage.

Returned/incoming area ratios range from {min(ratios):.6f} to {max(ratios):.6f}.
This is not an impossibility proof: source capacity and all other source poses
are unrecorded. Investigate capacity and return-group placement, with a separate
authored example before considering balanced groups moving both ways. Tracing
can perturb wall deadlines; there is no new quality claim, repeated unchanged
pilot, production integration or relaxed limit. H2/H5 remain open at 60%.
''')
note='''

**N4 return-frame diagnosis, 2026-10-17:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-frame-stage-diagnosis-20261017.md)
record 23 complete-set attempts. Every reciprocal frame is permitted and every
receiving-sheet repair succeeds, but all return-sheet repairs fail. None reaches
the final geometry/material guard. Orientation fallback is not the immediate
cause in these observations. Next inspect source capacity and placement of the
larger returned groups; area ratios alone do not prove impossibility. A balanced
multi-part exchange needs a separate authored feasibility example first.
Original results/limits remain; no production change or H5 closure. Completion 60%.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 return-frame outcome, 2026-10-17:**';assert s.count(needle)==1
s=s.replace(needle,note.strip()+'\n\n**N4 preceding return-frame outcome, 2026-10-17:**');p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print(json.dumps(review))
