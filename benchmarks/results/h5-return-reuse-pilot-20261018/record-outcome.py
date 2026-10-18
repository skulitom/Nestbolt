"""Record the completed pilot without assuming that any material pair passes."""
from pathlib import Path
import json
import shutil
import subprocess

root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-return-reuse-pilot-20261018'
load=lambda p:json.loads(p.read_bytes())
r=load(out/'results.json');v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json')
counters=load(out/'reuse-counters.json')
assert v['all_original_archives_verified'] and v['valid']==v['attempts']==72
assert audit['all_holes_reserved'] and audit['cases']==48
pairs=r['summary']['pairs'];assert len(pairs)==8 and all(p['complete'] for p in pairs)
failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
attempts=sum(p['arms']['candidate']['exchange_attempts'] for p in pairs)
accepted=sum(p['arms']['candidate']['exchanges'] for p in pairs)
reuses=counters['candidate_source_reuses']
details='; '.join(f"{p['job']} at {p['kerf_mm']} mm: {p['candidate_vs_normal_percent']:+.6f}%" for p in failed)
decision=('Reject this candidate for integration; do not open the full 13-job gate for it.' if failed else
          'All pilot material pairs pass; require the complete original 13-job H5 comparison before considering integration.')
note=f'''

**N4 source-repair reuse outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-return-reuse-pilot-20261018.md).
The independent filled-outer audit checks {audit['same_sheet_pairs']:,} same-sheet
pairs across all 48 common-mode layouts, retaining hole reservation and kerf.
There are {len(failed)} failed material pairs out of eight under the original +1%
limit. {details if failed else 'All eight pilot material pairs pass.'}
The candidate records {accepted} accepted exchanges from {attempts} attempts and
{reuses} compatible source-repair reuses. Reuse counts do not establish repair
completion or explain remaining failures. {decision} Production, prior failures
and frozen inputs remain unchanged. H2/H5 remain open at 60%.
'''

# Resolve every document and marker before making any append-only mutation.
status=root/'docs/STATUS.md';old_status=status.read_text(encoding='utf-8')
marker='**N4 assignment feasibility, 2026-10-18:**'
assert old_status.count(marker)==1
assert '**N4 source-repair reuse outcome, 2026-10-18:**' not in old_status
updated_status=old_status.replace(marker,note.strip()+'\n\n'+marker,1)
report=out.parent/(out.name+'.md');assert report.exists()
assert '## Independent hole-reservation check and decision' not in report.read_text(encoding='utf-8')
assert not (out/'record-outcome.py').exists()
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    assert '**N4 source-repair reuse outcome, 2026-10-18:**' not in (root/name).read_text(encoding='utf-8')
old_benchmark=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==old_benchmark

def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
append(report,f'''

## Independent hole-reservation check and decision

All 48 common-mode layouts pass the independent filled-outer audit of
{audit['same_sheet_pairs']:,} same-sheet pairs. Shapely {audit['shapely_version']}
transforms each original outer ring and checks disjointness and at least the
requested kerf, with the unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm
checking tolerance. Minimum clearance slack is {audit['minimum_clearance_slack_mm']:.12g} mm.
No hole interiors are subtracted.

**{decision}** There are {len(failed)} failed material pairs out of eight.
{details if failed else 'All eight pairs meet the original +1% material limit.'}
The candidate records {accepted} accepted exchanges from {attempts} attempts,
with {reuses} compatible source-repair reuses. Counters alone do not identify
the repair stages that remain unsuccessful, establish causality or prove
impossibility. No unchanged-build rerun, production integration or relaxed
limit follows. H2/H5 remain open; milestone completion stays 60%.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Compatible source-repair reuse paired outcome

[All 72 outcomes validate](benchmarks/results/h5-return-reuse-pilot-20261018.md)
with original quantities, independently cross-checked metrics and public
exports in {r['wall_seconds']/60:.3f} minutes. All original archives pass CRC and
member/hash checks. The independent filled-outer audit verifies
{audit['same_sheet_pairs']:,} same-sheet pairs across 48 common-mode layouts.
Minimum clearance slack is {audit['minimum_clearance_slack_mm']:.12g} mm against
the unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm checking tolerance.

{len(failed)} of eight material pairs fail the original +1% limit.
{details if failed else 'All eight pilot material pairs pass.'}
There are {accepted}/{attempts} accepted/attempted exchanges and {reuses} source
repair reuses. A reuse count alone does not establish a completed repair or
explain failure stages. {decision} All prior failed results, production and
frozen inputs remain unchanged; no reserved-input access or H5 credit.
H2/H5 remain open at 60%.
''')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,note)
status.write_text(updated_status,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
shutil.copyfile(root/'benchmarks/results/h5-return-reuse-preparation-20261018/candidate-final.patch',out/'candidate-formatted.patch')
assert (root/'BENCHMARKS.md').read_bytes().startswith(old_benchmark)
print(json.dumps({'failed_material_pairs':len(failed),'accepted':accepted,'attempted':attempts,'source_reuses':reuses,'decision':decision}))
