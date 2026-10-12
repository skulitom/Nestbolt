"""Retain audited comparator batches; incomplete matrices cannot pass."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from deepnest_report import audit_record as audit_deepnest
from sparrow_report import audit_record as audit_sparrow
from svgnest_report import audit_record as audit_svgnest
from lbf_report import contained_file
from dataset_selection import phase_cases
from svgnest import ROOT, digest, write

TOOLS = {'deepnest': ('output/playwright/deepnest', audit_deepnest),
         'svgnest': ('output/playwright/svgnest', audit_svgnest),
         'sparrow': ('output/sparrow-benchmark', audit_sparrow)}


def audit_batch(path, tool):
    directory, audit_record = TOOLS[tool]
    batch = json.loads(path.read_bytes())
    if batch['dataset'] not in ['S', 'B', 'M'] or (tool != 'sparrow' and batch['dataset'] == 'S'):
        raise ValueError('Unexpected dataset for this runner')
    phase = batch.get('phase', 'development')
    manifest, cases = phase_cases(ROOT, batch['dataset'], phase)
    if digest(manifest) != batch['dataset_manifest_sha256']:
        raise ValueError('Frozen dataset manifest changed')
    frozen = {r['id']:r for r in cases}
    selected = {r['id']:r for r in batch['cases']}
    if not selected or len(selected) != len(batch['cases']) or any(frozen.get(k) != v for k,v in selected.items()):
        raise ValueError('Unexpected, empty or duplicate frozen case selection')
    rows, seen = [], set()
    for entry in batch['runs']:
        key = entry['job']
        if key not in selected or key in seen:
            raise ValueError('Unexpected or duplicate run')
        source = contained_file(ROOT/'benchmarks/datasets', selected[key]['path'])
        if digest(source) != selected[key]['sha256']:
            raise ValueError('Frozen source changed')
        record_path = contained_file(ROOT, entry['record'])
        if not record_path.is_relative_to((ROOT/directory).resolve()):
            raise ValueError('Run is outside this comparator evidence directory')
        run = audit_record(record_path, entry['sha256'])
        if 'validator_snapshot' in batch:
            snapshot = batch['validator_snapshot']
            if 'validator_sha256' not in run and run['status'] in ['unsupported', 'failed']:
                pass  # Input preparation can fail before any checker is invoked.
            elif run.get('validator_sha256') != snapshot['sha256'] or run.get('validator_sources') != snapshot['sources']:
                raise ValueError('Run used a different validator than the batch snapshot')
        for name in ['seconds', 'seed', 'settings', 'axis', 'sources']:
            if run[name] != batch[name]:
                raise ValueError(f'Run differs from declared batch: {name}')
        if run.get('phase', 'development') != phase:
            raise ValueError('Run phase differs from its batch')
        if run['job'] != key or run['job_sha256'] != selected[key]['sha256'] or run['status'] != entry['status']:
            raise ValueError('Run identity or status differs from its batch entry')
        seen.add(key)
        validation = record_path.parent/'validation.json'
        rows.append({**entry, 'run':run, 'validation':json.loads(validation.read_bytes()) if validation.exists() else None})
    if not batch['complete'] or seen != set(selected):
        raise ValueError('Incomplete selected matrix')
    if batch['valid_runs'] != sum(row['run']['status'] == 'valid' for row in rows):
        raise ValueError('Incorrect valid-outcome count')
    return batch, rows


def report(path, tool):
    batch, rows = audit_batch(path, tool)
    stamp = datetime.now(timezone.utc)
    stem = f'{tool}-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    target = ROOT/'benchmarks/results'/stem
    scope = f'Provisional {tool} pilot: {len(rows)} {batch["dataset"]} jobs, one configuration and seed; no milestone or quality gate.'
    checkpoint = {'recorded_at':stamp.isoformat(), 'scope':scope, 'batch_sha256':digest(path), 'batch':batch, 'rows':rows}
    write(target.with_suffix('.json'), checkpoint)
    lines = [f'# Provisional {tool} baseline', '', scope, '',
             f"Seed {batch['seed']}, {batch['seconds']} s, {batch['settings']}, axis {batch['axis']}.", '',
             'Failures receive no score. Each row names its metric; lower is better.', '',
             '| Job | Status | Metric | Score |', '| --- | --- | --- | ---: |']
    for row in rows:
        run = row['run']
        metric = run.get('score_kind', 'normalized_material') if run['status'] == 'valid' else '—'
        score = f"{run['score']:.8f}" if run['status'] == 'valid' else '—'
        lines.append(f"| {row['job']} | {run['status']} | {metric} | {score} |")
    lines.extend(['', f'[Audited records and full precision]({stem}.json).', ''])
    with target.with_suffix('.md').open('x', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))
    with (ROOT/'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as f:
        f.write(f'\n- {stamp.isoformat()} | verified {tool} batch `{batch["batch_id"]}` | {batch["valid_runs"]}/{len(rows)} valid | [table](benchmarks/results/{stem}.md). Provisional; all failures retained.\n')
    print(target.with_suffix('.md'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tool', choices=TOOLS, required=True)
    parser.add_argument('--batch', type=Path, required=True)
    args = parser.parse_args()
    report(args.batch.resolve(strict=True), args.tool)
