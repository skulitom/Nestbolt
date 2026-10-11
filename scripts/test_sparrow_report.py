"""A current Sparrow score requires unchanged files and on-time native evidence."""
import json
from pathlib import Path
import tempfile
import unittest
from sparrow_benchmark import digest
from sparrow_report import audit_record


class SparrowEvidenceTests(unittest.TestCase):
    def fixture(self,root,change=None):
        solution={'strip_width':10}
        raw={'status':'completed','error':None,'workers':1,'seed':0,'seconds':5,'settings':'identical',
             'solution':solution,'candidates':1,'accepted_at_seconds':1}
        candidates=[{'solution':solution,'elapsed_seconds':1}]
        metrics={'normalized_material':.5}
        run={'status':'valid','score':.5,'score_kind':'normalized_material','metrics':metrics,
             'workers':1,'rayon_threads':1,'seed':0,'seconds':5,'settings':'identical','validator_exit_code':0}
        if change: change(run,raw,candidates)
        files={'job.json':{},'input.json':{},'request.json':{},'layout.json':{},
               'validation.json':{'valid':True,'metrics':metrics},'solver-result.json':raw}
        for name,value in files.items(): (root/name).write_text(json.dumps(value),encoding='utf-8')
        (root/'candidates.jsonl').write_text('\n'.join(json.dumps(c) for c in candidates)+'\n',encoding='utf-8')
        run['outputs']={p.name:digest(p) for p in root.iterdir()}
        run['job_sha256']=digest(root/'job.json')
        path=root/'run.json';path.write_text(json.dumps(run),encoding='utf-8');return path,digest(path)

    def test_valid_evidence_and_file_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            path,h=self.fixture(Path(temp));self.assertEqual(audit_record(path,h)['score'],.5)
            (path.parent/'layout.json').write_text('changed')
            with self.assertRaisesRegex(ValueError,'bytes changed'): audit_record(path,h)

    def test_late_candidate_changed_workers_or_selection_rejected(self):
        for change in [lambda r,n,c:c[0].update(elapsed_seconds=6),lambda r,n,c:n.update(workers=3),
                       lambda r,n,c:n.update(solution={'strip_width':9}),lambda r,n,c:n.update(accepted_at_seconds=.5)]:
            with tempfile.TemporaryDirectory() as temp:
                path,h=self.fixture(Path(temp),change)
                with self.assertRaises(ValueError):audit_record(path,h)

    def test_invalid_state_or_score_cannot_contradict_validator(self):
        for change in [lambda r,n,c:r.update(score=.4),lambda r,n,c:r.update(status='invalid')]:
            with tempfile.TemporaryDirectory() as temp:
                path,h=self.fixture(Path(temp),change)
                with self.assertRaises(ValueError):audit_record(path,h)


if __name__=='__main__': unittest.main()
