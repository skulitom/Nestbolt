"""Audit the saved early N0/N2 evidence; this does not assert H1 or H3."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from shop_sources import CORPUS, ROOT, load_lock


def canonical(element):
    return ET.canonicalize(ET.tostring(element, encoding='unicode'), strip_text=True)


def project(name):
    return ET.parse(CORPUS / 'probes' / name).getroot()


def values(element):
    return {child.tag: child.get('Value') for child in element if child.get('Value') is not None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'benchmarks/results/n0-n2-initial-20261013.json')
    parser.add_argument('--git-index', action='store_true', help='Also verify staged source/probe bytes, without line-ending conversion')
    args = parser.parse_args()
    checks = {}
    lock = load_lock(CORPUS / 'sources.lock.json')
    entries = [x for s in lock['sources'] for x in [*s['files'], *s['evidence']]]
    checks['reviewed_source_bytes'] = all(sha256((CORPUS/x['path']).read_bytes()).hexdigest() == x['sha256'] for x in entries)
    provenance = json.loads((CORPUS/'probes/manifest.json').read_text(encoding='utf-8'))['files']
    checks['probe_provenance_bytes'] = all(sha256((CORPUS/x['path']).read_bytes()).hexdigest() == x['sha256'] for x in provenance)
    if args.git_index:
        checks['git_preserves_all_original_bytes'] = all(
            sha256(subprocess.check_output(['git', 'show', ':'+(CORPUS/x['path']).relative_to(ROOT).as_posix()], cwd=ROOT)).hexdigest() == x['sha256']
            for x in [*entries, *provenance])
    flags = {'bottom-left': ('False', 'False'), 'top-left': ('False', 'True'),
             'top-right': ('True', 'True'), 'bottom-right': ('True', 'False')}
    origins = {name: project(f'origin-{name}.lbrn2') for name in flags}
    checks['origin_flags'] = all((r.get('MirrorX'), r.get('MirrorY')) == flags[name] for name, r in origins.items())
    shapes = [[canonical(s) for s in r.findall('Shape')] for r in origins.values()]
    checks['origin_shape_subtrees_equal'] = all(s == shapes[0] for s in shapes)
    r = origins['bottom-left']
    paths = [x for x in r.findall('Shape') if x.get('Type') == 'Path']
    checks['independent_primitive_sharing'] = (paths[0].get('PrimID') == paths[1].get('PrimID')
        and paths[0].get('VertID') != paths[1].get('VertID')
        and paths[0].find('PrimList') is not None and paths[1].find('PrimList') is None)
    features = project('features-before-leads.lbrn2')
    bitmaps = [x for x in features.iter('Shape') if x.get('Type') == 'Bitmap']
    checks['bitmap_sharing'] = (len(bitmaps) == 3 and all(x.get('SourceHash') == '0' for x in bitmaps)
        and bool(bitmaps[0].get('Data')) and all(x.get('Data') is None for x in bitmaps[1:]))
    text = next(x for x in features.findall('Shape') if x.get('Type') == 'Text')
    checks['editable_text_backup'] = text.get('HasBackupPath') == '1' and text.find('BackupPath') is not None
    for kind in ['line', 'arc']:
        layer = project(f'features-{kind}-leads.lbrn2').find('CutSetting')
        v = values(layer)
        checks[f'{kind}_lead_fields'] = all(v.get(k) == value for k, value in {
            'leadStyle': kind, 'leadIn': '1', 'leadLength': '3', 'leadAngle': '45',
            'speed': '20', 'maxPower': '35', 'kerf': '0.2'}.items())
    modes = project('layer-modes.lbrn2')
    scan = next(x for x in modes.findall('CutSetting') if x.get('type') == 'Scan')
    checks['fill_cut_sublayer'] = any(s.get('type') == 'Cut' for s in scan.findall('SubLayer'))
    checks['image_vector_index_collision'] = (modes.find('CutSetting/index').get('Value')
        == modes.find('CutSetting_Img/index').get('Value') == '0')
    checks['tool_and_offset_types'] = {'Tool', 'Offset'} <= {x.get('type') for x in modes.findall('CutSetting')}
    before, after = project('start-before.lbrn2'), project('start-after.lbrn2')
    changed = [s for s in after.findall('Shape') if s.get('StartV') is not None]
    checks['explicit_start_vertex'] = len(changed) == 1 and changed[0].get('StartV') == '2'
    if len(changed) == 1:
        del changed[0].attrib['StartV']
    for r in [before, after]:
        for thumb in r.findall('Thumbnail'):
            r.remove(thumb)
    checks['only_startv_and_thumbnail_changed'] = canonical(before) == canonical(after)
    native_palette = project('palette-dxf-reimport.lbrn2')
    checks['dxf_t1_becomes_c05'] = {values(s)['index'] for s in native_palette.findall('CutSetting')} == {'0','1','2','5'}
    true_palette = project('palette-truecolor-reimport.lbrn2')
    checks['truecolor_does_not_preserve_tool_layer'] = {values(s)['index'] for s in true_palette.findall('CutSetting')} == {'5','13'}
    raw = (CORPUS/'probes/palette.dxf').read_text(encoding='utf-8').splitlines()
    pairs = list(zip(raw[::2], raw[1::2]))
    header = {pairs[i][1].strip():pairs[i+1][1].strip() for i in range(len(pairs)-1) if pairs[i][0].strip() == '9'}
    checks['modern_dxf_mm'] = header.get('$ACADVER') == 'AC1021' and header.get('$INSUNITS') == '4'
    manifest = json.loads((CORPUS/'manifest.draft.json').read_text(encoding='utf-8'))
    source_files = [x for s in lock['sources'] for x in s['files'] if x.get('set', 'real') == 'real']
    result = {'recorded_at': datetime.now(timezone.utc).isoformat(),
              'scope': 'Initial N0 collection and N2 native format probes; no gate pass',
              'completed_milestone_weight_percent': 0, 'H1': False, 'H3': False,
              'counts': {'sources': sum(any(x.get('set', 'real') == 'real' for x in s['files']) for s in lock['sources']), 'real': len(source_files),
                         'formats': dict(Counter(Path(x['path']).suffix for x in source_files)),
                         'fusion_fingerprints': sum(x['writer']['name'] == 'Fusion 360' for x in manifest['files'])},
              'app_version': '2.1.01', 'title_bar_edition': 'Pro', 'checks': checks,
              'git_index_checked': args.git_index,
              'checks_pass': all(checks.values()),
              'probe_sha256': {p.relative_to(CORPUS).as_posix():sha256(p.read_bytes()).hexdigest()
                               for p in sorted((CORPUS/'probes').iterdir()) if p.is_file()},
              'remaining': ['H1 labelled LightBurn derivatives/exports, public and robustness samples, generated habits, labels, split and freeze',
                            'N2 reader/writer, independent oracle, validation, native nesting checks and all surfaces'],
              'method_notes': ['Native UI files, not reverse engineering.',
                               'Some UI accessibility actions acknowledged changes without completing dependent control updates; saved XML was checked and mouse controls used to obtain final values.',
                               'DXF inspection initially attempted dict(HeaderSection), which ezdxf rejects; read the original header pairs instead. No drawing bytes changed.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'checks_pass': result['checks_pass'], 'failed': [k for k,v in checks.items() if not v], 'counts': result['counts']}))
    if not result['checks_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
