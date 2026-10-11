"""Freeze/check maker jobs and the ten held-out reservations, without solving."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'benchmarks/datasets'
MANIFEST = DEST / 'makers.json'
CANDIDATES = ROOT / 'output/maker-candidates'
MAKERS = ROOT / 'benchmarks/makers'
PROOF = ROOT / 'output/maker-source-validation/report.json'
INPUTS = ['scripts/makers.py', 'scripts/maker_geometry.py', 'scripts/validate_makers.py',
          'benchmarks/makers/freesewing.mjs', 'benchmarks/makers/sources.json',
          'benchmarks/makers/package.json', 'benchmarks/makers/package-lock.json',
          'benchmarks/makers/requirements.txt']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def serialized(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')


def safe_path(relative):
    path = (DEST / relative).resolve()
    if not path.is_relative_to(DEST.resolve()):
        raise ValueError('Dataset path escapes its directory')
    return path


def check_frozen():
    manifest = json.loads(MANIFEST.read_bytes())
    for relative, expected in manifest['inputs'].items():
        if digest(ROOT / relative) != expected:
            raise ValueError(f'Frozen maker source changed: {relative}')
    for relative, expected in manifest['notice_files'].items():
        if digest(MAKERS / relative) != expected:
            raise ValueError(f'Frozen maker notice changed: {relative}')
    rows = manifest['instances']
    if len(rows) != 40 or len({r['id'] for r in rows}) != 40:
        raise ValueError('Expected forty distinct frozen maker jobs')
    reserved = sorted(r['id'] for r in rows if r['held_out'])
    if len(reserved) != 10 or reserved != manifest['held_out_ids']:
        raise ValueError('Held-out reservation changed')
    listed = set()
    for row in rows:
        for relative, expected in row['files'].items():
            if digest(safe_path(relative)) != expected:
                raise ValueError(f'Frozen maker file changed: {relative}')
            listed.add(relative)
        job = json.loads(safe_path(row['path']).read_bytes())
        if row['part_count'] != sum(p['quantity'] for p in job['parts']):
            raise ValueError('Maker copy count changed')
    actual = {p.relative_to(DEST).as_posix() for name in ['M', 'maker-assets']
              for p in (DEST / name).rglob('*') if p.is_file()}
    if listed != actual:
        raise ValueError('Missing or unlisted maker files')
    proof_path = safe_path(manifest['feasibility_proof']['path'])
    if digest(proof_path) != manifest['feasibility_proof']['sha256']:
        raise ValueError('Source-feasibility proof changed')
    proof = json.loads(proof_path.read_bytes())
    evidence = {r['id']: r for r in proof['instances']}
    if set(evidence) != {r['id'] for r in rows}:
        raise ValueError('Incomplete source-feasibility evidence')
    for row in rows:
        if evidence[row['id']]['job_sha256'] != row['files'][row['path']] or not evidence[row['id']]['validation']['valid']:
            raise ValueError('Source-feasibility evidence does not match the frozen job')
    print('Checked 40 frozen maker jobs, curve sources, notices and 10 held-out reservations.')


def rebuild_matches(rows):
    before = {r['id']: r['files'] for r in rows}
    python = ROOT / '.cache/maker-venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    subprocess.run([str(python), 'scripts/makers.py'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    after = json.loads((CANDIDATES / 'candidates.json').read_bytes())['instances']
    if before != {r['id']: r['files'] for r in after}:
        raise ValueError('Maker rebuild changed source bytes; freeze refused')
    print('All forty jobs and retained curves rebuild byte for byte.')


def freeze():
    if MANIFEST.exists() or (DEST / 'M').exists() or (DEST / 'maker-assets').exists():
        raise ValueError('A maker freeze already exists; never replace it after tuning')
    rows = json.loads((CANDIDATES / 'candidates.json').read_bytes())['instances']
    if len(rows) != 40 or sum(r['held_out'] for r in rows) != 10:
        raise ValueError('The maker set must contain forty jobs with ten reserved')
    rebuild_matches(rows)
    evidence = {r['id']: r for r in json.loads(PROOF.read_bytes())['instances']}
    for row in rows:
        if not re.fullmatch(r'm-[a-z0-9-]+', row['id']):
            raise ValueError('Unsafe maker identifier')
        if evidence[row['id']]['job_sha256'] != row['files']['job.json'] or not evidence[row['id']]['validation']['valid']:
            raise ValueError('Run independent source-feasibility checks before freezing')
    manifest = {'version': 1, 'frozen_at': datetime.now(timezone.utc).isoformat(),
        'status': 'frozen before any optimiser tuning',
        'policy': 'Held-out jobs may be checked for source validity and final acceptance only. They must not inform solver tuning or selection. This freeze performed no optimiser runs.',
        'curve_flattening_tolerance_mm': .005, 'coordinate_rounding_decimal_places': 9,
        'held_out_ids': sorted(r['id'] for r in rows if r['held_out']),
        'inputs': {name: digest(ROOT / name) for name in INPUTS},
        'notice_files': {p.relative_to(MAKERS).as_posix(): digest(p) for p in sorted((MAKERS / 'licenses').iterdir()) if p.is_file()},
        'feasibility_proof': {'path': 'maker-feasibility.json', 'sha256': digest(PROOF)}, 'instances': []}
    for row in rows:
        identifier = row['id']
        assets = DEST / 'maker-assets' / identifier
        assets.mkdir(parents=True)
        (DEST / 'M').mkdir(exist_ok=True)
        files = {}
        for name, expected in row['files'].items():
            if Path(name).name != name:
                raise ValueError('Unsafe source filename')
            source = CANDIDATES / identifier / name
            if digest(source) != expected:
                raise ValueError('Candidate file changed')
            destination = DEST / 'M' / f'{identifier}.json' if name == 'job.json' else assets / name
            shutil.copyfile(source, destination)
            files[destination.relative_to(DEST).as_posix()] = expected
        manifest['instances'].append({**row, 'path': f'M/{identifier}.json', 'files': files})
    shutil.copyfile(PROOF, DEST / 'maker-feasibility.json')
    with MANIFEST.open('xb') as handle:
        handle.write(serialized(manifest))
    check_frozen()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--freeze', action='store_true')
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--rebuild', action='store_true')
    args = parser.parse_args()
    if args.freeze:
        freeze()
    elif args.check:
        check_frozen()
    else:
        check_frozen()
        rows = json.loads(MANIFEST.read_bytes())['instances']
        adapted = [{**row, 'files': {'job.json' if path == row['path'] else Path(path).name: value
                                    for path, value in row['files'].items()}} for row in rows]
        rebuild_matches(adapted)


if __name__ == '__main__':
    main()
