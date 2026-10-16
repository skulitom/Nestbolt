"""Seal the complete depth-three pilot without repeating any search."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json, shutil, sys, zipfile
import psutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'benchmarks/results/h4-quadtree-depth-probe-20261016'
sys.path.insert(0,str(ROOT/'scripts'))
import h4_quadtree_depth_probe as pilot
quality=pilot.quality;load=pilot.load;write=pilot.write;digest=quality.digest
result=load(OUT/'results.json');plan=load(OUT/'plan.json');opened=load(OUT/'opened.json')
assert not psutil.pid_exists(opened['pid']) or not any('h4_quadtree_depth_probe.py' in p for p in psutil.Process(opened['pid']).cmdline())
assert result['guards_unchanged'] and pilot.guards(plan['cases'])==plan['guards']
assert digest(OUT/'plan.json')==opened['plan_sha256']
assert load(OUT/'records.json')==result['records']
summary=quality.summarize(result['records'],plan['cases'],[0,1,2],60)
assert summary==result['summary']
checked=[];affinity=[]
for engine,records in result['records'].items():
    assert len(records)==33 and {(r['job'],r['seed']) for r in records}=={(r['id'],s) for r in plan['cases'] for s in [0,1,2]}
    for row in records:
        folder=ROOT/row['directory'];assert load(folder/'case.json')==row
        if row['status']=='valid':
            validation=load(folder/'validate-stdout.json')
            saved=load(folder/('search-stdout.json' if engine=='native' else 'result.json'))
            layout=load(folder/'layout.json');case=next(r for r in plan['cases'] if r['id']==row['job'])
            assert validation['valid'] and saved['validation']['valid']
            assert quality.equivalent(validation['metrics'],saved['validation']['metrics'])==0
            assert row['material']==validation['metrics']['normalized_material']
            assert digest(folder/'layout.json')==row['layout_sha256']
            assert len(layout['placements'])==sum(r['quantity'] for r in load(ROOT/case['path'])['parts'])
            if 'library' in case:
                public=load(folder/'public-validate-stdout.json');assert public['valid']
                assert quality.equivalent(validation['metrics'],public['metrics'])==0
        checked.append({'engine':engine,'job':row['job'],'seed':row['seed'],'status':row['status'],'layout_sha256':row.get('layout_sha256')})
    if engine!='native':
        for seed in [0,1,2]:
            execution=load(OUT/engine/f's{seed}'/'execution.json')
            affinity.append({'engine':engine,'seed':seed,'exit_code':execution['exit_code'],'affinity_errors':execution['affinity_errors']})
for name,expected in plan['guards']['files'].items():
    source=ROOT/name;assert digest(source)==expected
    target=OUT/'snapshots'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
valid=sum(r['status']=='valid' for r in checked)
passes=summary['passes_subset'] and valid==99 and all(r['exit_code']==0 and not r['affinity_errors'] for r in affinity)
write(OUT/'verification.json',{'all_saved_artifacts_verified':True,'attempts':len(checked),'valid':valid,'records':checked,'browser_batches':affinity,'summary_recomputed':True,'guards_unchanged':True,'passed_pilot':passes,'H4_complete':False})
decision='Eligible for integration checks and a fresh full matrix; no H4 completion or release readiness yet' if passes else 'Reject for integration; preserve this failed pilot and diagnose before another changed candidate'
write(OUT/'assessment.json',{'decision':decision,'passed_pilot':passes,'integrated':False,'H4_complete':False,'completed_weight_percent':45,'results_sha256':digest(OUT/'results.json')})
shutil.copyfile(__file__,OUT/'finish.py')
files=sorted(p for p in OUT.rglob('*') if p.is_file());archive=OUT/'raw.zip';assert not archive.exists()
inventory={p.relative_to(OUT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in files}
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and set(z.namelist())==set(inventory)
    for name,r in inventory.items():
        raw=z.read(name);assert len(raw)==r['bytes'] and sha256(raw).hexdigest()==r['sha256']
write(OUT/'integrity.json',{'sha256':digest(archive),'bytes':archive.stat().st_size,'members':inventory,'crc_and_every_member_verified':True})
for name in ['native','chrome','firefox','snapshots']:
    target=(OUT/name).resolve();assert target.is_relative_to(OUT.resolve()) and target!=OUT
    for p in target.rglob('*'):
        if p.is_file():assert digest(p)==inventory[p.relative_to(OUT).as_posix()]['sha256']
    shutil.rmtree(target)
lines=['# Isolated collision-tree depth pilot — 2026-10-16','','**'+str(valid)+'/99 layouts valid. '+('Both browser subsets pass.' if passes else 'The candidate does not pass the pilot.')+'**','',decision+'.','',
'The [committed plan](h4-quadtree-depth-probe-20261016/plan.json) fixes all eleven',
'H4 development jobs, 60 seconds and seeds 0–2. The sole algorithm setting',
'change is separator-window base tree depth four to three; original geometry,',
'leaf threshold, aspect scaling, work coefficients and search budgets are unchanged.',
'Native and each browser run separately on physical CCD0 cores 0,2,…14, with',
'at most eight simultaneous searches. This session starts after both earlier',
'H4/H5 measurements finish and are sealed; no measured sessions overlap.',
f"The session took {result['wall_seconds']/60:.3f} minutes. Guards remain unchanged.",'',
'## Material comparison','',
'Per-job material is the median of all three fixed seeds. Positive differences',
'are worse. The original limits remain +1% subset median and +5% for every job.','',
'| Browser | Median vs native | Worst job | Total material | Pass |',
'| --- | ---: | ---: | ---: | --- |']
for engine,c in summary['comparisons'].items():
    def value(k):return 'incomplete' if c[k] is None else f"{c[k]:+.6f}%"
    lines.append(f"| {engine} | {value('median_difference_percent')} | {value('worst_difference_percent')} | {value('total_difference_percent')} | {'yes' if c['passes_subset'] else 'NO'} |")
lines+=['','All attempts and failures remain in [results](h4-quadtree-depth-probe-20261016/results.json).',
'Every valid layout covers all requested parts and agrees exactly with independently',
'recomputed original-geometry metrics; example library/request checks also agree.',
'[Verification](h4-quadtree-depth-probe-20261016/verification.json) retains all six',
'browser batch exits and affinity observations. Reliable temperatures are unavailable.',
'Hazard traversal order can change, so no fixed-work identity or isolated speed claim is made.','',
f"The raw archive has {len(inventory):,} members, {archive.stat().st_size:,} bytes and",
f"SHA-256 `{digest(archive)}`. CRC, every member size and hash pass.",
'Original layouts, diagnostics, inputs, runner and exact source/executable/site',
'snapshots remain preserved. Full quality/native matrices, current browser scale',
'and package checks remain separate requirements. Earlier failed comparisons',
'remain authoritative for their builds. H4 stays open; completion remains 45%.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'valid':valid,'passed_pilot':passes,'comparison':summary['comparisons'],'archive_sha256':digest(archive)}))
