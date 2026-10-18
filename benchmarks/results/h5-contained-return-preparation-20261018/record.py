"""Record contained-return qualification without claiming quality or starting a pilot."""
from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-contained-return-preparation-20261018'
checks=json.loads((out/'checks.json').read_bytes());assert checks['all_functional_checks_pass']
note='''**N4 contained-return preparation, 2026-10-18:** [the isolated return-seed change qualifies](../benchmarks/results/h5-contained-return-preparation-20261018.md).
All 133 optimized tests pass, retaining all 130 prior tests. A fitting returned
group may translate inside the existing source bounding box, with charged
geometry work and an exact second check. Other cases keep the old poses.
Existing choices, budgets, repairs and full acceptance checks remain.
Two expected old-behavior failures and the first implementation's rotated-edge
failure are preserved; its small interior-seed correction changes no assertion.
Strict lint/build, twelve branch outcomes, 29 public CLI checks, deterministic
replays, exact source reconstruction and five harness checks pass. No quality
pilot has started; its plan must be committed first. H2/H5 remain open at 60%.
'''
def append(path,text):
    with path.open('a',encoding='utf-8',newline='\n') as stream:stream.write(text)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 exchange-failure diagnosis, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify contained return initialization\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record.py')
print('Recorded contained-return functional qualification; no quality pilot started.')
