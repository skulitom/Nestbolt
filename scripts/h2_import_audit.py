"""Bounded native import diagnostics on the frozen training/robustness sets.

Held-out evaluation is intentionally not implemented here. This development
report is not H2 acceptance: exact cut-layer/warning and re-export fidelity
checks are separate requirements. Every rejection and timeout remains visible.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time
import psutil

ROOT=Path(__file__).resolve().parents[1]
CORPUS=ROOT/'benchmarks/datasets/shop'


def source_digest():
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','crates','web/src','Cargo.toml','Cargo.lock','scripts/h2_import_audit.py'],cwd=ROOT,text=True).splitlines()
    return sha256(b''.join(n.encode()+b'\0'+(ROOT/n).read_bytes() for n in sorted(set(names)))).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--baseline',action='store_true');parser.add_argument('--gap-checkpoint',action='store_true');parser.add_argument('--robustness',action='store_true');parser.add_argument('--only');args=parser.parse_args()
    manifest=json.loads((CORPUS/'manifest.json').read_text(encoding='utf-8'))
    label='robustness' if args.robustness else 'training-baseline' if args.baseline else 'training-gap-checkpoint' if args.gap_checkpoint else 'training'
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out=ROOT/'output'/f'h2-import-{label}-{stamp}';out.mkdir(parents=True,exist_ok=False)
    binary=ROOT/'target/release/nestbolt.exe';start_digest=source_digest()
    rows=[r for r in manifest['files'] if r['split']==('robustness' if args.robustness else 'training') and Path(r['path']).suffix.lower() in ['.svg','.dxf']]
    if args.only:rows=[r for r in rows if args.only in r['path']]
    assert rows and all(r['split']!='held_out' for r in rows)
    def run(index,row):
        assert sha256((CORPUS/row['path']).read_bytes()).hexdigest()==row['sha256']
        expected=json.loads((CORPUS/row['label']).read_text(encoding='utf-8')) if row.get('label') else None
        target=out/f'{index:03}.json';cmd=[str(binary),'import',str(CORPUS/row['path']),'--output',str(target)]
        options=expected.get('import_options',{}) if expected else {}
        if options.get('units')=='in':cmd+=['--dxf-unit-mm','25.4']
        unsupported=[]
        for key,flag in [('layers','--layers'),('colors','--colors'),('close_gaps_mm','--close-gaps')]:
            if key not in options:continue
            if args.baseline or (args.gap_checkpoint and key in ['layers','colors']):unsupported.append(key);continue
            value=options[key];cmd+=[flag,','.join(map(str,value)) if isinstance(value,list) else str(value)]
        # Start suspended on Windows: a fast import can exit before an after-
        # launch affinity call, and must never run briefly on the wrong core.
        if sys.platform!='win32':raise RuntimeError('This runner requires Windows for suspended, affinity-pinned process creation')
        begin=time.perf_counter();proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW|0x00000004)  # CREATE_SUSPENDED
        try:
            child=psutil.Process(proc.pid);child.cpu_affinity([2*(index%4)]);child.resume()
        except BaseException:
            proc.kill();proc.communicate();raise
        timed_out=False
        try:stdout,stderr=proc.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            timed_out=True;proc.kill();stdout,stderr=proc.communicate()
        elapsed=time.perf_counter()-begin
        result={'path':row['path'],'set':row['set'],'sha256':row['sha256'],'elapsed_s':elapsed,
            'status':'timeout' if timed_out else 'imported' if proc.returncode==0 else 'panic' if proc.returncode==101 or b'panicked at' in stderr else 'rejected',
            'exit_code':proc.returncode,'error':stderr.decode('utf-8',errors='replace')[-4000:],
            'baseline_unavailable_options':unsupported,'expected_negative_fixture':bool(expected and expected.get('negative_fixture'))}
        if proc.returncode==0:
            library=json.loads(target.read_text(encoding='utf-8'));parts=library['parts']
            result.update(parts=len(parts),holes=sorted(len(p['holes']) for p in parts),warnings=library['warnings'],imports=library.get('imports',[]))
            if expected:
                ep=expected['cut_parts'];result['expected_parts']=len(ep)
                result['part_and_hole_counts_match']=len(ep)==len(parts) and result['holes']==sorted(p['holes'] for p in ep)
        print(f'{index+1}/{len(rows)} {row["path"]}: {result["status"]} '+str(result.get('part_and_hole_counts_match','')),flush=True)
        return result
    # Work is partitioned across four fixed physical cores, so at most one
    # process occupies each core; builds use CCD1 separately.
    def batch(slot):return [run(i,r) for i,r in enumerate(rows) if i%4==slot]
    with ThreadPoolExecutor(max_workers=4) as pool:results=[r for group in pool.map(batch,range(4)) for r in group]
    results.sort(key=lambda r:r['path']);assert source_digest()==start_digest,'Product sources changed during import audit'
    summary={'label':label,'recorded_at':stamp,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'binary_sha256':sha256(binary.read_bytes()).hexdigest(),'source_sha256':start_digest,
        'manifest_sha256':sha256((CORPUS/'manifest.json').read_bytes()).hexdigest(),
        'held_out_read':False,'H2':False,'counts':dict(Counter(r['status'] for r in results)),
        'part_and_hole_count_matches':sum(r.get('part_and_hole_counts_match',False) for r in results),
        'scope':'Development count diagnostics only; not cut-layer, warning, actionable-failure or fidelity acceptance.',
        'files':results}
    path=ROOT/'benchmarks/results'/f'h2-import-{label}-{stamp}.json'
    path.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'report':str(path),'counts':summary['counts'],'part_and_hole_count_matches':summary['part_and_hole_count_matches']}))


if __name__=='__main__':main()
