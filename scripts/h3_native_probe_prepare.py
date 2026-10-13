"""Controlled native writer probes using original MIT format fixtures only.

These are explicit placements, not search results and not the full H3 gate.
Never opens the held-out corpus. Each source is in the authored probes folder.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json

ROOT = Path(__file__).resolve().parents[1]


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT / 'benchmarks/results' / f'h3-native-probe-{stamp}'
    folder.mkdir()
    digest_before = source_digest()
    cases = [
        ('text-moved', 'features-line-leads', 2, 0, False, [20, 40]),
        ('text-rotated', 'features-line-leads', 2, 90, False, [80, 10]),
        ('group-mirrored', 'features-line-leads', 0, 90, True, [150, 220]),
        ('bitmap-rehomed', 'features-line-leads', 4, 90, True, [140, 210]),
    ] + [(f'origin-{corner}', f'origin-{corner}', 0, 0, False, [-100, -62.05078])
         for corner in ['bottom-left', 'top-left', 'top-right', 'bottom-right']]
    records = []
    for name, stem, unit, degrees, mirrored, translation in cases:
        source = ROOT / 'benchmarks/datasets/shop/probes' / f'{stem}.lbrn2'
        raw = source.read_bytes()
        # Read the assembly from the existing deterministic diagnostic. The
        # output used below comes from the separate controlled-placement tool.
        assembly = json.loads(run(['target/release/examples/lightburn_roundtrip.exe', source]))
        assert assembly['status'] == 'written'
        transform = dict(translation=translation, rotation_radians=math.radians(degrees), mirrored=mirrored)
        request = dict(width_mm=300, height_mm=200, outline=False,
                       placements=[dict(unit=unit, transform=transform)])
        request_path = folder / f'{name}.request.json'
        write_json(request_path, request)
        output = run(['target/release/examples/lightburn_place.exe', source, request_path])
        output_path = folder / f'{name}.lbrn2'
        output_path.write_text(output, encoding='utf-8', newline='\n')
        scene = json.loads(run(['target/release/examples/lightburn_inspect.exe', output_path]))['scene']
        tops = [s for s in scene['shapes'] if s['parent'] is None]
        assert len(tops) == 1
        bounds = tops[0]['bounds_mm']
        records.append(dict(name=name, source=str(source.relative_to(ROOT)), source_sha256=sha256(raw).hexdigest(),
                            output=str(output_path.relative_to(ROOT)), output_sha256=sha256(output_path.read_bytes()).hexdigest(),
                            request=request, bounds_mm=bounds,
                            centre_mm=[(bounds[0]+bounds[2])/2, (bounds[1]+bounds[3])/2],
                            size_mm=[bounds[2]-bounds[0],bounds[3]-bounds[1]],
                            mirror_x=scene['mirror_x'],mirror_y=scene['mirror_y'],
                            kind=tops[0]['kind'],members=assembly['nesting']['units'][unit]['members']))
    assert digest_before == source_digest(), 'source changed during preparation'
    report = dict(scope='Controlled placements of original MIT format probes; not full H3 acceptance',
                  licence='MIT; LICENSE at repository root; derived from original Nestbolt format probes',
                  source_digest=digest_before,
                  binary_sha256={name:sha256((ROOT/'target/release/examples'/f'{name}.exe').read_bytes()).hexdigest()
                                 for name in ['lightburn_place','lightburn_roundtrip','lightburn_inspect']},
                  cases=records)
    write_json(folder / 'prepared.json', report)
    print(folder)
    for c in records:
        print(c['name'], 'centre', c['centre_mm'], 'size', c['size_mm'])


if __name__ == '__main__':
    main()
