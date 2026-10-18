"""Paired development pilot of provisional area-reducing assignment steps.

Four frozen H5 jobs, both kerfs, seeds 0-2 and matched 60-second wall budgets.
The isolated candidate retains the short exchange phase. The remaining original
relocation allowance may cross validated material-flat steps only when canonical
last-sheet filled area decreases. Steps stay provisional until strict whole-job
material reduction; incomplete sequences restore their saved layout and counts.
The original four-step cap, deadline, validation reserve and geometry guards
remain. 148 prior tests, one original-policy witness and seven new policy tests
must qualify first. This pilot cannot close H5 or establish a comparative claim.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
import os
from pathlib import Path
from queue import Queue
import shutil
import statistics
import subprocess
import time
import traceback
import zipfile

import psutil

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))

from cutting_development_set import ROOT, FOLDER, digest, load_cases, public_inputs
from h2_import_audit import source_digest
from h4_full_matrix import OVERRIDES, load, write
from h6_material_cost import run, equivalent, equivalent_common

PROBE = ROOT/'output/h5-assignment-bridge-probe-20261018'
CLI = PROBE/'public-checks/nestbolt-validator.exe'
ENGINES = {
    'normal': PROBE/'baseline-observer.exe',
    'baseline': PROBE/'baseline-observer.exe',
    'candidate': PROBE/'candidate-observer.exe',
}
JOBS = ['m-mechanical-large-plates', 'm-mechanical-panel-hardware', 'm-box-mini', 'c-bracket-mixed']
ARMS = ['normal', 'baseline', 'candidate']
SEEDS = [0, 1, 2]
KERFS = [0.2, 1.5]
CPUS = [0, 2, 4, 6, 8, 10, 12, 14]
H4 = ROOT/'benchmarks/results/h4-depth-reboot-recovery-20261016'


def tree_hash(folder):
    paths = sorted(p for p in folder.rglob('*') if p.is_file())
    return sha256(b''.join(p.relative_to(folder).as_posix().encode()+b'\0'+p.read_bytes() for p in paths)).hexdigest()


def guards():
    previous = ROOT/'benchmarks/results/h5-extended-repair-pilot-20261018'
    assert load(previous/'verification.json')['valid'] == 72
    require_runner_stopped(load(previous/'opened.json'), 'h5_extended_repair_pilot.py')
    paths = [Path(__file__), ROOT/'benchmarks/results/h5-boundary-pair-pilot-20261018/preflight-recovery/checks.json', ROOT/'scripts/test_h5_early_exchange_pilot.py',
             ROOT/'scripts/cutting_development_set.py', ROOT/'scripts/h6_material_cost.py',
             ROOT/'scripts/h4_full_matrix.py', FOLDER/'manifest.json', H4/'plan.json', ROOT/'benchmarks/results/h4-depth-recovered-scale-plan-20261016/plan.json', CLI,
             PROBE/'build.json', PROBE/'preparation.json', PROBE/'source-checks.json',
             PROBE/'public-checks/checks.json', ROOT/'benchmarks/results/h5-assignment-bridge-preparation-20261018/checks.json', *set(ENGINES.values())]
    paths.extend([ROOT/'benchmarks/results/h5-balanced-stage-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-balanced-exchange-witness-20261017/checks.json',
                  ROOT/'benchmarks/results/h5-return-capacity-diagnosis-20261017/verification.json',
                  ROOT/'benchmarks/results/h5-assignment-repack-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-assignment-repack-20261018/repeated-assignments.json',
                  ROOT/'benchmarks/results/h5-return-frame-pilot-20261017/verification.json',
                  ROOT/'benchmarks/results/h5-balanced-stage-20261018/observed-exchanges.json',
                  ROOT/'benchmarks/results/h5-balanced-stage-20261018/control-flow-review.json',
                  ROOT/'benchmarks/results/h5-post-exchange-fill-pilot-20261018/verification.json',
                  PROBE/'bridge-checks/checks.json', PROBE/'initial-geometry/checks.json', PROBE/'reconstruction.json',
                  ROOT/'benchmarks/results/h5-material-profile-preparation-20261018/profile-checks.json',
                  ROOT/'benchmarks/results/h5-frontier-observer-20261018/layout-checks.json',
                  ROOT/'benchmarks/results/h5-frontier-observer-20261018/source-review.json',
                  ROOT/'benchmarks/results/h5-boundary-observer-20261018/layout-checks.json',
                  ROOT/'benchmarks/results/h5-boundary-observer-20261018/source-review.json',
                  ROOT/'benchmarks/results/h5-exchange-failure-observer-20261018/failure-detail-checks.json',
                  ROOT/'benchmarks/results/h5-exchange-failure-observer-20261018/interpretation.json',
                  ROOT/'benchmarks/results/h5-productive-stage-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-productive-stage-20261018/source-review.json',
                  ROOT/'benchmarks/results/h5-mixed-exchange-witness-20261018/checks.json',
                  ROOT/'benchmarks/results/h5-mixed-stage-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-mixed-stage-20261018/source-review.json',
                  ROOT/'benchmarks/results/h5-larger-return-witness-20261018/checks.json',
                  ROOT/'benchmarks/results/h5-exact-state-20261018/layout-checks.json',
                  ROOT/'benchmarks/results/h5-exact-state-20261018/source-review.json',
                  ROOT/'benchmarks/results/h5-boundary-pair-pilot-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-boundary-pair-pilot-20261018/source-review.json',
                  ROOT/'benchmarks/results/h5-contained-return-pilot-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-contained-return-pilot-20261018/interpretation.json',
                  ROOT/'benchmarks/results/h5-free-return-pilot-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-free-return-observer-20261018/source-review.json',
                  ROOT/'benchmarks/results/h5-exchange-chain-pilot-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-continuous-repair-failure-20261018/checks.json',
                  ROOT/'benchmarks/results/h5-extended-repair-pilot-20261018/verification.json',
                  ROOT/'benchmarks/results/h5-extended-repair-pilot-20261018/interpretation.json',
                  ROOT/'benchmarks/results/h5-extended-repair-pilot-20261018/fixed-inventory-area.json'])
    paths.extend(ROOT/row['path'] for row, _ in load_cases())
    env = {name: os.environ.get(name) for name in OVERRIDES}
    assert all(value is None for value in env.values()), 'Experimental environment override is set'
    return {'production': source_digest(), 'environment': env,
            'baseline_source': tree_hash(PROBE/'baseline'),
            'candidate_source': tree_hash(PROBE/'candidate'),
            'files': {p.relative_to(ROOT).as_posix(): digest(p) for p in paths}}


def blocks():
    result = []
    for index, job in enumerate(JOBS):
        for ki, kerf in enumerate(KERFS):
            for seed in SEEDS:
                shift = (index+ki+seed) % len(ARMS)
                result.append({'job': job, 'kerf_mm': kerf, 'seed': seed,
                               'arm_order': ARMS[shift:]+ARMS[:shift]})
    return result


def summarize(records):
    expected = {(j, k, s, a) for j in JOBS for k in KERFS for s in SEEDS for a in ARMS}
    keys = [(r['job'], r['kerf_mm'], r['seed'], r['arm']) for r in records]
    coverage = len(keys) == len(expected) and len(set(keys)) == len(keys) and set(keys) == expected
    pairs = []
    for job in JOBS:
        for kerf in KERFS:
            pair = {'job': job, 'kerf_mm': kerf, 'arms': {}}
            for arm in ARMS:
                rows = [r for r in records if (r['job'], r['kerf_mm'], r['arm']) == (job, kerf, arm)]
                complete = len(rows) == 3 and sorted(r['seed'] for r in rows) == SEEDS
                complete = complete and all(r['status'] == 'valid' and isinstance(r.get('material'), (int, float))
                    and math.isfinite(r['material']) and r['material'] > 0 for r in rows)
                if arm != 'normal':
                    complete = complete and all(isinstance(r.get('saved_fraction'), (int, float))
                        and math.isfinite(r['saved_fraction']) and 0 <= r['saved_fraction'] <= 1 for r in rows)
                value = {'complete': complete, 'attempted': len(rows),
                         'failed': sum(r['status'] != 'valid' for r in rows)}
                if complete:
                    values = [r['material'] for r in rows]
                    q1, _, q3 = statistics.quantiles(values, n=4, method='inclusive')
                    value.update(material_median=statistics.median(values), material_q1=q1, material_q3=q3,
                        exchange_attempts=sum(r.get('stats', {}).get('directed_exchange_attempts', 0) for r in rows),
                        exchanges=sum(r.get('stats', {}).get('directed_exchanges', 0) for r in rows))
                    if arm != 'normal':
                        value['cut_savings_median_percent'] = 100*statistics.median(r['saved_fraction'] for r in rows)
                pair['arms'][arm] = value
            pair['complete'] = all(r['complete'] for r in pair['arms'].values())
            if pair['complete']:
                m = {a: r['material_median'] for a, r in pair['arms'].items()}
                pair.update(candidate_vs_baseline_percent=100*(m['candidate']/m['baseline']-1),
                    baseline_vs_normal_percent=100*(m['baseline']/m['normal']-1),
                    candidate_vs_normal_percent=100*(m['candidate']/m['normal']-1),
                    candidate_within_original_material_limit=m['candidate'] <= m['normal']*1.01)
                pair['per_seed'] = []
                for seed in SEEDS:
                    values = {r['arm']: r['material'] for r in records
                              if (r['job'], r['kerf_mm'], r['seed']) == (job, kerf, seed)}
                    pair['per_seed'].append({'seed': seed,
                        'candidate_vs_baseline_percent': 100*(values['candidate']/values['baseline']-1),
                        'candidate_vs_normal_percent': 100*(values['candidate']/values['normal']-1)})
            pairs.append(pair)
    return {'coverage_complete': coverage,
            'all_valid': coverage and all(p['complete'] for p in pairs),
            'pairs': pairs, 'H5_complete': False, 'automatic_integration_authorized_by_results': False}


def prepare(out):
    assert load(PROBE/'public-checks/checks.json')['all_checks_passed']
    assert load(PROBE/'build.json')['binaries']['baseline'] == digest(ENGINES['baseline'])
    assert load(PROBE/'build.json')['binaries']['candidate'] == digest(ENGINES['candidate'])
    assert digest(ENGINES['baseline']) != digest(ENGINES['candidate'])
    assert load(ROOT/'benchmarks/results/h5-assignment-bridge-preparation-20261018/checks.json')['all_functional_checks_pass']
    out.mkdir()
    plan = {'scope': __doc__, 'prepared_utc': datetime.now(timezone.utc).isoformat(),
        'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'guards': guards(), 'jobs': JOBS, 'kerfs_mm': KERFS, 'seeds': SEEDS, 'seconds': 60,
        'arms': {'normal': 'Unchanged preview, ordinary nesting at the same kerf spacing',
                 'baseline': 'Unchanged preview, common-line search bonus on',
                 'candidate': 'Isolated assignment-bridge candidate, common-line search bonus on'},
        'blocks': blocks(), 'attempts': 72, 'cpus': CPUS, 'concurrency': 8,
        'pairing': 'All three arms of a job/kerf/seed run sequentially on the same physical core; arm order rotates.',
        'geometry': 'Original frozen rings, quantities, stocks and rotations; only requested kerf spacing and common-line settings.',
        'search_external_timeout_seconds': 150, 'validation_export_timeout_seconds': 180,
        'revalidation_absolute_tolerance': 1e-9, 'whole_session_limit_seconds': 3600,
        'failed_attempts': 'Preserve all outcomes; any missing/duplicate/failed seed prevents a complete median and comparison.',
        'decision': 'Descriptive pilot only. Inspect material, cutting savings and exchange counters on every pair. Any invalid output precludes integration; H5 still requires the complete 13-job gate with unchanged thresholds.',
        'requires_completed_current_preview_and_scale_sequence': True,
        'original_unopened_pilot_preserved': 'benchmarks/results/h5-obstruction-set-pilot-20261016',
        'paired_case_blocks_summary_measurement_method_unchanged': True,
        'recovery_preserves_completed_current_outcomes': 402,
        'recovery_new_Firefox_outcomes': 201,
        'previous_failed_pilot': 'benchmarks/results/h5-extended-repair-pilot-20261018/results.json',
        'workflow_prerequisite': 'Wait until the current release matrix and conditional scale/export-check sequence finish. Preserve all failed H4/H5 outcomes; every gate limit is unchanged.',
        'held_out_geometry_read': False, 'H5_complete': False}
    write(out/'plan.json', plan)
    shutil.copyfile(__file__, out/'runner.py')
    print(json.dumps({'prepared': str(out), 'attempts': 72, 'measurement_started': False}), flush=True)


def case(row, job, block, arm, cpu, work, evidence, deadline):
    kerf, seed = block['kerf_mm'], block['seed']
    key = f"{row['id']}-k{kerf}-s{seed}-{arm}"
    folder = work/key
    folder.mkdir()
    record = {'job': row['id'], 'job_sha256': row['sha256'], 'kerf_mm': kerf, 'seed': seed,
              'arm': arm, 'cpu': cpu, 'seconds': 60, 'status': 'failed'}

    def bounded(seconds):
        remaining = deadline-time.perf_counter()
        assert remaining > 0, 'One-hour session cap reached; no new process started'
        return min(seconds, remaining)

    try:
        library, request = public_inputs(job, kerf, False)
        if arm == 'normal':
            request.pop('common_line')
        else:
            request['common_line']['search_bonus'] = True
        write(folder/'library.json', library)
        write(folder/'request.json', request)
        record['search'] = run([ENGINES[arm], folder/'library.json', folder/'request.json',
            folder/'nested', 60, seed, 'wall'], folder, 'search', cpu, bounded(150))
        assert record['search']['exit_code'] == 0, 'Search failed or timed out'
        search = load(folder/'nested/search.json')
        cutting = load(folder/'nested/cutting-report.json')
        expected = deepcopy(job)
        expected['clearance'] = kerf
        assert load(folder/'nested/job.json') == expected, 'Derived job changed beyond requested kerf'
        params = ['--library', folder/'library.json', '--request', folder/'request.json', '--layout', folder/'nested/layout.json']
        record['validation'] = run([CLI, 'validate', *params], folder, 'validate', cpu, bounded(180))
        assert record['validation']['exit_code'] == 0, 'Independent validation failed'
        checked = load(folder/'validate-stdout.json')
        assert checked['valid'] and search['validation']['valid'] and cutting['valid']
        layout = load(folder/'nested/layout.json')
        assert len(layout['placements']) == sum(p['quantity'] for p in job['parts'])
        delta = max(equivalent(checked['metrics'], search['validation']['metrics']),
                    equivalent(checked['metrics'], cutting['metrics']))
        if arm != 'normal':
            assert search['riders'] == 0, 'Common mode used a part hole'
            delta = max(delta, equivalent_common(checked['common_line'], cutting['common_line']))
            without = sum(r['cut_length_without_common_mm'] for r in checked['common_line'])
            with_common = sum(r['cut_length_with_common_mm'] for r in checked['common_line'])
            assert without > 0 and 0 <= with_common <= without
            record.update(cut_without_common_mm=without, cut_with_common_mm=with_common,
                          saved_fraction=1-with_common/without)
        record['export'] = run([CLI, 'export', *params, '--out-dir', folder/'export'], folder, 'export', cpu, bounded(180))
        assert record['export']['exit_code'] == 0, 'Public export failed'
        record.update(status='valid', material=checked['metrics']['normalized_material'], metrics=checked['metrics'],
            stats=search['stats'], history=search['history'], riders=search['riders'],
            elapsed_seconds=search['elapsed_seconds'], accepted_at_seconds=search['accepted_at_seconds'],
            layout_sha256=digest(folder/'nested/layout.json'), maximum_revalidation_difference=delta)
    except Exception:
        record['error'] = traceback.format_exc()
        record.pop('material', None)
    finally:
        record['artifacts'] = {p.relative_to(folder).as_posix(): digest(p) for p in sorted(folder.rglob('*')) if p.is_file()}
        write(folder/'case.json', record)
        archive = evidence/(key+'.zip')
        with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for path in sorted(folder.rglob('*')):
                if path.is_file():
                    z.write(path, path.relative_to(folder).as_posix())
        record.update(archive=archive.name, archive_sha256=digest(archive))
    return record


def require_runner_stopped(opened, runner):
    # A Windows PID is reusable. Establish identity before reading a command
    # line, which may be inaccessible for the unrelated replacement process.
    original_opened = datetime.fromisoformat(opened['utc']).timestamp()
    try:
        process = psutil.Process(opened['pid'])
        created = process.create_time()
        if created > original_opened:
            return {'pid': opened['pid'], 'state': 'reused_pid',
                    'original_opened': original_opened, 'current_created': created}
        arguments = process.cmdline()
    except psutil.NoSuchProcess:
        return {'pid': opened['pid'], 'state': 'absent'}
    assert not any(runner in arg for arg in arguments), 'Previous measurement runner is still active'
    return {'pid': opened['pid'], 'state': 'different_command', 'current_created': created}


def require_measurements_finished():
    diagnostic = ROOT/'benchmarks/results/h5-balanced-stage-20261018'
    assert load(diagnostic/'verification.json')['all_original_archives_verified']
    process_checks = [require_runner_stopped(load(diagnostic/'opened.json'), 'h5_balanced_stage.py')]
    import h4_preview_matrix as h4
    sequence = ROOT/'benchmarks/results/h4-depth-recovered-scale-plan-20261016'
    for folder, runner in [(H4, 'h4_depth_reboot_recovery.py'), (sequence, 'continue_recovered_depth_checks.py')]:
        process_checks.append(require_runner_stopped(load(folder/'opened.json'), runner))
        assert not (folder/'interruption.json').exists(), 'Review the original interrupted measurement first'
    terminal = sequence/('completed.json' if (sequence/'completed.json').exists() else 'stopped.json')
    state = load(terminal)
    assert all(stage['exit_code'] == 0 for stage in state['stages'])
    assert load(H4/'results.json')['guards_unchanged']
    verification = load(H4/'verification.json')
    assert verification['all_artifact_checks_passed']
    assert verification['completed_current_build_outcomes'] == 603
    assert verification['retained_current_build_outcomes'] == 402 and verification['new_recovery_outcomes'] == 201
    assert verification['original_infrastructure_interruption_preserved']
    assert verification['frozen_v1_outcomes'] == 195
    if terminal.name == 'completed.json':
        fidelity = load(sequence/'curve-export-fidelity/verification.json')
        assert fidelity['all_checks_pass'] and fidelity['both_scale_workflows_pass']
        for kind in ['curves','g5']:
            scale = load(ROOT/fidelity[kind]/'summary.json')
            assert scale['passes'] and scale['source_guards_passed']
            assert scale['archive']['crc_and_member_hashes_verified']
            assert digest(ROOT/fidelity[kind]/'raw.zip') == scale['archive']['sha256']
        visual = load(sequence/'visual-review.json')
        assert visual['reviewed'] and len(visual['screenshots']) == 4
        assert all(r['reviewed'] and digest(ROOT/r['path'])==r['sha256'] for r in visual['screenshots'])
    inventory = load(H4/'integrity.json')
    assert inventory['crc_and_every_member_verified'] and digest(H4/'raw.zip') == inventory['sha256']
    rows, _, _ = h4.cases()
    assert h4.guards(rows) == load(H4/'plan.json')['guards']
    paths = [H4/'results.json', H4/'verification.json', H4/'integrity.json', sequence/'plan.json', terminal]
    return {path.relative_to(ROOT).as_posix(): digest(path) for path in paths} | {'process_identity_checks': process_checks}


def measure(out):
    plan = load(out/'plan.json')
    assert guards() == plan['guards']
    assert subprocess.check_output(['git', 'show', 'HEAD:'+(out/'plan.json').relative_to(ROOT).as_posix()], cwd=ROOT) == (out/'plan.json').read_bytes(), 'Commit plan before measuring'
    prerequisites = require_measurements_finished()
    with (out/'opened.json').open('x', encoding='utf-8') as stream:
        json.dump({'pid': os.getpid(), 'utc': datetime.now(timezone.utc).isoformat(),
                   'plan_sha256': digest(out/'plan.json'), 'prerequisites': prerequisites}, stream, indent=2)
    work = ROOT/'output'/out.name
    work.mkdir()
    known = {row['id']: (row, job) for row, job in load_cases()}
    cpus = Queue()
    for cpu in CPUS:
        cpus.put(cpu)
    records = []
    started = time.perf_counter()

    def block_run(block):
        cpu = cpus.get()
        try:
            row, job = known[block['job']]
            return [case(row, job, block, arm, cpu, work, out, started+3600) for arm in block['arm_order']]
        finally:
            cpus.put(cpu)

    try:
        with ThreadPoolExecutor(8) as pool:
            futures = [pool.submit(block_run, block) for block in plan['blocks']]
            for future in as_completed(futures):
                records.extend(future.result())
                write(out/'progress.json', records)
                print(json.dumps({'done': len(records), 'valid': sum(r['status'] == 'valid' for r in records)}), flush=True)
        assert guards() == plan['guards'], 'Sources/engines/inputs changed during measurement'
        records.sort(key=lambda r: (r['job'], r['kerf_mm'], r['seed'], r['arm']))
        result = {'records': records, 'summary': summarize(records), 'guards_unchanged': True,
                  'wall_seconds': time.perf_counter()-started, 'finished_utc': datetime.now(timezone.utc).isoformat()}
        write(out/'results.json', result)
        print(json.dumps({'completed': str(out), 'all_valid': result['summary']['all_valid'], 'H5_complete': False}), flush=True)
    except BaseException:
        write(out/'interruption.json', {'error': traceback.format_exc(), 'wall_seconds': time.perf_counter()-started})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    assert out.parent == ROOT/'benchmarks/results'
    psutil.Process().cpu_affinity(list(range(16, 32)))
    if args.action == 'prepare':
        prepare(out)
    else:
        measure(out)
