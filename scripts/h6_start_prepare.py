"""Create a guarded, authored contour-start export probe (not H6 acceptance)."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    folder = ROOT/'benchmarks/results'/f'h6-starts-{stamp}'
    folder.mkdir(exist_ok=False)
    binary = ROOT/'target/release/examples/contour_starts.exe'
    guard = source_digest()
    binary_hash = digest(binary)
    runner_hash = digest(Path(__file__))
    run([binary, folder/'exports'], cpu=0)
    assert source_digest() == guard and digest(binary) == binary_hash
    assert digest(Path(__file__)) == runner_hash
    write_json(folder/'preparation.json', {'held_out_read': False,
               'scope': 'Authored ordered contour exports; no lead-footprint or searched native gate claim',
               'source_sha256': guard, 'binary_sha256': binary_hash,
               'runner_sha256': runner_hash, 'cpu_affinity': [0],
               'artifacts': {str(p.relative_to(folder)).replace('\\', '/'): digest(p)
                             for p in sorted((folder/'exports').iterdir())}})
    (folder/'LICENSES.md').write_text('# H6 authored start-point probe\n\n'
        'Geometry and derived native saves/screenshots are authored by Nestbolt '
        'contributors, copyright 2026, under the repository MIT LICENSE.\n', encoding='utf-8', newline='\n')
    print(folder)


if __name__ == '__main__':
    main()
