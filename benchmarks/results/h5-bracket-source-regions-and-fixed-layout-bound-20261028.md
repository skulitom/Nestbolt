# H5: source bracket regions and a fixed-layout exclusion

The 61-part control cannot be completed on its current two target sheets
without moving existing parts. An independent necessary area bound proves
this for all eight bracket orientations and continuous positions, even
allowing the five missing brackets to be reassigned between the sheets.
This excludes one fixed layout, **not the original mechanical job**.

The study also confirms a separate modelling restriction: each legal bracket
orientation has a source-valid position rejected by the cog-row rectangle
covers. All eight resulting 62-part controls pass original geometry checks.
They do not improve the existing valid 64-part result. H5 remains open.

## Original-source regions and witnesses

For every bracket orientation, the study compares three placement regions
against the unchanged 49 first-sheet originals: original-source clearance
throughout; source cog clearance plus orthogonal-part covers; and all-part
covers. All use the same 13 µm stock-model guard. The middle comparison
isolates losses caused by row covers. Source obstacles use the original
filled outlines and a conservative clearance buffer; holes remain reserved.

The [independent region audit](h5-bracket-source-regions-and-fixed-layout-bound-20261028/source-region-audit.json) verifies all
392 bracket-to-world-source obstacles through 37,184 independent Minkowski
hulls and checks all 32 saved regions. Each of eight deterministic witnesses
comes from the largest region lost to row covers, rounded to the nearest
micrometre with at most nine predefined grid checks. No packing optimizer
or restart is involved. All eight source readbacks pass 1,291 original-pair
checks each; the 61 pre-existing poses remain identical. The only new cover
collisions involve cog rows 41 or 42.

| Quarter turns | Mirrored | Anchor-space area excluded by row covers, mm² |
|---:|:---:|---:|
| 0 | No | 11.160176 |
| 1 | No | 2.636521 |
| 2 | No | 307.470795 |
| 3 | No | 320.625441 |
| 0 | Yes | 32.973915 |
| 1 | Yes | 256.903675 |
| 2 | Yes | 128.542033 |
| 3 | Yes | 2.006324 |

These are areas in **translation space**, not material savings. Full values
and original-pose references are retained in the
[region summary](h5-bracket-source-regions-and-fixed-layout-bound-20261028/source-region-summary.json) and
[witness summary](h5-bracket-source-regions-and-fixed-layout-bound-20261028/source62-witness-summary.json).

## Complete five-bracket construction, closed

A new restricted model holds those 61 originals fixed and requires every
one of the five missing brackets. All eight legal quarter/mirror modes are
available. Their source placement regions become 58 convex cells and
174 conservatively rounded halfplanes. Exact rational error bounds are
checked before use. Between brackets, disjoint rectangle covers independently
contain at least half the required original clearance on each part.

The [model audit](h5-bracket-source-regions-and-fixed-layout-bound-20261028/model-audit.json) verifies all 345 variables and
1,085 constraints, 40 mode choices, 290 cell selectors and 73 soft hints.
The positive 62-part control fails exactly four mandatory requirements;
an audit copy changing only those requirements passes. The full 66-part
negative control places all five brackets at the same otherwise valid pose:
its ten original collisions produce twenty cover collisions and the model
rejects it. Source geometry, all 90 cutouts and 10,026 hole vertices are retained.

One frozen call used a 60-second algorithm limit inside a 90-second shared
limit, four workers, seed 0 and `fj` disabled. It closed **INFEASIBLE** after
0.185030 returned solve seconds, with 0.867560 algorithm seconds and
0.928757 shared seconds. No soft overrun, incumbent or complete candidate
occurred. The returned worker reports 2,864 branches and 158 conflicts; those
are not aggregate counters across workers. The
[response audit](h5-bracket-source-regions-and-fixed-layout-bound-20261028/response-audit.json) rechecks the full model,
parameters, hashes, log, response and timing. Unused time is not reused.

This solver result alone excludes only the conservative, discretized
construction with the 61 parts fixed. The following independent necessary
bound establishes a stronger, specifically bounded result.

