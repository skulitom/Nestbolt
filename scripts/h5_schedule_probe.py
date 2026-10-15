"""Development-only probe of existing sheet search schedules and rigid pairs.

Reserve holes, disable common-line bonus, and retain all outcomes. This probes
the material shortfall on the two frozen mechanical jobs; it is not H5 evidence
for a new product implementation. No product defaults or source rings change.
Schedule arms have equal 60-second search budgets. The optional pairing probe
prepares a derived multipart job outside that budget and expands its placements
before validating/exporting the original job; it is not an equal-total-time test.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from queue import Queue
import statistics
import subprocess
import time
import traceback
import zipfile

import psutil

from cutting_development_set import ROOT, FOLDER, digest, load_cases, public_inputs, write_json
from h2_import_audit import source_digest
from h6_material_cost import run, equivalent

PROBE = ROOT/'target/release/examples/sheet_schedule.exe'
CLI = ROOT/'target/release/nestbolt.exe'
JOBS = ['m-mechanical-large-plates', 'm-mechanical-panel-hardware']


def guards():
    return {'product': source_digest(), 'probe': digest(PROBE), 'cli': digest(CLI),
            'runner': digest(Path(__file__)), 'pair_patterns': digest(ROOT/'scripts/h5_pair_patterns.py'),
            'manifest': digest(FOLDER/'manifest.json'),
            'dataset_script': digest(ROOT/'scripts/cutting_development_set.py'),
            'shared_runner': digest(ROOT/'scripts/h6_material_cost.py')}


def case(row, job, kerf, seed, warm, args, work, evidence, cpus):
    cpu = cpus.get()
    key = f"{row['id']}-k{kerf}-s{seed}-w{warm}"
    folder = work/key
    folder.mkdir()
    record = {'job': row['id'], 'job_sha256': row['sha256'], 'kerf_mm': kerf,
              'seed': seed, 'warm_fraction': warm, 'compress_fraction': args.compress,
              'window': args.window, 'seconds': args.seconds, 'cpu': cpu, 'status': 'failed'}
    try:
        derived = deepcopy(job)
        derived['clearance'] = kerf
        library, request = public_inputs(job, kerf, False)
        for name, value in [('job', derived), ('library', library), ('request', request)]:
            write_json(folder/(name+'.json'), value)
        search_job = folder/'job.json'
        patterns = None
        if args.pair_complements:
            from h5_pair_patterns import prepare
            started = time.perf_counter()
            grouped, patterns = prepare(derived)
            record['pattern_preparation_seconds_outside_search_budget'] = time.perf_counter()-started
            record['patterns'] = patterns
            search_job = folder/'grouped-job.json'
            write_json(search_job, grouped)
        command = [PROBE, search_job, folder/'nested', args.seconds, seed,
                   warm, args.compress, args.window]
        record['search'] = run(command, folder, 'search', cpu, args.seconds+60)
        assert record['search']['exit_code'] == 0, 'Search failed or timed out'
        result = json.loads((folder/'nested/result.json').read_text(encoding='utf-8'))
        layout_path = folder/'nested/layout.json'
        if patterns:
            from h5_pair_patterns import expand
            layout_path = folder/'expanded-layout.json'
            write_json(layout_path, expand(result['layout'], patterns))
        params = ['--library', folder/'library.json', '--request', folder/'request.json',
                  '--layout', layout_path]
        record['revalidation'] = run([CLI, 'validate', *params], folder, 'validate', cpu, 60)
        assert record['revalidation']['exit_code'] == 0, 'Independent validation failed'
        checked = json.loads((folder/'validate-stdout.json').read_text(encoding='utf-8'))
        assert checked['valid'] and result['validation']['valid'] and result['riders'] == 0
        # Grouped searches count rigid pairs, while the original contract counts
        # every member. Only material is comparable before expansion; all final
        # scores come from the fresh original-job validator above.
        record['maximum_metric_roundtrip_difference'] = equivalent(
            checked['metrics']['normalized_material'] if patterns else checked['metrics'],
            result['validation']['metrics']['normalized_material'] if patterns else result['validation']['metrics'],
            'normalized_material' if patterns else 'metrics')
        record['material'] = checked['metrics']['normalized_material']
        record['warm_material'] = result['warm_start']['normalized_material']
        record['history'] = result['history']
        record['stats'] = result['stats']
        record['accepted_at_seconds'] = result['accepted_at_seconds']
        record['elapsed_seconds'] = result['elapsed_seconds']
        record['export'] = run([CLI, 'export', *params, '--out-dir', folder/'export'],
                               folder, 'export', cpu, 60)
        assert record['export']['exit_code'] == 0, 'Public export failed'
        record['status'] = 'valid'
    except Exception:
        record['error'] = traceback.format_exc()
        record.pop('material', None)
    finally:
        record['artifacts'] = {p.relative_to(folder).as_posix(): digest(p)
                               for p in sorted(folder.rglob('*')) if p.is_file()}
        write_json(folder/'case.json', record)
        archive = evidence/(key+'.zip')
        with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
            for path in sorted(folder.rglob('*')):
                if path.is_file():
                    target.write(path, path.relative_to(folder).as_posix())
        record['archive'] = archive.name
        record['archive_sha256'] = digest(archive)
        cpus.put(cpu)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--warm', type=float, nargs='+', default=[0.1, 0.5, 0.85])
    parser.add_argument('--compress', type=float, default=0.25)
    parser.add_argument('--window', type=int, default=12)
    parser.add_argument('--pair-complements', action='store_true',
                        help='experimental rigid pairs; pattern preparation is outside the search budget')
    args = parser.parse_args()
    assert 0 < args.seconds <= 60 and len(set(args.warm)) == len(args.warm)
    assert all(0 <= w < 1 for w in args.warm) and 0 <= args.compress <= 1 and args.window >= 1
    selected = [(r, j) for r, j in load_cases() if r['id'] in JOBS]
    assert len(selected) == 2
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    name = ('h5-pair-probe-' if args.pair_complements else 'h5-schedule-probe-')+stamp
    work = ROOT/'output'/name
    evidence = ROOT/'benchmarks/results'/name
    work.mkdir()
    evidence.mkdir()
    for source in [Path(__file__), ROOT/'crates/core/examples/sheet_schedule.rs', ROOT/'scripts/h5_pair_patterns.py']:
        (evidence/source.name).write_bytes(source.read_bytes())
    before = guards()
    plan = {'scope': __doc__, 'started_at': stamp, 'guards': before,
            'product_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'jobs': JOBS, 'kerfs_mm': [0.2, 1.5], 'seeds': [0, 1, 2],
            'options': vars(args), 'cpus': list(range(0, 16, 2)), 'held_out_geometry_read': False}
    write_json(evidence/'plan.json', plan)
    print(json.dumps({'folder': str(evidence), 'runs': 12*len(args.warm)}), flush=True)
    # Pattern preparation and report work stay on CCD1. Each actual search and
    # validator starts suspended, pinned to its assigned CCD0 physical core.
    psutil.Process().cpu_affinity(list(range(16, 32)))
    cpus = Queue()
    for cpu in plan['cpus']:
        cpus.put(cpu)
    rows = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(case, row, job, kerf, seed, warm, args, work, evidence, cpus)
                   for row, job in selected for kerf in plan['kerfs_mm']
                   for seed in plan['seeds'] for warm in args.warm]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            write_json(evidence/'progress.json', rows)
            print(json.dumps({k: row.get(k) for k in ['job', 'kerf_mm', 'seed', 'warm_fraction', 'status', 'material']}), flush=True)
    assert before == guards(), 'Sources changed during measurement'
    rows.sort(key=lambda r: (r['job'], r['kerf_mm'], r['seed'], r['warm_fraction']))
    medians = []
    for job in JOBS:
        for kerf in plan['kerfs_mm']:
            for warm in args.warm:
                group = [r for r in rows if r['job'] == job and r['kerf_mm'] == kerf and r['warm_fraction'] == warm]
                item = {'job': job, 'kerf_mm': kerf, 'warm_fraction': warm,
                        'complete': len(group) == 3 and all(r['status'] == 'valid' for r in group)}
                if item['complete']:
                    item['material'] = statistics.median(r['material'] for r in group)
                    item['warm_material'] = statistics.median(r['warm_material'] for r in group)
                medians.append(item)
    record = {**plan, 'finished_at': datetime.now(timezone.utc).isoformat(),
              'rows': rows, 'medians': medians, 'valid': sum(r['status'] == 'valid' for r in rows), 'total': len(rows)}
    write_json(evidence/'results.json', record)
    print(json.dumps({'valid': record['valid'], 'total': record['total'], 'medians': medians}), flush=True)


if __name__ == '__main__':
    main()
