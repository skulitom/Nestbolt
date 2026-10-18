"""Validate every saved diagnostic stage and independently reconstruct material."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import ast,copy,itertools,json,math,shutil,subprocess,sys,traceback,zipfile
import shapely
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1];evidence=root/'benchmarks/results/h5-joint-observer-20261018'
sys.path.insert(0,str(root/'scripts'));import h5_joint_trace as reader
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert load(evidence/'verification.json')['all_original_archives_verified']
out=evidence/'geometry-checks';out.mkdir();cache={};records=[];pairs=0
cli=root/'output/h5-joint-repair-probe-20261018/public-checks/nestbolt-validator.exe'
assert digest(cli)=='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b'
sources={}
for name,names in [('output/check_h5_joint_observer_geometry.py',['write','validate']),
    ('output/inspect_h5_neutral_heights.py',['rounded','heights'])]:
    path=root/name;sources[name]=digest(path);tree=ast.parse(path.read_text(encoding='utf-8'))
    for name in names:
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'))
material_rows=[];source_rows=[]
def check_whole(job,layout,valid,metrics,origin):
    validate(job,layout,valid,metrics,origin)
    if valid:
        material,highest,poses,charged=heights(job,layout)
        assert material==metrics['material_area'],(origin,material,metrics['material_area'])
        credited=next(s for s in charged if s['sheet']==metrics['last_sheet_id'])
        assert credited['saving']==max(s['saving'] for s in charged)
        material_rows.append({'origin':origin,'material':material,'credited_sheet':credited['sheet'],
            'credited_height':credited['used_height'],'sheets':charged})
try:
    results=load(evidence/'results.json')
    for row in results['records']:
        with zipfile.ZipFile(evidence/row['archive']) as z:
            job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
        check_whole(job,layout,True,row['metrics'],{'archive':row['archive'],'stage':'final'})
    for forest in load(evidence/'trace-forests.json'):
        traces=forest['traces'];reader.check_traces(traces);by={t['id']:t for t in traces}
        for t in traces:
            origin={'archive':forest['archive'],'trace':t['id']}
            if t['kind']=='policy':
                check_whole(t['data']['job'],t['data']['baseline'],True,t['data']['metrics'],origin|{'stage':'baseline'})
            elif t['kind']=='attempt':
                trials=[e['data'] for e in t['events'] if e['stage']=='validated_trial']
                if trials:
                    trial=trials[0];report=trial['report'];job=by[t['parent']]['data']['job']
                    check_whole(job,trial['layout'],report['valid'],report.get('metrics'),origin|{'stage':'trial'})
            elif t['kind']=='pair':
                for stage in ['recrop_exit','lowering_exit']:
                    values=[e['data'] for e in t['events'] if e['stage']==stage]
                    if not values:continue
                    value=values[0];losses=value['losses'] if stage=='recrop_exit' else [value['loss']]
                    if any(v!=0 for v in losses):continue
                    pair=value['pair'];counts=sum((reader.inventory(x) for x in pair),Counter())
                    job=copy.deepcopy(t['data']['job']);job['parts']=[p for p in job['parts'] if counts[p['id']]>0]
                    for p in job['parts']:p['quantity']=counts[p['id']]
                    job['stocks'][0]['count']=None
                    layout={'version':1,'units':job['units'],'sheets':[],'placements':[]};copies=Counter()
                    for i,members in enumerate(pair):
                        if not members:continue
                        sid=f'sheet-{i}';layout['sheets'].append({'id':sid,'stock_id':job['stocks'][0]['id']})
                        for p in members:
                            layout['placements'].append({'part_id':p['part_id'],'copy_index':copies[p['part_id']],
                                'sheet_id':sid,'transform':p['transform']});copies[p['part_id']]+=1
                    validate(job,layout,True,None,origin|{'stage':stage,'component_geometry_only':True})
                recrop=[e['data'] for e in t['events'] if e['stage']=='recrop_exit']
                lowered=[e['data'] for e in t['events'] if e['stage']=='lowering_exit']
                if recrop and lowered:
                    before=Counter(reader.pose(p) for p in recrop[0]['pair'][1])
                    after=Counter(reader.pose(p) for p in lowered[0]['pair'][1])
                    changed=sum((before-after).values());assert changed==sum((after-before).values())
                    parts={p['id']:p for p in t['data']['job']['parts']}
                    def top(members):
                        values=[]
                        for p in members:
                            tr=p['transform'];c=math.cos(tr['rotation_radians']);s=math.sin(tr['rotation_radians']);m=-1 if tr['mirrored'] else 1
                            ymax=max(m*s*x+c*y+tr['translation'][1] for g in parts[p['part_id']]['geometry'] for x,y in g['outer'])
                            values.append({'part_id':p['part_id'],'top_mm':ymax,'transform':tr})
                        maximum=max(v['top_mm'] for v in values)
                        return maximum,[v for v in values if v['top_mm']>=maximum-1e-7]
                    top_before,owners_before=top(recrop[0]['pair'][1]);top_after,owners_after=top(lowered[0]['pair'][1])
                    source_rows.append(origin|{'pair_outcome':t['outcome'],'changed_source_poses_during_lowering':changed,
                        'source_top_before_lowering_mm':top_before,'source_top_after_lowering_mm':top_after,
                        'source_top_reduction_mm':top_before-top_after,'lowering_seconds':lowered[0]['lowering_seconds'],
                        'before_owners':owners_before,'after_owners':owners_after})
    report={'all_checks_passed':True,'CLI_checks':len(records),'valid_layouts':sum(r['valid'] for r in records),
        'expected_invalid_layouts':sum(not r['valid'] for r in records),'filled_outer_pairs':pairs,
        'whole_job_material_recomputations':len(material_rows),'all_material_values_exact':True,
        'all_nonselected_sheets_exact_by_trace_reader':True,'component_scope':'Pair quantities and original full stock geometry; original whole-job stock counts and internal crop validation remain separate.',
        'source_helpers_sha256':sources,'shapely_version':shapely.__version__,'tolerance_mm':1e-7,
        'new_searches':0,'records':records,'material_reconstructions':material_rows,'source_lowering':source_rows}
    write(out/'checks.json',report);shutil.copyfile(__file__,out/'check.py')
    print(json.dumps({k:report[k] for k in ['CLI_checks','valid_layouts','filled_outer_pairs','whole_job_material_recomputations']}))
except BaseException:
    write(out/'failure.json',{'error':traceback.format_exc(),'completed_records':records});raise
