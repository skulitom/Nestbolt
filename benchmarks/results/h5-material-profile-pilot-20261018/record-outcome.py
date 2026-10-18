"""Record the complete material-profile pilot without changing any gate."""
from pathlib import Path
from hashlib import sha256
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-material-profile-pilot-20261018'
load=lambda p:json.loads(p.read_bytes());digest=lambda p:sha256(p.read_bytes()).hexdigest()
r=load(out/'results.json');v=load(out/'verification.json');audit=load(out/'filled-outer-audit.json')
assert v['all_original_archives_verified'] and v['valid']==v['attempts']==72
assert audit['all_holes_reserved'] and audit['cases']==48
pairs=r['summary']['pairs'];assert len(pairs)==8 and all(p['complete'] for p in pairs)
failed=[p for p in pairs if not p['candidate_within_original_material_limit']]
attempts=sum(p['arms']['candidate']['exchange_attempts'] for p in pairs)
accepted=sum(p['arms']['candidate']['exchanges'] for p in pairs)
counters=load(out/'pair-counters.json');fill=load(out/'post-exchange-fill-counters.json')
neutral=load(out/'neutral-rejections.json');mixed=load(out/'mixed-counters.json')
exact=load(out/'exact-state-rejections.json');profile=load(out/'material-profile-rejections.json')
counts=f"The candidate accepts {accepted}/{attempts} exchanges, including {counters['accepted_pairs']}/{counters['attempted_pairs']} paired and {mixed['accepted']}/{mixed['attempts']} mixed-item exchanges. Follow-up gap filling runs {fill['calls']} times and moves {fill['moved']} parts. Of {neutral['rejections']} neutral rejections, {exact['rejections']} are caught by exact internal-state equality and {profile['rejections']} by the material profile before full validation. Counts do not establish time saving or improved final quality."
details='; '.join(f"{p['job']} at {p['kerf_mm']} mm: {p['candidate_vs_normal_percent']:+.6f}%" for p in failed)
if not failed:details='Every pilot material pair passes the original +1% limit.'
decision=('Reject this candidate for integration; do not open the full 13-job gate for it.' if failed else
    'All eight pilot material pairs pass; require the complete original 13-job H5 comparison before considering integration.')
