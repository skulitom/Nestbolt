"""G8 results page: every number behind the comparison, with tool versions, seeds
and hardware, as web/public/results/index.html and results.json (deployed with
the browser app to GitHub Pages).

Development phase (default): Nestbolt's development matrix records against the
frozen M1 competitor medians (three seeds each, held-out jobs excluded). The
page says so on every view; the final acceptance run (seeds 1000-1004 with the
held-out jobs) replaces it once it exists. Each competitor's per-job value is
the better of its two settings roles, as the gate uses; per-tool comparisons
are shown next to the best-of-tools comparison. Missing or failed competitor
results never count as wins.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import html
import json
from pathlib import Path
import platform
import statistics
import subprocess

import psutil

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT/'benchmarks/results/baseline-gap-20261012T033547Z-e9539412.json'
# G2 median target: the plan's base 5%. The M1 raise to 10.77231473513936% (half the
# measured gap) was waived by Artem on 2026-10-12 (docs/PLAN.md, decision 4).
TARGET = 5.0
RAISED_TARGET = 10.77231473513936
TIE = 1e-6
TOOLS = ['deepnest', 'svgnest', 'sparrow']
NAMES = {'deepnest': 'Deepnest', 'svgnest': 'SVGnest', 'sparrow': 'Sparrow', 'nestbolt': 'Nestbolt', 'lbf': 'jagua-rs LBF'}
REPO = 'https://github.com/skulitom/Nestbolt/blob/main/'


def quartiles(values):
    if len(values) == 1:
        return values[0], values[0], values[0]
    q = statistics.quantiles(values, n=4, method='inclusive')
    return q[0], statistics.median(values), q[2]


def hardware():
    cpu = platform.processor()
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DESCRIPTION\System\CentralProcessor\0')
        cpu = winreg.QueryValueEx(key, 'ProcessorNameString')[0].strip()
    except (ImportError, OSError):
        pass
    return {'cpu': cpu, 'physical_cores': psutil.cpu_count(False), 'logical_cpus': psutil.cpu_count(),
            'memory_gib': round(psutil.virtual_memory().total / 2**30), 'os': platform.platform()}


def tool_versions():
    out = []
    for tool, path in [('deepnest', 'benchmarks/deepnest/tool.json'), ('svgnest', 'benchmarks/svgnest/tool.json'),
                       ('lbf', 'benchmarks/lbf/tool.json')]:
        t = json.loads((ROOT/path).read_text(encoding='utf-8'))
        out.append({'tool': tool, 'name': t.get('tool') or t.get('name'), 'repository': t['repository'],
                    'revision': t['revision'], 'settings': sorted(t.get('settings', {})), 'config': path})
    cargo = (ROOT/'benchmarks/sparrow-benchmark/Cargo.toml').read_text(encoding='utf-8')
    rev = cargo.split('sparrow.git", rev = "')[1].split('"')[0]
    out.append({'tool': 'sparrow', 'name': 'sparrow (CLI)', 'repository': 'https://github.com/JeroenGar/sparrow',
                'revision': rev, 'settings': ['identical', 'upstream-default'],
                'config': 'benchmarks/sparrow-benchmark/Cargo.toml'})
    return out


def nestbolt_runs(paths):
    """Per job: material of each seed (None when a seed failed), and the records used."""
    runs, records = {}, []
    for path in paths:
        record = json.loads(path.read_text(encoding='utf-8'))
        records.append({'path': path.relative_to(ROOT).as_posix(), 'seed': record['seed'],
                        'seconds': record['seconds'], 'binary_sha256': record['binary_sha256']})
        for row in record['rows']:
            runs.setdefault(row['job'], {})[record['seed']] = row['material'] if row['status'] == 'valid' else None
    return runs, records


def ranked(values):
    """Median and quartiles with failures (None) ranked after every score (STATISTICS.md)."""
    order = sorted(values, key=lambda v: (v is None, v or 0.0))
    n = len(order)
    pick = lambda q: order[min(n - 1, max(0, round(q * (n - 1))))]
    return pick(0.25), pick(0.5), pick(0.75)


def final_competitors(seconds):
    """From the audited final-phase batches: per job and tool, the better settings role
    whose median over all five seeds is finite."""
    from comparator_batch_report import audit_batch
    from reproduce import BATCHES, excluded
    seeds, skip = {}, excluded()
    for tool in TOOLS:
        for path in sorted(ROOT.glob(f"{BATCHES[tool]}/*/batch.json")):
            if path.parent.name in skip:
                continue
            batch = json.loads(path.read_text(encoding='utf-8'))
            if batch.get('phase') != 'final' or batch['seconds'] != seconds or not batch.get('complete'):
                continue
            _, rows = audit_batch(path, tool)
            for row in rows:
                run = row['run']
                key = (row['job'], tool, batch['settings'])
                seeds.setdefault(key, {})[batch['seed']] = run['score'] if run['status'] == 'valid' else None
    out = {}
    for (job, tool, settings), by_seed in seeds.items():
        if sorted(by_seed) != [1000, 1001, 1002, 1003, 1004]:
            continue  # incomplete: no comparison, never a win
        q1, median, q3 = ranked(list(by_seed.values()))
        if median is None:
            continue
        entry = {'settings': settings, 'median': median, 'q1': q1, 'q3': q3, 'seeds': sorted(by_seed),
                 'by_seed': by_seed}
        tools = out.setdefault(job, {})
        if tool not in tools or median < tools[tool]['median']:
            tools[tool] = entry
    return out


def competitors(seconds, phase='development'):
    """Per job and tool: the better finite settings-role median, with its quartiles."""
    if phase == 'final':
        return final_competitors(seconds)
    rows = json.loads(BASELINE.read_text(encoding='utf-8'))['rows']
    out = {}
    for row in rows:
        if row['seconds'] != seconds:
            continue
        tools = {}
        for g in row['groups']:
            stats = g['comparison_statistics']
            if stats['median']['state'] != 'finite':
                continue
            entry = {'settings': g['settings'], 'role': g['settings_role'], 'median': stats['median']['value'],
                     'q1': stats['quartiles'][0]['value'], 'q3': stats['quartiles'][2]['value'],
                     'seeds': g['required_seeds']}
            if g['tool'] not in tools or entry['median'] < tools[g['tool']]['median']:
                tools[g['tool']] = entry
        out[row['job']] = tools
    return out


def compare(ours, theirs):
    if ours is None or theirs is None:
        return None
    if abs(ours - theirs) <= TIE * theirs:
        outcome = 'tie'
    else:
        outcome = 'win' if ours < theirs else 'loss'
    return {'reduction_percent': 100 * (1 - ours / theirs), 'outcome': outcome}


def summarise(comparisons):
    c = [x for x in comparisons if x]
    if not c:
        return None
    reductions = [x['reduction_percent'] for x in c]
    return {'jobs': len(c), 'median_reduction_percent': statistics.median(reductions),
            'wins_or_ties': sum(x['outcome'] != 'loss' for x in c),
            'worse_than_one_percent': sum(x['reduction_percent'] < -1 for x in c),
            'worst_percent': min(reductions)}


def budget_table(seconds, paths, phase='development'):
    runs, records = nestbolt_runs(paths)
    rivals = competitors(seconds, phase)
    rows = []
    for job in sorted(runs):
        seeds = runs[job]
        values = [v for v in seeds.values() if v is not None]
        failed = len(values) != len(seeds)
        q1, median, q3 = quartiles(values) if values and not failed else (None, None, None)
        tools = rivals.get(job, {})
        best = min(((t, v) for t, v in tools.items() if t in TOOLS), key=lambda tv: tv[1]['median'], default=None)
        rows.append({'job': job, 'nestbolt': {'median': median, 'q1': q1, 'q3': q3, 'seeds': seeds,
                                              'all_valid': not failed},
                     'tools': tools, 'best': {'tool': best[0], **best[1]} if best else None,
                     'vs_best': compare(median, best[1]['median']) if best else None,
                     'vs_tool': {t: compare(median, tools[t]['median']) if t in tools else None for t in TOOLS}})
    summary = {'best_of_tools': summarise([r['vs_best'] for r in rows]),
               'per_tool': {t: summarise([r['vs_tool'][t] for r in rows]) for t in TOOLS},
               'jobs': len(rows), 'jobs_without_competitor': sum(r['best'] is None for r in rows),
               'nestbolt_valid_runs': sum(v is not None for r in rows for v in r['nestbolt']['seeds'].values()),
               'nestbolt_runs': sum(len(r['nestbolt']['seeds']) for r in rows)}
    s = summary['best_of_tools']
    summary['g2_pass'] = bool(s and s['median_reduction_percent'] >= TARGET
                              and s['wins_or_ties'] >= 0.9 * s['jobs'] and s['worse_than_one_percent'] == 0)
    return {'seconds': seconds, 'records': records, 'summary': summary, 'rows': rows}


def strip_parity(phase):
    """G3: Nestbolt's strip adapter against Sparrow on set S, per-job medians over the
    phase's seeds (failures ranked last); the reference is Sparrow's better setting."""
    from comparator_batch_report import audit_batch
    from dataset_selection import PHASE_SEEDS
    from reproduce import BATCHES, excluded
    seeds, skip = PHASE_SEEDS[phase], excluded()
    ours, records = {}, []
    for path in sorted(ROOT.glob('benchmarks/results/strip-native-*.json')):
        record = json.loads(path.read_text(encoding='utf-8'))
        if record.get('phase', 'development') != phase:
            continue
        records.append({'path': path.relative_to(ROOT).as_posix(), 'binary_sha256': record['binary_sha256']})
        for row in record['rows']:
            if row['seed'] in seeds and row['seconds'] == 60:
                ours.setdefault(row['job'], {})[row['seed']] = (
                    row['result']['strip_length'] if row['status'] == 'valid' else None)
    theirs = {}
    for path in sorted(ROOT.glob(f"{BATCHES['sparrow']}/*/batch.json")):
        if path.parent.name in skip:
            continue
        batch = json.loads(path.read_text(encoding='utf-8'))
        if (batch.get('phase', 'development') != phase or batch['dataset'] != 'S' or batch['seconds'] != 60
                or not batch.get('complete') or batch['seed'] not in seeds):
            continue
        for row in audit_batch(path, 'sparrow')[1]:
            run = row['run']
            theirs.setdefault((row['job'], batch['settings']), {})[batch['seed']] = (
                run['score'] if run['status'] == 'valid' else None)
    rows = []
    for job in sorted(ours):
        mine = ours[job]
        if sorted(mine) != seeds:
            continue
        median = ranked(list(mine.values()))[1]
        refs = [(settings, ranked(list(v.values()))[1]) for (j, settings), v in theirs.items()
                if j == job and sorted(v) == seeds]
        refs = [(k, v) for k, v in refs if v is not None]
        best = min(refs, key=lambda kv: kv[1], default=None)
        rows.append({'job': job, 'nestbolt': median, 'seeds': mine,
                     'sparrow': best[1] if best else None, 'settings': best[0] if best else None,
                     'regression_percent': 100 * (median / best[1] - 1) if best and median else None})
    deltas = [r['regression_percent'] for r in rows if r['regression_percent'] is not None]
    summary = {'jobs': len(rows), 'compared': len(deltas),
               'median_regression_percent': statistics.median(deltas) if deltas else None,
               'worst_regression_percent': max(deltas) if deltas else None}
    summary['g3_pass'] = (bool(deltas) and len(deltas) == len(rows) == 13
                          and summary['median_regression_percent'] <= 1.0
                          and summary['worst_regression_percent'] <= 2.0)
    return {'records': records, 'summary': summary, 'rows': rows}


def speed(paths, phase):
    """G4: Nestbolt at 30 s against the best competitor's 300 s median, per job."""
    runs, records = nestbolt_runs(paths)
    rivals = competitors(300, phase)
    rows = []
    for job, seeds in sorted(runs.items()):
        best = min(((t, v) for t, v in rivals.get(job, {}).items() if t in TOOLS),
                   key=lambda tv: tv[1]['median'], default=None)
        if not best:
            continue
        median = ranked(list(seeds.values()))[1]
        rows.append({'job': job, 'nestbolt_30s': median, 'best_300s': best[1]['median'], 'tool': best[0],
                     'reached': median is not None and median <= best[1]['median'] * (1 + TIE)})
    reached = sum(r['reached'] for r in rows)
    return {'records': records, 'rows': rows,
            'summary': {'jobs': len(rows), 'reached': reached,
                        'g4_pass': bool(rows) and reached >= 0.8 * len(rows)}}


