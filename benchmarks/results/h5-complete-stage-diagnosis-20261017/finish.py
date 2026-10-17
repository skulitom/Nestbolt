from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
import shutil
import sys
import zipfile
import psutil
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
import h5_complete_stage_diagnosis as runner
out=root/'benchmarks/results/h5-complete-stage-diagnosis-20261017'
load,write,digest=runner.load,runner.write,runner.digest
result=load(out/'results.json');plan=load(out/'plan.json');opened=load(out/'opened.json')
try:cmd=psutil.Process(opened['pid']).cmdline()
except psutil.NoSuchProcess:cmd=[]
assert not any('h5_complete_stage_diagnosis.py' in c for c in cmd)
assert result['guards_unchanged'] and runner.guards()==plan['guards']
assert digest(out/'plan.json')==opened['plan_sha256']
assert result['wall_seconds']<1200
assert len(result['records'])==4
assert {(r['job'],r['kerf_mm'],r['seed']) for r in result['records']}=={(j,k,0) for j in runner.JOBS for k in [0.2,1.5]}
archives=[];observations=[];attempts=[];sampling=Counter()
for row in result['records']:
    archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
    verified=runner.read_trace(archive,row)
    assert verified==row['diagnosis'] and row['status']=='valid'
    with zipfile.ZipFile(archive) as z:
        case=json.loads(z.read('case.json'))
        assert case=={k:v for k,v in row.items() if k not in ['archive','archive_sha256','diagnosis']}
        assert set(z.namelist())==set(case['artifacts'])|{'case.json'}
        checked=json.loads(z.read('validate-stdout.json'));search=json.loads(z.read('nested/search.json'))
        job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
        assert checked['valid'] and search['validation']['valid']
        runner.prior.equivalent(checked['metrics'],search['validation']['metrics'])
        assert checked['metrics']==row['metrics'] and checked['metrics']['normalized_material']==row['material']
        assert len(layout['placements'])==sum(p['quantity'] for p in job['parts'])
        assert search['stats']==row['stats'] and search['riders']==row['riders']==0
        assert sha256(z.read('nested/layout.json')).hexdigest()==row['layout_sha256']
        assert row['search']['exit_code']==row['validation']['exit_code']==row['export']['exit_code']==0
        archives.append({'path':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'members':len(z.namelist())})
    attempts += [a for trace in verified['traces'] for a in trace['attempts']]
    sampling.update(verified['sampling_totals'])
    observations.append({'job':row['job'],'kerf_mm':row['kerf_mm'],**{k:v for k,v in verified.items() if k!='traces'}})
stages={'all':dict(Counter(a['outcome'] for a in attempts)),
    'complete':dict(Counter(a['outcome'] for a in attempts if a['victims']==a['blockers'])),
    'partial':dict(Counter(a['outcome'] for a in attempts if a['victims']<a['blockers']))}
write(out/'observed-stages.json',{'observations':observations,'aggregate_attempt_outcomes':stages,'sampling_totals':dict(sampling),
    'quality_or_speed_claim':False,'global_infeasibility_claim':False})
write(out/'verification.json',{'all_original_archives_and_traces_verified':True,'archives':archives,'valid':4,
    'actual_exchange_attempts':len(attempts),'unchanged_source_binary_input_guards':True,
    'original_job_metrics_and_quantities_verified':True,'H5_complete':False,'integrated':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'finish.py')
lines=['# Complete-set eligibility and repair diagnosis — 2026-10-17','',
    '**All four diagnostic layouts validate.** These observations locate filters',
    'and repair stages; they do not measure improvement or replace the failed pilot.','',
    'The [committed plan](h5-complete-stage-diagnosis-20261017/plan.json) fixes',
    'both mechanical jobs, both kerfs, seed zero, 60 seconds and serial CCD0 CPU 8.',
    'Production and the original rejected candidate remain unchanged. Aggregate',
    'tracing preserves decisions but may perturb wall-clock behavior.','',
    '| Job | Kerf mm | Attempted exchanges | Complete-set outcomes | Partial-set outcomes | Eligible full-set samples: smaller / equal-or-larger area |',
    '| --- | ---: | ---: | --- | --- | ---: |']
for row in observations:
    readable=lambda d:', '.join(f'{k}: {v}' for k,v in d.items()) or 'none'
    s=row['sampling_totals']
    lines.append(f"| {row['job']} | {row['kerf_mm']} | {row['attempts']} | {readable(row['complete_vs_partial']['complete'])} | {readable(row['complete_vs_partial']['partial'])} | {s['multi_eligible_smaller']} / {s['multi_eligible_not_smaller']} |")
lines += ['',f"The complete session takes {result['wall_seconds']/60:.3f} minutes. All four",
    'original-job validations, quantities, metrics, zero reported hole riders',
    'and public exports pass. Every immutable attempt archive passes CRC and',
    'all member hashes; trace attempt/acceptance counts match saved solver counters.',
    '[Full observations](h5-complete-stage-diagnosis-20261017/observed-stages.json)',
    'retain sample eligibility, returned-area ratios and both repair losses.',
    '[Verification](h5-complete-stage-diagnosis-20261017/verification.json) binds',
    'source/binaries/inputs to the precommitted plan.','',
    'An eligible sample is not proof of a feasible exchange, and a failed repair',
    'is not proof of impossibility. Any new heuristic needs separate authored',
    'correctness checks and a committed comparison. Original H5 conditions,',
    'failed measurements and the reserved split remain unchanged. **60% complete; H2/H5 open.**','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'all_four_valid':True,'stages':stages,'sampling':dict(sampling),'wall_seconds':result['wall_seconds']}))
