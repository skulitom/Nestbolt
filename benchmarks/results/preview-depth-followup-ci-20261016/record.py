"""Keep the follow-up browser CI failure and diagnostic attempts distinct from release acceptance."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
import subprocess
import zipfile
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/preview-depth-followup-ci-20261016'
out.mkdir(exist_ok=False)
raw=out/'raw.zip'
sources={}
for directory in ['preview-c36-firefox-diagnostic-20261016','preview-c36-firefox-selected-diagnostic-20261016',
                  'preview-c36-firefox-test-diagnostics-change-20261016','preview-c36-feature-diagnostics-final-20261016']:
    for p in (root/'output'/directory).rglob('*'):
        if p.is_file():sources[p.relative_to(root/'output').as_posix()]=p
for name in ['preview-c36-web-job.log','preview-c36-feature-diagnostics-final-stdout.log',
             'preview-c36-feature-diagnostics-final-stderr.log','diagnose_published_firefox_leads.py',
             'diagnose_published_firefox_leads_selected.py','verify_release_documentation.py']:
    sources[name]=root/'output'/name
digest=lambda p:sha256(p.read_bytes()).hexdigest()
inventory={name:{'bytes':p.stat().st_size,'sha256':digest(p)} for name,p in sources.items()}
with zipfile.ZipFile(raw,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,p in sources.items():z.write(p,name)
with zipfile.ZipFile(raw) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,row in inventory.items():
        data=z.read(name)
        assert len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256']
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
write(out/'integrity.json',{'archive':raw.name,'sha256':digest(raw),'bytes':raw.stat().st_size,'members':inventory,'crc_and_all_members_verified':True})
(out/'main-ci-observed.json').write_bytes(subprocess.check_output(['gh','run','view','38883652469','--json','status,conclusion,headSha,url,jobs'],cwd=root))
write(out/'diagnosis.json',{'original_main_ci_run':38883652469,'original_commit':'c36baa8145e9e7b51e5667f4e4eaa0242256fc6e',
    'original_browser_outcomes':{'passed':85,'failed':1,'skipped':4},
    'original_failure':'Firefox lead-report element absent through 90-second expectation; original page/error context was not uploaded.',
    'root_cause_established':False,'unchanged_functional_test_diagnostic':{'runs':16,'passed':16,'workers':8,'search_seconds':1,'affinity':'CCD1'},
    'initial_diagnostic_selector_error':'Anchored title matched no tests; retained; corrected selector listed one test before execution.',
    'diagnostic_helper_intermediate_failure':'Reusing the existing helper treated expected contour-review .error flags as fatal; two local failures preserved. Scope now uses the app role=alert.',
    'final_changed_feature_suite':{'passed':28,'failed':0,'browsers':['chromium','firefox'],'affinity':'CCD1'},
    'changed_test_search_budget':False,'weakened_feature_assertions':False,'released_product_changed':False,
    'CI_change':'Retain failure screenshots, traces and error context; report actual nesting alerts instead of waiting only for a lead report.',
    'hosted_confirmation_pending':True,'release_workflow_and_published_package_checks_pass':True})
for source in ['web/tests/features.spec.ts','web/playwright.config.ts','.github/workflows/ci.yml']:
    dest=out/'snapshots'/source;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/source,dest)
shutil.copyfile(__file__,out/'record.py')
report='''# Follow-up main CI browser observation — 2026-10-16

The [separate main check on c36baa8](https://github.com/skulitom/Nestbolt/actions/runs/38883652469)
has **85 passed, one failed, four skipped** browser tests. Firefox never shows
`.lead-report` within the original 90-second expectation in the one-second lead
fixture. The job did not upload its error context, so the actual page state and
root cause are unknown. This is not relabelled as a pass or an infrastructure
failure. The separately successful release workflow and actual published native
download checks remain recorded in the [publication report](preview-depth-published-20261016.md).

All sixteen local repetitions of the unchanged Firefox functional test pass on
CCD1 with eight concurrent workers and the original one-second search budget.
The first diagnostic command matched no tests because its title expression was
anchored; that launch and the corrected, explicitly listed selection are retained.
Local success does not replace the hosted failure or establish its cause.

The test now waits for either the result or the app's fatal alert and reports the
alert text. An intermediate attempt reused a helper that treated all `.error`
elements as fatal, including expected contour-review flags; both resulting local
failures and screenshots are retained. The helper now uses the application's
`role=alert`, preserving all lead coverage, geometry, export and flagged-contour
assertions. The complete affected feature suite passes **28/28** in Chromium and
Firefox on CCD1. No product behavior, search budget or acceptance limit changed.

Hosted failures now retain screenshot, Playwright trace and error-context files
for seven days. Fresh hosted confirmation is pending; the original cause remains
unresolved. The [diagnosis](preview-depth-followup-ci-20261016/diagnosis.json)
and [raw archive](preview-depth-followup-ci-20261016/raw.zip) preserve all observations.
No new quality measurement, reserved evaluation or milestone change occurs.
'''
(out.parent/(out.name+'.md')).write_text(report,encoding='utf-8',newline='\n')
notice='''

**Follow-up browser CI:** the [separate c36baa8 main run](../benchmarks/results/preview-depth-followup-ci-20261016.md)
has one Firefox lead-report failure (85 browser tests pass, four skip). Sixteen
unchanged local repetitions pass, and the affected 28-test suite passes after
improving error diagnostics. The original hosted cause is unresolved; new CI
retains failure screenshots/traces. Release workflow and actual native download
checks pass separately. Product behavior and gate thresholds are unchanged.
'''
for rel in ['docs/STATUS.md','docs/RELEASE_READINESS.md']:
    path=root/rel;text=path.read_text(encoding='utf-8')
    at=text.index('\n## ',text.index('\n')+1) if rel.endswith('RELEASE_READINESS.md') else text.index('\n**Release readiness')
    text=text[:at]+notice+'\n'+text[at:]
    path.write_text(text,encoding='utf-8',newline='\n')
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write('''

## 2026-10-16 — Follow-up Firefox CI failure retained; diagnostics improved

[Main CI on c36baa8](benchmarks/results/preview-depth-followup-ci-20261016.md)
reports one missing lead-report failure in Firefox, 85 browser passes and four
skips. Its page state was not uploaded; the cause remains unresolved. Sixteen
unchanged local repetitions pass with eight workers on CCD1. A helper adaptation
initially mistook expected lead flags for fatal errors; two failures remain
preserved. Scoping it to the app alert retains all original assertions and the
one-second budget; all 28 affected Chromium/Firefox feature tests then pass.
Failure screenshot/trace/context uploads are added for future hosted diagnosis.
This is functional evidence, not a quality measurement or replacement of the
original failed hosted result. Release and published native-download checks pass
separately. No product, reserved split or milestone weight changes.

Documentation link review also corrects STATUS's old seed-2 warm-start report
link to `sheets-ab-rects-30s-s2-20261012T143733Z-b0a39fa9.md`. The original
BENCHMARKS entry is preserved; only its historical link target was mistyped.
''')
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:
    f.write('\nbenchmarks/results/preview-depth-followup-ci-20261016/** -text -whitespace\n')
print(json.dumps({'original_CI_failure_preserved':True,'diagnostic_archive_members':len(inventory),'archive_bytes':raw.stat().st_size,'fresh_hosted_check_pending':True}))
