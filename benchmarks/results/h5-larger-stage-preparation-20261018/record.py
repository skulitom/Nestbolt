from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-larger-stage-preparation-20261018'
assert json.loads((out/'checks.json').read_bytes())['all_qualified']
assert (root/'benchmarks/results/h5-larger-stage-20261018/plan.json').is_file()
note='''**N4 larger-return diagnosis preparation, 2026-10-18:** [the isolated observer](../benchmarks/results/h5-larger-stage-preparation-20261018.md)
passes all 113 unchanged core tests, strict lint/build, fourteen authored trace
cases, the direct strict-material guard and 31 malformed-observation checks.
All 154 formatted files match an exact reconstruction, with only two observed
files. Timings distinguish construction, repairs and validation; complete
after-exchange/after-fill layouts will be checked independently. The first
logger compile failure remains preserved. Four serial seed-zero mechanical
observations retain the original 60-second budgets. Logging may perturb wall
time; this diagnoses the rejected candidate without replacing its failed
quality comparison. No integration or H5 credit; completion stays 60%.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';text=p.read_text(encoding='utf-8');marker='**N4 larger-return outcome, 2026-10-18:**';assert text.count(marker)==1
p.write_text(text.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify larger-return phase timing and saved layouts\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record.py');print('Diagnostic preparation linked; original benchmark bytes preserved.')
