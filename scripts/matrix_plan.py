"""Freeze job/seed coverage before Nestbolt optimisation tuning; no solver runs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'benchmarks/matrix-plan.json'
LONG_CASES = {
    'b-albano-nest-mb-free': 'Academic free rotation and large coordinates',
    'b-trousers-nest-mb-given': 'Academic constrained rotations and mixed irregular garment parts',
    'b-fu-strip-sheet': 'Fixed-sheet variant of a standard strip source',
    'b-jakobs2-strip-sheet': 'Larger repeated-copy strip-derived job',
    'b-shapes0-nest-mb-free': 'Academic high-copy free-rotation case',
    'b-swim-nest-mb-given': 'Detailed irregular academic contours',
    'm-box-mini': 'Finger-jointed flat-pack panels',
    'm-garment-teagan-2': 'Garment curves and grain rotations',
    'm-mechanical-defective-stock': 'Keep-out defects',
    'm-mechanical-mixed-stock': 'Mixed stock sizes and availability',
    'm-box-compact-2000': 'Held-out 2,000-copy scale test',
    'm-public-gear-6': 'Held-out public-source curved geometry',
}


def digest(path): return sha256(path.read_bytes()).hexdigest()


def expected():
    academic = ROOT/'benchmarks/datasets/academic.json'
    makers = ROOT/'benchmarks/datasets/makers.json'
    am, mm = json.loads(academic.read_bytes()), json.loads(makers.read_bytes())
    cases = []
    for row in am['instances'] + mm['instances']:
        path = row.get('path') or f"M/{row['id']}.json"
        checksum = row.get('sha256') or row['files'][path]
        if digest(ROOT/'benchmarks/datasets'/path) != checksum:
            raise ValueError('Dataset changed before schedule freeze')
        cases.append({'id':row['id'], 'set':row['set'], 'held_out':row['held_out'],
                      'path':path, 'sha256':checksum, 'part_count':row['part_count'],
                      'budgets_seconds':[60,300] if row['id'] in LONG_CASES else [60]})
    cases.sort(key=lambda r:r['id'])
    if len(cases)!=88 or len({r['id'] for r in cases})!=88:
        raise ValueError('Expected the complete 13 S, 35 B, 40 M freeze')
    if not set(LONG_CASES).issubset(r['id'] for r in cases):
        raise ValueError('Long-budget subset contains an unknown job')
    if {r['id'] for r in cases if r['held_out']} != set(mm['held_out_ids']):
        raise ValueError('Held-out reservations differ from the maker freeze')
    return {'version':1, 'frozen_on':'2026-10-11',
            'status':'job_and_seed_coverage_frozen_tool_settings_pending',
            'selection_basis':'Feature coverage; frozen after initial competitor pilots and before any Nestbolt search implementation/tuning. Held-out jobs have source checks only.',
            'generator_sha256':digest(Path(__file__)),
            'dataset_manifests':{'academic.json':digest(academic),'makers.json':digest(makers)},
            'seeds':{'development':[0,1,2], 'final':[1000,1001,1002,1003,1004]},
            'settings_roles':['identical_constraints','best_native_settings'],
            'settings_policy':'Exact per-tool configurations and any job-specific choices must be sealed before the acceptance run. Current provisional pilots are not the final settings freeze.',
            'long_budget_subset':[{'id':key,'reason':value} for key,value in LONG_CASES.items()],
            'cases':cases,
            'execution_policy':{'max_concurrent_runs':8,'workers_per_run':1,'session_limit_seconds':4*3600,
                                'separate_all_core_nestbolt_report':True,'held_out_development_runs':0},
            'score_policy':'Original-job independent validation is mandatory. Every selected attempt is retained; invalid/unsupported/timed-out runs have no fabricated score. Missing comparisons remain explicit and cannot silently count as a verified material reduction.'}


def schedule(plan, phase):
    if phase not in plan['seeds']: raise ValueError('Unknown phase')
    for row in plan['cases']:
        if phase=='development' and row['held_out']: continue
        for seconds in row['budgets_seconds']:
            for seed in plan['seeds'][phase]:
                for role in plan['settings_roles']:
                    yield {'job':row['id'],'set':row['set'],'held_out':row['held_out'],
                           'seconds':seconds,'seed':seed,'settings_role':role}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args(); plan=expected()
    if args.freeze:
        with DEST.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(plan,indent=2)+'\n')
    elif not DEST.exists() or json.loads(DEST.read_bytes())!=plan:
        raise SystemExit('Frozen matrix coverage differs; do not overwrite an existing acceptance schedule')
    print(json.dumps({'cases':len(plan['cases']),'long_budget_cases':len(plan['long_budget_subset']),
                      'development_slots_per_full_tool':len(list(schedule(plan,'development'))),
                      'final_slots_per_full_tool':len(list(schedule(plan,'final'))),
                      'note':'Coverage schedule only; runners/settings and gate completion remain separate.'}))
