from pathlib import Path
import json,collections
p=Path('benchmarks/results/h4-browser-profile-20261016T040030Z')
r=json.loads((p/'results.json').read_bytes());summary=[]
for row in r['rows']:
    raw=json.loads((p/row['job']/'cpu.cpuprofile').read_bytes());nodes={n['id']:n for n in raw['nodes']};totals=collections.Counter()
    for node,dt in zip(raw['samples'],raw['timeDeltas'],strict=True):totals[nodes[node]['callFrame']['functionName']]+=dt
    sample=sum(raw['timeDeltas']);span=raw['endTime']-raw['startTime']
    summary.append({'job':row['job'],'valid':row['validation']['status'],'profile_span_seconds':span/1e6,'sampled_seconds':sample/1e6,'unattributed_gap_seconds':(span-sample)/1e6,'top_self':[{'function':name,'seconds':micros/1e6,'percent_of_samples':100*micros/sample} for name,micros in totals.most_common(12)],'all_self_functions':[{'function':name,'seconds':micros/1e6,'percent_of_samples':100*micros/sample} for name,micros in totals.most_common()]})
(p/'aggregate.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
for row in summary:
    row.pop('all_self_functions');print(json.dumps(row))
