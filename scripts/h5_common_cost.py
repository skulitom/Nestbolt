"""Three-arm public-CLI common-line cost on the frozen H5/H6 development set.

Normal mode uses the same kerf spacing. Common-line arms disable part-in-hole
and differ only in the optional search bonus. Report cut savings and material
cost separately. This development measurement is not final held-out acceptance.
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


from h6_material_cost import run, equivalent, equivalent_common


def case(row, job, kerf, seed, arm, seconds, work, evidence, cpus):
    cpu=cpus.get()
    key=f"{row['id']}-k{kerf}-s{seed}-{arm}"
    folder=work/key; folder.mkdir()
    record={'job':row['id'],'job_sha256':row['sha256'],'kerf_mm':kerf,'seed':seed,
            'arm':arm,'seconds':seconds,'cpu':cpu,'status':'failed'}
    try:
        library,request=public_inputs(job,kerf,False)
        if arm=='normal': request.pop('common_line')
        else: request['common_line']['search_bonus']=arm=='bonus'
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
        if arm!='normal':
            delta=max(delta,equivalent_common(checked['common_line'],report['common_line']))
        record['material']=checked['metrics']['normalized_material']
        record['metrics']=checked['metrics']
        if arm!='normal':
            record['cut_without_common_mm']=sum(s['cut_length_without_common_mm'] for s in report['common_line'])
            record['cut_with_common_mm']=sum(s['cut_length_with_common_mm'] for s in report['common_line'])
            record['saved_fraction']=1-record['cut_with_common_mm']/record['cut_without_common_mm']
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
            arms={a:[r for r in subset if r['arm']==a and r['status']=='valid'] for a in ['normal','off','bonus']}
            pair={'job':job,'kerf_mm':kerf,'seeds':seeds,'complete':all(len(v)==len(seeds) for v in arms.values())}
            if pair['complete']:
                material={a:statistics.median(r['material'] for r in rows) for a,rows in arms.items()}
                pair.update(normal_material=material['normal'],off_material=material['off'],bonus_material=material['bonus'],
                    material_cost_percent=100*(material['bonus']/material['normal']-1),
                    off_saved_fraction=statistics.median(r['saved_fraction'] for r in arms['off']),
                    bonus_saved_fraction=statistics.median(r['saved_fraction'] for r in arms['bonus']))
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
    name=f'h5-common-{args.label}-{stamp}'
    work=ROOT/'output'/name; work.mkdir()
    evidence=ROOT/'benchmarks/results'/name; evidence.mkdir()
    (evidence/'runner.py').write_bytes(Path(__file__).read_bytes())
    guards={'product':source_digest(),'binary':digest(BINARY),
            'runner':digest(Path(__file__)),'dataset_script':digest(ROOT/'scripts/cutting_development_set.py'),'shared_runner':digest(ROOT/'scripts/h6_material_cost.py'),
            'manifest':digest(FOLDER/'manifest.json')}
    plan={'scope':__doc__,'started_at':stamp,'product_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'guards':guards,'jobs':[r['id'] for r,j in selected], 'kerfs_mm':[0.2,1.5],
          'seeds':args.seeds,'seconds':args.seconds,'cpus':args.cpus,
          'wall_timeout_seconds':args.seconds+180,'validation_timeout_seconds':180,
          'revalidation_numeric_absolute_tolerance':1e-9,
          'held_out_geometry_read':False,'work_directory':work.relative_to(ROOT).as_posix()}
    write_json(evidence/'plan.json',plan)
    print(json.dumps({'folder':str(evidence),'runs':len(selected)*2*3*len(args.seeds)}),flush=True)
    cpus=Queue()
    for cpu in args.cpus: cpus.put(cpu)
    rows=[]
    with ThreadPoolExecutor(max_workers=len(args.cpus)) as pool:
        futures=[pool.submit(case,row,job,kerf,seed,arm,args.seconds,work,evidence,cpus)
                 for row,job in selected for kerf in [0.2,1.5] for seed in args.seeds for arm in ['normal','off','bonus']]
        for future in as_completed(futures):
            row=future.result(); rows.append(row)
            write_json(evidence/'progress.json',rows)
            print(json.dumps({k:row[k] for k in ['job','kerf_mm','seed','arm','status']}),flush=True)
    assert guards=={'product':source_digest(),'binary':digest(BINARY),'runner':digest(Path(__file__)),
                    'dataset_script':digest(ROOT/'scripts/cutting_development_set.py'),'shared_runner':digest(ROOT/'scripts/h6_material_cost.py'),'manifest':digest(FOLDER/'manifest.json')}, 'Sources changed during measurement'
    rows.sort(key=lambda r:(r['job'],r['kerf_mm'],r['seed'],r['arm']))
    pairs=aggregate(rows)
    record={**plan,'finished_at':datetime.now(timezone.utc).isoformat(),'rows':rows,'pairs':pairs,
            'valid':sum(r['status']=='valid' for r in rows),'total':len(rows)}
    write_json(evidence/'results.json',record)
    lines=['# Common-line search development measurement', '',
           f"{record['valid']}/{record['total']} runs validated. {args.seconds:g} s wall budget, seeds {args.seeds}.",
           'Three arms: normal nesting at the kerf spacing, common-line bonus off, and common-line bonus on.',
           'Original frozen geometry, stock, rotations and quantities are unchanged. All raw outcomes are retained; failures are not scored.',
           '', '| Job | Kerf mm | Bonus off savings | Bonus on savings | Bonus material vs normal |',
           '| --- | ---: | ---: | ---: | ---: |']
    for pair in pairs:
        if pair['complete']:
            lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {100*pair['off_saved_fraction']:.3f}% | {100*pair['bonus_saved_fraction']:.3f}% | {pair['material_cost_percent']:+.3f}% |")
        else: lines.append(f"| {pair['job']} | {pair['kerf_mm']} | incomplete | incomplete | incomplete |")
    for kerf in [0.2,1.5]:
        available=[r for r in pairs if r['complete'] and r['kerf_mm']==kerf]
        if available:
            lines += ['', f"{kerf} mm: median savings {100*statistics.median(r['bonus_saved_fraction'] for r in available):.3f}%; median material cost {statistics.median(r['material_cost_percent'] for r in available):+.3f}%; worst material cost {max(r['material_cost_percent'] for r in available):+.3f}%. {len(available)} complete job pairs."]
    lines += ['', '[Full records and archived inputs/results](results.json)', '']
    (evidence/'README.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
    print(json.dumps({'folder':str(evidence),'valid':record['valid'],'total':record['total']}),flush=True)


if __name__=='__main__':
    main()
