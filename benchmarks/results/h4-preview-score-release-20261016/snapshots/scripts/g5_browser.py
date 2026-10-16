"""G5 browser quality: the WebAssembly build in real browsers against the native
build, on the development B/M jobs (held-out jobs excluded), same seed and budget.

The built site (`web/dist`, from `python scripts/build_web.py`) is served on
127.0.0.1 and `web/bench/run.mjs` runs every job through bench.html in its own
Web Worker, at most eight at once, in the installed Google Chrome and
Playwright's Firefox build, with the browser processes restricted to the
eight physical cores of the first CCD (logical CPUs 0, 2, ..., 14), the CPUs
the native batches are pinned to. Every layout is
re-checked with the native `nestbolt validate` and scored like the native batch.

Pass rule, fixed before the first run: in each browser every job returns a
valid layout, and both the median per-job material difference and the total
material over all jobs are within +2% of the native run (`--native`, a
`scripts/sheets_batch.py` record with the same seed and budget). The worst
single job is reported, not gated: one seed of a stochastic search varies more
than that between runs of the same build.
"""
import argparse
from datetime import datetime, timezone
from functools import partial
from hashlib import sha256
import http.server
import json
from pathlib import Path
import statistics
import subprocess
import sys
import threading
import time
import uuid

import psutil

from sheets_batch import ROOT, digest, select_cases

# One logical CPU per physical core of the first CCD, as the native batches use.
CPUS = list(range(0, 16, 2))
THRESHOLD = 2.0


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(directory):
    handler = partial(Quiet, directory=str(directory))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def pin_tree(root, seen):
    """Keep every process the runner starts on the benchmark CPUs; return how many."""
    try:
        procs = [root, *root.children(recursive=True)]
    except psutil.Error:
        return
    for p in procs:
        if p.pid in seen:
            continue
        try:
            p.cpu_affinity(CPUS)
            seen[p.pid] = p.name()
        except psutil.Error:
            pass


def peak_memory(root, peak):
    try:
        procs = [root, *root.children(recursive=True)]
        total = sum(p.memory_info().rss for p in procs if p.is_running())
        peak[0] = max(peak[0], total)
    except psutil.Error:
        pass


def run_browser(browser, cases, args, url, run_dir):
    plan_dir = run_dir/browser
    plan_dir.mkdir(parents=True)
    jobs = []
    for case in cases:
        job = ROOT/'benchmarks/datasets'/case['path']
        if digest(job) != case['sha256']:
            raise ValueError(f'{case["id"]}: job hash differs from the frozen manifest')
        (plan_dir/case['id']).mkdir()
        jobs.append({'id': case['id'], 'path': str(job), 'out': str(plan_dir/case['id'])})
    plan = {'browser': browser, 'url': url, 'seconds': args.seconds, 'seed': args.seed,
            'concurrency': args.concurrency, 'jobs': jobs, 'info': str(plan_dir/'browser.json')}
    (plan_dir/'plan.json').write_text(json.dumps(plan, indent=1), encoding='utf-8')
    node = subprocess.Popen(['node', str(ROOT/'web/bench/run.mjs'), str(plan_dir/'plan.json')], cwd=ROOT/'web',
                            stdout=subprocess.PIPE, text=True)
    root, seen, peak = psutil.Process(node.pid), {}, [0]
    stop = threading.Event()

    def watch():
        while not stop.is_set():
            pin_tree(root, seen)
            peak_memory(root, peak)
            stop.wait(0.2)
    watcher = threading.Thread(target=watch, daemon=True)
    watcher.start()
    for line in node.stdout:
        print(browser, line.rstrip(), flush=True)
    code = node.wait()
    stop.set()
    watcher.join()
    if code:
        raise SystemExit(f'{browser} runner exited with {code}')
    return json.loads((plan_dir/'browser.json').read_text(encoding='utf-8')), peak[0], sorted(set(seen.values()))


