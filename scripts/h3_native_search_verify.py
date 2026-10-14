"""Verify the five training/authored H3 native searches and saved UI evidence.

Run in the isolated shop environment. Native saves are independent observations;
the published MIT reader supplies geometry after the documented normalization.
No held-out source, geometry or label is opened.
"""
import argparse
import ctypes
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as E

from h3_geometry_audit import normalize, compare, sources, write_json

ROOT = Path(__file__).resolve().parents[1]


def controls(path):
    text = path.read_text(encoding='utf-8')
    assert 'Tree truncated' not in text, f'Incomplete native settings observation: {path}'
    found = {}
    pattern = r'\[e\d+\] (Edit|Spinner|ComboBox|CheckBox|RadioButton) [^\n]*#(MainWindow\.CutSettingEdit\.[^ @\r\n]+)([^\n]*)(?:\n    text: ([^\n]*))?'
    for role, name, state, value in re.findall(pattern, text):
        found[name] = dict(role=role, enabled='disabled' not in state,
                           value=value.strip(), toggle=(re.search(r'toggle: (On|Off)', state) or [None, None])[1])
    assert found, path
    return found


def bounds_fields(path):
    text = path.read_text(encoding='utf-8')
    pattern = r'#MainWindow\.tbNumericEdits\.QXYControl\.sb([XY]) @(\d+),[^\n]*\n    text: ([^\n]+)'
    fields = {(int(x), axis):float(value.replace(',', '')) for axis, x, value in re.findall(pattern, text)}
    columns = sorted({x for x, axis in fields})
    if len(columns) < 2 or any((x, axis) not in fields for x in columns[:2] for axis in ['X', 'Y']):
        return None
    return [fields[(columns[0], 'X')], fields[(columns[0], 'Y')],
            fields[(columns[1], 'X')], fields[(columns[1], 'Y')]]


def expected_bounds(scene, indices=None):
    bounds = [scene['shapes'][i]['bounds_mm'] for i in (scene['top_level'] if indices is None else indices)]
    bounds = [b for b in bounds if b is not None]
    x0, y0 = min(b[0] for b in bounds), min(b[1] for b in bounds)
    x1, y1 = max(b[2] for b in bounds), max(b[3] for b in bounds)
    return [(x0+x1)/2, (y0+y1)/2, x1-x0, y1-y0]


