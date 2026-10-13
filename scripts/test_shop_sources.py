"""Source collection must fail closed on licence, provenance and byte drift."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import shop_sources as shop


class ShopSourcesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nestbolt-shop-test-')
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        p = patch.object(shop, 'CORPUS', self.root)
        p.start()
        self.addCleanup(p.stop)
        self.entry = {'path': 'real/input.dxf', 'sha256': shop.digest(b'original'),
                      'download_url': 'https://raw.githubusercontent.com/owner/repo/' + 'a'*40 + '/input.dxf'}
        self.source = {'repository': 'owner/repo', 'revision': 'a'*40, 'licence': 'MIT',
                       'review': 'Reviewed full licence', 'evidence': [dict(self.entry, path='licences/LICENSE')],
                       'files': [self.entry]}

    def load(self, source):
        path = self.root / 'lock.json'
        path.write_text(json.dumps({'sources': [source]}), encoding='utf-8', newline='\n')
        return shop.load_lock(path)

    def test_excludes_unlicensed_and_copyleft_inputs(self):
        for licence in ['unknown', 'GPL-3.0', 'LGPL-3.0', 'MPL-2.0', 'CC-BY-NC-4.0']:
            with self.subTest(licence=licence), self.assertRaises(ValueError):
                self.load(dict(self.source, licence=licence))

    def test_rejects_paths_outside_corpus(self):
        for path in ['../other', '/tmp/other', 'C:/other', 'real/../../other', 'real\\..\\other']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                shop.destination(path)

    def test_requires_evidence_and_immutable_matching_source(self):
        bad = copy.deepcopy(self.source)
        bad['files'][0]['download_url'] = bad['files'][0]['download_url'].replace('a'*40, 'main')
        for source in [bad, dict(self.source, evidence=[]), dict(self.source, revision='main')]:
            with self.assertRaises(ValueError):
                self.load(source)

    def test_drift_does_not_overwrite_local_bytes_or_fetch(self):
        path = shop.destination(self.entry['path'])
        path.parent.mkdir(parents=True)
        path.write_bytes(b'changed')
        with patch.object(shop, 'download') as download, self.assertRaises(ValueError):
            shop.restore(self.entry)
        download.assert_not_called()
        self.assertEqual(path.read_bytes(), b'changed')

    def test_download_checksum_failure_leaves_no_output(self):
        with patch.object(shop, 'download', return_value=b'wrong'), self.assertRaises(ValueError):
            shop.restore(self.entry)
        self.assertFalse(shop.destination(self.entry['path']).exists())

    def test_valid_restore_and_offline_reuse(self):
        self.load(self.source)
        with patch.object(shop, 'download', return_value=b'original') as download:
            shop.restore(self.entry)
            shop.restore(self.entry)
        download.assert_called_once()
        self.assertEqual(shop.destination(self.entry['path']).read_bytes(), b'original')


if __name__ == '__main__':
    unittest.main()