def score(browser, cases, binary, run_dir):
    rows = []
    for case in cases:
        directory = run_dir/browser/case['id']
        row = {'job': case['id'], 'directory': directory.relative_to(ROOT).as_posix()}
        if not (directory/'layout.json').exists():
            row['status'] = 'failed'
            row['error'] = (directory/'error.txt').read_text(encoding='utf-8')[:500]
            rows.append(row)
            continue
        result = json.loads((directory/'result.json').read_text(encoding='utf-8'))
        job = ROOT/'benchmarks/datasets'/case['path']
        check = subprocess.run([str(binary), 'validate', '--job', str(job), '--layout', str(directory/'layout.json')],
                               capture_output=True)
        (directory/'validation.json').write_bytes(check.stdout)
        report = json.loads(check.stdout)
        if check.returncode or not report['valid']:
            row['status'] = 'invalid'
        elif report['metrics'] != result['validation']['metrics']:
            raise ValueError(f'{browser} {case["id"]}: native metrics differ from the browser report')
        else:
            row.update(status='valid', material=report['metrics']['normalized_material'],
                       sheets=report['metrics']['sheets_used'], elapsed_seconds=result['elapsed_seconds'],
                       accepted_at_seconds=result['accepted_at_seconds'], memory_bytes=result['memory_bytes'],
                       layout_sha256=digest(directory/'layout.json'))
        rows.append(row)
    return rows


