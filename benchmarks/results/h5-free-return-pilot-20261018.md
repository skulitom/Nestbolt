# Free-space-return exchange pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. Every original limit and the
complete 13-job requirement remain.

[Committed plan](h5-free-return-pilot-20261018/plan.json),
[all results](h5-free-return-pilot-20261018/results.json),
[archive verification](h5-free-return-pilot-20261018/verification.json),
[pair counters](h5-free-return-pilot-20261018/pair-counters.json).

## Method

The candidate searches at most 256 translations for each returned part
against the current source and already placed returns. It keeps original
orientations and reflections, reserves filled holes, charges geometry work
and observes the shared deadline. The prior seed remains as fallback.
Original choices, repair allocation and strict acceptance are unchanged.
[Qualification](h5-free-return-preparation-20261018.md) retains 137 passing
tests: 130 prior tests unchanged, three fixture expectations revised after
independent validation of actual improvement, and four new regressions.
The expected old-behavior failures, obsolete assumptions and corrected
coordinate-frame oracle remain. Exact source reconstruction, deterministic
public replays, independent authored checks, lint and build pass.

Four jobs, two kerfs, seeds 0–2 and three arms produce 72 outcomes. Ordinary
baseline, common baseline and common candidate run sequentially on the same
physical CCD0 core in rotating order; at most eight blocks run together.
Each search gets 60 seconds. Frozen geometry, quantities, stock and rotations
are unchanged. Block, score, case and measurement methods are AST-identical
to the preceding pilot. Every outcome requires independent validation and
public export; common mode must reserve hole interiors.
The session took 8.905 minutes.

## Three-seed medians

Positive material differences are worse. The unchanged limit is +1% against
ordinary mode. Exchange counts sum all three seeds; an accepted exchange
alone does not establish better final material use.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs baseline | Cut saving | All accepted / attempted | Pair accepted / attempted | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.616846% | +5.281226% | -0.317771% | 11.773372% | 3 / 9 | 2 / 8 | NO |
| m-mechanical-large-plates | 1.5 | +5.698164% | +5.706866% | +0.008233% | 13.343033% | 2 / 24 | 1 / 13 | NO |
| m-mechanical-panel-hardware | 0.2 | +6.261522% | +6.604732% | +0.322986% | 1.625803% | 2 / 14 | 2 / 8 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.895094% | +5.890184% | -0.004637% | 5.597291% | 1 / 28 | 0 / 15 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | -1.457950% | -0.882086% | +0.584384% | 22.426966% | 4 / 11 | 4 / 11 | yes |
| c-bracket-mixed | 1.5 | +1.067306% | +1.090957% | +0.023402% | 21.754746% | 4 / 7 | 4 / 7 | NO |

## Evidence and limits

Every attempt retains its original ZIP. CRC, member/layout hashes, counters
and independent metrics are verified; the summary is recomputed from every
record. A failed or incomplete arm cannot yield a passing median. All source,
binary, runner, data and environment guards remain unchanged.
The prior failed pilots, source-repair traces and authored witnesses remain.
No gate change, production integration or held-out access follows from this
diagnostic alone. H2/H5 remain open; completed weight is 60%.

## Observed follow-up gap filling

| Job | Kerf mm | Calls after accepted exchanges | Parts moved |
| --- | ---: | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 3 | 2 |
| m-mechanical-large-plates | 1.5 | 2 | 2 |
| m-mechanical-panel-hardware | 0.2 | 2 | 0 |
| m-mechanical-panel-hardware | 1.5 | 1 | 1 |
| m-box-mini | 0.2 | 0 | 0 |
| m-box-mini | 1.5 | 0 | 0 |
| c-bracket-mixed | 0.2 | 4 | 9 |
| c-bracket-mixed | 1.5 | 4 | 3 |

The step runs 16 times and moves 17 parts in total.
These operation counts do not by themselves establish final material improvement.

## Rejected unchanged-inventory swaps

| Job | Kerf mm | Rejections without material reduction |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 0 |
| m-mechanical-large-plates | 1.5 | 0 |
| m-mechanical-panel-hardware | 0.2 | 0 |
| m-mechanical-panel-hardware | 1.5 | 0 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 4 |
| c-bracket-mixed | 1.5 | 2 |

