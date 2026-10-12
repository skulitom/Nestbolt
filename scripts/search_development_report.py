"""Audit all65 development layouts and compare fixed-work diagnostics, never gates."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import median
import subprocess

from construct_profile_batch import ROOT, audited_profile, digest, select_cases


def summarize(rows):
    finite = [r for r in rows if r['competitor_60'] is not None]
    comparable = [r for r in finite if r['material'] is not None]
    missing = len(finite)-len(comparable)
    differences = [r['reduction_percent'] for r in comparable]
    return {'jobs':len(rows), 'outcomes':dict(Counter(r['status'] for r in rows)),
            'finite_competitors':len(finite), 'no_finite_competitor':len(rows)-len(finite),
            'missing_valid_nestbolt_comparisons':missing,
            'median_reduction_percent':median(differences) if differences and not missing else None,
            'win_or_tie':sum(r['win_or_tie'] is True for r in comparable),
            'more_than_one_percent_worse':sum(r['reduction_percent'] < -1 for r in comparable)}


def first_reached(profile, target):
    """Arrival of an accepted independently checked incumbent is an upper bound."""
    if target is None or profile['runs'][0]['exit_code'] != 0:
        return None
    elapsed = []
    for event in profile['runs'][0]['progress']:
        try:
            progress = json.loads(event['message'])
        except (ValueError,TypeError):
            continue
        if (progress.get('accepted') and progress.get('complete') and progress.get('material') is not None
                and progress['material'] <= target*(1+1e-6)):
            elapsed.append(event['elapsed_seconds'])
    return min(elapsed) if elapsed else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--retained',type=Path,help='Optional earlier four-case diversity proof')
    args = parser.parse_args()
    args.batch = args.batch.resolve(strict=True)
    if args.retained:
        args.retained = args.retained.resolve(strict=True)
    batch = json.loads(args.batch.read_bytes())
    retained = json.loads(args.retained.read_bytes()) if args.retained else {
        'final_runs':[], 'final_binary_sha256':batch['binary_sha256']}
    if batch['binary_sha256'] != retained['final_binary_sha256']:
        raise ValueError('Current runs must use the same executable')
    sources = [args.batch,Path(__file__),ROOT/'scripts/construct_profile_batch.py',
               ROOT/'benchmarks/baseline-target.json']
    if args.retained:
        sources.insert(1,args.retained)
    frozen = json.loads(sources[-1].read_bytes())
    baseline_path = ROOT/frozen['proof']
    if digest(baseline_path) != frozen['proof_sha256']:
        raise ValueError('Frozen comparison proof changed')
    sources.append(baseline_path)
    references = {seconds:{r['job']:r['competitor'] for r in json.loads(baseline_path.read_bytes())['rows']
                          if r['seconds'] == seconds} for seconds in [60,300]}
    prior = {}
    for path in ['benchmarks/results/repack-sheet-20261012T035142Z-a7b22154.json',
                 'benchmarks/results/repack-maker-20261012T035142Z-54130739.json']:
        sources.append(ROOT/path)
        for row in json.loads((ROOT/path).read_bytes())['rows']:
            prior[row['job']] = row
    cases = {case['id']:case for case in select_cases(ROOT)}
    entries = dict()
    for entry in batch['rows'] + retained['final_runs']:
        job = entry.get('job',entry.get('profile',{}).get('job'))
        if job not in cases or job in entries:
            raise ValueError('Unexpected or duplicate current job')
        entries[job] = entry
    if entries.keys() != cases.keys():
        raise ValueError('Every frozen development job requires an explicit outcome')
    rows = []
    for job, case in cases.items():
        entry = entries[job]
        result = None
        validation = None
        current = None
        if entry.get('status') == 'harness_error':
            status = 'harness_error'
        else:
            profile_path = ROOT/entry['profile_path']
            if digest(profile_path) != entry['profile_sha256']:
                raise ValueError('Retained profile changed')
            audit = audited_profile(ROOT,profile_path,case,batch['binary_sha256'])
            status, current, result = audit['status'], audit['profile'], audit['result']
            if result is not None:
                binary = Path(current['binary'])
                if digest(binary) != batch['binary_sha256']:
                    raise ValueError('Validation executable changed')
                command = [str(binary),'validate','--job',str(ROOT/'benchmarks/datasets'/case['path']),
                           '--layout',str(profile_path.parent/'0/layout.json')]
                checked = subprocess.run(command,cwd=ROOT,capture_output=True,timeout=90,check=True)
                validation = json.loads(checked.stdout)
                if validation != result['validation']:
                    raise ValueError('Standalone validator disagrees with retained result')
        competitor = references[60][job]
        score = result['validation']['metrics']['normalized_material'] if status == 'valid' else None
        old = prior[job]['report']['validation']['metrics']['normalized_material']
        reduction = 100*(1-score/competitor['median']) if score is not None and competitor else None
        target300 = references[300].get(job)
        reached = first_reached(current,target300['median']) if current and target300 else None
        rows.append({'job':job,'status':status,'job_sha256':case['sha256'],
            'profile_path':entry.get('profile_path'),'profile_sha256':entry.get('profile_sha256'),
            'material':score,'prior_material':old,
            'change_from_prior_percent':100*(1-score/old) if score is not None else None,
            'prior_requested_passes':prior[job]['report']['search']['requested_passes'],
            'completed_passes':result['completed_passes'] if result else None,
            'stopped':result['stopped'] if result else None,
            'cpu_seconds':current['runs'][0]['cpu_seconds'] if current else None,
            'wall_seconds':current['runs'][0]['wall_seconds'] if current else None,
            'competitor_60':competitor,'reduction_percent':reduction,
            'win_or_tie':score <= competitor['median']*(1+1e-6) if score is not None and competitor else None,
            'competitor_300':target300,'target300_observed_seconds':reached,
            'reached_target300_within30s':reached <= 30 if reached is not None else False if target300 else None,
            'standalone_validation':validation})
    stats = summarize(rows)
    changes = [r['change_from_prior_percent'] for r in rows if r['material'] is not None]
    stats['relative_to_prior_fixed_work'] = {'better':sum(c>0.0001 for c in changes),
        'tie':sum(abs(c)<=0.0001 for c in changes),'worse':sum(c < -0.0001 for c in changes)}
    stats['available_300s_targets'] = {'finite':sum(r['competitor_300'] is not None for r in rows),
        'within30s':sum(r['reached_target300_within30s'] is True for r in rows),
        'no_finite_competitor':sum(c is None for c in references[300].values()),
        'jobs_without300s_reference':len(rows)-len(references[300])}
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    target = ROOT/'benchmarks/results'/('search-coverage-'+stamp+'.json')
    proof = {'scope':f'All 65 development B/M jobs, seed 0, mixed search up to 1,024 passes / 80M queries / 60 s safety deadline. {len(retained["final_runs"])} earlier runs reused; {len(batch["rows"])} new runs. Prior Nestbolt baseline uses 64 B passes and 6 M passes; competitor reference uses three-seed 60 s medians. Work and populations differ: this is quality triage, not G1/G2/G4 acceptance. Ten held-out maker jobs remain unused.',
             'sources':{p.relative_to(ROOT).as_posix():digest(p) for p in sources},
             'summary':stats,'rows':rows}
    with target.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(proof,stream,indent=2);stream.write('\n')
    changes = stats['relative_to_prior_fixed_work']
    timing = stats['available_300s_targets']
    reduction = ('not computed because a comparable job failed' if stats['median_reduction_percent'] is None
                 else f"{stats['median_reduction_percent']:.6f}%")
    lines = ['# Combined placement search: development coverage','',proof['scope'],'',
        f"Valid layouts: **{stats['outcomes'].get('valid',0)}/65**. Against the preceding fixed-work layouts: {changes['better']} better, {changes['tie']} tied, {changes['worse']} worse; failed outputs are counted separately.",'',
        f"There are {stats['finite_competitors']} finite competitor comparisons at 60 s and {stats['no_finite_competitor']} jobs with no finite competitor. Nestbolt wins or ties {stats['win_or_tie']} comparisons; {stats['more_than_one_percent_worse']} are more than 1% worse. Median material reduction: **{reduction}**.",'',
        f"Of the {timing['finite']} available finite 300 s targets, {timing['within30s']} are reached within 30 s. Another {timing['no_finite_competitor']} subset job has no finite competitor, and {timing['jobs_without300s_reference']} jobs have no 300 s reference. Accepted-progress arrival provides an upper bound on observed time to target. Missing results never earn free wins. This subset cannot establish G4 across all sheet jobs.",'',
        '| Job | Material | Change from prior | Reduction vs 60 s competitor | Passes | Stop |',
        '| --- | ---: | ---: | ---: | ---: | --- |']
    for r in rows:
        num = lambda x: '—' if x is None else f'{x:.6f}'
        percent = lambda x: '—' if x is None else f'{x:.6f}%'
        stop = r['stopped'] or ('requested work complete' if r['status']=='valid' else r['status'])
        lines.append(f"| {r['job']} | {num(r['material'])} | {percent(r['change_from_prior_percent'])} | {percent(r['reduction_percent'])} | {r['completed_passes']} | {stop} |")
    lines += ['',f'[Full-precision audit and every standalone validation report]({target.name})','']
    with target.with_suffix('.md').open('x',encoding='utf-8',newline='\n') as stream:stream.write('\n'.join(lines))
    print(target,flush=True)
    print(json.dumps(stats,indent=2),flush=True)


if __name__ == '__main__':
    main()
