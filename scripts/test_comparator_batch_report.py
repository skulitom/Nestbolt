"""Reject incomplete or relabelled comparator matrices, even with fresh checksums."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import comparator_batch_report as reporting
from svgnest import digest


class MatrixAuditTests(unittest.TestCase):
    def fixture(self, root, tool):
        dataset = root/'benchmarks/datasets'
        source = dataset/'B/b-example.json'
        source.parent.mkdir(parents=True)
        source.write_text('{"name":"b-example"}', encoding='utf-8')
        case = {'id':'b-example', 'set':'B', 'path':'B/b-example.json', 'sha256':digest(source)}
        manifest = dataset/'academic.json'
        manifest.write_text(json.dumps({'instances':[case]}), encoding='utf-8')
        folder = root/reporting.TOOLS[tool][0]/'trial'
        folder.mkdir(parents=True)
        (folder/'job.json').write_bytes(source.read_bytes())
        run = {'job':'b-example', 'job_sha256':digest(source), 'status':'unsupported',
               'score':None, 'metrics':None, 'seconds':60, 'seed':0, 'settings':'identical', 'axis':'y',
               'sources':{'adapter':'frozen'}, 'outputs':{'job.json':digest(source)}}
        record = folder/'run.json'
        record.write_text(json.dumps(run), encoding='utf-8')
        batch = {key:run[key] for key in ['seconds','seed','settings','axis','sources']}
        batch.update(dataset='B', dataset_manifest_sha256=digest(manifest), cases=[case], complete=True, valid_runs=0,
                     runs=[{'job':case['id'], 'status':run['status'], 'record':record.relative_to(root).as_posix(), 'sha256':digest(record)}])
        path = root/'batch.json'
        return path, batch

    def check(self, root, path, batch, tool):
        path.write_text(json.dumps(batch), encoding='utf-8')
        with patch.object(reporting, 'ROOT', root):
            return reporting.audit_batch(path, tool)

    def test_every_failed_attempt_is_retained_and_source_tampering_rejected(self):
        for tool in ['deepnest','sparrow']:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp); path,batch = self.fixture(root,tool)
                _,rows = self.check(root,path,batch,tool)
                self.assertEqual(rows[0]['run']['status'],'unsupported')
                (root/'benchmarks/datasets/B/b-example.json').write_text('changed')
                with self.assertRaisesRegex(ValueError,'source changed'): self.check(root,path,batch,tool)

    def test_missing_duplicate_or_incomplete_rows_never_form_a_complete_matrix(self):
        for change in [lambda b:b.update(complete=False), lambda b:b.update(runs=[]),
                       lambda b:b['runs'].append(deepcopy(b['runs'][0])),
                       lambda b:b['cases'].append(deepcopy(b['cases'][0]))]:
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp);path,batch=self.fixture(root,'deepnest');change(batch)
                with self.assertRaises(ValueError): self.check(root,path,batch,'deepnest')

    def test_relabelling_budget_seed_or_outcome_is_rejected(self):
        for change in [lambda b:b.update(seed=1), lambda b:b.update(seconds=300),
                       lambda b:b.update(valid_runs=1), lambda b:b['runs'][0].update(status='valid')]:
            with tempfile.TemporaryDirectory() as temp:
                root=Path(temp);path,batch=self.fixture(root,'sparrow');change(batch)
                with self.assertRaises(ValueError): self.check(root,path,batch,'sparrow')


if __name__ == '__main__': unittest.main()
