"""Audit approved LightBurn repair prerequisites without changing frozen inputs.

All original training projects retain byte-identical inspection/no-op results.
The eight approved native text repairs are auxiliary inputs, with writer diffs
checked against their own bytes. This is not an original-geometry success or
held-out acceptance. Every independent rejection remains in the record.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from queue import Queue
import subprocess
import traceback
import xml.etree.ElementTree as E

from h2_import_audit import source_digest
from h3_writer_audit import audit
from h6_material_cost import run

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'
APPROVED = ROOT/'benchmarks/results/h3-text-cache-20261014T005902Z.json'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def guards():
    paths = [CORPUS/'manifest.json', APPROVED, Path(__file__), ROOT/'scripts/h3_writer_audit.py',
             ROOT/'scripts/h6_material_cost.py', ROOT/'target/release/nestbolt.exe',
             ROOT/'target/release/examples/lightburn_inspect.exe', ROOT/'target/release/examples/lightburn_roundtrip.exe']
    return {'product': source_digest(), **{p.relative_to(ROOT).as_posix(): digest(p) for p in paths}}


def main():
    manifest = json.loads((CORPUS/'manifest.json').read_text(encoding='utf-8'))
    assert digest(CORPUS/'manifest.json') == '02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
    training = {r['path']: r for r in manifest['files'] if r['split'] == 'training'}
    inventory = {r['path']: r['sha256'] for r in manifest['corpus_inventory']}
    originals = [r for r in training.values() if Path(r['path']).suffix in ['.lbrn', '.lbrn2']]
    assert len(originals) == 56
    repairs = json.loads(APPROVED.read_text(encoding='utf-8'))['rows']
    assert len(repairs) == 8 and sum(r['missing_original_caches'] for r in repairs) == 122
    cases = [dict(path=r['path'], sha256=r['sha256'], kind='original') for r in originals]
    for r in repairs:
        assert r['source'] in training and r['source_sha256'] == training[r['source']]['sha256']
        assert inventory[r['native_reference']] == r['native_reference_sha256']
        cases.append(dict(path=r['native_reference'], sha256=r['native_reference_sha256'], kind='native-repair',
                          original=r['source'], original_sha256=r['source_sha256'], repair_id=r['id']))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT/'benchmarks/results'/f'h3-reviewed-prerequisites-{stamp}'
    out.mkdir()
    before = guards()
    write(out/'plan.json', {'scope': __doc__, 'guards': before, 'cases': cases, 'cpus': [0, 2, 4, 6],
        'held_out_geometry_read': False, 'approved_decisions': [5, 6]})
    cpus = Queue()
    for cpu in [0, 2, 4, 6]:
        cpus.put(cpu)

    def check(index, case):
        cpu = cpus.get()
        folder = out/f'{index:03}'
        folder.mkdir()
        record = {**case, 'cpu': cpu, 'folder': folder.relative_to(ROOT).as_posix(), 'status': 'failed'}
        try:
            path = CORPUS/case['path']
            source = path.read_bytes()
            assert sha256(source).hexdigest() == case['sha256']
            root = E.fromstring(source)
            missing = sum(s.get('Type') == 'Text' and s.find('BackupPath') is None for s in root.iter('Shape'))
            record['uncached_text_shapes'] = missing
            record['inspect'] = run([ROOT/'target/release/examples/lightburn_inspect.exe', path], folder, 'inspect', cpu, 10)
            assert record['inspect']['exit_code'] == 0
            inspection = json.loads((folder/'inspect-stdout.json').read_bytes())
            assert inspection['noop_byte_identical']
            record['noop_byte_identical'] = True
            record['incomplete_leaf_shapes'] = [i for i, s in enumerate(inspection['scene']['shapes'])
                                                if s['kind'] != 'Group' and not s['geometry_complete']]
            repair_warnings = [w for w in inspection['scene']['warnings'] if 're-save in LightBurn' in w]
            record['text_repair_warning_count'] = len(repair_warnings)
            assert len(repair_warnings) == missing
            if case['kind'] == 'native-repair':
                assert missing == 0 and not record['incomplete_leaf_shapes']
            record['import'] = run([ROOT/'target/release/nestbolt.exe', 'import', path, '--output', folder/'library.json'],
                                   folder, 'import', cpu, 10)
            if record['import']['exit_code'] == 0:
                library = json.loads((folder/'library.json').read_bytes())
                assert library['lightburn']['xml'].encode('utf-8') == source
                record['public_import'] = 'imported'
                record['units'] = len(library['parts'])
            else:
                assert not (folder/'library.json').exists()
                error = (folder/'import-stderr.log').read_text(encoding='utf-8')
                record['public_import'] = 'rejected'
                record['import_error'] = error
                record['rejection_kind'] = next((kind for phrase, kind in [
                    ('group movable artwork separately', 'approved-mixed-group'),
                    ('incomplete geometry', 'approved-text-prerequisite' if missing else 'other-incomplete-geometry'),
                    ('no movable nesting units', 'no-movable-units'),
                    ('zero-width or zero-height', 'zero-area-open-path'),
                ] if phrase in error), 'unclassified')
                assert record['import']['exit_code'] != 'timeout'
            record['writer'] = run([ROOT/'target/release/examples/lightburn_roundtrip.exe', path], folder, 'writer', cpu, 10)
            assert record['writer']['exit_code'] == 0
            payload = json.loads((folder/'writer-stdout.json').read_bytes())
            record['writer_status'] = payload['status']
            if payload['status'] == 'written':
                record['canonical_checks'] = audit(source, payload)
                record['independently_validated'] = payload['validation'] is not None and payload['validation']['valid']
                record['writer_units'] = len(payload['nesting']['units'])
            else:
                record['writer_error'] = payload['error']
                assert record['public_import'] == 'rejected'
            if record.get('rejection_kind') == 'approved-mixed-group':
                assert payload['status'] == 'unit_error' and 'group movable artwork separately' in payload['error']
            record['status'] = 'checked'
        except Exception:
            record['error'] = traceback.format_exc()
        finally:
            cpus.put(cpu)
        record['artifacts'] = {p.name: digest(p) for p in folder.iterdir() if p.is_file()}
        write(folder/'case.json', record)
        return record

    rows = []
    with ThreadPoolExecutor(4) as pool:
        for future in as_completed([pool.submit(check, i, c) for i, c in enumerate(cases)]):
            row = future.result()
            rows.append(row)
            write(out/'progress.json', rows)
            print(json.dumps({k: row.get(k) for k in ['path', 'kind', 'status', 'public_import', 'rejection_kind', 'writer_status']}), flush=True)
    assert guards() == before, 'Source or executable changed during the audit'
    write(out/'results.json', {'scope': __doc__, 'guards': before, 'source_guards_passed': True,
        'held_out_geometry_read': False, 'all_checked': all(r['status'] == 'checked' for r in rows), 'rows': rows})
    print(out, flush=True)
    return 0 if all(r['status'] == 'checked' for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
