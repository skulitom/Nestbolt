"""Check unit footprints against hashed independent per-shape SVG references.

The references were produced by the published MIT reader with the documented,
native-checked normalization. No source or held-out geometry is regenerated.
Also checks the diagnostic placements using these reference footprints in GEOS.
"""
import argparse
import ctypes
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from shapely import Polygon, box, make_valid, union_all
from shapely.affinity import affine_transform

from h3_geometry_audit import sources
from maker_geometry import flatten_segment
from shop_public_reference_audit import curves, image_corners

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('writer_report',type=Path);args=parser.parse_args()
    kernel=ctypes.windll.kernel32;kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<8)
    source_hash=sources();runner_hash=sha256(Path(__file__).read_bytes()).hexdigest()
    writer=json.loads(args.writer_report.read_text(encoding='utf-8'));assert source_hash==writer['source_sha256']
    training={r['path']:r for r in json.loads((CORPUS/'manifest.json').read_text(encoding='utf-8'))['files'] if r['split']=='training'}
    oracle_report=ROOT/'benchmarks/results/h3-geometry-20261013T220610Z.json'
    oracle={r['path']:r for r in json.loads(oracle_report.read_text(encoding='utf-8'))['rows']}
    request=json.loads((ROOT/'output/h3-geometry-20261013T220610Z/request.json').read_text(encoding='utf-8'))
    references={r['path']:r for r in request['projects']}
    reports=[]
    for row in writer['rows']:
        assert row['path'] in training and row['source_sha256']==training[row['path']]['sha256']
        if row['status']!='written':continue
        payload_bytes=(ROOT/row['payload_path']).read_bytes();assert sha256(payload_bytes).hexdigest()==row['payload_sha256']
        payload=json.loads(payload_bytes);project=references[row['path']]
        scene_bytes=(ROOT/project['scene_path']).read_bytes();assert sha256(scene_bytes).hexdigest()==project['scene_sha256']
        scene=json.loads(scene_bytes)['scene'];cache={};checks=[];expected_units={}
        shape_hashes={r['index']:r['oracle_svg_sha256'] for r in oracle[row['path']]['shapes']}
        def geometry(index):
            key=index
            if key in cache:return cache[key]
            shape=scene['shapes'][index]
            if shape['kind']=='Group':
                value=union_all([geometry(i) for i in shape['children']])
            else:
                svg=Path(project['svg_directory'])/f'{index}.svg'
                assert sha256(svg.read_bytes()).hexdigest()==shape_hashes[index]
                paths=curves(svg);images=image_corners(svg)
                closed=shape['kind'] in ['Path','Rect','Ellipse','Polygon'] and shape['paths'] and all(p['closed'] for p in shape['paths'])
                if closed:
                    value=Polygon()
                    for path in paths:
                        points=[]
                        for segment in path:
                            flat=flatten_segment(segment,.0005)
                            points.extend([[p.real,-p.imag] for p in flat])
                        if len(points)>=3:value=value.symmetric_difference(make_valid(Polygon(points)))
                else:
                    bounds=[p.bbox() for p in paths if p]
                    bounds.extend((min(p[0] for p in image),max(p[0] for p in image),min(p[1] for p in image),max(p[1] for p in image)) for image in images)
                    x0=min(b[0] for b in bounds);x1=max(b[1] for b in bounds)
                    y0=-max(b[3] for b in bounds);y1=-min(b[2] for b in bounds)
                    # The documented open-stroke collision envelope applies to
                    # both standalone and grouped shapes; reference paths stay exact.
                    cx,cy=(x0+x1)/2,(y0+y1)/2
                    dx,dy=max(.0005,(x1-x0)/2),max(.0005,(y1-y0)/2)
                    x0,x1,y0,y1=cx-dx,cx+dx,cy-dy,cy+dy
                    value=box(x0,y0,x1,y1)
            cache[key]=value
            return value
        for unit in payload['nesting']['units']:
            try:
                expected=union_all([geometry(scene['top_level'][i]) for i in unit['members']])
                actual=union_all([Polygon(p['outer'],p['holes']) for p in unit['geometry']])
                delta=actual.boundary.hausdorff_distance(expected.boundary)
                check={'unit':unit['id'],'boundary_hausdorff_mm':delta,
                       'area_difference_mm2':abs(actual.area-expected.area),'passed':delta<=.01}
                expected_units[unit['id']]=expected
            except Exception as error:check={'unit':unit['id'],'passed':False,'error':str(error)}
            checks.append(check)
        placements=[]
        for sheet in payload['files']:
            placed=[];maximum_overlap=0.0;maximum_outside=0.0;complete=True
            for p in sheet['placements']:
                if p['unit'] not in expected_units:complete=False;continue
                import math
                t=p['transform'];s,c=math.sin(t['rotation_radians']),math.cos(t['rotation_radians']);m=-1 if t['mirrored'] else 1
                shape=affine_transform(expected_units[p['unit']],[m*c,-s,m*s,c,*t['translation']])
                maximum_outside=max(maximum_outside,shape.difference(box(0,0,payload['width_mm'],payload['height_mm'])).area)
                for prior in placed:maximum_overlap=max(maximum_overlap,shape.intersection(prior).area)
                placed.append(shape)
            placements.append({'sheet':sheet['sheet'],'reference_units':len(placed),'maximum_overlap_mm2':maximum_overlap,
                'maximum_outside_mm2':maximum_outside,'passed':complete and maximum_overlap<1e-8 and maximum_outside<1e-8})
        reports.append({'path':row['path'],'units':checks,'sheets':placements,
                        'passed':all(c['passed'] for c in checks+placements)})
        print(row['path'],reports[-1]['passed'],len(checks),'units',flush=True)
    assert sources()==source_hash and sha256(Path(__file__).read_bytes()).hexdigest()==runner_hash
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    result={'date':stamp,'H3':False,'held_out_read':False,'scope':'Training independent unit geometry and diagnostic placements, not native opening or public surfaces',
        'source_sha256':source_hash,'runner_sha256':runner_hash,'writer_report':str(args.writer_report),
        'oracle_report':str(oracle_report.relative_to(ROOT)),'oracle_report_sha256':sha256(oracle_report.read_bytes()).hexdigest(),
        'cpu':8,'limit_mm':.01,'projects_passed':sum(r['passed'] for r in reports),
        'units_passed':sum(c['passed'] for r in reports for c in r['units']),
        'units_failed':sum(not c['passed'] for r in reports for c in r['units']),'rows':reports}
    output=ROOT/'benchmarks/results'/f'h3-unit-geometry-{stamp}.json'
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n');print(output)


if __name__=='__main__':main()
