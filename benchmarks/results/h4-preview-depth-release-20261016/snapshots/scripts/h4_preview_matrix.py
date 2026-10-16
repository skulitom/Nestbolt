"""Confirm H4 on the integrated preview: 603 new development attempts.

Run the union of the full 65-job development set and eleven-job subset once per
native/Chrome/Firefox engine, at 60 seconds and seeds 0-2. Reuse only the 195
sealed frozen-v1 baseline outcomes, never the preceding product's outcomes.
No held-out inputs, final seeds, changed bounds or competing-tool claims.
Prepare and commit the plan before running; an opened marker prevents repeats.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
from queue import Queue
import shutil
import subprocess
import time
import traceback
from types import SimpleNamespace
import zipfile

import h4_full_matrix as full
import h4_quality as quality
from g5_browser import serve

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT/'benchmarks/results/h4-full-development-20261015'
SEEDS = [0, 1, 2]
load, write = full.load, full.write


def cases():
    development, subset = full.cases(), quality.cases()
    known = {r['id']: r for r in development}
    for row in subset:
        if row['id'] in known:
            assert row == known[row['id']]
        else:
            known[row['id']] = row
    rows = list(known.values())
    assert len(development) == 65 and len(subset) == 11 and len(rows) == 67
    return rows, development, subset


def baseline(rows):
    previous, plan, inventory = (load(PRIOR/name) for name in ['results.json', 'plan.json', 'integrity.json'])
    assert previous['summary']['all_quality_checks_pass']
    assert plan['seeds'] == SEEDS and plan['seconds'] == 60
    assert plan['baseline_sha256'] == full.BASELINE_SHA
    assert plan['cases'] == rows
    archive = PRIOR/'raw.zip'
    assert quality.digest(archive) == inventory['sha256']
    records = previous['records']['v1']
    assert len(records) == 195
    assert {(r['job'], r['seed']) for r in records} == {(r['id'], s) for r in rows for s in SEEDS}
    known = {r['id']: r for r in rows}
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        baseline_member = (PRIOR/'snapshots/engines/nestbolt-final-75cbb32.exe').relative_to(ROOT).as_posix()
        assert sha256(z.read(baseline_member)).hexdigest() == full.BASELINE_SHA
        for name in ['plan.json', 'results.json']:
            assert z.read((PRIOR/name).relative_to(ROOT).as_posix()) == (PRIOR/name).read_bytes()
        for r in records:
            assert r['status'] == 'valid' and not r['reused']
            files = {}
            for name in ['case.json', 'layout.json', 'search-stdout.json', 'validate-stdout.json']:
                member = r['directory']+'/'+name
                raw = z.read(member)
                assert sha256(raw).hexdigest() == inventory['members'][member]['sha256']
                files[name] = json.loads(raw)
            assert files['case.json'] == r
            assert files['validate-stdout.json']['valid'] and files['search-stdout.json']['validation']['valid']
            assert quality.equivalent(files['validate-stdout.json']['metrics'], files['search-stdout.json']['validation']['metrics']) == 0
            assert files['validate-stdout.json']['metrics']['normalized_material'] == r['material']
            assert sha256(z.read(r['directory']+'/layout.json')).hexdigest() == r['layout_sha256']
            assert len(files['layout.json']['placements']) == sum(p['quantity'] for p in load(ROOT/known[r['job']]['path'])['parts'])
    return [{**r, 'reused': True, 'source_archive': archive.relative_to(ROOT).as_posix()} for r in records]


def guards(rows):
    result = quality.guards(rows)
    for p in [Path(__file__), ROOT/'scripts/h4_full_matrix.py', ROOT/'scripts/test_h4_full_matrix.py',
              PRIOR/'plan.json', PRIOR/'results.json', PRIOR/'integrity.json', PRIOR/'raw.zip']:
        result['files'][p.relative_to(ROOT).as_posix()] = quality.digest(p)
    result['environment'] = {k: os.environ.get(k) for k in full.OVERRIDES}
    assert all(v is None for v in result['environment'].values())
    return result


def prepare(out):
    rows, development, subset = cases()
    reused = baseline(development)
    out.mkdir()
    plan = {'scope': __doc__, 'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'cases': rows, 'full_ids': [r['id'] for r in development], 'subset_ids': [r['id'] for r in subset],
        'seconds': 60, 'seeds': SEEDS, 'cpus': quality.CPUS, 'concurrency': 8,
        'guards': guards(rows), 'reused_v1': reused,
        'new_attempts': {'native': 201, 'chrome': 201, 'firefox': 201},
        'gates': {'subset_median_percent': 1, 'subset_every_job_percent': 5,
                  'native_median_percent': .5, 'G5_median_percent': 2, 'G5_total_percent': 2,
                  'every_layout_valid': True, 'G5_each_seed_also_checked': True},
        'maximum_session_hours': 4, 'held_out_geometry_read': False,
        'scale_confirmation_and_H4_requirement_review_separate': True}
    write(out/'plan.json', plan)
    for name in ['scripts/h4_preview_matrix.py', 'scripts/h4_quality.py', 'scripts/h4_full_matrix.py',
                 'scripts/test_h4_full_matrix.py', 'scripts/h6_material_cost.py', 'scripts/g5_browser.py', 'web/bench/run.mjs']:
        target = out/'snapshots'/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    print(json.dumps({'prepared': str(out), 'new_attempts': 603, 'reused_baseline': 195}), flush=True)


def measure(out):
    plan = load(out/'plan.json')
    rows, development, subset = cases()
    assert rows == plan['cases'] and guards(rows) == plan['guards']
    relative = (out/'plan.json').relative_to(ROOT).as_posix()
    assert subprocess.check_output(['git', 'show', 'HEAD:'+relative], cwd=ROOT) == (out/'plan.json').read_bytes()
    with (out/'opened.json').open('x', encoding='utf-8') as f:
        json.dump({'utc': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(),
                   'plan_sha256': quality.digest(out/'plan.json')}, f, indent=2)
    records = {'v1': plan['reused_v1'], 'native': [], 'chrome': [], 'firefox': []}
    def progress():
        write(out/'progress.json', {k: {'done': len(v), 'valid': sum(r['status'] == 'valid' for r in v)} for k, v in records.items()})
        write(out/'records.json', records)
    cpus = Queue()
    for cpu in quality.CPUS:
        cpus.put(cpu)
    started = time.perf_counter()
    def preflight():
        assert time.perf_counter()-started < 4*3600, 'Four-hour session cap reached'
        assert guards(rows) == plan['guards']
    progress()
    try:
        preflight()
        with ThreadPoolExecutor(8) as pool:
            futures = [pool.submit(quality.native, row, seed, 60, out, cpus) for seed in SEEDS for row in rows]
            for future in as_completed(futures):
                r = future.result()
                records['native'].append({**r, 'reused': False})
                progress()
                print('native', r['job'], r['seed'], r['status'], flush=True)
        server = serve(ROOT/'web/dist')
        try:
            args = SimpleNamespace(seconds=60, concurrency=8)
            url = f'http://127.0.0.1:{server.server_address[1]}/bench.html'
            for engine in ['chrome', 'firefox']:
                for seed in SEEDS:
                    preflight()
                    batch = quality.browser(engine, seed, rows, args, out, url)
                    records[engine].extend({**r, 'reused': False} for r in batch)
                    progress()
                    print(engine, seed, 'valid', sum(r['status'] == 'valid' for r in batch), '/', len(batch), flush=True)
        finally:
            server.shutdown()
        preflight()
        selected = lambda ids: {k: [r for r in v if r['job'] in ids] for k, v in records.items()}
        full_summary = full.summarize(selected(plan['full_ids']), plan['full_ids'])
        subset_summary = quality.summarize(selected(plan['subset_ids']), subset, SEEDS, 60)
        write(out/'results.json', {'records': records, 'full_summary': full_summary, 'subset_summary': subset_summary,
            'guards_unchanged': True, 'all_quality_checks_pass': bool(full_summary['all_quality_checks_pass'] and subset_summary['passes_subset']),
            'wall_seconds': time.perf_counter()-started, 'finished_utc': datetime.now(timezone.utc).isoformat(), 'H4_complete': False})
        print('Completed current preview comparison', flush=True)
    except BaseException:
        write(out/'interruption.json', {'error': traceback.format_exc(), 'wall_seconds': time.perf_counter()-started})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    assert out.parent == ROOT/'benchmarks/results'
    (prepare if args.action == 'prepare' else measure)(out)
