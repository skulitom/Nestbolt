from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
import shutil
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-area-witness-20261017';out.mkdir(exist_ok=False)
for source,name in [('h5-area-witness-20261017','original-width-assumption'),('h5-area-witness-height-20261017','height-preserving')]:
    shutil.copytree(root/'output'/source,out/name)
for name in ['check_h5_area_witness.py','check_h5_area_witness_height.py']:
    shutil.copyfile(root/'output'/name,out/name)
write=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
original=[json.loads((out/'original-width-assumption'/f'{name}-stdout.json').read_bytes()) for name in ['before','after']]
passed=json.loads((out/'height-preserving/checks.json').read_bytes())
assert all(r['valid'] for r in original)
assert original[0]['metrics']['material_area']==18800 and original[1]['metrics']['material_area']==19700
assert passed['material_before_mm2']==passed['material_after_mm2']==13300
assert passed['incoming_area_mm2']==2550 and passed['returned_area_mm2']==2700
write(out/'review.json',{'utc':datetime.now(timezone.utc).isoformat(),
    'original_assumption_failed':'Keeping width fixed did not preserve material: the validator charges last-sheet used height, which grew from 88 to 97 mm. Both original layouts were valid; the equality assertion correctly failed.',
    'original_reports_and_script_preserved':True,
    'second_authored_case':'Transpose all authored rectangle dimensions/placements so the return set retains the charged height; preserve relative blocker placement.',
    'independent_result':'A 2700 mm² return set replaces a 2550 mm² part while both before/after layouts validate at 13300 mm² material.',
    'conclusion':'The smaller-return-area filter is not required by geometry or material correctness. This does not show that any rejected mechanical proposal can be repaired, or that a changed search improves quality.',
    'new_searches':0,'held_out_inputs':0,'H5_complete':False})
shutil.copyfile(__file__,out/'record.py')
write(out/'integrity.json',{p.relative_to(out).as_posix():{'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()} for p in out.rglob('*') if p.is_file()})
(out.parent/(out.name+'.md')).write_text('''# Authored larger-return-set witness — 2026-10-17

The independent Clipper2 validator accepts both hand-built layouts with five
parts, unchanged stock/spacing/rotations and **13,300 mm² material**. A 2,550 mm²
incoming rectangle exchanges with three 900 mm² squares: 2,700 mm² combined.
The returned set retains its relative arrangement and fits within the same
charged last-sheet height. No optimizer or quality measurement runs here.

This shows that a smaller combined return area is a heuristic, not a required
consequence of the unchanged geometry/material guard. It does not prove that
any rejected development proposal is feasible or that accepting more proposals
improves search. The [four diagnostic traces](h5-obstruction-stage-diagnosis-20261017.md)
separately show that all 620 observed multi-blocker samples are filtered out by
that heuristic, leaving only partial exchanges.

The first authored orientation preserved width but increased charged height;
its equality assertion failed correctly (18,800 → 19,700 mm²). Both valid
layouts, reports and the failed assumption remain preserved. The second case
transposes the authored geometry and placement coordinates to test the actual
height metric. This is an explicit separate example, not a rescored benchmark.

[Review](h5-area-witness-20261017/review.json),
[passing checks](h5-area-witness-20261017/height-preserving/checks.json),
[all file hashes](h5-area-witness-20261017/integrity.json).
No product change, reserved geometry, integration or H5 closure; completion 60%.
''',encoding='utf-8',newline='\n')
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:f.write('\nbenchmarks/results/h5-area-witness-20261017/** -text -whitespace\n')
note='''

**N4 diagnosis, 2026-10-17:** [four current-candidate traces](../benchmarks/results/h5-obstruction-stage-diagnosis-20261017.md)
validate all layouts but show zero complete blocker-set proposals: 620 sampled
sets fail the smaller-area heuristic. All 29 attempted exchanges are partial;
27 fail receiving-sheet repair and two succeed. An [independently validated
authored witness](../benchmarks/results/h5-area-witness-20261017.md) demonstrates
that returning more combined part area can preserve both validity and material.
The first incorrectly oriented witness is retained with its failed material
assertion. This motivates a separately tested complete-set eligibility change;
it proves no mechanical feasibility or quality gain. Production stays unchanged,
and H2/H5 remain open at 60% completed weight.
'''
for rel in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    with (root/rel).open('a',encoding='utf-8',newline='\n') as f:f.write(note)
path=root/'docs/STATUS.md';text=path.read_text(encoding='utf-8')
anchor='The [completed obstruction-set pilot]'
assert text.count(anchor)==1
text=text.replace(anchor,note.strip()+'\n\n'+anchor)
path.write_text(text,encoding='utf-8',newline='\n')
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:f.write('''

## 2026-10-17 — Atomic-set stage traces and independent area witness

[All four diagnostic layouts validate](benchmarks/results/h5-obstruction-stage-diagnosis-20261017.md).
The smaller-area heuristic rejects all 620 observed complete multi-blocker sets;
all 29 actual attempts return a partial set. Twenty-seven fail receiving-sheet
repair and two succeed. Traces, original-job metrics/quantities and every raw
archive/member hash verify; source/binary/input guards remain unchanged. Trace
overhead may perturb deadlines, so these are not quality or speed comparisons.

[An authored validator-only witness](benchmarks/results/h5-area-witness-20261017.md)
exchanges 2550 mm² incoming area with 2700 mm² returned area while preserving
validity and exactly 13300 mm² material. The original width-preserving attempt
fails its material-equality assertion because the metric charges height; both
that failure (18800 → 19700 mm²) and the separate transposed passing example
are preserved. No search or original benchmark is rerun/rescored for this proof.
The observations motivate testing complete-set eligibility with the same final
geometry/material guards. No feasibility/improvement claim, production change,
reserved access or H5 credit; completed weight remains 60%.
''')
print(json.dumps({'witness_recorded':True,'original_failed_assumption_preserved':True}))
