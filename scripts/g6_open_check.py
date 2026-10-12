"""G6 export check: nest the fidelity fixtures, then open every export in Inkscape
and LibreCAD and compare the drawing size each application reports with the
size Nestbolt placed.

Inkscape renders and measures the SVG and imports the DXF; LibreCAD prints the
DXF to PDF at 1:1, which Inkscape then measures. Sizes include stroke widths,
so they may exceed the outlines by a fraction of a millimetre. Needs Inkscape
1.4 and LibreCAD 2.2 (paths below or INKSCAPE/LIBRECAD) and a release build.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
INKSCAPE = Path(os.environ.get('INKSCAPE', r'C:\Program Files\Inkscape\bin\inkscape.com'))
LIBRECAD = Path(os.environ.get('LIBRECAD', r'C:\Program Files\LibreCAD\LibreCAD.exe'))
FIXTURES = [ROOT/'examples/fidelity/curves-mm.svg', ROOT/'examples/fidelity/plate-in.dxf']
PX = 25.4 / 96  # Inkscape reports CSS pixels
TOLERANCE_MM = 0.5


def run(command, **kwargs):
    return subprocess.run([str(c) for c in command], cwd=ROOT, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=300, **kwargs)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def drawing_mm(path):
    """Inkscape's visual bounding box of the whole drawing, in millimetres."""
    rows = run([INKSCAPE, '--query-all', path]).stdout.strip().splitlines()
    if not rows:
        raise SystemExit(f'Inkscape could not read {path}')
    _, x, y, w, h = rows[0].split(',')
    return {'width_mm': float(w) * PX, 'height_mm': float(h) * PX, 'objects': len(rows) - 1}


def readable(source, png, width):
    """A people-friendly PNG: the exports' hairlines (and LibreCAD's thin filled
    strokes, printed in near-white colour 7) redrawn thick and black. Viewing only."""
    text = Path(source).read_text(encoding='utf-8')
    text = re.sub(r'stroke:#[0-9a-fA-F]{3,6}', 'stroke:#000000', text)
    text = re.sub(r'stroke="#[0-9a-fA-F]{3,6}"', 'stroke="#000000"', text)
    text = re.sub(r'stroke-width(:|=")[0-9.e-]+', lambda m: f'stroke-width{m.group(1)}{width}', text)
    text = text.replace('stroke:none', f'stroke:#000000;stroke-width:{width}')
    view = png.with_suffix('.svg')
    view.write_text(text, encoding='utf-8')
    run([INKSCAPE, '--export-type=png', '--export-dpi=96', '--export-area-drawing',
         '--export-background=white', f'--export-filename={png}', view])


