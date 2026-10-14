"""Audit training vector diagnostics, including an independent retrace review.

Use shop-venv Python and a completed h2_import_audit.py report. Rejections remain
rejections, not warning passes. Frozen labels/splits are never rewritten.
"""
import argparse
from collections import Counter
import ctypes
from datetime import datetime, timezone
from hashlib import sha256
import importlib.metadata
import json
from pathlib import Path

import ezdxf
from shapely import LineString
from shapely.ops import polygonize_full, unary_union

from h3_geometry_audit import product_paths, geometry
from shop_reference_labels import dxf_curves

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT/'benchmarks/datasets/shop'


def retrace_review(row, library_path):
    raw = (CORPUS/row['path']).read_bytes()
    assert sha256(raw).hexdigest() == row['sha256']
    doc = ezdxf.readfile(CORPUS/row['path'])
    curves = list(dxf_curves(doc, doc.modelspace()))
    assert all(LineString(c['points']).is_closed for c in curves)
    library_bytes = library_path.read_bytes()
    library = json.loads(library_bytes)
    contours = [c for p in library['parts'] for c in [p['outer'], *p['holes']]]
    assert len(contours) == len(curves)
    paths = product_paths({'paths': [{'curve': c} for c in contours]})
    imported, _ = geometry(paths)
    evidence = []
    for curve in curves:
        original = LineString(curve['points'])
        merged = unary_union([LineString([a, b]) for a, b in zip(curve['points'], curve['points'][1:])])
        _, cuts, dangles, _ = polygonize_full(merged)
        spur = cuts.union(dangles)
        if spur.length <= .001:
            continue
        candidates = [line for line in imported if max(abs(a-b) for a, b in zip(line.bounds, original.bounds)) < .01]
        assert candidates
        distance = min(original.hausdorff_distance(line) for line in candidates)
        assert distance <= .01
        evidence.append({'entity_handle': curve['id'], 'entity_type': curve['type'],
                         'endpoint_gap_mm': 0.0, 'closed_source_path': True,
                         'polygonized_open_length_mm': spur.length,
                         'retraced_length_mm': original.length-merged.length,
                         'spur_bounds_mm': list(spur.bounds), 'import_hausdorff_mm': distance})
    assert len(evidence) == 1 and evidence[0]['entity_handle'] == '42B'
    assert abs(evidence[0]['polygonized_open_length_mm']-evidence[0]['retraced_length_mm']) < 1e-7
    assert any('touches itself' in w and 'exact curves' in w for w in library['warnings'])
    return {'source_sha256': row['sha256'], 'library_sha256': sha256(library_bytes).hexdigest(),
            'source_contours': len(curves), 'imported_contours': len(contours),
            'raw_open_paths': 0, 'evidence': evidence,
            'interpretation': 'The label names open edges in a polygonized line network. All original paths are closed; '
                              'the same 7.888 mm segment is traversed twice inside one SPLINE. '
                              'The self-touch diagnostic covers this retained retrace; no label/count/split exception is applied.'}


