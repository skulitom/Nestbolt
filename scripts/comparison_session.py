"""Frozen, resumable development comparisons. Final acceptance is not enabled yet."""
import argparse
from datetime import datetime, timezone
import importlib
import json
import os
from pathlib import Path
import re

from lbf_report import contained_file
from matrix_plan import expected as expected_plan, schedule
from svgnest import ROOT, digest, write

MODULES = {'lbf':'lbf', 'deepnest':'deepnest', 'svgnest':'svgnest', 'sparrow':'sparrow_benchmark'}
AUDITORS = {'lbf':'lbf_report', 'deepnest':'deepnest_report', 'svgnest':'svgnest_report', 'sparrow':'sparrow_report'}
FOLDERS = {'lbf':'output/lbf', 'deepnest':'output/playwright/deepnest',
           'svgnest':'output/playwright/svgnest', 'sparrow':'output/sparrow-benchmark'}
SETTINGS = {'lbf':['identical','upstream-default'], 'sparrow':['identical','upstream-default'],
            'svgnest':['identical','expanded'], 'deepnest':['identical','expanded','clearance-safe']}


def session_dir(name):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,70}', name):
        raise ValueError('Session name must be a short identifier, without path separators')
    return ROOT/'output/comparison-sessions'/name


def sources(selected, settings_path):
    files = {Path(__file__).resolve(), settings_path, ROOT/'scripts/dataset_selection.py',
             ROOT/'scripts/matrix_plan.py', ROOT/'scripts/lbf_report.py', ROOT/'Cargo.lock',
             ROOT/'benchmarks/matrix-plan.json', ROOT/'benchmarks/datasets/academic.json',
             ROOT/'benchmarks/datasets/makers.json'}
    files.update((ROOT/'crates/validator/src').glob('*.rs'))
    files.add(ROOT/'target/debug'/('nestbolt.exe' if os.name=='nt' else 'nestbolt'))
    for tool in selected:
        module = importlib.import_module(MODULES[tool])
        files.update(ROOT/p for p in (module.SOURCE_FILES if tool=='svgnest' else module.SOURCES))
        files.add(ROOT/f'scripts/{AUDITORS[tool]}.py')
        config = ROOT/f'benchmarks/{tool}/tool.json'
        if config.exists(): files.add(config)
        if tool=='lbf':
            module.built_tool()
            files.update([module.binary_path(),module.BUILD])
        elif tool=='sparrow':
            files.update([module.BINARY,module.BUILD])
    return {p.relative_to(ROOT).as_posix():digest(p) for p in sorted(files)}


def create(name, settings_path):
    settings_path = settings_path.resolve(strict=True)
    if not settings_path.is_relative_to(ROOT):
        raise ValueError('Save session settings inside the repository for reproducible provenance')
    configs = json.loads(settings_path.read_bytes())
    if not configs or not set(configs).issubset(MODULES):
        raise ValueError('Select one or more supported comparison tools')
    roles = {'identical_constraints','best_native_settings'}
    for tool, variants in configs.items():
        if set(variants) != roles or variants['identical_constraints'] != 'identical' or any(v not in SETTINGS[tool] for v in variants.values()):
            raise ValueError(f'Invalid explicit settings roles for {tool}')
    plan = expected_plan()
    if plan != json.loads((ROOT/'benchmarks/matrix-plan.json').read_bytes()):
        raise ValueError('Coverage differs from the frozen plan')
    cases = {r['id']:r for r in plan['cases']}
    slots = []
    for row in schedule(plan,'development'):
        for tool in sorted(configs):
            if row['set']=='S' and tool!='sparrow': continue
            case = cases[row['job']]
            slot = {**row,'tool':tool,'settings':configs[tool][row['settings_role']],
                    'axis':'x' if row['set']=='S' else 'y','path':case['path'],'job_sha256':case['sha256']}
            slot['id'] = f'{len(slots):05d}'
            slots.append(slot)
    manifest = {'version':1,'kind':'development_comparison','name':name,
        'created_at':datetime.now(timezone.utc).isoformat(),'phase':'development',
        'scope':'Frozen development work queue only; settings are provisional, held-out jobs excluded. No final gate is established by this session.',
        'settings':configs,'sources':sources(configs,settings_path),'slots':slots}
    directory = session_dir(name)
    directory.mkdir(parents=True,exist_ok=False)
    write(directory/'manifest.json',manifest)
    print(json.dumps({'session':name,'slots':len(slots),'manifest':str(directory/'manifest.json')}))
    return manifest


def verify_sources(manifest):
    for name, checksum in manifest['sources'].items():
        if digest(contained_file(ROOT,name)) != checksum:
            raise ValueError(f'Frozen session input/code/binary changed: {name}')


