from pathlib import Path
from collections import Counter
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-return-reuse-stage-diagnosis-20261018'
load=lambda p:json.loads(p.read_bytes())
v=load(out/'verification.json');result=load(out/'results.json')
stages=load(out/'observed-stages.json');reuse=load(out/'observed-reuse.json')
assert v['all_original_archives_and_traces_verified'] and v['valid']==4
assert stages['aggregate_attempt_outcomes']['all']=={'source_repair_failed':24}
assert reuse['source_attempts']==24 and reuse['reused_attempts']==16
assert reuse['reused_improved_loss']==7 and reuse['all_zero_final_loss']==0
rows=reuse['rows'];negative=[a for a in rows if a['source_available_budget']<=0]
assert len(negative)==3
case_rows=[]
for record in result['records']:
    selected=[a for a in rows if (a['job'],a['kerf_mm'])==(record['job'],record['kerf_mm'])]
    case_rows.append({'job':record['job'],'kerf_mm':record['kerf_mm'],
        'source_repair_seconds':sum(a['source_elapsed_seconds'] for a in selected),
        'minimum_available_source_seconds':min(a['source_available_budget'] for a in selected),
        'maximum_available_source_seconds':max(a['source_available_budget'] for a in selected),
        'source_attempts':len(selected),'reuses':sum(a['source_reused'] for a in selected),
        'reuses_improving_loss':sum(a['source_reused'] and a['source_loss']<a['source_initial_loss'] for a in selected),
        'first_inventory':dict(Counter(selected[0]['source_inventory'])),
        'first_best_loss':selected[0]['source_loss'],
        'last_best_loss':selected[-1]['source_loss']})
status=root/'docs/STATUS.md';old=status.read_text(encoding='utf-8')
marker='**N4 source-repair reuse outcome, 2026-10-18:**'
heading='**N4 reuse-stage diagnosis, 2026-10-18:**'
assert old.count(marker)==1 and heading not in old
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:assert heading not in (root/name).read_text(encoding='utf-8')
assert not (out/'record-outcome.py').exists()
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior

detail='''All 24 complete-obstruction exchanges repair the receiver, then fail source
repair. Sixteen resume a compatible saved state; seven reduce loss further,
none reaches zero, and none reaches final material/geometry acceptance.
The reader verifies original inventories and exact restored loss across each
reuse. The issue is incomplete repair, not observed cache-state corruption.
'''
limits='''Each case spends 0.903–1.054 seconds in source repairs within the existing
early-call budget. Available windows shrink after successive attempts; three
late attempts reach source repair with an already-expired pair deadline and
return their unchanged state. These observed durations are not minimum required
repair times and do not prove that a larger allowance would solve H5.
'''
next_step='''The prior fixed-assignment witnesses and balanced two-to-three authored
exchange remain distinct evidence. Continuing one failed assignment longer
and changing the incoming group are separate hypotheses; the current cache
does neither. The next search change should alter the assignment or its repair
strategy with authored correctness checks and a new committed comparison,
while retaining the original whole-job budget and acceptance limits.
'''
note='\n\n'+heading+' [four diagnostic outputs validate](../benchmarks/results/h5-return-reuse-stage-diagnosis-20261018.md).\n'+detail+limits+'Production and all failed results remain unchanged. H2/H5 remain open at 60%.\n'
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
summary={'cases':case_rows,'nonpositive_source_windows':negative,
    'interpretation':detail+limits+next_step,'no_new_search':True,'H5_complete':False}
(out/'interpretation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
append(out.parent/(out.name+'.md'),'\n\n## Interpretation and next constraint\n\n'+detail+'\n'+limits+'\n'+next_step)
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Reused repairs remain unfinished\n\n[All four diagnostic outputs validate](benchmarks/results/h5-return-reuse-stage-diagnosis-20261018.md)\nwith original quantities, public exports, independent metrics and verified\narchive/trace hashes. All source/binary/input guards remain unchanged.\n\n'+detail+'\n'+limits+'\n'+next_step+'\nNo production integration, held-out access or H5 credit. H2/H5 remain open at 60%.\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,note)
status.write_text(old.replace(marker,note.strip()+'\n\n'+marker,1),encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'source_repair_failures':24,'reuses':16,'improved_reuses':7,'expired_source_windows':len(negative),'cases':case_rows}))
