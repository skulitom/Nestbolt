"""Preserve both timeout diagnosis and local validation before hosted CI."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil,subprocess
from pack_h5_evidence_archive import pack,digest
ROOT=Path(__file__).resolve().parents[1];NAME='ci-sparse-evidence-checkout-20261026';OUT=ROOT/'benchmarks/results'/NAME
BASE=ROOT/'output/ci-sparse-checkout-20261026';CAP=ROOT/'output/ci-checkout-timeout-20261026'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2);f.write('\n')
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
checks=load(BASE/'checks.json');selection=load(BASE/'selection.json');assert checks['passed'] and checks['existing_python_CI_commands_passed']==31
job=load(CAP/'job.json');assert job['conclusion']=='cancelled'
build=next(s for s in job['steps'] if s['name']=='Build the browser app and run Chromium and Firefox tests');assert build['conclusion']=='skipped'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==checks['source_head']
workflow=ROOT/'.github/workflows/ci.yml';old=subprocess.check_output(['git','show','HEAD:.github/workflows/ci.yml'],cwd=ROOT).decode()
new=workflow.read_text(encoding='utf-8');addition='          sparse-checkout: |\n            /*\n            !/benchmarks/results/**/*.zip\n          sparse-checkout-cone-mode: false\n'
assert new.replace('          # Historical evidence archives are not inputs to these checks.\n','').replace(addition,'')==old
OUT.mkdir()
for src,name in [(BASE/'checks.json','local-checks.json'),(BASE/'selection.json','selection.json'),(BASE/'dependency-review.json','dependency-review.json'),
                 (CAP/'step-times.json','attempt2-step-times.json'),(CAP/'annotations.json','attempt2-annotations.json'),(workflow,'candidate-ci.yml')]:shutil.copyfile(src,OUT/name)
members={}
for folder in [BASE,CAP]:
    for p in folder.iterdir():
        if p.is_file():members[folder.name+'/'+p.name]=p
for n in ['verify_ci_sparse_checkout.py','capture_ci_checkout_timeout.py','pack_h5_evidence_archive.py','ccd1.py']:
    p=ROOT/'output'/n;members['helpers/'+n]=p
archive,manifest=pack(ROOT,OUT,NAME,members)
write(OUT/'checks.json',{'passed':True,'utc':datetime.now(timezone.utc).isoformat(),'source_head':head,
 'workflow_sha256':digest(workflow),'only_checkout_patterns_changed':True,'tests_timeouts_dependencies_and_action_pins_unchanged':True,
 'tracked_archives_deleted':0,'excluded_archive_bytes':selection['omitted_bytes'],'excluded_archive_files':selection['omitted_archives'],
 'retained_files_verified':selection['included_files'],'existing_python_CI_commands_passed':31,
 'hosted_checks_pending':True,'main_push_pending':True,'H2_complete':False,'H5_complete':False,'completion_percent':60,**archive})
write(OUT/'next-step.json',{'action':'Commit this CI-only checkout repair and evidence with the four queued H5 checkpoints. Push the existing codex/v1-1-shop-files working branch and dispatch Checks for its exact head. No run on that branch is active and the old main browser attempt2 is terminal. Preserve all old success/failure records. Require all six branch jobs to succeed before a normal fast-forward push to main; verify main has not changed and the branch tree matches the validated commit. Then preserve and observe the new main checks to completion without cancellation. No release or registry publication qualifies from this infrastructure fix.','H2_complete':False,'H5_complete':False,'completion_percent':60})
shutil.copyfile(__file__,OUT/Path(__file__).name)
report=f'''# CI: omit historical evidence ZIPs from test checkouts — 2026-10-26

**Main's browser retry spends 18m07s checking out the repository, then reaches
the 30-minute limit during browser dependency installation. Tests never start.**
The earlier attempt also timed out, primarily during dependency downloads.
Both failures and the other five successful jobs remain preserved.

The current tree contains 4,134,207,071 bytes across 12,000 files. Historical ZIPs
under `benchmarks/results/` account for **3,512,792,276 bytes in 2,496 files**.
All four checkout steps now use the non-cone patterns `/*` and
`!/benchmarks/results/**/*.zip`. All other files remain selected. The pinned
[checkout implementation](https://github.com/actions/checkout/blob/d23441a48e516b6c34aea4fa41551a30e30af803/src/git-source-provider.ts#L182)
automatically fetches with `blob:none` when sparse checkout is supplied, so the
omitted archives need not be downloaded before checkout. Its original MIT licence
is preserved with the inspected upstream sources in the archive.

No repository evidence is deleted. Test commands, assertions, timeouts, tool
versions, action pins and benchmark budgets are unchanged. Build fixtures,
frozen inputs, result JSON, reports and published web assets remain available.

## Local validation

A fresh isolated Git checkout uses the exact non-cone patterns. All **9,504
selected files** match their original Git blob IDs; all **2,496 ZIPs** are absent.
The retained tree contains 621,414,795 bytes. The review follows 65 Python modules
reachable from CI entry points; historical-result reads use retained JSON files.
Product and browser tests do not reference the omitted evidence archives.

All **31 existing Python CI commands pass in this checkout**, including notices,
schemas, frozen dataset verification, maker manifests and the report/adapter
tests. Native schema generators also build as part of those checks. Full hosted
native tests, maker rebuilds, benchmark smoke and browser tests remain pending;
local selection and Python passes alone do not replace them.

## Publication sequence

Validate the exact candidate on the existing working branch with the complete
six-job Checks workflow. The old main run is terminal and no working-branch run
is active; starting this validation cancels neither. After all six pass, verify
remote main is unchanged, fast-forward the queued checkpoints and CI repair to
main, then observe that new main run. No release follows from this repair.
H2/H5 remain open at **60%** and all 22 reserved H2 vectors stay unopened.

[Local checks]({NAME}/local-checks.json), [selection inventory]({NAME}/selection.json),
[dependency review]({NAME}/dependency-review.json), [retry timings]({NAME}/attempt2-step-times.json),
[timeout annotations]({NAME}/attempt2-annotations.json), [workflow]({NAME}/candidate-ci.yml),
[next step]({NAME}/next-step.json), [manifest]({NAME}/raw-manifest.json).
The raw archive verifies {archive['archive_members']} canonical files and
{archive['verified_aliases']} identical-content aliases by bytes, SHA-256 and CRC.
'''
with (ROOT/'benchmarks/results'/f'{NAME}.md').open('x',encoding='utf-8',newline='\n') as f:f.write(report)
note='''\n\n**CI checkout repair, 2026-10-26:** [the diagnosis and local checks]({link})
preserve main36f162d0's second browser timeout:18m07s checkout, tests never started.
The four CI checkouts now omit only historical result ZIPs, avoiding3.51GB while
retaining all9,504 other files byte-for-byte. No evidence is deleted and all test
commands/timeouts remain unchanged. All31 existing Python CI commands pass in an
isolated sparse checkout. Full six-job validation will run on the working branch
before the normal main push; old runs remain preserved. H2/H5 remain open at60%,
all22 reserved vectors remain unopened and no release qualifies.\n'''
for n in ['BENCHMARKS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/STATUS.md']:
    append(ROOT/n,note.format(link=('' if n=='BENCHMARKS.md' else '../')+f'benchmarks/results/{NAME}.md'))
append(ROOT/'.gitattributes',f'\nbenchmarks/results/{NAME}/** -text -whitespace\n')
print({'sealed':NAME,**archive})
