"""Necessary area bounds for saved assignments, never a global infeasibility claim."""
from pathlib import Path
from hashlib import sha256
import json, shutil, zipfile
import shapely
from shapely.geometry import Polygon
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-source-frontier-pilot-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
boundaries=load(out/'final-boundaries.json');rows=[]
assert boundaries['all_saved_layout_checks_passed'] and load(out/'filled-outer-audit.json')['all_holes_reserved']
for row in boundaries['records']:
 archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
 with zipfile.ZipFile(archive) as z:
  job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
 parts={p['id']:p for p in job['parts']}
 sheet=next(s for s in layout['sheets'] if s['id']==row['credited_sheet'])
 stock=next(s for s in job['stocks'] if s['id']==sheet['stock_id'])
 assert job['units']=='mm' and not stock['outline'] and not stock['defects']
 assert all(len(p['geometry'])==1 for p in job['parts'])
 polygons={k:Polygon(p['geometry'][0]['outer']) for k,p in parts.items()}
 assert all(p.is_valid and p.area>0 for p in polygons.values())
 area=sum(polygons[p['part_id']].area for p in layout['placements'] if p['sheet_id']==row['credited_sheet'])
 e=job['edge_clearance'];m=stock['margins']
 capacity=max(0,stock['width']-m['left']-m['right']-2*e)*max(0,row['required_used_height_mm']-m['top']-m['bottom']-2*e)
 assert capacity>0
 # Cross-check polygon area independently with the shoelace formula.
 def shoelace(points):
  return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1])))/2
 independent=sum(shoelace(parts[p['part_id']]['geometry'][0]['outer']) for p in layout['placements'] if p['sheet_id']==row['credited_sheet'])
 assert abs(area-independent)<=max(1e-6,area*1e-12)
 rows.append({k:row[k] for k in ['job','kerf_mm','seed','archive','archive_sha256','credited_sheet','required_used_height_mm']} |
  {'filled_outer_area_mm2':area,'target_usable_rectangle_mm2':capacity,'area_fraction':area/capacity,
   'net_area_that_must_leave_this_sheet_mm2_at_least':max(0,area-capacity),
   'same_inventory_cannot_fit_this_target_by_area':area>capacity+1e-6})
failed=[r for r in rows if r['same_inventory_cannot_fit_this_target_by_area']]
assert len(rows)==len(boundaries['records'])
record={'all_saved_assignment_checks_passed':True,'final_boundaries_sha256':digest(out/'final-boundaries.json'),
 'shapely_version':shapely.__version__,'shoelace_crosscheck_passed':True,'records':rows,
 'same_inventory_area_failures':len(failed),'new_searches':0,
 'method':'Sum original filled outer-ring areas on the currently credited sheet, with hole interiors reserved. Compare with the required rectangular prefix after stock margins and edge clearance. Kerf between parts is omitted, making this a necessary rather than sufficient capacity condition.',
 'limitations':'Assignments flagged by this check exceed that conditional target area. They need a smaller inventory on this sheet or a different sheet/offcut arrangement. This does not prove a whole job infeasible. Area below capacity does not establish packability, and these final snapshots do not expose intermediate repair behavior. The 1e-6 mm² comparison slack is arithmetic tolerance, not a relaxed geometry acceptance rule.'}
with (out/'fixed-inventory-area.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(record,f,indent=2);f.write('\n')
shutil.copyfile(__file__,out/'check-fixed-inventory-area.py')
print(json.dumps({'saved_assignments':len(rows),'conditional_area_failures':len(failed),'new_searches':0}))
