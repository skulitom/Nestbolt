"""Strip comparison keeps every seed and rejects missing/duplicated coverage."""
from copy import deepcopy
import unittest
from strip_report import summarize


class StripStatisticsTests(unittest.TestCase):
    def setUp(self):
        self.reference={'example': {'median':100.0,'settings':'identical'}}
        self.rows=[{'job':'example','seed':seed,'status':'valid','result':{'strip_length':value}}
                   for seed,value in enumerate([99.0,100.0,101.0])]

    def test_complete_population_passes_with_failure_ranked_medians(self):
        report=summarize(self.rows,self.reference)
        self.assertEqual(report['median_regression_percent'],0.0)
        self.assertTrue(report['development_thresholds_met'])
        failed=deepcopy(self.rows)
        failed[0].update(status='failed',result=None)
        report=summarize(failed,self.reference)
        self.assertEqual(report['rows'][0]['native_median'],101.0)
        self.assertFalse(report['development_thresholds_met'])
        failed[1].update(status='timeout',result=None)
        self.assertIsNone(summarize(failed,self.reference)['median_regression_percent'])

    def test_missing_duplicate_and_regression_cannot_pass(self):
        for rows in [self.rows[:-1],self.rows+[self.rows[0]]]:
            with self.assertRaises(ValueError): summarize(rows,self.reference)
        for row in self.rows: row['result']['strip_length']=103.0
        self.assertFalse(summarize(self.rows,self.reference)['development_thresholds_met'])


if __name__=='__main__':
    unittest.main()
