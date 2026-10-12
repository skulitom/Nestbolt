"""Bounded native desktop comparator. Run inside Anode on Windows for hidden UI."""
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
from deepnest_io import prepare, layout
from svgnest import ROOT, digest, command, write, guard_held_out

CHECKOUT = ROOT / '.cache/upstream/deepnest-next'
CONFIG = ROOT / 'benchmarks/deepnest/tool.json'
SOURCES = ['scripts/deepnest.py', 'scripts/deepnest_io.py', 'scripts/svgnest.py',
           'scripts/svgnest_io.py', 'scripts/svg_export_transform.py', 'scripts/benchmark_io.py', 'benchmarks/deepnest/tool.json',
           'benchmarks/browser/deepnest.mjs', 'benchmarks/browser/deepnest-lifecycle.mjs', 'benchmarks/browser/deepnest-preload.cjs',
           'benchmarks/browser/deepnest-bootstrap.cjs', 'benchmarks/browser/cpu-limit.mjs',
           'benchmarks/browser/cpu-job.ps1', 'benchmarks/browser/package.json',
           'benchmarks/browser/cpu-tree-job.ps1',
           'benchmarks/browser/package-lock.json']
SOURCES += ['scripts/stock_inputs.py', 'crates/validator/examples/stock_adapter.rs']
SOURCES += ['scripts/dataset_selection.py']
SOURCES += ['scripts/comparison_cases.py', 'scripts/matrix_plan.py', 'benchmarks/matrix-plan.json']


def checkout_check():
    config = json.loads(CONFIG.read_bytes())
    if command(['git', 'rev-parse', 'HEAD'], CHECKOUT) != config['revision']:
        raise ValueError('Deepnest checkout differs from the pinned revision')
    if command(['git', 'status', '--porcelain', '--untracked-files=no'], CHECKOUT):
        raise ValueError('Deepnest checkout has tracked changes')
    lock = subprocess.check_output(['git', 'show', 'HEAD:package-lock.json'], cwd=CHECKOUT)
    if sha256(lock).hexdigest() != config['upstream_lock_git_blob_sha256']:
        raise ValueError('Deepnest dependency lock differs from the frozen Git blob')
    return config


