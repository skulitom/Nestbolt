import json
from pathlib import Path
import tempfile
import unittest

from construct_profile_batch import ROOT, audited_profile, digest, select_cases


class ProfileBatchTests(unittest.TestCase):
    def test_selection_excludes_holdouts_and_refuses_unknown_or_conflicting_ids(self):
        cases = select_cases(ROOT)
        self.assertEqual(len(cases),65)
        self.assertEqual(sum(c['id'].startswith('m-') for c in cases),30)
        for job in ['m-box-compact-2000','m-garment-bruce-4','unknown']:
            with self.assertRaisesRegex(ValueError,'forbidden'):
                select_cases(ROOT,[job],[])
            with self.assertRaisesRegex(ValueError,'forbidden'):
                select_cases(ROOT,[],[job])
        first = cases[0]['id']
        self.assertEqual(len(select_cases(ROOT,[first],[])),1)
        self.assertEqual(len(select_cases(ROOT,[],[first])),64)
        with self.assertRaisesRegex(ValueError,'included and excluded'):
            select_cases(ROOT,[first],[first])
        with self.assertRaisesRegex(ValueError,'No development jobs'):
            select_cases(ROOT,[],[case['id'] for case in cases])

    def test_audit_checks_binary_job_and_output_integrity_and_retains_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root/'output/construct-profiles/example'
            output = folder/'0'
            output.mkdir(parents=True)
            (output/'stdout.json').write_text('{}')
            profile = {'job':'a','job_sha256':'job-hash','binary_sha256':'binary-hash',
                       'runs':[{'exit_code':1,'outputs':{'stdout.json':digest(output/'stdout.json')}}]}
            path = folder/'profile.json'
            path.write_text(json.dumps(profile))
            case = {'id':'a','sha256':'job-hash'}
            self.assertEqual(audited_profile(root,path,case,'binary-hash')['status'],'failed')
            for bad_case, binary in [(case,'other'),({'id':'b','sha256':'job-hash'},'binary-hash')]:
                with self.assertRaisesRegex(ValueError,'provenance'):
                    audited_profile(root,path,bad_case,binary)
            (output/'stdout.json').write_text('{"changed":true}')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):
                audited_profile(root,path,case,'binary-hash')


if __name__ == '__main__':
    unittest.main()
