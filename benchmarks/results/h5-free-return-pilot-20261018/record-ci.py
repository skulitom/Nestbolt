"""Record the completed six-job check on the preceding main checkpoint."""
from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-free-return-pilot-20261018'
raw=subprocess.check_output(['gh','run','view','39109388124','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
r=json.loads(raw);assert r['headSha']=='8ae8b694e0400196d18a75107d1d435cd445e65d'
assert r['status']=='completed' and r['conclusion']=='success' and len(r['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in r['jobs'])
p=out/'main-ci-8ae8b69.json';assert not p.exists();p.write_bytes(raw)
note='All six hosted checks on preceding main `8ae8b69` pass, including Windows, Linux, browsers and both maker rebuilds. This is evidence for that checkpoint; the subsequent isolated free-space candidate still fails its original material pilot and remains excluded from production.'
prior=(root/'BENCHMARKS.md').read_bytes();assert prior==subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n'+note+' [Hosted evidence](benchmarks/results/h5-free-return-pilot-20261018/main-ci-8ae8b69.json).\n')
append(out.parent/(out.name+'.md'),'\n'+note+' [Six completed checks](h5-free-return-pilot-20261018/main-ci-8ae8b69.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 free-space-return outcome, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-free-return-pilot-20261018/main-ci-8ae8b69.json).\n\n'+needle),encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record-ci.py')
print(json.dumps({'main':'8ae8b69','passed_jobs':6,'run':r['url']}))
