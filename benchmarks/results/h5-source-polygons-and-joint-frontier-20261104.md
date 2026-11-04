# Original-source polygons and the joint frontier — 2026-11-04

Two distinct original-source polygon constructions return **grid-INFEASIBLE**
without placements or time overruns. Exhaustive joint area/count bounds for
all **259** surviving fixed-core arrangements exclude **none**. These results
do not prove continuous infeasibility of either polygon construction or any
whole-job allocation. H2/H5 remain open at **60% completed milestone weight**.

## Source geometry and the first construction

The [earlier rectangular construction](h5-broader-core-positive-construction-20261104.md)
used conservative cog band covers. The new method constructs Minkowski
obstacles directly from the original convex pieces, including every fixed29
original and twelve selected cogs. It uses fresh full-stock anchor bounds,
all legal rotations and mirrors, and a 0.231 mm square clearance inflation.
Constrained triangles are merged into convex placement regions.

For empty sites **[5,11,14]**, [exact original-source readback](h5-source-polygons-and-joint-frontier-20261104/first-source-audit.json)
verifies **178** rounded regions and **18,136** rational support certificates
against all twelve source modes. Minimum certified Euclidean separation is
**0.230999999513 mm**. All 41 fixed originals pass their separate source check.
The complete 66-original identity partition is preserved.

[Integer-plane verification](h5-source-polygons-and-joint-frontier-20261104/first-integer-audit.json) checks all
**677** inward halfplanes over the full 1500 × 3000 mm absolute coordinate
envelope. Coefficient rounding retains at least 0.0000001 mm inward reserve.
This is a safety proof for retained regions, not a complete free-space proof.

[The model audit](h5-source-polygons-and-joint-frontier-20261104/first-model-audit.json) exhaustively verifies
**1,696 variables / 6,470 constraints**. Equivalent source modes share
region selectors, reducing the count to **1,424**, while all **96 original
mode selectors and their individual stock bounds** remain explicit.
Sharing is justified by separate source certification for every alias.
All sixteen originals remain movable; 640 rigid coordinate links and sixteen
rectangle groups preserve every one of the 268 moving-component interactions.
No old placement, response or hint is used.

## All 259 joint bounds and a distinct selected arrangement

[The complete joint audit](h5-source-polygons-and-joint-frontier-20261104/all-joint-audit.json) checks **690 exact
group areas**, **39,235 anchor-box assignments**, and every bounded count
distribution for eight brackets and eight inserts across all 259 previously
retained choices. All survive this necessary bound. The original 196
bracket-only exclusions remain; no extra exclusion is inferred.

Complete preparation takes **26.682578 s** and independent exact replay takes
**12.535205 s**. The original failed insert control remains preserved and is
not adopted as fixed geometry.

Ranking all 259 by total exact joint reachable area, with lexicographic
tie-breaking, selects **[0,4,14]**. Its bound is **564,121.597558 mm²**;
this is an upper bound, not a packing witness. Fresh source geometry for this
different selection passes [14,874 rational supports](h5-source-polygons-and-joint-frontier-20261104/ranked-source-audit.json)
over **147 regions**. Minimum certified separation is
**0.230999999520 mm**. Its [546 integer planes](h5-source-polygons-and-joint-frontier-20261104/ranked-integer-audit.json)
and [1,448-variable / 5,422-constraint model](h5-source-polygons-and-joint-frontier-20261104/ranked-model-audit.json)
pass independently. All sixteen movers, 96 original modes and full inventory
remain intact.

## Closed calls and full preparation charges

| Arrangement | Preparation | Allocated solve | Returned solve | Algorithm total | Shared total |
|---|---:|---:|---:|---:|---:|
| [5,11,14] | 23.713349 s | 31.540247 s | 1.976455 s | 26.449704 s | 26.514206 s |
| [0,4,14] | 49.475790 s | 5.867108 s | 2.005805 s | 52.151574 s | 52.211289 s |

The [first ledger](h5-source-polygons-and-joint-frontier-20261104/first-preparation-charges.json) includes all
consumed source, selection, failed-control, polygon, integer and complete model
processes. The [ranked ledger](h5-source-polygons-and-joint-frontier-20261104/ranked-preparation-charges.json)
charges the entire 259-choice preparation used for its selection. Independent
verification time is recorded separately. Internal build times are preserved
but replaced by complete process times in both budgets.

Independent [first response readback](h5-source-polygons-and-joint-frontier-20261104/first-response-audit.json)
verifies **14,524 branches / 1,196 conflicts**; the
[ranked response readback](h5-source-polygons-and-joint-frontier-20261104/ranked-response-audit.json) verifies
**20,878 / 4,888**. Both sole calls enter search, return INFEASIBLE, and have
zero solve-slice, algorithm or shared-time overruns. Neither has an incumbent,
assignment, full66 source readback or native call. Both calls are closed and
must not be repeated, reseeded or extended. Neither supplies an independently
verified continuous unsatisfiability certificate.

## Remaining work

[The next proof hypothesis](h5-source-polygons-and-joint-frontier-20261104/next-step.json) examines local conflicts
between the existing continuous necessary anchor boxes. Exact inner-source
rectangles can certify that every pair of placements in two boxes collides.
Any clique capacity or finite graph bound must cover every continuous legal
anchor and carry an independently checked certificate before it excludes a
construction. This may detect local packing limits missed by total area.
No such bound is claimed or prepared in this checkpoint.

All **259** broader fixed-core choices, the earlier fixed33 choice and **440**
whole-job allocations remain open. Full66 source/native/material validation,
production integration and the H5 matrix are still required. H2 retains its
original gate and unopened reserved vectors. Product source, README and
release assets are unchanged.

Main remains f8ba0d95 at this review, with four successful jobs and two live
checks in [CI 41928746100](https://github.com/skulitom/Nestbolt/actions/runs/41928746100).
The previous broader-core checkpoint and this evidence await all six jobs and
the aggregate result before a normal push. No run was cancelled.

[The manifest](h5-source-polygons-and-joint-frontier-20261104/raw-manifest.json) preserves 432 new canonical
members in 2,247,139 compressed bytes. [External evidence](h5-source-polygons-and-joint-frontier-20261104/external-evidence.json)
and [input bindings](h5-source-polygons-and-joint-frontier-20261104/source-bindings.json) retain exact historical
dependencies. An independent archive reader verifies every new/reused member
and local report link before commit.
