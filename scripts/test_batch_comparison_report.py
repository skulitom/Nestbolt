"""A selected batch slice must preserve failures, coverage and unique attempts."""
from copy import deepcopy
import unittest
from batch_comparison_report import combine, split_build_failures, infrastructure_failure_kind
from comparison_cases import comparison_cases
from pathlib import Path


class BatchTests(unittest.TestCase):
    def test_legacy_exact_coordinate_guard_can_be_replaced_only_before_solving(self):
        run = {'tool': 'SVGnest', 'status': 'failed', 'score': None, 'seconds': 60}
        raw = {'status': 'failed', 'errors': ['Error: page.evaluate: Error: Source coordinate rounded during import: copy-0/67/1'],
               'candidates': 0, 'last': None}
        self.assertEqual(infrastructure_failure_kind(run, raw), 'exact_coordinate_guard_before_solve')
        for change in [{'candidates': 1}, {'last': {'elapsed_ms': 100}}, {'controller_solve_ms': 1},
                       {'errors': ['solver crashed']}, {'status': 'completed'}]:
            with self.assertRaises(ValueError):
                infrastructure_failure_kind(run, {**raw, **change})

    def test_native_infrastructure_replacement_cannot_hide_solver_failures(self):
        run = {'tool': 'deepnest-next', 'status': 'failed', 'score': None, 'seconds': 60}
        cleanup = {'status': 'failed', 'errors': ['Error: Command failed: taskkill /PID 123 /T /F'],
                   'stages_ms': {'budget_finished': 61000}, 'controller_solve_ms': 60001,
                   'candidates': 1, 'last': {'elapsed_ms': 59000}}
        self.assertEqual(infrastructure_failure_kind(run, cleanup), 'cleanup_after_budget')
        before = {'status': 'failed', 'errors': ['Error: Command failed: powershell.exe -NoProfile -NonInteractive -File cpu-tree-job.ps1 Access is denied Win32Exception,cpu-tree-job.ps1'],
                  'stages_ms': {'source_imported': 1000}, 'candidates': 0, 'last': None}
        self.assertEqual(infrastructure_failure_kind(run, before), 'affinity_before_solve')
        for field, value in [('status', 'invalid'), ('status', 'timeout'), ('status', 'no_layout'),
                             ('score', 1), ('metrics', {}), ('tool', 'svgnest')]:
            with self.assertRaises(ValueError):
                infrastructure_failure_kind({**run, field: value}, cleanup)
        for raw in [
            {**cleanup, 'errors': ['native solver crashed']},
            {**cleanup, 'errors': cleanup['errors'] + ['another error']},
            {**cleanup, 'stages_ms': {}}, {**cleanup, 'controller_solve_ms': 100},
            {**cleanup, 'last': {'elapsed_ms': 60001}},
            {**before, 'controller_solve_ms': 1}, {**before, 'candidates': 1},
            {**before, 'stages_ms': {'source_imported': 1000, 'budget_finished': 61000}},
        ]:
            with self.assertRaises(ValueError):
                infrastructure_failure_kind(run, raw)

    def test_replacements_cannot_hide_solver_failures_or_scores(self):
        failed = {'run': {'status': 'failed', 'score': None,
                         'reason': "Command '['cargo', 'build', '-p', 'nestbolt-cli', '--locked']' returned non-zero exit status 101.",
                         'outputs': {'job.json': 'hash', 'request.json': 'hash', 'input.svg': 'hash', 'input-0.svg': 'hash'}}}
        invalid = {'run': {'status': 'invalid', 'score': None}}
        retained, excluded = split_build_failures([failed, invalid])
        self.assertEqual(retained, [invalid])
        self.assertEqual(excluded, [failed])
        for field, value in [('score', 1), ('exit_code', 0), ('reason', 'solver crashed'),
                             ('outputs', {'browser-result.json': 'hash'})]:
            changed = deepcopy(failed)
            changed['run'][field] = value
            with self.assertRaisesRegex(ValueError, 'unstarted'):
                split_build_failures([changed])

    def test_long_budget_population_preserves_frozen_subset_and_excludes_held_out(self):
        root = Path(__file__).resolve().parents[1]
        selected = {group: comparison_cases(root, group, 300)[1] for group in ['S', 'B', 'M']}
        self.assertEqual({group: len(rows) for group, rows in selected.items()}, {'S': 0, 'B': 6, 'M': 4})
        self.assertFalse(any(row['held_out'] for rows in selected.values() for row in rows))
        self.assertEqual({row['id'] for row in selected['M']}, {
            'm-box-mini', 'm-garment-teagan-2', 'm-mechanical-defective-stock', 'm-mechanical-mixed-stock'})
        self.assertEqual(len(comparison_cases(root, 'M', 60)[1]), 30)
        with self.assertRaises(ValueError):
            comparison_cases(root, 'M', 120)

    def setUp(self):
        self.cases = [{'id': 'b-test', 'sha256': 'frozen'}]
        self.batch = {'dataset': 'B', 'seconds': 60, 'settings': 'identical', 'axis': 'y'}
        self.rows = [{'run': {'job': 'b-test', 'job_sha256': 'frozen', 'seed': seed,
                             'phase': 'development', 'revision': 'same', 'status': status, 'score': score}}
                     for seed, status, score in [(0, 'valid', 1), (1, 'valid', 2), (2, 'invalid', None)]]

    def aggregate(self, rows=None, batch=None):
        return combine('svgnest', 'B', 60, 'identical', self.cases,
                       [(batch or self.batch, self.rows if rows is None else rows)])[2][0]

    def test_failed_seed_participates_and_missing_seed_blocks(self):
        row = self.aggregate()
        self.assertEqual(row['comparison_statistics']['median'], {'state': 'finite', 'value': 2})
        self.assertEqual(row['comparison_statistics']['quartiles'][2]['state'], 'failed')
        self.assertEqual(self.aggregate(self.rows[:2])['comparison_statistics']['median']['state'], 'incomplete')

    def test_duplicate_and_foreign_attempts_cannot_be_selected_by_score(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.aggregate(self.rows + self.rows[:1])
        for field, value in [('job', 'held-out'), ('seed', 1000), ('job_sha256', 'changed'), ('phase', 'final')]:
            rows = deepcopy(self.rows)
            rows[0]['run'][field] = value
            with self.assertRaises(ValueError):
                self.aggregate(rows)

    def test_other_axis_and_upstream_versions_cannot_share_a_table(self):
        with self.assertRaisesRegex(ValueError, 'axis'):
            self.aggregate(batch={**self.batch, 'axis': 'x'})
        rows = deepcopy(self.rows)
        rows[0]['run']['revision'] = 'other'
        with self.assertRaisesRegex(ValueError, 'versions'):
            self.aggregate(rows)


if __name__ == '__main__':
    unittest.main()
