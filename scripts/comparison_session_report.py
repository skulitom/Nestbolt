"""Audited development tables: missing or invalid seeds never become eligible medians."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import median, quantiles
import uuid

import comparison_session as sessions
from lbf_report import contained_file
from svgnest import digest, write


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
        counts['missing'] = len(members)-len(found)
        rows.append(dict(zip(['tool','job','seconds','settings_role','settings','axis'],key)) | {
            'required_seeds':sorted(seeds),'outcomes':counts,'required':len(members),
            'completed':len(found),'eligible':len(valid)==len(members) and len(members)>=3,
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
        'scope':'Development comparison only. Valid-only statistics are diagnostic; an eligible row requires every declared seed to be independently valid. No final quality gate is established.',
        'rows':rows,'attempts':[{**entry,'run':runs[key]} for key,entry in entries.items()]}
    write(target.with_suffix('.json'),value)
    lines = ['# Development comparison session','',value['scope'],'',
        f"Session `{name}`: {len(entries)}/{len(manifest['slots'])} attempts recorded. All failures and missing attempts remain visible.",'',
        '| Tool | Job | Budget | Settings role / configuration | Outcomes | Eligible | Median of valid scores | Q1–Q3 of valid scores |',
        '| --- | --- | ---: | --- | --- | --- | ---: | --- |']
    for row in rows:
        middle = '—' if row['valid_only_median'] is None else f"{row['valid_only_median']:.8f}"
        quartiles = row['valid_only_quartiles']
        spread = '—' if quartiles is None else f'{quartiles[0]:.8f}–{quartiles[2]:.8f}'
        outcomes = ', '.join(f'{k}: {v}' for k,v in sorted(row['outcomes'].items()) if v)
        lines.append(f"| {row['tool']} | {row['job']} | {row['seconds']} s | {row['settings_role']} / {row['settings']} | {outcomes} | {'yes' if row['eligible'] else 'no'} | {middle} | {spread} |")
    lines.extend(['', 'Scores are normalized material for B/M and original-polygon strip length for S; lower is better. Incomplete or failed groups cannot be used for acceptance or a baseline-gap claim.', '',
        f'[Full precision, frozen schedule and audited attempt records]({stem}.json).',''])
    with target.with_suffix('.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines))
    print(target.with_suffix('.md'))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name',required=True)
    report(parser.parse_args().name)
