"""Read-only N2 training diagnostics; never examines a held-out project or label.

This does not claim H3: native comparison, nesting units, preserving sheet writes
and the public surfaces are separate work. Unsupported geometry stays explicit.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time

import psutil
from h2_import_audit import source_digest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def main():
    manifest_bytes = (CORPUS/'manifest.json').read_bytes()
    training = [r for r in json.loads(manifest_bytes)['files'] if r['split'] == 'training']
    rows = [r for r in training if Path(r['path']).suffix in ['.lbrn', '.lbrn2']]
    assert len(rows) == 56
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    work = ROOT/'output'/f'h3-reader-{stamp}'
    work.mkdir(exist_ok=False)
    binary = ROOT/'target/release/examples/lightburn_inspect.exe'
    binary_hash = sha256(binary.read_bytes()).hexdigest()
    source_hash = source_digest()
    runner_hash = sha256(Path(__file__).read_bytes()).hexdigest()

    def run(index, row):
        path = CORPUS/row['path']
        assert sha256(path.read_bytes()).hexdigest() == row['sha256']
        begin = time.perf_counter()
        proc = subprocess.Popen([str(binary), str(path)], cwd=ROOT, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW | 4)
        timed_out = False
        try:
            child = psutil.Process(proc.pid)
            child.cpu_affinity([2*(index % 4)])
            child.resume()
            try:
                out, err = proc.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                timed_out = True
                proc.kill()
                out, err = proc.communicate()
        except BaseException:
            proc.kill()
            proc.communicate()
            raise
        record = {'path': row['path'], 'source_sha256': row['sha256'], 'cpu': 2*(index % 4),
                  'elapsed_s': time.perf_counter()-begin, 'exit_code': proc.returncode,
                  'stderr': err.decode('utf-8', errors='replace'),
                  'status': 'timeout' if timed_out else 'error' if proc.returncode else 'parsed'}
        if not proc.returncode:
            payload = json.loads(out)
            target = work/f'{index:03}.json'
            target.write_bytes(out)
            scene = payload['scene']
            incomplete = [i for i, shape in enumerate(scene['shapes'])
                          if not shape['geometry_complete'] and shape['kind'] != 'Group']
            record.update(scene_path=str(target.relative_to(ROOT)),
                          scene_sha256=sha256(out).hexdigest(),
                          noop_byte_identical=payload['noop_byte_identical'],
                          format_version=scene['format_version'],
                          top_level_shapes=len(scene['top_level']),
                          all_shapes=len(scene['shapes']),
                          shape_types=dict(Counter(s['kind'] for s in scene['shapes'])),
                          paths=sum(len(s['paths']) for s in scene['shapes']),
                          bitmaps=sum(s['bitmap_corners'] is not None for s in scene['shapes']),
                          incomplete_shapes=incomplete, warnings=scene['warnings'])
        print(f'{index+1}/{len(rows)} {row["path"]}: {record["status"]}', flush=True)
        return record

    def batch(slot):
        return [run(i, r) for i, r in enumerate(rows) if i % 4 == slot]

    with ThreadPoolExecutor(max_workers=4) as pool:
        reports = [r for group in pool.map(batch, range(4)) for r in group]
    reports.sort(key=lambda r: r['path'])
    assert source_hash == source_digest()
    assert binary_hash == sha256(binary.read_bytes()).hexdigest()
    assert runner_hash == sha256(Path(__file__).read_bytes()).hexdigest()
    result = {'date': stamp, 'scope': 'N2 training reader and byte-preserving no-op, not H3 acceptance',
              'H3': False, 'held_out_read': False, 'source_sha256': source_hash,
              'binary_sha256': binary_hash, 'runner_sha256': runner_hash,
              'manifest_sha256': sha256(manifest_bytes).hexdigest(),
              'counts': dict(Counter(r['status'] for r in reports)),
              'noop_byte_identical': sum(r.get('noop_byte_identical', False) for r in reports),
              'geometry_complete_projects': sum(r['status'] == 'parsed' and not r['incomplete_shapes'] for r in reports),
              'rows': reports}
    output = ROOT/'benchmarks/results'/f'h3-reader-{stamp}.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(str(output))


if __name__ == '__main__':
    main()
