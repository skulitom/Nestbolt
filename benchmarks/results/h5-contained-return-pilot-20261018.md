# Contained-return exchange pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. Every original limit and the
complete 13-job requirement remain.

[Committed plan](h5-contained-return-pilot-20261018/plan.json),
[all results](h5-contained-return-pilot-20261018/results.json),
[archive verification](h5-contained-return-pilot-20261018/verification.json),
[pair counters](h5-contained-return-pilot-20261018/pair-counters.json).

## Method

The candidate shifts fitting return groups into the existing source
bounding box before the original repair. Already contained, oversized
or numerically uncontained groups retain their old poses. Original and
proposed geometry work is charged. Orientations and reflection, choices,
repair budgets and exact material/geometry acceptance remain. The
[preparation](h5-contained-return-preparation-20261018.md) retains 133
passing optimized tests, all 130 prior tests unchanged, 29 public CLI
checks, deterministic replays and exact source reconstruction. Expected
old-behavior failures and the repaired rotated-edge failure are preserved.

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
| m-mechanical-large-plates | 0.2 | +5.228683% | +5.219533% | -0.008695% | 11.762053% | 3 / 9 | 2 / 8 | NO |
| m-mechanical-large-plates | 1.5 | +5.046009% | +5.440022% | +0.375086% | 13.191587% | 1 / 24 | 1 / 12 | NO |
| m-mechanical-panel-hardware | 0.2 | +5.760002% | +5.617328% | -0.134904% | 1.629783% | 2 / 13 | 2 / 7 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.661753% | +5.658268% | -0.003298% | 6.058131% | 0 / 34 | 0 / 17 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +0.572116% | +2.014519% | +1.434198% | 22.641992% | 4 / 22 | 3 / 21 | NO |
| c-bracket-mixed | 1.5 | +0.051243% | +0.760888% | +0.709281% | 21.903055% | 4 / 9 | 4 / 9 | yes |

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
| m-mechanical-large-plates | 1.5 | 1 | 1 |
| m-mechanical-panel-hardware | 0.2 | 2 | 0 |
| m-mechanical-panel-hardware | 1.5 | 0 | 0 |
| m-box-mini | 0.2 | 0 | 0 |
| m-box-mini | 1.5 | 0 | 0 |
| c-bracket-mixed | 0.2 | 4 | 9 |
| c-bracket-mixed | 1.5 | 4 | 2 |

The step runs 14 times and moves 14 parts in total.
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
| c-bracket-mixed | 0.2 | 2 |
| c-bracket-mixed | 1.5 | 1 |

The exact-state, material-profile and original neutral guards reject 3 unchanged-inventory proposals without material reduction.
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
| c-bracket-mixed | 0.2 | 2 |
| c-bracket-mixed | 1.5 | 1 |

There are 3 material-profile rejections before full validation.
These and exact-state rejections are disjoint subsets of neutral rejections.
Counts do not measure saved time or establish final material improvement.


## Independent hole-reservation check and decision

Shapely 2.1.2 independently transforms every original filled
outer ring and checks 133,170 same-sheet pairs in 48 common-mode
layouts. All are disjoint and at least the requested kerf apart within the
unchanged 0.00000010 mm tolerance. Minimum slack is
4.07482377784e-07 mm. Hole interiors are not subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** 5 material pairs fail out of eight. m-mechanical-large-plates at 0.2 mm: +5.219533%; m-mechanical-large-plates at 1.5 mm: +5.440022%; m-mechanical-panel-hardware at 0.2 mm: +5.617328%; m-mechanical-panel-hardware at 1.5 mm: +5.658268%; c-bracket-mixed at 0.2 mm: +2.014519%
The candidate accepts 14/111 exchanges, including 12/74 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 14 times and moves 14 parts. Of 3 neutral rejections, 0 are caught by exact internal-state equality and 3 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject integration and a full H5 run for this candidate. All four mechanical comparisons remain above the original +1% material limit, and the 0.2 mm bracket comparison also fails. The aggregate counters do not identify individual return-seed decisions or establish a causal quality improvement over earlier pilots. Read-only source review shows that this change seeks containment only: an already feasible return seed can still sit at the height-defining edge without trying a lower free space. The next distinct hypothesis is a bounded search for collision-free return positions in the existing source layout, considering original allowed orientations and preferring lower occupied extent, while retaining the previous seed as fallback. Qualify it on authored cases with exact quantities, strict hole reservation, deterministic work charging, disabled/expired behavior and the original material guard before a new pilot. Existing global cross-sheet moves already exist; do not duplicate them. Preserve every failed candidate and do not repeat this unchanged quality pilot or relax its limits.
H2/H5 remain open at 60%.
