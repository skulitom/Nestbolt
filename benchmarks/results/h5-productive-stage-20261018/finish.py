from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,shutil,sys,zipfile
import psutil
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'));import h5_productive_stage as runner
out=root/'benchmarks/results/h5-productive-stage-20261018'
load,write,digest=runner.load,runner.write,runner.digest
result=load(out/'results.json');plan=load(out/'plan.json');opened=load(out/'opened.json')
try:cmd=psutil.Process(opened['pid']).cmdline()
except psutil.NoSuchProcess:cmd=[]
assert not any('h5_productive_stage.py' in c for c in cmd)
assert result['guards_unchanged'] and runner.guards()==plan['guards']
assert digest(out/'plan.json')==opened['plan_sha256'] and result['wall_seconds']<1200
assert len(result['records'])==4
assert {(r['job'],r['kerf_mm'],r['seed']) for r in result['records']}=={(j,k,0) for j in runner.JOBS for k in [0.2,1.5]}
archives=[];observations=[];attempts=[]
for row in result['records']:
    archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
    checked_trace=runner.read_trace(archive,row)
    assert checked_trace==row['diagnosis'] and row['status']=='valid'
    with zipfile.ZipFile(archive) as z:
        case=json.loads(z.read('case.json'))
        assert case=={k:v for k,v in row.items() if k not in ['archive','archive_sha256','diagnosis']}
        assert set(z.namelist())==set(case['artifacts'])|{'case.json'}
        checked=json.loads(z.read('validate-stdout.json'));search=json.loads(z.read('nested/search.json'))
        job=json.loads(z.read('nested/job.json'));layout=json.loads(z.read('nested/layout.json'))
        assert checked['valid'] and search['validation']['valid']
        runner.prior.equivalent(checked['metrics'],search['validation']['metrics'])
        assert checked['metrics']==row['metrics'] and checked['metrics']['normalized_material']==row['material']
        assert len(layout['placements'])==sum(p['quantity'] for p in job['parts'])
        assert search['stats']==row['stats'] and search['riders']==row['riders']==0
        assert sha256(z.read('nested/layout.json')).hexdigest()==row['layout_sha256']
        assert row['search']['exit_code']==row['validation']['exit_code']==row['export']['exit_code']==0
        archives.append({'path':archive.name,'sha256':digest(archive),'bytes':archive.stat().st_size,'members':len(z.namelist())})
    attempts += [{'job':row['job'],'kerf_mm':row['kerf_mm'],**a} for a in checked_trace['attempt_rows']]
    observations.append({'job':row['job'],'kerf_mm':row['kerf_mm'],**{k:v for k,v in checked_trace.items() if k not in ['traces','attempt_rows']}})
accepted=[a for a in attempts if a['outcome']=='accepted']
summary={'attempts':len(attempts),'outcomes':dict(Counter(a['outcome'] for a in attempts)),
    'paired_attempts':sum(a['proposal']['paired'] for a in attempts),
    'paired_accepted':sum(a['proposal']['paired'] for a in accepted),
    'neutral_attempts':sum(a['neutral_inventory'] for a in attempts),
    'neutral_accepted':sum(a['neutral_inventory'] for a in accepted),
    'accepted_material_decreases':sum(a['after_material']<a['before_material'] for a in accepted),
    'accepted_extent_decreases':sum(a['after_last_extent']<a['before_last_extent'] for a in accepted),
    'retained_proposals':sum(r['retained_proposals'] for r in observations),
    'retained_neutral_proposals':sum(r['retained_neutral_proposals'] for r in observations),
    'quality_claim':False,'earlier_pilot_trajectory_reconstructed':False}
