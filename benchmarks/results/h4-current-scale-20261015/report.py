"""Package completed scale evidence without repeating a measurement."""
import argparse
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from h4_scale import guards

def digest(data):
    return sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')

parser = argparse.ArgumentParser()
parser.add_argument('--curves', required=True)
parser.add_argument('--g5', required=True)
parser.add_argument('--out', required=True)
args = parser.parse_args()
base = ROOT/'benchmarks/results'
out = base/args.out
assert out.resolve().parent == base.resolve()
out.mkdir()
(out/'report.py').write_bytes(Path(__file__).read_bytes())
report = {'scope': 'Current bounded-score build, H4 curves and original G5 scale workflows',
    'H4_complete': False, 'completed_weight_percent': 45, 'held_out_geometry_read': False,
    'new_product_changes': False, 'new_quality_claim': False, 'runs': []}
for name, fixture in [(args.curves, 'curves'), (args.g5, 'g5')]:
    folder = (base/name).resolve()
    assert folder.parent == base.resolve()
    raw = load(folder/'results.json')
    assert raw['passes'] and len(raw['results']) == 2 and raw['fixture_kind'] == fixture
    assert {r['browser'] for r in raw['results']} == {'chrome', 'firefox'}
    assert guards(Path(raw['pinned_validator']), fixture) == raw['guards']
    assert raw['quick_start'] == (fixture == 'curves') and raw['workers_override'] is None
    summary = deepcopy(raw)
    for row in summary['results']:
        assert row['passes'] and row['status'] == 'valid' and not row['affinity_errors']
        for relative, expected in row['artifacts'].items():
            assert digest((folder/row['browser']/relative).read_bytes()) == expected
        row['app'].pop('telemetry', None)
        row['layout_sha256'] = row['artifacts']['layout.json']
        library = load(folder/row['browser']/'library.json')
        request = load(folder/row['browser']/'request.json')
        vertices = {p['id']: sum(len(g['outer'])+sum(map(len, g['holes']))
            for g in (p.get('components') or [p['polygon']])) for p in library['parts']}
        row['vertices_across_copies'] = sum(vertices[p['id']]*p['quantity'] for p in request['parts'])
    if fixture == 'curves':
        prior = base/'h4-curve-scale-20261015T183542Z'
        inventory = load(prior/'summary.json')['archive']
        assert digest((prior/'raw.zip').read_bytes()) == inventory['sha256']
        comparisons = []
        with zipfile.ZipFile(prior/'raw.zip') as old_archive:
            for browser in ['chrome', 'firefox']:
                for name_in_zip in [browser+'/layout.json', browser+'/project.zip']:
                    assert digest(old_archive.read(name_in_zip)) == inventory['members'][name_in_zip]['sha256']
                before = old_archive.read(browser+'/layout.json')
                after = (folder/browser/'layout.json').read_bytes()
                comparisons.append({'browser': browser, 'file': 'layout.json',
                    'before_sha256': digest(before), 'after_sha256': digest(after), 'identical': before == after})
                with zipfile.ZipFile(BytesIO(old_archive.read(browser+'/project.zip'))) as old, zipfile.ZipFile(folder/browser/'project.zip') as new:
                    assert old.testzip() is None and new.testzip() is None
                    files = sorted(n for n in old.namelist() if n.endswith(('.svg', '.dxf')))
                    assert files == sorted(n for n in new.namelist() if n.endswith(('.svg', '.dxf')))
                    for item in files:
                        a, b = old.read(item), new.read(item)
                        comparisons.append({'browser': browser, 'file': item,
                            'before_sha256': digest(a), 'after_sha256': digest(b), 'identical': a == b})
        summary['previous_scale_comparison'] = {'baseline': prior.relative_to(ROOT).as_posix(),
            'archive_sha256': inventory['sha256'], 'rows': comparisons}
    paths = sorted(p for p in folder.rglob('*') if p.is_file())
    archive = folder/'raw.zip'
    assert not archive.exists()
    inventory = {p.relative_to(folder).as_posix(): {'sha256': digest(p.read_bytes()), 'bytes': p.stat().st_size} for p in paths}
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in paths:
            z.write(p, p.relative_to(folder).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist()) == set(inventory)
        for name_in_zip, expected in inventory.items():
            data = z.read(name_in_zip)
            assert digest(data) == expected['sha256'] and len(data) == expected['bytes']
    summary['source_guards_passed'] = True
    summary['archive'] = {'path': 'raw.zip', 'sha256': digest(archive.read_bytes()),
        'bytes': archive.stat().st_size, 'members': inventory, 'crc_and_member_hashes_verified': True}
    write(folder/'summary.json', summary)
    report['runs'].append({'directory': folder.relative_to(ROOT).as_posix(), 'fixture': fixture,
        'source_guards_passed': True, 'guards': summary['guards'],
        'archive': {k: v for k, v in summary['archive'].items() if k != 'members'},
        'archive_members': len(inventory), 'passes': summary['passes'],
        'quick_start': summary['quick_start'], 'workers_override': summary['workers_override'],
        'results': [{**{k: r[k] for k in ['browser', 'status', 'passes', 'peak_rss_bytes',
            'peak_private_bytes', 'layout_sha256', 'independent_check', 'vertices_across_copies']},
            'app': {k: r['app'][k] for k in ['version', 'workers_field', 'worker_notice',
                'maximum_workers', 'maximum_long_task_ms', 'maximum_event_loop_gap_ms',
                'import_seconds', 'nest_seconds', 'export_seconds']}}
            for r in summary['results']],
        'previous_scale_comparison': summary.get('previous_scale_comparison')})
    # Remove only individually verified files inside this exact result directory.
    # Keep the frozen plan, runner snapshots and screenshots directly reviewable.
    for p in paths:
        if p.parent == folder and p.name not in ['progress.json', 'results.json']:
            continue
        if p.name == 'screen.png':
            continue
        assert p.resolve().is_relative_to(folder)
        assert digest(p.read_bytes()) == inventory[p.relative_to(folder).as_posix()]['sha256']
        p.unlink()
    print(json.dumps({'archived': folder.name, 'members': len(inventory), 'bytes': archive.stat().st_size}), flush=True)
report['frozen_shop_manifest_sha256'] = digest((ROOT/'benchmarks/datasets/shop/manifest.json').read_bytes())
assert report['frozen_shop_manifest_sha256'] == '02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
write(out/'checks.json', report)
print(json.dumps({'passes': all(r['passes'] for r in report['runs']), 'H4_complete': False}), flush=True)
