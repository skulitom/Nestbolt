"""Explain retained byte differences without changing the original replay result."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as E
import zipfile

from svgpathtools import Line, parse_path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h2-export-replay-20261015'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')

result=load(OUT/'results.json')
plan=load(OUT/'plan.json')
prior_path=ROOT/'benchmarks/results/h2-fidelity-20261014T012836Z.json'
assert digest(prior_path)==result['guards']['report']
prior={r['path']:r for r in load(prior_path)['rows']}
assert result['guards_unchanged'] and len(result['rows'])==246
assert all(r['library_geometry_equal'] and r['import']['exit_code']==r['export']['exit_code']==0 for r in result['rows'])
assert all(load(ROOT/r['folder']/'before/result.json')==prior[r['path']] for r in result['rows'])
reviews=[]
for row in result['rows']:
    folder=ROOT/row['folder']
    for file in row['files']:
        before=folder/'before'/file['file'];after=folder/'after'/file['file']
        assert digest(before)==file['before_sha256'] and digest(after)==file['after_sha256']
        if file['byte_identical']:
            assert before.read_bytes()==after.read_bytes()
            continue
        assert before.suffix=='.svg', 'Review unexpected format separately'
        old,new=E.fromstring(before.read_bytes()),E.fromstring(after.read_bytes())
        old_nodes=list(old.iter());new_nodes=list(new.iter())
        assert len(old_nodes)==len(new_nodes)
        changes=[];segments=0;paths=0
        for index,(a,b) in enumerate(zip(old_nodes,new_nodes)):
            assert a.tag==b.tag and a.text==b.text and a.tail==b.tail and len(a)==len(b)
            aa,bb=dict(a.attrib),dict(b.attrib)
            if a.tag.endswith('}path'):
                x,y=parse_path(aa.pop('d')),parse_path(bb.pop('d'))
                assert len(x)==len(y)
                assert len(x.continuous_subpaths())==len(y.continuous_subpaths())
                paths+=len(x.continuous_subpaths())
                segments+=len(x)
                for i,(s,t) in enumerate(zip(x,y)):
                    assert type(s)==type(t)
                    if s!=t:
                        assert isinstance(s,Line), 'Nonlinear difference requires a separate geometric bound'
                        changes.append({'element':index,'segment':i,'type':'Line',
                            'start_difference_mm':abs(s.start-t.start), 'end_difference_mm':abs(s.end-t.end)})
            assert aa==bb, 'Non-path geometry or metadata changed'
        maximum=max(max(r['start_difference_mm'],r['end_difference_mm']) for r in changes)
        # A straight segment is a convex combination of its endpoints. Matching
        # segment order bounds every corresponding point by the larger endpoint
        # displacement, and hence bounds the symmetric Hausdorff difference.
        original=prior[row['path']]['measurement']['max_hausdorff_mm']['svg']
        bound=original+maximum
        reviews.append({'path':row['path'],'file':file['file'],
            'before_sha256':file['before_sha256'],'after_sha256':file['after_sha256'],
            'subpaths':paths,'segments':segments,'changed_segments':changes,
            'maximum_endpoint_displacement_mm':maximum,
            'all_non_line_segments_and_other_xml_exact':True,
            'original_source_fidelity_mm':original,'triangle_bound_source_fidelity_mm':bound,
            'original_limit_mm':.01,'within_original_fidelity_limit':bound<=.01})
assert len(reviews)==1 and all(r['within_original_fidelity_limit'] for r in reviews)
review={'scope':__doc__,'H2_complete':False,'new_searches':0,'held_out_geometry_read':False,
    'input_result_sha256':digest(OUT/'results.json'),'original_byte_equality_passed':result['passed'],
    'current_import_geometry_matches':246,'current_saved_layout_exports_valid':246,
    'exports_compared':sum(len(r['files']) for r in result['rows']),
    'byte_identical_exports':sum(f['byte_identical'] for r in result['rows'] for f in r['files']),
    'fidelity_bridge_passes':True,'reviews':reviews,
    'historical_raw_hash_provenance':'Historical outputs were retained locally, with each case result equal to its committed report row. Raw-file hashes were first recorded during this replay, not at the original measurement.',
    'cause':'One-nanometre rounding differences are consistent with serialized-layout numeric replay; no isolated cause or byte identity is claimed for that SVG.',
    'original_failure_preserved':True,'threshold_changed':False}
(OUT/'review.py').write_bytes(Path(__file__).read_bytes())
write(OUT/'review.json',review)
paths=sorted(p for p in OUT.rglob('*') if p.is_file())
members={p.relative_to(OUT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in paths}
archive=OUT/'raw.zip'
assert not archive.exists()
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in paths:z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(members)
    for name,v in members.items():
        data=z.read(name)
        assert len(data)==v['bytes'] and sha256(data).hexdigest()==v['sha256']
write(OUT/'integrity.json',{'archive':'raw.zip','sha256':digest(archive),'bytes':archive.stat().st_size,
    'crc_and_every_member_hash_verified':True,'members':members})
for p in paths:
    if p.parent==OUT:continue
    assert p.resolve().is_relative_to(OUT.resolve())
    assert digest(p)==members[p.relative_to(OUT).as_posix()]['sha256']
    p.unlink()
print(json.dumps({'review':review,'archive_members':len(members),'archive_bytes':archive.stat().st_size},indent=2))
