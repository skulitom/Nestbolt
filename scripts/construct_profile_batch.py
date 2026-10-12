"""Bounded Windows development profiles; no acceptance-gate or equal-work claim."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
from queue import Queue
import subprocess
import sys
import uuid

from dataset_selection import development_cases

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def select_cases(root, include=(), exclude=()):
    cases = [case for group in ['B', 'M'] for case in development_cases(root, group)[1]]
    known = {case['id'] for case in cases}
    if (set(include) | set(exclude)) - known:
        raise ValueError('Choose frozen development B/M IDs; held-out and unknown IDs are forbidden')
    if set(include) & set(exclude):
        raise ValueError('A job cannot be included and excluded')
    selected = [case for case in cases if (not include or case['id'] in include) and case['id'] not in exclude]
    if not selected:
        raise ValueError('No development jobs selected')
    return selected


def audited_profile(root, profile_path, case, binary_hash):
    profile_path = profile_path.resolve(strict=True)
    if not profile_path.is_relative_to(root/'output/construct-profiles'):
        raise ValueError('Profile escaped the retained output folder')
    profile = json.loads(profile_path.read_bytes())
    if (profile['job'] != case['id'] or profile['job_sha256'] != case['sha256']
            or profile['binary_sha256'] != binary_hash or len(profile['runs']) != 1):
        raise ValueError('Profile provenance mismatch')
    run = profile['runs'][0]
    directory = profile_path.parent/'0'
    for name, expected in run['outputs'].items():
        if Path(name).name != name or digest(directory/name) != expected:
            raise ValueError('Profile output hash mismatch')
    result = None
    status = 'failed'
    if run['exit_code'] == 0:
        result = json.loads((directory/'stdout.json').read_bytes())
        if (not result['validation']['valid'] or not result['best']['complete']
                or result['best']['layout'] != json.loads((directory/'layout.json').read_bytes())):
            raise ValueError('Successful profile lacks a complete independently valid layout')
        status = 'valid'
    return {'status': status, 'profile_path': profile_path.relative_to(root).as_posix(),
            'profile_sha256': digest(profile_path), 'profile': profile, 'result': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--job', action='append', default=[])
    parser.add_argument('--exclude-job', action='append', default=[])
    parser.add_argument('--cpu', type=int, action='append', required=True)
    parser.add_argument('--passes', type=int, default=1024)
    parser.add_argument('--max-checks', type=int, default=80_000_000)
    parser.add_argument('--timeout-ms', type=int, default=60_000)
    args = parser.parse_args()
    if (os.name != 'nt' or not 1 <= len(args.cpu) <= 8 or len(set(args.cpu)) != len(args.cpu)
            or any(not 0 <= cpu < 64 for cpu in args.cpu)
            or not 1 <= args.passes <= 1024 or args.max_checks < 0
            or not 1 <= args.timeout_ms <= 60_000):
        parser.error('Windows; 1..8 distinct CPUs in0..63; passes1..1024; nonnegative work; deadline1..60000ms')
    try:
        cases = select_cases(ROOT, args.job, args.exclude_job)
    except ValueError as error:
        parser.error(str(error))
    binary = args.binary.resolve(strict=True)
    binary_hash = digest(binary)
    files = [ROOT/'Cargo.toml', ROOT/'Cargo.lock', Path(__file__), ROOT/'scripts/construct_profile.py',
             ROOT/'scripts/dataset_selection.py', ROOT/'benchmarks/datasets/academic.json',
             ROOT/'benchmarks/datasets/makers.json']
    for crate in ['core','validator','cli']:
        files += list((ROOT/'crates'/crate/'src').rglob('*.rs'))
        files.append(ROOT/'crates'/crate/'Cargo.toml')
    sources = {p.relative_to(ROOT).as_posix(): digest(p) for p in files}
    for case in cases:
        if digest(ROOT/'benchmarks/datasets'/case['path']) != case['sha256']:
            raise ValueError('Frozen input changed')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    directory = ROOT/'output/construct-profile-batches'/stamp
    directory.mkdir(parents=True)
    plan = {'scope':'Selected frozen development B/M jobs only. Fixed work with safety deadline; no gate.',
            'cases':cases, 'excluded':args.exclude_job, 'cpus':args.cpu, 'passes':args.passes,
            'max_checks':args.max_checks, 'timeout_ms':args.timeout_ms, 'seed':0,
            'binary_sha256':binary_hash, 'sources':sources}
    (directory/'plan.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(directory,flush=True)
    cpus = Queue()
    for cpu in args.cpu:
        cpus.put(cpu)

    def run(case):
        cpu = cpus.get()
        log = directory/(case['id']+'.log')
        command = [sys.executable, str(ROOT/'scripts/construct_profile.py'), '--binary', str(binary),
                   '--job', case['id'], '--cpu', str(cpu), '--passes', str(args.passes),
                   '--max-checks', str(args.max_checks), '--timeout-ms', str(args.timeout_ms), '--repeat','1']
        row = {'job':case['id'], 'job_sha256':case['sha256'], 'cpu':cpu, 'command':command}
        try:
            # Inner runner kills its native child after90s; this wrapper never
            # kills only the Python parent and leaves a solver behind.
            with log.open('wb') as stream:
                process = subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
            if process.returncode:
                raise ValueError(f'Profile harness exited {process.returncode}; see retained log')
            profile_path = Path(log.read_text().splitlines()[-1])/'profile.json'
            row.update(audited_profile(ROOT,profile_path,case,binary_hash))
            profile = row['profile']
            if (profile['passes'] != args.passes or profile['max_checks'] != args.max_checks
                    or profile['timeout_ms'] != args.timeout_ms
                    or profile['runs'][0]['cpu_mask'] != 1 << cpu):
                raise ValueError('Profile work controls or CPU differ from the declared plan')
        except Exception as error:
            row.update(status='harness_error',error=str(error))
        finally:
            cpus.put(cpu)
        row.update(log_path=log.relative_to(ROOT).as_posix(),log_sha256=digest(log))
        return row

    rows = []
    with ThreadPoolExecutor(max_workers=len(args.cpu)) as pool:
        futures = [pool.submit(run,case) for case in cases]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            with (directory/'progress.jsonl').open('a',encoding='utf-8',newline='\n') as stream:
                stream.write(json.dumps(row)+'\n')
            print(json.dumps({'completed':len(rows),'total':len(cases),'job':row['job'],'status':row['status']}),flush=True)
    if digest(binary) != binary_hash or any(digest(ROOT/p) != value for p,value in sources.items()):
        raise ValueError('Binary or source changed; retained progress is not a final result')
    target = ROOT/'benchmarks/results'/('search-development-'+stamp+'.json')
    result = dict(plan,rows=sorted(rows,key=lambda row:row['job']),
                  plan_path=(directory/'plan.json').relative_to(ROOT).as_posix())
    with target.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(result,stream,indent=2); stream.write('\n')
    print(target,flush=True)


if __name__ == '__main__':
    main()
