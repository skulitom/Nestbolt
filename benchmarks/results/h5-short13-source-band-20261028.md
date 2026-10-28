# Short-sheet source search and cog band-area bounds — 2026-10-28

The allocation of **seven brackets, five inserts and one cog** remains unresolved.
A new search with all 13 original shapes free fails the independent geometry
check. A separate, stronger necessary model accounts for the cog's original
filled area and returns **UNKNOWN**. Neither result is a feasible placement or
an impossibility proof. Both calls are closed.

## Original-source construction

All seven brackets, five inserts and the cog move; none of the previous nine
fixed neighbors stays fixed. The declared modes cover all eight bracket modes,
both insert outer classes and 36 cog phases. The geometry includes 415 source
pair obstacles: 379 exactly reused and 36 new bracket-pair obstacles. Preflight
checks verify 46 original modes, 3,735 original-shape pair samples, all 635 valid
12-part starting prefixes and 26 analytic-gradient components.

Both insert classes are evaluated on a 31 by 5 grid for every prefix: all
196,850 candidates are retained and independently replayed. The single selected
start uses prefix 258. One continuous position stage performs 123 objective
evaluations and 89 mode trials, with no accepted mode change or random restart.
It closes at a local minimum after 2.218165 search seconds and
5.856514 shared seconds. The final source readback checks all
13 originals, 78 pairs, 52 stock edges and 27 holes with 3,372 hole vertices.
**Fifteen pairs and two stock bounds fail.** The worst extra stock clearance is
−2.014812 mm. All raw failed placements, checks and logs are preserved.

## Exact area bounds for every cog angle

The original filled outer has area 50,062.718938 mm². Exact rational arithmetic
verifies all 80 source vertices lie within a 140.001 mm radius; allowing center
flooring gives a strict 140.003 mm bound. A 64-facet rational polygon encloses
that circle. It supplies upper bounds on area outside each horizontal band;
it is never substituted for the cog's filled collision geometry.

For each of 35 complete integer center-Y bins and 10 predeclared bands, subtract
outward-rounded lower and upper cap areas from inward-rounded original area.
Compare this with the minimum contribution of the old disjoint source strips,
and retain the larger valid lower bound. The full-stock band uses the full
source area directly. These are necessary bounds for every real rotation.

The independent audit recomputes 44,800 exact clipped-triangle caps and all
350 bounds. **275 bounds improve**, by up to 16,232.704661 mm². All 6,350
original-polygon band checks across the 635 valid prefixes agree. These samples
corroborate the exact proof; they do not establish angle completeness.

## Audited stronger model and closed result

All 12,197 prior variables and 15,458 constraints are preserved byte for byte.
The extension links the cog to exactly one complete Y bin and adds ten band
capacity constraints. Each sums the cog bound and the exact intersections of
selected source-contained noncog rectangles with that band. All 1,602 optional
intersection-height calculations and 178 whole-stock rectangle areas are
independently checked. Every original remains mandatory, all allowed modes
remain available, and there are no fixed poses, hints or objectives.

The complete model has **18,640 variables and 23,549 constraints**. Its sole
60-second call, with four workers and `fj` excluded, returns UNKNOWN after
67,352 branches and 40,926 conflicts. Solver wall time is 60.117023 seconds,
returned call time 60.120701 seconds, and shared time 61.081026 seconds. The
small soft overruns are retained. The independent response reader verifies
the model bytes, parameters, counters, status and absence of an assignment.

There is no short-sheet count exclusion, full valid 66-part layout, native
validation or H5 completion. The best current valid construction still has
64 originals with two brackets missing. Next investigate a stronger exact
structural projection or a different complete source construction; these
searches will not be repeated or extended.

## Publication

Main `390fb2d3` now passes all six jobs in
[CI 40676201231](https://github.com/skulitom/Nestbolt/actions/runs/40676201231).
The queued necessary-model checkpoint and this evidence can be pushed together
after a fresh remote and live-run check. Production, READMEs and Sparrow/Studio
heads and releases are unchanged. H2 and H5 remain open at **60% completed
milestone weight**; all 22 reserved H2 vectors remain unopened. No new release
qualifies.

[Source audit](h5-short13-source-band-20261028/source-result-checks.json),
[exact band audit](h5-short13-source-band-20261028/band-geometry-checks.json),
[necessity proof](h5-short13-source-band-20261028/band-area-proof.json),
[full model audit](h5-short13-source-band-20261028/band-model-checks.json),
[closed response](h5-short13-source-band-20261028/band-response-checks.json),
[publication review](h5-short13-source-band-20261028/publication-review.json),
[next step](h5-short13-source-band-20261028/next-step.json),
[byte-verified archive](h5-short13-source-band-20261028/raw-manifest.json).
The archive preserves 837 canonical files and
592 identical-byte aliases in 2,157,827
compressed bytes, including the original job, all reused obstacles, input
bindings, helper dependencies, exact proofs, model protobufs and raw failures.
