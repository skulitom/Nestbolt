from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exchange-failure-observer-preparation-20261018'
checks=json.loads((out/'checks.json').read_bytes());assert checks['all_qualified']
assert (root/'benchmarks/results/h5-exchange-failure-observer-20261018/plan.json').exists()
note=f'''**N4 exchange-failure observation, 2026-10-18:** [the isolated failure-detail observer qualifies](../benchmarks/results/h5-exchange-failure-observer-preparation-20261018.md).
All 130 optimized tests and strict code checks pass. The original short-circuit
conditions, clock reads and work charges are unchanged; extra loss/pose or
validated-trial data is recorded only inside existing failed branches.
Sixteen authored cases, 35 public baseline checks, twelve exact parent branch
witnesses, 34 malformed-record rejections and four synthetic parser cases pass.
The same two serial panel searches retain both kerfs, seed zero and 60 seconds.
Logging can change wall trajectories; no quality comparison or integration.
The committed scope requires independent checks of captured trials. H2/H5
remain open at 60%.
'''

def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 boundary-pair diagnosis, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify exchange failure reasons\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record.py')
print('Recorded qualified observation and two-case scope before measurement.')
