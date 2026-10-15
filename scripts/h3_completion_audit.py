"""Verify retained H3 evidence without rerunning searches or changing the gate.

Run after the once-only reserved-project evaluation. This only hashes frozen
inputs, checks saved results, and packages newly collected raw evidence.
"""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import zipfile

from h3_heldout_audit import guards

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'benchmarks/results'
OUT = RESULTS / 'h3-complete-20261015'
HELD = RESULTS / 'h3-heldout-20261015'
CALIBRATION = RESULTS / 'h3-evaluator-calibration-20261015T205719Z'
REPLAY = RESULTS / 'h3-completion-native-revalidation-20261015'
NATIVE = RESULTS / 'h3-lightburn-20261014T001636Z'


def digest(data):
    return sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def archive():
    """Keep result/plan/marker files loose; preserve every raw byte in a ZIP."""
    destination = OUT / 'raw.zip'
    if destination.exists():
        integrity = read(OUT / 'integrity.json')
    else:
        members = []
        with zipfile.ZipFile(destination, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            paths = sorted(p for root in [CALIBRATION, HELD, REPLAY]
                           for p in root.rglob('*') if p.is_file())
            for p in paths:
                data = p.read_bytes()
                name = p.relative_to(ROOT).as_posix()
                z.writestr(name, data)
                members.append({'path': name, 'bytes': len(data), 'sha256': digest(data)})
            for p in [ROOT/'scripts/h3_heldout_audit.py', ROOT/'scripts/h3_native_revalidation.py',
                      ROOT/'output/h3-heldout-20261015.log']:
                data = p.read_bytes()
                name = p.relative_to(ROOT).as_posix()
                z.writestr(name, data)
                members.append({'path': name, 'bytes': len(data), 'sha256': digest(data)})
        integrity = {'archive': 'raw.zip', 'sha256': digest(destination.read_bytes()),
                     'bytes': destination.stat().st_size, 'members': members}
    assert digest(destination.read_bytes()) == integrity['sha256']
    with zipfile.ZipFile(destination) as z:
        assert z.testzip() is None
        assert set(z.namelist()) == {r['path'] for r in integrity['members']}
        for r in integrity['members']:
            data = z.read(r['path'])
            assert len(data) == r['bytes'] and digest(data) == r['sha256'], r['path']
    integrity['crc_and_member_hashes_passed'] = True
    write(OUT/'integrity.json', integrity)
    return integrity


def main():
    OUT.mkdir(exist_ok=True)
    plan = read(HELD/'plan.json')
    original_plan = subprocess.check_output(['git', 'show',
        '5b70e7a:benchmarks/results/h3-heldout-20261015/plan.json'], cwd=ROOT)
    assert original_plan == (HELD/'plan.json').read_bytes()
    assert plan['guards'] == guards()
    held = read(HELD/'results.json')
    calibration = read(CALIBRATION/'results.json')
    replay = read(REPLAY/'results.json')
    assert held['all_passed'] and held['guards_unchanged'] and len(held['rows']) == 3
    assert not held['product_tuning_allowed'] and not held['published_v1_quality_run']
    assert digest((HELD/'plan.json').read_bytes()) == held['plan_sha256']
    assert calibration['row']['passed'] and calibration['guards'] == plan['guards']
    assert digest((CALIBRATION/'results.json').read_bytes()) == plan['calibration_sha256']
    assert replay['passed'] and replay['guards_unchanged'] and replay['guards'] == plan['guards']
    assert len(replay['rows']) == 5 and replay['new_searches'] == 0

    corpus = ROOT/'benchmarks/datasets/shop'
    manifest = read(corpus/'manifest.json')
    for r in manifest['corpus_inventory']:
        assert digest((corpus/r['path']).read_bytes()) == r['sha256'], r['path']
    assert len(manifest['corpus_inventory']) == 1181
    original_projects = {r['path'] for r in manifest['files']
                         if Path(r['path']).suffix in ['.lbrn', '.lbrn2']}
    training_path = RESULTS/'h3-reviewed-prerequisites-20261015T204219Z/results.json'
    training = read(training_path)
    assert training['all_checked'] and training['source_guards_passed']
    assert training['guards']['product'] == plan['guards']['product']
    assert all(r['noop_byte_identical'] for r in training['rows'])
    assert original_projects == {r['path'] for r in training['rows'] if r['kind']=='original'} | {
        r['path'] for r in held['rows']}
    assert len(original_projects) == 59
    old_training_path = RESULTS/'h3-reviewed-prerequisites-20261015T190641Z/results.json'
    old = {(r['path'],r['kind']):r for r in read(old_training_path)['rows']}
    assert all(r['artifacts']['inspect-stdout.json'] == old[r['path'],r['kind']]['artifacts']['inspect-stdout.json']
               for r in training['rows'])
    reader_path = RESULTS/'h3-reader-20261015T190547Z.json'
    readers = {r['path']:r for r in read(reader_path)['rows']}
    assert all(r['artifacts']['inspect-stdout.json'] == readers[r['path']]['scene_sha256']
               for r in training['rows'] if r['kind']=='original')
    geometry_path = RESULTS/'h3-geometry-20261015T190554Z.json'
    geometry = read(geometry_path)
    assert geometry['shapes_failed'] == 0 and geometry['shapes_passed'] == 1550
    repair_path = RESULTS/'h3-text-cache-20261015T190617Z.json'
    repair = read(repair_path)
    assert repair['repaired_geometry_passes'] and len(repair['rows']) == 8
    checks_path = RESULTS/'h3-missing-layer-native-20261015/checks.json'
    checks = read(checks_path)
    assert checks['cli_sha256'] == plan['guards']['files']['target/release/nestbolt.exe']
    assert checks['workspace-tests'] == {'passed':295,'failed':0,'ignored':1}
    assert checks['release-cli-tests']['passed'] == 26 and checks['browser_tests']['passed'] == 84
    native = read(NATIVE/'native-check.json')
    assert native['passed'] and all(r['passed'] for r in native['cases'])
    native_artifacts = read(NATIVE/'artifacts.json')
    for r in native_artifacts['files']:
        data = (NATIVE/r['path']).read_bytes()
        assert len(data) == r['bytes'] and digest(data) == r['sha256'], r['path']

    integrity = archive()
    with zipfile.ZipFile(OUT/'raw.zip') as z:
        for root, rows in [(HELD,held['rows']), (CALIBRATION,[calibration['row']])]:
            for row in rows:
                for name, expected in row['artifacts'].items():
                    member = (root/Path(row['path']).stem/name).relative_to(ROOT).as_posix()
                    assert digest(z.read(member)) == expected, member
    leaves = [s for r in held['rows'] for s in r['geometry']]
    original_leaves = [s for r in geometry['rows'] for s in r['shapes']]
    assert all(s['passed'] for s in leaves+original_leaves)
    placements = [p for r in held['rows'] for p in r['diagnostic_placements']+r['search_placements']]
    unit_geometries = [g for r in held['rows'] for key in ['unit_geometry','import_geometry','search_geometry'] for g in r[key]]
    assert all(p['passed'] for p in placements+unit_geometries)
    inputs = [HELD/'plan.json', HELD/'results.json', CALIBRATION/'results.json', REPLAY/'results.json',
              training_path, old_training_path, reader_path, geometry_path, repair_path, checks_path,
              NATIVE/'native-check.json', NATIVE/'artifacts.json',
              RESULTS/'h3-open-line-fix-20261015.json', RESULTS/'h3-missing-layer-native-20261015/previous-comparison.json']
    value = {
        'scope':'H3 requirement review after frozen training and once-only reserved evaluation',
        'H3':True, 'completion_percent':45, 'other_open_gates':['H2','H4','H5'],
        'product_commit':plan['product_commit'], 'evaluation_plan_commit':'5b70e7a', 'guards':plan['guards'],
        'frozen_inventory_files':1181, 'all_original_projects_accounted_for':len(original_projects),
        'noop_originals':59, 'noop_auxiliary_repairs':8, 'unchanged_training_inspection_payloads':64,
        'original_compared_leaves':len(original_leaves)+len(leaves),
        'original_missing_text_not_credited':122, 'approved_repair_leaves':477,
        'reserved':{'projects':3,'leaves':len(leaves),'contours':sum(s['paths'] for s in leaves),
            'maximum_point_mm':max(max(s['product_to_oracle_mm'],s['oracle_to_product_mm']) for s in leaves),
            'maximum_bounds_mm':max(s['bbox_difference_mm'] for s in leaves),
            'maximum_image_corner_mm':max(s['image_corner_difference_mm'] for s in leaves),
            'maximum_unit_boundary_mm':max(g['boundary_hausdorff_mm'] for g in unit_geometries),
            'maximum_overlap_mm2':max(p['maximum_overlap_mm2'] for p in placements),
            'maximum_outside_mm2':max(p['maximum_outside_mm2'] for p in placements),
            'metric_delta':max(r['metric_delta'] for r in held['rows']),
            'canonical_diagnostic_sheets':sum(len(r['canonical']) for r in held['rows']),
            'canonical_searched_sheets':sum(len(r['search_canonical']) for r in held['rows']),
            'native_zero_handle_checks':sum(len(r['native_zero_handle_checks']) for r in held['rows'])},
        'combined_diagnostic_sheets':checks['canonical_sheet_checks']+sum(len(r['canonical']) for r in held['rows']),
        'combined_diagnostic_units':checks['units']+sum(len(r['unit_geometry']) for r in held['rows']),
        'native_artifacts_verified':len(native_artifacts['files']),
        'current_native_replay':{'projects':5,'byte_identical':sum(c['byte_equal'] for r in replay['rows'] for c in r['comparisons']),
            'maximum_xform_delta':max(c['maximum_top_level_xform_difference'] for r in replay['rows'] for c in r['comparisons'])},
        'raw_archive':{'sha256':integrity['sha256'],'bytes':integrity['bytes'],'members':len(integrity['members']),
            'crc_and_member_hashes_passed':True},
        'input_reports':{p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in inputs},
        'script_sha256':digest(Path(__file__).read_bytes()),
        'held_out_evaluation_only':True, 'product_tuning_on_reserved_files':False,
        'published_v1_quality_run':False, 'release_or_registry_publication':False,
    }
    write(OUT/'checks.json',value)
    print(json.dumps({k:v for k,v in value.items() if k not in ['guards','input_reports']}))


if __name__ == '__main__':
    main()
