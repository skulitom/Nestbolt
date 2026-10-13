"""Retain authored-fixture CLI search/export evidence and the tight-sheet failure.

Development integration diagnostic, not corpus acceptance or a quality claim.
Requires the already-built release CLI. Windows child processes start suspended
and run sequentially on one CCD0 physical core. Never reads a held-out file.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

import psutil
from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT/'crates/core/tests/fixtures/roundtrip.lbrn2'
    binary = ROOT/'target/release/nestbolt.exe'
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    target = ROOT/'benchmarks/results'/f'h3-surfaces-{stamp}'
    target.mkdir(exist_ok=False)
    digest = source_digest()
    binary_hash = sha256(binary.read_bytes()).hexdigest()
    records = []
    for width, seconds in [(32, 1), (32, 5), (34, 1)]:
        name = f'w{width}-s{seconds}'
        request = target/f'{name}-request.json'
        request.write_text(json.dumps({'sheets': [{'width_mm': width, 'height_mm': 24}],
            'spacing_mm': 1, 'edge_spacing_mm': 0.5}, indent=2)+'\n', encoding='utf-8', newline='\n')
        command = [str(binary), 'nest', '--library', str(source), '--request', str(request),
                   '--out-dir', str(target/name), '--seconds', str(seconds), '--repeatable', '--time-limit', '30']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW | 0x00000004,
            env={**os.environ, 'NESTBOLT_DEBUG': '1', 'RAYON_NUM_THREADS': '1'})
        try:
            child = psutil.Process(process.pid)
            child.cpu_affinity([8])
            child.resume()
            stdout, stderr = process.communicate(timeout=40)
        except BaseException:
            process.kill()
            process.communicate()
            raise
        for extension, content in [('stdout.txt', stdout), ('stderr.txt', stderr)]:
            (target/f'{name}.{extension}').write_bytes(content)
        records.append({'name': name, 'command': command, 'exit_code': process.returncode,
                        'logical_cpu': 8, 'width_mm': width, 'height_mm': 24, 'seconds': seconds})
    assert digest == source_digest(), 'Sources changed during diagnostic'
    assert binary_hash == sha256(binary.read_bytes()).hexdigest(), 'Binary changed during diagnostic'
    report = {'kind': 'authored-fixture surface diagnostic', 'H3_acceptance': False,
        'source_sha256': digest, 'binary_sha256': binary_hash,
        'fixture_sha256': sha256(source.read_bytes()).hexdigest(),
        'runner_sha256': sha256(Path(__file__).read_bytes()).hexdigest(), 'runs': records}
    (target/'native.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'directory': str(target), 'runs': records}, indent=2))


if __name__ == '__main__':
    main()
