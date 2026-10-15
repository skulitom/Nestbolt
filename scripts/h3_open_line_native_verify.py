"""Verify saved native observations of the authored and repaired L17 searches.

The input audit pins training-only provenance. Native saves are compared with
the product using the published MIT reader, without replacing source files.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as E

import psutil

from h3_geometry_audit import compare, normalize, sources, write_json
from h3_native_search_verify import bounds_fields, expected_bounds, settings
from h6_material_cost import run

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audit', type=Path)
    parser.add_argument('native', type=Path)
    args = parser.parse_args()
    psutil.Process().cpu_affinity([8])
    folder, native = args.audit.resolve(), args.native.resolve()
    report = json.loads((folder/'results.json').read_bytes())
    before = sources()
    assert before == report['guards']['product'] and report['source_guards_passed']
    inspection = ROOT/'target/release/examples/lightburn_inspect.exe'
    binary_hash = sha256(inspection.read_bytes()).hexdigest()
    rows, projects = [], []
    for name in ['authored', 'L17']:
        case = next(r for r in report['rows'] if r['case'] == name)
        source = ROOT/case['source']
        assert sha256(source.read_bytes()).hexdigest() == case['source_sha256']
        exports = json.loads((folder/name/'nested/report.json').read_bytes())['files']
        assert len(exports) == 1
        product = folder/name/'nested'/exports[0]
        saved = native/f'{name}-resave.lbrn2'
        directory = native/name
        directory.mkdir(exist_ok=True)
        scenes = {}
        for label, path in [('product', product), ('native', saved)]:
            result = run([inspection, path], directory, label, 8, 30)
            assert result['exit_code'] == 0
            scenes[label] = json.loads((directory/(label+'-stdout.json')).read_bytes())['scene']
        assert len(scenes['product']['shapes']) == len(scenes['native']['shapes'])
        assert all(a['kind'] == b['kind'] for a, b in zip(scenes['product']['shapes'], scenes['native']['shapes'], strict=True))
        xml, indices, omitted, zeros = normalize(saved.read_bytes())
        assert not omitted
        normalized = directory/'normalized.lbrn2'
        normalized.write_text(xml, encoding='utf-8', newline='\n')
        projects.append({'path': name, 'normalized_xml': str(normalized), 'shape_indices': indices,
                         'svg_directory': str(directory/'oracle')})
        original_settings = settings(source)
        product_settings, native_settings = settings(product), settings(saved)
        changed = [list(k) for k, v in original_settings.items() if product_settings.get(k) != v or native_settings.get(k) != v]
        supplied_setting_values_preserved = not changed
        if name == 'authored':
            # This deliberately minimal authored fixture has no native defaults.
            # Record native additions, but require every supplied value unchanged.
            assert set(original_settings) == {('CutSetting', '0')}
            original = E.parse(source).getroot().find('CutSetting')
            actual = next(n for n in E.parse(saved).getroot().findall('CutSetting') if n.find('index').get('Value') == '0')
            canonical = lambda n: E.canonicalize(E.tostring(n, encoding='unicode'), strip_text=True)
            supplied_setting_values_preserved = original.attrib == actual.attrib and all(
                len(actual.findall(n.tag)) == 1 and canonical(n) == canonical(actual.find(n.tag)) for n in original)
        observed = bounds_fields(native/f'{name}-opened.txt')
        expected = expected_bounds(scenes['product'])
        assert observed is not None
        row = {'case': name, 'source_sha256': case['source_sha256'], 'product_sha256': sha256(product.read_bytes()).hexdigest(),
               'native_sha256': sha256(saved.read_bytes()).hexdigest(), 'original_settings_changed': changed,
               'supplied_setting_values_preserved': supplied_setting_values_preserved,
               'native_added_settings': {str(k): v for k, v in native_settings.items() if k not in original_settings},
               'product_open_paths': sum(not p['closed'] for s in scenes['product']['shapes'] for p in s['paths']),
               'native_open_paths': sum(not p['closed'] for s in scenes['native']['shapes'] for p in s['paths']),
               'native_xywh_mm': observed, 'expected_xywh_mm': expected,
               'maximum_ui_difference_mm': max(abs(a-b) for a, b in zip(observed, expected)),
               'all_leaves_compared': indices == [i for i, s in enumerate(scenes['product']['shapes']) if s['kind'] != 'Group']}
        rows.append(row)
    write_json(native/'oracle-request.json', {'projects': projects, 'oracle_report': str(native/'oracle-report.json')})
    result = run(['node', ROOT/'scripts/h3_geometry_oracle.mjs', native/'oracle-request.json'], native, 'oracle', 8, 120)
    assert result['exit_code'] == 0
    assert all('error' not in r for r in json.loads((native/'oracle-report.json').read_bytes())['reports'])
    for row, project in zip(rows, projects, strict=True):
        scene = json.loads((native/row['case']/'product-stdout.json').read_bytes())['scene']
        row['geometry'] = [{'shape': i, **compare(scene['shapes'][i], Path(project['svg_directory'])/f'{i}.svg')}
                           for i in project['shape_indices']]
        row['passed'] = (row['supplied_setting_values_preserved'] and row['product_open_paths'] == row['native_open_paths']
                         and row['maximum_ui_difference_mm'] <= .01 and row['all_leaves_compared']
                         and all(g['passed'] for g in row['geometry']))
    assert sources() == before and sha256(inspection.read_bytes()).hexdigest() == binary_hash
    write_json(native/'verification.json', {'scope': __doc__, 'H3': False, 'held_out_geometry_read': False,
        'source_sha256': before, 'binary_sha256': binary_hash, 'verifier_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_guards_passed': True, 'passed': all(r['passed'] for r in rows), 'rows': rows})
    print(json.dumps({r['case']: {'passed': r['passed'], 'leaves': len(r['geometry']), 'native_open_paths': r['native_open_paths']}
                      for r in rows}, indent=2))
    assert all(r['passed'] for r in rows)


if __name__ == '__main__':
    main()
