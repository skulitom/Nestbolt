"""Read-only whole-job necessary area bounds; never a packability claim."""
from pathlib import Path
from hashlib import sha256
import json, shutil, statistics, zipfile
import shapely
from shapely.geometry import Polygon
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-source-frontier-pilot-20261018'
load=lambda p:json.loads(p.read_bytes())
digest=lambda p:sha256(p.read_bytes()).hexdigest()
r=load(out/'results.json')
assert load(out/'verification.json')['all_original_archives_verified']
assert load(out/'filled-outer-audit.json')['all_holes_reserved']
records=[]
for pair in r['summary']['pairs']:
    selected=[a for a in r['records'] if (a['job'],a['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    target=1.01*statistics.median(a['metrics']['material_area'] for a in selected if a['arm']=='normal')
    jobs=[];sources=[]
    for row in selected:
        if row['arm']!='candidate':continue
        path=out/row['archive'];assert digest(path)==row['archive_sha256']
        with zipfile.ZipFile(path) as z:
            raw=z.read('nested/job.json');job=json.loads(raw)
        jobs.append(job);sources.append({'archive':row['archive'],'archive_sha256':row['archive_sha256'],
            'job_sha256':sha256(raw).hexdigest()})
    assert len(jobs)==3 and all(j==jobs[0] for j in jobs)
    job=jobs[0]
    assert job['units']=='mm' and all(len(p['geometry'])==1 for p in job['parts'])
    total=independent=0
    for part in job['parts']:
        points=part['geometry'][0]['outer'];polygon=Polygon(points)
        assert polygon.is_valid and polygon.area>0
        total+=part['quantity']*polygon.area
        independent+=part['quantity']*abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(points,points[1:]+points[:1])))/2
    assert abs(total-independent)<=max(1e-6,total*1e-12)
    records.append({'job':pair['job'],'kerf_mm':pair['kerf_mm'],'filled_outer_area_mm2':total,
        'normal_median_material_limit_mm2':target,'fraction_of_material_limit':total/target,
        'necessary_area_exceeds_material_limit':total>target+1e-6,'sources':sources})
record={'all_saved_job_checks_passed':True,'results_sha256':digest(out/'results.json'),
    'shapely_version':shapely.__version__,'shoelace_crosscheck_passed':True,'records':records,
    'whole_job_area_obstructions':sum(a['necessary_area_exceeds_material_limit'] for a in records),
    'new_searches':0,
    'method':'Sum every original filled outer-ring area multiplied by quantity, with no hole subtraction. These mutually disjoint filled shapes must consume at least this area. Compare with 1.01 times the matched normal three-seed median material area.',
    'limitations':'This omits margins, kerf, defects, packing inefficiency and stock combinations. A bound below the limit does not prove any compliant packing exists. It does not contradict the stronger conditional fixed-inventory bounds or establish global infeasibility.'}
with (out/'whole-job-area.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(record,f,indent=2);f.write('\n')
shutil.copyfile(__file__,out/'check-whole-job-area.py')
print(json.dumps({'pairs':len(records),'whole_job_area_obstructions':record['whole_job_area_obstructions']}))
