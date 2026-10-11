"""Offline integrity and coverage checks for the maker freeze."""
from collections import Counter
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import maker_freeze


class MakerFreezeTests(unittest.TestCase):
    def test_coverage_quantities_grain_and_reserved_split(self):
        manifest = json.loads(maker_freeze.MANIFEST.read_bytes())
        rows = manifest['instances']
        self.assertEqual(Counter(r['category'] for r in rows),
                         {'boxes': 8, 'garments': 8, 'lettering': 6, 'mechanical': 12, 'public-art': 6})
        self.assertEqual(Counter(r['category'] for r in rows if r['held_out']),
                         dict.fromkeys(['boxes', 'garments', 'lettering', 'mechanical', 'public-art'], 2))
        sizes, counts = set(), set()
        for row in rows:
            job = json.loads((maker_freeze.DEST / row['path']).read_bytes())
            self.assertEqual(job['mode'], 'all')
            sizes.update((s['width'], s['height']) for s in job['stocks'])
            counts.add(sum(p['quantity'] for p in job['parts']))
            if row['category'] == 'garments':
                for part in job['parts']:
                    self.assertEqual(part['rotations'], {'kind': 'list', 'degrees': [0, 180]})
                    self.assertFalse(part['allow_mirror'])
        self.assertTrue({(300, 200), (600, 400), (1220, 2440), (1250, 2500), (1500, 3000)} <= sizes)
        self.assertTrue({500, 1000, 2000} <= counts)
        self.assertEqual(max(counts), 2000)

    def test_changed_job_curve_or_unlisted_file_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='nestbolt-makers-') as temp:
            dest = Path(temp) / 'datasets'
            shutil.copytree(maker_freeze.DEST, dest)
            with patch.object(maker_freeze, 'DEST', dest), patch.object(maker_freeze, 'MANIFEST', dest / 'makers.json'):
                maker_freeze.check_frozen()
                for path in [next((dest / 'M').glob('*.json')), next((dest / 'maker-assets').rglob('curves.json'))]:
                    original = path.read_bytes()
                    path.write_bytes(original + b' ')
                    with self.assertRaisesRegex(ValueError, 'Frozen maker file changed'):
                        maker_freeze.check_frozen()
                    path.write_bytes(original)
                (dest / 'M/unlisted.json').write_text('{}')
                with self.assertRaisesRegex(ValueError, 'unlisted'):
                    maker_freeze.check_frozen()

    def test_freeze_cannot_replace_an_existing_manifest(self):
        with self.assertRaisesRegex(ValueError, 'already exists'):
            maker_freeze.freeze()
        with self.assertRaisesRegex(ValueError, 'escapes'):
            maker_freeze.safe_path('../outside.json')


if __name__ == '__main__':
    unittest.main()
