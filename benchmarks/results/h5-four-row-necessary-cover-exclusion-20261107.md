# Four-row necessary-cover exclusion — 2026-11-07

The valid 48-part core cannot be completed to its intended 66-part layout.
A full-sheet necessary cover for every allowed bracket orientation permits
at most **four brackets**, while **six are required**. This excludes the exact
fixed core, including positions outside the earlier conservative construction.
It does not exclude moving the core or changing the sheet allocation. H2/H5
remain open at **60% completed milestone weight**.

[The source construction](h5-four-row-necessary-cover-exclusion-20261107/source-cover-plan.json) begins with original
filled outlines, matching the existing no-hole-rider source validator. Holes
remain unchanged. It places **468 rectangles strictly inside the 18 fixed frames
and 15 fixed cogs**. Each bracket mode has two contained component rectangles.
Pairs of contained rectangles define exact open forbidden center rectangles.
The stock domain covers the complete physical first sheet, rounded outward;
no earlier constructive strip or center-cell restriction is imported.

[Independent readback](h5-four-row-necessary-cover-exclusion-20261107/independent-audit.json) verifies all contained
rectangles with rational arithmetic, including **1e-6 mm inward padding**.
It checks the 21 convex cog pieces against the original outline by oriented
boundary cancellation, and verifies the exact two-rectangle bracket decomposition.
The arithmetic error bound is below **5.821e-11 mm**, smaller than the padding.
[Containment records](h5-four-row-necessary-cover-exclusion-20261107/source-containment.json) preserve every source owner.
Zero clearance enlarges the feasible space and is used only for this exclusion.

Every obstacle endpoint partitions each axis into individual boundary points
and intervening open intervals. The producer labels their Cartesian classes
by slice assignment; the independent audit instead uses four signed rectangle
corners and two cumulative sums. All **3,707,540 continuous classes** match.
These are exhaustive regions, not sampled placement points. Boundary, corner,
overlapping-obstacle and outside-source negative controls pass.
[All eight allowed modes](h5-four-row-necessary-cover-exclusion-20261107/mode-census.json) are included. Only two modes
retain space: **3,564 classes**, covered by **six closed rectangles**. Closing
the component boundaries only enlarges the cover.
[Class and cover checks](h5-four-row-necessary-cover-exclusion-20261107/class-cover-controls.json) verify every retained
class and preserve all isolated boundary classes.

[The rational occupied-envelope bound](h5-four-row-necessary-cover-exclusion-20261107/capacity.json) contains every
possible bracket in that necessary cover within
**[1107.421999, 2555.932999]
to [1493.501001, 2993.501001] mm**.
Its area is **168935.817519 mm²**. Each filled original bracket
occupies 40,000 mm²; **39,999 mm²** is a conservative lower bound after the
explicit transform and rounding allowance. Five brackets already exceed the
envelope, so at most four fit. Six are required before even considering the
twelve remaining inserts. The exact fixed48 core therefore cannot extend to
this full 66-part allocation. Four earlier arrangements and all 440 whole-job
allocation candidates remain unresolved.

[Preparation](h5-four-row-necessary-cover-exclusion-20261107/preparation-process.json) closes in **2.304900 s**,
for **45.356320 s** retained preparation
if this lineage is consumed. [Independent audit](h5-four-row-necessary-cover-exclusion-20261107/audit-process.json)
closes in **0.828098 s**. Both use CCD1, one numerical
thread and the verified 2 GiB Job Object controls; all child processes close.
No optimizer or solver runs and no closed mathematical key is reopened.

[Next](h5-four-row-necessary-cover-exclusion-20261107/next-step.json), change the fixed arrangement or investigate an
unresolved allocation before another placement selection. Keep the valid48
reference and failed full66 results. Product integration, full66 source/native
validation, surface parity and the original H5 matrix remain required.

Main remains bf239548 with **5 passed / 1 live jobs** in
[this snapshot](h5-four-row-necessary-cover-exclusion-20261107/main-ci-at-review.json). The previous phase checkpoint is
committed locally as b6d43a8e. Product code, README and releases are unchanged.

[Archive checks](h5-four-row-necessary-cover-exclusion-20261107/archive-checks.json), [raw manifest](h5-four-row-necessary-cover-exclusion-20261107/raw-manifest.json),
[source bindings](h5-four-row-necessary-cover-exclusion-20261107/source-bindings.json), [historical references](h5-four-row-necessary-cover-exclusion-20261107/external-evidence.json)
and [runtime pins](h5-four-row-necessary-cover-exclusion-20261107/runtime-bindings.json) retain the complete proof inputs.
