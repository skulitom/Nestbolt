"""Compare a completed training-only reader/writer audit with frozen labels.

Membership comes from the product's actual nesting units. Physical cut holes
come from independent GEOS polygonization of original Scene curves, excluding
Text/Scan artwork inside groups as defined by the frozen labels. Collision
union holes are not physical cut holes. No corpus authoring or held-out reads.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import traceback

from h3_geometry_audit import product_paths
from maker_geometry import flatten_segment
from shop_reference_labels import topology

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def cutting(scene, shape):
    layer = next((l for l in scene['layers'] if l['index'] == shape['cut_index']
                  and l['image'] == shape['image_layer']), None)
    return not shape['fixed'] and (layer['cuts'] and layer['output'] if layer else
                                  not shape['image_layer'] and shape['cut_index'] < 30)


def leaves(scene, index):
    shape = scene['shapes'][index]
    if shape['kind'] == 'Group':
        for child in shape['children']:
            yield from leaves(scene, child)
    else:
        yield shape


def holes(scene, members):
    tops = [scene['shapes'][scene['top_level'][i]] for i in members]
    # A top-level cutting shape owns contained text, images and engraving.
    roots = [s for s in tops if s['kind'] not in ['Text', 'Bitmap'] and cutting(scene, s)
             and s['paths'] and all(p['closed'] for p in s['paths'])]
    root = roots[0] if roots else tops[0]
    assert len(roots) <= 1
    if root['kind'] == 'Group':
        index = scene['top_level'][root['top_level']]
        selected = [s for s in leaves(scene, index) if cutting(scene, s) and s['kind'] != 'Text']
    elif root['kind'] not in ['Text', 'Bitmap'] and root['paths'] and all(p['closed'] for p in root['paths']):
        selected = [root]
    else:
        return 0
    network = []
    for shape in selected:
        for curve in product_paths(shape):
            points = [z for segment in curve for z in flatten_segment(segment, .0002)[:-1]]
            if curve:
                points.append(curve.end)
            network.append({'points': [(z.real, z.imag) for z in points]})
    return sum(p['holes'] for p in topology(network)['cut_parts'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('audit', type=Path)
    args = parser.parse_args()
    assert digest(CORPUS/'manifest.json') == '02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7'
    manifest = json.loads((CORPUS/'manifest.json').read_bytes())
    training = {r['path']: r for r in manifest['files'] if r['split'] == 'training'}
    audit = json.loads(args.audit.read_bytes())
    assert audit['all_checked'] and audit['source_guards_passed'] and not audit['held_out_geometry_read']
    rows = []
    for original in audit['rows']:
        path = original.get('original', original['path'])
        source = training[path]  # Refuse any held-out row before reading it.
        assert digest(CORPUS/source['label']) == source['label_sha256']
        label = json.loads((CORPUS/source['label']).read_bytes())
        row = {'path': original['path'], 'kind': original['kind'], 'label': source['label'],
               'label_sha256': source['label_sha256'], 'public_import': original['public_import']}
        rows.append(row)
        if original['public_import'] != 'imported':
            row['rejection_kind'] = original['rejection_kind']
            continue
        try:
            folder = ROOT/original['folder']
            for name in ['inspect-stdout.json', 'writer-stdout.json', 'library.json']:
                assert digest(folder/name) == original['artifacts'][name]
            scene = json.loads((folder/'inspect-stdout.json').read_bytes())['scene']
            nesting = json.loads((folder/'writer-stdout.json').read_bytes())['nesting']
            expected = {tuple(sorted(p['top_level_shape_indices'])): p['holes'] for p in label['cut_parts']}
            actual = {tuple(sorted(u['members'])): holes(scene, u['members']) for u in nesting['units']}
            assert len(actual) == len(nesting['units']) and len(expected) == len(label['cut_parts'])
            row['expected'] = [{'members': list(k), 'holes': v} for k, v in sorted(expected.items())]
            row['actual'] = [{'members': list(k), 'holes': v} for k, v in sorted(actual.items())]
            row['membership_matches'] = set(actual) == set(expected)
            row['physical_cut_holes_match'] = actual == expected
            row['expected_fixed'] = sorted(s['top_level_shape_index'] for s in label.get('fixed_shapes', []))
            row['actual_fixed'] = sorted(nesting['fixed'])
            row['fixed_matches'] = row['expected_fixed'] == row['actual_fixed']
            row['expected_cut_layers'] = label['cut_layers']
            row['actual_cut_layers'] = sorted({s['cut_index'] for s in scene['shapes'] if s['kind'] != 'Group' and cutting(scene, s)})
            row['cut_layers_match'] = row['actual_cut_layers'] == row['expected_cut_layers']
            row['passed'] = all(row[k] for k in ['membership_matches', 'physical_cut_holes_match', 'fixed_matches', 'cut_layers_match'])
        except Exception:
            row['error'] = traceback.format_exc()
            row['passed'] = False
        print(original['kind'], source['label'], row['passed'], flush=True)
        write(args.audit.parent/'label-progress.json', rows)
    summary = {kind: {k: sum(r.get(k, False) for r in rows if r['kind'] == kind)
                         for k in ['membership_matches', 'physical_cut_holes_match', 'fixed_matches', 'cut_layers_match', 'passed']}
               for kind in ['original', 'native-repair']}
    write(args.audit.parent/'labels.json', {'scope': __doc__, 'audit': str(args.audit),
        'audit_sha256': digest(args.audit), 'script_sha256': digest(Path(__file__)),
        'held_out_geometry_read': False, 'summary': summary, 'rows': rows})
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
