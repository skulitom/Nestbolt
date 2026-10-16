"""One isolated separator-window depth-three experiment, never H4 completion.

Current CPU profiles identify collision-tree traversal as the main sampled cost.
Test one shallower level; retain original geometry, leaf threshold, aspect-depth
adjustment, budgets, work coefficients, score arithmetic and public defaults.
The unchanged eleven-job subset runs once: native/Chrome/Firefox, seeds 0-2,
60 seconds on eight physical CCD0 cores. Original +1% median/+5% job limits.
No exact fixed-work identity claim: hazard traversal order can change.
Prepare and commit before running. The opened marker forbids an unchanged retry.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from queue import Queue
import shutil
import statistics
import subprocess
import time
import traceback
from types import SimpleNamespace

import psutil

import h4_quality as quality
from h4_full_matrix import OVERRIDES
from g5_browser import serve
from h6_material_cost import run

ROOT=Path(__file__).resolve().parents[1]
PROBE=ROOT/'output/h4-quadtree-depth-probe'
WORK=PROBE/'workspace'
CANDIDATE=PROBE/'nestbolt-depth3.exe'
ORIGINAL=ROOT/'benchmarks/results/h4-preview-score-release-20261016'
PREP=ROOT/'benchmarks/results/h4-quadtree-depth-preparation-20261016'
H5=ROOT/'benchmarks/results/h5-early-exchange-pilot-20261016'
load=lambda p:json.loads(p.read_bytes())
write=quality.write


def guards(rows):
    value=quality.guards(rows)
    value['environment']={k:os.environ.get(k) for k in OVERRIDES}
    assert all(v is None for v in value['environment'].values())
    paths=[Path(__file__),CANDIDATE,PROBE/'build.json',PROBE/'preparation.json',PREP/'raw.zip',PREP/'integrity.json']
    paths += [WORK/r['path'] for r in load(PROBE/'preparation.json')['baseline_files']]
    paths += [ROOT/r['path'] for r in load(PROBE/'preparation.json')['baseline_files']]
    paths += [p for p in sorted((WORK/'web/dist').rglob('*')) if p.is_file()]
    for p in paths:
        value['files'][p.relative_to(ROOT).as_posix()]=quality.digest(p)
    return value


def prepare(out):
    assert load(PROBE/'build.json')['all_checks_passed']
    assert load(PREP/'integrity.json')['crc_and_every_member_verified']
    rows=quality.cases()
    out.mkdir()
    write(out/'plan.json',{'scope':__doc__,'baseline_product':'7eba929420d218d04169c1fdf24481051c8afae5',
        'cases':rows,'guards':guards(rows),'cpus':quality.CPUS,'seeds':[0,1,2],'seconds':60,
        'concurrency':8,'attempts':99,'fixed_work_identity_claim':False,
        'gates':{'median_difference_percent':1,'every_job_difference_percent':5,'every_layout_valid':True},
        'maximum_session_seconds':3600,'full_G5_native65_scale_separate':True,'H4_complete':False,
        'held_out_geometry_read':False,'source_change':'Separator-window base quadtree depth 4 to 3 only',
        'prerequisites':'Original complete matrix and H5 early-exchange pilot terminal and sealed',
        'failure_policy':'Retain every failed/incomplete attempt; no unchanged retry or seed substitution',
        'temperature_limitation':'No available reliable temperature sensor; CPU frequency is not temperature'})
    shutil.copyfile(__file__,out/'runner.py')
    print(out,flush=True)


def native(row,seed,out,cpus):
    cpu=cpus.get()
    folder=out/'native'/f's{seed}'/row['id'];folder.mkdir(parents=True)
    record={'job':row['id'],'seed':seed,'status':'failed','cpu':cpu,'directory':folder.relative_to(ROOT).as_posix()}
    try:
        record['run']=run([CANDIDATE,'sheets','--job',ROOT/row['path'],'--output',folder/'layout.json',
            '--seconds',60,'--seed',seed],folder,'search',cpu,150)
        assert record['run']['exit_code']==0
        record.update(quality.check(row,folder,cpu,load(folder/'search-stdout.json')))
    except Exception:
        record['error']=traceback.format_exc()
    finally:
        cpus.put(cpu)
    write(folder/'case.json',record)
    return record


def measure(out):
    original=load(ORIGINAL/'results.json')
    assert original['guards_unchanged']
    pid=load(ORIGINAL/'opened.json')['pid']
    assert not psutil.pid_exists(pid) or not any('h4_preview_matrix.py' in p for p in psutil.Process(pid).cmdline())
    assert load(ORIGINAL/'integrity.json')['crc_and_every_member_verified'], 'Seal the complete original first'
    assert load(H5/'verification.json')['all_original_archives_verified']
    assert load(H5/'assessment.json')['valid_attempts']==72
    h5pid=load(H5/'opened.json')['pid']
    assert not psutil.pid_exists(h5pid) or not any('h5_early_exchange_pilot.py' in p for p in psutil.Process(h5pid).cmdline())
    plan=load(out/'plan.json');rows=quality.cases()
    assert rows==plan['cases'] and guards(rows)==plan['guards']
    relative=(out/'plan.json').relative_to(ROOT).as_posix()
    assert subprocess.check_output(['git','show','HEAD:'+relative],cwd=ROOT)==(out/'plan.json').read_bytes()
    with (out/'opened.json').open('x',encoding='utf-8') as stream:
        json.dump({'utc':datetime.now(timezone.utc).isoformat(),'pid':psutil.Process().pid,
            'plan_sha256':quality.digest(out/'plan.json')},stream,indent=2)
    started=time.perf_counter()
    records={'native':[],'chrome':[],'firefox':[]}
    def preflight():
        assert time.perf_counter()-started<3600
        assert guards(rows)==plan['guards']
    def progress():
        write(out/'records.json',records)
        write(out/'progress.json',{k:{'done':len(v),'valid':sum(r['status']=='valid' for r in v)} for k,v in records.items()})
    try:
        preflight()
        cpus=Queue()
        for cpu in quality.CPUS:cpus.put(cpu)
        with ThreadPoolExecutor(8) as pool:
            futures=[pool.submit(native,row,seed,out,cpus) for seed in [0,1,2] for row in rows]
            for future in as_completed(futures):
                records['native'].append(future.result());progress()
        server=serve(WORK/'web/dist')
        try:
            args=SimpleNamespace(seconds=60,concurrency=8)
            url=f'http://127.0.0.1:{server.server_address[1]}/bench.html'
            for engine in ['chrome','firefox']:
                for seed in [0,1,2]:
                    preflight()
                    records[engine].extend(quality.browser(engine,seed,rows,args,out,url));progress()
                    print(engine,seed,len(records[engine]),flush=True)
        finally:
            server.shutdown()
        preflight()
        summary=quality.summarize(records,rows,[0,1,2],60)
        write(out/'results.json',{'records':records,'summary':summary,'guards_unchanged':True,
            'wall_seconds':time.perf_counter()-started,'H4_complete':False,'integrated':False})
        print(json.dumps(summary),flush=True)
    except BaseException:
        write(out/'interruption.json',{'error':traceback.format_exc(),'wall_seconds':time.perf_counter()-started})
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run'])
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    out=args.out.resolve()
    assert out.parent==ROOT/'benchmarks/results'
    (prepare if args.action=='prepare' else measure)(out)
