"""Observe whether exchange choices reach the parts setting charged sheet height.

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
import h5_material_profile_pilot as prior

ROOT = prior.ROOT
PROBE = ROOT/'output/h5-frontier-observer-20261018'
OLD = ROOT/'benchmarks/results/h5-material-profile-pilot-20261018'
JOBS = ['m-mechanical-panel-hardware']
load, write, digest = prior.load, prior.write, prior.digest


def guards():
    paths = [Path(__file__), ROOT/'scripts/h5_material_profile_pilot.py',
        ROOT/'scripts/cutting_development_set.py', ROOT/'scripts/h6_material_cost.py',
        ROOT/'scripts/h4_full_matrix.py', prior.CLI, PROBE/'preparation.json',
        PROBE/'build.json', PROBE/'exchange-diagnosis.exe', OLD/'verification.json',
        ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json',
        PROBE/'reconstruction.json', PROBE/'authored-trace-reader/checks.json',
        ROOT/'benchmarks/results/h5-frontier-observer-preparation-20261018/checks.json']
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
    assert load(ROOT/'benchmarks/results/h5-frontier-observer-preparation-20261018/checks.json')['all_qualified']
    assert digest(PROBE/'exchange-diagnosis.exe') == load(PROBE/'build.json')['binary_sha256']
    assert load(OLD/'verification.json')['valid'] == 72
    assert load(ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json')['H4_complete']
    out.mkdir(exist_ok=False)
    write(out/'plan.json', {'scope':__doc__, 'jobs':JOBS, 'kerfs_mm':[0.2,1.5],
        'seed':0, 'seconds':60, 'attempts':2, 'cpu':8, 'concurrency':1,
        'maximum_session_seconds':1200, 'guards':guards(),
        'source_change':'Record the validated public baseline/job, credited and source sheet, original part names for every choice, visited choices and actual attempted members with terminal outcome. All inserted observations reverse exactly; no decision or work charge changes.',
        'interpretation':'Diagnostic only; trace overhead can alter wall-clock outcomes. No quality comparison, no retry of the rejected paired pilot.',
        'retention':'All original attempts, traces, public exports and independent validation in immutable per-attempt ZIPs.',
        'held_out_geometry_read':False, 'production_changed':False, 'H5_complete':False})
    shutil.copyfile(__file__,out/'runner.py')


def check_traces(traces, stats=None):
    assert isinstance(traces,list)
    rows=[];visits=[];outcomes=Counter()
    allowed={'forbidden_incoming_orientation','receiver_repair_failed','source_repair_or_expiry',
        'exact_state_rejected','material_profile_rejected','independent_geometry_failed',
        'material_guard_or_expiry','neutral_inventory_rejected','accepted'}
    for trace in traces:
        assert set(trace)=={'baseline','choices','visits','attempts'}
        base=trace['baseline'];assert set(base)=={'job','layout','metrics','source_sheet'}
        job,layout,metrics=base['job'],base['layout'],base['metrics']
        assert isinstance(job,dict) and isinstance(layout,dict) and isinstance(metrics,dict)
        assert type(metrics['material_area']) in [int,float] and math.isfinite(metrics['material_area']) and metrics['material_area']>0
        names={p['id'] for p in job['parts']};assert len(names)==len(job['parts'])
        sheets={s['id'] for s in layout['sheets']};assert len(sheets)==len(layout['sheets'])
        assert base['source_sheet'] in sheets and metrics['last_sheet_id'] in sheets
        assert len({(p['part_id'],p['copy_index']) for p in layout['placements']})==len(layout['placements'])
        assert all(p['part_id'] in names and p['sheet_id'] in sheets for p in layout['placements'])
        inventory=Counter(p['part_id'] for p in layout['placements'] if p['sheet_id']==base['source_sheet'])
        assert inventory
        choices=trace['choices'];assert isinstance(choices,list) and choices
        single=Counter()
        for choice in choices:
            assert isinstance(choice,list) and 1<=len(choice)<=2
            assert all(type(name) is str and name in names for name in choice)
            assert not Counter(choice)-inventory
            if len(choice)==1:single.update(choice)
        assert single==inventory
        assert sum(len(c)==2 for c in choices)<=12
        seen={};last_index=-1
        for visit in trace['visits']:
            assert set(visit)=={'choice_index','target_sheet','retained_proposals'}
            i=visit['choice_index'];target=visit['target_sheet'];retained=visit['retained_proposals']
            assert type(i) is int and 0<=i<len(choices) and i>=last_index
            assert target in sheets and target!=base['source_sheet']
            assert type(retained) is int and 0<=retained<=6
            key=(i,target);assert key not in seen;seen[key]=(len(seen),retained);last_index=i
            visits.append(dict(visit,incoming=choices[i]))
        counts=Counter();last_visit=-1;accepted=0
        for index,attempt in enumerate(trace['attempts']):
            assert set(attempt)=={'choice_index','target_sheet','returned','outcome'}
            i=attempt['choice_index'];assert type(i) is int and 0<=i<len(choices)
            key=(i,attempt['target_sheet']);assert key in seen
            ordinal,retained=seen[key];assert ordinal>=last_visit;last_visit=ordinal
            counts[key]+=1;assert counts[key]<=retained
            returned=attempt['returned'];assert isinstance(returned,list) and 1<=len(returned)<=3
            target_inventory=Counter(p['part_id'] for p in layout['placements'] if p['sheet_id']==key[1])
            assert all(type(name) is str and name in names for name in returned)
            assert not Counter(returned)-target_inventory
            outcome=attempt['outcome'];assert outcome in allowed
            if outcome in ['exact_state_rejected','material_profile_rejected','neutral_inventory_rejected']:
                assert Counter(choices[i])==Counter(returned)
            if outcome=='accepted':
                accepted+=1;assert accepted<=1 and index==len(trace['attempts'])-1
            outcomes[outcome]+=1
            rows.append(dict(attempt,incoming=choices[i]))
    paired=[r for r in rows if len(r['incoming'])==2]
    mixed=[r for r in paired if len(set(r['incoming']))==2]
    counters={'directed_exchange_attempts':len(rows),'directed_exchanges':outcomes['accepted'],
        'paired_exchange_attempts':len(paired),'paired_exchanges':sum(r['outcome']=='accepted' for r in paired),
        'mixed_exchange_attempts':len(mixed),'mixed_exchanges':sum(r['outcome']=='accepted' for r in mixed),
        'neutral_exchange_rejections':sum(outcomes[k] for k in ['exact_state_rejected','material_profile_rejected','neutral_inventory_rejected']),
        'exact_state_exchange_rejections':outcomes['exact_state_rejected'],
        'material_profile_exchange_rejections':outcomes['material_profile_rejected']}
    if stats is not None:
        for key,value in counters.items():assert type(stats.get(key,0)) is int and stats.get(key,0)==value,(key,stats.get(key),value)
    return {'invocations':len(traces),'attempts':len(rows),'outcomes':dict(outcomes),
        'paired_attempts':len(paired),'mixed_attempts':len(mixed),'counters':counters,
        'attempt_rows':rows,'visit_rows':visits,'traces':traces}


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
