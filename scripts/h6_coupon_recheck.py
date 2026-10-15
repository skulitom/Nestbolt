"""Revalidate the three native-previewed searched coupons with the current public pipeline.

No new search, native session or corpus access. Preserve every original file.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json
from h6_lead_settings_recheck import cut_paths
from h6_material_cost import equivalent

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT/'benchmarks/results/h6-lead-coupons-20261015T091012Z'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    output=parser.parse_args().output.resolve()
    assert output.is_relative_to(ROOT/'benchmarks/results') and not output.exists()
    output.mkdir(parents=True)
    binary=ROOT/'target/release/nestbolt.exe'
    before=source_digest(); binary_hash=digest(binary)
    inputs={}; rows=[]
    for name in ['line45','arc45','arc90']:
        folder=output/name; folder.mkdir()
        data_path=ORIGINAL/f'exports/{name}.json'
        source=ORIGINAL/f'exports/{name}-source.svg'
        for p in [data_path,source,ORIGINAL/f'exports/{name}.svg']:
            inputs[p.relative_to(ROOT).as_posix()]=digest(p)
        old=json.loads(data_path.read_text(encoding='utf-8'))
        (folder/(name+'.svg')).write_bytes(source.read_bytes())
        run([binary,'import',folder/(name+'.svg'),'--output',folder/'library.json'])
        request={'parts':[{'id':old['job']['parts'][0]['id'],'quantity':4}],
                 'sheets':[{'id':'stock','width_mm':65,'height_mm':50,'count':1}],
                 'spacing_mm':0.2,'edge_spacing_mm':1.0,'lead_in':old['options']}
        write_json(folder/'request.json',request); write_json(folder/'layout.json',old['layout'])
        params=['--library',folder/'library.json','--request',folder/'request.json','--layout',folder/'layout.json']
        report=json.loads(run([binary,'validate',*params]))
        write_json(folder/'report.json',report)
        leads=report['lead_in']
        assert report['valid'] and leads['validation']['valid'] and leads['validation']['source_checked']
        assert (leads['expected_contours'],leads['reserved_contours'],leads['flagged_contours'])==(8,8,0)
        for p in leads['parts']:
            baseline=next(p0 for p0 in old['parts'] if p0['part_id']==p['part_id'])
            equivalent({k:p[k] for k in baseline},baseline)
        run([binary,'export',*params,'--out-dir',folder/'export','--sheet-outline','true'])
        assert cut_paths(folder/'export/sheet-0.svg')==cut_paths(ORIGINAL/f'exports/{name}.svg')
        rows.append({'coupon':name,'reserved_contours':8,'flags':0,
                     'original_native_tested_plans_unchanged':True,'CUT_SVG_attributes_unchanged':True,
                     'independent_source_coverage_attachment_and_owner_checked':True})
    assert before==source_digest() and binary_hash==digest(binary)
    assert all(digest(ROOT/p)==value for p,value in inputs.items())
    write_json(output/'checks.json',{'date':datetime.now(timezone.utc).isoformat(),
        'scope':__doc__,'held_out_geometry_read':False,'source_sha256':before,'binary_sha256':binary_hash,
        'runner_sha256':digest(Path(__file__)),'inputs':inputs,'cpu_affinity':[0],'cases':rows,
        'artifacts':{p.relative_to(output).as_posix():digest(p) for p in sorted(output.rglob('*')) if p.is_file()}})
    print(json.dumps(rows))


if __name__=='__main__':
    main()
