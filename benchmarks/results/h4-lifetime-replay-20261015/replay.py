"""Authored repeatable-work regression across window sizes/rotations; not H4 quality."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from hashlib import sha256
import json,sys,psutil
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from h2_import_audit import source_digest
from h6_material_cost import run, equivalent
psutil.Process().cpu_affinity(list(range(16,32)))
phase=sys.argv[1]; binary=Path(sys.argv[2]).resolve()
root=ROOT/'benchmarks/results/h4-lifetime-replay-20261015';root.mkdir(exist_ok=True)
out=root/phase;out.mkdir()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
before=source_digest();bh=sha256(binary.read_bytes()).hexdigest()
write(out/'plan.json',{'scope':__doc__,'source':before,'binary':str(binary),'binary_sha256':bh,'cpus':[0,2,4,6],'seconds':10,'time_limit':60,'seeds':[0,1],'windows':[1,12],'held_out_geometry_read':False})
def task(spec):
 kind,window,cpu=spec
 job={'version':1,'name':'authored L-part window replay '+kind,'units':'mm','mode':'all','clearance':1.5,'edge_clearance':2.5,
 'parts':[{'id':'ell','quantity':14,'geometry':[{'outer':[[0,0],[30,0],[30,8],[9,8],[9,20],[0,20]],'holes':[]}],
 'rotations':{'kind':'free'} if kind=='free' else {'kind':'list','degrees':[0,90,180,270]},'allow_mirror':True,'priority':1}],
 'stocks':[{'id':'stock','width':70,'height':50,'count':None,'margins':{'left':3,'right':1,'bottom':2,'top':4},'outline':[],'defects':[]}]}
 rows=[]
 for seed in [0,1]:
  folder=out/f'{kind}-w{window}-s{seed}';folder.mkdir();write(folder/'job.json',job)
  cmd=[binary,'sheets','--job',folder/'job.json','--output',folder/'layout.json','--seconds','10','--repeatable','--time-limit','60','--window',str(window),'--seed',str(seed)]
  solved=run(cmd,folder,'solve',cpu,75)
  row={'id':folder.name,'solve':solved,'valid':False}
  if solved['exit_code']==0:
   result=json.loads((folder/'solve-stdout.json').read_text(encoding='utf-8'))
   checked=run([binary,'validate','--job',folder/'job.json','--layout',folder/'layout.json'],folder,'validate',cpu,60)
   row['check']=checked
   report=json.loads((folder/'validate-stdout.json').read_text(encoding='utf-8'))
   row['maximum_metric_difference']=equivalent(report['metrics'],result['validation']['metrics'])
   row.update(valid=report['valid'] and checked['exit_code']==0,repeatable=result['repeatable'],material=report['metrics']['normalized_material'],layout_sha256=sha256((folder/'layout.json').read_bytes()).hexdigest())
   if phase=='after':
    previous=root/'before'/folder.name
    old=json.loads((previous/'solve-stdout.json').read_text(encoding='utf-8'))
    row['layout_identical']=(previous/'layout.json').read_bytes()==(folder/'layout.json').read_bytes()
    row['counts_identical']=old['counts']==result['counts']
    row['stats_identical']=old['stats']==result['stats']
    row['work_identical']=old['work']==result['work']
    row['result_except_wall_time_identical']={k:v for k,v in old.items() if k!='elapsed_seconds'}=={k:v for k,v in result.items() if k!='elapsed_seconds'}
  rows.append(row)
 return rows
specs=[('quarter',1,0),('quarter',12,2),('free',1,4),('free',12,6)]
with ThreadPoolExecutor(max_workers=4) as pool:rows=[r for batch in pool.map(task,specs) for r in batch]
assert source_digest()==before and sha256(binary.read_bytes()).hexdigest()==bh
write(out/'results.json',{'source_guards_passed':True,'rows':rows})
print(json.dumps(rows,indent=2))
