"""Verify the one-use isolated score probe and seal its original outcomes."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import psutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h4-score-chunks-probe-20261016'
sys.path.insert(0,str(ROOT/'scripts'))
import h4_score_chunks_probe as probe
load=probe.load
write=probe.write
digest=probe.quality.digest

result=load(OUT/'results.json')
assert not (OUT/'interruption.json').exists()
opened=load(OUT/'opened.json')
assert not psutil.pid_exists(opened['pid']) or not any('h4_score_chunks_probe.py' in p for p in psutil.Process(opened['pid']).cmdline())
plan=load(OUT/'plan.json')
assert digest(OUT/'plan.json')==opened['plan_sha256']
assert subprocess.check_output(['git','show','HEAD:'+ (OUT/'plan.json').relative_to(ROOT).as_posix()],cwd=ROOT)==(OUT/'plan.json').read_bytes()
rows=probe.quality.cases()
assert rows==plan['cases'] and probe.guards(rows)==plan['guards'] and result['guards_unchanged']
assert result['records']==load(OUT/'records.json')
summary=probe.quality.summarize(result['records'],rows,[0,1,2],60)
assert json.loads(json.dumps(summary))==result['summary']
assert result['wall_seconds']<3600
expected={(r['id'],s) for r in rows for s in [0,1,2]}
checked=[]
for engine,records in result['records'].items():
    assert len(records)==33 and {(r['job'],r['seed']) for r in records}==expected
    for record in records:
        folder=(ROOT/record['directory']).resolve()
        assert folder.is_relative_to(OUT.resolve())
        assert load(folder/'case.json')==record
        if record['status']!='valid':
            checked.append({'engine':engine,'job':record['job'],'seed':record['seed'],'status':record['status']})
            continue
        assert digest(folder/'layout.json')==record['layout_sha256']
        validation=load(folder/'validate-stdout.json')
        search=load(folder/('search-stdout.json' if engine=='native' else 'result.json'))
        assert validation['valid'] and search['validation']['valid']
        delta=probe.quality.equivalent(validation['metrics'],search['validation']['metrics'])
        assert validation['metrics']['normalized_material']==record['material']
        row=next(r for r in rows if r['id']==record['job'])
        assert len(load(folder/'layout.json')['placements'])==sum(p['quantity'] for p in load(ROOT/row['path'])['parts'])
        if 'library' in row:
            public=load(folder/'public-validate-stdout.json')
            assert public['valid']
            delta=max(delta,probe.quality.equivalent(public['metrics'],validation['metrics']))
        assert delta==record['maximum_metric_json_roundtrip_difference']
        checked.append({'engine':engine,'job':record['job'],'seed':record['seed'],'status':'valid','maximum_metric_roundtrip_difference':delta})
replays=load(OUT/'replay-results.json')
assert replays['all_passed'] and len(replays['records'])==4
for pair in replays['records']:
    results=[]
    for arm in ['baseline','candidate']:
        folder=ROOT/pair['arms'][arm]['directory']
        search=load(folder/'search-stdout.json')
        validation=load(folder/'validate-stdout.json')
        assert search['repeatable'] and validation['valid']
        probe.quality.equivalent(validation['metrics'],search['validation']['metrics'])
        search.pop('elapsed_seconds');results.append(search)
    assert results[0]==results[1]
    assert load(ROOT/pair['arms']['baseline']['directory']/'layout.json')==load(ROOT/pair['arms']['candidate']['directory']/'layout.json')
batches=[]
for engine in ['chrome','firefox']:
    for seed in [0,1,2]:
        folder=OUT/engine/f's{seed}'
        execution=load(folder/'execution.json')
        info=load(folder/'browser.json')
        batches.append({'browser':engine,'seed':seed,'version':info['version'],
            'exit_code':execution['exit_code'],'cpus':execution['cpus'],'affinity_errors':execution['affinity_errors']})
preparation=ROOT/'benchmarks/results/h4-score-chunks-preparation-20261016'
prep=load(preparation/'integrity.json')
assert digest(preparation/'raw.zip')==prep['sha256']
write(OUT/'verification.json',{'original_records_verified':True,'candidate_preparation_archive_sha256':prep['sha256'],
    'exact_replay_pairs':4,'quality_attempts':99,'valid':sum(r['status']=='valid' for r in checked),
    'maximum_metric_roundtrip_difference':max((r.get('maximum_metric_roundtrip_difference',0) for r in checked),default=0),
    'browser_batches':batches,'production_guards_unchanged':True,'subset_pass':summary['passes_subset'],
    'H4_complete':False,'integrated':False,'held_out_geometry_read':False})
shutil.copyfile(__file__,OUT/'finalize.py')
archive=OUT/'raw.zip'
assert not archive.exists()
files=sorted(p for p in OUT.rglob('*') if p.is_file())
inventory={p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p)} for p in files}
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,row in inventory.items():
        raw=z.read(name)
        assert len(raw)==row['bytes'] and sha256(raw).hexdigest()==row['sha256']
write(OUT/'integrity.json',{'archive':archive.relative_to(ROOT).as_posix(),'bytes':archive.stat().st_size,
    'sha256':digest(archive),'members':inventory,'crc_and_every_member_verified':True})
print(json.dumps({'subset_pass':summary['passes_subset'],'members':len(files),'sha256':digest(archive)}))
