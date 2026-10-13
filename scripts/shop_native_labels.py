"""N0 native-project labels from paired native SVG exports and XML reading.

All 15 exports were reviewed with Inkscape. The construction recipe separates
the two source copies and feature coupon, so their membership is independently
recoverable from the native SVG, without implementing a LightBurn path reader.
The five malformed legacy exports are negative fixtures; their intended shape
labels come from their paired ordinary DXF, never from a claimed successful read.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as E
import numpy as np
from svgpathtools import Document
from svgpathtools.parser import parse_transform
from shop_reference_labels import CORPUS, ROOT, write_json


def main():
    if (CORPUS/'manifest.json').exists(): raise ValueError('Authoring ended at H1 freeze')
    manifest=json.loads((CORPUS/'manifest.draft.json').read_text(encoding='utf-8'))
    native=[r for r in manifest['files'] if r['set']=='lightburn-native']
    by_path={r['path']:r for r in native}
    recipe=json.loads((CORPUS/'native/recipe.json').read_text(encoding='utf-8'))
    by_id={r['id']:r for r in recipe['designs']}
    audit=json.loads((ROOT/'benchmarks/results/n0-native-corrected-20261013.json').read_text(encoding='utf-8'))
    reports={r['id']:r for r in audit['files']}
    completed=[]
    for index,row in enumerate(native):
        file=Path(row['path']); stem=file.stem; key=f'N{index:02}'
        if file.suffix=='.lbrn2':
            root=E.parse(CORPUS/row['path']).getroot(); tops=root.findall('Shape')
            assert len(tops)==4 and tops[0].get('Type')=='Group' and tops[1].get('Type')=='Rect'
            assert tops[1].get('CutIndex')=='30'
            coupon_x=float(tops[0].findtext('XForm').split()[4])
            paired=by_path['native/'+stem+'.svg']
            svgdoc=Document(str(CORPUS/paired['path']))
            unit_boxes=[[],[],[]]
            def add(box):
                # Native SVG is flattened into world-space shape transforms.
                # Centrelines use mm and the SVG y-down convention.
                x0,x1,y0,y1=box; mid=(x0+x1)/2
                unit=0 if mid>=coupon_x else 1 if mid<500 else 2
                unit_boxes[unit].append([x0,-y1,x1,-y0])
            for p in svgdoc.paths():
                if not p: continue
                style=p.element.get('style','')
                if '#f36926' in style: continue  # fixed T1, not a movable unit
                add(p.bbox())
            for e in svgdoc.root.findall('{http://www.w3.org/2000/svg}image'):
                x,y,w,h=[float(e.get(k)) for k in ['x','y','width','height']]
                matrix=parse_transform(e.get('transform'))
                points=[matrix@np.array([px,py,1]) for px,py in [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]]
                add([min(p[0] for p in points),max(p[0] for p in points),min(p[1] for p in points),max(p[1] for p in points)])
            source=by_id[stem]['source']
            source_row=next(r for r in manifest['files'] if r['path']==source)
            source_label=json.loads((CORPUS/source_row['label']).read_text(encoding='utf-8'))
            source_holes=sum(p['holes'] for p in source_label['cut_parts'])
            parts=[]
            for i,(boxes,top) in enumerate(zip(unit_boxes,[tops[0],tops[2],tops[3]])):
                assert boxes
                b=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
                parts.append({'outer_bounds_mm':b,'outer_size_mm':[b[2]-b[0],b[3]-b[1]],
                              'holes':2 if i==0 else source_holes,
                              'unit_type':'rigid_group' if top.get('Type')=='Group' else 'closed_shape',
                              'top_level_shape_indices':[[0],[2],[3]][i],
                              'bounds_include_engraving_images_and_text':i==0})
            label={'schema_version':1,'file':row['path'],'sha256':row['sha256'],
                   'licence':row['licence'],'cut_parts':parts,'cut_layers':[0,1],
                   'cut_colors':['#000000','#0000ff'],'import_options':{},
                   'default_failure':None,'expected_warnings':[],
                   'geometry_tolerance_mm':.002,
                   'fixed_shapes':[{'top_level_shape_index':1,'cut_layer':30,'type':'Tool',
                                    'outer_bounds_mm':[1400,13,1452,39],'every_sheet':True}],
                   'layer_kerf_mm':{'0':.2},
                   'derivation':{'method':'Agent review of paired native SVG rendered by Inkscape, source design labels, the native GUI construction recipe and native XML top-level groups/layers. Bounds from analytic SVG paths plus all three native-exported bitmap rectangles; no Nestbolt or LightBurn path reader used.',
                                 'review_id':key,'render':paired['reference_render']['path'],
                                 'render_sha256':paired['reference_render']['sha256'],
                                 'paired_native_svg':paired['path'],'paired_native_svg_sha256':paired['sha256'],
                                 'source_label':source_row['label'],
                                 'membership':'Coupon=top-level Shape 0; T1=Shape 1 fixed; source copies=Shapes 2 and 3. Group children form one rigid nesting unit even when disconnected.'}}
            row['reference_render']=paired['reference_render']
        elif '-lines' in stem:
            design=stem.removesuffix('-lines'); paired=by_path['native/'+design+'.dxf']
            label=deepcopy(json.loads((CORPUS/paired['label']).read_text(encoding='utf-8')))
            error=reports[design]['lines_dxf']
            assert not error['parses'] and 'POLYLINE or SEQEND' in error['error']
            label.update(file=row['path'],sha256=row['sha256'],negative_fixture=True,
                expected_failure='Malformed legacy POLYLINE/SEQEND records from LightBurn Convert Arcs to Lines. Reject clearly; suggest Export Arcs, Modern DXF or SVG.',
                default_failure='Malformed legacy POLYLINE/SEQEND records; export again with Export Arcs, Modern DXF or SVG.',
                expected_warnings=['malformed_polyline_records'],
                cut_parts_meaning='Intended paired-project cut parts only. The malformed file is a negative fixture and does not earn a successful-import result.')
            label['derivation']={'method':'Native GUI export with Convert Arcs to Lines; raw DXF record inventory and independent ezdxf failure. Intended contours/bounds from paired normal DXF and its reviewed render. No fabricated render or successful parse of malformed bytes.',
                                 'review_id':key,'paired_dxf':paired['path'],'paired_dxf_sha256':paired['sha256'],
                                 'render':paired['reference_render']['path'],'render_sha256':paired['reference_render']['sha256'],
                                 'independent_reader_error':error['error'],'raw_entity_markers':error['raw_entity_markers']}
            row['reference_render']=paired['reference_render']
        else: continue
        relative='labels/native/'+key+'.json'
        write_json(CORPUS/relative,label);row['label']=relative
        row['label_sha256']=sha256((CORPUS/relative).read_bytes()).hexdigest()
        completed.append(row['path'])
    write_json(CORPUS/'manifest.draft.json',manifest)
    print(json.dumps({'project_and_negative_labels':len(completed),'native_labels':sum(bool(r['label']) for r in native),'H1':False}))


if __name__=='__main__':main()
