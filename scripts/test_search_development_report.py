import json
import unittest
from search_development_report import first_reached, summarize


class SearchReportTests(unittest.TestCase):
    def test_missing_layout_cannot_silently_improve_the_median_or_win_rate(self):
        rows = [dict(status='valid',competitor_60={'median':1},material=.9,reduction_percent=10,win_or_tie=True),
                dict(status='failed',competitor_60={'median':1},material=None,reduction_percent=None,win_or_tie=None),
                dict(status='valid',competitor_60=None,material=.8,reduction_percent=None,win_or_tie=None)]
        report = summarize(rows)
        self.assertEqual(report['finite_competitors'],2)
        self.assertEqual(report['no_finite_competitor'],1)
        self.assertEqual(report['win_or_tie'],1)
        self.assertEqual(report['missing_valid_nestbolt_comparisons'],1)
        self.assertIsNone(report['median_reduction_percent'])

    def test_time_to_target_requires_an_accepted_complete_layout(self):
        def event(seconds,accepted,complete,material):
            return {'elapsed_seconds':seconds,'message':json.dumps(dict(accepted=accepted,complete=complete,material=material))}
        profile = {'runs':[{'exit_code':0,'progress':[event(1,False,True,.5),event(2,True,False,.5),
                    event(3,True,True,2),event(31,True,True,1.0000005),event(32,True,True,.9)]}]}
        self.assertEqual(first_reached(profile,1),31)
        self.assertIsNone(first_reached(profile,None))
        self.assertIsNone(first_reached(profile,.1))
        profile['runs'][0]['exit_code'] = 1
        self.assertIsNone(first_reached(profile,1))


if __name__ == '__main__':
    unittest.main()
