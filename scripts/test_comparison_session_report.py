"""Partial/failed seed sets must remain visible and ineligible in comparison tables."""
import unittest
from comparison_session_report import summarize, ranked_statistics


class AggregationTests(unittest.TestCase):
    def slots(self):
        return [{'id':str(i),'tool':'svgnest','job':'b-test','seconds':60,
                 'settings_role':'identical_constraints','settings':'identical','axis':'y','seed':i}
                for i in range(3)]

    def test_missing_and_invalid_seeds_cannot_be_hidden_by_valid_only_statistics(self):
        results={'0':{'status':'valid','score':1},'1':{'status':'invalid','score':None}}
        row=summarize(self.slots(),results)[0]
        self.assertFalse(row['all_seeds_valid'])
        self.assertEqual(row['outcomes'],{'valid':1,'invalid':1,'missing':1})
        self.assertEqual(row['valid_only_median'],1)
        results['2']={'status':'unsupported','score':None}
        row=summarize(self.slots(),results)[0]
        self.assertFalse(row['all_seeds_valid'])
        self.assertEqual(row['completed'],3)

    def test_complete_seed_set_has_inclusive_quartiles_and_separate_configurations(self):
        results={str(i):{'status':'valid','score':v} for i,v in enumerate([1,2,7])}
        row=summarize(self.slots(),results)[0]
        self.assertTrue(row['all_seeds_valid'])
        self.assertEqual(row['valid_only_median'],2)
        self.assertEqual(row['valid_only_quartiles'],[1.5,2,4.5])
        slots=self.slots();slots[2]['settings']='expanded'
        self.assertTrue(all(not r['all_seeds_valid'] for r in summarize(slots,results)))

    def test_duplicate_seeds_unexpected_results_and_incompatible_metrics_are_rejected(self):
        slots=self.slots();slots[1]['seed']=0
        with self.assertRaisesRegex(ValueError,'Duplicate seed'):summarize(slots,{})
        with self.assertRaisesRegex(ValueError,'unexpected'):summarize(self.slots(),{'other':{}})
        runs={'0':{'status':'valid','score':1},'1':{'status':'valid','score':2,'score_kind':'strip_length'}}
        with self.assertRaisesRegex(ValueError,'Different metrics'):summarize(self.slots(),runs)

    def test_lbf_uses_the_independent_material_metric(self):
        slots=self.slots()
        for slot in slots:slot['tool']='lbf'
        runs={str(i):{'status':'valid','metrics':{'normalized_material':v}} for i,v in enumerate([2,3,6])}
        row=summarize(slots,runs)[0]
        self.assertTrue(row['all_seeds_valid'])
        self.assertEqual(row['valid_only_median'],3)

    def test_failed_seed_ranks_after_valid_scores_without_disappearing(self):
        rows={'0':{'status':'valid','score':1},'1':{'status':'valid','score':2},'2':{'status':'invalid','score':None}}
        row=summarize(self.slots(),rows)[0]
        self.assertFalse(row['all_seeds_valid'])
        self.assertTrue(row['comparable_median'])
        self.assertEqual(row['valid_only_median'],1.5)
        self.assertEqual(row['comparison_statistics']['median'],{'state':'finite','value':2})
        self.assertEqual(row['comparison_statistics']['quartiles'][2],{'state':'failed','value':None})

    def test_missing_and_failure_majority_have_no_comparison_value(self):
        for attempted,expected in [(2,'incomplete'),(3,'failed')]:
            stats=ranked_statistics([1],attempted,3)
            self.assertEqual(stats['median'],{'state':expected,'value':None})
        self.assertEqual(ranked_statistics([],3,3)['median'],{'state':'failed','value':None})
        with self.assertRaises(ValueError):ranked_statistics([float('inf')],3,3)


if __name__=='__main__':unittest.main()
