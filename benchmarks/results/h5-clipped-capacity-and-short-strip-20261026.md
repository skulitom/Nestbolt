# H5: clipped cell capacity and a different short-strip allocation — 2026-10-26

**Exact clipping proves 139 additional conflicts between cog regions, but the
stronger necessary model still closes UNKNOWN.** A separate attempt to place
another insert beside the short-sheet cog finds no candidate in its declared
finite queries. Neither result closes H5. H2/H5 remain open at 60%.

## Exact occupancy footprints

The preceding model retained each whole cell unless a single proof excluded it
entirely. This model instead subtracts every certified oblique-support and
required-clearance support box from each surviving integer cell. It preserves
the prior 66 whole-cell exclusions and all potentially valid floor-rounded
centers, including integer endpoints. The 1,794 boxes change 93 nonempty cell
footprints; none becomes empty. The remaining 1,045 cells contain 1,067 lattice
rectangles. Their convex hulls are outer relaxations, not source poses.

Independent atomic partitioning checks **1,313 integer regions** and exact
retained/removed lattice counts. It verifies **4,268 corners** against their
convex hulls. For every cell pair, the farthest hull vertices bound the greatest
possible center separation. The audit checks **545,490 cell pairs and 8,782,205
vertex pairs**, proving **139 additional conflicts** while preserving every old
edge among retained cells. All **112,596 conflicts** are covered by **1,746
verified cliques**, with no residual edges.

Any original fifteen-cog layout must select fifteen distinct compatible cells:
each cell's diameter is below the certified 254.297 mm rounded separation, and
the new exclusions preserve every source-feasible center at every angle. The
two inserts remain mandatory for a full layout and are omitted only from this
necessary test. The model cannot establish source feasibility from a positive.

## Single closed model call

The complete **1,045-variable, 1,747-constraint** model is independently
reconstructed from the inventory and exact graph, without objectives or hints.
It closes **UNKNOWN** after actual search in **20.044475 returned-call seconds**
and **21.306630 shared-process seconds**. The internal solver time is
20.037539 seconds. Internal/returned soft overruns of 0.037539/0.044475 seconds
are preserved; the 30-second shared limit is honored. There is no retry,
reseed or extension. The returned worker records 12,561 branches and
378 conflicts; separate worker counters remain in the raw evidence. No
selection, source layout, neighborhood exclusion or formal unsat proof exists.

## Different short-sheet allocation

The known six-bracket/five-insert/cog short strip has one compact bracket pair.
The new construction widens that pair to hold an insert, then proposes three
more inserts in a stack at the right stock edge. A successful cog placement
would make **six brackets, six inserts and one cog**, moving insert38 from the
main sheet. Four stack variants use left/right alignment and vertical reflection.
The target stock height and all original quantities and clearances stay fixed.

Independent direct-vertex readback validates all twelve fixed originals in each
variant: **264 pair checks, 192 stock edges, 96 cutouts and 11,712 hole vertices**
across the four variants. Minimum gap is 0.225 mm and extra stock margin 0.025 mm.
The bracket/insert block retains the source-checked nine-part construction.

The finite proposal procedure queries 36 actual half-degree angles from 0 to
17.5 degrees against each of the four variants, with no exact rotational-symmetry
assumption. All **144 conservative free-translation regions are empty**, producing
no proposals or thirteen-part candidate in **36.235296 seconds**, within the
declared 60-second generation allowance. No solver is opened. The audit reads
back all saved queries and verifies their provenance; it does **not** independently
recompute the conservative region helper. These records show no candidate from
this procedure, not an independent impossibility proof or all-angle exclusion.

## Remaining work and repository state

All four audits pass. Both attempts are closed. A materially changed next model
should jointly include both remaining inserts with the cog geometry, or move the
frame/bracket core; these calls may not be resumed. Preserve the existing
short12/partial64 and short15 alternatives. Full66 original source/native/material
validation, production integration within 60 seconds and the complete H5 matrix
remain required.

At 2026-10-26T16:48:34.874344+00:00, main is cb7f7b1f and its
[CI40359411459](https://github.com/skulitom/Nestbolt/actions/runs/40359411459)
is checked. 4 of six jobs pass; the run is in_progress. Queue this checkpoint until all six pass, preserving the running checks.
Production and READMEs remain unchanged. Upstream state is referenced to the
preceding recorded review; it was not rechecked during this seal. H2 retains
its original gate and all 22 reserved vectors remain untouched. No new release
is qualified.

[Checks](h5-clipped-capacity-and-short-strip-20261026/checks.json), [geometry](h5-clipped-capacity-and-short-strip-20261026/clipped-geometry-checks.json),
[necessity proof](h5-clipped-capacity-and-short-strip-20261026/clipped-necessity-proof.json),
[new edges](h5-clipped-capacity-and-short-strip-20261026/139-new-edge-certificates.json),
[model](h5-clipped-capacity-and-short-strip-20261026/clipped-model-checks.json),
[response](h5-clipped-capacity-and-short-strip-20261026/clipped-response-checks.json),
[short source/readback](h5-clipped-capacity-and-short-strip-20261026/short-source-readback-checks.json),
[scope](h5-clipped-capacity-and-short-strip-20261026/scope.json), [next step](h5-clipped-capacity-and-short-strip-20261026/next-step.json),
and [raw manifest](h5-clipped-capacity-and-short-strip-20261026/raw-manifest.json).
The archive verifies 213 canonical files and
22 aliases by bytes, SHA-256 and CRC.
