from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import base64
import json
import shutil
import subprocess
import sys
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/reconciliation-20261017';out.mkdir(exist_ok=False)
def gh(*args):return subprocess.check_output(['gh',*args],cwd=root,timeout=120)
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
sys.path.insert(0,str(root/'scripts'))
from h2_import_audit import source_digest
expected={38886270634:'2ba35d6ae32b3939c8b588c7e679280ba337eca2',39022613069:'72f97239dcd0a580e711ac112ee14da10b0c0252'}
runs=[]
for number,commit in expected.items():
    raw=gh('run','view',str(number),'--json','status,conclusion,headSha,url,jobs')
    run=json.loads(raw)
    assert run['status']=='completed' and run['conclusion']=='success' and run['headSha']==commit
    assert len(run['jobs'])==6 and all(j['conclusion']=='success' for j in run['jobs'])
    (out/f'ci-{number}.json').write_bytes(raw)
    web=next(j for j in run['jobs'] if j['name']=='web')
    log=gh('api',f'repos/skulitom/Nestbolt/actions/jobs/{web["databaseId"]}/logs')
    assert b'86 passed' in log and b'4 skipped' in log
    (out/f'web-{number}.log').write_bytes(log)
    runs.append({'run':number,'commit':commit,'url':run['url'],'all_six_pass':True,'browser_passed':86,'browser_skipped':4})
old=gh('run','view','38883652469','--json','status,conclusion,headSha,url,jobs')
(out/'original-c36-ci-terminal.json').write_bytes(old)
assert json.loads(old)['status']=='completed'
before=expected[38886270634];after=expected[39022613069]
changed=subprocess.check_output(['git','diff','--name-only',before,after],cwd=root,text=True).splitlines()
assert len(changed)==23 and not any(p.startswith(('crates/','web/','scripts/')) for p in changed)
assert source_digest()=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
upstream=json.loads(gh('api','repos/JeroenGar/sparrow-studio/commits/main'))
readme=json.loads(gh('api','repos/JeroenGar/sparrow-studio/contents/README.md?ref='+upstream['sha']))
data=base64.b64decode(readme['content'])
assert b'not published yet' in data
review={'utc':datetime.now(timezone.utc).isoformat(),'repository_head':after,'fast_forward_from':before,
    'changed_paths':changed,'product_digest':source_digest(),'application_source_unchanged':True,
    'changes':'Claude Code plugin, evals, agent/sibling tool docs and Chinese/Japanese READMEs; existing local work preserved.',
    'hosted_checks':runs,'original_Firefox_failure_cause_established':False,
    'original_failure_retained':'benchmarks/results/preview-depth-followup-ci-20261016',
    'stop_review':{'repository':'https://github.com/JeroenGar/sparrow-studio','head':upstream['sha'],
        'readme_url':f'https://github.com/JeroenGar/sparrow-studio/blob/{upstream["sha"]}/README.md',
        'readme_sha256':sha256(data).hexdigest(),'readme_bytes':len(data),
        'published_site':'https://sparrowstudio.app/',
        'finding':'Official live site still explicitly excludes fixed-sheet allocation and part-in-hole; repository describes the redesign as unpublished. Both pages read through web tools on 2026-10-17.',
        'stop_rule_triggered':False},'H2_pending_denominator_question_unchanged':True,
    'reserved_geometry_opened':False,'completed_weight_percent':60}
write(out/'review.json',review)
shutil.copyfile(__file__,out/'record.py')
write(out/'integrity.json',{p.name:{'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()} for p in out.iterdir() if p.is_file()})
(out.parent/(out.name+'.md')).write_text('''# Repository and hosted-check reconciliation — 2026-10-17

Main is fast-forwarded from `2ba35d6` to `72f9723`, preserving the new Claude
Code plugin/evals, agent documentation, sibling-tool links and Chinese/Japanese
READMEs. All 23 changed paths are packaging/documentation; application source
and its recorded digest are unchanged. User-owned local files remain untouched.

Both [the post-release checkpoint](https://github.com/skulitom/Nestbolt/actions/runs/38886270634)
and [the newly merged main commit](https://github.com/skulitom/Nestbolt/actions/runs/39022613069)
pass all six hosted checks. Each browser job reports 86 passes and four opt-in
skips. Exact job metadata and logs are retained. The original c36baa8 Firefox
failure remains a failure with unknown cause; later successes do not explain
or erase it. Its final run state is also captured.

The [live Sparrow Studio site](https://sparrowstudio.app/) still excludes
automatic fixed-sheet allocation and placement inside holes. The
[official repository](https://github.com/JeroenGar/sparrow-studio) still labels
its redesign unpublished; the read README commit/hash is recorded in
[review.json](reconciliation-20261017/review.json). The shipment stop rule is
not triggered. No competitor benchmark or dependency change follows.

H2's denominator clarification remains pending; no reserved geometry was opened.
The failed H5 atomic-set pilot remains authoritative for that experiment. Next
work diagnoses its proposal eligibility and repair stages in an isolated copy.
H1/H3/H4/H6 remain complete, **60%**; H2/H5 remain open.
''',encoding='utf-8',newline='\n')
oldnotice='''**Follow-up browser CI:** the [separate c36baa8 main run](../benchmarks/results/preview-depth-followup-ci-20261016.md)
has one Firefox lead-report failure (85 browser tests pass, four skip). Sixteen
unchanged local repetitions pass, and the affected 28-test suite passes after
improving error diagnostics. The original hosted cause is unresolved; new CI
retains failure screenshots/traces. Release workflow and actual native download
checks pass separately. Product behavior and gate thresholds are unchanged.'''
newnotice='''**Hosted checks, 2026-10-17:** [both follow-up main commits pass all six checks](../benchmarks/results/reconciliation-20261017.md),
including 86 browser tests with four opt-in skips each. The original c36baa8
Firefox failure remains preserved with unknown cause. New failure diagnostics
remain enabled. Main's new plugin and translated/agent READMEs are reconciled;
application source and gate thresholds are unchanged.'''
for rel in ['docs/STATUS.md','docs/RELEASE_READINESS.md']:
    path=root/rel;text=path.read_text(encoding='utf-8');assert text.count(oldnotice)==1
    text=text.replace(oldnotice,newnotice)
    if rel.endswith('STATUS.md'):text=text.replace('# Status — 2026-10-16','# Status — 2026-10-17',1)
    path.write_text(text,encoding='utf-8',newline='\n')
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:f.write('''

## 2026-10-17 — Reconcile main and passing hosted follow-up

[The reconciliation](benchmarks/results/reconciliation-20261017.md) retains exact
logs for both subsequent main runs: each passes all six jobs and 86 browser
tests, with four opt-in skips. The original c36baa8 Firefox failure and unknown
cause remain explicit. Main's plugin/evals, agent docs and translated READMEs
are fast-forwarded without application changes; product digest stays fixed.
Official Sparrow Studio pages still describe strip-only deployment and an
unpublished redesign, so the shipment stop rule is not triggered. No reserved
geometry, new benchmark, release or milestone closure; completion remains 60%.
''')
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:f.write('\nbenchmarks/results/reconciliation-20261017/** -text -whitespace\n')
print(json.dumps({'reconciled':after,'all_six_hosted_jobs_pass':True,'browser_passes_each':86,'source_unchanged':True}))
