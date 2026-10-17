# Complete-set eligibility common-line exchange pilot — 2026-10-17

**72/72 attempts are valid.**
This four-job diagnostic does not complete H5. The full 13-job comparison
remains required, and no original acceptance limit changes. This pilot
earns no completed H5 milestone weight.

[Committed complete-set eligibility plan](h5-complete-set-pilot-20261017/plan.json),
[all results](h5-complete-set-pilot-20261017/results.json),
[archive verification](h5-complete-set-pilot-20261017/verification.json).

## Method

The isolated candidate exchanges a last-sheet part with an actual
obstruction set of up to three parts on an earlier sheet, repairs both sheets,
and accepts only after
the independent whole-job geometry/material guard passes. It keeps the
incumbent intact on failure. The call now runs at the first feasible window
before fill can short-circuit relocation, sharing the existing ten-percent
budget and capped at 1.2 seconds. Ordinary mode retains its original path.
Both matched arms include the current aba989e collision-tree depth change.
Complete two/three-blocker sets are eligible regardless of combined part area,
preserving relative transforms and the original smaller single-part
fallbacks. It changes neither budget nor coefficients. Production is unchanged.
Source, tests and matched observers are retained in the
[preparation evidence](h5-complete-set-preparation-20261017.md).

Each job/kerf/seed block runs ordinary baseline, common-line baseline and
common-line candidate sequentially on the same physical CCD0 core. Order
rotates; seeds are 0–2, both kerfs are tested, every search gets 60 seconds,
and at most eight blocks run together. Original frozen geometry, quantities,
stocks and rotations are unchanged. Independent validation, public export
and the ban on part-in-hole in common mode are required for a valid outcome.
The complete session took 8.947 minutes.

## Three-seed medians

Positive material differences are worse. The candidate must remain within
+1% of ordinary mode; improving over a failing common-line baseline alone
does not pass that condition. Exchange counts sum all three seeds.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs common baseline | Candidate cut saving | Exchanges / attempts | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.469402% | +5.433792% | -0.033763% | 9.456276% | 2 / 10 | NO |
| m-mechanical-large-plates | 1.5 | +5.670704% | +6.521291% | +0.804941% | 10.926317% | 1 / 19 | NO |
| m-mechanical-panel-hardware | 0.2 | +5.960081% | +5.700699% | -0.244791% | 1.351530% | 0 / 16 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.776905% | +5.764347% | -0.011872% | 5.204868% | 0 / 17 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +0.869278% | +0.453010% | -0.412680% | 21.871755% | 4 / 7 | yes |
| c-bracket-mixed | 1.5 | -0.549101% | +0.250096% | +0.803610% | 21.013285% | 4 / 5 | yes |

## Evidence and limits

Every attempted outcome, including failures, has its own immutable ZIP.
CRC, all member hashes, layout hashes, saved counters and independently
computed metrics/cut savings were checked; the summary is recomputed from
all original records. No valid-only median replaces a failed/incomplete arm.
Source, binary, runner, data and environment guards remain unchanged.

The [earlier atomic-set pilot](h5-obstruction-set-recovered-pilot-20261016.md)
remains preserved with all 72 valid outcomes and five failed material pairs.
[Four diagnostic traces](h5-obstruction-stage-diagnosis-20261017.md) observed
620 complete sets rejected by the old area filter, and no complete sets
attempted. A validated authored example and equal/larger-area exchange tests
motivate this separate candidate. Those observations do not prove that any
particular mechanical proposal is feasible. This matched pilot evaluates
the changed eligibility on development jobs only. No quality/material limit
changes, and no isolated candidate is automatically integrated.
H2/H5 remain open; completed milestone weight is 60%.


## Independent hole-reservation check and decision

The [separate filled-outer audit](h5-complete-set-pilot-20261017/filled-outer-audit.json)
uses Shapely 2.1.2, independent original outer rings and every rigid placement.
All 48 common-mode layouts pass 133,412 same-sheet pair checks:
no overlap and at least the requested kerf, within the unchanged 0.0000001 mm
checking tolerance. Minimum observed clearance slack is
9.99999247131e-07 mm. No hole interiors are subtracted.

**Do not integrate this candidate.** All four mechanical job/kerf medians fail
the original +1% material limit (+5.433792%, +6.521291%, +5.700699%, +5.764347%).
All four control pairs meet the material limit. There are 74 exchange attempts
and eleven acceptances overall, with none on panel hardware. Aggregate counters
do not distinguish complete versus partial sets or the failed repair stage;
they do not justify another unchanged-build run or an infeasibility claim.
The full 13-job gate is not opened for this rejected candidate.
