from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exact-state-preparation-20261018'
checks=json.loads((out/'checks.json').read_bytes());assert checks['all_qualified']
assert (root/'benchmarks/results/h5-exact-state-20261018/plan.json').exists()
note='''**N4 exact-state diagnosis preparation, 2026-10-18:** [the observer passes all 116 optimized tests](../benchmarks/results/h5-exact-state-preparation-20261018.md),
strict lint/build, fourteen authored trace cases and 37 malformed-record checks.
All 113 prior tests remain unchanged. Exact reconstruction covers all 154 files;
153 are unchanged from the preceding observer. Two panel-hardware diagnostics
will compare complete internal pose multisets and independently check both
layouts saved for neutral rejections. The comparison records observations only;
all decisions, full validators, material guards and time limits remain.
No production integration, reserved access or quality claim; H2/H5 remain open
and completed weight stays 60%.
'''
def append(path,s):
    with path.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
status=root/'docs/STATUS.md';text=status.read_text(encoding='utf-8');needle='**N4 larger-return diagnosis, 2026-10-18:**'
assert text.count(needle)==1;status.write_text(text.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify exact-state observations\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record.py');print('Recorded qualified scope; no measurement executed.')
