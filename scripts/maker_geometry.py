"""Auditable curve-to-polygon conversion for benchmark authoring, not the product.

Bezier subdivision accepts a chord only when every control point lies within the
tolerance capsule around it. Convexity bounds the whole curve in that capsule;
the continuous projection between endpoints bounds the reverse distance too.
Elliptical arcs use the circle sagitta bound times the largest ellipse radius.
Source curves are retained separately for the later import/export fidelity gate.
"""
from math import acos, ceil, radians

from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import explain_validity
from svgpathtools import Arc, CubicBezier, Line, QuadraticBezier, parse_path

TOLERANCE_MM = 0.005
ROUND_DIGITS = 9


def point_segment_distance(point, start, end):
    direction = end - start
    if abs(direction) == 0:
        return abs(point - start)
    t = max(0.0, min(1.0, ((point - start).conjugate() * direction).real / abs(direction) ** 2))
    return abs(point - (start + t * direction))


def flatten_segment(segment, tolerance=TOLERANCE_MM, depth=0):
    """Return points including both endpoints; refuse unresolved subdivision."""
    if tolerance <= 0:
        raise ValueError('Tolerance must be positive')
    if isinstance(segment, Line):
        return [segment.start, segment.end]
    if isinstance(segment, Arc):
        radius = max(abs(segment.radius.real), abs(segment.radius.imag))
        step = 2 * acos(max(-1, min(1, 1 - tolerance / radius)))
        count = max(1, ceil(abs(radians(segment.delta)) / step))
        if count > 100000:
            raise ValueError('Excessive arc subdivisions')
        return [segment.point(i / count) for i in range(count + 1)]
    if isinstance(segment, (CubicBezier, QuadraticBezier)):
        controls = segment.bpoints()[1:-1]
        if max(point_segment_distance(p, segment.start, segment.end) for p in controls) <= tolerance:
            return [segment.start, segment.end]
        if depth >= 32:
            raise ValueError('Curve subdivision did not converge')
        left, right = segment.split(.5)
        return flatten_segment(left, tolerance, depth + 1)[:-1] + flatten_segment(right, tolerance, depth + 1)
    raise ValueError(f'Unsupported segment {type(segment).__name__}')


def path_rings(d, tolerance=TOLERANCE_MM):
    path = parse_path(d)
    if not path:
        raise ValueError('Empty source path')
    rings = []
    for subpath in path.continuous_subpaths():
        if abs(subpath.start - subpath.end) > 1e-8:
            raise ValueError('Source cut boundary is open')
        points = []
        for segment in subpath:
            points.extend(flatten_segment(segment, tolerance)[:-1])
        ring = []
        for point in points:
            pair = [round(point.real, ROUND_DIGITS), round(point.imag, ROUND_DIGITS)]
            if not ring or pair != ring[-1]:
                ring.append(pair)
        if ring and ring[0] == ring[-1]:
            ring.pop()
        if len(ring) < 3:
            raise ValueError('Degenerate source ring')
        rings.append(ring)
    return rings


def classify_rings(rings):
    """Even/odd filled contours, rejecting crossings/touches rather than repairing."""
    polygons = [Polygon(ring) for ring in rings]
    for polygon in polygons:
        if not polygon.is_valid or polygon.area <= 0:
            raise ValueError(f'Invalid source contour: {explain_validity(polygon)}')
    parent = [None] * len(rings)
    for i, polygon in enumerate(polygons):
        enclosing = []
        for j, other in enumerate(polygons):
            if i == j:
                continue
            if polygon.boundary.intersects(other.boundary):
                raise ValueError('Source contours cross or touch')
            if other.contains(polygon):
                enclosing.append(j)
            elif polygon.intersects(other) and not polygon.contains(other):
                raise ValueError('Source contours overlap')
        if enclosing:
            parent[i] = min(enclosing, key=lambda j: polygons[j].area)

    def depth(index):
        return 0 if parent[index] is None else 1 + depth(parent[index])

    result = []
    for i, outer in enumerate(rings):
        if depth(i) % 2 == 0:
            result.append({'outer': outer, 'holes': [ring for j, ring in enumerate(rings) if parent[j] == i]})
    return result


def normalize(geometry):
    min_x = min(p[0] for component in geometry for p in component['outer'])
    min_y = min(p[1] for component in geometry for p in component['outer'])

    def move(ring):
        return [[round(x - min_x, ROUND_DIGITS), round(y - min_y, ROUND_DIGITS)] for x, y in ring]

    return [{'outer': move(c['outer']), 'holes': [move(h) for h in c['holes']]} for c in geometry], [min_x, min_y]


def from_shapely(geometry):
    if geometry.is_empty or not geometry.is_valid:
        raise ValueError(f'Invalid constructed part: {explain_validity(geometry)}')
    components = [geometry] if isinstance(geometry, Polygon) else list(geometry.geoms)
    if not isinstance(geometry, (Polygon, MultiPolygon)):
        raise ValueError('Constructed part is not polygonal')
    return [{'outer': [list(p) for p in component.exterior.coords[:-1]],
             'holes': [[list(p) for p in hole.coords[:-1]] for hole in component.interiors]}
            for component in components]
