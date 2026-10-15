"""Bounded Anode-only H5 Deepnest comparison: original parts, spacing zero, SVG export.

Run one batch per physical CCD0 core, no more than three cases per Anode job.
All failures, native candidates, inputs and outputs are archived. No uploads.
"""
import argparse
from copy import deepcopy
from datetime import datetime,timezone
import json
import importlib.metadata
import os
from pathlib import Path
import subprocess
import time
import traceback
import zipfile

import psutil
from cutting_development_set import ROOT,FOLDER,digest,load_cases,write_json
from deepnest import checkout_check,SOURCES,CHECKOUT
from deepnest_io import prepare,layout
from h2_import_audit import source_digest
from h5_deepnest_svg import audit
from h6_material_cost import run

BINARY=ROOT/'target/release/nestbolt.exe'
EXTRA=['scripts/h5_deepnest_cost.py','scripts/h5_deepnest_svg.py',
       'scripts/cutting_development_set.py','scripts/h6_material_cost.py',
       'benchmarks/browser/deepnest-cut-export.mjs']


def guards():
    return {'product':source_digest(),'binary':digest(BINARY),'manifest':digest(FOLDER/'manifest.json'),
            'runner_sources':{n:digest(ROOT/n) for n in SOURCES+EXTRA},
            'export_service':digest(CHECKOUT/'build/ui/services/export.service.js')}