write(out/'observed-exchanges.json',{'summary':summary,'observations':observations,'attempts':attempts})
write(out/'verification.json',{'all_original_archives_verified':True,'all_traces_verified':True,
    'archives':archives,'valid':4,'actual_exchange_attempts':len(attempts),'unchanged_source_binary_input_guards':True,
    'original_job_metrics_and_quantities_verified':True,'H5_complete':False,'integrated':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'finish.py')
lines=['# Productive-exchange choices and repair allocations — 2026-10-18','',
    '**All four diagnostic layouts validate.** The observer records which',
    'original part types are available and move between sheets, requested repair',
    'time, elapsed duration, rejection stages and immediate',
    'material/last-sheet extent. These are new observations, not a reconstruction',
    'of the failed 72-outcome pilot or a quality comparison.','',
    '[The committed plan](h5-productive-stage-20261018/plan.json) uses the two',
    'mechanical development jobs, kerfs 0.2 and 1.5 mm, seed zero, 60 seconds',
    'and serial physical CCD0 CPU 8. All original algorithm settings remain.',
    'Instrumentation can perturb wall timing. Production stays unchanged.','',
    '| Job | Kerf mm | Attempts | Accepted pairs | Same-inventory accepted | Outcomes |',
    '| --- | ---: | ---: | ---: | ---: | --- |']
for row in observations:
    outcomes=', '.join(f'{k}: {v}' for k,v in row['outcomes'].items()) or 'none'
    lines.append(f"| {row['job']} | {row['kerf_mm']} | {row['attempts']} | {row['paired_accepted']} | {row['neutral_accepted']} | {outcomes} |")
lines += ['',f"Of {len(accepted)} accepted exchanges, {summary['neutral_accepted']} return the same original",
    'part types and quantities as they take. This preserves inventory, not',
    'necessarily positions or orientations. Immediate validated material',
    f"decreases in {summary['accepted_material_decreases']} accepted exchanges; last-sheet occupied",
    f"extent decreases in {summary['accepted_extent_decreases']}. These observations do not establish",
    'a later benefit or harm from rearrangement.','',
    f"There are {summary['retained_proposals']} retained proposals across the observed calls;",
    f"{summary['retained_neutral_proposals']} preserve inventory. Retained proposals are not necessarily",
    'attempted, and these counts are not all sampled configurations.','',
    f"The session took {result['wall_seconds']/60:.3f} minutes. All archive CRCs/member hashes,",
    'trace references, solver counters, original quantities, public exports and',
    'independently recomputed metrics pass. Source, input and binary guards match.',
    '[Every attempt](h5-productive-stage-20261018/observed-exchanges.json) and',
    '[verification](h5-productive-stage-20261018/verification.json) are retained.','',
    'No original failed result, gate, production implementation or held-out file',
    'is changed. **H2/H5 remain open; completed weight stays 60%.**','']
allocation=[]
for row in result['records']:
    traces=row['diagnosis']['traces'];valid=[t for t in traces if not t['disabled_or_expired'] and not t['baseline_invalid']]
    selected=[a for a in attempts if (a['job'],a['kerf_mm'])==(row['job'],row['kerf_mm'])]
    repairs=[a for a in selected if a['source_remaining'] is not None]
    itemsets=[dict(Counter(t['available_source_items'])) for t in valid]
    pairsets=[t['pair_choices'] for t in valid]
    allocation.append({'job':row['job'],'kerf_mm':row['kerf_mm'],'source_inventories':itemsets,
        'pair_choices':pairsets,'neutral_rejections':sum(a['outcome']=='neutral_inventory_rejected' for a in selected),
        'source_repairs':len(repairs),'source_failures':sum(a['outcome']=='source_repair_failed' for a in selected),
        'source_nonpositive_allowances':sum(a['source_remaining']<=0 for a in repairs),
        'source_remaining_range':([min(a['source_remaining'] for a in repairs),max(a['source_remaining'] for a in repairs)] if repairs else None),
        'source_elapsed_total':sum(a['source_elapsed'] for a in repairs),
        'source_elapsed_max':max((a['source_elapsed'] for a in repairs),default=0),
        'outcomes':row['diagnosis']['outcomes']})
write(out/'observed-allocations.json',{'records':allocation,'wall_durations_not_minimum_repair_time':True,'quality_claim':False})
lines += ['## Source choices and repair time','',
    '| Job | Kerf mm | Source inventory by original item ID | Pair choices by item ID | Neutral rejections | Source failures / repairs | Requested source time range, s | Total source time, s |',
    '| --- | ---: | --- | --- | ---: | ---: | --- | ---: |']
for r in allocation:
    lines.append(f"| {r['job']} | {r['kerf_mm']} | {r['source_inventories']} | {r['pair_choices']} | {r['neutral_rejections']} | {r['source_failures']} / {r['source_repairs']} | {r['source_remaining_range']} | {r['source_elapsed_total']:.6f} |")
lines += ['', 'Item IDs denote original model items; repeated IDs represent interchangeable',
    'copies. Retained choices are not necessarily attempted. Requested remaining',
    'time is logged immediately before each separator call and can be negative.',
    'Elapsed time can slightly overrun a checked deadline. These observations',
    'do not prove the minimum time needed or feasibility of failed assignments.','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps(summary))
