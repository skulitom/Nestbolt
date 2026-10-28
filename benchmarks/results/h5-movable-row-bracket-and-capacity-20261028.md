# H5: movable source row/bracket constraints and necessary capacities

The complete model now permits all 43 first-sheet blocks to move and removes
the false cog-row/bracket cover collisions observed in eight valid controls.
Its sole bounded search closes **UNKNOWN**, without a candidate. Two cheaper
geometry variants fail the frozen acceptance checks. A subsequent exact
capacity preflight passes and is ready for a fresh model. H5 remains open;
the best valid result still contains 64 of the 66 required originals.

## Source geometry and complete model

The unchanged short sheet contains seven brackets, four inserts and one cog.
The first sheet requires 18 frames, five brackets, 17 inserts and 14 cogs.
Those 54 originals move in 43 blocks with 86 independent anchor coordinates:
40 singleton parts and three rigid cog rows containing 5/5/4 cogs. Row
members retain their internal phase and spacing. The raw builder's field
`independently_movable_first_sheet_originals: 54` counts contained originals;
it does not mean that all 54 have independent anchors.

Original cog/bracket configuration obstacles are translated and united for
both row sizes and every one of eight legal bracket orientations. The
[geometry audit](h5-movable-row-bracket-and-capacity-20261028/source-region-audit.json) independently reconstructs
72 typed source pairs through 22,464 Minkowski hulls. Adjacent constrained
triangles merge only when their exact union remains convex. The resulting
16 domains contain 1,038 cells and 4,044 inward-rounded halfplanes. Rational
error checks prove every integer halfplane conservative. All 33 valid
control displacements are accepted; all 16 zero displacements are rejected.

The [model audit](h5-movable-row-bracket-and-capacity-20261028/model-audit.json) verifies every protobuf field:
7,932 variables, 32,137 constraints, 7,260 row/bracket cell selectors and
4,960 soft hints. Fifteen row/bracket owner pairs cover 120 orientation
cases. The three existing source row/row constraints remain; covers still
handle orthogonal parts and row-to-frame/insert clearance. All 903 block
pairs are accounted for, with every target block mandatory.

The 52-part primary control fails exactly its 14 missing-part requirements.
An audit copy changing only those presence requirements passes. All eight
62-part source witnesses similarly fail only the four absent brackets;
their previous false row-cover rejections disappear. The overlapping full
66-part control has 982 original-source collisions and fails all 30 relevant
collision constraints. The [source bridge](h5-movable-row-bracket-and-capacity-20261028/source-bridge-audit.json)
rechecks original transforms, and the
[identity audit](h5-movable-row-bracket-and-capacity-20261028/row-identity-audit.json) rejects all three wrong-size
row substitutions and accounts for every original exactly once.

## Closed search and rejected simplifications

One frozen search uses a 60-second algorithm limit within a 90-second shared
limit, four workers, seed 0 and `fj` disabled. Presolve reaches search at
14.96 seconds. The returned result is **UNKNOWN**, with no incumbent,
assignment or source candidate. UNKNOWN proves no infeasibility.

| Recorded quantity | Seconds |
|---|---:|
| Allocated solve time | 59.139071 |
| Returned solve time | 59.205333 |
| Solver wall time | 59.201197 |
| Algorithm time | 60.073948 |
| Shared time | 60.156130 |
| Returned solve soft overrun | 0.066262 |
| Algorithm soft overrun | 0.073948 |

The returned worker reports 37,709 branches and 11,173 conflicts; these are
not aggregate worker totals. The [response audit](h5-movable-row-bracket-and-capacity-20261028/response-audit.json)
rechecks the full model, source guards, hashes, parameters, logs, response
and timing. The call is closed; no restart, reseed or extension occurs.

A frozen finite study then compares exactly two conservative obstacle
simplifications. Eligibility requires exact containment of the precise
forbidden geometry, all 33 positive controls, all 16 negative controls and
at least 25% fewer expanded halfplanes.

| Variant | Expanded planes | Positive controls | Precise obstacle containment | Eligible |
|---|---:|---:|---|---|
| Full obstacle convex hull | 9,260 | 31/33 | Pass | No |
| Exact end cogs, middle hull | 21,020 | 33/33 | 13 failures | No |

The precise baseline has 28,640 expanded planes. The second variant misses
1.7552089812117774e-13 mm² in total, including boundary-only discrepancies;
the strict rule is retained despite the small area. The
[independent study audit](h5-movable-row-bracket-and-capacity-20261028/simplification-audit.json) preserves every
failure. Neither variant is selected, and neither receives a solver call.

## Necessary whole-sheet capacity preflight

The next strengthening uses rectangles strictly **inside** original filled
outlines. Each frame/insert has one, each bracket has two, and each cog has
92 from the previously audited 5 mm grid, translated to its actual row
position and rounded further inward. Holes remain reserved as required by
common-line mode. These are necessary occupancy bounds, not exterior
collision covers or another geometry simplification.

The [capacity audit](h5-movable-row-bracket-and-capacity-20261028/capacity-audit.json) verifies all 848 rectangles
across 14 modes using exact decimal-rational ray parity and 66,352 source
edge tests. All 173,106 same-mode rectangle pairs have disjoint interiors,
including rectangles in different cogs of the same row. Replication across
the existing block/mode choices gives 1,438 optional components.

Any valid original layout must satisfy two whole-sheet capacities: summed
rectangle heights at each X section cannot exceed 2,987,000 µm; summed widths
at each Y section cannot exceed 1,487,000 µm. These use the original source
stock dimensions and add no clearance. The
[necessity proof](h5-movable-row-bracket-and-capacity-20261028/capacity-proof.json) explains why no valid source
placement is excluded. Exact event sweeps accept the primary 52-part control
and all eight 62-part controls. The overlapping 66-part control exceeds both
bounds; all [control results](h5-movable-row-bracket-and-capacity-20261028/capacity-controls.json) are preserved.

This preflight creates **no new model and no solver call**. The next model
must retain every existing field and add only 2,876 conditional intervals
and two cumulative constraints, using existing mode literals and no new
variables. Audit all fields, controls and source identities before freezing
one separately bounded call. The failed hull variants and all closed
searches remain closed. Native validation still requires a complete,
original-source-valid 66-part candidate.

## Publication and scope

The prior source-region/fixed-layout checkpoints reached main 0d6dc0fa in a
normal atomic fast-forward after all six prior CI jobs passed. The saved
[push receipt](h5-movable-row-bracket-and-capacity-20261028/prior-push-receipt.json) records that transition.
At this checkpoint's snapshot, CI 40777420353 has five passing jobs and
Windows checks running. This checkpoint waits for all six before a new
normal push; no live run is cancelled.

Production source and all three READMEs are unchanged. Fresh GitHub reads
confirm unchanged Sparrow/Studio heads and releases, Stable v0.1.0 and
Preview v0.2.0-alpha.1. The original H2 gate remains open under Artem's
decision; its remaining 22 vectors stay unopened. All 444 necessary
allocation survivors and the valid 64-part result remain preserved. There
is no native validation, global infeasibility claim or qualified new release.
H2/H5 remain open at **60% completed milestone weight**.

The [raw manifest](h5-movable-row-bracket-and-capacity-20261028/raw-manifest.json) binds 826 canonical files,
531 identical aliases and 3986851 compressed bytes. It includes all
source geometry, failed variants, capacity evidence, full model/response,
scripts, source-hash dependencies and local Python imports. Independent
archive verification checks every byte, alias, binding, JSON and report link.
