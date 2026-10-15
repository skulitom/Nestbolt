"""Prepare authored public-CLI lead settings checks; no corpus files are read."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT/'benchmarks/results'/f'h6-lead-settings-{stamp}'
    folder.mkdir(exist_ok=False)
    binary = ROOT/'target/release/nestbolt.exe'
    before = source_digest()
    binary_hash = digest(binary)
    source = ROOT/'crates/core/tests/fixtures/leads.svg'
    (folder/'leads.svg').write_bytes(source.read_bytes())
    imported = run([binary, 'import', folder/'leads.svg', '--output', folder/'library.json'])
    (folder/'import.log').write_text(imported, encoding='utf-8', newline='\n')
    cases = []
    for style in ['line', 'arc']:
        request = {'parts': [{'id': 'leads-1', 'quantity': 2}],
                   'sheets': [{'width_mm': 60, 'height_mm': 35, 'count': 1}],
                   'spacing_mm': 0.2, 'edge_spacing_mm': 1,
                   'lead_in': {'kerf_mm': 0.2, 'style': style}}
        write_json(folder/f'{style}-request.json', request)
        command = [binary, 'nest', '--library', folder/'library.json', '--request',
                   folder/f'{style}-request.json', '--out-dir', folder/style,
                   '--seconds', '1', '--repeatable', '--time-limit', '30']
        report = json.loads(run(command, timeout=90))
        leads = report['lead_in']
        assert report['validation']['valid'] and leads['validation']['valid']
        assert (leads['expected_contours'], leads['reserved_contours'], leads['flagged_contours']) == (6, 4, 2)
        assert all(sum(r['shortened'] for r in p['reservations']) == 1 for p in leads['parts'])
        cases.append({'style': style, 'command': list(map(str, command)),
                      'expected_contours': 6, 'reserved_contours': 4, 'flagged_contours': 2,
                      'lengths_mm': [[r['length_mm'] for r in p['reservations']] for p in leads['parts']]})
    assert source_digest() == before and digest(binary) == binary_hash
    write_json(folder/'preparation.json', {
        'held_out_read': False, 'native_check_complete': False,
        'scope': 'Authored public-CLI searches; separate layer/native lead settings remain to verify',
        'source_sha256': before, 'binary_sha256': binary_hash,
        'runner_sha256': digest(Path(__file__)),
        'cpu_affinity': [0], 'cases': cases,
        'artifacts': {p.relative_to(folder).as_posix(): digest(p)
                      for p in sorted(folder.rglob('*')) if p.is_file()}})
    (folder/'LICENSES.md').write_text(
        '# Authored settings checks\n\nAll geometry and derived native files/screenshots '
        'are authored by Nestbolt contributors, copyright 2026, under the repository MIT LICENSE.\n',
        encoding='utf-8', newline='\n')
    print(folder)


if __name__ == '__main__':
    main()
