# Exact-state early-rejection pilot — 2026-10-18

**72/72 outcomes validate.**
This four-job pilot does not complete H5. Every original limit and the
complete 13-job requirement remain.

[Committed plan](h5-exact-reject-pilot-20261018/plan.json),
[all results](h5-exact-reject-pilot-20261018/results.json),
[archive verification](h5-exact-reject-pilot-20261018/verification.json),
[pair counters](h5-exact-reject-pilot-20261018/pair-counters.json).

## Method

The candidate adds an early rejection only for exact internal-state
duplicates of the validated incumbent. Shared original item/container
identity, transform bits, reflection and multiplicity are required.
All changed states and accepted exchanges retain the full independent
geometry/material checks. No limits, samples, ranking or repair budgets
change. The [preparation](h5-exact-reject-preparation-20261018.md) retains
117 passing optimized tests: all 113 prior tests plus four new tests.
The original expected failure, source and executable remain. Strict
lint/build, public interface checks and exact deterministic replays pass.

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
| m-mechanical-large-plates | 0.2 | +5.480992% | +5.349182% | -0.124961% | 12.814397% | 3 / 13 | 3 / 13 | NO |
| m-mechanical-large-plates | 1.5 | +5.213291% | +5.485080% | +0.258322% | 13.870797% | 2 / 29 | 1 / 19 | NO |
| m-mechanical-panel-hardware | 0.2 | +6.472156% | +6.767422% | +0.277318% | 5.144762% | 0 / 25 | 0 / 13 | NO |
| m-mechanical-panel-hardware | 1.5 | +5.144849% | +5.195747% | +0.048408% | 6.058131% | 0 / 24 | 0 / 9 | NO |
| m-box-mini | 0.2 | +0.000000% | +0.000000% | +0.000000% | 2.551020% | 0 / 0 | 0 / 0 | yes |
| m-box-mini | 1.5 | +0.000000% | +0.000000% | +0.000000% | 7.270408% | 0 / 0 | 0 / 0 | yes |
| c-bracket-mixed | 0.2 | +1.002742% | +1.027791% | +0.024800% | 22.455733% | 4 / 25 | 3 / 24 | NO |
| c-bracket-mixed | 1.5 | -0.190988% | +1.177346% | +1.370953% | 21.715715% | 4 / 9 | 4 / 9 | NO |

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
| c-bracket-mixed | 0.2 | 4 | 4 |
| c-bracket-mixed | 1.5 | 4 | 1 |

The step runs 13 times and moves 12 parts in total.
These operation counts do not by themselves establish final material improvement.

## Rejected unchanged-inventory swaps

| Job | Kerf mm | Rejections without material reduction |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 8 |
| m-mechanical-large-plates | 1.5 | 4 |
| m-mechanical-panel-hardware | 0.2 | 13 |
| m-mechanical-panel-hardware | 1.5 | 9 |
| m-box-mini | 0.2 | 0 |
| m-box-mini | 1.5 | 0 |
| c-bracket-mixed | 0.2 | 6 |
| c-bracket-mixed | 1.5 | 1 |

The early exact-state and original neutral guards reject 41 unchanged-inventory proposals without material reduction.
These counts do not identify other rejection stages or prove a global packing bound.

## Mixed-original-item exchanges

| Job | Kerf mm | Mixed accepted / attempted |
| --- | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 1 / 1 |
| m-mechanical-large-plates | 1.5 | 0 / 3 |
| m-mechanical-panel-hardware | 0.2 | 0 / 0 |
| m-mechanical-panel-hardware | 1.5 | 0 / 0 |
| m-box-mini | 0.2 | 0 / 0 |
| m-box-mini | 1.5 | 0 / 0 |
| c-bracket-mixed | 0.2 | 1 / 1 |
| c-bracket-mixed | 1.5 | 0 / 0 |

There are 2 accepted mixed-item exchanges in 5 attempts.
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


## Independent hole-reservation check and decision

Shapely 2.1.2 independently transforms every original filled
outer ring and checks all 133,535 same-sheet pairs in 48
common-mode layouts. All pairs are disjoint and at least the requested kerf
apart within the unchanged 0.00000010 mm audit
tolerance. Minimum slack is 9.99999247131e-07 mm.
Hole interiors are not subtracted.

**Reject this candidate for integration; do not open the full 13-job gate for it.** 6 material pairs fail out of eight.
m-mechanical-large-plates at 0.2 mm: +5.349182%; m-mechanical-large-plates at 1.5 mm: +5.485080%; m-mechanical-panel-hardware at 0.2 mm: +6.767422%; m-mechanical-panel-hardware at 1.5 mm: +5.195747%; c-bracket-mixed at 0.2 mm: +1.027791%; c-bracket-mixed at 1.5 mm: +1.177346%
There are 13/125 accepted/attempted exchanges, including 11/87
two-part exchanges. The post-exchange gap-fill step runs 13 times and moves 12 parts. The early exact-state and original neutral guards reject 41 same-inventory proposals without material improvement; mixed pairs account for 2/5 accepted/attempted exchanges. The neutral total includes 3 exact-state rejections before repeated validation. These counts alone do not establish final quality. Counters do not establish the remaining repair stage,
causality or impossibility. No unchanged-build quality rerun, integration or
relaxed limit follows. H2/H5 remain open at 60%.


## Read-only follow-up on neutral material

The preceding six panel neutral pairs all keep every sheet's highest
original cutting coordinate unchanged, including five pairs that change
two to four public poses. A separate reader reconstructs all twelve charged
material values exactly from their saved original vertices, public transforms
and the validator's grid, using the existing rectangular stock in millimetres.
No new search or changed validation is involved. This specific calculation is
not a general estimator for outlined stock, other units or arbitrary input.

If the pilot still fails, the next useful hypothesis is an early rejection
based on proven unchanged charged material, not a broader pose tolerance.
Derive a profile from the original geometry using exactly the validator's
transform/grid rules and require unchanged sheet-to-stock assignments. Equal
per-sheet highest coordinates then feed the same existing offcut calculation.
First prove this independently on saved layouts and authored cases involving
grid boundaries, rotations/reflections, units, margins, outlines and defects.
In particular, a same-inventory exchange that genuinely reduces material must
remain eligible. Any preliminary check may reject a proven non-improvement;
it must never approve an exchange. Every acceptance still requires the
unchanged full geometry and strict material guards. No such branch has been
implemented, and this read-only review proves no quality gain or time saving.

If the current pilot passes all pairs, retain its qualified candidate for
the original full 13-job gate before considering another algorithm change.

[Saved-height review](h5-exact-reject-pilot-20261018/neutral-height-review/checks.json).
