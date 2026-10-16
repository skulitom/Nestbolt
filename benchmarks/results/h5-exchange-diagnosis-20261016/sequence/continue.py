"""Finish the one active H4 pilot, then run the already-committed H5 diagnosis."""
from pathlib import Path
from datetime import datetime, timezone
import json, os, subprocess, sys, time, traceback
import psutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/depth-diagnosis-sequence-20261016'
H4=ROOT/'benchmarks/results/h4-quadtree-depth-probe-20261016'
H5=ROOT/'benchmarks/results/h5-exchange-diagnosis-20261016'
def load(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
OUT.mkdir();opened=datetime.now(timezone.utc).isoformat();stages=[]
write(OUT/'opened.json',{'utc':opened,'pid':os.getpid(),'h4':str(H4),'h5':str(H5)})
deadline=time.monotonic()+3600
try:
    pid=load(H4/'opened.json')['pid']
    while True:
        assert time.monotonic()<deadline,'Sequence wait exceeded one hour'
        try:args=psutil.Process(pid).cmdline()
        except psutil.NoSuchProcess:args=[]
        if not any('h4_quadtree_depth_probe.py' in a for a in args):break
        time.sleep(5)
    assert (H4/'results.json').exists() and not (H4/'interruption.json').exists()
    jobs=[('seal-h4',[sys.executable,'output/finish_h4_depth_pilot.py'],180),
          ('diagnose-h5',[sys.executable,'scripts/h5_exchange_diagnosis.py','run','--out',str(H5)],1800),
          ('seal-h5',[sys.executable,'output/finish_h5_exchange_diagnosis.py'],180)]
    for label,args,timeout in jobs:
        start=datetime.now(timezone.utc).isoformat()
        with (OUT/(label+'.log')).open('xb') as f:
            result=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
        row={'stage':label,'command':args,'started':start,'finished':datetime.now(timezone.utc).isoformat(),'exit_code':result.returncode}
        stages.append(row);write(OUT/'progress.json',stages);print(json.dumps(row),flush=True)
        assert result.returncode==0,'Preserve failure; do not restart sequence: '+label
    write(OUT/'completed.json',{'stages':stages,'utc':datetime.now(timezone.utc).isoformat(),'h4_passed_pilot':load(H4/'assessment.json')['passed_pilot'],'h5_all_valid':load(H5/'results.json')['all_valid']})
except BaseException:
    write(OUT/'interruption.json',{'error':traceback.format_exc(),'stages':stages});raise
