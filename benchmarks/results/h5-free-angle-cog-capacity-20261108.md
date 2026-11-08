# Free-angle cog capacity: nineteen fixed cores remain — 2026-11-08

**Independent continuous geometry proofs exclude another 218 of the 237
unresolved exact first32 arrangements.** Together with the prior 443 exclusions,
**661 of the original 680 fixed cores are excluded; nineteen remain**. Their
last cog and all brackets/inserts were free to move. These are conditional
proofs for the eighteen fixed frames and fourteen fixed cogs, not exclusions of
whole allocations or orientation classes. H2/H5 stay open at **60% completed
milestone weight**; the valid 64-part result remains best.

[Original-source geometry](h5-free-angle-cog-capacity-20261108/geometry-plan.json) establishes that every
rigid pose of the remaining cog has the same filled outer area. Exact rational
source vertices give **50,062.71893798297 mm²**. The symbolic shoelace polynomial
is source area times `c²+s²`; translation terms cancel and exact rotations have
`c²+s²=1`. [Independent triangle-fan, winding and segment checks](h5-free-angle-cog-capacity-20261108/geometry-audit.json)
verify all eighty vertices, 3,080 nonadjacent edge pairs and a centered disk
contained in the cog for every angle.

The first disk helper used an overly restrictive infinite-edge-line condition
and stopped on an assertion. [Its complete 0.184916 s process](h5-free-angle-cog-capacity-20261108/geometry-20261107-process.json)
and raw source are preserved. The corrected stage uses distance to the actual
segments; no result from the failed stage was treated as a certificate.

[The source certificate](h5-free-angle-cog-capacity-20261108/source-cog-geometry.json) distinguishes exact
rigid geometry from native floating-point behavior. It also supplies explicit
determinant, coordinate and vertex-error predicates for future native candidates.
It does not claim an unproved all-angle `sin_cos` accuracy guarantee. No full
native layout is accepted by these research proofs.

A conservative **50,000 mm²** cog body leaves at most **415,326.048858 mm²** for
short-sheet companions, wherever that cog is placed or rotated. [All original
whole-part inventories](h5-free-angle-cog-capacity-20261108/short-cog-inventories.json) still force at least
**495,777 mm²** of brackets/inserts onto the first sheet. [Every one of the 680
cores fails with the last source cog on the short sheet](h5-free-angle-cog-capacity-20261108/short-cog-capacities.json).
Thus each previously unresolved completion requires that cog on the first sheet.

[The necessary center cover](h5-free-angle-cog-capacity-20261108/center-cover-plan.json) uses a fixed-axis
152 mm square inside the universal cog disk, source-contained fixed obstacles,
and the physical stock. [Direct-mask readback](h5-free-angle-cog-capacity-20261108/center-cover-audit.json)
verifies **817,047 continuous point/interval classes**, **521,391 retained
classes** and **463 closed cover boxes**. All 237 cases initially have nonempty
necessary center domains. No sampled angle or feasible-pose claim is involved.

[The first coupled-area proof](h5-free-angle-cog-capacity-20261108/coarse-area-plan.json) covers each necessary
center with a continuous 10 mm cell. Any cog in that cell must occupy a common
set of companion-region cells inside its 108 mm disk. Their areas are subtracted
from the independently certified companion-area upper bound. Worst corner-pair
distances make the bound valid at every point in the center cell.

[Independent direct raster and integer shift sums](h5-free-angle-cog-capacity-20261108/coarse-area-audit.json)
replay all **948 arrays**, separately from the producer convolution. They exclude
**217,298 of 245,909 center cells** and **199 fixed cores**, leaving 38. The
calculation had completed before the user pause; resume audited its saved output
without rerunning the preparation.

| Verified refinement | Input cores | Newly excluded | Remaining |
|---|---:|---:|---:|
| 10 mm continuous occupancy bound | 237 | 199 | 38 |
| 5 mm occupancy, 109 mm source disk | 38 | 3 | 35 |
| Stock/frame/fixed-cog disk witnesses | 35 | 11 | 24 |
| 2.5 mm continuous occupancy bound | 24 | 5 | 19 |

