"""Retain the completed preceding-main CI result without claiming the new head passed."""
from pathlib import Path
import json, shutil, subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-extended-repair-pilot-20261018'
raw=subprocess.check_output(['gh','run','view','39115139160','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
r=json.loads(raw);assert r['headSha']=='02905f392e1bf6a5fefbc2c900436cf4e9229c5e'
assert r['status']=='completed' and r['conclusion']=='success' and len(r['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in r['jobs'])
p=out/'main-ci-02905f3.json';assert not p.exists();p.write_bytes(raw)
note=('All six hosted checks on preceding main `02905f3` pass, including Windows, Linux, browsers '
      'and both maker rebuilds. This confirms that exact checkpoint, including the reconciled plugin '
      'mock update. The newer `2f5d43f` checkpoint is pushed and its separate hosted run is still pending '
      'at this observation. The isolated extended-repair candidate fails five material comparisons '
      'and remains excluded from production.')
prior=(root/'BENCHMARKS.md').read_bytes()
assert prior.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n'+note+' [Hosted evidence](benchmarks/results/h5-extended-repair-pilot-20261018/main-ci-02905f3.json).\n')
append(out.parent/(out.name+'.md'),'\n'+note+' [Six completed checks](h5-extended-repair-pilot-20261018/main-ci-02905f3.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 extended-repair outcome, 2026-10-18:**'
assert s.count(needle)==1
p.write_text(s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-extended-repair-pilot-20261018/main-ci-02905f3.json).\n\n'+needle),encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-ci.py')
shutil.copyfile(root/'output/prepare_h5_extended_repair_outcome.py',out/'prepare-outcome.py')
print(json.dumps({'main':'02905f3','passed_jobs':6,'run':r['url']}))
