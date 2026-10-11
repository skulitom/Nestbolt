"""Build the maker benchmark candidates from pinned local source generators.

This authoring command does not run an optimiser. A separate explicit freeze
will reserve held-out jobs before any solver tuning.
"""
from collections import Counter
from datetime import datetime
from hashlib import sha256
import json
from math import cos, pi, sin
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from svgpathtools import Path as SvgPath, parse_path

from maker_geometry import classify_rings, normalize, path_rings

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache/maker-sources'
DEST = ROOT / 'output/maker-candidates'
SVG_NS = 'http://www.w3.org/2000/svg'


def serialized(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')


def polygon_path(points):
    return 'M ' + ' L '.join(f'{x:.12g},{y:.12g}' for x, y in points) + ' Z'


def circle_path(x, y, radius):
    return f'M {x-radius},{y} A {radius},{radius} 0 1 0 {x+radius},{y} A {radius},{radius} 0 1 0 {x-radius},{y} Z'


def rect_path(x, y, width, height):
    return polygon_path([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])


def source_part(identifier, paths, quantity, rotations, mirror=False):
    rings = [ring for d in paths for ring in path_rings(d)]
    geometry, offset = normalize(classify_rings(rings))
    return {'id': identifier, 'quantity': quantity, 'geometry': geometry,
            'rotations': rotations, 'allow_mirror': mirror, 'priority': 1.0}, {
                'id': identifier, 'paths': paths, 'normalization_offset_mm': offset}


def stock(width, height, count=None, margin=5, identifier='stock'):
    return {'id': identifier, 'width': width, 'height': height, 'count': count,
            'margins': dict.fromkeys(['left', 'right', 'bottom', 'top'], margin),
            'outline': [], 'defects': []}


def job(identifier, parts, stocks, gap=.5):
    return {'version': 1, 'name': identifier, 'units': 'mm', 'parts': parts,
            'stocks': stocks, 'clearance': gap, 'edge_clearance': gap, 'mode': 'all'}


QUARTERS = {'kind': 'list', 'degrees': [0, 90, 180, 270]}
GRAIN = {'kind': 'list', 'degrees': [0, 180]}
FREE = {'kind': 'free'}


def box_jobs():
    # Use the unmodified pinned checkout directly, avoiding wheel/build-tool drift.
    checkout = ROOT / '.cache/upstream/boxes'
    expected = json.loads((ROOT / 'benchmarks/makers/sources.json').read_bytes())['sources']['boxes']['revision']
    if subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip() != expected:
        raise ValueError('Boxes.py checkout is not at the pinned revision')
    if subprocess.check_output(['git', '-C', str(checkout), 'status', '--porcelain', '--untracked-files=no'], text=True).strip():
        raise ValueError('Boxes.py checkout has tracked changes')
    sys.path.insert(0, str(checkout))
    from boxes.generators.universalbox import UniversalBox
    specs = [
        ('mini', 60, 40, 30, 3, 4, (300, 200), False),
        ('desktop', 100, 80, 60, 3, 6, (600, 400), False),
        ('tool', 180, 120, 80, 4, 4, (600, 400), False),
        ('storage', 400, 300, 250, 6, 3, (1220, 2440), False),
        ('long', 500, 180, 140, 6, 3, (1220, 2440), False),
        ('batch-500', 160, 100, 80, 3, 100, (1220, 2440), False),
        ('compact-2000', 80, 55, 40, 3, 400, (1220, 2440), True),
        ('deep', 280, 220, 200, 6, 12, (1220, 2440), True),
    ]
    for name, x, y, h, thickness, copies, size, held in specs:
        identifier = f'm-box-{name}'
        args = [f'--x={x}', f'--y={y}', f'--h={h}', f'--thickness={thickness}',
                '--burn=0', '--reference=0', '--labels=false', '--inner_corners=corner', '--top_edge=e']
        box = UniversalBox()
        box.parseArgs(args)
        box.metadata['creation_date'] = datetime(2026, 10, 11)
        box.open()
        box.render()
        original = box.close().getvalue()
        root = ET.fromstring(original)
        parts, curves = [], []
        for group in root.findall(f'{{{SVG_NS}}}g'):
            if not group.attrib['id'].startswith('p-') or 'transform' in group.attrib:
                raise ValueError('Unexpected Boxes.py output grouping')
            paths = []
            for path in group:
                if path.tag != f'{{{SVG_NS}}}path' or 'transform' in path.attrib:
                    raise ValueError('Unexpected Boxes.py cut element')
                paths.append(path.attrib['d'])
            part, curve = source_part(group.attrib['id'], paths, copies, GRAIN if thickness == 6 else QUARTERS)
            parts.append(part)
            curves.append(curve)
        if len(parts) != 5:
            raise ValueError('UniversalBox open-top cut list changed')
        yield job(identifier, parts, [stock(*size)], .8), curves, {
            'category': 'boxes', 'held_out': held, 'source': 'boxes',
            'parameters': {'generator': 'UniversalBox', 'arguments': args, 'copies': copies,
                           'creation_date': '2026-10-11T00:00:00'},
            'construction': 'Five open-top finger-jointed panels per box. Closed contours in each source part group define outer boundary and holes; burn=0, no labels/reference.'
        }, {'boxes.svg': original}


def ops_path(ops):
    commands = []
    for op in ops:
        point = lambda key: ','.join(repr(x) for x in op[key])
        if op['type'] in ['move', 'line']:
            commands.append(('M ' if op['type'] == 'move' else 'L ') + point('to'))
        elif op['type'] == 'curve':
            commands.append('C ' + ' '.join(point(key) for key in ['cp1', 'cp2', 'to']))
        elif op['type'] == 'close':
            commands.append('Z')
        else:
            raise ValueError('Unexpected FreeSewing operation')
    return ' '.join(commands)


def unfold(d):
    """Join the open cut boundary to its reflection, removing the fold edge."""
    path = parse_path(d)
    if path.isclosed():
        raise ValueError('Expected an open seam-allowance boundary along the fold')
    # The generator includes short fold-line segments from the stitch boundary
    # to a hem allowance. They become interior edges when unfolded, so omit them.
    on_fold = lambda segment: all(abs(p.real) < 1e-8 for p in segment.bpoints())
    while len(path) and on_fold(path[0]):
        del path[0]
    while len(path) and on_fold(path[-1]):
        del path[-1]
    if not path or abs(path.start.real) > 1e-8 or abs(path.end.real) > 1e-8:
        raise ValueError('Fold endpoints are not on X=0')
    # Remove floating point sin(180 degrees) noise at the shared seam endpoints.
    path[0].start = complex(0, path.start.imag)
    path[-1].end = complex(0, path.end.imag)
    reflected = path.reversed().scaled(-1, 1, origin=0j)
    full = SvgPath(*path, *reflected)
    return full.d() + ' Z'


def garment_jobs():
    base = {'biceps': 320, 'chest': 960, 'hpsToBust': 260, 'hpsToWaistBack': 430,
            'neck': 390, 'shoulderToShoulder': 430, 'shoulderSlope': 18,
            'waistToArmpit': 220, 'waistToHips': 190, 'hips': 1000, 'waist': 830,
            'shoulderToWrist': 600, 'wrist': 170}
    bruce = {'hips': 1000, 'upperLeg': 580, 'waistToHips': 190, 'waistToUpperLeg': 320}
    for design in ['teagan', 'bruce']:
        for index, factor in enumerate([.85, .95, 1.05, 1.15]):
            identifier = f'm-garment-{design}-{index+1}'
            request = {'design': design, 'seam_allowance': 10,
                       'measurements': {k: round(v * factor, 5) if k != 'shoulderSlope' else v
                                        for k, v in (base if design == 'teagan' else bruce).items()}}
            result = subprocess.run(['node', 'freesewing.mjs'], cwd=ROOT / 'benchmarks/makers',
                                    input=serialized(request), capture_output=True)
            if result.returncode:
                raise ValueError(result.stderr.decode('utf-8'))
            data = json.loads(result.stdout)
            parts, curves = [], []
            copies = [4, 10, 30, 60][index]
            for original in data['parts']:
                name = original['id']
                d = ops_path(original['ops'])
                on_fold = name in ['teagan.front', 'teagan.back', 'bruce.back']
                if on_fold:
                    variants = [(name, unfold(d))]
                else:
                    closed = d if parse_path(d).isclosed() else d + ' Z'
                    variants = [(name + '-left', closed),
                                (name + '-right', parse_path(closed).scaled(-1, 1, origin=0j).d() + ' Z')]
                for name, path in variants:
                    part, curve = source_part(name, [path], copies, GRAIN)
                    parts.append(part)
                    curves.append(curve)
            yield job(identifier, parts, [stock(1500, [3000, 4000, 6000, 10000][index], margin=15)], 3), curves, {
                'category': 'garments', 'held_out': index == 3, 'source': 'freesewing',
                'parameters': {**request, 'garment_count': copies, 'synthetic_measurements': True},
                'construction': 'Original 10 mm seam allowance cut paths at full precision. On-fold parts unfolded at X=0; each cut-two part has explicit left/right contours. Grain parallel to Y, rotations 0/180, no placement reflection. Finite 1500 mm wide roll sections.'
            }, {'freesewing.json': serialized(data)}


def lettering_jobs():
    font = TTFont(CACHE / 'NotoSans.ttf')
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    cap_height = font['OS/2'].sCapHeight
    specs = [('NESTBOLT', 25, 12, (300, 200)), ('WORKSHOP', 45, 10, (600, 400)),
             ('OPEN STUDIO', 100, 6, (1220, 2440)), ('LASER LAB', 150, 10, (1220, 2440)),
             ('TOOLS AND IDEAS', 200, 8, (1220, 2440)), ('MAKER SPACE', 60, 30, (600, 400))]
    for index, (phrase, height, copies, size) in enumerate(specs):
        parts, curves = [], []
        for char, count in sorted(Counter(phrase.replace(' ', '')).items()):
            pen = SVGPathPen(glyphs)
            scale = height / cap_height
            glyphs[cmap[ord(char)]].draw(TransformPen(pen, (scale, 0, 0, -scale, 0, 0)))
            part, curve = source_part('letter-' + char, [pen.getCommands()], copies * count, QUARTERS)
            parts.append(part)
            curves.append(curve)
        yield job(f'm-sign-{index+1}', parts, [stock(*size)], 1), curves, {
            'category': 'lettering', 'held_out': index >= 4, 'source': 'noto-sans',
            'parameters': {'text': phrase, 'copies': copies, 'cap_height_mm': height,
                           'font_variation': 'default wght=400, wdth=100'},
            'construction': 'Separate uppercase sign letters; spaces omitted; repeated characters become quantities. Font quadratic curves retained; counters remain holes.'
        }, {}


def cog(radius, teeth, bore):
    points = []
    for tooth in range(teeth):
        for phase, scale in [(0, .78), (.2, 1), (.55, 1), (.75, .78)]:
            angle = 2 * pi * (tooth + phase) / teeth
            points.append((radius + radius * scale * cos(angle), radius + radius * scale * sin(angle)))
    return [polygon_path(points), circle_path(radius, radius, bore)]


def mechanical_jobs():
    specs = [
        ('small-brackets', 1, 20, (300, 200)), ('cog-washers', 1, 30, (600, 400)),
        ('mounting-kit', 1.5, 16, (600, 400)), ('frame-inserts', 2, 30, (1220, 2440)),
        ('panel-hardware', 3, 40, (1250, 2500)), ('large-plates', 5, 12, (1500, 3000)),
        ('mixed-stock', 2, 55, (600, 400)), ('defective-stock', 3, 70, (1250, 2500)),
        ('remnant-kit', 2, 35, (1220, 2440)), ('batch-1000', 1, 250, (1250, 2500)),
        ('batch-2000', 1, 500, (1500, 3000)), ('large-mixed', 4, 90, (1500, 3000)),
    ]
    for index, (name, scale, copies, size) in enumerate(specs):
        # Dimensioned original workshop parts, without random or solver-selected geometry.
        definitions = [
            ('bracket', [polygon_path([(0, 0), (60, 0), (60, 15), (20, 15), (20, 50), (0, 50)]),
                         circle_path(10, 10, 3), circle_path(48, 7.5, 3), circle_path(10, 40, 3)]),
            ('cog', cog(28, 12 + (index % 3) * 4, 8)),
            ('frame', [rect_path(0, 0, 90, 70), rect_path(10, 10, 70, 50)]),
            ('insert', [rect_path(0, 0, 36, 22), circle_path(18, 11, 3)]),
        ]
        parts, curves = [], []
        for n, (identifier, paths) in enumerate(definitions):
            paths = [parse_path(d).scaled(scale, origin=0j).d() + ' Z' for d in paths]
            part, curve = source_part(identifier, paths, copies if index >= 9 else copies + n * 3,
                                      FREE if n == 1 else QUARTERS, n == 0)
            parts.append(part)
            curves.append(curve)
        stocks = [stock(*size)]
        if index in [6, 11]:
            large_size = size if index == 11 else (1250, 2500)
            stocks = [stock(600, 400, 2, identifier='small'), stock(1220, 2440, 1, identifier='plywood'),
                      stock(*large_size, identifier='large')]
        if index == 7:
            stocks[0]['defects'] = [{'outer': [[400, 800], [530, 800], [530, 1200], [400, 1200]], 'holes': []}]
        if index == 8:
            remnant = stock(600, 400, 2, identifier='remnant')
            remnant['outline'] = [{'outer': [[0, 0], [600, 0], [600, 240], [380, 240], [380, 400], [0, 400]], 'holes': []}]
            stocks.insert(0, remnant)
        yield job('m-mechanical-' + name, parts, stocks, 1.5), curves, {
            'category': 'mechanical', 'held_out': index >= 10, 'source': 'procedural',
            'parameters': {'linear_scale': scale, 'base_copies': copies, 'cog_teeth': 12 + (index % 3) * 4},
            'construction': 'Original dimensioned L-brackets, radial trapezoid-tooth cogs, open frames and drilled inserts. Circular holes retain arcs. Quantity mix, stock caps and defects/remnants are declared in the job.'
        }, {}


def public_jobs():
    original = (CACHE / 'openclipart-gear.svg').read_bytes()
    root = ET.fromstring(original)
    original_path = next(p.attrib['d'] for p in root.findall(f'{{{SVG_NS}}}path') if p.attrib.get('id') == 'path2125')
    path = parse_path(original_path)
    x0, x1, y0, y1 = path.bbox()
    for index, (diameter, copies, size) in enumerate([
        (50, 20, (300, 200)), (90, 24, (600, 400)), (160, 60, (1220, 2440)),
        (240, 30, (1250, 2500)), (320, 40, (1500, 3000)), (35, 500, (600, 400))]):
        parts, curves = [], []
        for n, ratio in enumerate([1, .65]):
            transformed = path.scaled(diameter * ratio / max(x1-x0, y1-y0), origin=0j)
            part, curve = source_part('gear-' + str(n+1), [transformed.d() + ' Z'], copies, FREE)
            parts.append(part)
            curves.append(curve)
        yield job(f'm-public-gear-{index+1}', parts, [stock(*size)], 1), curves, {
            'category': 'public-art', 'held_out': index >= 4, 'source': 'openclipart-gear',
            'parameters': {'maximum_dimension_mm': diameter, 'secondary_scale': .65, 'copies_each': copies},
            'construction': 'Steren Gear SVG path2125 only; out-of-view decorative text omitted explicitly. Two uniform scales, original contour detail and central hole retained. Source viewBox units converted by declared maximum dimension.'
        }, {'original.svg': original}


def write_candidate(value, curves, row, originals):
    identifier = value['name']
    directory = DEST / identifier
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'job.json').write_bytes(serialized(value))
    (directory / 'curves.json').write_bytes(serialized(curves))
    for name, data in originals.items():
        (directory / name).write_bytes(data)
    # Contact sheet of one of each part type; quantities remain in the job.
    svg = ET.Element('svg', xmlns=SVG_NS)
    x, y, row_height, width = 0, 0, 0, 0
    for part, curve in zip(value['parts'], curves):
        w = max(p[0] for c in part['geometry'] for p in c['outer'])
        h = max(p[1] for c in part['geometry'] for p in c['outer'])
        if x and x + w > 1400:
            x, y, row_height = 0, y + row_height + 20, 0
        ox, oy = curve['normalization_offset_mm']
        group = ET.SubElement(svg, 'g', id=part['id'], transform=f'translate({x-ox} {y-oy})',
                              attrib={'data-quantity': str(part['quantity'])})
        ET.SubElement(group, 'path', d=' '.join(curve['paths']),
                      attrib={'fill-rule': 'evenodd', 'fill': '#9bbdcc', 'stroke': '#20363f', 'stroke-width': '.3'})
        x += w + 20
        row_height = max(row_height, h)
        width = max(width, x)
    height = y + row_height + 20
    svg.set('viewBox', f'-10 -10 {width} {height}')
    svg.set('width', f'{width}mm')
    svg.set('height', f'{height}mm')
    (directory / 'parts.svg').write_bytes(ET.tostring(svg, encoding='utf-8', xml_declaration=True))
    row.update({'id': identifier, 'set': 'M', 'units': 'mm', 'part_count': sum(p['quantity'] for p in value['parts']),
                'files': {p.name: sha256(p.read_bytes()).hexdigest() for p in sorted(directory.iterdir()) if p.is_file()}})
    print(f'{identifier}: {row["part_count"]} copies, {len(value["parts"])} types, held_out={row["held_out"]}', flush=True)
    return row


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    rows = []
    for generate in [box_jobs, garment_jobs, lettering_jobs, mechanical_jobs, public_jobs]:
        for value, curves, row, originals in generate():
            rows.append(write_candidate(value, curves, row, originals))
    if len(rows) != 40 or sum(r['held_out'] for r in rows) != 10:
        raise ValueError('Expected exactly forty jobs and ten held-out reservations')
    (DEST / 'candidates.json').write_bytes(serialized({'status': 'authoring-only, not yet frozen', 'instances': rows}))
    print('Built 40 candidates; independent source validation and provenance freeze are required.')


if __name__ == '__main__':
    main()
