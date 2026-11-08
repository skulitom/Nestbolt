# Full cog-body complement proof closes all 680 fixed cores — 2026-11-08

**The final nineteen cases are excluded by an independently checked source-body
area proof. All 680 exact first32 cores in this family are now excluded**, even
with the last cog and every bracket/insert free to move. The smallest deficit
in the final nineteen is **825.361864 mm²**. This is conditional on the eighteen
fixed frames and fourteen fixed cog poses; it does not exclude a whole allocation
or orientation class. H2/H5 remain open at **60% completed milestone weight**.
The preserved valid 64-part result remains best.

[Finer disk-domain witnesses](h5-free-cog-complement-closure-20261108/finer-disk-audit.json) independently verify
all 25,407 surviving 2.5 mm center cells, including the original fixed-source
disk certificates. They exclude another 1,296 cells but leave all nineteen
cases with 24,111 cells. No old stage is rerun.

[The stronger source-body proof](h5-free-cog-complement-closure-20261108/rectangle-complement-plan.json) uses the
entire cog's conservative **50,000 mm²** filled-area lower bound. [All eighty
original vertices](h5-free-cog-complement-closure-20261108/source-outer-bound.json) are inside a **140.001 mm**
circle about the source center; its convexity bounds the entire cog at every
exact rigid angle. No native floating-point all-angle guarantee is claimed.

Let `U` be the certified union of all possible bracket/insert component envelopes
and `F` the mandatory fixed source inner union. All companion bodies must lie in
`R = U minus F`, whose area was independently bounded earlier. A valid cog
cannot occupy `F`, so its area outside `R` is bounded by the area of its outer
neighborhood in stock outside `U union F`. Subtract that outside-area upper bound
from 50,000 mm² to obtain compulsory cog occupancy inside the companion region.
That occupied area is unavailable to brackets and inserts.

The first version uses each continuous center cell expanded to an outer rectangle.
A conservative 2.5 mm grid covers its possible outside area: only cells wholly
inside a certified `U` or `F` rectangle are removed. [Independent direct counting](h5-free-cog-complement-closure-20261108/rectangle-complement-audit.json)
replays all **24,111** rectangle queries, separately from producer prefix sums.
It leaves **2,997** center cells across the same nineteen cases.

[The circular refinement](h5-free-cog-complement-closure-20261108/circular-complement-plan.json) uses the actual
source outer-radius bound. A target grid square is included whenever its minimum
distance from the entire center square is at most 140.001 mm. This covers every
point of every possible cog throughout the continuous center cell; grid centers
are not sampled as substitute placements.

[Independent circular-stencil readback](h5-free-cog-complement-closure-20261108/circular-complement-audit.json)
checks **13,689 kernel cells**, retaining **10,301**, and directly counts all
**2,997** remaining complement queries. It uses no producer prefix queries.
[Boundary, diagonal and zero-padding controls](h5-free-cog-complement-closure-20261108/circular-controls.json)
pass, and every circular bound is no larger than its earlier rectangle bound.

[Every remaining center cell fails](h5-free-cog-complement-closure-20261108/circular-complement-cases.json): the
compulsory cog occupancy leaves too little of the certified companion region
for every necessary whole-part inventory. [The current frontier is empty](h5-free-cog-complement-closure-20261108/remaining-current-core-cases.json).
[All 680 source identities and their first excluding stages reconcile](h5-free-cog-complement-closure-20261108/fixed-core-frontier.json),
preserving the prior 661 exclusions and adding nineteen.

[A separate scope reconciliation](h5-free-cog-complement-closure-20261108/older-eight-scope-plan.json) identifies
the **eight earlier one-/three-turned first32 cores** that remain unexcluded.
It binds their actual source44 controls, exact fixed identities/poses, changed
world obstacles, family capacities and all necessary whole-part splits. The
source-invariant cog-area proof now excludes every short-sheet cog pose for all
eight, with a minimum **320.484383 mm²** deficit; any completion requires the
last cog on the first sheet. [All eight remain unresolved there](h5-free-cog-complement-closure-20261108/older-eight-core-scopes.json).
These are separate from the closed 680-case family.

The older worlds use **frame bit16**, with fifteen or sixteen cog sites; the
current seventeen-site/frame-bit17 masks cannot be reused. Historical review also
confirms that the [three-column eighteen-frame hard-domain scope already exists](h5-free-cog-complement-closure-20261108/historical-three-column-scope.json).
It must not be presented as a new construction or used to reopen a closed call.

| Bounded stage | Complete process (s) | Outcome |
|---|---:|---|
| free-cog-quarter-disk | 0.960994 | Pass |
| free-cog-quarter-disk-audit | 1.311539 | Pass |
| free-cog-complement | 0.754138 | Pass |
| free-cog-complement-audit | 1.674088 | Pass |
| free-cog-round-complement | 0.560196 | Pass |
| free-cog-round-complement-audit | 0.852081 | Pass |
| eight-core-scope | 0.814949 | Pass |

[Every bounded process closes](h5-free-cog-complement-closure-20261108/process-summary.json) with zero live
children under unchanged CCD1/thread and 2 GiB controls. Consumed preparation is
**116.459632 s**, including all inherited failed work. This is geometry research
on an exhausted numeric lineage, not a timed H5 pass. No optimizer is opened and
the timer may not reset.

[Next](h5-free-cog-complement-closure-20261108/next-step.json), derive complete source-dependent free-angle cog
center covers for the older eight cores, preserving their different world
geometry and bit identities. They retain necessary inventories, not layouts.
Four earlier arrangements and 440 whole-job allocations remain. Full66
source/native/material acceptance, product integration, parity and the H5 matrix
remain open.

[The preceding checkpoint reached main916859b2](h5-free-cog-complement-closure-20261108/prior-main-push-receipt.json);
[CI at review](h5-free-cog-complement-closure-20261108/main-ci-at-review.json) has **4 passed / 2 live
jobs**. This checkpoint awaits the ordinary push gate. Product, README and
release state are unchanged.

[Archive checks](h5-free-cog-complement-closure-20261108/archive-checks.json), [manifest](h5-free-cog-complement-closure-20261108/raw-manifest.json),
[source bindings](h5-free-cog-complement-closure-20261108/source-bindings.json), [historical references](h5-free-cog-complement-closure-20261108/external-evidence.json)
and [runtime pins](h5-free-cog-complement-closure-20261108/runtime-bindings.json) preserve the complete evidence.
