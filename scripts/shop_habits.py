"""Generate seeded shop-file faults and independent labels from ten clean bases.

This is benchmark authoring, not the product importer. No held-out maker data
is read. Source paths and analytical geometry supply labels before N1 changes.
Run with --check to regenerate in memory and reject any changed corpus bytes.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import io
import importlib.metadata
import json
from math import atan2, cos, degrees, hypot, radians, sin, sqrt, tan
from pathlib import Path
import random
import xml.etree.ElementTree as E

import ezdxf
from svgpathtools import Arc, CubicBezier, Line, Path as SvgPath, QuadraticBezier, parse_path
from maker_geometry import classify_rings, flatten_segment
from shop_sources import CORPUS, ROOT

SEED = 110013
TOLERANCE = 0.0005
HABITS = ['exploded-shuffled', 'gap-0.001', 'gap-0.05', 'gap-0.5',
          'overlap-0.001', 'overlap-0.5', 'duplicates-zero', 'fusion-splines-extrusion',
          'bulges-widths', 'nested-mirrored-blocks', 'single-block-insert',
          'missing-header-inches', 'missing-units-inches', 'centimetres',
          'annotations-construction', 'operation-colours', 'existing-nest']


def digest(data):
    return sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True)+'\n').encode('utf-8')


def xy(z):
    return z.real, z.imag


def circle(cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    return parse_path(f'M {cx-rx},{cy} A {rx},{ry} 0 1,0 {cx+rx},{cy} A {rx},{ry} 0 1,0 {cx-rx},{cy} Z')


def clean_bases():
    curves_path = ROOT/'examples/fidelity/curves-mm.svg'
    parts_path = ROOT/'examples/parts.svg'
    curves, parts = E.parse(curves_path).getroot(), E.parse(parts_path).getroot()
    by_id = {e.get('id'): e for e in curves.iter() if e.get('id')}
    example = {e.get('id'): e for e in parts.iter() if e.get('id')}
    r = by_id['rounded']; x, y, w, h, rx = (float(r.get(k)) for k in ['x','y','width','height','rx'])
    rounded = parse_path(f'M {x+rx},{y} H {x+w-rx} A {rx},{rx} 0 0,1 {x+w},{y+rx} V {y+h-rx} A {rx},{rx} 0 0,1 {x+w-rx},{y+h} H {x+rx} A {rx},{rx} 0 0,1 {x},{y+h-rx} V {y+rx} A {rx},{rx} 0 0,1 {x+rx},{y} Z')
    oval = by_id['oval']
    frame = parse_path(by_id['frame'].get('d')).rotated(15, origin=0j).translated(110+60j)
    # Refuse silent changes to the parent transform used for this fixture.
    group = next(e for e in curves if e.tag.endswith('g'))
    assert group.get('transform') == 'translate(110 60) rotate(15)'
    washer = [circle(float(example[n].get('cx')), float(example[n].get('cy')), float(example[n].get('r')))
              for n in ['washer-outer','washer-hole']]
    recipes = [('rounded', [rounded], curves_path, ['rounded']),
               ('bezier', [parse_path(by_id['bezier'].get('d'))], curves_path, ['bezier']),
               ('example-frame', [parse_path(example['frame'].get('d'))], parts_path, ['frame']),
               ('washer', washer, parts_path, ['washer-outer','washer-hole']),
               ('oval', [circle(float(oval.get('cx')), float(oval.get('cy')), float(oval.get('rx')), float(oval.get('ry')))], curves_path, ['oval']),
               ('rotated-frame', [frame], curves_path, ['frame'])]
    makers = json.loads((ROOT/'benchmarks/datasets/makers.json').read_text(encoding='utf-8'))
    job = 'm-mechanical-cog-washers'
    assert job not in makers['held_out_ids']
    entry = next(x for x in makers['instances'] if x['id'] == job)
    assert not entry['held_out'] and entry['source'] == 'procedural'
    maker_path = ROOT/f'benchmarks/datasets/maker-assets/{job}/curves.json'
    expected = entry['files'][f'maker-assets/{job}/curves.json']
    assert digest(maker_path.read_bytes()) == expected
    for part in json.loads(maker_path.read_text(encoding='utf-8')):
        recipes.append(('maker-'+part['id'], [parse_path(d) for d in part['paths']], maker_path, [part['id']]))
    bases = []
    for name, paths, source, ids in recipes:
        rings = [s for p in paths for s in p.continuous_subpaths()]
        assert all(abs(p.start-p.end) < 1e-8 for p in rings)
        min_x = min(p.bbox()[0] for p in rings); min_y = min(p.bbox()[2] for p in rings)
        rings = [p.translated(complex(10-min_x, 10-min_y)) for p in rings]
        bases.append({'id': name, 'paths': rings, 'source': source.relative_to(ROOT).as_posix(),
                      'source_sha256': digest(source.read_bytes()), 'source_elements': ids,
                      'source_translation_mm': [10-min_x, 10-min_y]})
    assert len(bases) == 10
    return bases


def flatten(paths):
    rings = []
    for p in paths:
        points = []
        for seg in p:
            points += flatten_segment(seg, TOLERANCE)[:-1]
        assert len(points) >= 3
        rings.append(points)
    return rings


def segments(rings):
    return [(a, b) for ring in rings for a, b in zip(ring, ring[1:]+ring[:1])]


def bounds(ring):
    return [min(z.real for z in ring), min(z.imag for z in ring), max(z.real for z in ring), max(z.imag for z in ring)]


def geometry_label(rings):
    components = classify_rings([[list(xy(z)) for z in ring] for ring in rings])
    result = []
    for c in components:
        b = bounds([complex(*p) for p in c['outer']])
        result.append({'holes': len(c['holes']), 'outer_bounds_mm': b,
                       'outer_size_mm': [b[2]-b[0], b[3]-b[1]]})
    return result


def doc_new(units=4, cut_layer='CUT', legacy=False):
    ezdxf.options.write_fixed_meta_data_for_testing = True
    doc = ezdxf.new('R12' if legacy else 'R2010'); doc.units = units
    for name, color in [(cut_layer,7),('SCORE',5),('ENGRAVE',1),('ANNOTATION',3),
                        ('bend',4),('extent',6),('SHEET',30)]:
        doc.layers.add(name, color=color)
    return doc


def add_lines(space, lines, layer='CUT', color=256):
    for a, b in lines:
        space.add_line(xy(a), xy(b), dxfattribs={'layer': layer, 'color': color})


def add_curves(space, paths, negative_extrusion=False):
    counts = CounterForFeatures()
    for path in paths:
        for s in path:
            attrs = {'layer':'CUT'}
            if isinstance(s, (Line, CubicBezier, QuadraticBezier)):
                points = [xy(p) for p in s.bpoints()]
                degree = len(points)-1
                space.add_open_spline(points, degree=degree, knots=[0]*(degree+1)+[1]*(degree+1), dxfattribs=attrs)
                counts['splines'] += 1
            elif isinstance(s, Arc) and abs(abs(s.radius.real)-abs(s.radius.imag)) < 1e-8:
                start = degrees(atan2((s.start-s.center).imag, (s.start-s.center).real))
                end = degrees(atan2((s.end-s.center).imag, (s.end-s.center).real))
                if s.delta < 0: start, end = end, start
                center = s.center
                if negative_extrusion:
                    center = complex(-center.real,center.imag)
                    start, end = 180-end, 180-start
                    attrs['extrusion'] = (0,0,-1)
                    counts['negative_extrusion_arcs'] += 1
                space.add_arc(xy(center), abs(s.radius.real), start % 360, end % 360, dxfattribs=attrs)
            else:
                # Noncircular arcs retain a bounded approximation in the fixture.
                points = flatten_segment(s,TOLERANCE)
                for a,b in zip(points,points[1:]):
                    space.add_open_spline([xy(a),xy(b)], degree=1, knots=[0,0,1,1], dxfattribs=attrs)
                    counts['splines'] += 1
    return dict(counts)


class CounterForFeatures(dict):
    def __missing__(self, key):
        self[key] = 0
        return 0


def cut_gap(ring, gap):
    """Remove an exact-distance prefix, even when curves have short chords."""
    start = ring[0]
    for i in range(len(ring)-1):
        a,b = ring[i],ring[i+1]
        if abs(b-start) < gap: continue
        d, q = b-a, a-start
        aa = abs(d)**2; bb = 2*(q.conjugate()*d).real; cc = abs(q)**2-gap**2
        t = (-bb+sqrt(max(0,bb*bb-4*aa*cc)))/(2*aa)
        assert -1e-8 <= t <= 1+1e-8
        endpoint = a+t*d
        points = [endpoint]+ring[i+1:]+[start]
        return list(zip(points,points[1:])), {'location_mm': list(xy(start)), 'other_endpoint_mm': list(xy(endpoint)), 'size_mm': abs(endpoint-start)}
    raise ValueError('Requested gap consumes the base ring')


def transformed_nested(z):
    # INNER insert: mirror X, rotate 30 degrees, translate (20,30).
    p = complex(-z.real,z.imag)*complex(cos(radians(30)),sin(radians(30)))+complex(20,30)
    # OUTER insert: scale anisotropically, rotate -15 degrees, translate (120,80).
    return complex(1.3*p.real,.8*p.imag)*complex(cos(radians(-15)),sin(radians(-15)))+complex(120,80)


def dxf_bytes(doc, strip_header=False):
    # The required-class registry iterates a set. Canonical order is needed
    # across Python processes even when geometry RNG and metadata are fixed.
    if doc.dxfversion != 'AC1009':
        doc.classes.add_required_classes(doc.dxfversion)
        doc.classes.classes = dict(sorted(doc.classes.classes.items()))
    stream = io.StringIO(newline='\n'); doc.write(stream)
    raw = stream.getvalue()
    if strip_header:
        lines = raw.splitlines(); pairs=list(zip(lines[::2],lines[1::2]))
        begin=next(i for i,(k,v) in enumerate(pairs) if k.strip()=='2' and v=='HEADER')-1
        end=next(i for i in range(begin+2,len(pairs)) if pairs[i][0].strip()=='0' and pairs[i][1]=='ENDSEC')+1
        raw='\n'.join(v for pair in pairs[:begin]+pairs[end:] for v in pair)+'\n'
    return raw.encode('utf-8')


def generate_case(base, habit, seed):
    rng = random.Random(seed)
    paths=base['paths']; rings=flatten(paths); expected=deepcopy(rings)
    cut_layer='Operation A' if habit=='operation-colours' else 'CUT'
    # A headerless file must remain legal R12; stripping a modern HEADER alone
    # leaves incompatible object/layout records and introduces an unrelated fault.
    doc=doc_new(5 if habit=='centimetres' else 4,cut_layer,legacy=habit=='missing-header-inches'); space=doc.modelspace()
    features={}; warnings=[]; options={'layers':[cut_layer]}; default_failure=None
    base_lines=segments(rings)
    if habit=='fusion-splines-extrusion':
        features=add_curves(space,paths,negative_extrusion=True)
    elif habit=='bulges-widths':
        bulges=0
        for path in paths:
            points=[]
            for s in path:
                if isinstance(s,Arc) and abs(abs(s.radius.real)-abs(s.radius.imag))<1e-8:
                    points.append((*xy(s.start),.15,.3,tan(radians(s.delta)/4)));bulges+=1
                else:
                    points.extend((*xy(z),.15,.3,0) for z in flatten_segment(s,TOLERANCE)[:-1])
            space.add_lwpolyline(points,format='xyseb',close=True,dxfattribs={'layer':'CUT'})
        features={'nonzero_widths':True,'bulged_segments':bulges}; warnings=['polyline_widths_ignored_for_cut_centerline']
    elif habit=='nested-mirrored-blocks':
        inner=doc.blocks.new('INNER');add_lines(inner,base_lines)
        outer=doc.blocks.new('OUTER');outer.add_blockref('INNER',(20,30),dxfattribs={'xscale':-1,'rotation':30,'layer':'CUT'})
        space.add_blockref('OUTER',(120,80),dxfattribs={'xscale':1.3,'yscale':.8,'rotation':-15,'layer':'CUT'})
        expected=[[transformed_nested(z) for z in ring] for ring in rings]
        features={'block_depth':2,'negative_scale':True,'nonuniform_scale':True}
    elif habit=='single-block-insert':
        block=doc.blocks.new('WHOLE_DRAWING');add_lines(block,base_lines)
        space.add_blockref('WHOLE_DRAWING',(0,0),dxfattribs={'layer':'CUT'})
        features={'modelspace_geometry':'one INSERT','block_depth':1}
    elif habit=='existing-nest':
        b=bounds(rings[0]); width,height=b[2]-b[0],b[3]-b[1]
        expected=[]
        for i in range(3):
            moved=[[z+complex(i*(width+10),0) for z in ring] for ring in rings]
            add_lines(space,segments(moved)); expected+=moved
        sheet=[(0,0),(3*width+40,0),(3*width+40,height+20),(0,height+20)]
        space.add_lwpolyline(sheet,close=True,dxfattribs={'layer':'SHEET'})
        features={'sheet_outline_mm':sheet,'sheet_layer':'SHEET','prearranged_parts':3}
        warnings=['sheet_outline_available']
    else:
        lines=list(base_lines)
        if habit.startswith('gap-'):
            gap=float(habit[4:]); lines,gap_info=cut_gap(rings[0],gap)
            lines+=segments(rings[1:]);features={'gap':gap_info}
            if gap>.005:
                options['close_gaps_mm']=gap+.001
                warnings=['gap_closed_with_explicit_tolerance']
                default_failure={'reason':'open contour', 'fix':f'enable Close gaps up to {gap+.001:g} mm', 'no_silent_missing_part':True}
        elif habit.startswith('overlap-'):
            requested=float(habit[8:]); index=max(range(len(lines)),key=lambda i:abs(lines[i][1]-lines[i][0]))
            a,b=lines.pop(index);actual=min(requested,abs(b-a)/2);unit=(b-a)/abs(b-a);middle=(a+b)/2
            lines.extend([(a,middle+unit*actual/2),(middle-unit*actual/2,b)])
            features={'overlap_requested_mm':requested,'overlap_actual_mm':actual,'merge_count':1}
            warnings=['overlapping_collinear_segments_merged']
        elif habit=='duplicates-zero':
            a,b=lines[0];lines += [(a,b),(b,a),(a,a)]
            features={'duplicate_segments_added':2,'zero_length_segments_added':1}
            warnings=['duplicate_segments_removed','zero_length_segments_removed']
        factor=1
        if habit in ['missing-header-inches','missing-units-inches']:
            factor=1/25.4; del doc.header['$INSUNITS'];options['units']='in'
            features={'actual_drawing_units':'inches','header_missing':habit=='missing-header-inches',
                      'default_must_not_rescale':True,'default_bounds_scale_vs_label':factor}
            warnings=['units_missing_possible_inches']
        elif habit=='centimetres':
            factor=.1;features={'INSUNITS':5,'drawing_units':'centimetres'}
        rng.shuffle(lines)
        lines=[(b,a) if rng.random()<.5 else (a,b) for a,b in lines]
        add_lines(space,[(factor*a,factor*b) for a,b in lines],cut_layer)
        if habit=='annotations-construction':
            space.add_text('Do not cut this note',dxfattribs={'layer':'ANNOTATION','insert':(10,120),'height':5})
            space.add_mtext('Dimensions and hatches are annotations',dxfattribs={'layer':'ANNOTATION','insert':(10,140),'char_height':4})
            space.add_aligned_dim((10,10),(50,10),distance=-8,dxfattribs={'layer':'ANNOTATION'}).render()
            hatch=space.add_hatch(color=3,dxfattribs={'layer':'ANNOTATION'});hatch.paths.add_polyline_path([(20,20),(25,20),(25,25),(20,25)],is_closed=True)
            space.add_leader([(10,150),(20,145),(30,145)],dxfattribs={'layer':'ANNOTATION'})
            space.add_solid([(40,140),(45,140),(40,145)],dxfattribs={'layer':'ANNOTATION'})
            add_lines(space,[(0j,200+200j)],'bend');add_lines(space,[(200j,200+0j)],'extent')
            features={'ignored_types':['TEXT','MTEXT','DIMENSION','HATCH','LEADER','SOLID'],'ignored_layers':['ANNOTATION','bend','extent']}
            warnings=['annotations_ignored','construction_layers_ignored']
        elif habit=='operation-colours':
            doc.layers.add('Operation B',color=5);doc.layers.add('Operation C',color=1)
            add_lines(space,[(20+120j,80+120j)],'Operation B')
            space.add_circle((40,140),3,dxfattribs={'layer':'Operation C'})
            options={'colors':[7]};features={'cut_aci':7,'score_aci':5,'engrave_aci':1,'operation_names_deliberately_generic':True}
    label={'schema_version':1,'base':base['id'],'habit':habit,'seed':seed,
           'derivation':'Analytical source paths, explicit generator edits and transforms; no Nestbolt import used.',
           'geometry_tolerance_mm':TOLERANCE,'cut_parts':geometry_label(expected),
           'cut_layers':[cut_layer],'cut_dxf_aci':[7],'import_options':options,
           'expected_warnings':warnings,'default_failure':default_failure,'features':features}
    return dxf_bytes(doc,strip_header=habit=='missing-header-inches'),label


def all_outputs(seed):
    outputs={};rows=[];base_rows=[]
    for base in clean_bases():
        geometry=[p.d() for p in base['paths']]
        paths=''.join(f'<path d="{d}"/>' for d in geometry)
        clean=f'<svg xmlns="http://www.w3.org/2000/svg" width="200mm" height="200mm" viewBox="0 0 200 200"><g fill="none" stroke="#000000">{paths}</g></svg>\n'
        clean_path=f'bases/{base["id"]}.svg';outputs[clean_path]=clean.encode('utf-8')
        base_rows.append({**{k:v for k,v in base.items() if k!='paths'},'path':clean_path,
                          'sha256':digest(outputs[clean_path]),'licence':'MIT','licence_location':'LICENSE (repository root)',
                          'derivation':'Selected source elements, exact simple-shape path conversion, original group transform, then translation to min (10,10) mm.'})
        for habit in HABITS:
            case_seed=int(digest(f'{seed}:{base["id"]}:{habit}'.encode())[:12],16)
            data,label=generate_case(base,habit,case_seed)
            path=f'generated/{base["id"]}--{habit}.dxf'; label_path=f'labels/generated/{base["id"]}--{habit}.json'
            label['file']=path; label['sha256']=digest(data)
            outputs[path]=data; outputs[label_path]=json_bytes(label)
            rows.append({'path':path,'set':'generated','label':label_path,'sha256':digest(data),
                         'label_sha256':digest(outputs[label_path]),'base':base['id'],'habit':habit,'seed':case_seed,
                         'licence':'MIT','licence_location':'LICENSE (repository root)',
                         'writer':{'name':'scripts/shop_habits.py with ezdxf 1.4.4','evidence':'Deterministic seeded generation from the recorded base paths; fixed DXF timestamps and GUIDs.'}})
    outputs['generated/manifest.json']=json_bytes({'state':'draft-not-frozen','seed':seed,'bases':base_rows,'files':rows,
                                                 'generator_sha256':digest(Path(__file__).read_bytes()),
                                                 'geometry_helper_sha256':digest((ROOT/'scripts/maker_geometry.py').read_bytes()),
                                                 'dependencies':{p:importlib.metadata.version(p) for p in ['ezdxf','svgpathtools','numpy','scipy','shapely']},'H1':False})
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--seed',type=int,default=SEED)
    parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if (CORPUS/'manifest.json').exists() and not args.check:
        raise ValueError('Corpus is frozen; only --check is allowed')
    outputs=all_outputs(args.seed)
    for relative,data in outputs.items():
        path=CORPUS/relative
        if args.check:
            if path.read_bytes()!=data: raise ValueError('Deterministic regeneration differs: '+relative)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print(json.dumps({'bases':10,'habits':len(HABITS),'generated_files':10*len(HABITS),
                      'labels':10*len(HABITS),'seed':args.seed,'byte_reproduction_checked':args.check,'H1':False}))


if __name__=='__main__':
    main()
