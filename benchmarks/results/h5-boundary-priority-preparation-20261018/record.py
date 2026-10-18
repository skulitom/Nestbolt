from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-boundary-priority-preparation-20261018'
assert json.loads((out/'checks.json').read_bytes())['all_functional_checks_pass']
assert (root/'benchmarks/results/h5-boundary-priority-pilot-20261018/plan.json').exists()
note='''**N4 boundary-priority preparation, 2026-10-18:** [all 126 optimized tests pass](../benchmarks/results/h5-boundary-priority-preparation-20261018.md),
with 123 prior tests unchanged. The isolated candidate orders incoming parts
by upper extent before area, retaining stable ties and the existing bounded
pair generators. Selected pairs keep their original member anchor order. Budgets, sampling, repairs, work charges and every full
acceptance check are unchanged. Two original ordering regressions fail as
expected and are preserved; all three new tests pass afterwards. The first
revision also exposes three existing exchange regressions; preserving pair
anchors resolves them with unchanged assertions and retained failures. The order
fixture and twelve rejection-boundary outcomes pass 25 frozen-CLI checks.
Strict lint/build, public parity/replay, five pilot tests and exact source
reconstruction pass. The unchanged 72-outcome plan is committed before
measurement. No quality or integration claim; H2/H5 remain open at 60%.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 height-setting part diagnosis, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify boundary-priority exchange ordering\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record.py')
print('Recorded qualified ordering and unchanged paired pilot scope.')
