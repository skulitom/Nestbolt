"""Document a zero-search preflight repair before the amended plan starts."""
from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-boundary-pair-pilot-20261018'
checks=json.loads((out/'preflight-recovery/checks.json').read_bytes())
assert checks['all_checks_pass'] and len(checks['tests'])==6 and not checks['measurement_started_before_recovery']
assert not (out/'opened.json').exists()
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
note='''**N4 boundary-pair preflight recovery, 2026-10-18:** the first launch stops
before any measurement because the old balanced-diagnostic PID now belongs to
`svchost.exe`, whose command line is protected. Its creation time is later than
the original diagnostic's recorded start, proving PID reuse. The old runner
and committed plan are preserved in [the recovery record](../benchmarks/results/h5-boundary-pair-pilot-20261018/preflight-recovery/checks.json).
The guard now checks process creation time before attempting the command
line. Six checks cover missing/reused processes, active original-runner
rejection, the existing different-command behavior and both inaccessible
identity cases. Unresolved identity still fails closed. The two old H4 PIDs
are absent. Block, scoring, case and measurement functions are AST-identical;
no candidate, budget, input or scoring change and zero searches before repair.
The amended plan is committed before its first measurement. H2/H5 remain open
at 60%.
'''
def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Preserve a PID-reuse preflight failure\n\n'+note.replace('../benchmarks/','benchmarks/'))
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 exact boundary-copy diagnosis, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
append(root/'benchmarks/results/h5-boundary-pair-preparation-20261018.md','\n\n## Preflight amendment before any search\n\n'+note.replace('../benchmarks/results/',''))
(out/'preflight-recovery/README.md').write_text('# Preflight recovery before the first search\n\n'+note.replace('../benchmarks/results/h5-boundary-pair-pilot-20261018/preflight-recovery/checks.json','checks.json'),encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'preflight-recovery/record.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print('Recorded the preserved preflight failure and qualified amendment; no searches have started.')
