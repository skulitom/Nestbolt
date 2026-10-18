from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=(root/'output/record_h5_exchange_chain_outcome.py').read_text(encoding='utf-8')
s=s.replace('h5-exchange-chain','h5-extended-repair').replace('h5_exchange_chain','h5_extended_repair')
s=s.replace('exchange-continuation','extended-repair').replace('Exchange-continuation','Extended repair')
s=s.replace("start = old.index('**N4 extended-repair preparation, 2026-10-18:**')", "start = old.index('**N4 two-phase repair qualification, 2026-10-18:**')")
s=s.replace("end = old.index('**N4 free-space', start)", "end = old.index('**N4 ', start+1)")
s=s.replace("root / 'output/prepare_h5_free_return_finish.py'", "root / 'output/prepare_h5_extended_repair_finish.py'")
needle="details = '; '.join"
addition='''stage = load(out / 'extended-counters.json')
boundaries = load(out / 'final-boundaries.json')
capacity = load(out / 'fixed-inventory-area.json')
assert boundaries['all_saved_layout_checks_passed'] and capacity['all_saved_assignment_checks_passed']
counts += (f" The extended phase accepts {stage['accepted']}/{stage['attempted']} attempts "
           f"and rejects {stage['flat_rejections']} material-flat trials. Six extended "
           "acceptances are mechanical; all flat rejections are bracket cases.")
boundary_note = ("Saved mechanical layouts require 138.702–200.994 mm less height on the currently "
    "credited sheet, with 6–28 current copies above the conditional target. Five large-plate "
    "inventories exceed that target's usable rectangle area even before inter-part kerf. "
    "Those same copies cannot fit that same target sheet; other assignments and offcut sheets "
    "remain possible. Area below the bound does not prove packability, and this is not a global "
    "infeasibility result. No new search is used for either analysis.")
'''
assert s.count(needle)==1;s=s.replace(needle,addition+'\n'+needle)
s=s.replace('{counts} {followup}\nH2/H5', '{counts} {boundary_note}\n\n[Final boundaries](h5-extended-repair-pilot-20261018/final-boundaries.json) and\n[fixed-inventory area](h5-extended-repair-pilot-20261018/fixed-inventory-area.json)\nretain all fifteen layouts from failed pairs.\n\n{followup}\nH2/H5')
s=s.replace("'current_attempt_member_coverage_observed': False, 'quality_claim': False,", "'current_attempt_member_coverage_observed': False, 'final_boundary_analysis_completed': True,\n          'fixed_inventory_area_failures': capacity['same_inventory_area_failures'], 'quality_claim': False,")
compile(s,'record_h5_extended_repair_outcome.py','exec')
(root/'output/record_h5_extended_repair_outcome.py').write_text(s,encoding='utf-8',newline='\n')
print('Prepared outcome recorder from the prior audited reporting method.')
