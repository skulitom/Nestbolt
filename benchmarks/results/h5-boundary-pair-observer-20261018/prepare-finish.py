"""Prepare data-driven reporting; require a reviewed interpretation after diagnosis."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/record_h5_boundary_observer_outcome.py').read_text(encoding='utf-8')
s=s.replace('h5-boundary-observer','h5-boundary-pair-observer').replace('h5-boundary-priority-probe','h5-boundary-pair-probe')
s=s.replace('Exact boundary-copy selection diagnosis','Both-upper-part pair diagnosis')
s=s.replace('**N4 exact boundary-copy diagnosis, 2026-10-18:**','**N4 boundary-pair diagnosis, 2026-10-18:**')
s=s.replace('**N4 exact boundary-copy observation, 2026-10-18:**','**N4 boundary-pair observation, 2026-10-18:**')
s=s.replace('**N4 boundary-priority outcome, 2026-10-18:**','**N4 boundary-pair outcome, 2026-10-18:**')
start=s.index('assert count==summary');end=s.index("lines=['#",start)
s=s[:start]+'''interpretation=load(out/'interpretation.json')
assert interpretation['all_attempts']==summary['attempts']
assert interpretation['attempts_with_all_height_copies']==complete
assert interpretation['quality_claim'] is False
assert interpretation['layout_checks_sha256']==sha256((out/'layout-checks.json').read_bytes()).hexdigest()
followup=interpretation['followup']
'''+s[end:]
s=s.replace('Diagnose exact boundary-copy selection','Diagnose attempts to move both upper parts')
s=s.replace('both_height_copies_absent_from_all_available_choices=True,', "both_height_copies_absent_from_all_available_choices=all(not b['all_height_copies_choice_indices'] for b in a['baselines']),")
s=s.replace("'output/prepare_h5_boundary_observer_layout_checks.py'", "'output/prepare_h5_boundary_pair_observer.py'")
s=s.replace("'output/prepare_h5_boundary_observer_seal.py'", "'output/prepare_h5_boundary_pair_observer_record.py'")
needle="selectors=code[code.index('fn incoming_pairs('):code.index('fn same_original_inventory(')]"
s=s.replace(needle,needle+"\npriority=code[code.index('// Reserve the first choice'):code.index('struct Proposal {')]\nreview['boundary_pair_inclusion']=priority")
compile(s,'record','exec')
(root/'output/record_h5_boundary_pair_observer_outcome.py').write_text(s,encoding='utf-8',newline='\n')
print('Prepared diagnostic reporting; reviewed interpretation is still required.')
