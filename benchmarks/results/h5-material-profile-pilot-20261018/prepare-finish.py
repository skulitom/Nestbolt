"""Prepare archive and geometry verification without reading unfinished results."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/finish_h5_exact_reject_pilot.py').read_text(encoding='utf-8')
s=s.replace('h5-exact-reject','h5-material-profile').replace('h5_exact_reject','h5_material_profile')
s=s.replace('# Exact-state early-rejection pilot','# Exact material-profile rejection pilot')
start=s.index("    'The candidate adds an early rejection only")
end=s.index("    'Four jobs, two kerfs",start)
s=s[:start]+'''    'The candidate retains exact-state rejection and adds a sufficient',
    'unchanged-material check for same-inventory exchanges. It uses original',
    'geometry footprints, transforms and grid from the unchanged validator.',
    'Profiles require the same immutable job, sheet/stock assignments, exact',
    'sheet maxima and original copy identities. Equality permits rejection',
    'only. Every accepted exchange retains full geometry and strict material',
    'checks. Budgets and coefficients are unchanged; new footprint work uses',
    'the existing validated-vertex charge. The [preparation]',
    '(h5-material-profile-preparation-20261018.md) retains 123 passing optimized',
    'tests, all 117 prior tests unchanged, 47 frozen-CLI profile checks and',
    '24 frozen-CLI branch checks. Original preparation failures and the',
    'expected failing regression remain. Strict lint/build, public parity',
    'and exact deterministic replays pass.','',
'''+s[end:]
s=s.replace('The early exact-state and original neutral guards reject','The exact-state, material-profile and original neutral guards reject')
needle="(OUT.parent/(OUT.name+'.md')).write_text";assert s.count(needle)==1
extra='''profile_rows=[]
for row in result['records']:
    stats=row.get('stats',{});count=stats.get('material_profile_exchange_rejections',0)
    exact_count=stats.get('exact_state_exchange_rejections',0)
    assert type(count) is int and 0<=count<=stats.get('neutral_exchange_rejections',0)
    assert count+exact_count<=stats.get('neutral_exchange_rejections',0)<=stats.get('directed_exchange_attempts',0)
    if row['arm']!='candidate':assert count==0
    profile_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | {'profile_rejections':count})
profiles={'rejections':sum(r['profile_rejections'] for r in profile_rows),'records':profile_rows}
write(OUT/'material-profile-rejections.json',profiles)
lines += ['## Proven unchanged-material rejections','',
    '| Job | Kerf mm | Profile rejections before full validation |', '| --- | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in profile_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {sum(r['profile_rejections'] for r in selected)} |")
lines += ['',f"There are {profiles['rejections']} material-profile rejections before full validation.",
    'These and exact-state rejections are disjoint subsets of neutral rejections.',
    'Counts do not measure saved time or establish final material improvement.','']
'''
s=s.replace(needle,extra+needle)
path=root/'output/finish_h5_material_profile_pilot.py';compile(s,str(path),'exec');path.write_text(s,encoding='utf-8',newline='\n')
s=(root/'output/audit_h5_exact_reject.py').read_text(encoding='utf-8').replace('h5-exact-reject','h5-material-profile')
path=root/'output/audit_h5_material_profile.py';compile(s,str(path),'exec');path.write_text(s,encoding='utf-8',newline='\n')
print('Prepared archive verification, unchanged geometry audit and profile counter report.')
