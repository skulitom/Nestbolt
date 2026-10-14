"""Audit saved native H5 geometry independently of Nestbolt's reader/exporter."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

import ezdxf
from svgpathtools import Document
from h3_geometry_audit import normalize

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    assert not path.exists(), 'Never replace earlier evidence'
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def dimensions(path):
    x0, x1, y0, y1 = path.bbox()
    return [x1-x0, y1-y0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    folder = args.folder.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    preparation = json.loads((folder/'preparation.json').read_text(encoding='utf-8'))
    assert preparation['held_out_read'] is False
    assert digest(ROOT/'benchmarks/datasets/shop/manifest.json') == preparation['guards']['manifest']
    for name, expected in preparation['artifacts'].items():
        assert digest(folder/name) == expected, name
    work = ROOT/'output'/('h5-native-audit-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    work.mkdir()
    normalized = work/'normalized'
    normalized.mkdir()
    for row in preparation['cases']:
        name = f"{row['name']}-{row['native_format']}-native.lbrn2"
        xml, indices, omitted, zero_handles = normalize((folder/name).read_text(encoding='utf-8'))
        assert len(indices) == 3 and not omitted and not zero_handles
        (normalized/name).write_text(xml, encoding='utf-8', newline='\n')
    oracle = work/'oracle'
    subprocess.run(['node', str(ROOT/'scripts/h5_lightburn_oracle.mjs'), str(normalized), str(oracle)],
                   check=True, timeout=30, capture_output=True)
    rows = []
    for row in preparation['cases']:
        stem = f"{row['name']}-{row['native_format']}"
        root = E.parse(folder/f'{stem}-native.lbrn2').getroot()
        assert root.get('AppVersion') == '2.1.01' and root.get('DeviceName') == 'No Machine'
        layers = dict(Counter(s.get('CutIndex') for s in root.iter('Shape') if s.get('Type') != 'Group'))
        assert layers == {'0': 2, '1': 1}, layers
        settings = {s.find('index').get('Value'): s.get('type') for s in root.findall('CutSetting')}
        assert settings == {'0': 'Cut', '1': 'Cut'}
        native = Document(oracle/f'{stem}-native.svg').paths()
        assert len(native) == 3
        closed = sorted([p for p in native if p.isclosed()], key=lambda p: p.bbox()[0])
        opened = [p for p in native if not p.isclosed()]
        assert len(closed) == 2 and len(opened) == 1
        common = opened[0]
        boxes = [p.bbox() for p in native]
        size = [max(b[1] for b in boxes)-min(b[0] for b in boxes),
                max(b[3] for b in boxes)-min(b[2] for b in boxes)]
        part_errors = [max(abs(a-b) for a, b in zip(dimensions(p), [40, 30])) for p in closed]
        native_error = max(abs(a-b) for a, b in zip(size, row['expected']['size_mm']))
        cx = common.bbox()[0]
        half_kerf_distances = [cx-closed[0].bbox()[1], closed[1].bbox()[0]-cx]
        offset_error = max(abs(d-row['kerf_mm']/2) for d in half_kerf_distances)
        common_error = max(abs(a-b) for a, b in zip(dimensions(common), [0, 30]))
        assert max(native_error, offset_error, common_error, *part_errors) <= 0.00005
        assert abs(common.length()-30) <= 0.00005
        assert all(abs(p.length()-140) <= 0.00005 for p in closed)
        ui = json.loads((folder/f'{stem}-ui.json').read_text(encoding='utf-8'))
        fields = {e['bounds']['y']: float(e['text']) for e in ui['elements']
                  if e['role'] == 'Spinner' and e['bounds']['x'] == 217}
        ui_size = [fields[93], fields[124]]
        assert max(abs(a-b) for a, b in zip(ui_size, row['expected']['size_mm'])) < 0.0005
        dxf = ezdxf.readfile(folder/f"{row['name']}.dxf")
        audit = dxf.audit()
        assert not audit.errors and not audit.fixes
        assert Counter((e.dxftype(), e.dxf.layer) for e in dxf.modelspace()) == {('LINE', 'CUT'): 8, ('LINE', 'COMMON'): 1}
        assert dxf.layers.get('CUT').dxf.color == 7 and dxf.layers.get('COMMON').dxf.color == 5
        assert dxf.layers.get('CUT').dxf.true_color == 0 and dxf.layers.get('COMMON').dxf.true_color == 255
        rows.append({'name': row['name'], 'format': row['native_format'], 'kerf_mm': row['kerf_mm'],
                     'expected_size_mm': row['expected']['size_mm'], 'ui_size_mm': ui_size,
                     'native_size_mm': size, 'native_size_max_error_mm': native_error,
                     'part_sizes_mm': [dimensions(p) for p in closed], 'part_size_errors_mm': part_errors,
                     'common_size_mm': dimensions(common), 'common_length_mm': common.length(),
                     'common_half_kerf_distances_mm': half_kerf_distances,
                     'maximum_offset_error_mm': offset_error, 'native_layer_leaf_counts': layers,
                     'native_cut_settings': settings, 'dxf_audit_errors': 0, 'dxf_audit_fixes': 0,
                     'native_project': f'{stem}-native.lbrn2', 'screenshot': f'{stem}-native.png',
                     'oracle_svg_sha256': digest(oracle/f'{stem}-native.svg')})
    result = {'recorded_at': datetime.now(timezone.utc).isoformat(), 'held_out_read': False,
              'native_check_complete': True, 'milestone_h5_complete': False,
              'scope': 'Two authored repeatable search exports; no savings gate or competitor comparison',
              'lightburn': 'Pro 2.1.01', 'anode': '0.11.2, hidden session 3, No Machine, 1920x1080 at 100%',
              'native_warnings': False, 'cleanup': 'Owned LightBurn closed; display restored; lease released',
              'independent_oracle': 'lbrn2-to-svg 0.5.3 (MIT), unmodified published package',
              'oracle_normalization': 'Existing H3 normalization composes group transforms into leaves and resolves references before conversion. Raw direct-conversion failure is retained in probes/.',
              'oracle_palette_note': 'The oracle uses a different colour table. Actual native CutIndex 0/1 and screenshots prove CUT/COMMON palette mapping; oracle SVG colours are not palette evidence.',
              'python_versions': {p: importlib.metadata.version(p) for p in ['svgpathtools', 'ezdxf']},
              'script_sha256': digest(Path(__file__)), 'oracle_runner_sha256': digest(ROOT/'scripts/h5_lightburn_oracle.mjs'),
              'normalization_script_sha256': digest(ROOT/'scripts/h3_geometry_audit.py'),
              'rows': rows, 'artifacts': {str(p.relative_to(folder)).replace('\\', '/'): digest(p)
                                        for p in sorted(folder.rglob('*')) if p.is_file()}}
    write_json(folder/'native-audit.json', result)
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
