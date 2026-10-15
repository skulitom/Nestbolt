"""Report ordering must not waive coordinate or multiplicity checks."""
from copy import deepcopy
import unittest
from h6_material_cost import equivalent_common


class CommonReportComparison(unittest.TestCase):
    def test_unordered_collections_keep_strict_geometry_and_counts(self):
        a=[{'sheet_id':'sheet-0','shared_edges':[
            {'from_mm':[54.00012000000001,93.25],'to_mm':[79.00012,93.25],'owners':['a','b']},
            {'from_mm':[54.00012,119.75],'to_mm':[84.00012,119.75],'owners':['b','c']}],
            'paths':[{'start':[1.,2.],'segments':[{'kind':'line','to':[3.,4.]}]},
                     {'start':[5.,6.],'segments':[{'kind':'line','to':[7.,8.]}]}]}]
        b=deepcopy(a)
        b[0]['shared_edges'].reverse(); b[0]['paths'].reverse()
        b[0]['shared_edges'][1]['from_mm'][0]=54.00012
        self.assertLess(equivalent_common(a,b),1e-9)
        changed=deepcopy(b); changed[0]['shared_edges'][0]['to_mm'][0]+=1e-7
        with self.assertRaises(AssertionError): equivalent_common(a,changed)
        changed=deepcopy(b); changed[0]['paths'].append(deepcopy(changed[0]['paths'][0]))
        with self.assertRaises(AssertionError): equivalent_common(a,changed)
        changed=deepcopy(b); changed[0]['shared_edges'][0]['owners'].reverse()
        with self.assertRaises(AssertionError): equivalent_common(a,changed)


if __name__=='__main__':
    unittest.main()
