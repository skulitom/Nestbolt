"""Check the new independent source validator on retained native-tested layouts.

No search, native application run or held-out geometry is involved. The original
mixed-settings artifacts stay unchanged; all new outputs go to a new directory.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json
from h6_lead_settings_recheck import cut_paths

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    original, output = args.original.resolve(), args.output.resolve()
    assert original.is_relative_to(ROOT/'benchmarks/results')
    assert output.is_relative_to(ROOT/'benchmarks/results') and not output.exists()
    output.mkdir(parents=True)
    inputs = [original/'library.json', original/'arc/layout.json', original/'arc/sheet-0.svg']
    inputs += [original/f'{style}-request.json' for style in ['line', 'arc']]
    inputs += [original/f'revised-2/{style}/report.json' for style in ['line', 'arc']]
    input_hashes = {str(p.relative_to(ROOT)): digest(p) for p in inputs}
    before = source_digest()
    binary = ROOT/'target/release/nestbolt.exe'
    binary_hash = digest(binary)
    rows = []
    for style in ['line', 'arc']:
        target = output/style
        target.mkdir()
        parameters = ['--library', original/'library.json', '--request', original/f'{style}-request.json',
                      '--layout', original/'arc/layout.json']
        report = json.loads(run([binary, 'validate', *parameters], cpu=0))
        write_json(target/'report.json', report)
        lead = report['lead_in']
        assert report['valid'] and lead['validation']['valid'] and lead['validation']['source_checked']
        assert lead['validation']['coverage'] == {
            'expected_contours': 6, 'reserved_contours': 4, 'flagged_contours': 2}
        previous = json.loads((original/f'revised-2/{style}/report.json').read_text(encoding='utf-8'))
        assert lead['parts'] == previous['lead_in']['parts']
        result = run([binary, 'export', *parameters, '--out-dir', target, '--sheet-outline', 'false'], cpu=0)
        (target/'export.log').write_text(result, encoding='utf-8', newline='\n')
        assert cut_paths(target/'sheet-0.svg') == cut_paths(original/'arc/sheet-0.svg')
        rows.append({'style': style, 'original_curves_and_coverage_checked': True,
                     'native_tested_plans_unchanged': True, 'cut_svg_attributes_unchanged': True})
    assert source_digest() == before and digest(binary) == binary_hash
    assert all(digest(ROOT/p) == value for p, value in input_hashes.items())
    write_json(output/'checks.json', {
        'date': datetime.now(timezone.utc).isoformat(), 'held_out_geometry_read': False,
        'scope': 'Revalidate/export retained authored native-tested searched layout; no new search or native run',
        'source_sha256': before, 'binary_sha256': binary_hash,
        'runner_sha256': digest(Path(__file__)), 'inputs': input_hashes,
        'cpu_affinity': [0], 'cases': rows,
        'artifacts': {str(p.relative_to(output)).replace('\\', '/'): digest(p)
                      for p in sorted(output.rglob('*')) if p.is_file()},
    })
    print(json.dumps(rows))


if __name__ == '__main__':
    main()
