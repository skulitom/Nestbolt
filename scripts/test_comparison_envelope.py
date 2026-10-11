"""Admission bounds and failed/interrupted chunks never trigger hidden retries."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import comparison_envelope as envelope


class EnvelopeTests(unittest.TestCase):
    def test_next_chunk_must_fit_remaining_time_and_attempt_allowance(self):
        rows=[{'id':str(i),'seconds':300 if i==0 else 60} for i in range(40)]
        self.assertEqual(envelope.select_chunk(rows,759,10,'lbf'),[])
        self.assertEqual(len(envelope.select_chunk(rows,760,10,'lbf')),1)
        self.assertEqual(len(envelope.select_chunk(rows,10800,2,'lbf')),2)
        self.assertEqual(len(envelope.select_chunk(rows,10800,40,'deepnest')),3)

    def test_failed_chunk_is_retained_and_never_retried(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/'manifest.json').write_text(json.dumps({'settings':{'lbf':{}}}))
            with patch.object(envelope.sessions,'session_dir',return_value=root), \
                 patch.object(envelope.sessions,'verify_sources'), \
                 patch.object(envelope.sessions,'pending',return_value=[{'id':'0','seconds':60}]), \
                 patch.object(envelope.sessions,'execute',side_effect=RuntimeError('interrupted')) as run:
                with self.assertRaisesRegex(RuntimeError,'interrupted'):envelope.continue_queue('test','lbf',600,10)
                self.assertEqual(run.call_count,1)
            final=json.loads(next((root/'envelopes').glob('*/finished.json')).read_bytes())
            self.assertEqual(final['status'],'failed')
            self.assertEqual(final['completed_attempts'],0)


if __name__=='__main__':unittest.main()
