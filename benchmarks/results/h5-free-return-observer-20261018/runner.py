"""Observe actual free-return seeding and subsequent repair/material outcomes.

Four diagnostic-only searches: both mechanical jobs, both kerfs, seed zero,
60 seconds, serial physical CCD0 CPU 8. No search decision, work charge,
deadline, random draw, geometry or acceptance guard changes. All 137 tests
are unchanged. Logging can perturb wall trajectories; no quality claim.
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
import h5_free_return_pilot as prior

ROOT = prior.ROOT
PROBE = ROOT/'output/h5-free-return-observer-20261018'
OLD = ROOT/'benchmarks/results/h5-free-return-pilot-20261018'
JOBS = ['m-mechanical-large-plates','m-mechanical-panel-hardware']
load, write, digest = prior.load, prior.write, prior.digest


def guards():
    paths = [Path(__file__), ROOT/'scripts/h5_free_return_pilot.py', ROOT/'scripts/h5_frontier_observer.py', ROOT/'scripts/h5_boundary_pair_observer.py',
        ROOT/'scripts/cutting_development_set.py', ROOT/'scripts/h6_material_cost.py',
        ROOT/'scripts/h4_full_matrix.py', prior.CLI, PROBE/'preparation.json',
        PROBE/'build.json', PROBE/'exchange-diagnosis.exe', OLD/'verification.json',
        ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json',
        PROBE/'reconstruction.json', PROBE/'authored-trace-reader/checks.json',
        ROOT/'benchmarks/results/h5-free-return-observer-preparation-20261018/checks.json']
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
    assert load(ROOT/'benchmarks/results/h5-free-return-observer-preparation-20261018/checks.json')['all_qualified']
    assert digest(PROBE/'exchange-diagnosis.exe') == load(PROBE/'build.json')['binary_sha256']
    assert load(OLD/'verification.json')['valid'] == 72
    assert load(ROOT/'benchmarks/results/h4-depth-complete-20261016/checks.json')['H4_complete']
    out.mkdir(exist_ok=False)
    write(out/'plan.json', {'scope':__doc__, 'jobs':JOBS, 'kerfs_mm':[0.2,1.5],
        'seed':0, 'seconds':60, 'attempts':4, 'cpu':8, 'concurrency':1,
        'maximum_session_seconds':1200, 'guards':guards(),
        'source_change':'Capture actual contained and placed return poses, source inventory, work counters, repair losses and full validated material outcomes including acceptance. No former seed formula is recomputed. Removing observation code reconstructs the failed candidate exactly; all 137 tests remain unchanged.',
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
    stripped=copy.deepcopy(traces);observations=[]
    count_fields={'constructor_checks','containers','evaluated_vertices','evaluations','rect_operations',
                  'registered_items','tracked_items','tracked_vertices','validated_vertices'}
    def finite(value):
        assert type(value) in [int,float] and math.isfinite(value) and value>=0
    def poses(values):
        assert isinstance(values,list)
        for p in values:pose_key(p)
        return Counter(p['part_id'] for p in values)
    for invocation,(trace,clean) in enumerate(zip(traces,stripped)):
        base=trace['baseline'];inventory=Counter({p['id']:p['quantity'] for p in base['job']['parts']})
        source=Counter(p['part_id'] for p in base['layout']['placements'] if p['sheet_id']==base['source_sheet'])
        for index,(attempt,without) in enumerate(zip(trace['attempts'],clean['attempts'])):
            seed=without.pop('return_seed_detail');repair=without.pop('repair_detail');material=without.pop('material_detail')
            outcome=attempt['outcome'];choice=trace['choices'][attempt['choice_index']]
            expected=source.copy();expected.subtract(choice);assert all(v>=0 for v in expected.values());expected=+expected
            if outcome=='forbidden_incoming_orientation':
                assert seed is repair is material is None
                continue
            assert isinstance(seed,dict) and set(seed)=={'source_before','contained','placed','work_before','work_after'}
            assert poses(seed['source_before'])==expected
            physical_source=Counter(pose_key({'part_id':p['part_id'],'transform':p['transform']})
                for p in base['layout']['placements'] if p['sheet_id']==base['source_sheet'])
            physical_source.subtract(pose_key(p) for p in trace['choice_poses'][attempt['choice_index']])
            assert all(v>=0 for v in physical_source.values())
            assert Counter(pose_key(p) for p in seed['source_before'])==+physical_source
            expected.update(attempt['returned'])
            assert poses(seed['contained'])==poses(seed['placed'])==Counter(attempt['returned'])
            assert [p['part_id'] for p in seed['contained']]==[p['part_id'] for p in seed['placed']]==attempt['returned']
            for before,after in zip(seed['contained'],seed['placed']):
                for field in ['rotation_radians','mirrored']:assert before['transform'][field]==after['transform'][field]
            for work in [seed['work_before'],seed['work_after']]:
                assert isinstance(work,dict) and set(work)==count_fields
                for v in work.values():finite(v)
            delta={k:seed['work_after'][k]-seed['work_before'][k] for k in count_fields}
            assert all(v>=0 for v in delta.values()) and delta['evaluations']<=257*len(attempt['returned'])
            assert all(delta[k]==0 for k in count_fields-{'evaluations','evaluated_vertices','rect_operations'})
            assert isinstance(repair,dict) and set(repair)=={'receiver_loss','source_loss','source_after'}
            finite(repair['receiver_loss'])
            if outcome=='receiver_repair_failed':
                assert repair['receiver_loss']>0 and repair['source_loss'] is repair['source_after'] is material is None
                reason='receiver_loss_positive'
            else:
                assert repair['receiver_loss']==0;finite(repair['source_loss']);assert poses(repair['source_after'])==expected
                if outcome=='source_repair_or_expiry':
                    assert material is None
                    reason='source_loss_positive' if repair['source_loss']>0 else 'source_deadline'
                else:
                    assert repair['source_loss']==0;reason=outcome
            if outcome in ['material_guard_or_expiry','neutral_inventory_rejected','accepted']:
                assert isinstance(material,dict) and set(material)=={'material_increased','metrics','layout'}
                after=material['metrics'];old=base['metrics'];finite(after['material_area'])
                assert type(after['sheets_used']) is int and after['sheets_used']>0
                assert type(material['material_increased']) is bool
                increased=after['sheets_used']>old['sheets_used'] or after['material_area']>old['material_area']
                assert material['material_increased']==increased
                layout=material['layout'];assert set(layout)==set(base['layout'])
                assert Counter(p['part_id'] for p in layout['placements'])==inventory
                assert len({(p['part_id'],p['copy_index']) for p in layout['placements']})==len(layout['placements'])
                known_sheets={p['sheet_id'] for p in base['layout']['placements']}
                for p in layout['placements']:
                    assert p['sheet_id'] in known_sheets;pose_key({'part_id':p['part_id'],'transform':p['transform']})
                if outcome=='accepted':
                    assert not increased
                    if Counter(choice)==Counter(attempt['returned']):assert after['material_area']<old['material_area']
                elif outcome=='neutral_inventory_rejected':
                    assert Counter(choice)==Counter(attempt['returned']) and not increased and after['material_area']==old['material_area']
                else:reason='material_increased' if increased else 'exchange_deadline'
            else:assert material is None
            observations.append({'invocation':invocation,'attempt_index':index,'choice_index':attempt['choice_index'],
                'target_sheet':attempt['target_sheet'],'outcome':outcome,'reason':reason,'work_delta':delta,
                'return_seed_detail':seed,'repair_detail':repair,'material_detail':material})
    result=parent.check_traces(stripped,stats);result['traces']=traces
    result['attempt_observations']=observations;result['reason_counts']=dict(Counter(o['reason'] for o in observations))
    result['actual_seed_and_stage_records_verified']=True
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
