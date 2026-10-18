"""Prepare unchanged archive and geometry verification for boundary ordering."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/finish_h5_material_profile_pilot.py').read_text(encoding='utf-8')
s=s.replace('h5-material-profile-pilot','h5-boundary-priority-pilot').replace('h5_material_profile_pilot','h5_boundary_priority_pilot').replace('h5-material-profile-preparation','h5-boundary-priority-preparation')
s=s.replace('# Exact material-profile rejection pilot','# Boundary-priority exchange pilot')
start=s.index("    'The candidate retains exact-state rejection")
end=s.index("    'Four jobs, two kerfs",start)
s=s[:start]+'''    'The candidate ranks incoming last-sheet members by upper extent, then',
    'area, retaining stable equal ties. Selected pairs preserve their original',
    'area/stable member order and anchor. Existing pair generators, caps,',
    'samples, repairs, budgets, work charges, early neutral rejections and full',
    'acceptance validation remain. The [preparation](h5-boundary-priority-preparation-20261018.md)',
    'retains 126 passing optimized tests, all 123 prior tests unchanged, 25',
    'frozen-CLI order/boundary checks, public parity and deterministic replays.',
    'Both expected original-order failures and the three failed first-revision',
    'regressions remain preserved. Restoring original pair anchors repairs',
    'those regressions without changing their assertions.','',
'''+s[end:]
path=root/'output/finish_h5_boundary_priority_pilot.py';compile(s,str(path),'exec');path.write_text(s,encoding='utf-8',newline='\n')
s=(root/'output/audit_h5_material_profile.py').read_text(encoding='utf-8').replace('h5-material-profile-pilot','h5-boundary-priority-pilot')
path=root/'output/audit_h5_boundary_priority.py';compile(s,str(path),'exec');path.write_text(s,encoding='utf-8',newline='\n')
print('Prepared original archive/geometry checks and counters; no unfinished results scored.')
