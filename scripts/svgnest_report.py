"""Verify immutable SVGnest evidence before retaining a provisional baseline table."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from svgnest import ROOT, digest, write
from lbf_report import contained_file


def audit_record(path, expected_hash):
    if digest(path) != expected_hash:
        raise ValueError('Run record changed')
    run = json.loads(path.read_bytes())
    for name, checksum in run['outputs'].items():
        if digest(contained_file(path.parent, name)) != checksum:
            raise ValueError('Recorded output changed')
    if digest(path.parent / 'job.json') != run['job_sha256']:
        raise ValueError('Copied source job changed')
    if run['status'] == 'valid':
        if run.get('output_decoding') != 'native_svg_attributes_v2':
            raise ValueError('Legacy browser-matrix decode requires correction from saved native SVG attributes')
        required = {'job.json', 'layout.json', 'validation.json', 'request.json', 'browser-result.json', 'candidates.jsonl'}
        if not required.issubset(run['outputs']):
            raise ValueError('Valid run is missing independent evidence')
        checked = json.loads((path.parent / 'validation.json').read_bytes())
        raw = json.loads((path.parent / 'browser-result.json').read_bytes())
        if run.get('input_encoding') == 'linear_svg_paths_v2':
            proof = raw.get('input_fidelity')
            if not proof or proof != run.get('input_fidelity') or proof.get('encoding') != run['input_encoding'] or proof.get('maximum_absolute_error') != 0 or proof.get('coordinates',0) < 6:
                raise ValueError('Native input fidelity was not verified')
        if not checked['valid'] or run['validator_exit_code'] != 0 or run['metrics'] != checked['metrics'] or run['score'] != checked['metrics']['normalized_material']:
            raise ValueError('Recorded score differs from independent validation')
        if raw['status'] != 'completed' or raw['errors'] or raw['last']['elapsed_ms'] > run['seconds'] * 1000:
            raise ValueError('Native result is incomplete or exceeded its budget')
        affinity = raw['affinity']
        expected = affinity.get('mask', affinity.get('cpu'))
        evidence = raw.get('affinity_verification', [])
        if raw['configured_workers'] != 1 or len(evidence) < 2 or any(p['affinity'] != expected for p in evidence):
            raise ValueError('Run lacks a verified single-core process tree')
        if affinity['platform'] == 'win32' and affinity.get('method') != 'JOB_OBJECT_LIMIT_AFFINITY':
            raise ValueError('Run lacks enforced Windows process-tree affinity')
        if run['affinity_verification'] != evidence or run['cpu_affinity'] != affinity:
            raise ValueError('Run CPU provenance differs from native evidence')
    elif run['score'] is not None or run.get('metrics') is not None:
        raise ValueError('Failed or unsupported run cannot receive a score')
    return run


def report(path):
    batch = json.loads(path.read_bytes())
    manifest = ROOT / 'benchmarks/datasets/academic.json'
    if digest(manifest) != batch['dataset_manifest_sha256']:
        raise ValueError('Dataset manifest changed')
    frozen = {r['id']: r for r in json.loads(manifest.read_bytes())['instances'] if r['set'] == 'B'}
    selected = {r['id']: r for r in batch['cases']}
    if len(selected) != len(batch['cases']) or any(frozen.get(k) != v for k, v in selected.items()):
        raise ValueError('Unexpected or duplicate frozen batch case')
    rows, seen = [], set()
    for entry in batch['runs']:
        key = entry['job']
        if key not in selected or key in seen:
            raise ValueError('Unexpected or duplicate run')
        source = ROOT / 'benchmarks/datasets' / selected[key]['path']
        if digest(source) != selected[key]['sha256']:
            raise ValueError('Frozen job source changed')
        record_path = contained_file(ROOT, entry['record'])
        if not record_path.is_relative_to((ROOT / 'output/playwright/svgnest').resolve()):
            raise ValueError('Run record is outside the SVGnest evidence directory')
        run = audit_record(record_path, entry['sha256'])
        for name in ['seed', 'seconds', 'settings', 'axis', 'sources']:
            if run[name] != batch[name]:
                raise ValueError(f'Run differs from frozen batch: {name}')
        if run['job'] != key or run['job_sha256'] != selected[key]['sha256'] or run['status'] != entry['status']:
            raise ValueError('Run does not match the declared source/outcome')
        seen.add(key)
        rows.append({**entry, 'run': run})
    if not batch['complete'] or seen != set(selected):
        raise ValueError('Incomplete selected batch')
    stamp = datetime.now(timezone.utc)
    checkpoint = {'recorded_at': stamp.isoformat(), 'kind': batch['kind'],
        'scope': f'Provisional single-seed SVGnest baseline for {len(selected)} of 35 B jobs; not M1 or a Nestbolt quality gate.',
        'batch_sha256': digest(path), 'batch': batch, 'rows': rows}
    stem = f'svgnest-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    output = ROOT / 'benchmarks/results' / stem
    write(output.with_suffix('.json'), checkpoint)
    lines = ['# Provisional SVGnest baseline', '', checkpoint['scope'], '',
        f"Seed {batch['seed']}, {batch['seconds']} s, {batch['settings']}, axis {batch['axis']}; single core and one worker.", '',
        'Failures and unsupported cases receive no score. Lower normalized material is better.', '',
        '| Job | Status | Sheets | Material |', '| --- | --- | ---: | ---: |']
    for row in rows:
        run = row['run']
        values = f"{run['metrics']['sheets_used']} | {run['score']:.6f}" if run['status'] == 'valid' else '— | —'
        lines.append(f"| {row['job']} | {run['status']} | {values} |")
    lines.extend(['', f'[Verified records and full precision]({stem}.json).', ''])
    with output.with_suffix('.md').open('x', encoding='utf-8', newline='\n') as file:
        file.write('\n'.join(lines))
    with (ROOT / 'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as file:
        file.write(f'\n- {stamp.isoformat()} | verified SVGnest batch `{batch["batch_id"]}` | '
                   f'{len(rows)} selected B outcomes retained | [table](benchmarks/results/{stem}.md). Provisional; full M1 and all quality gates pending.\n')
    print(output.with_suffix('.md'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', required=True, type=Path)
    report(parser.parse_args().batch.resolve(strict=True))
