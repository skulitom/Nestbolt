# Cog halfplane search and exact source capacity — 2026-11-07

The smaller support-halfplane model completes its sole call **UNKNOWN**, with
no incumbent or placement. It stays within the overall 60/90-second and 2 GiB
limits. The call is closed. New exact source-contained rectangles now support
global packing constraints for a distinct model; that model has not been built.
Four fixed arrangements and all 440 whole allocations remain. H2/H5 stay open
at **60% completed milestone weight**.

## Complete model and independently read response

[Full serialized-model readback](h5-cog-halfplane-search-and-capacity-20261107/model-audit.json) verifies all **28,254
variables and 58,169 constraints**, binary/text equality and an actual solver
import. All 28 movers, twelve independently positioned cogs, 108 source modes,
258 cog interactions and 120 orthogonal-owner interactions remain. Every typed
halfplane uses its certified lower bound and every pocket its upper-bound planes.
The 5,646-value partial cog hint satisfies all 221 fully hinted active constraints;
it does not place the sixteen orthogonal companions.

[Complete preparation](h5-cog-halfplane-search-and-capacity-20261107/closed-model-preparation-charges.json) totals
**6.504612 seconds**, including the 2.573594-second complete new model build.
[The response audit](h5-cog-halfplane-search-and-capacity-20261107/response-audit.json) verifies one four-worker,
seed-zero call: 48.670477 seconds allocated, 50.188645 seconds returned,
165,457 branches and 490 conflicts. **The 1.518168-second solve-slice overrun
is preserved**. Preparation-inclusive algorithm/shared totals are
**57.533015 / 57.630837 seconds**, below the original 60/90-second limits.

[The Windows Job record](h5-cog-halfplane-search-and-capacity-20261107/closed-search-process.json) closes all three
processes with zero active descendants. Peak aggregate committed memory is
**2,102,865,920 bytes**, below 2,147,483,648. Unlike the preceding model's
memory stop, this call returns an actual response protobuf. Its status is
UNKNOWN, with no assignment, incumbent, source checker or native call.
It proves no continuous or whole-allocation exclusion and will not be repeated,
reseeded or extended. The raw LP diagnostics are preserved in the archive.

## New global necessary occupancy constraints

[The fresh preparation](h5-cog-halfplane-search-and-capacity-20261107/capacity-preparation.json) retains all **13
source modes and 108 per-original mode options**. Each transformed L bracket
contributes two inset component rectangles; each insert contributes one.
For the 7-degree cog, 32 horizontal bands use every source vertex-height section
and both band edges. All common intervals are rounded inward on the 0.01 mm grid.
The resulting cog rectangles cover **90.562604%** of its filled outer area.
Holes remain part of the final source geometry; filled outer occupancy is used
because common-line part-in-hole remains disabled.

[Independent exact readback](h5-cog-halfplane-search-and-capacity-20261107/capacity-source-audit.json) verifies
**101 rectangle-containment proofs and 5,104 source edge/box checks** using
rational values of the original vertices and actual affine coefficients.
For each rectangle, its center is inside the source outer and no source boundary
edge enters its open interior. Each mode's rectangles have disjoint interiors.
These checks cover 80 profile rectangles and 21 separate coarse rectangles.

The auditor independently partitions both projection axes at every source and
profile endpoint, checking **230 elementary slabs** and exact area conservation.
Expanding over every owner/mode gives **1,564 X-axis and 552 Y-axis profile
intervals**. The [outward-rounded stock](h5-cog-halfplane-search-and-capacity-20261107/capacity-stock.json) permits
capacities 88,561 and 148,696 grid units respectively. Every rectangle stays
inside it at every source-mode domain extreme.

A separate coarse system has **172 optional rectangles**, with 36 active under
any full mode selection: 24 orthogonal components and twelve source-contained
cog squares. Each rectangle's two intervals must share the original mode
selector and translate rigidly with the original coordinates. This permits a
global NoOverlap2D constraint alongside the two cumulative profiles.
No count-capacity table, detached strip coordinate or omitted part is allowed.

[Both preparation and audit processes close successfully](h5-cog-halfplane-search-and-capacity-20261107/capacity-process.json).
The complete new preparation takes **0.315775 seconds**; the separate complete
audit takes 2.133900 seconds. The current closed models/searches are absent from
the capacity geometry's input graph. Historical source provenance is retained.

## Next complete construction

[The next model specification](h5-cog-halfplane-search-and-capacity-20261107/next-step.json) adds these globally
coupled necessary constraints while preserving all full pair halfplanes/pockets,
original modes, rigid component geometry and valid identical-copy ordering.
The [complete source-preparation ledger](h5-cog-halfplane-search-and-capacity-20261107/next-preparation-charges.json)
is **4.246794 seconds before the new model build**, which must also be charged.
Every protobuf field and all capacity/rectangle assignments require independent
readback before one newly frozen call under the same limits.

No new complete model or search opens in this checkpoint. A source-valid 66-part
layout, native/material validation, production integration and the unchanged
complete H5 matrix remain required. H2 retains its original gate and unopened
reserved vectors. Production, READMEs and release assets remain unchanged.
[Main CI at review](h5-cog-halfplane-search-and-capacity-20261107/main-ci-at-review.json) is preserved; no live run is
cancelled. A normal push waits for all six jobs and aggregate success.

[The archive](h5-cog-halfplane-search-and-capacity-20261107/raw-manifest.json) contains 68
canonical members and 2,873,883 ZIP bytes.
[Historical references](h5-cog-halfplane-search-and-capacity-20261107/external-evidence.json) and
[source bindings](h5-cog-halfplane-search-and-capacity-20261107/source-bindings.json) preserve all consumed evidence.
Independent archive verification is required before commit.
