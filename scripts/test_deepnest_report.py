"""Deepnest evidence cannot invent a score, exceed its budget or lose provenance."""
import json
from pathlib import Path
import tempfile
import unittest

from deepnest_report import audit_record
from svgnest import digest


class DeepnestEvidenceTests(unittest.TestCase):
    def fixture(self, root, mutate=None):
        metrics = {'normalized_material': 0.5, 'sheets_used': 1}
        controls = {'affinity': {'platform':'win32','mask':'4','method':'JOB_OBJECT_LIMIT_AFFINITY'},
                    'affinity_verification':[{'pid':1,'affinity':'4'},{'pid':2,'affinity':'4'}],
                    'worker_check':{'workers':1,'seed':0}, 'native_binaries':[{'sha256':'native'}],
                    'electron_executable_sha256':'electron'}
        raw = {**controls, 'status':'completed','errors':[], 'last':{'elapsed_ms':1000},
               'configured_workers':1,'imported':{'seed':0}}
        run = {**controls, 'status':'valid','score':0.5,'metrics':metrics,'seed':0,'seconds':5,'validator_exit_code':0}
        if mutate: mutate(run,raw)
        files = {'job.json':{},'layout.json':{},'request.json':{},'browser-result.json':raw,
                 'validation.json':{'valid':True,'metrics':metrics},'candidates.jsonl':{}}
        for name,value in files.items(): (root/name).write_text(json.dumps(value),encoding='utf-8')
        run['outputs'] = {name:digest(root/name) for name in files}
        run['job_sha256'] = digest(root/'job.json')
        path = root/'run.json';path.write_text(json.dumps(run),encoding='utf-8')
        return path,digest(path)

    def test_valid_evidence_and_file_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            path,checksum = self.fixture(Path(temp))
            self.assertEqual(audit_record(path,checksum)['score'],0.5)
            (path.parent/'layout.json').write_text('changed',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'output changed'): audit_record(path,checksum)

    def test_failed_state_and_score_cannot_contradict_checker(self):
        for change in [lambda run,raw:run.update(score=0.4),lambda run,raw:run.update(status='failed')]:
            with tempfile.TemporaryDirectory() as temp:
                path,checksum=self.fixture(Path(temp),change)
                with self.assertRaises(ValueError):audit_record(path,checksum)

    def test_matching_multicore_masks_do_not_count_as_single_core(self):
        def multicore(run,raw):
            raw['affinity']['mask']='3'
            for row in raw['affinity_verification']:row['affinity']='3'
        with tempfile.TemporaryDirectory() as temp:
            path,checksum=self.fixture(Path(temp),multicore)
            with self.assertRaisesRegex(ValueError,'single-core'):audit_record(path,checksum)

    def test_missing_controls_native_binary_and_late_result_are_rejected(self):
        for change in [lambda run,raw:raw['last'].update(elapsed_ms=5001),
                       lambda run,raw:raw['worker_check'].update(workers=4),
                       lambda run,raw:raw.update(native_binaries=[]),
                       lambda run,raw:raw['affinity_verification'][0].update(affinity='255')]:
            with tempfile.TemporaryDirectory() as temp:
                path,checksum=self.fixture(Path(temp),change)
                with self.assertRaises(ValueError):audit_record(path,checksum)

    def test_parser_fidelity_and_stock_derivation_require_matching_evidence(self):
        for change in [lambda run,raw:run.update(input_encoding='linear_svg_paths_v2'),
                       lambda run,raw:run.update(stock_preparation={'output_sha256':'invented','input_job_sha256':'invented'})]:
            with tempfile.TemporaryDirectory() as temp:
                path,checksum=self.fixture(Path(temp),change)
                with self.assertRaises(ValueError):audit_record(path,checksum)
        def proof(run,raw):
            run['input_encoding']='linear_svg_paths_v2'
            value={'encoding':'linear_svg_paths_v2','coordinates':8,'maximum_absolute_error':0,
                   'maximum_scaled_error':0,'scaled_error_limit':8,'error_scale':'Number.EPSILON * max(1, abs(source_coordinate))'}
            run['input_fidelity']=raw['input_fidelity']=raw['imported']['input_fidelity']=value
        with tempfile.TemporaryDirectory() as temp:
            path,checksum=self.fixture(Path(temp),proof)
            audit_record(path,checksum)


if __name__ == '__main__':
    unittest.main()
