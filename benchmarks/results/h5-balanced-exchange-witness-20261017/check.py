"""Authored balanced two-to-three exchange; no optimizer or development measurements."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,shutil,subprocess,traceback
root=Path(__file__).resolve().parents[1];out=root/'output/h5-balanced-exchange-witness-20261017';out.mkdir()
cli=root/'target/release/nestbolt.exe';digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert digest(cli)=='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b'
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def rect(name,w,h,q):
    return {'id':name,'quantity':q,'geometry':[{'outer':[[0,0],[w,0],[w,h],[0,h]],'holes':[]}],
        'rotations':{'kind':'list','degrees':[0]},'allow_mirror':False,'priority':1}
def place(name,copy,sheet,x,y):
    return {'part_id':name,'copy_index':copy,'sheet_id':f'sheet-{sheet}',
        'transform':{'translation':[x,y],'rotation_radians':0,'mirrored':False}}
job={'version':1,'name':'Authored balanced two-to-three exchange','units':'mm',
    'parts':[rect('filler',60,94,2),rect('return',30,30,3),rect('incoming',30,45,2)],
    'stocks':[{'id':'stock','width':100,'height':100,'count':None,
        'margins':{'left':0,'right':0,'top':0,'bottom':0},'outline':[],'defects':[]}],
    'clearance':0.2,'edge_clearance':1,'mode':'all'}
before={'version':1,'units':'mm','sheets':[{'id':f'sheet-{i}','stock_id':'stock'} for i in [0,1]],
    'placements':[place('filler',i,i,36,2) for i in [0,1]]+
                 [place('return',i,0,2,2+32*i) for i in range(3)]+
                 [place('incoming',i,1,2,2+47*i) for i in range(2)]}
after=deepcopy(before)
for p in after['placements']:
    if p['part_id']=='incoming':p['sheet_id']='sheet-0'
    if p['part_id']=='return':p['sheet_id']='sheet-1'
write(out/'job.json',job);reports={}
shutil.copyfile(__file__,out/'check.py')
try:
    for name,layout in [('before',before),('balanced-after',after)]:
        write(out/(name+'.json'),layout)
        command=[str(cli),'validate','--job',str(out/'job.json'),'--layout',str(out/(name+'.json'))]
        result=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
        (out/(name+'-stdout.json')).write_bytes(result.stdout);(out/(name+'-stderr.log')).write_bytes(result.stderr)
        write(out/(name+'-command.json'),{'command':command,'exit_code':result.returncode})
        reports[name]=json.loads(result.stdout)
        assert result.returncode==0 and reports[name]['valid']
        assert reports[name]['metrics']['placed_parts']==7
    assert reports['before']['metrics']==reports['balanced-after']['metrics']
    # Necessary packing bound, deliberately ignoring positive part clearance.
    # Every small axis-aligned rectangle has width 30 and height at least 30.
    usable=100-2*job['edge_clearance'];side_space=usable-60;vertical_space=usable-94
    assert vertical_space<30 and side_space<2*30
    # All small rectangles intersect the filler's vertical range, so must lie
    # to one side. Both sides cannot each fit width 30. In that one side their
    # x intervals overlap, so the sum of their heights must be <= usable height.
    single=[]
    for returned in range(4):
        receiver_height=45+(3-returned)*30
        source_height=45+returned*30
        assert max(receiver_height,source_height)>usable
        single.append({'returned_squares':returned,'receiver_height_lower_bound':receiver_height,
                       'source_height_lower_bound':source_height,'cannot_fit_both_sheets':True})
    assert 2*45+job['clearance']<=usable and 3*30+2*job['clearance']<=usable
    write(out/'checks.json',{'authored_only':True,'optimizer_runs':0,'CLI_validation_runs':2,
        'both_layouts_valid':True,'all_metrics_identical':True,'parts':7,
        'material_mm2':reports['before']['metrics']['material_area'],'incoming_group_area_mm2':2700,'returned_group_area_mm2':2700,
        'scope':'The selected incoming parts are the two 30x45 rectangles; returned parts are the three 30x30 squares. One 60x94 filler remains on each sheet. All orientations are fixed to zero degrees.',
        'usable_width_and_height':usable,'combined_side_space':side_space,'combined_top_bottom_space':vertical_space,
        'single_incoming_bounds':single,'bound_ignores_positive_clearance_conservatively':True,
        'filler_exact_positions_not_required_by_bound':True,
        'does_not_rule_out_other_part_selections_or_global_layouts':True,
        'mechanical_applicability_proven':False,'production_changed':False,'H5_complete':False,'cli_sha256':digest(cli)})
except BaseException:
    write(out/'failure.json',{'error':traceback.format_exc()});raise
print(json.dumps({'both_layouts_valid':True,'all_metrics_identical':True,'material_mm2':reports['before']['metrics']['material_area'],
    'single_selected_incoming_bounds':single,'mechanical_applicability_proven':False}))
