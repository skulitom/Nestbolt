"""Keep a failed upstream download from bypassing frozen source checksums."""
from hashlib import sha256
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from maker_setup import CONFIG, source_data
import json


class SourceDownloadTests(unittest.TestCase):
    def test_bundled_openclipart_is_the_exact_frozen_download_without_network(self):
        config = json.loads((CONFIG / 'sources.json').read_text(encoding='utf-8'))
        source = config['sources']['openclipart-gear']
        self.assertEqual(source['license'], 'CC0-1.0')
        with patch('maker_setup.fetch', side_effect=AssertionError('network used')):
            data = source_data(source['downloads'][0])
        self.assertEqual(sha256(data).hexdigest(), source['downloads'][0]['sha256'])

    def test_corrupt_local_copy_fails_without_silent_network_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'source.svg').write_bytes(b'changed source')
            download = dict(cache_name='source.svg', url='https://example.invalid/source', sha256=sha256(b'original').hexdigest())
            with patch('maker_setup.fetch', side_effect=AssertionError('network used')):
                with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                    source_data(download, root)

    def test_unbundled_download_still_requires_the_frozen_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            download = dict(cache_name='source.svg', url='https://example.invalid/source', sha256=sha256(b'original').hexdigest())
            with patch('maker_setup.fetch', return_value=b'original') as fetch:
                self.assertEqual(source_data(download, Path(directory)), b'original')
                fetch.assert_called_once_with(download['url'])
            with patch('maker_setup.fetch', return_value=b'changed'):
                with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                    source_data(download, Path(directory))


if __name__ == '__main__':
    unittest.main()
