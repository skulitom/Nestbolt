"""Prepare actual common-line nests for a native LightBurn import check.

Authored MIT rectangles only; no corpus or held-out geometry is read. The native
observations and independent saved-project audit are separate records.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json, exact_size

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT/'benchmarks/results'/f'h5-lightburn-{stamp}'
    folder.mkdir(exist_ok=False)
    binary = ROOT/'target/release/nestbolt.exe'
    guards = {'product': source_digest(), 'binary': digest(binary),
              'runner': digest(Path(__file__)),
              'run_helper': digest(ROOT/'scripts/h2_lightburn_prepare.py'),
              'manifest': digest(ROOT/'benchmarks/datasets/shop/manifest.json')}
    shutil.copyfile(ROOT/'crates/core/tests/fixtures/common-panels.svg', folder/'panels.svg')
    cases = []
    for name, kerf, native_format in [('laser', 0.2, 'svg'), ('plasma', 1.5, 'dxf')]:
        case = folder/name
        case.mkdir()
        run([binary, 'import', folder/'panels.svg', '--output', case/'library.json'])
        library = json.loads((case/'library.json').read_text(encoding='utf-8'))
        request = {'name': f'H5 {name} native check',
                   'parts': [{'id': library['parts'][0]['id'], 'quantity': 2}],
                   'sheets': [{'width_mm': 86, 'height_mm': 36, 'count': 1}],
                   'spacing_mm': 5, 'edge_spacing_mm': 1}
        write_json(case/'input-request.json', request)
        run([binary, 'nest', '--library', case/'library.json', '--request', case/'input-request.json',
             '--common-line', '--kerf', kerf, '--out-dir', case/'nest',
             '--seconds', 1, '--repeatable', '--time-limit', 30], timeout=60)
        report = json.loads((case/'nest/report.json').read_text(encoding='utf-8'))
        layout = json.loads((case/'nest/layout.json').read_text(encoding='utf-8'))
        job = json.loads((case/'nest/job.json').read_text(encoding='utf-8'))
        assert report['validation']['valid'] and report['repeatable']
        assert len(layout['sheets']) == 1 and len(layout['placements']) == 2
        assert job['clearance'] == kerf
        common = report['common_line'][0]
        assert abs(common['saved_length_mm']-30) < 1e-6
        assert len(common['shared_edges']) == len(common['paths']) == 1
        expected = exact_size(library, layout)
        # The constructor adds a sub-micron-scale contact guard; compare native
        # geometry with actual exact placed bounds, not the ideal kerf alone.
        assert max(abs(a-b) for a, b in zip(expected['size_mm'], [80+kerf, 30])) < 0.0001
        exports = {}
        for extension in ['svg', 'dxf']:
            target = folder/f'{name}.{extension}'
            shutil.copyfile(case/f'nest/sheet-0.{extension}', target)
            exports[extension] = {'file': target.name, 'sha256': digest(target)}
        cases.append({'name': name, 'kerf_mm': kerf, 'native_format': native_format,
                      'expected': expected, 'individual_part_size_mm': [40, 30],
                      'common_size_mm': [0, 30], 'common_line': common, 'exports': exports,
                      'validation_valid': True, 'repeatable': True,
                      'cpu_affinity': [0], 'seconds': 1, 'seed': 0})
        print(name, expected['size_mm'], flush=True)
    assert source_digest() == guards['product']
    assert digest(binary) == guards['binary'] and digest(Path(__file__)) == guards['runner']
    assert digest(ROOT/'scripts/h2_lightburn_prepare.py') == guards['run_helper']
    assert digest(ROOT/'benchmarks/datasets/shop/manifest.json') == guards['manifest']
    write_json(folder/'preparation.json', {'recorded_at': stamp, 'held_out_read': False,
               'native_check_complete': False, 'guards': guards, 'cases': cases,
               'artifacts': {str(p.relative_to(folder)).replace('\\', '/'): digest(p)
                             for p in sorted(folder.rglob('*')) if p.is_file()}})
    (folder/'LICENSES.md').write_text('# H5 authored common-line coupon\n\n'
        'All geometry is authored by Nestbolt contributors, copyright 2026, under '
        'the repository MIT LICENSE. Native saves and screenshots derive only from '
        'this coupon. No corpus or held-out geometry was opened.\n', encoding='utf-8', newline='\n')
    print(folder)


if __name__ == '__main__':
    main()
