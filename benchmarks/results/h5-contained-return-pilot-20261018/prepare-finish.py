"""Prepare unchanged archive/geometry audits and a reviewed outcome record."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def adapt(s):return s.replace('h5-boundary-pair','h5-contained-return').replace('h5_boundary_pair','h5_contained_return')
def save(name,s):
    compile(s,name,'exec');(root/'output'/name).write_text(s,encoding='utf-8',newline='\n')
s=adapt((root/'output/finish_h5_boundary_pair_pilot.py').read_text(encoding='utf-8'))
start=s.index("assert not psutil.pid_exists(");end=s.index('\n',start)
s=s[:start]+"pid_check=pilot.require_runner_stopped(opened,'h5_contained_return_pilot.py')"+s[end:]
s=s.replace("'all_original_archives_verified':True", "'process_identity_check':pid_check,'all_original_archives_verified':True")
start=s.index("    'The candidate includes the two");end=s.index("    'Four jobs, two kerfs",start)
s=s[:start]+'''    'The candidate shifts fitting return groups into the existing source',
    'bounding box before the original repair. Already contained, oversized',
    'or numerically uncontained groups retain their old poses. Original and',
    'proposed geometry work is charged. Orientations and reflection, choices,',
    'repair budgets and exact material/geometry acceptance remain. The',
    '[preparation](h5-contained-return-preparation-20261018.md) retains 133',
    'passing optimized tests, all 130 prior tests unchanged, 29 public CLI',
    'checks, deterministic replays and exact source reconstruction. Expected',
    'old-behavior failures and the repaired rotated-edge failure are preserved.','',
'''+s[end:]
s=s.replace('Boundary-pair exchange pilot','Contained-return exchange pilot')
save('finish_h5_contained_return_pilot.py',s)
s=adapt((root/'output/audit_h5_boundary_pair.py').read_text(encoding='utf-8'))
save('audit_h5_contained_return.py',s)
s=adapt((root/'output/record_h5_boundary_pair_outcome.py').read_text(encoding='utf-8'))
s=s.replace('boundary-pair','contained-return').replace('Boundary-pair','Contained-return')
start=s.index('followup = (');end=s.index('\nnote = ',start)
s=s[:start]+'''interpretation=load(out/'interpretation.json')
assert interpretation['failed_material_pairs']==len(failed) and interpretation['quality_claim'] is False
assert interpretation['results_sha256']==__import__('hashlib').sha256((out/'results.json').read_bytes()).hexdigest()
followup=interpretation['followup']
'''+s[end:]
s=s.replace('**N4 exact boundary-copy diagnosis, 2026-10-18:**','**N4 exchange-failure diagnosis, 2026-10-18:**')
s=s.replace("'output/prepare_h5_contained_return_checks.py'","'output/prepare_h5_contained_return_finish.py'")
save('record_h5_contained_return_outcome.py',s)
print('Prepared archive verification, independent filled-outer audit and reviewed outcome record.')
