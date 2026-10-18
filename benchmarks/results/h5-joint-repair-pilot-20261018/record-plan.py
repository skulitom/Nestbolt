from pathlib import Path
from hashlib import sha256
import json, shutil, subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-joint-repair-pilot-20261018'
probe=root/'output/h5-joint-repair-probe-20261018'
assert not (out/'opened.json').exists()
for name in ['pilot-harness-tests.log','paired-method-review.json','counter-audit-method.json']:
    shutil.copyfile(probe/name,out/name)
for name in ['prepare_h5_joint_pilot.py','check_h5_joint_repair_harness.py','finish_h5_joint_repair_pilot.py','audit_h5_joint_repair.py']:
    shutil.copyfile(root/'output'/name,out/name)
plan=json.loads((out/'plan.json').read_bytes())
assert plan['attempts']==72 and plan['seconds']==60
note='''**N4 joint-repair pilot plan, 2026-10-18:** the [72-outcome plan](../benchmarks/results/h5-joint-repair-pilot-20261018/plan.json)
is prepared for the qualified isolated candidate. Four unchanged development jobs,
both kerfs, three seeds and three arms retain the original 60-second budgets and
rotating matched physical cores. Six execution/scoring functions are AST-identical
to the preceding pilot; all five existing adversarial harness tests pass. The
finisher retains archive/metric checks and adds joint-repair completion, expiry,
acceptance and rollback counter checks. Every outcome is retained; no search has
started at this checkpoint. Only a passing original material limit on every pilot
pair can open the full 13-job comparison. Production is unchanged; H2/H5 remain
open at 60%.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
status=root/'docs/STATUS.md';text=status.read_text(encoding='utf-8')
marker='**N4 joint-repair qualification, 2026-10-18:**'
assert marker in text and '**N4 joint-repair pilot plan' not in text
status.write_text(text.replace(marker,note+'\n'+marker,1),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n'+note)
old=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==old
append(root/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(old)
attr='benchmarks/results/h5-joint-repair-pilot-20261018/** -text -whitespace'
assert attr not in (root/'.gitattributes').read_text(encoding='utf-8')
append(root/'.gitattributes','\n'+attr+'\n')
shutil.copyfile(__file__,out/'record-plan.py')
print(json.dumps({'plan_sha256':sha256((out/'plan.json').read_bytes()).hexdigest(),
    'measurement_started':False,'harness_tests_passed':5,'production_changed':False}))
