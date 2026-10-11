"""Verify immutable SVGnest evidence before retaining a provisional baseline table."""
import argparse
import json
import math
from pathlib import Path

from svgnest import digest
from lbf_report import contained_file


def audit_record(path, expected_hash):
    if digest(path) != expected_hash:
        raise ValueError('Run record changed')
    run = json.loads(path.read_bytes())
    for name, checksum in run['outputs'].items():
        if digest(contained_file(path.parent, name)) != checksum:
            raise ValueError('Recorded output changed')
    if digest(path.parent / 'job.json') != run['job_sha256']:
        raise ValueError('Copied source job changed')
    if run['status'] == 'valid':
        if run.get('output_decoding') != 'native_svg_attributes_v2':
            raise ValueError('Legacy browser-matrix decode requires correction from saved native SVG attributes')
        required = {'job.json', 'layout.json', 'validation.json', 'request.json', 'browser-result.json', 'candidates.jsonl'}
        if not required.issubset(run['outputs']):
            raise ValueError('Valid run is missing independent evidence')
        checked = json.loads((path.parent / 'validation.json').read_bytes())
        raw = json.loads((path.parent / 'browser-result.json').read_bytes())
        if run.get('input_encoding') == 'linear_svg_paths_v2':
            proof = raw.get('input_fidelity')
            if not proof or proof != run.get('input_fidelity') or proof.get('encoding') != run['input_encoding'] or proof.get('coordinates',0) < 6:
                raise ValueError('Native input fidelity was not verified')
            if 'scaled_error_limit' in proof:
                if (proof['scaled_error_limit'] != 8 or proof.get('error_scale') != 'Number.EPSILON * max(1, abs(source_coordinate))'
                        or not 0 <= proof.get('maximum_scaled_error',float('inf')) <= 8
                        or not math.isfinite(proof.get('maximum_absolute_error',float('inf'))) or proof['maximum_absolute_error'] < 0):
                    raise ValueError('Native input fidelity exceeds double-precision rounding allowance')
            elif proof.get('maximum_absolute_error') != 0:
                raise ValueError('Legacy exact input fidelity claim has no rounding evidence')
        if not checked['valid'] or run['validator_exit_code'] != 0 or run['metrics'] != checked['metrics'] or run['score'] != checked['metrics']['normalized_material']:
            raise ValueError('Recorded score differs from independent validation')
        if raw['status'] != 'completed' or raw['errors'] or raw['last']['elapsed_ms'] > run['seconds'] * 1000:
            raise ValueError('Native result is incomplete or exceeded its budget')
        affinity = raw['affinity']
        expected = affinity.get('mask', affinity.get('cpu'))
        evidence = raw.get('affinity_verification', [])
        if raw['configured_workers'] != 1 or len(evidence) < 2 or any(p['affinity'] != expected for p in evidence):
            raise ValueError('Run lacks a verified single-core process tree')
        if affinity['platform'] == 'win32' and affinity.get('method') != 'JOB_OBJECT_LIMIT_AFFINITY':
            raise ValueError('Run lacks enforced Windows process-tree affinity')
        if affinity['platform'] == 'win32':
            mask=int(affinity['mask'])
            if mask<=0 or mask&(mask-1) or ('cpu_index' in affinity and mask != 1<<affinity['cpu_index']):
                raise ValueError('Windows evidence does not select a single-core affinity')
        if run['affinity_verification'] != evidence or run['cpu_affinity'] != affinity:
            raise ValueError('Run CPU provenance differs from native evidence')
    elif run['score'] is not None or run.get('metrics') is not None:
        raise ValueError('Failed or unsupported run cannot receive a score')
    return run


def report(path):
    from comparator_batch_report import report as report_batch
    return report_batch(path, 'svgnest')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', required=True, type=Path)
    report(parser.parse_args().batch.resolve(strict=True))