note=f'''**N4 material-profile rejection outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-material-profile-pilot-20261018.md).
The independent filled-outer audit checks {audit['same_sheet_pairs']:,} same-sheet
pairs across 48 common-mode layouts. {len(failed)} of eight material pairs fail
the original +1% limit. {details}
{counts} {decision} Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.
'''
status=root/'docs/STATUS.md';old=status.read_text(encoding='utf-8')
start=old.index('**N4 material-profile candidate preparation, 2026-10-18:**')
end=old.index('**N4 exact-state early-rejection outcome, 2026-10-18:**',start)
assert '**N4 material-profile rejection outcome, 2026-10-18:**' not in old
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    assert '**N4 material-profile rejection outcome, 2026-10-18:**' not in (root/name).read_text(encoding='utf-8')
assert not (out/'record-outcome.py').exists()
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
assert (root/'BENCHMARKS.md').read_bytes()==prior
def append(p,text):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(text)
append(out.parent/(out.name+'.md'),f'''

## Independent hole-reservation check and decision

Shapely {audit['shapely_version']} independently transforms every original filled
outer ring and checks {audit['same_sheet_pairs']:,} same-sheet pairs in 48 common-mode
layouts. All are disjoint and at least the requested kerf apart within the
unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm tolerance. Minimum slack is
{audit['minimum_clearance_slack_mm']:.12g} mm. Hole interiors are not subtracted.

**{decision}** {len(failed)} material pairs fail out of eight. {details}
{counts} No unchanged-build quality rerun, integration or relaxed limit
follows. H2/H5 remain open at 60%.
''')
append(root/'BENCHMARKS.md',f'''

## 2026-10-18 — Exact material-profile rejection comparison

[All 72 outcomes validate](benchmarks/results/h5-material-profile-pilot-20261018.md)
with original quantities, public exports and independent metrics in
{r['wall_seconds']/60:.3f} minutes. All ZIP CRCs and member hashes pass; the summary
is recomputed from every record. An independent filled-outer audit checks
{audit['same_sheet_pairs']:,} same-sheet pairs in 48 layouts, retaining the original
{audit['absolute_clearance_tolerance_mm']:.8f} mm tolerance and reserved hole interiors.

{len(failed)} of eight material pairs fail the unchanged +1% limit. {details}
{counts} {decision} No new reserved-input access or H5 credit. Production,
frozen inputs and earlier failures remain unchanged. H2/H5 remain open at 60%.
''')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
status.write_text(old[:start]+note+'\n'+old[end:],encoding='utf-8',newline='\n')
frontier=root/'output/h5-neutral-frontier-review-20261018';f=load(frontier/'checks.json')
assert f['all_checks_passed'] and f['pairs']==f['pairs_with_unchanged_credited_top_poses']==6
choices=load(frontier/'choices.json')
assert choices['all_checks_passed'] and choices['archived_diagnostics']==2 and choices['attempts']==16 and choices['attempts_selecting_insert']==0
assert digest(root/f['source'])==f['source_sha256'];shutil.copytree(frontier,out/'neutral-frontier-review')
followup=('The six previously validated neutral panel pairs preserve the physical poses of both inserts defining the height of the sheet receiving the largest offcut credit. Five pairs change other poses. This explains their unchanged material, but does not identify every new pilot failure. The next diagnostic should connect actual attempted exchange members to the parts defining charged height, including whether the current ordering reaches those parts. Qualify any resulting selector change with authored cases and retain all budgets and full acceptance checks. No new selector or quality gain is established.' if failed else
    'The pilot passes all eight material pairs. Preserve this candidate and proceed to the complete original 13-job gate before considering any further algorithm change. The supplemental frontier inspection explains only six older neutral pairs and warrants no quality claim.')
review={'pilot_material_failures':len(failed),'exact_state_rejections':exact['rejections'],
    'material_profile_rejections':profile['rejections'],'neutral_rejections':neutral['rejections'],
    'supplemental_pairs':6,'supplemental_searches':0,'earlier_attempts':16,'earlier_attempts_selecting_insert':0,
    'old_selection_coverage_not_attributed_to_current_pilot':True,
    'new_selector_implemented':False,'followup':followup,'quality_claim':False}
(out/'source-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
append(out.parent/(out.name+'.md'),'\n\n## Read-only inspection of parts setting the used height\n\n'+followup+'\n\n[Saved-layout inspection](h5-material-profile-pilot-20261018/neutral-frontier-review/checks.json).\n')
append(out.parent/(out.name+'.md'),'\nMapping the pinned importer indices back to original part IDs also shows that none of the 16 attempts in those two earlier diagnostics selects an insert. The insert pair is present later in the choices. This coverage predates the new profile branch and is not attributed to its pilot. [Retained choice audit](h5-material-profile-pilot-20261018/neutral-frontier-review/choices.json).\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    append(root/name,'\nThe [read-only frontier inspection](../benchmarks/results/h5-material-profile-pilot-20261018/source-review.json) finds unchanged top-defining insert poses in all six older neutral panel pairs. It uses no new search or held-out geometry and makes no claim about every current failure.\n')
append(root/'BENCHMARKS.md','\nA read-only inspection of six older validated neutral panel pairs finds unchanged physical poses for the two inserts setting the credited sheet height. Five pairs move other parts. The saved evidence motivates checking actual selection order if this pilot fails; it neither implements a selector nor proves a gain or packing bound.\n')
shutil.copyfile(__file__,out/'record-outcome.py')
shutil.copyfile(root/'benchmarks/results/h5-material-profile-preparation-20261018/candidate.patch',out/'candidate-formatted.patch')
shutil.copyfile(root/'output/prepare_h5_material_profile_finish.py',out/'prepare-finish.py')
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'failed_material_pairs':len(failed),'accepted':accepted,'attempts':attempts,
    'profile_rejections':profile['rejections'],'exact_rejections':exact['rejections'],'decision':decision}))
