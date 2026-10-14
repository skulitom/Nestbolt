"""Prepare and verify a native-authored legacy-format conversion diagnostic.

Run in the isolated shop Python environment. This uses only the explicitly
named, original MIT probe folder; it never enumerates or opens corpus inputs.
Native observations and saves are made separately in the hidden Anode desktop.
"""
import argparse
from copy import deepcopy
import ctypes
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as E

from h3_geometry_audit import normalize, compare, sources, write_json

ROOT = Path(__file__).resolve().parents[1]


def canonical(node):
    return E.canonicalize(E.tostring(node, encoding='unicode'), strip_text=True)


def run(args, folder, name):
    result = subprocess.run(list(map(str, args)), cwd=ROOT, capture_output=True, timeout=90)
    (folder/f'{name}.stdout.txt').write_bytes(result.stdout)
    (folder/f'{name}.stderr.txt').write_bytes(result.stderr)
    assert result.returncode == 0, result.stderr.decode('utf-8', errors='replace')
    return result.stdout.decode('utf-8')


def prepare(folder):
    folder.mkdir(exist_ok=False)
    probe = ROOT/'output/h3-legacy-probe'
    for name in ['features-legacy.lbrn', 'baseline-native.lbrn2', 'baseline.png',
                 'flag-only.lbrn2', 'flag-only.png', 'with-both-lists.lbrn2',
                 'with-both-lists.png', 'both-native.lbrn2']:
        shutil.copyfile(probe/name, folder/name)
    source = folder/'features-legacy.lbrn'
    assembly = json.loads(run(['target/release/examples/lightburn_roundtrip.exe', source], folder, 'assembly'))
    assert assembly['status'] == 'written'
    assert assembly['validation']['valid']
    write_json(folder/'identity.request.json', dict(width_mm=300, height_mm=200, outline=False,
        placements=[dict(unit=u['id'], transform=dict(translation=[0, 0], rotation_radians=0, mirrored=False))
                    for u in assembly['nesting']['units']]))
    output = run(['target/release/examples/lightburn_place.exe', source, folder/'identity.request.json'], folder, 'identity')
    (folder/'identity.lbrn2').write_text(output, encoding='utf-8', newline='\n')
    write_json(folder/'search.request.json', dict(sheets=[dict(width_mm=300, height_mm=200)], spacing_mm=1, edge_spacing_mm=1))
    command = ['target/release/nestbolt.exe', 'nest', '--library', str(source), '--request', str(folder/'search.request.json'),
               '--out-dir', str(folder/'searched'), '--seconds', '1', '--repeatable', '--time-limit', '60']
    run(command, folder, 'search')
    report = json.loads((folder/'searched/report.json').read_text(encoding='utf-8'))
    assert report['validation']['valid']
    assert len(report['files']) == 1
    (folder/'searched.lbrn2').write_bytes((folder/'searched'/report['files'][0]).read_bytes())
    write_json(folder/'prepared.json', dict(scope='Authored legacy conversion diagnostic; not H3 acceptance',
        licence='MIT; original Nestbolt geometry.svg, checker.png and feature probe; native Save As .lbrn in LightBurn Pro 2.1.01',
        source_sha256=sha256(source.read_bytes()).hexdigest(), source_digest=sources(),
        binaries={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in [
            ROOT/'target/release/nestbolt.exe', ROOT/'target/release/examples/lightburn_place.exe',
            ROOT/'target/release/examples/lightburn_inspect.exe', ROOT/'target/release/examples/lightburn_roundtrip.exe']},
        units=len(assembly['nesting']['units']), search_command=command,
        affinity='CPU 8; sequential subprocesses inherit affinity',
        runner_sha256=sha256(Path(__file__).read_bytes()).hexdigest()))
    print(folder)


