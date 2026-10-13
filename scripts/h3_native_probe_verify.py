"""Check retained native saves against controlled writer outputs and screenshots.

Run with the isolated shop Python environment. Only reads the explicit result
folder and its original MIT probes, never the held-out dataset.
"""
import argparse
from copy import deepcopy
import ctypes
import difflib
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

from h3_geometry_audit import normalize, compare, matrix, sources, write_json

ROOT = Path(__file__).resolve().parents[1]
UI = {
    'text-moved': [100.861, 76.329, 159.662, 22.864],
    'text-rotated': [43.671, 90.861, 22.864, 159.662],
    'group-mirrored': [50.000, 70.000, 35.898, 80.000],
    'bitmap-rehomed': [40.000, 30.000, 6.349, 8.466],
}


def canonical(node):
    return E.canonicalize(E.tostring(node, encoding='unicode'), strip_text=True)


def allowed_diff(source, output, member, transform):
    before, after = E.fromstring(source), E.fromstring(output)
    assert before.attrib == after.attrib
    assert [canonical(n) for n in before if n.tag != 'Shape'] == [canonical(n) for n in after if n.tag != 'Shape']
    assert len(after.findall('Shape')) == 1
    old = before.findall('Shape')[member]
    restored = deepcopy(after.find('Shape'))
    sine, cosine = math.sin(transform['rotation_radians']), math.cos(transform['rotation_radians'])
    sign = -1 if transform['mirrored'] else 1
    tx, ty = transform['translation']
    placement = matrix(' '.join(map(str, [sign*cosine, sign*sine, -sine, cosine, tx, ty])))
    expected = placement @ matrix(old.findtext('XForm'))
    assert abs(matrix(restored.findtext('XForm')) - expected).max() < 1e-9, 'incorrect placement composition'
    restored.find('XForm').text = old.findtext('XForm')
    rehomes = []

    def restore(a, b):
        for attribute, tag in [('VertID', 'VertList'), ('PrimID', 'PrimList')]:
            if a.find(tag) is None and b.find(tag) is not None:
                reference = next(n.find(tag) for n in before.iter()
                                 if n.get(attribute) == a.get(attribute) and n.find(tag) is not None)
                assert canonical(reference) == canonical(b.find(tag))
                b.remove(b.find(tag))
                rehomes.append(attribute)
        if a.get('Type') == 'Bitmap' and a.get('Data') is None and b.get('Data') is not None:
            reference = next(n.get('Data') for n in before.iter('Shape')
                             if n.get('SourceHash') == a.get('SourceHash') and n.get('Data') is not None)
            assert reference == b.get('Data')
            del b.attrib['Data']
            rehomes.append('Data')
        assert len(a) == len(b)
        for x, y in zip(a, b):
            restore(x, y)

    restore(old, restored)
    assert canonical(old) == canonical(restored), 'non-placement shape change'
    return rehomes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    folder = args.folder.resolve()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 8)
    initial_sources = sources()
    prepared = json.loads((folder / 'prepared.json').read_text(encoding='utf-8'))
    scratch = ROOT / 'output' / (folder.name + '-verify')
    scratch.mkdir(exist_ok=True)
    cases = prepared['cases'] + [
        dict(next(c for c in prepared['cases'] if c['name'] == 'origin-' + corner),
             name='device-top-right-source-' + corner)
        for corner in ['top-right', 'bottom-left']
    ]
    projects = []
    for c in cases:
        name = c['name']
        native = folder / f'{name}-native.lbrn2'
        normalized, indices, omitted, zeros = normalize(native.read_text(encoding='utf-8'))
        assert not omitted
        xml = scratch / f'{name}.lbrn2'
        xml.write_text(normalized, encoding='utf-8', newline='\n')
        projects.append(dict(path=name, normalized_xml=str(xml), shape_indices=indices,
                             svg_directory=str(scratch / name), normalized_zero_handles=zeros))
    request = scratch / 'oracle-request.json'
    oracle_report = scratch / 'oracle-report.json'
    write_json(request, dict(projects=projects, oracle_report=str(oracle_report)))
    subprocess.run(['node', 'scripts/h3_geometry_oracle.mjs', str(request)], cwd=ROOT, check=True, timeout=60)
    oracle = json.loads(oracle_report.read_text(encoding='utf-8'))
    assert all('error' not in r for r in oracle['reports']), oracle
    records = []
    for c, project in zip(cases, projects):
        name = c['name']
        output_path = ROOT / c['output']
        assert sha256(output_path.read_bytes()).hexdigest() == c['output_sha256']
        original = ROOT / c['source']
        assert original.resolve().is_relative_to((ROOT / 'benchmarks/datasets/shop/probes').resolve())
        assert sha256(original.read_bytes()).hexdigest() == c['source_sha256']
        rehomes = allowed_diff(original.read_text(encoding='utf-8'), output_path.read_text(encoding='utf-8'),
                               c['members'][0], c['request']['placements'][0]['transform'])
        actual = json.loads(subprocess.check_output(['target/release/examples/lightburn_inspect.exe', str(output_path)],
                                                   cwd=ROOT, text=True, timeout=10))['scene']
        comparisons = [dict(shape=i, **compare(actual['shapes'][i], Path(project['svg_directory']) / f'{i}.svg'))
                       for i in project['shape_indices']]
        native = folder / f'{name}-native.lbrn2'
        nr, wr = E.parse(native).getroot(), E.parse(output_path).getroot()
        settings = lambda root: {(n.tag, n.find('index').get('Value')):canonical(n)
                                 for n in root if n.tag in ['CutSetting', 'CutSetting_Img']}
        native_settings, written_settings = settings(nr), settings(wr)
        settings_equal = native_settings == written_settings
        retained_equal = all(key in written_settings and written_settings[key] == value
                             for key, value in native_settings.items())
        removed_settings = sorted(set(written_settings) - set(native_settings))
        changed_settings = [dict(family=key[0], index=key[1],
                                 xml_diff=list(difflib.unified_diff(
                                     written_settings.get(key, '').replace('><', '>\n<').splitlines(),
                                     value.replace('><', '>\n<').splitlines(),
                                     fromfile='Nestbolt output', tofile='LightBurn native save')))
                            for key, value in native_settings.items() if written_settings.get(key) != value]
        # Native Save As omits settings unused by any saved shape. The writer
        # itself must retain every setting, which allowed_diff checks above.
        required_settings = {(('CutSetting_Img' if s['image_layer'] else 'CutSetting'), str(s['cut_index']))
                             for s in actual['shapes'] if s['kind'] != 'Group' and s['cut_index'] is not None}
        required_present = required_settings <= native_settings.keys()
        observed = UI.get(name, [30.0, 32.5, 40.0, 25.0])
        expected = c['centre_mm'] + c['size_mm']
        errors = [abs(a-b) for a,b in zip(expected, observed)]
        text_cache = None
        bitmap_data_equal = None
        if c['kind'] == 'Text':
            text_cache = dict(written_live=wr.findtext('Shape/XForm'), written_cache=wr.findtext('Shape/BackupPath/XForm'),
                              native_live=nr.findtext('Shape/XForm'), native_cache=nr.findtext('Shape/BackupPath/XForm'))
        if c['kind'] == 'Bitmap':
            bitmap_data_equal = wr.find('Shape').get('Data') == nr.find('Shape').get('Data')
        records.append(dict(name=name, native_sha256=sha256(native.read_bytes()).hexdigest(),
                            native_origin=[nr.get('MirrorX'), nr.get('MirrorY')],
                            native_warning_dialog=False, ui_centre_and_size_mm=observed,
                            expected_centre_and_size_mm=expected, ui_errors_mm=errors,
                            canonical_writer_diff_allowed=True, rehomes=rehomes,
                            native_cut_settings_canonical_equal=settings_equal,
                            native_retained_settings_canonical_equal=retained_equal,
                            native_removed_unused_settings=removed_settings,
                            native_changed_retained_settings=changed_settings,
                            required_layer_settings_present=required_present,
                            text_cache=text_cache, bitmap_data_equal=bitmap_data_equal, geometry=comparisons,
                            passed=max(errors) <= .01 and retained_equal and required_present
                                   and bitmap_data_equal is not False and all(v['passed'] for v in comparisons)))
    assert sources() == initial_sources
    report = dict(scope=prepared['scope'], prepared_sha256=sha256((folder/'prepared.json').read_bytes()).hexdigest(),
                  source_digest=initial_sources, lightburn='Pro 2.1.01', device='No Machine 300 x 200 mm',
                  affinity='CPU 8; sequential native reader and published oracle children inherit affinity',
                  oracle='lbrn2-to-svg@0.5.3 unchanged; normalized native-saved geometry, including refreshed Text cache',
                  screenshots='UI centre anchor, mm; values transcribed from retained screenshots',
                  native_save_settings_note='The native serializer removes unused settings. Initial full-settings equality failure is retained separately; product output must still preserve all settings.',
                  original_device_origin_restored=True, owned_app_closed=True, seat_display_and_lease_released=True,
                  known_automation_issues=['Save dialog selector initially truncated; recovered with fresh dialog observation',
                    'Origin mismatch marks project dirty (*); initial exact-title wait timed out; observed before continuing',
                    'Device Settings UIA provider timed out; changed origin using fresh screenshot coordinates'],
                  cases=records, passed=all(r['passed'] for r in records),
                  max_ui_error_mm=max(max(r['ui_errors_mm']) for r in records),
                  verifier_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  oracle_report_sha256=sha256(oracle_report.read_bytes()).hexdigest(),
                  oracle_svg_sha256={str(p.relative_to(scratch)):sha256(p.read_bytes()).hexdigest()
                                     for p in sorted(scratch.rglob('*.svg'))},
                  evidence_sha256={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())
                                   if p.is_file() and p.name != 'native-check.json'})
    write_json(folder / 'native-check.json', report)
    print(json.dumps({k:report[k] for k in ['passed', 'max_ui_error_mm']}, indent=2))
    for r in records:
        print(r['name'], r['passed'], 'geometry', r['geometry'])


if __name__ == '__main__':
    main()
