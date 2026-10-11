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
    def fixture(self, root, tool, group='B', held_out=False):
        dataset = root/'benchmarks/datasets'
        name = f'{group.lower()}-example'
        relative = f'{group}/{name}.json'
        source = dataset/relative
        source.parent.mkdir(parents=True)
        source.write_text(json.dumps({'name':name}), encoding='utf-8')
        case = {'id':name, 'set':group, 'path':relative, 'sha256':digest(source)}
        if group == 'M':
            case = {'id':name,'set':group,'held_out':held_out,'files':{relative:digest(source)}}
        manifest = dataset/('makers.json' if group == 'M' else 'academic.json')
        manifest.write_text(json.dumps({'instances':[case]}), encoding='utf-8')
        if group == 'M': case.update(path=relative,sha256=digest(source))
        folder = root/reporting.TOOLS[tool][0]/'trial'
        folder.mkdir(parents=True)
        (folder/'job.json').write_bytes(source.read_bytes())
        run = {'job':name, 'job_sha256':digest(source), 'status':'unsupported',
               'score':None, 'metrics':None, 'seconds':60, 'seed':0, 'settings':'identical', 'axis':'y',
               'sources':{'adapter':'frozen'}, 'outputs':{'job.json':digest(source)}}
        record = folder/'run.json'
        record.write_text(json.dumps(run), encoding='utf-8')
        batch = {key:run[key] for key in ['seconds','seed','settings','axis','sources']}
        batch.update(dataset=group, dataset_manifest_sha256=digest(manifest), cases=[case], complete=True, valid_runs=0,
                     runs=[{'job':case['id'], 'status':run['status'], 'record':record.relative_to(root).as_posix(), 'sha256':digest(record)}])
        path = root/'batch.json'
        return path, batch

    def check(self, root, path, batch, tool):
        path.write_text(json.dumps(batch), encoding='utf-8')
        with patch.object(reporting, 'ROOT', root):
            return reporting.audit_batch(path, tool)

    def test_every_failed_attempt_is_retained_and_source_tampering_rejected(self):
        for tool in ['deepnest','sparrow','svgnest']:
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

    def test_maker_sources_are_audited_and_held_out_jobs_cannot_enter_development(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path,batch=self.fixture(root,'deepnest','M')
            _,rows=self.check(root,path,batch,'deepnest')
            self.assertEqual(rows[0]['job'],'m-example')
            (root/'benchmarks/datasets/M/m-example.json').write_text('changed')
            with self.assertRaisesRegex(ValueError,'source changed'):
                self.check(root,path,batch,'deepnest')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path,batch=self.fixture(root,'deepnest','M',True)
            with self.assertRaisesRegex(ValueError,'frozen case selection'):
                self.check(root,path,batch,'deepnest')


if __name__ == '__main__': unittest.main()
