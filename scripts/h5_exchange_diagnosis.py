"""Four diagnostic-only H5 searches to locate directed-exchange repair failures.

Use the rejected early-exchange implementation with per-invocation stage traces.
No proposal, repair, acceptance, work coefficient or budget changes. Tracing can
perturb wall time, so these single-seed records are not quality comparisons.
Run both mechanical jobs at both kerfs, seed zero, 60 seconds, serial CPU 8.
Wait for the H4 depth-three pilot to finish and be sealed; commit the plan first.
No held-out inputs, unchanged-pilot retry, integration or H5 completion claim.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import shutil
import subprocess
import time
import traceback
import zipfile

import psutil
import h5_early_exchange_pilot as prior

ROOT=prior.ROOT
PROBE=ROOT/'output/h5-exchange-diagnosis'
H4=ROOT/'benchmarks/results/h4-quadtree-depth-probe-20261016'
JOBS=['m-mechanical-large-plates','m-mechanical-panel-hardware']
load,write,digest=prior.load,prior.write,prior.digest


def guards():
    paths=[Path(__file__),ROOT/'scripts/h5_early_exchange_pilot.py',
           ROOT/'scripts/cutting_development_set.py',ROOT/'scripts/h6_material_cost.py',
           prior.CLI,PROBE/'preparation.json',PROBE/'build.json',PROBE/'exchange-diagnosis.exe']
    paths += [ROOT/r['path'] for r,_ in prior.load_cases()]
    env={k:os.environ.get(k) for k in prior.OVERRIDES}
    assert all(v is None for v in env.values())
    return {'production':prior.source_digest(),'diagnostic_source':prior.tree_hash(PROBE/'workspace'),
        'rejected_source':prior.tree_hash(Path(load(PROBE/'preparation.json')['old_source'])),
        'environment':env,'files':{p.relative_to(ROOT).as_posix():digest(p) for p in paths}}


def prepare(out):
    assert load(PROBE/'build.json')['all_passed']
    assert digest(PROBE/'exchange-diagnosis.exe')==load(PROBE/'build.json')['binary_sha256']
    out.mkdir()
    write(out/'plan.json',{'scope':__doc__,'jobs':JOBS,'kerfs_mm':[0.2,1.5],'seed':0,'seconds':60,
        'attempts':4,'cpu':8,'concurrency':1,'maximum_session_seconds':1800,'guards':guards(),
        'source_change':'Diagnostic counters and one trace line at each directed-exchange invocation exit only',
        'interpretation':'Identify observed failure stages. Tracing may perturb deadlines; no material/speed comparison or inference about all seeds.',
        'prerequisite':'H4 depth-three pilot terminal and every raw member verified',
        'retention':'Every outcome, trace, failed attempt, layout, validation and public export retained in immutable per-attempt ZIPs',
        'held_out_geometry_read':False,'H5_complete':False,'production_changed':False})
    shutil.copyfile(__file__,out/'runner.py')


def read_trace(archive,record):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=load_from_bytes(z.read('case.json'))
        for name,expected in case['artifacts'].items():
            assert prior.sha256(z.read(name)).hexdigest()==expected
        traces=[json.loads(line.removeprefix('EXCHANGE_DIAG '))
            for line in z.read('search-stderr.log').decode('utf-8').splitlines()
            if line.startswith('EXCHANGE_DIAG ')]
    attempts=[a for t in traces for a in t['attempts']]
    counts=Counter(a['outcome'] for a in attempts)
    assert not counts['unfinished']
    if record['status']=='valid':
        assert len(attempts)==record['stats']['directed_exchange_attempts']
        assert counts['accepted']==record['stats']['directed_exchanges']
    return {'invocations':len(traces),'attempts':len(attempts),'outcomes':dict(counts),
        'receivers':sum(t['receivers'] for t in traces),'proposals':sum(t['proposals'] for t in traces),
        'expired_before_attempt':sum(t['expired_before_attempt'] for t in traces),'traces':traces}


def load_from_bytes(raw):
    return json.loads(raw)


def run(out):
    plan=load(out/'plan.json');assert guards()==plan['guards']
    assert subprocess.check_output(['git','show','HEAD:'+(out/'plan.json').relative_to(ROOT).as_posix()],cwd=ROOT)==(out/'plan.json').read_bytes()
    old=load(H4/'opened.json')
    try:arguments=psutil.Process(old['pid']).cmdline()
    except psutil.NoSuchProcess:arguments=[]
    assert not any('h4_quadtree_depth_probe.py' in a for a in arguments)
    integrity=load(H4/'integrity.json')
    assert integrity['crc_and_every_member_verified'] and digest(H4/'raw.zip')==integrity['sha256']
    assert load(H4/'verification.json')['attempts']==99
    with (out/'opened.json').open('x',encoding='utf-8') as f:
        json.dump({'pid':os.getpid(),'utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':digest(out/'plan.json'),'h4_integrity_sha256':digest(H4/'integrity.json')},f,indent=2)
    work=PROBE/'measurements';work.mkdir()
    prior.ENGINES['candidate']=PROBE/'exchange-diagnosis.exe'
    known={r['id']:(r,j) for r,j in prior.load_cases()}
    records=[];started=time.perf_counter()
    try:
        for job_id in JOBS:
            for kerf in [0.2,1.5]:
                assert guards()==plan['guards']
                row,job=known[job_id];block={'job':job_id,'kerf_mm':kerf,'seed':0}
                record=prior.case(row,job,block,'candidate',8,work,out,started+1800)
                records.append(record);write(out/'records.json',records)
                try:record['diagnosis']=read_trace(out/record['archive'],record)
                except Exception:record['trace_error']=traceback.format_exc()
                write(out/'records.json',records)
                print(json.dumps({'job':job_id,'kerf':kerf,'status':record['status'],'outcomes':record.get('diagnosis',{}).get('outcomes'),'trace_error':record.get('trace_error')}),flush=True)
        assert guards()==plan['guards']
        write(out/'results.json',{'records':records,'guards_unchanged':True,'wall_seconds':time.perf_counter()-started,
            'all_valid':len(records)==4 and all(r['status']=='valid' and 'diagnosis' in r for r in records),
            'quality_claim':False,'H5_complete':False,'integrated':False})
    except BaseException:
        write(out/'interruption.json',{'error':traceback.format_exc(),'wall_seconds':time.perf_counter()-started});raise


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run']);p.add_argument('--out',required=True,type=Path)
    args=p.parse_args();out=args.out.resolve();assert out.parent==ROOT/'benchmarks/results'
    (prepare if args.action=='prepare' else run)(out)
