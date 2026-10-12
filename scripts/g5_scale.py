"""G5 scale: a 2,000-part job imports, solves and exports in the browser app with
memory under 1.5 GB.

The parts are the four drawings of the development job m-mechanical-batch-1000
(`parts.svg`), imported through the app's file input at 500 copies each, nested
on 1250 x 2500 mm sheets with 1.5 mm spacing for 60 s with the app's default
workers, then every sheet exported to the SVG/DXF ZIP. `web/tests/scale.spec.ts`
drives the app; this script samples the memory of every browser process
(working set, summed over the whole process tree, so shared pages count more
than once) every 0.2 s from outside the browser and writes the report.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import uuid

import psutil

ROOT = Path(__file__).resolve().parents[1]
SVG = ROOT/'benchmarks/datasets/maker-assets/m-mechanical-batch-1000/parts.svg'
LIMIT = 1.5e9
BROWSER = ('chrome', 'firefox', 'headless_shell', 'chrome-headless-shell')


def browser_processes(root):
    try:
        return [p for p in root.children(recursive=True) if p.name().lower().removesuffix('.exe') in BROWSER]
    except psutil.Error:
        return []


def run(project, seconds, out_dir):
    out = out_dir/f'{project}.json'
    env = {**os.environ, 'SCALE_SVG': str(SVG), 'SCALE_SECONDS': str(seconds), 'SCALE_OUT': str(out)}
    if project == 'chrome':
        env['PW_CHROME'] = '1'
    process = subprocess.Popen(['npx', 'playwright', 'test', 'tests/scale.spec.ts', f'--project={project}'],
                               cwd=ROOT/'web', env=env, shell=sys.platform == 'win32')
    root, peak, samples, stop = psutil.Process(process.pid), {'rss': 0, 'private': 0, 'largest_process': 0}, [], threading.Event()

    def watch():
        while not stop.is_set():
            rss = private = largest = 0
            for p in browser_processes(root):
                try:
                    info = p.memory_info()
                except psutil.Error:
                    continue
                rss += info.rss
                private += getattr(info, 'private', 0)
                largest = max(largest, info.rss)
            peak['rss'] = max(peak['rss'], rss)
            peak['private'] = max(peak['private'], private)
            peak['largest_process'] = max(peak['largest_process'], largest)
            samples.append(rss)
            stop.wait(0.2)
    watcher = threading.Thread(target=watch, daemon=True)
    watcher.start()
    code = process.wait()
    stop.set()
    watcher.join()
    report = json.loads(out.read_text(encoding='utf-8')) if out.exists() else {}
    return {'project': project, 'exit_code': code, 'app': report, 'peak_rss_bytes': peak['rss'],
            'peak_private_bytes': peak['private'], 'peak_largest_process_rss_bytes': peak['largest_process'],
            'samples': len(samples),
            'passes': code == 0 and bool(report) and peak['rss'] < LIMIT and peak['private'] < LIMIT}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', action='append', choices=['chrome', 'chromium', 'firefox'])
    parser.add_argument('--seconds', type=float, default=60)
    args = parser.parse_args()
    projects = args.project or ['chrome', 'firefox']
    if not (ROOT/'web/dist/index.html').exists():
        parser.error('build the site first: python scripts/build_web.py')
    started = datetime.now(timezone.utc)
    stamp = started.strftime('%Y%m%dT%H%M%SZ')
    out_dir = ROOT/'output/g5-scale'/f'{stamp}-{uuid.uuid4().hex[:8]}'
    out_dir.mkdir(parents=True)
    results = [run(p, args.seconds, out_dir) for p in projects]
    name = f'g5-scale-{stamp}-{uuid.uuid4().hex[:8]}'
    record = {'scope': 'G5 scale: 2,000 parts through the browser app (import, nest, export), memory under 1.5 GB.',
              'recorded_at': datetime.now(timezone.utc).isoformat(), 'svg': SVG.relative_to(ROOT).as_posix(),
              'copies_per_part': 500, 'seconds': args.seconds, 'limit_bytes': LIMIT, 'results': results}
    target = ROOT/'benchmarks/results'
    (target/f'{name}.json').write_text(json.dumps(record, indent=1) + '\n', encoding='utf-8', newline='\n')
    gb = lambda b: f'{b / 1e9:.2f} GB'
    lines = ['# G5 scale: 2,000 parts in the browser', '',
             f'`{SVG.relative_to(ROOT).as_posix()}` (four parts of the development job m-mechanical-batch-1000) '
             'imported through the app at 500 copies each, nested on 1250 × 2500 mm sheets with 1.5 mm spacing for '
             f'{args.seconds:g} s with the default workers, and every sheet exported to the SVG/DXF ZIP. Memory is the '
             'peak over all browser processes, sampled every 0.2 s from outside the browser. Limit 1.5 GB.', '',
             '| Browser | Result | Import | Nest | Export | Longest task while solving | Peak working set | Peak private | Largest process | Pass |',
             '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    for r in results:
        a = r['app']
        lines.append(f"| {r['project']} | {a.get('summary', 'failed').replace(chr(10), ' ')} | "
                     f"{a.get('import_seconds', float('nan')):.1f} s | {a.get('nest_seconds', float('nan')):.1f} s | "
                     f"{a.get('export_seconds', float('nan')):.1f} s | {a.get('longest_task_while_solving_ms', float('nan')):.0f} ms | "
                     f"{gb(r['peak_rss_bytes'])} | {gb(r['peak_private_bytes'])} | {gb(r['peak_largest_process_rss_bytes'])} | "
                     f"{'yes' if r['passes'] else 'no'} |")
    lines += ['', f'[Full record]({name}.json)', '']
    (target/f'{name}.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print(target/f'{name}.md')
    return 0 if all(r['passes'] for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