[The 5 mm refinement](h5-free-angle-cog-capacity-20261108/fine-area-audit.json) checks all eighty rational
segment distances justify a **109 mm** disk, then subdivides only surviving
parent cells. Independent vertical-prefix sums replay the producer's horizontal
stripes and all 152 arrays. No excluded parent cell returns.

[Disk-domain witnesses](h5-free-angle-cog-capacity-20261108/disk-domain-audit.json) independently check
**1,360 fixed-source segment distances**, seventeen conservative fixed-cog disks
and eighteen frame rectangles. Every rejected cell has a complete stock, frame
or cog witness. This removes 25,019 stock cells, 5,809 frame cells and 756 cog
cells, leaving 34,551 cells across twenty-four cores.

[The 2.5 mm refinement](h5-free-angle-cog-capacity-20261108/quarter-area-audit.json) independently verifies
96 arrays and all **138,204 child cells**. It excludes 112,797 cells and five
more cores. [Nineteen cases and 25,407 necessary center cells remain](h5-free-angle-cog-capacity-20261108/remaining-first32-cases.json).
They are not placements. [The full 680-case frontier](h5-free-angle-cog-capacity-20261108/fixed-core-frontier.json)
reconciles every identity and its first excluding stage, without conflating
these cases with four earlier unresolved arrangements or 440 whole-job allocations.

| Bounded stage | Complete process (s) | Outcome |
|---|---:|---|
| geometry-20261107 | 0.184916 | Failure preserved |
| geometry-v2-20261107 | 0.196523 | Pass |
| geometry-audit-20261107 | 0.634327 | Pass |
| centers-20261107 | 0.546312 | Pass |
| centers-audit-20261107 | 0.651918 | Pass |
| area-grid-20261107 | 11.933263 | Pass |
| area-grid-audit-20261108 | 18.907152 | Pass |
| fine-grid-20261108 | 1.943706 | Pass |
| fine-grid-audit-20261108 | 3.025308 | Pass |
| disk-domain-20261108 | 0.449443 | Pass |
| disk-domain-audit-20261108 | 1.112525 | Pass |
| quarter-grid-20261108 | 8.118565 | Pass |
| quarter-grid-audit-20261108 | 10.908943 | Pass |

[All process receipts](h5-free-angle-cog-capacity-20261108/process-summary.json) close with zero live children
under unchanged CCD1/thread and 2 GiB Windows Job controls. Complete consumed
preparation is **113.369355 s**, including the new failure and all inherited
failed work. This research lineage exceeds 60 seconds and may not open an
optimizer or reset its timer. It is not a timed H5 pass.

[Next](h5-free-angle-cog-capacity-20261108/next-step.json), apply the existing disk-domain witnesses to the
new 2.5 mm cells, then inspect the controlling geometry and inventories of any
survivors. Preserve complete continuous coverage. Any future timed constructor
must recompute numerical input independently from original sources and pass a
new preflight. Full66 source/native/material acceptance, integration, parity and
the H5 matrix remain open.

[The prior three checkpoints reached main](h5-free-angle-cog-capacity-20261108/prior-main-push-receipt.json)
and [all six checks on cc38001e pass](h5-free-angle-cog-capacity-20261108/main-ci-at-review.json). This evidence
checkpoint awaits its ordinary fast-forward push. Product code, README and
releases remain unchanged.

[Archive checks](h5-free-angle-cog-capacity-20261108/archive-checks.json), [manifest](h5-free-angle-cog-capacity-20261108/raw-manifest.json),
[source bindings](h5-free-angle-cog-capacity-20261108/source-bindings.json), [historical references](h5-free-angle-cog-capacity-20261108/external-evidence.json)
and [runtime pins](h5-free-angle-cog-capacity-20261108/runtime-bindings.json) preserve the complete evidence.
