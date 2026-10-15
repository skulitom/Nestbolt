"""Independent geometry/settings and bounded raster checks of authored native leads."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, map_coordinates
from shapely.affinity import translate
from shapely.ops import unary_union
from svgpathtools import Document, parse_path

from h3_geometry_audit import normalize
from h6_start_audit import geometry
ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def raster_check(folder, style, report, layout, references):
    # Original 1920x1080 Anode screenshots, manually observed panel corners.
    # No pixels are edited. Eight corners establish scale and translation.
    corners = {'line': [(161, 326, 941, 716), (1062, 326, 1841, 716)],
               'arc': [(123, 334, 920, 733), (1044, 334, 1841, 733)]}[style]
    world, pixels = [], []
    for shape, (left, top, right, bottom) in zip(references[::3], corners):
        x0, y0, x1, y1 = shape.bounds
        world.extend([(x0, y1), (x1, y1), (x0, y0), (x1, y0)])
        pixels.extend([(left, top), (right, top), (left, bottom), (right, bottom)])
    world, pixels = np.array(world), np.array(pixels)
    ax = np.linalg.lstsq(np.column_stack([world[:, 0], np.ones(8)]), pixels[:, 0], rcond=None)[0]
    ay = np.linalg.lstsq(np.column_stack([world[:, 1], np.ones(8)]), pixels[:, 1], rcond=None)[0]
    scale = min(abs(ax[0]), abs(ay[0]))
    rgb = np.asarray(Image.open(folder/f'{style}-native-preview.png').convert('RGB')).astype(int)
    assert rgb.shape == (1080, 1920, 3)
    # A red traversal over a black cut is dark red (observed 110,57,57),
    # not neutral gray. Traversal alone is lighter (181,127,127). Keep
    # dark cut pixels even at those crossings; do not count red travel alone.
    dark = rgb.max(axis=2) < 170
    distance = distance_transform_edt(~dark)
    rows = []
    for part, placement in zip(report['lead_in']['parts'], layout['placements']):
        transform = placement['transform']
        assert transform['rotation_radians'] == 0 and not transform['mirrored']
        offset = np.array(transform['translation'])
        for reservation in part['reservations']:
            directions = []
            for path in reservation['paths']:
                t = np.linspace(0, 1, 101)
                if path['kind'] == 'line':
                    a, b = np.array(path['from_mm']), np.array(path['to_mm'])
                    points = a + t[:, None]*(b-a)
                else:
                    angles = path['start_radians']+t*path['sweep_radians']
                    points = np.array(path['center_mm']) + path['radius_mm']*np.column_stack([np.cos(angles), np.sin(angles)])
                points += offset
                xx, yy = ax[0]*points[:, 0]+ax[1], ay[0]*points[:, 1]+ay[1]
                assert xx.min() >= 0 and yy.min() >= 0 and xx.max() < 1920 and yy.max() < 1080
                errors = map_coordinates(distance, [yy, xx], order=1)/scale
                directions.append(float(errors.max()))
            rows.append({'copy_index': part['copy_index'], 'contour_index': reservation['contour_index'],
                         'maximum_pixel_distance_mm_by_direction': directions,
                         'matching_direction': int(np.argmin(directions)),
                         'pass': min(directions) <= 0.075})
    return {'raster_tolerance_mm': 0.075, 'observed_panel_corners_pixels': corners,
            'pixels_per_mm': [float(ax[0]), float(-ay[0])], 'leads': rows,
            'scope': 'Expected lead samples versus native dark pixels; supports visual inspection, not a vector clearance gate',
            'pass': all(r['pass'] for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    folder = parser.parse_args().folder.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    for prep in [folder/'preparation.json', folder/'revised-2/preparation.json']:
        for path, want in json.loads(prep.read_text(encoding='utf-8'))['artifacts'].items():
            assert digest(folder/path) == want
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    scratch = ROOT/'output'/f'h6-settings-audit-{stamp}'
    normalized = scratch/'normalized'
    normalized.mkdir(parents=True)
    settings, native_indices = {}, {}
    for style in ['line', 'arc']:
        source = folder/f'{style}-native.lbrn2'
        root = E.parse(source).getroot()
        layers = {int(c.find('index').get('Value')): {x.tag: x.get('Value') for x in c}
                  for c in root.findall('CutSetting')}
        assert set(layers) == {0, 3, 4}
        for index, length, angle in [(0, 3, 45), (4, 1.7 if style == 'line' else 1.2, -90)]:
            layer = layers[index]
            assert layer['leadIn'] == '1' and layer['leadStyle'] == style
            assert float(layer['leadLength']) == length and float(layer['leadAngle']) == angle
        assert layers[3].get('leadIn', '0') == '0'
        assert all(layer.get('doOutput', '1') == '1' and layer.get('leadOut', '0') == '0'
                   and layer.get('overcut', '0') == '0' for layer in layers.values())
        assert root.find('UIPrefs/Optimize_OptimalEntryPoint').get('Value') == '0'
        assert root.find('UIPrefs/Optimize_AllowReverse').get('Value') == '1'
        xml, indices, omitted, zeros = normalize(source.read_text(encoding='utf-8'))
        assert not omitted and len(indices) == 6
        shapes = E.fromstring(xml).findall('Shape')
        assert len(shapes) == 6 and all(s.get('StartV') in [None, '0'] for s in shapes)
        native_indices[style] = [int(s.get('CutIndex')) for s in shapes]
        (normalized/f'{style}.lbrn2').write_text(xml, encoding='utf-8', newline='\n')
        settings[style] = {'layers': layers, 'zero_handle_indices': zeros}
    subprocess.run(['node', str(ROOT/'scripts/h6_lead_settings_oracle.mjs'), str(normalized), str(scratch/'oracle')],
                   check=True, capture_output=True, timeout=30)
    results = []
    layout = json.loads((folder/'arc/layout.json').read_text(encoding='utf-8'))
    for style in ['line', 'arc']:
        report = json.loads((folder/f'revised-2/{style}/report.json').read_text(encoding='utf-8'))
        svg = E.parse(folder/f'revised-2/{style}/sheet-0.svg').getroot()
        group = next(g for g in svg if g.get('id') == 'CUT')
        paths = [sub for p in group for sub in parse_path(p.get('d')).continuous_subpaths()]
        assert len(paths) == 6 and all(p.isclosed() for p in paths)
        height = float(svg.get('height').removesuffix('mm'))
        references = [translate(geometry(p, flip=True), yoff=height) for p in paths]
        starts = [np.array([p.start.real, height-p.start.imag]) for p in paths]
        native = [sub for p in Document(scratch/f'oracle/{style}.svg').paths() for sub in p.continuous_subpaths()]
        assert len(native) == 6 and all(p.isclosed() for p in native)
        native_shapes = [geometry(p, flip=True) for p in native]
        shift = np.array(unary_union(native_shapes).bounds[:2])-unary_union(references).bounds[:2]
        native_shapes = [translate(p, xoff=-shift[0], yoff=-shift[1]) for p in native_shapes]
        native_starts = [np.array([p.start.real, -p.start.imag])-shift for p in native]
        unmatched = set(range(6))
        rows = []
        for index, (ref, start) in enumerate(zip(references, starts)):
            match = min(unmatched, key=lambda i: ref.hausdorff_distance(native_shapes[i]))
            unmatched.remove(match)
            distance = ref.hausdorff_distance(native_shapes[match])
            start_error = float(np.linalg.norm(native_starts[match]-start))
            layer = native_indices[style][match]
            rows.append({'copy_index': index//3, 'contour_index': index%3,
                         'geometry_error_mm': distance, 'start_error_mm': start_error,
                         'native_layer': layer, 'pass': max(distance, start_error) < 0.01
                         and layer == [0, 3, 4][index%3]})
        raster = raster_check(folder, style, report, layout, references)
        results.append({'style': style, 'settings': settings[style], 'translation_mm': shift.tolist(),
                        'contours': rows, 'raster': raster,
                        'pass': all(r['pass'] for r in rows) and raster['pass']})
    def flags(path):
        obs = json.loads(path.read_text(encoding='utf-8'))
        return {e['automationId']: e['toggleState'] for e in obs['elements'] if e['role'] == 'CheckBox'}
    original = flags(folder/'optimization-original.json')
    assert len(original) == 10 and original == flags(folder/'optimization-restored.json')
    audit = {'held_out_read': False, 'h6_complete': False, 'results': results,
             'optimization_unchanged': True, 'pass': all(r['pass'] for r in results),
             'script_sha256': digest(Path(__file__)),
             'oracle_sha256': digest(ROOT/'scripts/h6_lead_settings_oracle.mjs'),
             'artifacts': {p.relative_to(folder).as_posix(): digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}}
    target = folder/f'native-audit-{stamp}.json'
    target.write_text(json.dumps(audit, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'report': str(target), 'pass': audit['pass'],
                      'results': [{'style': r['style'], 'native_start_max_mm': max(c['start_error_mm'] for c in r['contours']),
                                   'native_geometry_max_mm': max(c['geometry_error_mm'] for c in r['contours']),
                                   'raster': r['raster']} for r in results]}, indent=2))
    assert audit['pass'], 'Retained failed audit; inspect evidence before another attempt'


if __name__ == '__main__':
    main()
