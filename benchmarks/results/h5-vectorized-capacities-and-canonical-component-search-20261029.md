# H5 vectorized capacities and canonical component search — 2026-10-29

Generic preparation now regenerates all **39 exact component-count certificates**
and the same **132 remaining distributions** in **2.006985 seconds**. This makes
the constraints usable inside the unchanged placement budget. Two distinct,
independently audited models each received one bounded call and returned
`UNKNOWN` without a placement. Both calls are closed.

H5 remains open. No continuous site choice, overall allocation or source part
was removed by these calls. The 29 site choices, 440 allocation candidates,
valid short11 and valid64 remain. No full66 source or native check ran, and
milestone completion remains **60%**.

## Generic preparation and independent equivalence

The builder regenerates contained source rectangles and all family support
components from their original geometric inputs. It enumerates 643 exact
subset-area inequalities, then screens all 214,200 mixed-subset axis halfspaces
with vectorized floating estimates. Estimates only select potential violations;
they never authorize an exclusion. Seven candidate halfspaces are recomputed
with exact rationals, yielding the same six halfspace certificates alongside
the same 33 subset-area certificates. No discovered list of cuts is an input.

The [equivalence audit](h5-vectorized-capacities-and-canonical-component-search-20261029/vectorized-equivalence-audit.json) confirms
byte-identical source inner rectangles, identical component geometry and source
attribution, every exact certificate identical to its
[previously independently verified witness](h5-joint-component-count-capacities-20261029.md),
and the same progression from 329 to 139 to 132 distributions. It verifies all
6,940 mode attributions and 4,549 unique family/geometry/region attributions;
all mode aliases agree on component membership. The audit took 1.812409 s.
This demonstrates equivalence for these inputs, not universal accuracy of
floating screening or a repeated performance benchmark.

## Source positions constrained by component counts

The first model retains all 13 moving original parts, 80 legal per-copy source
mode choices, 7,403 unary regions and 30,208 integer source-hull planes. Positions
remain variable on the previously audited local 0.1 mm grid. Twenty outward
source-piece rectangles stay rigidly attached to their owners; all 183 pairs
belonging to different owners retain the 0.3 mm clearance construction.

New selectors represent 29 allowed empty-cog-site pairs and 132 certified count
distributions. Exactly one pair and one distribution are selected. Under the
selected pair, 122 component count equalities count the chosen original unary
regions and match the selected distribution. All source-mode aliases and every
eligible region are checked before membership is counted. The model has
8,497 variables and 43,817 constraints; its exhaustive independent audit passes.
See [count-model audit](h5-vectorized-capacities-and-canonical-component-search-20261029/count-model-audit.json).

The second model assigns interchangeable copies to components first, then orders
them lexicographically by X and Y inside each component. It removes the earlier
11 unconditional X-order constraints and adds 377 conditional owner-component
equalities and 1,176 within-component ordering constraints. All 132 distributions
and all source positions remain available up to relabelling identical copies.
The independent reader checks identical same-family domains, modes and unary
geometry, complete different-owner separation coverage, every canonical identity
assignment and the integer scale used for lexicographic order. This model has
8,497 variables and 45,359 constraints. See
[canonical model audit](h5-vectorized-capacities-and-canonical-component-search-20261029/canonical-model-audit.json).

## Closed calls and complete budget accounting

Both calls used four workers, seed zero, no objective or hints and the recorded
parameters. Construction charges include the valid short-sheet shared time of
22.247810100321658 s and every required source/geometry stage. The new measured
generic preparation replaces the slower diagnostic construction; its source
and certificate equivalence is independently checked. Earlier solver runtimes
are not reused as construction, and neither earlier call was resumed.

| Model | Charged preparation | Allocated solve | Returned solve | Algorithm total | Shared total | Result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Component counts | 36.253446 s | 19.004168 s | 19.219705 s | 56.230721 s | 56.292517 s | UNKNOWN |
| Canonical component order | 36.586539 s | 18.407734 s | 18.476369 s | 56.085155 s | 56.145837 s | UNKNOWN |

The internal solve-slice overruns are preserved: **0.2155372005654499 s** and
**0.06863490049727261 s** respectively. Both complete algorithm times are below
60 seconds and both shared times below 90 seconds. Neither call was restarted,
extended or reseeded. Both recorded zero assignments, incumbents, source-checker
calls and native calls.

The [first response audit](h5-vectorized-capacities-and-canonical-component-search-20261029/count-response-audit.json) verifies 92,981
branches and 22,162 conflicts; the
[canonical response audit](h5-vectorized-capacities-and-canonical-component-search-20261029/canonical-response-audit.json) verifies 80,460
branches and 19,006 conflicts. Both read the raw response, model, parameters,
logs, charges and process closure. Raw LP diagnostics are preserved, including
zero overflow counters; they are not treated as source-geometry validation.
`UNKNOWN` establishes neither feasibility nor infeasibility.

## Next work and publication state

The [next investigation](h5-vectorized-capacities-and-canonical-component-search-20261029/next-step.json) tests mandatory occupied material
inside bounded axis strips, using exact source-rectangle breakpoints and unary
hull projection intervals. Single-boundary halfspaces may miss such constraints.
Every proposed exclusion requires independent exact verification; unprocessed
choices must remain. No strip preparation or further search has been opened.
Full66 source success must precede native/material checks, production integration
and the complete H5 matrix.

The prior two checkpoints were normally fast-forwarded to main and the work
branch as bd68c967 after all six checks on 286223ae passed. The
[push receipt](h5-vectorized-capacities-and-canonical-component-search-20261029/prior-main-push-receipt.json) is preserved. At this
checkpoint's snapshot, five jobs on bd68c967 passed and Windows remained running.
Another push requires all six checks and fresh remote-head/live-run verification.

Production source, all three READMEs, upstream Sparrow/Studio state and releases
are unchanged. H2 retains its original gate, with no reserved vectors evaluated.
Stable Latest is v0.1.0 and preview v0.2.0-alpha.1. These research results do not
qualify another release; H2/H5 remain open.

The [manifest](h5-vectorized-capacities-and-canonical-component-search-20261029/raw-manifest.json) preserves 4841 canonical files and
889 identical aliases in 59716342 bytes of multipart evidence, including
all original inputs, models, calls, exact readers and publication snapshots.
Separate archive verification checks every byte, binding and local report link.
