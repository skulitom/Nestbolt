# Joint-cell choices and vectorized gradients — 2026-11-07

The expanded search closes after three new physical configurations and **4,122
proposal scores**. Its best candidate, from call 0, still fails **30 source pairs**,
with **18,450.266096 mm²** original overlap. Both later candidates are worse.
All fixed-part clearances and stock checks pass. H2/H5 remain open at **60%
completed milestone weight**; no source-valid full66 layout, native call,
allocation exclusion or qualifying release follows.

## Measured numerical improvement

The new boundary integral retains every clipped line's parent edge, reduces
its endpoint parameters in arrays, and integrates the same translation and
rotation velocities. Nested collections and isolated points are handled
explicitly. Shared boundaries retain the existing half-weight convention;
this does not turn nonsmooth contacts into classical derivatives.

[Correctness controls](h5-joint-cell-vector-construction-20261107/vector-gradient-audit.json) cover fourteen
synthetic pairs, a nested collection with intermediate collinear vertices,
406 positive original/clearance boundary terms, four complete objectives and
81 central finite differences. Maximum gradient difference from the two scalar
references is **1.36425e-11**; maximum central-difference error is **6.67284e-7**.
All checks pass. [Ten alternating-order timings per fixed case](h5-joint-cell-vector-construction-20261107/vector-gradient-timings.json)
show **1.7243–2.0405×** median whole-objective speedups. These are research-kernel
measurements on four validation cases, not a production performance or packing
claim. Historical optimized points are used only for these controls.

## Expanded compound proposals

At a source-only initial point, the new selector enumerates 78 unique single-owner
changes and **1,296 bracket/insert two-owner changes**. Each changed center is
clamped to its target hard cell; all other positions remain fixed for scoring.
The full pair objective is evaluated by cached single-owner deltas plus the
exact correction for the pair changed twice. Scores are ranked after rounding
to 0.000001 mm², then by owner and mode; this is a declared tie rule.

[Independent preparation replay](h5-joint-cell-vector-construction-20261107/neighbor-audit.json) reconstructs the
original and clearance polygons and fully sums all 1,056 terms for every one
of **1,375 full scores**. It uses no delta correction. Maximum score difference
is **4.36558e-10 mm²**; all centers, expected vectors, keys and choices match.
The initial best single score is 78,177.927349 mm² and best joint score is
85,800.290452 mm², versus the 79,154.624600 mm² baseline. Joint proposals do not
provide an initial improvement. The complete new preparation process takes
0.411814 s, bringing consumed source-only preparation to **9.533010 s**.

## Frozen search and replay

The new pipeline selects the best unvisited proposal before every call and
retains the global best separately. It excludes all three physical vectors
from the closed predecessor and each newly called vector. It never consumes
an optimized ancestor point. There are at most three calls, each with a
14-second slice; all 33 centers and fifteen cog angles remain continuous.
Hard domains, source outlines, clearance, objective weights and full66 checks
are unchanged. Every call stops on time without a numerical return.

| Call | Selected move | Failed pairs | Original overlap (mm²) |
|---|---|---:|---:|
| 0 | bracket owner 4 → mode 3 | 30 | 18,450.266096 |
| 1 | bracket owner 2 → mode 9 | 30 | 19,402.083123 |
| 2 | insert owner 17 → mode 2 | 31 | 20,350.616355 |

All selected moves affect one owner. The 1,296 joint alternatives at each round
score worse than its selected single-owner change. Their evaluation is retained;
no actual joint move or packing gain is claimed from adding them.

[Independent response replay](h5-joint-cell-vector-construction-20261107/response-audit.json) reconstructs all
4,122 expected proposal vectors, full scores, clamps and selected models. It
verifies **539 retained points and 585 evaluation counters**, all three prior
closed-vector exclusions, complete original source transforms and every
response. Each response checks all 66 originals, 1,380 same-sheet pairs,
264 stock edges, 90 holes and 10,026 hole vertices. [All source failures](h5-joint-cell-vector-construction-20261107/source-failures.json)
and both worse candidates remain preserved.

Algorithm/shared totals including preparation are **53.378490/53.439519 s**,
within the unchanged 60/90-second limits. Slice overruns of 0.060660, 0.003205
and 0.053420 s remain recorded. Peak aggregate committed memory is 97,775,616
bytes; [all five search processes close](h5-joint-cell-vector-construction-20261107/closed-search-process.json).
These three calls and their predecessor remain closed despite unused time.

[A diagnostic of the retained candidate](h5-joint-cell-vector-construction-20261107/candidate-diagnostic.json)
attributes 14,107.916224 mm² to eight bracket/cog pairs, 4,011.017783 mm² to
twenty cog/cog pairs, and 331.332090 mm² to two cog/insert pairs. Twenty-five
coordinates lie on hard bounds. The projected gradient remains nonzero;
neither numerical stationarity nor geometric impossibility is claimed.

[The next investigation](h5-joint-cell-vector-construction-20261107/next-step.json) first reconciles historical
bracket/cog contact work, then assesses original-outline contact candidates
for simultaneous translations beyond nearest-bound clamping. No new contact
geometry, complete model or optimizer call is prepared. Consumed work remains
chargeable and optimized candidates cannot reset their clocks.

Four fixed arrangements and 440 whole allocations remain unresolved. Full66
source/native/material checks, production parity and the unchanged H5 matrix
are still required. [Main c3af6112 has five passed jobs and a running Windows
native job at review](h5-joint-cell-vector-construction-20261107/main-ci-at-review.json); checkpoint be75186f and
this checkpoint await the ordinary push gate. Production, README, releases
and reserved H2 vectors remain unchanged.

[Raw manifest](h5-joint-cell-vector-construction-20261107/raw-manifest.json) and [source bindings](h5-joint-cell-vector-construction-20261107/source-bindings.json)
preserve both new evidence and exact prior archive references.
