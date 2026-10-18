# Productive-exchange pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. Every original limit and the
complete 13-job requirement remain.

[Committed plan](h5-productive-exchange-pilot-20261018/plan.json),
[all results](h5-productive-exchange-pilot-20261018/results.json),
[archive verification](h5-productive-exchange-pilot-20261018/verification.json),
[pair counters](h5-productive-exchange-pilot-20261018/pair-counters.json).

## Method

The candidate distributes bounded same-item pairs across original part
types and requires strict material improvement for equal-inventory swaps.
Changed-inventory swaps keep their original nonincrease rule. Geometry
validation, repairs, total limits and post-exchange filling remain.
The [preparation](h5-productive-exchange-preparation-20261018.md) retains
101 passing core tests, strict lint, public checks and both original
regression failures. A corrected positive fixture protects actual material
savings; its rounding-only predecessor remains preserved.

Four jobs, two kerfs, seeds 0–2 and three arms produce 72 outcomes. Ordinary
baseline, common baseline and common candidate run sequentially on the same
physical CCD0 core in rotating order; at most eight blocks run together.
Each search gets 60 seconds. Frozen geometry, quantities, stock and rotations
are unchanged. Block, score, case and measurement methods are AST-identical
to the preceding pilot. Every outcome requires independent validation and
public export; common mode must reserve hole interiors.
The session took 8.936 minutes.

## Three-seed medians

Positive material differences are worse. The unchanged limit is +1% against
ordinary mode. Exchange counts sum all three seeds; an accepted exchange
alone does not establish better final material use.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs baseline | Cut saving | All accepted / attempted | Pair accepted / attempted | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.482886% | +5.483065% | +0.000170% | 12.516393% | 3 / 14 | 0 / 11 | NO |
| m-mechanical-large-plates | 1.5 | +5.274215% | +5.402498% | +0.121856% | 13.948157% | 1 / 23 | 0 / 6 | NO |
| m-mechanical-panel-hardware | 0.2 | +7.178859% | +7.022646% | -0.145750% | 5.573654% | 0 / 18 | 0 / 6 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.981338% | +5.298801% | -0.644016% | 2.610913% | 0 / 22 | 0 / 6 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +0.046299% | +0.003025% | -0.043254% | 22.023208% | 4 / 29 | 1 / 23 | yes |
| c-bracket-mixed | 1.5 | +0.428995% | -0.263232% | -0.689270% | 21.207429% | 4 / 15 | 0 / 10 | yes |

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
| m-mechanical-large-plates | 0.2 | 3 | 3 |
| m-mechanical-large-plates | 1.5 | 1 | 1 |
| m-mechanical-panel-hardware | 0.2 | 0 | 0 |
| m-mechanical-panel-hardware | 1.5 | 0 | 0 |
| m-box-mini | 0.2 | 0 | 0 |
| m-box-mini | 1.5 | 0 | 0 |
| c-bracket-mixed | 0.2 | 4 | 5 |
| c-bracket-mixed | 1.5 | 4 | 2 |

The step runs 12 times and moves 11 parts in total.
These operation counts do not by themselves establish final material improvement.

## Rejected unchanged-inventory swaps

| Job | Kerf mm | Rejections without material reduction |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 11 |
| m-mechanical-large-plates | 1.5 | 5 |
| m-mechanical-panel-hardware | 0.2 | 6 |
| m-mechanical-panel-hardware | 1.5 | 6 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 12 |
| c-bracket-mixed | 1.5 | 5 |

The new guard rejects 45 unchanged-inventory proposals without material reduction.
These counts do not identify other rejection stages or prove a global packing bound.


## Independent hole-reservation check and decision

Shapely 2.1.2 independently transforms every original filled
outer ring and checks all 133,603 same-sheet pairs in 48
common-mode layouts. All pairs are disjoint and at least the requested kerf
apart within the unchanged 0.00000010 mm audit
tolerance. Minimum slack is 9.99999247131e-07 mm.
Hole interiors are not subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** 4 material pairs fail out of eight.
m-mechanical-large-plates at 0.2 mm: +5.483065%; m-mechanical-large-plates at 1.5 mm: +5.402498%; m-mechanical-panel-hardware at 0.2 mm: +7.022646%; m-mechanical-panel-hardware at 1.5 mm: +5.298801%
There are 12/121 accepted/attempted exchanges, including 1/62
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 11 parts. The new guard rejects 45 same-inventory proposals without material improvement; these counts alone do not establish final quality. Counters do not establish the remaining repair stage,
causality or impossibility. No unchanged-build quality rerun, integration or
relaxed limit follows. H2/H5 remain open at 60%.
