"""N2 geometry comparison with the published MIT reader, training split only.

Compatibility normalization is test-only: compose group transforms into leaves,
use native world-space text caches, materialize shared resources, expand compact
linear runs and regular polygons. These are the previously native-checked N0
oracle limitations, not Nestbolt implementation code. Uncached text stays missing.
"""
import argparse
from collections import Counter
from copy import deepcopy
import ctypes
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as E

import numpy as np
from shapely import LineString, STRtree, distance, points
from svgpathtools import Path as SvgPath, Line, CubicBezier, QuadraticBezier, Arc
from maker_geometry import flatten_segment
from shop_public_reference_audit import curves, image_corners, image_difference

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def sources():
    names = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard',
                                     'crates','web/src','Cargo.toml','Cargo.lock','scripts/h2_import_audit.py'],cwd=ROOT,text=True).splitlines()
    return sha256(b''.join(n.encode()+b'\0'+(ROOT/n).read_bytes() for n in sorted(set(names)))).hexdigest()


def matrix(text):
    a,b,c,d,e,f = map(float,(text or '1 0 0 1 0 0').split())
    return np.array([[a,c,e],[b,d,f],[0,0,1]])


def normalize(source):
    root = E.fromstring(source)
    definitions = {tag: {s.get(ref): s.find(tag).text for s in root.iter()
                         if s.get(ref) is not None and s.find(tag) is not None}
                   for tag,ref in [('VertList','VertID'),('PrimList','PrimID')]}
    images = {s.get('SourceHash'):s.get('Data') for s in root.iter('Shape')
              if s.get('Type')=='Bitmap' and s.get('Data')}
    leaves = []; indices = []; omitted = []; zero_handles = []; sequence = 0
    def visit(shape, parent):
        nonlocal sequence
        index = sequence; sequence += 1
        kind = shape.get('Type'); world = parent@matrix(shape.findtext('XForm'))
        if kind == 'Group':
            for child in shape.findall('Children/Shape'):visit(child, world)
            return
        if kind == 'Text':
            backup = shape.find('BackupPath')
            if backup is None:
                omitted.append({'index':index,'reason':'uncached text; no font approximation'});return
            node = deepcopy(backup);node.tag='Shape'
            world = matrix(backup.findtext('XForm'))
        else:node = deepcopy(shape)
        if kind not in ['Text','Path','Rect','Ellipse','Polygon','Bitmap']:
            omitted.append({'index':index,'reason':f'unsupported oracle shape {kind}'});return
        xform = node.find('XForm')
        if xform is None:xform=E.SubElement(node,'XForm')
        xform.text=' '.join(format(n,'.17g') for n in [world[0,0],world[1,0],world[0,1],world[1,1],world[0,2],world[1,2]])
        for tag,ref in [('VertList','VertID'),('PrimList','PrimID')]:
            if node.find(tag) is None and node.get(ref) is not None:
                E.SubElement(node,tag).text=definitions[tag][node.get(ref)]
            node.attrib.pop(ref,None)
        if kind=='Polygon':
            n=int(node.get('N'));rx=float(node.get('Rx'));ry=float(node.get('Ry'))
            node.set('Type','Path')
            E.SubElement(node,'VertList').text=''.join(f'V{rx*math.cos(math.tau*i/n):.17g} {ry*math.sin(math.tau*i/n):.17g}' for i in range(n))
            E.SubElement(node,'PrimList').text='LineClosed'
        if kind=='Bitmap' and not node.get('Data'):
            node.set('Data',images[node.get('SourceHash')])
        verts=node.find('VertList');prims=node.find('PrimList')
        if verts is not None:
            # Native SVGs lb-02..05 independently confirm that a missing zero
            # component is not the lone c0x1/c1x1 absent-handle sentinel.
            pattern=r'([-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?)'
            changed=False
            used={(int(a),'c0') for a,b in re.findall(r'B(\d+)\s+(\d+)',prims.text or '')} if prims is not None else set()
            if prims is not None:used.update((int(b),'c1') for a,b in re.findall(r'B(\d+)\s+(\d+)',prims.text or ''))
            vertex_index=-1
            def fill_zeros(match):
                nonlocal changed,vertex_index
                vertex_index+=1
                text=match.group(0)
                for h in ['c0','c1']:
                    x=re.search(h+'x'+pattern,text);y=re.search(h+'y'+pattern,text)
                    if x and not y and float(x.group(1))!=1:
                        text=text[:x.end()]+h+'y0'+text[x.end():];changed |= (vertex_index,h) in used
                    elif y and not x:
                        text=text[:y.start()]+h+'x0'+text[y.start():];changed |= (vertex_index,h) in used
                return text
            verts.text=re.sub(r'V[^V]*',fill_zeros,verts.text or '')
            if changed:zero_handles.append(index)
        if verts is not None and prims is not None and (prims.text or '').strip() in ['LineClosed','LineOpen']:
            n=(verts.text or '').count('V');closed=prims.text.strip()=='LineClosed'
            prims.text=''.join(f'L{i} {i+1}' for i in range(n-1))+(f'L{n-1} 0' if closed and n else '')
        leaves.append(node);indices.append(index)
    for shape in root.findall('Shape'):visit(shape,np.identity(3))
    for shape in root.findall('Shape'):root.remove(shape)
    root.extend(leaves)
    return E.tostring(root,encoding='unicode'),indices,omitted,zero_handles


