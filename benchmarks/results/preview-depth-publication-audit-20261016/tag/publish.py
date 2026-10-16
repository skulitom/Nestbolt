"""Publish the user-authorized qualified preview tag, never overwrite an existing tag."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
import subprocess
import sys
import tomllib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/preview-depth-tag-20261016'
TAG='v0.2.0-alpha.1'
COMMIT='c36baa8145e9e7b51e5667f4e4eaa0242256fc6e'
CI_COMMIT='21835bad284fd6fef494a3639e214db0cd2c12bd'
DRY_COMMIT='23442be38ee2e881669e753bc405ab3269ff1b39'
REPO='skulitom/Nestbolt'
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def run(*args):return subprocess.check_output(list(args),cwd=ROOT,timeout=180)
def git(*args):return run('git',*args)
def gh(*args):return run('gh',*args)
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')

assert not OUT.exists()
OUT.mkdir()
assert git('rev-parse','HEAD').decode().strip()==COMMIT
subprocess.run(['git','diff','--quiet'],cwd=ROOT,check=True)
subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT,check=True)
assert tomllib.loads((ROOT/'Cargo.toml').read_text(encoding='utf-8'))['workspace']['package']['version']==TAG[1:]
assert source_digest()=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
allowed={'.gitattributes','BENCHMARKS.md','docs/STATUS.md','docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md','docs/RELEASE_READINESS.md','mcpb/RELEASE_NOTES.md'}
differences={}
for base in [CI_COMMIT,DRY_COMMIT]:
    changed=git('diff','--name-only',base,COMMIT).decode().splitlines()
    assert all(p in allowed or p.startswith('benchmarks/results/') for p in changed),changed
    differences[base]=changed
# The sole distribution-document change since the dry run explains the hosted
# browser's older deployment. Packaging code, archives' README and binaries'
# complete source/build/test inputs have not changed.
assert git('diff','--name-only',CI_COMMIT,COMMIT,'--','mcpb')==b''
ci=json.loads(gh('run','view','38857882488','-R',REPO,'--json','conclusion,headSha,jobs,url,status'))
assert ci['headSha']==CI_COMMIT and ci['status']=='completed' and ci['conclusion']=='success'
assert len(ci['jobs'])==6 and all(j['conclusion']=='success' for j in ci['jobs'])
write(OUT/'tested-ci.json',ci)
proofs={
    'H4':'benchmarks/results/h4-depth-complete-20261016/checks.json',
    'integration':'benchmarks/results/h4-depth-integration-20261016/checks.json',
    'packages':'benchmarks/results/preview-depth-release-dryrun-20261016/checks.json',
    'features':'benchmarks/results/preview-depth-features-20261016/checks.json',
    'completed_features':'benchmarks/results/preview-depth-completed-features-20261016/checks.json'}
p={k:load(ROOT/v) for k,v in proofs.items()}
assert p['H4']['all_explicit_H4_requirements_pass'] and p['H4']['completed_weight_percent']==60
assert p['integration']['all_checks_passed'] and not p['integration']['H5_exchange_integrated']
assert p['packages']['all_checks_passed'] and p['packages']['release_commit']==DRY_COMMIT
assert p['features']['all_checks_pass'] and p['completed_features']['all_review_checks_pass']
subprocess.run(['git','fetch','origin'],cwd=ROOT,check=True,timeout=180)
remote_main=git('rev-parse','origin/main').decode().strip()
subprocess.run(['git','merge-base','--is-ancestor',remote_main,COMMIT],cwd=ROOT,check=True)
assert not git('ls-remote','origin','refs/tags/'+TAG).strip()
assert subprocess.run(['git','show-ref','--verify','--quiet','refs/tags/'+TAG],cwd=ROOT).returncode==1
releases=json.loads(gh('api',f'repos/{REPO}/releases?per_page=100'))
assert all(r['tag_name']!=TAG for r in releases)
latest=json.loads(gh('api',f'repos/{REPO}/releases/latest'))
assert latest['tag_name']=='v0.1.0' and not latest['prerelease']
stable={'id':latest['id'],'tag':latest['tag_name'],'url':latest['html_url'],
    'assets':[{k:a[k] for k in ['id','name','size','digest']} for a in latest['assets']]}
current_ci=json.loads(gh('run','view','38878505590','-R',REPO,'--json','conclusion,headSha,jobs,url,status'))
write(OUT/'newer-main-ci.json',current_ci)
preflight={'tag':TAG,'commit':COMMIT,'utc':datetime.now(timezone.utc).isoformat(),
    'user_authorization':'docs/PLAN_V1_1.md reviewed decision 7, 2026-10-16; next GitHub release when ready',
    'product_digest':source_digest(),'tested_ci_commit':CI_COMMIT,'tested_ci_run':ci['url'],
    'dry_run_commit':DRY_COMMIT,'only_evidence_and_reviewed_documentation_differs':differences,
    'evidence_sha256':{name:digest(ROOT/path) for name,path in proofs.items()},'evidence_paths':proofs,
    'stable_latest':stable,'remote_main':remote_main,
    'newer_main_ci_disposition':'Recorded separately; keep it running. This tag retains all application/build/test inputs of the completed successful CI.',
    'expected_prerelease':True,'expected_latest':False,'registry_publication_authorized_or_started':False,
    'H2_H5_disclosed_open':True,'all_prepublication_checks_pass':True}
write(OUT/'preflight.json',preflight)
(OUT/'publish.py').write_bytes(Path(__file__).read_bytes())
subprocess.run(['git','tag','-a',TAG,COMMIT,'-m','Nestbolt 0.2.0-alpha.1: LightBurn preservation, import controls and lead allowances preview'],cwd=ROOT,check=True)
assert git('rev-parse',TAG+'^{commit}').decode().strip()==COMMIT
policy=json.loads(run('node','mcpb/release.mjs',TAG));assert policy=={'prerelease':True,'latest':False}
write(OUT/'policy.json',policy)
pushed=subprocess.run(['git','push','origin','refs/tags/'+TAG],cwd=ROOT,capture_output=True,timeout=180)
(OUT/'push-stdout.log').write_bytes(pushed.stdout);(OUT/'push-stderr.log').write_bytes(pushed.stderr)
assert pushed.returncode==0,'Retain tag/preflight and inspect push result; never recreate or force a tag.'
remote=git('ls-remote','origin','refs/tags/'+TAG,'refs/tags/'+TAG+'^{}').decode().splitlines()
assert any(line.split()==[COMMIT,'refs/tags/'+TAG+'^{}'] for line in remote)
write(OUT/'tag-pushed.json',{'tag':TAG,'commit':COMMIT,'utc':datetime.now(timezone.utc).isoformat(),
    'remote_refs':remote,'ordinary_non_forced_push':True,'publication_workflow_started_by_tag':True,
    'release_assets_not_yet_verified':True,'stable_latest_preserved_by_policy':True,'registry_publication_started':False})
print(json.dumps({'tag_pushed':TAG,'commit':COMMIT,'prerelease':True,'latest':False,'release_build_and_download_verification_pending':True}))
