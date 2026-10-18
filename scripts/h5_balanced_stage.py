"""Observe retained proposal identities, repair stages and immediate effects of the rejected balanced-pair candidate.

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
import math
import os
import shutil
import subprocess
import time
import traceback
import zipfile

import psutil
import h5_balanced_group_pilot as prior

ROOT = prior.ROOT
PROBE = ROOT/'output/h5-balanced-stage-20261018'
OLD = ROOT/'benchmarks/results/h5-balanced-group-pilot-20261018'
JOBS = ['m-mechanical-large-plates', 'm-mechanical-panel-hardware']
load, write, digest = prior.load, prior.write, prior.digest


def guards():
    paths = [Path(__file__), ROOT/'scripts/h5_balanced_group_pilot.py',
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
        'source_change':'Read-only retained proposal item identities, receiver/source losses, immediate material and last-sheet extent, final rejection stage. One stderr trace per invocation.',
        'interpretation':'Diagnostic only; trace overhead can alter wall-clock outcomes. No quality comparison, no retry of the rejected paired pilot.',
        'retention':'All original attempts, traces, public exports and independent validation in immutable per-attempt ZIPs.',
        'held_out_geometry_read':False, 'production_changed':False, 'H5_complete':False})
    shutil.copyfile(__file__,out/'runner.py')


def neutral(proposal):
    return sorted(proposal['incoming_ids']) == sorted(proposal['returned_ids'])


def check_traces(traces, stats=None):
    assert isinstance(traces,list) and traces
    attempts=[];proposals=[]
    def positive(value):
        assert type(value) in [int,float] and math.isfinite(value) and value>0
    def loss(value):
        assert value is None or (type(value) in [int,float] and math.isfinite(value) and value>=0)
    outcomes={'accepted','receiver_repair_failed','source_repair_failed','expired_after_repairs',
              'independent_geometry_failed','material_guard_failed','expired_before_acceptance',
              'forbidden_incoming_orientation'}
    for t in traces:
        assert type(t['disabled_or_expired']) is bool and type(t['baseline_invalid']) is bool
        ps=t['proposals'];seen=set()
        if t['disabled_or_expired'] or t['baseline_invalid']:
            assert not ps and not t['attempts']
            assert t['before_material'] is None and t['before_last_extent'] is None
            continue
        positive(t['before_material']);positive(t['before_last_extent'])
        for p in ps:
            assert type(p['paired']) is bool and type(p['target']) is int and p['target']>=0
            for key in ['incoming_ids','returned_ids']:
                assert isinstance(p[key],list) and p[key] and all(type(i) is int and i>=0 for i in p[key])
            assert len(p['incoming_ids'])==(2 if p['paired'] else 1)
            assert 1<=len(p['returned_ids'])<=p['blockers']<=3 and type(p['blockers']) is int
            positive(p['incoming_area']);positive(p['returned_area'])
            if p['paired']:
                assert p['incoming_ids'][0]==p['incoming_ids'][1]
                assert len(p['returned_ids'])==p['blockers']
                assert p['returned_area']<=p['incoming_area']
            elif len(p['returned_ids'])==1:
                assert p['returned_area']<p['incoming_area']
        proposals.extend(ps)
        for a in t['attempts']:
            i=a['proposal_index']
            assert type(i) is int and 0<=i<len(ps) and i not in seen
            seen.add(i);p=ps[i]
            assert a['outcome'] in outcomes
            for key in ['receiver_initial_loss','receiver_loss','source_initial_loss','source_loss']:loss(a[key])
            for key in ['after_material','after_last_extent']:
                if a[key] is not None:positive(a[key])
            outcome=a['outcome']
            if outcome=='forbidden_incoming_orientation':
                assert p['paired'] and all(a[k] is None for k in ['receiver_initial_loss','receiver_loss','source_initial_loss','source_loss','after_material','after_last_extent'])
            elif outcome=='receiver_repair_failed':
                assert a['receiver_initial_loss'] is not None and a['receiver_loss']>0
                assert all(a[k] is None for k in ['source_initial_loss','source_loss','after_material','after_last_extent'])
            else:
                assert a['receiver_initial_loss'] is not None and a['receiver_loss']==0
                assert a['source_initial_loss'] is not None and a['source_loss'] is not None
                if outcome=='source_repair_failed':assert a['source_loss']>0
                else:assert a['source_loss']==0
                if outcome in ['source_repair_failed','expired_after_repairs']:
                    assert a['after_material'] is None and a['after_last_extent'] is None
                elif outcome=='independent_geometry_failed':
                    assert a['after_material'] is None and a['after_last_extent'] is not None
                else:
                    assert a['after_material'] is not None and a['after_last_extent'] is not None
                if outcome=='accepted':assert a['after_material']<=t['before_material']
            attempts.append({**a,'proposal':p,'neutral_inventory':neutral(p),
                'before_material':t['before_material'],'before_last_extent':t['before_last_extent']})
    counts=Counter(a['outcome'] for a in attempts)
    paired=[a for a in attempts if a['proposal']['paired']]
    if stats is not None:
        assert len(attempts)==stats.get('directed_exchange_attempts',0)
        assert counts['accepted']==stats.get('directed_exchanges',0)
        assert len(paired)==stats.get('paired_exchange_attempts',0)
        assert sum(a['outcome']=='accepted' for a in paired)==stats.get('paired_exchanges',0)
    return {'invocations':len(traces),'attempts':len(attempts),'outcomes':dict(counts),
        'paired_attempts':len(paired),'paired_accepted':sum(a['outcome']=='accepted' for a in paired),
        'neutral_attempts':sum(a['neutral_inventory'] for a in attempts),
        'neutral_accepted':sum(a['neutral_inventory'] and a['outcome']=='accepted' for a in attempts),
        'retained_proposals':len(proposals),'retained_neutral_proposals':sum(neutral(p) for p in proposals),
        'attempt_rows':attempts,'traces':traces}


def read_trace(archive, record):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        for name,expected in case['artifacts'].items():assert prior.sha256(z.read(name)).hexdigest()==expected
        traces=[json.loads(line.removeprefix('BALANCED_DIAG '))
            for line in z.read('search-stderr.log').decode('utf-8').splitlines() if line.startswith('BALANCED_DIAG ')]
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
    psutil.Process().cpu_affinity(list(range(16,32)))
    (prepare if args.action=='prepare' else run)(out)
