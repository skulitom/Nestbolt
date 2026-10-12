"""Audit explicit development tables and freeze the M1 gap only at full coverage."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import median
import uuid

from comparator_batch_report import TOOLS
from comparison_session_report import summarize
from lbf_report import audit_record as audit_lbf, contained_file
from svgnest import ROOT, digest, write


SETTINGS = {'lbf': 'upstream-default', 'sparrow': 'upstream-default',
            'svgnest': 'expanded', 'deepnest': 'expanded'}
GROUP_FIELDS = ['tool', 'job', 'seconds', 'settings_role', 'settings', 'axis']


def key(row):
    return tuple(row[field] for field in GROUP_FIELDS)


def audit_table(path, plan):
    table = json.loads(path.read_bytes())
    cases = {case['id']: case for case in plan['cases'] if not case['held_out']}
    entries = {entry['slot_id']: entry for entry in table['attempts']}
    if len(entries) != len(table['attempts']):
        raise ValueError('Duplicate table attempt')
    slots, runs = [], {}
    for row in table['rows']:
        if row['required_seeds'] != plan['seeds']['development'] or len(row['slot_ids']) != 3:
            raise ValueError('Expected all three frozen development seeds')
        case = cases.get(row['job'])
        if case is None or row['seconds'] not in case['budgets_seconds']:
            raise ValueError('Unexpected job, held-out job or budget')
        source = contained_file(ROOT/'benchmarks/datasets', case['path'])
        if digest(source) != case['sha256']:
            raise ValueError('Frozen job changed')
        for seed, slot_id in zip(row['required_seeds'], row['slot_ids']):
            slots.append({field: row[field] for field in GROUP_FIELDS} | {'id': slot_id, 'seed': seed})
            if slot_id not in entries:
                continue
            entry = entries[slot_id]
            audit = audit_lbf if row['tool'] == 'lbf' else TOOLS[row['tool']][1]
            run = audit(contained_file(ROOT, entry['record']), entry['sha256'])
            if run != entry['run'] or run['status'] != entry['status']:
                raise ValueError('Embedded outcome differs from audited record')
            identity = (run.get('job', run.get('job_name')), run['seed'],
                        run.get('seconds', run.get('seconds_limit')), run['settings'],
                        run['job_sha256'])
            if identity != (row['job'], seed, row['seconds'], row['settings'], case['sha256']):
                raise ValueError('Attempt differs from table slot')
            runs[slot_id] = run
    rebuilt = summarize(slots, runs)
    if sorted(rebuilt, key=key) != sorted(table['rows'], key=key) or set(entries) != set(runs):
        raise ValueError('Table statistics differ from audited attempts')
    for field in ['replaced_checker_build_failures', 'replaced_infrastructure_failures']:
        for entry in table.get(field, []):
            audit = TOOLS[table['tool']][1]
            run = audit(contained_file(ROOT, entry['record']), entry['sha256'])
            if run != entry['run']:
                raise ValueError('Replaced infrastructure record changed')
    return rebuilt


def build_gap(plan, rows):
    """No missing group can masquerade as a failed competitor or a free win."""
    groups = {}
    for row in rows:
        group = key(row)
        if group in groups:
            raise ValueError('Duplicate group; explicitly select one audited table per group')
        groups[group] = row
    results, used = [], set()
    for case in plan['cases']:
        if case['held_out'] or case['set'] == 'S':
            continue
        for seconds in case['budgets_seconds']:
            selected, missing, outcomes = [], [], Counter()
            for tool, best in SETTINGS.items():
                if tool == 'deepnest' and case['set'] == 'M':
                    best = 'clearance-safe'
                for role, settings in [('identical_constraints', 'identical'), ('best_native_settings', best)]:
                    group = (tool, case['id'], seconds, role, settings, 'y')
                    used.add(group)
                    row = groups.get(group)
                    if (row is None or row['required_seeds'] != plan['seeds']['development']
                            or row['required'] != 3 or row['completed'] != 3
                            or row['outcomes'].get('missing', 0)):
                        missing.append({'tool': tool, 'settings': settings})
                    else:
                        selected.append(row)
                        outcomes.update(row['outcomes'])
            finite = [row for row in selected if row['comparable_median']
                      and row['comparison_statistics']['median']['state'] == 'finite']
            def best_of(baseline):
                eligible = [row for row in finite if (row['tool'] == 'lbf') == baseline]
                if not eligible:
                    return None
                row = min(eligible, key=lambda r: r['comparison_statistics']['median']['value'])
                return {'tool': row['tool'], 'settings': row['settings'],
                        'median': row['comparison_statistics']['median']['value']}
            competitor, baseline = best_of(False), best_of(True)
            state = ('incomplete' if missing else 'no_finite_competitor' if competitor is None
                     else 'no_finite_lbf' if baseline is None else 'paired')
            gap = None
            if state == 'paired':
                if competitor['median'] <= 0 or baseline['median'] <= 0:
                    raise ValueError('Material comparison requires positive scores')
                gap = 100 * (1 - competitor['median'] / baseline['median'])
            results.append({'job': case['id'], 'dataset': case['set'], 'seconds': seconds,
                            'state': state, 'missing_groups': missing, 'outcomes': dict(outcomes),
                            'competitor': competitor, 'lbf': baseline, 'gap_percent': gap,
                            'groups': selected})
    # Strip tables are useful supporting evidence, but cannot enlarge the gap
    # population. Other unrequested groups indicate a configuration mistake.
    strips = {case['id'] for case in plan['cases'] if case['set'] == 'S' and not case['held_out']}
    if any(group not in used and group[1] not in strips for group in groups):
        raise ValueError('Unexpected group outside the frozen sheet/maker populations')
    budgets = []
    for seconds in [60, 300]:
        population = [row for row in results if row['seconds'] == seconds]
        states = Counter(row['state'] for row in population)
        gaps = [row['gap_percent'] for row in population if row['state'] == 'paired']
        complete = bool(population) and not states['incomplete']
        budgets.append({'seconds': seconds, 'jobs': len(population), 'states': dict(states),
                        'complete': complete, 'paired_jobs': len(gaps),
                        'gap_percent': median(gaps) if complete and gaps else None})
    complete = all(b['complete'] and b['paired_jobs'] for b in budgets)
    target = max(5.0, 0.5 * max(0.0, *(b['gap_percent'] for b in budgets))) if complete else None
    return {'complete': complete, 'target_percent': target, 'budgets': budgets, 'rows': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--table', type=Path, action='append', required=True)
    parser.add_argument('--allow-incomplete', action='store_true', help='Write coverage only; never freeze a partial target')
    args = parser.parse_args()
    plan_path = ROOT/'benchmarks/matrix-plan.json'
    plan = json.loads(plan_path.read_bytes())
    paths = [contained_file(ROOT, str(path)) for path in args.table]
    if len(set(paths)) != len(paths):
        raise ValueError('Duplicate table path')
    rows = [row for path in paths for row in audit_table(path, plan)]
    result = build_gap(plan, rows)
    if not result['complete'] and not args.allow_incomplete:
        raise ValueError('Incomplete M1 comparison; no target frozen')
    stamp = datetime.now(timezone.utc)
    stem = f'baseline-gap-{stamp:%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}'
    result.update(recorded_at=stamp.isoformat(),
                  scope='Audited development comparison. No held-out jobs, final seeds or Nestbolt scores enter the M1 target.',
                  sources={str(p.relative_to(ROOT).as_posix()): digest(p) for p in
                           [Path(__file__).resolve(), ROOT/'scripts/comparison_session_report.py',
                            *[ROOT/f'scripts/{name}_report.py' for name in ['lbf', 'deepnest', 'svgnest', 'sparrow']],
                            ROOT/'benchmarks/STATISTICS.md', plan_path]},
                  tables=[{'path': p.relative_to(ROOT).as_posix(), 'sha256': digest(p)} for p in paths])
    target = ROOT/'benchmarks/results'/stem
    write(target.with_suffix('.json'), result)
    lines = ['# M1 baseline gap', '', result['scope'], '',
             f"Frozen quality target: {result['target_percent']:.8f}%." if result['complete']
             else 'Incomplete coverage: no quality target is frozen.', '',
             '| Budget | Jobs | Paired | Missing | No finite competitor | No finite LBF | Median gap |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for b in result['budgets']:
        states = b['states']
        gap = 'incomplete' if b['gap_percent'] is None else f"{b['gap_percent']:.8f}%"
        lines.append(f"| {b['seconds']} s | {b['jobs']} | {b['paired_jobs']} | {states.get('incomplete', 0)} | "
                     f"{states.get('no_finite_competitor', 0)} | {states.get('no_finite_lbf', 0)} | {gap} |")
    lines += ['', 'Each job has equal weight within its budget. Failed medians remain explicit; '
              'no competitor result earns a free win. Target = max(5, half the larger nonnegative budget gap).', '',
              '| Job | Budget | State | Competitor median | LBF median | Gap |',
              '| --- | ---: | --- | ---: | ---: | ---: |']
    for row in result['rows']:
        def score(value):
            return '—' if value is None else f"{value['median']:.8f}"
        gap = '—' if row['gap_percent'] is None else f"{row['gap_percent']:.8f}%"
        lines.append(f"| {row['job']} | {row['seconds']} | {row['state']} | {score(row['competitor'])} | {score(row['lbf'])} | {gap} |")
    lines += ['', f'[Full precision, every tool outcome and source evidence]({stem}.json).', '']
    with target.with_suffix('.md').open('x', encoding='utf-8', newline='\n') as out:
        out.write('\n'.join(lines))
    print(target.with_suffix('.md'))


if __name__ == '__main__':
    main()
