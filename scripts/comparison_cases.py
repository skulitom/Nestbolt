"""Select the already-frozen population of a phase for an exact time budget."""
import json

from dataset_selection import phase_cases
from matrix_plan import expected


def comparison_cases(root, dataset, seconds, phase='development'):
    if seconds not in [60, 300]:
        raise ValueError('Comparison budget must be 60 or 300 seconds')
    plan = json.loads((root/'benchmarks/matrix-plan.json').read_bytes())
    if plan != expected():
        raise ValueError('Frozen comparison coverage changed')
    manifest, cases = phase_cases(root, dataset, phase)
    selected = {row['id']: row for row in plan['cases']
                if row['set'] == dataset and (phase == 'final' or not row['held_out'])
                and seconds in row['budgets_seconds']}
    rows = [row for row in cases if row['id'] in selected]
    if len(rows) != len(selected) or any(row['sha256'] != selected[row['id']]['sha256'] for row in rows):
        raise ValueError('Dataset differs from frozen comparison population')
    return manifest, rows
