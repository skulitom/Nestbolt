"""Bounded phase diagnostics for one frozen training vector fidelity case."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import time

import psutil

from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', required=True)
    parser.add_argument('--timeout', type=int, default=90)
    args = parser.parse_args()
    assert 10 <= args.timeout <= 360
    raw = (CORPUS/'manifest.json').read_bytes()
    training = [r for r in json.loads(raw)['files'] if r['split'] == 'training']
    selected = [r for r in training if args.only in r['path']]
    assert len(selected) == 1, 'Select exactly one training input'
    row = selected[0]
    assert Path(row['path']).suffix.lower() in ['.svg', '.dxf']
    assert sha256((CORPUS/row['path']).read_bytes()).hexdigest() == row['sha256']
    label_bytes = (CORPUS/row['label']).read_bytes()
    assert sha256(label_bytes).hexdigest() == row['label_sha256']
    options = dict(json.loads(label_bytes).get('import_options', {}))
    units = options.pop('units', None)
    assert units in [None, 'mm', 'in']
    if units == 'in':
        options['dxf_unit'] = 25.4
    for key in ['layers', 'colors']:
        if key in options:
            options[key] = list(map(str, options[key]))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT/'output'/f'h2-dense-profile-{stamp}'
    work.mkdir(exist_ok=False)
    binary = ROOT/'target/release/examples/fidelity.exe'
    binary_hash = sha256(binary.read_bytes()).hexdigest()
    digest = source_digest()
    runner_hash = sha256(Path(__file__).read_bytes()).hexdigest()
    task = dict(path=str(CORPUS/row['path']), options=options, seconds=1,
                time_limit=20, output=str(work/'exports'))
    write_json(work/'task.json', task)
    start = time.perf_counter()
    timeout = False
    with (work/'stdout.txt').open('wb') as stdout, (work/'stderr.txt').open('wb') as stderr:
        proc = subprocess.Popen([str(binary), '--task', str(work/'task.json')], cwd=ROOT,
            env={**os.environ, 'NESTBOLT_DEBUG':'1'}, stdout=stdout, stderr=stderr,
            creationflags=subprocess.CREATE_NO_WINDOW | 4)
        try:
            child = psutil.Process(proc.pid)
            child.cpu_affinity([8])
            child.resume()
            try:
                proc.wait(timeout=args.timeout)
            except subprocess.TimeoutExpired:
                timeout = True
                proc.kill()
                proc.wait()
        except BaseException:
            proc.kill()
            proc.wait()
            raise
    elapsed = time.perf_counter()-start
    assert source_digest() == digest
    assert sha256(binary.read_bytes()).hexdigest() == binary_hash
    assert sha256(Path(__file__).read_bytes()).hexdigest() == runner_hash
    report = dict(date=stamp, scope='Training-only bounded fidelity phase diagnostic; not H2 acceptance',
        H2=False, held_out_read=False, source=row['path'], source_sha256=row['sha256'],
        label_sha256=row['label_sha256'], manifest_sha256=sha256(raw).hexdigest(),
        product_digest=digest, binary_sha256=binary_hash, runner_sha256=runner_hash,
        cpu=8, task=task, external_timeout_s=args.timeout, elapsed_s=elapsed,
        timed_out=timeout, exit_code=proc.returncode,
        stdout=(work/'stdout.txt').read_text(encoding='utf-8', errors='replace'),
        stderr=(work/'stderr.txt').read_text(encoding='utf-8', errors='replace'),
        exported_files=sorted(p.name for p in (work/'exports').glob('*')))
    out = ROOT/'benchmarks/results'/f'h2-dense-profile-{stamp}.json'
    write_json(out, report)
    print(json.dumps(dict(report=str(out), elapsed_s=elapsed, timed_out=timeout,
                         stderr=report['stderr'], files=report['exported_files']), indent=2))


if __name__ == '__main__':
    main()
