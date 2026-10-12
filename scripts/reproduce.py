"""G8: one command rebuilds the datasets, runs the comparison matrix and writes the
results table, charts and page.

    python scripts/reproduce.py --phase development
    python scripts/reproduce.py --phase final --final-acceptance

Stages run in order (choose with --only): `datasets` rebuilds the academic jobs
from their pinned sources and the maker jobs from their pinned generators and
checks every byte against the freeze; `competitors` runs Deepnest, SVGnest and
Sparrow with the sealed settings (benchmarks/final-settings.json) over every job,
budget, seed and settings role of the phase; `nestbolt` runs Nestbolt over the
same jobs, budgets and seeds; `report` writes web/public/results.

The run is resumable across sessions: a slot whose complete, audited batch
record already exists is reused, and nothing is retried automatically, so failed
attempts stay in the evidence. At most eight runs at once, one CPU each. Deepnest
opens Electron windows; on Artem's PC its batches run inside the hidden Anode
desktop (pass --tools deepnest there, the rest here). The final phase includes
the held-out jobs, which ends tuning, so it needs --final-acceptance.
"""
import argparse
import glob
import json
from pathlib import Path
import subprocess
import os
import sys
import threading
import time

import psutil

from comparison_cases import comparison_cases
from dataset_selection import PHASE_SEEDS, check_seed

ROOT = Path(__file__).resolve().parents[1]
SETTINGS = ROOT/'benchmarks/final-settings.json'
BATCHES = {'deepnest': 'output/playwright/deepnest-batches', 'svgnest': 'output/playwright/svgnest-batches',
           'sparrow': 'output/sparrow-batches'}
SCRIPTS = {'deepnest': 'scripts/deepnest.py', 'svgnest': 'scripts/svgnest.py', 'sparrow': 'scripts/sparrow_benchmark.py'}
CPUS = list(range(0, 16, 2))


def run(command):
    print('+', ' '.join(map(str, command)), flush=True)
    return subprocess.run(command, cwd=ROOT).returncode


def datasets():
    for command in [[sys.executable, 'scripts/datasets.py'], [sys.executable, 'scripts/maker_setup.py'],
                    [sys.executable, 'scripts/maker_freeze.py', '--rebuild'],
                    [sys.executable, 'scripts/matrix_plan.py', '--check']]:
        if run(command):
            raise SystemExit(f'dataset stage failed: {" ".join(command)}')


def finished_runs(tool, phase):
    """(dataset, seconds, seed, settings, axis, job) of every run in a complete batch, and
    the same keys for batches that started but never completed (interruptions)."""
    complete, interrupted = set(), set()
    for start in glob.glob(str(ROOT/BATCHES[tool]/'*'/'start.json')):
        path = Path(start)
        batch = json.loads((path.with_name('batch.json') if path.with_name('batch.json').exists() else path)
                           .read_text(encoding='utf-8'))
        if batch.get('phase', 'development') != phase:
            continue
        key = tuple(batch[k] for k in ['dataset', 'seconds', 'seed', 'settings', 'axis'])
        if batch.get('complete'):
            complete.update(key + (run['job'],) for run in batch['runs'])
        else:
            interrupted.update(key + (c['id'],) for c in batch['cases'])
    return complete, interrupted - complete


