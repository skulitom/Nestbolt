"""Finish only the status update after an outdated insertion marker failed."""
from pathlib import Path
from hashlib import sha256
import ast,json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-return-capacity-diagnosis-20261017'
source=root/'output/record_return_capacity_outcome.py'
shutil.copyfile(source,out/'record-outcome-status-marker-failure.py')
tree=ast.parse(source.read_text(encoding='utf-8'))
note=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='note' for t in n.targets))
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    assert (root/name).read_text(encoding='utf-8').count(note)==1
assert (root/'BENCHMARKS.md').read_text(encoding='utf-8').count('## 2026-10-18 — Return-sheet area bounds do not explain the failed repairs')==1
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8')
needle='**N4 return-frame diagnosis, 2026-10-17:**';assert s.count(needle)==1
s=s.replace(needle,note.strip()+'\n\n'+needle).replace('# Status — 2026-10-17','# Status — 2026-10-18')
p.write_text(s,encoding='utf-8',newline='\n')
record={'failure':'AssertionError: expected a standalone N4 balanced-group witness heading in STATUS.md; it is instead embedded in the preceding return-frame paragraph.',
    'already_completed_before_failure':['numeric evidence assertions','review.json','outcome report','BENCHMARKS.md append','PLAN_V1_1.md append','V1_1_RESEARCH.md append'],
    'recovery':'Only STATUS.md was updated using its verified existing return-frame heading. Earlier completed appends were checked unique and not repeated.',
    'source_sha256':sha256(source.read_bytes()).hexdigest(),'new_searches':0,'measurement_or_numeric_change':False}
(out/'doc-update-review.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'finish-status.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print(json.dumps(record))
