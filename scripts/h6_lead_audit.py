"""Independently check authored searched exports and their native saved starts.

Native preview lead clearance is a separate visual observation, not inferred
from the saved project (which does not contain LightBurn's computed lead paths).
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

import ezdxf
import numpy as np
from shapely.affinity import translate
from shapely.ops import unary_union
from svgpathtools import Document, parse_path

from h3_geometry_audit import normalize, product_paths
from h6_start_audit import area_sign, dxf_geometry, geometry

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['line45', 'arc45', 'arc90']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def match(rows, references, shapes, starts, threshold):
    assert len(rows) == len(shapes)
    remaining = set(range(len(shapes)))
    records = []
    for row, ref in zip(rows, references):
        i = min(remaining, key=lambda i: ref.hausdorff_distance(shapes[i]))
        remaining.remove(i)
        distance = ref.hausdorff_distance(shapes[i])
        start_error = float(np.linalg.norm(starts[i]-row['attachment_mm']))
        records.append({'copy_index': row['copy_index'], 'contour_index': row['contour_index'],
                        'matched_index': i, 'geometry_error_mm': distance,
                        'start_error_mm': start_error,
                        # DXF helper unions primitive segments, losing directed
                        # order. Only ordered SVG/native paths establish winding.
                        'winding_reversed': (area_sign(ref)*area_sign(shapes[i]) < 0
                                             if shapes[i].geom_type == 'LineString' else None),
                        'pass': max(distance, start_error) <= threshold})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    folder = args.folder.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    preparation = json.loads((folder/'preparation.json').read_text(encoding='utf-8'))
    for name, want in preparation['artifacts'].items():
        assert digest(folder/name) == want
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    scratch = ROOT/'output'/f'h6-lead-audit-{stamp}'
    normalized = scratch/'normalized'
    normalized.mkdir(parents=True)
    settings = {}
    for name in NAMES:
        source = folder/f'{name}-native.lbrn2'
        root = E.parse(source).getroot()
        layers = {int(c.find('index').get('Value')): {x.tag: x.get('Value') for x in c}
                  for c in root.findall('CutSetting')}
        settings[name] = layers
        assert layers[0]['leadIn'] == '1' and layers[0]['leadLength'] == '3'
        assert layers[0]['leadAngle'] == ('90' if name == 'arc90' else '45')
        assert layers[0]['leadStyle'] == ('line' if name == 'line45' else 'arc')
        assert layers[0].get('leadOut', '0') == layers[0].get('overcut', '0') == '0'
        assert all(layer['doOutput'] == '0' for i, layer in layers.items() if i != 0)
        assert root.find('UIPrefs/Optimize_OptimalEntryPoint').get('Value') == '0'
        assert root.find('UIPrefs/Optimize_AllowReverse').get('Value') == '1'
        xml, indices, omitted, zeros = normalize(source.read_text(encoding='utf-8'))
        assert not omitted
        normalized_root = E.fromstring(xml)
        for shape in normalized_root.findall('Shape'):
            if shape.get('CutIndex') != '0':
                normalized_root.remove(shape)
            else:
                assert shape.get('StartV') in [None, '0']
        settings[name]['normalization'] = {'leaf_count': len(indices), 'zero_handle_indices': zeros}
        (normalized/f'{name}.lbrn2').write_text(E.tostring(normalized_root, encoding='unicode'),
                                              encoding='utf-8', newline='\n')
    subprocess.run(['node', str(ROOT/'scripts/h6_lead_oracle.mjs'), str(normalized), str(scratch/'oracle')],
                   check=True, capture_output=True, timeout=30)
    results = []
    for name in NAMES:
        case = json.loads((folder/f'exports/{name}.json').read_text(encoding='utf-8'))
        rows = case['expected_contours']
        references = [geometry(product_paths({'paths': [{'curve': r['contour']}]})[0]) for r in rows]
        svg = E.parse(folder/f'exports/{name}.svg').getroot()
        group = next(g for g in svg if g.get('id') == 'CUT')
        paths = [sub for p in group for sub in parse_path(p.get('d')).continuous_subpaths()]
        height = float(svg.get('height').removesuffix('mm'))
        svg_shapes = [translate(geometry(p, flip=True), yoff=height) for p in paths]
        svg_starts = [np.array([p.start.real, height-p.start.imag]) for p in paths]
        assert all(p.isclosed() for p in paths)
        svg_rows = match(rows, references, svg_shapes, svg_starts, 0.00005)
        doc = ezdxf.readfile(folder/f'exports/{name}.dxf')
        audit = doc.audit()
        assert not audit.errors and not audit.fixes
        entities = [e for e in doc.modelspace() if e.dxf.layer == 'CUT']
        dxf = [dxf_geometry(e) for e in entities]
        assert all(closed for _, _, closed in dxf)
        dxf_rows = match(rows, references, [d[0] for d in dxf], [d[1] for d in dxf], 0.00005)
        native_paths = [sub for p in Document(scratch/f'oracle/{name}.svg').paths()
                        for sub in p.continuous_subpaths()]
        native_shapes = [geometry(p, flip=True) for p in native_paths]
        bounds = unary_union(native_shapes).bounds
        ref_bounds = unary_union(references).bounds
        shift = np.array(bounds[:2])-ref_bounds[:2]
        native_shapes = [translate(p, xoff=-shift[0], yoff=-shift[1]) for p in native_shapes]
        native_starts = [np.array([p.start.real, -p.start.imag])-shift for p in native_paths]
        native_rows = match(rows, references, native_shapes, native_starts, 0.01)
        results.append({'case': name, 'settings': settings[name], 'translation_mm': shift.tolist(),
                        'svg': svg_rows, 'dxf': dxf_rows, 'native': native_rows,
                        'pass': all(row['pass'] for row in [*svg_rows, *dxf_rows, *native_rows])})
    def flags(path):
        data = json.loads(path.read_text(encoding='utf-8'))
        return {e['automationId']: e['toggleState'] for e in data['elements'] if e['role'] == 'CheckBox'}
    original = flags(folder/'optimization-original.json')
    assert len(original) >= 10 and original == flags(folder/'optimization-restored.json')
    report = {'recorded_at': stamp, 'held_out_read': False, 'h6_complete': False,
              'native_preview_scope': 'Three screenshots require visual inspection; saved projects contain settings, not computed native leads',
              'results': results, 'pass': all(case['pass'] for case in results),
              'optimization_unchanged': True, 'script_sha256': digest(Path(__file__)),
              'oracle_sha256': digest(ROOT/'scripts/h6_lead_oracle.mjs'),
              'artifacts': {str(p.relative_to(folder)).replace('\\', '/'): digest(p)
                            for p in sorted(folder.rglob('*')) if p.is_file()}}
    target = folder/f'geometry-audit-{stamp}.json'
    target.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'report': str(target), 'pass': report['pass'],
                     'cases': [{'name': c['case'], 'pass': c['pass'],
                                'native_max_start_error_mm': max(r['start_error_mm'] for r in c['native']),
                                'native_max_geometry_error_mm': max(r['geometry_error_mm'] for r in c['native'])}
                               for c in results]}, indent=2))


if __name__ == '__main__':
    main()
