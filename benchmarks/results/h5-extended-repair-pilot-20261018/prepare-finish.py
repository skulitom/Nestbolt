from pathlib import Path
from hashlib import sha256
import json
root=Path(__file__).resolve().parents[1];probe=root/'output/h5-extended-repair-probe-20261018'
def adapt(s):return s.replace('h5-exchange-chain','h5-extended-repair').replace('h5_exchange_chain','h5_extended_repair').replace('Exchange-continuation','Extended-repair')
s=adapt((root/'output/finish_h5_exchange_chain_pilot.py').read_text(encoding='utf-8'))
a=s.index("    'The candidate continues after strict material improvements");b=s.index("    'Four jobs, two kerfs",a)
s=s[:a]+'''    'The candidate retains the original short exchange phase, then uses any',
    'remaining existing relocation allowance for continuous source repairs.',
    'Additional acceptances require strict material reduction. Both phases',
    'share the four-exchange cap; overall search time, validation reserve and',
    'original geometry/inventory/frozen-sheet guards remain. The original',
    'proposal order and receiver allowance remain. Stage counters are separate.',
    '[Qualification](h5-extended-repair-preparation-20261018.md) retains 148 passing',
    'tests: 141 prior bodies unchanged and seven new regressions. The three',
    'opportunities lost by direct-long-source repair match their prior witnesses',
    'exactly. Both red runs and the corrected newly authored frozen-sheet fixture',
    'remain. Source reconstruction, public replay, geometry, lint and build pass.','',
'''+s[b:]
needle='fill_rows=[]'
stage='''extended_rows=[]
for row in result['records']:
    stats=row.get('stats',{})
    attempted=stats.get('extended_exchange_attempts',0)
    accepted=stats.get('extended_exchanges',0)
    flat=stats.get('extended_flat_rejections',0)
    assert all(type(x) is int and x>=0 for x in [attempted,accepted,flat])
    assert accepted<=attempted<=stats.get('directed_exchange_attempts',0)
    assert accepted<=stats.get('directed_exchanges',0) and flat+accepted<=attempted
    assert flat+stats.get('neutral_exchange_rejections',0)+stats.get('directed_exchanges',0)<=stats.get('directed_exchange_attempts',0)
    if row['arm']!='candidate':assert attempted==accepted==flat==0
    extended_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | {'attempted':attempted,'accepted':accepted,'flat_rejections':flat})
extended={key:sum(r[key] for r in extended_rows) for key in ['attempted','accepted','flat_rejections']}
extended['records']=extended_rows
write(OUT/'extended-counters.json',extended)
lines += ['## Extended repair phase','',
    '| Job | Kerf mm | Accepted / attempted | Flat trials rejected |',
    '| --- | ---: | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in extended_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {sum(r['accepted'] for r in selected)} / {sum(r['attempted'] for r in selected)} | {sum(r['flat_rejections'] for r in selected)} |")
lines += ['', 'Extended attempts are a subset of total attempts. These counters',
    'identify the later phase; they do not measure repair duration or establish',
    'a final material benefit. Flat rejections are separate from original neutral',
    'rejections. Every extended acceptance requires a strict material reduction.','']
'''
assert s.count(needle)==1;s=s.replace(needle,stage+needle);compile(s,'finish','exec');(root/'output/finish_h5_extended_repair_pilot.py').write_text(s,encoding='utf-8',newline='\n')
s=adapt((root/'output/audit_h5_exchange_chain.py').read_text(encoding='utf-8'));(root/'output/audit_h5_extended_repair.py').write_text(s,encoding='utf-8',newline='\n')
record={'parent':'output/finish_h5_exchange_chain_pilot.py','parent_sha256':sha256((root/'output/finish_h5_exchange_chain_pilot.py').read_bytes()).hexdigest(),'geometry_archive_scoring_and_existing_counter_checks_unchanged':True,'new_stage_counter_checks':['nonnegative integers','extended subset of all attempts and accepts','flat and accepted outcomes disjoint','flat plus original neutral plus all accepts bounded by total attempts','baseline stage counters zero'],'shared_four_acceptances_per_fill_window_check_retained':True,'candidate_finisher_sha256':sha256((root/'output/finish_h5_extended_repair_pilot.py').read_bytes()).hexdigest(),'new_searches':0}
(probe/'counter-audit-method.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(record))
