"""Report the isolated probe without converting trajectory rates into speed claims."""
import json
from pathlib import Path
import statistics
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h4-score-chunks-probe-20261016'
OLD=ROOT/'benchmarks/results/h4-preview-development-20261016'
load=lambda p:json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
result=load(OUT/'results.json')
verification=load(OUT/'verification.json')
inventory=load(OUT/'integrity.json')
assert verification['original_records_verified'] and inventory['crc_and_every_member_verified']
summary=result['summary']
replays=load(OUT/'replay-results.json')
prior=load(OLD/'results.json')
diagnostics={}
with zipfile.ZipFile(OLD/'raw.zip') as z:
    for engine,records in result['records'].items():
        by_key={(r['job'],r['seed']):r for r in prior['records'][engine]}
        pairs=[]
        for row in records:
            old=by_key[row['job'],row['seed']]
            if row['status']!='valid' or old['status']!='valid':continue
            name='search-stdout.json' if engine=='native' else 'result.json'
            baseline=json.loads(z.read(old['directory']+'/'+name))
            current=load(ROOT/row['directory']/name)
            if min(baseline['elapsed_seconds'],current['elapsed_seconds'],baseline['work'],current['work'])>0:
                pairs.append({'job':row['job'],'seed':row['seed'],
                    'work_rate_difference_percent':100*((current['work']/current['elapsed_seconds'])/(baseline['work']/baseline['elapsed_seconds'])-1),
                    'material_difference_percent':100*(row['material']/old['material']-1)})
        diagnostics[engine]={'matched_valid_pairs':len(pairs),'records':pairs,
            'median_work_rate_difference_percent':statistics.median(r['work_rate_difference_percent'] for r in pairs) if len(pairs)==33 else None,
            'median_single_attempt_material_difference_percent':statistics.median(r['material_difference_percent'] for r in pairs) if len(pairs)==33 else None}
write(OUT/'historical-diagnostics.json',{'scope':'Same job/seed comparison to the earlier integrated-preview run. Trajectories and wall-time conditions differ; neither an isolated speed test nor a gate.',
    'engines':diagnostics,'speed_claim':False})
lines=['# Isolated eight-pair score-bound probe — 2026-10-16','',
    f"**The eleven-job subset {'passes' if summary['passes_subset'] else 'fails'} its unchanged limits.**",
    'This is an isolated candidate, not an integrated release or complete H4 gate.',
    'Completed milestone weight remains 45%. The original preview failure is',
    'preserved and no unchanged-build trial was repeated.','',
    '[Fixed plan](h4-score-chunks-probe-20261016/plan.json),',
    '[complete results](h4-score-chunks-probe-20261016/results.json),',
    '[artifact verification](h4-score-chunks-probe-20261016/verification.json).','',
    '## Correctness and method','',
    'Only exact-bound check granularity changes: check after eight pole pairs',
    'rather than an entire row. [Preparation checks](h4-score-chunks-preparation-20261016.md)',
    'cover reference score bits, ties, complete evaluation, long/partial chunks,',
    'optimized builds and strict lint. No geometry, score arithmetic, accumulation',
    'order, work charge, default, deadline or dependency changes.','',
    'Before quality measurement, all eight fixed-work native runs validate.',
    'Four baseline/candidate pairs retain the entire result except actual elapsed',
    'wall time, including layouts, counters, history, accepted-at time and metrics.',
    f"Their median wall difference is {replays['median_wall_difference_percent']:+.6f}%.",
    'These short, baseline-first pairs do not establish a speed gain.','',
    'The quality plan uses the same eleven development jobs, seeds 0–2 and',
    '60-second budgets in native, installed Chrome and Firefox. It runs once,',
    'with one worker per browser job and at most eight physical CCD0 cores.',
    'The unchanged root CLI independently validates every output, including the',
    'actual public library/request for both examples. Source, binary, site, input,',
    'runner and environment guards remain unchanged. No held-out geometry is read.',
    f"The session took {result['wall_seconds']/60:.3f} minutes.",'',
    '## Subset result','',
    'The original limits are +1% median material and +5% for every job versus',
    'native, using the median of each job’s three seeds.','',
    '| Browser | Valid | Median difference | Worst job | Total difference | Result |',
    '| --- | ---: | ---: | ---: | ---: | --- |']
for engine,row in summary['comparisons'].items():
    lines.append(f"| {engine.title()} | {row['valid']}/{row['attempted']} | {row['median_difference_percent']:+.6f}% | {row['worst_difference_percent']:+.6f}% | {row['total_difference_percent']:+.6f}% | {'pass' if row['passes_subset'] else 'FAIL'} |")
lines += ['', '| Job | Native median | Chrome difference | Firefox difference |',
    '| --- | ---: | ---: | ---: |']
for row in load(OUT/'plan.json')['cases']:
    name=row['id']
    lines.append(f"| {name} | {summary['medians']['native'][name]:.9f} | {summary['comparisons']['chrome']['per_job_difference_percent'][name]:+.6f}% | {summary['comparisons']['firefox']['per_job_difference_percent'][name]:+.6f}% |")
lines += ['', '## Limits and retained evidence','',
    'A [historical diagnostic](h4-score-chunks-probe-20261016/historical-diagnostics.json)',
    'compares charged-work rates and material against the original preview on the',
    'same jobs/seeds. Search trajectories and wall-time conditions differ, so those',
    'rates are not isolated kernel throughput or a general speed claim.','',
    'The full 65-job G5/native matrix, scale confirmation and final integration',
    'checks remain separate. This subset does not complete H4 or authorize a new',
    'public comparison. H2 and H5 remain open independently.','',
    f"The [raw archive](h4-score-chunks-probe-20261016/raw.zip) retains {len(inventory['members']):,} members,",
    f"{inventory['bytes']:,} bytes, SHA-256 `{inventory['sha256']}`.",
    'CRC, every member size and hash were verified. Exact candidate binaries,',
    'source and site remain bound to the separately verified preparation archive;',
    'the original baseline is retained in the complete preview archive.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'subset_pass':summary['passes_subset'],'historical_diagnostics':{k:{a:b for a,b in v.items() if a!='records'} for k,v in diagnostics.items()}}))