def case(row,job,args,work,evidence,settings):
    # Follow the existing comparator's after-import search pinning. Restricting
    # Electron startup and its control subprocesses to the solver core can stall
    # startup/cleanup. Setup uses CCD1; the controller pins its loaded process
    # tree to the selected CCD0 core before starting the timed solve.
    psutil.Process().cpu_affinity(list(range(16,32)))
    key=f"{row['id']}-s{args.seed}"
    folder=work/key;folder.mkdir()
    record={'job':row['id'],'original_job_sha256':row['sha256'],'seed':args.seed,
            'seconds':args.seconds,'cpu':args.cpu,'status':'failed','score':None}
    try:
        zero=deepcopy(job);zero['clearance']=0
        write_json(folder/'original-job.json',job);write_json(folder/'zero-spacing-job.json',zero)
        prepared=prepare(zero,settings,'y')
        assert prepared['config']['spacing']==0 and prepared['config']['mergeLines']
        write_json(folder/'request.json',{'seconds':args.seconds,'seed':args.seed,
                                         'prepared':prepared,'common_line_export':True})
        env={**os.environ,'NESTBENCH_CPU':str(args.cpu)}
        with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
            started=time.perf_counter()
            child=subprocess.Popen(['node','benchmarks/browser/deepnest.mjs',str(folder/'request.json')],
                                   cwd=ROOT,stdout=out,stderr=err,env=env,creationflags=subprocess.CREATE_NO_WINDOW)
            try:code=child.wait(timeout=args.seconds+210)
            except subprocess.TimeoutExpired:
                owned=psutil.Process(child.pid)
                descendants=owned.children(recursive=True)
                for process in reversed(descendants):
                    try:process.kill()
                    except psutil.NoSuchProcess:pass
                child.kill();child.wait(timeout=10)
                _,alive=psutil.wait_procs(descendants,timeout=10)
                assert not alive,'Owned native descendants did not exit after timeout'
                code='timeout'
            record['controller']={'exit_code':code,'elapsed_wall_seconds':time.perf_counter()-started}
        assert code==0,'Native controller failed or timed out'
        raw=json.loads((folder/'browser-result.json').read_text(encoding='utf-8'))
        record['native_status']=raw['status'];record['native_errors']=raw['errors'];record['candidates']=raw['candidates']
        if raw['status']!='completed' or raw['errors']:
            record['status']=raw['status'] if not raw['errors'] else 'failed'
            return record
        assert raw['last']['elapsed_ms']<=args.seconds*1000
        assert raw['worker_check']=={'workers':1,'seed':args.seed}
        assert raw['affinity']['cpu_index']==args.cpu and raw['affinity']['method']=='JOB_OBJECT_LIMIT_AFFINITY'
        assert len(raw['affinity_verification'])>=2 and all(p['affinity']==str(1<<args.cpu) for p in raw['affinity_verification'])
        assert raw['input_fidelity']['maximum_scaled_error']<=8
        write_json(folder/'layout.json',layout(prepared,raw['last']['native']))
        checked=run([BINARY,'validate','--job',folder/'zero-spacing-job.json','--layout',folder/'layout.json'],
                    folder,'validate',args.cpu,120)
        record['validation_process']=checked
        validation=json.loads((folder/'validate-stdout.json').read_text(encoding='utf-8'))
        record['validation']=validation
        psutil.Process().cpu_affinity([args.cpu])
        record['svg_audit']=audit(folder,prepared,raw)
        record['status']='valid' if checked['exit_code']==0 and validation['valid'] else 'invalid'
        if record['status']=='valid':record['score']=validation['metrics']['normalized_material']
        return record
    except Exception:
        record['error']=traceback.format_exc();record['score']=None
        return record
    finally:
        # Isolated browser profiles are temporary state, not geometry evidence.
        record['artifacts']={p.relative_to(folder).as_posix():digest(p) for p in sorted(folder.iterdir()) if p.is_file()}
        write_json(folder/'case.json',record)
        archive=evidence/(key+'.zip')
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
            for p in sorted(folder.iterdir()):
                if p.is_file():z.write(p,p.relative_to(folder).as_posix())
        record['archive']=archive.name;record['archive_sha256']=digest(archive)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',nargs='+',required=True)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--seconds',type=int,default=60)
    parser.add_argument('--cpu',type=int,required=True)
    parser.add_argument('--label',default='development')
    args=parser.parse_args()
    assert args.seed in [0,1,2] and args.cpu in [0,2,4,6,8,10,12,14]
    assert 0<args.seconds<=300 and len(set(args.jobs))==len(args.jobs) and len(args.jobs)*(args.seconds+400)<=27*60
    assert args.label.replace('-','').isalnum()
    psutil.Process().cpu_affinity(list(range(16,32)))
    config=checkout_check()
    selected=[(r,j) for r,j in load_cases() if r['id'] in args.jobs]
    assert len(selected)==len(args.jobs)
    settings={**config['settings']['expanded'],'rotations':4,'free_rotation_samples':4,'mergeLines':True,'timeRatio':.5}
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    name=f'h5-deepnest-{args.label}-{stamp}-cpu{args.cpu}'
    work=ROOT/'output'/name;work.mkdir()
    evidence=ROOT/'benchmarks/results'/name;evidence.mkdir()
    before=guards()
    record={'scope':__doc__,'started_at':stamp,'revision':config['revision'],'guards':before,
            'jobs':args.jobs,'seed':args.seed,'seconds':args.seconds,'cpu':args.cpu,'settings':settings,
            'setup_cpus':list(range(16,32)), 'search_affinity_stage':'after import, before timed solve',
            'python_dependencies':{n:importlib.metadata.version(n) for n in ['psutil','svgpathtools','shapely']},
            'held_out_geometry_read':False,'network_blocked':True,'no_dxf_conversion':True,
            'work_directory':work.relative_to(ROOT).as_posix(),'rows':[]}
    write_json(evidence/'plan.json',record)
    print(json.dumps({'folder':str(evidence),'cases':len(selected)}),flush=True)
    for row,job in selected:
        assert guards()==before,'Source changed during comparator batch'
        result=case(row,job,args,work,evidence,settings);record['rows'].append(result)
        write_json(evidence/'progress.json',record)
        print(json.dumps({k:result[k] for k in ['job','seed','status','score']}),flush=True)
    assert guards()==before,'Source changed during comparator batch'
    record['finished_at']=datetime.now(timezone.utc).isoformat();record['complete']=True
    record['valid']=sum(r['status']=='valid' for r in record['rows'])
    write_json(evidence/'results.json',record)
    print(json.dumps({'folder':str(evidence),'valid':record['valid'],'total':len(selected)}),flush=True)


if __name__=='__main__':main()
