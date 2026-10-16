"""Finish read-only provenance verification without rerunning successful package tests."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
out = root / 'benchmarks/results/preview-depth-published-20261016'
download = root / 'output/preview-depth-published-20261016'
retry = out / 'attestation-sequential'
retry.mkdir(exist_ok=False)
repo = 'skulitom/Nestbolt'
tag = 'v0.2.0-alpha.1'
commit = 'c36baa8145e9e7b51e5667f4e4eaa0242256fc6e'
def digest(path):
    return sha256(path.read_bytes()).hexdigest()
def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')
def gh(*args):
    return json.loads(subprocess.check_output(['gh', *args], cwd=root, timeout=120))
package = json.loads((out/'checks.json').read_bytes())
assert package['all_checks_passed'] and package['release_commit'] == commit
assert not package['dry_run_only'] and all(x['exit_code'] == 0 for x in package['downloaded_Windows_archive_and_MCPB_smokes'])
original = {p.relative_to(out).as_posix(): {'sha256':digest(p),'bytes':p.stat().st_size}
            for p in out.iterdir() if p.is_file()}
write(retry/'plan.json', {'cause':'Concurrent GitHub CLI verifiers contend over the same Windows Sigstore TUF cache; three fail before verification, one succeeds.',
    'action':'Verify all four assets sequentially with identical provenance policy.',
    'original_results_preserved':original, 'package_tests_repeated':False,
    'assets_redownloaded_or_replaced':False, 'started_at':datetime.now(timezone.utc).isoformat()})
checksums = {}
for line in (download/'assets/SHA256SUMS').read_text(encoding='utf-8').splitlines():
    value,name = line.split(maxsplit=1)
    name = name.removeprefix('*')
    assert Path(name).name == name and name not in checksums and digest(download/'assets'/name) == value
    checksums[name] = value
for item in package['archives']:
    assert checksums[item['file']] == item['sha256']
assert checksums['nestbolt-windows-x64.mcpb'] == package['MCPB_sha256']
provenance = []
for name in [x['file'] for x in package['archives']] + ['nestbolt-windows-x64.mcpb']:
    command = ['gh','attestation','verify',str(download/'assets'/name),'--repo',repo,
        '--signer-workflow',repo+'/.github/workflows/release.yml',
        '--source-digest',commit,'--source-ref','refs/tags/'+tag,
        '--deny-self-hosted-runners','--format','json']
    result = subprocess.run(command, cwd=root, capture_output=True, timeout=180)
    (retry/(name+'.json')).write_bytes(result.stdout)
    (retry/(name+'-stderr.log')).write_bytes(result.stderr)
    assert result.returncode == 0, (name,result.stderr.decode(errors='replace'))
    verified = json.loads(result.stdout)
    assert isinstance(verified,list) and verified
    provenance.append({'asset':name,'sha256':digest(download/'assets'/name),'exit_code':result.returncode,
        'command':command,'verified_attestations':len(verified)})
    print(json.dumps({'verified':name}),flush=True)
workflow = gh('run','view','38882959832','--json','conclusion,headSha,jobs,url,status,event,headBranch')
assert workflow['conclusion'] == 'success' and workflow['headSha'] == commit
assert workflow['event'] == 'push' and workflow['headBranch'] == tag
assert all(j['conclusion'] == 'success' for j in workflow['jobs'])
release = gh('release','view',tag,'-R',repo,'--json','assets,isPrerelease,isDraft,tagName,url,targetCommitish,publishedAt,body')
assert release['tagName'] == tag and release['isPrerelease'] and not release['isDraft']
assert {a['name'] for a in release['assets']} == set(checksums)|{'SHA256SUMS'}
for a in release['assets']:
    path = download/'assets'/a['name']
    assert path.stat().st_size == a['size']
    assert a['digest'] == 'sha256:'+digest(path)
ref = gh('api',f'repos/{repo}/git/ref/tags/{tag}')['object']
while ref['type'] == 'tag':
    ref = gh('api',f'repos/{repo}/git/tags/'+ref['sha'])['object']
assert ref['type'] == 'commit' and ref['sha'] == commit
latest = gh('api',f'repos/{repo}/releases/latest')
before = json.loads((root/'output/preview-depth-tag-20261016/preflight.json').read_bytes())['stable_latest']
assert latest['id'] == before['id'] and latest['tag_name'] == before['tag'] == 'v0.1.0'
assert not latest['prerelease']
assets = [{k:a[k] for k in ['id','name','size','digest']} for a in latest['assets']]
assert sorted(assets,key=lambda a:a['id']) == sorted(before['assets'],key=lambda a:a['id'])
for name, entry in original.items():
    assert digest(out/name) == entry['sha256'], name
write(out/'release.json',release)
write(out/'latest.json', {'tag':latest['tag_name'],'url':latest['html_url'],'prerelease':False,'id':latest['id'],'assets':assets})
shutil.copyfile(download/'assets/SHA256SUMS',out/'SHA256SUMS')
shutil.copyfile(__file__,out/'finish_provenance.py')
shutil.copyfile(root/'output/complete_published_depth_verification.py',out/'verify_publication.py')
write(out/'publication-verification.json',{'all_checks_passed':True,'tag':tag,'commit':commit,
    'release_url':release['url'],'release_workflow':workflow['url'],'is_prerelease':True,
    'stable_latest':latest['tag_name'],'checksums':checksums,'stable_latest_and_asset_snapshot_unchanged':True,
    'all_four_artifacts_have_verified_provenance':True,'provenance':provenance,
    'actual_published_Windows_archive_and_MCPB_smokes_pass':True,
    'registry_publication_performed_by_this_verification':False,
    'initial_concurrent_cache_errors_preserved':True,'verified_at':datetime.now(timezone.utc).isoformat()})
inventory = {p.relative_to(out).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size}
             for p in sorted(out.rglob('*')) if p.is_file() and p.name != 'integrity.json'}
write(out/'integrity.json',inventory)
print(json.dumps({'published_downloads_verified':True,'provenance_verified':4,'stable_latest':latest['tag_name']}))
