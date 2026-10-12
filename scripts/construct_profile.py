"""Windows-only development timing diagnostic on one explicit CPU, never a gate."""
import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import threading
import time
import uuid

from dataset_selection import development_cases

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--job', required=True)
    parser.add_argument('--cpu', type=int, default=8)
    parser.add_argument('--passes', type=int, default=0)
    parser.add_argument('--repeat', type=int, default=2)
    parser.add_argument('--max-checks', type=int)
    parser.add_argument('--timeout-ms', type=int)
    args = parser.parse_args()
    if os.name != 'nt' or not 0 <= args.cpu < 64 or not 0 <= args.passes <= 64 or not 1 <= args.repeat <= 3:
        parser.error('Use Windows, CPU 0..63, passes 0..64 and repeats 1..3')
    if (args.max_checks is not None and (not args.passes or args.max_checks < 0)
            or args.timeout_ms is not None and (not args.passes or not 1 <= args.timeout_ms <= 300_000)):
        parser.error('Search controls require passes, a nonnegative check limit and a 1..300000 ms deadline')
    binary = args.binary.resolve(strict=True)
    cases = [case for dataset in ['B', 'M'] for case in development_cases(ROOT, dataset)[1]]
    case = next((case for case in cases if case['id'] == args.job), None)
    if case is None:
        parser.error('Choose a frozen development B/M job; held-out profiling is disabled')
    job = ROOT/'benchmarks/datasets'/case['path']
    if digest(job) != case['sha256']:
        raise ValueError('Frozen job changed')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    directory = ROOT/'output/construct-profiles'/stamp
    directory.mkdir(parents=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.SetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.c_size_t]
    kernel.GetProcessAffinityMask.argtypes = [wintypes.HANDLE, ctypes.POINTER(ctypes.c_size_t), ctypes.POINTER(ctypes.c_size_t)]
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE, *([ctypes.POINTER(wintypes.FILETIME)] * 4)]
    binary_hash = digest(binary)
    runs = []
    for repeat in range(args.repeat):
        dest = directory/str(repeat)
        dest.mkdir()
        command = [str(binary), 'improve' if args.passes else 'construct', '--job', str(job),
                   '--output', str(dest/'layout.json'), '--seed', '0', '--samples', '64']
        if args.passes:
            command += ['--passes', str(args.passes)]
            if args.max_checks is not None:
                command += ['--max-checks', str(args.max_checks)]
            if args.timeout_ms is not None:
                command += ['--timeout-ms', str(args.timeout_ms)]
        progress = []
        started = time.monotonic()
        with (dest/'stdout.json').open('wb') as output:
            process = subprocess.Popen(command, cwd=ROOT, stdout=output, stderr=subprocess.PIPE, text=True)
            handle = wintypes.HANDLE(int(process._handle))
            mask, system = ctypes.c_size_t(), ctypes.c_size_t()
            if not kernel.SetProcessAffinityMask(handle, 1 << args.cpu) or not kernel.GetProcessAffinityMask(handle, ctypes.byref(mask), ctypes.byref(system)) or mask.value != 1 << args.cpu:
                process.kill()
                process.wait()
                raise ctypes.WinError(ctypes.get_last_error())
            timer = threading.Timer(90, process.kill)
            timer.start()
            for line in process.stderr:
                progress.append({'elapsed_seconds': time.monotonic()-started, 'message': line.rstrip()})
            process.wait()
            timer.cancel()
            times = [wintypes.FILETIME() for _ in range(4)]
            if not kernel.GetProcessTimes(handle, *(ctypes.byref(t) for t in times)):
                raise ctypes.WinError(ctypes.get_last_error())
            ticks = lambda t: (t.dwHighDateTime << 32) + t.dwLowDateTime
            row = {'repeat': repeat, 'exit_code': process.returncode, 'wall_seconds': time.monotonic()-started,
                   'cpu_seconds': (ticks(times[2])+ticks(times[3]))/10_000_000,
                   'cpu_mask': mask.value, 'progress': progress,
                   'outputs': {p.name: digest(p) for p in dest.iterdir()}}
        if process.returncode == 0:
            report = json.loads((dest/'stdout.json').read_bytes())
            if not report['validation']['valid']:
                raise ValueError('Native success lacks independent validity')
            construction = report['best'] if args.passes else report['construction']
            row['collision_checks'] = construction['collision_checks']
            row['surrogate_rejections'] = construction['surrogate_rejections']
            if args.passes:
                row.update(total_collision_checks=report['collision_checks'], stopped=report['stopped'],
                           completed_passes=report['completed_passes'])
        runs.append(row)
        print(json.dumps(row), flush=True)
    if digest(binary) != binary_hash:
        raise ValueError('Profiled binary changed')
    proof = {'scope': 'Development timing diagnostic; explicit single CPU after process creation, 90-second cap. No G4 claim.',
             'binary': str(binary), 'binary_sha256': binary_hash, 'job': args.job,
             'job_sha256': case['sha256'], 'script_sha256': digest(Path(__file__)), 'passes': args.passes,
             'max_checks': args.max_checks, 'timeout_ms': args.timeout_ms, 'runs': runs}
    (directory/'profile.json').write_text(json.dumps(proof, indent=2)+'\n', encoding='utf-8')
    print(directory, flush=True)


if __name__ == '__main__':
    main()
