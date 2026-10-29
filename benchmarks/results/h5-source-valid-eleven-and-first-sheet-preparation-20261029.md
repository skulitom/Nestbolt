# Source-valid eleven-part short sheet and first-sheet preparation

2026-10-29. H5 development evidence for `m-mechanical-large-plates`.

The short sheet now contains **five original brackets, four original inserts and
two original cogs**, with independent checks of every contour, hole, placement,
pair and stock edge. Its matching first sheet must contain 18 frames, seven
brackets, 17 inserts and 13 cogs. That 55-part sheet is not constructed yet.
The complete 66-part source/native/material checks, production integration and
full H5 matrix remain. H2/H5 remain open; completion remains **60%**.

## Verified short-sheet result

- [Original source transforms](h5-source-valid-eleven-and-first-sheet-preparation-20261029/source-valid11.json).
- [Independent source replay](h5-source-valid-eleven-and-first-sheet-preparation-20261029/independent-source-audit.json) and
  [every source pair and stock check](h5-source-valid-eleven-and-first-sheet-preparation-20261029/source-valid11-checks.json).
- [Full response and timing audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/integer-response-audit.json).

The solver returned one assignment and one incumbent, which match exactly.
All 7,634 assignment variables and all 26,264 constraints replay correctly:
801 constraints are active and 25,463 guarded constraints are inactive.
The model is a satisfaction problem without an objective; `OPTIMAL` establishes
its feasibility, not a claim of optimal nesting quality. The response audit also
verifies 5,255 recursive input bindings.

An independent reader reconstructs all eleven transforms from the selected modes
and integer positions, then uses a separate affine transformation path on the
original rings. All **55 pairs, 44 stock edges, 21 holes and 2,718 hole vertices**
pass. The minimum pair gap is **0.227483219919 mm**, above the required
0.211708672510 mm. The minimum extra stock clearance is **0.026 mm**, above the
0.011444091797 mm guard. Part-in-hole remains disabled.

The call uses four workers and seed zero. It returns after **18.356101 seconds**,
with 80,234 branches and 8,176 conflicts. Preparation and readback bring the
algorithm time to **22.181037 seconds** and shared time to **22.247810 seconds**.
The charged preparation is 2.705251 seconds. There are no overruns and no retry.

## Geometry and complete orientation coupling

The [mode audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/all-mode-audit.json) checks all 13 family modes, 58
instance options, eleven distinct filled geometries and 232 original-source
stock-domain corners. All bracket quarter-turn/mirror combinations and insert
quarter-turns are retained. Equivalent insert outer geometries share geometry
templates while preserving their distinct original source transforms and holes.
Both cogs retain a declared seven-degree phase; other free cog angles are outside
this construction.

The [pair-region audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/pair-region-audit.json) covers all 55 original
pairs through 95 cached ordered geometry templates and 1,081 expanded geometry
cases. Constrained triangulation and exact-area convex merges produce 666 cached
regions. After rounding vertices to nine decimal places, **21,890 exact rational
support proofs** establish at least **0.225460638934 mm** of original-source
clearance throughout each convex region. Floating free-space construction and
conservative inflation restrict any negative conclusions.

The [integer geometry audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/integer-geometry-audit.json) proves that each
integer halfplane implies its already certified convex region. Positions use a
one-micrometre grid. Integer normal rounding is bounded over the full relative
position domain and tightened by that error plus 0.0000001 mm. Stock domains are
rounded inward. The [complete model audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/integer-model-audit.json)
checks 7,634 variables and 26,264 constraints, including every guarded plane,
mode-dependent stock domain, both-owner mode coupling and copy-order condition.
The model has no deactivation constants, continuous vertex weights or objective.

## Closed continuous predecessor

The earlier full-orientation convex-combination formulation is preserved with
its [model audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/continuous-model-audit.json) and
[response audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/continuous-response-audit.json). It has 33,208 variables,
8,260 rows and 107,950 nonzeros, including 7,612 binary selectors. It retains all
58 source-mode options and has no deactivation constants or tiny coefficients.

Its only call stops at the time limit after 214 nodes, with no assignment or
source-checker call. The allocated solve slice was 54.849117 seconds; the solver
returned after 55.151844 seconds. The **0.302728-second solve-slice overrun is
retained**, although the preparation-inclusive algorithm/shared totals of
57.309598/57.362527 seconds remain inside the overall 60/90-second limits.
No infeasibility or allocation exclusion is claimed. The call is closed.

## Matching first-sheet preparation

The [next construction plan](h5-source-valid-eleven-and-first-sheet-preparation-20261029/next-step.json),
[identity inventory](h5-source-valid-eleven-and-first-sheet-preparation-20261029/first55-inventory.json),
[preparation counts](h5-source-valid-eleven-and-first-sheet-preparation-20261029/first55-preflight.json) and
[independent audit](h5-source-valid-eleven-and-first-sheet-preparation-20261029/first55-preflight-audit.json) preserve 18 frames and
eleven side inserts from the existing valid64 layout. Eleven identical insert
copies are explicitly relabelled to the identities required by the new split;
their source geometry and world transforms remain unchanged.

Those 29 fixed originals and the new short11 form a
[valid 40-part partial control](h5-source-valid-eleven-and-first-sheet-preparation-20261029/partial40-source-checks.json): 461
same-sheet pairs, 50 holes and 4,132 hole vertices pass. This control is incomplete
and does not replace the preserved valid64 result.

The remaining **26 originals comprise seven brackets, six inserts and 13 cogs**.
They have 93 source-mode options, 325 original pairs and 3,038 expanded geometry
cases using 95 ordered template types. Their first-sheet lower-left domains
begin 0.225 mm beyond the fixed originals' maximum Y. Every one of 372
mode-domain corner controls passes against all 29 fixed original contours.
All 66 identities are a verified disjoint fixed29/moving26/short11 partition.

Next, regenerate the pair regions for this taller strip and audit their source
supports, integer rounding and full 26-mover model before opening a bounded call.
The integer-normal error envelope must cover the new 1,500 by 900 mm relative
domain. No first55 model or search has been opened. This fixes the existing frame
and side-insert arrangement and cog phase, so a negative result would not prove
global infeasibility.

## Preservation and publication

The prior valid64 file retains SHA-256
`bab709f97ac044ede2bcf8c40d75ba14162607c3c17c05bcacc1b4fa1614e9ee`.
No allocation is excluded; the authoritative frontier remains 440 candidates.
There are no native validator calls or production edits in this checkpoint.

[Publication review](h5-source-valid-eleven-and-first-sheet-preparation-20261029/publication-review.json) confirms unchanged production,
READMEs, upstream heads and releases. Stable remains v0.1.0 and preview remains
v0.2.0-alpha.1. All six checks on source/main `407f91ed` pass in
[run 40814954855](https://github.com/skulitom/Nestbolt/actions/runs/40814954855).
H2 retains its original gate and all 22 reserved vectors remain unopened.
No new release qualifies.

The archive contains **4561 canonical members**, **910 verified identical
aliases** and **35820973 ZIP bytes**, including all raw calls, failures, timings,
source placements, certificates, models, readers, recursive input bindings and
the prior normal-push receipt. The archive verifier checks ZIP integrity, every
member and alias hash, every bound input, JSON parsing and every local report link.
