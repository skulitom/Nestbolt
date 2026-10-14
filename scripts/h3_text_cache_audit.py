"""Check uncached training text and the existing native cache repair evidence.

Native references are auxiliary repaired inputs, never replacements for frozen
sources or labels. Filter by training source before reading either document.
"""
from collections import Counter
import ctypes
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as E

from h3_geometry_audit import normalize, compare, sources, write_json

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def settings(root):
    return {(n.tag, n.find('index').get('Value')):E.canonicalize(E.tostring(n, encoding='unicode'), strip_text=True)
            for n in root if n.tag in ['CutSetting', 'CutSetting_Img']}


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 8)
    digest = sources()
    raw = (CORPUS/'manifest.json').read_bytes()
    manifest = json.loads(raw)
    training = {r['path']:r for r in manifest['files'] if r['split'] == 'training'}
    inventory = {r['path']:r['sha256'] for r in manifest['corpus_inventory']}
    refs = json.loads((CORPUS/'references/public/manifest.json').read_text(encoding='utf-8'))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT/'output'/f'h3-text-cache-{stamp}'
    work.mkdir(exist_ok=False)
    binary = ROOT/'target/release/examples/lightburn_inspect.exe'
    binary_hash = sha256(binary.read_bytes()).hexdigest()
    projects, rows = [], []
    for ref in refs['rows']:
        if ref['source'] not in training:
            continue
        source = CORPUS/ref['source']
        original_bytes = source.read_bytes()
        assert sha256(original_bytes).hexdigest() == training[ref['source']]['sha256'] == ref['source_sha256']
        original = E.fromstring(original_bytes)
        missing = [s for s in original.iter('Shape') if s.get('Type') == 'Text' and s.find('BackupPath') is None]
        if not missing:
            continue
        native_relative = f"references/public/{ref['id']}.lbrn2"
        native = CORPUS/native_relative
        native_bytes = native.read_bytes()
        assert sha256(native_bytes).hexdigest() == inventory[native_relative] == ref['native_project_sha256']
        repaired = E.fromstring(native_bytes)
        native_text = [s for s in repaired.iter('Shape') if s.get('Type') == 'Text']
        original_text = [s for s in original.iter('Shape') if s.get('Type') == 'Text']
        def inspect(path, label):
            result = subprocess.run([str(binary), str(path)], cwd=ROOT, capture_output=True, check=True, timeout=10)
            (work/f"{ref['id']}-{label}.json").write_bytes(result.stdout)
            return json.loads(result.stdout)
        original_result = inspect(source, 'original')
        native_result = inspect(native, 'native')
        before, after = settings(original), settings(repaired)
        row = dict(id=ref['id'], source=ref['source'], source_sha256=ref['source_sha256'],
            native_reference=native_relative, native_reference_sha256=ref['native_project_sha256'],
            licence=ref['licence'], split='training', missing_original_caches=len(missing),
            fonts=dict(Counter(s.get('Font') for s in missing)),
            native_text_count=len(native_text), native_cached_text_count=sum(s.find('BackupPath') is not None for s in native_text),
            text_strings_preserved=[s.get('Str') for s in original_text] == [s.get('Str') for s in native_text],
            original_incomplete=[i for i,s in enumerate(original_result['scene']['shapes']) if not s['geometry_complete']],
            native_incomplete=[i for i,s in enumerate(native_result['scene']['shapes']) if not s['geometry_complete']],
            original_warnings=original_result['scene']['warnings'],
            native_changed_settings=[list(k) for k in sorted(set(before)|set(after)) if before.get(k) != after.get(k)],
            native_shape_count=len(native_result['scene']['shapes']))
        xml, indices, omitted, zeros = normalize(native_bytes)
        assert not omitted
        normalized = work/f"{ref['id']}-normalized.lbrn2"
        normalized.write_text(xml, encoding='utf-8', newline='\n')
        projects.append(dict(path=ref['id'], normalized_xml=str(normalized), shape_indices=indices,
                             svg_directory=str(work/ref['id']), normalized_zero_handles=zeros))
        rows.append(row)
    assert len(rows) == 8 and sum(r['missing_original_caches'] for r in rows) == 122
    write_json(work/'request.json', dict(projects=projects, oracle_report=str(work/'oracle.json')))
    subprocess.run(['node', 'scripts/h3_geometry_oracle.mjs', str(work/'request.json')], cwd=ROOT, check=True, timeout=120)
    oracle = json.loads((work/'oracle.json').read_text(encoding='utf-8'))
    assert all('error' not in r for r in oracle['reports'])
    for row, project in zip(rows, projects):
        scene = json.loads((work/f"{row['id']}-native.json").read_text(encoding='utf-8'))['scene']
        row['geometry'] = [dict(shape=i, kind=scene['shapes'][i]['kind'], **compare(scene['shapes'][i], Path(project['svg_directory'])/f'{i}.svg')) for i in project['shape_indices']]
        row['all_leaves_compared'] = project['shape_indices'] == [i for i,s in enumerate(scene['shapes']) if s['kind'] != 'Group']
        row['repaired_geometry_passes'] = not row['native_incomplete'] and row['all_leaves_compared'] and all(r['passed'] for r in row['geometry'])
    assert digest == sources() and binary_hash == sha256(binary.read_bytes()).hexdigest()
    report = dict(date=stamp, scope='Training-only missing-text-cache diagnosis and native repair evidence; not H3 acceptance',
        H3=False, held_out_read=False, original_input_gate_pass=False,
        source_digest=digest, binary_sha256=binary_hash, runner_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        manifest_sha256=sha256(raw).hexdigest(), native_reference_manifest_sha256=sha256((CORPUS/'references/public/manifest.json').read_bytes()).hexdigest(),
        source_documentation='https://docs.lightburnsoftware.com/legacy/UI/FontsAndText',
        oracle='Published MIT lbrn2-to-svg@0.5.3 with documented test-only normalization; 64 samples per contour; limit 0.01 mm',
        repaired_geometry_passes=all(r['repaired_geometry_passes'] for r in rows), rows=rows)
    target = ROOT/'benchmarks/results'/f'h3-text-cache-{stamp}.json'
    write_json(target, report)
    print(json.dumps(dict(report=str(target), originals=8, missing_caches=122,
        repaired_geometry_passes=report['repaired_geometry_passes'],
        leaves=sum(len(r['geometry']) for r in rows),
        text_leaves=sum(sum(g['kind']=='Text' for g in r['geometry']) for r in rows),
        changed_settings_projects=[r['id'] for r in rows if r['native_changed_settings']]), indent=2))
    assert report['repaired_geometry_passes']


if __name__ == '__main__':
    main()
