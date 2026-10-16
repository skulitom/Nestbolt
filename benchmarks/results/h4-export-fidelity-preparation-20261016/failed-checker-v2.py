"""Independently check exact placed Bezier/line geometry in saved H4 cutting files.

No search, export regeneration or production code is called. SVG uses svgpathtools;
DXF uses ezdxf. Matching Bezier control points bound the entire curve difference
because Bernstein basis weights are nonnegative and sum to one. The existing
0.01 mm fidelity limit is unchanged. Only the frozen line/quad/cubic fixture is
supported; unexpected primitives or missing/extra entities fail explicitly.
"""
from collections import Counter
from hashlib import sha256
from io import BytesIO, TextIOWrapper
from itertools import zip_longest
import argparse
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
import ezdxf
from ezdxf.addons.iterdxf import single_pass_modelspace
from svgpathtools import parse_path, Line, QuadraticBezier, CubicBezier

LIMIT_MM=0.01
NS='{http://www.w3.org/2000/svg}'

def transformed(point, placement, height=None):
    t=placement['transform']
    x,y=point
    if t['mirrored']: x=-x
    c,s=math.cos(t['rotation_radians']),math.sin(t['rotation_radians'])
    x,y=c*x-s*y+t['translation'][0],s*x+c*y+t['translation'][1]
    return complex(x,height-y if height is not None else y)

def source_segments(part, placement, height=None):
    for contour in [part['outer'],*part['holes']]:
        previous=contour['start']
        assert previous==contour['segments'][-1]['to'], 'Fixture contour must close exactly'
        for segment in contour['segments']:
            kind=segment['kind']
            if kind=='line': points=[previous,segment['to']]
            elif kind=='quad': points=[previous,segment['control'],segment['to']]
            elif kind=='cubic': points=[previous,*segment['controls'],segment['to']]
            else: raise AssertionError('Unexpected source primitive: '+kind)
            yield kind,tuple(transformed(p,placement,height) for p in points)
            previous=segment['to']

def compare(expected, actual):
    count=Counter();maximum=0.0
    for before,after in zip_longest(expected,actual):
        assert before is not None and after is not None, 'Missing/extra exported primitive'
        kind,points=before
        assert kind==after[0] and len(points)==len(after[1]), 'Primitive type or degree changed'
        error=max(abs(a-b) for a,b in zip(points,after[1]))
        assert math.isfinite(error) and error<=LIMIT_MM, f'Curve control error {error} mm exceeds {LIMIT_MM}'
        maximum=max(maximum,error);count[kind]+=1
    return count,maximum

def svg_segments(path):
    for segment in parse_path(path):
        if isinstance(segment,Line): yield 'line',(segment.start,segment.end)
        elif isinstance(segment,QuadraticBezier): yield 'quad',(segment.start,segment.control,segment.end)
        elif isinstance(segment,CubicBezier): yield 'cubic',(segment.start,segment.control1,segment.control2,segment.end)
        else: raise AssertionError('Unexpected SVG primitive: '+type(segment).__name__)

def svg_check(archive,name,parts,placements,height):
    expected={p['part_id']+'#'+str(p['copy_index']):p for p in placements}
    assert len(expected)==len(placements)
    counts=Counter();maximum=0.0;groups=[];paths=0
    with archive.open(name) as stream:
        for event,element in ET.iterparse(stream,events=('start','end')):
            if event=='start':
                assert 'transform' not in element.attrib, 'Unexpected additional SVG transform'
                if element.tag==NS+'g': groups.append(element.attrib.get('id'))
            else:
                if element.tag==NS+'path':
                    assert groups==['CUT'] and element.attrib.get('fill-rule')=='evenodd'
                    placement=expected.pop(element.attrib['id'])
                    c,m=compare(source_segments(parts[placement['part_id']],placement,height),svg_segments(element.attrib['d']))
                    counts.update(c);maximum=max(maximum,m);paths+=1
                elif element.tag==NS+'g': groups.pop()
                elif element.tag not in [NS+'svg',NS+'title']:
                    raise AssertionError('Unexpected SVG element: '+element.tag)
                element.clear()
    assert not expected and not groups
    return {'paths':paths,'primitives':dict(counts),'maximum_control_point_error_mm':maximum}

