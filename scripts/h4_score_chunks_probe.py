"""One isolated eight-pair score-bound experiment, never an H4 completion claim.

First require eight valid, exact paired fixed-work native replays (letters and
gear-1, seeds 0/1, 20 work seconds, 120-second hard limit). Then measure the
unchanged H4 eleven-job subset once: native/Chrome/Firefox, seeds 0-2, 60 seconds.
Keep all original failures. No held-out inputs or changed limits. The root
preview must finish its original matrix before any new measured search starts.
Prepare and commit the full plan before running; an opened marker forbids retry.
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
PROBE=ROOT/'output/h4-score-granularity-probe'
WORK=PROBE/'workspace'
CANDIDATE=PROBE/'nestbolt-score-chunks8.exe'
ORIGINAL=ROOT/'benchmarks/results/h4-preview-development-20261016'
REPLAY_IDS=['example-letters','m-public-gear-1']
load=lambda p:json.loads(p.read_bytes())
write=quality.write


def guards(rows):
    value=quality.guards(rows)
    value['environment']={k:os.environ.get(k) for k in OVERRIDES}
    assert all(v is None for v in value['environment'].values())
    paths=[Path(__file__),CANDIDATE,PROBE/'build-v3.json',PROBE/'plan.json',
           PROBE/'formatted-v3-plan.json',PROBE/'bounded-tests-v2.json']
    paths += [WORK/r['path'] for r in load(PROBE/'plan.json')['baseline_files']]
    paths += [p for p in sorted((WORK/'web/dist').rglob('*')) if p.is_file()]
    for p in paths:
        value['files'][p.relative_to(ROOT).as_posix()]=quality.digest(p)
    return value


def prepare(out):
    assert load(PROBE/'build-v3.json')['all_passed']
    rows=quality.cases()
    out.mkdir()
    write(out/'plan.json',{'scope':__doc__,'baseline_product':'0a9fb440560bf96f5a81bd05e3f50d7df01238b3',
        'cases':rows,'guards':guards(rows),'cpus':quality.CPUS,'seeds':[0,1,2],'seconds':60,
        'concurrency':8,'replay':{'ids':REPLAY_IDS,'seeds':[0,1],'seconds':20,'time_limit':120,
            'cpus':[8,10],'arm_order':'baseline, then candidate for each pair on the same core',
            'speed_claim':False},
        'gates':{'median_difference_percent':1,'every_job_difference_percent':5,'every_layout_valid':True},
        'maximum_session_seconds':3600,'full_G5_native65_scale_separate':True,'H4_complete':False,
        'held_out_geometry_read':False,'source_change':'Eight-pair score-bound granularity only, plus explicit test coverage'})
    shutil.copyfile(__file__,out/'runner.py')
    print(out,flush=True)


def replay_one(row,seed,out,cpu):
    record={'job':row['id'],'seed':seed,'cpu':cpu,'passed':False,'arms':{}}
    try:
        for arm,binary in [('baseline',quality.CLI),('candidate',CANDIDATE)]:
            folder=out/'replay'/arm/f's{seed}'/row['id']
            folder.mkdir(parents=True)
            execution=run([binary,'sheets','--job',ROOT/row['path'],'--output',folder/'layout.json',
                '--seconds',20,'--seed',seed,'--repeatable','--time-limit',120],folder,'search',cpu,150)
            record['arms'][arm]={'execution':execution,'directory':folder.relative_to(ROOT).as_posix()}
            assert execution['exit_code']==0
            result=load(folder/'search-stdout.json')
            assert result['repeatable'],'Hard deadline reached: not a complete equal-work outcome'
            record['arms'][arm]['validation']=quality.check(row,folder,cpu,result)
        first=ROOT/record['arms']['baseline']['directory']
        second=ROOT/record['arms']['candidate']['directory']
        assert load(first/'layout.json')==load(second/'layout.json')
        before,after=(load(p/'search-stdout.json') for p in [first,second])
        # Whole results agree, apart from actual elapsed wall time.
        before.pop('elapsed_seconds');after.pop('elapsed_seconds')
        assert before==after,'Fixed-work search result differs'
        record['identical_result_except_wall_time']=True
        record['wall_difference_percent']=100*(record['arms']['candidate']['execution']['elapsed_wall_seconds']/
            record['arms']['baseline']['execution']['elapsed_wall_seconds']-1)
        record['passed']=True
    except Exception:
        record['error']=traceback.format_exc()
    return record


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
        replay_rows=[r for r in rows if r['id'] in REPLAY_IDS]
        assert len(replay_rows)==2
        replays=[]
        def lane(index,row):
            return [replay_one(row,seed,out,8+2*index) for seed in [0,1]]
        with ThreadPoolExecutor(2) as pool:
            futures=[pool.submit(lane,i,row) for i,row in enumerate(replay_rows)]
            for future in as_completed(futures):
                replays.extend(future.result())
        write(out/'replay-results.json',{'records':replays,'all_passed':all(r['passed'] for r in replays),
            'performance_claim':False,'median_wall_difference_percent':statistics.median(r['wall_difference_percent'] for r in replays) if all(r['passed'] for r in replays) else None})
        assert len(replays)==4 and all(r['passed'] for r in replays)
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
