"""Record every extended-repair pilot outcome under the original H5 limit."""
from pathlib import Path
import json, shutil, subprocess

root = Path(__file__).resolve().parents[1]
out = root / 'benchmarks/results/h5-extended-repair-pilot-20261018'
load = lambda p: json.loads(p.read_bytes())
r = load(out / 'results.json')
v = load(out / 'verification.json')
audit = load(out / 'filled-outer-audit.json')
assert v['all_original_archives_verified'] and v['valid'] == v['attempts'] == 72
assert audit['all_holes_reserved'] and audit['cases'] == 48
pairs = r['summary']['pairs']
assert len(pairs) == 8 and all(p['complete'] for p in pairs)
failed = [p for p in pairs if not p['candidate_within_original_material_limit']]
attempts = sum(p['arms']['candidate']['exchange_attempts'] for p in pairs)
accepted = sum(p['arms']['candidate']['exchanges'] for p in pairs)
counters = load(out / 'pair-counters.json')
fill = load(out / 'post-exchange-fill-counters.json')
neutral = load(out / 'neutral-rejections.json')
mixed = load(out / 'mixed-counters.json')
exact = load(out / 'exact-state-rejections.json')
profile = load(out / 'material-profile-rejections.json')
counts = (f"The candidate accepts {accepted}/{attempts} exchanges, including "
          f"{counters['accepted_pairs']}/{counters['attempted_pairs']} paired and "
          f"{mixed['accepted']}/{mixed['attempts']} mixed-item exchanges. Follow-up "
          f"gap filling runs {fill['calls']} times and moves {fill['moved']} parts. "
          f"Of {neutral['rejections']} neutral rejections, {exact['rejections']} "
          f"are caught by exact internal-state equality and {profile['rejections']} "
          "by the material profile before full validation. Counts do not establish "
          "time saving or improved final quality.")
stage = load(out / 'extended-counters.json')
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

details = '; '.join(f"{p['job']} at {p['kerf_mm']} mm: {p['candidate_vs_normal_percent']:+.6f}%" for p in failed)
if not failed:
    details = 'Every pilot material pair passes the original +1% limit.'
decision = ('Reject this candidate for integration; do not open the full 13-job gate for it.' if failed else
            'All eight pilot material pairs pass; require the complete original 13-job H5 comparison before considering integration.')
interpretation=load(out/'interpretation.json')
assert interpretation['failed_material_pairs']==len(failed) and interpretation['quality_claim'] is False
assert interpretation['results_sha256']==__import__('hashlib').sha256((out/'results.json').read_bytes()).hexdigest()
followup=interpretation['followup']

note = f'''**N4 extended-repair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-extended-repair-pilot-20261018.md).
The independent filled-outer audit checks {audit['same_sheet_pairs']:,} same-sheet
pairs across 48 common-mode layouts. {len(failed)} of eight material pairs fail
the original +1% limit. {details}
{counts} {decision} Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.
'''
status = root / 'docs/STATUS.md'
old = status.read_text(encoding='utf-8')
start = old.index('**N4 two-phase repair qualification, 2026-10-18:**')
end = old.index('**N4 ', start+1)
assert '**N4 extended-repair outcome, 2026-10-18:**' not in old
for name in ['docs/PLAN_V1_1.md', 'docs/V1_1_RESEARCH.md']:
    assert '**N4 extended-repair outcome, 2026-10-18:**' not in (root / name).read_text(encoding='utf-8')
assert not (out / 'record-outcome.py').exists()
prior = subprocess.check_output(['git', 'show', 'HEAD:BENCHMARKS.md'], cwd=root)
assert (root / 'BENCHMARKS.md').read_bytes() == prior

def append(path, text):
    with path.open('a', encoding='utf-8', newline='\n') as stream:
        stream.write(text)

append(out.parent / (out.name + '.md'), f'''

## Independent hole-reservation check and decision

Shapely {audit['shapely_version']} independently transforms every original filled
outer ring and checks {audit['same_sheet_pairs']:,} same-sheet pairs in 48 common-mode
layouts. All are disjoint and at least the requested kerf apart within the
unchanged {audit['absolute_clearance_tolerance_mm']:.8f} mm tolerance. Minimum slack is
{audit['minimum_clearance_slack_mm']:.12g} mm. Hole interiors are not subtracted.

**{decision}** {len(failed)} material pairs fail out of eight. {details}
{counts} {boundary_note}

[Final boundaries](h5-extended-repair-pilot-20261018/final-boundaries.json) and
[fixed-inventory area](h5-extended-repair-pilot-20261018/fixed-inventory-area.json)
retain all fifteen layouts from failed pairs.

{followup}
H2/H5 remain open at 60%.
''')
append(root / 'BENCHMARKS.md', f'''

## 2026-10-18 — Extended repair exchange comparison

[All 72 outcomes validate](benchmarks/results/h5-extended-repair-pilot-20261018.md)
with original quantities, public exports and independent metrics in
{r['wall_seconds']/60:.3f} minutes. All ZIP CRCs and member hashes pass; the summary
is recomputed from every record. An independent filled-outer audit checks
{audit['same_sheet_pairs']:,} same-sheet pairs in 48 layouts, retaining the original
{audit['absolute_clearance_tolerance_mm']:.8f} mm tolerance and reserved hole interiors.

{len(failed)} of eight material pairs fail the unchanged +1% limit. {details}
{counts} {decision} {followup}
No new reserved-input access or H5 credit. Production, frozen inputs and
earlier failures remain unchanged. H2/H5 remain open at 60%.
''')
for name in ['docs/PLAN_V1_1.md', 'docs/V1_1_RESEARCH.md']:
    append(root / name, '\n\n' + note)
status.write_text(old[:start] + note + '\n' + old[end:], encoding='utf-8', newline='\n')
review = {'pilot_material_failures': len(failed), 'attempts': attempts, 'accepted': accepted,
          'exact_state_rejections': exact['rejections'], 'material_profile_rejections': profile['rejections'],
          'neutral_rejections': neutral['rejections'], 'followup': followup,
          'current_attempt_member_coverage_observed': False, 'final_boundary_analysis_completed': True,
          'fixed_inventory_area_failures': capacity['same_inventory_area_failures'], 'quality_claim': False,
          'integrated': False, 'H5_complete': False}
(out / 'source-review.json').write_text(json.dumps(review, indent=2) + '\n', encoding='utf-8', newline='\n')
shutil.copyfile(__file__, out / 'record-outcome.py')
shutil.copyfile(root / 'benchmarks/results/h5-extended-repair-preparation-20261018/candidate.patch', out / 'candidate-formatted.patch')
shutil.copyfile(root / 'output/prepare_h5_extended_repair_finish.py', out / 'prepare-finish.py')
assert (root / 'BENCHMARKS.md').read_bytes().startswith(prior)
print(json.dumps({'failed_material_pairs': len(failed), 'accepted': accepted, 'attempts': attempts,
                  'profile_rejections': profile['rejections'], 'exact_rejections': exact['rejections'],
                  'decision': decision}))