def audit_result(slot, path, checksum):
    if not path.resolve().is_relative_to((ROOT/FOLDERS[slot['tool']]).resolve()):
        raise ValueError('Result is outside the selected tool evidence directory')
    run = importlib.import_module(AUDITORS[slot['tool']]).audit_record(path,checksum)
    tool = slot['tool']
    job_key, time_key = ('job_name','seconds_limit') if tool=='lbf' else ('job','seconds')
    if (run[job_key] != slot['job'] or run['job_sha256'] != slot['job_sha256']
            or run[time_key] != slot['seconds'] or run['seed'] != slot['seed']
            or run['settings'] != slot['settings'] or run.get('phase') != 'development'
            or (tool!='lbf' and run['axis'] != slot['axis'])):
        raise ValueError('Native attempt differs from its frozen slot')
    return run


def completed(directory, manifest):
    slots = {s['id']:s for s in manifest['slots']}
    rows = {}
    for path in sorted((directory/'attempts').glob('*/completed.json')):
        entry = json.loads(path.read_bytes())
        key = entry['slot_id']
        if key not in slots or key in rows or path.parent.name != key:
            raise ValueError('Unexpected or duplicate completed slot')
        start = json.loads((path.parent/'start.json').read_bytes())
        if start['slot'] != slots[key] or start['manifest_sha256'] != digest(directory/'manifest.json'):
            raise ValueError('Session manifest or original attempt changed')
        run = audit_result(slots[key],contained_file(ROOT,entry['record']),entry['sha256'])
        if entry['status'] != run['status']:
            raise ValueError('Saved slot status differs from the native record')
        rows[key] = entry
    return rows


def pending(directory, manifest, tool):
    done = completed(directory,manifest)
    rows = []
    for slot in manifest['slots']:
        if slot['tool'] != tool or slot['id'] in done: continue
        if (directory/'attempts'/slot['id']).exists():
            raise ValueError(f"Slot {slot['id']} was started without an audited completion; inspect its live process and evidence before any retry")
        rows.append(slot)
    return rows


def invoke(slot, name):
    module = importlib.import_module(MODULES[slot['tool']])
    path = ROOT/'benchmarks/datasets'/slot['path']
    if digest(path) != slot['job_sha256']:
        raise ValueError('Frozen job changed before native invocation')
    if slot['tool']=='lbf':
        run = module.run(path,slot['seconds'],slot['seed'],slot['settings'],batch_id=name,verbose=False,phase='development')
    else:
        run = module.run(argparse.Namespace(job=path,seconds=slot['seconds'],seed=slot['seed'],
            settings=slot['settings'],axis=slot['axis'],phase='development'))
    return ROOT/FOLDERS[slot['tool']]/run['run_id']/'run.json'


def execute(name, tool, limit):
    directory = session_dir(name)
    manifest = json.loads((directory/'manifest.json').read_bytes())
    verify_sources(manifest)
    if not 1 <= limit <= 30 or tool not in manifest['settings']:
        raise ValueError('Choose a configured tool and a limit of 1..30 attempts')
    selected = pending(directory,manifest,tool)[:limit]
    # Anode has a 30-minute hard lifetime; reserve three minutes of headroom.
    ceiling = 27*60 if tool=='deepnest' else 3*3600
    if sum(s['seconds']+400 for s in selected) > ceiling:
        raise ValueError('Requested chunk could exceed its bounded session; reduce --limit')
    # One process per session prevents duplicate work or concurrent app control.
    lock = directory/'active.lock'
    with lock.open('x',encoding='utf-8') as f:
        json.dump({'pid':os.getpid(),'tool':tool,'started_at':datetime.now(timezone.utc).isoformat()},f)
    try:
        for slot in selected:
            verify_sources(manifest)
            attempt = directory/'attempts'/slot['id']
            attempt.mkdir(parents=True,exist_ok=False)
            write(attempt/'start.json',{'slot':slot,'pid':os.getpid(),
                'started_at':datetime.now(timezone.utc).isoformat(),'manifest_sha256':digest(directory/'manifest.json')})
            result_path = invoke(slot,name)
            verify_sources(manifest)
            checksum = digest(result_path)
            run = audit_result(slot,result_path,checksum)
            entry = {'slot_id':slot['id'],'status':run['status'],
                     'record':result_path.relative_to(ROOT).as_posix(),'sha256':checksum}
            write(attempt/'completed.json',entry)
            print(json.dumps(entry),flush=True)
    finally:
        lock.unlink()


def progress(name):
    directory = session_dir(name)
    manifest = json.loads((directory/'manifest.json').read_bytes())
    rows = completed(directory,manifest)
    counts = {}
    for row in rows.values(): counts[row['status']] = counts.get(row['status'],0)+1
    print(json.dumps({'completed':len(rows),'required':len(manifest['slots']),'outcomes':counts,
                      'complete':len(rows)==len(manifest['slots']),'scope':manifest['scope']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    creating=sub.add_parser('create');creating.add_argument('--settings',type=Path,required=True)
    running=sub.add_parser('run');running.add_argument('--tool',choices=MODULES,required=True);running.add_argument('--limit',type=int,default=3)
    inspecting=sub.add_parser('progress')
    for item in [creating,running,inspecting]:item.add_argument('--name',required=True)
    args=parser.parse_args()
    if args.command=='create':create(args.name,args.settings)
    elif args.command=='run':execute(args.name,args.tool,args.limit)
    else:progress(args.name)
