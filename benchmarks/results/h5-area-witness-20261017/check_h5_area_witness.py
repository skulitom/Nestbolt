"""Independent validation of an authored area-increasing exchange, without search."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json
import shutil
import subprocess
root=Path(__file__).resolve().parents[1]
out=root/'output/h5-area-witness-20261017';out.mkdir(exist_ok=False)
cli=root/'target/release/nestbolt.exe'
def write(path,x):path.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def rect(name,w,h,q=1):
    return {'id':name,'quantity':q,'geometry':[{'outer':[[0,0],[w,0],[w,h],[0,h]],'holes':[]}],
        'rotations':{'kind':'list','degrees':[0]},'allow_mirror':False,'priority':1}
def placement(name,copy,sheet,x,y):
    return {'part_id':name,'copy_index':copy,'sheet_id':f'sheet-{sheet}',
        'transform':{'translation':[x,y],'rotation_radians':0,'mirrored':False}}
job={'version':1,'name':'Authored larger return set, same last-sheet extent','units':'mm',
    'parts':[rect('filler',60,94),rect('return',30,30,3),rect('incoming',30,85)],
    'stocks':[{'id':'stock','width':100,'height':100,'count':None,
        'margins':{'left':0,'right':0,'top':0,'bottom':0},'outline':[],'defects':[]}],
    'clearance':0.2,'edge_clearance':1,'mode':'all'}
before={'version':1,'units':'mm','sheets':[{'id':f'sheet-{i}','stock_id':'stock'} for i in [0,1]],
    'placements':[placement('filler',0,0,2,2),placement('incoming',0,1,2,2)] +
        [placement('return',i,0,64,2+32*i) for i in range(3)]}
after=deepcopy(before)
for p in after['placements']:
    if p['part_id']=='incoming':p['sheet_id']='sheet-0';p['transform']['translation']=[64,2]
    if p['part_id']=='return':p['sheet_id']='sheet-1';p['transform']['translation']=[2,2+32*p['copy_index']]
write(out/'job.json',job);reports={}
for name,layout in [('before',before),('after',after)]:
    write(out/(name+'.json'),layout)
    command=[str(cli),'validate','--job',str(out/'job.json'),'--layout',str(out/(name+'.json'))]
    result=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
    (out/(name+'-stdout.json')).write_bytes(result.stdout);(out/(name+'-stderr.log')).write_bytes(result.stderr)
    assert result.returncode==0,(name,result.stderr)
    reports[name]=json.loads(result.stdout);assert reports[name]['valid']
    assert reports[name]['metrics']['placed_parts']==5
assert reports['before']['metrics']['material_area']==reports['after']['metrics']['material_area']
check={'authored_fixture_only':True,'searches_run':0,'both_independently_valid':True,
    'incoming_area_mm2':30*85,'returned_area_mm2':3*30*30,
    'material_before_mm2':reports['before']['metrics']['material_area'],
    'material_after_mm2':reports['after']['metrics']['material_area'],
    'cli_sha256':sha256(cli.read_bytes()).hexdigest(),
    'finding':'Combined returned area greater than incoming area does not imply a material increase or invalid placement. Both layouts fit the same original stock, spacing, rotations and quantities.',
    'development_quality_claim':False,'H5_complete':False}
write(out/'checks.json',check);shutil.copyfile(__file__,out/'check.py')
print(json.dumps(check))
