# Conditional bracket capacity — 2026-11-09

**The exact fixed29 arrangement omitting cog sites `[11,12,13]` is excluded.**
After verified conditional cell removals, its available occupied-envelope area
is at most **469,860.310592 mm²**, below the required **478,384 mm²** by
**8,523.689408 mm²**. Only **`[0,5,10]` and `[5,10,11]` remain** in this family:
453 of 455 arrangements are excluded at the original 0.2 mm clearance, including
428 already excluded at zero clearance. No whole allocation or orientation
class is excluded. H2/H5 remain open at **60% completed milestone weight**.

These are **common-line occupied outer envelopes with holes reserved**, not
net material. All 90 original holes remain in cutting geometry. The preceding
[scope audit](h5-fixed29-pointwise-capacity-20261108/occupancy-scope/checks.json)
binds production policy, original outer-envelope areas and rejection of parts
inside holes. No ordinary part-in-hole configuration is excluded. The fixed29
and twelve fixed cog poses retain their original identities; the first-sheet
movers are eight brackets and eight inserts, with the validated short9 unchanged.

## Complete pivot coverage and bounded conditional queries

[The conflict-row audit](h5-conditional-bracket-capacity-20261109/fixed29-pivot-dominance-audit.json) verifies all
**7,319 possible bracket reference cells**, their source self-collision witnesses
and complete mappings to **3,942 minimal rows**. A chosen bracket leaves seven
other brackets and eight inserts. If row A is a subset of row B, the allowed
companions for B are a subset of those for A. This permits graph-only area deficits
to transfer through the recorded mapping. Independent replay checks 2,975,446
antichain pairs; current compact positions and stable source labels stay distinct.

[Exactly nine predetermined queries](h5-conditional-bracket-capacity-20261109/fixed29-conditional-area-pilot-pivot-results.json)
sample the minimum, median and maximum forbidden-row cardinalities in each
case. All 27 family/joint bounds replay by independent horizontal and vertical
rectangle sweeps. Case 21 reference 613 fails by 7,066.696282 mm²; the certified
subset mapping excludes current bracket positions 613–616. This pilot does not
claim to cover every minimal row.

The initial independent audit matched six area queries, then a local coordinate
variable overwrote its dominance record when recording the first deficit.
[The failed audit and correction](h5-conditional-bracket-capacity-20261109/failed-audit-correction.json) remain
preserved. The producer was not repeated. A separately frozen corrected audit
verifies all nine queries; the complete failed audit cost remains charged.

[Eight pointwise queries](h5-conditional-bracket-capacity-20261109/fixed29-conditional-pointwise-pilot-audit.json)
then use occupied-envelope rectangles common to every position of the reference
bracket. Their 141 µm square buffers remain strictly within the original 0.2 mm
clearance. Open forbidden companion anchors are subtracted from closed covers,
preserving all boundary points and lines. Independent replay verifies 256 common
rectangle/cell corner checks, 17,025 companion covers, 380,225 complete Cartesian
boundary/interior classes and 24 exact areas. Three more individual reference
cells are excluded. These pose-dependent results **do not transfer through
graph dominance**.

[Three complete parent-region groups](h5-conditional-bracket-capacity-20261109/fixed29-group-pointwise-pilot-pivot-results.json)
cover every current child with the seed's original parent label and geometry.
Intersecting all member conflict rows gives a companion domain valid for any
chosen member. Common occupied rectangles use the whole enclosing anchor box.
Case 01 group `[317,318]` and case 21 group `[1461,1462,1463,1464]` fail; group
`[661,662,663,664]` remains open, while its earlier singleton 664 exclusion stands.
The union of permitted graph, singleton and group deductions contains **11
distinct bracket positions**, with their proof provenance retained.

## Reconciled full-domain exclusion

[Independent frontier readback](h5-conditional-bracket-capacity-20261109/fixed29-conditional-frontier-audit.json)
verifies 12,371 source self-collision witnesses and 2,471,360 directed root-clique
edges. Fourteen further cells are removed only where selecting that cell leaves
a clique-cover upper bound below the remaining required part count. Each
simultaneous-round witness is checked against the prior active set. All other
cells remain in the complete source cover.

