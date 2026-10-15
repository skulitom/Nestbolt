"""Prepare an authored rigid LightBurn group through the public CLI, CPU0 only.

Original project and both cutting sidecars are retained for native review. This
does not read corpus geometry or run the final acceptance set.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    folder = parser.parse_args().output.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results') and not folder.exists()
    folder.mkdir()
    binary = ROOT/'target/release/nestbolt.exe'
    before, binary_hash = source_digest(), digest(binary)
    source = ROOT/'crates/core/tests/fixtures/lead-group.lbrn2'
    (folder/source.name).write_bytes(source.read_bytes())
    imported = run([binary,'import',folder/source.name,'--output',folder/'library.json'])
    (folder/'import.log').write_text(imported,encoding='utf-8',newline='\n')
    request = {'parts':[{'id':'lead-group-unit-1','quantity':2}],
               'sheets':[{'width_mm':150,'height_mm':100,'count':1}],
               'spacing_mm':0.2,'edge_spacing_mm':1,'lead_in':{'kerf_mm':0.2}}
    write_json(folder/'request.json',request)
    command = [binary,'nest','--library',folder/'library.json','--request',folder/'request.json',
               '--out-dir',folder/'nested','--seconds','1','--repeatable','--time-limit','30']
    report = json.loads(run(command))
    lead = report['lead_in']
    assert report['validation']['valid'] and lead['validation']['valid'] and lead['validation']['source_checked']
    assert (lead['expected_contours'],lead['reserved_contours'],lead['flagged_contours']) == (10,8,2)
    assert len(report['files']) == 3
    params = ['--library',folder/'library.json','--request',folder/'request.json','--layout',folder/'nested/layout.json']
    checked = json.loads(run([binary,'validate',*params]))
    write_json(folder/'checked.json',checked)
    assert checked['lead_in'] == lead
    assert checked['metrics'] == report['validation']['metrics']
    run([binary,'export',*params,'--out-dir',folder/'reexport'])
    assert all((folder/'nested'/f).read_bytes()==(folder/'reexport'/f).read_bytes() for f in report['files'])
    request.pop('lead_in')
    write_json(folder/'preserving-request.json',request)
    run([binary,'export','--library',folder/'library.json','--request',folder/'preserving-request.json',
         '--layout',folder/'nested/layout.json','--out-dir',folder/'preserving'])
    native = 'lead-group-sheet-1.lbrn2'
    assert (folder/'nested'/native).read_bytes() == (folder/'preserving'/native).read_bytes()
    assert source_digest() == before and digest(binary) == binary_hash
    write_json(folder/'preparation.json',{
        'date':datetime.now(timezone.utc).isoformat(),'held_out_geometry_read':False,
        'scope':'Authored public CLI search, revalidation and identical repeated exports; native review recorded separately',
        'source_sha256':before,'binary_sha256':binary_hash,'runner_sha256':digest(Path(__file__)),
        'cpu_affinity':[0],'command':list(map(str,command)),
        'expected_contours':10,'reserved_contours':8,'flagged_open_contours':2,
        'preserved_project_identical_with_leads_enabled':True,
        'artifacts':{p.relative_to(folder).as_posix():digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}})
    print(json.dumps({'folder':str(folder),'coverage':lead['validation']['coverage']}))


if __name__ == '__main__':
    main()
