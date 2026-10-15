"""Current public import/export regression on saved H2 training layouts.

Functional checks only: no nesting searches, timing claims or held-out inputs.
Run sequentially on CCD1 CPU 16 while the separately guarded H4 matrix uses CCD0.
The old per-case result must equal its committed report row. Historical raw
outputs were retained locally; their hashes are first recorded by this replay.
"""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import traceback

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from h2_import_audit import source_digest

CORPUS = ROOT/'benchmarks/datasets/shop'
REPORT = ROOT/'benchmarks/results/h2-fidelity-20261014T012836Z.json'
OLD = ROOT/'output/h2-fidelity-20261014T012836Z'
OUT = ROOT/'benchmarks/results/h2-export-replay-20261015'
CLI = ROOT/'target/release/nestbolt.exe'
digest = lambda p: sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_bytes())

def write(p, value):
    p.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')

def guards():
    return {'product':source_digest(), 'cli':digest(CLI), 'report':digest(REPORT),
        'runner':digest(Path(__file__)), 'manifest':digest(CORPUS/'manifest.json')}

def run(command, folder, name):
    with (folder/(name+'-stdout.json')).open('wb') as stdout, (folder/(name+'-stderr.log')).open('wb') as stderr:
        p=subprocess.Popen(list(map(str,command)),cwd=ROOT,stdout=stdout,stderr=stderr,
            creationflags=subprocess.CREATE_NO_WINDOW | 4)
        try:
            child=psutil.Process(p.pid)
            child.cpu_affinity([16])
            child.resume()
            code=p.wait(timeout=120)
        except subprocess.TimeoutExpired:
            p.kill();p.wait();code='timeout'
        except BaseException:
            p.kill();p.wait();raise
    return {'command':list(map(str,command)), 'exit_code':code, 'cpu':16}

psutil.Process().cpu_affinity([16])
before=guards()
assert before['cli']=='5e07f350761f3b5dfb820e404c85982dacd039d0789b8bfca63f66e76bf20bf7'
assert before['manifest']=='02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
manifest=load(CORPUS/'manifest.json')
training={r['path']:r for r in manifest['files'] if r['split']=='training'
    and Path(r['path']).suffix in ['.svg','.dxf'] and r.get('label')}
report=load(REPORT)
assert report['only'] is None and report['counts']=={'passed':246,'rejected':11}
rows_by_path={r['path']:r for r in report['rows']}
assert set(rows_by_path)==set(training) and len(training)==257
prepared=[]
seen=set()
OUT.mkdir()
(OUT/'runner.py').write_bytes(Path(__file__).read_bytes())
for source_folder in sorted(p for p in OLD.iterdir() if p.is_dir()):
    task=load(source_folder/'task.json')
    source_path=Path(task['path']).resolve().relative_to(CORPUS.resolve()).as_posix()
    entry=training[source_path]
    assert source_path not in seen
    seen.add(source_path)
    result=load(source_folder/'result.json')
    assert result==rows_by_path[source_path]
    assert digest(CORPUS/source_path)==entry['sha256']
    assert digest(CORPUS/entry['label'])==entry['label_sha256']
    if result['status']!='passed':
        assert result['status']=='rejected'
        continue
    folder=OUT/source_folder.name
    baseline=folder/'before'
    baseline.mkdir(parents=True)
    inputs=[source_folder/'task.json',source_folder/'result.json',
        *sorted(p for p in (source_folder/'exports').iterdir() if p.is_file())]
    hashes={}
    for p in inputs:
        target=baseline/p.name
        assert not target.exists()
        shutil.copyfile(p,target)
        assert digest(target)==digest(p)
        hashes[p.name]=digest(p)
    prepared.append({'path':source_path, 'folder':folder.relative_to(ROOT).as_posix(),
        'source_sha256':entry['sha256'],'label_sha256':entry['label_sha256'],
        'input_sha256':hashes, 'prior_status':'passed'})