def verify(folder):
    prepared = json.loads((folder/'prepared.json').read_text(encoding='utf-8'))
    assert prepared['source_sha256'] == sha256((folder/'features-legacy.lbrn').read_bytes()).hexdigest()
    before = E.parse(folder/'features-legacy.lbrn').getroot()
    after = E.parse(folder/'identity.lbrn2').getroot()
    restored = deepcopy(after)
    restored.set('FormatVersion', '0')
    for node in restored.iter():
        for item in list(node):
            if item.tag in ['VertList', 'PrimList']:
                node.remove(item)
    assert canonical(before) == canonical(restored), 'identity conversion changed original metadata or V/P'
    baseline = E.parse(folder/'baseline-native.lbrn2').getroot()
    native = E.parse(folder/'identity-native.lbrn2').getroot()
    # Native saves from both original legacy and our modern output must converge
    # to the same entire project, including sharing, text caches and settings.
    assert canonical(baseline) == canonical(native), 'native identity save differs from legacy baseline'
    settings = lambda root: [canonical(n) for n in root if n.tag in ['CutSetting', 'CutSetting_Img']]
    assert settings(before) == settings(after) == settings(baseline) == settings(native)
    scratch = ROOT/'output'/f'{folder.name}-oracle'
    scratch.mkdir(exist_ok=True)
    cases = [('identity', 'baseline-native'), ('identity', 'identity-native'), ('searched-fixed', 'searched-fixed-native')]
    projects = []
    for product, reference in cases:
        xml, indices, omitted, zeros = normalize((folder/f'{reference}.lbrn2').read_text(encoding='utf-8'))
        assert not omitted
        path = scratch/f'{reference}.lbrn2'
        path.write_text(xml, encoding='utf-8', newline='\n')
        projects.append(dict(path=reference, product=product, normalized_xml=str(path), shape_indices=indices,
                             svg_directory=str(scratch/reference), normalized_zero_handles=zeros))
    write_json(scratch/'request.json', dict(projects=projects, oracle_report=str(scratch/'report.json')))
    subprocess.run(['node', 'scripts/h3_geometry_oracle.mjs', str(scratch/'request.json')], cwd=ROOT, check=True, timeout=60)
    oracle = json.loads((scratch/'report.json').read_text(encoding='utf-8'))
    assert all('error' not in r for r in oracle['reports']), oracle
    results = []
    for project in projects:
        product, reference = project['product'], project['path']
        scene = json.loads(run(['target/release/examples/lightburn_inspect.exe', folder/f'{product}.lbrn2'], folder, f'inspect-{reference}'))['scene']
        checks = [dict(shape=i, **compare(scene['shapes'][i], Path(project['svg_directory'])/f'{i}.svg')) for i in project['shape_indices']]
        expected_indices = [i for i, shape in enumerate(scene['shapes']) if shape['kind'] != 'Group']
        counts_equal = expected_indices == project['shape_indices']
        a, b = E.parse(folder/f'{product}.lbrn2').getroot(), E.parse(folder/f'{reference}.lbrn2').getroot()
        equal = settings(a) == settings(b)
        keyed = lambda root: {(n.tag,n.find('index').get('Value')):canonical(n) for n in root if n.tag in ['CutSetting', 'CutSetting_Img']}
        original, written, saved = keyed(before), keyed(a), keyed(b)
        original_equal = all(written.get(key) == saved.get(key) == value for key,value in original.items())
        additions = set(written) - set(original)
        added_equal = set(saved) == set(written)
        if additions:
            # This authored source has four settings (priorities 0..3), no T1.
            # Native normalizes only the newly generated Tool name and priority;
            # every original setting still needs exact canonical equality.
            expected = E.fromstring('<CutSetting type="Tool"><index Value="30"/><name Value="T1"/><priority Value="4"/></CutSetting>')
            added_equal &= additions == {('CutSetting','30')} and saved.get(('CutSetting','30')) == canonical(expected)
        results.append(dict(product=product, native_reference=reference, geometry=checks, native_settings_equal=equal,
                            native_original_settings_equal=original_equal, new_tool_native_defaults_equal=added_equal,
                            all_leaves_present=counts_equal, expected_leaves=len(expected_indices), native_leaves=len(project['shape_indices']),
                            passed=original_equal and added_equal and counts_equal and all(c['passed'] for c in checks)))
    observations = json.loads((folder/'observations.json').read_text(encoding='utf-8'))
    report = dict(scope='Authored legacy conversion diagnostic; not H3 acceptance', source_digest=sources(),
        identity_preserves_original_elements=True, native_identity_entire_project_equal=True,
        retained_vp_are_not_duplicate_cuts=True,
        settings_note='All four original settings are canonically unchanged. The new T1 setting normalizes name SHEET to T1 and adds priority 4 in native Save As; strict all-settings failure retained in native-check-new-tool-defaults.json.',
        observations=observations, cases=results, passed=all(r['passed'] for r in results),
        oracle=oracle, oracle_svg_sha256={str(p.relative_to(scratch)):sha256(p.read_bytes()).hexdigest() for p in sorted(scratch.rglob('*.svg'))},
        verifier_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    write_json(folder/'native-check.json', report)
    print(json.dumps({'passed':report['passed'], 'cases':len(results),
                      'leaves':sum(len(r['geometry']) for r in results),
                      'max_point_mm':max(c['product_to_oracle_mm'] for r in results for c in r['geometry']),
                      'max_bounds_mm':max(c['bbox_difference_mm'] for r in results for c in r['geometry'])}, indent=2))
    assert report['passed']


def refresh(folder):
    command = ['target/release/nestbolt.exe', 'export', '--library', str(folder/'features-legacy.lbrn'),
               '--request', str(folder/'search.request.json'), '--layout', str(folder/'searched/layout.json'),
               '--out-dir', str(folder/'corrected')]
    run(command, folder, 'refresh')
    (folder/'searched-fixed.lbrn2').write_bytes((folder/'corrected/features-legacy-sheet-1.lbrn2').read_bytes())
    write_json(folder/'refreshed.json', dict(source_digest=sources(), command=command,
        binary_sha256=sha256((ROOT/'target/release/nestbolt.exe').read_bytes()).hexdigest(),
        note='Re-export the identical validated search layout after correcting T1 root element order; initial files and failure retained.'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'refresh', 'verify'])
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 8)
    digest = sources()
    {'prepare':prepare, 'refresh':refresh, 'verify':verify}[args.action](args.folder.resolve())
    assert digest == sources(), 'Sources changed during diagnostic'


if __name__ == '__main__':
    main()
