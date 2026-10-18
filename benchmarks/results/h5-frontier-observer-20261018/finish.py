from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,shutil,sys,zipfile
import psutil
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'));import h5_frontier_observer as runner
out=root/'benchmarks/results/h5-frontier-observer-20261018'
load,write,digest=runner.load,runner.write,runner.digest
result=load(out/'results.json');plan=load(out/'plan.json');opened=load(out/'opened.json')
try:cmd=psutil.Process(opened['pid']).cmdline()
except psutil.NoSuchProcess:cmd=[]
assert not any('h5_frontier_observer.py' in c for c in cmd)
assert result['guards_unchanged'] and runner.guards()==plan['guards']
assert digest(out/'plan.json')==opened['plan_sha256'] and result['wall_seconds']<1200
assert len(result['records'])==2
assert {(r['job'],r['kerf_mm'],r['seed']) for r in result['records']}=={(j,k,0) for j in runner.JOBS for k in [0.2,1.5]}
archives=[];observations=[];attempts=[]
for row in result['records']:
    archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
    checked_trace=runner.read_trace(archive,row)
    assert checked_trace==row['diagnosis'] and row['status']=='valid'
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
    attempts += [{'job':row['job'],'kerf_mm':row['kerf_mm'],**a} for a in checked_trace['attempt_rows']]
    observations.append({'job':row['job'],'kerf_mm':row['kerf_mm'],**{k:v for k,v in checked_trace.items() if k not in ['traces','attempt_rows']}})
summary={'attempts':len(attempts),'outcomes':dict(Counter(a['outcome'] for a in attempts)),
    'paired_attempts':sum(len(a['incoming'])==2 for a in attempts),
    'mixed_attempts':sum(len(set(a['incoming']))==2 for a in attempts),
    'quality_claim':False,'earlier_pilot_trajectory_reconstructed':False}
write(out/'observed-exchanges.json',{'summary':summary,'observations':observations,'attempts':attempts})
write(out/'verification.json',{'all_original_archives_verified':True,'all_traces_verified':True,
    'archives':archives,'valid':2,'actual_exchange_attempts':len(attempts),'unchanged_source_binary_input_guards':True,
    'original_job_metrics_and_quantities_verified':True,'H5_complete':False,'integrated':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'finish.py')
print(json.dumps(summary))
