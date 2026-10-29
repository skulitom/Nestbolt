# H5: short11 source readback and a restricted translation contradiction

Date: 2026-10-29. Evidence and documentation only. H2/H5 remain open at
60% completed milestone weight. No new release qualifies.

The all-movable **5 brackets / 4 inserts / 2 cogs** necessary model finds a
satisfying assignment, but its original source contours fail **ten pair checks
and six stock checks**. A distinct fixed-orientation translation model also
fails. An independently verified exact cycle explains that failure: six frozen
pair-separation directions and two stock bounds imply `0 <= -33.42045275048 mm`.
At least one of those directions or an orientation must change.

This certificate applies only to the frozen translation system. **No allocation
is excluded**, and all 440 remaining candidates stay open. Neither a valid
short11 layout nor the complete 66-part layout is produced.

## The eleven-part necessary model

The [previous checkpoint](h5-short12-exclusion-and-seven-part-readback-20261029.md)
prepared short11=5 brackets/4 inserts/2 cogs and first55=18 frames/7 brackets/
17 inserts/13 cogs. Insert0 and insert2 move to the first sheet. Every original
identity remains accounted for exactly once.

The [model audit](h5-short11-source-readback-and-translation-cycle-20261029/short11-model-audit.json) verifies two changed presence
requirements and two hint values relative to the original thirteen-owner model.
All 1,876 variables and the other 1,911 constraints remain unchanged. All eleven
active owners are mandatory, with free anchors and all original legal modes.
The [inactive-owner proof](h5-short11-source-readback-and-translation-cycle-20261029/short11-inactive-owner-proof.json) classifies
263 variables and 259 touching constraints, checks five global optional-interval
uses and verifies 22 complete cross-part tables with 200 rows. The inactive slots
cannot restrict active source-feasible placements.

The positive ten-part source control fails only its missing mandatory cog0;
disabling exactly that requirement makes every model constraint pass. The
negative eleven-part control fails 84 constraints. Insert-capacity peaks are
two and four respectively.

The sole call returns **OPTIMAL** with one assignment in 1.834956600 seconds.
This is a satisfaction model with no objective, so the status does not establish
optimal source packing. The [response audit](h5-short11-source-readback-and-translation-cycle-20261029/short11-response-audit.json)
checks 5,003 recursive input bindings, the exact model, every assignment
constraint and all eleven active/two inactive owners. Algorithm/shared times
are 2.848882300/2.921346600 seconds, with no overrun.

The original-source reader rejects the [simplified placement](h5-short11-source-readback-and-translation-cycle-20261029/short11-core-placement.json).
The nine orthogonal originals have five pair failures and four stock failures;
with both cogs at the declared 7-degree baseline, the complete short11 has ten
pair failures and six stock failures. The cog phase loop is not run because
changing only cog angles cannot repair the already failing orthogonal anchors.
The [independent source audit](h5-short11-source-readback-and-translation-cycle-20261029/short11-source-audit.json) reconstructs all
eleven transforms and reproduces the [source failures](h5-short11-source-readback-and-translation-cycle-20261029/short11-source-failures.json)
over all 21 cutouts and 2,718 hole vertices. This checks the actual failed
candidate without excluding other placements or orientations.

## Original-source translation model

A distinct construction method keeps the nine orthogonal modes and both
7-degree cog phases, while allowing all **22 translation coordinates** to vary.
The [geometry preparation](h5-short11-source-readback-and-translation-cycle-20261029/translation-preflight.json) partitions the
original filled outlines into 174 convex pieces: two rectangles per bracket,
one per insert and 80 center-fan triangles per cog. Filling holes is appropriate
for the required PIH-off source separation.

For each of 8,726 piece pairs belonging to different originals, one unit
separating axis is selected from the rejected seed. Its inequality requires
0.225 mm separation. Original outline bounds require 0.025 mm stock clearance.
These exceed the unchanged required pair gap and stock guard. The objective
minimizes maximum absolute coordinate movement using one auxiliary variable.
There are **23 variables and 8,770 rows**.

The [independent geometry audit](h5-short11-source-readback-and-translation-cycle-20261029/translation-geometry-audit.json)
checks original-outline coverage, all posed pieces, every selected axis and
projection bound, all 22 stock domains and per-row positive/negative sign
controls. These sign controls are separate tests of each inequality, not a
joint feasible placement. Thirty-six seed rows fall below the target gap;
the largest independent projection replay difference is below 2.3e-13 mm.

