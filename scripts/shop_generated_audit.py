"""Read generated DXF centreline bounds with ezdxf, independently of authoring.

Applies each INSERT's matrix to leaf geometry in order. Flattening nested INSERTs
into a replacement INSERT loses shear under nonuniform scaling; do not use that
approximation. Polyline widths are excluded from the cutting centreline bounds.
This does not test the Nestbolt importer or assert its H2 gate.
"""
from datetime import datetime, timezone
from collections import Counter
from hashlib import sha256
import json
from math import dist
from pathlib import Path

import ezdxf
from ezdxf.path import make_path
from shop_sources import CORPUS, ROOT


def points(doc, entities, layers, frames=()):
    for entity in entities:
        if entity.dxftype() == 'INSERT':
            yield from points(doc, doc.blocks.get(entity.dxf.name), layers, (*frames,entity.matrix44()))
        elif entity.dxf.layer in layers:
            path=make_path(entity)
            for p in path.flattening(distance=.0002):
                for matrix in reversed(frames): p=matrix.transform(p)
                yield p


def main():
    manifest=json.loads((CORPUS/'generated/manifest.json').read_text(encoding='utf-8'))
    rows=[]
    for row in manifest['files']:
        data=(CORPUS/row['path']).read_bytes(); label_data=(CORPUS/row['label']).read_bytes()
        assert sha256(data).hexdigest()==row['sha256'],row['path']
        assert sha256(label_data).hexdigest()==row['label_sha256'],row['label']
        label=json.loads(label_data)
        doc=ezdxf.readfile(CORPUS/row['path'])
        pts=list(points(doc,doc.modelspace(),label['cut_layers']))
        scale=25.4 if 'inches' in row['habit'] else 10 if row['habit']=='centimetres' else 1
        actual=[min(p.x for p in pts)*scale,min(p.y for p in pts)*scale,
                max(p.x for p in pts)*scale,max(p.y for p in pts)*scale]
        wanted=[min(p['outer_bounds_mm'][0] for p in label['cut_parts']),min(p['outer_bounds_mm'][1] for p in label['cut_parts']),
                max(p['outer_bounds_mm'][2] for p in label['cut_parts']),max(p['outer_bounds_mm'][3] for p in label['cut_parts'])]
        delta=max(abs(a-b) for a,b in zip(actual,wanted))
        feature_checks={}
        habit=row['habit']
        raw_entities=list(doc.modelspace())
        if habit.startswith('gap-'):
            ends=Counter((round(p.x,7),round(p.y,7)) for e in raw_entities
                         if e.dxftype()=='LINE' and e.dxf.layer=='CUT'
                         for p in [e.dxf.start,e.dxf.end])
            loose=[p for p,count in ends.items() if count==1]
            feature_checks['two_open_endpoints']=len(loose)==2
            feature_checks['measured_gap']=len(loose)==2 and abs(dist(*loose)-label['features']['gap']['size_mm'])<2e-7
        if habit=='duplicates-zero':
            lines=[(tuple(e.dxf.start),tuple(e.dxf.end)) for e in raw_entities if e.dxftype()=='LINE']
            counts=Counter(tuple(sorted((a,b))) for a,b in lines if a!=b)
            feature_checks['two_duplicate_segments']=sum(v-1 for v in counts.values())==2
            feature_checks['one_zero_segment']=sum(a==b for a,b in lines)==1
        if habit=='missing-header-inches': feature_checks['no_header']=b'\nHEADER\n' not in data
        if habit=='missing-units-inches': feature_checks['no_insunits']=b'$INSUNITS' not in data
        if habit=='centimetres': feature_checks['cm_header']=doc.units==5
        if habit=='single-block-insert': feature_checks['one_insert']=len(raw_entities)==1 and raw_entities[0].dxftype()=='INSERT'
        if habit=='annotations-construction':
            feature_checks['annotation_types']=set(label['features']['ignored_types']) <= {e.dxftype() for e in raw_entities}
        if habit=='operation-colours':
            feature_checks['operation_colours']=[doc.layers.get(n).dxf.color for n in ['Operation A','Operation B','Operation C']]==[7,5,1]
        rows.append({'path':row['path'],'sha256':row['sha256'],'label_sha256':row['label_sha256'],
                     'centerline_bounds_mm':actual,'label_bounds_mm':wanted,'max_difference_mm':delta,
                     'fault_checks':feature_checks,'pass':delta<=.002 and all(feature_checks.values())})
    result={'recorded_at':datetime.now(timezone.utc).isoformat(),'scope':'N0 generated geometry authoring check; no product import',
            'files':len(rows),'bases':len(manifest['bases']),'limit_mm':.002,'pass':all(r['pass'] for r in rows),
            'max_difference_mm':max(r['max_difference_mm'] for r in rows),'rows':rows,
            'method':'ezdxf paths flattened at 0.0002 mm; nested INSERT matrices composed without intermediate decomposition; cut centrelines only; declared inch/cm scales explicit',
            'H1':False,'H2':False,'completed_milestone_weight_percent':0}
    path=ROOT/'benchmarks/results/n0-generated-20261013.json'
    path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','method')}))
    if not result['pass']: raise SystemExit(1)


if __name__=='__main__':
    main()
