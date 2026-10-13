"""Prepare five training-only nests (ten exports) for the native H2 check.

Expected sizes are analytic bounds of the library's exact curves after placement,
computed independently here rather than taken from re-imported exports. Does not
run or score held-out files. Native observations are recorded separately.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
import shutil
import subprocess

import psutil
from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'benchmarks/datasets/shop'
CASES = [
    ('fusion', 'real/tahnok--lacc/13eb7081-side.dxf'),
    ('freecad', 'real/nasa-jpl--open-source-rover/a14b3446-top_front.dxf'),
    ('legacy', 'real/keebio--iris-case/725b3b48-iris-switch-plate_left.dxf'),
    ('splines', 'generated/bezier--fusion-splines-extrusion.dxf'),
    ('inches', 'generated/rounded--missing-units-inches.dxf'),
]


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def run(args, cpu=0, timeout=90):
    proc = subprocess.Popen(list(map(str, args)), cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW | 4)
    try:
        child = psutil.Process(proc.pid)
        child.cpu_affinity([cpu])
        child.resume()
        stdout, stderr = proc.communicate(timeout=timeout)
    except BaseException:
        proc.kill()
        proc.communicate()
        raise
    if proc.returncode:
        raise RuntimeError(stderr.decode('utf-8', errors='replace'))
    return stdout.decode('utf-8')


def point(p, transform, vector=False):
    x, y = p
    if transform['mirrored']:
        x = -x
    c, s = math.cos(transform['rotation_radians']), math.sin(transform['rotation_radians'])
    tx, ty = (0, 0) if vector else transform['translation']
    return [x*c-y*s+tx, x*s+y*c+ty]


def bezier_candidates(points):
    ts = [0.0, 1.0]
    for axis in [0, 1]:
        p = [v[axis] for v in points]
        if len(p) == 3:
            den = p[0]-2*p[1]+p[2]
            if den:
                ts.append((p[0]-p[1])/den)
        else:
            a, b, c = -p[0]+3*p[1]-3*p[2]+p[3], 2*(p[0]-2*p[1]+p[2]), p[1]-p[0]
            epsilon = 1e-14*max(abs(a), abs(b), abs(c), 1)
            if abs(a) < epsilon:
                if abs(b) >= epsilon:
                    ts.append(-c/b)
            elif b*b-4*a*c >= 0:
                root = math.sqrt(b*b-4*a*c)
                ts.extend([(-b-root)/(2*a), (-b+root)/(2*a)])
    for t in ts:
        if 0 <= t <= 1:
            work = points
            while len(work) > 1:
                work = [[(1-t)*a[k]+t*b[k] for k in [0, 1]] for a, b in zip(work, work[1:])]
            yield work[0]


def contour_candidates(contour, transform):
    at = contour['start']
    yield point(at, transform)
    for segment in contour['segments']:
        kind = segment['kind']
        if kind == 'arc':
            center = point(segment['center'], transform)
            rx, ry = segment['radii']
            c, s = math.cos(segment['rotation']), math.sin(segment['rotation'])
            u, v = point([rx*c, rx*s], transform, True), point([-ry*s, ry*c], transform, True)
            start, sweep = segment['start'], segment['sweep']
            angles = [start, start+sweep]
            for axis in [0, 1]:
                t = math.atan2(v[axis], u[axis])
                for candidate in [t, t+math.pi]:
                    delta = ((candidate-start)*(1 if sweep >= 0 else -1)) % math.tau
                    if delta <= abs(sweep)+1e-12:
                        angles.append(candidate)
            for t in angles:
                yield [center[k]+u[k]*math.cos(t)+v[k]*math.sin(t) for k in [0, 1]]
            t = start+sweep
            at = [segment['center'][0]+rx*c*math.cos(t)-ry*s*math.sin(t),
                  segment['center'][1]+rx*s*math.cos(t)+ry*c*math.sin(t)]
        else:
            controls = segment.get('controls', [segment['control']] if 'control' in segment else [])
            points = [point(p, transform) for p in [at, *controls, segment['to']]]
            yield from points if kind == 'line' else bezier_candidates(points)
            at = segment['to']


def exact_size(library, layout):
    parts = {p['id']: p for p in library['parts']}
    points = [v for placement in layout['placements']
              for v in contour_candidates(parts[placement['part_id']]['outer'], placement['transform'])]
    bounds = [min(p[0] for p in points), min(p[1] for p in points),
              max(p[0] for p in points), max(p[1] for p in points)]
    return {'bounds_mm': bounds, 'size_mm': [bounds[2]-bounds[0], bounds[3]-bounds[1]]}


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT / 'output' / f'h2-lightburn-{stamp}'
    out = ROOT / 'benchmarks/results' / f'h2-lightburn-{stamp}'
    work.mkdir(exist_ok=False)
    out.mkdir(exist_ok=False)
    binary = ROOT / 'target/release/nestbolt.exe'
    digest = source_digest()
    script_digest = sha256(Path(__file__).read_bytes()).hexdigest()
    manifest_bytes = (CORPUS/'manifest.json').read_bytes()
    training = {f['path']: f for f in json.loads(manifest_bytes)['files'] if f['split'] == 'training'}
    rows = []
    for name, path in CASES:
        row = training[path]  # Split is checked before any geometry/label read.
        assert sha256((CORPUS/path).read_bytes()).hexdigest() == row['sha256']
        label_bytes = (CORPUS/row['label']).read_bytes()
        assert sha256(label_bytes).hexdigest() == row['label_sha256']
        label = json.loads(label_bytes)
        case = work/name
        case.mkdir()
        args = [binary, 'import', CORPUS/path, '--output', case/'library.json']
        options = label.get('import_options', {})
        for key, flag in [('layers', '--layers'), ('colors', '--colors'), ('close_gaps_mm', '--close-gaps')]:
            if key in options:
                v = options[key]
                args += [flag, ','.join(map(str, v)) if isinstance(v, list) else str(v)]
        if options.get('units') == 'in':
            args += ['--dxf-unit-mm', '25.4']
        run(args)
        library = json.loads((case/'library.json').read_text(encoding='utf-8'))
        sizes = [(p['bounds_mm'][2]-p['bounds_mm'][0], p['bounds_mm'][3]-p['bounds_mm'][1]) for p in library['parts']]
        width = math.ceil(sum(2*(w+4) for w, _ in sizes)+20)
        height = math.ceil(max(max(w, h) for w, h in sizes)+20)
        request = {'name': name, 'parts': [{'id': p['id'], 'quantity': 2} for p in library['parts']],
                   'sheets': [{'width_mm': width, 'height_mm': height, 'count': 1,
                               'margins_mm': {'left': 5, 'right': 5, 'top': 5, 'bottom': 5}}],
                   'spacing_mm': 2, 'edge_spacing_mm': 1}
        write_json(case/'request.json', request)
        run([binary, 'nest', '--library', case/'library.json', '--request', case/'request.json',
             '--out-dir', case/'nest', '--seconds', '1', '--repeatable', '--time-limit', '240'], timeout=300)
        report = json.loads((case/'nest/report.json').read_text(encoding='utf-8'))
        layout = json.loads((case/'nest/layout.json').read_text(encoding='utf-8'))
        assert report['validation']['valid'] and len(layout['sheets']) == 1
        exports = {}
        for ext in ['svg', 'dxf']:
            target = out/f'{name}.{ext}'
            shutil.copyfile(case/f'nest/sheet-0.{ext}', target)
            exports[ext] = {'file': target.name, 'sha256': sha256(target.read_bytes()).hexdigest()}
        rows.append({'name': name, 'source': path, 'source_sha256': row['sha256'],
                     'label': row['label'], 'label_sha256': row['label_sha256'],
                     'source_url': row.get('source'), 'licence': row['licence'],
                     'source_attribution': 'benchmarks/datasets/shop/LICENSES.md',
                     'import_options': options, 'placed_parts': len(layout['placements']),
                     'nest_elapsed_s': report['elapsed_s'], 'repeatable': report['repeatable'],
                     'validation_valid': True, 'expected': exact_size(library, layout), 'exports': exports,
                     'library_sha256': sha256((case/'library.json').read_bytes()).hexdigest(),
                     'layout': layout})
        print(name, rows[-1]['expected']['size_mm'], flush=True)
    run([ROOT/'target/release/examples/export_palette.exe', work/'palette'])
    for p in (work/'palette').iterdir():
        shutil.copyfile(p, out/p.name)
    assert source_digest() == digest, 'Product sources changed during preparation'
    assert sha256(Path(__file__).read_bytes()).hexdigest() == script_digest
    write_json(out/'preparation.json', {'recorded_at': stamp, 'held_out_read': False, 'native_check_complete': False,
               'source_sha256': digest, 'binary_sha256': sha256(binary.read_bytes()).hexdigest(),
               'preparation_script_sha256': script_digest,
               'palette_binary_sha256': sha256((ROOT/'target/release/examples/export_palette.exe').read_bytes()).hexdigest(),
               'manifest_sha256': sha256(manifest_bytes).hexdigest(), 'work_directory': str(work), 'cases': rows})
    (out/'LICENSES.md').write_text('# H2 native-check derivatives\n\n'
        'The SVG/DXF files are transformed derivatives of the sources listed in `preparation.json`; '
        'they retain those source licences. Full upstream attribution and licence texts are in '
        '`../../datasets/shop/LICENSES.md` and its referenced files. Native saves and screenshots '
        'of these files retain the same attribution. The authored palette coupon is MIT, copyright '
        '2026 Nestbolt contributors, under the repository LICENSE.\n', encoding='utf-8', newline='\n')
    print(out)


if __name__ == '__main__':
    main()