The [method](h5-short11-source-readback-and-translation-cycle-20261029/translation-method.json) is a sufficient fixed-orientation,
fixed-axis construction system. Its negative result cannot establish source
infeasibility for the allocation. The single HiGHS dual-simplex call reports
INFEASIBLE after 0.010998900 seconds of solving, with no assignment. Its
0.391201000-second preparation is charged to the budget: algorithm/shared
totals are **3.100802900/3.148054900 seconds**. The
[response audit](h5-short11-source-readback-and-translation-cycle-20261029/translation-response-audit.json) reconstructs all matrix
rows, domains, objective and timing. No solver call is retried or extended.

## Exact restricted contradiction

The response audit derives axis-aligned necessary consequences of the frozen
LP, conservatively accounting for tiny non-axis coefficients over the full
stock domains. An additional 1e-9 mm allowance is included in each derived
pair bound. An eight-edge negative cycle contains six pair constraints and
two stock constraints.

The [independent cycle audit](h5-short11-source-readback-and-translation-cycle-20261029/translation-cycle-audit.json) reconstructs
those inequalities using exact rational arithmetic. Every left-hand coefficient
cancels and the right-hand sum is strictly negative, approximately
**-33.42045275048004 mm**. The [certificate](h5-short11-source-readback-and-translation-cycle-20261029/translation-cycle-certificate.json)
retains the complete rational sum, source plane indices, affected identities
and bounds. Thus arbitrary translation cannot rescue those frozen choices.
It does not exclude a different pair-separation direction, orientation or cog
phase, and it does not narrow the 440-candidate frontier.

## Preserved audit failures and next model

Two reader-preparation failures remain in the [failure record](h5-short11-source-readback-and-translation-cycle-20261029/preserved-failures.json):
an assertion attempted to replace absent cosmetic text, before any reader was
written; then a copied seven-part hole-count assertion omitted the four inserts.
The separate corrected reader derives the complete inventory from the original
job and required identities: 21 holes and 2,718 vertices. Original failed scripts,
a record of the two failed dependent invocations, and separate corrections are preserved.
No search is rerun to repair these audit defects.

The [next preflight](h5-short11-source-readback-and-translation-cycle-20261029/next-axis-choice-preflight.json) prepares **90 axis
variants across the six contradictory pair rows**. Every old branch remains
available; all other 8,720 pair rows remain fixed. All 1,440 stock-domain corner
checks pass for the proposed deactivation constants. The
[next method](h5-short11-source-readback-and-translation-cycle-20261029/next-axis-choice-method.json) specifies one selector per
variant, one selected variant per group, all 22 free translations and the
unchanged source clearances. Expected dimensions are 113 variables / 8,860 rows.
The [next-step record](h5-short11-source-readback-and-translation-cycle-20261029/next-step.json) requires an independent full model
audit before a single bounded mixed-integer call. **No such model or search has
opened.** First55 still needs construction, followed by complete source/native/
material validation, production integration and the entire H5 matrix.

## Publication and archive

The [push receipt](h5-short11-source-readback-and-translation-cycle-20261029/prior-main-push-receipt.json) records the normal atomic
fast-forward to **9dab2f4e** at 02:18 UTC after all six previous CI jobs passed.
At the [captured snapshot](h5-short11-source-readback-and-translation-cycle-20261029/main-ci-snapshot.json),
[CI 40805531238](https://github.com/skulitom/Nestbolt/actions/runs/40805531238)
has four passing jobs and Ubuntu/Windows checks running. This checkpoint queues
until all six pass; no live run is cancelled.

The [publication review](h5-short11-source-readback-and-translation-cycle-20261029/publication-review.json) confirms unchanged
production source, all three READMEs, upstream heads/releases, stable v0.1.0
and preview v0.2.0-alpha.1. The valid64 layout and 440-candidate frontier are
byte-identical. H2 retains its original gate and all 22 reserved vectors remain
unopened. Both new calls remain within their 60/90-second limits; there are no
native calls or complete source66 results.

The [manifest](h5-short11-source-readback-and-translation-cycle-20261029/raw-manifest.json) preserves **4360 canonical files**
and **870 identical aliases** in **31374396 archive bytes**, including the
raw models, source witness, all failed checks, exact certificate, preparation
failures and separate corrections. Independent ZIP/hash/alias/source-binding/
JSON/link verification is saved as `archive-checks.json` beside the manifest.
