"""The M1 target must not reward failed competitors or partial coverage."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from baseline_gap import audit_table, build_gap, digest, SETTINGS
from comparison_session_report import summarize


def fixture():
    plan = {'seeds': {'development': [0, 1, 2]}, 'cases': [
        {'id': 'example', 'set': 'B', 'held_out': False, 'budgets_seconds': [60, 300]}]}
    rows = []
    for seconds in [60, 300]:
        for tool, best in SETTINGS.items():
            for role, setting in [('identical_constraints', 'identical'), ('best_native_settings', best)]:
                rows.append({'tool': tool, 'job': 'example', 'seconds': seconds, 'axis': 'y',
                             'settings_role': role, 'settings': setting, 'required_seeds': [0, 1, 2],
                             'required': 3, 'completed': 3, 'outcomes': {'valid': 3, 'missing': 0},
                             'comparable_median': True,
                             'comparison_statistics': {'median': {'state': 'finite',
                                 'value': 100 if tool == 'lbf' else 80 if seconds == 60 else 70}}})
    return plan, rows


def failed(row):
    row.update(outcomes={'no_layout': 3, 'missing': 0}, comparable_median=False,
               comparison_statistics={'median': {'state': 'failed', 'value': None}})


class GapTests(unittest.TestCase):
    def test_audit_recomputes_statistics_and_rejects_relabelled_attempts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root/'benchmarks/datasets/job.json'
            source.parent.mkdir(parents=True)
            source.write_text('{}', encoding='utf-8')
            checksum = digest(source)
            plan = {'seeds': {'development': [0, 1, 2]}, 'cases': [
                {'id': 'example', 'set': 'B', 'path': 'job.json', 'sha256': checksum,
                 'held_out': False, 'budgets_seconds': [60]}]}
            slots, runs, attempts = [], {}, []
            for seed in range(3):
                slot_id = str(seed)
                slots.append({'id': slot_id, 'tool': 'lbf', 'job': 'example', 'seconds': 60,
                              'settings_role': 'identical_constraints', 'settings': 'identical',
                              'axis': 'y', 'seed': seed})
                run = {'job_name': 'example', 'seed': seed, 'seconds_limit': 60,
                       'settings': 'identical', 'job_sha256': checksum, 'status': 'valid',
                       'metrics': {'normalized_material': 10 + seed}}
                record = root/f'run-{seed}.json'
                record.write_text(json.dumps(run), encoding='utf-8')
                attempts.append({'slot_id': slot_id, 'record': record.name, 'sha256': digest(record),
                                 'run': run, 'status': 'valid'})
                runs[slot_id] = run
            table = {'rows': summarize(slots, runs), 'attempts': attempts}
            path = root/'table.json'
            def audit(path, checksum):
                self.assertEqual(digest(path), checksum)
                return json.loads(path.read_bytes())
            with patch('baseline_gap.ROOT', root), patch('baseline_gap.audit_lbf', audit):
                path.write_text(json.dumps(table), encoding='utf-8')
                self.assertEqual(audit_table(path, plan), table['rows'])
                changed = deepcopy(table)
                changed['rows'][0]['comparison_statistics']['median']['value'] = 1
                path.write_text(json.dumps(changed), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'statistics differ'):
                    audit_table(path, plan)
                changed = deepcopy(table)
                changed['rows'][0]['settings'] = 'upstream-default'
                path.write_text(json.dumps(changed), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'differs from table slot'):
                    audit_table(path, plan)

    def test_half_larger_gap_uses_lbf_denominator_and_best_finite_settings(self):
        plan, rows = fixture()
        result = build_gap(plan, rows)
        self.assertTrue(result['complete'])
        self.assertAlmostEqual(result['target_percent'], 15)
        self.assertAlmostEqual(result['budgets'][0]['gap_percent'], 20)
        self.assertAlmostEqual(result['budgets'][1]['gap_percent'], 30)

    def test_missing_other_setting_blocks_target_even_with_finite_competitor(self):
        plan, rows = fixture()
        result = build_gap(plan, rows[:-1])
        self.assertFalse(result['complete'])
        self.assertIsNone(result['target_percent'])
        self.assertIsNone(result['budgets'][1]['gap_percent'])
        self.assertEqual(result['rows'][1]['state'], 'incomplete')
        rows[-1]['completed'] = 2
        rows[-1]['outcomes'] = {'valid': 2, 'missing': 1}
        self.assertFalse(build_gap(plan, rows)['complete'])

    def test_failed_competitors_are_separate_not_free_wins(self):
        plan, rows = fixture()
        extra_case = deepcopy(plan['cases'][0])
        extra_case['id'] = 'no-comparison'
        plan['cases'].append(extra_case)
        extra_rows = deepcopy(rows)
        for row in extra_rows:
            row['job'] = 'no-comparison'
            if row['tool'] != 'lbf':
                failed(row)
        result = build_gap(plan, rows + extra_rows)
        self.assertTrue(result['complete'])
        self.assertAlmostEqual(result['target_percent'], 15)
        for budget in result['budgets']:
            self.assertEqual(budget['jobs'], 2)
            self.assertEqual(budget['paired_jobs'], 1)
            self.assertEqual(budget['states']['no_finite_competitor'], 1)
        self.assertIsNone(result['rows'][2]['gap_percent'])

    def test_no_lbf_or_no_pairs_cannot_freeze_a_target(self):
        plan, rows = fixture()
        for row in rows:
            if row['tool'] == 'lbf':
                failed(row)
        result = build_gap(plan, rows)
        self.assertFalse(result['complete'])
        self.assertIsNone(result['target_percent'])
        self.assertEqual(result['rows'][0]['state'], 'no_finite_lbf')

    def test_five_percent_floor_and_duplicate_or_unexpected_groups(self):
        plan, rows = fixture()
        for row in rows:
            row['comparison_statistics']['median']['value'] = 100
        self.assertEqual(build_gap(plan, rows)['target_percent'], 5)
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            build_gap(plan, rows + [rows[0]])
        rows[0]['settings'] = 'undeclared'
        with self.assertRaisesRegex(ValueError, 'Unexpected'):
            build_gap(plan, rows)

    def test_held_out_cases_never_enter_gap_and_cannot_supply_scores(self):
        plan, rows = fixture()
        case = deepcopy(plan['cases'][0])
        case.update(id='reserved', held_out=True)
        plan['cases'].append(case)
        self.assertEqual(build_gap(plan, rows)['budgets'][0]['jobs'], 1)
        extra = deepcopy(rows[0])
        extra['job'] = 'reserved'
        with self.assertRaisesRegex(ValueError, 'Unexpected'):
            build_gap(plan, rows + [extra])


if __name__ == '__main__':
    unittest.main()
