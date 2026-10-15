"""Audit archived measurements and revalidate harness-only failures without rerunning search."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import zipfile

from cutting_development_set import ROOT, FOLDER, digest, load_cases, write_json
from h2_import_audit import source_digest
from h2_lightburn_prepare import run
from h6_material_cost import aggregate, equivalent, equivalent_common


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('original',type=Path); parser.add_argument('output',type=Path)
    args=parser.parse_args(); original=args.original.resolve(); output=args.output.resolve()
    assert original.is_relative_to(ROOT/'benchmarks/results') and output.is_relative_to(ROOT/'benchmarks/results') and not output.exists()
    output.mkdir()
    record=json.loads((original/'results.json').read_text(encoding='utf-8'))
    binary=ROOT/'target/release/nestbolt.exe'
    assert source_digest()==record['guards']['product'] and digest(binary)==record['guards']['binary']
    assert digest(FOLDER/'manifest.json')==record['guards']['manifest']
    expected={(r['id'],k,s,a) for r,j in load_cases() for k in [0.2,1.5] for s in [0,1,2] for a in ['baseline','leads']}
    observed={(r['job'],r['kerf_mm'],r['seed'],r['arm']) for r in record['rows']}
    assert len(record['rows'])==156 and observed==expected
    corrected=[]; rows=deepcopy(record['rows']); maximum=0.0
    for row in rows:
        archive=original/row['archive']
        assert digest(archive)==row['archive_sha256']
        with zipfile.ZipFile(archive) as zipped:
            case=json.loads(zipped.read('case.json'))
            for name,wanted in case['artifacts'].items():
                assert sha256(zipped.read(name)).hexdigest()==wanted,(archive.name,name)
            searched=json.loads(zipped.read('nested/report.json'))
            checked=json.loads(zipped.read('validate-stdout.json'))
            assert searched['validation']['valid'] and checked['valid']
            maximum=max(maximum,equivalent(checked['metrics'],searched['validation']['metrics']))
            maximum=max(maximum,equivalent_common(checked['common_line'],searched['common_line']))
            if row['arm']=='leads':
                maximum=max(maximum,equivalent(checked['lead_in'],searched['lead_in']))
                assert checked['lead_in']['validation']['valid'] and checked['lead_in']['validation']['source_checked']
            if row['status']=='valid':
                equivalent(row['metrics'],checked['metrics'])
                continue
            assert row['nest']['exit_code']==0 and row['revalidation']['exit_code']==0
            assert "common_line" in row['error'] and row['arm']=='baseline', 'Unexpected failure requires investigation'
            target=output/archive.stem; target.mkdir()
            for name in ['library.json','request.json','nested/layout.json']:
                (target/Path(name).name).write_bytes(zipped.read(name))
            params=['--library',target/'library.json','--request',target/'request.json','--layout',target/'layout.json']
            fresh=json.loads(run([binary,'validate',*params],cpu=0))
            write_json(target/'fresh-validation.json',fresh)
            assert fresh['valid']
            maximum=max(maximum,equivalent(fresh['metrics'],searched['validation']['metrics']))
            maximum=max(maximum,equivalent_common(fresh['common_line'],searched['common_line']))
            corrected.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'seed':row['seed'],'arm':row['arm'],
                'original_status':'failed','reason':'Only unordered COMMON edge/path list order differed after f64 JSON round trip',
                'original_archive':archive.relative_to(ROOT).as_posix(),'original_archive_sha256':row['archive_sha256'],
                'saved_layout_unchanged':True,'new_search':False,'fresh_validation_valid':True})
            row.update(status='valid',original_status='failed',material=fresh['metrics']['normalized_material'],metrics=fresh['metrics'],
                       cut_without_common_mm=sum(r['cut_length_without_common_mm'] for r in fresh['common_line']),
                       cut_with_common_mm=sum(r['cut_length_with_common_mm'] for r in fresh['common_line']))
    assert source_digest()==record['guards']['product'] and digest(binary)==record['guards']['binary']
    result={'date':datetime.now(timezone.utc).isoformat(),'scope':__doc__,
        'original':original.relative_to(ROOT).as_posix(),'original_results_sha256':digest(original/'results.json'),
        'source_sha256':source_digest(),'binary_sha256':digest(binary),'script_sha256':digest(Path(__file__)),
        'comparator_sha256':digest(ROOT/'scripts/h6_material_cost.py'),
        'held_out_geometry_read':False,'new_search':False,'cpu_affinity':[0],
        'archive_count_verified':len(rows),'original_valid':record['valid'],'valid':len(rows),
        'maximum_numeric_difference':maximum,'corrections':corrected,'rows':rows,'pairs':aggregate(rows),
        'artifacts':{p.relative_to(output).as_posix():digest(p) for p in sorted(output.rglob('*')) if p.is_file()}}
    write_json(output/'reconciled.json',result)
    print(json.dumps({'valid':len(rows),'corrections':corrected,'maximum_numeric_difference':maximum}))


if __name__=='__main__':
    main()
