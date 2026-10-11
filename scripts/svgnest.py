"""Bounded SVGnest runs with immutable provenance and independent validation."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import uuid

from benchmark_io import UnsupportedJob
from svgnest_io import prepare, layout

ROOT = Path(__file__).resolve().parents[1]
CHECKOUT = ROOT / '.cache/upstream/svgnest'
CONFIG = ROOT / 'benchmarks/svgnest/tool.json'
PACKAGE = ROOT / 'benchmarks/browser'
SOURCE_FILES = ['scripts/svgnest.py', 'scripts/svgnest_io.py', 'scripts/benchmark_io.py',
                'benchmarks/browser/svgnest.mjs', 'benchmarks/browser/cpu-limit.mjs',
                'benchmarks/browser/cpu-job.ps1', 'benchmarks/browser/package.json',
                'benchmarks/browser/package-lock.json', 'benchmarks/svgnest/tool.json']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def command(args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, text=True, encoding='utf-8').strip()


def write(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as file:
        json.dump(value, file, indent=2, allow_nan=False)
        file.write('\n')


def checkout_check():
    config = json.loads(CONFIG.read_bytes())
    if command(['git', 'rev-parse', 'HEAD'], CHECKOUT) != config['revision']:
        raise ValueError('SVGnest checkout differs from the pinned revision')
    if command(['git', 'status', '--porcelain', '--untracked-files=no'], CHECKOUT):
        raise ValueError('SVGnest checkout has tracked changes')
    return config


def setup():
    config = json.loads(CONFIG.read_bytes())
    if not CHECKOUT.exists():
        CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', '--no-checkout', '--filter=blob:none', config['repository'], str(CHECKOUT)], check=True)
        subprocess.run(['git', '-C', str(CHECKOUT), 'checkout', '--detach', config['revision']], check=True)
    checkout_check()
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    subprocess.run([npm, 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=PACKAGE, check=True)
    subprocess.run(['node', 'node_modules/playwright/cli.js', 'install', 'chromium'], cwd=PACKAGE, check=True)
    print('Prepared pinned SVGnest and Chromium.')


def guard_held_out(job, phase):
    manifest = json.loads((ROOT / 'benchmarks/datasets/makers.json').read_bytes())
    if job['name'] in manifest['held_out_ids'] and phase != 'final':
        raise ValueError('Held-out maker jobs are reserved for final acceptance, never development tuning')


def run(args):
    config = checkout_check()
    job_path = Path(args.job).resolve()
    job = json.loads(job_path.read_bytes())
    guard_held_out(job, args.phase)
    identifier = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    dest = ROOT / 'output/playwright/svgnest' / identifier
    dest.mkdir(parents=True)
    source = dest / 'job.json'
    shutil.copyfile(job_path, source)
    record = {'tool': 'SVGnest', 'run_id': identifier, 'revision': config['revision'], 'job': job['name'],
              'job_sha256': digest(source), 'seed': args.seed, 'seconds': args.seconds,
              'settings': args.settings, 'axis': args.axis, 'phase': args.phase,
              'settings_finalized': config['settings_finalized'], 'score': None,
              'started_at': datetime.now(timezone.utc).isoformat(),
              'commit': command(['git', 'rev-parse', 'HEAD']),
              'dirty': bool(command(['git', 'status', '--porcelain'])),
              'platform': platform.platform(), 'node': command(['node', '--version']),
              'sources': {name: digest(ROOT / name) for name in SOURCE_FILES}}
    record['cpu'] = command(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                              '(Get-CimInstance Win32_Processor).Name']) if os.name == 'nt' else platform.processor()
    try:
        prepared = prepare(job, config['settings'][args.settings], args.axis)
        record['restrictions'] = prepared['restrictions']
        record['configuration'] = prepared['config']
        write(dest / 'request.json', {'seconds': args.seconds, 'seed': args.seed, 'prepared': prepared})
        (dest / 'input.svg').write_text(prepared['svg'] + '\n', encoding='utf-8', newline='\n')
        subprocess.run(['cargo', 'build', '-p', 'nestbolt-cli', '--locked'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        binary = ROOT / 'target/debug' / ('nestbolt.exe' if os.name == 'nt' else 'nestbolt')
        record['validator_sha256'] = digest(binary)
        record['validator_sources'] = {p.relative_to(ROOT).as_posix(): digest(p)
            for p in [ROOT / 'Cargo.lock', *sorted((ROOT / 'crates/validator/src').glob('*.rs'))]}
        blank = {'version': 1, 'units': job['units'], 'sheets': [], 'placements': []}
        write(dest / 'empty-layout.json', blank)
        contract = subprocess.run([str(binary), 'validate', '--job', str(source), '--layout', str(dest / 'empty-layout.json')],
                                  capture_output=True, cwd=ROOT, timeout=60)
        checked = json.loads(contract.stdout)
        if any(v['code'] != 'quantity' for v in checked['violations']):
            raise ValueError('Invalid job source contract')
        with (dest / 'stdout.log').open('wb') as stdout, (dest / 'stderr.log').open('wb') as stderr:
            child = subprocess.Popen(['node', 'benchmarks/browser/svgnest.mjs', str(dest / 'request.json')],
                                     cwd=ROOT, stdout=stdout, stderr=stderr, start_new_session=os.name != 'nt')
            try:
                code = child.wait(timeout=args.seconds + 90)
            except subprocess.TimeoutExpired:
                if os.name == 'nt':
                    subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'], capture_output=True, check=False)
                else:
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait()
                record['status'] = 'timeout'
                code = None
        if code is not None:
            record['exit_code'] = code
            raw_path = dest / 'browser-result.json'
            if code != 0 or not raw_path.exists():
                record['status'] = 'failed'
            else:
                raw = json.loads(raw_path.read_bytes())
                record.update({'browser_version': raw.get('browser_version'), 'cpu_affinity': raw['affinity'],
                               'browser_executables': raw.get('browser_executables'),
                               'affinity_verification': raw.get('affinity_verification'),
                               'candidates': raw['candidates'], 'controller_solve_ms': raw.get('controller_solve_ms')})
                if raw['status'] != 'completed' or raw['errors']:
                    record['status'] = raw['status'] if not raw['errors'] else 'failed'
                else:
                    common = layout(prepared, raw['last']['sheets'])
                    write(dest / 'layout.json', common)
                    for i, svg in enumerate(raw['last']['svgs']):
                        (dest / f'native-sheet-{i}.svg').write_text(svg + '\n', encoding='utf-8', newline='\n')
                    validation = subprocess.run([str(binary), 'validate', '--job', str(source), '--layout', str(dest / 'layout.json')],
                                                capture_output=True, cwd=ROOT, timeout=120)
                    (dest / 'validation.json').write_bytes(validation.stdout)
                    report = json.loads(validation.stdout)
                    record['validator_exit_code'] = validation.returncode
                    record['status'] = 'valid' if validation.returncode == 0 and report['valid'] else 'invalid'
                    if record['status'] == 'valid':
                        record['metrics'] = report['metrics']
                        record['score'] = report['metrics']['normalized_material']
    except UnsupportedJob as error:
        record.update({'status': 'unsupported', 'reason': str(error)})
    except Exception as error:
        record.update({'status': 'failed', 'reason': str(error)})
    record['finished_at'] = datetime.now(timezone.utc).isoformat()
    record['outputs'] = {p.name: digest(p) for p in sorted(dest.iterdir()) if p.is_file()}
    write(dest / 'run.json', record)
    relative = (dest / 'run.json').relative_to(ROOT).as_posix()
    with (ROOT / 'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as file:
        file.write(f'\n- {record["finished_at"]} | SVGnest `{job["name"]}` seed {args.seed}, {args.seconds}s, {args.settings}, axis {args.axis} | {record["status"]} | material {record["score"]} | [record]({relative}). Provisional settings, one worker and one CPU affinity.\n')
    print(json.dumps({'status': record['status'], 'score': record['score'], 'record': relative, 'reason': record.get('reason')}), flush=True)
    return record


def batch(args):
    from datasets import check_frozen, MANIFEST, DEST
    check_frozen()
    rows = sorted((row for row in json.loads(MANIFEST.read_bytes())['instances'] if row['set'] == 'B'), key=lambda row: row['id'])
    selected = rows[args.offset:args.offset + args.count]
    if not selected:
        raise ValueError('Batch selection is empty')
    # Reserve controller startup, source validation and independent output checks
    # as well as solve time. Compilation/setup is performed before this session.
    if len(selected) * (args.seconds + 300) > 3 * 3600:
        raise ValueError('Selected batch could exceed three hours; reduce --count')
    sources = {name: digest(ROOT / name) for name in SOURCE_FILES}
    subprocess.run(['cargo', 'build', '-p', 'nestbolt-cli', '--locked'], cwd=ROOT, check=True)
    identifier = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    dest = ROOT / 'output/playwright/svgnest-batches' / identifier
    dest.mkdir(parents=True)
    record = {'batch_id': identifier, 'kind': 'provisional_svgnest_baseline', 'dataset': 'B',
              'dataset_manifest_sha256': digest(MANIFEST), 'cases': selected, 'sources': sources,
              'seed': args.seed, 'seconds': args.seconds, 'axis': args.axis, 'settings': args.settings,
              'complete': False, 'runs': []}
    write(dest / 'start.json', record)
    for row in selected:
        if {name: digest(ROOT / name) for name in SOURCE_FILES} != sources:
            raise ValueError('Runner changed during the batch; preserving incomplete evidence')
        source = DEST / row['path']
        if digest(source) != row['sha256']:
            raise ValueError('Frozen batch source changed')
        result = run(argparse.Namespace(job=source, seconds=args.seconds, seed=args.seed,
                    settings=args.settings, axis=args.axis, phase='development'))
        path = ROOT / 'output/playwright/svgnest' / result['run_id'] / 'run.json'
        entry = {'job': row['id'], 'status': result['status'], 'record': path.relative_to(ROOT).as_posix(), 'sha256': digest(path)}
        record['runs'].append(entry)
        with (dest / 'runs.jsonl').open('a', encoding='utf-8', newline='\n') as file:
            file.write(json.dumps(entry) + '\n')
    record['complete'] = True  # all selected attempts recorded, including failures
    record['valid_runs'] = sum(r['status'] == 'valid' for r in record['runs'])
    write(dest / 'batch.json', record)
    print(f'Batch finished: {record["valid_runs"]}/{len(selected)} valid. Evidence: {dest / "batch.json"}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('setup')
    running = commands.add_parser('run')
    batching = commands.add_parser('batch', help='A bounded sequential slice of frozen B jobs; every outcome retained')
    for sub in [running, batching]:
        sub.add_argument('--seconds', type=int, default=60)
        sub.add_argument('--seed', type=int, default=0)
        sub.add_argument('--settings', choices=['identical', 'expanded'], default='identical')
        sub.add_argument('--axis', choices=['x', 'y'], default='y')
    running.add_argument('--job', required=True)
    running.add_argument('--phase', choices=['development', 'final'], default='development')
    batching.add_argument('--offset', type=int, default=0)
    batching.add_argument('--count', type=int, default=24)
    args = parser.parse_args()
    if args.command == 'setup':
        setup()
    else:
        if not 1 <= args.seconds <= 300 or not 0 <= args.seed < 2**32:
            parser.error('Budget must be 1..300 seconds; seed must be an unsigned 32-bit integer')
        if args.command == 'batch':
            if args.offset < 0 or not 1 <= args.count <= 35:
                parser.error('offset must be nonnegative; count must be 1..35')
            batch(args)
        else:
            result = run(args)
            sys.exit(0 if result['status'] in ['valid', 'unsupported'] else 1)


if __name__ == '__main__':
    main()
