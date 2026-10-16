"""Run the committed current-profile plan exactly once after all prerequisites."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,subprocess,sys,traceback
import psutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h4-current-profile-plan-20261016'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def inactive(folder,pattern):
    opened=folder/'opened.json'
    if not opened.exists():return
    try:command=psutil.Process(load(opened)['pid']).cmdline()
    except psutil.NoSuchProcess:return
    assert not any(pattern in a for a in command),'Measurement still live: '+pattern
plan=load(OUT/'plan.json')
assert subprocess.check_output(['git','show','HEAD:'+str((OUT/'plan.json').relative_to(ROOT)).replace('\\','/')],cwd=ROOT)==(OUT/'plan.json').read_bytes()
assert not (OUT/'opened.json').exists(),'Preserve the original profile attempt'
matrix=ROOT/'benchmarks/results/h4-preview-score-release-20261016'
sequence=ROOT/'benchmarks/results/h4-preview-score-scale-plan-20261016'
pilot=ROOT/'benchmarks/results/h5-early-exchange-pilot-20261016'
inactive(matrix,'h4_preview_matrix.py');inactive(sequence,'continue_preview_score_checks.py')
assert not (matrix/'interruption.json').exists() and not (sequence/'interruption.json').exists()
assert (matrix/'results.json').exists() and (matrix/'integrity.json').exists()
assert (sequence/'completed.json').exists() or (sequence/'stopped.json').exists()
assert load(matrix/'verification.json')['all_artifact_checks_passed']
assert digest(matrix/'raw.zip')==load(matrix/'integrity.json')['sha256']
# This diagnostic is queued immediately before the already prepared H5 pilot.
assert not (pilot/'opened.json').exists(),'H5 pilot must finish/review before changing the measurement schedule'
assert all(digest(ROOT/name)==value for name,value in plan['files'].items())
sys.path.insert(0,str(ROOT/'scripts'))
import h4_quality
assert h4_quality.guards(plan['jobs'])==plan['guards']
psutil.Process().cpu_affinity(list(range(16,32)))
write(OUT/'opened.json',{'pid':psutil.Process().pid,'utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':digest(OUT/'plan.json')})
try:
    with (OUT/'stdout.log').open('xb') as stdout,(OUT/'stderr.log').open('xb') as stderr:
        p=subprocess.run([sys.executable,str(ROOT/'output/ccd1.py'),sys.executable,'-X','utf8',str(ROOT/'output/profile_current_h4.py')],cwd=ROOT,stdout=stdout,stderr=stderr,timeout=700)
    write(OUT/'execution.json',{'exit_code':p.returncode,'stdout_sha256':digest(OUT/'stdout.log'),'stderr_sha256':digest(OUT/'stderr.log')})
    assert p.returncode==0,'Original profile attempt failed; preserve its outputs'
    folder=Path((OUT/'stdout.log').read_text(encoding='utf-8').splitlines()[0]).resolve()
    assert folder.parent==ROOT/'benchmarks/results'
    result=load(folder/'results.json');assert result['guards_unchanged'] and len(result['rows'])==3
    assert h4_quality.guards(plan['jobs'])==plan['guards']
    write(OUT/'completed.json',{'folder':folder.relative_to(ROOT).as_posix(),'results_sha256':digest(folder/'results.json'),'requires_profile_review':True,'gate_evidence':False})
    print(json.dumps({'profile_completed':str(folder),'gate_evidence':False}))
except BaseException:
    write(OUT/'interruption.json',{'error':traceback.format_exc()});raise
