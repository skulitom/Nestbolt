"""Record the passing candidate CI and verified ordinary push without rerunning tests."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
source=root/'output/push-preview-evidence-after-ci-20261016'
out=root/'benchmarks/results/preview-depth-hosted-checks-20261016'
workflow=json.loads((source/'workflow.json').read_bytes())
pushed=json.loads((source/'completed.json').read_bytes())
tested='23442be38ee2e881669e753bc405ab3269ff1b39'
assert workflow['status']=='completed' and workflow['conclusion']=='success'
assert workflow['headSha']==tested and len(workflow['jobs'])==6
assert all(j['conclusion']=='success' for j in workflow['jobs'])
assert pushed['tested_commit']==tested and pushed['CI_passed'] and pushed['remote_main_verified']
assert not pushed['force_used'] and not pushed['release_created']
scope=['crates','web/src','Cargo.toml','Cargo.lock','rust-toolchain.toml','.cargo',
    'web/package.json','web/package-lock.json','.github/workflows/ci.yml',
    '.github/workflows/release.yml','scripts','mcpb/*.mjs']
delta=subprocess.check_output(['git','diff','--name-only',tested,pushed['pushed_commit'],'--',*scope],cwd=root)
assert not delta
sys.path.insert(0,str(root/'scripts'))
from h2_import_audit import source_digest
product=source_digest()
assert product=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
out.mkdir(exist_ok=False)
for path in source.iterdir():
    assert path.is_file()
    (out/path.name).write_bytes(path.read_bytes())
(out/'record.py').write_bytes(Path(__file__).read_bytes())
checks={'all_six_jobs_pass':True,'tested_commit':tested,'workflow_url':workflow['url'],
    'jobs':[{k:j[k] for k in ['name','conclusion','startedAt','completedAt','url']} for j in workflow['jobs']],
    'pushed_commit':pushed['pushed_commit'],'product_digest':product,
    'product_build_workflow_and_runner_inputs_unchanged_after_tested_commit':True,
    'compared_paths':scope,'ordinary_push_verified':True,'release_created':False,
    'new_main_CI':{'run':38857882488,'status_at_recording':'in_progress',
        'url':'https://github.com/skulitom/Nestbolt/actions/runs/38857882488'},
    'full_quality_scale_and_export_review_still_required':True,'H4_complete':False}
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8',newline='\n')
inventory={p.name:{'sha256':sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
    for p in sorted(out.iterdir()) if p.is_file()}
(out/'integrity.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8',newline='\n')
report=f'''# Current preview hosted checks and push — 2026-10-16

**All six hosted checks pass for the tested implementation.**
[Run 38854287845]({workflow['url']}) tests commit `23442be`:
Windows and Linux native checks, browser tests, both maker-corpus rebuilds,
and benchmark smoke all succeed. Windows completes at 05:49:21 UTC.

The ordinary push of reviewed evidence commit `21835ba` completes at
05:50:27 UTC, after that run finishes. Remote main is verified at that exact
commit. No force or retry was used. [Checks](preview-depth-hosted-checks-20261016/checks.json)
and the original workflow/push outputs retain the identities and results.

Every product, build, test-runner and packaging-module path listed in the check
is unchanged between the tested and pushed commits. The current product digest
remains `{product}`. The newer
[main run 38857882488](https://github.com/skulitom/Nestbolt/actions/runs/38857882488)
is still in progress at this checkpoint; it is not reported as already passed.

This completes hosted-check verification for the code under measurement.
The [full H4 comparison](h4-preview-depth-release-20261016/plan.json),
conditional browser scale workflows, all-placement exported-curve checks,
screenshots and final requirement review remain outstanding. No release,
registry publication or milestone closure follows from CI alone. Completion
remains 45%.
'''
(out.parent/(out.name+'.md')).write_text(report,encoding='utf-8',newline='\n')

path=root/'docs/RELEASE_READINESS.md';text=path.read_text(encoding='utf-8')
before='''its isolated browser pilot and current package verification. Full quality,
scale, exported-curve fidelity and hosted checks are still required. Milestone'''
after='''its isolated browser pilot, current package verification and all six hosted
checks. Full quality, scale and exported-curve fidelity remain required. Milestone'''
assert before in text;text=text.replace(before,after)
before='''- [Current hosted checks](https://github.com/skulitom/Nestbolt/actions/runs/38854287845)
  remain in progress. Their completion and current quality/scale confirmation
  are still required before publishing.
'''
after='''- [All six hosted checks pass for the tested implementation](../benchmarks/results/preview-depth-hosted-checks-20261016.md).
  Reviewed evidence is pushed to main as `21835ba`; all product, build and
  runner inputs match tested commit `23442be`. Its newer main CI run is still
  underway at this checkpoint. Full current quality/scale/export confirmation
  remains required before publishing.
'''
assert before in text;text=text.replace(before,after)
path.write_text(text,encoding='utf-8',newline='\n')
path=root/'docs/STATUS.md';text=path.read_text(encoding='utf-8')
before='Current hosted checks remain in progress. The [requirement preflight]'
after='[All six hosted checks pass for this code](../benchmarks/results/preview-depth-hosted-checks-20261016.md); reviewed evidence is pushed to main as `21835ba`. The [requirement preflight]'
assert before in text;path.write_text(text.replace(before,after),encoding='utf-8',newline='\n')
path=root/'BENCHMARKS.md';before=path.read_bytes()
assert before.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with path.open('a',encoding='utf-8',newline='\n') as f:
    f.write('''

## 2026-10-16 — Current implementation passes all six hosted checks

[Run 38854287845](benchmarks/results/preview-depth-hosted-checks-20261016.md)
passes all six jobs on `23442be`, including Windows/Linux checks, both browser
engines, both dataset rebuilds and benchmark smoke. After it finishes, reviewed
evidence commit `21835ba` is pushed normally to main and the remote identity is
verified. Product, build, test-runner and packaging-module inputs are unchanged.
The newer main CI run is still in progress at this checkpoint; no result is
inferred for it. Full current H4 quality, scale, exported-curve fidelity and
final review remain required. No release or gate closure occurs; completion
stays 45%.
''')
assert path.read_bytes().startswith(before)
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\nbenchmarks/results/preview-depth-hosted-checks-20261016/** -text -whitespace\n')
print('Recorded all six passing candidate CI jobs and the verified main push; measurement remains unchanged.')
