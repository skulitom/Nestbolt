# H5: necessary capacities and rejected domain reductions

The complete capacity-strengthened model passes every geometry, field and
control audit, but its sole bounded search closes **UNKNOWN** without a
candidate. Two finite representation studies provide no eligible reduction.
H5 remains open, and the best source-valid layout still contains 64 of the
66 required originals.

## Necessary capacities, fully verified

The previous precise row/bracket model is preserved byte for byte: all
7,932 variables, all 32,137 constraints and all soft hints. The new model
adds only 2,876 conditional intervals and two cumulative constraints, for
35,015 constraints in total. It uses the existing orientation selectors;
there are no new variables. All 43 first-sheet blocks remain mandatory and
movable, containing 54 originals; the exact twelve short-sheet originals
remain fixed. All 903 block pairs are still checked.

The [fresh containment audit](h5-row-bracket-capacity-and-domain-studies-20261028/capacity-containment-audit.json) proves
848 rectangles strictly inside their original filled outlines through
66,352 exact rational source-edge checks. All 173,106 same-mode rectangle
pairs have disjoint interiors. These become 1,438 optional component choices.
The [necessity proof](h5-row-bracket-capacity-and-domain-studies-20261028/capacity-necessity-proof.json) justifies capacities
of 2,987,000 µm for summed heights at each X section and 1,487,000 µm for
summed widths at each Y section, with no extra clearance or exterior area.
The containment record precedes model creation; its `new_model_created: false`
describes that earlier audit stage, not the final checkpoint.

The [model audit](h5-row-bracket-capacity-and-domain-studies-20261028/model-audit.json) independently rechecks every field
in all three ancestor models, every unchanged field and each new constraint.
It reproduces all ten capacity event sweeps from the actual serialized model
and compares them to the independent geometric preflight. The 52-part
control fails only its 14 missing-part requirements, and all eight 62-part
controls fail only their four absent brackets. Audit copies disabling only
those missing requirements pass. The full overlapping control now fails
32 constraints, including both new capacities. The
[control records](h5-row-bracket-capacity-and-domain-studies-20261028/model-controls.json) retain exact failures and slacks.
Source and row-cardinality checks again account for all 66 original identities.

## Sole search, closed

The frozen call uses a 60-second algorithm limit inside a 90-second shared
limit, four workers, seed 0 and `fj` disabled. Search starts at 16.88 seconds.
It returns **UNKNOWN**, with no incumbent, assignment or source candidate.

| Quantity | Seconds |
|---|---:|
| Allocated solve time | 59.173989 |
| Returned solve time | 59.234050 |
| Solver wall time | 59.230060 |
| Algorithm time | 60.067082 |
| Shared time | 60.142702 |
| Returned solve soft overrun | 0.060061 |
| Algorithm soft overrun | 0.067082 |

The returned worker reports 44,065 branches and 2,093 conflicts; these are
not aggregate counters across workers. The
[response audit](h5-row-bracket-capacity-and-domain-studies-20261028/response-audit.json) verifies model bytes, parameters,
logs, response, counters and timing. The call is closed. UNKNOWN supplies
no infeasibility certificate, and no native validation occurred.

## Convex-cover study: safe but too small a reduction

One deterministic finite study considers pairwise convex hulls of existing
free-domain cells. A merge is allowed only when its hull stays inside the
unchanged source-free domain, the halfplane count falls, and every vertex
of both original halfplane relaxations satisfies every new inward-rounded
plane. Selection prioritizes the largest plane saving, then area and stable
creation IDs. Cells may overlap. The original domains remain exactly equal
to the union of the resulting cells.

The [independent audit](h5-row-bracket-capacity-and-domain-studies-20261028/convex-cover-audit.json) uses rational polygon
clipping, separately from the constructor's pairwise line intersections.
It verifies 3,960 vertices and 16,214 exact vertex/plane inequalities, accounts
for every old cell once, and confirms every new halfplane is conservative.
The [proof](h5-row-bracket-capacity-and-domain-studies-20261028/convex-cover-proof.json) covers **every previously accepted
integer displacement**, not only the 33 positive and 16 negative controls.

Forty-seven merges reduce 1,038 cells to 991 and typed planes from 4,044 to
3,888. After owner replication, selectors fall from 7,260 to 6,890 and planes
from 28,640 to 27,380. That is only **4.3994%**, below the frozen 25% threshold.
The geometry proof passes, but the representation is not selected and no
replacement model or solver call is created.

## Repeated-spacing inventory: also rejected

The second finite study explores the exact integer identity
`deltaX = q * 258900 + r`, with `0 <= r <= 258899`, to share repeated cog-row
geometry. It inventories all stock-permitted quotients for every one of the
16 existing row/bracket types, retaining the original source obstacles.
The 104 quotient cases form 88 typed local groups.

This decomposition projects to **29,190 planes**, 1.9204% more than the
28,640 baseline, and 7,875 cells. Only 24 transformed geometric domains are
strictly equal to their originals; all 80 discrepancies remain recorded.
The [inventory audit](h5-row-bracket-capacity-and-domain-studies-20261028/periodic-inventory-audit.json) verifies the
quotient coverage, grouping, counts and equality outcomes. It does not certify
replacement geometry or preservation of old integer placements. The size
prefilter already rejects this approach, so it receives no model or search.

## Next conditional construction and publication

The next preflight fixes only the fourteen first-sheet cog poses at the three
row anchors of the audited 61-part control. All forty orthogonal blocks will
remain movable and mandatory; the exact short twelve are unchanged. Preserve
all previous source/capacity constraints, add six anchor equalities and use
the 61-part layout only as soft hints for the other present parts. Audit the
whole model, the 61-part control, all eight 62-part controls and an overlapping
full negative before any separately bounded call. This is a conditional
construction, not the previously excluded arrangement with all 61 poses fixed.
No such new model or call exists in this checkpoint.

Main remains 0d6dc0fa at the snapshot, and all six jobs in CI 40777420353 now
pass. Prior local checkpoint 0b84eb89 and this checkpoint can be pushed
together after commit and fresh branch/ref checks. No live run is cancelled.
Fresh GitHub reads confirm unchanged Sparrow/Studio heads and releases,
Stable v0.1.0 and Preview v0.2.0-alpha.1. Production and all three READMEs
remain unchanged. The valid 64, all 444 necessary allocation survivors, H2's
original gate and its 22 unopened vectors are preserved. H2/H5 remain open
at **60% completed milestone weight**. No new release qualifies.

The [raw manifest](h5-row-bracket-capacity-and-domain-studies-20261028/raw-manifest.json) binds 874 canonical files,
538 identical aliases and 5029264 compressed bytes. It includes full
models and controls, both rejected studies, exact rational certificates,
the closed solver response, scripts and recursive source dependencies.
Independent verification checks every byte, alias, hash binding, JSON and
local report link.