def gate_sections(data):
    e = html.escape
    out = []
    if data.get('strip'):
        g = data['strip']
        sm = g['summary']
        verdict = 'pass' if sm['g3_pass'] else 'not met'
        out.append(f"<h2>Strip parity (G3)</h2><p>Nestbolt's strip adapter against the Sparrow CLI on the {sm['jobs']} "
                   f"strip jobs at 60 s: median regression {fmt(sm['median_regression_percent'], 3)}%, worst "
                   f"{fmt(sm['worst_regression_percent'], 3)}% (pass: median at most 1%, never more than 2%): "
                   f"<strong>{verdict}</strong>.</p>")
        out.append('<div class="table"><table><tr><th>Job</th><th>Nestbolt length</th><th>Sparrow length</th>'
                   '<th>Regression</th></tr>')
        for r in g['rows']:
            out.append(f"<tr><td>{e(r['job'])}</td><td>{fmt(r['nestbolt'])}</td><td>{fmt(r['sparrow'])}</td>"
                       f"<td>{fmt(r['regression_percent'], 3)}%</td></tr>")
        out.append('</table></div>')
    if data.get('speed'):
        g = data['speed']
        sm = g['summary']
        verdict = 'pass' if sm['g4_pass'] else 'not met'
        out.append(f"<h2>Speed (G4)</h2><p>Nestbolt at 30 s reaches the best competitor's 300 s median on "
                   f"{sm['reached']} of {sm['jobs']} jobs (pass: at least 80%): <strong>{verdict}</strong>.</p>")
        out.append('<div class="table"><table><tr><th>Job</th><th>Nestbolt 30 s</th><th>Best 300 s</th>'
                   '<th>Tool</th><th>Reached</th></tr>')
        for r in g['rows']:
            out.append(f"<tr><td>{e(r['job'])}</td><td>{fmt(r['nestbolt_30s'])}</td><td>{fmt(r['best_300s'])}</td>"
                       f"<td>{NAMES[r['tool']]}</td><td>{'yes' if r['reached'] else 'no'}</td></tr>")
        out.append('</table></div>')
    return '\n'.join(out)


