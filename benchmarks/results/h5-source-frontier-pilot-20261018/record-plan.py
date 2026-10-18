"""Record the qualified matched plan and current no-overlap preflight."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-source-frontier-pilot-20261018'
probe=root/'output/h5-frontier-probe-20261018'
assert not (out/'opened.json').exists()
sys.path.insert(0,str(root/'scripts'));import h5_source_frontier_pilot as pilot
prerequisites=pilot.require_measurements_finished()
pilot.write(out/'preflight.json',prerequisites)
for name in ['frontier-pilot-harness-tests.log','frontier-paired-method-review.json']:shutil.copyfile(probe/name,out/name)
for name in ['prepare_h5_frontier_pilot_tools.py','finish_h5_source_frontier_pilot.py','audit_h5_source_frontier_pilot.py']:
    shutil.copyfile(root/'output'/name,out/name)
plan=pilot.load(out/'plan.json');assert plan['attempts']==72 and plan['seconds']==60
assert plan['guards']==pilot.guards()
note='''**N4 source-frontier pilot plan, 2026-10-18:** the [72-outcome matched plan](../benchmarks/results/h5-source-frontier-pilot-20261018/plan.json)
is ready for the qualified isolated policy. The same four jobs, two kerfs, three
seeds, ordinary/common baseline engines, 60-second allowance and rotating physical
cores remain. Six execution/scoring functions are AST-identical to the preceding
pilot; all five adversarial harness checks pass. The verified preflight confirms
that earlier local measurements are finished. Archive, metric, hole and rollback
checks remain; a separate counter identifies proposals with a tighter source crop.
No measurement has started at this checkpoint. Every original failure and threshold
remains. The full 13-job comparison still requires every pilot material pair to
pass. Production is unchanged; H2/H5 remain open at 60%.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**N4 source-frontier qualification, 2026-10-18:**'
assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
append(root/'.gitattributes','\nbenchmarks/results/h5-source-frontier-pilot-20261018/** -text -whitespace\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-plan.py')
print(json.dumps({'plan_sha256':sha256((out/'plan.json').read_bytes()).hexdigest(),'measurement_started':False,'preflight_passed':True}))