def product_paths(shape):
    result=[]
    for item in shape['paths']:
        value=item['curve'];current=complex(*value['start']);segments=[]
        for s in value['segments']:
            kind=s['kind']
            if kind=='line':segment=Line(current,complex(*s['to']))
            elif kind=='quad':segment=QuadraticBezier(current,complex(*s['control']),complex(*s['to']))
            elif kind=='cubic':segment=CubicBezier(current,*map(lambda p:complex(*p),s['controls']),complex(*s['to']))
            elif kind=='arc':
                center=complex(*s['center']);rx,ry=s['radii'];rotation=s['rotation']
                def at(t):return center+complex(math.cos(rotation),math.sin(rotation))*complex(rx*math.cos(t),ry*math.sin(t))
                count=max(1,math.ceil(abs(s['sweep'])/(math.pi/2)))
                for i in range(count):
                    a=s['start']+s['sweep']*i/count;b=s['start']+s['sweep']*(i+1)/count
                    segments.append(Arc(at(a),complex(rx,ry),math.degrees(rotation),False,s['sweep']>0,at(b)))
                current=segments[-1].end;continue
            else:raise ValueError(kind)
            segments.append(segment);current=segment.end
        if segments:result.append(SvgPath(*segments))
    return result


def geometry(paths, flip=False):
    lines=[];samples=[]
    point=lambda z:(z.real,-z.imag if flip else z.imag)
    for p in paths:
        if not p or p.length()==0:continue
        vertices=[]
        for s in p:vertices.extend(flatten_segment(s,.0005)[:-1])
        vertices.append(p.end)
        lines.append(LineString([point(z) for z in vertices]))
        samples.extend(point(p.point(t)) for t in np.linspace(0,1,64))
    return lines,samples


def sampled(source, target):
    if not source and not target:return 0.0
    if not source or not target:return None
    ps=points(source);near=STRtree(target).nearest(ps)
    return float(np.max(distance(ps,np.asarray(target,dtype=object)[near])))