def setup():
    config = json.loads(CONFIG.read_bytes())
    if not CHECKOUT.exists():
        CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', '--no-checkout', '--filter=blob:none', config['repository'], str(CHECKOUT)], check=True)
        subprocess.run(['git', '-C', str(CHECKOUT), 'checkout', '--detach', config['revision']], check=True)
    checkout_check()
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    subprocess.run([npm, 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=CHECKOUT, check=True)
    subprocess.run(['node', 'node_modules/typescript/bin/tsc'], cwd=CHECKOUT, check=True)
    subprocess.run(['node', 'node_modules/electron/install.js'], cwd=CHECKOUT, check=True)
    subprocess.run([npm, 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=ROOT / 'benchmarks/browser', check=True)
    print('Prepared pinned Deepnest and local browser controller.')


def run(args):
    config = checkout_check()
    job_path = Path(args.job).resolve()
    job = json.loads(job_path.read_bytes())
    guard_held_out(job, args.phase)
    identifier = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    dest = ROOT / 'output/playwright/deepnest' / identifier
    dest.mkdir(parents=True)
    shutil.copyfile(job_path, dest / 'job.json')
    record = {'tool': 'deepnest-next', 'revision': config['revision'], 'run_id': identifier,
              'job': job['name'], 'job_sha256': digest(dest / 'job.json'), 'seed': args.seed,
              'seconds': args.seconds, 'settings': args.settings, 'axis': args.axis, 'phase': args.phase,
              'settings_finalized': config['settings_finalized'], 'score': None,
              'input_encoding': 'linear_svg_paths_v2',
              'started_at': datetime.now(timezone.utc).isoformat(), 'commit': command(['git', 'rev-parse', 'HEAD']),
              'dirty': bool(command(['git', 'status', '--porcelain'])), 'platform': platform.platform(),
              'node': command(['node', '--version']), 'sources': {name: digest(ROOT / name) for name in SOURCES},
              'upstream_lock_sha256': digest(CHECKOUT / 'package-lock.json')}
    record['cpu'] = command(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                            '(Get-CimInstance Win32_Processor).Name']) if os.name == 'nt' else platform.processor()
    try:
        settings = config['settings'][args.settings]
        stock_geometry = None
        if any(s['outline'] or s['defects'] for s in job['stocks']):
            from stock_inputs import prepare_stocks
            stock_geometry, record['stock_preparation'] = prepare_stocks(
                dest/'job.json', job['clearance']*settings.get('spacing_multiplier',1), dest/'stock-inputs.json')
        prepared = prepare(job, settings, args.axis, stock_geometry)
        record['configuration'] = prepared['config']
        record['restrictions'] = prepared['restrictions']
        write(dest / 'request.json', {'seconds': args.seconds, 'seed': args.seed, 'prepared': prepared})
        for source in prepared['imports']:
            (dest / f'input-{source["source"]}.svg').write_text(source['svg']+'\n', encoding='utf-8', newline='\n')
        snapshot = getattr(args, 'validator_snapshot', None)
        if snapshot:
            binary = ROOT / snapshot['path']
            if digest(binary) != snapshot['sha256']:
                raise ValueError('Batch validator binary changed')
        else:
            subprocess.run(['cargo', 'build', '--locked', '-p', 'nestbolt-cli'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
            binary = ROOT / 'target/debug' / ('nestbolt.exe' if os.name == 'nt' else 'nestbolt')
        record['validator_sha256'] = digest(binary)
        record['validator_sources'] = snapshot['sources'] if snapshot else {p.relative_to(ROOT).as_posix(): digest(p)
            for p in [ROOT / 'Cargo.lock', *sorted((ROOT / 'crates/validator/src').glob('*.rs'))]}
        write(dest / 'empty-layout.json', {'version': 1, 'units': job['units'], 'sheets': [], 'placements': []})
        contract = subprocess.run([str(binary), 'validate', '--job', str(dest / 'job.json'), '--layout', str(dest / 'empty-layout.json')],
                                  capture_output=True, cwd=ROOT, timeout=60)
        if any(v['code'] != 'quantity' for v in json.loads(contract.stdout)['violations']):
            raise ValueError('Invalid original job source contract')
        record['compiled_app_sources'] = {p.relative_to(CHECKOUT).as_posix(): digest(p)
            for p in sorted((CHECKOUT / 'build').rglob('*.js'))}
        with (dest / 'stdout.log').open('wb') as stdout, (dest / 'stderr.log').open('wb') as stderr:
            child = subprocess.Popen(['node', 'benchmarks/browser/deepnest.mjs', str(dest / 'request.json')],
                                     cwd=ROOT, stdout=stdout, stderr=stderr, start_new_session=os.name != 'nt')
            try:
                code = child.wait(timeout=args.seconds+210)
            except subprocess.TimeoutExpired:
                if os.name == 'nt':
                    subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'], capture_output=True, check=False)
                else:
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait()
                record['status'], code = 'timeout', None
        if code is not None:
            record['exit_code'] = code
            raw_path = dest / 'browser-result.json'
            if code != 0 or not raw_path.exists():
                record['status'] = 'failed'
            else:
                raw = json.loads(raw_path.read_bytes())
                for name in ['versions', 'affinity', 'affinity_verification', 'worker_check', 'electron_executable_sha256', 'native_binaries', 'stages_ms', 'controller_solve_ms', 'candidates', 'input_fidelity']:
                    record[name] = raw.get(name)
                if raw['errors'] or raw['status'] != 'completed':
                    record['status'] = 'failed' if raw['errors'] else raw['status']
                else:
                    write(dest / 'layout.json', layout(prepared, raw['last']['native']))
                    validation = subprocess.run([str(binary), 'validate', '--job', str(dest / 'job.json'), '--layout', str(dest / 'layout.json')],
                                                capture_output=True, cwd=ROOT, timeout=120)
                    (dest / 'validation.json').write_bytes(validation.stdout)
                    checked = json.loads(validation.stdout)
                    record['validator_exit_code'] = validation.returncode
                    record['status'] = 'valid' if validation.returncode == 0 and checked['valid'] else 'invalid'
                    if record['status'] == 'valid':
                        record['metrics'], record['score'] = checked['metrics'], checked['metrics']['normalized_material']
    except UnsupportedJob as error:
        record.update(status='unsupported', reason=str(error))
    except Exception as error:
        record.update(status='failed', reason=str(error))
    record['finished_at'] = datetime.now(timezone.utc).isoformat()
    record['outputs'] = {p.name: digest(p) for p in sorted(dest.iterdir()) if p.is_file()}
    write(dest / 'run.json', record)
    relative = (dest / 'run.json').relative_to(ROOT).as_posix()
    with (ROOT / 'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as file:
        file.write(f'\n- {record["finished_at"]} | deepnest-next `{job["name"]}` seed {args.seed}, {args.seconds}s, {args.settings}, axis {args.axis} | '
                   f'{record["status"]} | material {record["score"]} | [record]({relative}). Provisional native settings; independent score only for valid output.\n')
    print(json.dumps({'status': record['status'], 'score': record['score'], 'record': relative, 'reason': record.get('reason')}), flush=True)
    return record


def freeze_validator(destination, from_batch=None):
    sources = {p.relative_to(ROOT).as_posix(): digest(p)
               for p in [ROOT/'Cargo.lock', *sorted((ROOT/'crates/validator/src').glob('*.rs'))]}
    if from_batch:
        previous = json.loads(Path(from_batch).read_bytes())['validator_snapshot']
        binary = (ROOT/previous['path']).resolve(strict=True)
        if (not binary.is_relative_to(ROOT) or previous['sources'] != sources
                or digest(binary) != previous['sha256']):
            raise ValueError('Reusable checker snapshot changed or has incompatible source provenance')
        checksum = previous['sha256']
    else:
        subprocess.run(['cargo', 'build', '--locked', '-p', 'nestbolt-cli'], cwd=ROOT, check=True)
        binary = ROOT/'target/debug'/('nestbolt.exe' if os.name == 'nt' else 'nestbolt')
        checksum = digest(binary)
    frozen = destination/binary.name
    shutil.copy2(binary, frozen)
    if digest(frozen) != checksum:
        raise ValueError('Checker binary changed while copying')
    return {'path': frozen.relative_to(ROOT).as_posix(), 'sha256': checksum, 'sources': sources}


def batch(args):
    from dataset_selection import check_seed, phase_cases
    check_seed(args.phase, args.seed)
    if args.dataset == 'M':
        from maker_freeze import check_frozen, DEST
    else:
        from datasets import check_frozen, DEST
    check_frozen()
    manifest, rows = phase_cases(ROOT, args.dataset, args.phase)
    if args.seconds == 300:
        from comparison_cases import comparison_cases
        manifest, rows = comparison_cases(ROOT, args.dataset, args.seconds, args.phase)
    selected = rows[args.offset:args.offset+args.count]
    # Anode jobs have a 30-minute hard lifetime. Reserve startup, both checks,
    # controller teardown and metadata collection even if every attempt fails.
    if not selected or len(selected)*(args.seconds+400) > 27*60:
        raise ValueError('Empty batch or worst-case session over 27 minutes; reduce --count')
    sources = {name:digest(ROOT/name) for name in SOURCES}
    identifier = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    dest = ROOT/'output/playwright/deepnest-batches'/identifier
    dest.mkdir(parents=True)
    validator_snapshot = freeze_validator(dest, getattr(args, 'validator_from_batch', None))
    record = {'batch_id':identifier, 'tool':'deepnest-next', 'dataset':args.dataset,
              'dataset_manifest_sha256':digest(manifest), 'cases':selected, 'sources':sources,
              'seconds':args.seconds, 'seed':args.seed, 'settings':args.settings, 'axis':args.axis,
              'phase':args.phase, 'complete':False, 'runs':[], 'validator_snapshot':validator_snapshot}
    write(dest/'start.json', record)
    for row in selected:
        if {name:digest(ROOT/name) for name in SOURCES} != sources:
            raise ValueError('Runner changed during batch; incomplete evidence retained')
        source = DEST/row['path']
        if digest(source) != row['sha256']:
            raise ValueError('Frozen job source changed')
        result = run(argparse.Namespace(job=source, seconds=args.seconds, seed=args.seed,
                     settings=args.settings, axis=args.axis, phase=args.phase, validator_snapshot=validator_snapshot))
        path = ROOT/'output/playwright/deepnest'/result['run_id']/'run.json'
        entry = {'job':row['id'], 'status':result['status'], 'record':path.relative_to(ROOT).as_posix(), 'sha256':digest(path)}
        record['runs'].append(entry)
        with (dest/'runs.jsonl').open('a', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(entry)+'\n')
    record['complete'] = True
    record['valid_runs'] = sum(r['status'] == 'valid' for r in record['runs'])
    write(dest/'batch.json', record)
    print(f'Batch finished: {record["valid_runs"]}/{len(selected)} valid. Evidence: {dest / "batch.json"}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    subs.add_parser('setup')
    running = subs.add_parser('run')
    batching = subs.add_parser('batch')
    running.add_argument('--job', required=True)
    for sub in [running, batching]:
        sub.add_argument('--seconds', type=int, default=60)
        sub.add_argument('--seed', type=int, default=0)
        sub.add_argument('--settings', choices=['identical','expanded','clearance-safe'], default='identical')
        sub.add_argument('--axis', choices=['x','y'], default='y')
    running.add_argument('--phase', choices=['development','final'], default='development')
    batching.add_argument('--offset', type=int, default=0)
    batching.add_argument('--count', type=int, default=3)
    batching.add_argument('--dataset', choices=['B','M'], default='B', help='development M excludes every held-out job')
    batching.add_argument('--phase', choices=['development','final'], default='development',
                          help='final: seeds 1000-1004 and the held-out jobs (acceptance run only)')
    batching.add_argument('--validator-from-batch', type=Path,
                          help='Reuse a verified immutable checker snapshot from an earlier batch JSON')
    args = parser.parse_args()
    if args.command == 'setup':
        setup()
    else:
        if not 1 <= args.seconds <= 300 or not 0 <= args.seed < 2**32:
            parser.error('Budget must be 1..300 seconds and seed uint32')
        if args.command == 'batch':
            if args.offset < 0 or not 1 <= args.count <= 35:
                parser.error('Offset must be nonnegative; count must be 1..35')
            batch(args)
        else:
            outcome = run(args)
            sys.exit(0 if outcome['status'] in ['valid','unsupported'] else 1)
