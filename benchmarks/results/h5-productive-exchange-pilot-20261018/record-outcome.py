from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-productive-exchange-pilot-20261018'
load=lambda p:json.loads(p.read_bytes())
r=load(out/'results.json');v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json');counters=load(out/'pair-counters.json')
assert v['all_original_archives_verified'] and v['valid']==v['attempts']==72
assert audit['all_holes_reserved'] and audit['cases']==48
pairs=r['summary']['pairs'];assert len(pairs)==8 and all(p['complete'] for p in pairs)
failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
attempts=sum(p['arms']['candidate']['exchange_attempts'] for p in pairs)
accepted=sum(p['arms']['candidate']['exchanges'] for p in pairs)
pa=counters['attempted_pairs'];pc=counters['accepted_pairs']
fill=load(out/'post-exchange-fill-counters.json')
neutral=load(out/'neutral-rejections.json')
fill_note=f"The post-exchange gap-fill step runs {fill['calls']} times and moves {fill['moved']} parts. The new guard rejects {neutral['rejections']} same-inventory proposals without material improvement; these counts alone do not establish final quality."
details='; '.join(f"{p['job']} at {p['kerf_mm']} mm: {p['candidate_vs_normal_percent']:+.6f}%" for p in failed)
decision=('Reject this candidate for integration; do not open the full 13-job gate for it.' if failed else
          'All eight pilot material pairs pass; require the complete original 13-job H5 comparison before considering integration.')
note=f'''**N4 productive-exchange outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-productive-exchange-pilot-20261018.md).
The independent filled-outer audit checks {audit['same_sheet_pairs']:,} same-sheet
pairs across 48 common-mode layouts. {len(failed)} of eight material pairs fail
the original +1% limit. {details if failed else 'All eight pilot material pairs pass.'}
The candidate accepts {accepted}/{attempts} total exchanges, including {pc}/{pa}
two-part exchanges. {fill_note} These counts do not establish improved final material or
identify remaining failure stages. {decision} Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.
'''
status=root/'docs/STATUS.md';old=status.read_text(encoding='utf-8')
start=old.index('**N4 productive-exchange preparation, 2026-10-18:**')
end=old.index('**N4 post-exchange gap-fill outcome, 2026-10-18:**',start)
assert '**N4 productive-exchange outcome, 2026-10-18:**' not in old
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:assert '**N4 productive-exchange outcome, 2026-10-18:**' not in (root/name).read_text(encoding='utf-8')
assert not (out/'record-outcome.py').exists()
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
append(out.parent/(out.name+'.md'),f'''

## Independent hole-reservation check and decision

Shapely {audit['shapely_version']} independently transforms every original filled
outer ring and checks all {audit['same_sheet_pairs']:,} same-sheet pairs in 48
common-mode layouts. All pairs are disjoint and at least the requested kerf
apart within the unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm audit
tolerance. Minimum slack is {audit['minimum_clearance_slack_mm']:.12g} mm.
Hole interiors are not subtracted.

**{decision}** {len(failed)} material pairs fail out of eight.
{details if failed else 'Every pair meets the original +1% material limit.'}
There are {accepted}/{attempts} accepted/attempted exchanges, including {pc}/{pa}
two-part exchanges. {fill_note} Counters do not establish the remaining repair stage,
causality or impossibility. No unchanged-build quality rerun, integration or
relaxed limit follows. H2/H5 remain open at 60%.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Productive-exchange comparison

[All 72 outcomes validate](benchmarks/results/h5-productive-exchange-pilot-20261018.md)
with original quantities, public exports and independent metrics in
{r['wall_seconds']/60:.3f} minutes. All archives pass CRC and member/hash checks;
the summary is recomputed from all records. The filled-outer audit verifies
{audit['same_sheet_pairs']:,} same-sheet pairs in 48 common-mode layouts with
minimum slack {audit['minimum_clearance_slack_mm']:.12g} mm and unchanged
{audit['absolute_clearance_tolerance_mm']:.8f} mm tolerance. Hole interiors stay reserved.

{len(failed)} of eight material pairs fail the original +1% limit.
{details if failed else 'Every pilot material pair passes.'}
The candidate accepts {accepted}/{attempts} exchanges, including {pc}/{pa}
two-part exchanges. {fill_note} {decision} Counts alone do not identify failure stages or
prove impossibility. Original failures, production and frozen inputs remain
unchanged. No reserved-input access or H5 credit; H2/H5 remain open at 60%.
''')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
status.write_text(old[:start]+note+'\n'+old[end:],encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'record-outcome.py')
shutil.copyfile(root/'benchmarks/results/h5-productive-exchange-preparation-20261018/candidate-final.patch',out/'candidate-formatted.patch')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'failed_material_pairs':len(failed),'accepted':accepted,'attempted':attempts,'pair_accepted':pc,'pair_attempted':pa,'decision':decision}))
