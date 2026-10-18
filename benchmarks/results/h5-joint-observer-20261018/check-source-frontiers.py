"""Read exact selected copies and the next source boundary; construct no packing."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,math,shutil,sys
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-joint-observer-20261018'
sys.path.insert(0,str(root/'scripts'));import h5_joint_trace as reader
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
assert load(out/'geometry-checks/checks.json')['all_checks_passed']
observed=load(out/'observed-exchanges.json');rows=[]
for forest in load(out/'trace-forests.json'):
    traces=forest['traces'];reader.check_traces(traces);by={t['id']:t for t in traces}
    for attempt in [t for t in traces if t['kind']=='attempt']:
        base=by[attempt['parent']]['data'];job=base['job'];parts={p['id']:p for p in job['parts']}
        sid=f"sheet-{base['frozen_count']+attempt['data']['source_active_sheet']}"
        source=[p for p in base['baseline']['placements'] if p['sheet_id']==sid]
        selected=Counter(reader.pose(p) for p in attempt['data']['incoming'])
        def top(p):
            t=p['transform'];s=math.sin(t['rotation_radians']);c=math.cos(t['rotation_radians']);m=-1 if t['mirrored'] else 1
            return max(m*s*x+c*y+t['translation'][1] for g in parts[p['part_id']]['geometry'] for x,y in g['outer'])
        remaining=[];removed=[]
        for p in source:
            key=reader.pose(p)
            if selected[key]>0:selected[key]-=1;removed.append(p)
            else:remaining.append(p)
        assert not +selected and len(removed)==len(attempt['data']['incoming'])
        original_top=max(top(p) for p in source)
        assert remaining # all captured cases retain a non-empty source
        exposed_top=max(top(p) for p in remaining)
        source_sheet=next(s for s in base['baseline']['sheets'] if s['id']==sid)
        stock=next(s for s in job['stocks'] if s['id']==source_sheet['stock_id'])
        assert not stock['outline'] and not stock['defects']
        detail=next(a for a in observed['attempts'] if a['archive']==forest['archive'] and a['attempt_id']==attempt['id'])
        rows.append({'archive':forest['archive'],'job':forest['job'],'kerf_mm':forest['kerf_mm'],
            'attempt_id':attempt['id'],'outcome':attempt['outcome'],'resolved_reason':detail['resolved_reason'],
            'source_sheet':sid,'credited_source':sid==base['metrics']['last_sheet_id'],
            'selected_exact_physical_copies':attempt['data']['incoming'],
            'original_source_top_mm':original_top,'next_top_after_selected_removal_mm':exposed_top,
            'exposed_band_height_mm':original_top-exposed_top,
            'gross_band_area_mm2':stock['width']*(original_top-exposed_top),
            'observed_material_gain_mm2':detail['material_gain_mm2'],
            'target_packing_constructed_or_proven_feasible':False})
assert len(rows)==observed['summary']['attempts']
positive=[r for r in rows if r['exposed_band_height_mm']>1e-7]
record={'all_saved_selected_copy_checks_passed':True,'source_trace_sha256':digest(out/'trace-forests.json'),
    'geometry_checks_sha256':digest(out/'geometry-checks/checks.json'),'attempts':len(rows),
    'attempts_exposing_lower_source_boundary':len(positive),
    'exposed_band_range_mm':[min(r['exposed_band_height_mm'] for r in positive),max(r['exposed_band_height_mm'] for r in positive)],
    'records':rows,'new_searches':0,
    'limitations':'Exact original physical poses identify the removed copies. The next boundary describes only the source after removing them, before returning displaced members. It does not establish that the returned parts can fit, that joint repair will find a layout, or that the whole-job target is reachable. The band area is a conditional geometric opportunity, not an observed or guaranteed saving.'}
with (out/'source-frontiers.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(record,f,indent=2);f.write('\n')
shutil.copyfile(__file__,out/'check-source-frontiers.py')
print(json.dumps({k:record[k] for k in ['attempts','attempts_exposing_lower_source_boundary','exposed_band_range_mm']}))
