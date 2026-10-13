"""Audit retained H2 native saves and exports, without reading corpus geometry.

Run with the pinned shop venv after the native GUI observations are saved.
The output is a new JSON record, not an edit to any previous observation.
"""
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

ROOT = Path(__file__).resolve().parents[1]
PALETTE = {'CUT': (7, 0), 'COMMON': (5, 255), 'LEADIN': (1, 16711680), 'SHEET': (30, 15952166)}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def svg_size(path):
    boxes = [v.bbox() for v in Document(path).paths()]
    return [float(max(v[1] for v in boxes)-min(v[0] for v in boxes)),
            float(max(v[3] for v in boxes)-min(v[2] for v in boxes))]


def native_layers(path):
    root = E.parse(path).getroot()
    assert root.get('AppVersion') == '2.1.01'
    return {'cut_settings': {c.find('index').get('Value'): c.get('type') for c in root.findall('CutSetting')},
            'shapes_by_cut_index': dict(Counter(s.get('CutIndex') for s in root.iter('Shape')
                                               if s.get('Type') != 'Group'))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    folder = args.results.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    assert not args.output.exists(), 'Never replace an earlier audit'
    preparation = json.loads((folder/'preparation.json').read_text(encoding='utf-8'))
    observed = json.loads((folder/'native-observations.json').read_text(encoding='utf-8'))
    assert preparation['held_out_read'] is False and observed['held_out_read'] is False
    # Metadata selection only: no corpus geometry or label paths are opened.
    manifest_path = ROOT/'benchmarks/datasets/shop/manifest.json'
    assert digest(manifest_path) == preparation['manifest_sha256']
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    training = {r['path']: r for r in manifest['files'] if r['split'] == 'training'}
    for row in preparation['cases']:
        assert row['source_sha256'] == training[row['source']]['sha256']
        assert row['label_sha256'] == training[row['source']]['label_sha256']
        assert row['validation_valid'] and row['repeatable']
    work = ROOT/'output'/('h2-native-oracle-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    oracle_run = subprocess.run(['node', str(ROOT/'scripts/h2_lightburn_oracle.mjs'), str(folder), str(work)],
                                cwd=ROOT, check=True, capture_output=True, text=True, timeout=30)
    rows = []
    artifacts = ['preparation.json', 'native-observations.json', 'expected.json']
    for row in preparation['cases']:
        for fmt in ['dxf', 'svg']:
            name = row['exports'][fmt]['file']
            assert digest(folder/name) == row['exports'][fmt]['sha256']
            stem = f"{row['name']}-{fmt}-native"
            measurement = next(m for m in observed['measurements'] if m['file'] == name)
            assert measurement['warnings'] is False and measurement['lightburn_layer'] == 'C00'
            layers = native_layers(folder/(stem+'.lbrn2'))
            assert set(layers['shapes_by_cut_index']) == {'0'}
            assert layers['cut_settings'] == {'0': 'Cut'}
            size = svg_size(work/(stem+'.svg'))
            expected = row['expected']['size_mm']
            rows.append({'file': name, 'expected_mm': expected, 'native_ui_mm': measurement['size_mm'],
                         'native_saved_geometry_mm': size,
                         'ui_max_error_mm': max(abs(a-b) for a, b in zip(measurement['size_mm'], expected)),
                         'saved_geometry_max_error_mm': max(abs(a-b) for a, b in zip(size, expected)),
                         'export_svg_size_mm': svg_size(folder/name) if fmt == 'svg' else None,
                         'native_layers': layers, 'screenshot': stem+'.png', 'native_project': stem+'.lbrn2'})
            artifacts.extend([name, stem+'.lbrn2', stem+'.png'])
    assert len(rows) == len(observed['measurements']) == 10
    dxf_rows = []
    for name in [row['name'] for row in preparation['cases']] + ['palette']:
        doc = ezdxf.readfile(folder/(name+'.dxf'))
        audit = doc.audit()
        palette = {n: [doc.layers.get(n).dxf.color, doc.layers.get(n).dxf.true_color] for n in PALETTE}
        dxf_rows.append({'file': name+'.dxf', 'errors': len(audit.errors), 'repairs': len(audit.fixes),
                         'version': doc.dxfversion, 'units': doc.units, 'palette': palette,
                         'entities_bylayer': all(e.dxf.color == 256 for e in doc.modelspace())})
        assert not audit.errors and not audit.fixes
        assert doc.dxfversion == 'AC1021' and doc.units == 4 and dxf_rows[-1]['entities_bylayer']
        assert all(palette[n] == list(v) for n, v in PALETTE.items())
    palette_saves = {}
    for fmt in ['dxf', 'svg']:
        stem = 'palette-'+fmt+'-native'
        layers = native_layers(folder/(stem+'.lbrn2'))
        assert layers['cut_settings'] == {'0': 'Cut', '1': 'Cut', '2': 'Cut', '30': 'Tool'}
        assert layers['shapes_by_cut_index'] == {'0': 2, '1': 1, '2': 1, '30': 1}
        palette_saves[fmt] = layers
        artifacts.extend(['palette.'+fmt, stem+'.lbrn2', stem+'.png'])
    artifacts.extend(['settings-tool-import-enabled.png', 'settings-tool-import-restored.png'])
    result = {'recorded_at': datetime.now(timezone.utc).isoformat(), 'held_out_read': False,
              'H2': False, 'scope': 'Ten native imports, native saved dimensions and export palette only',
              'dependencies': {n: importlib.metadata.version(n) for n in ['ezdxf', 'svgpathtools']},
              'native_oracle': 'unmodified published MIT lbrn2-to-svg@0.5.3',
              'oracle_stdout': oracle_run.stdout, 'oracle_stderr': oracle_run.stderr,
              'oracle_package_sha256': digest(ROOT/'.cache/shop-oracle/node_modules/lbrn2-to-svg/package.json'),
              'scripts_sha256': {n: digest(ROOT/'scripts'/n) for n in ['h2_lightburn_oracle.mjs', 'h2_lightburn_audit.py']},
              'source_sha256': preparation['source_sha256'], 'binary_sha256': preparation['binary_sha256'],
              'manifest_sha256': preparation['manifest_sha256'], 'measurements': rows,
              'dxf_audits': dxf_rows, 'palette_saves': palette_saves,
              'all_sizes_within_g6_0_01_mm': all(r['saved_geometry_max_error_mm'] <= .01 and r['ui_max_error_mm'] <= .01 for r in rows),
              'ui_rounds_to_analytic_size_count': sum(all(f'{a:.3f}' == f'{b:.3f}' for a, b in zip(r['native_ui_mm'], r['expected_mm'])) for r in rows),
              'max_saved_geometry_error_mm': max(r['saved_geometry_max_error_mm'] for r in rows),
              'max_ui_error_mm': max(r['ui_max_error_mm'] for r in rows),
              'artifacts_sha256': {n: digest(folder/n) for n in artifacts}}
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: result[k] for k in ['all_sizes_within_g6_0_01_mm', 'ui_rounds_to_analytic_size_count',
                                            'max_saved_geometry_error_mm', 'max_ui_error_mm']}))


if __name__ == '__main__':
    main()
