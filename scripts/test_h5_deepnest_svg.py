import tempfile
import unittest
from pathlib import Path

from h5_deepnest_svg import audit


class SvgAuditTests(unittest.TestCase):
    def test_shared_line_export_has_expected_length_and_rejects_changed_geometry(self):
        prepared={'imports':[{'kind':'part','source_rings':[[[0,0],[20,0],[20,20],[0,20]]]}]}
        native={'placements':[{'sheetplacements':[{'source':0,'x':x,'y':0,'rotation':0} for x in [0,20]]}]}
        raw={'last':{'native':native},'cut_exports':{'selected_candidate':native,'network_conversion':False,
            'native_merged_length':20,'sheet_bounds':[{'x':0,'y':0,'width':40,'height':20}]}}
        opening='<svg xmlns="http://www.w3.org/2000/svg" width="40mm" height="20mm" viewBox="0 0 40 20">'
        square='<path d="M0 0L20 0L20 20L0 20Z"/>'
        unmerged=opening+square+'<g transform="translate(20, 0)">'+square+'</g></svg>'
        merged=opening+'<path d="M0 0L40 0L40 20L0 20Z"/><line x1="20" y1="0" x2="20" y2="20"/></svg>'
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            (folder/'cuts-unmerged.svg').write_text(unmerged,encoding='utf-8')
            (folder/'cuts-merged.svg').write_text(merged,encoding='utf-8')
            result=audit(folder,prepared,raw)
            self.assertEqual(result['source_cut_length_mm'],160)
            self.assertEqual(result['export_saved_length_mm'],20)
            self.assertEqual(result['exports']['merged']['length_mm'],140)
            for bad in [merged.replace('x1="20"','x1="19"'),
                        opening+'<path d="M0 0L40 0L40 20L0 20Z"/></svg>',
                        merged.replace('width="40mm"','width="41mm"')]:
                (folder/'cuts-merged.svg').write_text(bad,encoding='utf-8')
                with self.assertRaises(AssertionError):audit(folder,prepared,raw)


if __name__=='__main__':unittest.main()
