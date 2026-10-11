"""Evidence audits reject altered files, invented scores and missing CPU limits."""
import json
from pathlib import Path
import tempfile
import unittest

from svgnest import digest
from svgnest_report import audit_record


class SvgNestEvidenceTests(unittest.TestCase):
    def make_record(self, directory, change=None):
        evidence = [{'pid': 1, 'affinity': '1'}, {'pid': 2, 'affinity': '1'}]
        affinity = {'platform': 'win32', 'mask': '1', 'method': 'JOB_OBJECT_LIMIT_AFFINITY'}
        raw = {'status': 'completed', 'errors': [], 'last': {'elapsed_ms': 1000},
               'configured_workers': 1, 'affinity': affinity, 'affinity_verification': evidence}
        metrics = {'normalized_material': 0.5, 'sheets_used': 1}
        run = {'status': 'valid', 'score': 0.5, 'metrics': metrics, 'seconds': 5,
               'output_decoding': 'native_svg_attributes_v2',
               'validator_exit_code': 0, 'affinity_verification': evidence, 'cpu_affinity': affinity}
        if change:
            change(run, raw)
        files = {'job.json': {}, 'layout.json': {}, 'request.json': {},
                 'validation.json': {'valid': True, 'metrics': metrics},
                 'browser-result.json': raw, 'candidates.jsonl': {}}
        for name, value in files.items():
            (directory / name).write_text(json.dumps(value), encoding='utf-8')
        run['outputs'] = {name: digest(directory / name) for name in files}
        run['job_sha256'] = digest(directory / 'job.json')
        path = directory / 'run.json'
        path.write_text(json.dumps(run), encoding='utf-8')
        return path, digest(path)

    def test_file_tampering_and_directory_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path, checksum = self.make_record(root)
            self.assertEqual(audit_record(path, checksum)['score'], 0.5)
            (root / 'layout.json').write_text('changed', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'output changed'):
                audit_record(path, checksum)
            path, checksum = self.make_record(root)
            value = json.loads(path.read_bytes())
            value['outputs']['../escape.json'] = 'ignored'
            path.write_text(json.dumps(value), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'evidence path'):
                audit_record(path, digest(path))

    def test_score_and_failed_state_must_match_validation(self):
        for change in [lambda run, raw: run.update(score=0.1), lambda run, raw: run.update(status='invalid')]:
            with tempfile.TemporaryDirectory() as temp:
                path, checksum = self.make_record(Path(temp), change)
                with self.assertRaises(ValueError):
                    audit_record(path, checksum)

    def test_late_results_and_unverified_cpu_tree_are_ineligible(self):
        for change in [lambda run, raw: raw['last'].update(elapsed_ms=5001),
                       lambda run, raw: run.update(output_decoding='legacy_svg_matrix'),
                       lambda run, raw: raw.update(affinity_verification=[]),
                       lambda run, raw: raw['affinity'].update(method='inherited_unverified'),
                       lambda run, raw: raw.update(configured_workers=4)]:
            with tempfile.TemporaryDirectory() as temp:
                path, checksum = self.make_record(Path(temp), change)
                with self.assertRaises(ValueError):
                    audit_record(path, checksum)

    def test_exact_path_input_claim_requires_observed_parser_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            path, checksum = self.make_record(Path(temp), lambda run,raw:run.update(input_encoding='linear_svg_paths_v2'))
            with self.assertRaisesRegex(ValueError,'input fidelity'): audit_record(path,checksum)
        with tempfile.TemporaryDirectory() as temp:
            def controls(run,raw):
                run['input_encoding']='linear_svg_paths_v2'
                run['input_fidelity']=raw['input_fidelity']={'encoding':'linear_svg_paths_v2','coordinates':8,'maximum_absolute_error':0}
            path,checksum=self.make_record(Path(temp),controls)
            audit_record(path,checksum)


if __name__ == '__main__':
    unittest.main()
