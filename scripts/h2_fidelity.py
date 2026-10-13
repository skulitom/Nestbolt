"""Training-only H2 export fidelity using the G6 exact-curve measurement.

Select the frozen training split before opening any source or label. Four
physical CCD0 cores, one suspended/affinity-pinned child per core. Each file
retains its options, output and result, including errors/timeouts. No builds
occur in this runner and product/batch hashes must stay unchanged throughout.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time

import psutil

from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', help='Optional training-path substring for a diagnostic pilot')
    args = parser.parse_args()
    manifest_bytes = (CORPUS/'manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    training = [r for r in manifest['files'] if r['split'] == 'training' and r.get('label')]
    rows = [r for r in training if Path(r['path']).suffix.lower() in ['.svg', '.dxf']]
    if args.only:
        rows = [r for r in rows if args.only in r['path']]
    assert rows
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT/'output'/f'h2-fidelity-{stamp}'
    work.mkdir(exist_ok=False)
    binary = ROOT/'target/release/examples/fidelity.exe'
    binary_hash = sha256(binary.read_bytes()).hexdigest()
    start_digest = source_digest()
    script_digest = sha256(Path(__file__).read_bytes()).hexdigest()

    def run(index, row):
        assert sha256((CORPUS/row['path']).read_bytes()).hexdigest() == row['sha256']
        label_bytes = (CORPUS/row['label']).read_bytes()
        assert sha256(label_bytes).hexdigest() == row['label_sha256']
        label = json.loads(label_bytes)
        options = dict(label.get('import_options', {}))
        units = options.pop('units', None)
        assert units in [None, 'mm', 'in'], units
        if units == 'in':
            options['dxf_unit'] = 25.4
        for key in ['layers', 'colors']:
            if key in options:
                options[key] = list(map(str, options[key]))
        case = work/f'{index:03}'
        case.mkdir()
        task = {'path': str(CORPUS/row['path']), 'options': options,
                'seconds': 1, 'time_limit': 240, 'output': str(case/'exports')}
        write_json(case/'task.json', task)
        start = time.perf_counter()
        proc = subprocess.Popen([str(binary), '--task', str(case/'task.json')], cwd=ROOT,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=subprocess.CREATE_NO_WINDOW | 4)
        timeout = False
        try:
            child = psutil.Process(proc.pid)
            child.cpu_affinity([2*(index % 4)])
            child.resume()
            try:
                stdout, stderr = proc.communicate(timeout=360)
            except subprocess.TimeoutExpired:
                timeout = True
                proc.kill()
                stdout, stderr = proc.communicate()
        except BaseException:
            proc.kill()
            proc.communicate()
            raise
        result = {'path': row['path'], 'set': row['set'], 'source_sha256': row['sha256'],
                  'label_sha256': row['label_sha256'], 'import_options': options,
                  'cpu': 2*(index % 4), 'elapsed_s': time.perf_counter()-start,
                  'exit_code': proc.returncode, 'stderr': stderr.decode('utf-8', errors='replace'),
                  'status': 'timeout' if timeout else 'process_error' if proc.returncode else 'measured'}
        try:
            measurement = json.loads(stdout)
            result['measurement'] = measurement
            if not timeout and proc.returncode == 0:
                result['status'] = 'rejected' if 'skipped' in measurement else 'measurement_error' if 'error' in measurement else 'measured'
                if result['status'] == 'measured':
                    distances = measurement['max_hausdorff_mm']
                    result['pass'] = measurement['all_parts_measured'] and measurement['unmatched'] == 0 and all(
                        distances.get(fmt) is not None and distances[fmt] <= .01 for fmt in ['svg', 'dxf'])
                    result['expected_parts'] = len(label['cut_parts'])
                    result['part_count_matches_label'] = measurement['parts'] == len(label['cut_parts'])
                    result['status'] = 'passed' if result['pass'] else 'fidelity_failure'
        except (ValueError, KeyError) as error:
            result['parse_error'] = str(error)
            result['stdout'] = stdout.decode('utf-8', errors='replace')[-4000:]
            if result['status'] == 'measured':
                result['status'] = 'measurement_error'
        write_json(case/'result.json', result)
        print(f"{index+1}/{len(rows)} {row['path']}: {result['status']}", flush=True)
        return result

    def batch(slot):
        return [run(i, r) for i, r in enumerate(rows) if i % 4 == slot]

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = [r for group in pool.map(batch, range(4)) for r in group]
    assert source_digest() == start_digest, 'Product sources changed during fidelity run'
    assert sha256(Path(__file__).read_bytes()).hexdigest() == script_digest
    assert sha256(binary.read_bytes()).hexdigest() == binary_hash
    results.sort(key=lambda r: r['path'])
    measured = [r for r in results if 'pass' in r]
    worst = {fmt: max((r['measurement']['max_hausdorff_mm'][fmt] for r in measured
                      if r['measurement']['max_hausdorff_mm'].get(fmt) is not None), default=None)
             for fmt in ['svg', 'dxf']}
    unbounded = {fmt: sum(r['measurement']['max_hausdorff_mm'].get(fmt) is None for r in measured)
                 for fmt in ['svg', 'dxf']}
    summary = {'recorded_at': stamp, 'scope': 'H2 training vector export fidelity; no held-out evaluation',
               'H2': False, 'held_out_read': False, 'only': args.only,
               'source_sha256': start_digest, 'binary_sha256': binary_hash, 'runner_sha256': script_digest,
               'manifest_sha256': sha256(manifest_bytes).hexdigest(), 'work_directory': str(work),
               'limit_mm': .01, 'flatten_tolerance_mm': .0005, 'seconds': 1, 'time_limit': 240,
               'external_timeout_s': 360, 'counts': dict(Counter(r['status'] for r in results)),
               'max_finite_hausdorff_mm': worst, 'unbounded_distances': unbounded,
               'contours_compared': sum(r['measurement']['rings_compared'] for r in measured),
               'native_project_training_files_pending': sum(Path(r['path']).suffix.lower() in ['.lbrn', '.lbrn2'] for r in training),
               'rows': results}
    out = ROOT/'benchmarks/results'/f'h2-fidelity-{stamp}'
    write_json(out.with_suffix('.json'), summary)
    lines = ['# H2 training vector fidelity', '',
             f"Counts: {summary['counts']}. Compared contours: {summary['contours_compared']}.",
             f'Largest finite measured distances: {worst}. Limit 0.01 mm; exact curves flattened at 0.0005 mm.', '',
             f'Unbounded/unmatched distances: {unbounded}. These remain failures, never zero-distance successes.', '',
             'Each file uses its frozen label options and byte decoding, with every imported part nested. '
             'SVG/DXF re-imports require one-to-one contour matches, including extra-contour detection. '
             'Each successful nest is independently validated. Rejections/errors/timeouts remain visible.', '',
             'This is export fidelity against the imported curves, not proof that the importer recovered '
             'every source feature. Native projects, label/cut selection and remaining H2 requirements '
             'still need separate evidence. No held-out geometry or labels were read.', '',
             '| Source | Status | SVG mm | DXF mm | Unmatched |', '| --- | --- | ---: | ---: | ---: |']
    for row in results:
        m = row.get('measurement', {})
        d = m.get('max_hausdorff_mm', {})
        lines.append(f"| {row['path']} | {row['status']} | {d.get('svg', '')} | {d.get('dxf', '')} | {m.get('unmatched', '')} |")
    out.with_suffix('.md').write_text('\n'.join(lines)+'\n', encoding='utf-8', newline='\n')
    print(out.with_suffix('.json'))


if __name__ == '__main__':
    main()
