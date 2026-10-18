"""Audit captured failure details using saved original geometry; no searches."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import ast, copy, itertools, json, math, shutil, subprocess, sys
import shapely
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-exchange-failure-observer-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(root/'scripts'));import h5_exchange_failure_observer as observer
assert load(out/'verification.json')['all_original_archives_verified']
assert load(out/'layout-checks.json')['all_checks_passed']
cli=root/'target/release/nestbolt.exe';expected='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b';assert digest(cli)==expected
folder=out/'failed-trials';folder.mkdir();trials=[];sources=[];causes=Counter();parent_sources={}
tolerance=1e-7
for name,functions in [('output/check_h5_larger_stage_layouts.py',['filled_geometry']),('output/inspect_h5_neutral_heights.py',['rounded','heights'])]:
    p=root/name;tree=ast.parse(p.read_text(encoding='utf-8'));parent_sources[name]=digest(p)
    for fn in functions:
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==fn)
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'))

def write(p,value):
    with p.open('x',encoding='utf-8',newline='\n') as stream:json.dump(value,stream,indent=2);stream.write('\n')

def inspect_source(job,poses,stock):
    parts={p['id']:p for p in job['parts']};shapes=[]
    for p in poses:
        part=parts[p['part_id']];assert len(part['geometry'])==1
        shape=Polygon(part['geometry'][0]['outer']);assert shape.is_valid and shape.area>0
        t=p['transform'];c=math.cos(t['rotation_radians']);s=math.sin(t['rotation_radians']);m=-1 if t['mirrored'] else 1
        shape=affine_transform(shape,[m*c,-s,m*s,c,*t['translation']]);assert shape.is_valid
        shapes.append(shape)
    violations=[];minimum=math.inf;count=0
    for i,j in itertools.combinations(range(len(shapes)),2):
        a,b=shapes[i],shapes[j];count+=1;slack=a.distance(b)-job['clearance'];minimum=min(minimum,slack)
        overlap=a.intersection(b).area
        if not a.disjoint(b) or slack < -tolerance:
            violations.append({'indices':[i,j],'families':[poses[i]['part_id'],poses[j]['part_id']],
                'clearance_slack_mm':slack,'overlap_area_mm2':overlap})
    outside=[i for i,p in enumerate(shapes) if p.bounds[0]<-tolerance or p.bounds[1]<-tolerance or p.bounds[2]>stock['width']+tolerance or p.bounds[3]>stock['height']+tolerance]
    return {'same_sheet_pairs':count,'minimum_clearance_slack_mm':minimum if count else None,
        'pair_violations':violations,'outside_nominal_stock_indices':outside,
        'highest_original_vertex_mm':max(p.bounds[3] for p in shapes),
        'limits':'Original filled outers and nominal stock bounds only; excludes cropped separator boundary and proxy-loss weighting.'}

for row in load(out/'results.json')['records']:
    traces=row['diagnosis']['traces'];checked=observer.check_traces(traces,row['stats']);causes.update(checked['failure_reason_counts'])
    for d in checked['failure_details']:
        base=traces[d['invocation']]['baseline'];job=base['job'];detail=d['detail']
        common={'kerf_mm':row['kerf_mm'],'invocation':d['invocation'],'attempt_index':d['attempt_index'],'choice_index':d['choice_index'],'reason':d['reason']}
        if d['outcome']=='material_guard_or_expiry':
            case=folder/f"k{row['kerf_mm']}-i{d['invocation']}-a{d['attempt_index']}";case.mkdir()
            write(case/'job.json',job);write(case/'layout.json',detail['layout']);write(case/'record.json',d)
            args=[str(cli),'validate','--job',str(case/'job.json'),'--layout',str(case/'layout.json')]
            result=subprocess.run(args,capture_output=True,timeout=60)
            (case/'stdout.json').write_bytes(result.stdout);(case/'stderr.log').write_bytes(result.stderr)
            write(case/'command.json',{'command':args,'exit_code':result.returncode})
            validated=json.loads(result.stdout);assert result.returncode==0 and validated['valid']
            assert validated['metrics']==detail['metrics']
            geometry=filled_geometry(job,detail['layout'])
            material,highest,poses,charged=heights(job,detail['layout']);assert material==detail['metrics']['material_area']
            trials.append({**common,'path':case.relative_to(out).as_posix(),'baseline_material':base['metrics']['material_area'],
                'trial_material':material,'material_change':material-base['metrics']['material_area'],
                'baseline_sheets':base['metrics']['sheets_used'],'trial_sheets':detail['metrics']['sheets_used'],
                'sheets_with_original_height_owners':charged,**geometry})
        elif d['outcome']=='source_repair_or_expiry':
            trace=traces[d['invocation']];choice=trace['choice_poses'][d['choice_index']]
            removed=Counter(observer.pose_key(p) for p in choice)
            initial=[]
            for p in base['layout']['placements']:
                if p['sheet_id']!=base['source_sheet']:continue
                q={'part_id':p['part_id'],'transform':p['transform']};key=observer.pose_key(q)
                if removed[key]:removed[key]-=1
                else:initial.append(q)
            assert not +removed;initial+=detail['returned_initial']
            assert Counter(p['part_id'] for p in initial)==Counter(p['part_id'] for p in detail['source_after'])
            stock_id=next(s['stock_id'] for s in base['layout']['sheets'] if s['id']==base['source_sheet'])
            stock=next(s for s in job['stocks'] if s['id']==stock_id)
            sources.append({**common,'source_loss':detail['source_loss'],'initial':inspect_source(job,initial,stock),
                'after':inspect_source(job,detail['source_after'],stock)})
assert digest(cli)==expected
result={'all_checks_passed':True,'failure_reason_counts':dict(causes),'validated_material_trials':len(trials),
    'all_trial_metrics_exact':True,'all_trial_material_reconstructed':True,'source_failures_inspected':len(sources),
    'trials':trials,'sources':sources,'CLI_sha256':expected,'shapely_version':shapely.__version__,
    'absolute_clearance_tolerance_mm':tolerance,'reused_functions_sha256':parent_sources,
    'production_changed':False,'new_searches':0,'quality_claim':False}
write(out/'failure-detail-checks.json',result);shutil.copyfile(__file__,out/'check-failure-details.py')
print(json.dumps({k:v for k,v in result.items() if k not in ['trials','sources','reused_functions_sha256']}))
