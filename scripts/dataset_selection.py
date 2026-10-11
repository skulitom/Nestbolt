"""Consistent frozen-case selection for development competitor batches/reports."""
import json


def development_cases(root, dataset):
    if dataset not in ['S', 'B', 'M']:
        raise ValueError('Unknown frozen dataset')
    manifest = root/'benchmarks/datasets'/('makers.json' if dataset == 'M' else 'academic.json')
    rows = []
    for original in json.loads(manifest.read_bytes())['instances']:
        if original['set'] != dataset or original.get('held_out', False):
            continue
        row = dict(original)
        if dataset == 'M':
            # The maker manifest tracks original curves and job JSON together.
            # Retain that provenance while exposing the same job-path interface.
            path = f"M/{row['id']}.json"
            row.update(path=path, sha256=row['files'][path])
        rows.append(row)
    return manifest, sorted(rows, key=lambda row:row['id'])
