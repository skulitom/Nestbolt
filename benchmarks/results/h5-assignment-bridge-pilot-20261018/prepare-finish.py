from pathlib import Path
from hashlib import sha256
import json
root=Path(__file__).resolve().parents[1];probe=root/'output/h5-assignment-bridge-probe-20261018'
def adapt(s):return s.replace('h5-extended-repair','h5-assignment-bridge').replace('h5_extended_repair','h5_assignment_bridge').replace('Extended-repair','Assignment-bridge')
s=adapt((root/'output/finish_h5_extended_repair_pilot.py').read_text(encoding='utf-8'))
a=s.index("    'The candidate retains the original short exchange phase");b=s.index("    'Four jobs, two kerfs",a)
s=s[:a]+'''    'The candidate retains the original short exchange phase. Its remaining',
    'relocation allowance can cross validated material-flat steps when canonical',
    'last-sheet filled area strictly decreases. A sequence commits only after',
    'whole-job material strictly decreases; otherwise layout, tracker and accepted',
    'counts roll back. Attempts and provisional diagnostics remain visible.',
    'The original overall budget, validation reserve, four-step cap and geometry',
    'guards remain. [Qualification](h5-assignment-bridge-preparation-20261018.md)',
    'retains 156 passing tests: 148 old bodies, one unchanged-policy witness and',
    'seven new policy regressions. Eight independent checks validate the original',
    'flat-flat-gain sequence; 24 further checks cover actual bridge outputs.',
    'Source reconstruction, exact old witnesses, public replay, lint and build pass.','',
'''+s[b:]
needle="    'rejections. Every extended acceptance requires a strict material reduction.','']"
replacement="    'rejections. Committed extended counts include provisional steps in a sequence',\n    'that ultimately strictly reduces material; they do not all reduce it alone.','']"
assert s.count(needle)==1;s=s.replace(needle,replacement)
needle='fill_rows=[]'
addition='''bridge_rows=[]
for row in result['records']:
    stats=row.get('stats',{})
    names=['assignment_bridge_steps','assignment_bridge_flat_steps','assignment_bridge_committed','assignment_bridge_rolled_back','assignment_bridge_area_rejections','assignment_bridge_rollbacks']
    counts={n:stats.get(n,0) for n in names}
    assert all(type(v)is int and v>=0 for v in counts.values())
    steps,flat,committed,rolled,rejected,rollbacks=[counts[n] for n in names]
    assert steps==committed+rolled and flat<=steps<=stats.get('extended_exchange_attempts',0)
    assert committed<=stats.get('extended_exchanges',0) and rejected<=stats.get('extended_flat_rejections',0)
    assert rollbacks<=rolled
    assert stats.get('directed_exchanges',0)+rolled+stats.get('neutral_exchange_rejections',0)+stats.get('extended_flat_rejections',0)<=stats.get('directed_exchange_attempts',0)
    if row['arm']!='candidate':assert not any(counts.values())
    bridge_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | counts)
bridge={name:sum(r[name] for r in bridge_rows) for name in names}
bridge['records']=bridge_rows;write(OUT/'bridge-counters.json',bridge)
lines += ['## Provisional assignment steps','',
    '| Job | Kerf mm | Steps | Flat steps | Committed | Rolled back |',
    '| --- | ---: | ---: | ---: | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in bridge_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    values=[sum(r[name] for r in selected) for name in names[:4]]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {' | '.join(map(str,values))} |")
lines += ['', 'Steps equal committed plus rolled back. Committed steps can include',
    'material-flat intermediates; only the completed sequence must improve material.',
    'These counters do not establish final quality or measure repair duration.','']
'''
assert s.count(needle)==1;s=s.replace(needle,addition+needle);compile(s,'finish','exec')
(root/'output/finish_h5_assignment_bridge_pilot.py').write_text(s,encoding='utf-8',newline='\n')
s=adapt((root/'output/audit_h5_extended_repair.py').read_text(encoding='utf-8'))
(root/'output/audit_h5_assignment_bridge.py').write_text(s,encoding='utf-8',newline='\n')
record={'parent':'output/finish_h5_extended_repair_pilot.py','parent_sha256':sha256((root/'output/finish_h5_extended_repair_pilot.py').read_bytes()).hexdigest(),
 'geometry_archive_scoring_and_existing_counter_checks_unchanged':True,
 'new_counter_checks':['provisional steps equal committed plus rolled back','flat steps bounded by all steps','steps bounded by extended attempts','committed bounded by extended accepts','area rejections bounded by extended flat rejections','rolled-back steps excluded from original accepted counts','baseline bridge counters zero'],
 'candidate_finisher_sha256':sha256((root/'output/finish_h5_assignment_bridge_pilot.py').read_bytes()).hexdigest(),'new_searches':0}
(probe/'counter-audit-method.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(record))
