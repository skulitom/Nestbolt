"""Recheck retained development layouts and require identical independent reports."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import time
import uuid

from dataset_selection import development_cases
from lbf_report import contained_file
from svgnest import ROOT, digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--pilot', type=Path, action='append', required=True)
    args = parser.parse_args()
    binary = args.binary.resolve(strict=True)
    binary_hash = digest(binary)
    cases = {case['id']: case for group in ['S', 'B', 'M']
             for case in development_cases(ROOT, group)[1]}
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    directory = ROOT/'output/validator-replays'/stamp
    directory.mkdir(parents=True)
    sources = {name: digest(ROOT/name) for name in
               ['crates/validator/src/lib.rs', 'crates/validator/src/job.rs', 'Cargo.lock',
                'scripts/validator_replay.py']}
    pilots, rows = [], []
    for supplied in args.pilot:
        pilot = contained_file(ROOT, str(supplied))
        data = json.loads(pilot.read_bytes())
        pilots.append({'path': pilot.relative_to(ROOT).as_posix(), 'sha256': digest(pilot)})
        for attempt in data['rows']:
            case = cases[attempt['job']]
            job = ROOT/'benchmarks/datasets'/case['path']
            if digest(job) != case['sha256'] or attempt['job_sha256'] != case['sha256']:
                raise ValueError('Frozen source changed')
            if attempt['status'] != 'valid':
                raise ValueError('This replay requires retained valid outputs, not missing layouts')
            saved = attempt.get('report') or attempt['result']
            layout = (saved.get('construction') or saved)['layout']
            expected = saved['validation']
            dest = directory/str(len(rows))
            dest.mkdir()
            (dest/'layout.json').write_text(json.dumps(layout),encoding='utf-8',newline='\n')
            start = time.monotonic()
            run = subprocess.run([str(binary), 'validate', '--job', str(job), '--layout',
                                  str(dest/'layout.json')], capture_output=True, timeout=60, cwd=ROOT)
            elapsed = time.monotonic()-start
            (dest/'stdout.json').write_bytes(run.stdout)
            (dest/'stderr.txt').write_bytes(run.stderr)
            actual = json.loads(run.stdout) if run.returncode == 0 else None
            rows.append({'job':case['id'], 'pilot':pilot.relative_to(ROOT).as_posix(),
                         'job_sha256':case['sha256'], 'exit_code':run.returncode,
                         'identical_report':actual == expected, 'wall_seconds':elapsed,
                         'outputs':{p.name:digest(p) for p in dest.iterdir()}})
    if digest(binary) != binary_hash or any(digest(ROOT/p) != h for p,h in sources.items()):
        raise ValueError('Replay executable or sources changed')
    target = ROOT/'benchmarks/results'/f'validator-replay-{stamp}.json'
    proof = {'scope':'Retained development layouts only; exact independent-report equivalence, no new solve or final validity gate.',
             'binary_sha256':binary_hash, 'sources':sources, 'pilots':pilots,
             'directory':directory.relative_to(ROOT).as_posix(), 'rows':rows,
             'all_reports_identical':all(row['identical_report'] for row in rows)}
    with target.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(proof,stream,indent=2)
        stream.write('\n')
    print(target, flush=True)
    if not proof['all_reports_identical']:
        raise ValueError('Independent validation changed; inspect retained replay')
    print(f'All {len(rows)} independent reports are exactly equal.', flush=True)


if __name__ == '__main__':
    main()
