"""Timed development batch for `nestbolt sheets`; no held-out jobs, no gate claim.

Each job runs as one native process pinned to one logical CPU, at most eight at
once. Every outcome is retained. Successful layouts are re-checked with the
standalone `validate` command before they are scored. Comparisons use the frozen
M1 three-seed competitor medians; a single development seed is triage only.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
from queue import Queue
import statistics
import subprocess
import sys
import time
import uuid

import psutil

from dataset_selection import development_cases

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT/'benchmarks/results/baseline-gap-20261012T033547Z-e9539412.json'
TIE = 0.000001


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def lf_digest(path):
    return sha256(Path(path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def select_cases(include=(), exclude=()):
    cases = [case for group in ['B', 'M'] for case in development_cases(ROOT, group)[1]]
    known = {case['id'] for case in cases}
    if (set(include) | set(exclude)) - known:
        raise ValueError('Choose frozen development B/M IDs; held-out and unknown IDs are forbidden')
    selected = [c for c in cases if (not include or c['id'] in include) and c['id'] not in exclude]
    if not selected:
        raise ValueError('No development jobs selected')
    return selected


def competitor_medians(seconds):
    rows = json.loads(BASELINE.read_bytes())['rows']
    return {row['job']: row['competitor']['median'] for row in rows
            if row['seconds'] == seconds and row.get('competitor')}


def compare(material, competitor):
    if material is None or competitor is None:
        return None
    if abs(material - competitor) <= TIE * competitor:
        outcome = 'tie'
    elif material < competitor:
        outcome = 'win'
    else:
        outcome = 'loss'
    return {'reduction_percent': 100 * (1 - material / competitor), 'outcome': outcome,
            'within_one_percent': material / competitor <= 1.01}


def run_case(binary, case, args, run_dir, cpus):
    cpu = cpus.get()
    try:
        directory = run_dir/case['id']
        directory.mkdir(parents=True)
        job = ROOT/'benchmarks/datasets'/case['path']
        if digest(job) != case['sha256']:
            raise ValueError(f'{case["id"]}: job hash differs from the frozen manifest')
        layout = directory/'layout.json'
        command = [str(binary), 'sheets', '--job', str(job), '--output', str(layout),
                   '--seconds', str(args.seconds), '--seed', str(args.seed), *args.solver_arg]
        started = time.perf_counter()
        with open(directory/'stdout.json', 'wb') as out, open(directory/'progress.log', 'wb') as err:
            process = subprocess.Popen(command, stdout=out, stderr=err)
            psutil.Process(process.pid).cpu_affinity([cpu])
            try:
                code = process.wait(timeout=args.seconds + 60)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                code = 'timeout'
        wall = time.perf_counter() - started
        row = {'job': case['id'], 'job_sha256': case['sha256'], 'cpu': cpu, 'exit_code': code,
               'wall_seconds': wall, 'directory': directory.relative_to(ROOT).as_posix()}
        if code != 0:
            row['status'] = 'failed'
            return row
        result = json.loads((directory/'stdout.json').read_bytes())
        check = subprocess.run([str(binary), 'validate', '--job', str(job), '--layout', str(layout)],
                               capture_output=True)
        (directory/'validation.json').write_bytes(check.stdout)
        report = json.loads(check.stdout)
        if check.returncode != 0 or not report['valid']:
            row['status'] = 'invalid'
            return row
        if report['metrics'] != result['validation']['metrics']:
            raise ValueError(f'{case["id"]}: standalone metrics differ from the solver report')
        row.update(status='valid', material=report['metrics']['normalized_material'],
                   sheets=report['metrics']['sheets_used'],
                   warm_material=result['warm_start']['normalized_material'],
                   accepted_at_seconds=result['accepted_at_seconds'],
                   elapsed_seconds=result['elapsed_seconds'], stats=result['stats'],
                   history=result['history'], layout_sha256=digest(layout),
                   validation_sha256=digest(directory/'validation.json'))
        return row
    finally:
        cpus.put(cpu)


SOURCE_FILES = ['scripts/sheets_batch.py', 'crates/core/src/sheets.rs', 'crates/core/src/sheets/vstrip.rs',
                'crates/core/src/separate.rs', 'crates/core/src/construct.rs', 'crates/core/src/optimize.rs',
                'crates/core/src/holes.rs', 'crates/core/src/clock.rs', 'crates/core/src/curves.rs']


def report(rows, args, binary_hash, started, run_dir, sources):
    competitors = competitor_medians(args.reference_seconds)
    lines = ['# Fixed-sheet separator: development batch', '',
             f'All selected development B/M jobs, seed {args.seed}, {args.seconds} s wall clock per job, '
             'one pinned logical CPU per process. Ten held-out maker jobs are excluded. Competitor '
             f'references are the frozen M1 three-seed {args.reference_seconds} s medians; one Nestbolt '
             'seed is development evidence, not final acceptance.', '', f'Solver arguments: `{" ".join(args.solver_arg) or "defaults"}`.', '']
    valid = [r for r in rows if r['status'] == 'valid']
    lines.append(f'Valid layouts: **{len(valid)}/{len(rows)}**. Failed or invalid outcomes are listed below and never scored.')
    comparisons = []
    for row in rows:
        row['comparison'] = compare(row.get('material'), competitors.get(row['job']))
        if row['comparison']:
            comparisons.append(row['comparison'])
    if comparisons:
        reductions = [c['reduction_percent'] for c in comparisons]
        wins = sum(c['outcome'] != 'loss' for c in comparisons)
        worse = sum(not c['within_one_percent'] for c in comparisons)
        lines += ['', f'Finite competitor comparisons: {len(comparisons)}; wins/ties {wins} '
                  f'({100 * wins / len(comparisons):.1f}%); more than 1% worse: {worse}; '
                  f'median material reduction **{statistics.median(reductions):.4f}%**. '
                  f'Jobs without a finite competitor median: {len(rows) - len(comparisons)}; they earn no wins.']
    lines += ['', '| Job | Status | Material | Warm start | Competitor | Reduction | Sheets | Accepted at s |',
              '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for row in rows:
        c = row['comparison']
        competitor = competitors.get(row['job'])
        fmt = lambda v, d=6: '—' if v is None else f'{v:.{d}f}'
        reduction = '—' if not c else f"{c['reduction_percent']:.3f}%"
        lines.append(f"| {row['job']} | {row['status']} | {fmt(row.get('material'))} | "
                     f"{fmt(row.get('warm_material'))} | {fmt(competitor)} | {reduction} | "
                     f"{row.get('sheets', '—')} | {fmt(row.get('accepted_at_seconds'), 1)} |")
    stamp = started.strftime('%Y%m%dT%H%M%SZ')
    name = f'sheets-{args.label}-{stamp}-{uuid.uuid4().hex[:8]}'
    record = {'scope': 'Development B/M only; one seed; timed; no acceptance-gate claim.',
              'recorded_at': datetime.now(timezone.utc).isoformat(), 'seed': args.seed,
              'seconds': args.seconds, 'reference_seconds': args.reference_seconds, 'cpus': args.cpu, 'solver_args': args.solver_arg, 'binary_sha256': binary_hash,
              'baseline': {'path': BASELINE.relative_to(ROOT).as_posix(), 'git_lf_sha256': lf_digest(BASELINE)},
              'sources_at_start': sources,
              'run_directory': run_dir.relative_to(ROOT).as_posix(), 'rows': rows}
    out = ROOT/'benchmarks/results'
    (out/f'{name}.json').write_text(json.dumps(record, indent=1) + '\n', encoding='utf-8', newline='\n')
    lines += ['', f'[Full record]({name}.json)', '']
    (out/f'{name}.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    return out/f'{name}.md'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, default=ROOT/'target/release/nestbolt.exe')
    parser.add_argument('--job', action='append', default=[])
    parser.add_argument('--exclude-job', action='append', default=[])
    parser.add_argument('--cpu', type=int, action='append', required=True)
    parser.add_argument('--seconds', type=float, default=60.0)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--solver-arg', action='append', default=[],
                        help='extra argument passed to `nestbolt sheets`, e.g. --solver-arg=--window=8')
    parser.add_argument('--label', default='development')
    parser.add_argument('--reference-seconds', type=int, choices=[60, 300], default=60)
    args = parser.parse_args()
    if not 1 <= len(args.cpu) <= 8 or len(set(args.cpu)) != len(args.cpu) or not 0 < args.seconds <= 300:
        parser.error('1..8 distinct CPUs; budget in (0, 300] seconds')
    try:
        cases = select_cases(args.job, args.exclude_job)
    except ValueError as error:
        parser.error(str(error))
    binary = args.binary.resolve(strict=True)
    binary_hash = digest(binary)
    sources = {p: lf_digest(ROOT/p) for p in SOURCE_FILES}
    started = datetime.now(timezone.utc)
    run_dir = ROOT/'output/sheets-batches'/f"{started.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    run_dir.mkdir(parents=True)
    cpus = Queue()
    for cpu in args.cpu:
        cpus.put(cpu)
    with ThreadPoolExecutor(len(args.cpu)) as pool:
        futures = [pool.submit(run_case, binary, case, args, run_dir, cpus) for case in cases]
        rows = []
        for future in futures:
            row = future.result()
            rows.append(row)
            print(json.dumps({k: row.get(k) for k in ['job', 'status', 'material', 'warm_material']}), flush=True)
    print(report(rows, args, binary_hash, started, run_dir, sources))


if __name__ == '__main__':
    sys.exit(main())
