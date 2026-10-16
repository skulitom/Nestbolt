"""Prepare current scale sealing with independent fidelity and visual evidence."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root/'output/h4_current_scale_report.py').read_text(encoding='utf-8')
source = source.replace('from io import BytesIO\n', '')
source = source.replace('Current bounded-score build, H4 curves and original G5 scale workflows',
                        'Current depth-three build, H4 curves and original G5 scale workflows')
# Byte identity with a previous solver's selected layout is descriptive, not
# an acceptance condition. The current complete, independent curve check is
# the required fidelity evidence; it handles any valid changed sheet count.
start = source.index("    if fixture == 'curves':\n        prior =")
end = source.index("    paths = sorted(p for p in folder.rglob('*') if p.is_file())", start)
source = source[:start]+source[end:]
source = source.replace("        'previous_scale_comparison': summary.get('previous_scale_comparison')})",
                        "        'exact_curve_fidelity': fidelity if fixture == 'curves' else None})")
before = 'out.mkdir()\n'
after = '''sequence = ROOT/'benchmarks/results/h4-preview-depth-scale-plan-20261016'
terminal = load(sequence/'completed.json')
assert not (sequence/'interruption.json').exists()
assert all(s['exit_code'] == 0 for s in terminal['stages'])
fidelity = load(sequence/'curve-export-fidelity/verification.json')
assert fidelity['all_checks_pass'] and fidelity['both_scale_workflows_pass']
assert fidelity['every_curve_sheet_selected']
assert fidelity['curves'] == 'benchmarks/results/'+args.curves
assert fidelity['g5'] == 'benchmarks/results/'+args.g5
for row in fidelity['records']:
    project = ROOT/row['project']
    checked = load(sequence/'curve-export-fidelity'/(row['browser']+'.json'))
    assert digest(project.read_bytes()) == row['project_sha256'] == checked['project_zip_sha256']
    assert checked['all_checks_pass'] and checked['full_project_checked']
    assert checked['total_placements_checked'] == 2000 and checked['limit_mm'] == 0.01
    assert checked['searches_run'] == 0 and not checked['exports_regenerated']
    assert digest((sequence/'curve-export-fidelity'/(row['browser']+'.json')).read_bytes()) == row['report_sha256']
visual = load(sequence/'visual-review.json')
assert visual['reviewed'] and len(visual['screenshots']) == 4
expected_screens = {f'benchmarks/results/{name}/{browser}/screen.png'
    for name in [args.curves,args.g5] for browser in ['chrome','firefox']}
assert {r['path'] for r in visual['screenshots']} == expected_screens
assert all(r['reviewed'] and digest((ROOT/r['path']).read_bytes()) == r['sha256']
    for r in visual['screenshots'])
out.mkdir()
'''
assert source.count(before) == 1
source = source.replace(before,after)
before = "        assert row['passes'] and row['status'] == 'valid' and not row['affinity_errors']\n"
after = before+'''        assert row['peak_rss_bytes'] < 1500000000 and row['peak_private_bytes'] < 1500000000
        assert row['app']['maximum_event_loop_gap_ms'] <= 200
        task = row['app']['maximum_long_task_ms']
        assert task is None or task <= 200
'''
assert source.count(before) == 1
source = source.replace(before,after)
before = "write(out/'checks.json', report)"
after = "report['visual_review'] = visual\n"+before
assert source.count(before) == 1
source = source.replace(before,after)
target = root/'output/h4_depth_scale_report.py'
assert not target.exists()
compile(source,str(target),'exec')
target.write_text(source,encoding='utf-8',newline='\n')
print('Prepared scale sealer; complete scale, all-placement fidelity and four reviewed screenshots are required.')
