from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exact-reject-preparation-20261018'
assert json.loads((out/'checks.json').read_bytes())['all_functional_checks_pass']
assert (root/'benchmarks/results/h5-exact-reject-pilot-20261018/plan.json').exists()
note='''**N4 exact-state candidate preparation, 2026-10-18:** [all 117 optimized tests pass](../benchmarks/results/h5-exact-reject-preparation-20261018.md),
with all 113 prior tests unchanged. The new branch regression first fails
against the original runtime; its source, executable and log are preserved.
The candidate rejects only a complete exact internal-state match before
repeated validation. Changed states and all accepted exchanges retain the
original full validators, strict material guards and budgets. Twelve branch
outcomes pass 24 frozen-CLI checks; strict lint/build, ten public outcomes,
four CLI comparisons and five adversarial pilot checks also pass. The paired
72-outcome method is unchanged and committed before measurement. No quality
result, production integration or release claim; H2/H5 remain open at 60%.
All six hosted checks on main `924336a` have passed.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';text=p.read_text(encoding='utf-8');needle='**N4 exact-state diagnosis, 2026-10-18:**';assert text.count(needle)==1
p.write_text(text.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify exact-state early rejection\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record.py');print('Recorded qualified candidate and unchanged pilot scope.')
