"""Refresh collection provenance only; never create a split or assert H1.

Original real-file writer investigations are retained. Native derivative history
comes from the explicit GUI recipe, not from trusting AppVersion alone.
"""
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as E
from shop_sources import CORPUS, load_lock


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def main():
    target = CORPUS/'manifest.draft.json'
    old = json.loads(target.read_text(encoding='utf-8'))
    if old['state'] != 'draft-not-frozen' or (CORPUS/'manifest.json').exists():
        raise ValueError('The frozen manifest must never be changed by this collector')
    existing = {r['path']: r for r in old['files']}
    lock = load_lock(CORPUS/'sources.lock.json')
    rows = []
    for source in lock['sources']:
        for item in source['files']:
            if item['path'] in existing:
                row = existing[item['path']]
                if row['sha256'] != item['sha256']:
                    raise ValueError('A recorded source changed: '+item['path'])
                rows.append(row)
                continue
            kind = item.get('set', 'real')
            writer = {'name': 'Unknown', 'evidence': 'No writer attribution inferred from the DXF version; source test-suite provenance is recorded separately.'}
            if kind == 'public-lightburn':
                root = E.parse(CORPUS/item['path']).getroot()
                writer = {'name': 'LightBurn-format public project', 'evidence':
                          'Publicly distributed XML; AppVersion is a format claim, not proof that the application wrote these bytes.',
                          'app_version_attribute': root.get('AppVersion'), 'format_version_attribute': root.get('FormatVersion')}
                if source['repository'] == 'MarcinZukowski/lightburn-tester':
                    writer['name'] = 'lightburn-tester generator'
                    writer['evidence'] = 'Source README explicitly documents the commands generating the two example .lbrn projects.'
                if source['repository'] == 'jlucaso1/lbrn2-to-svg':
                    writer['name'] = 'lbrn2-to-svg minimized fixture'
            elif kind == 'oracle-svg':
                writer = {'name': 'lbrn2-to-svg expected SVG fixture', 'evidence': 'Paired test artifact from the same pinned MIT source.'}
            rows.append({'path': item['path'], 'set': kind, 'source': item['source_url'],
                         'licence': source['licence'], 'licence_evidence': [e['source_url'] for e in source['evidence']],
                         'sha256': item['sha256'], 'writer': writer, 'label': None, 'split': None,
                         'expectation': 'imports_or_fails_clearly_within_10s' if kind == 'robustness' else None})
    source_rows = {r['path']: r for r in rows}
    recipe = json.loads((CORPUS/'native/recipe.json').read_text(encoding='utf-8'))
    native_rows = []
    for design in recipe['designs']:
        parent = source_rows[design['source']]
        names = [design['id']+ext for ext in ['.lbrn2', '.dxf', '.svg']]
        if design['id'] in ['lb-01','lb-02','lb-03','lb-04','lb-05']:
            names.append(design['id']+'-lines.dxf')
        for name in names:
            relative = 'native/'+name
            native_rows.append({'path': relative, 'set': 'lightburn-native',
                'source': parent['source'], 'derived_from': design['source'], 'lineage': design['source'],
                'licence': parent['licence'], 'licence_evidence': parent['licence_evidence'],
                'modification_notice': 'Nestbolt test derivative: LightBurn import, duplicate, reposition, original feature coupon, native save/export. Source licence retained.',
                'sha256': sha256((CORPUS/relative).read_bytes()).hexdigest(),
                'writer': {'name': 'LightBurn 2.1.01', 'evidence': 'Hidden Anode desktop native GUI; native/recipe.json and benchmarks/results/n0-native-20261013.md',
                           'export': 'Convert Arcs to Lines' if '-lines.dxf' in name else 'native project' if name.endswith('.lbrn2') else 'default Export Arcs / SVG'},
                'label': existing.get(relative, {}).get('label'), 'split': None})
    auxiliaries = []
    for name, writer in [('feature-coupon-input.lbrn2', 'Agent preparation from original MIT probes'),
                         ('tool-layer-enabled.lbrn2', 'LightBurn 2.1.01 native GUI re-import of original palette-truecolor.dxf')]:
        path = 'native/'+name
        auxiliaries.append({'path': path, 'set': 'format-probe', 'licence': 'MIT',
                            'licence_location': 'LICENSE (repository root)', 'source': 'Original Nestbolt test drawing',
                            'writer': writer, 'counts_towards_H1_native': False,
                            'sha256': sha256((CORPUS/path).read_bytes()).hexdigest()})
    write_json(CORPUS/'native/manifest.json', {'state': 'draft-not-frozen', 'files': native_rows+auxiliaries})
    write_json(target, {'state': 'draft-not-frozen', 'files': rows+native_rows,
                        'note': 'Labels, generated cases and held-out freeze are not yet complete. No N1 changes allowed.'})
    print(json.dumps({'source_files': len(rows), 'native_derivatives': len(native_rows), 'auxiliary_probes': len(auxiliaries), 'H1': False}))


if __name__ == '__main__':
    main()
