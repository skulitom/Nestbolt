# Direct original-source pose construction — 2026-11-07

The new continuous-pose model reduces actual summed overlap from
**41,109.022811 to 27,392.624149 mm²** and failing pairs from **39 to 32**.
It stops at its frozen time limit. The best layout remains invalid: **29
overlaps and three insufficient-clearance pairs**, with no stock failures.
No native or LightBurn call follows. H2/H5 remain open at **60% completed
milestone weight**; four fixed arrangements and 440 whole allocations remain.
Neither a valid layout nor an allocation exclusion has been established.

## Fresh source geometry and all-angle domains

The model uses **56 independent translation coordinates and 12 continuous
cog-angle coordinates**, retaining each bracket/insert's selected legal pose.
Every angle spans one complete 2π interval. Cog angle coordinates are scaled
by 140 mm, with an explicit source-center pivot and independently checked
translation reconstruction. All **378 pairs of moving originals** remain.

The objective equally weights two areas: actual filled-original intersections
and intersections of clearance contours derived from those originals. Both
terms have units mm². Filled outers enforce noPIH; all original contours and
holes remain unchanged in source output. The clearance term remains positive
at original contact or a short gap, where original intersection area can be zero.

Fresh local clearance contours are unions of original convex pieces expanded
by a 0.115 mm square. [Independent exact winding and support readback](h5-direct-source-pose-construction-20261107/source-and-model-audit.json)
checks **9,344 source-edge/expanded-edge pairs**. Every expanded contour
contains a disc expansion of radius 0.114 mm about its filled original.
The minimum certified local boundary gap is **0.114999999975 mm**. Disjoint
clearance interiors therefore provide at least 0.228 mm original separation
under rigid geometry, above the unchanged 0.2117086725 mm source checker
threshold. Numerical output still requires independent source validation.

[The stock-domain proof](h5-direct-source-pose-construction-20261107/stock-domain-proof.json) derives a conservative
all-angle cog radius of **140.000002 mm** directly from exact original vertices.
Its center box fits the entire original at every angle. Selected bracket and
insert domains retain their source bounds. The fixed 29-part core and nine-part short sheet
are independently source-valid, and the moving box clears the fixed core.
[208 original-source corner controls](h5-direct-source-pose-construction-20261107/stock-corner-controls.json)
exercise every owner and several cog angles; all pass.

[Four seed positions are clamped](h5-direct-source-pose-construction-20261107/seed-domain-clamps.json) only as needed
for the new all-angle domains. The reconstructed seed retains all 66 originals
and still fails 39 pairs. Its original summed overlap is 41,109.022811 mm²;
the source changes are explicitly preserved and are not claimed as a repair.

[Complete geometry/model preparation](h5-direct-source-pose-construction-20261107/preparation-process.json) takes
**1.020532 s**, including source-buffer construction, exact support selection,
source checks, initial scoring and serialization. The complete consumed
preparation charge is **46.995655 s**, including the earlier candidate lineage.

## Independent model and derivative checks

The audit reconstructs every owner, parameter, bounds interval, source pose,
pair and clamp. All full 66 original seed checks are replayed. The batched
boundary-gradient implementation is compared with the separately implemented
scalar source kernel in **156 cases**, with zero discrepancy. Shared edges
retain the explicit symmetric half-weight convention; no unique classical
derivative is claimed at a nonsmooth configuration.

[136 independent central differences](h5-direct-source-pose-construction-20261107/derivative-controls.json),
[six projected one-sided descent controls](h5-direct-source-pose-construction-20261107/directional-controls.json)
and [four overlap/contact/short-gap/separated controls](h5-direct-source-pose-construction-20261107/clearance-controls.json)
pass. These are local controls, not a global convergence guarantee. Pinned
SciPy 1.17.1 tool hashes and optimizer controls pass. [The complete independent
source/model audit](h5-direct-source-pose-construction-20261107/model-audit-process.json) takes **6.330012 s** and
closes all descendants normally.

## One closed continuous-pose call

The frozen call allows no restart, reseed or extension. It allocates
**8.269466 s** to L-BFGS-B, reserving four seconds for full original validation
within the preparation-inclusive 60/90-second and 2 GiB limits.

[Independent response replay](h5-direct-source-pose-construction-20261107/response-audit.json) verifies all **51
strictly improving points and 64 evaluations**, including 68 parameters and
their gradients. The optimizer stops on time; it does **not** return a
numerical convergence result. The best combined penalty falls from
**83,533.582835 to 55,803.019516 mm²**. [All 12 legal cog rotations](h5-direct-source-pose-construction-20261107/cog-angle-changes.json)
are independently reconstructed from the scaled coordinates.

Full source replay checks **66 originals, 1,632 same-sheet pairs, 264 stock
edges, 90 holes and 10,026 hole vertices**. [The failing source pairs](h5-direct-source-pose-construction-20261107/source-failures.json)
include 29 positive-area intersections and three clearance-only failures.
Every stock edge passes. Summed pairwise areas can double-count; they are
not a union-area or material measure. This remains an invalid candidate.

The optimizer's returned slice is **8.345532 s**, exceeding its allocated slice
by **0.076065 s**. This overrun is preserved. Complete algorithm/shared totals
are **56.273396 / 56.340300 s**, within their original limits, with no overall
algorithm overrun. [All five processes close](h5-direct-source-pose-construction-20261107/closed-search-process.json),
with **92,430,336 bytes** peak committed memory. The separate complete
[response audit](h5-direct-source-pose-construction-20261107/response-audit-process.json) takes **9.805810 s**.

## Explicit budget closure and next work

The consumed candidate lineage now leaves only **3.659700 s**, less than the
required four-second source reserve even before new preparation. It cannot
support another optimization. Continuing this candidate under a reset clock,
or changing only its seed, would violate the closed-call/resource rules.

[The next task](h5-direct-source-pose-construction-20261107/next-step.json) assesses a genuinely broader physical
model: legal discrete bracket/insert orientations alongside continuous cog
rotations. Those 16 originals remain fixed in this closed model. Any new
construction must first establish deterministic original-source initialization,
all legal modes and domains, complete independent readback and a new fully
charged bounded pipeline. Historical candidate transforms, mode choices,
buffers, gradients or initialization must not be hidden in constants or
treated as free data. Pure verified code may be reused. No broader model,
initializer or optimizer call has been prepared or opened.

H2's original gate remains open under the earlier user decision. Full66 source,
native, material, unchanged H5 matrix and production UI/CLI/MCP parity remain
required. [Main 9118d6cb CI](h5-direct-source-pose-construction-20261107/main-ci-at-review.json) has five successful
jobs and a live Windows native job at review. The preceding 0ae08d60 checkpoint
and this checkpoint await the ordinary fast-forward push gate. No live CI run
is cancelled, and no production, README or release change is made.

[Raw evidence](h5-direct-source-pose-construction-20261107/raw-manifest.json) preserves 114
canonical members and 884,312 ZIP bytes.
[Historical references](h5-direct-source-pose-construction-20261107/external-evidence.json) and [source bindings](h5-direct-source-pose-construction-20261107/source-bindings.json)
retain the complete consumed lineage. Independent archive readback passed all 114 canonical members, 99 aliases,
6,161 historical references and 6,191 input bindings across 14 parent archives.
