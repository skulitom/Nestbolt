"""Prepare five actual searches for the H3 native LightBurn check.

Only four explicitly selected frozen training projects and one original MIT
origin probe are read. The split is checked before opening any source or label.
This is format/fidelity evidence, not a new solver-quality acceptance run.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

import psutil
from h2_import_audit import source_digest
from h2_lightburn_prepare import write_json
from h3_writer_audit import audit

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'
CASES = [('tri-hard', 'native/lb-02.lbrn2', 560, 340),
         ('lacc-bottom', 'native/lb-07.lbrn2', 1200, 650),
         ('lacc-side', 'native/lb-09.lbrn2', 640, 440),
         ('sofle', 'native/lb-11.lbrn2', 440, 300),
         ('mirrored-origin', 'probes/origin-top-right.lbrn2', 160, 120)]


def main():
    psutil.Process().cpu_affinity([8])
    raw = (CORPUS/'manifest.json').read_bytes()
    manifest = json.loads(raw)
    training = {r['path']:r for r in manifest['files'] if r['split'] == 'training'}
    digest = source_digest()
    binary = ROOT/'target/release/nestbolt.exe'
    binary_digest = sha256(binary.read_bytes()).hexdigest()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT/'benchmarks/results'/f'h3-lightburn-{stamp}'
    folder.mkdir()
    cases = []
    for name, relative, width, height in CASES:
        if relative.startswith('native/'):
            row = training[relative]
            source = CORPUS/row['path']
            assert sha256(source.read_bytes()).hexdigest() == row['sha256']
            provenance = {k:row[k] for k in ['licence','source','derived_from','sha256','split']}
        else:
            assert relative == 'probes/origin-top-right.lbrn2'
            source = CORPUS/relative
            provenance = dict(licence='MIT', source='Original Nestbolt geometry.svg native origin probe',
                              sha256=sha256(source.read_bytes()).hexdigest(), split='authored probe; not a frozen input')
        case = folder/name
        case.mkdir()
        request = dict(sheets=[dict(width_mm=width, height_mm=height)], spacing_mm=2, edge_spacing_mm=2)
        write_json(case/'request.json', request)
        def run(command, label, timeout=120):
            result = subprocess.run(list(map(str, command)), cwd=ROOT, capture_output=True, timeout=timeout)
            (case/f'{label}.stdout.txt').write_bytes(result.stdout)
            (case/f'{label}.stderr.txt').write_bytes(result.stderr)
            return result
        command = [binary,'nest','--library',source,'--request',case/'request.json','--out-dir',case/'nested',
                   '--seconds','3','--repeatable','--time-limit','90']
        result = run(command, 'search')
        record = dict(name=name, source=str(source.relative_to(ROOT)), provenance=provenance,
                      request=request, command=list(map(str, command)), exit_code=result.returncode)
        if result.returncode == 0:
            report = json.loads((case/'nested/report.json').read_text(encoding='utf-8'))
            record['validation'] = report['validation']
            assembly_result = run(['target/release/examples/lightburn_roundtrip.exe',source], 'assembly')
            assert assembly_result.returncode == 0
            assembly = json.loads(assembly_result.stdout)
            assert assembly['status'] == 'written'
            scene_result = run(['target/release/examples/lightburn_inspect.exe',source], 'source-scene')
            assert scene_result.returncode == 0
            scene = json.loads(scene_result.stdout)['scene']
            # Feed actual search placements to the independent canonical-diff
            # checker. It does not accept the solver's embedded output geometry.
            layout = json.loads((case/'nested/layout.json').read_text(encoding='utf-8'))
            library_path = case/'library.json'
            assert run([binary,'import',source,'--output',library_path], 'import').returncode == 0
            library = json.loads(library_path.read_text(encoding='utf-8'))
            unit_ids = library['lightburn']['unit_ids']
            payload = dict(nesting=assembly['nesting'], identity_byte_equal=assembly['identity_byte_equal'],
                           width_mm=width, height_mm=height, validation=report['validation'], files=[])
            for i, sheet in enumerate(layout['sheets']):
                xml = (case/'nested'/report['files'][i]).read_text(encoding='utf-8')
                placements = [dict(unit=unit_ids.index(p['part_id']),transform=p['transform'])
                              for p in layout['placements'] if p['sheet_id'] == sheet['id']]
                payload['files'].append(dict(sheet=i, xml=xml, placements=placements))
            record['canonical_diff'] = audit(source.read_text(encoding='utf-8'), payload)
            record['files'] = report['files']
            record['units'] = assembly['nesting']['units']
            record['fixed'] = assembly['nesting']['fixed']
            record['source_origin'] = [scene['mirror_x'], scene['mirror_y']]
            root = E.parse(source).getroot()
            record['settings'] = [{'family':n.tag,'index':n.find('index').get('Value'),
                'canonical_sha256':sha256(E.canonicalize(E.tostring(n,encoding='unicode'),strip_text=True).encode()).hexdigest()}
                for n in root if n.tag in ['CutSetting','CutSetting_Img']]
        cases.append(record)
        write_json(folder/'prepared.json', dict(scope='Five actual training/authored searches for native H3 checks; native verification still required',
            manifest_sha256=sha256(raw).hexdigest(), source_digest=digest, binary_sha256=binary_digest,
            affinity='CPU 8; one CCD0 physical core; sequential child processes inherit affinity', cases=cases))
        print(name, 'exit',result.returncode, 'sheets',len(record.get('files',[])), flush=True)
    assert digest == source_digest(), 'Sources changed during native preparation'
    assert binary_digest == sha256(binary.read_bytes()).hexdigest(), 'Binary changed during native preparation'
    print(folder)


if __name__ == '__main__':
    main()
