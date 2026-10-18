"""Describe the final height gap using saved layouts; do not search or infer feasibility."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json, math, shutil, statistics, zipfile
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-assignment-bridge-pilot-20261018'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
result=load(out/'results.json')
assert load(out/'verification.json')['all_original_archives_verified']
assert load(out/'filled-outer-audit.json')['all_holes_reserved']
pairs=result['summary']['pairs'];records=[]
for pair in pairs:
 if pair['candidate_within_original_material_limit']:continue
 rows=[r for r in result['records'] if (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
 normal=[r['metrics']['material_area'] for r in rows if r['arm']=='normal']
 assert len(normal)==3
 target=statistics.median(normal)*1.01
 for row in rows:
  if row['arm']!='candidate':continue
  archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
  with zipfile.ZipFile(archive) as z:
   job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
   assert sha256(z.read('nested/layout.json')).hexdigest()==row['layout_sha256']
  assert job['units']=='mm' and all(not s['outline'] for s in job['stocks'])
  stocks={s['id']:s for s in job['stocks']}
  full=sum(stocks[s['stock_id']]['width']*stocks[s['stock_id']]['height'] for s in layout['sheets'])
  assert math.isclose(full,row['metrics']['full_stock_area'],rel_tol=0,abs_tol=1e-6)
  last=row['metrics']['last_sheet_id'];sheet=next(s for s in layout['sheets'] if s['id']==last)
  stock=stocks[sheet['stock_id']];width=stock['width'];height=stock['height']
  # This is the required height if this same sheet continues to provide the
  # credited offcut, with the stock inventory and all other sheets unchanged.
  required_height=height-(full-target)/width
  threshold=required_height-job['edge_clearance']-stock['margins']['top']
  parts={p['id']:p for p in job['parts']};tops=[]
  for placement in layout['placements']:
   if placement['sheet_id']!=last:continue
   t=placement['transform'];s=math.sin(t['rotation_radians']);c=math.cos(t['rotation_radians'])
   m=-1 if t['mirrored'] else 1
   ymax=max(m*s*x+c*y+t['translation'][1] for g in parts[placement['part_id']]['geometry'] for x,y in g['outer'])
   tops.append({'part_id':placement['part_id'],'copy_index':placement['copy_index'],'outline_top_mm':ymax})
  current=max(t['outline_top_mm'] for t in tops)+job['edge_clearance']+stock['margins']['top']
  # Original validator rounds coordinates/offcut upward on its micrometre grid.
  assert abs(min(height,current)-row['metrics']['last_sheet_used_height'])<=2e-6
  assert abs(full-width*(height-row['metrics']['last_sheet_used_height'])-row['metrics']['material_area'])<=1e-6
  crossing=[p for p in tops if p['outline_top_mm']>threshold+2e-6]
  records.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'seed':row['seed'],
   'archive':row['archive'],'archive_sha256':row['archive_sha256'],'layout_sha256':row['layout_sha256'],
   'credited_sheet':last,'stock_width_mm':width,'current_used_height_mm':row['metrics']['last_sheet_used_height'],
   'target_material_mm2':target,'required_used_height_mm':required_height,
   'height_reduction_mm':row['metrics']['last_sheet_used_height']-required_height,
   'required_outline_top_mm':threshold,'crossing_parts':crossing,
   'crossing_count':len(crossing),'crossing_families':dict(Counter(p['part_id'] for p in crossing)),
   'current_layout_satisfies_pair_median_target':row['metrics']['material_area']<=target})
assert len(records)==3*sum(not p['candidate_within_original_material_limit'] for p in pairs)
mechanical=[r for r in records if r['job'].startswith('m-mechanical-')]
summary={'mechanical_layouts':len(mechanical),
 'mechanical_crossing_count_range':[min(r['crossing_count'] for r in mechanical),max(r['crossing_count'] for r in mechanical)],
 'mechanical_height_reduction_mm_range':[min(r['height_reduction_mm'] for r in mechanical),max(r['height_reduction_mm'] for r in mechanical)]}
record={'all_saved_layout_checks_passed':True,'results_sha256':digest(out/'results.json'),
 'method':'For every candidate layout in a failed pair, use 1.01 times the matched normal material median. With its existing stock inventory and credited offcut sheet, derive the required rectangular prefix height. Independently transform every original outer-ring vertex on that sheet and count copies above that target. Verify the current used height and material against the saved validator metrics.',
 'boundary_tolerance_mm':2e-6,'geometry_acceptance_tolerance_changed':False,
 'limitations':'A conditional description of final geometry, not a bound on achievable packing or a required move count for all algorithms. A different sheet could supply the offcut; collective compression or reassignment can change the conclusion. No target packing is constructed or proven feasible. These saved final layouts do not reveal individual repair losses, durations or accepted-move gains.',
 'new_searches':0,'summary':summary,'records':records}
with (out/'final-boundaries.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(record,f,indent=2);f.write('\n')
shutil.copyfile(__file__,out/'check-final-boundaries.py')
print(json.dumps(summary))
