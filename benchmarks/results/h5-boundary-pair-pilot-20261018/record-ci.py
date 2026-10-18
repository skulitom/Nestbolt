"""Record completed main checks alongside the boundary-priority pilot."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-boundary-pair-pilot-20261018'
assert (out/'record-outcome.py').exists()
raw=subprocess.check_output(['gh','run','view','39104655556','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
ci=json.loads(raw)
assert ci['headSha']=='a471993a037d5527de2e1876b412057d0dddefe0'
assert ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in ci['jobs'])
path=out/'main-ci-a471993.json';assert not path.exists();path.write_bytes(raw)
note='All six hosted checks on main `a471993` have passed, including Windows, Linux and browser checks. This confirmation precedes the next periodic push; the experimental pilot is assessed separately against the unchanged H5 requirements.'
prior=(root/'BENCHMARKS.md').read_bytes()
assert prior.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n'+note+' [Hosted evidence](benchmarks/results/h5-boundary-pair-pilot-20261018/main-ci-a471993.json).\n')
with (out.parent/(out.name+'.md')).open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n\n## Main CI confirmation\n\n'+note+' [Six completed jobs](h5-boundary-pair-pilot-20261018/main-ci-a471993.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 exact boundary-copy diagnosis, 2026-10-18:**'
assert s.count(needle)==1
s=s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-boundary-pair-pilot-20261018/main-ci-a471993.json).\n\n'+needle)
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-ci.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'main':'a471993','passed_jobs':6,'captured_utc':datetime.now(timezone.utc).isoformat()}))
