"""Retain the successful hosted check for the preceding main checkpoint."""
from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-exchange-chain-pilot-20261018'
raw=subprocess.check_output(['gh','run','view','39112090234','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
r=json.loads(raw);assert r['headSha']=='bfde198cde7e99cda524116a0246135f14a12f02'
assert r['status']=='completed' and r['conclusion']=='success' and len(r['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in r['jobs'])
p=out/'main-ci-bfde198.json';assert not p.exists();p.write_bytes(raw)
note='All six hosted checks on preceding main `bfde198` pass, including Windows, Linux, browsers and both maker rebuilds. This confirms that checkpoint. The subsequent isolated continuation experiment still fails all four mechanical material comparisons and remains excluded from production.'
prior=(root/'BENCHMARKS.md').read_bytes();assert prior==subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n'+note+' [Hosted evidence](benchmarks/results/h5-exchange-chain-pilot-20261018/main-ci-bfde198.json).\n')
append(out.parent/(out.name+'.md'),'\n'+note+' [Six completed checks](h5-exchange-chain-pilot-20261018/main-ci-bfde198.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 exchange-continuation outcome, 2026-10-18:**';assert s.count(needle)==1
p.write_text(s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-exchange-chain-pilot-20261018/main-ci-bfde198.json).\n\n'+needle),encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior);shutil.copyfile(__file__,out/'record-ci.py')
print(json.dumps({'main':'bfde198','passed_jobs':6,'run':r['url']}))
