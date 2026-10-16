"""Describe the original completed preview measurement, including its failure."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/h4-preview-development-20261016'
load=lambda p:json.loads(p.read_bytes())
result=load(OUT/'results.json')
verification=load(OUT/'verification.json')
inventory=load(OUT/'integrity.json')
assert verification['all_artifact_checks_passed'] and inventory['crc_and_every_member_verified']
assert not result['all_quality_checks_pass']
full,subset=result['full_summary'],result['subset_summary']
lines=['# Integrated preview H4: complete original measurement — 2026-10-16','',
    '**H4 fails and the preview release remains pending.** All 603 newly measured',
    'layouts are valid, and all 195 reused frozen-v1 outcomes are verified. The',
    'Chrome subset exceeds the original +1% median limit. Every completed outcome,',
    'including Firefox, is retained; no unchanged-build repeat or threshold change',
    'was used. Completed milestone weight remains 45%.','',
    '[Full results](h4-preview-development-20261016/results.json),',
    '[artifact verification](h4-preview-development-20261016/verification.json),',
    '[original committed plan](h4-preview-development-20261016/plan.json).','',
    '## Fixed method','',
    'Product source is the integrated preview at `0a9fb44`. The union of the 65-job',
    'development matrix and eleven-job curve subset contains 67 jobs. Each engine',
    'runs all 67 at 60 seconds and seeds 0–2: 201 native, 201 Chrome and 201 Firefox',
    'attempts. Only 195 frozen-v1 development outcomes are reused, from the verified',
    'preceding archive. No current-build outcome, held-out input or final seed is',
    'substituted. One worker per browser job; eight physical CCD0 cores at most.',
    'Separate builds/tests use CCD1. All source, executable, site, input, runner',
    'and environment guards remain unchanged.','',
    f"The run took {result['wall_seconds']/60:.3f} minutes, below its four-hour cap.",
    'Every layout hash, requested part count and independent validation result is',
    'checked; saved and standalone metrics agree exactly. The public examples also',
    'pass validation against their original library/request. All six browser',
    'batches exit successfully with zero affinity deviations.','',
    '## Full 65-job comparisons','',
    'Three-seed job medians; positive differences mean more material. Native uses',
    'the unchanged +0.5% median bound. Browser G5 retains +2% median and total',
    'bounds, also checked for each seed separately.','',
    '| Comparison | Median difference | Total difference | Worst job | Result |',
    '| --- | ---: | ---: | ---: | --- |']
for label,row,passed in [('Native vs frozen v1',full['native_vs_v1'],full['native_vs_v1']['passes']),
    *[(name.title()+' vs native',row,row['passes_aggregate_bounds'] and row['all_seeds_within_original_G5_bounds']) for name,row in full['browsers_vs_native'].items()]]:
    lines.append(f"| {label} | {row['median_difference_percent']:+.6f}% | {row['total_difference_percent']:+.6f}% | {row['worst_difference_percent']:+.6f}% | {'pass' if passed else 'FAIL'} |")
lines += ['', '| Browser | Seed | Median difference | Total difference | Result |',
    '| --- | ---: | ---: | ---: | --- |']
for engine,value in full['browsers_vs_native'].items():
    for seed,row in value['per_seed'].items():
        lines.append(f"| {engine.title()} | {seed} | {row['median_difference_percent']:+.6f}% | {row['total_difference_percent']:+.6f}% | {'pass' if row['within_original_G5_bounds'] else 'FAIL'} |")
lines += ['', '## Eleven-job curve subset','',
    'The median must be at most +1%, and every job at most +5%. A full G5 pass',
    'does not override a failed subset.','',
    '| Browser | Valid | Median difference | Worst job | Total difference | Result |',
    '| --- | ---: | ---: | ---: | ---: | --- |']
for engine,row in subset['comparisons'].items():
    lines.append(f"| {engine.title()} | {row['valid']}/{row['attempted']} | {row['median_difference_percent']:+.6f}% | {row['worst_difference_percent']:+.6f}% | {row['total_difference_percent']:+.6f}% | {'pass' if row['passes_subset'] else 'FAIL'} |")
lines += ['', 'The earlier [Chrome failure report](h4-preview-chrome-failure-20261016.md)',
    'remains an accurate checkpoint taken while Firefox was running. This report',
    'adds the completed original arm. It does not identify which code change or',
    'source of timing variation caused the observed difference.','',
    '## Decision and retained evidence','',
    'Do not release this candidate from the failed result. The separately prepared',
    '[score-bound experiment](h4-score-chunks-preparation-20261016.md) must earn its',
    'own evidence; no optimization is accepted from this failure alone. Current',
    'scale checks have not been run on this failed build. The final corrected',
    'candidate still needs full requirements and release verification. H2/H5 remain',
    'open independently, and published v1 claims remain unchanged.','',
    f"The [raw archive](h4-preview-development-20261016/raw.zip) retains {len(inventory['members']):,} members,",
    f"{inventory['bytes']:,} bytes, SHA-256 `{inventory['sha256']}`.",
    'It includes all new raw results and validation outputs, original plans,',
    'process/browser metadata, exact native executables and the measured site.',
    'CRC, every member size and every hash were verified against the',
    '[inventory](h4-preview-development-20261016/integrity.json). Reused baseline',
    'bytes remain in their separately verified archive.','']
(OUT.parent/(OUT.name+'.md')).write_text('\n'.join(lines),encoding='utf-8',newline='\n')
print(json.dumps({'native_median':full['native_vs_v1']['median_difference_percent'],
    'subset':{k:{key:v[key] for key in ['median_difference_percent','worst_difference_percent','passes_subset']} for k,v in subset['comparisons'].items()},
    'all_quality_checks_pass':result['all_quality_checks_pass']}))
