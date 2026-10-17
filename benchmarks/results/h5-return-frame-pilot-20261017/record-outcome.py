from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-return-frame-pilot-20261017'
load=lambda p:json.loads(p.read_bytes())
r=load(out/'results.json');v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json')
assert v['all_original_archives_verified'] and v['valid']==v['attempts']==72
assert audit['all_holes_reserved'] and audit['cases']==48
pairs=r['summary']['pairs'];assert len(pairs)==8 and all(p['complete'] for p in pairs)
failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
attempts=sum(p['arms']['candidate']['exchange_attempts'] for p in pairs)
accepted=sum(p['arms']['candidate']['exchanges'] for p in pairs)
details='; '.join(f"{p['job']} at {p['kerf_mm']} mm: {p['candidate_vs_normal_percent']:+.6f}%" for p in failed)
decision=('Reject this candidate for integration; do not open the full 13-job gate for it.' if failed else
          'The pilot meets its material checks; require the complete original 13-job H5 comparison before considering integration.')
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
append(out.parent/(out.name+'.md'),f'''

## Independent hole-reservation check and decision

All 48 common-mode layouts pass the independent filled-outer audit of
{audit['same_sheet_pairs']:,} same-sheet pairs. Shapely {audit['shapely_version']}
transforms every original outer ring and checks disjointness and at least the
requested kerf, with the unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm
checking tolerance. Minimum clearance slack is {audit['minimum_clearance_slack_mm']:.12g} mm.
No hole interiors are subtracted.

**{decision}** There are {len(failed)} failed material pairs out of eight.
{details if failed else 'All eight pairs meet the original +1% material limit.'}
The candidate records {accepted} accepted exchanges from {attempts} attempts.
Counters alone do not identify repair-stage causes or prove impossibility.
No unchanged-build rerun, production integration or relaxed gate follows.
H2/H5 remain open; milestone completion stays 60%.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-17 — Reciprocal return-frame paired outcome

[All 72 outcomes validate](benchmarks/results/h5-return-frame-pilot-20261017.md)
with original quantities, exact independently cross-checked metrics and public
exports in {r['wall_seconds']/60:.3f} minutes. Every archive passes CRC and all
member/hash checks. The separate filled-outer audit verifies {audit['same_sheet_pairs']:,}
same-sheet pairs across 48 common-mode layouts, retaining holes and kerf spacing.
Minimum clearance slack is {audit['minimum_clearance_slack_mm']:.12g} mm against
the unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm audit tolerance.

{len(failed)} of eight material pairs fail the original +1% limit.
{details if failed else 'All eight pilot material pairs pass.'}
The candidate records {accepted}/{attempts} accepted/attempted exchanges.
{decision} Prior outcomes, guarded floating-point rejection and authored fixture
repairs remain preserved. Production and frozen inputs are unchanged; no
infeasibility claim or reserved-input access. H2/H5 remain open at 60%.
''')
note=f'''

**N4 return-frame outcome, 2026-10-17:** [all 72 outcomes validate](../benchmarks/results/h5-return-frame-pilot-20261017.md),
with an independent hole-reservation audit of {audit['same_sheet_pairs']:,} same-sheet
pairs across all 48 common-mode layouts. {len(failed)} of eight material pairs fail
the original +1% limit. {details if failed else 'All pilot material pairs pass.'}
There are {accepted} accepted exchanges from {attempts} attempts.
{decision} Production remains unchanged. Counters alone do not establish the
remaining repair bottleneck or impossibility. H2/H5 remain open at 60%.
'''
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,note)
p=root/'docs/STATUS.md';s=p.read_text(encoding='utf-8')
start=s.index('**N4 return-frame preparation, 2026-10-17:**')
end=s.index('**N4 preceding diagnostic, 2026-10-17:**',start)
s=s[:start]+note.strip()+'\n\n'+s[end:]
s=s.replace('**N4 latest outcome, 2026-10-17:**','**N4 preceding complete-set outcome, 2026-10-17:**')
p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
shutil.copyfile(root/'benchmarks/results/h5-return-frame-preparation-20261017/candidate-final.patch',out/'candidate-formatted.patch')
assert (root/'BENCHMARKS.md').read_bytes().startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
print(json.dumps({'failed_material_pairs':len(failed),'accepted':accepted,'attempted':attempts,'decision':decision}))
