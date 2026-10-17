from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];source=root/'output/h5-balanced-exchange-witness-20261017'
out=root/'benchmarks/results/h5-balanced-exchange-witness-20261017'
checks=json.loads((source/'checks.json').read_bytes())
assert checks['both_layouts_valid'] and checks['all_metrics_identical'] and checks['material_mm2']==19700
assert checks['optimizer_runs']==0 and len(checks['single_incoming_bounds'])==4
assert not (source/'failure.json').exists()
shutil.copytree(source,out);shutil.copyfile(__file__,out/'record.py')
inventory={p.name:{'sha256':sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in out.iterdir() if p.is_file()}
(out/'integrity.json').write_text(json.dumps({'files':inventory,'all_source_copies_exact':all((out/p.name).read_bytes()==p.read_bytes() for p in source.iterdir() if p.is_file())},indent=2)+'\n',encoding='utf-8',newline='\n')
(out.parent/(out.name+'.md')).write_text('''# Balanced two-to-three exchange witness — 2026-10-17

The independent CLI validator accepts both authored layouts with seven parts
and **identical metrics, including 19,700 mm² material**. Two 30 × 45 mm parts
move from the last sheet to the first, and three 30 × 30 mm squares move back.
Both moved groups have area 2,700 mm². Each sheet keeps one 60 × 94 mm filler.
All rotations are fixed at zero, stock is 100 × 100 mm, edge clearance is 1 mm,
and part clearance is 0.2 mm. Only sheet assignments change in the valid witness.

## Why moving one selected incoming part is insufficient

This bound concerns those two narrow incoming parts and three return squares,
with one filler on each sheet; it does not rule out other part selections or
global layouts. The filler may move within its sheet without invalidating the bound.

Each usable sheet is 98 × 98 mm. Its filler leaves only 4 mm of combined space
above/below it, so every small rectangle must lie to one side. Combined side
space is 38 mm; two sides cannot each fit a 30 mm-wide part. All small parts
therefore share one side band of width at most 38 mm. Their 30 mm-wide horizontal
intervals overlap, so their heights must stack without overlap within 98 mm.

Moving only one 45 mm-high incoming part and returning k squares gives these
necessary heights, even before adding positive clearance:

| Returned squares k | Receiving sheet | Return sheet | Can both fit within 98 mm? |
| ---: | ---: | ---: | --- |
| 0 | 135 mm | 45 mm | No |
| 1 | 105 mm | 75 mm | No |
| 2 | 75 mm | 105 mm | No |
| 3 | 45 mm | 135 mm | No |

Moving both incoming parts and all three squares instead requires 90.2 mm and
90.4 mm including minimum inter-part clearance. The saved concrete placements
use 2 mm gaps and pass the independent validator. The group exchange therefore
addresses a real limitation of these single-incoming choices without changing
geometry, quantities, orientations or the material limit.

No optimizer ran, no mechanical benchmark feasibility or improvement is proved,
and no new search heuristic is implemented here. The mechanical traces still
need source-capacity/placement inspection. H2/H5 remain open at 60%.
''',encoding='utf-8',newline='\n')
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as f:f.write('\nbenchmarks/results/h5-balanced-exchange-witness-20261017/** -text -whitespace\n')
with (root/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:f.write('''

## 2026-10-17 — Balanced two-to-three authored feasibility witness

[Both seven-part layouts validate](benchmarks/results/h5-balanced-exchange-witness-20261017.md)
with identical metrics and 19,700 mm² material. Two 30x45 parts exchange sheets
with three 30x30 squares; both groups have 2,700 mm² area. With one 60x94 filler
per 98x98 usable sheet, a necessary stacking bound rules out moving just one of
the selected incoming parts for any zero-to-three returned-square count. The
bound allows filler movement, ignores positive clearance conservatively and is
explicitly scoped to those part selections. It does not prove global or
mechanical-job infeasibility. The balanced concrete placements satisfy all
clearances, fixed orientations, quantities and the unchanged material guard.
Two public validations, zero optimizer runs; all source/report bytes and hashes
are retained. Source-capacity inspection remains needed before selecting a new
mechanical heuristic. No production change or H5 credit; completion remains 60%.
''')
note='''

**N4 balanced-group witness, 2026-10-17:** [two independently valid layouts](../benchmarks/results/h5-balanced-exchange-witness-20261017.md)
show two incoming rectangles exchanging with three return squares at identical
material and quantities. A necessary stacking bound excludes all single-incoming
choices within that explicitly scoped selection. This supports investigating
balanced groups, but proves no mechanical improvement; inspect actual source
capacity/placement before implementing a new heuristic. No optimizer run,
production change or gate relaxation. H2/H5 remain open at 60%.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    with (root/name).open('a',encoding='utf-8',newline='\n') as f:f.write(note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8')
needle='A balanced\nmulti-part exchange needs a separate authored feasibility example first.'
replacement='A [balanced two-to-three authored example now validates](../benchmarks/results/h5-balanced-exchange-witness-20261017.md)\nat identical material; its scoped stacking bound explains why those single-incoming\nchoices cannot work. Mechanical source capacity/placement remains unproved.'
assert s.count(needle)==1;s=s.replace(needle,replacement);p.write_text(s,encoding='utf-8',newline='\n')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print(json.dumps({'recorded':str(out),'files':len(inventory),'material_mm2':19700,'optimizer_runs':0}))
