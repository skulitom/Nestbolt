"""A stopped/failed attempt cannot become an invisible retry or a smaller matrix."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import comparison_session as sessions
from svgnest import digest, write


class SessionTests(unittest.TestCase):
    def fixture(self, root):
        (root/'guard.txt').write_text('frozen',encoding='utf-8')
        slot={'id':'00000','tool':'svgnest','job':'b-fixture','job_sha256':'job-hash',
              'seconds':60,'seed':0,'settings':'identical','axis':'y'}
        directory=root/'output/comparison-sessions/test'
        directory.mkdir(parents=True)
        manifest={'settings':{'svgnest':{}},'slots':[slot],'sources':{'guard.txt':digest(root/'guard.txt')}}
        write(directory/'manifest.json',manifest)
        return directory,manifest

    def record(self, root, slot):
        path=root/'output/playwright/svgnest/trial/run.json'
        path.parent.mkdir(parents=True)
        (path.parent/'job.json').write_text('{}',encoding='utf-8')
        # A real unsupported native-record shape, with checksum-protected input.
        value={'job':slot['job'],'job_sha256':digest(path.parent/'job.json'),
               'seconds':slot['seconds'],'seed':slot['seed'],'settings':slot['settings'],
               'axis':slot['axis'],'phase':'development','status':'unsupported','score':None,
               'outputs':{'job.json':digest(path.parent/'job.json')}}
        write(path,value)
        return path

    def test_interrupted_attempt_is_never_invoked_again(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);directory,manifest=self.fixture(root)
            with patch.object(sessions,'ROOT',root), patch.object(sessions,'invoke',side_effect=RuntimeError('interrupted')) as invoke:
                with self.assertRaisesRegex(RuntimeError,'interrupted'):sessions.execute('test','svgnest',1)
                self.assertFalse((directory/'active.lock').exists())
                self.assertTrue((directory/'attempts/00000/start.json').exists())
                with self.assertRaisesRegex(ValueError,'started without'):sessions.execute('test','svgnest',1)
                self.assertEqual(invoke.call_count,1)

    def test_source_change_stops_before_starting_native_work(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);directory,manifest=self.fixture(root)
            (root/'guard.txt').write_text('edited',encoding='utf-8')
            with patch.object(sessions,'ROOT',root),patch.object(sessions,'invoke') as invoke:
                with self.assertRaisesRegex(ValueError,'changed'):sessions.execute('test','svgnest',1)
                invoke.assert_not_called()
                self.assertFalse((directory/'attempts').exists())

    def test_failed_outcome_is_completed_once_and_manifest_changes_are_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);directory,manifest=self.fixture(root)
            slot=manifest['slots'][0]
            path=self.record(root,slot)
            slot['job_sha256']=json.loads(path.read_bytes())['job_sha256']
            (directory/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
            with patch.object(sessions,'ROOT',root),patch.object(sessions,'invoke',return_value=path) as invoke:
                sessions.execute('test','svgnest',1)
                sessions.execute('test','svgnest',1)
                self.assertEqual(invoke.call_count,1)
                self.assertEqual(sessions.completed(directory,manifest)['00000']['status'],'unsupported')
                manifest['slots'].append({**slot,'id':'00001'})
                (directory/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'manifest'):sessions.completed(directory,manifest)

    def test_chunk_limit_and_foreign_lock_do_not_modify_existing_work(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);directory,manifest=self.fixture(root)
            lock=directory/'active.lock';lock.write_text('owned elsewhere',encoding='utf-8')
            with patch.object(sessions,'ROOT',root),patch.object(sessions,'invoke') as invoke:
                with self.assertRaises(FileExistsError):sessions.execute('test','svgnest',1)
                self.assertEqual(lock.read_text(),'owned elsewhere')
                with self.assertRaisesRegex(ValueError,'limit'):sessions.execute('test','svgnest',31)
                invoke.assert_not_called()


if __name__=='__main__':unittest.main()
