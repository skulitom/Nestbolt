from pathlib import Path
from hashlib import sha256
import difflib
import json
import shutil
import subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-complete-set-pilot-20261017'
load=lambda p:json.loads(p.read_bytes())
r=load(out/'results.json');v=load(out/'verification.json');a=load(out/'filled-outer-audit.json')
assert v['all_original_archives_verified'] and v['valid']==v['attempts']==72 and a['all_holes_reserved'] and a['cases']==48
pairs=r['summary']['pairs'];failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
assert len(failed)==4 and all(p['job'].startswith('m-mechanical-') for p in failed)
attempts=sum(p['arms']['candidate']['exchange_attempts'] for p in pairs)
accepted=sum(p['arms']['candidate']['exchanges'] for p in pairs)
assert (attempts,accepted)==(74,11)
def append(name,text):
    with (root/name).open('ab') as f:f.write(text.encode('utf-8'))
append('benchmarks/results/h5-complete-set-pilot-20261017.md',f'''

## Independent hole-reservation check and decision

The [separate filled-outer audit](h5-complete-set-pilot-20261017/filled-outer-audit.json)
uses Shapely 2.1.2, independent original outer rings and every rigid placement.
All 48 common-mode layouts pass {a['same_sheet_pairs']:,} same-sheet pair checks:
no overlap and at least the requested kerf, within the unchanged 0.0000001 mm
checking tolerance. Minimum observed clearance slack is
{a['minimum_clearance_slack_mm']:.12g} mm. No hole interiors are subtracted.

**Do not integrate this candidate.** All four mechanical job/kerf medians fail
the original +1% material limit (+5.433792%, +6.521291%, +5.700699%, +5.764347%).
All four control pairs meet the material limit. There are 74 exchange attempts
and eleven acceptances overall, with none on panel hardware. Aggregate counters
do not distinguish complete versus partial sets or the failed repair stage;
they do not justify another unchanged-build run or an infeasibility claim.
The full 13-job gate is not opened for this rejected candidate.
''')
append('BENCHMARKS.md','''

## 2026-10-17 — Complete-set eligibility still fails mechanical material limits

[All 72 paired outcomes](benchmarks/results/h5-complete-set-pilot-20261017.md)
validate with unchanged geometry, quantities, metrics and public exports in
8.947 minutes. Every original archive passes CRC and member/hash checks.
The independent filled-outer audit checks 133,412 same-sheet pairs across all
48 common-mode outputs: no overlap or part-in-hole, with minimum kerf slack
0.000000999999247131 mm against a 0.0000001 mm checking tolerance.

The candidate fails all four mechanical material pairs against the unchanged
+1% limit: large plates +5.433792% laser / +6.521291% plasma; panel hardware
+5.700699% / +5.764347%. All four control pairs meet material limits. Of 74
exchange attempts, eleven are accepted; none on panel hardware. Neither a
few accepted exchanges nor slight improvements against the failing common
baseline establishes H5. The candidate remains unintegrated; the full 13-job
gate is not started. Existing failures, source/build/data guards, thresholds
and reserved isolation remain. Aggregate counters do not identify the current
repair bottleneck or prove infeasibility. H2/H5 remain open; completion is 60%.
''')
note='''

**N4 complete-set outcome, 2026-10-17:** [all 72 outcomes validate](../benchmarks/results/h5-complete-set-pilot-20261017.md),
including an independent filled-outer audit of 133,412 same-sheet pairs in all
48 common-mode layouts. All four mechanical material pairs still fail +1%, at
+5.433792% / +6.521291% for large plates and +5.700699% / +5.764347% for panel
hardware (laser/plasma). Four control pairs meet material limits. Of 74 exchange
attempts, eleven succeed; none on panel hardware. The candidate is rejected for
integration and the full gate is not opened. Counters alone do not establish
which repair stage now limits progress. Original outcomes/limits remain;
H2/H5 are open at 60%.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(name,note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8')
old='''**N4 next comparison, 2026-10-17:** [the complete-set eligibility candidate](../benchmarks/results/h5-complete-set-preparation-20261017.md)
passes 85 core tests, strict lint and authored public checks. Its
[72-outcome pilot plan](../benchmarks/results/h5-complete-set-pilot-20261017/plan.json)
retains all original paired budgets and material limits. No quality claim or
production integration; H2/H5 remain open at 60%.'''
new='''**N4 latest outcome, 2026-10-17:** [all 72 complete-set pilot outcomes validate](../benchmarks/results/h5-complete-set-pilot-20261017.md),
but all four mechanical pairs still fail the +1% material limit, at +5.433792%
to +6.521291%. All four control pairs pass the material limit. The separate
filled-outer audit confirms all 48 common-mode outputs keep holes reserved.
There are 74 exchange attempts and eleven acceptances, none on panel hardware.
The candidate is rejected for integration; the full 13-job gate is not started.
Original results/limits remain; H2/H5 are open at 60%.'''
assert s.count(old)==1;s=s.replace(old,new);p.write_text(s,encoding='utf-8',newline='\n')
oldsource=root/'output/h5-obstruction-set-probe/candidate/crates/core/src/sheets/vstrip/exchange.rs'
newsource=root/'output/h5-complete-set-probe-20261017/candidate/crates/core/src/sheets/vstrip/exchange.rs'
(out/'candidate-formatted.patch').write_text(''.join(difflib.unified_diff(oldsource.read_text(encoding='utf-8').splitlines(True),newsource.read_text(encoding='utf-8').splitlines(True),fromfile='rejected-atomic-set',tofile='complete-set-built-source')),encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print(json.dumps({'failed_material_pairs':len(failed),'accepted_exchanges':accepted,'attempted_exchanges':attempts,'integrated':False}))
