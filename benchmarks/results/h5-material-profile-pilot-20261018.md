# Exact material-profile rejection pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. Every original limit and the
complete 13-job requirement remain.

[Committed plan](h5-material-profile-pilot-20261018/plan.json),
[all results](h5-material-profile-pilot-20261018/results.json),
[archive verification](h5-material-profile-pilot-20261018/verification.json),
[pair counters](h5-material-profile-pilot-20261018/pair-counters.json).

## Method

The candidate retains exact-state rejection and adds a sufficient
unchanged-material check for same-inventory exchanges. It uses original
geometry footprints, transforms and grid from the unchanged validator.
Profiles require the same immutable job, sheet/stock assignments, exact
sheet maxima and original copy identities. Equality permits rejection
only. Every accepted exchange retains full geometry and strict material
checks. Budgets and coefficients are unchanged; new footprint work uses
the existing validated-vertex charge. The [preparation]
(h5-material-profile-preparation-20261018.md) retains 123 passing optimized
tests, all 117 prior tests unchanged, 47 frozen-CLI profile checks and
24 frozen-CLI branch checks. Original preparation failures and the
expected failing regression remain. Strict lint/build, public parity
and exact deterministic replays pass.

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
| m-mechanical-large-plates | 0.2 | +5.456113% | +5.169797% | -0.271502% | 12.377450% | 3 / 13 | 3 / 13 | NO |
| m-mechanical-large-plates | 1.5 | +5.935324% | +6.158488% | +0.210661% | 13.419174% | 2 / 29 | 1 / 19 | NO |
| m-mechanical-panel-hardware | 0.2 | +6.182428% | +6.407212% | +0.211696% | 5.300606% | 0 / 39 | 0 / 26 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.920884% | +5.654893% | -0.251123% | 6.058131% | 0 / 38 | 0 / 24 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +0.394613% | +1.823168% | +1.422940% | 22.442185% | 4 / 19 | 3 / 17 | NO |
| c-bracket-mixed | 1.5 | -0.823913% | +0.539842% | +1.375084% | 21.582693% | 4 / 9 | 4 / 9 | yes |

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
| m-mechanical-large-plates | 0.2 | 3 | 5 |
| m-mechanical-large-plates | 1.5 | 2 | 2 |
| m-mechanical-panel-hardware | 0.2 | 0 | 0 |
| m-mechanical-panel-hardware | 1.5 | 0 | 0 |
| m-box-mini | 0.2 | 0 | 0 |
| m-box-mini | 1.5 | 0 | 0 |
| c-bracket-mixed | 0.2 | 4 | 8 |
| c-bracket-mixed | 1.5 | 4 | 1 |

The step runs 13 times and moves 16 parts in total.
These operation counts do not by themselves establish final material improvement.

## Rejected unchanged-inventory swaps

| Job | Kerf mm | Rejections without material reduction |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 8 |
| m-mechanical-large-plates | 1.5 | 4 |
| m-mechanical-panel-hardware | 0.2 | 18 |
| m-mechanical-panel-hardware | 1.5 | 18 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 0 |
| c-bracket-mixed | 1.5 | 1 |

The exact-state, material-profile and original neutral guards reject 49 unchanged-inventory proposals without material reduction.
These counts do not identify other rejection stages or prove a global packing bound.

## Mixed-original-item exchanges

| Job | Kerf mm | Mixed accepted / attempted |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 1 / 1 |
| m-mechanical-large-plates | 1.5 | 0 / 3 |
| m-mechanical-panel-hardware | 0.2 | 0 / 8 |
| m-mechanical-panel-hardware | 1.5 | 0 / 6 |
| m-box-mini | 0.2 | 0 / 0 |
| m-box-mini | 1.5 | 0 / 0 |
| c-bracket-mixed | 0.2 | 0 / 0 |
| c-bracket-mixed | 1.5 | 0 / 0 |

There are 1 accepted mixed-item exchanges in 18 attempts.
These are subsets of the paired counters and do not establish final material improvement.

## Exact-state early rejections

| Job | Kerf mm | Exact duplicates rejected before validation |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 0 |
| m-mechanical-large-plates | 1.5 | 0 |
| m-mechanical-panel-hardware | 0.2 | 3 |
| m-mechanical-panel-hardware | 1.5 | 0 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 0 |
| c-bracket-mixed | 1.5 | 0 |

There are 3 exact-state rejections before repeated validation.
These are a subset of neutral rejections. Counts alone do not establish
saved wall time or final material improvement.

## Proven unchanged-material rejections

| Job | Kerf mm | Profile rejections before full validation |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 8 |
| m-mechanical-large-plates | 1.5 | 4 |
| m-mechanical-panel-hardware | 0.2 | 15 |
| m-mechanical-panel-hardware | 1.5 | 18 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 0 |
| c-bracket-mixed | 1.5 | 1 |

There are 46 material-profile rejections before full validation.
These and exact-state rejections are disjoint subsets of neutral rejections.
Counts do not measure saved time or establish final material improvement.


## Independent hole-reservation check and decision

Shapely 2.1.2 independently transforms every original filled
outer ring and checks 133,235 same-sheet pairs in 48 common-mode
layouts. All are disjoint and at least the requested kerf apart within the
unchanged 0.00000010 mm tolerance. Minimum slack is
9.99999247131e-07 mm. Hole interiors are not subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** 5 material pairs fail out of eight. m-mechanical-large-plates at 0.2 mm: +5.169797%; m-mechanical-large-plates at 1.5 mm: +6.158488%; m-mechanical-panel-hardware at 0.2 mm: +6.407212%; m-mechanical-panel-hardware at 1.5 mm: +5.654893%; c-bracket-mixed at 0.2 mm: +1.823168%
The candidate accepts 13/147 exchanges, including 11/108 paired and 1/18 mixed-item exchanges. Follow-up gap filling runs 13 times and moves 16 parts. Of 49 neutral rejections, 3 are caught by exact internal-state equality and 46 by the material profile before full validation. Counts do not establish time saving or improved final quality. No unchanged-build quality rerun, integration or relaxed limit
follows. H2/H5 remain open at 60%.


## Read-only inspection of parts setting the used height

The six previously validated neutral panel pairs preserve the physical poses of both inserts defining the height of the sheet receiving the largest offcut credit. Five pairs change other poses. This explains their unchanged material, but does not identify every new pilot failure. The next diagnostic should connect actual attempted exchange members to the parts defining charged height, including whether the current ordering reaches those parts. Qualify any resulting selector change with authored cases and retain all budgets and full acceptance checks. No new selector or quality gain is established.

[Saved-layout inspection](h5-material-profile-pilot-20261018/neutral-frontier-review/checks.json).

Mapping the pinned importer indices back to original part IDs also shows that none of the 16 attempts in those two earlier diagnostics selects an insert. The insert pair is present later in the choices. This coverage predates the new profile branch and is not attributed to its pilot. [Retained choice audit](h5-material-profile-pilot-20261018/neutral-frontier-review/choices.json).