def chart(rows):
    """Horizontal bars of reduction vs the best competitor, sorted, with 0 and target lines."""
    data = sorted(((r['vs_best']['reduction_percent'], r['job']) for r in rows if r['vs_best']), reverse=True)
    if not data:
        return ''
    lo, hi = min(-5.0, min(d for d, _ in data) - 1), max(TARGET + 5, max(d for d, _ in data) + 2)
    left, width, bar = 210, 560, 14
    height = 30 + bar * len(data)
    x = lambda v: left + (v - lo) / (hi - lo) * width
    parts = [f'<svg viewBox="0 0 {left + width + 60} {height}" role="img" aria-label="Material reduction per job" class="chart">']
    for v in range(int(lo // 5 * 5), int(hi) + 1, 5):
        parts.append(f'<line x1="{x(v):.1f}" y1="18" x2="{x(v):.1f}" y2="{height}" class="grid"/>'
                     f'<text x="{x(v):.1f}" y="12" class="tick">{v}%</text>')
    for i, (d, job) in enumerate(data):
        y = 22 + i * bar
        x0, x1 = sorted([x(0), x(d)])
        cls = 'pass' if d >= TARGET else ('win' if d > 0 else 'loss')
        parts.append(f'<text x="{left - 6}" y="{y + 10}" class="label">{html.escape(job)}</text>'
                     f'<rect x="{x0:.1f}" y="{y + 1}" width="{max(x1 - x0, 0.8):.1f}" height="{bar - 3}" class="{cls}">'
                     f'<title>{html.escape(job)}: {d:.2f}%</title></rect>')
    parts.append(f'<line x1="{x(0):.1f}" y1="18" x2="{x(0):.1f}" y2="{height}" class="zero"/>'
                 f'<line x1="{x(TARGET):.1f}" y1="18" x2="{x(TARGET):.1f}" y2="{height}" class="target"/>'
                 f'<text x="{x(TARGET) + 4:.1f}" y="{height - 4}" class="tick target-label">G2 target {TARGET:.2f}%</text></svg>')
    return ''.join(parts)


def fmt(v, digits=4):
    return '—' if v is None else f'{v:.{digits}f}'


def page(data):
    e = html.escape
    hw, phase = data['hardware'], data['phase']
    banner = ('Development results: three seeds per job, held-out jobs excluded. These are not the final '
              'acceptance run, which uses fresh seeds 1000-1004 and adds ten held-out jobs.'
              if phase == 'development' else 'Final acceptance run: seeds 1000-1004, held-out jobs included.')
    out = [f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nestbolt results</title><meta name="description" content="Every number behind Nestbolt's comparison with Deepnest, SVGnest and Sparrow.">
<style>
:root{{--bg:#f6f5f1;--panel:#fff;--text:#1d2228;--muted:#5d6670;--line:#d9d6cd;--accent:#2f6db5;--good:#3d8b4f;--bad:#b3261e;--pass:#1f6f8b}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#15181c;--panel:#1e2227;--text:#e6e8eb;--muted:#9aa3ad;--line:#343a42;--accent:#7fb0ec;--good:#7cc58a;--bad:#f2b8b5;--pass:#6fc3df}}}}
:root[data-theme=dark]{{--bg:#15181c;--panel:#1e2227;--text:#e6e8eb;--muted:#9aa3ad;--line:#343a42;--accent:#7fb0ec;--good:#7cc58a;--bad:#f2b8b5;--pass:#6fc3df}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:16px}}h1{{font-size:24px;margin:8px 0}}h2{{font-size:18px;margin:24px 0 8px}}
a{{color:var(--accent)}}.banner{{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);padding:10px 14px;border-radius:6px}}
.table{{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:6px}}table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{padding:4px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}}th:first-child,td:first-child{{text-align:left}}
th{{color:var(--muted);font-weight:600}}.win{{fill:var(--good);color:var(--good)}}.loss{{fill:var(--bad);color:var(--bad)}}.pass{{fill:var(--pass);color:var(--pass)}}
.chart{{width:100%;height:auto;background:var(--panel);border:1px solid var(--line);border-radius:6px}}.chart .label,.chart .tick{{font-size:10px;fill:var(--muted)}}
.chart .label{{text-anchor:end}}.chart .tick{{text-anchor:middle}}.chart .grid{{stroke:var(--line)}}.chart .zero{{stroke:var(--text)}}.chart .target{{stroke:var(--pass);stroke-dasharray:4 3}}
.chart .target-label{{text-anchor:start;fill:var(--pass)}}.muted{{color:var(--muted)}}dl{{display:grid;grid-template-columns:max-content 1fr;gap:2px 16px}}dt{{color:var(--muted)}}dd{{margin:0}}
</style></head><body><main>
<h1>Nestbolt results</h1><p class="banner">{e(banner)}</p>
<p>Material used = (sheets − 1) + used length of the last sheet ÷ its length, from an independent Clipper2 validator; lower is better.
Each tool runs single-threaded at equal wall-clock budgets on the same PC, at most eight runs at once. A competitor's value per job is the
better of its two settings (identical constraints, its own best settings); jobs where no competitor produced a valid layout earn no wins.
G2 passes when the median reduction against the best competitor is at least {TARGET:.2f}%, Nestbolt wins or ties at least 90% of jobs and is
never more than 1% worse (<a href="{REPO}docs/PLAN.md">plan</a>, section 6; the earlier raise to {RAISED_TARGET:.2f}% was
waived on 2026-10-12, decision 4).</p>
<dl><dt>Generated</dt><dd>{e(data['generated_at'])} from commit <code>{e(data['commit'][:10])}</code></dd>
<dt>Hardware</dt><dd>{e(hw['cpu'])}, {hw['physical_cores']} cores / {hw['logical_cpus']} threads, {hw['memory_gib']} GiB, {e(hw['os'])}; runs pinned one per physical core of the first CCD</dd>
<dt>Seeds</dt><dd>{e(', '.join(map(str, data['seeds'])))} for every tool</dd></dl>
<h2>Tools</h2><div class="table"><table><tr><th>Tool</th><th>Revision</th><th>Settings</th><th>Configuration</th></tr>''']
    for t in data['tools']:
        out.append(f'<tr><td><a href="{e(t["repository"])}">{e(t["name"])}</a></td><td><code>{e(t["revision"][:12])}</code></td>'
                   f'<td>{e(", ".join(t["settings"]))}</td><td><a href="{REPO}{e(t["config"])}">{e(t["config"])}</a></td></tr>')
    nb = {r['binary_sha256'][:8] for b in data['budgets'] for r in b['records']}
    out.append(f'<tr><td>Nestbolt</td><td><code>{e(data["commit"][:12])}</code></td><td>defaults</td><td>binaries {e(", ".join(sorted(nb)))}</td></tr></table></div>')
    for b in data['budgets']:
        s, best = b['summary'], b['summary']['best_of_tools']
        out.append(f'<h2>{b["seconds"]} s budget</h2>')
        if best:
            verdict = 'meets' if s['g2_pass'] else 'does not meet'
            out.append(f'<p><strong>{best["median_reduction_percent"]:.2f}%</strong> less material than the best competitor at the median over '
                       f'{best["jobs"]} jobs; wins or ties on {best["wins_or_ties"]} ({100 * best["wins_or_ties"] / best["jobs"]:.1f}%); '
                       f'{best["worse_than_one_percent"]} more than 1% worse (worst {best["worst_percent"]:.2f}%). This {verdict} the G2 target. '
                       f'{s["jobs_without_competitor"]} of {s["jobs"]} jobs have no valid competitor result. Nestbolt layouts valid: '
                       f'{s["nestbolt_valid_runs"]}/{s["nestbolt_runs"]}.</p>')
        out.append('<div class="table"><table><tr><th>Against</th><th>Jobs</th><th>Median reduction</th><th>Wins or ties</th><th>More than 1% worse</th></tr>')
        for name, v in [('Best of all three', best)] + [(NAMES[t], s['per_tool'][t]) for t in TOOLS]:
            if v:
                out.append(f'<tr><td>{e(name)}</td><td>{v["jobs"]}</td><td>{v["median_reduction_percent"]:.2f}%</td>'
                           f'<td>{v["wins_or_ties"]}</td><td>{v["worse_than_one_percent"]}</td></tr>')
        out.append('</table></div>' + chart(b['rows']))
        out.append('<div class="table"><table><tr><th>Job</th><th>Nestbolt median [IQR]</th>'
                   + ''.join(f'<th>{NAMES[t]}</th>' for t in TOOLS) + '<th>Best</th><th>Reduction</th></tr>')
        for r in b['rows']:
            n = r['nestbolt']
            cells = ''.join(f'<td title="{e(r["tools"][t]["settings"])}">{fmt(r["tools"][t]["median"])}</td>' if t in r['tools']
                            else '<td class="muted">—</td>' for t in TOOLS)
            red = r['vs_best']
            red_cell = (f'<td class="{red["outcome"] if red["reduction_percent"] < TARGET else "pass"}">{red["reduction_percent"]:.2f}%</td>'
                        if red else '<td class="muted">no competitor</td>')
            seeds = ', '.join(f'{k}: {fmt(v)}' for k, v in sorted(n['seeds'].items()))
            out.append(f'<tr><td>{e(r["job"])}</td><td title="seeds {e(seeds)}">{fmt(n["median"])} [{fmt(n["q1"])}–{fmt(n["q3"])}]</td>'
                       f'{cells}<td>{e(NAMES[r["best"]["tool"]]) if r["best"] else "—"}</td>{red_cell}</tr>')
        out.append('</table></div><p class="muted">Records: '
                   + ', '.join(f'<a href="{REPO}{e(x["path"].replace(".json", ".md"))}">seed {x["seed"]}</a>' for x in b['records'])
                   + f'; competitor medians: <a href="{REPO}{e(BASELINE.relative_to(ROOT).as_posix().replace(".json", ".md"))}">M1 audit</a>. '
                   'Hover a value for its settings or per-seed results.</p>')
    out.append(gate_sections(data))
    out.append(f'''<h2>All gates</h2><p>Gate-by-gate evidence, including every failed and superseded run, is in
<a href="{REPO}docs/STATUS.md">STATUS.md</a> and <a href="{REPO}BENCHMARKS.md">BENCHMARKS.md</a>. All numbers on this page are in
<a href="results.json">results.json</a>; rebuild it with <code>python scripts/results_page.py</code>.</p>
<p class="muted"><a href="../">Back to the Nestbolt app</a></p></main></body></html>''')
    return '\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--nestbolt-60', type=Path, nargs='+', required=True, help='sheets_batch records, one per seed')
    parser.add_argument('--nestbolt-300', type=Path, nargs='*', default=[])
    parser.add_argument('--out', type=Path, default=ROOT/'web/public/results')
    parser.add_argument('--phase', choices=['development', 'final'], default='development')
    parser.add_argument('--nestbolt-30', type=Path, nargs='*', default=[], help='30 s records on the long subset (G4)')
    parser.add_argument('--strip', action='store_true', help='include G3 strip parity from the phase records')
    args = parser.parse_args()
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    budgets = [budget_table(60, [p.resolve() for p in args.nestbolt_60], args.phase)]
    if args.nestbolt_300:
        budgets.append(budget_table(300, [p.resolve() for p in args.nestbolt_300], args.phase))
    data = {'phase': args.phase, 'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),
            'commit': commit, 'hardware': hardware(), 'tools': tool_versions(), 'target_percent': TARGET,
            'seeds': sorted({r['seed'] for b in budgets for r in b['records']}),
            'baseline': {'path': BASELINE.relative_to(ROOT).as_posix(), 'sha256': sha256(BASELINE.read_bytes()).hexdigest()},
            'budgets': budgets}
    if args.nestbolt_30:
        data['speed'] = speed([p.resolve() for p in args.nestbolt_30], args.phase)
    if args.strip:
        data['strip'] = strip_parity(args.phase)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out/'results.json').write_text(json.dumps(data, indent=1) + '\n', encoding='utf-8', newline='\n')
    (args.out/'index.html').write_text(page(data), encoding='utf-8', newline='\n')
    for b in budgets:
        print(b['seconds'], json.dumps(b['summary']['best_of_tools']), 'G2', b['summary']['g2_pass'])
    print(args.out/'index.html')


if __name__ == '__main__':
    main()
