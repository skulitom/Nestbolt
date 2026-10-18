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
OUT=ROOT/'benchmarks/results/h5-return-reuse-pilot-20261018'
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'output'))
import h5_return_reuse_pilot as pilot
load,write,digest=pilot.load,pilot.write,pilot.digest
result=load(OUT/'results.json')
plan=load(OUT/'plan.json')
opened=load(OUT/'opened.json')
assert not psutil.pid_exists(opened['pid']) or not any('h5_return_reuse_pilot.py' in p for p in psutil.Process(opened['pid']).cmdline())
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

reuse_rows=[]
for row in result['records']:
    stats=row.get('stats',{})
    reuses=stats.get('directed_source_reuses',0)
    assert isinstance(reuses,int) and reuses>=0
    attempts=stats.get('directed_exchange_attempts',0)
    assert reuses<=attempts
    if row['arm']!='candidate':assert reuses==0
    reuse_rows.append({k:row[k] for k in ['job','kerf_mm','seed','arm']} |
                     {'attempts':attempts,'accepted':stats.get('directed_exchanges',0),'source_reuses':reuses})
write(OUT/'reuse-counters.json',{'source':'Original archive search counters, checked against every saved record',
    'candidate_source_reuses':sum(r['source_reuses'] for r in reuse_rows), 'records':reuse_rows})
lines=['# Compatible source-repair reuse pilot — 2026-10-18','',
    f"**{sum(r['status']=='valid' for r in result['records'])}/{len(result['records'])} outcomes validate.**",
    'This four-job pilot does not complete H5. The full 13-job comparison and',
    'every original acceptance limit remain required.','',
    '[Committed plan](h5-return-reuse-pilot-20261018/plan.json),',
    '[all outcomes](h5-return-reuse-pilot-20261018/results.json),',
    '[archive verification](h5-return-reuse-pilot-20261018/verification.json),',
    '[repair reuse counters](h5-return-reuse-pilot-20261018/reuse-counters.json).','',
    '## Method','',
    'The isolated candidate retains one best source-sheet repair state within',
    'each exchange invocation. It resumes only when the static container and',
    'original part-object multiset match, all stored poses are permitted and',
    'the saved loss is no worse than the fresh state. Restoring the snapshot',
    'also restores tracker indices; guided-search weights and RNG continue.',
    'Normal mode, proposal caps, repair deadlines, the whole-job acceptance',
    'guard and production remain unchanged. All 90 preceding tests and six',
    'new tests pass; see the [preparation](h5-return-reuse-preparation-20261018.md).','',
    'Four frozen jobs, two kerfs and seeds 0–2 produce 72 outcomes across',
    'ordinary baseline, common-line baseline and common-line candidate.',
    'The three arms run sequentially on the same physical CCD0 core in',
    'rotating order; at most eight blocks run together. Each search receives',
    '60 seconds. Frozen geometry, quantities, stock and rotations are unchanged.',
    'The paired blocks, scoring and measurement functions remain AST-identical',
    'to the preceding return-frame pilot. Every output requires independent',
    'public validation and export; common mode must reserve hole interiors.',
    f"The session took {result['wall_seconds']/60:.3f} minutes.",'',
    '## Three-seed medians','',
    'Positive material differences are worse. The candidate must remain within',
    '+1% of ordinary mode. Counts sum all three seeds; a reuse is not an',
    'accepted exchange or evidence of material improvement.','',
    '| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs baseline | Cut saving | Accepted / attempted | Reuses | Within +1% |',
    '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
for pair in summary['pairs']:
    if not pair['complete']:
        lines.append(f"| {pair['job']} | {pair['kerf_mm']} | incomplete | incomplete | incomplete | incomplete | incomplete | incomplete | no |")
        continue
    c=pair['arms']['candidate']
    reused=sum(r['source_reuses'] for r in reuse_rows if r['arm']=='candidate' and (r['job'],r['kerf_mm'])==(pair['job'],pair['kerf_mm']))
    lines.append(f"| {pair['job']} | {pair['kerf_mm']} | {pair['baseline_vs_normal_percent']:+.6f}% | {pair['candidate_vs_normal_percent']:+.6f}% | {pair['candidate_vs_baseline_percent']:+.6f}% | {c['cut_savings_median_percent']:.6f}% | {c['exchanges']} / {c['exchange_attempts']} | {reused} | {'yes' if pair['candidate_within_original_material_limit'] else 'NO'} |")
lines += ['', '## Evidence and limits','',
    'Every attempted outcome, including failures, retains its original ZIP.',
    'CRC, member hashes, layout hashes, counters and independent metrics are',
    'verified. The summary is recomputed from every record; incomplete or',
    'failed arms cannot yield a passing median. Source, binary, runner, inputs',
    'and environment guards remain unchanged.','',
    'The earlier [return-frame pilot](h5-return-frame-pilot-20261017.md),',
    '[capacity traces](h5-return-capacity-diagnosis-20261017.md) and',
    '[fixed-assignment witnesses](h5-assignment-repack-20261018.md) are preserved.',
    'Three fixed assignments have independent feasible witnesses; the fourth',
    'remains unresolved. Those diagnostic timings do not establish the minimum',
    'repair time or prove whether this bounded reuse method can satisfy H5.',
    'No relaxed threshold or automatic integration. H2/H5 remain open at 60%.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'all_valid':summary['all_valid'],'source_reuses':sum(r['source_reuses'] for r in reuse_rows),
    'pairs':[{k:v for k,v in p.items() if k not in ['arms','per_seed']} for p in summary['pairs']]}))
