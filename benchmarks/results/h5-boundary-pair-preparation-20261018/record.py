from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-boundary-pair-preparation-20261018'
assert json.loads((out/'checks.json').read_bytes())['all_functional_checks_pass']
assert (root/'benchmarks/results/h5-boundary-pair-pilot-20261018/plan.json').exists()
note='''**N4 boundary-pair preparation, 2026-10-18:** [all 130 optimized tests pass](../benchmarks/results/h5-boundary-pair-preparation-20261018.md),
including all 126 prior tests unchanged. The isolated candidate includes the
two highest source members first in the appropriate same-item or mixed pair
list, removes duplicate pairs and retains the six-plus-six caps and remaining
nearby alternatives. Original pair anchors, repairs, budgets, work charges and
all full acceptance checks remain. Three expected failures are preserved.
Independent original-contour checks confirm both highest physical copies in
same-item and mixed-item witnesses. Those and twelve rejection-boundary cases
pass 26 frozen-CLI checks. Strict lint/build, public parity/replay, source
reconstruction and five pilot harness checks pass. The unchanged 72-outcome
plan is committed before measurement. No quality claim; H2/H5 remain open at 60%.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 exact boundary-copy diagnosis, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify including both highest source members\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record.py')
print('Recorded qualified pair coverage and the unchanged paired pilot scope.')
