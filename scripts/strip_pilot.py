"""Bounded native strip runs on set S (G3 strip parity): development seeds 0-2, or
the final seeds 1000-1004 with --phase final. One process, optionally pinned to a CPU."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import uuid

import psutil

from dataset_selection import check_seed, phase_cases

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=int, default=60)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--phase', choices=['development', 'final'], default='development')
    parser.add_argument('--cpu', type=int, help='pin the solver processes to this logical CPU')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--count', type=int, default=13)
    parser.add_argument('--binary', type=Path, default=ROOT/'target/release/nestbolt.exe')
    args = parser.parse_args()
    if not 1 <= args.seconds <= 300 or args.offset < 0 or not 1 <= args.count <= 13:
        parser.error('Use 1..300 seconds, nonnegative offset and 1..13 cases')
    try:
        check_seed(args.phase, args.seed)
    except ValueError as error:
        parser.error(str(error))
    manifest, cases = phase_cases(ROOT, 'S', args.phase)
    cases = cases[args.offset:args.offset+args.count]
    if not cases:
        parser.error('No development strip cases selected')
    binary = args.binary.resolve()
    binary_hash = digest(binary)
    sources = {p: digest(ROOT/p) for p in [
        'Cargo.toml', 'Cargo.lock', 'crates/core/Cargo.toml', 'crates/core/src/strip.rs',
        'crates/core/src/lib.rs', 'crates/cli/src/main.rs', 'crates/validator/src/job.rs',
        'crates/validator/src/lib.rs', 'scripts/strip_pilot.py']}
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    directory = ROOT/'output/strip-pilots'/stamp
    directory.mkdir(parents=True)
    rows = []
    env = dict(os.environ, RAYON_NUM_THREADS='1')
    for case in cases:
        job = ROOT/'benchmarks/datasets'/case['path']
        assert digest(job) == case['sha256']
        run_dir = directory/case['id']
        run_dir.mkdir()
        with (run_dir/'stdout.json').open('wb') as out, (run_dir/'stderr.jsonl').open('wb') as err:
            try:
                process = subprocess.Popen([str(binary), 'strip', '--job', str(job), '--output',
                    str(run_dir/'layout.json'), '--seconds', str(args.seconds), '--seed', str(args.seed)],
                    cwd=ROOT, env=env, stdout=out, stderr=err)
                if args.cpu is not None:
                    psutil.Process(process.pid).cpu_affinity([args.cpu])
                exit_code = process.wait(timeout=args.seconds+90)
                status = 'valid' if exit_code == 0 else 'failed'
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                status, exit_code = 'timeout', None
        result = json.loads((run_dir/'stdout.json').read_bytes()) if status == 'valid' else None
        if result is not None:
            assert result['validation']['valid'] and result['accepted_at_seconds'] <= args.seconds
            check = subprocess.run([str(binary), 'validate', '--job', str(job), '--layout',
                                    str(run_dir/'layout.json')], capture_output=True, check=True, cwd=ROOT)
            assert json.loads(check.stdout)['valid']
            (run_dir/'independent.json').write_bytes(check.stdout)
        row = {'job':case['id'], 'job_sha256':case['sha256'], 'seconds':args.seconds, 'seed':args.seed,
               'status':status, 'exit_code':exit_code, 'result':result,
               'directory':run_dir.relative_to(ROOT).as_posix(),
               'outputs':{p.name:digest(p) for p in run_dir.iterdir()}}
        rows.append(row)
        (directory/'progress.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8',newline='\n')
        print(json.dumps({'job':case['id'],'seed':args.seed,'status':status,
                          'strip_length':None if result is None else result['strip_length']}), flush=True)
    assert digest(binary) == binary_hash
    assert all(digest(ROOT/p) == checksum for p,checksum in sources.items())
    target = ROOT/'benchmarks/results'/f'strip-native-{stamp}.json'
    with target.open('x',encoding='utf-8',newline='\n') as f:
        json.dump({'scope':('Native strip development slice; explicit seed and timed budget. Not full G3 acceptance.'
                            if args.phase == 'development' else 'Native strip final-phase run (G3), one seed of five.'),
                   'phase':args.phase, 'seed':args.seed, 'cpu':args.cpu,
                   'manifest_sha256':digest(manifest), 'binary_sha256':binary_hash, 'sources':sources,
                   'rows':rows},f,indent=2)
        f.write('\n')
    print(target,flush=True)


if __name__ == '__main__':
    main()
