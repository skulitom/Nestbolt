"""Audit a Deepnest result before using its independently validated material score."""
import argparse
import json
import math
from pathlib import Path

from svgnest import digest
from lbf_report import contained_file


def audit_record(path, expected_hash):
    if digest(path) != expected_hash:
        raise ValueError('Deepnest run record changed')
    run = json.loads(path.read_bytes())
    for name, checksum in run['outputs'].items():
        if digest(contained_file(path.parent, name)) != checksum:
            raise ValueError('Recorded output changed')
    if digest(path.parent / 'job.json') != run['job_sha256']:
        raise ValueError('Original job copy changed')
    if run['status'] == 'valid':
        required = {'job.json','layout.json','validation.json','browser-result.json','request.json','candidates.jsonl'}
        if not required.issubset(run['outputs']):
            raise ValueError('Valid run lacks independent evidence')
        checked = json.loads((path.parent / 'validation.json').read_bytes())
        raw = json.loads((path.parent / 'browser-result.json').read_bytes())
        if run.get('input_encoding') == 'linear_svg_paths_v2':
            proof = raw.get('input_fidelity')
            if not proof or proof != run.get('input_fidelity') or proof != raw['imported'].get('input_fidelity') or proof.get('encoding') != run['input_encoding'] or proof.get('coordinates',0) < 6:
                raise ValueError('Native input fidelity was not verified')
            if (proof.get('scaled_error_limit') != 8 or proof.get('error_scale') != 'Number.EPSILON * max(1, abs(source_coordinate))'
                    or not 0 <= proof.get('maximum_scaled_error',float('inf')) <= 8
                    or not math.isfinite(proof.get('maximum_absolute_error',float('inf'))) or proof['maximum_absolute_error'] < 0):
                raise ValueError('Native input fidelity exceeds double-precision rounding allowance')
        if 'stock_preparation' in run:
            proof = run['stock_preparation']
            if proof['output_sha256'] != run['outputs'].get('stock-inputs.json') or proof['input_job_sha256'] != run['job_sha256']:
                raise ValueError('Stock preparation differs from original job/evidence')
        if not checked['valid'] or run['validator_exit_code'] != 0 or run['metrics'] != checked['metrics'] or run['score'] != checked['metrics']['normalized_material']:
            raise ValueError('Score differs from independent validation')
        if raw['status'] != 'completed' or raw['errors'] or raw['last']['elapsed_ms'] > run['seconds']*1000:
            raise ValueError('Native result failed or exceeded its budget')
        if raw['worker_check'] != {'workers':1,'seed':run['seed']} or raw['imported']['seed'] != run['seed'] or raw['configured_workers'] != 1:
            raise ValueError('Worker/seed controls differ from the run declaration')
        affinity = raw['affinity']
        expected = affinity.get('mask', affinity.get('cpu'))
        observed = raw.get('affinity_verification', [])
        if len(observed) < 2 or any(p['affinity'] != expected for p in observed):
            raise ValueError('Single-core process tree was not verified')
        if affinity['platform'] == 'win32' and affinity.get('method') != 'JOB_OBJECT_LIMIT_AFFINITY':
            raise ValueError('Windows job affinity was not enforced')
        if affinity['platform'] == 'win32':
            mask=int(affinity['mask'])
            if mask<=0 or mask&(mask-1) or ('cpu_index' in affinity and mask != 1<<affinity['cpu_index']):
                raise ValueError('Windows evidence does not select a single-core affinity')
        for key in ['affinity','affinity_verification','worker_check','native_binaries','electron_executable_sha256']:
            if not raw.get(key) or run[key] != raw[key]:
                raise ValueError(f'Native provenance differs or is absent: {key}')
    elif run['score'] is not None or run.get('metrics') is not None:
        raise ValueError('Failed or unsupported result must not receive a score')
    return run


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', type=Path, required=True)
    parser.add_argument('--sha256', required=True, help='Expected run hash from the immutable batch/retained checkpoint')
    args = parser.parse_args()
    run = audit_record(args.record.resolve(strict=True), args.sha256)
    print(json.dumps({'status':run['status'], 'score':run['score']}))
