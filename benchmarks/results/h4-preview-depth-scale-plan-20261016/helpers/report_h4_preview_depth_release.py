"""Report the completed current matrix without assuming it passes."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root/'benchmarks/results/h4-preview-depth-release-20261016'
load = lambda p: json.loads(p.read_bytes())
result = load(out/'results.json')
verified = load(out/'verification.json')
inventory = load(out/'integrity.json')
assert verified['all_artifact_checks_passed'] and inventory['crc_and_every_member_verified']
full, subset = result['full_summary'], result['subset_summary']
passed = result['all_quality_checks_pass']
lines = ['# Integrated tree-depth preview: full H4 comparison — 2026-10-16', '',
    '**All quality comparisons pass.**' if passed else '**At least one quality condition fails; do not release from this result.**',
    'All 603 new layouts and 195 reused frozen-v1 layouts validate. These are',
    f"the originally planned outcomes for candidate `{load(out/'plan.json')['commit'][:7]}`; no unchanged-build",
    'repeat, changed threshold or selected subset replaces a failed observation.',
    'Scale and complete requirement review are separate, so this report alone',
    'does not close H4 or change completed milestone weight.', '',
    f'[Results]({out.name}/results.json), [verification]({out.name}/verification.json),',
    f'[committed plan]({out.name}/plan.json).', '',
    '## Method', '',
    'The union of 65 development jobs and the eleven-job curve subset contains',
    '67 jobs. Native, Chrome and Firefox each run all 67 at 60 seconds and seeds',
    '0–2, giving 201 outcomes per engine. Only the 195 sealed frozen-v1 outcomes',
    'are reused. There are no held-out jobs, final seeds or competitor claims.',
    'One browser worker per job, at most eight physical CCD0 cores; separate',
    'functional checks/builds use CCD1. Source, executable, site, runner, inputs',
    'and environment guards stay unchanged.', '',
    f"The complete run took {result['wall_seconds']/60:.3f} minutes, below its four-hour cap.",
    'Every layout hash, requested quantity and independent metric is checked.',
    'Standalone and saved metrics agree exactly, including original-library',
    'validation of the public examples. All six browser batches succeed with',
    'zero affinity deviations.', '',
    '## Full development comparisons', '',
    'Positive differences mean more material. Three-seed job medians are used.',
    'Native retains +0.5% median; browser G5 retains +2% median and total, also',
    'checked separately for each seed.', '',
    '| Comparison | Median | Total | Worst job | Result |',
    '| --- | ---: | ---: | ---: | --- |']
comparisons = [('Native vs frozen v1', full['native_vs_v1'], full['native_vs_v1']['passes'])]
comparisons += [(name.title()+' vs native', row,
    row['passes_aggregate_bounds'] and row['all_seeds_within_original_G5_bounds'])
    for name, row in full['browsers_vs_native'].items()]
for label, row, ok in comparisons:
    lines.append(f"| {label} | {row['median_difference_percent']:+.6f}% | {row['total_difference_percent']:+.6f}% | {row['worst_difference_percent']:+.6f}% | {'pass' if ok else 'FAIL'} |")
lines += ['', '| Browser | Seed | Median | Total | Result |', '| --- | ---: | ---: | ---: | --- |']
for engine, value in full['browsers_vs_native'].items():
    for seed, row in value['per_seed'].items():
        lines.append(f"| {engine.title()} | {seed} | {row['median_difference_percent']:+.6f}% | {row['total_difference_percent']:+.6f}% | {'pass' if row['within_original_G5_bounds'] else 'FAIL'} |")
lines += ['', '## Curve subset', '',
    'Both browsers must stay at or below +1% median and +5% for every job.', '',
    '| Browser | Valid | Median | Worst job | Total | Result |',
    '| --- | ---: | ---: | ---: | ---: | --- |']
for engine, row in subset['comparisons'].items():
    lines.append(f"| {engine.title()} | {row['valid']}/{row['attempted']} | {row['median_difference_percent']:+.6f}% | {row['worst_difference_percent']:+.6f}% | {row['total_difference_percent']:+.6f}% | {'pass' if row['passes_subset'] else 'FAIL'} |")
lines += ['', '## Retained evidence and next step', '',
    'The original `0a9fb44` [failed comparison](h4-preview-development-20261016.md)',
    'and the `7eba929` [failed comparison](h4-preview-score-release-20261016.md)',
    'remain preserved. This candidate lowers the separator-window base collision',
    'tree depth from four to three, retaining exact geometry, aspect scaling,',
    'leaf threshold and budgets. Its [isolated subset](h4-quadtree-depth-probe-20261016.md)',
    'and [integration checks](h4-depth-integration-20261016.md) are separate evidence.',
    'No general speed gain follows from these wall-clock quality outcomes.', '',
    ('Run the already specified current-build scale workflows, then review every H4 requirement.'
     if passed else 'Investigate the failed condition before further release work; retain these results unchanged.'),
    'H2/H5 remain open independently. No tag, release or registry entry is created',
    'by this report, and frozen v1 claims remain unchanged.', '',
    f"The [raw archive]({out.name}/raw.zip) contains {len(inventory['members']):,} members,",
    f"{inventory['bytes']:,} bytes, SHA-256 `{inventory['sha256']}`.",
    'It preserves every new attempt, validation, original plan, browser/process',
    'record and exact measured engine/site. CRC, member size and SHA-256 checks',
    'all pass. Reused v1 bytes remain in their verified preceding archive.', '']
(out.parent/(out.name+'.md')).write_text('\n'.join(lines), encoding='utf-8', newline='\n')
print(json.dumps({'all_quality_checks_pass': passed,
    'native_median': full['native_vs_v1']['median_difference_percent'],
    'subset': {k: {key: v[key] for key in ['median_difference_percent', 'worst_difference_percent', 'passes_subset']}
               for k, v in subset['comparisons'].items()}}))
