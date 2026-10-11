"""Audited development tables with explicit missing seeds and failure-ranked statistics."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from statistics import median, quantiles
import uuid

import comparison_session as sessions
from lbf_report import contained_file
from svgnest import digest, write


def ranked_statistics(values, attempted, required):
    """Failures rank after every valid score, without inventing a numeric score."""
    if not 0<=len(values)<=attempted<=required or required<1:
        raise ValueError('Invalid attempt coverage')
    if any(not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or v<0 for v in values):
        raise ValueError('Comparison scores must be finite and nonnegative')
    values=sorted(values)
    def percentile(fraction):
        if attempted!=required:return {'state':'incomplete','value':None}
        rank=(required-1)*fraction
        low,high=math.floor(rank),math.ceil(rank)
        if high>=len(values):return {'state':'failed','value':None}
        return {'state':'finite','value':values[low]+(values[high]-values[low])*(rank-low)}
    return {'median':percentile(0.5),'quartiles':[percentile(p) for p in (0.25,0.5,0.75)]}


def summarize(slots, runs):
    if len({s['id'] for s in slots}) != len(slots) or not set(runs).issubset(s['id'] for s in slots):
        raise ValueError('Duplicate slots or unexpected results')
    groups = defaultdict(list)
    for slot in slots:
        key = tuple(slot[k] for k in ['tool','job','seconds','settings_role','settings','axis'])
        groups[key].append(slot)
    rows = []
    for key, members in sorted(groups.items()):
        seeds = [s['seed'] for s in members]
        if len(set(seeds)) != len(seeds):
            raise ValueError('Duplicate seed in one comparison group')
        found = [runs[s['id']] for s in members if s['id'] in runs]
        valid = [r for r in found if r['status']=='valid']
        metric_kinds = {r.get('score_kind','normalized_material') for r in valid}
        if len(metric_kinds)>1:
            raise ValueError('Different metrics cannot share a median')
        values = [r['metrics']['normalized_material'] if key[0]=='lbf' else r['score'] for r in valid]
        counts = dict(Counter(r['status'] for r in found))
        if not set(counts).issubset({'valid','invalid','unsupported','no_layout','timeout','failed'}):
            raise ValueError('Unknown native outcome')
        counts['missing'] = len(members)-len(found)
        ranked=ranked_statistics(values,len(found),len(members))
        rows.append(dict(zip(['tool','job','seconds','settings_role','settings','axis'],key)) | {
            'required_seeds':sorted(seeds),'outcomes':counts,'required':len(members),
            'completed':len(found),'all_seeds_valid':len(valid)==len(members) and len(members)>=3,
            'comparable_median':len(members)>=3 and ranked['median']['state']=='finite',
            'comparison_statistics':ranked,
            'metric':next(iter(metric_kinds),None),
            'valid_only_median':median(values) if values else None,
            'valid_only_quartiles':quantiles(values,n=4,method='inclusive') if len(values)>=2 else None,
            'slot_ids':[s['id'] for s in members]})
    return rows


def report(name):
    directory = sessions.session_dir(name)
    manifest = json.loads((directory/'manifest.json').read_bytes())
    entries = sessions.completed(directory,manifest)
    runs = {key:json.loads(contained_file(sessions.ROOT,entry['record']).read_bytes()) for key,entry in entries.items()}
    rows = summarize(manifest['slots'],runs)
    stamp = datetime.now(timezone.utc)
    stem = f'comparison-session-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    target = sessions.ROOT/'benchmarks/results'/stem
    value = {'recorded_at':stamp.isoformat(),'session':name,'manifest_sha256':digest(directory/'manifest.json'),
        'report_source_sha256':digest(Path(__file__)),'manifest':manifest,'completed_slots':len(entries),
        'required_slots':len(manifest['slots']),'complete':len(entries)==len(manifest['slots']),
        'statistics_policy_sha256':digest(sessions.ROOT/'benchmarks/STATISTICS.md'),
        'scope':'Development comparison only. Every declared seed participates: failed outcomes rank after valid scores; missing seeds prevent comparison. Failure-valued statistics have no invented numeric score. Valid-only statistics are diagnostic. No final quality gate is established.',
        'rows':rows,'attempts':[{**entry,'run':runs[key]} for key,entry in entries.items()]}
    write(target.with_suffix('.json'),value)
    lines = ['# Development comparison session','',value['scope'],'',
        f"Session `{name}`: {len(entries)}/{len(manifest['slots'])} attempts recorded. All failures and missing attempts remain visible.",'',
        '| Tool | Job | Budget | Settings role / configuration | Outcomes | All seeds valid | Comparison median | Comparison Q1–Q3 |',
        '| --- | --- | ---: | --- | --- | --- | ---: | --- |']
    for row in rows:
        def display(stat):return f"{stat['value']:.8f}" if stat['state']=='finite' else stat['state']
        middle=display(row['comparison_statistics']['median'])
        quartiles=row['comparison_statistics']['quartiles']
        spread=f'{display(quartiles[0])}–{display(quartiles[2])}'
        outcomes = ', '.join(f'{k}: {v}' for k,v in sorted(row['outcomes'].items()) if v)
        lines.append(f"| {row['tool']} | {row['job']} | {row['seconds']} s | {row['settings_role']} / {row['settings']} | {outcomes} | {'yes' if row['all_seeds_valid'] else 'no'} | {middle} | {spread} |")
    lines.extend(['', 'Scores are normalized material for B/M and original-polygon strip length for S; lower is better. Missing seeds prevent comparison. A failed median cannot produce a percentage reduction. Valid-only diagnostics are retained in JSON, separately from the comparison statistics. See [the frozen statistics policy](../STATISTICS.md).', '',
        f'[Full precision, frozen schedule and audited attempt records]({stem}.json).',''])
    with target.with_suffix('.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines))
    print(target.with_suffix('.md'))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name',required=True)
    report(parser.parse_args().name)
