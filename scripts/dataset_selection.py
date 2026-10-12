"""Consistent frozen-case selection for competitor and Nestbolt batches/reports.

Development uses seeds 0-2 and never the ten held-out maker jobs; the final
acceptance run uses fresh seeds 1000-1004 and includes them. Each phase refuses
the other's seeds, so a development batch can never consume a final seed.
"""
import json

PHASE_SEEDS = {'development': [0, 1, 2], 'final': [1000, 1001, 1002, 1003, 1004]}


def check_seed(phase, seed):
    if phase not in PHASE_SEEDS:
        raise ValueError('Unknown phase')
    other = [s for p, seeds in PHASE_SEEDS.items() if p != phase for s in seeds]
    if seed in other or (phase == 'final' and seed not in PHASE_SEEDS['final']):
        raise ValueError(f'Seed {seed} is reserved for another phase')


def phase_cases(root, dataset, phase):
    if dataset not in ['S', 'B', 'M']:
        raise ValueError('Unknown frozen dataset')
    if phase not in PHASE_SEEDS:
        raise ValueError('Unknown phase')
    manifest = root/'benchmarks/datasets'/('makers.json' if dataset == 'M' else 'academic.json')
    rows = []
    for original in json.loads(manifest.read_bytes())['instances']:
        if original['set'] != dataset or (phase == 'development' and original.get('held_out', False)):
            continue
        row = dict(original)
        if dataset == 'M':
            # The maker manifest tracks original curves and job JSON together.
            # Retain that provenance while exposing the same job-path interface.
            path = f"M/{row['id']}.json"
            row.update(path=path, sha256=row['files'][path])
        rows.append(row)
    return manifest, sorted(rows, key=lambda row:row['id'])


def development_cases(root, dataset):
    return phase_cases(root, dataset, 'development')
