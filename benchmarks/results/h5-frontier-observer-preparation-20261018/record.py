from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-frontier-observer-preparation-20261018'
checks=json.loads((out/'checks.json').read_bytes());assert checks['all_qualified']
assert (root/'benchmarks/results/h5-frontier-observer-20261018/plan.json').exists()
note=f'''**N4 height-setting part observation, 2026-10-18:** [the isolated diagnostic qualifies](../benchmarks/results/h5-frontier-observer-preparation-20261018.md).
All 123 existing optimized tests pass. The observer records original part
families for available, visited and attempted exchange choices alongside the
validated public baseline. It changes no decision, work charge or budget.
Sixteen authored cases, sixteen malformed-record rejections and
{checks['frozen_CLI_baseline_checks']} frozen-CLI baseline checks pass. Twelve parent branch witnesses
and their counters match exactly; every formatted source file reconstructs.
Two serial panel diagnostics retain both kerfs, seed zero, 60 seconds and
physical CCD0 CPU 8. Logging can affect wall trajectories, so this is not a
quality comparison. No new selector, integration or H5 credit; H2/H5 stay open
at 60%. The plan is committed before measurement.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 material-profile rejection outcome, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify height-setting part observation\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record.py')
print('Recorded qualified observation and two-case scope before measurement.')
