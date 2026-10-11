"""Bounded development-only constructor diagnostic; never a final gate."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time
import uuid

from dataset_selection import development_cases

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    directory = ROOT/'output/construct-pilots'/stamp
    directory.mkdir(parents=True)
    binary = ROOT/'target/release/nestbolt.exe'
    manifest, cases = development_cases(ROOT, 'M')
    sources = {p: digest(ROOT/p) for p in ['Cargo.lock','crates/core/src/construct.rs',
        'crates/cli/src/main.rs','crates/validator/src/lib.rs','crates/validator/src/job.rs']}
    rows = []
    for case in cases:
        job = ROOT/'benchmarks/datasets'/case['path']
        assert digest(job) == case['sha256']
        run_dir = directory/case['id']
        run_dir.mkdir()
        start = time.monotonic()
        with (run_dir/'stdout.json').open('wb') as out, (run_dir/'stderr.txt').open('wb') as err:
            try:
                run = subprocess.run([str(binary), 'construct', '--job', str(job), '--output',
                    str(run_dir/'layout.json'), '--seed', '0', '--samples', '64'],
                    cwd=ROOT, stdout=out, stderr=err, timeout=60)
                status = 'valid' if run.returncode == 0 else 'failed'
                exit_code = run.returncode
            except subprocess.TimeoutExpired:
                status, exit_code = 'timeout', None
        wall = time.monotonic()-start
        report = None
        if (run_dir/'stdout.json').stat().st_size:
            report = json.loads((run_dir/'stdout.json').read_bytes())
            if not report['construction']['complete']:
                status = 'incomplete'
        if status == 'valid':
            assert report['validation']['valid'] and report['construction']['complete']
            check = subprocess.run([str(binary),'validate','--job',str(job),'--layout',str(run_dir/'layout.json')],
                cwd=ROOT,capture_output=True,check=True)
            assert json.loads(check.stdout)['valid']
            (run_dir/'independent.json').write_bytes(check.stdout)
        row = {'job':case['id'],'job_sha256':case['sha256'],'status':status,'exit_code':exit_code,
            'wall_seconds':wall,'report':report,'stderr':(run_dir/'stderr.txt').read_text(),
            'outputs':{p.name:digest(p) for p in run_dir.iterdir()}}
        rows.append(row)
        print(json.dumps({k:row[k] for k in ['job','status','wall_seconds']}),flush=True)
        (directory/'progress.json').write_text(json.dumps(rows,indent=2)+'\n')
    assert all(digest(ROOT/p)==checksum for p,checksum in sources.items())
    result={'scope':'First Nestbolt constructor diagnostic: all 30 development maker jobs, seed 0, 64 random samples per orientation/region, 60-second process cap. No held-out jobs or quality gate.',
        'binary_sha256':digest(binary),'sources':sources,'manifest_sha256':digest(manifest),'rows':rows}
    target=ROOT/'benchmarks/results'/f'construct-maker-{stamp}.json'
    with target.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(target,flush=True)


if __name__=='__main__':
    main()
