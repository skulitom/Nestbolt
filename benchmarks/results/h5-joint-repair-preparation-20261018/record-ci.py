"""Retain the completed preceding-main CI result without claiming the new head passed."""
from pathlib import Path
import json, shutil, subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-joint-repair-preparation-20261018'
raw=subprocess.check_output(['gh','run','view','39121375578','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
r=json.loads(raw);assert r['headSha']=='abd3baeb710b6cb97a49b388f9c71ef068ac51f0'
assert r['status']=='completed' and r['conclusion']=='success' and len(r['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in r['jobs'])
p=out/'main-ci-abd3bae.json';assert not p.exists();p.write_bytes(raw)
note=('All six hosted checks on preceding main `abd3bae` pass, including Windows, Linux, browsers '
      'and both maker rebuilds. This confirms that exact pushed checkpoint. The newly qualified '
      'joint-repair candidate remains isolated and still requires a committed matched development '
      'pilot before any integration decision. Production code and published release assets remain '
      'unchanged; H2/H5 remain open at 60%.')
prior=(root/'BENCHMARKS.md').read_bytes()
assert prior.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n'+note+' [Hosted evidence](benchmarks/results/h5-joint-repair-preparation-20261018/main-ci-abd3bae.json).\n')
append(out.parent/(out.name+'.md'),'\n'+note+' [Six completed checks](h5-joint-repair-preparation-20261018/main-ci-abd3bae.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 joint-repair qualification, 2026-10-18:**'
assert s.count(needle)==1
p.write_text(s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-joint-repair-preparation-20261018/main-ci-abd3bae.json).\n\n'+needle),encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-ci.py')
print(json.dumps({'main':'abd3bae','passed_jobs':6,'run':r['url']}))
