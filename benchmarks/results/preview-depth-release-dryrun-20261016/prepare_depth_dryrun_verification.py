"""Download the current identified dry-run artifacts and prepare verification."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[1]
run = '38854620093'
commit = '23442be38ee2e881669e753bc405ab3269ff1b39'
download = root / ('output/preview-depth-release-dryrun-' + run)
workflow = subprocess.check_output([
    'gh', 'run', 'view', run, '--json',
    'conclusion,headSha,jobs,url,status,event'], cwd=root)
record = json.loads(workflow)
assert record['conclusion'] == 'success' and record['status'] == 'completed'
assert record['headSha'] == commit and record['event'] == 'workflow_dispatch'
assert all(j['conclusion'] == 'success' for j in record['jobs'] if j['name'] != 'release')
assert next(j for j in record['jobs'] if j['name'] == 'release')['conclusion'] == 'skipped'
download.mkdir(exist_ok=False)
(download / 'workflow.json').write_bytes(workflow)

def fetch(pair):
    platform, target = pair
    subprocess.run(['gh', 'run', 'download', run, '-n',
                    'nestbolt-build-' + target, '-D', str(download / platform)],
                   cwd=root, check=True, timeout=300)
    return platform

with ThreadPoolExecutor(max_workers=3) as pool:
    print('Downloaded:', ', '.join(pool.map(fetch, [
        ('windows', 'x86_64-pc-windows-msvc'),
        ('linux', 'x86_64-unknown-linux-gnu'),
        ('macos', 'aarch64-apple-darwin')
    ])))

source = (root / 'output/verify_preview_score_dryrun.py').read_text(encoding='utf-8')
for before, after in [
    ('output/preview-score-release-dryrun-38840747735', 'output/preview-depth-release-dryrun-' + run),
    ('benchmarks/results/preview-score-release-dryrun-20261016', 'benchmarks/results/preview-depth-release-dryrun-20261016'),
    ('7eba929420d218d04169c1fdf24481051c8afae5', commit),
    ('7eba929', commit[:7]),
]:
    assert before in source
    source = source.replace(before, after)
verifier = root / 'output/verify_preview_depth_dryrun.py'
assert not verifier.exists()
compile(source, str(verifier), 'exec')
verifier.write_text(source, encoding='utf-8', newline='\n')
print('Prepared unchanged isolated package checks for commit ' + commit)
