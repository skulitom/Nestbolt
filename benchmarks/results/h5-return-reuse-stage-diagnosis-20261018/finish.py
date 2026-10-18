from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
import shutil
import sys
import zipfile
import psutil
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'scripts'))
import h5_return_reuse_stage_diagnosis as runner
out=root/'benchmarks/results/h5-return-reuse-stage-diagnosis-20261018'
load,write,digest=runner.load,runner.write,runner.digest
result=load(out/'results.json');plan=load(out/'plan.json');opened=load(out/'opened.json')
try:cmd=psutil.Process(opened['pid']).cmdline()
except psutil.NoSuchProcess:cmd=[]
assert not any('h5_return_reuse_stage_diagnosis.py' in c for c in cmd)
assert result['guards_unchanged'] and runner.guards()==plan['guards']
assert digest(out/'plan.json')==opened['plan_sha256']
assert result['wall_seconds']<1200
assert len(result['records'])==4
assert {(r['job'],r['kerf_mm'],r['seed']) for r in result['records']}=={(j,k,0) for j in runner.JOBS for k in [0.2,1.5]}
archives=[];observations=[];attempts=[];sampling=Counter()
for row in result['records']:
    archive=out/row['archive'];assert digest(archive)==row['archive_sha256']
    verified=runner.read_trace(archive,row)
    assert verified==row['diagnosis'] and row['status']=='valid'
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
    attempts += [a for trace in verified['traces'] for a in trace['attempts']]
    sampling.update(verified['sampling_totals'])
    observations.append({'job':row['job'],'kerf_mm':row['kerf_mm'],**{k:v for k,v in verified.items() if k!='traces'}})
stages={'all':dict(Counter(a['outcome'] for a in attempts)),
    'complete':dict(Counter(a['outcome'] for a in attempts if a['victims']==a['blockers'])),
    'partial':dict(Counter(a['outcome'] for a in attempts if a['victims']<a['blockers']))}
frame_modes=dict(Counter(a['frame']['mode'] for a in attempts))
by_frame={mode:dict(Counter(a['outcome'] for a in attempts if a['frame']['mode']==mode)) for mode in sorted(frame_modes)}
write(out/'observed-frames.json',{'frame_modes':frame_modes,'outcomes_by_frame':by_frame,
    'forbidden_member_counts':dict(Counter(str(sum(not m['hypothetical_allowed'] for m in a['frame']['members'])) for a in attempts if a['frame']['mode']=='forbidden_translation')),
    'validated_material_changes':[{'before':a['before_material'],'after':a['after_material'],'outcome':a['outcome']} for a in attempts if a['after_material'] is not None],
    'quality_claim':False})
write(out/'observed-stages.json',{'observations':observations,'aggregate_attempt_outcomes':stages,'sampling_totals':dict(sampling),
    'quality_or_speed_claim':False,'global_infeasibility_claim':False})
write(out/'verification.json',{'all_original_archives_and_traces_verified':True,'archives':archives,'valid':4,
    'actual_exchange_attempts':len(attempts),'unchanged_source_binary_input_guards':True,
    'original_job_metrics_and_quantities_verified':True,'H5_complete':False,'integrated':False,'completed_weight_percent':60})
shutil.copyfile(__file__,out/'finish.py')

source_rows=[]
for record in result['records']:
    for ti,trace in enumerate(record['diagnosis']['traces']):
        for ai,attempt in enumerate(trace['attempts']):
            if attempt['source_reused'] is None:continue
            source_rows.append({'job':record['job'],'kerf_mm':record['kerf_mm'],
                'trace_index':ti,'attempt_index':ai,**{k:attempt[k] for k in [
                'source_inventory','source_reused','source_fresh_loss','source_initial_loss','source_loss',
                'source_initial_weighted_loss','source_best_weighted_loss','source_elapsed_seconds',
                'source_available_budget','outcome']}})
reused=[a for a in source_rows if a['source_reused']]
reuse_summary={'source_attempts':len(source_rows),'reused_attempts':len(reused),
    'reused_improved_loss':sum(a['source_loss']<a['source_initial_loss'] for a in reused),
    'reused_zero_final_loss':sum(a['source_loss']==0 for a in reused),
    'all_zero_final_loss':sum(a['source_loss']==0 for a in source_rows),
    'outcomes_by_reuse':{str(flag):dict(Counter(a['outcome'] for a in source_rows if a['source_reused'] is flag)) for flag in [False,True]},
    'source_repair_seconds':sum(a['source_elapsed_seconds'] for a in source_rows),
    'rows':source_rows,'quality_claim':False,'minimum_required_repair_time_claim':False}
write(out/'observed-reuse.json',reuse_summary)
lines=['# Source-repair reuse stages — 2026-10-18','',
    '**All four diagnostic layouts validate.** These observations locate repair',
    'and acceptance stages. They do not measure improvement or replace the',
    'failed 72-outcome comparison.','',
    'The [committed plan](h5-return-reuse-stage-diagnosis-20261018/plan.json)',
    'uses both mechanical jobs, both kerfs, seed zero, 60 seconds and serial',
    'physical CCD0 CPU 8. Production and the rejected candidate are unchanged.',
    'Read-only tracing preserves decisions but can perturb wall deadlines.','',
    '| Job | Kerf mm | Attempts | Reuses | Outcomes after reuse | Other outcomes |',
    '| --- | ---: | ---: | ---: | --- | --- |']
readable=lambda d:', '.join(f'{k}: {v}' for k,v in d.items()) or 'none'
for row in observations:
    counts=row['outcomes_by_reuse'];others=Counter(counts['False'])+Counter(counts['None'])
    lines.append(f"| {row['job']} | {row['kerf_mm']} | {row['attempts']} | {row['source_reuses']} | {readable(counts['True'])} | {readable(others)} |")
lines += ['',f"The session takes {result['wall_seconds']/60:.3f} minutes. Original quantities,",
    'independently recomputed metrics, public exports and zero reported hole',
    'riders pass. Every original ZIP passes CRC and member/hash checks. Trace',
    'attempt, acceptance and reuse counts match the saved solver counters.',
    'Reused attempts preserve the prior inventory and best unweighted loss',
    'within the same invocation, and start no worse than the fresh alternative.','',
    f"There are {len(reused)} reused source attempts; {reuse_summary['reused_improved_loss']}",
    f"reduce their initial loss and {reuse_summary['reused_zero_final_loss']} finish with zero source loss.",
    'A zero internal loss still requires whole-job geometry and material checks.','',
    '[Source loss/time observations](h5-return-reuse-stage-diagnosis-20261018/observed-reuse.json)',
    'retain every fresh/resumed repair, inventory, loss, available budget and',
    'elapsed duration. [All stages](h5-return-reuse-stage-diagnosis-20261018/observed-stages.json)',
    'and [frames](h5-return-reuse-stage-diagnosis-20261018/observed-frames.json)',
    'retain sampling and orientation context. The',
    '[verification](h5-return-reuse-stage-diagnosis-20261018/verification.json)',
    'binds the results to the unchanged source, binary and input guards.','',
    'Failed finite repairs do not establish impossibility. Observed repair',
    'durations are not minimum required times, and losses are not quality scores.',
    'Any new candidate needs separate correctness checks and a committed paired',
    'comparison. No gate change, integration or reserved-input access.',
    '**H2/H5 remain open; completed weight stays 60%.**','']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'all_four_valid':True,'stages':stages,'reuse':{k:v for k,v in reuse_summary.items() if k!='rows'},'wall_seconds':result['wall_seconds']}))
