"""Check actual seed movement and repair geometry from originals; no new searches."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import ast,itertools,json,math,shutil,subprocess,sys
import shapely
from shapely.geometry import Polygon
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-free-return-observer-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
sys.path.insert(0,str(root/'scripts'));import h5_free_return_observer as observer
assert load(out/'verification.json')['all_original_archives_verified'] and load(out/'layout-checks.json')['all_checks_passed']
cli=root/'target/release/nestbolt.exe';expected='97de6a34f17760ca30230742e716b3e74940f1a2ede71453ecb3b13bac73dc2b';assert digest(cli)==expected
folder=out/'material-trials';folder.mkdir();trials=[];sources=[];causes=Counter();parent_sources={};tolerance=1e-7
for name,functions in [('output/check_h5_larger_stage_layouts.py',['filled_geometry']),('output/inspect_h5_neutral_heights.py',['rounded','heights']),('output/check_h5_exchange_failure_details.py',['inspect_source'])]:
 p=root/name;tree=ast.parse(p.read_text(encoding='utf-8'));parent_sources[name]=digest(p)
 for fn in functions:
  node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==fn)
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(p),'exec'))
def write(p,value):
 with p.open('x',encoding='utf-8',newline='\n') as stream:json.dump(value,stream,indent=2);stream.write('\n')
for row in load(out/'results.json')['records']:
 traces=row['diagnosis']['traces'];checked=observer.check_traces(traces,row['stats']);causes.update(checked['reason_counts'])
 for d in checked['attempt_observations']:
  base=traces[d['invocation']]['baseline'];job=base['job'];seed=d['return_seed_detail'];repair=d['repair_detail'];detail=d['material_detail']
  common={k:row[k] for k in ['job','kerf_mm']};common.update({k:d[k] for k in ['invocation','attempt_index','choice_index','outcome','reason']})
  if detail is not None:
   case=folder/f"{row['job']}-k{row['kerf_mm']}-i{d['invocation']}-a{d['attempt_index']}";case.mkdir()
   write(case/'job.json',job);write(case/'layout.json',detail['layout']);write(case/'record.json',d)
   args=[str(cli),'validate','--job',str(case/'job.json'),'--layout',str(case/'layout.json')]
   result=subprocess.run(args,capture_output=True,timeout=60);(case/'stdout.json').write_bytes(result.stdout);(case/'stderr.log').write_bytes(result.stderr)
   write(case/'command.json',{'command':args,'exit_code':result.returncode});validated=json.loads(result.stdout)
   assert result.returncode==0 and validated['valid'] and validated['metrics']==detail['metrics']
   geometry=filled_geometry(job,detail['layout']);material,highest,poses,charged=heights(job,detail['layout']);assert material==detail['metrics']['material_area']
   trials.append({**common,'path':case.relative_to(out).as_posix(),'baseline_material':base['metrics']['material_area'],
    'trial_material':material,'material_change':material-base['metrics']['material_area'],
    'baseline_sheets':base['metrics']['sheets_used'],'trial_sheets':detail['metrics']['sheets_used'],'sheets_with_original_height_owners':charged,**geometry})
  stock_id=next(s['stock_id'] for s in base['layout']['sheets'] if s['id']==base['source_sheet']);stock=next(s for s in job['stocks'] if s['id']==stock_id)
  contained=seed['source_before']+seed['contained'];placed=seed['source_before']+seed['placed']
  assert Counter(p['part_id'] for p in contained)==Counter(p['part_id'] for p in placed)
  movements=[]
  for a,b in zip(seed['contained'],seed['placed']):
   before=inspect_source(job,[a],stock);after=inspect_source(job,[b],stock)
   movements.append({'part_id':a['part_id'],'translation_changed':a['transform']['translation']!=b['transform']['translation'],
    'before_highest_original_vertex_mm':before['highest_original_vertex_mm'],'after_highest_original_vertex_mm':after['highest_original_vertex_mm'],
    'height_change_mm':after['highest_original_vertex_mm']-before['highest_original_vertex_mm']})
  record={**common,'source_loss':repair['source_loss'],'work_delta':d['work_delta'],'returned_members':movements,
   'contained':inspect_source(job,contained,stock),'seeded':inspect_source(job,placed,stock),
   'after_repair':inspect_source(job,repair['source_after'],stock) if repair['source_after'] is not None else None}
  sources.append(record)
assert digest(cli)==expected
changed=sum(m['translation_changed'] for s in sources for m in s['returned_members']);lowered=sum(m['height_change_mm']<0 for s in sources for m in s['returned_members'])
result={'all_checks_passed':True,'reason_counts':dict(causes),'validated_material_trials':len(trials),
 'accepted_trials':sum(t['outcome']=='accepted' for t in trials),'all_trial_metrics_exact':True,'all_trial_material_reconstructed':True,
 'return_sources_inspected':len(sources),'returned_members':sum(len(s['returned_members']) for s in sources),
 'translated_return_members':changed,'lowered_return_members':lowered,'trials':trials,'sources':sources,
 'CLI_sha256':expected,'shapely_version':shapely.__version__,'absolute_clearance_tolerance_mm':tolerance,
 'reused_functions_sha256':parent_sources,'production_changed':False,'new_searches':0,'quality_claim':False,
 'limits':'Original filled outer geometry and nominal stock bounds only; source snapshots are not claimed valid. This does not reconstruct cropped proxy boundaries, loss weights or unlogged pilot trajectories.'}
write(out/'seed-detail-checks.json',result);shutil.copyfile(__file__,out/'check-seed-details.py')
print(json.dumps({k:v for k,v in result.items() if k not in ['trials','sources','reused_functions_sha256']}))
