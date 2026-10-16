"""Verify an already published preview; this script never creates a release."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TAG = 'v0.2.0-alpha.1'
REPO = 'skulitom/Nestbolt'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--run', required=True, type=int)
parser.add_argument('--commit', required=True)
args = parser.parse_args()
COMMIT = args.commit
assert len(COMMIT) == 40 and all(c in '0123456789abcdef' for c in COMMIT)
prepublication = json.loads((ROOT/'output/preview-depth-tag-20261016/preflight.json').read_bytes())
assert prepublication['commit'] == COMMIT and prepublication['tag'] == TAG
assert prepublication['all_prepublication_checks_pass']
# Evidence/docs may advance after qualification; measured product inputs may not.
subprocess.run(['git','diff','--quiet','aba989e1173f64ca1f273af1c839bd990d8cea05',
    COMMIT,'--','crates','web/src','Cargo.toml','Cargo.lock','rust-toolchain.toml',
    '.cargo','web/package.json','web/package-lock.json'],cwd=ROOT,check=True)
DOWNLOAD = ROOT/'output/preview-depth-published-20261016'
OUT = ROOT/'benchmarks/results/preview-depth-published-20261016'
assert not DOWNLOAD.exists() and not OUT.exists(), 'Preserve any earlier verification attempt'
DOWNLOAD.mkdir()

def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')
def gh(*arguments):
    return subprocess.check_output(['gh', *map(str, arguments)], cwd=ROOT, timeout=180)
def digest(path):
    return sha256(path.read_bytes()).hexdigest()

workflow_raw = gh('run','view',args.run,'--json','conclusion,headSha,jobs,url,status,event,headBranch')
workflow = json.loads(workflow_raw)
assert workflow['conclusion'] == 'success' and workflow['headSha'] == COMMIT
assert workflow['event'] == 'push' and workflow['headBranch'] == TAG
assert all(job['conclusion'] == 'success' for job in workflow['jobs'])
assert any(job['name'] == 'release' for job in workflow['jobs'])
(DOWNLOAD/'workflow.json').write_bytes(workflow_raw)
release = json.loads(gh('release','view',TAG,'-R',REPO,'--json',
    'assets,isPrerelease,isDraft,tagName,url,targetCommitish,publishedAt,body'))
assert release['tagName'] == TAG and release['isPrerelease'] and not release['isDraft']
latest = json.loads(gh('api',f'repos/{REPO}/releases/latest'))
assert latest['tag_name'] != TAG and not latest['prerelease']
stable_before = prepublication['stable_latest']
assert latest['id'] == stable_before['id'] and latest['tag_name'] == stable_before['tag']
stable_assets = [{k: a[k] for k in ['id','name','size','digest']} for a in latest['assets']]
assert sorted(stable_assets,key=lambda a:a['id']) == sorted(stable_before['assets'],key=lambda a:a['id'])
tag = json.loads(gh('api',f'repos/{REPO}/git/ref/tags/{TAG}'))['object']
for _ in range(5):
    if tag['type'] == 'commit':
        break
    assert tag['type'] == 'tag'
    tag = json.loads(gh('api',f'repos/{REPO}/git/tags/'+tag['sha']))['object']
assert tag['type'] == 'commit' and tag['sha'] == COMMIT
write(DOWNLOAD/'release.json',release)
write(DOWNLOAD/'latest.json',{'tag':latest['tag_name'],'url':latest['html_url'],'prerelease':latest['prerelease']})
archives = {
    'windows': f'nestbolt-{TAG}-x86_64-pc-windows-msvc.zip',
    'linux': f'nestbolt-{TAG}-x86_64-unknown-linux-gnu.tar.gz',
    'macos': f'nestbolt-{TAG}-aarch64-apple-darwin.tar.gz',
}
expected = set(archives.values()) | {'nestbolt-windows-x64.mcpb','nestbolt-windows-x64.mcpb.sha256','SHA256SUMS'}
assert {asset['name'] for asset in release['assets']} == expected
subprocess.run(['gh','release','download',TAG,'-R',REPO,'-D',str(DOWNLOAD/'assets')],cwd=ROOT,check=True,timeout=180)
assert {p.name for p in (DOWNLOAD/'assets').iterdir()} == expected
checksums = {}
for line in (DOWNLOAD/'assets/SHA256SUMS').read_text(encoding='utf-8').splitlines():
    value, name = line.split(maxsplit=1)
    name = name.removeprefix('*')
    assert len(value) == 64 and Path(name).name == name and name not in checksums
    assert digest(DOWNLOAD/'assets'/name) == value
    checksums[name] = value
assert set(checksums) == expected-{'SHA256SUMS'}
for platform, name in archives.items():
    (DOWNLOAD/platform).mkdir()
    shutil.copyfile(DOWNLOAD/'assets'/name,DOWNLOAD/platform/name)
for name in ['nestbolt-windows-x64.mcpb','nestbolt-windows-x64.mcpb.sha256']:
    shutil.copyfile(DOWNLOAD/'assets'/name,DOWNLOAD/'windows'/name)

artifacts = json.loads(gh('api',f'repos/{REPO}/actions/runs/{args.run}/artifacts'))['artifacts']
assert any(a['name'] == 'nestbolt-mcpb' and not a['expired'] for a in artifacts)
subprocess.run(['gh','run','download',str(args.run),'-n','nestbolt-mcpb','-D',str(DOWNLOAD/'workflow-bundle')],
    cwd=ROOT,check=True,timeout=180)
for name in ['nestbolt-windows-x64.mcpb','nestbolt-windows-x64.mcpb.sha256']:
    assert (DOWNLOAD/'workflow-bundle'/name).read_bytes() == (DOWNLOAD/'assets'/name).read_bytes()
shutil.copyfile(DOWNLOAD/'workflow-bundle/server.registry.json',DOWNLOAD/'windows/server.registry.json')

# Reuse the already exercised archive/bundle verifier, adjusting only its
# locations and the expected successful publication status. Keep it separate.
source = (ROOT/'output/verify_preview_depth_dryrun.py').read_text(encoding='utf-8')
replacements = [
    ('23442be38ee2e881669e753bc405ab3269ff1b39', COMMIT),
    ('23442be', COMMIT[:7]),
    ('Verify downloaded dry-run packages without observing the active benchmark tree.', 'Verify published packages from an isolated copy of the verified package tools.'),
    ('output/preview-depth-release-dryrun-38854620093', 'output/preview-depth-published-20261016'),
    ('benchmarks/results/preview-depth-release-dryrun-20261016', 'benchmarks/results/preview-depth-published-20261016'),
    ("['conclusion']=='skipped'", "['conclusion']=='success'"),
    ("'dry_run_only':True,'release_job_skipped':True", "'dry_run_only':False,'release_job_skipped':False"),
    ('Dry runs do not attest; verify published artifact attestation after release', 'Published-artifact provenance is checked by the surrounding verification script'),
    (",'performance_and_release_commit_CI_pending':True", ''),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before,after)
verifier = ROOT/'output/verify_published_depth_preview_packages.py'
assert not verifier.exists()
compile(source,str(verifier),'exec')
verifier.write_text(source,encoding='utf-8',newline='\n')
subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),str(verifier)],cwd=ROOT,check=True,timeout=300)
package = json.loads((OUT/'checks.json').read_bytes())
assert package['all_checks_passed'] and not package['dry_run_only']

def attest(name):
    command = ['gh','attestation','verify',str(DOWNLOAD/'assets'/name),'--repo',REPO,
        '--signer-workflow',REPO+'/.github/workflows/release.yml',
        '--source-digest',COMMIT,'--source-ref','refs/tags/'+TAG,
        '--deny-self-hosted-runners','--format','json']
    completed = subprocess.run(command,cwd=ROOT,capture_output=True,timeout=180)
    (OUT/(name+'-attestation.json')).write_bytes(completed.stdout)
    (OUT/(name+'-attestation-stderr.log')).write_bytes(completed.stderr)
    assert completed.returncode == 0, name
    verified = json.loads(completed.stdout)
    assert isinstance(verified,list) and verified
    return {'asset':name,'sha256':digest(DOWNLOAD/'assets'/name),'exit_code':completed.returncode,
            'command':command,'verified_attestations':len(verified)}

with ThreadPoolExecutor(max_workers=4) as pool:
    provenance = list(pool.map(attest,[*archives.values(),'nestbolt-windows-x64.mcpb']))
for name in ['release.json','latest.json']:
    shutil.copyfile(DOWNLOAD/name,OUT/name)
shutil.copyfile(DOWNLOAD/'assets/SHA256SUMS',OUT/'SHA256SUMS')
shutil.copyfile(__file__,OUT/'verify_publication.py')
write(OUT/'publication-verification.json',{'all_checks_passed':True,'tag':TAG,'commit':COMMIT,
    'release_url':release['url'],'release_workflow':workflow['url'],
    'is_prerelease':True,'stable_latest':latest['tag_name'],'checksums':checksums,
    'stable_latest_and_asset_snapshot_unchanged':True,
    'all_four_artifacts_have_verified_provenance':True,'provenance':provenance,
    'actual_published_Windows_archive_and_MCPB_smokes_pass':True,
    'registry_publication_performed_by_this_verification':False,
    'notes':'Registry metadata validation and a GitHub release do not publish a registry version.'})
inventory = {p.relative_to(OUT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size}
             for p in sorted(OUT.rglob('*')) if p.is_file()}
write(OUT/'integrity.json',inventory)
print(json.dumps({'published_downloads_verified':True,'provenance_verified':4,
                  'release_url':release['url'],'stable_latest':latest['tag_name']}))
