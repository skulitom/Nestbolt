# Full mixed-part outer-cover model — 2026-10-28

The new model keeps **all 25 remaining parts mandatory** around the verified
41 fixed originals. Its sole bounded call returns **UNKNOWN with no layout**.
This is not an infeasibility result. The call is closed, and H2/H5 remain open
at **60% completed milestone weight**.

This formulation replaces the earlier relative-cell model with conservative
outer rectangle covers and NoOverlap2D. The complete filled outer polygon is
first expanded by a 112 µm square; only then is its union partitioned into
rectangles with disjoint interiors. Cog covers use 2 mm slabs and outward
rounding. These are **outer covers**, unlike the previously used source-contained
capacity rectangles. Holes remain reserved; the 56-part control's original holes
are checked separately in source readback. The finite mode set is one 7° cog orientation, eight bracket
quarter/mirror modes and four insert quarter turns; no free-angle claim follows.

Independent coverage checks reconstruct 118 triangle/square Minkowski hulls
across all 13 modes and verify 39,068 same-owner rectangle pairs. Each cog uses
280 rectangles, covering 51,420.521888 mm² versus 50,312.411340 mm² for the
expanded source: **1,108.110548 mm² of conservative excess**. Maximum difference
between legal original transforms and normalized source coordinates is
5.69e-14 mm, far below the retained source-clearance margin.

The initial aligned control at 264 mm pitch passes original-source geometry but
fails the cover model with **20 overlapping component pairs**. Its bytes, source
success and failed cover audit remain preserved. A separate deterministic
construction uses full cover width plus 1 µm horizontally, and the maximum
forbidden vertical interval endpoint plus 1 µm for all 18 adjacent-row offsets.
Its pitches are **280.177 mm × 269.022 mm**, with an 80 mm middle-row offset.
Neither the source modes nor cover resolution changed.

The corrected 56-original control passes **925 original pairs, 224 stock edges,
74 holes / 8,074 hole vertices**, and **8,940,106 integer cover-component pairs**.
The ten absent parts are omitted only from this control. The actual search
requires all 25 movers, accounting for every one of the 66 originals exactly once.

The serialized model audit checks **142 variables, 8,819 constraints, 50
independent anchor coordinates, 67 mode choices, 4,305 component options and
70 partial hint values**. Every source bound, placement link, mandatory-part
constraint, NoOverlap2D entry, capacity and ordering constraint is inspected.
For the partial-control test, exactly ten mandatory-presence domains change
from one to zero in a separate model copy; restoring them recreates the actual
model bytes. That partial assignment fails all ten missing-part constraints
in the actual 66-original target. It is never presented as a complete solution.

The sole 60-second, four-worker call starts search after the logged **25.42 s**
presolve transition and returns UNKNOWN. Solver time is **60.511707 s**,
returned time **60.517049 s** and shared time **61.248900 s**, within the hard
90-second shared limit. The returned **0.517049 s soft overrun** is retained.
The response reports 172 branches and zero conflicts for its returned worker;
these are not aggregate claims about the whole portfolio. There are no
incumbents, source candidates, native calls or H5 completion credit.

The next experiment will test a smaller initial full25 relaxation and add
source collision constraints only for pairs exposed by complete candidates.
It must use the fresh mixed26 fixed-owner regions, verify all reusable intrinsic
pair geometry and retain all 66 required originals. A candidate remains rejected
until every source pair, stock edge and hole passes. Any new sequence will have
one total 60-second algorithm budget, a 90-second shared limit and at most eight
distinct solves; the time budget will not reset for each model. No closed call
is restarted, and UNKNOWN will not trigger a repeat of an identical model.

The previous three checkpoints were pushed normally and atomically to main
**b699d1c1** after all six jobs on 8713c6e1 passed. New
[CI 40748909850](https://github.com/skulitom/Nestbolt/actions/runs/40748909850)
has three passing jobs at this review; web, Linux and Windows checks remain live.
This checkpoint waits for all six jobs and fresh remote guards before pushing.
Production, READMEs and upstream heads/releases are unchanged. The previous
valid64, 444 necessary allocations, original H2 gate and all 22 unopened reserved
vectors remain preserved. No new release qualifies.

Evidence: [source coverage](h5-mixed25-outer-covers-20261028/geometry-audit.json),
[mode coverage details](h5-mixed25-outer-covers-20261028/mode-coverage.json),
[preserved failed control](h5-mixed25-outer-covers-20261028/preserved-control-failure.json),
[complete model audit](h5-mixed25-outer-covers-20261028/model-audit.json),
[partial-control distinction](h5-mixed25-outer-covers-20261028/partial-control-check.json),
[response audit](h5-mixed25-outer-covers-20261028/response-audit.json),
[next step](h5-mixed25-outer-covers-20261028/next-step.json),
[raw manifest](h5-mixed25-outer-covers-20261028/raw-manifest.json).
The verified archive contains 73 canonical files and
50 identical-byte aliases in 592,492
compressed bytes, including all inputs, failed and corrected controls, models,
source readbacks, logs, response and publication receipt.
