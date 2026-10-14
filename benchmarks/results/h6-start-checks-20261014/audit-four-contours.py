"""Independent SVG/DXF/native start-point probe; records failures, never H6 acceptance."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

import ezdxf
import numpy as np
from shapely import LineString
from shapely.affinity import translate
from shapely.ops import unary_union
from svgpathtools import Document

from h3_geometry_audit import normalize, product_paths
from maker_geometry import flatten_segment

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def geometry(path, flip=False):
    points = []
    for segment in path:
        points.extend(flatten_segment(segment, 0.000001)[:-1])
    points.append(path.end)
    return LineString([(p.real, -p.imag if flip else p.imag) for p in points])


def source_start(row):
    curve = row['contour']
    from_point = curve['start'] if row['segment'] == 0 else curve['segments'][row['segment']-1]['to']
    segment = curve['segments'][row['segment']]
    t = row['parameter']
    if segment['kind'] == 'arc':
        a = segment['start']+segment['sweep']*t
        x, y = segment['radii'][0]*np.cos(a), segment['radii'][1]*np.sin(a)
        c, s = np.cos(segment['rotation']), np.sin(segment['rotation'])
        return np.array([segment['center'][0]+c*x-s*y, segment['center'][1]+s*x+c*y])
    # Independent de Casteljau evaluation of the original source controls.
    controls = segment.get('controls', [segment['control']] if 'control' in segment else [])
    points = np.array([from_point, *controls, segment['to']])
    while len(points) > 1:
        points = (1-t)*points[:-1]+t*points[1:]
    return points[0]


def dxf_geometry(entity):
    if entity.dxftype() == 'SPLINE':
        tool = entity.construction_tool()
        knots = sorted(set(entity.knots))
        ts = [t for a, b in zip(knots, knots[1:]) for t in np.linspace(a, b, 1025)[:-1]]+[knots[-1]]
        first = tool.point(knots[0])
        return LineString([(p.x, p.y) for p in tool.points(ts)]), np.array([first.x, first.y]), bool(entity.closed)
    assert entity.dxftype() == 'LWPOLYLINE'
    lines = []
    for e in entity.virtual_entities():
        if e.dxftype() == 'LINE':
            lines.append(LineString([(p.x, p.y) for p in [e.dxf.start, e.dxf.end]]))
        else:
            assert e.dxftype() == 'ARC'
            lines.append(LineString([(p.x, p.y) for p in e.flattening(0.000001)]))
    return unary_union(lines), np.array(entity.get_points('xy')[0]), bool(entity.closed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    folder = args.folder.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    prepared = json.loads((folder/'preparation.json').read_text(encoding='utf-8'))
    for name, want in prepared['artifacts'].items():
        assert digest(folder/name) == want
    expected = json.loads((folder/'exports/expected.json').read_text(encoding='utf-8'))
    rows = expected['contours']
    references = [geometry(product_paths({'paths': [{'curve': r['contour']} ]})[0]) for r in rows]
    starts = [source_start(r) for r in rows]
    for row, start in zip(rows, starts):
        assert np.linalg.norm(start-row['expected_start_mm']) < 1e-10
    svg_paths = [p for p in Document(folder/'exports/ordered.svg').paths() if p.isclosed()]
    assert len(svg_paths) == len(rows) == 4
    doc = ezdxf.readfile(folder/'exports/ordered.dxf')
    audit = doc.audit()
    assert not audit.errors and not audit.fixes
    entities = [e for e in doc.modelspace() if e.dxf.layer == 'CUT']
    assert len(entities) == len(rows)
    records = []
    for i, (row, ref, start, svg, dxf) in enumerate(zip(rows, references, starts, svg_paths, entities)):
        svg_start = np.array([svg.start.real, expected['height_mm']-svg.start.imag])
        svg_geometry = translate(geometry(svg, flip=True), yoff=expected['height_mm'])
        dxf_path, dxf_start, closed = dxf_geometry(dxf)
        record = {'part': row['source'], 'expected_start_mm': start.tolist(),
                  'svg_start_error_mm': float(np.linalg.norm(svg_start-start)),
                  'dxf_start_error_mm': float(np.linalg.norm(dxf_start-start)),
                  'svg_geometry_error_mm': ref.hausdorff_distance(svg_geometry),
                  'dxf_geometry_error_mm': ref.hausdorff_distance(dxf_path),
                  'dxf_entity': dxf.dxftype(), 'dxf_closed': closed}
        record['pass'] = closed and max(record[k] for k in ['svg_start_error_mm', 'dxf_start_error_mm', 'svg_geometry_error_mm', 'dxf_geometry_error_mm']) < 0.00005
        records.append(record)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    scratch = ROOT/'output'/f'h6-start-audit-{stamp}'
    normalized = scratch/'normalized'
    normalized.mkdir(parents=True)
    native_formats = []
    for fmt in ['svg', 'dxf']:
        source = folder/f'{fmt}-native.lbrn2'
        if not source.exists():
            continue
        xml, indices, omitted, zeros = normalize(source.read_text(encoding='utf-8'))
        assert len(indices) == 8 and not omitted and not zeros
        root = E.fromstring(xml)
        for shape in root.findall('Shape'):
            if shape.get('CutIndex') != '0': root.remove(shape)
            else: assert shape.get('StartV') in [None, '0'], 'Honor explicit start override before scoring'
        (normalized/source.name).write_text(E.tostring(root, encoding='unicode'), encoding='utf-8', newline='\n')
        native_formats.append(fmt)
    subprocess.run(['node', str(ROOT/'scripts/h6_start_oracle.mjs'), str(normalized), str(scratch/'oracle')], check=True, capture_output=True, timeout=30)
    native = []
    ref_bounds = unary_union(references).bounds
    for fmt in native_formats:
        paths = Document(scratch/f'oracle/{fmt}-native.svg').paths()
        assert len(paths) == 4
        shapes = [geometry(p, flip=True) for p in paths]
        bounds = unary_union(shapes).bounds
        shift = [bounds[0]-ref_bounds[0], bounds[1]-ref_bounds[1]]
        results = []
        for row, ref, start, path, shape in zip(rows, references, starts, paths, shapes):
            point = np.array([path.start.real, -path.start.imag])-shift
            start_error = float(np.linalg.norm(point-start))
            geometry_error = ref.hausdorff_distance(translate(shape, xoff=-shift[0], yoff=-shift[1]))
            results.append({'part': row['source'], 'start_error_mm': start_error,
                            'geometry_error_mm': geometry_error, 'pass': max(start_error, geometry_error) <= 0.01})
        native.append({'format': fmt, 'translation_mm': shift, 'contours': results, 'pass': all(r['pass'] for r in results)})
    report = {'held_out_read': False, 'h6_complete': False, 'scope': 'Authored format probe only; no allowance/search/surface gate claim',
              'records': records, 'native': native, 'export_pass': all(r['pass'] for r in records),
              'native_pass': bool(native) and all(r['pass'] for r in native),
              'script_sha256': digest(Path(__file__)), 'artifacts': {str(p.relative_to(folder)).replace('\\', '/'): digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}}
    target = folder/f'format-audit-{stamp}.json'
    target.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'report': str(target), 'export_pass': report['export_pass'], 'native': native}, indent=2))


if __name__ == '__main__':
    main()
