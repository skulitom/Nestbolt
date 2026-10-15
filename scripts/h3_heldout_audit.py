"""Fixed H3 correctness evaluation, separate from published v1 quality claims.

Calibrate the existing geometry/writer checks on training lb-02, then commit
the plan before opening the three reserved native projects. Evaluation runs
once; every outcome remains recorded. Do not tune on these inputs afterward.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import traceback

import psutil
from h2_import_audit import source_digest
from h2_lightburn_labels import holes, cutting
from h3_geometry_audit import normalize, compare, write_json
from h3_open_line_audit import independent_units, independent_placements
from h3_writer_audit import audit
from h6_material_cost import run, equivalent
from shop_public_reference_audit import curves

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'
OUT = ROOT/'benchmarks/results/h3-heldout-20261015'
CLI = ROOT/'target/release/nestbolt.exe'
CPU = 8
REQUEST = {'sheets': [{'width_mm':2000, 'height_mm':2000}], 'spacing_mm':2, 'edge_spacing_mm':2}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def manifest():
    assert digest(CORPUS/'manifest.json') == '02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
    return {r['path']: r for r in json.loads((CORPUS/'manifest.json').read_bytes())['files']}


def guards():
    paths = [CLI, ROOT/'target/release/examples/lightburn_inspect.exe',
             ROOT/'target/release/examples/lightburn_roundtrip.exe', CORPUS/'manifest.json']
    paths += [ROOT/'scripts'/p for p in [Path(__file__).name, 'h2_import_audit.py',
        'h2_lightburn_labels.py','h3_geometry_audit.py','h3_geometry_oracle.mjs',
        'h3_open_line_audit.py','h3_writer_audit.py','h6_material_cost.py',
        'shop_reference_labels.py','shop_public_reference_audit.py','maker_geometry.py',
        'cutting_development_set.py']]
    paths += [p for p in (ROOT/'.cache/shop-oracle/node_modules/lbrn2-to-svg').rglob('*') if p.is_file()]
    paths.append(ROOT/'.cache/shop-oracle/package-lock.json')
    return {'product': source_digest(), 'files': {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}}


def case(entry, pair, directory):
    directory.mkdir()
    record = {'path':entry['path'], 'source_sha256':entry['sha256'],
              'label':entry['label'], 'label_sha256':entry['label_sha256'],
              'split':entry['split'], 'passed':False}
    def execute(command, name, timeout):
        execution = run(command, directory, name, CPU, timeout)
        record[name] = execution
        write_json(directory/'progress.json', record)
        assert execution['exit_code'] == 0, execution
        return json.loads((directory/(name+'-stdout.json')).read_bytes())
    try:
        source_path = CORPUS/entry['path']
        assert digest(source_path) == entry['sha256']
        assert digest(CORPUS/entry['label']) == entry['label_sha256']
        source = source_path.read_bytes()
        label = json.loads((CORPUS/entry['label']).read_bytes())
        inspected = execute([ROOT/'target/release/examples/lightburn_inspect.exe', source_path], 'inspect', 10)
        scene = inspected['scene']
        assert inspected['noop_byte_identical']
        assert all(s['geometry_complete'] for s in scene['shapes'])
        record['noop_byte_identical'] = True
        execute([CLI,'import',source_path,'--output',directory/'library.json'], 'import', 10)
        library = json.loads((directory/'library.json').read_bytes())
        assert library['lightburn']['xml'].encode('utf-8') == source
        writer = execute([ROOT/'target/release/examples/lightburn_roundtrip.exe',source_path], 'writer', 10)
        assert writer['status'] == 'written' and writer['identity_byte_equal'] and writer['validation']['valid']
        record['canonical'] = audit(source, writer)
        normalized, indices, omitted, zeros = normalize(source)
        record['omitted'] = omitted
        record['zero_handle_shapes'] = zeros
        assert not omitted
        (directory/'normalized.lbrn2').write_text(normalized, encoding='utf-8', newline='\n')
        write_json(directory/'oracle-request.json', {'projects':[{'path':entry['path'],
            'normalized_xml':str(directory/'normalized.lbrn2'), 'shape_indices':indices,
            'svg_directory':str(directory/'oracle')}], 'oracle_report':str(directory/'oracle.json')})
        oracle = run(['node',ROOT/'scripts/h3_geometry_oracle.mjs',directory/'oracle-request.json'], directory, 'oracle', CPU, 120)
        record['oracle'] = oracle
        assert oracle['exit_code'] == 0
        assert 'error' not in json.loads((directory/'oracle.json').read_bytes())['reports'][0]
        geometry = []
        for i in indices:
            try:
                geometry.append({'shape':i, **compare(scene['shapes'][i],directory/'oracle'/f'{i}.svg')})
            except Exception:
                geometry.append({'shape':i, 'passed':False, 'error':traceback.format_exc()})
        record['geometry'] = geometry
        record['native_zero_handle_checks'] = []
        if zeros:
            assert pair['split'] == entry['split'] and digest(CORPUS/pair['path']) == pair['sha256']
            native = curves(CORPUS/pair['path'])
            for i in zeros:
                shape = scene['shapes'][i]
                x0,y0,x1,y1 = shape['bounds_mm']
                def delta(path):
                    a,b,c,d = path.bbox()
                    return max(abs(a-x0),abs(b-x1),abs(-d-y0),abs(-c-y1))
                reference = min(native,key=delta)
                record['native_zero_handle_checks'].append({'shape':i, 'reference':pair['path'],
                    'sha256':pair['sha256'], **compare(shape,CORPUS/pair['path'],[reference])})
        assert all(r['passed'] for r in geometry + record['native_zero_handle_checks'])
        nesting = writer['nesting']
        expected = {tuple(sorted(p['top_level_shape_indices'])): p['holes'] for p in label['cut_parts']}
        actual = {tuple(sorted(u['members'])): holes(scene,u['members']) for u in nesting['units']}
        record['label_checks'] = {'membership_and_physical_holes_match':actual == expected,
            'expected':[{'members':list(k),'holes':v} for k,v in sorted(expected.items())],
            'actual':[{'members':list(k),'holes':v} for k,v in sorted(actual.items())],
            'expected_fixed':sorted(s['top_level_shape_index'] for s in label.get('fixed_shapes',[])),
            'actual_fixed':sorted(nesting['fixed']), 'expected_cut_layers':label['cut_layers'],
            'actual_cut_layers':sorted({s['cut_index'] for s in scene['shapes'] if s['kind']!='Group' and cutting(scene,s)})}
        checks = record['label_checks']
        assert actual == expected and len(actual) == len(nesting['units']) == len(library['parts'])
        assert checks['expected_fixed'] == checks['actual_fixed'] and checks['expected_cut_layers'] == checks['actual_cut_layers']
        record['unit_geometry'], expected_units = independent_units(scene,directory/'oracle',nesting,.0005,
            [u['geometry'] for u in nesting['units']])
        record['diagnostic_placements'] = independent_placements(expected_units,writer)
        record['import_geometry'], _ = independent_units(scene,directory/'oracle',nesting,library['tolerance'],
            [p.get('components') or [p['polygon']] for p in library['parts']])
        write_json(directory/'request.json', REQUEST)
        execute([CLI,'nest','--library',source_path,'--request',directory/'request.json','--out-dir',directory/'nested',
                 '--seconds',3,'--seed',0,'--repeatable','--time-limit',90], 'search', 120)
        report = json.loads((directory/'nested/report.json').read_bytes())
        layout = json.loads((directory/'nested/layout.json').read_bytes())
        job = json.loads((directory/'nested/job.json').read_bytes())
        assert report['validation']['valid'] and len(layout['placements']) == len(nesting['units'])
        geometry_by_id = {p['id']:p['geometry'] for p in job['parts']}
        ids = library['lightburn']['unit_ids']
        record['search_geometry'], expected_units = independent_units(scene,directory/'oracle',nesting,
            library['tolerance'],[geometry_by_id[id] for id in ids])
        payload = {'nesting':nesting, 'identity_byte_equal':writer['identity_byte_equal'],
                   'width_mm':2000,'height_mm':2000,'files':[], 'validation':report['validation']}
        for sheet, filename in zip(layout['sheets'],report['files'],strict=True):
            assert filename.endswith('.lbrn2')
            payload['files'].append({'sheet':sheet['id'], 'xml':(directory/'nested'/filename).read_text(encoding='utf-8'),
                'placements':[{'unit':ids.index(p['part_id']),'transform':p['transform']} for p in layout['placements'] if p['sheet_id']==sheet['id']]})
        record['search_canonical'] = audit(source,payload)
        record['search_placements'] = independent_placements(expected_units,payload)
        validated = execute([CLI,'validate','--library',directory/'library.json','--request',directory/'request.json',
                             '--layout',directory/'nested/layout.json'], 'validate', 60)
        assert validated['valid']
        record['metric_delta'] = equivalent(validated['metrics'],report['validation']['metrics'])
        record['search_metrics'] = validated['metrics']
        record['passed'] = True
    except Exception:
        record['error'] = traceback.format_exc()
    record['artifacts'] = {p.relative_to(directory).as_posix():digest(p) for p in directory.rglob('*') if p.is_file()}
    write_json(directory/'result.json',record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['calibrate','plan','evaluate'])
    parser.add_argument('--calibration',type=Path)
    args = parser.parse_args()
    psutil.Process().cpu_affinity([CPU])
    entries = manifest()
    if args.action == 'calibrate':
        directory = ROOT/'benchmarks/results'/('h3-evaluator-calibration-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        directory.mkdir()
        entry = entries['native/lb-02.lbrn2']
        assert entry['split'] == 'training'
        before = guards()
        result = case(entry,entries['native/lb-02.svg'],directory/'lb-02')
        assert guards() == before
        write_json(directory/'results.json',{'guards':before,'row':result,'held_out_geometry_read':False})
        print(directory, result['passed'], flush=True)
        return 0 if result['passed'] else 1
    if args.action == 'plan':
        assert args.calibration is not None
        calibration = json.loads(args.calibration.read_bytes())
        assert calibration['row']['passed'] and calibration['guards'] == guards()
        selected = [r for r in entries.values() if r['split']=='held_out' and Path(r['path']).suffix in ['.lbrn','.lbrn2']]
        assert {r['path'] for r in selected} == {'native/lb-01.lbrn2','native/lb-06.lbrn2','native/lb-08.lbrn2'}
        pairs = [entries[str(Path(r['path']).with_suffix('.svg')).replace('\\','/')] for r in selected]
        assert all(p['split']=='held_out' for p in pairs)
        OUT.mkdir()
        write_json(OUT/'plan.json',{'scope':__doc__,'product_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'calibration':str(args.calibration),'calibration_sha256':digest(args.calibration),'guards':guards(),
            'cases':selected,'paired_native_svgs':pairs,'cpu':CPU,'request':REQUEST,
            'search':{'repeatable_seconds':3,'seed':0,'time_limit_seconds':90,'external_limit_seconds':120},
            'criteria':{'geometry_mm':.01,'samples_per_contour':64,'flatten_mm':.0005,'unit_boundary_mm':.01,
                        'independent_overlap_outside_mm2':1e-8,'metrics_json_difference':1e-9},
            'prior_training_complete':True,'held_out_geometry_read_at_plan':False,'published_v1_quality_run':False})
        print(OUT/'plan.json',flush=True)
        return 0
    plan_path = OUT/'plan.json'
    plan = json.loads(plan_path.read_bytes())
    # A committed, unchanged plan is required before the first reserved read.
    committed = subprocess.check_output(['git','show','HEAD:'+plan_path.relative_to(ROOT).as_posix()],cwd=ROOT)
    assert committed == plan_path.read_bytes() and plan['guards'] == guards()
    assert plan['request'] == REQUEST
    marker = OUT/'opened.json'
    with marker.open('x',encoding='utf-8',newline='\n') as opened:
        json.dump({'started_utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':digest(plan_path)},opened,indent=2)
        opened.write('\n')
    rows = []
    for entry,pair in zip(plan['cases'],plan['paired_native_svgs'],strict=True):
        assert guards() == plan['guards']
        assert entry == entries[entry['path']] and pair == entries[pair['path']]
        row = case(entry,pair,OUT/Path(entry['path']).stem)
        rows.append(row)
        write_json(OUT/'progress.json',rows)
        print(entry['path'],row['passed'],flush=True)
    unchanged = guards() == plan['guards']
    write_json(OUT/'results.json',{'scope':__doc__,'plan_sha256':digest(plan_path),'guards_unchanged':unchanged,
        'all_passed':unchanged and len(rows)==3 and all(r['passed'] for r in rows),'rows':rows,
        'held_out_geometry_read':True,'product_tuning_allowed':False,'published_v1_quality_run':False})
    return 0 if unchanged and all(r['passed'] for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
