"""Reusable checker snapshots must remain independent of product rebuilds."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import deepnest


class SnapshotTests(unittest.TestCase):
    def test_verified_snapshot_is_copied_without_building_and_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root/'crates/validator/src'
            source.mkdir(parents=True)
            (source/'lib.rs').write_text('validator', encoding='utf-8')
            (root/'Cargo.lock').write_text('locked', encoding='utf-8')
            binary = root/'saved/nestbolt.exe'
            binary.parent.mkdir()
            binary.write_bytes(b'checker bytes')
            snapshot = {'path': 'saved/nestbolt.exe', 'sha256': deepnest.digest(binary),
                        'sources': {p.relative_to(root).as_posix(): deepnest.digest(p)
                                    for p in [root/'Cargo.lock', source/'lib.rs']}}
            batch = root/'previous.json'
            batch.write_text(json.dumps({'validator_snapshot': snapshot}), encoding='utf-8')
            destination = root/'next'
            destination.mkdir()
            with patch.object(deepnest, 'ROOT', root), patch.object(deepnest.subprocess, 'run') as build:
                copied = deepnest.freeze_validator(destination, batch)
                self.assertEqual(copied['sha256'], snapshot['sha256'])
                self.assertEqual((destination/'nestbolt.exe').read_bytes(), binary.read_bytes())
                build.assert_not_called()
                binary.write_bytes(b'changed binary')
                with self.assertRaisesRegex(ValueError, 'snapshot changed'):
                    deepnest.freeze_validator(destination, batch)
                binary.write_bytes(b'checker bytes')
                (source/'lib.rs').write_text('changed validator', encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'snapshot changed'):
                    deepnest.freeze_validator(destination, batch)


if __name__ == '__main__':
    unittest.main()
