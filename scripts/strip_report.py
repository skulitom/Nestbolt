"""Audit the complete three-seed native strip development comparison."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import median
import subprocess
import uuid

from baseline_gap import audit_table
from dataset_selection import development_cases
from lbf_report import contained_file
from sparrow_io import strip_length
from svgnest import ROOT, digest, write


def summarize(rows, reference):
    groups = {}
    for row in rows:
        key = (row['job'], row['seed'])
        if key in groups:
            raise ValueError('Duplicate native strip attempt')
        groups[key] = row
    expected = {(job, seed) for job in reference for seed in [0, 1, 2]}
    if set(groups) != expected:
        raise ValueError('Missing or unexpected native strip development slot')
    result = []
    for job, comparator in sorted(reference.items()):
        attempts = [groups[(job, seed)] for seed in [0, 1, 2]]
        finite = sorted(row['result']['strip_length'] for row in attempts if row['status'] == 'valid')
        value = finite[1] if len(finite) >= 2 else None
        result.append({'job': job, 'outcomes': dict(Counter(row['status'] for row in attempts)),
                       'native_median': value, 'reference': comparator,
                       'regression_percent': None if value is None else 100 * (value / comparator['median'] - 1)})
    deltas = [row['regression_percent'] for row in result if row['regression_percent'] is not None]
    valid = all(row['status'] == 'valid' for row in rows)
    return {'rows': result, 'all_outputs_valid': valid,
            'median_regression_percent': median(deltas) if len(deltas) == len(result) else None,
            'maximum_regression_percent': max(deltas) if len(deltas) == len(result) else None,
            'development_thresholds_met': valid and len(deltas) == len(result)
                and median(deltas) <= 1.0 and max(deltas) <= 2.0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot', type=Path, action='append', required=True)
    args = parser.parse_args()
    manifest, cases = development_cases(ROOT, 'S')
    cases = {case['id']: case for case in cases}
    binary = ROOT/'target/release/nestbolt.exe'
    binary_hash = digest(binary)
    pilots, rows = [], []
    for supplied in args.pilot:
        path = contained_file(ROOT, str(supplied))
        pilot = json.loads(path.read_bytes())
        if pilot['binary_sha256'] != binary_hash or pilot['manifest_sha256'] != digest(manifest):
            raise ValueError('Re-audit requires the recorded binary and frozen manifest')
        for row in pilot['rows']:
            case = cases[row['job']]
            if row['seconds'] != 60 or row['seed'] not in [0, 1, 2] or row['job_sha256'] != case['sha256']:
                raise ValueError('Unexpected strip job, seed, budget or source hash')
            job = ROOT/'benchmarks/datasets'/case['path']
            if digest(job) != case['sha256']:
                raise ValueError('Frozen strip source changed')
            directory = contained_file(ROOT, row['directory']+'/stdout.json').parent
            for name, checksum in row['outputs'].items():
                if Path(name).name != name or digest(contained_file(directory, name)) != checksum:
                    raise ValueError('Native strip output changed')
            if row['status'] == 'valid':
                saved = json.loads((directory/'stdout.json').read_bytes())
                layout = json.loads((directory/'layout.json').read_bytes())
                if saved != row['result'] or saved['layout'] != layout or row['exit_code'] != 0:
                    raise ValueError('Native strip report differs from saved files')
                if saved['seconds'] != 60 or saved['seed'] != row['seed'] or not 0 <= saved['accepted_at_seconds'] <= 60:
                    raise ValueError('Candidate outside the declared native budget')
                check = subprocess.run([str(binary), 'validate', '--job', str(job), '--layout',
                                        str(directory/'layout.json')], capture_output=True, check=True, cwd=ROOT)
                if not json.loads(check.stdout)['valid']:
                    raise ValueError('Native strip failed independent validation')
                measured = strip_length(json.loads(job.read_bytes()), layout)
                if abs(measured-saved['strip_length']) > 1e-10 * max(1.0, abs(measured)):
                    raise ValueError('Native strip score differs from original transformed vertices')
            elif row['status'] not in ['failed', 'timeout'] or row['result'] is not None:
                raise ValueError('Unrecognized native failure or scored failure')
            rows.append(row)
        pilots.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path)})
    freeze = json.loads((ROOT/'benchmarks/baseline-target.json').read_bytes())
    plan = json.loads((ROOT/'benchmarks/matrix-plan.json').read_bytes())
    reference, tables = {}, []
    for name in freeze['tables']:
        path = ROOT/name
        table = json.loads(path.read_bytes())
        if not any(row['job'] in cases for row in table['rows']):
            continue
        for row in audit_table(path, plan):
            if row['job'] not in cases:
                continue
            stat = row['comparison_statistics']['median']
            if row['tool'] != 'sparrow' or row['seconds'] != 60 or not row['comparable_median'] or stat['state'] != 'finite':
                raise ValueError('Expected complete finite Sparrow strip reference')
            if row['job'] not in reference or stat['value'] < reference[row['job']]['median']:
                reference[row['job']] = {'settings':row['settings'], 'median':stat['value']}
        tables.append({'path':name, 'sha256':digest(path)})
    if set(reference) != set(cases):
        raise ValueError('Missing strip reference')
    result = summarize(rows, reference)
    stamp = datetime.now(timezone.utc)
    stem = f'strip-development-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    result.update(scope='Complete development S matrix: seeds 0/1/2, 60 seconds. Reference is conservatively the better finite median of Sparrow identical and upstream-default settings. This is not final-seed G3 acceptance.',
                  recorded_at=stamp.isoformat(), pilots=pilots, reference_tables=tables,
                  binary_sha256=binary_hash, script_sha256=digest(Path(__file__)), attempts=rows)
    target = ROOT/'benchmarks/results'/stem
    write(target.with_suffix('.json'), result)
    lines = ['# Native strip development comparison', '', result['scope'], '',
             f"All outputs valid: {result['all_outputs_valid']}. Development thresholds met: {result['development_thresholds_met']}.",
             f"Median regression: {result['median_regression_percent']}%. Maximum regression: {result['maximum_regression_percent']}%.", '',
             '| Job | Native median | Sparrow median | Reference settings | Regression | Outcomes |',
             '| --- | ---: | ---: | --- | ---: | --- |']
    for row in result['rows']:
        native = 'failed' if row['native_median'] is None else f"{row['native_median']:.8f}"
        delta = 'failed' if row['regression_percent'] is None else f"{row['regression_percent']:.8f}%"
        lines.append(f"| {row['job']} | {native} | {row['reference']['median']:.8f} | {row['reference']['settings']} | {delta} | {row['outcomes']} |")
    lines += ['', f'[Full precision, all attempts and audited references]({stem}.json).', '']
    with target.with_suffix('.md').open('x',encoding='utf-8',newline='\n') as f:
        f.write('\n'.join(lines))
    print(target.with_suffix('.md'))


if __name__ == '__main__':
    main()
