"""Reproduce the R43 training-label discrepancy without changing frozen data.

Run with the pinned .cache/shop-venv/Scripts/python.exe. The manifest split is
filtered before either source geometry or labels are read. This diagnostic is
not a new oracle, relabelling step, or H2 scoring exception.
"""
from hashlib import sha256
import json
from pathlib import Path

import ezdxf
from shapely import LineString
from shop_reference_labels import dxf_curves, topology


def main():
    root = Path(__file__).resolve().parents[1]
    corpus = root / 'benchmarks/datasets/shop'
    manifest_bytes = (corpus / 'manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    training = [f for f in manifest['files'] if f['split'] == 'training']
    row = next(f for f in training if f['path'] ==
               'real/keebio--iris-case/ecaf0a9e-iris-PE-switch-plate-mx-alps.dxf')
    source_bytes = (corpus / row['path']).read_bytes()
    label_bytes = (corpus / row['label']).read_bytes()
    assert sha256(source_bytes).hexdigest() == row['sha256']
    assert sha256(label_bytes).hexdigest() == row['label_sha256']
    doc = ezdxf.readfile(corpus / row['path'])
    curves = list(dxf_curves(doc, doc.modelspace()))
    pair = [next(c for c in curves if c['id'] == handle) for handle in ['7D', '21A']]
    assert len(pair[0]['points']) == len(pair[1]['points'])
    rounded = [dict(c, points=[(round(x, 9), round(y, 9)) for x, y in c['points']])
               for c in curves]
    report = {
        'source': row['path'], 'split': row['split'], 'held_out_read': False,
        'manifest_sha256': sha256(manifest_bytes).hexdigest(),
        'source_sha256': row['sha256'], 'label_sha256': row['label_sha256'],
        'frozen_cut_parts': json.loads(label_bytes)['cut_parts'],
        'duplicate_source_curves': pair,
        'duplicate_hausdorff_mm': LineString(pair[0]['points']).hausdorff_distance(LineString(pair[1]['points'])),
        'original_reference_topology': topology(curves),
        'diagnostic_only_rounding_mm': 1e-9,
        'rounded_reference_topology': topology(rounded),
        'H2_scoring_changed': False,
        'interpretation': 'The apparent island is a duplicate cutout bounded by sub-picometre coordinate noise. '
            'The original reference counts two nearly coincident rings as a hole and an island; rounding only '
            'this diagnostic network to 1e-9 mm yields one plate with 37 holes. Frozen labels and scoring remain unchanged.',
    }
    target = root / 'benchmarks/results/h2-r43-label-discrepancy-20261013.json'
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'report': str(target), 'duplicate_hausdorff_mm': report['duplicate_hausdorff_mm'],
                     'original_parts': len(report['original_reference_topology']['cut_parts']),
                     'rounded_parts': len(report['rounded_reference_topology']['cut_parts'])}))


if __name__ == '__main__':
    main()
