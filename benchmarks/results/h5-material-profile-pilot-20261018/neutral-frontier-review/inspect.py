"""Inspect the already-validated neutral pairs; no new search or geometry inputs."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,shutil
root=Path(__file__).resolve().parents[1]
source=root/'benchmarks/results/h5-exact-reject-pilot-20261018/neutral-height-review/checks.json'
out=root/'output/h5-neutral-frontier-review-20261018';out.mkdir()
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
height=load(source);assert height['all_checks_passed'] and height['pairs']==6
for name,expected in height['input_sha256'].items():assert digest(root/name)==expected
def physical(owners):
    return Counter((o['part_id'],o['transform']['rotation_radians'],
        *o['transform']['translation'],o['transform']['mirrored']) for o in owners)
records=[]
for row in height['records']:
    before=row['before_sheets'];after={s['sheet']:s for s in row['after_sheets']}
    maximum=max(s['saving'] for s in before)
    credited=[s for s in before if s['saving']==maximum]
    owners=[]
    for sheet in credited:
        trial=after[sheet['sheet']]
        same=physical(sheet['owners'])==physical(trial['owners'])
        owners.append({'sheet':sheet['sheet'],'saving':maximum,'height':sheet['used_height'],
            'top_parts':[o['part_id'] for o in sheet['owners']],
            'top_physical_poses_unchanged':same,'top_before':sheet['owners'],'top_after':trial['owners']})
    records.append({'kerf_mm':row['kerf_mm'],'attempt':row['attempt'],
        'changed_incumbent_poses':row['changed_incumbent_poses'],
        'credited_sheets':owners,'all_credited_top_poses_unchanged':all(s['top_physical_poses_unchanged'] for s in owners)})
checks={'all_checks_passed':True,'pairs':len(records),
    'pairs_with_unchanged_credited_top_poses':sum(r['all_credited_top_poses_unchanged'] for r in records),
    'records':records,'source':source.relative_to(root).as_posix(),'source_sha256':digest(source),
    'input_hashes_rechecked':True,'copy_indices_ignored_for_physical_pose_comparison':True,
    'limits':'Saved neutral panel states only. Unchanged top poses explain equal material in these cases; no claim about every new pilot outcome, selected internal item IDs, feasibility or global optimality.',
    'new_searches':0,'production_changed':False,'quality_claim':False}
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'inspect.py')
print(json.dumps({k:v for k,v in checks.items() if k!='records'}))
