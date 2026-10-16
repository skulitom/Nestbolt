"""Seal completed production checks without replacing earlier candidate evidence."""
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/preview-integration-20261016'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
checks=load(OUT/'checks.json')
assert checks['all_checks_passed'] and all(s['exit_code']==0 for s in checks['stages'])
totals={}
for stage in ['workspace','optimized-cli','optimized-sparrow','stock-helper']:
    matches=re.findall(r'test result: ok\. (\d+) passed; (\d+) failed; (\d+) ignored', (OUT/(stage+'-stdout.log')).read_text(encoding='utf-8'))
    assert matches
    totals[stage]={'passed':sum(int(r[0]) for r in matches),'failed':sum(int(r[1]) for r in matches),'ignored':sum(int(r[2]) for r in matches)}
assert totals['workspace']=={'passed':302,'failed':0,'ignored':1}
assert totals['optimized-cli']['passed']==27
packaging=(OUT/'packaging-stdout.log').read_text(encoding='utf-8')
assert re.search(r'\bpass 23\b',packaging) and re.search(r'\bfail 0\b',packaging) and re.search(r'\bskipped 1\b',packaging)
web=(OUT/'web-build-and-tests-stdout.log').read_text(encoding='utf-8')
assert re.search(r'86 passed',web) and re.search(r'4 skipped',web)
assert '2 failed' not in web and '1 failed' not in web
candidate=load(ROOT/'benchmarks/results/release-surface-probe-20261016-v2/checks.json')
for name,expected in candidate['core_source'].items():
    assert digest(ROOT/'crates/core/src'/name)==expected,name
integration=load(OUT/'integration.json')
paths=integration['copied']+['Cargo.toml','Cargo.lock','web/package.json','web/package-lock.json','server.json',
    'README.md','llms.txt','mcpb/manifest.json','mcpb/RELEASE_NOTES.md','mcpb/PUBLISHING.md',
    'docs/LBRN2.md','scripts/h4_preview_matrix.py','output/ccd1.py']
for name in paths:
    target=OUT/'snapshots'/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/name,target)
shutil.copyfile(__file__,OUT/'finalize.py')
write(OUT/'verification.json',{'all_checks_passed':True,'native_totals':totals,
    'packaging':{'passed':23,'skipped':1,'real_release_cli_and_MCPB_checks_passed':True},
    'browser':{'passed':86,'opt_in_skipped':4,'new_message_viewport_assertions_passed':True},
    'production_core_identical_to_reviewed_candidate':True,
    'frozen_inventory':{'files':1181,'manifest_sha256':'02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7','verified':True},
    'harness_preflights':[{'action':'Python gate tests','initial':'Interpreter omitted from affinity wrapper; Windows error 193 before test execution','corrected':'Five tests pass with explicit Python interpreter'},
      {'action':'Frozen inventory check','initial':'Global Python lacked ezdxf; no input evaluation','corrected':'Pinned shop virtual environment verifies all 1181 hashes'}],
    'held_out_geometry_evaluated':False,'performance_and_remote_release_checks_pending':True})
archive=OUT/'raw.zip'
assert not archive.exists()
files=sorted(p for p in OUT.rglob('*') if p.is_file())
inventory={p.relative_to(ROOT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in files}
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,expected in inventory.items():
        raw=z.read(name)
        assert len(raw)==expected['bytes'] and sha256(raw).hexdigest()==expected['sha256']
write(OUT/'integrity.json',{'archive':archive.relative_to(ROOT).as_posix(),'sha256':digest(archive),
    'bytes':archive.stat().st_size,'members':inventory,'crc_and_every_member_verified':True})
# Consolidate only raw browser artifacts, keeping all logs and source snapshots.
folder=(OUT/'browser-artifacts').resolve()
assert OUT.resolve() in folder.parents
for p in sorted(folder.rglob('*'),reverse=True):
    assert folder in p.resolve().parents
    if p.is_file():
        assert digest(p)==inventory[p.relative_to(ROOT).as_posix()]['sha256']
        p.unlink()
    elif p.is_dir() and not any(p.iterdir()):p.rmdir()
folder.rmdir()
print(json.dumps({'tests':totals,'archive_sha256':digest(archive),'archive_bytes':archive.stat().st_size,'members':len(inventory)}))
