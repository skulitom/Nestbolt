"""Public-SVG adapter for unmodified deepnest-next and the common validator."""
import math
import xml.etree.ElementTree as ET

from benchmark_io import UnsupportedJob, finite_number
from svgnest_io import allowed


def svg(rings):
    root = ET.Element('svg', xmlns='http://www.w3.org/2000/svg')
    for i, ring in enumerate(rings):
        ET.SubElement(root, 'polygon', id=f'ring-{i}', points=' '.join(f'{x:.17g},{y:.17g}' for x, y in ring))
    return ET.tostring(root, encoding='unicode')


def prepare(job, settings, axis='y'):
    if job['version'] != 1 or job['mode'] != 'all':
        raise UnsupportedJob('Deepnest adapter requires all-parts polygon jobs')
    if axis not in ['x', 'y']:
        raise ValueError('Unknown solver axis')
    quantities = [p['quantity'] for p in job['parts']]
    if not quantities or any(type(q) is not int or q <= 0 for q in quantities) or sum(quantities) > 2000:
        raise ValueError('Deepnest adapter accepts 1..2000 positive part copies')
    if any(len(p['geometry']) != 1 for p in job['parts']):
        raise UnsupportedJob('Deepnest import cannot retain disconnected components as one rigid part')
    if any(s['outline'] or s['defects'] for s in job['stocks']):
        raise UnsupportedJob('Nonrectangular/defective stock conversion is not yet implemented')
    all_free = all(p['rotations']['kind'] == 'free' for p in job['parts'])
    rotations = settings['free_rotation_samples'] if all_free else 0
    if not all_free:
        grids = [n for n in range(1, 361) if all(allowed(p, i * 360/n) for p in job['parts'] for i in range(n))]
        if not grids:
            raise UnsupportedJob('Deepnest global rotation grid cannot express the allowed rules')
        rotations = max(grids)
        for p in job['parts']:
            rule = p['rotations']
            if rule['kind'] == 'free':
                continue
            angles = rule['degrees'] if rule['kind'] == 'list' else [i*rule['degrees'] for i in range(math.ceil(360/rule['degrees']))]
            if any(not any(abs((a-i*360/rotations+180) % 360-180) < 1e-8 for i in range(rotations)) for a in angles):
                raise UnsupportedJob('Deepnest global rotation grid would discard a permitted discrete angle')
    restrictions = []
    multiplier = settings.get('spacing_multiplier', 1)
    if multiplier < 1:
        raise ValueError('Native spacing must not be weaker than the source constraint')
    native_gap = job['clearance'] * multiplier
    if multiplier != 1:
        restrictions.append(f'Conservative setting requests {multiplier} times interpart spacing to cover native half-gap behavior at holes; original job still determines validity.')
    if any(p['rotations']['kind'] == 'free' for p in job['parts']):
        restrictions.append(f'Native free-angle search uses {rotations} equally spaced samples.')
    if any(p['allow_mirror'] for p in job['parts']):
        restrictions.append('Native search has no mirroring; unmirrored placements remain allowed.')
    imports, copies, stocks = [], {}, {}
    for source, part in enumerate(job['parts']):
        component = part['geometry'][0]
        rings = [component['outer'], *component['holes']]
        if axis == 'y':
            rings = [[[y, -x] for x, y in ring] for ring in rings]
        imports.append({'source': source, 'kind': 'part', 'quantity': part['quantity'],
                        'svg': svg(rings), 'hole_count': len(rings)-1})
        for copy in range(part['quantity']):
            copies[str(len(copies))] = {'source': source, 'part_id': part['id'], 'copy_index': copy}
    for index, stock in enumerate(job['stocks']):
        source = len(imports)
        margins = stock['margins']
        width, height = stock['width'], stock['height']
        left, right, bottom, top = (margins[k] for k in ['left', 'right', 'bottom', 'top'])
        if axis == 'y':
            width, height = height, width
            left, right, bottom, top = bottom, top, right, left
        gap, edge = native_gap, job['edge_clearance']
        # This pinned engine inflates parts by gap/2, but does not apply its
        # negative sheet offset. Accommodate that exact public engine behavior.
        width = width-left-right-2*edge+gap
        height = height-bottom-top-2*edge+gap
        if min(width, height) <= gap:
            raise ValueError('No usable stock interior')
        quantity = len(copies) if stock['count'] is None else min(stock['count'], len(copies))
        imports.append({'source': source, 'kind': 'stock', 'quantity': quantity,
                        'svg': svg([[[0,0],[width,0],[width,height],[0,height]]]), 'hole_count': 0})
        for copy in range(quantity):
            stocks[f'{index:04d}-{copy:04d}'] = {'source': source, 'stock_id': stock['id'],
                'origin': [left+edge-gap/2, bottom+edge-gap/2], 'original_width': stock['width']}
    config = {k:v for k,v in settings.items() if k not in ['free_rotation_samples', 'spacing_multiplier']}
    config.update(rotations=rotations, spacing=native_gap)
    return {'imports': imports, 'copies': copies, 'stocks': stocks, 'config': config,
            'axis': axis, 'units': job['units'], 'restrictions': restrictions}


def layout(prepared, native):
    result = {'version': 1, 'units': prepared['units'], 'sheets': [], 'placements': []}
    seen_parts, seen_sheets = set(), set()
    for sheet in native['placements']:
        sheet_id = sheet['sheetid']
        if sheet_id not in prepared['stocks'] or sheet_id in seen_sheets:
            raise ValueError('Unknown or duplicate returned stock copy')
        stock = prepared['stocks'][sheet_id]
        if sheet['sheet'] != stock['source']:
            raise ValueError('Returned stock source does not match its copy ID')
        seen_sheets.add(sheet_id)
        result['sheets'].append({'id': sheet_id, 'stock_id': stock['stock_id']})
        for placed in sheet['sheetplacements']:
            key = str(placed['id'])
            if key not in prepared['copies'] or key in seen_parts:
                raise ValueError('Unknown or duplicate returned part copy')
            part = prepared['copies'][key]
            if placed['source'] != part['source']:
                raise ValueError('Returned part source does not match its copy ID')
            if any(k in placed for k in ['scale','matrix','flip','flipped','mirrored']):
                raise ValueError('Unexpected non-rigid or reflected native transform')
            seen_parts.add(key)
            x, y = finite_number(placed['x'])+stock['origin'][0], finite_number(placed['y'])+stock['origin'][1]
            if prepared['axis'] == 'y':
                x, y = stock['original_width']-y, x
            result['placements'].append({'part_id': part['part_id'], 'copy_index': part['copy_index'], 'sheet_id': sheet_id,
                'transform': {'translation': [x,y], 'rotation_radians': math.radians(finite_number(placed['rotation'])) % (2*math.pi), 'mirrored': False}})
    return result
