"""Derive a separate pilot for the early call point; retain previous pilots."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root/'scripts/h5_exchange_pilot_v2.py').read_text(encoding='utf-8')
end = source.index('"""', 3)+3
source = '''"""Paired development pilot for the isolated early-exchange candidate.

Current 7eba929 baseline and candidate share the finer exact-score bound.
Four frozen H5 jobs, both kerfs, seeds 0-2 and matched 60-second wall budgets.
The candidate changes only the experimental exchange call point, alongside its
retained guards. The earlier failed pilot is never replaced or rescored.
Wait for the active release matrix and its conditional scale sequence to finish,
regardless of their quality outcome. This pilot cannot close H5 or justify a
public comparative claim. No measured work may overlap the release checks.
"""''' + source[end:]
replacements = [
    ("ROOT/'output/h5-exchange-probe'", "ROOT/'output/h5-early-exchange-probe'"),
    ("PROBE/'nestbolt-baseline.exe'", "PROBE/'public-checks-v1/nestbolt-validator.exe'"),
    ('nestbolt-baseline-exchange-observer.exe', 'nestbolt-baseline-observer.exe'),
    ('nestbolt-candidate-exchange-observer-v2.exe', 'nestbolt-candidate-observer.exe'),
    ('test_h5_exchange_pilot.py', 'test_h5_early_exchange_pilot.py'),
    ('h4-preview-development-20261016', 'h4-preview-score-release-20261016'),
    ('observer-build-baseline-v1.json', 'baseline-observer-build.json'),
    ('observer-build-candidate-v2.json', 'candidate-observer-build.json'),
    ('observer-checks-v1.json', 'public-checks-v1/checks.json'),
    ("['all_checks_pass']", "['all_checks_passed']"),
    ("tree_hash(PROBE/'baseline-workspace')", "tree_hash(PROBE/'baseline')"),
    ("tree_hash(PROBE/'workspace')", "tree_hash(PROBE/'candidate')"),
    ('Isolated exchange candidate, common-line search bonus on', 'Isolated early-exchange candidate, common-line search bonus on'),
    ("'requires_completed_sealed_original_preview_and_chunks_probe': True,", "'requires_completed_current_preview_and_scale_sequence': True,"),
    ("'supersedes_unopened_plan': 'benchmarks/results/h5-exchange-pilot-20261016/plan.json',", "'previous_failed_pilot': 'benchmarks/results/h5-exchange-pilot-v2-20261016/results.json',"),
    ("'workflow_prerequisite_change_only': 'Wait for completed measurements, not a passing unrelated gate; H4 remains failed and every H5 limit is unchanged.',", "'workflow_prerequisite': 'Wait until the current release matrix and conditional scale sequence finish. Preserve all failed H4/H5 outcomes; every gate limit is unchanged.',"),
]
for before, after in replacements:
    assert before in source, before
    source = source.replace(before, after)
source = source.replace("    out.mkdir()\n    plan =", "    assert load(ROOT/'benchmarks/results/h5-early-exchange-preparation-20261016/checks.json')['all_functional_checks_pass']\n    out.mkdir()\n    plan =")
source = source.replace("PROBE/'public-checks-v1/checks.json', *set(ENGINES.values())]", "PROBE/'public-checks-v1/checks.json', ROOT/'benchmarks/results/h5-early-exchange-preparation-20261016/checks.json', *set(ENGINES.values())]")
start = source.index('def require_measurements_finished():')
end = source.index('\ndef measure(out):', start)
source = source[:start] + '''def require_measurements_finished():
    import h4_preview_matrix as h4
    sequence = ROOT/'benchmarks/results/h4-preview-score-scale-plan-20261016'
    for folder, runner in [(H4, 'h4_preview_matrix.py'), (sequence, 'continue_preview_score_checks.py')]:
        opened = load(folder/'opened.json')
        try:
            arguments = psutil.Process(opened['pid']).cmdline()
        except psutil.NoSuchProcess:
            arguments = []
        assert not any(runner in arg for arg in arguments), 'Release measurements are still running'
        assert not (folder/'interruption.json').exists(), 'Review the original interrupted measurement first'
    terminal = sequence/('completed.json' if (sequence/'completed.json').exists() else 'stopped.json')
    state = load(terminal)
    assert all(stage['exit_code'] == 0 for stage in state['stages'])
    assert load(H4/'results.json')['guards_unchanged']
    verification = load(H4/'verification.json')
    assert verification['all_artifact_checks_passed'] and verification['new_attempts'] == 603
    inventory = load(H4/'integrity.json')
    assert inventory['crc_and_every_member_verified'] and digest(H4/'raw.zip') == inventory['sha256']
    rows, _, _ = h4.cases()
    assert h4.guards(rows) == load(H4/'plan.json')['guards']
    paths = [H4/'results.json', H4/'verification.json', H4/'integrity.json', sequence/'plan.json', terminal]
    return {path.relative_to(ROOT).as_posix(): digest(path) for path in paths}

''' + source[end:]
target = root/'scripts/h5_early_exchange_pilot.py'
assert not target.exists()
compile(source, str(target), 'exec')
target.write_text(source, encoding='utf-8', newline='\n')
test = (root/'scripts/test_h5_exchange_pilot.py').read_text(encoding='utf-8')
assert 'import h5_exchange_pilot as pilot' in test
test = test.replace('import h5_exchange_pilot as pilot', 'import h5_early_exchange_pilot as pilot')
test = test.replace('    def test_original_material_failures', '''    def test_active_release_measurement_prevents_opening_this_pilot(self):
        with patch.object(pilot, 'load', return_value={'pid': 100}), patch.object(pilot.psutil, 'Process') as process:
            process.return_value.cmdline.return_value = ['python', 'h4_preview_matrix.py', 'run']
            with self.assertRaisesRegex(AssertionError, 'Release measurements are still running'):
                pilot.require_measurements_finished()

    def test_engines_are_current_separate_workspaces(self):
        self.assertEqual(pilot.ENGINES['normal'], pilot.ENGINES['baseline'])
        self.assertNotEqual(pilot.ENGINES['baseline'], pilot.ENGINES['candidate'])
        self.assertEqual(pilot.PROBE.name, 'h5-early-exchange-probe')
        self.assertEqual(pilot.H4.name, 'h4-preview-score-release-20261016')

    def test_original_material_failures''')
target = root/'scripts/test_h5_early_exchange_pilot.py'
assert not target.exists()
compile(test, str(target), 'exec')
target.write_text(test, encoding='utf-8', newline='\n')
print('Prepared the new runner and seven harness checks; no pilot opened.')
