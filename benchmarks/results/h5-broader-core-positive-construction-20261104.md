# Broader fixed-core positive construction — 2026-11-04

Releasing both edge brackets and both adjoining inserts produces a new
sixteen-mover construction whose sole call closes **grid-INFEASIBLE**.
It returns no placement, with zero time overruns. The complete algorithm/shared
totals are **32.216088 / 32.294957 s**. This does not prove continuous source
infeasibility. H2/H5 remain open at **60% completed milestone weight**.

## Joint capacities and a preserved failed control

The existing exact bracket-only capacities have two largest-capacity choices:
empty sites [5,11,13] and [5,11,14]. Both have capacity twelve for the required
eight brackets. The new [joint area/count audit](h5-broader-core-positive-construction-20261104/joint-capacity-audit.json)
checks all **four group areas**, **283 anchor-box assignments**, and every
bounded count distribution for **eight brackets and eight inserts**.
Neither choice is excluded.

The combined reachable areas are **533,849.577777 mm²** and
**540,300.758900 mm²**. A frozen largest-area rule, with lexicographic tie break,
selects [5,11,14]. These are necessary upper bounds on available space, not
attainable packing areas or positive witnesses.

Both choices include an isolated necessary insert pocket. A direct attempt
places original insert6 vertically above the right-side insert stack at
(1383.47,1989.01) mm. [Independent original-source readback](h5-broader-core-positive-construction-20261104/failed-insert-audit.json)
confirms that the 42-part control **fails**: insert6 overlaps cog4 by
**3.404385377309365 mm²**. All 861 pairs, 168 stock edges, 42 cutouts and 3,936
hole vertices were checked. The failed control, coordinates and original result
are preserved. Its fixed30 is not used; all sixteen originals remain movable.

## Fresh positive geometry and model

[The positive-region audit](h5-broader-core-positive-construction-20261104/region-audit.json) verifies **5,249
source-covering fixed obstacles**, all **12 legal original modes**, and
**214,933,987 integer arrangement cells** over the full physical stock.
Independent count events reproduce every forbidden overlap cell. The complete
free-cell cover has **925 positive boxes**: 251 bracket and 674 insert regions.
The fixed29 and twelve selected reference cogs pass a fresh 41-part original
source readback; the complete66 identity partition remains intact.

[Every model field passes independent verification](h5-broader-core-positive-construction-20261104/model-audit.json):
**7,672 variables and 15,870 constraints**, with 96 legal mode selectors,
7,400 positive-region selectors, 640 rigid coordinate links, and 16 rectangle
groups covering all 268 different-owner component pairs. All eight brackets
and eight inserts are free; there is no inherited five/one assignment, fixed
failed insert, old placement or hint.

[The complete charge ledger](h5-broader-core-positive-construction-20261104/preparation-charges.json) totals
**26.152827 s**. It includes the original source/cog/short-sheet geometry,
2.778012 s necessary inner bodies, 2.211135 s necessary full-stock cover,
14.375178 s complete 455-choice component capacities used to select candidates,
0.466033 s fresh joint capacities, the 0.302666 s failed direct control,
3.659609 s positive regions and 1.098525 s complete model build.
The internal build time is preserved but replaced by complete process time.

[Independent response readback](h5-broader-core-positive-construction-20261104/response-audit.json) verifies the
sole call: **29.059216 s allocated**, **5.260162 s returned**, **59,063 branches**
and **3,721 conflicts**. Search begins at 1.74 solver seconds. All 60/90-second
limits pass with zero overruns. There are no incumbents, assignments, full66
source checks or native calls. This call remains closed and cannot be repeated,
reseeded or extended.

## Remaining work and publication

The fixed rectangular covers are a sufficient safety approximation; their
grid-INFEASIBLE result does not exclude original polygon placements.
[The next method](h5-broader-core-positive-construction-20261104/next-step.json) replaces the band rectangles by
original convex-source Minkowski obstacles for this fixed29 and cog selection.
It must include every fixed original, full-stock bounds and all source-mode
aliases. New convex positive regions need exact rational separation
certificates and safe integer halfplanes before a distinct model. The old
top-strip geometry and model cannot be reused as full-stock evidence. No such
polygon construction has been prepared or run yet.

The broader 259-choice necessary frontier, fixed33's single continuous choice,
and all 440 whole-job allocations remain unchanged. Full66 source/native/material
validation, production integration and the H5 matrix remain required. H2's
original gate and unopened reserved vectors remain preserved. Production,
README and releases are unchanged.

The two preceding checkpoints were [pushed normally](h5-broader-core-positive-construction-20261104/main-sync-receipt.json)
to main at f8ba0d95 after every job and the aggregate
[prior CI](https://github.com/skulitom/Nestbolt/actions/runs/41922730064) passed.
[New main CI](https://github.com/skulitom/Nestbolt/actions/runs/41928746100) is
running at this checkpoint; no live run was cancelled.

[The manifest](h5-broader-core-positive-construction-20261104/raw-manifest.json) contains 138 new canonical
members and 2,477,541 compressed bytes.
[External references](h5-broader-core-positive-construction-20261104/external-evidence.json) and
[source bindings](h5-broader-core-positive-construction-20261104/source-bindings.json) retain exact historical inputs.
The independent archive reader verifies all new/reused members and report links.
