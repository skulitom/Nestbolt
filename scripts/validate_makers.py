"""Prove maker source feasibility without performing any nesting optimisation."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / 'output/maker-candidates'


def witness(job):
    # Deliberately wasteful authoring proof: one copy per unlimited full sheet.
    # It is never a baseline, quality score or optimiser-tuning observation.
    stock = max((s for s in job['stocks'] if s['count'] is None and not s['outline']),
                key=lambda s: s['width'] * s['height'])
    layout = {'version': 1, 'units': 'mm', 'sheets': [], 'placements': []}
    for part in job['parts']:
        for copy in range(part['quantity']):
            sheet = f'authoring-{len(layout["sheets"])}'
            layout['sheets'].append({'id': sheet, 'stock_id': stock['id']})
            layout['placements'].append({'part_id': part['id'], 'copy_index': copy, 'sheet_id': sheet,
                'transform': {'translation': [stock['margins']['left'] + job['edge_clearance'],
                                              stock['margins']['bottom'] + job['edge_clearance']],
                              'rotation_radians': 0, 'mirrored': False}})
    return layout


def main():
    subprocess.run(['cargo', 'build', '--locked', '-p', 'nestbolt-cli'], cwd=ROOT, check=True)
    binary = ROOT / 'target/debug' / ('nestbolt.exe' if os.name == 'nt' else 'nestbolt')
    dest = ROOT / 'output/maker-source-validation'
    dest.mkdir(parents=True, exist_ok=True)
    rows = []
    for row in json.loads((CANDIDATES / 'candidates.json').read_bytes())['instances']:
        job_path = CANDIDATES / row['id'] / 'job.json'
        job = json.loads(job_path.read_bytes())
        layout = witness(job)
        layout_path = dest / (row['id'] + '-layout.json')
        layout_path.write_text(json.dumps(layout) + '\n', encoding='utf-8', newline='\n')
        completed = subprocess.run([str(binary), 'validate', '--job', str(job_path), '--layout', str(layout_path)],
                                   capture_output=True, cwd=ROOT, check=True)
        report = json.loads(completed.stdout)
        if not report['valid']:
            raise ValueError(row['id'] + ' failed source feasibility')
        rows.append({'id': row['id'], 'job_sha256': sha256(job_path.read_bytes()).hexdigest(),
                     'witness_sha256': sha256(layout_path.read_bytes()).hexdigest(), 'validation': report})
    (dest / 'report.json').write_text(json.dumps({'purpose': 'Source feasibility only. One copy per sheet; no optimisation, benchmark comparison or tuning.',
        'validator_sha256': sha256(binary.read_bytes()).hexdigest(), 'instances': rows}, indent=2) + '\n',
        encoding='utf-8', newline='\n')
    print(f'Independent source-feasibility proofs: {len(rows)}/{len(rows)} valid.')


if __name__ == '__main__':
    main()
