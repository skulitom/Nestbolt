"""Review saved validator reports; preserve the initial incorrect literal assertion."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
root=Path(__file__).resolve().parents[1]
source=root/'output/h5-return-frame-witness-20261017'
out=root/'benchmarks/results/h5-return-frame-witness-20261017';out.mkdir()
load=lambda p:json.loads(p.read_bytes())
reports={name:load(source/(name+'-stdout.json')) for name in ['before','translation-only','frame-aligned']}
assert reports['before']['valid'] and reports['frame-aligned']['valid']
assert not reports['translation-only']['valid']
assert reports['before']['metrics']==reports['frame-aligned']['metrics']
m=reports['before']['metrics'];assert m['material_area']==19500 and m['last_sheet_id']=='sheet-0'
assert m['trailing_offcut_area']==500 and m['full_stock_area']==20000 and m['placed_parts']==6
assert (source/'failure.json').is_file()
for p in source.iterdir():
    if p.is_file():shutil.copyfile(p,out/p.name)
shutil.copyfile(root/'output/check_h5_return_frame_witness.py',out/'original-check.py')
shutil.copyfile(__file__,out/'review.py')
review={'authored_only':True,'new_searches':0,'new_validations_during_review':0,
    'initial_and_aligned_layouts_valid':True,'translation_only_rejected':True,
    'all_before_after_metrics_identical':True,'material_mm2':19500,'parts':6,
    'initial_failed_assertion_preserved':True,
    'initial_bookkeeping_error':'Expected 19700 mm2 based on the last listed sheet. The validator chooses the largest reusable trailing offcut, on sheet-0 here: 20000 - 500 = 19500, identically before and after.',
    'validator_rule':'crates/validator/src/job.rs selects the greatest offcut across used sheets.',
    'threshold_or_geometry_changed':False,'production_changed':False,'mechanical_applicability_unproven':True,'H5_complete':False}
(out/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
inventory={p.name:{'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()} for p in out.iterdir() if p.is_file()}
(out/'integrity.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8',newline='\n')
(out.parent/(out.name+'.md')).write_text('''# Return-group orientation witness — 2026-10-17

The original six-part layout and an authored quarter-turn exchange both pass
the independent validator with **identical metrics and 19,500 mm² material**.
Returning the same three squares by translation alone produces overlaps and
out-of-bounds geometry. Rotating the group into the incoming part's vacated
orientation fits, preserving all quantities and allowed orientations.

The initial script correctly validated these three outcomes, then failed a
hardcoded 19,700 mm² expectation. That bookkeeping error assumed the last listed
sheet supplies the offcut. The validator selects the largest reusable offcut:
sheet-0 saves 500 mm², so both valid layouts use 20,000 - 500 = 19,500 mm².
The separate review uses the original saved reports without rerunning validation,
changing geometry or relaxing any tolerance. The original script and failure remain.

This supports testing reciprocal rigid-frame initialization for returned groups,
with an all-or-nothing legality check and the previous translation fallback when
any part disallows the new orientation. Both repairs, independent whole-job
material/geometry acceptance and deadlines must remain. It proves no improvement
on the mechanical development jobs. No optimizer runs or production changes;
H2/H5 remain open at 60%.
''',encoding='utf-8',newline='\n')
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:f.write('\nbenchmarks/results/h5-return-frame-witness-20261017/** -text -whitespace\n')
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:f.write('''

## 2026-10-17 — Authored return-frame witness, with bookkeeping failure retained

[The six-part witness](benchmarks/results/h5-return-frame-witness-20261017.md)
has independently valid before/quarter-turn-after layouts with identical metrics:
19,500 mm² material. Translation-only return overlaps a neighbour and leaves stock.
The original script then failed a hardcoded 19,700 expectation; it assumed the
last listed sheet, while the validator uses the largest reusable offcut (500 mm²
on sheet-0). A separate review checks the unchanged saved reports; no rerun,
geometry edit or tolerance change. Original script/error and every hash remain.
This motivates isolated frame-aligned initialization with legal orientations
and translation fallback, not a quality claim. No search or H5 closure; 60%.
''')
print(json.dumps(review))
