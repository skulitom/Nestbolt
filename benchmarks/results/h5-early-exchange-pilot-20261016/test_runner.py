"""A failed or incomplete pilot must not become a passing median."""
from copy import deepcopy
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
import zipfile

import h5_early_exchange_pilot as pilot


def records():
    return [{'job': j, 'kerf_mm': k, 'seed': s, 'arm': a, 'status': 'valid',
             'material': {'normal': 1.0, 'baseline': 1.06, 'candidate': 1.02}[a],
             'saved_fraction': 0.15, 'stats': {'directed_exchanges': int(a == 'candidate')}}
            for j in pilot.JOBS for k in pilot.KERFS for s in pilot.SEEDS for a in pilot.ARMS]


class PilotSummaryTests(unittest.TestCase):
    def test_active_release_measurement_prevents_opening_this_pilot(self):
        with patch.object(pilot, 'load', return_value={'pid': 100}), patch.object(pilot.psutil, 'Process') as process:
            process.return_value.cmdline.return_value = ['python', 'h4_preview_matrix.py', 'run']
            with self.assertRaisesRegex(AssertionError, 'Release measurements are still running'):
                pilot.require_measurements_finished()

    def test_engines_are_current_separate_workspaces(self):
        self.assertEqual(pilot.ENGINES['normal'], pilot.ENGINES['baseline'])
        self.assertNotEqual(pilot.ENGINES['baseline'], pilot.ENGINES['candidate'])
        self.assertEqual(pilot.PROBE.name, 'h5-early-exchange-probe')
        self.assertEqual(pilot.H4.name, 'h4-preview-score-release-20261016')

    def test_original_material_failures_stay_failures_despite_improvement(self):
        result = pilot.summarize(records())
        self.assertTrue(result['all_valid'])
        self.assertFalse(result['H5_complete'])
        for pair in result['pairs']:
            self.assertLess(pair['candidate_vs_baseline_percent'], 0)
            self.assertAlmostEqual(pair['candidate_vs_normal_percent'], 2.0)
            self.assertFalse(pair['candidate_within_original_material_limit'])
            self.assertEqual(pair['arms']['candidate']['exchanges'], 3)

    def test_missing_duplicate_and_failed_seeds_never_get_complete_comparison(self):
        complete = records()
        for rows in [complete[1:], complete+[deepcopy(complete[0])]]:
            summary = pilot.summarize(rows)
            self.assertFalse(summary['coverage_complete'])
            self.assertFalse(summary['all_valid'])
            self.assertNotIn('candidate_vs_normal_percent', summary['pairs'][0])
        complete[0]['status'] = 'failed'
        summary = pilot.summarize(complete)
        self.assertTrue(summary['coverage_complete'])
        self.assertFalse(summary['all_valid'])
        self.assertNotIn('material_median', summary['pairs'][0]['arms']['normal'])

    def test_nonfinite_invalid_scores_and_missing_cut_savings_are_not_scored(self):
        for value in [None, float('inf'), float('nan'), -1.0, 0.0]:
            rows = records()
            rows[0]['material'] = value
            self.assertFalse(pilot.summarize(rows)['all_valid'])
        rows = records()
        rows[1].pop('saved_fraction')
        self.assertFalse(pilot.summarize(rows)['all_valid'])

    def test_each_block_keeps_all_arms_and_balances_order_across_seeds(self):
        blocks = pilot.blocks()
        self.assertEqual(len(blocks), 24)
        for job in pilot.JOBS:
            for kerf in pilot.KERFS:
                subset = [b for b in blocks if (b['job'], b['kerf_mm']) == (job, kerf)]
                self.assertEqual({b['seed'] for b in subset}, set(pilot.SEEDS))
                for position in range(3):
                    self.assertEqual({b['arm_order'][position] for b in subset}, set(pilot.ARMS))

    def test_expired_session_preserves_failure_without_starting_a_process(self):
        job = {'name': 'authored', 'mode': 'all', 'edge_clearance': 0.2,
               'parts': [{'id': 'square', 'quantity': 1, 'rotations': {'kind': 'list', 'degrees': [0]},
                          'allow_mirror': False, 'priority': 1,
                          'geometry': [{'outer': [[0, 0], [10, 0], [10, 10], [0, 10]], 'holes': []}]}],
               'stocks': [{'id': 'sheet', 'width': 20, 'height': 20, 'count': None,
                           'margins': dict.fromkeys(['left', 'right', 'top', 'bottom'], 0),
                           'defects': [], 'outline': []}]}
        with tempfile.TemporaryDirectory(prefix='nestbolt-h5-pilot-') as raw:
            folder = Path(raw).resolve()
            self.assertTrue(folder.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            work, evidence = folder/'work', folder/'evidence'
            work.mkdir()
            evidence.mkdir()
            with patch.object(pilot, 'run', side_effect=AssertionError('A process must not start')) as invoke:
                result = pilot.case({'id': 'authored', 'sha256': 'test'}, job,
                    {'kerf_mm': 0.2, 'seed': 0}, 'baseline', 0, work, evidence, time.perf_counter()-1)
                invoke.assert_not_called()
            self.assertEqual(result['status'], 'failed')
            self.assertNotIn('material', result)
            self.assertIn('One-hour session cap', result['error'])
            with zipfile.ZipFile(evidence/result['archive']) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('case.json', archive.namelist())


if __name__ == '__main__':
    unittest.main()
