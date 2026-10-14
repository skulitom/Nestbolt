"""Record seeded analytic importer/search properties on four CCD0 cores.

Build beforehand on CCD1 with cargo test --release -p nestbolt-core --test
import_habits --test search_fuzz --no-run --message-format json, saving stdout
to output/h2-habits-build.jsonl. This runner never loads corpus geometry.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import time

import psutil

from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]
TESTS = {
    'import_habits': ('random_shop_habits_preserve_analytic_parts', 2500),
    'search_fuzz': ('imported_shop_habits_nest_with_original_geometry', 250),
}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build-log', type=Path, default=ROOT/'output/h2-habits-build.jsonl')
    args = parser.parse_args()
    artifacts = {}
    for line in args.build_log.read_text(encoding='utf-8-sig').splitlines():
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if item.get('reason') == 'compiler-artifact' and item.get('executable'):
            if item['target']['name'] in TESTS and item.get('profile', {}).get('test'):
                artifacts[item['target']['name']] = Path(item['executable'])
    assert artifacts.keys() == TESTS.keys(), 'Build both optimized test binaries first'
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT/'output'/f'h2-habit-fuzz-{stamp}'
    work.mkdir(exist_ok=False)
    before = source_digest()
    runner_hash = sha256(Path(__file__).read_bytes()).hexdigest()
    binaries = {key: sha256(path.read_bytes()).hexdigest() for key, path in artifacts.items()}

    def batch(seed):
        results = []
        for key, (test, cases) in TESTS.items():
            env = os.environ.copy()
            env.update(NESTBOLT_HABIT_CASES=str(cases), PROPTEST_RNG_SEED=str(seed),
                       NESTBOLT_HABIT_TRACE='1')
            begin = time.perf_counter()
            proc = subprocess.Popen([str(artifacts[key]), '--exact', test, '--nocapture', '--test-threads=1'],
                                    cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW | 4)
            timeout = False
            try:
                child = psutil.Process(proc.pid)
                child.cpu_affinity([2*seed])
                child.resume()
                try:
                    stdout, stderr = proc.communicate(timeout=900)
                except subprocess.TimeoutExpired:
                    timeout = True
                    proc.kill()
                    stdout, stderr = proc.communicate()
            except BaseException:
                proc.kill()
                proc.communicate()
                raise
            (work/f'{key}-{seed}.stdout').write_bytes(stdout)
            (work/f'{key}-{seed}.stderr').write_bytes(stderr)
            coverage = Counter(line.removeprefix('habit-pass ') for line in stderr.decode('utf-8', errors='replace').splitlines()
                               if line.startswith('habit-pass '))
            result = {'test': test, 'seed': seed, 'cpu': 2*seed, 'requested_cases': cases,
                      'elapsed_s': time.perf_counter()-begin, 'exit_code': proc.returncode,
                      'timeout': timeout, 'habit_coverage': dict(sorted(coverage.items())),
                      'stdout_sha256': sha256(stdout).hexdigest(), 'stderr_sha256': sha256(stderr).hexdigest(),
                      'passed': not timeout and proc.returncode == 0 and sum(coverage.values()) >= cases
                                and len(coverage) == 17 and b'test result: ok. 1 passed' in stdout}
            results.append(result)
            print(f'{key} seed {seed}: {sum(coverage.values())} checked, passed={result["passed"]}', flush=True)
        return results

    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = [row for batch_rows in pool.map(batch, range(4)) for row in batch_rows]
    guards = {'product_sources_unchanged': source_digest() == before,
              'runner_unchanged': sha256(Path(__file__).read_bytes()).hexdigest() == runner_hash,
              'binaries_unchanged': all(sha256(path.read_bytes()).hexdigest() == binaries[key]
                                        for key, path in artifacts.items())}
    summary = {'recorded_at': stamp, 'scope': 'H2 analytic shop-habit proptest and feasible search properties',
               'H2': False, 'held_out_read': False, 'corpus_files_read': 0,
               'source_sha256': before, 'runner_sha256': runner_hash, 'binary_sha256': binaries,
               'work_directory': str(work), 'guards': guards,
               'passed': all(guards.values()) and all(row['passed'] for row in rows), 'rows': rows}
    out = ROOT/'benchmarks/results'/f'h2-habit-fuzz-{stamp}'
    write_json(out.with_suffix('.json'), summary)
    lines = ['# H2 analytic shop-habit fuzzing', '', f'Passed: **{summary["passed"]}**.', '',
             'Four fixed seeds (0–3), each with 2,500 importer cases and 250 feasible search cases; '
             'saved regression replays may add cases. All 17 N0 habits must occur in each batch. '
             'No corpus file or held-out label/geometry is opened.', '',
             'The independent analytic fixtures vary sizes, translations, shuffled/reversed entities, '
             'gaps, overlaps, duplicates, cubic SPLINEs, negative extrusion, bulges/widths, block bases '
             'and nesting, units, annotations, construction layers, colours and sheet outlines. '
             'Checks cover counts, bounds, area, off-centre hole geometry and expected diagnostics. '
             'Searches vary quantities, quarter-turns and mirroring; every feasible job must succeed '
             'and pass the independent original-polygon validator.', '',
             f'Guards: {guards}. One child per CCD0 physical core 0/2/4/6; builds run separately on CCD1. '
             'Each child has a 900 s external bound. Failures/timeouts are retained and never counted as passes.', '',
             '| Test | Seed | Requested | Observed checks | Seconds | Passed |',
             '| --- | ---: | ---: | ---: | ---: | --- |']
    for row in rows:
        lines.append(f'| {row["test"]} | {row["seed"]} | {row["requested_cases"]} | '
                     f'{sum(row["habit_coverage"].values())} | {row["elapsed_s"]:.3f} | {row["passed"]} |')
    lines += ['', 'This supplies habit-fuzz evidence only. Remaining H2 requirements and H3 are not waived.']
    out.with_suffix('.md').write_text('\n'.join(lines)+'\n', encoding='utf-8', newline='\n')
    print(out.with_suffix('.json'))
    if not summary['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
