from pathlib import Path
from copy import deepcopy
from functools import partial
import sys, json, math, subprocess
from zipfile import ZipFile
from collections import Counter, defaultdict
import numpy as np
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root/'benchmarks/results/h5-repeated-bands-20261120'))
from rows import catalogue
from construct import construct
def run(archive, size, out):
 out.mkdir(exist_ok=True,parents=True)
 with ZipFile(archive) as z:
  job,layout=[json.loads(z.read(f'nested/{name}.json')) for name in ['job','layout']]
  for name in ['request','library']:(out/(name+'.json')).write_bytes(z.read(name+'.json'))
 def ident(p):return p['part_id'],p['copy_index']
 def rigid(p):
  t=p['transform'];a=t['rotation_radians'];c,s=math.cos(a),math.sin(a);f=-1 if t['mirrored'] else 1;x,y=t['translation']
  return np.array([[c*f,-s,x],[s*f,c,y],[0,0,1.]])
 parts={p['id']:p for p in job['parts']}
 holes=[];outer={}
 for p in layout['placements']:
  key=ident(p);v=parts[key[0]]['geometry'];assert len(v)==1
  mat=rigid(p);m=[mat[0,0],mat[0,1],mat[1,0],mat[1,1],mat[0,2],mat[1,2]]
  outer[key]=affine_transform(Polygon(v[0]['outer']),m)
  for h in v[0]['holes']:holes.append((p,affine_transform(Polygon(h),m)))
 riders={}
 hosts=defaultdict(list)
 for p in layout['placements']:
  key=ident(p);parents=[q for q,h in holes if q['sheet_id']==p['sheet_id'] and ident(q)!=key and h.contains(outer[key])]
  if parents:
   q,=parents;hosts[ident(q)].append(p);riders[key]=ident(q)
 assert not(set(hosts)&set(riders))
 free=defaultdict(list)
 for p in layout['placements']:
  if ident(p) not in riders:free[p['part_id']].append(p)
 proxy=deepcopy(job);proxy['parts']=[p for p in proxy['parts'] if p['id'] in free]
 for p in proxy['parts']:
  p['quantity']=len(free[p['id']])
  for g in p['geometry']:
   ring=g['outer'];g['holes']=[]
   if any(abs(a[0]-b[0])>1e-9 and abs(a[1]-b[1])>1e-9 for a,b in zip(ring,ring[1:]+ring[:1])):
    x,y=zip(*ring); g['outer']=[[min(x),min(y)],[max(x),min(y)],[max(x),max(y)],[min(x),max(y)]]
  if p['rotations']['kind']=='free':p['rotations']={'kind':'list','degrees':[0,90]}
  else:p['rotations']['degrees']=sorted(set(p['rotations']['degrees']))
 trial,details=construct(proxy,layout,partial(catalogue,maximum_size=size));print('riders',len(riders),'shape families',[(p['id'],p['quantity']) for p in proxy['parts']], 'catalogue',details['catalogue'],flush=True)
 if trial is None:return
 for q in trial['placements'].copy():
  old=free[q['part_id']][q['copy_index']];q['copy_index']=old['copy_index']
  delta=rigid(q)@np.linalg.inv(rigid(old))
  for rider in hosts[ident(old)]:
   m=delta@rigid(rider);mirror=bool(np.linalg.det(m)<0);factor=-1 if mirror else 1
   trial['placements'].append(dict(rider,sheet_id=q['sheet_id'],transform=dict(translation=list(m[:2,2]),rotation_radians=math.atan2(m[1,0]*factor,m[0,0]*factor)%(2*math.pi),mirrored=mirror)))
 assert len(trial['placements'])==len(layout['placements'])
 path=out/'layout.json';path.write_text(json.dumps(trial),encoding='utf-8')
 resp=subprocess.run([root/'target/release/nestbolt.exe','validate','--library',out/'library.json','--request',out/'request.json','--layout',path],capture_output=True)
 (out/'validation.json').write_bytes(resp.stdout)
 if not resp.stdout:raise RuntimeError(resp.stderr)
 v=json.loads(resp.stdout)
 print(archive.name,size,v['valid'],v.get('metrics',{}).get('normalized_material'),v.get('violations',[])[:2],flush=True)
 (out/'calculation.json').write_text(json.dumps(details,indent=2),encoding='utf-8')
if __name__=='__main__':run(Path(sys.argv[1]),int(sys.argv[2]),Path(sys.argv[3]))
