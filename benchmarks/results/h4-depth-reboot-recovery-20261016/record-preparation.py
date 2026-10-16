"""Record the servicing interruption and committed-scope recovery before measurement."""
from pathlib import Path
import json
import subprocess

root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h4-depth-reboot-recovery-20261016'
assert (out/'plan.json').exists() and not (out/'opened.json').exists()
workflow=subprocess.check_output(['gh','run','view','38857882488','--json','status,conclusion,headSha,jobs,url'],cwd=root)
ci=json.loads(workflow)
assert ci['headSha']=='21835bad284fd6fef494a3639e214db0cd2c12bd'
assert ci['conclusion']=='success' and len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
(out/'followup-ci.json').write_bytes(workflow)
(out/'record-preparation.py').write_bytes(Path(__file__).read_bytes())

path=root/'docs/RELEASE_READINESS.md';text=path.read_text(encoding='utf-8')
before='''- [The full comparison plan](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
  fixes all 67 union jobs, seeds 0–2 and 60 seconds in native/Chrome/Firefox:
  603 new outcomes plus 195 verified frozen-v1 baselines. Its original bounds
  and every attempt must pass before scale measurements begin.
'''
after='''- [The original full comparison](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
  was interrupted by a Windows servicing restart after 201 native and 201 Chrome
  valid outcomes. Firefox had started but saved no outcomes; scale never began.
  The [recovery plan and preserved interruption](../benchmarks/results/h4-depth-reboot-recovery-20261016.md)
  retain all 402 completed current-build outcomes plus 195 frozen-v1 baselines,
  then run the missing 201 Firefox outcomes with the unchanged build, jobs,
  seeds, budgets and limits. Native and Chrome quality bounds pass; full H4
  acceptance still requires Firefox, scale and export review. The original
  session is never relabelled as complete or passing.
'''
assert before in text;text=text.replace(before,after)
before='''  runner inputs match tested commit `23442be`. Its newer main CI run is still
  underway at this checkpoint. Full current quality/scale/export confirmation
  remains required before publishing.
'''
after='''  runner inputs match tested commit `23442be`. Its newer main CI run
  [38857882488](https://github.com/skulitom/Nestbolt/actions/runs/38857882488)
  also passes all six jobs. Full recovered quality/scale/export confirmation
  remains required before publishing.
'''
assert before in text;text=text.replace(before,after)
path.write_text(text,encoding='utf-8',newline='\n')
path=root/'docs/STATUS.md';text=path.read_text(encoding='utf-8')
before='''The [fresh full matrix](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
is now running with unchanged limits. Its [conditional scale/export sequence](../benchmarks/results/h4-preview-depth-scale-plan-20261016/plan.json)
waits for a quality pass. [All three downloaded packages and the Windows MCPB]'''
after='''The [full matrix](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
was interrupted by Windows servicing at 06:00 UTC after 201 native and 201
Chrome valid outcomes; Firefox saved no outcomes and scale never began.
The [recorded recovery](../benchmarks/results/h4-depth-reboot-recovery-20261016.md)
retains every completed result and the original interruption, then runs only
the missing Firefox phase under the unchanged limits. Native and Chrome
quality bounds pass; Firefox, scale/export checks and final H4 review remain
required. [All three downloaded packages and the Windows MCPB]'''
assert before in text;path.write_text(text.replace(before,after),encoding='utf-8',newline='\n')

path=root/'BENCHMARKS.md';before=path.read_bytes()
assert before.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with path.open('a',encoding='utf-8',newline='\n') as f:
    f.write('''

## 2026-10-16 — Windows servicing interrupted H4; preserve and recover Firefox

[The recovery record](benchmarks/results/h4-depth-reboot-recovery-20261016.md)
preserves the original session as interrupted, never completed or passing.
Windows servicing requested restart at 05:59:24 UTC; shutdown/boot followed
at 06:00:07/06:00:33. Both original processes are absent. All 201 native and
201 Chrome outcomes completed and independently validate; Firefox 157.0 had
started its first batch but saved no outcome or error. The precise number of
started workers is unknown. No scale run began. Original files and the one-use
marker are unchanged; all evidence plus the exact build is archived with CRC,
every-member SHA-256 and byte-length verification.

All original application, executable/site/input/runner/environment guards
still match. The recovery retains all 402 completed current-build outcomes
and 195 frozen-v1 outcomes without score selection, then runs the missing
201 Firefox outcomes once at the original settings and limits. The new boot
and OS environment are explicit; the original four-hour session is not
retroactively extended. A separate one-hour recovery cap applies. Native's
median is +0.000614% versus frozen v1; Chrome's subset median +0.851159% and
worst +2.455588% meet the original limits. Full Firefox, scale, all-placement
curve fidelity and final requirement review remain required. The unopened
common-line pilot waits. No completed result is rerun or replaced, no
reserved input is opened, and no release or gate closure occurs. Completion
stays 45%. Main commit `21835ba` has also passed all six hosted checks.
''')
assert path.read_bytes().startswith(before)
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\nbenchmarks/results/h4-depth-reboot-recovery-20261016/** -text -whitespace\n')
print('Recorded the original interruption and recovery plan; no new measurement started.')