def compare(shape, svg, reference_override=None):
    actual=product_paths(shape);reference=curves(svg) if reference_override is None else reference_override
    al,ap=geometry(actual,True);bl,bp=geometry(reference)
    ab=sampled(ap,bl);ba=sampled(bp,al)
    corners=shape['bitmap_corners']
    actual_images=[[[x,-y] for x,y in corners]] if corners else []
    reference_images=image_corners(svg) if reference_override is None else []
    image_delta=image_difference(actual_images,reference_images)
    boxes=[p.bbox() for p in reference if p]
    boxes.extend([(min(p[0] for p in c),max(p[0] for p in c),min(p[1] for p in c),max(p[1] for p in c)) for c in reference_images])
    rb=[min(b[0] for b in boxes),-max(b[3] for b in boxes),max(b[1] for b in boxes),-min(b[2] for b in boxes)] if boxes else None
    pb=shape['bounds_mm']
    bbox_delta=max(abs(a-b) for a,b in zip(pb,rb)) if pb and rb else 0 if pb==rb else None
    matches=len(actual)==len(reference)
    return {'paths':len(actual),'oracle_paths':len(reference),'path_counts_match':matches,
            'product_to_oracle_mm':ab,'oracle_to_product_mm':ba,'bbox_difference_mm':bbox_delta,
            'image_corner_difference_mm':image_delta,
            'passed':matches and all(v is not None and v<=.01 for v in [ab,ba,bbox_delta,image_delta])}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('reader_report',type=Path);args=parser.parse_args()
    # One CCD0 physical core; child Node inherits it. No other benchmark runner
    # is active while this comparison runs.
    kernel=ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype=ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(),1<<8), 'Cannot pin the geometry comparison to CCD0'
    reader=json.loads(args.reader_report.read_text(encoding='utf-8'))
    manifest_bytes=(CORPUS/'manifest.json').read_bytes()
    training={r['path']:r for r in json.loads(manifest_bytes)['files'] if r['split']=='training'}
    assert all(r['path'] in training for r in reader['rows'])
    assert reader['source_sha256']==sources()
    scripts=[Path(__file__),ROOT/'scripts/h3_geometry_oracle.mjs']
    hashes={p.name:sha256(p.read_bytes()).hexdigest() for p in scripts}
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work=ROOT/'output'/f'h3-geometry-{stamp}';work.mkdir(exist_ok=False)
    projects=[]
    for i,row in enumerate(reader['rows']):
        if row['status']!='parsed':continue
        source=(CORPUS/row['path']).read_bytes()
        assert sha256(source).hexdigest()==training[row['path']]['sha256']==row['source_sha256']
        xml,indices,omitted,zero_handles=normalize(source)
        case=work/f'{i:03}';case.mkdir();normalized=case/'normalized.lbrn2'
        normalized.write_text(xml,encoding='utf-8',newline='\n')
        projects.append({'path':row['path'],'scene_path':row['scene_path'],'scene_sha256':row['scene_sha256'],
                         'normalized_xml':str(normalized),'svg_directory':str(case/'svg'),'shape_indices':indices,'omitted':omitted,'zero_handle_shapes':zero_handles})
    request={'projects':projects,'oracle_report':str(work/'oracle-report.json')};write_json(work/'request.json',request)
    subprocess.run(['node',str(ROOT/'scripts/h3_geometry_oracle.mjs'),str(work/'request.json')],cwd=ROOT,check=True)
    oracle={r['path']:r for r in json.loads((work/'oracle-report.json').read_text(encoding='utf-8'))['reports']}
    reports=[]
    for project in projects:
        scene_bytes=(ROOT/project['scene_path']).read_bytes();assert sha256(scene_bytes).hexdigest()==project['scene_sha256']
        scene=json.loads(scene_bytes)['scene'];row={'path':project['path'],'oracle':oracle[project['path']], 'omitted':project['omitted'],'shapes':[],'native_zero_handle_checks':[]}
        if 'error' not in row['oracle']:
            for index in project['shape_indices']:
                svg=Path(project['svg_directory'])/f'{index}.svg'
                try:comparison=compare(scene['shapes'][index],svg)
                except Exception as error:comparison={'passed':False,'error':str(error)}
                row['shapes'].append({'index':index,'kind':scene['shapes'][index]['kind'],'oracle_svg_sha256':sha256(svg.read_bytes()).hexdigest(),**comparison})
        if project['zero_handle_shapes']:
            paired=str(Path(project['path']).with_suffix('.svg')).replace('\\','/')
            assert paired in training, 'Independent native check must also be training-only'
            native=CORPUS/paired;assert sha256(native.read_bytes()).hexdigest()==training[paired]['sha256']
            native_paths=curves(native)
            for index in project['zero_handle_shapes']:
                shape=scene['shapes'][index];x0,y0,x1,y1=shape['bounds_mm']
                def delta(p):
                    a,b,c,d=p.bbox();return max(abs(a-x0),abs(b-x1),abs(-d-y0),abs(-c-y1))
                candidate=min(native_paths,key=delta)
                comparison=compare(shape,native,[candidate])
                row['native_zero_handle_checks'].append({'index':index,'native_svg':paired,'native_svg_sha256':training[paired]['sha256'],**comparison})
        row['compared_geometry_passed']='error' not in row['oracle'] and all(s['passed'] for s in row['shapes'])
        row['compared_geometry_passed'] &= all(s['passed'] for s in row['native_zero_handle_checks'])
        row['all_geometry_proved']=row['compared_geometry_passed'] and not row['omitted']
        reports.append(row);print(project['path'],row['compared_geometry_passed'],'omitted',len(row['omitted']),flush=True)
    assert reader['source_sha256']==sources()
    assert all(sha256(p.read_bytes()).hexdigest()==hashes[p.name] for p in scripts)
    result={'date':stamp,'scope':'N2 training shape comparison, published MIT oracle with documented N0 normalization; not H3 acceptance',
            'H3':False,'held_out_read':False,'reader_report':str(args.reader_report),'source_sha256':reader['source_sha256'],
            'manifest_sha256':sha256(manifest_bytes).hexdigest(),'scripts_sha256':hashes,
            'oracle':'lbrn2-to-svg@0.5.3','samples_per_contour':64,'flatten_tolerance_mm':.0005,'limit_mm':.01,'cpu':8,
            'projects_compared_geometry_passed':sum(r['compared_geometry_passed'] for r in reports),
            'projects_all_geometry_proved':sum(r['all_geometry_proved'] for r in reports),
            'shapes_passed':sum(s['passed'] for r in reports for s in r['shapes']),
            'shapes_failed':sum(not s['passed'] for r in reports for s in r['shapes']),
            'shapes_omitted':sum(len(r['omitted']) for r in reports),'rows':reports}
    target=ROOT/'benchmarks/results'/f'h3-geometry-{stamp}.json';write_json(target,result)
    print(str(target))


if __name__=='__main__':main()
