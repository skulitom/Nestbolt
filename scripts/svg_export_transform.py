"""Read native SVGnest export attributes without the browser's float32 SVGMatrix."""
import math
import re
import xml.etree.ElementTree as ET

NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?'
TRANSFORM = re.compile(r'\s*translate\(\s*('+NUMBER+r')(?:\s*,\s*|\s+)('+NUMBER+r')\s*\)\s*rotate\(\s*('+NUMBER+r')\s*\)\s*')


def rigid_matrix(attribute):
    match = TRANSFORM.fullmatch(attribute)
    if not match:
        raise ValueError('Expected native translate(x y) rotate(angle) export transform')
    x, y, degrees = map(float, match.groups())
    if not all(math.isfinite(v) for v in [x,y,degrees]):
        raise ValueError('Non-finite export transform')
    radians = math.radians(degrees % 360)
    c, s = math.cos(radians), math.sin(radians)
    return [c,s,-s,c,x,y]


def groups_from_exports(exports):
    sheets = []
    ns = '{http://www.w3.org/2000/svg}'
    for text in exports:
        root = ET.fromstring(text)
        if root.tag != ns+'svg':
            raise ValueError('Native export is not an SVG document')
        groups = []
        for group in root:
            if group.tag != ns+'g':
                continue
            children = list(group)
            if not children or any(c.tag not in [ns+'polygon', ns+'path'] or 'id' not in c.attrib for c in children):
                raise ValueError('Malformed native exported part group')
            if any(c.get('transform') for c in children):
                raise ValueError('Unexpected additional transform on an exported source polygon')
            groups.append({'outer_id': children[0].attrib['id'], 'hole_ids': [c.attrib['id'] for c in children[1:]],
                           'matrix': rigid_matrix(group.get('transform',''))})
        sheets.append(groups)
    return sheets
