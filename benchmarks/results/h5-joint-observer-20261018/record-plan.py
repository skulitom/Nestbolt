from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-joint-observer-20261018'
prep=root/'benchmarks/results/h5-joint-observer-preparation-20261018'
assert json.loads((prep/'checks.json').read_bytes())['all_qualified']
assert not (out/'opened.json').exists()
note='''**N4 joint-repair observation plan, 2026-10-18:** the [diagnostic observer](../benchmarks/results/h5-joint-observer-preparation-20261018.md)
passes all 165 unchanged tests and preserves 86 exact native witnesses. Its 48
linked native trace records pass structural checks; nine malformed records are
rejected. Independent checks validate 23 saved layouts and 53 filled-outer pairs.
Four public fixed-work outcomes match the unobserved candidate exactly except
elapsed time. All 157 source files reconstruct, with 155 unrelated files unchanged;
lint/build pass. The first public reference-path error is preserved and its saved
outcome reused. The [four-case plan](../benchmarks/results/h5-joint-observer-20261018/plan.json)
retains both mechanical jobs, both kerfs, seed zero, 60 seconds and serial physical
CCD0 CPU 8. It records actual pair membership, material gains, repair/lowering
times, expiry, rejection and rollback. No development observation has started at
this checkpoint. Logging can change wall trajectories; no quality comparison,
pilot retry or integration follows. Production and the released preview remain
unchanged; H2/H5 remain open at 60%.
'''
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
status=root/'docs/STATUS.md';s=status.read_text(encoding='utf-8')
marker='**N4 joint-repair outcome, 2026-10-18:**'
assert '**N4 joint-repair observation plan' not in s
status.write_text(s.replace(marker,note+'\n'+marker,1),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
for folder in [out,prep]:
    pattern=folder.relative_to(root).as_posix()+'/** -text -whitespace'
    assert pattern not in (root/'.gitattributes').read_text(encoding='utf-8')
    append(root/'.gitattributes','\n'+pattern+'\n')
shutil.copyfile(__file__,out/'record-plan.py')
shutil.copyfile(root/'scripts/h5_joint_trace.py',out/'trace-reader.py')
print('Recorded qualified observer and unstarted four-case diagnostic plan.')