| Omitted sites | Seed removals | Further count implications | Full joint area upper (mm²) | Result |
|---|---:|---:|---:|---|
| [0,5,10] | 2 | 9 | 497,091.028543 | Open |
| [5,10,11] | 0 | 0 | 484,740.614909 | Open |
| [11,12,13] | 9 | 5 | 469,860.310592 | Excluded |

The required global area is 478,384 mm². [All three full-domain results](h5-conditional-bracket-capacity-20261109/fixed29-conditional-frontier-case-results.json)
and [the two remaining cases](h5-conditional-bracket-capacity-20261109/remaining-fixed29-cases.json) preserve exact
integer bounds. The surviving masks retain **8,903 current nodes**. Case 21's
retained-node record is negative evidence preceding its whole-case exclusion,
not an open search domain. No new optimizer graph/model or call is opened.

[Five whole-reference-envelope checks](h5-conditional-bracket-capacity-20261109/fixed29-reference-body-pilot-audit.json)
tighten three surviving conditional bounds but exclude no further reference
cell. Let R be the companion union minus **fixed** forbidden regions, before
common-reference subtraction. The reference's full occupied area is at least
39,999 mm²; its possible area outside R is bounded exactly. Its compulsory
occupancy inside R reduces the space left for the seven other brackets and
eight inserts. This remains separate from the earlier common-moving-buffer
bound, avoiding double subtraction. All ten exact areas independently replay.

## Closed processes and remaining work

| Bounded stage | Complete process (s) | Cap (s) | Result |
|---|---:|---:|---|
| fixed29-pivot-dominance | 1.845322 | 20 | Pass |
| fixed29-pivot-dominance-audit | 1.275651 | 30 | Pass |
| fixed29-conditional-area-pilot | 5.964222 | 30 | Pass |
| fixed29-conditional-area-pilot-audit | 26.498850 | 60 | Preserved failure |
| fixed29-conditional-area-pilot-audit-v2 | 29.472051 | 60 | Pass |
| fixed29-conditional-pointwise-pilot | 5.488861 | 40 | Pass |
| fixed29-conditional-pointwise-pilot-audit | 27.293233 | 60 | Pass |
| fixed29-group-pointwise-pilot | 2.036029 | 40 | Pass |
| fixed29-group-pointwise-pilot-audit | 5.796569 | 60 | Pass |
| fixed29-conditional-frontier | 6.470054 | 30 | Pass |
| fixed29-conditional-frontier-audit | 33.859108 | 60 | Pass |
| fixed29-reference-body-pilot | 5.614348 | 30 | Pass |
| fixed29-reference-body-pilot-audit | 41.156976 | 60 | Pass |

[All thirteen processes close](h5-conditional-bracket-capacity-20261109/process-summary.json) with zero children,
unchanged CCD1/thread controls and 2 GiB Windows Job limits. Raw filenames retain
their preparation-date suffix; each process also records its actual UTC opening.
Consumed numeric preparation is **208.194276 s**, including the failed audit.
No optimizer, timer reset or timed H5 acceptance is permitted from this lineage.

[Next](h5-conditional-bracket-capacity-20261109/next-step.json), a complete subdivision proof could tighten
reference-cell bounds in the two surviving scopes. None has been prepared.
All 440 whole-job allocations, full 66-part source/native/material validation,
production integration and the full H5 matrix remain open. The valid 64-part layout
stays best. The separate eight older first32 and 680 five-column cores stay
closed. Product, README and release state are unchanged.

[The preceding checkpoint reached main 22157486](h5-conditional-bracket-capacity-20261109/prior-main-push-receipt.json).
[Its CI at review](h5-conditional-bracket-capacity-20261109/main-ci-at-review.json) has **5 passed / 1
live jobs**; this checkpoint awaits the ordinary push gate.
[Archive checks](h5-conditional-bracket-capacity-20261109/archive-checks.json), [manifest](h5-conditional-bracket-capacity-20261109/raw-manifest.json),
[source bindings](h5-conditional-bracket-capacity-20261109/source-bindings.json),
[historical references](h5-conditional-bracket-capacity-20261109/external-evidence.json) and
[runtime pins](h5-conditional-bracket-capacity-20261109/runtime-bindings.json) preserve every consumed input.
