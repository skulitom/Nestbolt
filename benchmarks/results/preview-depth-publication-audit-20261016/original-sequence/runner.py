"""Wait for the authorized tag build, then verify its actual published downloads once."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
import os
import subprocess
import sys
import time
import traceback

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/preview-depth-publication-sequence-20261016'
RUN='38882959832'
COMMIT='c36baa8145e9e7b51e5667f4e4eaa0242256fc6e'
TAG='v0.2.0-alpha.1'
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def utc():return datetime.now(timezone.utc).isoformat()
assert not OUT.exists()
OUT.mkdir()
commands=[['python','output/verify_published_depth_preview.py','--run',RUN,'--commit',COMMIT],
          ['python','output/verify_published_depth_features.py']]
helpers=['output/verify_published_depth_preview.py','output/verify_published_depth_features.py',
    'output/verify_preview_depth_dryrun.py','output/check_downloaded_depth_features.py',
    'output/check_downloaded_depth_features.mjs','output/seal_downloaded_depth_features.py']
plan={'run':RUN,'commit':COMMIT,'tag':TAG,'commands':commands,'helpers':{n:digest(ROOT/n) for n in helpers},
    'production_digest':source_digest(),'prepublication_sha256':digest(ROOT/'output/preview-depth-tag-20261016/preflight.json'),
    'poll_seconds':30,'wait_limit_seconds':5400,'no_automatic_retry_or_republication':True,
    'scope':'Read the already dispatched tag workflow; then download, verify and test its published artifacts on CCD1. Never publish a registry version.'}
assert plan['production_digest']=='8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
write(OUT/'plan.json',plan)
write(OUT/'opened.json',{'pid':os.getpid(),'utc':utc(),'plan_sha256':digest(OUT/'plan.json')})
(OUT/'runner.py').write_bytes(Path(__file__).read_bytes())
stages=[];started=time.monotonic();last=None
try:
    while True:
        raw=subprocess.check_output(['gh','run','view',RUN,'-R','skulitom/Nestbolt','--json','status,conclusion,headSha,headBranch,url,jobs,event'],cwd=ROOT,timeout=120)
        state=json.loads(raw)
        assert state['headSha']==COMMIT and state['headBranch']==TAG and state['event']=='push'
        write(OUT/'workflow-latest.json',state)
        compact={k:state[k] for k in ['status','conclusion']}
        compact['jobs']=[{k:j[k] for k in ['name','status','conclusion']} for j in state['jobs']]
        if compact!=last:
            print(json.dumps(compact),flush=True);last=compact
        if state['status']=='completed':
            assert state['conclusion']=='success' and all(j['conclusion']=='success' for j in state['jobs'])
            break
        assert time.monotonic()-started<5400,'Publication build wait cap reached; retain state and inspect the same run.'
        time.sleep(30)
    for index,command in enumerate(commands):
        assert source_digest()==plan['production_digest']
        assert all(digest(ROOT/n)==h for n,h in plan['helpers'].items())
        begin=utc()
        with (OUT/f'stage-{index}-stdout.log').open('xb') as out,(OUT/f'stage-{index}-stderr.log').open('xb') as err:
            result=subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),*command],cwd=ROOT,stdout=out,stderr=err,timeout=900)
        row={'index':index,'command':command,'started':begin,'finished':utc(),'exit_code':result.returncode,
            'stdout_sha256':digest(OUT/f'stage-{index}-stdout.log'),'stderr_sha256':digest(OUT/f'stage-{index}-stderr.log')}
        stages.append(row);write(OUT/'progress.json',stages);print(json.dumps(row),flush=True)
        assert result.returncode==0,'Original verification failure retained; inspect it before any follow-up.'
    write(OUT/'completed.json',{'stages':stages,'finished':utc(),'published_downloads_provenance_and_authored_features_verified':True,
        'commit':COMMIT,'tag':TAG,'registry_publication_started':False,'goal_complete':False})
except BaseException:
    write(OUT/'interruption.json',{'error':traceback.format_exc(),'stages':stages,'utc':utc()});raise
