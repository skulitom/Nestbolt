"""H4 scale: frozen 2,000 letters/gears through the actual browser app.

Default workers, 60-second search, all original geometry and exports retained.
Whole browser process-tree RSS/private memory must be below 1.5e9 bytes. A 20 ms
event-loop heartbeat conservatively gates responsiveness in both browsers; when
available, Long Tasks entries must also stay <=200 ms. Missing telemetry fails.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import threading
import time
import traceback
import zipfile

import psutil
from g5_browser import serve
from h2_import_audit import source_digest
from h6_material_cost import run as checked_run, equivalent

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT/'benchmarks/datasets/browser-curves'
CLI = ROOT/'target/release/nestbolt.exe'
CPUS = [0, 2]
LIMIT = 1_500_000_000


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def guards():
    return {'product': source_digest(), 'python_runner': digest(Path(__file__)),
            'browser_runner': digest(ROOT/'web/bench/scale.mjs'),
            'fixture_manifest': digest(FIXTURE/'manifest.json'),
            'fixture': digest(FIXTURE/'letters-gears-2000.svg'), 'validator': digest(CLI),
            'built_site': {p.relative_to(ROOT/'web/dist').as_posix(): digest(p)
                           for p in sorted((ROOT/'web/dist').rglob('*')) if p.is_file()}}


def validate_export(folder):
    with zipfile.ZipFile(folder/'project.zip') as archive:
        assert archive.testzip() is None, 'ZIP CRC failure'
        project = json.loads(archive.read('project.json'))
        library, request, result = project['library'], project['request'], project['result']
        assert len(library['parts']) == 4 and sum(p['quantity'] for p in request['parts']) == 2000
        assert len(result['layout']['placements']) == 2000
        assert request['spacing_mm'] == request['edge_spacing_mm'] == 1.5
        assert all(s['width_mm'] == 1250 and s['height_mm'] == 2500 for s in request['sheets'])
        assert all(s['margins_mm'] == dict.fromkeys(['left', 'right', 'bottom', 'top'], 5)
                   and s['count'] is None and not s['defects_mm'] for s in request['sheets'])
        assert all(p['quantity'] == 500 and not p['allow_mirror']
                   and p['rotations'] == {'kind': 'list', 'degrees': [0, 90, 180, 270]}
                   for p in request['parts'])
        for sheet in result['layout']['sheets']:
            for extension in ['svg', 'dxf']:
                data = archive.read(f"sheets/{sheet['id']}.{extension}")
                assert len(data) > 100, 'Missing or empty sheet export'
        for name, value in [('library', library), ('request', request), ('layout', result['layout'])]:
            write(folder/(name+'.json'), value)
        contour_segments = [{ 'id': p['id'], 'source': p['source'],
            'outer_segments': len(p['outer']['segments']),
            'outer_curved_segments': sum(s['kind'] != 'line' for s in p['outer']['segments']),
            'proxy_vertices': len(p['polygon']['outer']), 'holes': len(p['holes'])} for p in library['parts']]
        letters = [p for p in contour_segments if '#letter-' in p['source']]
        gears = [p for p in contour_segments if '#gear-' in p['source']]
        assert len(letters) == len(gears) == 2
        assert all(p['outer_curved_segments'] > 0 for p in letters)
        # The shipped gear example represents its curved outline as a dense
        # polyline. Preserve that exact source, and record its actual complexity.
        assert all(p['proxy_vertices'] >= 500 for p in gears)
    validation = checked_run([CLI, 'validate', '--library', folder/'library.json',
        '--request', folder/'request.json', '--layout', folder/'layout.json'], folder, 'validate', 4, 180)
    assert validation['exit_code'] == 0, 'Independent native validation failed'
    checked = json.loads((folder/'validate-stdout.json').read_text(encoding='utf-8'))
    assert checked['valid']
    delta = equivalent(checked['metrics'], result['validation']['metrics'])
    return {'valid': True, 'validation': validation, 'maximum_metric_roundtrip_difference': delta,
            'sheets': len(result['layout']['sheets']), 'contours': contour_segments,
            'metrics': checked['metrics']}


def case(browser, url, out):
    folder = out/browser
    folder.mkdir()
    plan = {'browser': browser, 'url': url, 'out': str(folder), 'seconds': 60,
            'svg': str(FIXTURE/'letters-gears-2000.svg')}
    write(folder/'plan.json', plan)
    stop = threading.Event()
    samples = []
    affinity_errors = []
    started = time.perf_counter()
    command = [shutil.which('node'), str(ROOT/'web/bench/scale.mjs'), str(folder/'plan.json')]
    record = {'browser': browser, 'status': 'failed', 'command': command}
    with (folder/'stdout.log').open('wb') as stdout, (folder/'stderr.log').open('wb') as stderr:
        process = subprocess.Popen(command, cwd=ROOT/'web', stdout=stdout, stderr=stderr,
                                   creationflags=subprocess.CREATE_NO_WINDOW | 4)
        root = psutil.Process(process.pid)
        root.cpu_affinity(CPUS)
        root.resume()
        def watch():
            while not stop.is_set():
                rss = private = largest = 0
                names = []
                try:
                    children = root.children(recursive=True)
                except psutil.Error:
                    children = []
                for child in children:
                    try:
                        if child.cpu_affinity() != CPUS:
                            affinity_errors.append({'pid': child.pid, 'observed': child.cpu_affinity()})
                            child.cpu_affinity(CPUS)
                        name = child.name().lower().removesuffix('.exe')
                        if name not in ['chrome', 'chromium', 'firefox', 'headless_shell', 'chrome-headless-shell']:
                            continue
                        info = child.memory_info()
                        rss += info.rss
                        private += getattr(info, 'private', 0)
                        largest = max(largest, info.rss)
                        names.append(name)
                    except psutil.Error:
                        continue
                samples.append({'seconds': time.perf_counter()-started, 'rss': rss,
                                'private': private, 'largest': largest, 'processes': names})
                stop.wait(0.2)
        watcher = threading.Thread(target=watch, daemon=True)
        watcher.start()
        try:
            record['exit_code'] = process.wait(timeout=900)
        except subprocess.TimeoutExpired:
            record['exit_code'] = 'timeout'
            for child in reversed(root.children(recursive=True)):
                try:
                    child.kill()
                except psutil.Error:
                    pass
            process.kill()
            process.wait()
        finally:
            stop.set()
            watcher.join()
    record.update(elapsed_wall_seconds=time.perf_counter()-started,
                  peak_rss_bytes=max((s['rss'] for s in samples), default=0),
                  peak_private_bytes=max((s['private'] for s in samples), default=0),
                  samples=len(samples), affinity_errors=affinity_errors)
    write(folder/'memory.json', samples)
    if (folder/'app.json').exists():
        record['app'] = json.loads((folder/'app.json').read_text(encoding='utf-8'))
    try:
        assert record['exit_code'] == 0 and record.get('app', {}).get('status') == 'completed'
        record['independent_check'] = validate_export(folder)
        record['status'] = 'valid'
    except Exception:
        record['error'] = traceback.format_exc()
    record['passes'] = (record['status'] == 'valid' and not affinity_errors
        and record.get('app', {}).get('responsive', False)
        and 0 < record['peak_rss_bytes'] < LIMIT and 0 < record['peak_private_bytes'] < LIMIT)
    write(folder/'case.json', record)
    record['artifacts'] = {p.relative_to(folder).as_posix(): digest(p) for p in sorted(folder.iterdir()) if p.is_file()}
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', choices=['chrome', 'firefox'], action='append')
    args = parser.parse_args()
    fixture = json.loads((FIXTURE/'manifest.json').read_text(encoding='utf-8'))
    assert digest(FIXTURE/fixture['svg']) == fixture['sha256']
    for source in fixture['sources']:
        assert digest(ROOT/source['path']) == source['sha256']
    assert (ROOT/'web/dist/index.html').is_file()
    psutil.Process().cpu_affinity(list(range(16, 32)))
    name = 'h4-curve-scale-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT/'benchmarks/results'/name
    out.mkdir()
    before = guards()
    plan = {'scope': __doc__, 'baseline_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'guards': before, 'cpus': CPUS, 'memory_limit_bytes': LIMIT, 'responsiveness_limit_ms': 200,
            'memory_sample_seconds': 0.2, 'external_timeout_seconds': 900,
            'held_out_geometry_read': False, 'fixture': fixture}
    write(out/'plan.json', plan)
    for source in [Path(__file__), ROOT/'web/bench/scale.mjs']:
        (out/source.name).write_bytes(source.read_bytes())
    print(json.dumps({'folder': str(out)}), flush=True)
    server = serve(ROOT/'web/dist')
    rows = []
    try:
        for browser in args.browser or ['chrome', 'firefox']:
            row = case(browser, f'http://127.0.0.1:{server.server_address[1]}/', out)
            rows.append(row)
            write(out/'progress.json', rows)
            print(json.dumps({k: row[k] for k in ['browser', 'status', 'passes', 'peak_rss_bytes', 'peak_private_bytes']}), flush=True)
    finally:
        server.shutdown()
    assert guards() == before, 'Sources changed during measurement'
    record = {**plan, 'results': rows, 'passes': all(r['passes'] for r in rows)}
    write(out/'results.json', record)
    print(json.dumps({'folder': str(out), 'passes': record['passes']}), flush=True)


if __name__ == '__main__':
    main()
