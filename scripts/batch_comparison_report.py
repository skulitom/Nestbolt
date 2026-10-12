"""Combine explicitly selected audited batches without dropping missing or failed seeds."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import uuid

from comparator_batch_report import TOOLS, audit_batch
from comparison_session_report import summarize
from comparison_cases import comparison_cases
from lbf_report import contained_file
from svgnest import ROOT, digest, write


def split_build_failures(rows):
    """Retain every solver outcome; only a failed checker build can be replaced."""
    retained, excluded = [], []
    for row in rows:
        run = row['run']
        if run['status'] != 'failed':
            retained.append(row)
            continue
        if (run.get('reason') != "Command '['cargo', 'build', '-p', 'nestbolt-cli', '--locked']' returned non-zero exit status 101."
                or run.get('score') is not None
                or any(k in run for k in ['validator_sha256', 'exit_code', 'stages_ms', 'candidates', 'controller_solve_ms'])
                or any(name not in ['job.json', 'request.json', 'input.svg'] and not (name.startswith('input-') and name.endswith('.svg'))
                       for name in run['outputs'])):
            raise ValueError('Only an unstarted checker-build failure may be replaced')
        excluded.append(row)
    if not excluded:
        raise ValueError('The replacement batch contains no failed checker builds')
    return retained, excluded


def infrastructure_failure_kind(run, raw):
    """Recognize harness faults, never native crashes or failed layouts."""
    if (run['status'] != 'failed'
            or run.get('score') is not None or run.get('metrics') is not None
            or raw.get('status') != 'failed' or len(raw.get('errors', [])) != 1):
        raise ValueError('Not a recognized infrastructure failure')
    error = raw['errors'][0]
    stages = raw.get('stages_ms', {})
    if run.get('tool') == 'SVGnest':
        if (error.startswith('Error: page.evaluate: Error: Source coordinate rounded during import: copy-')
                and raw.get('controller_solve_ms') is None
                and raw.get('candidates') == 0 and raw.get('last') is None):
            return 'exact_coordinate_guard_before_solve'
        raise ValueError('Not a recognized SVGnest infrastructure failure')
    if run.get('tool') != 'deepnest-next':
        raise ValueError('Not a recognized Deepnest infrastructure failure')
    if (re.fullmatch(r'Error: Command failed: taskkill /PID [1-9][0-9]* /T /F', error)
            and 'budget_finished' in stages
            and raw.get('controller_solve_ms', 0) >= run['seconds'] * 1000
            and raw.get('candidates', 0) > 0 and raw.get('last')
            and 0 <= raw['last']['elapsed_ms'] <= run['seconds'] * 1000):
        return 'cleanup_after_budget'
    if (error.startswith('Error: Command failed: powershell.exe -NoProfile -NonInteractive -File ')
            and 'cpu-tree-job.ps1' in error and 'Win32Exception,cpu-tree-job.ps1' in error
            and 'Access is' in error and 'denied' in error
            and 'source_imported' in stages and 'budget_finished' not in stages
            and raw.get('controller_solve_ms') is None
            and raw.get('candidates') == 0 and raw.get('last') is None):
        return 'affinity_before_solve'
    raise ValueError('Not a recognized Deepnest infrastructure failure')


def split_infrastructure_failures(rows):
    retained, excluded = [], []
    for row in rows:
        run = row['run']
        if run['status'] != 'failed':
            retained.append(row)
            continue
        record = contained_file(ROOT, row['record'])
        raw_path = record.parent/'browser-result.json'
        if digest(raw_path) != run['outputs'].get('browser-result.json'):
            raise ValueError('Infrastructure evidence changed')
        kind = infrastructure_failure_kind(run, json.loads(raw_path.read_bytes()))
        excluded.append({**row, 'infrastructure_failure_kind': kind})
    if not excluded:
        raise ValueError('The replacement batch contains no infrastructure failures')
    return retained, excluded


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
    manifest, cases = comparison_cases(ROOT, args.dataset, args.seconds)
    selected = [path.resolve(strict=True) for path in args.batch]
    audited = [audit_batch(path, args.tool) for path in selected]
    replace = {path.resolve(strict=True) for path in getattr(args, 'replace_build_failures', [])}
    infrastructure = {path.resolve(strict=True) for path in getattr(args, 'replace_infrastructure_failures', [])}
    if not (replace | infrastructure).issubset(selected) or replace & infrastructure:
        raise ValueError('A replacement must name an explicitly audited batch')
    excluded, infra_excluded, filtered = [], [], []
    for path, (batch, records) in zip(selected, audited):
        if path in replace:
            records, removed = split_build_failures(records)
            excluded.extend(removed)
        elif path in infrastructure:
            records, removed = split_infrastructure_failures(records)
            infra_excluded.extend(removed)
        filtered.append((batch, records))
    slots, attempts, rows = combine(args.tool, args.dataset, args.seconds, args.settings, cases, filtered)
    for row in excluded + infra_excluded:
        run = row['run']
        replacement = attempts.get(f"{run['job']}:{run['seed']}")
        if replacement is None or replacement['sha256'] == row['sha256']:
            raise ValueError('Every excluded infrastructure failure needs an audited replacement attempt')
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
            'benchmarks/STATISTICS.md', 'scripts/comparison_cases.py',
            'scripts/matrix_plan.py', 'benchmarks/matrix-plan.json']},
        'dataset_manifest_sha256': digest(manifest),
        'batches': [{'path': p.relative_to(ROOT).as_posix(), 'sha256': digest(p), 'manifest': b}
                    for p, (b, _) in zip(selected, audited)],
        'required_slots': len(slots), 'completed_slots': len(attempts),
        'complete': len(slots) == len(attempts), 'rows': rows,
        'replaced_checker_build_failures': excluded,
        'replaced_infrastructure_failures': infra_excluded,
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
    if excluded:
        lines += [f'{len(excluded)} explicitly named checker-build failures occurred before the competitor started. '
                  'Their audited records remain in the JSON alongside all replacement outcomes. '
                  'Solver failures, invalid layouts and timeouts are never replaced by this option.', '']
    if infra_excluded:
        lines += [f'{len(infra_excluded)} explicitly named harness failures were replaced: '
                  'input guard or affinity setup before solving, or process cleanup after the budget. '
                  'Original audited records and all replacement outcomes remain in the JSON. '
                  'This option rejects solver crashes, invalid layouts, timeouts and no-layout outcomes.', '']
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
    parser.add_argument('--replace-build-failures', type=Path, action='append', default=[],
                        help='Explicit audited batch whose pre-solver checker-build failures have replacement attempts')
    parser.add_argument('--replace-infrastructure-failures', type=Path, action='append', default=[],
                        help='Explicit audited batch with recognized pre-solve input/affinity or post-budget cleanup faults')
    report(parser.parse_args())
