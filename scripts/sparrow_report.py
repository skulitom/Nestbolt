"""Audit immutable current-Sparrow candidate deadlines and independent scores."""
import json
from lbf_report import contained_file
from sparrow_benchmark import digest
from sparrow_io import strip_length


def audit_record(path, expected_hash):
    if digest(path)!=expected_hash: raise ValueError('Sparrow record changed')
    run=json.loads(path.read_bytes())
    for name,h in run['outputs'].items():
        if digest(contained_file(path.parent,name))!=h: raise ValueError('Output bytes changed')
    if digest(path.parent/'job.json')!=run['job_sha256']: raise ValueError('Original job changed')
    if run['status']=='valid':
        required={'job.json','input.json','request.json','layout.json','validation.json','solver-result.json','candidates.jsonl'}
        if not required.issubset(run['outputs']): raise ValueError('Incomplete validation evidence')
        raw=json.loads((path.parent/'solver-result.json').read_bytes())
        checked=json.loads((path.parent/'validation.json').read_bytes())
        if not checked['valid'] or run['validator_exit_code']!=0 or run['metrics']!=checked['metrics']: raise ValueError('Invalid independent result')
        if raw['status']!='completed' or raw['error'] or raw['workers']!=1 or run['workers']!=1 or run['rayon_threads']!=1:
            raise ValueError('Unsuccessful native run or changed worker count')
        if raw['seed']!=run['seed'] or raw['seconds']!=run['seconds'] or raw['settings']!=run['settings']:
            raise ValueError('Native configuration differs')
        candidates=[json.loads(line) for line in (path.parent/'candidates.jsonl').read_text().splitlines()]
        if not candidates or len(candidates)!=raw['candidates'] or candidates[-1]['solution']!=raw['solution']:
            raise ValueError('Selected solution differs from retained candidate history')
        elapsed=[c['elapsed_seconds'] for c in candidates]
        widths=[c['solution']['strip_width'] for c in candidates]
        if any(t<0 or t>run['seconds'] for t in elapsed) or elapsed!=sorted(elapsed) or any(a<=b for a,b in zip(widths,widths[1:])):
            raise ValueError('Late, unordered or non-improving candidates')
        if elapsed[-1]!=raw['accepted_at_seconds']: raise ValueError('Selection time differs')
        if run['score_kind']=='strip_length':
            wanted=strip_length(json.loads((path.parent/'job.json').read_bytes()),json.loads((path.parent/'layout.json').read_bytes()))
        elif run['score_kind']=='normalized_material': wanted=checked['metrics']['normalized_material']
        else: raise ValueError('Unknown score metric')
        if run['score']!=wanted: raise ValueError('Score differs from original geometry')
    elif run['score'] is not None or run['metrics'] is not None: raise ValueError('Invalid outputs cannot be scored')
    return run