def placed_mm(job, layout):
    """Extents of the placed polygons (the exact curves lie within the import tolerance)."""
    parts = {p['id']: p for p in job['parts']}
    xs, ys = [], []
    for placement in layout['placements']:
        t = placement['transform']
        c, s = math.cos(t['rotation_radians']), math.sin(t['rotation_radians'])
        for polygon in parts[placement['part_id']]['geometry']:
            for x, y in polygon['outer']:
                x = -x if t['mirrored'] else x
                xs.append(x * c - y * s + t['translation'][0])
                ys.append(x * s + y * c + t['translation'][1])
    return {'width_mm': max(xs) - min(xs), 'height_mm': max(ys) - min(ys)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, default=ROOT/'target/release/nestbolt.exe')
    args = parser.parse_args()
    started = datetime.now(timezone.utc)
    stamp = f"{started.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    work = ROOT/'output/g6-open'/stamp
    work.mkdir(parents=True)
    library = work/'library.json'
    imported = run([args.binary, 'import', *FIXTURES, '--output', library])
    if imported.returncode:
        raise SystemExit(imported.stderr)
    lib = json.loads(library.read_text(encoding='utf-8'))
    request = {'parts': [{'id': p['id'], 'quantity': 2, 'rotations': {'kind': 'list', 'degrees': [0, 90, 180, 270]}}
                         for p in lib['parts']],
               'sheets': [{'width_mm': 400, 'height_mm': 300,
                           'margins_mm': {'left': 5, 'right': 5, 'bottom': 5, 'top': 5}}],
               'spacing_mm': 1.0, 'edge_spacing_mm': 1.0}
    (work/'request.json').write_text(json.dumps(request, indent=1), encoding='utf-8')
    nested = run([args.binary, 'nest', '--library', library, '--request', work/'request.json',
                  '--out-dir', work/'run', '--seconds', '10', '--seed', '0'])
    if nested.returncode:
        raise SystemExit(nested.stderr)
    run_dir = work/'run'
    report = json.loads((run_dir/'report.json').read_text(encoding='utf-8'))
    expected = placed_mm(json.loads((run_dir/'job.json').read_text(encoding='utf-8')),
                         json.loads((run_dir/'layout.json').read_text(encoding='utf-8')))
    svg, dxf = run_dir/'sheet-0.svg', run_dir/'sheet-0.dxf'
    checks = []

    def check(name, measured, note):
        ok = (abs(measured['width_mm'] - expected['width_mm']) <= TOLERANCE_MM
              and abs(measured['height_mm'] - expected['height_mm']) <= TOLERANCE_MM)
        checks.append({'check': name, **measured, 'pass': ok, 'note': note})

    rendered = run([INKSCAPE, '--export-type=png', '--export-dpi=150', '--export-area-drawing',
                    '--export-background=white', f'--export-filename={work/"svg-inkscape.png"}', svg])
    check('SVG opened in Inkscape', drawing_mm(svg),
          f'rendered to PNG: exit {rendered.returncode}; {svg.read_text(encoding="utf-8").count(" A ")} SVG arc commands kept')
    converted = run([INKSCAPE, '--export-type=svg', '--export-plain-svg',
                     f'--export-filename={work/"dxf-inkscape.svg"}', dxf])
    check('DXF imported by Inkscape', drawing_mm(work/'dxf-inkscape.svg'),
          f'Inkscape DXF input, exit {converted.returncode}')
    # LibreCAD's batch printer ignores --paper and uses A4, so print at a fixed
    # 1:2 scale, centred, and double the measured size. Its PNG/SVG converters
    # write nothing on Windows (2.2.1.5).
    printed = run([LIBRECAD, 'dxf2pdf', '-s', '0.5', '-c', '-m', '-o', work/'dxf-librecad.pdf', dxf])
    half = drawing_mm(work/'dxf-librecad.pdf')
    check('DXF opened in LibreCAD (printed 1:2, doubled)',
          {**half, 'width_mm': 2 * half['width_mm'], 'height_mm': 2 * half['height_mm']},
          f'LibreCAD dxf2pdf, exit {printed.returncode}; {half["objects"]} drawn objects, measured by Inkscape')
    run([INKSCAPE, '--export-type=svg', '--export-plain-svg', f'--export-filename={work/"dxf-librecad.svg"}',
         work/'dxf-librecad.pdf'])
    readable(svg, work/'readable-svg-inkscape.png', 0.8)
    readable(work/'dxf-inkscape.svg', work/'readable-dxf-inkscape.png', 2.5)
    readable(work/'dxf-librecad.svg', work/'readable-dxf-librecad.png', 3)
    versions = {
        'inkscape': run([INKSCAPE, '--version']).stdout.strip(),
        # Without a subcommand LibreCAD opens its window; dxf2pdf answers --version.
        'librecad': next((l for l in run([LIBRECAD, 'dxf2pdf', '--version']).stdout.splitlines()
                          if l.startswith('LibreCAD')), 'LibreCAD'),
        'nestbolt_binary_sha256': digest(args.binary),
    }
    result = {'scope': 'G6 export opening check (development)', 'recorded_at': started.isoformat(),
              'fixtures': {str(f.relative_to(ROOT)): digest(f) for f in FIXTURES},
              'exports': {'sheet-0.svg': digest(svg), 'sheet-0.dxf': digest(dxf)},
              'validation_valid': report['validation']['valid'], 'expected': expected,
              'tolerance_mm': TOLERANCE_MM, 'checks': checks, 'versions': versions,
              'work_directory': str(work.relative_to(ROOT)), 'pass': all(c['pass'] for c in checks)}
    out = ROOT/'benchmarks/results'/f'g6-open-{stamp}'
    out.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    lines = ['# G6 export opening check', '',
             f"Fixtures `examples/fidelity/curves-mm.svg` (mm SVG: rounded corners, circle, ellipse, Béziers, "
             f"elliptical arc, rotated frame with a hole) and `examples/fidelity/plate-in.dxf` (inch DXF: bulged "
             f"polyline, circle hole, ellipse, line-and-arc slot), two copies each, nested for 10 s and exported "
             f"once; the layout passed independent validation: **{report['validation']['valid']}**.", '',
             f"Placed drawing: {expected['width_mm']:.3f} × {expected['height_mm']:.3f} mm. Each application's "
             f"drawing size must agree within {TOLERANCE_MM} mm (strokes included).", '',
             '| Check | Width mm | Height mm | Pass | Note |', '| --- | ---: | ---: | --- | --- |']
    lines += [f"| {c['check']} | {c['width_mm']:.3f} | {c['height_mm']:.3f} | {'yes' if c['pass'] else '**no**'} | {c['note']} |"
              for c in checks]
    lines += ['', f"Versions: {versions['inkscape']}; {versions['librecad']}; Nestbolt binary "
              f"`{versions['nestbolt_binary_sha256'][:16]}`. Files and `readable-*.png` views (strokes "
              f"thickened for viewing only): `{result['work_directory']}`.",
              '', f"**Result: {'pass' if result['pass'] else 'fail'}.** LightBurn remains Artem's manual check."]
    out.with_suffix('.md').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    print(out.with_suffix('.md'))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
