"""G6 fidelity: exported parts match the imported ones within 0.01 mm.

Runs `crates/core/examples/fidelity.rs` over the fidelity fixtures, the example
parts and, when present, the pinned boxes.py example drawings
(`.cache/upstream/boxes/examples`, generated drawings outside boxes.py's GPL;
not committed). Each file is imported, nested with mirroring allowed, exported
to SVG and DXF and re-imported; every placed contour is compared with its source
curves under the same placement (Hausdorff distance in mm, curves flattened at
0.0005 mm). Writes a report under benchmarks/results/.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
LIMIT_MM = 0.01
FIXTURES = ['examples/fidelity/curves-mm.svg', 'examples/fidelity/plate-in.dxf',
            'examples/fidelity/badge-in.svg', 'examples/parts.svg']
CORPUS = ROOT/'.cache/upstream/boxes'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jsonl', type=Path, help='reuse measurements written by the fidelity example')
    args = parser.parse_args()
    started = datetime.now(timezone.utc)
    binary = ROOT/'target/release/examples/fidelity.exe'
    files = [ROOT/f for f in FIXTURES] + sorted((CORPUS/'examples').glob('*.svg'))
    if args.jsonl:
        lines = args.jsonl.read_text(encoding='utf-8').splitlines()
    else:
        subprocess.run(['cargo', 'build', '--release', '--locked', '-p', 'nestbolt-core', '--example', 'fidelity'],
                       cwd=ROOT, check=True)
        lines = subprocess.run([str(binary), *map(str, files)], cwd=ROOT, check=True, capture_output=True,
                               text=True, encoding='utf-8').stdout.splitlines()
    rows = [json.loads(l) for l in lines if l.strip()]
    measured = [r for r in rows if 'max_hausdorff_mm' in r]
    skipped = [r for r in rows if 'skipped' in r]
    errors = [r for r in rows if 'error' in r]
    worst = {f: max((r['max_hausdorff_mm'].get(f) or float('inf')) for r in measured) for f in ['svg', 'dxf']}
    rings = sum(r['rings_compared'] for r in measured)
    unmatched = sum(r['unmatched'] for r in measured)
    kinds = {}
    for r in measured:
        for k, v in r['segments'].items():
            kinds[k] = kinds.get(k, 0) + v
    failing = [r['file'] for r in measured
               if r['unmatched'] or any((r['max_hausdorff_mm'].get(f) or float('inf')) > LIMIT_MM for f in ['svg', 'dxf'])]
    revision = subprocess.run(['git', '-C', str(CORPUS), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    passed = not failing and not errors and unmatched == 0
    result = {'scope': 'G6 export fidelity (development)', 'recorded_at': started.isoformat(),
              'limit_mm': LIMIT_MM, 'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
              'boxes_revision': revision or None, 'files': len(rows), 'measured': len(measured),
              'skipped': [{'file': r['file'], 'reason': r['skipped']} for r in skipped],
              'errors': errors, 'rings_compared': rings, 'unmatched': unmatched,
              'max_hausdorff_mm': worst, 'segments': kinds, 'failing': failing,
              'source_reuse': str(args.jsonl) if args.jsonl else None, 'rows': rows, 'pass': passed}
    stamp = f"{started.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    out = ROOT/'benchmarks/results'/f'g6-fidelity-{stamp}'
    out.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    fixtures = [r for r in measured if any(r['file'] == Path(f).name for f in FIXTURES)]
    lines = ['# G6 export fidelity', '',
             f'{len(rows)} files: the fidelity fixtures, the example parts and {len(rows) - len(FIXTURES)} '
             f'boxes.py example drawings (revision `{revision[:12] or "absent"}`). Each is imported, nested '
             f'(quarter turns, mirroring allowed), exported to SVG and DXF and re-imported; every placed contour '
             f'is compared with its source curves under the same placement.', '',
             f'- Measured files: **{len(measured)}**; no closed outlines or not importable: {len(skipped)}; '
             f'errors: {len(errors)}.',
             f'- Contours compared: **{rings}** (both formats); unmatched: **{unmatched}**.',
             f"- Largest Hausdorff distance: SVG **{worst['svg']:.2e} mm**, DXF **{worst['dxf']:.2e} mm** "
             f'(limit {LIMIT_MM} mm).',
             f"- Source segments kept as curves: {', '.join(f'{k} {v}' for k, v in sorted(kinds.items()))}.", '',
             '| Fixture | Parts | Contours | SVG mm | DXF mm | Segments |', '| --- | ---: | ---: | ---: | ---: | --- |']
    lines += [f"| {r['file']} | {r['parts']} | {r['rings_compared']} | {r['max_hausdorff_mm']['svg']:.2e} | "
              f"{r['max_hausdorff_mm']['dxf']:.2e} | {', '.join(f'{k} {v}' for k, v in sorted(r['segments'].items()))} |"
              for r in fixtures]
    if skipped:
        lines += ['', 'Not measured (no closed outline survives import):', '']
        lines += [f"- {r['file']}: {r['skipped']}" for r in skipped]
    if errors:
        lines += ['', 'Errors:', ''] + [f"- {r['file']}: {r['error']}" for r in errors]
    lines += ['', f"**Result: {'pass' if passed else 'fail'}.** Failing files: {', '.join(failing) or 'none'}."]
    out.with_suffix('.md').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    print(out.with_suffix('.md'))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
