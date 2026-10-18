# Mixed-original-item exchange pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. Every original limit and the
complete 13-job requirement remain.

[Committed plan](h5-mixed-exchange-pilot-20261018/plan.json),
[all results](h5-mixed-exchange-pilot-20261018/results.json),
[archive verification](h5-mixed-exchange-pilot-20261018/verification.json),
[pair counters](h5-mixed-exchange-pilot-20261018/pair-counters.json).

## Method

The candidate interleaves six existing same-item pairs with up to six
nearby mixed-item pairs. Mixed-group corner anchors supplement original
samples and charge their transforms. Existing phase/total budgets, repair
limits, complete obstruction sets, returned-area bound, per-member poses,
geometry/material guards and post-exchange filling remain.
The [preparation](h5-mixed-exchange-preparation-20261018.md) retains 107
passing core tests, strict lint, public checks and both original failures
(unchanged-runtime regression and first candidate missing seed two).

Four jobs, two kerfs, seeds 0–2 and three arms produce 72 outcomes. Ordinary
baseline, common baseline and common candidate run sequentially on the same
physical CCD0 core in rotating order; at most eight blocks run together.
Each search gets 60 seconds. Frozen geometry, quantities, stock and rotations
are unchanged. Block, score, case and measurement methods are AST-identical
to the preceding pilot. Every outcome requires independent validation and
public export; common mode must reserve hole interiors.
The session took 8.912 minutes.

## Three-seed medians

Positive material differences are worse. The unchanged limit is +1% against
ordinary mode. Exchange counts sum all three seeds; an accepted exchange
alone does not establish better final material use.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs baseline | Cut saving | All accepted / attempted | Pair accepted / attempted | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +4.737201% | +6.069459% | +1.272001% | 10.926929% | 2 / 25 | 0 / 15 | NO |
| m-mechanical-large-plates | 1.5 | +5.836022% | +6.160993% | +0.307051% | 11.988464% | 2 / 22 | 0 / 10 | NO |
| m-mechanical-panel-hardware | 0.2 | +6.817083% | +6.770269% | -0.043826% | 6.886945% | 0 / 27 | 0 / 11 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.179911% | +5.607046% | +0.406099% | 6.058131% | 0 / 24 | 0 / 9 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | -0.020039% | +0.581624% | +0.601783% | 22.538147% | 4 / 15 | 1 / 12 | yes |
| c-bracket-mixed | 1.5 | -1.459449% | +0.004365% | +1.485494% | 21.977948% | 4 / 19 | 0 / 12 | yes |

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
| m-mechanical-large-plates | 0.2 | 2 | 2 |
| m-mechanical-large-plates | 1.5 | 2 | 4 |
| m-mechanical-panel-hardware | 0.2 | 0 | 0 |
| m-mechanical-panel-hardware | 1.5 | 0 | 0 |
| m-box-mini | 0.2 | 0 | 0 |
| m-box-mini | 1.5 | 0 | 0 |
| c-bracket-mixed | 0.2 | 4 | 10 |
| c-bracket-mixed | 1.5 | 4 | 3 |

The step runs 12 times and moves 19 parts in total.
These operation counts do not by themselves establish final material improvement.

## Rejected unchanged-inventory swaps

| Job | Kerf mm | Rejections without material reduction |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 14 |
| m-mechanical-large-plates | 1.5 | 8 |
| m-mechanical-panel-hardware | 0.2 | 11 |
| m-mechanical-panel-hardware | 1.5 | 9 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 1 |
| c-bracket-mixed | 1.5 | 6 |

The new guard rejects 49 unchanged-inventory proposals without material reduction.
These counts do not identify other rejection stages or prove a global packing bound.

## Mixed-original-item exchanges

| Job | Kerf mm | Mixed accepted / attempted |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 0 / 4 |
| m-mechanical-large-plates | 1.5 | 0 / 4 |
| m-mechanical-panel-hardware | 0.2 | 0 / 0 |
| m-mechanical-panel-hardware | 1.5 | 0 / 0 |
| m-box-mini | 0.2 | 0 / 0 |
| m-box-mini | 1.5 | 0 / 0 |
| c-bracket-mixed | 0.2 | 0 / 1 |
| c-bracket-mixed | 1.5 | 0 / 2 |

There are 0 accepted mixed-item exchanges in 11 attempts.
These are subsets of the paired counters and do not establish final material improvement.


## Independent hole-reservation check and decision

Shapely 2.1.2 independently transforms every original filled
outer ring and checks all 133,299 same-sheet pairs in 48
common-mode layouts. All pairs are disjoint and at least the requested kerf
apart within the unchanged 0.00000010 mm audit
tolerance. Minimum slack is -5.99520433298e-15 mm.
Hole interiors are not subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** 4 material pairs fail out of eight.
m-mechanical-large-plates at 0.2 mm: +6.069459%; m-mechanical-large-plates at 1.5 mm: +6.160993%; m-mechanical-panel-hardware at 0.2 mm: +6.770269%; m-mechanical-panel-hardware at 1.5 mm: +5.607046%
There are 12/132 accepted/attempted exchanges, including 1/69
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 19 parts. The new guard rejects 49 same-inventory proposals without material improvement; mixed pairs account for 0/11 accepted/attempted exchanges. These counts alone do not establish final quality. Counters do not establish the remaining repair stage,
causality or impossibility. No unchanged-build quality rerun, integration or
relaxed limit follows. H2/H5 remain open at 60%.
