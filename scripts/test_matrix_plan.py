"""Acceptance coverage cannot lose large/held-out jobs or leak them into tuning."""
from collections import Counter
import unittest
from matrix_plan import expected, schedule


class MatrixCoverageTests(unittest.TestCase):
    def test_full_dataset_and_both_budgets(self):
        plan=expected();self.assertEqual(Counter(r['set'] for r in plan['cases']),{'S':13,'B':35,'M':40})
        long=[r for r in plan['cases'] if 300 in r['budgets_seconds']]
        self.assertEqual(len(long),12);self.assertEqual(Counter(r['set'] for r in long),{'B':6,'M':6})
        self.assertTrue(any(r['held_out'] and r['part_count']==2000 for r in long))

    def test_no_held_out_tuning_and_fresh_final_seeds(self):
        plan=expected();development=list(schedule(plan,'development'));final=list(schedule(plan,'final'))
        self.assertFalse(any(r['held_out'] for r in development))
        self.assertEqual(len({r['job'] for r in final if r['held_out']}),10)
        self.assertFalse(set(plan['seeds']['development']) & set(plan['seeds']['final']))
        self.assertEqual(len(development),528);self.assertEqual(len(final),1000)

    def test_every_final_job_budget_has_both_settings_and_five_seeds(self):
        rows=list(schedule(expected(),'final'));counts=Counter((r['job'],r['seconds']) for r in rows)
        self.assertEqual(set(counts.values()),{10})
        self.assertEqual(len(counts),100)


if __name__=='__main__':unittest.main()
