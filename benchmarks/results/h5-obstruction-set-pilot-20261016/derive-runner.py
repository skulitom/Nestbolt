"""Prepare the same paired pilot method for the new obstruction-set candidate."""
from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]
original=(ROOT/'scripts/h5_early_exchange_pilot.py').read_text(encoding='utf-8')
s=original[original.index('import argparse'):]
s='''"""Paired development pilot for atomic obstruction-set exchanges.

Current depth-three baseline and candidate share geometry and search budgets.
Four frozen H5 jobs, both kerfs, seeds 0-2 and matched 60-second wall budgets.
The candidate can return the complete smaller actual obstruction set, keeping
the existing one-victim fallbacks, repair/validation guards and early deadline.
Earlier paired failures and diagnostic traces remain unchanged. Wait for the
current full H4 matrix and conditional scale/export-check sequence to finish.
This pilot cannot close H5 or justify a public comparative claim.
"""\n'''+s
s=s.replace('output/h5-early-exchange-probe','output/h5-obstruction-set-probe')
s=s.replace('public-checks-v1','public-checks')
s=s.replace('nestbolt-baseline-observer.exe','baseline-observer.exe').replace('nestbolt-candidate-observer.exe','candidate-observer.exe')
s=s.replace('h4-preview-score-release-20261016','h4-preview-depth-release-20261016')
s=s.replace('h4-preview-score-scale-plan-20261016','h4-preview-depth-scale-plan-20261016')
s=s.replace('continue_preview_score_checks.py','continue_preview_depth_checks.py')
s=s.replace('h5-early-exchange-preparation-20261016','h5-obstruction-set-preparation-20261016')
s=s.replace("PROBE/'baseline-observer-build.json', PROBE/'candidate-observer-build.json'", "PROBE/'build-v2.json', PROBE/'fixture-repair.json'")
s=s.replace("load(PROBE/'baseline-observer-build.json')['binary_sha256']", "load(PROBE/'build-v2.json')['binaries']['baseline']")
s=s.replace("load(PROBE/'candidate-observer-build.json')['binary_sha256']", "load(PROBE/'build-v2.json')['binaries']['candidate']")
s=s.replace('Isolated early-exchange candidate, common-line search bonus on','Isolated complete-obstruction-set candidate, common-line search bonus on')
s=s.replace('benchmarks/results/h5-exchange-pilot-v2-20261016/results.json','benchmarks/results/h5-early-exchange-pilot-20261016/results.json')
s=s.replace('Wait until the current release matrix and conditional scale sequence finish.', 'Wait until the current release matrix and conditional scale/export-check sequence finish.')
def body(source,name):
    return ast.dump(next(n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name),include_attributes=False)
for name in ['blocks','summarize','case']:
    assert body(original,name)==body(s,name),'Paired method changed: '+name
compile(s,'h5_obstruction_set_pilot.py','exec')
(ROOT/'scripts/h5_obstruction_set_pilot.py').write_text(s,encoding='utf-8',newline='\n')
print('Prepared runner; paired blocks, summary and individual-case method are AST-identical to the retained pilot.')
