"""Observe available pair choices, requested repair time and rejection stages of the larger-return candidate.

Two diagnostic-only searches: panel hardware, both kerfs,
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
import struct
import os
import shutil
import subprocess
import time
import traceback
import zipfile

import psutil
import h5_larger_return_pilot as prior

ROOT = prior.ROOT
PROBE = ROOT/'output/h5-exact-state-20261018'
OLD = ROOT/'benchmarks/results/h5-larger-return-pilot-20261018'
JOBS = ['m-mechanical-panel-hardware']
load, write, digest = prior.load, prior.write, prior.digest


def guards():
    paths = [Path(__file__), ROOT/'scripts/h5_larger_return_pilot.py',
        ROOT/'scripts/cutting_development_set.py', ROOT/'scripts/h6_material_cost.py',
        ROOT/'scripts/h4_full_matrix.py', prior.CLI, PROBE/'preparation.json',
        PROBE/'build.json', PROBE/'exchange-diagnosis.exe', OLD/'verification.json',
        ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json',
        PROBE/'reconstruction.json', PROBE/'authored-trace-reader/checks.json',
        ROOT/'benchmarks/results/h5-exact-state-preparation-20261018/checks.json']
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
    assert load(ROOT/'benchmarks/results/h5-exact-state-preparation-20261018/checks.json')['all_qualified']
    assert digest(PROBE/'exchange-diagnosis.exe') == load(PROBE/'build.json')['binary_sha256']
    assert load(OLD/'verification.json')['valid'] == 72
    assert load(ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json')['H4_complete']
    out.mkdir(exist_ok=False)
    write(out/'plan.json', {'scope':__doc__, 'jobs':JOBS, 'kerfs_mm':[0.2,1.5],
        'seed':0, 'seconds':60, 'attempts':2, 'cpu':8, 'concurrency':1,
        'maximum_session_seconds':1200, 'guards':guards(),
        'source_change':'Read-only source inventory and bounded pair choices, receiver/source requested time and actual duration, losses, immediate material/extent and rejection stage. Pair sample rejection partitions, choice construction/attempt setup/reconstruction/validation duration, accepted phase and total remaining time, and complete after-exchange/after-fill layouts. Also compare complete internal pose multisets using exact float bits and shared original item/container identity, and retain both public layouts for each neutral rejection. Every inserted observation reverses exactly; no decision or work charge changes.',
        'interpretation':'Diagnostic only; trace overhead can alter wall-clock outcomes. No quality comparison, no retry of the rejected paired pilot.',
        'retention':'All original attempts, traces, public exports and independent validation in immutable per-attempt ZIPs.',
        'held_out_geometry_read':False, 'production_changed':False, 'H5_complete':False})
    shutil.copyfile(__file__,out/'runner.py')


def neutral(proposal):
    return sorted(proposal['incoming_ids']) == sorted(proposal['returned_ids'])


def public_signature(layout):
    assert len({(p['part_id'],p['copy_index']) for p in layout['placements']})==len(layout['placements'])
    result=Counter()
    for p in layout['placements']:
        t=p['transform'];values=[t['rotation_radians'],*t['translation']]
        assert len(values)==3 and all(type(v) in [int,float] and math.isfinite(v) for v in values)
        assert type(t['mirrored']) is bool
        result[(p['sheet_id'],p['part_id'],*(struct.pack('!d',float(v)) for v in values),t['mirrored'])]+=1
    return result


def check_traces(traces, stats=None):
    assert isinstance(traces,list) and traces
    attempts=[];proposals=[]
    def positive(value):
        assert type(value) in [int,float] and math.isfinite(value) and value>0
    def loss(value):
        assert value is None or (type(value) in [int,float] and math.isfinite(value) and value>=0)
    outcomes={'accepted','receiver_repair_failed','source_repair_failed','expired_after_repairs',
              'independent_geometry_failed','material_guard_failed','expired_before_acceptance',
              'forbidden_incoming_orientation','neutral_inventory_rejected'}
    for t in traces:
        assert type(t['disabled_or_expired']) is bool and type(t['baseline_invalid']) is bool
        ps=t['proposals'];seen=set()
        assert type(t['total_elapsed']) in [int,float] and math.isfinite(t['total_elapsed']) and t['total_elapsed']>=0
        for key in ['entry_remaining','baseline_elapsed']:
            value=t[key]
            assert value is None or (type(value) in [int,float] and math.isfinite(value))
        assert t['baseline_elapsed'] is None or t['baseline_elapsed']>=0
        assert isinstance(t['choice_setup'],list) and isinstance(t['layouts'],list)
        for setup in t['choice_setup']:
            assert type(setup['paired']) is bool and type(setup['target']) is int and setup['target']>=0
            assert len(setup['incoming_ids'])==(2 if setup['paired'] else 1)
            assert all(type(i) is int and i>=0 for i in setup['incoming_ids'])
            for key in ['elapsed','start_remaining']:assert type(setup[key]) in [int,float] and math.isfinite(setup[key])
            assert setup['elapsed']>=0
        assert sum(s['paired'] for s in t['choice_setup'])==len(t['generations'])
        if t['layouts']:
            assert [v['stage'] for v in t['layouts']]==['after_exchange','after_fill']
            assert sum(a['outcome']=='accepted' for a in t['attempts'])==1
            counts=[v['exchange_count'] for v in t['layouts']]
            assert counts[0]==counts[1] and type(counts[0]) is int and counts[0]>0
            for view in t['layouts']:
                assert type(view['remaining']) in [int,float] and math.isfinite(view['remaining'])
                assert view['stats']['directed_exchanges']==counts[0]
                assert isinstance(view['layout']['placements'],list) and view['layout']['placements']
            assert t['layouts'][1]['stats']['post_exchange_fill_calls']==t['layouts'][0]['stats'].get('post_exchange_fill_calls',0)+1

        assert isinstance(t['generations'],list)
        if t['disabled_or_expired'] or t['baseline_invalid']:
            assert not ps and not t['attempts'] and not t['generations']
            assert t['before_material'] is None and t['before_last_extent'] is None
            continue
        positive(t['before_material']);positive(t['before_last_extent'])
        source=t['available_source_items'];choices=t['pair_choices']
        assert isinstance(source,list) and all(type(i) is int and i>=0 for i in source)
        assert isinstance(choices,list) and len(choices)<=12
        inventory=Counter(source)
        for pair in choices:
            assert isinstance(pair,list) and len(pair)==2
            assert all(type(i) is int and i>=0 for i in pair)
            assert not (Counter(pair)-inventory)
        for key in ['exchange_remaining','pair_phase_remaining']:
            assert type(t[key]) in [int,float] and math.isfinite(t[key])
        assert abs(t['pair_phase_remaining']-max(0,t['exchange_remaining'])*.5)<=1e-9

        for g in t['generations']:
            ids=g['incoming_ids'];assert isinstance(ids,list) and len(ids)==2
            assert all(type(i) is int and i>=0 for i in ids) and ids in choices
            assert not (Counter(ids)-inventory)
            counts=['sample_total','seen','invalid_pose','boundary','empty','over_three','area_rejected','eligible','retained']
            assert all(type(g[k]) is int and g[k]>=0 for k in counts)
            assert g['area_rejected']==0, 'The candidate has no paired area filter'
            assert g['seen']<=g['sample_total']
            assert g['seen']==sum(g[k] for k in ['invalid_pose','boundary','empty','over_three','area_rejected','eligible'])
            assert g['retained']<=min(6,g['eligible'])
            assert type(g['deadline_reached']) is bool
            assert g['deadline_reached']==(g['seen']<g['sample_total'])
            assert type(g['start_remaining']) in [int,float] and math.isfinite(g['start_remaining'])
            assert type(g['elapsed']) in [int,float] and math.isfinite(g['elapsed']) and g['elapsed']>=0
        assert sum(g['retained'] for g in t['generations'])==sum(p['paired'] for p in ps)
        for p in ps:
            assert type(p['paired']) is bool and type(p['target']) is int and p['target']>=0
            for key in ['incoming_ids','returned_ids']:
                assert isinstance(p[key],list) and p[key] and all(type(i) is int and i>=0 for i in p[key])
            assert len(p['incoming_ids'])==(2 if p['paired'] else 1)
            assert not (Counter(p['incoming_ids'])-inventory)
            if p['paired']:assert p['incoming_ids'] in choices
            assert 1<=len(p['returned_ids'])<=p['blockers']<=3 and type(p['blockers']) is int
            positive(p['incoming_area']);positive(p['returned_area'])
            if p['paired']:
                assert len(p['returned_ids'])==p['blockers']
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

            for stage in ['receiver','source']:
                remaining=a[stage+'_remaining'];elapsed=a[stage+'_elapsed']
                if a[stage+'_initial_loss'] is None:
                    assert remaining is None and elapsed is None
                else:
                    assert type(remaining) in [int,float] and math.isfinite(remaining)
                    assert type(elapsed) in [int,float] and math.isfinite(elapsed) and elapsed>=0
            for key in ['attempt_setup_elapsed','reconstruction_elapsed','validation_elapsed']:
                value=a[key]
                assert value is None or (type(value) in [int,float] and math.isfinite(value) and value>=0)
            assert (a['attempt_setup_elapsed'] is None)==(a['receiver_initial_loss'] is None)
            assert (a['reconstruction_elapsed'] is None)==(a['after_last_extent'] is None)
            assert (a['validation_elapsed'] is None)==(a['after_last_extent'] is None)
            for key in ['accepted_phase_remaining','accepted_total_remaining']:
                value=a[key]
                if a['outcome']=='accepted':assert type(value) in [int,float] and math.isfinite(value)
                else:assert value is None
            value=a['identity_elapsed']
            assert value is None or (type(value) in [int,float] and math.isfinite(value) and value>=0)
            assert (value is None)==(a['after_last_extent'] is None)
            if value is None:assert a['exact_state'] is None
            else:assert type(a['exact_state']) is bool
            views=a['neutral_layouts']
            if a['outcome']=='neutral_inventory_rejected':
                assert type(views) is dict and set(views)=={'incumbent','trial'}
                assert views['incumbent']['sheets']==views['trial']['sheets']
                left=public_signature(views['incumbent']);right=public_signature(views['trial'])
                assert Counter(p['part_id'] for p in views['incumbent']['placements'])==Counter(p['part_id'] for p in views['trial']['placements'])
                if a['exact_state']:assert left==right
            else:assert views is None
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
                if outcome=='accepted':
                    assert a['after_material']<=t['before_material']
                    if neutral(p):assert a['after_material']<t['before_material']
                elif outcome=='neutral_inventory_rejected':
                    assert neutral(p) and a['after_material']==t['before_material']
            attempts.append({**a,'proposal':p,'neutral_inventory':neutral(p),
                'before_material':t['before_material'],'before_last_extent':t['before_last_extent']})
    counts=Counter(a['outcome'] for a in attempts)
    paired=[a for a in attempts if a['proposal']['paired']]
    mixed=[a for a in paired if len(set(a['proposal']['incoming_ids']))==2]
    if stats is not None:
        assert len(mixed)==stats.get('mixed_exchange_attempts',0)
        assert sum(a['outcome']=='accepted' for a in mixed)==stats.get('mixed_exchanges',0)
        assert len(attempts)==stats.get('directed_exchange_attempts',0)
        assert counts['accepted']==stats.get('directed_exchanges',0)
        assert counts['neutral_inventory_rejected']==stats.get('neutral_exchange_rejections',0)
        assert len(paired)==stats.get('paired_exchange_attempts',0)
        assert sum(a['outcome']=='accepted' for a in paired)==stats.get('paired_exchanges',0)
    return {'invocations':len(traces),'attempts':len(attempts),'outcomes':dict(counts),
        'mixed_attempts':len(mixed),'mixed_accepted':sum(a['outcome']=='accepted' for a in mixed),
        'paired_attempts':len(paired),'paired_accepted':sum(a['outcome']=='accepted' for a in paired),
        'neutral_attempts':sum(a['neutral_inventory'] for a in attempts),
        'neutral_accepted':sum(a['neutral_inventory'] and a['outcome']=='accepted' for a in attempts),
        'retained_proposals':len(proposals),'retained_neutral_proposals':sum(neutral(p) for p in proposals),
        'attempt_rows':attempts,'traces':traces}


def parse_log(log):
    traces=[];pending=[]
    for line in log.splitlines():
        if line.startswith('LARGER_GENERATION '):
            pending.append(json.loads(line.removeprefix('LARGER_GENERATION ')))
        elif line.startswith('LARGER_DIAG '):
            trace=json.loads(line.removeprefix('LARGER_DIAG '))
            assert 'generations' not in trace
            trace['generations']=pending;trace['layouts']=[];pending=[];traces.append(trace)
        elif line.startswith('LARGER_LAYOUT '):
            assert traces and not pending, 'orphaned layout trace'
            traces[-1]['layouts'].append(json.loads(line.removeprefix('LARGER_LAYOUT ')))
    assert not pending,'orphaned generation trace'
    return traces


def read_trace(archive, record):
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        for name,expected in case['artifacts'].items():assert prior.sha256(z.read(name)).hexdigest()==expected
        traces=parse_log(z.read('search-stderr.log').decode('utf-8'))
    summary=check_traces(traces,record.get('stats') if record['status']=='valid' else None)
    assert sum(len(t['layouts']) for t in traces)==2*summary['outcomes'].get('accepted',0)
    assert [t['layouts'][0]['exchange_count'] for t in traces if t['layouts']]==list(range(1,summary['outcomes'].get('accepted',0)+1))
    return summary


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