The exact-state, material-profile and original neutral guards reject 6 unchanged-inventory proposals without material reduction.
These counts do not identify other rejection stages or prove a global packing bound.

## Mixed-original-item exchanges

| Job | Kerf mm | Mixed accepted / attempted |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 0 / 0 |
| m-mechanical-large-plates | 1.5 | 0 / 3 |
| m-mechanical-panel-hardware | 0.2 | 0 / 0 |
| m-mechanical-panel-hardware | 1.5 | 0 / 0 |
| m-box-mini | 0.2 | 0 / 0 |
| m-box-mini | 1.5 | 0 / 0 |
| c-bracket-mixed | 0.2 | 1 / 1 |
| c-bracket-mixed | 1.5 | 0 / 0 |

There are 1 accepted mixed-item exchanges in 4 attempts.
These are subsets of the paired counters and do not establish final material improvement.

## Exact-state early rejections

| Job | Kerf mm | Exact duplicates rejected before validation |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 0 |
| m-mechanical-large-plates | 1.5 | 0 |
| m-mechanical-panel-hardware | 0.2 | 0 |
| m-mechanical-panel-hardware | 1.5 | 0 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 0 |
| c-bracket-mixed | 1.5 | 0 |

There are 0 exact-state rejections before repeated validation.
These are a subset of neutral rejections. Counts alone do not establish
saved wall time or final material improvement.

## Proven unchanged-material rejections

| Job | Kerf mm | Profile rejections before full validation |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 0 |
| m-mechanical-large-plates | 1.5 | 0 |
| m-mechanical-panel-hardware | 0.2 | 0 |
| m-mechanical-panel-hardware | 1.5 | 0 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 3 |
| c-bracket-mixed | 1.5 | 2 |

There are 5 material-profile rejections before full validation.
These and exact-state rejections are disjoint subsets of neutral rejections.
Counts do not measure saved time or establish final material improvement.


## Independent hole-reservation check and decision

Shapely 2.1.2 independently transforms every original filled
outer ring and checks 133,284 same-sheet pairs in 48 common-mode
layouts. All are disjoint and at least the requested kerf apart within the
unchanged 0.00000010 mm tolerance. Minimum slack is
0 mm. Hole interiors are not subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** 5 material pairs fail out of eight. m-mechanical-large-plates at 0.2 mm: +5.281226%; m-mechanical-large-plates at 1.5 mm: +5.706866%; m-mechanical-panel-hardware at 0.2 mm: +6.604732%; m-mechanical-panel-hardware at 1.5 mm: +5.890184%; c-bracket-mixed at 1.5 mm: +1.090957%
The candidate accepts 16/93 exchanges, including 13/62 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 16 times and moves 17 parts. Of 6 neutral rejections, 0 are caught by exact internal-state equality and 5 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject integration and a full H5 run for this candidate. All four mechanical comparisons remain above the original +1% material limit, and the 1.5 mm bracket comparison also fails. The candidate accepts eight of 75 mechanical exchange attempts, but aggregate counters cannot identify which physical members moved, the return-seed choices, the accepted height reductions or the remaining rejection causes. The authored gains therefore do not establish a useful final development improvement. The next step is a separately qualified observation-only diagnostic of this exact failed candidate: both mechanical jobs, both kerfs, seed zero and the original 60-second budget, serially on CCD0 CPU 8. Capture the actual returned poses before and after free-space seeding, source repair loss, charged work and actual whole-job material outcomes, including accepted trials. Do not recompute a former seed formula as if it were the actual new seed. Prove that removing instrumentation recovers the candidate exactly, retain all 137 tests, qualify the reader with actual authored outcomes and malformed records, and independently validate saved original geometry. Logging may perturb wall trajectories, so the diagnostic must make no quality claim. Use that evidence before selecting another search change; do not repeat this unchanged quality pilot, relax limits, integrate it or open reserved inputs.
H2/H5 remain open at 60%.

All six hosted checks on preceding main `8ae8b69` pass, including Windows, Linux, browsers and both maker rebuilds. This is evidence for that checkpoint; the subsequent isolated free-space candidate still fails its original material pilot and remains excluded from production. [Six completed checks](h5-free-return-pilot-20261018/main-ci-8ae8b69.json).