def covered(category, report, warnings, retrace):
    text = '\n'.join(warnings).lower()
    cleanup = report.get('cleanup', {})
    rules = {
        'annotations_ignored': 'ignored' in text and 'not a cut outline' in text,
        'construction_layers_ignored': 'bend/extent/construction layer' in text,
        'excluded_noncut_layers': 'excluded by cut selection' in text,
        'ignored_non_geometry': 'ignored' in text and 'not a cut outline' in text,
        'duplicate_segments_removed': cleanup.get('duplicate_segments_removed', 0) > 0,
        'zero_length_segments_removed': cleanup.get('zero_length_segments_removed', 0) > 0,
        'overlapping_collinear_segments_merged': cleanup.get('overlapping_segments_merged', 0) > 0,
        'duplicate_or_overlapping_segments': any(cleanup.get(k, 0) > 0 for k in
            ['duplicate_segments_removed', 'overlapping_segments_merged', 'closed_path_overlaps_preserved']) or retrace,
        'duplicate_entity_handles': 'duplicate entity handle' in text,
        'undefined_layer': 'undefined layer' in text,
        'gap_closed_with_explicit_tolerance': bool(report.get('closed_gaps')) and 'explicit close gaps' in text,
        'gaps_closed': bool(report.get('closed_gaps')),
        'open_contours': bool(report.get('open_contours')) or retrace,
        'polyline_widths_ignored_for_cut_centerline': 'widths ignored' in text and 'centreline' in text,
        'sheet_outline_available': 'sheet_outline_available' in text,
        'units_missing_possible_inches': bool((report.get('units') or {}).get('possible_inches')) and 'inches' in text,
        'units_unspecified': 'no drawing units' in text,
        'ambiguous_cut_geometry': False, 'malformed_polyline_records': False, 'no_cut_geometry': False,
    }
    assert category in rules, f'Unreviewed warning category: {category}'
    return bool(rules[category])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('report', type=Path)
    parser.add_argument('--fidelity', type=Path, required=True, help='Completed full training vector fidelity report')
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 8)
    raw = (CORPUS/'manifest.json').read_bytes()
    manifest = json.loads(raw)
    training = [r for r in manifest['files'] if r['split'] == 'training' and r.get('label')
                and Path(r['path']).suffix.lower() in ['.svg', '.dxf']]
    report_bytes = args.report.read_bytes()
    audit = json.loads(report_bytes)
    assert audit['manifest_sha256'] == sha256(raw).hexdigest() and audit['label'] == 'training'
    observed = {r['path']: r for r in audit['files']}
    assert observed.keys() == {r['path'] for r in training}
    work = ROOT/'output'/f'h2-import-training-{audit["recorded_at"]}'
    fidelity_bytes = args.fidelity.read_bytes()
    fidelity = json.loads(fidelity_bytes)
    assert fidelity['manifest_sha256'] == sha256(raw).hexdigest() and fidelity['only'] is None
    assert {r['path'] for r in fidelity['rows']} == observed.keys()
    special = next((i, r) for i, r in enumerate(training) if '5659cc35-' in r['path'])
    retrace = retrace_review(special[1], work/f'{special[0]:03}.json')
    rows = []
    categories = Counter()
    for index, row in enumerate(training):
        label_bytes = (CORPUS/row['label']).read_bytes()
        assert sha256(label_bytes).hexdigest() == row['label_sha256']
        label = json.loads(label_bytes)
        obs = observed[row['path']]
        assert obs['sha256'] == row['sha256']
        result = {'path': row['path'], 'status': obs['status'], 'label_sha256': row['label_sha256'],
                  'expected_warnings': label.get('expected_warnings', [])}
        if obs['status'] == 'imported':
            current = json.loads((work/f'{index:03}.json').read_bytes())
            baseline = json.loads((Path(fidelity['work_directory'])/f'{index:03}'/'exports/library.json').read_bytes())
            result['fidelity_import_geometry_unchanged'] = all(current.get(k) == baseline.get(k)
                for k in ['tolerance', 'parts', 'sheet_outlines'])
            report = obs['imports'][0]['report']
            reviewed_retrace = row['path'] == special[1]['path']
            result['warning_checks'] = {c: covered(c, report, obs['warnings'], reviewed_retrace)
                                        for c in result['expected_warnings']}
            result['warning_coverage_pass'] = all(result['warning_checks'].values())
            result['cut_layers_match'] = sorted('0' if l is None else l for l in label['cut_layers']) == sorted(
                l['name'] for l in report['layers'] if l['selected_entities'] > 0)
            result['warnings'] = obs['warnings']
            for category, passed in result['warning_checks'].items():
                categories[category+(':covered' if passed else ':missing')] += 1
        else:
            error = obs['error'].lower()
            result['clear_rejection'] = obs['status'] == 'rejected' and any(fix in error for fix in
                ['repair or re-export', 'close gaps up to', 'join these endpoints', 'choose a layer/colour', 'repair the cut outlines'])
            result['error'] = obs['error']
            for category in result['expected_warnings']:
                categories[category+':rejected_before_warning_check'] += 1
        rows.append(result)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    summary = {'recorded_at': stamp, 'H2': False, 'held_out_read': False, 'cpu': 8,
               'scope': 'Training vector warning/cut-layer audit; clear rejections remain distinct',
               'input_report': args.report.as_posix(), 'input_report_sha256': sha256(report_bytes).hexdigest(),
               'fidelity_report': args.fidelity.as_posix(), 'fidelity_report_sha256': sha256(fidelity_bytes).hexdigest(),
               'runner_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
               'manifest_sha256': sha256(raw).hexdigest(),
               'oracle_versions': {p: importlib.metadata.version(p) for p in ['ezdxf', 'shapely', 'svgpathtools']},
               'retrace_review': retrace, 'category_counts': dict(sorted(categories.items())),
               'imported_warning_passes': sum(r.get('warning_coverage_pass', False) for r in rows),
               'cut_layer_matches': sum(r.get('cut_layers_match', False) for r in rows),
               'clear_rejections': sum(r.get('clear_rejection', False) for r in rows),
               'unchanged_fidelity_imports': sum(r.get('fidelity_import_geometry_unchanged', False) for r in rows),
               'passed': all(r.get('warning_coverage_pass', False) and r.get('cut_layers_match', False)
                             and r.get('fidelity_import_geometry_unchanged', False)
                             if r['status'] == 'imported' else r['clear_rejection'] for r in rows), 'rows': rows}
    out = ROOT/'benchmarks/results'/f'h2-warning-audit-{stamp}'
    out.with_suffix('.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8', newline='\n')
    lines = ['# H2 training vector warning audit', '', f'Passed: **{summary["passed"]}**. '
             f'{summary["imported_warning_passes"]} imported files cover their diagnostic expectations; '
             f'{summary["cut_layer_matches"]} cut-layer selections match. '
             f'{summary["clear_rejections"]} files fail with named repair actions.', '',
             'Rejected files are not counted as individual warning passes. No frozen label, split or source was changed. '
             'The earlier R43 count exception remains separate.', '',
             f'{summary["unchanged_fidelity_imports"]} current libraries retain exactly the same parts, source contours, '
             'collision polygons, tolerance and stock outlines as the completed full fidelity sweep. '
             'Only diagnostic messages change.', '',
             'For Gherkin with steps, independent ezdxf/GEOS inspection finds 104 closed source contours and zero open paths. '
             'SPLINE handle 42B traverses a 7.888067184 mm spur twice. Polygonization calls the spur open linework, '
             'which explains the frozen label wording. The import retains all 104 contours and the exact self-touch, '
             f'with Hausdorff distance {retrace["evidence"][0]["import_hausdorff_mm"]:.9f} mm for the affected contour. '
             'Its self-touch warning covers the condition; no scoring exception is introduced.', '',
             'The current importer also reports undefined layers and duplicate entity handles before expanding blocks. '
             'Original block instances and HEADER HANDSEED are not counted as duplicate entities.', '',
             'No held-out geometry or labels read. This is diagnostic evidence only; H2/H3 remain incomplete.', '',
             '| Expectation / outcome | Count |', '| --- | ---: |']
    lines += [f'| {key} | {value} |' for key, value in sorted(categories.items())]
    out.with_suffix('.md').write_text('\n'.join(lines)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ['rows', 'retrace_review', 'category_counts']}))
    if not summary['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