def summary(rows, native):
    diffs, browser_total, native_total = [], 0.0, 0.0
    for row in rows:
        reference = native.get(row['job'])
        if row['status'] != 'valid' or reference is None:
            row['difference_percent'] = None
            continue
        row['native_material'] = reference
        row['difference_percent'] = 100 * (row['material'] / reference - 1)
        diffs.append(row['difference_percent'])
        browser_total += row['material']
        native_total += reference
    valid = sum(r['status'] == 'valid' for r in rows)
    out = {'valid': valid, 'jobs': len(rows), 'compared': len(diffs)}
    if diffs:
        worst = max(rows, key=lambda r: -1e9 if r['difference_percent'] is None else r['difference_percent'])
        out.update(median_difference_percent=statistics.median(diffs),
                   total_difference_percent=100 * (browser_total / native_total - 1),
                   worst_job=worst['job'], worst_difference_percent=worst['difference_percent'],
                   within_two_percent=sum(d <= THRESHOLD for d in diffs))
        out['passes'] = (valid == len(rows) and len(diffs) == len(rows)
                         and out['median_difference_percent'] <= THRESHOLD
                         and out['total_difference_percent'] <= THRESHOLD)
    else:
        out['passes'] = False
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True, help='sheets_batch.py JSON record, same seed and budget')
    parser.add_argument('--browser', action='append', choices=['chrome', 'chromium', 'firefox'],
                        help='chrome is the installed Google Chrome (default: chrome and firefox)')
    parser.add_argument('--binary', type=Path, default=ROOT/'target/release/nestbolt.exe')
    parser.add_argument('--job', action='append', default=[])
    parser.add_argument('--seconds', type=float, default=60.0)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--concurrency', type=int, default=8)
    parser.add_argument('--label', default='g5-browser')
    args = parser.parse_args()
    if not 1 <= args.concurrency <= 8:
        parser.error('at most eight runs at once')
    browsers = args.browser or ['chrome', 'firefox']
    native_record = json.loads(args.native.read_text(encoding='utf-8'))
    if native_record['seed'] != args.seed or native_record['seconds'] != args.seconds:
        parser.error('the native record must use the same seed and budget')
    native = {r['job']: r['material'] for r in native_record['rows'] if r['status'] == 'valid'}
    cases = select_cases(args.job)
    dist = ROOT/'web/dist'
    wasm = sorted(dist.glob('assets/*.wasm'))
    if len(wasm) != 1 or not (dist/'bench.html').exists():
        parser.error('build the site first: python scripts/build_web.py')
    binary = args.binary.resolve(strict=True)
    started = datetime.now(timezone.utc)
    stamp = started.strftime('%Y%m%dT%H%M%SZ')
    run_dir = ROOT/'output/g5-browser'/f'{stamp}-{uuid.uuid4().hex[:8]}'
    run_dir.mkdir(parents=True)
    server = serve(dist)
    url = f'http://127.0.0.1:{server.server_address[1]}/bench.html'
    results = {}
    try:
        for browser in browsers:
            t0 = time.perf_counter()
            info, peak, processes = run_browser(browser, cases, args, url, run_dir)
            rows = score(browser, cases, binary, run_dir)
            results[browser] = {'info': info, 'peak_process_tree_rss_bytes': peak, 'pinned_processes': processes,
                                'wall_seconds': time.perf_counter() - t0, 'summary': summary(rows, native), 'rows': rows}
            print(browser, json.dumps(results[browser]['summary']), flush=True)
    finally:
        server.shutdown()
    name = f'{args.label}-s{args.seed}-{stamp}-{uuid.uuid4().hex[:8]}'
    record = {'scope': 'G5 quality: development B/M jobs, WebAssembly in browsers vs native, same seed and budget.',
              'recorded_at': datetime.now(timezone.utc).isoformat(), 'seed': args.seed, 'seconds': args.seconds,
              'concurrency': args.concurrency, 'cpus': CPUS, 'threshold_percent': THRESHOLD,
              'wasm_sha256': sha256(wasm[0].read_bytes()).hexdigest(), 'wasm_file': wasm[0].name,
              'validator_sha256': digest(binary),
              'native_record': args.native.resolve().relative_to(ROOT).as_posix(),
              'native_binary_sha256': native_record['binary_sha256'],
              'run_directory': run_dir.relative_to(ROOT).as_posix(), 'browsers': results}
    out = ROOT/'benchmarks/results'
    (out/f'{name}.json').write_text(json.dumps(record, indent=1) + '\n', encoding='utf-8', newline='\n')
    lines = ['# G5 browser quality', '',
             f'Development B/M jobs, seed {args.seed}, {args.seconds} s wall clock per job, the WebAssembly build in '
             f'its own Web Worker per job, at most {args.concurrency} at once, browser processes on logical CPUs '
             f'{", ".join(map(str, CPUS))}. Native reference: [{args.native.name}]({args.native.name}). Pass: every layout valid, median '
             f'and total material within +{THRESHOLD}% of native.', '',
             '| Browser | Version | Valid | Median difference | Total difference | Worst job | Within 2% | Pass |',
             '| --- | --- | ---: | ---: | ---: | --- | ---: | --- |']
    for browser, r in results.items():
        s = r['summary']
        lines.append(f"| {browser} | {r['info']['version']} | {s['valid']}/{s['jobs']} | "
                     f"{s.get('median_difference_percent', float('nan')):+.3f}% | "
                     f"{s.get('total_difference_percent', float('nan')):+.3f}% | "
                     f"{s.get('worst_job', '—')} ({s.get('worst_difference_percent', float('nan')):+.2f}%) | "
                     f"{s.get('within_two_percent', 0)}/{s['compared']} | {'yes' if s['passes'] else 'no'} |")
    lines += ['', '| Job | Native | ' + ' | '.join(results) + ' |', '| --- | ---: |' + ' ---: |' * len(results)]
    for case in cases:
        cells = []
        for r in results.values():
            row = next(x for x in r['rows'] if x['job'] == case['id'])
            cells.append(row['status'] if row['status'] != 'valid'
                         else f"{row['material']:.6f} ({row['difference_percent']:+.2f}%)")
        lines.append(f"| {case['id']} | {native.get(case['id'], float('nan')):.6f} | " + ' | '.join(cells) + ' |')
    lines += ['', f'[Full record]({name}.json)', '']
    (out/f'{name}.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print(out/f'{name}.md')
    return 0 if all(r['summary']['passes'] for r in results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