def dxf_entity_types(archive,name):
    section=None;last=None;counts=Counter()
    with archive.open(name) as raw,TextIOWrapper(raw,encoding='utf-8',errors='strict') as stream:
        iterator=iter(stream)
        for code in iterator:
            value=next(iterator).strip();code=int(code)
            if code==2 and last==(0,'SECTION'): section=value
            elif code==0 and value=='ENDSEC': section=None
            elif section=='ENTITIES' and code==0: counts[value]+=1
            last=(code,value)
    assert counts and set(counts)<= {'LINE','SPLINE'}, counts
    return counts

def dxf_segments(archive,name):
    with archive.open(name) as stream:
        for entity in single_pass_modelspace(stream,errors='strict'):
            assert entity.dxf.layer=='CUT' and entity.dxf.paperspace==0
            if entity.dxftype()=='LINE':
                points=[entity.dxf.start,entity.dxf.end];kind='line'
            elif entity.dxftype()=='SPLINE':
                degree=entity.dxf.degree
                assert degree in [2,3] and len(entity.control_points)==degree+1
                assert list(entity.knots)==[0.0]*(degree+1)+[1.0]*(degree+1)
                assert not list(entity.weights) and not list(entity.fit_points)
                points=entity.control_points;kind='quad' if degree==2 else 'cubic'
            else: raise AssertionError('Unexpected DXF entity: '+entity.dxftype())
            assert all(float(p[2])==0 for p in points), 'Unexpected Z coordinate'
            yield kind,tuple(complex(p[0],p[1]) for p in points)

def verify(project_zip,sheet_ids=None):
    with zipfile.ZipFile(BytesIO(project_zip)) as archive:
        assert archive.testzip() is None
        project=json.loads(archive.read('project.json'))
        parts={p['id']:p for p in project['library']['parts']}
        layout=project['result']['layout'];request=project['request']
        assert len(parts)==4 and sum(p['quantity'] for p in request['parts'])==2000
        assert len(layout['placements'])==2000 and not request.get('common_line') and not request.get('lead_in')
        sheets=layout['sheets']
        if sheet_ids is not None:
            assert set(sheet_ids)<={s['id'] for s in sheets}
            sheets=[s for s in sheets if s['id'] in sheet_ids]
        rows=[]
        for sheet in sheets:
            sid=sheet['id'];placements=[p for p in layout['placements'] if p['sheet_id']==sid]
            assert placements and all(not p['transform']['mirrored'] for p in placements)
            svg_name=f'sheets/{sid}.svg';dxf_name=f'sheets/{sid}.dxf'
            assert len(request['sheets'])==1 and sheet['stock_id']=='sheet-type-1'
            svg=svg_check(archive,svg_name,parts,placements,request['sheets'][0]['height_mm'])
            entities=dxf_entity_types(archive,dxf_name)
            expected=(s for p in placements for s in source_segments(parts[p['part_id']],p))
            counts,maximum=compare(expected,dxf_segments(archive,dxf_name))
            assert sum(counts.values())==sum(entities.values()) and dict(counts)==svg['primitives']
            rows.append({'sheet':sid,'placements':len(placements),'SVG':svg,
                'DXF':{'primitives':dict(counts),'entity_types':dict(entities),'maximum_control_point_error_mm':maximum},
                'files':{n:sha256(archive.read(n)).hexdigest() for n in [svg_name,dxf_name]}})
    return {'all_checks_pass':True,'project_zip_sha256':sha256(project_zip).hexdigest(),
        'method':'Every placed line/quadratic/cubic control point, original library and placement; independent SVG/DXF parsers; all exported primitives accounted for',
        'limit_mm':LIMIT_MM,'total_placements_checked':sum(r['placements'] for r in rows),'sheets':rows,
        'full_project_checked':sheet_ids is None,'searches_run':0,'exports_regenerated':False,
        'ezdxf_version':ezdxf.__version__}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',type=Path)
    p.add_argument('--raw-archive',type=Path)
    p.add_argument('--member',default='chrome/project.zip')
    p.add_argument('--sheet',action='append')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();assert bool(a.project)!=bool(a.raw_archive)
    assert not a.out.exists(), 'Preserve previous checks'
    if a.project: raw=a.project.read_bytes()
    else:
        with zipfile.ZipFile(a.raw_archive) as z: raw=z.read(a.member)
    result=verify(raw,a.sheet)
    a.out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'passed':True,'placements_checked':result['total_placements_checked'],'out':str(a.out)}))
