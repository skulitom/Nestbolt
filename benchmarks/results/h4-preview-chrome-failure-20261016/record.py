"""Record the completed Chrome arm while the original Firefox arm continues."""
from datetime import datetime, timezone
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import h4_preview_matrix as matrix
out=ROOT/'benchmarks/results/h4-preview-chrome-failure-20261016'
assert not out.exists()
out.mkdir()
active=ROOT/'benchmarks/results/h4-preview-development-20261016'
plan=matrix.load(active/'plan.json')
records=matrix.load(active/'records.json')
assert len(records['native'])==len(records['chrome'])==201
assert all(r['status']=='valid' for e in ['native','chrome'] for r in records[e])
rows,_,subset=matrix.cases()
assert matrix.guards(rows)==plan['guards']
selected=lambda ids:{k:[r for r in v if r['job'] in ids] for k,v in records.items()}
full=matrix.full.summarize(selected(plan['full_ids']),plan['full_ids'])
small=matrix.quality.summarize(selected(plan['subset_ids']),subset,[0,1,2],60)
chrome=small['comparisons']['chrome']
assert not chrome['passes_subset'] and chrome['median_difference_percent']>1
data={'scope':__doc__,'utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':matrix.quality.digest(active/'plan.json'),
    'source_guards_unchanged':True,'native':full['native_vs_v1'],
    'chrome_full':full['browsers_vs_native']['chrome'],'chrome_subset':chrome,
    'subset_native_medians':small['medians']['native'],'subset_chrome_medians':small['medians']['chrome'],
    'records':{e:records[e] for e in ['v1','native','chrome']},
    'firefox_not_finished':True,'release_ready':False,'H4_complete':False,'no_repeat_or_threshold_change':True}
matrix.write(out/'checks.json',data)
(out/'record.py').write_bytes(Path(__file__).read_bytes())
lines=['# Integrated preview: Chrome subset misses H4 — 2026-10-16','',
    '**Release remains pending.** All 201 native and 201 Chrome layouts validate,',
    f"but Chrome's eleven-job median material difference is **+{chrome['median_difference_percent']:.6f}%** against the unchanged +1% limit.",
    'Every subset job remains within +5%. The original Firefox arm is still running;',
    'it will finish and be retained. No run is restarted and no bound is changed.','',
    'The complete native 65-job median difference from frozen v1 is 0%, passing',
    'its +0.5% limit. Chrome passes full G5: median +0.242546%, total +0.571472%,',
    'with all three individual seeds also inside the original G5 bounds. These',
    'passes do not override the subset failure. H4 remains open at 45% completed',
    'milestone weight. The failed preview candidate is 0a9fb44.','',
    '| Subset job | Native median | Chrome median | Chrome difference |',
    '| --- | ---: | ---: | ---: |']
for row in subset:
    name=row['id']
    lines.append(f"| {name} | {small['medians']['native'][name]:.9f} | {small['medians']['chrome'][name]:.9f} | {chrome['per_job_difference_percent'][name]:+.6f}% |")
lines += ['', 'All input/source/executable/site guards still match the committed plan.',
    'This report records a completed arm, not a new measurement. The raw outcomes',
    'remain in the active matrix and will be sealed when its original process ends.',
    'It does not establish which change or source of timing variation caused the gap.',
    'A subsequent candidate must have an actual implementation change, preserve',
    'geometry and deadlines, and earn its own performance evidence. The existing',
    'profile identifies collision scoring as a cost worth investigating; no new',
    'optimization is accepted from this failure alone.','',
    '[Recorded calculations and records](h4-preview-chrome-failure-20261016/checks.json)', '']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'chrome_subset_median_percent':chrome['median_difference_percent'],'release_ready':False,'original_measurement_continues':True}))
