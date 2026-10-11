"""Combine explicitly selected audited batches without dropping missing or failed seeds."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from comparator_batch_report import TOOLS, audit_batch
from comparison_session_report import summarize
from dataset_selection import development_cases
from svgnest import ROOT, digest, write


def combine(tool, dataset, seconds, settings, cases, batches):
    axis = 'x' if dataset == 'S' else 'y'
    role = 'identical_constraints' if settings == 'identical' else 'best_native_settings'
    slots = [{
        'id': f"{case['id']}:{seed}", 'tool': tool, 'job': case['id'],
        'job_sha256': case['sha256'], 'seconds': seconds, 'seed': seed,
        'settings_role': role, 'settings': settings, 'axis': axis,
    } for case in cases for seed in [0, 1, 2]]
    expected = {row['id']: row for row in slots}
    attempts = {}
    revisions = set()
    for batch, rows in batches:
        if (batch['dataset'], batch['seconds'], batch['settings'], batch['axis']) != (dataset, seconds, settings, axis):
            raise ValueError('Batch differs from the requested dataset, budget, settings or axis')
        for row in rows:
            run = row['run']
            key = f"{run['job']}:{run['seed']}"
            if key not in expected or run['job_sha256'] != expected[key]['job_sha256']:
                raise ValueError('Unexpected job, seed or changed source')
            if run.get('phase') != 'development':
                raise ValueError('Development tables cannot include final/held-out attempts')
            if key in attempts:
                raise ValueError('Duplicate attempt: select batches explicitly; never choose by score')
            revisions.add(run['revision'])
            attempts[key] = row
    if len(revisions) > 1:
        raise ValueError('Different upstream versions cannot share a comparison table')
    return slots, attempts, summarize(slots, {key: row['run'] for key, row in attempts.items()})


def report(args):
    manifest, cases = development_cases(ROOT, args.dataset)
    selected = [path.resolve(strict=True) for path in args.batch]
    audited = [audit_batch(path, args.tool) for path in selected]
    slots, attempts, rows = combine(args.tool, args.dataset, args.seconds, args.settings, cases, audited)
    stamp = datetime.now(timezone.utc)
    stem = f'comparison-batches-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    target = ROOT/'benchmarks/results'/stem
    value = {
        'recorded_at': stamp.isoformat(), 'tool': args.tool, 'dataset': args.dataset,
        'seconds': args.seconds, 'settings': args.settings,
        'scope': 'Development comparison slice, not a complete M1 or final quality gate. '
                 'All three declared seeds participate. Missing seeds prevent comparison; failures rank after finite scores.',
        'sources': {name: digest(ROOT/name) for name in [
            'scripts/batch_comparison_report.py', 'scripts/comparator_batch_report.py',
            'scripts/comparison_session_report.py', f'scripts/{args.tool}_report.py',
            'benchmarks/STATISTICS.md']},
        'dataset_manifest_sha256': digest(manifest),
        'batches': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': digest(p), 'manifest': b}
                    for p, (b, _) in zip(selected, audited)],
        'required_slots': len(slots), 'completed_slots': len(attempts),
        'complete': len(slots) == len(attempts), 'rows': rows,
        'attempts': [{'slot_id': key, **row} for key, row in sorted(attempts.items())],
    }
    write(target.with_suffix('.json'), value)
    lines = [f'# {args.tool}: three-seed development comparison', '', value['scope'], '',
             f"{args.dataset}, {args.seconds} s, {args.settings}: {len(attempts)}/{len(slots)} attempts audited.", '',
             '| Job | Outcomes | Median | Q1 | Q3 |', '| --- | --- | ---: | ---: | ---: |']
    for row in rows:
        def display(stat):
            return f"{stat['value']:.8f}" if stat['state'] == 'finite' else stat['state']
        stats = row['comparison_statistics']
        outcomes = ', '.join(f'{key}: {count}' for key, count in sorted(row['outcomes'].items()) if count)
        lines.append(f"| {row['job']} | {outcomes} | {display(stats['median'])} | "
                     f"{display(stats['quartiles'][0])} | {display(stats['quartiles'][2])} |")
    lines += ['', 'Metric: original-polygon strip length for S, normalized material for B/M. '
              'This explicitly selected batch set retains runner and validator versions per attempt; '
              'it does not establish a frozen final comparison.', '',
              f'[Full precision, selection and audited evidence]({stem}.json).', '']
    with target.with_suffix('.md').open('x', encoding='utf-8', newline='\n') as out:
        out.write('\n'.join(lines))
    with (ROOT/'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as out:
        out.write(f'\n- {stamp.isoformat()} | {args.tool} {args.dataset} {args.settings}, '
                  f'{args.seconds} s: {len(attempts)}/{len(slots)} audited development attempts '
                  f'| [three-seed table](benchmarks/results/{stem}.md). No final gate.\n')
    print(target.with_suffix('.md'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tool', choices=TOOLS, required=True)
    parser.add_argument('--dataset', choices=['S', 'B', 'M'], required=True)
    parser.add_argument('--settings', required=True)
    parser.add_argument('--seconds', type=int, choices=[60, 300], required=True)
    parser.add_argument('--batch', type=Path, action='append', required=True)
    report(parser.parse_args())
