"""Observe proposal filtering and repair stages in the rejected complete-set candidate.

Four diagnostic-only searches: both mechanical development jobs, both kerfs,
seed 0, 60 seconds, serial physical CCD0 CPU 8. Instrumentation preserves the
original algorithm and limits but can perturb wall deadlines. No quality or
speed comparison, no changed candidate integration, and no held-out inputs.
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
import h5_complete_set_pilot as prior

ROOT = prior.ROOT
PROBE = ROOT/'output/h5-complete-stage-diagnosis-20261017'
OLD = ROOT/'benchmarks/results/h5-complete-set-pilot-20261017'
JOBS = ['m-mechanical-large-plates', 'm-mechanical-panel-hardware']
load, write, digest = prior.load, prior.write, prior.digest


def guards():
    paths = [Path(__file__), ROOT/'scripts/h5_complete_set_pilot.py',
        ROOT/'scripts/cutting_development_set.py', ROOT/'scripts/h6_material_cost.py',
        ROOT/'scripts/h4_full_matrix.py', prior.CLI, PROBE/'preparation.json',
        PROBE/'build.json', PROBE/'exchange-diagnosis.exe', OLD/'verification.json',
        ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json']
    paths += [ROOT/r['path'] for r, _ in prior.load_cases()]
    environment = {k:os.environ.get(k) for k in prior.OVERRIDES}
    assert all(v is None for v in environment.values())
    return {'production':prior.source_digest(),
        'diagnostic_source':prior.tree_hash(PROBE/'workspace'),
        'rejected_source':prior.tree_hash(Path(load(PROBE/'preparation.json')['old_source'])),
        'environment':environment, 'files':{p.relative_to(ROOT).as_posix():digest(p) for p in paths}}


def prepare(out):
    assert load(PROBE/'build.json')['all_passed']
    assert digest(PROBE/'exchange-diagnosis.exe') == load(PROBE/'build.json')['binary_sha256']
    assert load(OLD/'verification.json')['valid'] == 72
    assert load(ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json')['H4_complete']
    out.mkdir(exist_ok=False)
    write(out/'plan.json', {'scope':__doc__, 'jobs':JOBS, 'kerfs_mm':[0.2,1.5],
        'seed':0, 'seconds':60, 'attempts':4, 'cpu':8, 'concurrency':1,
        'maximum_session_seconds':1200, 'guards':guards(),
        'source_change':'Aggregate sampling eligibility, eligible full sets by returned-area relation, retained proposal counts and repair-stage outcomes; one stderr trace per exchange invocation.',
        'interpretation':'Diagnostic only; trace overhead can alter wall-clock outcomes. No quality comparison, no retry of the rejected paired pilot.',
        'retention':'All original attempts, traces, public exports and independent validation in immutable per-attempt ZIPs.',
        'held_out_geometry_read':False, 'production_changed':False, 'H5_complete':False})
    shutil.copyfile(__file__,out/'runner.py')


def read_trace(archive, record):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case = json.loads(z.read('case.json'))
        for name, expected in case['artifacts'].items():
            assert prior.sha256(z.read(name)).hexdigest() == expected
        traces = [json.loads(line.removeprefix('OBSTRUCTION_DIAG '))
            for line in z.read('search-stderr.log').decode('utf-8').splitlines()
            if line.startswith('OBSTRUCTION_DIAG ')]
    assert traces, 'Expected at least one recorded invocation'
    attempts = [a for t in traces for a in t['attempts']]
    samplings = [s for t in traces for s in t['samplings']]
    counts = Counter(a['outcome'] for a in attempts)
    assert not counts['unfinished']
    for attempt in attempts:
        assert 1 <= attempt['victims'] <= attempt['blockers'] <= 3
        assert attempt['returned_area'] > 0 and attempt['incoming_area'] > 0
        if attempt['victims'] == 1:
            assert attempt['returned_area'] < attempt['incoming_area']
    for sample in samplings:
        assert sample['examined'] <= sample['samples']
        assert len(sample['retained_victim_counts']) == len(sample['retained_blocker_counts']) <= 6
        assert sample['smallest_not_smaller_area_ratio'] is None or sample['smallest_not_smaller_area_ratio'] >= 1
    if record['status'] == 'valid':
        # These counters explicitly omit serialized zero values in the solver.
        assert len(attempts) == record['stats'].get('directed_exchange_attempts',0)
        assert counts['accepted'] == record['stats'].get('directed_exchanges',0)
    fields = ['samples','examined','collision_free','over_three_collisions','non_item_collision',
        'multi_eligible_smaller','multi_eligible_not_smaller']
    by_kind = {}
    for kind, selected in [('complete',[a for a in attempts if a['victims']==a['blockers']]),
                           ('partial',[a for a in attempts if a['victims']<a['blockers']])]:
        by_kind[kind] = dict(Counter(a['outcome'] for a in selected))
    return {'invocations':len(traces), 'attempts':len(attempts), 'outcomes':dict(counts),
        'complete_vs_partial':by_kind, 'sampling_totals':{k:sum(s[k] for s in samplings) for k in fields},
        'proposals':sum(t['proposals'] for t in traces), 'traces':traces}


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
            'all_valid':len(records)==4 and all(r['status']=='valid' and 'diagnosis' in r for r in records),
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
    (prepare if args.action=='prepare' else run)(out)
