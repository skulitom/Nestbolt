# Hard-cell continuous construction — 2026-11-07

The construction closes at its three-call limit with **30 failing source pairs**:
28 positive overlaps and two clearance-only failures. Total original overlap is
**18,638.988042 mm²**. All fixed-part clearances and stock checks pass. Reduced
objective is not a valid layout. H2/H5 remain open at **60% completed milestone
weight**; four fixed arrangements and 440 whole allocations remain unresolved.
No native validation or allocation exclusion follows.

## Source-certified domains

The new model frees eleven side-strip inserts, retaining 33 movers: six brackets,
twelve inserts and fifteen cogs with continuous angles. Eighteen three-column
frames and fifteen short-sheet originals stay fixed. There are 81 continuous
parameters and 528 moving pairs; the historical short allocation is six brackets,
nine inserts and no cogs.

[Independent source readback](h5-hard-cell-continuous-construction-20261107/source-audit.json) checks 13 base orientation
arrangements, 45 atomic cells, 17 compound orientation/cell options, 147 owner
bindings and 708 original-source corner controls. Exact whole-cell support
proofs protect fixed frames with a minimum certified axis gap of 0.230001 mm.
These conservative rectangular cells do not claim complete free-space coverage.
The 59-part source control remains valid, with 1,051 pair checks, 236 stock edges,
71 holes and 7,708 hole vertices. It does not provide a full66 placement.

The first source preparation fails because inward-rounded cells exclude seed
centers by a few nanometres. A versioned correction projects 26 source-derived
centers to their nearest legal cells, by at most **4.242641 nanometres**; all
partial source geometry is then rechecked. Both preparations remain charged.
[A separate unit-label correction](h5-hard-cell-continuous-construction-20261107/unit-label-correction.json) preserves
the producer's mistaken micrometre wording; geometry and numerical bytes are
unchanged. Complete consumed source preparation is **4.512212 s**.

## Compound modes and deterministic initialization

Physical equivalence requires the same exact nominal filled outline and the
same effective cell rectangle. Orientation aliases use the explicit intersection
of their nearly equal source bounds. Different corner, side and top cells remain
distinct. This conservatively yields 111 physical owner options from 147 source
bindings, with 78 distinct single-owner neighbors; it does not broaden domains.

One deterministic initializer retains source-derived cog positions and angles,
then places brackets and inserts using 9×9 cell grids and legal source seed
centers. All cogs and side inserts remain movable. [The model audit](h5-hard-cell-continuous-construction-20261107/model-audit.json)
replays **10,932 trials**, 147 full scores, 115 dynamic vectors, 56 scalar/batched
gradient controls, 162 central derivatives, three descent controls, 137 compound
equivalence controls and eleven corruptions. All pass. The initial candidate
has 14 failing source pairs and 39,222.720379 mm² overlap; it is not source-valid.
Complete preparation, including the failed source stage, is **9.121196 s**.

## Closed search and independent replay

The frozen pipeline permits three distinct compound vectors with optimizer
slices of 16, 12 and 12 seconds. Later calls choose the lowest-scoring unvisited
single-owner neighbor of the best retained candidate; proposals may initially
increase the objective. All calls stop on time without a numerical return.
The pipeline stops at its declared call limit and cannot be extended.

| Call | Failed source pairs | Original overlap (mm²) | Objective (mm²) |
|---|---:|---:|---:|
| 0 | 30 | 20,635.026684 | 42,089.950117 |
| 1 | 29 | 18,773.127855 | 38,316.302155 |
| 2 | 30 | 18,638.988042 | 38,064.063464 |

[Response replay](h5-hard-cell-continuous-construction-20261107/response-audit.json) verifies **155 mode trials, 256
retained points and 289 evaluation counters**. Each call reconstructs all 66
original parts and checks 1,380 same-sheet pairs, 264 stock edges, 90 holes and
10,026 hole vertices. [The pair-by-pair failures](h5-hard-cell-continuous-construction-20261107/source-failures.json)
are retained. Every fixed–fixed and fixed–moving check passes in all three calls.

Preparation-inclusive algorithm/shared totals are **52.616504/52.686635 s**.
Slice overruns of 0.005838, 0.140486 and 0.092327 s are recorded; the overall
60/90-second limits pass. Peak aggregate committed memory is 94,507,008 bytes,
and [all five search processes close](h5-hard-cell-continuous-construction-20261107/closed-search-process.json).
The separate complete response audit takes 39.551456 s. All prior calls remain
closed; neither local failure nor bounded search excludes an allocation.

## Next investigation and repository state

[The next investigation](h5-hard-cell-continuous-construction-20261107/next-step.json) measures vectorized exact
boundary integration and assesses joint bracket/insert compound-cell choices.
It requires independent numerical controls and a frozen new scope before any
new optimization. No successor model or optimizer call is prepared. Consumed
preparation must be charged; optimized candidates cannot restart their clocks.

[The previous two checkpoints reached main c3af6112](h5-hard-cell-continuous-construction-20261107/prior-main-push-receipt.json)
after all six prior CI jobs and the aggregate run passed, preserving 52 remote
files. [Fresh main CI is still running at review](h5-hard-cell-continuous-construction-20261107/main-ci-at-review.json).
Production, README, releases and H2 reserved vectors are unchanged. Full66
source/native/material checks, production parity and the unchanged full H5
matrix remain necessary; no release qualifies.

[Raw manifest](h5-hard-cell-continuous-construction-20261107/raw-manifest.json) and [source bindings](h5-hard-cell-continuous-construction-20261107/source-bindings.json)
preserve new bytes and exact references to the previously verified archive graph.
