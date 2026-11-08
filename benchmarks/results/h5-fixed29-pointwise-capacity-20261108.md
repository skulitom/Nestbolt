# Fixed29 pointwise capacity — 2026-11-08

**One more exact fixed29/cog arrangement is excluded: omitted sites
`[10,11,12]`. Three remain: `[0,5,10]`, `[5,10,11]`, `[11,12,13]`.**
The excluded arrangement has at most **477,644.122166 mm²** available for
eight original brackets and eight original inserts, which require at least
**478,384 mm²**. The **739.877834 mm² deficit** holds even at zero clearance.
This brings the fixed29 family to **452 of 455 excluded**, including **428 at
zero clearance**. It is conditional on the actual fixed29 and twelve fixed
cog poses. No whole allocation or orientation class is excluded.

H2/H5 remain open at **60% completed milestone weight**; the valid 64-part layout
remains best. The separate eight older first32 cores and 680 five-column cores
remain closed. No optimizer call, placement, native validation or release occurs.

The current scope fixes 18 frames and 11 inserts, twelve of fifteen cog sites,
and leaves 8 brackets + 8 inserts free over their complete source orientation domains.
The independently validated short9 remains 4 brackets + 2 inserts + 3 cogs. Site-template
labels designate positions, not original cog-owner assignments. The earlier
[identity/scope reconciliation](h5-older-cog-family-closure-20261108/remaining-fixed29-scopes.json)
preserves all 66 original quantities and ownership constraints.

## Current domains and exact area controls

[The initial area audit](h5-fixed29-pointwise-capacity-20261108/four-fixed29-current-areas-v3-audit.json) checks
all **16,267 current exact-circle graph cells**, 10 geometry groups and 12 original
mode aliases, including all 80 component vertices. The graph positions are
compacted; their source-node labels remain unchanged. Exact prior-node maps and
the subsequent capacity-model inputs are verified, preserving all 16 strip
inequalities. Each original component is enclosed outward, swept over every
closed anchor cell and clipped to outward physical stock. Required areas use
conservative source lower bounds 39,999/19,799 mm² per bracket/insert.

The first preparation failed an incorrect source-label/index equality. The
second passed the mapping check but hit its preset dense-grid size guard.
Neither produced a case area or exclusion. Both complete failures and corrections
are retained: [index mapping](h5-fixed29-pointwise-capacity-20261108/failed-indexing-correction.json),
[grid-size guard](h5-fixed29-pointwise-capacity-20261108/failed-grid-size-correction.json). A new bounded vertical
strip algorithm replaced dense allocation. Its exact signed endpoint prefixes
agree with an independent horizontal active-rectangle interval merge/subtraction.

[Finer source material](h5-fixed29-pointwise-capacity-20261108/fixed29-dense-cog-material-audit.json) adds
**12,870 rectangles across 15 cog sites**, derived inside the original convex
source pieces in bands no more than 1 mm high. Exact binary64 transforms are
rational arithmetic. Independent replay checks **51,480 rectangle corners
against 678,960 source halfplanes**. The earlier 75 rectangles per cog remain.
The material union alone excludes no additional case.

[Pointwise source covers](h5-fixed29-pointwise-capacity-20261108/fixed29-pointwise-domains-audit.json) then
subtract the OPEN forbidden anchor rectangles from every CLOSED current cell.
It refines **2,743 cells** while removing no whole current cell. The combined
cover of all 16,267 current cells contains **20,290 closed boxes**. Every boundary point and open-interval class is retained exactly:
**668,825 complete classes** pass independent set-equality checks, without reuse
of the producer subtraction algorithm. Exact swept-area conservation then
excludes `[10,11,12]`. Every source mode and every continuous anchor is covered.

[The original-clearance check](h5-fixed29-pointwise-capacity-20261108/fixed29-clearance-domains-audit.json)
uses the unchanged 0.2 mm job requirement. Each certified fixed-source rectangle
is expanded 141 µm on both axes; every buffer offset has squared norm at most
39,762 µm², strictly below 40,000 µm². These are **forbidden clearance regions**,
not additional source material. A source point there would be too close to an
actual fixed-source point. Another **590,749 boundary/interior classes** and
nine exact area bounds pass; all three remaining cases stay open.

| Omitted sites | Current area | Finer fixed material | Pointwise, zero clearance | Original clearance | Result |
|---|---:|---:|---:|---:|---|
| [0, 5, 10] | 503,016.528981 | 501,461.824992 | 497,479.737709 | 497,091.028543 | Open |
| [5, 10, 11] | 491,960.686511 | 490,084.306520 | 485,094.419723 | 484,740.614909 | Open |
| [10, 11, 12] | 485,306.699036 | 483,115.064649 | 477,644.122166 | — | Excluded |
| [11, 12, 13] | 492,069.274645 | 488,975.800301 | 481,250.607685 | 480,776.633787 | Open |

Areas are mm² upper bounds for the combined moving material. They must reach
478,384 mm²; a surplus is only a necessary relaxation, not a valid placement.
[The four-case frontier](h5-fixed29-pointwise-capacity-20261108/four-case-frontier.json) and
[remaining cases](h5-fixed29-pointwise-capacity-20261108/remaining-fixed29-cases.json) retain exact integers.

## Closed processes and remaining work

| Bounded stage | Complete process (s) | Cap (s) | Result |
|---|---:|---:|---|
| four-fixed29-current-areas | 0.429996 | 30 | Preserved failure |
| four-fixed29-current-areas-v2 | 0.398253 | 30 | Preserved failure |
| four-fixed29-current-areas-v3 | 0.907339 | 30 | Pass |
| four-fixed29-current-areas-v3-audit | 5.068955 | 60 | Pass |
| fixed29-dense-cog-material | 2.672135 | 30 | Pass |
| fixed29-dense-cog-material-audit | 20.005834 | 60 | Pass |
| fixed29-pointwise-domains | 7.690333 | 40 | Pass |
| fixed29-pointwise-domains-audit | 27.350413 | 60 | Pass |
| fixed29-clearance-domains | 5.843790 | 40 | Pass |
| fixed29-clearance-domains-audit | 41.276618 | 60 | Pass |

[All ten processes close](h5-fixed29-pointwise-capacity-20261108/process-summary.json) with zero children,
unchanged CCD1/thread controls and 2 GiB Windows Job limits. Both failed
preparations remain charged. Consumed numeric preparation is **154.076606 s**;
no optimizer, timer reset or timed H5 acceptance is permitted from this lineage.

[Next](h5-fixed29-pointwise-capacity-20261108/next-step.json), stronger conditional companion bounds may use
these complete pointwise covers. No conditional graph or optimizer model is
prepared. The three exact scopes, all 440 whole-job allocations, full 66-part
source/native/material checks, production integration and the full H5 matrix
remain open. Product, README and releases are unchanged.

[The prior checkpoint reached main 38fec6c9](h5-fixed29-pointwise-capacity-20261108/prior-main-push-receipt.json).
[Its CI at review](h5-fixed29-pointwise-capacity-20261108/main-ci-at-review.json) has **4 passed / 2
live jobs**; this checkpoint awaits the ordinary push gate.
[Archive checks](h5-fixed29-pointwise-capacity-20261108/archive-checks.json), [manifest](h5-fixed29-pointwise-capacity-20261108/raw-manifest.json),
[source bindings](h5-fixed29-pointwise-capacity-20261108/source-bindings.json),
[historical references](h5-fixed29-pointwise-capacity-20261108/external-evidence.json) and
[runtime pins](h5-fixed29-pointwise-capacity-20261108/runtime-bindings.json) preserve the evidence.
