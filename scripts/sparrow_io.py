"""Current Sparrow strip/single-sheet adapter, preserving the original job."""
from copy import deepcopy
import math

from benchmark_io import UnsupportedJob, finite_number, jagua_input, jagua_layout


def prepare(job, axis='x'):
    if axis not in ['x', 'y']:
        raise ValueError('Unknown strip axis')
    if len(job['stocks']) != 1 or job['stocks'][0]['count'] == 0:
        raise UnsupportedJob('Sparrow single-sheet comparison requires one available stock type')
    stock = job['stocks'][0]
    if stock['outline'] or stock['defects']:
        raise UnsupportedJob('Sparrow has no remnant/defective strip support')
    # Reuse the strict item conversion, adapting only the virtual strip's edge.
    surrogate = deepcopy(job)
    surrogate['edge_clearance'] = job['clearance']
    if axis == 'y':
        for part in surrogate['parts']:
            for component in part['geometry']:
                component['outer'] = [[y,-x] for x,y in component['outer']]
                component['holes'] = [[[y,-x] for x,y in ring] for ring in component['holes']]
    items = jagua_input(surrogate)['items']
    if axis == 'y':
        for item in items:
            if item['orientation']['reflection_axes']:
                item['orientation']['reflection_axes'] = [0]
    m = stock['margins']
    gap, edge = job['clearance'], job['edge_clearance']
    if axis == 'x':
        height = stock['height']-m['bottom']-m['top']-2*edge+2*gap
        origin = [m['left']+edge-gap, m['bottom']+edge-gap]
    else:
        height = stock['width']-m['left']-m['right']-2*edge+2*gap
        origin = [m['bottom']+edge-gap, m['right']+edge-gap]
    if height <= 2*gap:
        raise ValueError('No usable strip height remains')
    return {'input': {'name': job['name'], 'min_item_separation': gap,
                      'strip_height': height, 'items': items}, 'axis': axis, 'origin': origin,
            'original_width': stock['width']}


def layout(job, prepared, raw):
    solution = raw['solution']
    width = finite_number(solution['strip_width'])
    if width <= 0 or solution['layout']['container_id'] != 0:
        raise ValueError('Invalid native strip width/container')
    result = jagua_layout(job, {'solution': {'layouts': [solution['layout']]}})
    for placed in result['placements']:
        transform = placed['transform']
        x,y = [a+b for a,b in zip(transform['translation'], prepared['origin'])]
        if prepared['axis'] == 'y':
            x,y = prepared['original_width']-y,x
            if transform['mirrored']:
                transform['rotation_radians'] = (transform['rotation_radians']+math.pi) % (2*math.pi)
        transform['translation'] = [x,y]
    return result


def strip_length(job, common):
    """Measure original transformed polygons, never the solver's reported width."""
    parts = {p['id']:p for p in job['parts']}
    farthest = 0.0
    for placed in common['placements']:
        t = placed['transform']
        c,s = math.cos(t['rotation_radians']),math.sin(t['rotation_radians'])
        for component in parts[placed['part_id']]['geometry']:
            for x,y in component['outer']:
                if t['mirrored']: x=-x
                farthest=max(farthest,x*c-y*s+t['translation'][0])
    return farthest
