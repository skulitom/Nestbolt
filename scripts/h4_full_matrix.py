"""Complete H4 development quality and native parity, never final acceptance.

Exactly 65 development jobs, seeds 0-2, 60 seconds. Reuse the matching nine-job
portion of the completed a977279 subset after checking its archived evidence.
Measure frozen 75cbb32 on all 195 development cases; do not substitute final
seeds or the older M4 binary. At most eight physical CCD0 lanes. Prepare and
commit the plan before `run`; an opened marker refuses automatic repetition.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
import os
from pathlib import Path
from queue import Queue
import shutil
import statistics
import subprocess
import time
import traceback
from types import SimpleNamespace
import zipfile

import h4_quality as quality
from g5_browser import serve
from h6_material_cost import run as execute
from sheets_batch import select_cases

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT/'output/bin/nestbolt-final-75cbb32.exe'
BASELINE_SHA = '1dd58ac0ef3347af878271f888b7c326045961ba9d959cc4743acbce04b526de'
REUSE = ROOT/'benchmarks/results/h4-quality-20261015T215607Z'
ARCHIVE = ROOT/'benchmarks/results/h4-score-pruning-20261015/raw.zip'
INTEGRITY = ARCHIVE.with_name('integrity.json')
ENGINES = ['v1', 'native', 'chrome', 'firefox']
SEEDS = [0, 1, 2]
OVERRIDES = ['NESTBOLT_SIMPLIFY', 'NESTBOLT_NO_FILL', 'NESTBOLT_DEBUG',
             'NESTBOLT_TRACE', 'RUSTFLAGS', 'CARGO_PROFILE_RELEASE_LTO']


def load(path):
    return json.loads(path.read_bytes())


def write(path, value):
    temporary = path.with_name(path.name+'.tmp')
    temporary.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')
    temporary.replace(path)


def cases():
    rows = [{**r, 'path': 'benchmarks/datasets/'+r['path']} for r in select_cases()]
    assert len(rows) == 65 and not any(r.get('held_out') for r in rows)
    assert len({r['id'] for r in rows}) == 65
    for row in rows:
        assert quality.digest(ROOT/row['path']) == row['sha256']
    return rows


def guards(rows):
    result = quality.guards(rows)
    for p in [Path(__file__), ROOT/'scripts/test_h4_full_matrix.py', BASELINE,
              REUSE/'plan.json', REUSE/'results.json', ARCHIVE, INTEGRITY]:
        result['files'][p.relative_to(ROOT).as_posix()] = quality.digest(p)
    result['environment'] = {k: os.environ.get(k) for k in OVERRIDES}
    assert all(v is None for v in result['environment'].values())
    assert quality.digest(BASELINE) == BASELINE_SHA
    return result


def reuse(rows):
    """Use only byte-verified, complete evidence from this exact product/build."""
    prior_plan, prior = load(REUSE/'plan.json'), load(REUSE/'results.json')
    current = quality.guards(rows)
    assert current['product'] == prior_plan['guards']['product']
    for name, expected in prior_plan['guards']['files'].items():
        assert quality.digest(ROOT/name) == expected, name
    assert prior_plan['seconds'] == 60 and prior_plan['seeds'] == SEEDS
    assert prior['summary']['guards_unchanged'] and prior['summary']['passes_subset']
    known = {r['id']: r for r in rows}
    selected = {r['id'] for r in prior_plan['cases']} & set(known)
    assert selected == set(quality.SUBSET) and len(selected) == 9
    for r in prior_plan['cases']:
        if r['id'] in selected:
            assert r['sha256'] == known[r['id']]['sha256']
    inventory = load(INTEGRITY)
    assert quality.digest(ARCHIVE) == inventory['sha256']
    records = {name: [] for name in ENGINES}
    with zipfile.ZipFile(ARCHIVE) as z:
        for name in ['plan.json', 'results.json']:
            assert z.read((REUSE/name).relative_to(ROOT).as_posix()) == (REUSE/name).read_bytes()
        for engine in ENGINES[1:]:
            for record in prior['records'][engine]:
                if record['job'] not in selected:
                    continue
                folder = record['directory']
                files = ['layout.json', 'validate-stdout.json', 'case.json',
                         'search-stdout.json' if engine == 'native' else 'result.json']
                verified = {}
                for name in files:
                    member = folder+'/'+name
                    raw = z.read(member)
                    assert sha256(raw).hexdigest() == inventory['members'][member]['sha256']
                    verified[name] = json.loads(raw)
                assert verified['case.json'] == record and record['status'] == 'valid'
                assert verified['validate-stdout.json']['valid']
                assert verified['validate-stdout.json']['metrics']['normalized_material'] == record['material']
                assert len(verified['layout.json']['placements']) == sum(
                    p['quantity'] for p in load(ROOT/known[record['job']]['path'])['parts'])
                assert sha256(z.read(folder+'/layout.json')).hexdigest() == record['layout_sha256']
                records[engine].append({**record, 'reused': True,
                    'source_archive': ARCHIVE.relative_to(ROOT).as_posix()})
            assert len(records[engine]) == 27
            assert {(r['job'], r['seed']) for r in records[engine]} == {
                (name, seed) for name in selected for seed in SEEDS}
    return records, selected


def summarize(records, ids):
    """No missing, duplicate or failed attempt may receive acceptance credit."""
    ids = list(ids)
    expected = {(name, seed) for name in ids for seed in SEEDS}
    complete, medians, failures = {}, {}, {}
    for engine in ENGINES:
        group = records.get(engine, [])
        identities = [(r['job'], r['seed']) for r in group]
        complete[engine] = (len(identities) == len(expected) and set(identities) == expected)
        failures[engine] = sum(r.get('status') != 'valid' or not isinstance(r.get('material'), (int, float))
                               or not math.isfinite(r['material']) or r['material'] <= 0 for r in group)
        medians[engine] = {}
        for name in ids:
            attempts = [r for r in group if r['job'] == name]
            valid = (len(attempts) == 3 and sorted(r['seed'] for r in attempts) == SEEDS
                and all(r.get('status') == 'valid' and isinstance(r.get('material'), (int, float))
                        and math.isfinite(r['material']) and r['material'] > 0 for r in attempts))
            medians[engine][name] = statistics.median(r['material'] for r in attempts) if valid else None

    def compare(a, b):
        values = {name: 100*(a[name]/b[name]-1) if a[name] is not None and b[name] is not None
                  else None for name in ids}
        valid = all(v is not None for v in values.values())
        return {'per_job_difference_percent': values,
            'median_difference_percent': statistics.median(values.values()) if valid else None,
            'total_difference_percent': 100*(sum(a.values())/sum(b.values())-1) if valid else None,
            'worst_difference_percent': max(values.values()) if valid else None,
            'complete': valid}

    native = compare(medians['native'], medians['v1'])
    native['passes'] = (complete['v1'] and complete['native'] and not failures['v1']
        and not failures['native'] and native['complete'] and native['median_difference_percent'] <= .5)
    browsers = {}
    for engine in ['chrome', 'firefox']:
        result = compare(medians[engine], medians['native'])
        per_seed = {}
        for seed in SEEDS:
            def values_for(eng):
                attempts = [r for r in records.get(eng, []) if r['seed'] == seed]
                if len(attempts) != len(ids) or {r['job'] for r in attempts} != set(ids):
                    return dict.fromkeys(ids)
                return {r['job']: r.get('material') if r.get('status') == 'valid'
                        and isinstance(r.get('material'), (int, float)) and math.isfinite(r['material'])
                        and r['material'] > 0 else None for r in attempts}
            per_seed[seed] = compare(values_for(engine), values_for('native'))
            s = per_seed[seed]
            s['within_original_G5_bounds'] = bool(s['complete'] and s['median_difference_percent'] <= 2
                                                   and s['total_difference_percent'] <= 2)
        result['per_seed'] = per_seed
        result['passes_aggregate_bounds'] = (complete[engine] and complete['native']
            and not failures[engine] and not failures['native'] and result['complete']
            and result['median_difference_percent'] <= 2 and result['total_difference_percent'] <= 2)
        # Also retain each original G5 single-seed comparison; no seed is dropped.
        result['all_seeds_within_original_G5_bounds'] = all(s['within_original_G5_bounds'] for s in per_seed.values())
        browsers[engine] = result
    return {'attempt_coverage_complete': complete, 'failed_attempts': failures,
        'medians': medians, 'native_vs_v1': native, 'browsers_vs_native': browsers,
        'all_quality_checks_pass': bool(native['passes'] and all(
            r['passes_aggregate_bounds'] and r['all_seeds_within_original_G5_bounds'] for r in browsers.values())),
        'H4_complete': False, 'scale_and_complete_requirement_audit_needed': True}


def native(row, seed, engine, out, cpus):
    cpu = cpus.get()
    folder = out/engine/f's{seed}'/row['id']
    folder.mkdir(parents=True)
    binary = BASELINE if engine == 'v1' else quality.CLI
    record = {'job': row['id'], 'seed': seed, 'status': 'failed', 'cpu': cpu,
        'reused': False, 'directory': folder.relative_to(ROOT).as_posix()}
    try:
        record['run'] = execute([binary, 'sheets', '--job', ROOT/row['path'], '--output', folder/'layout.json',
            '--seconds', 60, '--seed', seed], folder, 'search', cpu, 150)
        assert record['run']['exit_code'] == 0, 'Native search failed'
        result = load(folder/'search-stdout.json')
        record.update(quality.check(row, folder, cpu, result))
    except Exception:
        record['error'] = traceback.format_exc()
    finally:
        cpus.put(cpu)
    write(folder/'case.json', record)
    return record


def prepare(out):
    rows = cases()
    records, reused = reuse(rows)
    out.mkdir()
    before = guards(rows)
    plan = {'scope': __doc__, 'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'cases': rows, 'seeds': SEEDS, 'seconds': 60, 'cpus': quality.CPUS,
        'concurrency': 8, 'guards': before, 'baseline_sha256': BASELINE_SHA,
        'reused_jobs': sorted(reused), 'reused_records': records,
        'new_attempts': {'v1': 195, 'native': 168, 'chrome': 168, 'firefox': 168},
        'gates': {'native_median_limit_percent': .5, 'G5_median_limit_percent': 2,
                  'G5_total_limit_percent': 2, 'all_layouts_valid': True},
        'per_seed_G5_checks': 'Report and check all three original single-seed median/total comparisons in addition to per-job three-seed medians.',
        'held_out_geometry_read': False, 'published_final_results_changed': False}
    write(out/'plan.json', plan)
    for name in ['scripts/h4_full_matrix.py', 'scripts/test_h4_full_matrix.py', 'scripts/h4_quality.py',
                 'scripts/h6_material_cost.py', 'scripts/g5_browser.py', 'web/bench/run.mjs']:
        target = out/'snapshots'/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    print(json.dumps({'prepared': str(out), 'new_attempts': plan['new_attempts'], 'reused_attempts': 81}), flush=True)


def measure(out):
    plan = load(out/'plan.json')
    rows = cases()
    assert rows == plan['cases'] and guards(rows) == plan['guards']
    relative = (out/'plan.json').relative_to(ROOT).as_posix()
    assert subprocess.check_output(['git', 'show', 'HEAD:'+relative], cwd=ROOT) == (out/'plan.json').read_bytes(), 'Commit the frozen plan before measuring'
    with (out/'opened.json').open('x', encoding='utf-8') as f:
        json.dump({'started_utc': datetime.now(timezone.utc).isoformat(), 'pid': os.getpid(),
                   'plan_sha256': quality.digest(out/'plan.json')}, f, indent=2)
    records = plan['reused_records']
    remaining = [r for r in rows if r['id'] not in plan['reused_jobs']]
    assert len(remaining) == 56
    def progress():
        write(out/'progress.json', {k: {'done': len(v), 'valid': sum(r['status']=='valid' for r in v),
            'reused': sum(r.get('reused', False) for r in v)} for k,v in records.items()})
        write(out/'records.json', records)
    cpus = Queue()
    for cpu in quality.CPUS:
        cpus.put(cpu)
    started = time.perf_counter()
    progress()
    try:
        for engine, selected in [('v1', rows), ('native', remaining)]:
            assert guards(rows) == plan['guards']
            with ThreadPoolExecutor(8) as pool:
                futures = [pool.submit(native, row, seed, engine, out, cpus) for seed in SEEDS for row in selected]
                for future in as_completed(futures):
                    result = future.result()
                    records[engine].append(result)
                    progress()
                    print(engine, result['job'], result['seed'], result['status'], flush=True)
        server = serve(ROOT/'web/dist')
        try:
            url = f'http://127.0.0.1:{server.server_address[1]}/bench.html'
            args = SimpleNamespace(seconds=60, concurrency=8)
            for engine in ['chrome', 'firefox']:
                for seed in SEEDS:
                    assert guards(rows) == plan['guards']
                    batch = quality.browser(engine, seed, remaining, args, out, url)
                    records[engine].extend({**r, 'reused': False} for r in batch)
                    progress()
                    print(engine, seed, 'valid', sum(r['status']=='valid' for r in batch), '/', len(batch), flush=True)
        finally:
            server.shutdown()
        unchanged = guards(rows) == plan['guards']
        summary = summarize(records, [r['id'] for r in rows])
        summary['guards_unchanged'] = unchanged
        summary['all_quality_checks_pass'] &= unchanged
        write(out/'results.json', {'records': records, 'summary': summary,
            'wall_seconds': time.perf_counter()-started, 'finished_utc': datetime.now(timezone.utc).isoformat()})
        assert unchanged
        print(json.dumps({'completed': str(out), 'all_quality_checks_pass': summary['all_quality_checks_pass']}), flush=True)
    except BaseException:
        write(out/'interruption.json', {'error': traceback.format_exc(), 'wall_seconds': time.perf_counter()-started})
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    assert out.parent == ROOT/'benchmarks/results'
    (prepare if args.action == 'prepare' else measure)(out)


if __name__ == '__main__':
    main()
