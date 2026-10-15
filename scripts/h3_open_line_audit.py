"""Independent open-stroke footprints, preserving exports and actual search.

Only the eight approved training repairs and an authored MIT fixture are read.
The original files, labels and prior rejections remain unchanged. This is
an H3 development check, not held-out acceptance or search-quality evidence.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path

import psutil
from shapely import Polygon, box, make_valid, union_all
from shapely.affinity import affine_transform

from h3_geometry_audit import compare, normalize, write_json
from h3_reviewed_prerequisites import guards
from h3_writer_audit import audit
from h6_material_cost import run
from maker_geometry import flatten_segment
from shop_public_reference_audit import curves, image_corners

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def footprint(scene, directory, index, tolerance):
    shape = scene['shapes'][index]
    if shape['kind'] == 'Group':
        return union_all([footprint(scene, directory, i, tolerance) for i in shape['children']])
    paths = curves(directory/f'{index}.svg')
    closed = shape['kind'] in ['Path', 'Rect', 'Ellipse', 'Polygon'] and shape['paths'] and all(p['closed'] for p in shape['paths'])
    if closed:
        result = Polygon()
        for path in paths:
            points = [[p.real, -p.imag] for segment in path for p in flatten_segment(segment, .0005)]
            if len(points) >= 3:
                result = result.symmetric_difference(make_valid(Polygon(points)))
        return result
    bounds = [p.bbox() for p in paths if p]
    bounds.extend((min(p[0] for p in image), max(p[0] for p in image), min(p[1] for p in image), max(p[1] for p in image))
                  for image in image_corners(directory/f'{index}.svg'))
    x0, x1 = min(b[0] for b in bounds), max(b[1] for b in bounds)
    y0, y1 = -max(b[3] for b in bounds), -min(b[2] for b in bounds)
    half_width = max(tolerance, .000001, (x1-x0)/2)
    half_height = max(tolerance, .000001, (y1-y0)/2)
    cx, cy = (x0+x1)/2, (y0+y1)/2
    x0, x1, y0, y1 = cx-half_width, cx+half_width, cy-half_height, cy+half_height
    return box(x0, y0, x1, y1)


def independent_units(scene, directory, nesting, tolerance, actual):
    checks, expected = [], {}
    for unit, polygons in zip(nesting['units'], actual, strict=True):
        reference = union_all([footprint(scene, directory, scene['top_level'][m], tolerance) for m in unit['members']])
        product = union_all([Polygon(p['outer'], p['holes']) for p in polygons])
        delta = product.boundary.hausdorff_distance(reference.boundary)
        checks.append({'unit': unit['id'], 'boundary_hausdorff_mm': delta,
                       'reference_area_mm2': reference.area, 'product_area_mm2': product.area,
                       'passed': delta <= .01 and product.is_valid and reference.is_valid and reference.area > 0})
        expected[unit['id']] = reference
    assert all(c['passed'] for c in checks), checks
    return checks, expected


def independent_placements(expected, payload):
    checks = []
    for sheet in payload['files']:
        shapes, overlap, outside = [], 0., 0.
        for placement in sheet['placements']:
            t = placement['transform']
            s, c = math.sin(t['rotation_radians']), math.cos(t['rotation_radians'])
            m = -1 if t['mirrored'] else 1
            shape = affine_transform(expected[placement['unit']], [m*c, -s, m*s, c, *t['translation']])
            outside = max(outside, shape.difference(box(0, 0, payload['width_mm'], payload['height_mm'])).area)
            for other in shapes:
                overlap = max(overlap, shape.intersection(other).area)
            shapes.append(shape)
        checks.append({'sheet': sheet['sheet'], 'units': len(shapes), 'maximum_overlap_mm2': overlap,
                       'maximum_outside_mm2': outside, 'passed': overlap < 1e-8 and outside < 1e-8})
    assert all(c['passed'] for c in checks), checks
    return checks


def main():
    psutil.Process().cpu_affinity([8])
    manifest = json.loads((CORPUS/'manifest.json').read_bytes())
    training = {r['path']: r for r in manifest['files'] if r['split'] == 'training'}
    decisions = ROOT/'benchmarks/results/h3-reviewed-decisions-20261015.json'
    repairs = json.loads(decisions.read_bytes())['projects']
    assert len(repairs) == 8
    for approved in repairs:
        assert training[approved['path']]['sha256'] == digest(CORPUS/approved['path']) == approved['sha256']
        assert digest(CORPUS/approved['label']) == approved['label_sha256']
        assert digest(CORPUS/approved['native_reference']) == approved['native_reference_sha256']
    before = {**guards(), 'script': digest(Path(__file__)), 'oracle_script': digest(ROOT/'scripts/h3_geometry_oracle.mjs'),
              'geometry_adapter': digest(ROOT/'scripts/h3_geometry_audit.py'), 'decisions': digest(decisions)}
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT/'benchmarks/results'/f'h3-open-lines-{stamp}'
    out.mkdir()
    write_json(out/'plan.json', {'scope': __doc__, 'guards': before, 'cpu': 8, 'held_out_geometry_read': False,
                               'repairs': repairs, 'search_cases': ['authored', 'L17'], 'search_seconds': 60, 'seed': 0})
    rows = []
    cases = [('authored', ROOT/'crates/core/tests/fixtures/open-lines.lbrn2')]
    cases.extend((r['id'], CORPUS/r['native_reference']) for r in repairs)
    for name, path in cases:
        folder = out/name
        folder.mkdir()
        source = path.read_bytes()
        record = {'case': name, 'source': path.relative_to(ROOT).as_posix(), 'source_sha256': sha256(source).hexdigest()}
        def execute(command, label, timeout=30):
            result = run(command, folder, label, 8, timeout)
            record[label] = result
            write_json(folder/'progress.json', record)
            assert result['exit_code'] == 0, result
            return json.loads((folder/(label+'-stdout.json')).read_bytes())
        inspection = execute([ROOT/'target/release/examples/lightburn_inspect.exe', path], 'inspect')
        assert inspection['noop_byte_identical']
        scene = inspection['scene']
        normalized, indices, omitted, zeros = normalize(source)
        assert not omitted and all(s['geometry_complete'] for s in scene['shapes'])
        (folder/'normalized.lbrn2').write_text(normalized, encoding='utf-8', newline='\n')
        write_json(folder/'oracle-request.json', {'projects': [{'path': name, 'normalized_xml': str(folder/'normalized.lbrn2'),
            'shape_indices': indices, 'svg_directory': str(folder/'oracle')}], 'oracle_report': str(folder/'oracle.json')})
        result = run(['node', ROOT/'scripts/h3_geometry_oracle.mjs', folder/'oracle-request.json'], folder, 'oracle', 8, 120)
        assert result['exit_code'] == 0 and 'error' not in json.loads((folder/'oracle.json').read_bytes())['reports'][0]
        record['geometry'] = [{'shape': i, **compare(scene['shapes'][i], folder/'oracle'/f'{i}.svg')} for i in indices]
        assert all(c['passed'] for c in record['geometry'])
        diagnostic = execute([ROOT/'target/release/examples/lightburn_roundtrip.exe', path], 'writer')
        assert diagnostic['status'] == 'written' and diagnostic['identity_byte_equal'] and diagnostic['validation']['valid']
        record['diagnostic_canonical'] = audit(source, diagnostic)
        record['diagnostic_units'], expected = independent_units(scene, folder/'oracle', diagnostic['nesting'], .0005,
                                                               [u['geometry'] for u in diagnostic['nesting']['units']])
        record['diagnostic_placements'] = independent_placements(expected, diagnostic)
        execute([ROOT/'target/release/nestbolt.exe', 'import', path, '--output', folder/'library.json'], 'import')
        library = json.loads((folder/'library.json').read_bytes())
        assert library['lightburn']['xml'].encode('utf-8') == source
        record['import_units'], _ = independent_units(scene, folder/'oracle', diagnostic['nesting'], library['tolerance'],
            [p.get('components') or [p['polygon']] for p in library['parts']])
        if name not in ['authored', 'L17']:
            record['passed'] = True
            record['artifacts'] = {p.relative_to(folder).as_posix(): digest(p) for p in folder.rglob('*') if p.is_file()}
            write_json(folder/'result.json', record)
            rows.append(record)
            print(name, 'passed', len(record['diagnostic_units']), 'diagnostic units', flush=True)
            continue
        request = {'sheets': [{'width_mm': 900, 'height_mm': 900}], 'spacing_mm': 1, 'edge_spacing_mm': 1}
        write_json(folder/'request.json', request)
        execute([ROOT/'target/release/nestbolt.exe', 'nest', '--library', folder/'library.json', '--request', folder/'request.json',
                 '--out-dir', folder/'nested', '--seconds', 60, '--seed', 0], 'nest', 180)
        report = json.loads((folder/'nested/report.json').read_bytes())
        layout = json.loads((folder/'nested/layout.json').read_bytes())
        job = json.loads((folder/'nested/job.json').read_bytes())
        assert report['validation']['valid'] and len(layout['placements']) == len(library['parts'])
        unit_ids = library['lightburn']['unit_ids']
        part_geometry = {p['id']: p['geometry'] for p in job['parts']}
        record['search_units'], expected = independent_units(scene, folder/'oracle', diagnostic['nesting'], library['tolerance'],
                                                           [part_geometry[part_id] for part_id in unit_ids])
        payload = {'nesting': diagnostic['nesting'], 'width_mm': 900, 'height_mm': 900, 'files': [],
                   'identity_byte_equal': diagnostic['identity_byte_equal'], 'validation': report['validation']}
        for sheet, filename in zip(layout['sheets'], report['files'], strict=True):
            payload['files'].append({'sheet': sheet['id'], 'xml': (folder/'nested'/filename).read_text(encoding='utf-8'),
                'placements': [{'unit': unit_ids.index(p['part_id']), 'transform': p['transform']} for p in layout['placements'] if p['sheet_id'] == sheet['id']]})
        record['search_canonical'] = audit(source, payload)
        record['search_placements'] = independent_placements(expected, payload)
        checked = execute([ROOT/'target/release/nestbolt.exe', 'validate', '--library', folder/'library.json', '--request', folder/'request.json',
                           '--layout', folder/'nested/layout.json'], 'validate', 120)
        assert checked['valid'] and checked['metrics'] == report['validation']['metrics']
        record['search_metrics'] = checked['metrics']
        record['passed'] = True
        record['artifacts'] = {p.relative_to(folder).as_posix(): digest(p) for p in folder.rglob('*') if p.is_file()}
        write_json(folder/'result.json', record)
        rows.append(record)
        print(name, 'passed', len(record['search_units']), 'units', flush=True)
    assert before == {**guards(), 'script': digest(Path(__file__)), 'oracle_script': digest(ROOT/'scripts/h3_geometry_oracle.mjs'),
                      'geometry_adapter': digest(ROOT/'scripts/h3_geometry_audit.py'), 'decisions': digest(decisions)}
    write_json(out/'results.json', {'scope': __doc__, 'H3': False, 'guards': before, 'source_guards_passed': True,
                                  'held_out_geometry_read': False, 'rows': rows})
    print(out, flush=True)


if __name__ == '__main__':
    main()
