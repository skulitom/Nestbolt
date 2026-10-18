"""Independently check filled outer geometry, so common mode cannot use a part hole."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import itertools
import json
import math
import shutil
import traceback
import zipfile
import shapely
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-mixed-exchange-pilot-20261018'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
def write(p,x):
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,indent=2);f.write('\n')
assert load(out/'verification.json')['all_original_archives_verified']
result=load(out/'results.json')
rows=[r for r in result['records'] if r['arm']!='normal']
assert len(rows)==48
tolerance=1e-7
# An insert inside a frame's hole must fail when only the original outer ring is used.
frame_outer=Polygon([(0,0),(10,0),(10,10),(0,10)])
inside=Polygon([(4,4),(6,4),(6,6),(4,6)])
assert frame_outer.intersects(inside) and frame_outer.distance(inside)==0
records=[]
try:
    for row in rows:
        assert row['status']=='valid'
        archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
            assert sha256(z.read('nested/layout.json')).hexdigest()==row['layout_sha256']
        assert job['clearance']==row['kerf_mm']
        parts={p['id']:p for p in job['parts']}
        assert Counter(p['part_id'] for p in layout['placements'])==Counter({p['id']:p['quantity'] for p in job['parts']})
        assert len({(p['part_id'],p['copy_index']) for p in layout['placements']})==len(layout['placements'])
        sheets={}
        for p in layout['placements']:
            part=parts[p['part_id']];assert len(part['geometry'])==1
            shape=Polygon(part['geometry'][0]['outer']);assert shape.is_valid and shape.area>0
            t=p['transform'];c=math.cos(t['rotation_radians']);s=math.sin(t['rotation_radians']);m=-1 if t['mirrored'] else 1
            transformed=affine_transform(shape,[m*c,-s,m*s,c,*t['translation']])
            assert transformed.is_valid
            sheets.setdefault(p['sheet_id'],[]).append((p['part_id'],p['copy_index'],transformed))
        pairs=0;minimum=math.inf
        for shapes in sheets.values():
            for a,b in itertools.combinations(shapes,2):
                pairs+=1
                assert a[2].disjoint(b[2]),(row['archive'],a[:2],b[:2],'filled outer overlap')
                slack=a[2].distance(b[2])-row['kerf_mm'];minimum=min(minimum,slack)
                assert slack>=-tolerance,(row['archive'],a[:2],b[:2],slack)
        records.append({'archive':row['archive'],'sha256':row['archive_sha256'],
                        'parts':len(layout['placements']),'same_sheet_pairs':pairs,
                        'minimum_clearance_slack_mm':minimum if pairs else None})
    write(out/'filled-outer-audit.json',{'all_holes_reserved':True,'cases':len(records),
        'same_sheet_pairs':sum(r['same_sheet_pairs'] for r in records),
        'minimum_clearance_slack_mm':min(r['minimum_clearance_slack_mm'] for r in records if r['same_sheet_pairs']),
        'absolute_clearance_tolerance_mm':tolerance,'shapely_version':shapely.__version__,
        'method':'Every original filled outer ring is transformed independently. All same-sheet pairs must be disjoint and at least kerf apart; no hole interiors are subtracted.',
        'source_sha256':digest(Path(__file__)),'records':records,'new_searches':0})
    shutil.copyfile(__file__,out/'audit-filled-outers.py')
except BaseException:
    write(out/'filled-outer-audit-failure.json',{'error':traceback.format_exc(),'completed_records':records});raise
print(json.dumps({'all_holes_reserved':True,'cases':len(records),'same_sheet_pairs':sum(r['same_sheet_pairs'] for r in records)}))
