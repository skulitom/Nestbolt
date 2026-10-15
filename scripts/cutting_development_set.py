"""Freeze the 13 development jobs named by H5/H6, without held-out geometry.

The eight maker jobs are referenced at their frozen hashes. Five new MIT jobs
are authored from rectangles and brackets. The measured geometry is each job's
polygon contract, represented as exact lines in the public library format.
"""
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from dataset_selection import development_cases

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT/'benchmarks/datasets/cutting'
MAKERS = ['m-box-batch-500', 'm-box-desktop', 'm-box-long', 'm-box-mini',
          'm-box-storage', 'm-box-tool', 'm-mechanical-large-plates',
          'm-mechanical-panel-hardware']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8', newline='\n')


def rect(w, h, x=0, y=0):
    return [[x,y],[x+w,y],[x+w,y+h],[x,y+h]]


def authored():
    ell = [[0,0],[60,0],[60,12],[12,12],[12,45],[0,45]]
    tee = [[0,0],[70,0],[70,50],[58,50],[58,12],[12,12],[12,50],[0,50]]
    panel = {'outer':rect(70,50), 'holes':[rect(10,10,10,20),rect(10,10,50,20)]}
    specs = [
        ('c-rect-equal',300,200,[(60,rect(40,30))]),
        ('c-rect-mixed',400,300,[(40,rect(60,25)),(40,rect(30,25)),(10,rect(90,40))]),
        ('c-bracket-l',400,300,[(60,ell)]),
        ('c-bracket-u',400,300,[(50,tee)]),
        ('c-bracket-mixed',400,300,[(32,ell),(24,tee),(24,panel)]),
    ]
    for name,w,h,parts in specs:
        yield {'version':1,'name':name,'units':'mm',
            'parts':[{'id':f'p-{i}','quantity':q,
                      'geometry':[p if isinstance(p,dict) else {'outer':p,'holes':[]}],
                      'rotations':{'kind':'list','degrees':[0,90,180,270]},
                      'allow_mirror':False,'priority':1.0} for i,(q,p) in enumerate(parts)],
            'stocks':[{'id':'stock','width':w,'height':h,'count':None,
                       'margins':{'left':0,'right':0,'bottom':0,'top':0},'outline':[],'defects':[]}],
            'clearance':0.2,'edge_clearance':1.0,'mode':'all'}


def freeze():
    assert not FOLDER.exists(), 'Frozen development set already exists; never replace it'
    _, candidates = development_cases(ROOT, 'M')
    selected = {r['id']:r for r in candidates if r['id'] in MAKERS}
    assert set(selected)==set(MAKERS)
    rows=[]
    for name in MAKERS:
        row=selected[name]
        path=ROOT/'benchmarks/datasets'/row['path']
        assert not row['held_out'] and digest(path)==row['sha256'], name
        rows.append({'id':name,'path':path.relative_to(ROOT).as_posix(),
                     'sha256':row['sha256'],'source':'Frozen v1 development maker job',
                     'license_record':'benchmarks/makers/sources.json'})
    FOLDER.mkdir()
    for job in authored():
        path=FOLDER/(job['name']+'.json')
        write_json(path,job)
        rows.append({'id':job['name'],'path':path.relative_to(ROOT).as_posix(),
                     'sha256':digest(path),'source':'Authored rectangle/bracket job',
                     'license_record':'LICENSE','license':'MIT'})
    record={'version':1,'frozen_at':datetime.now(timezone.utc).isoformat(),
            'scope':'H5/H6 development only; eight prescribed maker jobs and five authored jobs',
            'maker_manifest_sha256':digest(ROOT/'benchmarks/datasets/makers.json'),
            'generator_sha256':digest(Path(__file__)),'kerfs_mm':[0.2,1.5],
            'seeds':[0,1,2],'jobs':rows,
            'geometry':'Original frozen polygon job rings become exact line contours; no simplification or curve reconstruction',
            'held_out_geometry_read':False}
    write_json(FOLDER/'manifest.json',record)
    print(json.dumps({'manifest':str(FOLDER/'manifest.json'),'jobs':len(rows),'sha256':digest(FOLDER/'manifest.json')}))


def load_cases():
    manifest=json.loads((FOLDER/'manifest.json').read_text(encoding='utf-8'))
    makers=json.loads((ROOT/'benchmarks/datasets/makers.json').read_text(encoding='utf-8'))
    assert digest(ROOT/'benchmarks/datasets/makers.json')==manifest['maker_manifest_sha256']
    held=set(makers['held_out_ids'])
    assert len(manifest['jobs'])==13 and not held.intersection(r['id'] for r in manifest['jobs'])
    rows=[]
    for row in manifest['jobs']:
        path=ROOT/row['path']
        assert digest(path)==row['sha256'], row['id']
        job=json.loads(path.read_text(encoding='utf-8'))
        assert job['name']==row['id'] and job['units']=='mm' and job['mode']=='all'
        assert all(len(p['geometry'])==1 for p in job['parts']), 'Public polygon library needs one component'
        rows.append((row,job))
    return rows


def contour(ring):
    assert len(ring)>=3
    return {'start':ring[0], 'segments':[{'kind':'line','to':p} for p in ring[1:]+ring[:1]]}


def area(ring):
    return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(ring,ring[1:]+ring[:1])))/2


def public_inputs(job, kerf, leads):
    library={'version':1,'tolerance':0.0,'parts':[],'warnings':[],'imports':[]}
    for p in job['parts']:
        poly=deepcopy(p['geometry'][0]); ring=poly['outer']
        library['parts'].append({'id':p['id'],'source':job['name'],
            'outer':contour(ring),'holes':[contour(h) for h in poly['holes']],
            'polygon':poly,'area_mm2':area(ring)-sum(area(h) for h in poly['holes']),
            'bounds_mm':[min(v[0] for v in ring),min(v[1] for v in ring),
                         max(v[0] for v in ring),max(v[1] for v in ring)]})
    request={'name':job['name'],'parts':[{k:deepcopy(p[k]) for k in ['id','quantity','rotations','allow_mirror','priority']} for p in job['parts']],
        'sheets':[{'id':s['id'],'width_mm':s['width'],'height_mm':s['height'],'count':s['count'],
                   'margins_mm':s['margins'],'defects_mm':s['defects'],'outline_mm':s['outline']} for s in job['stocks']],
        'spacing_mm':kerf,'edge_spacing_mm':job['edge_clearance'],'mode':job['mode'],
        'common_line':{'kerf_mm':kerf}}
    if leads:
        request['lead_in']={'kerf_mm':kerf,'length_mm':3.0,'style':'line',
                            'outer_angle_degrees':45.0,'hole_angle_degrees':90.0}
    return library,request


if __name__=='__main__':
    freeze()
