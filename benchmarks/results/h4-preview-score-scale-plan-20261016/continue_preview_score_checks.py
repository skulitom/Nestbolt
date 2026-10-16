"""Finish the active matrix, then run its fixed scale checks only if it passes."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys
import time
import traceback
import psutil

root = Path(__file__).resolve().parents[1]
out = root/'benchmarks/results/h4-preview-score-scale-plan-20261016'
matrix = root/'benchmarks/results/h4-preview-score-release-20261016'
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()
def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')

if sys.argv[1:] == ['prepare']:
    out.mkdir(exist_ok=False)
    sys.path.insert(0, str(root/'scripts'))
    import h4_scale
    plan = {
        'scope': __doc__, 'candidate': '7eba929420d218d04169c1fdf24481051c8afae5',
        'matrix_directory': matrix.relative_to(root).as_posix(),
        'matrix_plan_sha256': digest(matrix/'plan.json'),
        'matrix_opened': load(matrix/'opened.json'),
        'scale_guards': {fixture: h4_scale.guards(fixture=fixture) for fixture in ['curves', 'g5']},
        'limits': {'peak_RSS_and_private_bytes': 1500000000, 'heartbeat_ms': 200,
                   'Long_Tasks_ms_when_available': 200, 'parts': 2000, 'search_seconds': 60},
        'commands': [
            ['python', 'output/finalize_h4_preview_score_release.py'],
            ['python', 'output/report_h4_preview_score_release.py'],
            ['python', 'scripts/h4_scale.py', '--quick-start'],
            ['python', 'scripts/h4_scale.py', '--fixture', 'g5'],
        ],
        'helpers': {name: digest(root/name) for name in ['output/continue_preview_score_checks.py',
            'output/finalize_h4_preview_score_release.py', 'output/report_h4_preview_score_release.py']},
        'method': 'Keep existing fixture, automatic workers, Chrome/Firefox, runner, physical CCD0 0/2 and independent validation on 4. Curves quick-start on, G5 off. Sequential, no repeated outcome or threshold change.',
        'exclusive_measurements_until_complete': True,
        'source_and_root_build_freeze_until_complete': True,
        'held_out_geometry_read': False,
        'quality_failure_behavior': 'Preserve and report the original full matrix; do not run scale or publish.',
    }
    write(out/'plan.json', plan)
    (out/'runner.py').write_bytes(Path(__file__).read_bytes())
    print('Prepared conditional scale sequence; no additional measurement started.')
    raise SystemExit(0)

assert sys.argv[1:] == ['run']
assert not (out/'opened.json').exists()
plan = load(out/'plan.json')
assert subprocess.check_output(['git','show','HEAD:'+str((out/'plan.json').relative_to(root)).replace('\\','/')], cwd=root) == (out/'plan.json').read_bytes()
assert digest(matrix/'plan.json') == plan['matrix_plan_sha256']
assert all(digest(root/name) == expected for name, expected in plan['helpers'].items())
psutil.Process().cpu_affinity(list(range(16,32)))
write(out/'opened.json', {'pid': psutil.Process().pid, 'utc': datetime.now(timezone.utc).isoformat(), 'plan_sha256': digest(out/'plan.json')})
stages = []
try:
    expires = time.monotonic() + 4*60*60
    while True:
        assert not (matrix/'interruption.json').exists(), 'Original matrix interruption retained; investigate it'
        pid = plan['matrix_opened']['pid']
        try:
            active = any('h4_preview_matrix.py' in arg for arg in psutil.Process(pid).cmdline())
        except psutil.NoSuchProcess:
            active = False
        if not active:
            assert (matrix/'results.json').exists(), 'Matrix stopped without complete results'
            break
        assert time.monotonic() < expires, 'Conditional wait expired without changing the running matrix'
        time.sleep(10)
    for index, command in enumerate(plan['commands']):
        if index == 2:
            if not load(matrix/'results.json')['all_quality_checks_pass']:
                write(out/'stopped.json', {'reason': 'Current full quality comparison failed; no scale measurements started', 'stages': stages})
                print('Current quality condition failed; raw evidence sealed, scale not started.', flush=True)
                raise SystemExit(0)
        if index >= 2:
            sys.path.insert(0, str(root/'scripts'))
            import h4_scale
            fixture = 'curves' if index == 2 else 'g5'
            assert h4_scale.guards(fixture=fixture) == plan['scale_guards'][fixture]
        log = out/f'stage-{index}.log'
        assert not log.exists()
        started = datetime.now(timezone.utc).isoformat()
        with log.open('wb') as stream:
            completed = subprocess.run([sys.executable, str(root/'output/ccd1.py'), *command],
                cwd=root, stdout=stream, stderr=subprocess.STDOUT, timeout=3900)
        stage = {'index': index, 'command': command, 'started': started,
            'finished': datetime.now(timezone.utc).isoformat(), 'exit_code': completed.returncode,
            'log_sha256': digest(log)}
        stages.append(stage)
        write(out/'progress.json', stages)
        print(json.dumps(stage), flush=True)
        assert completed.returncode == 0, 'Preserve original stage failure; no automatic rerun'
    write(out/'completed.json', {'stages': stages, 'scale_outcomes_need_review': True,
          'milestone_closed': False, 'release_created': False})
except SystemExit:
    raise
except BaseException:
    write(out/'interruption.json', {'error': traceback.format_exc(), 'stages': stages})
    raise
