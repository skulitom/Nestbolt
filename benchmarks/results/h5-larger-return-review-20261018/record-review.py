"""Record the unqualified candidate and the evidence needed before correcting it."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-larger-return-review-20261018'
load=lambda p:json.loads(p.read_bytes())
c=load(out/'checks.json');r=load(out/'output-comparison.json');assert not c['candidate_qualified'] and c['all_observed_layouts_valid']
diffs=[p['difference_mm2'] for p in r['pairs']]
assert abs(diffs[0])<1e-9 and abs(diffs[1]+66.0529)<1e-6 and abs(diffs[2]+266.0522)<1e-6 and abs(diffs[3]-.0388)<1e-6
assert r['pairs'][3]['original_gap_sheet']==['sheet-0'] and r['pairs'][3]['broader_gap_sheet']==['sheet-1']
gap=next(row for row in r['records'] if row['arm']=='broader' and row['test']=='accepted_exchange_still_fills_a_known_gap')
assert gap['stats']['post_exchange_fill_calls']==gap['stats']['post_exchange_fill_moves']==gap['stats']['direct_insertions']==1
source=root/'output/h5-larger-return-probe-20261018/candidate/crates/core/src/sheets/vstrip.rs';text=source.read_text(encoding='utf-8')
start=text.index('                        let gaps = std::env::var_os("NESTBOLT_NO_FILL")');end=text.index('                    if shape.sheets > 1 && strip.in_last',start)
followup='''The broader search produces an equally charged valid result for the old
single-fallback fixture and lower charged material for the two return-frame
fixtures. Those outcomes show that the older chosen-route assertions are not
equivalent to the whole-job geometry/material invariants. They do not by
themselves justify changing any assertion or qualify the candidate.

The gap-filling fixture is different: the broader result uses 0.0388 mm2 more
material than the original result and leaves the named small part on sheet 1.
It remains valid and below its own before-layout material. Counters record one
successful post-exchange fill, but do not identify the part that moved or prove
that this intermediate placement survives later exploration/compression.

Next, observe the actual layouts immediately before/after exchange and gap
filling, plus the final accepted snapshot, for this authored fixed-work case.
Require its final result to reproduce the saved outcome before attributing
the missing placement to filling, a different chosen swap, or later snapshot
selection. Then choose a correction and preserve targeted strict-material,
rotated-return and single-fallback coverage. Do not merely loosen four assertions
to obtain a passing suite. The quality pilot remains unopened.
'''
review={'candidate_qualified':False,'observed_material_differences_mm2':diffs,'broader_gap_statistics':gap['stats'],
    'fill_callsite_source':source.relative_to(root).as_posix(),'fill_callsite_source_sha256':sha256(source.read_bytes()).hexdigest(),
    'fill_callsite_line':text[:start].count('\n')+1,'exact_fill_and_snapshot_sequence':text[start:end],
    'source_review_limit':'The code and operation counts do not establish which part moved, its intermediate location, or whether it was retained in the final result.',
    'next_action':followup,'assertions_changed':False,'quality_pilot_started':False,'production_changed':False}
(out/'source-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
note='''**N4 larger-return candidate review, 2026-10-18:** [the first implementation is unqualified](../benchmarks/results/h5-larger-return-review-20261018.md).
The new larger-return regression first fails against unchanged runtime, then
passes after removing the paired proposal area filter. All four new tests
pass, but the complete suite reports 107 passes and four older failures.
Every original assertion, failed source and binary is preserved. Six new
actual outcomes and ten original/broader comparison observations pass 32
independent CLI validations. The broader results are equal in one case and
save 66.0529 / 266.0522 mm2 in two; the gap-filling case is 0.0388 mm2 worse
and leaves its named small part on the last sheet despite one recorded fill.
A logging-setup failure and shared-target stale executable are preserved;
recovery uses a fresh target and reuses all completed original observations.
Next inspect the intermediate fill and accepted snapshots before correcting
behavior or targeted tests. No assertion change, quality pilot, integration
or H5 credit; H2/H5 remain open at 60%.
'''
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';old=p.read_text(encoding='utf-8');marker='**N4 mixed-pair diagnosis, 2026-10-18:**';assert old.count(marker)==1
p.write_text(old.replace(marker,note+'\n'+marker),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
append(out.parent/(out.name+'.md'),'\n## Next investigation\n\n'+followup+'\n[Source review](h5-larger-return-review-20261018/source-review.json) preserves\nthe exact fill/snapshot call site and hash. No test assertion is changed.\n')
append(root/'BENCHMARKS.md','''

## 2026-10-18 — Preserve the larger-return candidate failure and compare outputs

[The candidate remains unqualified](benchmarks/results/h5-larger-return-review-20261018.md).
The unchanged runtime first fails the new positive regression with two guards
passing. Removing the paired proposal area rejection makes all four new tests
pass, but the complete suite reports 107 passes and four older route/placement
failures. Original assertions, sources, logs and binaries remain preserved.

Six actual new cases pass twelve independent before/after CLI validations.
Ten original/broader comparison observations pass twenty more. All layouts
are valid and preserve strict material nonincrease against their own inputs.
Compared with original final outputs, the broader result is equal in one case,
better by 66.0529 and 266.0522 mm2 in two, and worse by 0.0388 mm2 in the
gap-filling case. That case leaves the named part on the last sheet despite
one successful fill counter. Actual intermediate placements and snapshot
selection must be observed before choosing a correction; counts alone are
insufficient and no assertion has been relaxed.

The first logging preparation failed before a build. A shared target then
returned the original executable for the second arm; the unexpected passing
test stopped the comparison before scoring it. Both failures remain. Recovery
builds the unchanged broader arm in a fresh target, verifies a distinct binary
and retains all six original observations without repeating them. The sealed
archive passes CRC and all 1,164 member hashes. No quality pilot, production
change, reserved access or H5 credit; completed milestone weight stays 60%.
''')
append(root/'.gitattributes','\nbenchmarks/results/h5-larger-return-review-20261018/** -text -whitespace\n')
shutil.copyfile(__file__,out/'record-review.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'candidate_qualified':False,'public_validations':32,'assertions_changed':False,'next':'observe actual gap-fill and accepted snapshots'}))
