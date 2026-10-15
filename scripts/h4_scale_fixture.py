"""Freeze the required H4 2,000-part letters/gears workload from shipped examples."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'benchmarks/datasets/browser-curves'


def main():
    assert not OUT.exists(), 'Never replace the frozen scale fixture'
    makers = json.loads((ROOT/'benchmarks/datasets/makers.json').read_text(encoding='utf-8'))
    assert 'm-public-gear-1' not in makers['held_out_ids']
    ns = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', ns)
    svg = ET.Element('{'+ns+'}svg', {'width': '700mm', 'height': '400mm',
                                   'viewBox': '0 0 700 400', 'fill': 'none', 'stroke': 'black'})
    sources = []
    for name in ['letters', 'gears']:
        path = ROOT/f'web/public/examples/{name}.svg'
        source = ET.fromstring(path.read_text(encoding='utf-8'))
        sources.append({'path': path.relative_to(ROOT).as_posix(),
                        'sha256': sha256(path.read_bytes()).hexdigest()})
        group = ET.SubElement(svg, '{'+ns+'}g', {'transform': 'translate(0 0)' if name == 'letters' else 'translate(500 200)'})
        if name == 'letters':
            selected = [e for e in source if e.get('id') in ['letter-S-80mm', 'letter-B-80mm']]
            assert len(selected) == 2
        else:
            selected = list(source)
        for element in selected:
            group.append(deepcopy(element))
    ids = [e.get('id') for e in svg.iter() if e.get('id')]
    assert set(ids) == {'letter-S-80mm', 'letter-B-80mm', 'gear-1', 'gear-2'}
    OUT.mkdir()
    drawing = OUT/'letters-gears-2000.svg'
    drawing.write_text(ET.tostring(svg, encoding='unicode')+'\n', encoding='utf-8', newline='\n')
    manifest = {'version': 1, 'scope': 'H4 development scale; no held-out geometry',
                'svg': drawing.name, 'sha256': sha256(drawing.read_bytes()).hexdigest(),
                'copies_per_part': 500, 'total_parts': 2000, 'ids': ids,
                'sheet_mm': [1250, 2500], 'spacing_mm': 1.5, 'edge_spacing_mm': 1.5,
                'seconds': 60, 'workers': 'app default (effective cap two above 1000 parts)',
                'sources': sources, 'license_record': 'web/public/examples/LICENSES.txt',
                'licenses': {'letters': 'Bitstream Vera / DejaVu outlined drawing geometry, as prescribed by PLAN_V1_1',
                             'gears': 'Steren Openclipart gear, public domain / CC0'},
                'generator_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
