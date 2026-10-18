"""Prepare retention and reporting helpers for the conditional pose observer."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/seal_h5_frontier_observer.py').read_text(encoding='utf-8')
s=s.replace('h5-frontier-observer','h5-boundary-observer').replace('h5_frontier_observer','h5_boundary_observer')
s=s.replace('123','126').replace('all_123','all_126')
s=s.replace("len(reader['malformed_records_rejected'])==16", "len(reader['malformed_records_rejected'])==21")
s=s.replace("'malformed_records_rejected':16", "'malformed_records_rejected':21")
s=s.replace("'frontier_reader.py'", "'boundary_pose_reader.py'")
s=s.replace("'prepare_h5_frontier_runner.py'", "'prepare_h5_boundary_observer_runner.py'")
s=s.replace("'check_h5_frontier_reader.py'", "'check_h5_boundary_observer_reader.py'")
s=s.replace("'check_h5_frontier_source.py'", "'check_h5_boundary_observer_source.py'")
s=s.replace("'record_h5_frontier_preparation.py'", "'record_h5_boundary_observer_preparation.py'")
s=s.replace("assert reader['parent_profile_branch_witnesses_exact']==12", "assert reader['all_choice_poses_match_unique_baseline_members']\nassert reader['parent_profile_branch_witnesses_exact']==12")
s=s.replace("'exact_parent_reconstruction':True", "'exact_choice_poses_verified':True,'exact_parent_reconstruction':True")
start=s.index("doc=f'''");end=s.index("(out.parent/",start)
s=s[:start]+'''doc=f\x27\x27\x27# Boundary-part physical selection — observation preparation, 2026-10-18

The [completed boundary-priority pilot](h5-boundary-priority-pilot-20261018.md)
provides quality evidence for the candidate. This separate observer qualifies
only after that pilot fails at least one material comparison. It does not
repeat the quality pilot or change any selection, budget, repair or acceptance.

The observer retains the preceding family/outcome trace and additionally
records each choice's exact public physical poses. Conversion uses the same
sheet-offset subtraction and model transformation as the ordinary exporter.
The reader requires each pose to match a unique member of the independently
validated baseline exactly, with complete single-copy coverage and bounded
pair multiplicity. This distinguishes actual boundary copies from other
copies of the same part. Family and stage checks reuse the qualified prior
reader; its source is included in the measurement guards.

All 126 existing optimized tests, strict lint and the observer build pass.
Sixteen authored cases qualify actual traces; 21 malformed observations are
rejected. All {reader['frozen_CLI_baseline_checks']} captured baselines validate
with the frozen public CLI and reproduce their metrics exactly. Twelve
profile-branch witnesses match the unobserved parent's saved records exactly,
and their aggregated counters equal logged attempts. All 156 formatted source
files reconstruct exactly, with 155 unchanged and every original test retained.

The diagnostic plan retains panel hardware, both kerfs, seed zero, 60 seconds,
serial physical CCD0 CPU 8 and the original 20-minute session cap. The measured
run function is AST-identical to the previous two-case diagnostic; per-case
validation/export is unchanged. The plan is committed before measurement.
Logging may alter wall trajectories, so no comparative quality or speed claim
follows. Production, reserved data, release and README claims remain unchanged.
H2/H5 remain open at 60%.

[Checks](h5-boundary-observer-preparation-20261018/checks.json),
[reader checks](h5-boundary-observer-preparation-20261018/reader-checks.json),
[source reconstruction](h5-boundary-observer-preparation-20261018/reconstruction.json),
[archive integrity](h5-boundary-observer-preparation-20261018/integrity.json).
\x27\x27\x27
'''+s[end:]
compile(s,'seal','exec')
(root/'output/seal_h5_boundary_observer.py').write_text(s,encoding='utf-8',newline='\n')
s=(root/'output/record_h5_frontier_preparation.py').read_text(encoding='utf-8')
s=s.replace('h5-frontier-observer','h5-boundary-observer')
s=s.replace('height-setting part observation','exact boundary-copy observation')
s=s.replace('123','126').replace('sixteen malformed-record','21 malformed-record')
s=s.replace('families for available, visited and attempted exchange choices alongside the\nvalidated public baseline.', 'families and exact physical poses for available, visited and attempted\nexchange choices alongside the validated public baseline. Each chosen pose\nmatches a unique baseline copy exactly, with complete single-copy coverage.')
s=s.replace('**N4 material-profile rejection outcome, 2026-10-18:**','**N4 boundary-priority outcome, 2026-10-18:**')
s=s.replace('Qualify height-setting part observation','Qualify exact boundary-copy observation')
compile(s,'record','exec')
(root/'output/record_h5_boundary_observer_preparation.py').write_text(s,encoding='utf-8',newline='\n')
s=(root/'output/finish_h5_frontier_observer.py').read_text(encoding='utf-8').replace('h5_frontier_observer','h5_boundary_observer').replace('h5-frontier-observer','h5-boundary-observer')
compile(s,'finish','exec')
(root/'output/finish_h5_boundary_observer.py').write_text(s,encoding='utf-8',newline='\n')
print('Prepared conditional observer sealing, reporting and archive verification helpers.')
