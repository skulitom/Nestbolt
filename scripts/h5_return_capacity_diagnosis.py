"""Observe shortened-container capacity, complete initial/repaired geometry, frame legality and repair stages in the rejected return-frame candidate.

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
import h5_return_frame_pilot as prior

ROOT = prior.ROOT
PROBE = ROOT/'output/h5-return-capacity-diagnosis-20261017'
OLD = ROOT/'benchmarks/results/h5-return-frame-pilot-20261017'
JOBS = ['m-mechanical-large-plates', 'm-mechanical-panel-hardware']
load, write, digest = prior.load, prior.write, prior.digest


def guards():
    paths = [Path(__file__), ROOT/'scripts/h5_return_frame_pilot.py',
        ROOT/'scripts/cutting_development_set.py', ROOT/'scripts/h6_material_cost.py',
        ROOT/'scripts/h4_full_matrix.py', prior.CLI, PROBE/'preparation.json',
        PROBE/'build.json', PROBE/'exchange-diagnosis.exe', OLD/'verification.json',
        ROOT/'output/audit_h5_return_capacity.py', PROBE/'independent-audit-checks.json',
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
        'source_change':'Previous frame/stage records plus source/receiver contexts, actual collision-container polygons, every part identity/internal/public pose and collision polygon, and complete initial and returned-best-snapshot repair layouts. Captures can consume wall time; policy, charges and repair caps unchanged.',
        'interpretation':'Diagnostic only; trace overhead can alter wall-clock outcomes. No quality comparison, no retry of the rejected paired pilot.',
        'retention':'All original attempts, traces, public exports and independent validation in immutable per-attempt ZIPs.',
        'held_out_geometry_read':False, 'production_changed':False, 'H5_complete':False})
    shutil.copyfile(__file__,out/'runner.py')


def check_frame_attempt(attempt):
    frame=attempt['frame'];members=frame['members']
    assert len(members)==attempt['victims'] and members
    assert frame['mode'] in ['single','same_frame_translation','reciprocal','forbidden_translation']
    def pose(p):
        assert isinstance(p['reflected'],bool)
        assert len(p['translation'])==2
        assert all(isinstance(x,(float,int)) and math.isfinite(x) for x in [p['rotation'],*p['translation']])
    for p in [frame['incoming_before'],frame['incoming_here']]:pose(p)
    for member in members:
        assert isinstance(member['external_id'],int) and member['external_id']>=0
        assert isinstance(member['hypothetical_allowed'],bool) and member['actual_allowed'] is True
        for key in ['previous','hypothetical','actual']:pose(member[key])
    before,here=frame['incoming_before'],frame['incoming_here']
    same=before['rotation']==here['rotation'] and before['reflected']==here['reflected']
    if len(members)==1:
        assert frame['mode']=='single'
    elif same:
        assert frame['mode']=='same_frame_translation'
    elif all(m['hypothetical_allowed'] for m in members):
        assert frame['mode']=='reciprocal'
        assert all(m['actual']==m['hypothetical'] for m in members)
    else:
        assert frame['mode']=='forbidden_translation'
    if frame['mode'] in ['same_frame_translation','forbidden_translation']:
        for m in members:
            a,p=m['actual'],m['previous']
            assert a['rotation']==p['rotation'] and a['reflected']==p['reflected']
            for axis in [0,1]:
                expected=p['translation'][axis]+before['translation'][axis]-here['translation'][axis]
                # Trace coordinates are serialized f32. This checks the mapping,
                # not geometric validity, which has the unchanged public validator.
                scale=max(1,abs(p['translation'][axis]),abs(before['translation'][axis]),abs(here['translation'][axis]))
                assert abs(a['translation'][axis]-expected)<=5e-7*scale
    assert math.isfinite(attempt['before_material']) and attempt['before_material']>0
    if attempt['after_material'] is not None:
        assert math.isfinite(attempt['after_material']) and attempt['after_material']>0
    if attempt['outcome']=='accepted':
        assert attempt['after_material'] is not None and attempt['after_material']<=attempt['before_material']
        assert attempt['receiver_loss']==attempt['source_loss']==0
    for key in ['receiver_initial_loss','source_initial_loss','receiver_loss','source_loss']:
        value=attempt[key]
        assert value is None or (math.isfinite(value) and value>=0)



def check_capacity_trace(trace):
    def polygon(points):
        assert isinstance(points,list) and len(points)>=3
        assert all(len(p)==2 and all(isinstance(v,(int,float)) and math.isfinite(v) for v in p) for p in points)
        twice=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(points,points[1:]+points[:1]))
        assert abs(twice)>0
    def layout(value):
        polygon(value['container'])
        keys=[]
        for item in value['items']:
            keys.append(item['key'])
            assert isinstance(item['key'],str) and item['key']
            for field in ['external_id','item_index']:assert isinstance(item[field],int) and item[field]>=0
            assert math.isfinite(item['area_hint']) and item['area_hint']>0
            polygon(item['polygon'])
            pose=item['pose'];public=item['public_transform']
            assert isinstance(pose['reflected'],bool) and isinstance(public['mirrored'],bool)
            assert len(pose['translation'])==len(public['translation'])==2
            assert all(math.isfinite(v) for v in [pose['rotation'],*pose['translation'],public['rotation_radians'],*public['translation']])
        assert len(keys)==len(set(keys))
        return Counter((item['item_index'],item['external_id']) for item in value['items'])
    for context in trace['contexts']:
        layout(context['source_after_removal']);layout(context['receiver_before_removal'])
        assert context['shape_last']>0 and context['full_width']>=context['shape_last']
        assert 0<=context['target_index']<context['last_index'] and context['frozen_sheets']>=0
    for attempt in trace['attempts']:
        check_frame_attempt(attempt)
        assert isinstance(attempt['context_index'],int) and 0<=attempt['context_index']<len(trace['contexts'])
        context=trace['contexts'][attempt['context_index']]
        incoming=context['incoming'];identity=(incoming['item_index'],incoming['external_id'])
        assert incoming['pose']==attempt['frame']['incoming_before']
        source=layout(context['source_after_removal']);receiver=layout(context['receiver_before_removal'])
        original={item['key']:item for item in context['receiver_before_removal']['items']}
        members=attempt['frame']['members']
        assert len({m['receiver_key'] for m in members})==len(members)
        for member in members:
            previous=original[member['receiver_key']]
            assert previous['pose']==member['previous'] and previous['external_id']==member['external_id']
            item=(previous['item_index'],previous['external_id'])
            receiver[item]-=1;source[item]+=1
        receiver[identity]+=1
        receiver=+receiver
        for name,expected,boundary in [('source',source,context['source_after_removal']['container']),('receiver',receiver,context['receiver_before_removal']['container'])]:
            initial=attempt[name+'_initial'];repaired=attempt[name+'_repaired']
            assert layout(initial)==expected and initial['container']==boundary
            assert (repaired is None)==(attempt[name+'_loss'] is None)
            if repaired is not None:
                assert layout(repaired)==expected and repaired['container']==boundary


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
    for trace in traces:check_capacity_trace(trace)
    attempts = [a for t in traces for a in t['attempts']]
    samplings = [s for t in traces for s in t['samplings']]
    counts = Counter(a['outcome'] for a in attempts)
    assert not counts['unfinished']
    for attempt in attempts:
        check_frame_attempt(attempt)
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
        'frame_modes':dict(Counter(a['frame']['mode'] for a in attempts)),
        'outcomes_by_frame':{mode:dict(Counter(a['outcome'] for a in attempts if a['frame']['mode']==mode)) for mode in sorted({a['frame']['mode'] for a in attempts})},
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
