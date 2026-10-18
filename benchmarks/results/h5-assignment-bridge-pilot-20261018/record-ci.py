"""Retain the completed preceding-main CI result without claiming the new head passed."""
from pathlib import Path
import json, shutil, subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-assignment-bridge-pilot-20261018'
raw=subprocess.check_output(['gh','run','view','39117914996','--json','databaseId,headSha,status,conclusion,jobs,url'],cwd=root)
r=json.loads(raw);assert r['headSha']=='2f5d43f265b5b637d8dd713bf236e17d6da5c7db'
assert r['status']=='completed' and r['conclusion']=='success' and len(r['jobs'])==6
assert all(j['status']=='completed' and j['conclusion']=='success' for j in r['jobs'])
p=out/'main-ci-2f5d43f.json';assert not p.exists();p.write_bytes(raw)
note=('All six hosted checks on preceding main `2f5d43f` pass, including Windows, Linux, browsers '
      'and both maker rebuilds. This confirms that exact checkpoint. The assignment-bridge '
      'candidate fails four material comparisons and remains excluded from production. '
      'Application code remains unchanged from the published v0.2.0-alpha.1 preview; '
      'the English, Japanese and Chinese READMEs already describe the preview and remaining gates. '
      'There is no new qualified application build to release at this checkpoint.')
prior=(root/'BENCHMARKS.md').read_bytes()
assert prior.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
def append(p,s):
 with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
append(root/'BENCHMARKS.md','\n'+note+' [Hosted evidence](benchmarks/results/h5-assignment-bridge-pilot-20261018/main-ci-2f5d43f.json).\n')
append(out.parent/(out.name+'.md'),'\n'+note+' [Six completed checks](h5-assignment-bridge-pilot-20261018/main-ci-2f5d43f.json).\n')
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');needle='**N4 assignment-bridge outcome, 2026-10-18:**'
assert s.count(needle)==1
p.write_text(s.replace(needle,note+' [Hosted evidence](../benchmarks/results/h5-assignment-bridge-pilot-20261018/main-ci-2f5d43f.json).\n\n'+needle),encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record-ci.py')
print(json.dumps({'main':'2f5d43f','passed_jobs':6,'run':r['url']}))
