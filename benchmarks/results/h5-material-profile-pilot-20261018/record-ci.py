"""Retain the completed main CI result before the next periodic push."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-material-profile-pilot-20261018'
raw=subprocess.check_output(['gh','run','view','39100065948','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
ci=json.loads(raw)
assert ci['headSha']=='d7204d6ef316ee29f1e9498d3bfd235927d4b779'
assert ci['status']=='completed' and ci['conclusion']=='success' and len(ci['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in ci['jobs'])
path=out/'main-ci-d7204d6.json';assert not path.exists();path.write_bytes(raw)
note='All six hosted checks on main `d7204d6` have now passed, including Windows, Linux and browser checks. This confirmation precedes the next periodic push; it does not turn the experimental material-profile pilot into a passing H5 result.'
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n'+note+' [Hosted evidence](benchmarks/results/h5-material-profile-pilot-20261018/main-ci-d7204d6.json).\n')
with (out.parent/(out.name+'.md')).open('a',encoding='utf-8',newline='\n') as f:
    f.write('\n\n## Main CI confirmation\n\n'+note+' [Six completed jobs](h5-material-profile-pilot-20261018/main-ci-d7204d6.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 exact-state early-rejection outcome, 2026-10-18:**'
assert s.count(needle)==1
s=s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-material-profile-pilot-20261018/main-ci-d7204d6.json).\n\n'+needle)
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-ci.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'main':'d7204d6','passed_jobs':6,'captured_utc':datetime.now(timezone.utc).isoformat()}))
