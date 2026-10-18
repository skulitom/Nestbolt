"""Audit saved attempt geometry; no optimizer invocation or quality rescoring."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import itertools,json,math,shutil,sys,zipfile
import shapely
from shapely.geometry import Polygon,box
from shapely.affinity import affine_transform
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-return-capacity-diagnosis-20261017'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()

def summarize(polys,boundary):
    assert boundary.is_valid and boundary.area>0
    assert all(p.is_valid and not p.is_empty and p.area>0 for p in polys)
    outside=[p.difference(boundary).area for p in polys]
    pairs=[(i,j,a.intersection(b).area) for (i,a),(j,b) in itertools.combinations(enumerate(polys),2)]
    # This only groups diagnostic magnitudes; it is not the validator tolerance.
    # All raw pair/intersection and outside values remain in the output.
    return {'container_area_mm2':boundary.area,'sum_part_area_mm2':math.fsum(p.area for p in polys),
        'area_excess_mm2':math.fsum(p.area for p in polys)-boundary.area,
        'outside_area_sum_mm2':math.fsum(outside),'outside_area_by_item_mm2':outside,
        'pair_intersection_sum_mm2':math.fsum(row[2] for row in pairs),
        'positive_pair_intersections_mm2':[row for row in pairs if row[2]>0],
        'tested_pairs':len(pairs),'part_bounds':[p.bounds for p in polys]}

def analyze_layout(value,job):
    collision=[Polygon(item['polygon']) for item in value['items']]
    search=summarize(collision,Polygon(value['container']))
    stock=job['stocks'][0];m=stock['margins'];edge=job['edge_clearance']
    physical=box(m['left']+edge,m['bottom']+edge,stock['width']-m['right']-edge,stock['height']-m['top']-edge)
    originals=[]
    for item in value['items']:
        part=job['parts'][item['external_id']];assert len(part['geometry'])==1
        outer=Polygon(part['geometry'][0]['outer']);assert outer.is_valid and outer.area>0
        t=item['public_transform'];c=math.cos(t['rotation_radians']);s=math.sin(t['rotation_radians']);mirror=-1 if t['mirrored'] else 1
        originals.append(affine_transform(outer,[mirror*c,-s,mirror*s,c,*t['translation']]))
    full=summarize(originals,physical)
    return {'search_collision_polygons':search,'original_filled_outer_rings_vs_full_stock':full,
        'part_ids':[job['parts'][item['external_id']]['id'] for item in value['items']]}

if __name__=='__main__':
    results=load(out/'results.json');assert results['all_valid'];rows=[]
    for record in results['records']:
        archive=out/record['archive'];assert digest(archive)==record['archive_sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            case=json.loads(z.read('case.json'))
            assert all(sha256(z.read(name)).hexdigest()==expected for name,expected in case['artifacts'].items())
            job=json.loads(z.read('nested/job.json'));assert len(job['stocks'])==1
            traces=[json.loads(line.removeprefix('OBSTRUCTION_DIAG ')) for line in z.read('search-stderr.log').decode().splitlines() if line.startswith('OBSTRUCTION_DIAG ')]
        for ti,trace in enumerate(traces):
            for ai,attempt in enumerate(trace['attempts']):
                context=trace['contexts'][attempt['context_index']]
                states={name:analyze_layout(attempt[name],job) for name in ['source_initial','source_repaired','receiver_initial','receiver_repaired'] if attempt[name] is not None}
                before=analyze_layout(context['source_after_removal'],job)
                initial=states['source_initial'];search=initial['search_collision_polygons'];full=initial['original_filled_outer_rings_vs_full_stock']
                rows.append({'job':record['job'],'kerf_mm':record['kerf_mm'],'archive':record['archive'],'trace_index':ti,'attempt_index':ai,
                    'outcome':attempt['outcome'],'victims':attempt['victims'],'frame_mode':attempt['frame']['mode'],
                    'source_search_area_ratio':search['sum_part_area_mm2']/search['container_area_mm2'],
                    'source_full_stock_area_ratio':full['sum_part_area_mm2']/full['container_area_mm2'],
                    'source_remaining_before_return':before,'states':states})
    report={'method':__doc__,'source_sha256':digest(Path(__file__)),'shapely_version':shapely.__version__,
        'results_sha256':digest(out/'results.json'),'attempts':len(rows),'outcomes':dict(Counter(r['outcome'] for r in rows)),
        'source_search_area_ratio_range':[min(r['source_search_area_ratio'] for r in rows),max(r['source_search_area_ratio'] for r in rows)],
        'source_full_stock_area_ratio_range':[min(r['source_full_stock_area_ratio'] for r in rows),max(r['source_full_stock_area_ratio'] for r in rows)],
        'overfull_shortened_search_assignments':sum(r['source_search_area_ratio']>1 for r in rows),
        'overfull_physical_full_sheet_assignments':sum(r['source_full_stock_area_ratio']>1 for r in rows),
        'original_holes_filled':True,'all_raw_positive_intersections_and_outside_areas_retained':True,
        'simple_area_bound_below_one_proves_feasibility':False,'global_infeasibility_claim':False,
        'new_searches':0,'quality_claim':False,'H5_complete':False,'records':rows}
    (out/'independent-capacity-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    shutil.copyfile(__file__,out/'audit-capacity.py')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}))
