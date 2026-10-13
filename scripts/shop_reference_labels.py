"""Independent N0 label worksheet: ezdxf/Inkscape renders plus geometry reading.

This is corpus authoring, never a Nestbolt import test. Candidate topology needs
an explicit visual-review record before it can become a frozen label. All reads
occur before the new held-out split; rerunning against held-out data for tuning
is forbidden after the freeze.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from math import hypot
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

import ezdxf
from ezdxf.path import make_path
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree
from shapely import LineString, Polygon, normalize
from shapely.ops import polygonize_full, unary_union
from svgpathtools import Document
from maker_geometry import flatten_segment
from shop_sources import ROOT, CORPUS

OUT = ROOT/'output/shop-labels'
UNITS = {0:1, 1:25.4, 2:304.8, 4:1, 5:10, 6:1000}
GEOMETRY = {'LINE','ARC','CIRCLE','ELLIPSE','SPLINE','LWPOLYLINE','POLYLINE'}
SVG_NS = '{http://www.w3.org/2000/svg}'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def dxf_curves(doc, entities, frames=(), inherited='0', inherited_color=7):
    for ent in entities:
        layer = ent.dxf.layer
        if layer == '0': layer = inherited
        color = ent.dxf.get('color',256)
        if color == 256: color = abs(doc.layers.get(layer).dxf.color) if layer in doc.layers else 7
        if color == 0: color = inherited_color
        if ent.dxftype() == 'INSERT':
            yield from dxf_curves(doc, doc.blocks.get(ent.dxf.name),
                                  (*frames,ent.matrix44()),layer,color)
        elif ent.dxftype() in GEOMETRY:
            p = make_path(ent)
            pts = []
            for v in p.flattening(distance=.0002/UNITS[doc.units]):
                for frame in reversed(frames): v=frame.transform(v)
                pts.append((v.x*UNITS[doc.units],v.y*UNITS[doc.units]))
            yield {'id':ent.dxf.handle,'layer':layer,'color':color,'points':pts,
                   'type':ent.dxftype()}


def svg_length(value, default):
    if value is None: return default
    m=re.fullmatch(r'\s*([\d.eE+\-]+)(mm|cm|in|px|pt|pc)?\s*',value)
    if not m: raise ValueError('Unsupported SVG size '+value)
    return float(m[1])*{'mm':1,'cm':10,'in':25.4,'px':25.4/96,
                       'pt':25.4/72,'pc':25.4/6,None:25.4/96}[m[2]]


def svg_curves(path):
    doc=Document(str(path)); root=doc.root
    # Illustrator's standard SVG fallback is under <switch>. Select the first
    # branch that does not require a proprietary extension, as Inkscape does.
    for switch in list(root.iter(SVG_NS+'switch')):
        supported=next((c for c in switch if not c.get('requiredExtensions') and not c.get('requiredFeatures')),None)
        switch[:]=[supported] if supported is not None else []
        switch.tag=SVG_NS+'g'
    box=[float(v) for v in root.get('viewBox','').replace(',',' ').split()]
    if box:
        w=svg_length(root.get('width'),box[2]*25.4/96)
        h=svg_length(root.get('height'),box[3]*25.4/96)
        sx,sy=w/box[2],h/box[3]; ox,oy=box[:2]
        if root.get('preserveAspectRatio','xMidYMid meet') != 'none':
            # Default meet, centred viewport. Source coordinates are offset by
            # viewBox origin; centring changes location only, not outer sizes.
            sx=sy=min(sx,sy)
    else: sx=sy=25.4/96; ox=oy=0
    parents={c:p for p in root.iter() for c in p}
    css={}
    for style in root.iter(SVG_NS+'style'):
        for selector,body in re.findall(r'([^{}]+)\{([^{}]+)\}',style.text or ''):
            declarations=dict(x.split(':',1) for x in body.split(';') if ':' in x)
            for token in selector.split(','): css[token.strip()]=declarations
    for index,p in enumerate(doc.paths()):
        elem=p.element; lineage=[]; node=elem; styles={}
        while node is not None:
            lineage.append(node); node=parents.get(node)
        for node in reversed(lineage):
            styles.update({k:node.get(k) for k in ['stroke','fill','display','visibility'] if node.get(k) is not None})
            for cls in node.get('class','').split(): styles.update(css.get('.'+cls,{}))
            if node.get('id'): styles.update(css.get('#'+node.get('id'),{}))
            styles.update(dict(x.split(':',1) for x in node.get('style','').split(';') if ':' in x))
        if styles.get('display')=='none' or styles.get('visibility')=='hidden': continue
        layer=next((e.get('{http://www.inkscape.org/namespaces/inkscape}label') or e.get('id') for e in lineage[1:] if e.tag==SVG_NS+'g'),None)
        for sub_index,sub in enumerate(p.continuous_subpaths()):
            pts=[]
            for seg in sub:
                pts.extend(flatten_segment(seg,.0002/max(sx,sy))[:-1])
            if sub: pts.append(sub.end)
            color=styles.get('stroke')
            if color in (None,'none'): color=styles.get('fill','#000000')
            yield {'id':f'{elem.get("id",str(index))}:{sub_index}','layer':layer,
                   'color':color,
                   'points':[((z.real-ox)*sx,(z.imag-oy)*sy) for z in pts],
                   'type':elem.tag.split('}')[-1]}


def topology(curves, join_tolerance=.005):
    # Independent line-network reconstruction: clustered endpoints followed by
    # GEOS polygonization, rather than the product's contour importer.
    useful=[c for c in curves if len(c['points'])>=2]
    lines=[list(c['points']) for c in useful]
    if not lines: return {'cut_parts':[], 'ring_count':0, 'open_length_mm':0}
    ends=np.array([p for line in lines for p in (line[0],line[-1])])
    links=list(cKDTree(ends).query_pairs(join_tolerance))
    parent=list(range(len(ends)))
    def find(i):
        while parent[i]!=i: parent[i]=parent[parent[i]]; i=parent[i]
        return i
    for a,b in links: parent[find(b)]=find(a)
    clusters={}
    for i in range(len(ends)): clusters.setdefault(find(i),[]).append(i)
    snapped=ends.copy()
    for indices in clusters.values(): snapped[indices]=np.mean(ends[indices],axis=0)
    for i,line in enumerate(lines): line[0]=snapped[i*2]; line[-1]=snapped[i*2+1]
    merged=unary_union([LineString(line) for line in lines])
    faces,cuts,dangles,invalid=polygonize_full(merged)
    unique={}
    for face in faces.geoms:
        for ring in [face.exterior,*face.interiors]:
            p=normalize(Polygon(ring))
            if p.area>1e-8: unique[p.wkb]=p
    rings=sorted(unique.values(),key=lambda p:-p.area)
    containers=[[j for j,q in enumerate(rings[:i]) if q.contains(p)] for i,p in enumerate(rings)]
    parts=[]
    for i,p in enumerate(rings):
        if len(containers[i])%2: continue
        holes=[j for j,c in enumerate(containers) if c and c[-1]==i and len(c)%2]
        b=list(p.bounds)
        parts.append({'outer_bounds_mm':b,'outer_size_mm':[b[2]-b[0],b[3]-b[1]],
                      'holes':len(holes),'hole_bounds_mm':[list(rings[j].bounds) for j in holes]})
    return {'cut_parts':parts,'ring_count':len(rings),
            'open_length_mm':cuts.length+dangles.length,'invalid_length_mm':invalid.length,
            'endpoint_snap_limit_mm':join_tolerance,'curve_flattening_mm':.0002,
            'duplicate_or_overlapping_length_mm':sum(LineString(l).length for l in lines)-merged.length}


def render(path, target, black=False):
    if path.suffix.lower()=='.svg':
        result=subprocess.run(['C:/Program Files/Inkscape/bin/inkscape.exe',str(path),
             '--export-area-drawing','--export-width=1200','--export-background=white',
             '--export-background-opacity=1','--export-filename='+str(target)],
             capture_output=True,text=True,timeout=45)
        if result.returncode or not target.exists():
            # An empty drawing has no drawing-area dimensions. Render its page
            # to retain independent evidence of the blank source.
            result=subprocess.run(['C:/Program Files/Inkscape/bin/inkscape.exe',str(path),
                 '--export-area-page','--export-width=1200','--export-background=white',
                 '--export-background-opacity=1','--export-filename='+str(target)],
                 capture_output=True,text=True,timeout=45)
            if result.returncode or not target.exists(): raise ValueError(result.stderr)
        return 'Inkscape 1.4.4'
    doc=ezdxf.readfile(path)
    fig,ax=plt.subplots(figsize=(10,7),dpi=150)
    Frontend(RenderContext(doc),MatplotlibBackend(ax,adjust_figure=False),
             Configuration(background_policy=BackgroundPolicy.WHITE,
                           color_policy=ColorPolicy.BLACK if black else ColorPolicy.COLOR)).draw_layout(doc.modelspace(),finalize=True)
    fig.savefig(target,bbox_inches='tight',pad_inches=.03); plt.close(fig)
    return 'ezdxf 1.4.4 drawing add-on / MatplotlibBackend'


def finalize_reviewed(row, entry, decision):
    if not decision.get('reviewed'): return
    if row.get('error'): raise ValueError('Cannot approve an errored worksheet')
    parts=row['topology']['cut_parts']
    if 'expected_holes' in decision and sorted(p['holes'] for p in parts)!=sorted(decision['expected_holes']):
        raise ValueError('Review count no longer matches: '+row['id'])
    if decision.get('expected_failure') and row['topology']['open_length_mm']<1:
        raise ValueError('Negative open-geometry fixture no longer has significant open geometry')
    if row['topology']['open_length_mm']>.001 and not decision.get('open_geometry_review'):
        raise ValueError('Unreviewed open geometry: '+row['id'])
    category='real' if entry['set']=='real' else 'native'
    render_rel='renders/'+category+'/'+row['id']+'.png'
    target=CORPUS/render_rel; target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(OUT/(row['id']+'.png'),target)
    cuts=decision.get('cut_layers',list(dict.fromkeys(x['layer'] for x in row['layer_color_counts'])))
    warnings=list(decision.get('expected_warnings',[]))
    if row.get('units_code')==0: warnings.append('units_unspecified')
    if row.get('ignored_non_geometry'): warnings.append('ignored_non_geometry')
    if row['topology'].get('duplicate_or_overlapping_length_mm',0)>.001:
        warnings.append('duplicate_or_overlapping_segments')
    options={'layers':cuts} if Path(entry['path']).suffix=='.dxf' else {}
    if decision.get('cut_colors'): options['colors']=decision['cut_colors']
    if decision.get('join_tolerance_mm',.005)>.005:
        options['close_gaps_mm']=decision['join_tolerance_mm']; warnings.append('gaps_closed')
    label={'schema_version':1,'file':entry['path'],'sha256':entry['sha256'],
           'licence':entry['licence'],'cut_parts':[] if decision.get('expected_failure') else parts,'cut_layers':cuts,
           'cut_colors':decision.get('cut_colors',list(dict.fromkeys(x['color'] for x in row['layer_color_counts'] if x['layer'] in cuts))),
           'import_options':options,'default_failure':decision.get('default_failure'),
           'expected_warnings':sorted(set(warnings)),
           'geometry_tolerance_mm':max(.002,decision.get('join_tolerance_mm',0)),
           'derivation':{'method':'Agent review of ezdxf drawing add-on or Inkscape rendering and raw entity/layer/units reading; independent ezdxf/svgpathtools curves and GEOS endpoint-network polygonization. No Nestbolt importer used.',
                         'review_id':row['id'],'review_note':decision['note'],
                         'renderer':'Inkscape 1.4.4' if Path(entry['path']).suffix=='.svg' else 'ezdxf 1.4.4 drawing add-on / MatplotlibBackend',
                         'render':render_rel,'render_sha256':sha256(target.read_bytes()).hexdigest(),
                         'render_colors':'black for legibility; entity colours retained in metadata' if decision.get('black_render') else 'source colours',
                         'endpoint_snap_limit_mm':row['topology'].get('endpoint_snap_limit_mm',.005),
                         'curve_flattening_mm':.0002,
                         'units':'DXF INSUNITS honoured literally; unspecified defaults to mm' if 'units_code' in row else 'SVG root dimensions and viewBox; 96 px per inch for pixel-only artwork'},
           'source_observations':{k:row[k] for k in ['units_code','entities','ignored_non_geometry','layer_color_counts'] if k in row}}
    if decision.get('expected_failure'):
        label['expected_failure']=decision['expected_failure']
        label['negative_fixture']=True
        label['cut_parts_meaning']='No complete automatic cut job: reject with an actionable open/ambiguous-contour report. Empty output is not a successful import.'
        label['source_observations']['closed_regions_not_a_complete_cut_job']=parts
    elif not parts and decision.get('default_failure'):
        label['negative_fixture']=True
        label['expected_failure']=decision['default_failure']
        label['cut_parts_meaning']='No non-degenerate cut geometry; empty output is not a successful import.'
    label['source_observations']['open_length_mm']=row['topology']['open_length_mm']
    label['source_observations']['duplicate_or_overlapping_length_mm']=row['topology'].get('duplicate_or_overlapping_length_mm',0)
    label_rel='labels/'+category+'/'+row['id']+'.json'
    write_json(CORPUS/label_rel,label)
    entry['label']=label_rel; entry['label_sha256']=sha256((CORPUS/label_rel).read_bytes()).hexdigest()
    entry['reference_render']={'path':render_rel,'sha256':label['derivation']['render_sha256'],'licence':entry['licence']}
    row['reviewed']=True


def contacts(rows):
    for start in range(0,len(rows),12):
        fig,axes=plt.subplots(4,3,figsize=(18,18),dpi=110)
        for ax,row in zip(axes.flat,rows[start:start+12]):
            target=OUT/(row['id']+'.png')
            if target.exists(): ax.imshow(plt.imread(target))
            parts=row.get('topology',{}).get('cut_parts',[])
            ax.set_title(f'{row["id"]} {Path(row["path"]).name[:43]}\n{len(parts)} parts; holes '+str([p['holes'] for p in parts])[:85],fontsize=9)
            ax.axis('off')
        for ax in list(axes.flat)[len(rows[start:start+12]):]: ax.axis('off')
        fig.tight_layout(); fig.savefig(OUT/f'contact-{start//12+1:02d}.png'); plt.close(fig)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--set',default='real')
    parser.add_argument('--render',action='store_true'); parser.add_argument('--only')
    parser.add_argument('--finalize',action='store_true')
    args=parser.parse_args()
    if (CORPUS/'manifest.json').exists(): raise ValueError('Authoring ended at H1 freeze')
    manifest=json.loads((CORPUS/'manifest.draft.json').read_text(encoding='utf-8'))
    OUT.mkdir(parents=True,exist_ok=True)
    config_path=CORPUS/'labels/review-decisions.json'
    decisions=json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
    rows=[]
    for i,entry in enumerate(e for e in manifest['files'] if e['set']==args.set):
        row={'id':f'R{i:02d}' if args.set=='real' else f'N{i:02d}',
             'path':entry['path'],'sha256':entry['sha256'],'reviewed':False}
        if args.only and row['id'] not in args.only.split(','): continue
        path=CORPUS/entry['path']; decision=decisions.get(row['id'],{})
        try:
            if path.suffix=='.dxf':
                doc=ezdxf.readfile(path)
                curves=list(dxf_curves(doc,doc.modelspace()))
                row['units_code']=doc.units
                row['entities']=dict(Counter(e.dxftype() for e in doc.modelspace()))
                row['ignored_non_geometry']=dict(Counter(e.dxftype() for e in doc.modelspace() if e.dxftype() not in GEOMETRY|{'INSERT'}))
            elif path.suffix=='.svg': curves=list(svg_curves(path))
            else: continue
            row['layer_color_counts']=[{'layer':k[0],'color':k[1],'entities':v} for k,v in Counter((c['layer'],c['color']) for c in curves).items()]
            selected=[c for c in curves if ('cut_layers' not in decision or c['layer'] in decision['cut_layers'])
                      and ('cut_colors' not in decision or c['color'] in decision['cut_colors'])
                      and c['id'] not in decision.get('exclude_entities',[])]
            row['topology']=topology(selected,decision.get('join_tolerance_mm',.005))
            row['selection']=decision
            row['curves']=[{k:v for k,v in c.items() if k!='points'} for c in curves]
            target=OUT/(row['id']+'.png')
            if args.render and not target.exists(): row['renderer']=render(path,target,decision.get('black_render',False))
            if args.finalize: finalize_reviewed(row,entry,decision)
            print(row['id'],len(row['topology']['cut_parts']),'parts',round(row['topology']['open_length_mm'],4),'open mm',flush=True)
        except Exception as exc:
            row['error']=str(exc); print(row['id'],'ERROR',str(exc),flush=True)
        write_json(OUT/(row['id']+'.json'),row); rows.append(row)
    write_json(OUT/(args.set+'-worksheet.json'),rows)
    if args.finalize:
        write_json(CORPUS/'manifest.draft.json',manifest)
    if args.render: contacts(rows)
    if any(r.get('error') for r in rows): raise SystemExit(1)


if __name__=='__main__': main()
