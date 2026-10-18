"""One diagnostic repack of each first saved return assignment, never a quality pilot.

Four cases, seed zero, serial physical CCD0 CPU8. Restore the exact original
model/container/polygons, then at most six ten-second rounds: saved positions
first, followed by five full random restarts. Stop at the first separator-clear
snapshot. Retain every round; independent geometry still decides feasibility.
"""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import argparse,json,os,shutil,subprocess,time,traceback,zipfile
import psutil
import h5_return_frame_pilot as prior
ROOT=prior.ROOT;PROBE=ROOT/'output/h5-assignment-repack-20261018'
load,write,digest=prior.load,prior.write,prior.digest

def guards():
    prep=load(PROBE/'preparation.json')
    paths=[Path(__file__),PROBE/'preparation.json',PROBE/'build.json',PROBE/'assignment-repack.exe',
        PROBE/'restore-checks/checks.json',prior.CLI,ROOT/'output/audit_h5_assignment_repack.py']
    paths += [PROBE/'inputs'/r['input'] for r in prep['selection']]
    paths += [ROOT/'benchmarks/results/h5-return-capacity-diagnosis-20261017'/r['archive'] for r in prep['selection']]
    environment={key:os.environ.get(key) for key in prior.OVERRIDES};assert all(v is None for v in environment.values())
    return {'production':prior.source_digest(),'diagnostic_source':prior.tree_hash(PROBE/'workspace'),
        'original_candidate':prior.tree_hash(Path(prep['old_source'])),'environment':environment,
        'files':{p.relative_to(ROOT).as_posix():digest(p) for p in paths}}

def prepare(out):
    assert load(PROBE/'build.json')['all_passed'] and load(PROBE/'restore-checks/checks.json')['all_checks_pass']
    out.mkdir(exist_ok=False)
    write(out/'plan.json',{'scope':__doc__,'selection':load(PROBE/'preparation.json')['selection'],
        'seed':0,'max_seconds_each':60,'max_rounds':6,'round_limit_seconds':10,'cpu':8,'serial':True,
        'session_limit_seconds':600,'guards':guards(),'new_searches_planned':4,
        'interpretation':'A geometrically valid result is a witness for that fixed source assignment only. Failure cannot prove impossibility; neither result closes H5 or changes its original material/quality limits.',
        'production_changed':False,'held_out_geometry_read':False,'H5_complete':False})
    shutil.copyfile(__file__,out/'runner.py')

def run(out):
    psutil.Process().cpu_affinity(list(range(16,32)))
    plan=load(out/'plan.json');assert guards()==plan['guards']
    assert subprocess.check_output(['git','show','HEAD:'+(out/'plan.json').relative_to(ROOT).as_posix()],cwd=ROOT)==(out/'plan.json').read_bytes(),'Commit the plan before measuring'
    for p in psutil.process_iter(['pid','name']):
        assert (p.info['name'] or '').lower() not in ['assignment-repack.exe','exchange-diagnosis.exe','candidate-observer.exe','baseline-observer.exe'],'Another measured search is running'
    with (out/'opened.json').open('x',encoding='utf-8',newline='\n') as f:
        json.dump({'pid':os.getpid(),'utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':digest(out/'plan.json'),'search_cpu_affinity':[8],'controller_and_packaging_affinity':list(range(16,32))},f,indent=2)
    work=PROBE/'measurements';work.mkdir();records=[];started=time.perf_counter()
    try:
        for row in plan['selection']:
            assert guards()==plan['guards'] and time.perf_counter()-started<plan['session_limit_seconds']
            name=Path(row['input']).stem;case=work/name;case.mkdir()
            shutil.copyfile(PROBE/'inputs'/row['input'],case/'input.json')
            command=[str(PROBE/'assignment-repack.exe'),str(case/'input.json'),str(case/'output.json'),'60','0']
            begin=time.perf_counter();timeout=False
            with (case/'stdout.log').open('xb') as stdout,(case/'stderr.log').open('xb') as stderr:
                psutil.Process().cpu_affinity([8]);assert psutil.Process().cpu_affinity()==[8]
                proc=subprocess.Popen(command,cwd=ROOT,stdout=stdout,stderr=stderr)
                try:code=proc.wait(timeout=90)
                except subprocess.TimeoutExpired:
                    timeout=True;proc.kill();code=proc.wait()
                finally:psutil.Process().cpu_affinity(list(range(16,32)))
            result=load(case/'output.json') if (case/'output.json').exists() else None
            record={**row,'command':command,'exit_code':code,'timed_out':timeout,'wall_seconds':time.perf_counter()-begin,
                'output_written':result is not None,'separator_clear_snapshot_found':result.get('separator_clear_snapshot_found') if result else None,
                'rounds':len(result['rounds']) if result else 0,'independent_validation_pending':True}
            write(case/'record.json',record)
            members={p.name:{'sha256':digest(p),'bytes':p.stat().st_size} for p in case.iterdir() if p.is_file()}
            archive=out/(name+'.zip')
            # Compression is evidence packaging outside the timed search.
            with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
                for member in members:z.write(case/member,member)
            with zipfile.ZipFile(archive) as z:
                assert z.testzip() is None
                for member,expected in members.items():
                    data=z.read(member);assert len(data)==expected['bytes'] and sha256(data).hexdigest()==expected['sha256']
            record.update(archive=archive.name,archive_sha256=digest(archive),members=members)
            records.append(record);write(out/'records.json',records)
            print(json.dumps({k:record[k] for k in ['job','kerf_mm','exit_code','rounds','separator_clear_snapshot_found','wall_seconds']}),flush=True)
        assert guards()==plan['guards']
        write(out/'results.json',{'records':records,'guards_unchanged':True,'wall_seconds':time.perf_counter()-started,
            'all_four_completed':len(records)==4 and all(r['exit_code']==0 and r['output_written'] for r in records),
            'independent_validation_pending':True,'quality_claim':False,'H5_complete':False})
    except BaseException:
        write(out/'interruption.json',{'error':traceback.format_exc(),'records':records,'wall_seconds':time.perf_counter()-started});raise

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','run']);p.add_argument('--out',required=True,type=Path)
    args=p.parse_args();out=args.out.resolve();assert out.parent==ROOT/'benchmarks/results'
    (prepare if args.action=='prepare' else run)(out)
