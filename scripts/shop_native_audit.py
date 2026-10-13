"""Audit N0's real LightBurn saves, without using the Nestbolt importer.

Requires the corpus ezdxf environment. This is collection evidence, not H1/H2/H3.
The five native legacy line exports are intentionally retained byte for byte,
including their serialization defect; parser failures are recorded, not hidden.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import logging
from pathlib import Path
import xml.etree.ElementTree as E

import ezdxf
from ezdxf import bbox
from shop_sources import CORPUS, ROOT, load_lock


def value_map(element):
    return {c.tag: c.get('Value') for c in element if c.get('Value') is not None}


def signature(node, vertices, primitives, top=True):
    """Compare the actual duplicated geometry, resolving native shared lists."""
    attrs = {k: v for k, v in node.attrib.items() if k not in ('VertID', 'PrimID')}
    children = [(c.tag, signature(c, vertices, primitives, False)) for c in node
                if c.tag not in ('VertList', 'PrimList') and not (top and c.tag == 'XForm')]
    for tag, key, definitions in [('VertList', 'VertID', vertices), ('PrimList', 'PrimID', primitives)]:
        if key in node.attrib:
            children.append((tag, definitions[node.get(key)]))
        elif node.find(tag) is not None:
            children.append((tag, ''.join(node.find(tag).itertext()).strip()))
    return attrs, (node.text or '').strip(), children


def project_audit(path):
    root = E.parse(path).getroot()
    shapes = list(root.iter('Shape'))
    vectors = {value_map(c)['index']: c for c in root.findall('CutSetting')}
    images = root.findall('CutSetting_Img')
    bitmaps = [s for s in shapes if s.get('Type') == 'Bitmap']
    texts = [s for s in shapes if s.get('Type') == 'Text']
    vertices = {s.get('VertID'): s.findtext('VertList').strip() for s in shapes
                if s.get('VertID') is not None and s.find('VertList') is not None}
    primitives = {s.get('PrimID'): s.findtext('PrimList').strip() for s in shapes
                  if s.get('PrimID') is not None and s.find('PrimList') is not None}
    source, duplicate = root.findall('Shape')[-2:]
    cut = value_map(vectors['0'])
    checks = {
        'native_version': root.get('AppVersion') == '2.1.01' and root.get('FormatVersion') == '1',
        'cut_score_engrave_tool': {i: vectors[i].get('type') for i in ['0','1','2','30']}
                                  == {'0': 'Cut', '1': 'Cut', '2': 'Scan', '30': 'Tool'},
        'kerf_and_leads': all(cut.get(k) == v for k, v in {
            'kerf': '0.2', 'leadIn': '1', 'leadStyle': 'arc', 'leadLength': '3', 'leadAngle': '45'}.items()),
        'text_with_backup': len(texts) == 1 and texts[0].find('BackupPath') is not None,
        'three_shared_images': len(bitmaps) == 3 and len({s.get('SourceHash') for s in bitmaps}) == 1
                               and sum(bool(s.get('Data')) for s in bitmaps) == 1,
        'image_setting_index_collision': len(images) == 1 and value_map(images[0])['index'] == '0',
        'start_point': any(s.get('StartV') == '2' for s in shapes),
        'source_copy_geometry_equal': signature(source, vertices, primitives) == signature(duplicate, vertices, primitives),
        'source_copy_transform_differs': source.findtext('XForm') != duplicate.findtext('XForm'),
        'shared_geometry_resolves': all(s.get('VertID') in vertices for s in shapes if 'VertID' in s.attrib)
                                    and all(s.get('PrimID') in primitives for s in shapes if 'PrimID' in s.attrib),
    }
    return {'checks': checks, 'shape_types': dict(Counter(s.get('Type') for s in shapes)),
            'top_level_types': [s.get('Type') for s in root.findall('Shape')],
            'source_xform': source.findtext('XForm'), 'duplicate_xform': duplicate.findtext('XForm')}


def dxf_audit(path):
    lines = path.read_text(encoding='utf-8').splitlines()
    tags = Counter(v.strip() for k, v in zip(lines[::2], lines[1::2]) if k.strip() == '0')
    result = {'raw_entity_markers': dict(tags), 'reader_warnings': []}
    class CaptureWarnings(logging.Handler):
        def emit(self, record):
            result['reader_warnings'].append(record.getMessage())
    logger = logging.getLogger('ezdxf')
    handler = CaptureWarnings(level=logging.WARNING)
    logger.addHandler(handler)
    try:
        doc = ezdxf.readfile(path)
        bounds = bbox.extents(doc.modelspace())
        result.update({'parses': True, 'version': doc.dxfversion, 'units': doc.units,
                       'entity_types': dict(Counter(e.dxftype() for e in doc.modelspace())),
                       'layers': dict(Counter(e.dxf.layer for e in doc.modelspace())),
                       'bounds_mm': [*tuple(bounds.extmin)[:2], *tuple(bounds.extmax)[:2]]})
    except (ezdxf.DXFError, ValueError, IndexError) as ex:
        result.update({'parses': False, 'error': f'{type(ex).__name__}: {ex}'})
    finally:
        logger.removeHandler(handler)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'benchmarks/results/n0-native-20261013.json')
    args = parser.parse_args()
    recipe = json.loads((CORPUS/'native/recipe.json').read_text(encoding='utf-8'))
    rows, checks = [], {}
    for design in recipe['designs']:
        stem = CORPUS/'native'/design['id']
        project = project_audit(stem.with_suffix('.lbrn2'))
        dxf = dxf_audit(stem.with_suffix('.dxf'))
        svg = E.parse(stem.with_suffix('.svg')).getroot()
        x, y, w, h = map(float, svg.get('viewBox').split())
        expected = [x, -(y+h), x+w, -y]
        delta = max(abs(a-b) for a, b in zip(expected, dxf['bounds_mm'])) if dxf['parses'] else None
        extra = stem.with_name(stem.name+'-lines.dxf')
        rows.append({'id': design['id'], 'project': project, 'dxf': dxf,
                     'svg_bounds_mm': expected, 'dxf_svg_max_bbox_difference_mm': delta,
                     'lines_dxf': dxf_audit(extra) if extra.exists() else None})
        checks[design['id']+'_native_features'] = all(project['checks'].values())
        checks[design['id']+'_standard_dxf_parses'] = dxf['parses']
        checks[design['id']+'_source_unchanged'] = sha256((CORPUS/design['source']).read_bytes()).hexdigest() == design['source_sha256']
    checks['fifteen_projects'] = len(rows) == 15
    checks['five_native_lines_exports'] = sum(r['lines_dxf'] is not None for r in rows) == 5
    checks['native_lines_defect_recorded'] = all(not r['lines_dxf']['parses'] and
        'Expected DXF entity POLYLINE or SEQEND' in r['lines_dxf']['error'] for r in rows if r['lines_dxf'])
    tool = E.parse(CORPUS/'native/tool-layer-enabled.lbrn2').getroot()
    checks['tool_import_option_probe'] = [s.get('CutIndex') for s in tool.findall('Shape')] == ['5','30']
    lock = load_lock(CORPUS/'sources.lock.json')
    counts = Counter(f.get('set', 'real') for s in lock['sources'] for f in s['files'])
    result = {'recorded_at': datetime.now(timezone.utc).isoformat(), 'scope': 'N0 collection and native writer audit only',
              'H1': False, 'H2': False, 'H3': False, 'completed_milestone_weight_percent': 0,
              'independent_parser': 'ezdxf '+ezdxf.__version__, 'source_counts': dict(counts),
              'native_outputs': 3*len(rows)+sum(r['lines_dxf'] is not None for r in rows),
              'checks': checks, 'collection_checks_pass': all(checks.values()), 'files': rows,
              'remaining': ['independent labels and renders', 'generated habits', 'stratified held-out split and H1 freeze',
                            'N1-N5 implementation and all remaining gates']}
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'collection_checks_pass': result['collection_checks_pass'],
                      'failed': [k for k,v in checks.items() if not v], 'native_outputs': result['native_outputs'],
                      'bbox_max_mm': max(r['dxf_svg_max_bbox_difference_mm'] for r in rows),
                      'source_counts': dict(counts)}))
    if not result['collection_checks_pass']: raise SystemExit(1)


if __name__ == '__main__':
    main()
