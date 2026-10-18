from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-free-return-observer-preparation-20261018'
r=json.loads((out/'checks.json').read_bytes());assert r['all_qualified']
note=f'''**N4 actual return-seed observation preparation, 2026-10-18:** the [isolated diagnostic](../benchmarks/results/h5-free-return-observer-preparation-20261018.md)
records actual contained/placed return poses, original source members, charged
work, repair losses and validated material outcomes including acceptance. It
reconstructs the failed candidate exactly after removing observations; all 137
tests remain unchanged and pass, as do lint and build. Sixteen authored cases,
{r['frozen_CLI_baseline_checks']} frozen-CLI baselines, {r['frozen_CLI_trial_checks']} trial validations,
twelve exact parent branch witnesses and 44 malformed-record checks qualify the
reader. Four serial mechanical diagnostics are planned; no measurement has begun.
Logging can affect wall trajectories and supports no quality claim. No production
change, reserved-input access or H5 credit. H2/H5 remain open at 60%.
'''
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 free-space-return outcome, 2026-10-18:**';assert s.count(needle)==1;p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=(root/'BENCHMARKS.md').read_bytes();assert prior==subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify actual return-seed observation\n\n'+note.replace('../benchmarks/','benchmarks/'))
append(root/'.gitattributes','\nbenchmarks/results/h5-free-return-observer-preparation-20261018/** -text -whitespace\nbenchmarks/results/h5-free-return-observer-20261018/** -text -whitespace\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record.py')
print('Recorded diagnostic qualification; no quality rerun or production change.')