assert len(prepared)==246 and seen==set(training)
write(OUT/'plan.json', {'scope':__doc__, 'guards':before,'cases':prepared,
    'cpu':16,'concurrency':1,'held_out_geometry_read':False,'new_searches':0,
    'prior_rejections_preserved':11,'historical_raw_hashes_previously_recorded':False,
    'checks':['Current import geometry equals retained library',
        'Saved layout validates through current public export',
        'Every current SVG/DXF byte equals its retained previously measured counterpart']})
results=[]
for index,entry in enumerate(prepared):
    folder=ROOT/entry['folder']; baseline=folder/'before'
    record={**entry,'status':'failed'}
    try:
        task=load(baseline/'task.json')
        command=[CLI,'import',CORPUS/entry['path'],'--output',folder/'library.json']
        options=task['options']
        for key,flag in [('layers','--layers'),('colors','--colors'),('close_gaps_mm','--close-gaps'),('dxf_unit','--dxf-unit-mm')]:
            if key in options and options[key] is not None:
                value=options[key]
                command += [flag,','.join(map(str,value)) if isinstance(value,list) else str(value)]
        record['import']=run(command,folder,'import')
        assert record['import']['exit_code']==0
        library=load(folder/'library.json'); old_library=load(baseline/'library.json')
        record['library_geometry_equal']=all(library.get(k)==old_library.get(k)
            for k in ['parts','tolerance','sheet_outlines','lightburn'])
        assert record['library_geometry_equal'], 'Current import geometry differs'
        old_job=load(baseline/'job.json')
        request={'name':old_job['name'],'parts':[{k:p[k] for k in ['id','quantity','rotations','allow_mirror','priority']} for p in old_job['parts']],
            'sheets':[{'id':s['id'],'width_mm':s['width'],'height_mm':s['height'],'count':s['count'],
                'margins_mm':s['margins'],'defects_mm':s['defects'],'outline_mm':s['outline']}
                for s in old_job['stocks']],
            'spacing_mm':1.0,'edge_spacing_mm':1.0,'mode':'all'}
        assert old_job['units']=='mm' and old_job['mode']=='all'
        assert all(p['quantity']==1 and p['allow_mirror'] for p in request['parts'])
        assert old_job['clearance']==1.0+2*library['tolerance']
        assert old_job['edge_clearance']==1.0+library['tolerance']
        write(folder/'request.json',request)
        record['export']=run([CLI,'export','--library',folder/'library.json','--request',folder/'request.json',
            '--layout',baseline/'layout.json','--out-dir',folder/'after','--sheet-outline','false'],folder,'export')
        assert record['export']['exit_code']==0, 'Current standalone export/validation failed'
        expected=sorted(p.name for p in baseline.iterdir() if p.suffix in ['.svg','.dxf'])
        actual=sorted(p.name for p in (folder/'after').iterdir() if p.suffix in ['.svg','.dxf'])
        assert expected==actual and len(expected)==2*len(load(baseline/'layout.json')['sheets'])
        record['files']=[{'file':name,'before_sha256':digest(baseline/name),'after_sha256':digest(folder/'after'/name),
            'byte_identical':(baseline/name).read_bytes()==(folder/'after'/name).read_bytes()} for name in expected]
        assert all(r['byte_identical'] for r in record['files']), 'Export bytes changed'
        record['status']='passed'
    except Exception:
        record['error']=traceback.format_exc()
    write(folder/'case.json',record)
    results.append(record)
    write(OUT/'progress.json', {'done':len(results),'passed':sum(r['status']=='passed' for r in results),
        'failed':sum(r['status']!='passed' for r in results)})
    if record['status']!='passed' or (index+1)%20==0:
        print(json.dumps({'done':index+1,'path':entry['path'],'status':record['status'], 'error':record.get('error')}),flush=True)
unchanged=guards()==before
write(OUT/'results.json',{'scope':__doc__,'guards':before,'guards_unchanged':unchanged,
    'passed':unchanged and len(results)==246 and all(r['status']=='passed' for r in results),
    'imported_files':246,'prior_rejections':11,'held_out_geometry_read':False,'new_searches':0,
    'exported_files':sum(len(r.get('files',[])) for r in results),'rows':results})
assert unchanged
print(json.dumps({'out':str(OUT),'passed':all(r['status']=='passed' for r in results)}),flush=True)
