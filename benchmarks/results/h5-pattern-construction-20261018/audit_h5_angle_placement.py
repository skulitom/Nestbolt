from pathlib import Path
from collections import Counter
import copy,gzip,importlib.util,json
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit',ROOT/'output/audit_h5_pattern_constructions.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
base=audit.base;load=base.load;write=base.write
out=ROOT/'output/h5-angle-pattern-placement-20261018'
assert load(ROOT/'output/h5-pattern-audit-20261018/checks.json')['all_checks_passed']
records=[]
for folder in sorted(out.glob('m-*')):
    job=load(folder/'job.json');patterns=load(folder/'patterns.json');selection=load(folder/'selection.json')
    old=load(ROOT/'output/h5-mixed-pattern-catalog-20261018'/folder.name/'patterns.json')
    radial=load(ROOT/'output/h5-radial-angle-diagnosis-20261018'/folder.name/'patterns.json')
    audited_members={json.dumps(p['members'],sort_keys=True) for p in list(old.values())+radial}
    assert all(json.dumps(p['members'],sort_keys=True) in audited_members for p in patterns.values())
    quantities=Counter();area=0;meta=load(folder/'metadata.json');g=meta['block_spacing']
    for name,n in selection['selected'].items():
        for p in patterns[name]['members']:quantities[p['part_id']]+=n
        area+=n*(patterns[name]['width']+g)*(patterns[name]['height']+g)
    expected=Counter({p['id']:p['quantity'] for p in job['parts']})
    assert quantities==expected and abs(area-selection['padded_area'])<=1e-6
    if not selection['area_possible']:continue
    target=load(folder/'conditional-target.json');count=0
    with gzip.open(folder/'attempts.jsonl.gz','rt',encoding='utf-8') as f:
        for line in f:
            row=json.loads(line);count+=1;assert row['attempt']==count and row['left']
            layout=base.layout_of(job,patterns,row['placed'])
            qty=Counter(p['part_id'] for p in layout['placements']);missing=Counter(m['part_id'] for name in row['left'] for m in patterns[name]['members'])
            assert qty+missing==expected
            part_job=copy.deepcopy(job);part_job['parts']=[p for p in part_job['parts'] if qty[p['id']]]
            for p in part_job['parts']:p['quantity']=qty[p['id']]
            check=audit.geometry(part_job,layout);parts={p['id']:p for p in job['parts']};st=job['stocks'][0]
            for p in layout['placements']:
                if p['sheet_id']!='sheet-1':continue
                top=base.gap.pose(audit.Polygon(parts[p['part_id']]['geometry'][0]['outer']),p['transform']).bounds[3]
                assert top+st['margins']['top']+job['edge_clearance']<=target['required_used_height_mm']+1e-7
            records.append({'case':folder.name,'attempt':count,'missing':sum(missing.values()),**check})
    assert count==load(folder/'result.json')['attempts']==324
assert len(records)==648
write(out/'independent-checks.json',{'all_checks_passed':True,'partial_placement_attempts':len(records),
    'filled_outer_pairs':sum(r['pairs'] for r in records),'all_patterns_match_prior_independent_component_checks':True,
    'original_quantities_accounted_with_explicit_missing_copies':True,'full_layouts_found':0,
    'absolute_clearance_tolerance_mm':1e-7,'records':records})
print(json.dumps({'partial_placement_attempts':len(records),'filled_outer_pairs':sum(r['pairs'] for r in records)}))
