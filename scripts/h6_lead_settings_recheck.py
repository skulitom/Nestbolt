"""Recheck/export both lead styles on the retained authored searched layout."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import xml.etree.ElementTree as E

from h2_import_audit import source_digest
from h2_lightburn_prepare import run, write_json
from h6_lead_settings_prepare import ROOT, digest


def cut_paths(path):
    root = E.parse(path).getroot()
    return [p.attrib for g in root if g.get('id') == 'CUT' for p in g]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--attempt', default='revised')
    args = parser.parse_args()
    folder = args.folder.resolve()
    assert folder.is_relative_to(ROOT/'benchmarks/results')
    target = folder/args.attempt
    assert target.resolve().is_relative_to(folder)
    target.mkdir(exist_ok=False)
    original = json.loads((folder/'preparation.json').read_text(encoding='utf-8'))
    for path, want in original['artifacts'].items():
        assert digest(folder/path) == want
    before = source_digest()
    binary = ROOT/'target/release/nestbolt.exe'
    binary_hash = digest(binary)
    rows = []
    # Reuse an actual searched layout, with no movement or new solver run.
    layout = folder/'arc/layout.json'
    for style in ['line', 'arc']:
        out = target/style
        out.mkdir()
        args = ['--library', folder/'library.json', '--request', folder/f'{style}-request.json',
                '--layout', layout]
        report = json.loads(run([binary, 'validate', *args]))
        write_json(out/'report.json', report)
        leads = report['lead_in']
        assert report['valid'] and leads['validation']['valid']
        assert (leads['expected_contours'], leads['reserved_contours'], leads['flagged_contours']) == (6, 4, 2)
        assert all(sum(r['shortened'] for r in p['reservations']) == 1
                   and all(abs(r['length_mm']*10-round(r['length_mm']*10)) < 1e-9
                           for r in p['reservations']) for p in leads['parts'])
        exported = run([binary, 'export', *args, '--out-dir', out, '--sheet-outline', 'false'])
        (out/'export.log').write_text(exported, encoding='utf-8', newline='\n')
        assert cut_paths(out/'sheet-0.svg') == cut_paths(folder/'arc/sheet-0.svg')
        rows.append({'style': style, 'lengths_mm': [[r['length_mm'] for r in p['reservations']]
                                                  for p in leads['parts']],
                     'cut_svg_attributes_unchanged': True})
    assert source_digest() == before and digest(binary) == binary_hash
    write_json(target/'preparation.json', {
        'date': datetime.now(timezone.utc).isoformat(), 'held_out_read': False,
        'scope': 'New standalone validation/export on the original actual searched arc layout; no solver rerun',
        'source_sha256': before, 'binary_sha256': binary_hash, 'runner_sha256': digest(Path(__file__)),
        'layout': str(layout.relative_to(folder)), 'cpu_affinity': [0], 'cases': rows,
        'artifacts': {p.relative_to(folder).as_posix(): digest(p)
                      for p in sorted(target.rglob('*')) if p.is_file()}})
    print(json.dumps(rows))


if __name__ == '__main__':
    main()
