"""Prepare isolated, pinned maker-source generators (never installed in the app)."""
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.request import Request, urlopen
import venv

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'benchmarks/makers'


def main():
    config = json.loads((CONFIG / 'sources.json').read_bytes())
    if sys.version_info[:2] != (3, 11):
        raise ValueError('Run setup with Python 3.11; rebuild comparison verifies exact output bytes')
    node = subprocess.check_output(['node', '--version'], text=True).strip().removeprefix('v')
    if node != config['node_version']:
        raise ValueError(f'Use pinned Node {config["node_version"]}; found {node}')
    checkout = ROOT / '.cache/upstream/boxes'
    boxes = config['sources']['boxes']
    if not checkout.exists():
        checkout.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', '--no-checkout', '--filter=blob:none', boxes['repository'], str(checkout)], check=True)
        subprocess.run(['git', '-C', str(checkout), 'checkout', '--detach', boxes['revision']], check=True)
    actual = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != boxes['revision'] or subprocess.check_output(
            ['git', '-C', str(checkout), 'status', '--porcelain', '--untracked-files=no'], text=True).strip():
        raise ValueError('Preserve the existing Boxes.py checkout; a clean pinned checkout is required')
    cache = ROOT / '.cache/maker-sources'
    cache.mkdir(parents=True, exist_ok=True)
    for source in config['sources'].values():
        for download in source.get('downloads', []):
            path = cache / download['cache_name']
            if not path.exists():
                data = urlopen(Request(download['url'], headers={'User-Agent': 'Nestbolt benchmark source fetcher'}), timeout=60).read()
                if sha256(data).hexdigest() != download['sha256']:
                    raise ValueError(f'Source checksum mismatch: {download["cache_name"]}')
                path.write_bytes(data)
            elif sha256(path.read_bytes()).hexdigest() != download['sha256']:
                raise ValueError(f'Cached source checksum mismatch: {path.name}')
    environment = ROOT / '.cache/maker-venv'
    python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        venv.create(environment, with_pip=True)
    subprocess.run([str(python), '-m', 'pip', 'install', '--require-hashes', '-r', str(CONFIG / 'requirements.txt')], check=True)
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    if not npm:
        raise ValueError('npm is required alongside the pinned Node runtime')
    subprocess.run([npm, 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=CONFIG, check=True)
    print(f'Prepared isolated generators: {python}')


if __name__ == '__main__':
    main()
