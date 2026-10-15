"""Acceptance cannot silently discard missing/failed seeds or total-material loss."""
from copy import deepcopy
import unittest
from h4_full_matrix import ENGINES, SEEDS, summarize


def records():
    return {engine: [{'job': job, 'seed': seed, 'status': 'valid', 'material': value}
                    for job, value in [('small', 1.), ('medium', 2.), ('large', 100.)]
                    for seed in SEEDS] for engine in ENGINES}


IDS = ['small', 'medium', 'large']


class GateTests(unittest.TestCase):
    def test_complete_equal_results_pass(self):
        result = summarize(records(), IDS)
        self.assertTrue(result['all_quality_checks_pass'])
        self.assertFalse(result['H4_complete'])

    def test_native_limit_and_improvements(self):
        for factor, expected in [(1.0049, True), (1.0051, False), (.90, True)]:
            data = records()
            for engine in ENGINES[1:]:
                for row in data[engine]:
                    row['material'] *= factor
            self.assertEqual(summarize(data, IDS)['all_quality_checks_pass'], expected)

    def test_missing_failed_and_duplicate_attempts_never_pass(self):
        for engine in ENGINES:
            for kind in ['missing', 'failed', 'duplicate', 'wrong_seed', 'nan']:
                with self.subTest(engine=engine, kind=kind):
                    data = records()
                    if kind == 'missing':
                        data[engine].pop()
                    elif kind == 'failed':
                        data[engine][0]['status'] = 'failed'
                        data[engine][0].pop('material')
                    elif kind == 'duplicate':
                        data[engine].append(deepcopy(data[engine][0]))
                    elif kind == 'wrong_seed':
                        data[engine][0]['seed'] = 1000
                    else:
                        data[engine][0]['material'] = float('nan')
                    self.assertFalse(summarize(data, IDS)['all_quality_checks_pass'])

    def test_total_material_guard_is_not_hidden_by_the_median(self):
        data = records()
        for row in data['chrome']:
            if row['job'] == 'large':
                row['material'] *= 1.03
        result = summarize(data, IDS)['browsers_vs_native']['chrome']
        self.assertEqual(result['median_difference_percent'], 0.)
        self.assertGreater(result['total_difference_percent'], 2.)
        self.assertFalse(result['passes_aggregate_bounds'])

    def test_one_worse_seed_is_retained_even_when_three_seed_median_passes(self):
        data = records()
        for row in data['firefox']:
            if row['seed'] == 0:
                row['material'] *= 1.03
        result = summarize(data, IDS)
        browser = result['browsers_vs_native']['firefox']
        self.assertTrue(browser['passes_aggregate_bounds'])
        self.assertFalse(browser['per_seed'][0]['within_original_G5_bounds'])
        self.assertFalse(browser['all_seeds_within_original_G5_bounds'])
        self.assertFalse(result['all_quality_checks_pass'])


if __name__ == '__main__':
    unittest.main()
