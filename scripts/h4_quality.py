"""H4 quality on the eleven declared development jobs, native/Chrome/Firefox.

G5 method: one fresh worker per browser job, physical CCD0 cores, 60 seconds,
seeds 0-2. Every saved layout receives standalone native validation. Compare
per-job three-seed material medians; missing/failing attempts cannot pass.
Subset limits: median <=+1%, every job <=+5%. Pilots are never gate evidence.
No held-out jobs, optional search modes, baseline substitution or tuning here.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from queue import Queue
import shutil
import statistics
import subprocess
import threading
import time
import traceback

import psutil
from g5_browser import serve
from h2_import_audit import source_digest
from h6_material_cost import run, equivalent
from sheets_batch import select_cases

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT/'target/release/nestbolt.exe'
FIXTURE = ROOT/'benchmarks/datasets/browser-quality'
CPUS = list(range(0, 16, 2))
SUBSET = ([f'm-public-gear-{i}' for i in range(1, 5)]
          + [f'm-sign-{i}' for i in range(1, 5)] + ['m-mechanical-cog-washers'])


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def cases():
    rows = [{**r, 'path': 'benchmarks/datasets/'+r['path']} for r in select_cases(SUBSET)]
    manifest = json.loads((FIXTURE/'manifest.json').read_bytes())
    assert len(rows) == 9 and len(manifest['cases']) == 2
    assert digest(ROOT/'web/public/examples/examples.json') == manifest['source_manifest']
    for name, value in manifest['files'].items():
        assert digest(FIXTURE/name) == value, name
    rows += manifest['cases']
    for row in rows:
        assert digest(ROOT/row['path']) == row['sha256'], row['id']
        if 'source_sha256' in row:
            assert digest(ROOT/row['source']) == row['source_sha256'], row['id']
    return rows


def guards(rows):
    paths = [Path(__file__), ROOT/'scripts/g5_browser.py', ROOT/'scripts/sheets_batch.py',
             ROOT/'scripts/dataset_selection.py', ROOT/'scripts/h6_material_cost.py',
             ROOT/'web/bench/run.mjs', CLI, FIXTURE/'manifest.json',
             ROOT/'benchmarks/datasets/makers.json', ROOT/'benchmarks/datasets/academic.json']
    paths += [ROOT/r['path'] for r in rows]
    paths += [ROOT/r[k] for r in rows for k in ['library', 'request'] if k in r]
    paths += [p for p in sorted((ROOT/'web/dist').rglob('*')) if p.is_file()]
    return {'product': source_digest(), 'files': {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}}


def check(row, folder, cpu, result):
    command = run([CLI, 'validate', '--job', ROOT/row['path'], '--layout', folder/'layout.json'],
                  folder, 'validate', cpu, 60)
    assert command['exit_code'] == 0, 'Standalone validator failed'
    validation = json.loads((folder/'validate-stdout.json').read_bytes())
    assert validation['valid']
    delta = equivalent(validation['metrics'], result['validation']['metrics'])
    assert len(json.loads((folder/'layout.json').read_bytes())['placements']) == sum(
        p['quantity'] for p in json.loads((ROOT/row['path']).read_bytes())['parts'])
    if 'library' in row:
        public = run([CLI, 'validate', '--library', ROOT/row['library'], '--request', ROOT/row['request'],
                      '--layout', folder/'layout.json'], folder, 'public-validate', cpu, 60)
        assert public['exit_code'] == 0
        report = json.loads((folder/'public-validate-stdout.json').read_bytes())
        assert report['valid'], 'Example layout fails its actual public request'
        delta = max(delta, equivalent(report['metrics'], validation['metrics']))
    return {'status': 'valid', 'material': validation['metrics']['normalized_material'],
            'sheets': validation['metrics']['sheets_used'], 'validation': command,
            'maximum_metric_json_roundtrip_difference': delta,
            'elapsed_seconds': result['elapsed_seconds'],
            'accepted_at_seconds': result['accepted_at_seconds'],
            'layout_sha256': digest(folder/'layout.json')}


def native(row, seed, seconds, out, cpus):
    cpu = cpus.get()
    folder = out/'native'/f's{seed}'/row['id']
    folder.mkdir(parents=True)
    record = {'job': row['id'], 'seed': seed, 'status': 'failed', 'cpu': cpu,
              'directory': folder.relative_to(ROOT).as_posix()}
    try:
        record['run'] = run([CLI, 'sheets', '--job', ROOT/row['path'], '--output', folder/'layout.json',
                             '--seconds', seconds, '--seed', seed], folder, 'search', cpu, seconds+90)
        assert record['run']['exit_code'] == 0, 'Native search failed'
        result = json.loads((folder/'search-stdout.json').read_bytes())
        record.update(check(row, folder, cpu, result))
    except Exception:
        record['error'] = traceback.format_exc()
    finally:
        cpus.put(cpu)
    write(folder/'case.json', record)
    return record


def browser(name, seed, rows, args, out, url):
    folder = out/name/f's{seed}'
    folder.mkdir(parents=True)
    jobs = []
    for row in rows:
        target = folder/row['id']
        target.mkdir()
        jobs.append({'id': row['id'], 'path': str(ROOT/row['path']), 'out': str(target)})
    plan = {'browser': name, 'url': url, 'seconds': args.seconds, 'seed': seed,
            'concurrency': args.concurrency, 'jobs': jobs, 'info': str(folder/'browser.json')}
    write(folder/'plan.json', plan)
    command = [shutil.which('node'), str(ROOT/'web/bench/run.mjs'), str(folder/'plan.json')]
    observed, errors = {}, []
    stop = threading.Event()
    started = time.perf_counter()
    with (folder/'stdout.log').open('wb') as stdout, (folder/'stderr.log').open('wb') as stderr:
        process = subprocess.Popen(command, cwd=ROOT/'web', stdout=stdout, stderr=stderr,
                                   creationflags=subprocess.CREATE_NO_WINDOW | 4)
        root = psutil.Process(process.pid)
        root.cpu_affinity(CPUS)
        root.resume()

        def watch():
            while not stop.is_set():
                try:
                    children = [root, *root.children(recursive=True)]
                except psutil.Error:
                    children = []
                for child in children:
                    try:
                        affinity = child.cpu_affinity()
                        if affinity != CPUS:
                            errors.append({'pid': child.pid, 'affinity': affinity})
                            child.cpu_affinity(CPUS)
                        observed[child.pid] = child.name()
                    except psutil.Error:
                        pass
                stop.wait(0.1)

        watcher = threading.Thread(target=watch, daemon=True)
        watcher.start()
        try:
            code = process.wait(timeout=(args.seconds+90)*((len(rows)+args.concurrency-1)//args.concurrency)+120)
        except subprocess.TimeoutExpired:
            code = 'timeout'
            for child in reversed(root.children(recursive=True)):
                try:
                    child.kill()
                except psutil.Error:
                    pass
            process.kill()
            process.wait()
        finally:
            stop.set()
            watcher.join()
    execution = {'command': command, 'exit_code': code, 'wall_seconds': time.perf_counter()-started,
                 'cpus': CPUS, 'processes': observed, 'affinity_errors': errors}
    write(folder/'execution.json', execution)
    records = []
    for row in rows:
        target = folder/row['id']
        record = {'job': row['id'], 'seed': seed, 'status': 'failed',
                  'directory': target.relative_to(ROOT).as_posix()}
        try:
            assert (target/'layout.json').exists(), (target/'error.txt').read_text(encoding='utf-8') if (target/'error.txt').exists() else 'No browser output'
            result = json.loads((target/'result.json').read_bytes())
            record.update(check(row, target, 0, result))
            record['wasm_memory_bytes'] = result['memory_bytes']
            assert code == 0 and not errors, 'Browser execution or CPU-affinity guard failed'
        except Exception:
            record['status'] = 'failed'
            record.pop('material', None)
            record['error'] = traceback.format_exc()
        write(target/'case.json', record)
        records.append(record)
    return records


def summarize(records, rows, seeds, seconds):
    complete = seeds == [0, 1, 2] and seconds == 60 and len(rows) == 11
    medians = {}
    for engine in ['native', 'chrome', 'firefox']:
        medians[engine] = {}
        for case in rows:
            group = [r for r in records[engine] if r['job'] == case['id']]
            values = sorted((r.get('material') if r['status'] == 'valid' else None for r in group),
                            key=lambda v: (v is None, v or 0))
            # Failure-valued upper ranks, never a valid-only median.
            valid = len(group) == len(seeds) and sorted(r['seed'] for r in group) == seeds
            value = values[len(values)//2] if valid and len(seeds) == 3 else None
            medians[engine][case['id']] = value
    comparisons = {}
    for engine in ['chrome', 'firefox']:
        differences = {r['id']: None if medians['native'][r['id']] is None or medians[engine][r['id']] is None
                       else 100*(medians[engine][r['id']]/medians['native'][r['id']]-1) for r in rows}
        finite = [v for v in differences.values() if v is not None]
        valid = sum(r['status'] == 'valid' for r in records[engine])
        coverage = len(finite) == len(rows)
        median = statistics.median(finite) if coverage else None
        worst = max(finite) if coverage else None
        comparisons[engine] = {'valid': valid, 'attempted': len(records[engine]),
            'per_job_difference_percent': differences, 'median_difference_percent': median,
            'worst_difference_percent': worst,
            'total_difference_percent': (100*(sum(medians[engine].values())/sum(medians['native'].values())-1)
                                         if coverage else None),
            'passes_subset': bool(complete and coverage and valid == 33 and
                                  all(r['status'] == 'valid' for r in records['native']) and median <= 1 and worst <= 5)}
    return {'complete_development_subset': complete, 'medians': medians, 'comparisons': comparisons,
            'passes_subset': all(r['passes_subset'] for r in comparisons.values()),
            'H4_complete': False, 'full_G5_and_native_matrix_evaluated': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--seed', type=int, action='append')
    parser.add_argument('--job', action='append', default=[])
    parser.add_argument('--concurrency', type=int, default=8)
    args = parser.parse_args()
    seeds = sorted(args.seed or [0, 1, 2])
    assert len(set(seeds)) == len(seeds) and set(seeds) <= {0, 1, 2}
    assert 1 <= args.concurrency <= 8 and 0 < args.seconds <= 60
    rows = cases()
    if args.job:
        assert set(args.job) <= {r['id'] for r in rows}
        rows = [r for r in rows if r['id'] in args.job]
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT/'benchmarks/results'/f'h4-quality-{stamp}'
    out.mkdir()
    before = guards(rows)
    write(out/'plan.json', {'scope': __doc__, 'seeds': seeds, 'seconds': args.seconds,
                           'cpus': CPUS, 'concurrency': args.concurrency, 'cases': rows, 'guards': before,
                           'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()})
    records = {'native': [], 'chrome': [], 'firefox': []}
    print(out, flush=True)

    def progress():
        write(out/'progress.json', {k: {'done': len(v), 'valid': sum(r['status'] == 'valid' for r in v)}
                                   for k, v in records.items()})

    cpus = Queue()
    for cpu in CPUS[:args.concurrency]:
        cpus.put(cpu)
    with ThreadPoolExecutor(args.concurrency) as pool:
        futures = [pool.submit(native, row, seed, args.seconds, out, cpus) for seed in seeds for row in rows]
        for future in as_completed(futures):
            r = future.result()
            records['native'].append(r)
            progress()
            print('native', r['job'], r['seed'], r['status'], r.get('material'), flush=True)
    server = serve(ROOT/'web/dist')
    try:
        url = f'http://127.0.0.1:{server.server_address[1]}/bench.html'
        for engine in ['chrome', 'firefox']:
            for seed in seeds:
                assert guards(rows) == before, 'Inputs changed between batches'
                batch = browser(engine, seed, rows, args, out, url)
                records[engine].extend(batch)
                progress()
                print(engine, seed, 'valid', sum(r['status'] == 'valid' for r in batch), '/', len(batch), flush=True)
    finally:
        server.shutdown()
    unchanged = guards(rows) == before
    summary = summarize(records, rows, seeds, args.seconds)
    summary['guards_unchanged'] = unchanged
    summary['passes_subset'] &= unchanged
    write(out/'results.json', {'records': records, 'summary': summary})
    print(json.dumps(summary), flush=True)
    assert unchanged, 'Sources/executables/site/inputs changed during measurement'


if __name__ == '__main__':
    main()
