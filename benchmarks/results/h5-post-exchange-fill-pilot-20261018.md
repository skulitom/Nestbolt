# Post-exchange gap-fill pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. Every original limit and the
complete 13-job requirement remain.

[Committed plan](h5-post-exchange-fill-pilot-20261018/plan.json),
[all results](h5-post-exchange-fill-pilot-20261018/results.json),
[archive verification](h5-post-exchange-fill-pilot-20261018/verification.json),
[pair counters](h5-post-exchange-fill-pilot-20261018/pair-counters.json).

## Method

The candidate retains balanced pair exchanges and now runs the existing
direct gap-fill step after every accepted exchange. The original relocation
short circuit, exchange rules, gap sampler, work charges, normal mode and
overall search limits remain. Omitted-zero counters track follow-up calls
and parts moved. The [preparation](h5-post-exchange-fill-preparation-20261018.md)
retains 98 passing core tests, strict lint, public checks and the original
known-gap regression failure on the unchanged runtime.

Four jobs, two kerfs, seeds 0–2 and three arms produce 72 outcomes. Ordinary
baseline, common baseline and common candidate run sequentially on the same
physical CCD0 core in rotating order; at most eight blocks run together.
Each search gets 60 seconds. Frozen geometry, quantities, stock and rotations
are unchanged. Block, score, case and measurement methods are AST-identical
to the preceding pilot. Every outcome requires independent validation and
public export; common mode must reserve hole interiors.
The session took 8.968 minutes.

## Three-seed medians

Positive material differences are worse. The unchanged limit is +1% against
ordinary mode. Exchange counts sum all three seeds; an accepted exchange
alone does not establish better final material use.

| Job | Kerf mm | Baseline vs ordinary | Candidate vs ordinary | Candidate vs baseline | Cut saving | All accepted / attempted | Pair accepted / attempted | Within +1% |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | +5.484386% | +5.484564% | +0.000170% | 12.048090% | 3 / 3 | 2 / 2 | NO |
| m-mechanical-large-plates | 1.5 | +5.033031% | +5.388338% | +0.338281% | 12.574994% | 2 / 12 | 2 / 3 | NO |
| m-mechanical-panel-hardware | 0.2 | +5.916366% | +6.386542% | +0.443913% | 1.379583% | 3 / 3 | 3 / 3 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.594530% | +5.563315% | -0.029561% | 0.903554% | 3 / 3 | 3 / 3 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +0.439757% | +0.618323% | +0.177784% | 22.354470% | 4 / 14 | 1 / 11 | yes |
| c-bracket-mixed | 1.5 | +1.049160% | +0.525376% | -0.518345% | 21.176157% | 4 / 7 | 1 / 2 | yes |

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
| m-mechanical-large-plates | 1.5 | 2 | 0 |
| m-mechanical-panel-hardware | 0.2 | 3 | 0 |
| m-mechanical-panel-hardware | 1.5 | 3 | 0 |
| m-box-mini | 0.2 | 0 | 0 |
| m-box-mini | 1.5 | 0 | 0 |
| c-bracket-mixed | 0.2 | 4 | 7 |
| c-bracket-mixed | 1.5 | 4 | 5 |

The step runs 19 times and moves 14 parts in total.
These operation counts do not by themselves establish final material improvement.


## Independent hole-reservation check and decision

Shapely 2.1.2 independently transforms every original filled
outer ring and checks all 133,374 same-sheet pairs in 48
common-mode layouts. All pairs are disjoint and at least the requested kerf
apart within the unchanged 0.00000010 mm audit
tolerance. Minimum slack is 9.99999247131e-07 mm.
Hole interiors are not subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** 4 material pairs fail out of eight.
m-mechanical-large-plates at 0.2 mm: +5.484564%; m-mechanical-large-plates at 1.5 mm: +5.388338%; m-mechanical-panel-hardware at 0.2 mm: +6.386542%; m-mechanical-panel-hardware at 1.5 mm: +5.563315%
There are 19/42 accepted/attempted exchanges, including 12/24
two-part exchanges. The post-exchange gap-fill step runs 19 times and moves 14 parts; these counts alone do not establish final quality. Counters do not establish the remaining repair stage,
causality or impossibility. No unchanged-build quality rerun, integration or
relaxed limit follows. H2/H5 remain open at 60%.
