"""Verify original per-attempt archives and report the descriptive H5 pilot."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import psutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h5-boundary-pair-pilot-20261018'
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'output'))
import h5_boundary_pair_pilot as pilot
load,write,digest=pilot.load,pilot.write,pilot.digest
result=load(OUT/'results.json')
plan=load(OUT/'plan.json')
opened=load(OUT/'opened.json')
assert not psutil.pid_exists(opened['pid']) or not any('h5_boundary_pair_pilot.py' in p for p in psutil.Process(opened['pid']).cmdline())
assert result['guards_unchanged'] and pilot.guards()==plan['guards']
assert digest(OUT/'plan.json')==opened['plan_sha256']
assert subprocess.check_output(['git','show','HEAD:'+(OUT/'plan.json').relative_to(ROOT).as_posix()],cwd=ROOT)==(OUT/'plan.json').read_bytes()
summary=pilot.summarize(result['records'])
assert json.loads(json.dumps(summary))==result['summary'] and summary['coverage_complete']
assert result['wall_seconds']<3600
archives=[]
for row in result['records']:
    archive=OUT/row['archive']
    assert digest(archive)==row['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        case=json.loads(z.read('case.json'))
        assert case=={k:v for k,v in row.items() if k not in ['archive','archive_sha256']}
        assert set(z.namelist())==set(case['artifacts'])|{'case.json'}
        for name,expected in case['artifacts'].items():assert sha256(z.read(name)).hexdigest()==expected
        if row['status']=='valid':
            search=json.loads(z.read('nested/search.json'))
            checked=json.loads(z.read('validate-stdout.json'))
            assert checked['valid'] and search['validation']['valid']
            pilot.equivalent(checked['metrics'],search['validation']['metrics'])
            assert checked['metrics']==row['metrics'] and checked['metrics']['normalized_material']==row['material']
            job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
            assert len(layout['placements'])==sum(p['quantity'] for p in job['parts'])
            assert row['search']['exit_code']==row['validation']['exit_code']==row['export']['exit_code']==0
            assert search['stats']==row['stats'] and search['riders']==row['riders']
            assert sha256(z.read('nested/layout.json')).hexdigest()==row['layout_sha256']
            if row['arm']!='normal':
                assert row['riders']==0
                before=sum(r['cut_length_without_common_mm'] for r in checked['common_line'])
                after=sum(r['cut_length_with_common_mm'] for r in checked['common_line'])
                assert before==row['cut_without_common_mm'] and after==row['cut_with_common_mm']
                assert row['saved_fraction']==1-after/before
        archives.append({'path':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'members':len(z.namelist())})
write(OUT/'verification.json',{'all_original_archives_verified':True,'archives':archives,
    'attempts':len(result['records']),'valid':sum(r['status']=='valid' for r in result['records']),
    'summary_recomputed':True,'production_and_observer_guards_unchanged':True,'H5_complete':False,'integrated':False})
shutil.copyfile(__file__,OUT/'finish.py')


pair_rows=[]
for row in result['records']:
    stats=row.get('stats',{})
    attempted=stats.get('paired_exchange_attempts',0);accepted=stats.get('paired_exchanges',0)
    assert type(attempted) is int and type(accepted) is int
    assert 0<=accepted<=attempted<=stats.get('directed_exchange_attempts',0)
    assert accepted<=stats.get('directed_exchanges',0)
    if row['arm']!='candidate':assert attempted==accepted==0
    pair_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} |
        {'attempted_pairs':attempted,'accepted_pairs':accepted,
         'all_attempts':stats.get('directed_exchange_attempts',0),'all_accepted':stats.get('directed_exchanges',0)})
counters={'attempted_pairs':sum(r['attempted_pairs'] for r in pair_rows),
          'accepted_pairs':sum(r['accepted_pairs'] for r in pair_rows),'records':pair_rows}
write(OUT/'pair-counters.json',counters)
lines=['# Boundary-pair exchange pilot — 2026-10-18','',
    f"**{sum(r['status']=='valid' for r in result['records'])}/{len(result['records'])} outcomes validate.**",
    'This four-job pilot does not complete H5. Every original limit and the',
    'complete 13-job requirement remain.','',
    '[Committed plan](h5-boundary-pair-pilot-20261018/plan.json),',
    '[all results](h5-boundary-pair-pilot-20261018/results.json),',
    '[archive verification](h5-boundary-pair-pilot-20261018/verification.json),',
    '[pair counters](h5-boundary-pair-pilot-20261018/pair-counters.json).','',
    '## Method','',
    'The candidate includes the two highest-ranked source parts as the first',
    'same-item or mixed pair, removes a duplicate in either anchor order,',
    'and retains the six-plus-six caps and remaining nearby alternatives.',
    'Original pair anchor frames, samples, repairs, budgets, work charges,',
    'early neutral rejections and full acceptance checks remain. The',
    '[preparation](h5-boundary-pair-preparation-20261018.md) retains 130',
    'passing optimized tests, all 126 prior tests unchanged, 26 frozen-CLI',
    'pair/boundary checks, public parity and deterministic replays. Three',
    'expected failures under the previous selector remain preserved.','',
    'Four jobs, two kerfs, seeds 0–2 and three arms produce 72 outcomes. Ordinary',
    'baseline, common baseline and common candidate run sequentially on the same',
    'physical CCD0 core in rotating order; at most eight blocks run together.',
    'Each search gets 60 seconds. Frozen geometry, quantities, stock and rotations',
    'are unchanged. Block, score, case and measurement methods are AST-identical',
    'to the preceding pilot. Every outcome requires independent validation and',
    'public export; common mode must reserve hole interiors.',
    f"The session took {result['wall_seconds']/60:.3f} minutes.",'',
    '## Three-seed medians','',
    'Positive material differences are worse. The unchanged limit is +1% against',
    'ordinary mode. Exchange counts sum all three seeds; an accepted exchange',
    'alone does not establish better final material use.','',
    '| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs baseline | Cut saving | All accepted / attempted | Pair accepted / attempted | Within +1% |',
    '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
for pair in summary['pairs']:
    if not pair['complete']:
        lines.append(f"| {pair['job']} | {pair['kerf_mm']} | incomplete | incomplete | incomplete | incomplete | incomplete | incomplete | no |")
        continue
    c=pair['arms']['candidate']
    rows=[r for r in pair_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {pair['baseline_vs_normal_percent']:+.6f}% | {pair['candidate_vs_normal_percent']:+.6f}% | {pair['candidate_vs_baseline_percent']:+.6f}% | {c['cut_savings_median_percent']:.6f}% | {c['exchanges']} / {c['exchange_attempts']} | {sum(r['accepted_pairs'] for r in rows)} / {sum(r['attempted_pairs'] for r in rows)} | {'yes' if pair['candidate_within_original_material_limit'] else 'NO'} |")
lines += ['', '## Evidence and limits','',
    'Every attempt retains its original ZIP. CRC, member/layout hashes, counters',
    'and independent metrics are verified; the summary is recomputed from every',
    'record. A failed or incomplete arm cannot yield a passing median. All source,',
    'binary, runner, data and environment guards remain unchanged.',
    'The prior failed pilots, source-repair traces and authored witnesses remain.',
    'No gate change, production integration or held-out access follows from this',
    'diagnostic alone. H2/H5 remain open; completed weight is 60%.','']
fill_rows=[]
for row in result['records']:
    stats=row.get('stats',{})
    calls=stats.get('post_exchange_fill_calls',0);moved=stats.get('post_exchange_fill_moves',0)
    assert type(calls) is int and type(moved) is int and calls>=0 and moved>=0
    assert moved<=stats.get('direct_insertions',0)
    if row['arm']=='candidate':assert calls==stats.get('directed_exchanges',0)
    else:assert calls==moved==0
    fill_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | {'calls':calls,'moved':moved})
fill={'calls':sum(r['calls'] for r in fill_rows),'moved':sum(r['moved'] for r in fill_rows),'records':fill_rows}
write(OUT/'post-exchange-fill-counters.json',fill)
lines += ['## Observed follow-up gap filling','',
    '| Job | Kerf mm | Calls after accepted exchanges | Parts moved |',
    '| --- | ---: | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in fill_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {sum(r['calls'] for r in selected)} | {sum(r['moved'] for r in selected)} |")
lines += ['',f"The step runs {fill['calls']} times and moves {fill['moved']} parts in total.",
    'These operation counts do not by themselves establish final material improvement.','']
neutral_rows=[]
for row in result['records']:
    stats=row.get('stats',{});rejected=stats.get('neutral_exchange_rejections',0)
    assert type(rejected) is int and 0<=rejected<=stats.get('directed_exchange_attempts',0)
    assert rejected+stats.get('directed_exchanges',0)<=stats.get('directed_exchange_attempts',0)
    if row['arm']!='candidate':assert rejected==0
    neutral_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | {'neutral_rejections':rejected})
neutral={'rejections':sum(r['neutral_rejections'] for r in neutral_rows),'records':neutral_rows}
write(OUT/'neutral-rejections.json',neutral)
lines += ['## Rejected unchanged-inventory swaps','',
    '| Job | Kerf mm | Rejections without material reduction |',
    '| --- | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in neutral_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {sum(r['neutral_rejections'] for r in selected)} |")
lines += ['',f"The exact-state, material-profile and original neutral guards reject {neutral['rejections']} unchanged-inventory proposals without material reduction.",
    'These counts do not identify other rejection stages or prove a global packing bound.','']
mixed_rows=[]
for row in result['records']:
    stats=row.get('stats',{});attempted=stats.get('mixed_exchange_attempts',0);accepted=stats.get('mixed_exchanges',0)
    assert type(attempted) is int and type(accepted) is int
    assert 0<=accepted<=attempted<=stats.get('paired_exchange_attempts',0)
    assert accepted<=stats.get('paired_exchanges',0)
    if row['arm']!='candidate':assert attempted==accepted==0
    mixed_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | {'mixed_attempts':attempted,'mixed_accepted':accepted})
mixed={'attempts':sum(r['mixed_attempts'] for r in mixed_rows),'accepted':sum(r['mixed_accepted'] for r in mixed_rows),'records':mixed_rows}
write(OUT/'mixed-counters.json',mixed)
lines += ['## Mixed-original-item exchanges','',
    '| Job | Kerf mm | Mixed accepted / attempted |', '| --- | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in mixed_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {sum(r['mixed_accepted'] for r in selected)} / {sum(r['mixed_attempts'] for r in selected)} |")
lines += ['',f"There are {mixed['accepted']} accepted mixed-item exchanges in {mixed['attempts']} attempts.",
    'These are subsets of the paired counters and do not establish final material improvement.','']
exact_rows=[]
for row in result['records']:
    stats=row.get('stats',{});count=stats.get('exact_state_exchange_rejections',0)
    assert type(count) is int and 0<=count<=stats.get('neutral_exchange_rejections',0)
    if row['arm']!='candidate':assert count==0
    exact_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} | {'exact_rejections':count})
exact={'rejections':sum(r['exact_rejections'] for r in exact_rows),'records':exact_rows}
write(OUT/'exact-state-rejections.json',exact)
lines += ['## Exact-state early rejections','',
    '| Job | Kerf mm | Exact duplicates rejected before validation |', '| --- | ---: | ---: |']
for pair in summary['pairs']:
    selected=[r for r in exact_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm'])]
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {sum(r['exact_rejections'] for r in selected)} |")
lines += ['',f"There are {exact['rejections']} exact-state rejections before repeated validation.",
    'These are a subset of neutral rejections. Counts alone do not establish',
    'saved wall time or final material improvement.','']
profile_rows=[]
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
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'all_valid':summary['all_valid'],'paired_attempts':counters['attempted_pairs'],
    'paired_accepted':counters['accepted_pairs'],'pairs':[{k:v for k,v in p.items() if k not in ['arms','per_seed']} for p in summary['pairs']]}))
