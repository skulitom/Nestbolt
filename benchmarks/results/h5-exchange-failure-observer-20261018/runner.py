"""Diagnose existing exchange failure branches without changing their conditions.

Two diagnostic-only searches: panel hardware, both kerfs, seed 0, 60 seconds,
serial physical CCD0 CPU 8. The original search decisions, budgets and work
charges remain. Logging overhead can change wall trajectories. No quality
or speed comparison, integration or held-out geometry access.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import math
import struct
import os
import shutil
import subprocess
import time
import traceback
import zipfile

import psutil
import h5_boundary_pair_pilot as prior

ROOT = prior.ROOT
PROBE = ROOT/'output/h5-exchange-failure-observer-20261018'
OLD = ROOT/'benchmarks/results/h5-boundary-pair-pilot-20261018'
JOBS = ['m-mechanical-panel-hardware']
load, write, digest = prior.load, prior.write, prior.digest


def guards():
    paths = [Path(__file__), ROOT/'scripts/h5_boundary_pair_pilot.py', ROOT/'scripts/h5_frontier_observer.py', ROOT/'scripts/h5_boundary_pair_observer.py',
        ROOT/'scripts/cutting_development_set.py', ROOT/'scripts/h6_material_cost.py',
        ROOT/'scripts/h4_full_matrix.py', prior.CLI, PROBE/'preparation.json',
        PROBE/'build.json', PROBE/'exchange-diagnosis.exe', OLD/'verification.json',
        ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json',
        PROBE/'reconstruction.json', PROBE/'authored-trace-reader/checks.json',
        ROOT/'benchmarks/results/h5-exchange-failure-observer-preparation-20261018/checks.json']
    paths += [ROOT/r['path'] for r, _ in prior.load_cases()]
    environment = {k:os.environ.get(k) for k in prior.OVERRIDES}
    assert all(v is None for v in environment.values())
    return {'production':prior.source_digest(),
        'diagnostic_source':prior.tree_hash(PROBE/'workspace'),
        'rejected_source':prior.tree_hash(Path(load(PROBE/'preparation.json')['old_source'])),
        'environment':environment, 'files':{p.relative_to(ROOT).as_posix():digest(p) for p in paths}}


def prepare(out):
    assert load(PROBE/'build.json')['all_passed']
    assert load(PROBE/'authored-trace-reader/checks.json')['all_checks_pass']
    assert load(ROOT/'benchmarks/results/h5-exchange-failure-observer-preparation-20261018/checks.json')['all_qualified']
    assert digest(PROBE/'exchange-diagnosis.exe') == load(PROBE/'build.json')['binary_sha256']
    assert load(OLD/'verification.json')['valid'] == 72
    assert load(ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json')['H4_complete']
    out.mkdir(exist_ok=False)
    write(out/'plan.json', {'scope':__doc__, 'jobs':JOBS, 'kerfs_mm':[0.2,1.5],
        'seed':0, 'seconds':60, 'attempts':2, 'cpu':8, 'concurrency':1,
        'maximum_session_seconds':1200, 'guards':guards(),
        'source_change':'Add failure details only after the original short-circuit branches reject: exact loss and source poses, or validated trial layout and material. The original conditions, clock reads, work charges and 130 tests remain. Recomputed return poses are pure and are observed only after failure.',
        'interpretation':'Diagnostic only; trace overhead can alter wall-clock outcomes. No quality comparison, no retry of the rejected paired pilot.',
        'retention':'All original attempts, traces, public exports and independent validation in immutable per-attempt ZIPs.',
        'held_out_geometry_read':False, 'production_changed':False, 'H5_complete':False})
    shutil.copyfile(__file__,out/'runner.py')


def pose_key(value):
    assert set(value)=={'part_id','transform'} and type(value['part_id']) is str
    transform=value['transform']
    assert set(transform)=={'translation','rotation_radians','mirrored'}
    assert type(transform['mirrored']) is bool
    assert isinstance(transform['translation'],list) and len(transform['translation'])==2
    numbers=[*transform['translation'],transform['rotation_radians']]
    assert all(type(x) in [int,float] and math.isfinite(x) for x in numbers)
    return (value['part_id'],*numbers,transform['mirrored'])


def check_traces(traces, stats=None):
    import copy
    import h5_boundary_pair_observer as parent
    stripped=copy.deepcopy(traces)
    details=[]
    for invocation,(trace,clean) in enumerate(zip(traces,stripped)):
        base=trace['baseline']
        source=Counter(p['part_id'] for p in base['layout']['placements'] if p['sheet_id']==base['source_sheet'])
        job_inventory=Counter({p['id']:p['quantity'] for p in base['job']['parts']})
        def finite_nonnegative(value):
            assert type(value) in [int,float] and math.isfinite(value) and value>=0
        def poses(values):
            assert isinstance(values,list)
            for p in values:pose_key(p)
            return Counter(p['part_id'] for p in values)
        for index,(attempt,without) in enumerate(zip(trace['attempts'],clean['attempts'])):
            assert 'failure_detail' in attempt
            detail=without.pop('failure_detail');outcome=attempt['outcome'];reason=None
            if outcome=='receiver_repair_failed':
                assert isinstance(detail,dict) and set(detail)=={'receiver_loss'}
                finite_nonnegative(detail['receiver_loss']);assert detail['receiver_loss']>0
                reason='receiver_loss_positive'
            elif outcome=='source_repair_or_expiry':
                assert isinstance(detail,dict) and set(detail)=={'source_loss','source_after','returned_initial'}
                finite_nonnegative(detail['source_loss'])
                assert poses(detail['returned_initial'])==Counter(attempt['returned'])
                expected=source.copy();expected.subtract(trace['choices'][attempt['choice_index']]);expected.update(attempt['returned'])
                assert all(v>=0 for v in expected.values())
                assert poses(detail['source_after'])==+expected
                reason='source_loss_positive' if detail['source_loss']>0 else 'source_deadline'
            elif outcome=='material_guard_or_expiry':
                assert isinstance(detail,dict) and set(detail)=={'material_increased','metrics','layout'}
                after=detail['metrics'];old=base['metrics']
                finite_nonnegative(after['material_area'])
                assert type(after['sheets_used']) is int and after['sheets_used']>0
                assert type(detail['material_increased']) is bool
                increased=after['sheets_used']>old['sheets_used'] or after['material_area']>old['material_area']
                assert detail['material_increased']==increased
                layout=detail['layout'];assert set(layout)==set(base['layout'])
                assert Counter(p['part_id'] for p in layout['placements'])==job_inventory
                known_sheets={p['sheet_id'] for p in base['layout']['placements']}
                for p in layout['placements']:
                    assert p['sheet_id'] in known_sheets
                    pose_key({'part_id':p['part_id'],'transform':p['transform']})
                reason='material_increased' if increased else 'exchange_deadline'
            else:
                assert detail is None
            if reason:
                details.append({'invocation':invocation,'attempt_index':index,'choice_index':attempt['choice_index'],
                    'target_sheet':attempt['target_sheet'],'outcome':outcome,'reason':reason,'detail':detail})
    result=parent.check_traces(stripped,stats)
    result['traces']=traces
    result['failure_details']=details
    result['failure_reason_counts']=dict(Counter(d['reason'] for d in details))
    result['failure_details_verified']=True
    return result


def parse_log(log):
    return [json.loads(line.removeprefix('FRONTIER_DIAG ')) for line in log.splitlines() if line.startswith('FRONTIER_DIAG ')]


def read_trace(archive, record):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        for name,expected in case['artifacts'].items():assert prior.sha256(z.read(name)).hexdigest()==expected
        traces=parse_log(z.read('search-stderr.log').decode('utf-8'))
    assert traces,'No baseline observation from the two-sheet diagnostic'
    return check_traces(traces,record.get('stats') if record['status']=='valid' else None)


def run(out):
    plan = load(out/'plan.json')
    assert guards() == plan['guards']
    assert subprocess.check_output(['git','show','HEAD:'+(out/'plan.json').relative_to(ROOT).as_posix()],cwd=ROOT) == (out/'plan.json').read_bytes(), 'Commit plan before running'
    for proc in psutil.process_iter(['pid','name','cmdline']):
        if proc.info['pid'] == os.getpid():
            continue
        name = (proc.info['name'] or '').lower()
        assert name not in ['exchange-diagnosis.exe','candidate-observer.exe','baseline-observer.exe'], 'Another measured observer is running'
    with (out/'opened.json').open('x',encoding='utf-8',newline='\n') as f:
        json.dump({'pid':os.getpid(),'utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':digest(out/'plan.json')},f,indent=2)
    work=PROBE/'measurements';work.mkdir(exist_ok=False)
    prior.ENGINES['candidate']=PROBE/'exchange-diagnosis.exe'
    known={r['id']:(r,j) for r,j in prior.load_cases()}
    records=[];started=time.perf_counter()
    try:
        for job_id in JOBS:
            for kerf in [0.2,1.5]:
                assert guards() == plan['guards']
                row,job=known[job_id]
                record=prior.case(row,job,{'job':job_id,'kerf_mm':kerf,'seed':0},'candidate',8,work,out,started+1200)
                records.append(record);write(out/'records.json',records)
                try:
                    record['diagnosis']=read_trace(out/record['archive'],record)
                except Exception:
                    record['trace_error']=traceback.format_exc()
                write(out/'records.json',records)
                print(json.dumps({'job':job_id,'kerf':kerf,'status':record['status'],
                    'outcomes':record.get('diagnosis',{}).get('outcomes'),'trace_error':record.get('trace_error')}),flush=True)
        assert guards() == plan['guards']
        write(out/'results.json',{'records':records,'guards_unchanged':True,'wall_seconds':time.perf_counter()-started,
            'all_valid':len(records)==2 and all(r['status']=='valid' and 'diagnosis' in r for r in records),
            'quality_claim':False,'H5_complete':False,'integrated':False})
    except BaseException:
        write(out/'interruption.json',{'error':traceback.format_exc(),'wall_seconds':time.perf_counter()-started})
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','run'])
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args();out=args.out.resolve()
    assert out.parent == ROOT/'benchmarks/results'
    psutil.Process().cpu_affinity(list(range(16,32)))
    (prepare if args.action=='prepare' else run)(out)
