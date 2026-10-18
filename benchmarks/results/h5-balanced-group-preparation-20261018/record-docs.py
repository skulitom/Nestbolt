from pathlib import Path
import json,shutil
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-balanced-group-preparation-20261018'
checks=json.loads((out/'checks.json').read_bytes())
pilot=root/'benchmarks/results/h5-balanced-group-pilot-20261018'
plan=json.loads((pilot/'plan.json').read_bytes())
assert checks['all_functional_checks_pass'] and checks['optimized_core_passed']==97
assert plan['attempts']==72 and not (pilot/'opened.json').exists()
heading='**N4 balanced-pair preparation, 2026-10-18:**'
marker='**N4 reuse-stage diagnosis, 2026-10-18:**'
status=root/'docs/STATUS.md';text=status.read_text(encoding='utf-8')
assert text.count(marker)==1 and heading not in text
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:assert heading not in (root/name).read_text(encoding='utf-8')
note='''**N4 balanced-pair preparation, 2026-10-18:** [the isolated candidate](../benchmarks/results/h5-balanced-group-preparation-20261018.md)
passes 97 optimized core tests, strict lint, ten authored observer outcomes,
four public CLI comparisons and five unchanged paired-harness checks. All 90
prior tests remain; seven new tests cover the two-to-three exchange, permissions,
frozen sheets, bounded pair selection, valid single fallback and rejected
attempts. The original test-assumption failures and independently valid fallback
output remain preserved. Normal output stays exact and common replay passes.

Two nearby copies can move together against their complete obstruction union,
using at most half the existing exchange window before the single-part path.
The original total budget, independent geometry/material acceptance and saved
incumbent guards stay. [The committed 72-outcome plan](../benchmarks/results/h5-balanced-group-pilot-20261018/plan.json)
retains the same cases, kerfs, seeds, matched cores, 60-second limits and +1%
condition. No measured improvement, production change or H5 credit is claimed;
the full 13-job gate remains required. H2/H5 are open at 60%.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    with (root/name).open('a',encoding='utf-8',newline='\n') as f:f.write('\n\n'+note)
status.write_text(text.replace(marker,note+'\n'+marker,1),encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-docs.py')
print('Recorded qualified preparation and unopened paired plan; completion remains 60%.')
