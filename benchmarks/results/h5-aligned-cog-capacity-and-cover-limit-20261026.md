# H5: aligned cog capacity and rectangle-cover limit — 2026-10-26

**A different allowed cog angle changes the nine-part necessary capacity test
from negative to positive. Its selected orientation pattern still fails the
full coordinate model. A conservative rectangle-cover model stalls and is
terminated by its watchdog. No full target layout is claimed; H2/H5 remain
open at 60% completed milestone weight.**

## Rotation and necessary capacity

Screen the original 80-vertex cog over the full rotation range using hull
support switches, width/height stationary points, crossings and area extrema.
This produces 105 support intervals and 251 candidate angles. Independent
original-polygon rotation recomputes every candidate and checks 315 interval
samples. The screen selects an angle near 56.25 degrees; the new profile uses
exactly 5π/16 radians. This is numeric angle selection, not a packing theorem.

The cog's width and height fall from approximately **279.949211 mm to
278.541800 mm**, a **1.407411 mm** reduction. Vertical travel inside the usable
short sheet increases from 32.977692 to 34.385103 mm before extra stock guards.
All 80 outer vertices and the original 200-vertex cutout remain required.
Ten other profiles remain unchanged; all 11 original-profile reconstructions
pass with maximum error 8.04×10⁻¹⁴ mm.

Recompute **42,525 exact band-area lower bounds** over **675** vertical cells
and **63** stock bands. A separate rational edge-integral audit verifies every
coefficient and all integer anchor coverage. The new model requires four
brackets, one insert and four cogs at the aligned angle. Its sole bounded call
returns **OPTIMAL in 0.123573 solver / 0.784745 shared seconds**. Independent
readback checks all 675 values, 66 constraints, family counts and band loads.
The result is a necessary allocation, not a coordinate witness.

All identities remain explicit: 55 checked first-sheet originals, second-sheet
originals **21/22/25/26/37/53/63/64/65**, and pending first-sheet brackets
**28/29**. The earlier current-angle negatives are not transferred.

## Full coordinate model for the selected pattern

The allocation selects profiles **4/5/5/6/10/9/9/9/9**. All 18 coordinates are
free throughout the guarded short stock, with no band-cell locks or hints.
Four unchanged bracket collision cases are reused; eight cases are rebuilt.
Independent original geometry checks reconstruct all 12 cases from 7,264
triangle-pair hulls, 191 guarded faces and 7,917 outside planes. The minimum
source guard is 0.2126 mm, above the required native 0.211709 mm.

The complete **8,561-variable / 8,738-constraint** model and actual import pass
independent reconstruction, retaining all 36 physical pairs. Its sole call
returns **INFEASIBLE in 1.767172 solver / 2.465369 shared seconds**. This excludes
only the specified profiles, guarded source and coordinate grid.

## Conservative rectangle covers and timeout

To test a different representation, dilate each original profile by a square
with half-side 0.1063 mm, then cover the guarded shape with disjoint rectangles.
Whole-row covers add 5,645.918 mm² beyond a guarded cog. Keeping disconnected
tooth-tip components separate reduces that excess to **1,467.443 mm²**.
Neither shape is substituted for the original at final acceptance.

Independent triangle-plus-square construction verifies all guarded polygons,
complete cover containment, original stock bounds and all 49,463 internal
rectangle pairs for the component covers. Twice the minimum cover-boundary
gap is **0.213651 mm**, above the native pair requirement. A non-overlapping
cover placement would therefore be sufficient, pending original verification;
a cover-model negative would not exclude original placements.

The model permits all eight bracket orientations and both insert orientations,
with shared original anchors. All **52 variables / 2,732 constraints**, including
2,652 optional intervals and one complete **1,326-rectangle NoOverlap2D**, pass
independent reconstruction and real solver import. Every original is mandatory.

The single call starts search but returns no solver response by its 45-second
soft limit. The **60-second outer watchdog terminates it**. Controller elapsed
time is **60.016700 seconds**, including **0.016700 seconds** of shutdown overhead.
The exact model, parameters, partial log and missing-result state are preserved;
a process check confirms no runner remains. This is a watchdog failure, **not
UNKNOWN or INFEASIBLE, and not a budget pass**. No retry is opened.

## Production review and next action

A read-only production review confirms that ordinary optimization enables
hole riders while common-line optimization disables them. The translation
bonus bounds material against its own starting layout; the external H5
ordinary comparison remains a separate requirement. Reusing an ordinary
hole-rider layout or changing that comparison would not close the current gate.
No production change or quality benchmark follows this review.

Next audit a conditional profile-count exclusion for the failed source pattern
in the aligned-angle band master. It must exclude exactly bracket counts
p4=1, p5=2, p6=1 with insert p10=1, using the identical-original-copy permutation
argument and full coordinate-model scope. Other patterns remain available.
Complete 66-original/native/material checks, production integration and the
full H5 matrix remain required; allocations alone earn no gate credit.

At 2026-10-26T06:03:14.749836+00:00, all six checks for main **81cc4186** pass in
[CI40273506020](https://github.com/skulitom/Nestbolt/actions/runs/40273506020).
Checkpoint 68f82c02 and this evidence can be pushed normally after verification.
Production, accurate READMEs, upstream heads/releases and all 22 reserved H2
vectors remain unchanged. No new release is qualified.

[Checks](h5-aligned-cog-capacity-and-cover-limit-20261026/checks.json), [closed calls](h5-aligned-cog-capacity-and-cover-limit-20261026/closed-calls.json),
[watchdog audit](h5-aligned-cog-capacity-and-cover-limit-20261026/cover_probe-timeout-audit-checks.json),
[next step](h5-aligned-cog-capacity-and-cover-limit-20261026/next-step.json), [raw manifest](h5-aligned-cog-capacity-and-cover-limit-20261026/raw-manifest.json).
All 250 canonical files and 203
aliases are byte/SHA-256/CRC verified in 1 archive parts.
