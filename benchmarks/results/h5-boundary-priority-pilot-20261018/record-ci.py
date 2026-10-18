"""Record completed main checks alongside the boundary-priority pilot."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-boundary-priority-pilot-20261018'
assert (out/'record-outcome.py').exists()
raw=subprocess.check_output(['gh','run','view','39102356591','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
ci=json.loads(raw)
assert ci['headSha']=='93759c24db8ec30450091cb8b062344271370529'
assert ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in ci['jobs'])
path=out/'main-ci-93759c2.json';assert not path.exists();path.write_bytes(raw)
note='All six hosted checks on main `93759c2` have passed, including Windows, Linux and browser checks. This confirmation precedes the next periodic push; the experimental pilot is assessed separately against the unchanged H5 requirements.'
prior=(root/'BENCHMARKS.md').read_bytes()
assert prior.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n'+note+' [Hosted evidence](benchmarks/results/h5-boundary-priority-pilot-20261018/main-ci-93759c2.json).\n')
with (out.parent/(out.name+'.md')).open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n\n## Main CI confirmation\n\n'+note+' [Six completed jobs](h5-boundary-priority-pilot-20261018/main-ci-93759c2.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 height-setting part diagnosis, 2026-10-18:**'
assert s.count(needle)==1
s=s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-boundary-priority-pilot-20261018/main-ci-93759c2.json).\n\n'+needle)
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-ci.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'main':'93759c2','passed_jobs':6,'captured_utc':datetime.now(timezone.utc).isoformat()}))