def settings(path):
    root = E.parse(path).getroot()
    return {(n.tag, n.find('index').get('Value')):E.canonicalize(E.tostring(n, encoding='unicode'), strip_text=True)
            for n in root if n.tag in ['CutSetting', 'CutSetting_Img']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--partial', action='store_true', help='Record incomplete observations without claiming the five-project gate')
    args = parser.parse_args()
    folder = args.folder.resolve()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 8)
    digest = sources()
    prepared = json.loads((folder/'prepared.json').read_text(encoding='utf-8'))
    observations = json.loads((folder/'ui-observations.json').read_text(encoding='utf-8'))
    manifest = (ROOT/'benchmarks/datasets/shop/manifest.json').read_bytes()
    assert sha256(manifest).hexdigest() == prepared['manifest_sha256']
    training = {r['path']:r for r in json.loads(manifest)['files'] if r['split'] == 'training'}
    scratch = ROOT/'output'/f'{folder.name}-oracle'
    scratch.mkdir(exist_ok=True)
    projects, records = [], []
    for case in prepared['cases']:
        name = case['name']
        source = ROOT/case['source']
        if case['provenance']['split'] == 'training':
            relative = str(source.relative_to(ROOT/'benchmarks/datasets/shop')).replace('\\', '/')
            assert relative in training
        else:
            assert name == 'mirrored-origin' and source.name == 'origin-top-right.lbrn2'
        assert sha256(source.read_bytes()).hexdigest() == case['provenance']['sha256']
        assert case['exit_code'] == 0 and case['validation']['valid']
        assert case['canonical_diff'] and all(r['canonical_diff_allowed'] for r in case['canonical_diff'])
        directory = folder/name
        if args.partial and not all((directory/phase/'native-resave.lbrn2').exists() for phase in ['before', 'after']):
            records.append(dict(name=name, pending=True, passed=False))
            continue
        record = dict(name=name, pending=False, dialogs=[], geometry=[], bounds=[], units=[])
        before_pages = sorted((directory/'before').glob('*.txt'))
        for page in before_pages:
            if page.name == 'all-bounds.txt':
                continue
            a, b = controls(page), controls(directory/'after'/page.name)
            differences = {k:dict(before=a.get(k), after=b.get(k)) for k in sorted(set(a)|set(b)) if a.get(k) != b.get(k)}
            record['dialogs'].append(dict(page=page.name, controls=len(a), differences=differences, passed=not differences))
        assert record['dialogs'], name
        product = directory/'nested'/case['files'][0]
        original = settings(source)
        written = settings(product)
        native_before = settings(directory/'before/native-resave.lbrn2')
        native_after = settings(directory/'after/native-resave.lbrn2')
        record['original_settings_equal'] = all(written.get(k) == native_before.get(k) == native_after.get(k) == v for k, v in original.items())
        record['additional_settings'] = [list(k) for k in set(written)-set(original)]
        record['native_setting_keys_equal'] = set(native_before) == set(original) and set(native_after) == set(written)
        record['new_tool_defaults_equal'] = True
        if record['additional_settings']:
            expected_tool = '<CutSetting type="Tool"><index Value="30"></index><name Value="T1"></name><priority Value="3"></priority></CutSetting>'
            record['new_tool_defaults_equal'] = name == 'mirrored-origin' and record['additional_settings'] == [['CutSetting', '30']] and native_after.get(('CutSetting', '30')) == expected_tool
        for phase, input_file in [('before', source), ('after', product)]:
            native = directory/phase/'native-resave.lbrn2'
            result = subprocess.run(['target/release/examples/lightburn_inspect.exe', str(input_file)], cwd=ROOT, capture_output=True, check=True, timeout=60)
            (directory/phase/'product-scene.json').write_bytes(result.stdout)
            scene = json.loads(result.stdout)['scene']
            observed = observations['all_bounds_xywh_mm'][name][phase]
            accessible = bounds_fields(directory/phase/'all-bounds.txt')
            assert accessible is None or accessible == observed, (name, phase, accessible, observed)
            expected = expected_bounds(scene)
            difference = max(abs(a-b) for a,b in zip(observed, expected))
            record['bounds'].append(dict(phase=phase, native_xywh_mm=observed, expected_xywh_mm=expected, difference_mm=difference, passed=difference <= .01))
            if phase == 'after':
                selection_to_unit = observations.get('selection_to_unit', {}).get(name, {str(u['id']):u['id'] for u in case['units']})
                assert sorted(selection_to_unit.values()) == sorted(u['id'] for u in case['units'])
                assert set(selection_to_unit) == set(observations['units_xywh_mm'][name])
                for unit in case['units']:
                    selection = next(k for k,v in selection_to_unit.items() if v == unit['id'])
                    # Membership indexes address the top-level array; shapes
                    # inside each group use the separate flat scene indexes.
                    expected_unit = expected_bounds(scene, [scene['top_level'][i] for i in unit['members']])
                    observed_unit = observations['units_xywh_mm'][name][selection]
                    image = directory/'after'/f'unit-{selection}.png'
                    assert image.is_file()
                    delta = max(abs(a-b) for a,b in zip(observed_unit, expected_unit))
                    record['units'].append(dict(unit=unit['id'], selection=selection, native_xywh_mm=observed_unit,
                        expected_xywh_mm=expected_unit, screenshot=str(image.relative_to(folder)),
                        screenshot_sha256=sha256(image.read_bytes()).hexdigest(), difference_mm=delta, passed=delta <= .01))
            xml, indices, omitted, zeros = normalize(native.read_text(encoding='utf-8'))
            assert not omitted, omitted
            normalized = scratch/f'{name}-{phase}.lbrn2'
            normalized.write_text(xml, encoding='utf-8', newline='\n')
            projects.append(dict(path=f'{name}/{phase}', name=name, phase=phase, normalized_xml=str(normalized),
                svg_directory=str(scratch/f'{name}-{phase}'), shape_indices=indices, normalized_zero_handles=zeros,
                scene_file=str(directory/phase/'product-scene.json')))
        records.append(record)
    write_json(scratch/'request.json', dict(projects=projects, oracle_report=str(scratch/'report.json')))
    subprocess.run(['node', 'scripts/h3_geometry_oracle.mjs', str(scratch/'request.json')], cwd=ROOT, check=True, timeout=120)
    oracle = json.loads((scratch/'report.json').read_text(encoding='utf-8'))
    assert all('error' not in r for r in oracle['reports']), oracle
    for project in projects:
        scene = json.loads(Path(project['scene_file']).read_text(encoding='utf-8'))['scene']
        checks = [dict(shape=i, **compare(scene['shapes'][i], Path(project['svg_directory'])/f'{i}.svg')) for i in project['shape_indices']]
        all_leaves = project['shape_indices'] == [i for i,s in enumerate(scene['shapes']) if s['kind'] != 'Group']
        record = next(r for r in records if r['name'] == project['name'])
        record['geometry'].append(dict(phase=project['phase'], all_leaves_present=all_leaves, checks=checks,
                                       passed=all_leaves and all(c['passed'] for c in checks)))
    for record in records:
        if not record['pending']:
            record['passed'] = all(record[k] for k in ['original_settings_equal', 'native_setting_keys_equal', 'new_tool_defaults_equal']) and all(r['passed'] for key in ['dialogs', 'geometry', 'bounds', 'units'] for r in record[key])
    assert digest == sources(), 'Source files changed during verification'
    report = dict(scope='Five training/authored actual searches and native observations; not full H3 acceptance',
        H3=False, held_out_read=False, manifest_sha256=prepared['manifest_sha256'], source_digest=digest,
        binaries={name:sha256((ROOT/name).read_bytes()).hexdigest() for name in ['target/release/nestbolt.exe', 'target/release/examples/lightburn_inspect.exe']},
        oracle='Published MIT lbrn2-to-svg@0.5.3; documented test-only normalization; 64 samples per contour, 0.01 mm limit',
        cases=records, passed=all(r['passed'] for r in records),
        oracle_report=oracle, verifier_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    write_json(folder/('native-check-partial.json' if args.partial else 'native-check.json'), report)
    print(json.dumps({r['name']:dict(passed=r['passed'], pending=r['pending']) for r in records}, indent=2))
    if not args.partial:
        assert report['passed']


if __name__ == '__main__':
    main()
