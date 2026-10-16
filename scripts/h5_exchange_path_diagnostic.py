"""Two diagnostic path observations after the original H5 pilot, not quality repeats.

Use the unchanged candidate with its existing NESTBOLT_DEBUG timers, once for
each originally failing mechanical job at kerf 0.2, seed 0 and 60 seconds.
This changes logging only and cannot supply quality or speed claims. Every
output is preserved and independently validated. Prepare/commit before running.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import traceback
import zipfile

import psutil
import h5_exchange_pilot_v2 as pilot

ROOT=pilot.ROOT
PILOT=ROOT/'benchmarks/results/h5-exchange-pilot-v2-20261016'
JOBS=pilot.JOBS[:2]
load,write,digest=pilot.load,pilot.write,pilot.digest


def guards():
    return {'pilot':pilot.guards(),'runner':digest(Path(__file__)),
        'inputs':{name:digest(PILOT/(name+'-k0.2-s0-candidate.zip')) for name in JOBS}}


def prepare(out):
    out.mkdir()
    write(out/'plan.json',{'scope':__doc__,'jobs':JOBS,'kerf_mm':0.2,'seed':0,'seconds':60,
        'cpus':[8,10],'concurrency':2,'child_environment':{'NESTBOLT_DEBUG':'1'},
        'guards':guards(),'quality_gate_evidence':False,'speed_claim':False,
        'held_out_geometry_read':False,'requires_completed_original_pilot':True})
    shutil.copyfile(__file__,out/'runner.py')
    print(out,flush=True)


def case(name,cpu,out):
    folder=out/name;folder.mkdir()
    record={'job':name,'cpu':cpu,'status':'failed'}
    try:
        with zipfile.ZipFile(PILOT/(name+'-k0.2-s0-candidate.zip')) as z:
            for member in ['library.json','request.json']:(folder/member).write_bytes(z.read(member))
        command=list(map(str,[pilot.ENGINES['candidate'],folder/'library.json',folder/'request.json',folder/'nested',60,0,'wall']))
        env={**os.environ,'NESTBOLT_DEBUG':'1'}
        started=time.perf_counter()
        with (folder/'stdout.log').open('xb') as stdout,(folder/'stderr.log').open('xb') as stderr:
            process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=stdout,stderr=stderr,
                creationflags=subprocess.CREATE_NO_WINDOW | 4)
            child=psutil.Process(process.pid);child.cpu_affinity([cpu]);child.resume()
            try:code=process.wait(timeout=150)
            except subprocess.TimeoutExpired:
                process.kill();process.wait();code='timeout'
        record['execution']={'command':command,'exit_code':code,'wall_seconds':time.perf_counter()-started,'debug_override':True}
        assert code==0
        search=load(folder/'nested/search.json')
        params=['--library',folder/'library.json','--request',folder/'request.json','--layout',folder/'nested/layout.json']
        record['validation']=pilot.run([pilot.CLI,'validate',*params],folder,'validate',cpu,180)
        checked=load(folder/'validate-stdout.json')
        assert record['validation']['exit_code']==0 and checked['valid'] and search['validation']['valid']
        delta=pilot.equivalent(checked['metrics'],search['validation']['metrics'])
        lines=(folder/'stderr.log').read_text(encoding='utf-8',errors='replace').splitlines()
        timer_lines=[line.removeprefix('debug timers ') for line in lines if line.startswith('debug timers ')]
        timers=[json.loads(line) for line in timer_lines]
        record.update(status='valid',timers=timers,timers_observed=bool(timers),
            exchange_timed_call_observed=any('exchange' in t for t in timers),
            stats=search['stats'],history=search['history'],maximum_metric_difference=delta,
            quality_gate_evidence=False,speed_claim=False)
    except Exception:record['error']=traceback.format_exc()
    write(folder/'case.json',record)
    return record


def measure(out):
    plan=load(out/'plan.json')
    assert guards()==plan['guards']
    assert subprocess.check_output(['git','show','HEAD:'+(out/'plan.json').relative_to(ROOT).as_posix()],cwd=ROOT)==(out/'plan.json').read_bytes()
    assert load(PILOT/'results.json')['guards_unchanged']
    prior=load(PILOT/'opened.json')
    assert not psutil.pid_exists(prior['pid']) or not any('h5_exchange_pilot_v2.py' in p for p in psutil.Process(prior['pid']).cmdline())
    with (out/'opened.json').open('x',encoding='utf-8') as stream:
        json.dump({'pid':os.getpid(),'utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':digest(out/'plan.json')},stream,indent=2)
    with ThreadPoolExecutor(2) as pool:
        records=list(pool.map(lambda pair:case(pair[0],pair[1],out),zip(JOBS,[8,10])))
    assert guards()==plan['guards']
    write(out/'results.json',{'records':records,'guards_unchanged':True,'quality_gate_evidence':False,'speed_claim':False})
    print(json.dumps([{'job':r['job'],'status':r['status'],'exchange_call':r.get('exchange_timed_call_observed'),'timers':r.get('timers')} for r in records]),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run']);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();out=args.out.resolve()
    assert out.parent==ROOT/'benchmarks/results'
    (prepare if args.action=='prepare' else measure)(out)
