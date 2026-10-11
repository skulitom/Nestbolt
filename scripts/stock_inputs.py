"""Prepare comparator stock contours; validation always retains the original job."""
import json
import os
from pathlib import Path
import subprocess

from svgnest import ROOT, digest

SOURCES = ['crates/validator/examples/stock_adapter.rs', 'crates/validator/Cargo.toml',
           'crates/validator/src/lib.rs', 'crates/validator/src/job.rs', 'Cargo.lock']


def prepare_stocks(job_path, native_gap, destination):
    subprocess.run(['cargo', 'build', '--locked', '-p', 'nestbolt-validator',
                    '--example', 'stock_adapter'], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
    binary = ROOT/'target/debug/examples'/('stock_adapter.exe' if os.name == 'nt' else 'stock_adapter')
    result = subprocess.run([str(binary), str(Path(job_path).resolve()), str(native_gap)],
                            cwd=ROOT, capture_output=True, timeout=120)
    if result.returncode:
        raise ValueError(f'Stock input preparation failed: {result.stderr.decode("utf-8", errors="replace")}')
    parsed = json.loads(result.stdout)
    destination.write_bytes(result.stdout)
    return parsed, {'binary_sha256': digest(binary), 'sources': {name:digest(ROOT/name) for name in SOURCES},
                    'input_job_sha256': digest(job_path), 'native_gap':native_gap,
                    'output_sha256':digest(destination)}
