"""Independent line-only SVG audit for the native H5 comparator export.

Uses original prepared source rings and the saved native rigid placements.
No Nestbolt importer, exporter or common-line detector is used by this oracle.
"""
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from shapely.geometry import LineString
from shapely.ops import unary_union
from svgpathtools import Line, parse_path

IDENTITY=(1.,0.,0.,1.,0.,0.)
TOLERANCE_MM=0.001


def multiply(a,b):
    return (a[0]*b[0]+a[2]*b[1], a[1]*b[0]+a[3]*b[1],
            a[0]*b[2]+a[2]*b[3], a[1]*b[2]+a[3]*b[3],
            a[0]*b[4]+a[2]*b[5]+a[4], a[1]*b[4]+a[3]*b[5]+a[5])


def transform(text):
    result=IDENTITY
    for match in re.finditer(r'([A-Za-z]+)\s*\(([^)]*)\)',text):
        name=match[1]; values=[float(v) for v in re.split(r'[\s,]+',match[2].strip()) if v]
        if name=='matrix' and len(values)==6: current=values
        elif name=='translate' and len(values) in [1,2]: current=(1,0,0,1,values[0],values[1] if len(values)==2 else 0)
        elif name=='scale' and len(values) in [1,2]: current=(values[0],0,0,values[-1],0,0)
        elif name=='rotate' and len(values) in [1,3]:
            angle=math.radians(values[0]);c,s=math.cos(angle),math.sin(angle)
            current=(c,s,-s,c,0,0)
            if len(values)==3:
                x,y=values[1:];current=multiply((1,0,0,1,x,y),multiply(current,(1,0,0,1,-x,-y)))
        else: raise ValueError(f'Unsupported SVG transform {match[0]}')
        result=multiply(result,current)
    assert not re.sub(r'[A-Za-z]+\s*\([^)]*\)','',text).strip(' ,\t\r\n'),text
    return result


def point(matrix,p):
    x,y=p
    return (matrix[0]*x+matrix[2]*y+matrix[4],matrix[1]*x+matrix[3]*y+matrix[5])


def svg_lines(path):
    root=ET.fromstring(Path(path).read_bytes())
    width=float(root.attrib['width'].removesuffix('mm'))
    height=float(root.attrib['height'].removesuffix('mm'))
    assert root.attrib['width'].endswith('mm') and root.attrib['height'].endswith('mm')
    box=[float(v) for v in root.attrib['viewBox'].split()]
    sx,sy=width/box[2],height/box[3]
    assert math.isclose(sx,sy,rel_tol=1e-12)
    lines=[]
    def visit(element,parent):
        matrix=multiply(parent,transform(element.attrib.get('transform','')))
        tag=element.tag.split('}')[-1]
        if tag=='path':
            for segment in parse_path(element.attrib.get('d','')):
                assert isinstance(segment,Line), 'Native straight input unexpectedly exported as a curve'
                a=point(matrix,(segment.start.real,segment.start.imag));b=point(matrix,(segment.end.real,segment.end.imag))
                assert all(math.isfinite(v) for p in [a,b] for v in p)
                if a!=b: lines.append(LineString([a,b]))
        elif tag=='line':
            a=point(matrix,(float(element.attrib.get('x1',0)),float(element.attrib.get('y1',0))))
            b=point(matrix,(float(element.attrib.get('x2',0)),float(element.attrib.get('y2',0))))
            assert all(math.isfinite(v) for p in [a,b] for v in p)
            if a!=b:lines.append(LineString([a,b]))
        elif tag not in ['svg','g','title','desc','metadata']:
            raise ValueError(f'Unsupported exported element {tag}')
        for child in element:visit(child,matrix)
    visit(root,(sx,0,0,sy,-box[0]*sx,-box[1]*sy))
    assert lines
    return lines,{'width_mm':width,'height_mm':height,'mm_per_native_unit':sx}


def expected_lines(prepared,native,bounds):
    lines=[];height=0
    assert len(native['placements'])==len(bounds)
    for sheet,bound in zip(native['placements'],bounds):
        origin=(-bound['x'],height-bound['y'])
        for placed in sheet['sheetplacements']:
            angle=math.radians(placed['rotation']);c,s=math.cos(angle),math.sin(angle)
            matrix=(c,s,-s,c,placed['x']+origin[0],placed['y']+origin[1])
            source=prepared['imports'][placed['source']]
            assert source['kind']=='part'
            for ring in source['source_rings']:
                for a,b in zip(ring,ring[1:]+ring[:1]):
                    a,b=point(matrix,a),point(matrix,b)
                    if a!=b:lines.append(LineString([a,b]))
        height+=bound['height']
    assert lines
    return lines


def audit(folder,prepared,raw):
    folder=Path(folder);native=raw['last']['native'];proof=raw['cut_exports']
    assert proof['selected_candidate']==native and not proof['network_conversion']
    expected=expected_lines(prepared,native,proof['sheet_bounds'])
    source=unary_union(expected);total=sum(l.length for l in expected)
    out={'tolerance_mm':TOLERANCE_MM,'source_cut_length_mm':total,'exports':{}}
    for kind in ['unmerged','merged']:
        lines,dimensions=svg_lines(folder/f'cuts-{kind}.svg')
        assert abs(dimensions['mm_per_native_unit']-1)<1e-12
        drawn=unary_union(lines)
        extra=drawn.difference(source.buffer(TOLERANCE_MM)).length
        missing=source.difference(drawn.buffer(TOLERANCE_MM)).length
        assert extra<1e-7 and missing<1e-7,(kind,extra,missing)
        length=sum(l.length for l in lines)
        out['exports'][kind]={'length_mm':length,'segments':len(lines),'extra_length_mm':extra,
                              'missing_length_mm':missing,**dimensions}
    unmerged=out['exports']['unmerged']['length_mm'];merged=out['exports']['merged']['length_mm']
    assert abs(unmerged-total)<1e-7*max(1,total)
    assert merged<=unmerged+1e-7*max(1,total)
    out.update(native_merged_length_mm=proof['native_merged_length'],
               export_saved_length_mm=unmerged-merged,export_saved_fraction=(unmerged-merged)/unmerged)
    return out
