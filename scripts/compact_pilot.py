"""Compact an explicitly selected development pilot; retain every outcome."""
import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time
import uuid

from dataset_selection import development_cases
from svgnest import ROOT, digest, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--dataset', choices=['B', 'M'], required=True)
    parser.add_argument('--cpu', type=int, default=4)
    parser.add_argument('--relocate', action='store_true')
    args = parser.parse_args()
    if os.name != 'nt' or not 0 <= args.cpu < 64:
        parser.error('This diagnostic uses Windows single-CPU affinity')
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.SetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.c_size_t]
    kernel.GetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t)]
    handle = kernel.GetCurrentProcess()
    mask, system = ctypes.c_size_t(), ctypes.c_size_t()
    if (not kernel.SetProcessAffinityMask(handle, 1 << args.cpu)
            or not kernel.GetProcessAffinityMask(handle, ctypes.byref(mask), ctypes.byref(system))
            or mask.value != 1 << args.cpu):
        raise ctypes.WinError(ctypes.get_last_error())
    baseline = json.loads(args.baseline.read_bytes())
    manifest, cases = development_cases(ROOT, args.dataset)
    cases = {row['id']: row for row in cases}
    if {r['job'] for r in baseline['rows']} != set(cases) or len(baseline['rows']) != len(cases):
        raise ValueError('Baseline must contain exactly the development population')
    binary = ROOT/'target/release/nestbolt.exe'
    binary_hash = digest(binary)
    files = ['Cargo.lock', 'scripts/compact_pilot.py', 'crates/cli/src/main.rs',
             'crates/core/src/construct.rs', 'crates/core/src/construct/repair.rs',
             'crates/core/src/construct/repair/compact.rs', 'crates/core/src/control.rs',
             'crates/validator/src/lib.rs', 'crates/validator/src/job.rs']
    sources = {name: digest(ROOT/name) for name in files}
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    directory = ROOT/'output/compact-pilots'/stamp
    directory.mkdir(parents=True)
    rows = []
    for old in baseline['rows']:
        case = cases[old['job']]
        job = ROOT/'benchmarks/datasets'/case['path']
        if old['job_sha256'] != case['sha256'] or digest(job) != case['sha256'] or old['status'] != 'valid':
            raise ValueError('Baseline job changed or has no valid source layout')
        dest = directory/case['id']
        dest.mkdir()
        write(dest/'source-layout.json', old['report']['construction']['layout'])
        started = time.monotonic()
        with (dest/'stdout.json').open('wb') as out, (dest/'stderr.txt').open('wb') as err:
            try:
                result = subprocess.run([str(binary), 'compact', '--job', str(job), '--layout',
                    str(dest/'source-layout.json'), '--output', str(dest/'layout.json'), '--sweeps', '2']
                    + (['--relocate'] if args.relocate else []),
                    stdout=out, stderr=err, cwd=ROOT, timeout=60)
                status, code = ('valid' if result.returncode == 0 else 'failed'), result.returncode
            except subprocess.TimeoutExpired:
                status, code = 'timeout', None
        row = {'job': case['id'], 'job_sha256': case['sha256'], 'status': status, 'exit_code': code,
               'wall_seconds': time.monotonic()-started,
               'before': old['report']['validation']['metrics']['normalized_material']}
        if status == 'valid':
            report = json.loads((dest/'stdout.json').read_bytes())
            checked = subprocess.run([str(binary), 'validate', '--job', str(job), '--layout', str(dest/'layout.json')],
                                     capture_output=True, check=True, timeout=60)
            independent = json.loads(checked.stdout)
            assert independent['valid'] and report['validation'] == independent
            (dest/'independent.json').write_bytes(checked.stdout)
            row.update(report=report, after=independent['metrics']['normalized_material'])
        row.update(stderr=(dest/'stderr.txt').read_text(encoding='utf-8'),
                   outputs={p.name: digest(p) for p in dest.iterdir()})
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k not in ['report','outputs','stderr']}), flush=True)
        with (directory/'progress.json').open('w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(rows, indent=2)+'\n')
    assert digest(binary) == binary_hash and sources == {name:digest(ROOT/name) for name in files}
    proof = {'scope': 'Two-sweep compaction of saved development layouts. 60-second process cap per case; no G2/G4 claim.',
             'relocate': args.relocate,
             'baseline': args.baseline.as_posix(), 'baseline_sha256': digest(args.baseline),
             'dataset': args.dataset, 'manifest_sha256': digest(manifest), 'binary_sha256': binary_hash,
             'sources': sources, 'inherited_cpu_mask': mask.value, 'rows': rows}
    stem = f'compact-{args.dataset.lower()}-{stamp}'
    target = ROOT/'benchmarks/results'/stem
    write(target.with_suffix('.json'), proof)
    lines = ['# Development compaction diagnostic', '', proof['scope'], '',
             '| Job | Status | Before | After | Wall seconds |', '| --- | --- | ---: | ---: | ---: |']
    for row in rows:
        after = f"{row['after']:.8f}" if row['status'] == 'valid' else '—'
        lines.append(f"| {row['job']} | {row['status']} | {row['before']:.8f} | {after} | {row['wall_seconds']:.3f} |")
    lines += ['', f'[Full outputs, original-layout hashes and provenance]({stem}.json).', '']
    with target.with_suffix('.md').open('x', encoding='utf-8', newline='\n') as f:f.write('\n'.join(lines))
    with (ROOT/'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as f:
        f.write(f'\n- {datetime.now(timezone.utc).isoformat()} | Two-sweep compaction of {len(rows)} {args.dataset} development layouts; every attempt retained | [evidence](benchmarks/results/{stem}.md).\n')
    print(target.with_suffix('.md'))


if __name__ == '__main__':
    main()
