"""Compare adapted package reference curves against independent native SVGs."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as E
import numpy as np
from shapely import LineString, MultiLineString, points, distance, STRtree
from svgpathtools import Document
from svgpathtools.parser import parse_transform
from maker_geometry import flatten_segment
from shop_reference_labels import ROOT, CORPUS, render, write_json

BASE=ROOT/'output/shop-public-native'


def curves(path):
    if path.stat().st_size==0:return []
    return [s for p in Document(str(path)).paths() for s in p.continuous_subpaths() if s]


def geometry(paths):
    lines=[]; samples=[]
    for p in paths:
        pts=[]
        for seg in p:pts.extend(flatten_segment(seg,.0005)[:-1])
        pts.append(p.end)
        line=LineString([(z.real,z.imag) for z in pts])
        if line.length:lines.append(line)
        samples.extend([(p.point(t).real,p.point(t).imag) for t in np.linspace(0,1,65)])
    return lines,samples


def sampled_distance(source,target_lines):
    if not source and not target_lines:return 0
    if not source or not target_lines:return None
    ps=points(source);tree=STRtree(target_lines);near=tree.nearest(ps)
    return float(np.max(distance(ps,np.asarray(target_lines,dtype=object)[near])))


def image_corners(path):
    if not path.stat().st_size:return []
    corners=[]
    def visit(node,parent=np.identity(3)):
        world=parent@parse_transform(node.get('transform'))
        if node.tag.endswith('}image'):
            x,y,w,h=[float(node.get(k)) for k in ['x','y','width','height']]
            corners.append([(world@np.array([px,py,1]))[:2].tolist()
                for px,py in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]])
        for child in node:visit(child,world)
    visit(E.parse(path).getroot())
    return corners


def image_difference(a,b):
    if len(a)!=len(b):return None
    if not a:return 0
    from scipy.spatial import cKDTree
    aa=np.array(a).reshape((-1,2));bb=np.array(b).reshape((-1,2))
    return float(max(cKDTree(aa).query(bb)[0].max(),cKDTree(bb).query(aa)[0].max()))


def main():
    collection=json.loads((BASE/'collection.json').read_text(encoding='utf-8'))
    reports=[]
    for row in collection['rows']:
        key=row['id'];native=BASE/(key+'.svg');adapted=BASE/'per-shape'/(key+'-native-visible.svg')
        a=curves(native);b=curves(adapted);al,ap=geometry(a);bl,bp=geometry(b)
        ab=sampled_distance(ap,bl);ba=sampled_distance(bp,al)
        boxes=lambda ps:[p.bbox() for p in ps]
        def bounds(ps):
            bs=boxes(ps)
            return [min(b[0] for b in bs),min(b[2] for b in bs),max(b[1] for b in bs),max(b[3] for b in bs)] if bs else None
        aa,bb=bounds(a),bounds(b)
        delta=max(abs(x-y) for x,y in zip(aa,bb)) if aa and bb else 0 if aa==bb else None
        ai,bi=image_corners(native),image_corners(adapted);image_delta=image_difference(ai,bi)
        report={'id':key,'native_svg_sha256':sha256(native.read_bytes()).hexdigest(),
                'adapted_oracle_svg_sha256':sha256(adapted.read_bytes()).hexdigest(),
                'native_curve_subpaths':len(a),'oracle_curve_subpaths':len(b),
                'native_bounds_mm':aa,'oracle_bounds_mm':bb,'bbox_difference_mm':delta,
                'native_to_oracle_sample_distance_mm':ab,'oracle_to_native_sample_distance_mm':ba,
                'native_image_count':len(ai),'oracle_image_count':len(bi),
                'image_corner_difference_mm':image_delta,
                'image_reference_agrees':image_delta is not None and image_delta<=.01,
                'vector_reference_agrees':all(v is not None and v<=.01 for v in [ab,ba,delta])}
        reports.append(report); print(key,report['vector_reference_agrees'],delta,ab,ba,flush=True)
    write_json(BASE/'reference-audit.json',{'scope':'N0 compatibility reference versus independent native SVG, not an H3 product check',
        'samples_per_subpath':65,'target_flattening_mm':.0005,'limit_mm':.01,'rows':reports})
    # Rendering uses the native SVG, never the adapted oracle, except the
    # native exporter produced zero bytes for the known empty fixture L33.
    def draw(row):
        key=row['id'];source=BASE/(key+'.svg');target=BASE/(key+'.png')
        if source.stat().st_size==0:source=BASE/'per-shape'/(key+'-all.svg')
        try:
            if not target.exists():render(source,target)
            return {'id':key,'source':str(source.relative_to(ROOT)),'png':str(target.relative_to(ROOT))}
        except Exception as ex:return {'id':key,'error':str(ex)}
    with ThreadPoolExecutor(max_workers=4) as pool:renders=list(pool.map(draw,collection['rows']))
    write_json(BASE/'renders.json',renders)
    print('Rendered',sum('error' not in r for r in renders),'of',len(renders))
    if not all(r['vector_reference_agrees'] and r['image_reference_agrees'] for r in reports):raise SystemExit(1)


if __name__=='__main__':main()
