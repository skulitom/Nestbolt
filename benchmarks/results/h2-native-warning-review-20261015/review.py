"""Read-only diagnostic coverage review of all frozen training native labels."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'benchmarks/results'
CORPUS = ROOT/'benchmarks/datasets/shop'
AUDIT = BASE/'h3-reviewed-prerequisites-20261015T204219Z/results.json'
ARCHIVE = BASE/'h3-missing-layer-native-20261015/raw.zip'
OUT = BASE/'h2-native-warning-review-20261015'
load = lambda p: json.loads(p.read_bytes())
digest = lambda p: sha256(p.read_bytes()).hexdigest()

def covered(category, warnings):
    text = '\n'.join(warnings).lower()
    rules = {
        'fixed_tool_or_output_disabled_shapes': 'tool/output-off shapes stay at their original positions' in text,
        'bounding_rectangle_proxy': any(p in text for p in ['bounding rectangle', 'bounding-rectangle', 'bounding box']),
        'engraving_inside_multiple_outlines_smallest_selected': 'inside several cutting outlines' in text and 'smallest' in text,
        'text_without_backup_path': 'no backuppath' in text and 're-save' in text,
        'zero_area_proxy': 'zero' in text and any(p in text for p in ['bounds', 'rectangle', 'width', 'height']),
        'missing_bezier_control_points_native_line_fallback': 'control' in text and 'line' in text,
        # The reader does not query installed fonts. A useful portable diagnostic
        # should describe cached outline use, without claiming a local font is absent.
        'font_missing_native_backup_used': any(p in text for p in ['cached', 'backup']) and any(p in text for p in ['font', 'text']),
        'no_movable_shapes': False,
        'rigid_group_contains_fixed_shapes': False,
    }
    assert category in rules, category
    return rules[category]

assert digest(CORPUS/'manifest.json') == '02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
manifest = load(CORPUS/'manifest.json')
training = {r['path']: r for r in manifest['files'] if r['split']=='training'
    and Path(r['path']).suffix in ['.lbrn', '.lbrn2']}
assert len(training) == 56
audit = load(AUDIT)
originals = [r for r in audit['rows'] if r['kind']=='original']
assert {r['path'] for r in originals} == set(training)
assert audit['all_checked'] and audit['source_guards_passed'] and not audit['held_out_geometry_read']
changes = subprocess.check_output(['git', 'diff', '--name-only', '5fb6b5a', 'HEAD', '--', 'crates', 'web/src'], cwd=ROOT, text=True).splitlines()
assert set(changes) == {'crates/core/src/separate.rs', 'crates/core/src/separate/score.rs'}
integrity = load(ARCHIVE.with_name('integrity.json'))
assert digest(ARCHIVE) == integrity['sha256']
rows = []
counts = Counter()
with zipfile.ZipFile(ARCHIVE) as z:
    for original in originals:
        source = training[original['path']]
        assert digest(CORPUS/source['label']) == source['label_sha256']
        label = load(CORPUS/source['label'])
        row = {'path': original['path'], 'label': source['label'],
            'source_sha256': source['sha256'], 'label_sha256': source['label_sha256'],
            'public_import': original['public_import'], 'expected_warnings': label.get('expected_warnings', [])}
        if original['public_import'] == 'imported':
            member = original['folder']+'/library.json'
            raw = z.read(member)
            expected = original['artifacts']['library.json']
            assert sha256(raw).hexdigest() == expected == integrity['members'][member]['sha256']
            library = json.loads(raw)
            row.update(archive_member=member, library_sha256=expected, warnings=library['warnings'])
            row['coverage'] = {c: covered(c, library['warnings']) for c in row['expected_warnings']}
            row['missing_categories'] = [c for c, ok in row['coverage'].items() if not ok]
            for c, ok in row['coverage'].items():
                counts[c+(':covered' if ok else ':missing')] += 1
        else:
            row.update(rejection_kind=original['rejection_kind'], error=original['import_error'])
            row['clear_rejection'] = original['rejection_kind'] in [
                'approved-text-prerequisite', 'approved-mixed-group', 'no-movable-units']
            assert row['clear_rejection']
            for c in row['expected_warnings']:
                counts[c+':rejected_before_warning_check'] += 1
        rows.append(row)
missing = [r for r in rows if r.get('missing_categories')]
report = {'scope': __doc__, 'H2_complete': False, 'held_out_geometry_read': False,
    'new_imports_or_searches': 0, 'new_product_changes': False,
    'evidence_product_commit': '5fb6b5a',
    'review_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'code_changes_since_evidence': changes, 'importer_and_public_warning_code_unchanged': True,
    'audit': AUDIT.relative_to(ROOT).as_posix(), 'audit_sha256': digest(AUDIT),
    'archive': ARCHIVE.relative_to(ROOT).as_posix(), 'archive_sha256': integrity['sha256'],
    'original_training_projects': len(rows),
    'imported': sum(r['public_import']=='imported' for r in rows),
    'clear_rejections': sum(r.get('clear_rejection',False) for r in rows),
    'imported_projects_missing_expected_diagnostics': len(missing),
    'category_counts': dict(sorted(counts.items())), 'rows': rows,
    'interpretation': 'Diagnostic message coverage only. Missing messages are not missing geometry, failed H3 preservation, or a relaxed label. Native font availability is not inferred; describe cached outlines truthfully. Original rejections remain rejections.'}
OUT.mkdir()
(OUT/'review.py').write_bytes(Path(__file__).read_bytes())
(OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
print(json.dumps([{'label':r['label'],'missing':r['missing_categories']} for r in missing],indent=2))
