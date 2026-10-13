"""Pre-freeze public-project worksheet using native-validated reference SVGs.

This authors expectations without calling Nestbolt. Original XML supplies
membership and layer state, analytic SVG paths supply bounds, and GEOS supplies
topology. Finalization requires separately recorded visual-review decisions.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as E
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely import Polygon, box, make_valid
from shapely.ops import unary_union
from shop_public_reference_audit import BASE, curves, image_corners
from shop_reference_labels import ROOT, CORPUS, topology, write_json
from maker_geometry import flatten_segment


def leaves(shape):
    if shape.get('Type')=='Group':
        for s in shape.findall('Children/Shape'):yield from leaves(s)
    else:yield shape


def settings(root):
    return {(c.tag,int(c.find('index').get('Value'))):
            {'type':c.get('type'),**{n.tag:n.get('Value') for n in c if n.tag!='SubLayer'},
             'cut_sublayer':any(s.get('type')=='Cut' for s in c.findall('SubLayer'))}
            for c in root if c.tag in ['CutSetting','CutSetting_Img']}


def layer(s,cs):
    kind='CutSetting_Img' if s.get('Type')=='Bitmap' else 'CutSetting'
    return cs.get((kind,int(s.get('CutIndex','0'))),{'type':'Image' if kind.endswith('_Img') else 'Cut'})


def fixed(s,cs):
    c=layer(s,cs)
    return c['type']=='Tool' or c.get('doOutput','1')=='0'


def cutting(s,cs):
    c=layer(s,cs)
    return not fixed(s,cs) and (c['type'] in ['Cut','Scan+Cut','ScanCut'] or c.get('cut_sublayer',False))


def profile(file):
    paths=curves(file); images=image_corners(file)
    boxes=[[b[0],-b[3],b[1],-b[2]] for p in paths if p for b in [p.bbox()]]
    boxes.extend([[min(p[0] for p in v),-max(p[1] for p in v),max(p[0] for p in v),-min(p[1] for p in v)] for v in images])
    bounds=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)] if boxes else None
    network=[]; rings=[]; all_closed=bool(paths) and not images
    for p in paths:
        pts=[]
        for seg in p:pts.extend(flatten_segment(seg,.0002)[:-1])
        pts.append(p.end); pts=[(z.real,-z.imag) for z in pts]
        closed=abs(p.start-p.end)<=.005
        all_closed=all_closed and closed
        if closed:
            pts[-1]=pts[0]
            if len(pts)>=4:
                poly=make_valid(Polygon(pts))
                if not poly.is_empty:rings.append(poly)
        network.append({'points':pts})
    topo=topology(network)
    # Enclosure is tested against exterior silhouettes, so an engraving may
    # occupy an interior cut hole without changing membership of its parent.
    outline=unary_union([Polygon(p.exterior) for r in rings for p in
                         ([r] if r.geom_type=='Polygon' else list(r.geoms)) if p.geom_type=='Polygon'])
    return {'bounds':bounds,'closed':all_closed,'topology':topo,'outline':outline}


def worksheet(row):
    key=row['id']; original=E.parse(CORPUS/row['source']).getroot()
    tops=original.findall('Shape');cs=settings(original); observed=[];warn=set()
    for i,s in enumerate(tops):
        ps=profile(BASE/'per-shape'/f'{key}-{i:03}.svg')
        ls=list(leaves(s));states=[fixed(x,cs) for x in ls]
        is_fixed=any(states)
        if is_fixed and not all(states):warn.add('rigid_group_contains_fixed_shapes')
        if s.get('Type')=='Group':
            cut=profile(BASE/'per-shape'/f'{key}-{i:03}-cut.svg')
            holes=sum(p['holes'] for p in cut['topology']['cut_parts'])
        else:holes=sum(p['holes'] for p in ps['topology']['cut_parts']) if ps['closed'] and s.get('Type')!='Text' else 0
        if s.get('Type') in ['Bitmap','Text']:kind='bounds_proxy'
        elif s.get('Type')=='Group':kind='rigid_group'
        else:kind='closed_shape' if ps['closed'] else 'bounds_proxy'
        observed.append({'index':i,'type':s.get('Type'),'fixed':is_fixed,'unit_type':kind,
            'bounds':ps['bounds'],'holes':holes,'profile':ps,
            'layers':sorted({int(x.get('CutIndex','0')) for x in ls}),
            'layer_types':sorted({layer(x,cs)['type'] for x in ls}),
            'cut_candidate':not is_fixed and s.get('Type') not in ['Group','Text','Bitmap'] and ps['closed'] and cutting(s,cs),
            'engraving_candidate':not is_fixed and s.get('Type')!='Group' and (s.get('Type') in ['Text','Bitmap'] or layer(s,cs)['type'] in ['Scan','Image'])})
    attached={}; candidates=[s for s in observed if s['cut_candidate']]
    for s in observed:
        if not s['engraving_candidate'] or not s['bounds']:continue
        parents=[p for p in candidates if p['index']!=s['index'] and p['profile']['outline'].buffer(.00001).covers(box(*s['bounds']))]
        if parents:
            parent=min(parents,key=lambda p:(p['profile']['outline'].area,p['index']))
            attached[s['index']]=parent['index']
            if len(parents)>1:warn.add('engraving_inside_multiple_outlines_smallest_selected')
    parts=[];fixeds=[]
    for s in observed:
        if s['fixed']:
            fixeds.append({'top_level_shape_index':s['index'],'layers':s['layers'],
                'outer_bounds_mm':s['bounds'],'every_sheet':True});continue
        if s['index'] in attached:continue
        if not s['bounds']:
            warn.add('empty_shape');continue
        b=s['bounds'];members=[s['index']]+[i for i,p in attached.items() if p==s['index']]
        parts.append({'outer_bounds_mm':b,'outer_size_mm':[b[2]-b[0],b[3]-b[1]],
            'holes':s['holes'],'unit_type':s['unit_type'],'top_level_shape_indices':members})
        if b[0]==b[2] or b[1]==b[3]:
            warn.add('zero_area_proxy');parts[-1]['degenerate_proxy']=True
    text_without_cache=sum(s.get('Type')=='Text' and s.find('BackupPath') is None for top in tops for s in leaves(top))
    if text_without_cache:warn.add('text_without_backup_path')
    if any(p['unit_type']=='bounds_proxy' for p in parts):warn.add('bounding_rectangle_proxy')
    if fixeds:warn.add('fixed_tool_or_output_disabled_shapes')
    if not parts:warn.add('no_movable_shapes')
    if key=='L28':warn.add('missing_bezier_control_points_native_line_fallback')
    if key=='L40':warn.add('font_missing_native_backup_used')
    cuts=sorted({int(s.get('CutIndex','0')) for top in tops for s in leaves(top) if s.get('Type')!='Bitmap' and cutting(s,cs)})
    return {'id':key,'file':row['source'],'cut_parts':parts,'fixed_shapes':fixeds,
        'cut_layers':cuts,'expected_warnings':sorted(warn),
        'top_level_shape_count':len(tops),'top_level_types':dict(Counter(s.get('Type') for s in tops)),
        'text_without_backup_count':text_without_cache,
        'layers':[{'element':tag,'index':idx,**s} for (tag,idx),s in cs.items()],
        'shapes':[{k:v for k,v in s.items() if k not in ['profile','cut_candidate','engraving_candidate']} for s in observed]}


def contacts(rows):
    for start in range(0,len(rows),12):
        fig,axes=plt.subplots(4,3,figsize=(18,18),dpi=110)
        for ax,row in zip(axes.flat,rows[start:start+12]):
            ax.imshow(plt.imread(BASE/(row['id']+'.png')))
            ax.set_title(f'{row["id"]} {Path(row["file"]).name[:36]}\n{len(row["cut_parts"])} movable / {len(row["fixed_shapes"])} fixed; holes '+str([p['holes'] for p in row['cut_parts']])[:70],fontsize=9)
            ax.axis('off')
        for ax in list(axes.flat)[len(rows[start:start+12]):]:ax.axis('off')
        fig.tight_layout();fig.savefig(BASE/f'contact-{start//12+1:02}.png');plt.close(fig)


def finalize(rows):
    decisions=json.loads((CORPUS/'labels/public-review-decisions.json').read_text(encoding='utf-8'))
    reviewed={r[0]:r[1:] for r in decisions['rows']}
    collection=json.loads((BASE/'collection.json').read_text(encoding='utf-8'))
    collected={r['id']:r for r in collection['rows']}
    manifest=json.loads((CORPUS/'manifest.draft.json').read_text(encoding='utf-8'))
    entries={r['path']:r for r in manifest['files']}
    palette=json.loads(Path('C:/Program Files/LightBurn/palette.json').read_text(encoding='utf-8'))
    references=[]
    for row in rows:
        key=row['id']; count,fixed_count,histogram,note=reviewed[key]
        assert len(row['cut_parts'])==count and len(row['fixed_shapes'])==fixed_count,key
        assert dict(Counter(str(p['holes']) for p in row['cut_parts']))==histogram,key
        src=collected[key];entry=entries[row['file']]
        assert sha256((CORPUS/entry['path']).read_bytes()).hexdigest()==src['source_sha256']==entry['sha256']
        ref={**src,'files':[]}
        for suffix in ['.lbrn2','.svg','.png']:
            relative='references/public/'+key+suffix;dest=CORPUS/relative
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(BASE/(key+suffix),dest)
            ref['files'].append({'path':relative,'sha256':sha256(dest.read_bytes()).hexdigest(),
                'licence':entry['licence'],'derived_from':entry['path'],
                'licence_evidence':entry['licence_evidence'],
                'modification':'Native 2.1.01 Save As / SVG export; Inkscape PNG render. Original corpus project is unchanged.'})
        render_ref=ref['files'][2]
        label={'schema_version':1,'file':entry['path'],'sha256':entry['sha256'],
            'licence':entry['licence'],'cut_parts':row['cut_parts'],
            'cut_parts_meaning':'Movable nesting units under PLAN_V1_1 section 3. Group cut holes exclude Scan artwork and Text. Exact degenerate open-path bounds remain explicit; no silent geometry inflation.',
            'cut_layers':row['cut_layers'],'cut_colors':['#'+palette[i][-6:] for i in row['cut_layers']],
            'import_options':{},'default_failure':None,'expected_warnings':row['expected_warnings'],
            'geometry_tolerance_mm':.002,'fixed_shapes':row['fixed_shapes'],
            'derivation':{'method':decisions['method']+' Bounds from the unmodified published lbrn2-to-svg@0.5.3 on documented compatibility inputs; all exported vectors and image corners independently validated against native SVG. Source XML supplies layer state and top-level identity; GEOS supplies cut-hole topology. No Nestbolt importer used.',
                'review_id':key,'review_note':note,'render':render_ref['path'],'render_sha256':render_ref['sha256'],
                'native_reference_project':ref['files'][0]['path'],'native_reference_svg':ref['files'][1]['path'],
                'reference_audit':'references/public/reference-audit.json',
                'text_reference_caveat':'Native-generated text caches are reference evidence only; original missing-cache state remains a warning.',
                'empty_render_diagnostic':key=='L33'},
            'source_observations':{k:row[k] for k in ['top_level_shape_count','top_level_types','text_without_backup_count','layers','shapes']}}
        if not count:label['expected_layout_failure']='No movable shapes; enable a cutting/output layer or add geometry. Reader/no-op preservation must still succeed.'
        if 'zero_area_proxy' in row['expected_warnings']:
            label['expected_layout_failure']='Axis-aligned open paths have zero-area bounds; group them with their intended part or explicitly choose a nonzero proxy. Never silently omit them.'
        relative='labels/public/'+key+'.json';write_json(CORPUS/relative,label)
        entry.update(label=relative,label_sha256=sha256((CORPUS/relative).read_bytes()).hexdigest(),
            reference_render={k:render_ref[k] for k in ['path','sha256','licence']},
            native_reference_project=ref['files'][0]['path'])
        references.append(ref)
    for name in ['reference-audit.json','reference-audit-before-group-normalization.json','L40-missing-font.png']:
        shutil.copyfile(BASE/name,CORPUS/'references/public'/name)
    write_json(CORPUS/'references/public/manifest.json',{
        'writer':collection['writer'],'recorded_at':collection['recorded_at'],
        'purpose':'Auxiliary native geometry/label evidence. Does not increase real/native/public corpus counts.',
        'no_op_round_trip_evidence':False,
        'empty_L33':'Native SVG is zero bytes; PNG renders the independent converter diagnostic No shapes found.',
        'originals_unchanged':True,'rows':references,
        'metadata_licence':'MIT for original Nestbolt review/report metadata; per-file derived geometry retains its source licence.',
        'font_warning_image':{'path':'references/public/L40-missing-font.png','licence':'MIT','derived_from':collected['L40']['source']}})
    write_json(CORPUS/'manifest.draft.json',manifest)
    print('Finalized public labels:',len(rows))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--contacts-only',action='store_true');parser.add_argument('--finalize',action='store_true');args=parser.parse_args()
    if (CORPUS/'manifest.json').exists():raise ValueError('N0 authoring ended at freeze')
    audit=json.loads((BASE/'reference-audit.json').read_text(encoding='utf-8'))
    assert all(r['vector_reference_agrees'] and r['image_reference_agrees'] for r in audit['rows'])
    if args.contacts_only or args.finalize:rows=json.loads((BASE/'label-worksheet.json').read_text(encoding='utf-8'))
    else:
        collection=json.loads((BASE/'collection.json').read_text(encoding='utf-8'))
        rows=[]
        for row in collection['rows']:
            w=worksheet(row);rows.append(w)
            print(w['id'],len(w['cut_parts']),len(w['fixed_shapes']),[p['holes'] for p in w['cut_parts']],w['expected_warnings'],flush=True)
        write_json(BASE/'label-worksheet.json',rows)
    if args.finalize:finalize(rows)
    else:contacts(rows)


if __name__=='__main__':main()
