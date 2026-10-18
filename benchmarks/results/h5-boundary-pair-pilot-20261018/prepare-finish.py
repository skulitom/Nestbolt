"""Reuse the fixed comparison and qualification methods for boundary-pair coverage."""
from pathlib import Path
from hashlib import sha256
import ast,json
root=Path(__file__).resolve().parents[1];probe=root/'output/h5-boundary-pair-probe-20261018'
ref=root/'scripts/h5_boundary_priority_pilot.py';original=ref.read_text(encoding='utf-8');s=original
s=s.replace('h5-boundary-priority-probe','h5-boundary-pair-probe').replace('h5-boundary-priority-preparation','h5-boundary-pair-preparation')
s=s.replace('h5-material-profile-pilot','h5-boundary-priority-pilot')
s=s.replace("PROBE/'order-checks/checks.json'", "PROBE/'pair-checks/checks.json'")
needle="ROOT/'benchmarks/results/h5-frontier-observer-20261018/source-review.json'"
s=s.replace(needle,needle+",\n                  ROOT/'benchmarks/results/h5-boundary-observer-20261018/layout-checks.json',\n                  ROOT/'benchmarks/results/h5-boundary-observer-20261018/source-review.json'")
s=s.replace('Isolated boundary-priority candidate','Isolated boundary-pair candidate')
end=s.index('"""',3)+3
s='''"""Paired development pilot of including the two highest source parts together.

Four frozen H5 jobs, both kerfs, seeds 0-2 and matched 60-second wall budgets.
The baseline is the unchanged preview. The isolated candidate puts the two
highest-ranked source members first in the appropriate same-item or mixed
pair list, removes an equivalent duplicate in either order and retains the
six-plus-six caps and remaining nearby alternatives. Original member anchor
frames, sampling, repairs, deadlines, work charges and every full acceptance
check remain. All 126 prior tests are unchanged; four new coverage, duplicate,
cap, anchor and empty/single-source tests are added. This descriptive pilot
cannot close H5 or justify a comparative claim.
"""'''+s[end:]
path=root/'scripts/h5_boundary_pair_pilot.py';assert not path.exists();compile(s,str(path),'exec')
path.write_text(s,encoding='utf-8',newline='\n')
def fn(t,n):return next(x for x in ast.parse(t).body if isinstance(x,ast.FunctionDef) and x.name==n)
names=['blocks','summarize','case','measure']
for n in names:assert ast.dump(fn(s,n))==ast.dump(fn(original,n))
method={'reference':ref.relative_to(root).as_posix(),'reference_sha256':sha256(ref.read_bytes()).hexdigest(),
        'candidate_runner':path.relative_to(root).as_posix(),'runner_sha256':sha256(path.read_bytes()).hexdigest(),
        'identical_function_ASTs':names,'scoring_or_measurement_changed':False}
(probe/'pilot-method.json').write_text(json.dumps(method,indent=2)+'\n',encoding='utf-8',newline='\n')
for stage in ['public','branch','harness']:
    s=(root/f'output/check_h5_boundary_priority_{stage}.py').read_text(encoding='utf-8')
    s=s.replace('h5-boundary-priority','h5-boundary-pair').replace('h5_boundary_priority','h5_boundary_pair')
    (root/f'output/check_h5_boundary_pair_{stage}.py').write_text(s,encoding='utf-8',newline='\n')
s=(root/'output/finish_h5_boundary_priority_pilot.py').read_text(encoding='utf-8').replace('h5-boundary-priority','h5-boundary-pair').replace('h5_boundary_priority','h5_boundary_pair')
start=s.index("    'The candidate ranks incoming");end=s.index("    'Four jobs, two kerfs",start)
s=s[:start]+'''    'The candidate includes the two highest-ranked source parts as the first',
    'same-item or mixed pair, removes a duplicate in either anchor order,',
    'and retains the six-plus-six caps and remaining nearby alternatives.',
    'Original pair anchor frames, samples, repairs, budgets, work charges,',
    'early neutral rejections and full acceptance checks remain. The',
    '[preparation](h5-boundary-pair-preparation-20261018.md) retains 130',
    'passing optimized tests, all 126 prior tests unchanged, 26 frozen-CLI',
    'pair/boundary checks, public parity and deterministic replays. Three',
    'expected failures under the previous selector remain preserved.','',
'''+s[end:]
s=s.replace('Boundary-priority exchange pilot','Boundary-pair exchange pilot')
compile(s,'finish','exec');(root/'output/finish_h5_boundary_pair_pilot.py').write_text(s,encoding='utf-8',newline='\n')
s=(root/'output/audit_h5_boundary_priority.py').read_text(encoding='utf-8').replace('h5-boundary-priority','h5-boundary-pair')
(root/'output/audit_h5_boundary_pair.py').write_text(s,encoding='utf-8',newline='\n')
s=(root/'output/record_h5_boundary_priority_outcome.py').read_text(encoding='utf-8').replace('h5-boundary-priority','h5-boundary-pair')
s=s.replace('boundary-priority','boundary-pair').replace('Boundary-priority','Boundary-pair')
s=s.replace('**N4 height-setting part diagnosis, 2026-10-18:**','**N4 exact boundary-copy diagnosis, 2026-10-18:**')
s=s.replace('Check whether the revised ordering actually reaches the height-setting parts, and identify the outcomes of those attempts, using a separately qualified observer.',
    'Check whether the new pair actually reaches both height-setting copies together and identify the stage at which those proposals stop, using a separately qualified observer.')
s=s.replace("'output/prepare_h5_boundary_finish.py'", "'output/prepare_h5_boundary_pair_checks.py'")
compile(s,'record-outcome','exec');(root/'output/record_h5_boundary_pair_outcome.py').write_text(s,encoding='utf-8',newline='\n')
print(json.dumps(method))
