from pathlib import Path
import json
import shutil
import subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-complete-stage-diagnosis-20261017'
load=lambda p:json.loads(p.read_bytes())
v=load(out/'verification.json');s=load(out/'observed-stages.json')
assert v['valid']==4 and v['all_original_archives_and_traces_verified']
assert s['aggregate_attempt_outcomes']=={'all':{'source_repair_failed':23},'complete':{'source_repair_failed':23},'partial':{}}
assert s['sampling_totals']['multi_eligible_not_smaller']==427
def append(name,text):
    with (root/name).open('ab') as f:f.write(text.encode('utf-8'))
append('benchmarks/results/h5-complete-stage-diagnosis-20261017.md','''

## Observed bottleneck

All 23 actual attempts are complete sets. Receiving-sheet repair succeeds in
every attempt; returning the displaced group to the last sheet fails in all 23
within the unchanged repair budget. No partial sets are attempted and no
exchanges are accepted in these four traces. Sampling observes 427 eligible
complete sets with equal or larger combined area and zero smaller complete sets.

The next concrete investigation is return-group initialization and repair within
the existing constraints. These observations establish neither sufficient room
for a successful exchange nor mathematical impossibility. Changing more search
time or replaying the same candidate is not supported by this evidence. The
failed paired pilot remains the quality result; production remains unchanged.
''')
append('BENCHMARKS.md','''

## 2026-10-17 — Complete groups reach the return-sheet repair and fail there

[Four diagnostic traces](benchmarks/results/h5-complete-stage-diagnosis-20261017.md)
validate every saved layout/export and original-job metrics/quantities. Every
immutable ZIP, trace and counter passes verification. All 23 actual attempts
are complete blocker sets; all pass receiving-sheet repair and fail return-sheet
repair within the unchanged budget. No partial attempts or acceptances occur.
Sampling records 427 eligible complete sets of equal/larger combined area, zero
smaller complete sets, among 1,108 examined samples (451 over-three-collision
and 38 non-item-collision observations; categories can overlap).

The session lasts 243.2476863 seconds, serial CCD0 CPU 8. Instrumentation can
perturb wall deadlines, so this is stage diagnosis only; it cannot replace the
72-outcome failed quality comparison. Next investigate return-group placement
and repair, preserving incumbent geometry, quantities and original material
limits. No global infeasibility claim, production integration, reserved-input
access or gate closure. H2/H5 remain open; completed weight stays 60%.
''')
note='''

**N4 return-stage diagnosis, 2026-10-17:** [all four traced outputs validate](../benchmarks/results/h5-complete-stage-diagnosis-20261017.md).
All 23 actual attempts move complete blocker sets, pass receiving-sheet repair
and fail return-sheet repair within the existing budget. There are 427 eligible
equal/larger-area samples and no smaller complete sets. No partial attempt or
acceptance occurs. Source/binary/input/trace integrity is verified. Next inspect
how returned groups are placed and repaired; these observations do not prove
feasibility or impossibility, or replace the failed quality pilot. Production
and gate limits remain unchanged; H2/H5 are open at 60%.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(name,note)
p=root/'docs/STATUS.md';text=p.read_text(encoding='utf-8');needle='**N4 latest outcome, 2026-10-17:**'
assert text.count(needle)==1
text=text.replace(needle,'''**N4 next target, 2026-10-17:** [four traced outputs validate](../benchmarks/results/h5-complete-stage-diagnosis-20261017.md),
but all 23 complete-set attempts fail return-sheet repair after the receiving
sheet succeeds. Investigate return-group initialization/repair within the
existing budget and material guard. This locates a stage, not an impossibility
proof or quality gain; the failed paired comparison remains the outcome.

'''+needle)
p.write_text(text,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print('Recorded all 23 complete-set return repair failures; no integration or gate changes.')
