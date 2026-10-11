"""Rigid, auditable adapters for unmodified SVGnest's public SVG interface."""
import math
import xml.etree.ElementTree as ET

from benchmark_io import UnsupportedJob, finite_number


def allowed(part, angle):
    rule = part['rotations']
    if rule['kind'] == 'free':
        return True
    angles = rule['degrees'] if rule['kind'] == 'list' else [i * rule['degrees'] for i in range(math.ceil(360 / rule['degrees']))]
    return any(abs((angle - a + 180) % 360 - 180) < 1e-8 for a in angles)


def linear_path(points):
    # SVG polygon.points exposes float32 coordinates in Chromium. The pinned
    # path-segment polyfill parses M/L values as JS doubles instead.
    return ' '.join(f'{"M" if i == 0 else "L"}{x:.17g} {y:.17g}' for i,(x,y) in enumerate(points)) + ' Z'


def prepare(job, settings, axis='y'):
    if job['version'] != 1 or job['mode'] != 'all':
        raise UnsupportedJob('SVGnest supports all-parts polygon jobs only')
    quantities = [p['quantity'] for p in job['parts']]
    if not quantities or any(type(q) is not int or q <= 0 for q in quantities) or sum(quantities) > 2000:
        raise ValueError('SVGnest adapter accepts 1..2000 positive part copies')
    if len(job['stocks']) != 1:
        raise UnsupportedJob('SVGnest cannot express mixed stock sizes')
    stock = job['stocks'][0]
    if stock['outline'] or stock['defects']:
        raise UnsupportedJob('SVGnest cannot express stock remnants or defects')
    if any(len(p['geometry']) != 1 for p in job['parts']):
        raise UnsupportedJob('SVGnest cannot preserve disconnected components as one rigid part')
    if axis not in ['x', 'y']:
        raise ValueError('Unknown solver axis')
    # SVGnest has one equally-spaced angle grid shared by every part. Search the
    # largest native grid permitted by every source rule; never add an angle.
    maximum = settings['free_rotation_samples']
    grids = [n for n in range(1, max(360, maximum) + 1)
             if all(allowed(p, 360 * i / n) for p in job['parts'] for i in range(n))]
    if not grids:
        raise UnsupportedJob('No native SVGnest angle grid matches the allowed rotation rules')
    all_free = all(p['rotations']['kind'] == 'free' for p in job['parts'])
    rotations = maximum if all_free else max(grids)
    restrictions = []
    if any(p['rotations']['kind'] == 'free' for p in job['parts']):
        restrictions.append(f'Native finite-angle search uses {rotations} equally spaced angles within the allowed free rotations.')
    if any(p['allow_mirror'] for p in job['parts']):
        restrictions.append('Native SVGnest has no mirror search; unmirrored placements remain permitted.')
    for p in job['parts']:
        rule = p['rotations']
        if rule['kind'] != 'free':
            declared = rule['degrees'] if rule['kind'] == 'list' else [i * rule['degrees'] for i in range(math.ceil(360 / rule['degrees']))]
            if any(not any(abs((a - i*360/rotations + 180) % 360 - 180) < 1e-8 for i in range(rotations)) for a in declared):
                raise UnsupportedJob('SVGnest global rotation grid would drop a declared discrete angle')
    if stock['count'] is not None:
        restrictions.append('Sheet cap enforced by independent validation; the native search opens identical bins as needed.')
    m = stock['margins']
    width, height = stock['width'], stock['height']
    left, right, bottom, top = m['left'], m['right'], m['bottom'], m['top']
    if axis == 'y':
        width, height = height, width
        left, right, bottom, top = bottom, top, right, left
    gap, edge = job['clearance'], job['edge_clearance']
    # Upstream inflates parts by gap/2, insets bin by gap/2, then moves the
    # inset bin to zero. This virtual bin and final origin shift express the
    # exact original margin + edge gap, including when edge != interpart gap.
    bin_width = width - left - right - 2 * edge + 2 * gap
    bin_height = height - bottom - top - 2 * edge + 2 * gap
    if min(bin_width, bin_height) <= 2 * gap:
        raise ValueError('No usable stock interior')
    origin = [left + edge - gap/2, bottom + edge - gap/2]
    count = sum(p['quantity'] for p in job['parts'])
    columns = math.ceil(math.sqrt(count))
    transformed = []
    for part in job['parts']:
        component = part['geometry'][0]
        rings = [component['outer'], *component['holes']]
        rings = [[[y, -x] if axis == 'y' else [x, y] for x, y in ring] for ring in rings]
        xs, ys = [p[0] for p in rings[0]], [p[1] for p in rings[0]]
        transformed.append((part, rings, min(xs), min(ys), max(xs)-min(xs), max(ys)-min(ys)))
    pitch_x = max(t[4] for t in transformed) + 10
    pitch_y = max(t[5] for t in transformed) + 10
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg')
    source_rings = {'sheet': [[0,0],[bin_width,0],[bin_width,bin_height],[0,bin_height]]}
    ET.SubElement(svg, 'path', id='sheet', d=linear_path(source_rings['sheet']))
    mapping = {}
    for part, rings, min_x, min_y, _, _ in transformed:
        for copy in range(part['quantity']):
            index = len(mapping)
            key = f'copy-{index}'
            offset = [bin_width + 10 + (index % columns) * pitch_x - min_x,
                      (index // columns) * pitch_y - min_y]
            mapping[key] = {'part_id': part['id'], 'copy_index': copy, 'offset': offset, 'hole_count': len(rings)-1}
            for r, ring in enumerate(rings):
                identifier = key if r == 0 else f'{key}-hole-{r}'
                points = [[x+offset[0],y+offset[1]] for x,y in ring]
                source_rings[identifier] = points
                ET.SubElement(svg, 'path', id=identifier, d=linear_path(points))
    config = {k: v for k, v in settings.items() if k != 'free_rotation_samples'}
    config.update({'rotations': rotations, 'spacing': gap})
    return {'svg': ET.tostring(svg, encoding='unicode'), 'mapping': mapping,
            'origin': origin, 'axis': axis, 'original_width': stock['width'],
            'stock_id': stock['id'], 'config': config, 'restrictions': restrictions,
            'copies': count, 'units': job['units'], 'source_rings': source_rings,
            'input_encoding': 'linear_svg_paths_v2'}


def layout(prepared, sheets):
    result = {'version': 1, 'units': prepared['units'], 'sheets': [], 'placements': []}
    seen = set()
    for index, groups in enumerate(sheets):
        sheet_id = f'sheet-{index}'
        result['sheets'].append({'id': sheet_id, 'stock_id': prepared['stock_id']})
        for group in groups:
            identifier = group['outer_id']
            if identifier not in prepared['mapping'] or identifier in seen:
                raise ValueError('Unknown or duplicate returned copy')
            seen.add(identifier)
            source = prepared['mapping'][identifier]
            if len(group['hole_ids']) != source['hole_count'] or set(group['hole_ids']) != {f'{identifier}-hole-{i+1}' for i in range(source['hole_count'])}:
                raise ValueError('SVGnest omitted or reassigned source holes')
            if len(group['matrix']) != 6:
                raise ValueError('Malformed returned transform')
            a, b, c, d, e, f = map(finite_number, group['matrix'])
            if max(abs(a-d), abs(b+c), abs(a*a+b*b-1), abs(a*d-b*c-1)) > 1e-9:
                raise ValueError('Non-rigid or reflected SVGnest transform')
            ox, oy = source['offset']
            x, y = e + a*ox + c*oy + prepared['origin'][0], f + b*ox + d*oy + prepared['origin'][1]
            if prepared['axis'] == 'y':
                x, y = prepared['original_width'] - y, x
            result['placements'].append({'part_id': source['part_id'], 'copy_index': source['copy_index'],
                'sheet_id': sheet_id, 'transform': {'translation': [x, y],
                    'rotation_radians': math.atan2(b, a) % (2*math.pi), 'mirrored': False}})
    return result
