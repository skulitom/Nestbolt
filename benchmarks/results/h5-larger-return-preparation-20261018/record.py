from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-larger-return-preparation-20261018'
c=json.loads((out/'checks.json').read_bytes());assert c['all_functional_checks_pass'] and c['optimized_core_passed']==113
assert (root/'benchmarks/results/h5-larger-return-pilot-20261018/plan.json').is_file()
note='''**N4 larger-return qualification, 2026-10-18:** [the corrected isolated candidate](../benchmarks/results/h5-larger-return-preparation-20261018.md)
passes 113 optimized core tests, strict lint/build, ten public outcomes,
four CLI comparisons and five pilot checks. The original candidate's four
failures remain. An exact replay with eight validated intermediate layouts
shows gap filling moves the named part correctly; later compression moves it
again while reducing material. Four route-specific tests now target their
invariants, 103 prior tests are unchanged and six tests are added. The actual
strict material guard rejects even a one-ULP increase. A direct post-exchange
fill test and all six larger-return outcomes pass fourteen more independent
validations. Guard extraction reverses exactly; all other runtime text is
unchanged beyond the area filter and unused sum removal. The same 72-outcome
pilot is committed before measurement. No quality or integration claim;
H2/H5 remain open at 60%.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';text=p.read_text();marker='**N4 larger-return candidate review, 2026-10-18:**';assert text.count(marker)==1
p.write_text(text.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify larger-return pairs after direct failure diagnosis\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record.py')
print('Qualified preparation linked; benchmark log remains append-only.')
