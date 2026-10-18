"""Count equivalent source inventories and containers in saved traces only."""
from pathlib import Path
from hashlib import sha256
from collections import Counter,defaultdict
import json,shutil
root=Path(__file__).resolve().parents[1];source=root/'benchmarks/results/h5-return-capacity-diagnosis-20261017'
out=root/'benchmarks/results/h5-assignment-repack-20261018'
integrity=json.loads((source/'records-integrity.json').read_bytes())
raw=(source/'results.json').read_bytes();assert sha256(raw).hexdigest()==integrity['members']['results.json']['sha256']
records=json.loads(raw)['records'];groups=[]
for record in records:
    for ti,trace in enumerate(record['diagnosis']['traces']):
        bucket=defaultdict(list);definitions={}
        for ai,attempt in enumerate(trace['attempts']):
            layout=attempt['source_initial']
            inventory=Counter((p['item_index'],p['external_id']) for p in layout['items'])
            signature={'container':layout['container'],'inventory':[[*key,count] for key,count in sorted(inventory.items())]}
            key=sha256(json.dumps(signature,sort_keys=True,separators=(',',':')).encode()).hexdigest();definitions[key]=signature
            bucket[key].append({'attempt_index':ai,'outcome':attempt['outcome'],'initial_loss':attempt['source_initial_loss'],'best_loss':attempt['source_loss']})
        for key,attempts in bucket.items():
            groups.append({'job':record['job'],'kerf_mm':record['kerf_mm'],'trace_index':ti,'signature_sha256':key,
                'signature':definitions[key],'attempts':attempts,'repeated_after_first':len(attempts)-1})
result={'scope':__doc__,'source_results_sha256':sha256(raw).hexdigest(),'attempts':sum(len(g['attempts']) for g in groups),
    'distinct_assignments_within_invocations':len(groups),'repeated_after_first':sum(g['repeated_after_first'] for g in groups),
    'identity_assumption':'Within one invocation the immutable original Model maps each internal item index to the same geometry and allowed orientations. Identical copies are interchangeable; snapshot placement keys are deliberately excluded.',
    'interpretation':'These are potential reuse opportunities, not measured cache hits, savings or evidence of quality improvement. A cache must preserve container, full inventory, geometry and orientation permissions, and continue to use independent whole-job acceptance.',
    'new_searches':0,'H5_complete':False,'groups':groups}
(out/'repeated-assignments.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'inspect-repetitions.py')
print(json.dumps({k:v for k,v in result.items() if k!='groups'}))