def competitor_tasks(phase, tools):
    """Remaining batches: the phase's jobs per tool, dataset, budget, seed and settings
    without a completed run, in chunks of the tool's batch size."""
    sealed = json.loads(SETTINGS.read_text(encoding='utf-8'))
    tasks, total, blocked = [], 0, []
    for tool, config in sealed['tools'].items():
        if tools and tool not in tools:
            continue
        complete, interrupted = finished_runs(tool, phase)
        for dataset, roles in config['datasets'].items():
            axis = 'x' if dataset == 'S' else 'y'
            for seconds in [60, 300]:
                if dataset == 'S' and seconds == 300:
                    continue
                cases = comparison_cases(ROOT, dataset, seconds, phase)[1]
                size = config['batch_size'][str(seconds)]
                for seed in PHASE_SEEDS[phase]:
                    for settings in sorted(set(roles.values())):
                        key = (dataset, seconds, seed, settings, axis)
                        total += len(cases)
                        blocked += [key + (c['id'],) for c in cases if key + (c['id'],) in interrupted]
                        remaining = [c for c in cases if key + (c['id'],) not in complete | interrupted]
                        for offset in range(0, len(remaining), size):
                            chunk = remaining[offset:offset + size]
                            # A batch takes a contiguous slice of the phase's job list.
                            ids = [c['id'] for c in cases]
                            first, last = ids.index(chunk[0]['id']), ids.index(chunk[-1]['id'])
                            if last - first + 1 != len(chunk):
                                chunk = [chunk[0]]
                                first = last = ids.index(chunk[0]['id'])
                            tasks.append({'tool': tool, 'dataset': dataset, 'seconds': seconds, 'seed': seed,
                                          'settings': settings, 'axis': axis, 'offset': first,
                                          'count': last - first + 1, 'phase': phase})
    return tasks, total, blocked


def competitors(phase, tools, cpus, dry_run, minutes=None):
    tasks, total, blocked = competitor_tasks(phase, tools)
    print(json.dumps({'competitor_runs': total, 'remaining_batches': len(tasks),
                      'interrupted_runs': len(blocked)}), flush=True)
    if blocked:
        raise SystemExit(f'interrupted runs need inspection before continuing: {blocked[:5]}')
    if dry_run:
        for t in tasks[:10]:
            print('would run', t)
        return

    def one(task, cpu):
        command = [sys.executable, SCRIPTS[task['tool']], 'batch', '--dataset', task['dataset'],
                   '--offset', str(task['offset']), '--count', str(task['count']), '--seconds', str(task['seconds']),
                   '--seed', str(task['seed']), '--settings', task['settings'], '--axis', task['axis'],
                   '--phase', task['phase']]
        print(f'+ [cpu {cpu}]', ' '.join(command), flush=True)
        # Browser runners pin their tool via NESTBENCH_CPU; the batch process and every
        # descendant (Sparrow included) also inherit this one-CPU affinity.
        process = subprocess.Popen(command, cwd=ROOT, env={**os.environ, 'NESTBENCH_CPU': str(cpu)})
        try:
            psutil.Process(process.pid).cpu_affinity([cpu])
        except psutil.Error:
            pass
        return process.wait()
    # Each batch runs its native tool on one CPU; Deepnest batches may run side by
    # side inside one hidden desktop, as the development matrix did. With a time
    # limit (an Anode job lives 30 minutes), a batch starts only if its worst
    # case still fits; the rest wait for the next invocation.
    deadline = time.monotonic() + 60 * minutes if minutes else None
    queue, lock, codes = list(tasks), threading.Lock(), []

    def lane(cpu):
        while True:
            with lock:
                fits = [t for t in queue if deadline is None
                        or time.monotonic() + t['count'] * (t['seconds'] + 400) < deadline]
                if not fits:
                    return
                task = fits[0]
                queue.remove(task)
            codes.append(one(task, cpu))
    lanes = [threading.Thread(target=lane, args=(cpu,)) for cpu in cpus[:8]]
    for t in lanes:
        t.start()
    for t in lanes:
        t.join()
    print(json.dumps({'ran_batches': len(codes), 'left_for_later': len(queue)}), flush=True)
    if any(codes):
        raise SystemExit('some competitor batches failed; their evidence is retained')


