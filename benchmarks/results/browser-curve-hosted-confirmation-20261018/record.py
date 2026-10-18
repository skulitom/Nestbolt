"""Record the successful hosted browser job without claiming the whole workflow passed."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];source=root/'output/ci-4b13a85-browser-confirmation-20261018'
out=root/'benchmarks/results/browser-curve-hosted-confirmation-20261018'
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
job=json.loads((source/'web-job.json').read_bytes());log=(source/'web.log').read_text(encoding='utf-8')
assert job['status']=='completed' and job['conclusion']=='success' and job['head_sha']=='4b13a858ec181f5cb3507927322a7458847f91f8'
assert '86 passed' in log and '4 skipped' in log
lines=[x for x in log.splitlines() if 'DXF and SVG import; exports keep arcs and curves' in x]
assert len(lines)==2 and any('[chromium]' in x for x in lines) and any('[firefox]' in x for x in lines)
assert all('\u2713' in x for x in lines)
assert subprocess.check_output(['git','show',job['head_sha']+':web/tests/features.spec.ts'],cwd=root)==(root/'web/tests/features.spec.ts').read_bytes()
state=json.loads(subprocess.check_output(['gh','run','view','39130020220','--json','status,conclusion,headSha,jobs,url'],cwd=root))
out.mkdir()
for name in ['web.log','web-job.json']:shutil.copyfile(source/name,out/name)
checks={'observed_utc':datetime.now(timezone.utc).isoformat(),'browser_job_passed':True,'browser_passed':86,'opt_in_skipped':4,
    'Chromium_and_Firefox_curve_test_passed':True,'source_test_exact_at_verified_head':True,'head':job['head_sha'],
    'original_failure_preserved':True,'whole_workflow_claimed_passed':False,
    'files':{name:digest(out/name) for name in ['web.log','web-job.json']},'workflow_snapshot':state}
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8',newline='\n')
doc='''# Hosted curve-test confirmation — 2026-10-18

The corrected browser job on main `4b13a85` passes **86 tests with four opt-in
skips**. Both Chromium and Firefox pass the curve import/export test with the
explicit quick initial layout, the original five-second allowance and all
original assertions. The saved source at that exact commit matches the tested
file, including the added checks for all eight placements and the saved option.

The original [d414824 failure and local repair](browser-curve-initial-layout-20261018.md)
remain preserved. This confirms the browser test correction, not an application
performance gain or H5 result. The full workflow is still tracked separately;
its Windows checks are not inferred from the completed browser job.

[Hosted browser job](https://github.com/skulitom/Nestbolt/actions/runs/39130020220/job/117683115467),
[checks and workflow snapshot](browser-curve-hosted-confirmation-20261018/checks.json),
[original log](browser-curve-hosted-confirmation-20261018/web.log).
'''
(out.parent/(out.name+'.md')).write_text(doc,encoding='utf-8',newline='\n')
note='''**Hosted browser confirmation, 2026-10-18:** [main 4b13a85 passes the browser job](../benchmarks/results/browser-curve-hosted-confirmation-20261018.md):
86 tests pass with four opt-in skips, including the corrected curve import/export
test in Chromium and Firefox. The original failed job remains preserved. This
confirms the test-only correction; the separate Windows workflow checks are
still pending. Product source, release assets and gate limits remain unchanged.
'''
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
append(root/'BENCHMARKS.md','\n'+note.replace('../benchmarks/','benchmarks/'))
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n'+note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8');marker='**Browser curve-test follow-up, 2026-10-18:**'
assert s.count(marker)==1;p.write_text(s.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
append(root/'.gitattributes','\nbenchmarks/results/browser-curve-hosted-confirmation-20261018/** -text -whitespace\n')
shutil.copyfile(__file__,out/'record.py')
print(json.dumps({'hosted_browser_passed':86,'skipped':4,'workflow_status':state['status'],'whole_workflow_claimed_passed':False}))
