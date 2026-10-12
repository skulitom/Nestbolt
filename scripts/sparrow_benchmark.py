"""Pinned current Sparrow, one worker, strict candidate deadline, original-job validation."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import uuid

from benchmark_io import UnsupportedJob
from sparrow_io import prepare, layout, strip_length
from svgnest import guard_held_out

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'benchmarks/sparrow-benchmark/Cargo.toml'
TARGET=ROOT/'.cache/build/sparrow-benchmark'
BINARY=TARGET/'release'/('nestbolt-sparrow-benchmark.exe' if os.name=='nt' else 'nestbolt-sparrow-benchmark')
BUILD=TARGET/'build.json'
SOURCES=['scripts/sparrow_benchmark.py','scripts/sparrow_io.py','scripts/benchmark_io.py','scripts/svgnest.py',
         'scripts/svgnest_io.py','scripts/svg_export_transform.py',
         'benchmarks/sparrow-benchmark/Cargo.toml','benchmarks/sparrow-benchmark/Cargo.lock',
         'benchmarks/sparrow-benchmark/src/main.rs','scripts/dataset_selection.py',
         'scripts/comparison_cases.py','scripts/matrix_plan.py','benchmarks/matrix-plan.json']


def digest(path): return sha256(path.read_bytes()).hexdigest()


def command(args): return subprocess.check_output(args,cwd=ROOT,text=True,encoding='utf-8').strip()


def write(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f: f.write(json.dumps(value,indent=2,allow_nan=False)+'\n')


def build():
    env={**os.environ,'CARGO_BUILD_JOBS':'4','CARGO_TARGET_DIR':str(TARGET),'RUSTFLAGS':''}
    subprocess.run(['cargo','+1.98.1','build','--release','--locked','--manifest-path',str(MANIFEST)],cwd=ROOT,env=env,check=True)
    record={'built_at':datetime.now(timezone.utc).isoformat(),'compiler':command(['rustc','+1.98.1','-vV']),
            'binary_sha256':digest(BINARY),'rustflags':'','sources':{s:digest(ROOT/s) for s in SOURCES if s.startswith('benchmarks/')}}
    BUILD.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Built pinned Sparrow benchmark wrapper.')


def run(args):
    built=json.loads(BUILD.read_bytes())
    if digest(BINARY)!=built['binary_sha256'] or any(digest(ROOT/s)!=h for s,h in built['sources'].items()):
        raise ValueError('Sparrow build cache changed; run build explicitly')
    source=Path(args.job).resolve();job=json.loads(source.read_bytes())
    guard_held_out(job,args.phase)
    identifier=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    dest=ROOT/'output/sparrow-benchmark'/identifier;dest.mkdir(parents=True)
    (dest/'job.json').write_bytes(source.read_bytes())
    record={'run_id':identifier,'tool':'sparrow','revision':'4629b22795ae6b25b3b460ccde6fb36a71292b6d',
            'job':job['name'],'job_sha256':digest(dest/'job.json'),'seed':args.seed,'seconds':args.seconds,
            'axis':args.axis,'settings':args.settings,'settings_finalized':False,'phase':args.phase,
            'build':built,'workers':1,'rayon_threads':1,'score':None,'metrics':None,
            'sources':{s:digest(ROOT/s) for s in SOURCES},'commit':command(['git','rev-parse','HEAD']),
            'dirty':bool(command(['git','status','--porcelain'])),'platform':platform.platform(),
            'cpu':command(['powershell.exe','-NoProfile','-NonInteractive','-Command','(Get-CimInstance Win32_Processor).Name']) if os.name=='nt' else platform.processor(),
            'started_at':datetime.now(timezone.utc).isoformat()}
    try:
        prepared=prepare(job,args.axis);write(dest/'request.json',prepared);write(dest/'input.json',prepared['input'])
        snapshot=getattr(args,'validator_snapshot',None)
        if snapshot:
            validator=ROOT/snapshot['path']
            if digest(validator)!=snapshot['sha256']: raise ValueError('Batch validator binary changed')
        else:
            subprocess.run(['cargo','build','--locked','-p','nestbolt-cli'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
            validator=ROOT/'target/debug'/('nestbolt.exe' if os.name=='nt' else 'nestbolt')
        record['validator_sha256']=digest(validator)
        record['validator_sources']=snapshot['sources'] if snapshot else {p.relative_to(ROOT).as_posix():digest(p) for p in [ROOT/'Cargo.lock',*sorted((ROOT/'crates/validator/src').glob('*.rs'))]}
        write(dest/'empty-layout.json',{'version':1,'units':job['units'],'sheets':[],'placements':[]})
        probe=subprocess.run([str(validator),'validate','--job',str(dest/'job.json'),'--layout',str(dest/'empty-layout.json')],capture_output=True,timeout=60)
        if any(v['code']!='quantity' for v in json.loads(probe.stdout)['violations']): raise ValueError('Invalid original job contract')
        record['command']=[str(BINARY),str(dest/'input.json'),str(args.seconds),str(args.seed),args.settings]
        started=time.monotonic()
        with (dest/'stdout.log').open('wb') as out,(dest/'stderr.log').open('wb') as err:
            process=subprocess.run(record['command'],cwd=dest,env={**os.environ,'RAYON_NUM_THREADS':'1'},stdout=out,stderr=err,timeout=args.seconds+30)
        record['solver_exit_code']=process.returncode;record['solver_wall_seconds']=time.monotonic()-started
        if process.returncode: raise ValueError('Sparrow failed; see retained stderr.log')
        raw=json.loads((dest/'solver-result.json').read_bytes());record['native_summary']={k:v for k,v in raw.items() if k!='solution'}
        if raw['status']!='completed': record['status']='no_layout'
        elif raw['error']: raise ValueError(raw['error'])
        else:
            if raw['accepted_at_seconds']>args.seconds or raw['workers']!=1 or raw['seed']!=args.seed: raise ValueError('Native deadline/worker/seed differs')
            common=layout(job,prepared,raw);write(dest/'layout.json',common)
            checked=subprocess.run([str(validator),'validate','--job',str(dest/'job.json'),'--layout',str(dest/'layout.json')],capture_output=True,timeout=120)
            (dest/'validation.json').write_bytes(checked.stdout)
            report=json.loads(checked.stdout);record['validator_exit_code']=checked.returncode
            record['status']='valid' if report['valid'] and checked.returncode==0 else 'invalid'
            if record['status']=='valid':
                record['metrics']=report['metrics']
                record['score_kind']='strip_length' if args.axis=='x' and job['name'].startswith('s-') else 'normalized_material'
                record['score']=strip_length(job,common) if record['score_kind']=='strip_length' else report['metrics']['normalized_material']
    except UnsupportedJob as error: record.update(status='unsupported',reason=str(error))
    except subprocess.TimeoutExpired as error: record.update(status='timeout',reason=f'Process exceeded {error.timeout}s')
    except Exception as error: record.update(status='failed',reason=str(error))
    record['finished_at']=datetime.now(timezone.utc).isoformat()
    record['outputs']={p.name:digest(p) for p in sorted(dest.iterdir()) if p.is_file()}
    write(dest/'run.json',record)
    path=(dest/'run.json').relative_to(ROOT).as_posix()
    with (ROOT/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:
        f.write(f'\n- {record["finished_at"]} | current Sparrow `{job["name"]}` seed {args.seed}, {args.seconds}s, {args.settings}, axis {args.axis} | {record["status"]} | score {record["score"]} | [record]({path}). Provisional single-strip comparison; deadline includes construction.\n')
    print(json.dumps({'status':record['status'],'score':record['score'],'record':path,'reason':record.get('reason')}),flush=True)
    return record


def batch(args):
    from comparison_cases import comparison_cases
    if args.dataset=='M':
        from maker_freeze import check_frozen, DEST
    else:
        from datasets import check_frozen, DEST
    check_frozen()
    from dataset_selection import check_seed
    check_seed(args.phase,args.seed)
    DATASET,rows=comparison_cases(ROOT,args.dataset,args.seconds,args.phase)
    selected=rows[args.offset:args.offset+args.count]
    if not selected or len(selected)*(args.seconds+300)>3*3600: raise ValueError('Empty selection or batch over three hours')
    sources={s:digest(ROOT/s) for s in SOURCES}
    identifier=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    dest=ROOT/'output/sparrow-batches'/identifier;dest.mkdir(parents=True)
    subprocess.run(['cargo','build','--locked','-p','nestbolt-cli'],cwd=ROOT,check=True)
    validator=ROOT/'target/debug'/('nestbolt.exe' if os.name=='nt' else 'nestbolt')
    frozen=dest/validator.name
    shutil.copy2(validator,frozen)
    validator_snapshot={'path':frozen.relative_to(ROOT).as_posix(),'sha256':digest(frozen),
        'sources':{p.relative_to(ROOT).as_posix():digest(p) for p in [ROOT/'Cargo.lock',*sorted((ROOT/'crates/validator/src').glob('*.rs'))]}}
    record={'batch_id':identifier,'dataset':args.dataset,'dataset_manifest_sha256':digest(DATASET),'cases':selected,
            'sources':sources,'seconds':args.seconds,'seed':args.seed,'settings':args.settings,'axis':args.axis,
            'phase':args.phase,'complete':False,'runs':[],'validator_snapshot':validator_snapshot}
    write(dest/'start.json',record)
    for row in selected:
        if {s:digest(ROOT/s) for s in SOURCES}!=sources: raise ValueError('Runner changed during batch')
        source=DEST/row['path']
        if digest(source)!=row['sha256']: raise ValueError('Frozen source changed')
        result=run(argparse.Namespace(job=source,seconds=args.seconds,seed=args.seed,settings=args.settings,axis=args.axis,phase=args.phase,validator_snapshot=validator_snapshot))
        path=ROOT/'output/sparrow-benchmark'/result['run_id']/'run.json'
        entry={'job':row['id'],'status':result['status'],'record':path.relative_to(ROOT).as_posix(),'sha256':digest(path)}
        record['runs'].append(entry)
        with (dest/'runs.jsonl').open('a',encoding='utf-8',newline='\n') as f: f.write(json.dumps(entry)+'\n')
    record['complete']=True;record['valid_runs']=sum(r['status']=='valid' for r in record['runs'])
    write(dest/'batch.json',record)
    print(f'Batch finished: {record["valid_runs"]}/{len(selected)} valid; {dest / "batch.json"}',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);subs=parser.add_subparsers(dest='command',required=True)
    subs.add_parser('build');running=subs.add_parser('run');batching=subs.add_parser('batch')
    for sub in [running,batching]:
        sub.add_argument('--seconds',type=int,default=60);sub.add_argument('--seed',type=int,default=0)
        sub.add_argument('--settings',choices=['identical','upstream-default'],default='identical');sub.add_argument('--axis',choices=['x','y'],default='x')
    running.add_argument('--job',required=True);running.add_argument('--phase',choices=['development','final'],default='development')
    batching.add_argument('--dataset',choices=['S','B','M'],default='S');batching.add_argument('--offset',type=int,default=0);batching.add_argument('--count',type=int,default=13)
    batching.add_argument('--phase',choices=['development','final'],default='development',help='final: seeds 1000-1004 and the held-out jobs (acceptance run only)')
    args=parser.parse_args()
    if args.command=='build': build()
    else:
        if not 1<=args.seconds<=300 or not 0<=args.seed<2**64: parser.error('Budget 1..300, seed unsigned 64-bit')
        if args.command=='batch':
            if args.offset<0 or not 1<=args.count<=35: parser.error('Offset nonnegative, count 1..35')
            batch(args)
        else:
            result=run(args);sys.exit(0 if result['status'] in ['valid','unsupported'] else 1)