def strips(phase, dry_run):
    """G3: Nestbolt's strip adapter on set S, one process per seed on its own CPU."""
    done = {json.loads(Path(p).read_text(encoding='utf-8')).get('seed') for p in
            glob.glob(str(ROOT/'benchmarks/results/strip-native-*.json'))
            if json.loads(Path(p).read_text(encoding='utf-8')).get('phase') == phase}
    todo = [seed for seed in PHASE_SEEDS[phase] if seed not in done]
    commands = [[sys.executable, 'scripts/strip_pilot.py', '--phase', phase, '--seed', str(seed),
                 '--cpu', str(CPUS[i % len(CPUS)])] for i, seed in enumerate(todo)]
    if dry_run:
        for c in commands:
            print('would run', ' '.join(c))
        return
    processes = [subprocess.Popen(c, cwd=ROOT) for c in commands]
    if any(p.wait() for p in processes):
        raise SystemExit('a strip run failed; evidence retained')


def nestbolt(phase, binary, final, dry_run):
    strips(phase, dry_run)
    slots = [(60, False), (300, True), (30, True)]
    for seconds, long_subset in slots:
        for seed in PHASE_SEEDS[phase]:
            check_seed(phase, seed)
            label = f'{phase}-{seconds}s-s{seed}'
            existing = [p for p in glob.glob(str(ROOT/'benchmarks/results'/f'sheets-{label}-*.json'))
                        if json.loads(Path(p).read_text(encoding='utf-8')).get('phase', 'development') == phase]
            if existing:
                continue
            command = [sys.executable, 'scripts/sheets_batch.py', '--binary', str(binary), '--seconds', str(seconds),
                       '--seed', str(seed), '--label', label, '--phase', phase,
                       '--reference-seconds', '300' if seconds != 60 else '60',
                       *[a for c in CPUS for a in ('--cpu', str(c))]]
            if long_subset:
                command.append('--long-subset')
            if final:
                command.append('--final-acceptance')
            if dry_run:
                print('would run', ' '.join(command))
            elif run(command):
                raise SystemExit(f'Nestbolt batch {label} failed; evidence retained')


def report(phase):
    records = lambda seconds: sorted(glob.glob(str(ROOT/'benchmarks/results'/f'sheets-{phase}-{seconds}s-s*.json')))
    sixty, long, quick = records(60), records(300), records(30)
    if not sixty:
        raise SystemExit(f'no {phase} Nestbolt records yet')
    command = [sys.executable, 'scripts/results_page.py', '--phase', phase, '--nestbolt-60', *sixty, '--strip']
    if long:
        command += ['--nestbolt-300', *long]
    if quick:
        command += ['--nestbolt-30', *quick]
    if run(command):
        raise SystemExit('report failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--phase', choices=['development', 'final'], required=True)
    parser.add_argument('--final-acceptance', action='store_true')
    parser.add_argument('--only', choices=['datasets', 'competitors', 'nestbolt', 'report'], action='append')
    parser.add_argument('--tools', choices=['deepnest', 'svgnest', 'sparrow'], action='append')
    parser.add_argument('--cpus', type=int, nargs='+', default=CPUS,
                        help='one competitor lane per logical CPU, at most eight (default: physical cores of CCD0)')
    parser.add_argument('--binary', type=Path, default=ROOT/'target/release/nestbolt.exe')
    parser.add_argument('--dry-run', action='store_true', help='list what would run')
    parser.add_argument('--minutes', type=float, help='start no competitor batch that could end after this')
    args = parser.parse_args()
    stages = args.only or ['datasets', 'competitors', 'nestbolt', 'report']
    # Competitor runs on held-out jobs inform nothing about Nestbolt; Nestbolt's own
    # runs on them end tuning, so that stage needs an explicit confirmation.
    if args.phase == 'final' and 'nestbolt' in stages and not args.final_acceptance and not args.dry_run:
        parser.error('Nestbolt on the held-out jobs ends tuning: pass --final-acceptance')
    if 'datasets' in stages and not args.dry_run:
        datasets()
    if 'competitors' in stages:
        competitors(args.phase, args.tools, args.cpus, args.dry_run, args.minutes)
    if 'nestbolt' in stages:
        nestbolt(args.phase, args.binary.resolve(), args.final_acceptance, args.dry_run)
    if 'report' in stages and not args.dry_run:
        report(args.phase)


if __name__ == '__main__':
    main()
