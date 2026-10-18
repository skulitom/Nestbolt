"""Read saved validated neutral layouts; inspect charged heights without new searches."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,math,shutil
root=Path(__file__).resolve().parents[1];old=root/'benchmarks/results/h5-exact-state-20261018'
out=root/'output/h5-neutral-height-review-20261018';out.mkdir()
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
audit=load(old/'layout-checks.json');assert audit['all_checks_passed']
def rounded(x):return math.floor(x+0.5) if x>=0 else math.ceil(x-0.5)
def heights(job,layout):
    assert job['units']=='mm'
    parts={p['id']:p for p in job['parts']};stocks={s['id']:s for s in job['stocks']}
    assert all(not s['outline'] and not s['defects'] for s in stocks.values())
    highest={};owners={};poses=Counter()
    for p in layout['placements']:
        t=p['transform'];sin=math.sin(t['rotation_radians']);cos=math.cos(t['rotation_radians'])
        ys=[]
        for polygon in parts[p['part_id']]['geometry']:
            for x,y in polygon['outer']:
                if t['mirrored']:x=-x
                ys.append(rounded((x*sin+y*cos+t['translation'][1])*1_000_000.0))
        top=max(ys);sheet=p['sheet_id']
        if sheet not in highest or top>highest[sheet]:highest[sheet]=top;owners[sheet]=[]
        if top==highest[sheet]:owners[sheet].append({'part_id':p['part_id'],'copy_index':p['copy_index'],'transform':t})
        poses[(sheet,p['part_id'],t['rotation_radians'],*t['translation'],t['mirrored'])]+=1
    full=0.0;offcut=0.0;charged=[]
    for sheet in layout['sheets']:
        stock=stocks[sheet['stock_id']];w=rounded(stock['width']*1_000_000.0);h=rounded(stock['height']*1_000_000.0)
        gross=(w*h)/2_000_000_000_000.0*2.0
        used=min(stock['height'],max(0,highest[sheet['id']]/1_000_000.0+job['edge_clearance']+stock['margins']['top']))
        used=math.ceil(used/0.000001)*0.000001
        prefix=(w*rounded(min(used,stock['height'])*1_000_000.0))/2_000_000_000_000.0*2.0
        saving=max(0,gross-prefix);full+=gross;offcut=max(offcut,saving)
        charged.append({'sheet':sheet['id'],'top_grid':highest[sheet['id']],'used_height':min(used,stock['height']),'saving':saving,'owners':owners[sheet['id']]})
    return max(0,full-offcut),highest,poses,charged
rows=[];inputs={}
for pair in audit['pairs']:
    values=[]
    for record in pair['layouts']:
        folder=old/record['path'];job=load(folder/'job.json');layout=load(folder/'layout.json');checked=load(folder/'stdout.json')
        assert checked['valid'];material,top,poses,charged=heights(job,layout)
        assert material==checked['metrics']['material_area'],(record['path'],material,checked['metrics']['material_area'])
        values.append((material,top,poses,charged))
        for name in ['job.json','layout.json','stdout.json']:
            p=folder/name;inputs[p.relative_to(root).as_posix()]=digest(p)
    a,b=values
    rows.append({'kerf_mm':pair['kerf_mm'],'attempt':pair['attempt'],'exact_internal':pair['internal_exact_state'],
        'material_before':a[0],'material_after':b[0],'exact_charged_material_recomputed':True,
        'all_sheet_top_coordinates_equal':a[1]==b[1],
        'changed_incumbent_poses':sum((a[2]-b[2]).values()),'changed_trial_poses':sum((b[2]-a[2]).values()),
        'before_sheets':a[3],'after_sheets':b[3]})
record={'scope':__doc__,'all_checks_passed':True,'pairs':len(rows),'all_twelve_material_values_exact':True,
    'same_highest_coordinates_pairs':sum(r['all_sheet_top_coordinates_equal'] for r in rows),
    'records':rows,'input_sha256':inputs,'validator_source_sha256':{p:digest(root/p) for p in ['crates/validator/src/lib.rs','crates/validator/src/job.rs']},
    'scope_limits':'These already validated layouts use rectangular stock in mm. This reader is not a general material estimator or an acceptance validator. No new early rejection is implemented.',
    'new_searches':0,'production_changed':False,'quality_claim':False}
(out/'checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'inspect.py')
print(json.dumps({k:v for k,v in record.items() if k not in ['records','input_sha256','validator_source_sha256']}))
