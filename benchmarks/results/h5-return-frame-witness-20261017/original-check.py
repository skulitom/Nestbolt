"""Authored geometry witness for return-group frame alignment; no optimizer runs."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json
import math
import shutil
import subprocess
import traceback
root=Path(__file__).resolve().parents[1]
out=root/'output/h5-return-frame-witness-20261017';out.mkdir()
cli=root/'target/release/nestbolt.exe'
assert sha256(cli.read_bytes()).hexdigest()=='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b'
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def rect(name,w,h,q=1,rotations=(0,)):
    return {'id':name,'quantity':q,'geometry':[{'outer':[[0,0],[w,0],[w,h],[0,h]],'holes':[]}],
        'rotations':{'kind':'list','degrees':list(rotations)},'allow_mirror':False,'priority':1}
def place(name,copy,sheet,x,y,angle=0):
    return {'part_id':name,'copy_index':copy,'sheet_id':f'sheet-{sheet}',
        'transform':{'translation':[x,y],'rotation_radians':math.radians(angle),'mirrored':False}}
job={'version':1,'name':'Authored rotated return group fills the vacated strip','units':'mm',
    'parts':[rect('receiver-filler',94,60),rect('source-filler',60,94),
             rect('return',30,30,3,(0,90,180,270)),rect('incoming',85,30,1,(0,90))],
    'stocks':[{'id':'stock','width':100,'height':100,'count':None,
        'margins':{'left':0,'right':0,'top':0,'bottom':0},'outline':[],'defects':[]}],
    'clearance':0.2,'edge_clearance':1,'mode':'all'}
before={'version':1,'units':'mm','sheets':[{'id':f'sheet-{i}','stock_id':'stock'} for i in [0,1]],
    'placements':[place('receiver-filler',0,0,2,2),place('source-filler',0,1,36,2),
                  place('incoming',0,1,32,2,90)]+[place('return',i,0,2+32*i,64) for i in range(3)]}
translated=deepcopy(before);aligned=deepcopy(before)
for layout in [translated,aligned]:
    incoming=next(p for p in layout['placements'] if p['part_id']=='incoming')
    incoming['sheet_id']='sheet-0';incoming['transform']['translation']=[2,64];incoming['transform']['rotation_radians']=0
# Centered incoming poses: receiver (44.5,79), source (17,44.5).
# Translation-only therefore shifts all previous return parts by (-27.5,-34.5).
for p in translated['placements']:
    if p['part_id']=='return':
        p['sheet_id']='sheet-1';p['transform']['translation']=[2+32*p['copy_index']-27.5,64-34.5]
# The reciprocal rigid map is (x,y) -> (96-y,x), giving three vertical squares.
for p in aligned['placements']:
    if p['part_id']=='return':
        p['sheet_id']='sheet-1';p['transform']['translation']=[32,2+32*p['copy_index']]
        p['transform']['rotation_radians']=math.pi/2
write(out/'job.json',job);reports={}
try:
    for name,layout in [('before',before),('translation-only',translated),('frame-aligned',aligned)]:
        write(out/(name+'.json'),layout)
        command=[str(cli),'validate','--job',str(out/'job.json'),'--layout',str(out/(name+'.json'))]
        p=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
        (out/(name+'-stdout.json')).write_bytes(p.stdout);(out/(name+'-stderr.log')).write_bytes(p.stderr)
        write(out/(name+'-command.json'),{'command':command,'exit_code':p.returncode})
        reports[name]=json.loads(p.stdout)
        if name!='translation-only':
            assert p.returncode==0 and reports[name]['valid'],(name,reports[name])
            assert reports[name]['metrics']['placed_parts']==6
        else:assert not reports[name]['valid'],'Expected collision/out-of-bounds counterexample was accepted'
    assert reports['before']['metrics']['material_area']==reports['frame-aligned']['metrics']['material_area']==19700
    write(out/'checks.json',{'authored_only':True,'searches':0,'initial_and_frame_aligned_valid':True,
        'translation_only_correctly_rejected':True,'parts':6,'material_before_and_after_mm2':19700,
        'returned_area_mm2':2700,'incoming_area_mm2':2550,'cli_sha256':sha256(cli.read_bytes()).hexdigest(),
        'mechanical_job_applicability_unproven':True,'H5_complete':False,'production_changed':False})
    shutil.copyfile(__file__,out/'check.py')
except BaseException:
    write(out/'failure.json',{'error':traceback.format_exc()});raise
print(json.dumps(load if False else {'before_valid':reports['before']['valid'],'translated_valid':reports['translation-only']['valid'],
    'aligned_valid':reports['frame-aligned']['valid'],'material_mm2':19700}))
