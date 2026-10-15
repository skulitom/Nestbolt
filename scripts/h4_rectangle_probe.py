"""Measure existing rectangle packing before ordinary initial construction.

Development diagnostic only: the frozen H4 letters/gears job, seeds 0-2,
with/without the existing hole grouping. Uses 3% of a 60-second budget for
rectangle operations, as the current solver does after its ordinary warm start.
No product defaults change. Every expanded layout is freshly validated.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from queue import Queue
import subprocess
import traceback
import zipfile

import psutil
from h2_import_audit import source_digest
from h6_material_cost import run, equivalent

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT/'benchmarks/results/h4-curve-native-diagnostic-20261015T155538Z'
PROBE = ROOT/'target/release/examples/rectangle_start.exe'
CLI = ROOT/'target/release/nestbolt.exe'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def guards():
    return {'product': source_digest(), 'probe': digest(PROBE), 'validator': digest(CLI),
            'runner': digest(Path(__file__)), 'shared_runner': digest(ROOT/'scripts/h6_material_cost.py'),
            'library': digest(INPUT/'library.json'), 'request': digest(INPUT/'request.json'),
            'fixture': digest(ROOT/'benchmarks/datasets/browser-curves/letters-gears-2000.svg')}


def case(seed, holes, work, evidence, cpus):
    cpu = cpus.get()
    key = f's{seed}-holes-{str(holes).lower()}'
    folder = work/key
    folder.mkdir()
    row = {'seed': seed, 'holes': holes, 'cpu': cpu, 'status': 'failed'}
    try:
        row['probe'] = run([PROBE, INPUT/'library.json', INPUT/'request.json', folder/'packed',
                            60, seed, str(holes).lower(), 0.03], folder, 'probe', cpu, 90)
        assert row['probe']['exit_code'] == 0, 'Rectangle start failed'
        row['result'] = json.loads((folder/'packed/result.json').read_text(encoding='utf-8'))
        row['check'] = run([CLI, 'validate', '--library', INPUT/'library.json',
                            '--request', INPUT/'request.json', '--layout', folder/'packed/layout.json'],
                           folder, 'validate', cpu, 90)
        assert row['check']['exit_code'] == 0, 'Fresh original-geometry validation failed'
        checked = json.loads((folder/'validate-stdout.json').read_text(encoding='utf-8'))
        assert checked['valid'] and row['result']['validation']['valid']
        assert checked['metrics']['placed_parts'] == checked['metrics']['requested_parts'] == 2000
        row['maximum_metric_difference'] = equivalent(checked['metrics'], row['result']['validation']['metrics'])
        row['material'] = checked['metrics']['normalized_material']
        row['within_60_seconds'] = row['result']['total_seconds'] <= 60
        row['status'] = 'valid'
    except Exception:
        row['error'] = traceback.format_exc()
    finally:
        row['artifacts'] = {p.relative_to(folder).as_posix(): digest(p)
                            for p in sorted(folder.rglob('*')) if p.is_file()}
        write(folder/'case.json', row)
        archive = evidence/(key+'.zip')
        with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as target:
            for path in sorted(folder.rglob('*')):
                if path.is_file():
                    target.write(path, path.relative_to(folder).as_posix())
        row['archive'] = archive.name
        row['archive_sha256'] = digest(archive)
        cpus.put(cpu)
    return row


def main():
    psutil.Process().cpu_affinity(list(range(16, 32)))
    name = 'h4-rectangle-probe-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work, out = ROOT/'output'/name, ROOT/'benchmarks/results'/name
    work.mkdir()
    out.mkdir()
    before = guards()
    plan = {'scope': __doc__, 'baseline_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'guards': before, 'seconds': 60, 'rectangle_share': 0.03, 'seeds': [0, 1, 2],
            'cpus': list(range(0, 12, 2)), 'held_out_geometry_read': False}
    write(out/'plan.json', plan)
    for source in [Path(__file__), ROOT/'crates/core/examples/rectangle_start.rs']:
        (out/source.name).write_bytes(source.read_bytes())
    cpus = Queue()
    for cpu in plan['cpus']:
        cpus.put(cpu)
    rows = []
    print(json.dumps({'folder': str(out)}), flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(case, seed, holes, work, out, cpus)
                   for holes in [False, True] for seed in plan['seeds']]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            write(out/'progress.json', rows)
            print(json.dumps({k: row.get(k) for k in ['seed', 'holes', 'status', 'material', 'within_60_seconds']}), flush=True)
    assert before == guards(), 'Sources changed during measurement'
    write(out/'results.json', {**plan, 'results': sorted(rows, key=lambda r: (r['holes'], r['seed']))})


if __name__ == '__main__':
    main()