## Necessary area bound with continuous positions

The bound uses rectangles **inside** the originals, rather than collision
covers outside them. It retains 1,323 contained rectangles from the 49 fixed
first-sheet parts and two contained rectangles for each legal bracket mode.
Cog rectangles come from the previously verified 5 mm source grid, translated
to the actual fixed poses and rounded further inward. No additional part
clearance is imposed. Stock anchor bounds expand outward by 2 µm from the
unguarded source bounds; anchors are continuous, with no grid restriction.

Exact rectangle no-fit boxes exclude only anchors that necessarily collide
with a fixed contained rectangle. Their complementary regions are represented
by 27 orthogonal slabs. Sweeping every moving contained rectangle over every
allowed slab and all eight modes yields 54 rectangles whose union contains
all possible occupied inner-bracket area. Strict source containment and the
original positive gap prevent omitted boundary-only feasible anchors.

The [independent necessary-bound audit](h5-bracket-source-regions-and-fixed-layout-bound-20261028/necessary-bound-audit.json)
checks 1,339 contained rectangles using 103,276 exact rational source-edge
tests. It verifies all 6,022 continuous X strips of the rectangle arrangements,
all sweep sums and the union area using integer interval arithmetic and
integer polygon shoelace areas.

| Quantity | Area, mm² |
|---|---:|
| First-sheet possible inner-bracket envelope | 144,813.690060 |
| Minimum contained area of one bracket, across all modes | 39,997.225036 |
| Minimum contained area of five brackets | 199,986.125180 |
| First-sheet deficit for five brackets | 55,172.435120 |

At most **three** additional brackets can occupy this first sheet while its
49 existing originals remain fixed. The
[saved envelope](h5-bracket-source-regions-and-fixed-layout-bound-20261028/first-sheet-envelope.json) is a union of possible
occupied areas, not a claim that any particular arrangement fills it.

The short sheet independently has at most **one** bracket's remaining
capacity. After expanding every stock edge by 2 µm and rounding its area up,
its area is at most 465,330 mm². Exact rational areas of the twelve existing
filled outlines, each rounded down, total at least 409,257 mm². Thus only
56,073 mm² can remain, less than the minimum contained area of two brackets.
The [short-sheet area record](h5-bracket-source-regions-and-fixed-layout-bound-20261028/short-sheet-area-checks.json) preserves
the exact fractions and downward rounding.

Both sheets therefore accommodate at most four of the five missing brackets.
The [proof and scope](h5-bracket-source-regions-and-fixed-layout-bound-20261028/necessary-bound-proof.json) cover the fixed
61 original poses on these two unchanged target stock bounds, including
redistribution of the missing brackets. Existing source acceptance rules
are unchanged; the relaxations apply only to this necessary proof.
No other source pose, allocation or global layout is excluded.

## Next work and publication

The next construction must permit existing parts to move. Before another
packing call, derive and audit complete original-source row-to-bracket
displacement domains for both cog-row sizes and all eight bracket modes.
The eight source-valid controls provide direct tests for that replacement.
Keep all 66 parts mandatory and both previous 43-block calls closed. The
444 necessary allocation survivors remain unchanged because the certificate
excludes only one layout. The best valid 64-part layout is preserved.

Remote main remains 608fecf1. Prior checkpoint 98a5651c and this checkpoint
wait for CI 40771628220: five jobs pass and Windows checks remain running at
this snapshot. No live run is cancelled. Production source, all three
READMEs, Sparrow/Studio heads and release state are unchanged. The original
H2 gate remains open under Artem's explicit decision; 22 reserved vectors
remain unopened. H2/H5 are open at **60% completed milestone weight**.
No new release or native-validation claim is made.

The [raw manifest](h5-bracket-source-regions-and-fixed-layout-bound-20261028/raw-manifest.json) binds 695 canonical files,
568 identical aliases and 2372670 compressed bytes, including all
source controls, full regions, exact arithmetic evidence, scripts and the
closed solver response. Recursive source hashes and local imports are
included. The archive verifier checks every byte, alias, binding, JSON
document and local report link.
