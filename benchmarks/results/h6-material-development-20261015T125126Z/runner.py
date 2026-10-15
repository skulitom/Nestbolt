"""Paired public-CLI allowance cost on the frozen H5/H6 development set.

Both arms use common-line mode, with its search bonus off, at the same kerf.
Only the lead setting differs. All outcomes, flags and raw files are retained;
failures receive no material score. This is not final acceptance or H5 savings.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
from queue import Queue
import statistics
import subprocess
import time
import traceback
import zipfile

import psutil
from cutting_development_set import ROOT, FOLDER, digest, load_cases, public_inputs, write_json
from h2_import_audit import source_digest

BINARY=ROOT/'target/release/nestbolt.exe'


def equivalent(a, b, path='report'):
    """JSON round-tripping can change f64 sums at the last decimal place.

    Require identical structure/discrete values and <=1e-9 absolute difference
    for floats, far below the geometry gate. Return the largest difference.
    """
    if isinstance(a,dict):
        assert isinstance(b,dict) and a.keys()==b.keys(), path
        return max((equivalent(a[k],b[k],path+'.'+k) for k in a),default=0)
    if isinstance(a,list):
        assert isinstance(b,list) and len(a)==len(b), path
        return max((equivalent(x,y,f'{path}[{i}]') for i,(x,y) in enumerate(zip(a,b))),default=0)
    if isinstance(a,float):
        assert isinstance(b,(int,float)) and math.isfinite(a) and math.isfinite(b),path
        difference=abs(a-b)
        assert difference<=1e-9,(path,a,b)
        return difference
    assert a==b,(path,a,b)
    return 0


def run(command, folder, name, cpu, timeout):
    started=time.perf_counter()
    with (folder/(name+'-stdout.json')).open('wb') as out, (folder/(name+'-stderr.log')).open('wb') as err:
        process=subprocess.Popen(list(map(str,command)),cwd=ROOT,stdout=out,stderr=err,
                                 creationflags=subprocess.CREATE_NO_WINDOW | 4)
        try:
            child=psutil.Process(process.pid)
            child.cpu_affinity([cpu])
            child.resume()
            code=process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait(); code='timeout'
        except BaseException:
            process.kill(); process.wait(); raise
    return {'command':list(map(str,command)), 'exit_code':code,
            'elapsed_wall_seconds':time.perf_counter()-started, 'cpu':cpu}


def case(row, job, kerf, seed, leads, seconds, work, evidence, cpus):
    cpu=cpus.get()
    arm='leads' if leads else 'baseline'
    key=f"{row['id']}-k{kerf}-s{seed}-{arm}"
    folder=work/key; folder.mkdir()
    record={'job':row['id'],'job_sha256':row['sha256'],'kerf_mm':kerf,'seed':seed,
            'arm':arm,'seconds':seconds,'cpu':cpu,'status':'failed'}
    try:
        library,request=public_inputs(job,kerf,leads)
        write_json(folder/'library.json',library); write_json(folder/'request.json',request)
        command=[BINARY,'nest','--library',folder/'library.json','--request',folder/'request.json',
                 '--out-dir',folder/'nested','--seconds',seconds,'--seed',seed]
        outcome=run(command,folder,'nest',cpu,seconds+180)
        record['nest']=outcome
        if outcome['exit_code']!=0:
            return record
        report=json.loads((folder/'nested/report.json').read_text(encoding='utf-8'))
        derived=json.loads((folder/'nested/job.json').read_text(encoding='utf-8'))
        expected=deepcopy(job); expected['clearance']=kerf
        assert derived==expected, 'Public conversion changed original job beyond requested kerf'
        params=['--library',folder/'library.json','--request',folder/'request.json','--layout',folder/'nested/layout.json']
        validation=run([BINARY,'validate',*params],folder,'validate',cpu,180)
        record['revalidation']=validation
        assert validation['exit_code']==0, 'Fresh validation failed or timed out'
        checked=json.loads((folder/'validate-stdout.json').read_text(encoding='utf-8'))
        assert report['validation']['valid'] and checked['valid']
        delta=equivalent(checked['metrics'],report['validation']['metrics'],'metrics')
        delta=max(delta,equivalent(checked['common_line'],report['common_line'],'common_line'))
        record['material']=checked['metrics']['normalized_material']
        record['metrics']=checked['metrics']
        record['cut_without_common_mm']=sum(s['cut_length_without_common_mm'] for s in report['common_line'])
        record['cut_with_common_mm']=sum(s['cut_length_with_common_mm'] for s in report['common_line'])
        if leads:
            plan=checked['lead_in']
            delta=max(delta,equivalent(plan,report['lead_in'],'lead_in'))
            assert plan['validation']['valid'] and plan['validation']['source_checked']
            assert plan['expected_contours']==plan['reserved_contours']+plan['flagged_contours']
            record['coverage']={k:plan[k] for k in ['expected_contours','reserved_contours','flagged_contours']}
        record['maximum_revalidation_roundtrip_difference']=delta
        record['status']='valid'
        return record
    except Exception:
        record['error']=traceback.format_exc()
        record.pop('material',None)
        return record
    finally:
        record['artifacts']={p.relative_to(folder).as_posix():digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}
        write_json(folder/'case.json',record)
        archive=evidence/(key+'.zip')
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as target:
            for path in sorted(folder.rglob('*')):
                if path.is_file(): target.write(path,path.relative_to(folder).as_posix())
        record['archive']=archive.name; record['archive_sha256']=digest(archive)
        cpus.put(cpu)


def aggregate(rows):
    pairs=[]
    for job in sorted({r['job'] for r in rows}):
        for kerf in sorted({r['kerf_mm'] for r in rows}):
            subset=[r for r in rows if r['job']==job and r['kerf_mm']==kerf]
            seeds=sorted({r['seed'] for r in subset})
            baseline=[r for r in subset if r['arm']=='baseline' and r['status']=='valid']
            leads=[r for r in subset if r['arm']=='leads' and r['status']=='valid']
            pair={'job':job,'kerf_mm':kerf,'seeds':seeds,'complete':len(baseline)==len(leads)==len(seeds)}
            if pair['complete']:
                base=statistics.median(r['material'] for r in baseline)
                with_leads=statistics.median(r['material'] for r in leads)
                pair.update(baseline_median=base,leads_median=with_leads,
                            material_cost_percent=100*(with_leads/base-1),
                            maximum_flagged_contours=max(r['coverage']['flagged_contours'] for r in leads),
                            minimum_reserved_contours=min(r['coverage']['reserved_contours'] for r in leads),
                            expected_contours=leads[0]['coverage']['expected_contours'])
            pairs.append(pair)
    return pairs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=float,default=60)
    parser.add_argument('--seeds',type=int,nargs='+',default=[0,1,2])
    parser.add_argument('--jobs',nargs='+')
    parser.add_argument('--cpus',type=int,nargs='+',default=[0,2,4,6,8,10,12,14])
    parser.add_argument('--label',default='development')
    args=parser.parse_args()
    assert 0<args.seconds<=300 and set(args.seeds)<={0,1,2} and len(set(args.seeds))==len(args.seeds)
    assert 1<=len(args.cpus)<=8 and len(set(args.cpus))==len(args.cpus) and set(args.cpus)<={0,2,4,6,8,10,12,14}
    assert args.label.replace('-','').isalnum()
    candidates=load_cases()
    assert not args.jobs or set(args.jobs)<={r['id'] for r,j in candidates}
    selected=[(r,j) for r,j in candidates if not args.jobs or r['id'] in args.jobs]
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    name=f'h6-material-{args.label}-{stamp}'
    work=ROOT/'output'/name; work.mkdir()
    evidence=ROOT/'benchmarks/results'/name; evidence.mkdir()
    (evidence/'runner.py').write_bytes(Path(__file__).read_bytes())
    guards={'product':source_digest(),'binary':digest(BINARY),
            'runner':digest(Path(__file__)),'dataset_script':digest(ROOT/'scripts/cutting_development_set.py'),
            'manifest':digest(FOLDER/'manifest.json')}
    plan={'scope':__doc__,'started_at':stamp,'product_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'guards':guards,'jobs':[r['id'] for r,j in selected], 'kerfs_mm':[0.2,1.5],
          'seeds':args.seeds,'seconds':args.seconds,'cpus':args.cpus,
          'wall_timeout_seconds':args.seconds+180,'validation_timeout_seconds':180,
          'revalidation_numeric_absolute_tolerance':1e-9,
          'held_out_geometry_read':False,'work_directory':work.relative_to(ROOT).as_posix()}
    write_json(evidence/'plan.json',plan)
    print(json.dumps({'folder':str(evidence),'runs':len(selected)*2*2*len(args.seeds)}),flush=True)
    cpus=Queue()
    for cpu in args.cpus: cpus.put(cpu)
    rows=[]
    with ThreadPoolExecutor(max_workers=len(args.cpus)) as pool:
        futures=[pool.submit(case,row,job,kerf,seed,leads,args.seconds,work,evidence,cpus)
                 for row,job in selected for kerf in [0.2,1.5] for seed in args.seeds for leads in [False,True]]
        for future in as_completed(futures):
            row=future.result(); rows.append(row)
            write_json(evidence/'progress.json',rows)
            print(json.dumps({k:row[k] for k in ['job','kerf_mm','seed','arm','status']}),flush=True)
    assert guards=={'product':source_digest(),'binary':digest(BINARY),'runner':digest(Path(__file__)),
                    'dataset_script':digest(ROOT/'scripts/cutting_development_set.py'),'manifest':digest(FOLDER/'manifest.json')}, 'Sources changed during measurement'
    rows.sort(key=lambda r:(r['job'],r['kerf_mm'],r['seed'],r['arm']))
    pairs=aggregate(rows)
    record={**plan,'finished_at':datetime.now(timezone.utc).isoformat(),'rows':rows,'pairs':pairs,
            'valid':sum(r['status']=='valid' for r in rows),'total':len(rows)}
    write_json(evidence/'results.json',record)
    lines=['# Lead allowance material cost', '',
           f"{record['valid']}/{record['total']} runs validated. {args.seconds:g} s wall budget, seeds {args.seeds}.",
           'Both arms use common-line mode at the same kerf, bonus off. Leads use default line / 3 mm / 45° outer / 90° hole.',
           'Geometry is the frozen polygon job, represented as exact line contours. Material includes lead extents. Flags remain unresolved and are never hidden.',
           'Every pair uses the ratio of the two seed medians. Incomplete pairs are not scored. This development result does not change published v1 claims.', '',
           '| Job | Kerf mm | Baseline material | Lead material | Cost | Flagged / expected (max) |',
           '| --- | ---: | ---: | ---: | ---: | ---: |']
    for pair in pairs:
        if pair['complete']:
            lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {pair['baseline_median']:.6f} | {pair['leads_median']:.6f} | {pair['material_cost_percent']:+.3f}% | {pair['maximum_flagged_contours']}/{pair['expected_contours']} |")
        else:
            lines.append(f"| {pair['job']} | {pair['kerf_mm']} | failed/incomplete | — | — | — |")
    for kerf in [0.2,1.5]:
        available=[r['material_cost_percent'] for r in pairs if r['complete'] and r['kerf_mm']==kerf]
        if available:
            lines += ['',f'{kerf} mm kerf: median measured cost {statistics.median(available):+.3f}% across {len(available)} complete job pairs.']
    lines += ['', '[Full records and archived raw inputs/results](results.json)', '']
    (evidence/'README.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    print(json.dumps({'folder':str(evidence),'valid':record['valid'],'total':record['total']}),flush=True)


if __name__=='__main__':
    main()
