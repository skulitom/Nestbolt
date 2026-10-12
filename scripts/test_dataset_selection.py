"""Phase guards: development never touches held-out jobs or final seeds."""
from pathlib import Path
import unittest

from dataset_selection import check_seed, phase_cases

ROOT = Path(__file__).resolve().parents[1]


class PhaseTests(unittest.TestCase):
    def test_development_excludes_held_out_and_final_includes_them(self):
        dev = {r['id'] for r in phase_cases(ROOT, 'M', 'development')[1]}
        final = {r['id'] for r in phase_cases(ROOT, 'M', 'final')[1]}
        self.assertEqual(len(dev), 30)
        self.assertEqual(len(final), 40)
        self.assertTrue(dev < final)
        self.assertIn('m-box-compact-2000', final - dev)

    def test_seeds_belong_to_one_phase(self):
        check_seed('development', 0)
        check_seed('final', 1004)
        for phase, seed in [('development', 1000), ('final', 2), ('final', 7)]:
            with self.assertRaises(ValueError):
                check_seed(phase, seed)


if __name__ == '__main__':
    unittest.main()
