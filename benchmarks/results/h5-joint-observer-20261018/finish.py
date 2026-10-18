"""Verify every original diagnostic member and derive per-attempt observations."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,shutil,subprocess,sys,zipfile
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'));import h5_joint_observer as runner;import h5_joint_trace as trace
out=root/'benchmarks/results/h5-joint-observer-20261018'
load,write,digest=runner.load,runner.write,runner.digest
result=load(out/'results.json');plan=load(out/'plan.json');opened=load(out/'opened.json')
identity=runner.prior.require_runner_stopped(opened,'h5_joint_observer.py')
assert result['guards_unchanged'] and runner.guards()==plan['guards']
assert digest(out/'plan.json')==opened['plan_sha256'] and result['wall_seconds']<1200
assert subprocess.check_output(['git','show','HEAD:'+str((out/'plan.json').relative_to(root)).replace('\\','/')],cwd=root)==(out/'plan.json').read_bytes()
assert len(result['records'])==4 and result['all_valid']
assert {(r['job'],r['kerf_mm'],r['seed']) for r in result['records']}=={(j,k,0) for j in runner.JOBS for k in [0.2,1.5]}
archives=[];observations=[];attempts=[];forests=[]
def delta(before,after):return {n:after[n]-before[n] for n in sorted(set(before)|set(after)) if after[n]!=before[n]}
for row in result['records']:
    archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
    checked_trace=runner.read_trace(archive,row);assert checked_trace==row['diagnosis'] and row['status']=='valid'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        assert case=={k:v for k,v in row.items() if k not in ['archive','archive_sha256','diagnosis']}
        assert set(z.namelist())==set(case['artifacts'])|{'case.json'}
        for name,expected in case['artifacts'].items():assert sha256(z.read(name)).hexdigest()==expected
        checked=json.loads(z.read('validate-stdout.json'));search=json.loads(z.read('nested/search.json'))
        job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
        assert checked['valid'] and search['validation']['valid']
        runner.prior.equivalent(checked['metrics'],search['validation']['metrics'])
        assert checked['metrics']==row['metrics'] and checked['metrics']['normalized_material']==row['material']
        assert len(layout['placements'])==sum(p['quantity'] for p in job['parts'])
        assert search['stats']==row['stats'] and search['riders']==row['riders']==0
        assert sha256(z.read('nested/layout.json')).hexdigest()==row['layout_sha256']
        assert row['search']['exit_code']==row['validation']['exit_code']==row['export']['exit_code']==0
        traces=trace.parse_log(z.read('search-stderr.log').decode('utf-8'))
        archives.append({'path':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'members':len(z.namelist())})
    forests.append({'archive':row['archive'],'job':row['job'],'kerf_mm':row['kerf_mm'],'traces':traces})
    by={t['id']:t for t in traces};committed=set()
    for chain in [t for t in traces if t['kind']=='chain' and t['outcome']=='completed']:
        policies=sorted((t for t in traces if t['parent']==chain['id'] and t['outcome']=='accepted'),key=lambda t:t['id'])
        keep=trace.event(chain,'finished')['committed']
        for policy in policies[:keep]:committed.add(next(t['id'] for t in traces if t['parent']==policy['id'] and t['outcome']=='accepted'))
    for a in [t for t in traces if t['kind']=='attempt']:
        policy=by[a['parent']]['data'];pair=next(t for t in traces if t['parent']==a['id'])
        assert policy['job']==job and pair['data']['job']==job
        sid=f"sheet-{policy['frozen_count']+a['data']['source_active_sheet']}"
        original=trace.inventory([p for p in policy['baseline']['placements'] if p['sheet_id']==sid])
        proposed=trace.inventory(pair['data']['proposed'][1])
        recrops=[e['data'] for e in pair['events'] if e['stage']=='recrop_exit']
        lowers=[e['data'] for e in pair['events'] if e['stage']=='lowering_exit']
        sep=[e['data'] for e in pair['events'] if e['stage']=='separator_exit']
        trial=[e['data'] for e in a['events'] if e['stage']=='validated_trial']
        after=trial[0]['report'].get('metrics') if trial else None
        before=policy['metrics'];gain=before['material_area']-after['material_area'] if after else None
        reason=a['outcome']
        if reason=='material_guard_or_expiry':
            assert after is not None
            reason='material_increase' if after['sheets_used']>before['sheets_used'] or after['material_area']>before['material_area'] else 'whole_job_validation_expired'
        final=trace.inventory(lowers[0]['pair'][1]) if lowers else None
        attempts.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'archive':row['archive'],
            'attempt_id':a['id'],'policy_id':a['parent'],'pair_id':pair['id'],
            'outcome':a['outcome'],'resolved_reason':reason,'pair_outcome':pair['outcome'],
            'committed':a['id'] in committed,'material_gain_mm2':gain,
            'before_material_mm2':before['material_area'],'after_material_mm2':after['material_area'] if after else None,
            'before_credited_sheet':before['last_sheet_id'],'after_credited_sheet':after['last_sheet_id'] if after else None,
            'source_sheet':sid,'original_source_inventory':dict(original),'proposed_source_inventory':dict(proposed),
            'final_source_inventory':dict(final) if final is not None else None,
            'extra_net_source_changes':delta(proposed,final) if final is not None else None,
            'net_source_changes_from_baseline':delta(original,final) if final is not None else None,
            'separator_seconds':sep[0]['separator_seconds'] if sep else None,
            'lowering_seconds':lowers[0]['lowering_seconds'] if lowers else None,
            'pair_total_observed_seconds':pair['elapsed_seconds'],
            'note':'material_increase proves that guard fired; concurrent expiry is not separately sampled. Net inventories do not identify same-family copy swaps.'})
    observations.append({'job':row['job'],'kerf_mm':row['kerf_mm'],**checked_trace})
summary={'attempts':len(attempts),'outcomes':dict(Counter(a['outcome'] for a in attempts)),
    'resolved_reasons':dict(Counter(a['resolved_reason'] for a in attempts)),
    'pair_outcomes':dict(Counter(a['pair_outcome'] for a in attempts)),
    'accepted':sum(a['outcome']=='accepted' for a in attempts),'committed':sum(a['committed'] for a in attempts),
    'completed_with_extra_net_migration':sum(a['pair_outcome']=='completed' and bool(a['extra_net_source_changes']) for a in attempts),
    'accepted_with_extra_net_migration':sum(a['outcome']=='accepted' and bool(a['extra_net_source_changes']) for a in attempts),
    'accepted_material_gains_mm2':[a['material_gain_mm2'] for a in attempts if a['outcome']=='accepted'],
    'quality_claim':False,'earlier_pilot_trajectory_reconstructed':False}
write(out/'observed-exchanges.json',{'summary':summary,'observations':observations,'attempts':attempts})
write(out/'trace-forests.json',forests)
write(out/'verification.json',{'process_identity_check':identity,'all_original_archives_verified':True,'all_traces_verified':True,
    'archives':archives,'valid':4,'actual_exchange_attempts':len(attempts),'unchanged_source_binary_input_guards':True,
    'original_job_metrics_and_quantities_verified':True,'H5_complete':False,'integrated':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'finish.py');print(json.dumps(summary))
