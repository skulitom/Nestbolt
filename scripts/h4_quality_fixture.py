"""Freeze H4's two shipped examples using their actual public request settings.

The other nine subset jobs are already in the frozen development manifest.
Do not regenerate this folder after a measurement; its hashes are the inputs.
"""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from h6_material_cost import run, equivalent

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'benchmarks/datasets/browser-quality'
CLI = ROOT/'target/release/nestbolt.exe'
HELPER = ROOT/'target/release/examples/project_job.exe'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def main():
    assert not OUT.exists(), 'Never replace the frozen quality examples'
    OUT.mkdir()
    source = ROOT/'web/public/examples'
    examples = json.loads((source/'examples.json').read_bytes())
    cases = []
    for example in [e for e in examples if e['id'] in ['letters', 'gears']]:
        folder = OUT/example['id']
        folder.mkdir()
        command = run([CLI, 'import', source/example['file'], '--output', folder/'library.json'],
                      folder, 'import', 0, 30)
        assert command['exit_code'] == 0
        library = json.loads((folder/'library.json').read_bytes())
        parts = []
        elements = set()
        for part in library['parts']:
            element = part['source'].split('#')[1].split(':')[0]
            elements.add(element)
            assert element in example['quantities'], element
            parts.append({'id': part['id'], 'quantity': example['quantities'][element],
                          'rotations': example.get('overrides', {}).get(element, example['rotations']),
                          'allow_mirror': False, 'priority': 1})
        assert elements == set(example['quantities']), 'A shipped example element was lost'
        request = {'name': 'H4 browser example: '+example['id'], 'parts': parts,
                   'sheets': [{'id': 'sheet-type-1', 'width_mm': example['sheet'][0],
                               'height_mm': example['sheet'][1], 'count': None,
                               'margins_mm': dict.fromkeys(['left', 'right', 'bottom', 'top'], example['margin']),
                               'defects_mm': []}],
                   'spacing_mm': example['spacing'], 'edge_spacing_mm': example['edge'], 'mode': 'all'}
        write(folder/'request.json', request)
        converted = run([HELPER, folder/'library.json', folder/'request.json'], folder, 'job', 0, 30)
        assert converted['exit_code'] == 0
        # Keep the helper's exact serialization as the benchmark input.
        (folder/'job.json').write_bytes((folder/'job-stdout.json').read_bytes())
        job = json.loads((folder/'job.json').read_bytes())
        assert len(job['parts']) == len(library['parts'])
        assert job['clearance'] == example['spacing'] + 2*library['tolerance']
        assert job['edge_clearance'] == example['edge'] + library['tolerance']
        geometry_delta = 0.0
        for actual, original, wanted in zip(job['parts'], library['parts'], parts):
            geometry_delta = max(geometry_delta, equivalent(
                actual['geometry'], original.get('components') or [original['polygon']]))
            assert all(actual[k] == v for k, v in wanted.items())
        cases.append({'id': 'example-'+example['id'], 'path': (folder/'job.json').relative_to(ROOT).as_posix(),
                      'sha256': digest(folder/'job.json'), 'parts': len(job['parts']),
                      'copies': sum(p['quantity'] for p in job['parts']),
                      'declared_glyph_quantities': sum(example['quantities'].values()),
                      'maximum_geometry_json_roundtrip_difference': geometry_delta,
                      'source': (source/example['file']).relative_to(ROOT).as_posix(),
                      'source_sha256': digest(source/example['file']), 'example': example,
                      'import_command': command, 'job_command': converted,
                      'library': (folder/'library.json').relative_to(ROOT).as_posix(),
                      'request': (folder/'request.json').relative_to(ROOT).as_posix()})
    assert len(cases) == 2
    manifest = {'scope': __doc__, 'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                'seconds': 60, 'seeds': [0, 1, 2], 'quick_start': False,
                'source_manifest': digest(source/'examples.json'),
                'licenses': 'web/public/examples/LICENSES.txt',
                'cli_sha256': digest(CLI), 'helper_sha256': digest(HELPER),
                'generator_sha256': digest(Path(__file__)), 'cases': cases,
                'files': {p.relative_to(OUT).as_posix(): digest(p) for p in sorted(OUT.rglob('*')) if p.is_file()}}
    write(OUT/'manifest.json', manifest)
    print(json.dumps({'cases': [{k: r[k] for k in ['id', 'parts', 'copies', 'declared_glyph_quantities']} for r in cases]}))


if __name__ == '__main__':
    main()
