"""Experimental rigid pairs of identical concave orthogonal parts.

No source ring is simplified or replaced. Search proxies use the existing
multipart convex hull; output placements expand back to the original copies.
Pattern selection knows geometry/permissions only, never a job or part name.
"""
from copy import deepcopy
import math

from shapely.affinity import translate
from shapely.geometry import Polygon
from shapely.ops import unary_union


def quarter(point, turns):
    x, y = point
    return [(x, y), (-y, x), (-x, -y), (y, -x)][turns % 4]


def allowed(part):
    rule = part['rotations']
    if rule['kind'] == 'free':
        return [0, 1, 2, 3]
    if rule['kind'] != 'list':
        return []
    degrees = [d % 360 for d in rule['degrees']]
    if any(abs(d/90-round(d/90)) > 1e-9 for d in degrees):
        return []
    return sorted({round(d/90) % 4 for d in degrees})


def pattern(part, clearance):
    if len(part['geometry']) != 1 or part['quantity'] < 2:
        return None
    turns = allowed(part)
    if not turns:
        return None
    ring = part['geometry'][0]['outer']
    if len(ring) > 32 or any(a[0] != b[0] and a[1] != b[1]
                              for a, b in zip(ring, ring[1:]+ring[:1])):
        return None
    filled = Polygon(ring)
    if filled.convex_hull.area <= filled.area * 1.05:
        return None
    gap = clearance + 2e-6
    best = None
    for rotation in range(4):
        # Every permitted group orientation must preserve each member's rule.
        if any((a+rotation) % 4 not in turns or
               (part['allow_mirror'] and (a-rotation) % 4 not in turns) for a in turns):
            continue
        rotated = [quarter(p, rotation) for p in ring]
        other = Polygon(rotated)
        offsets = sorted({(a[0]-b[0]+dx, a[1]-b[1]+dy)
                          for a in ring for b in rotated
                          for dx in [-gap, 0, gap] for dy in [-gap, 0, gap]})
        for dx, dy in offsets:
            moved = translate(other, dx, dy)
            if filled.intersects(moved) or filled.distance(moved) < clearance+1e-6:
                continue
            hull = unary_union([filled, moved]).convex_hull
            if hull.area >= 1.8*filled.convex_hull.area:
                continue
            left, bottom, right, top = hull.bounds
            score = (hull.area, (right-left)*(top-bottom), max(right-left, top-bottom), rotation, dx, dy)
            if best is None or score < best[0]:
                best = (score, {'rotation_quarters': rotation, 'translation': [dx, dy],
                               'filled_clearance': filled.distance(moved),
                               'pair_hull_area': hull.area, 'two_single_hulls_area': 2*filled.convex_hull.area})
    return best[1] if best else None


def prepare(job):
    result = deepcopy(job)
    result['parts'] = []
    patterns = {}
    ids = {p['id'] for p in job['parts']}
    for part in job['parts']:
        found = pattern(part, job['clearance'])
        if found is None:
            result['parts'].append(deepcopy(part))
            continue
        group_id = part['id']+'-experimental-pair'
        assert group_id not in ids
        count = part['quantity']//2
        group = deepcopy(part)
        group.update(id=group_id, quantity=count)
        moved = deepcopy(part['geometry'][0])
        def transform(ring):
            return [[q[0]+found['translation'][0], q[1]+found['translation'][1]]
                    for p in ring for q in [quarter(p, found['rotation_quarters'])]]
        moved['outer'] = transform(moved['outer'])
        moved['holes'] = [transform(h) for h in moved['holes']]
        group['geometry'].append(moved)
        result['parts'].append(group)
        patterns[group_id] = {**found, 'original_id': part['id'], 'pairs': count}
        if part['quantity'] % 2:
            remainder = deepcopy(part)
            remainder['quantity'] = 1
            result['parts'].append(remainder)
    return result, patterns


def expand(layout, patterns):
    expanded = deepcopy(layout)
    expanded['placements'] = []
    remainders = {v['original_id']: 2*v['pairs'] for v in patterns.values()}
    for placement in layout['placements']:
        pat = patterns.get(placement['part_id'])
        if pat is None:
            single = deepcopy(placement)
            single['copy_index'] += remainders.get(single['part_id'], 0)
            expanded['placements'].append(single)
            continue
        first = deepcopy(placement)
        first.update(part_id=pat['original_id'], copy_index=2*placement['copy_index'])
        second = deepcopy(first)
        second['copy_index'] += 1
        t = placement['transform']
        angle = t['rotation_radians']
        c, s = math.cos(angle), math.sin(angle)
        x, y = pat['translation']
        if t['mirrored']:
            x = -x
        second['transform']['translation'] = [t['translation'][0]+c*x-s*y, t['translation'][1]+s*x+c*y]
        second['transform']['rotation_radians'] += (-1 if t['mirrored'] else 1)*pat['rotation_quarters']*math.pi/2
        expanded['placements'].extend([first, second])
    return expanded
