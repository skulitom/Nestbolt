# H5: geometry for variable two-sheet allocations — 2026-10-26

**The next model can vary the short-sheet composition while retaining all 66
originals and every real cog rotation.** Its source geometry and allocation
domains are now independently verified. No allocation-aware solver has opened
and no complete layout or exclusion is claimed. H2/H5 remain open at 60%.

## Removing the fixed short-sheet assumption

The prepared geometry retains **all 454 necessary surviving count vectors** from
the earlier full short-sheet frontier, not just its 32 Pareto vectors. Each
vector carries the exact complementary first-sheet counts. Restricting to the
Pareto vectors would not be justified by source feasibility, so no such
restriction is introduced. All 18 frames remain on the first sheet because
their minimum allowed height is 350 mm, greater than the short sheet.

Thirteen geometry variants cover all eight bracket quarter-turn/mirror modes,
both rectangular frame and insert footprints, and one cog proxy valid at every
real rotation. Half-turns of the rectangular filled outers are geometrically
equivalent; their holes remain reserved. There are 26 variant/sheet domains,
24 of them allowed. The two excluded domains are the short-sheet frame modes.

The non-cog rectangles retain two-micrometre insets to absorb coordinate
flooring. An independent reader transforms original source rings with exact
quarter turns, proves their grid-cell containment after expanding each rectangle
by one micrometre, and checks component disjointness. It verifies all 28
non-cog rectangles and every legal outline orientation.

## Two different cog bounds

The previously audited all-angle source proof supplies a **109.113 mm**
quantization-safe inscribed disk. A 153 mm coarse square and 16 horizontal strips
lie inside that disk for every rotation. The strips occupy **33,830.014276 mm²**.
These source-contained shapes may participate in necessary collision/capacity
constraints with all other part families.

A different bound comes from the independently certified **254.297 mm minimum
separation of rounded cog centers**, valid for every pair of real rotations.
Disks of radius **127.148 mm** about those centers therefore cannot overlap one
another. Their 16 inner strips occupy **45,936.033464 mm²**. These larger disks
are **not source-contained**: they may constrain cog-to-cog capacity only and
must never be used as mixed-family collision shapes.

The all-angle stock support radius is 139.270 mm, larger than the virtual disk
radius, so these virtual disks remain inside the relaxed stock for every allowed
center. The new audit checks 132 exact integer disk corners, the center-distance
inequality, all eight virtual-disk stock edges and all 104 domain endpoints.

## Necessary relaxation and acceptance remain separate

The original source short top remains **319.4269023299994 mm**. The mathematical
necessary bounds use the existing outward top **319.42699 mm** and an additional
0.020 mm outward stock relaxation for quantization. These relaxations cannot be
used to accept a layout, enlarge the material target or bypass native guards.

The geometry audit verifies all 66 unique original identities, all 454 count
vectors and their complements, all mode/stock domains and the separate uses of
the source and virtual cog disks. A future positive necessary assignment still
needs actual cog angles, full original-ring readback and native/material checks.
The current work contains **zero solver calls and zero native calls**.

The concrete next model can give each original exactly one sheet/mode option,
with optional source rectangles, source-capacity strips and a separate cog-only
virtual-capacity system. All count choices must remain linked to those options.
The serialized model must be independently checked before a bounded solve.
All prior fixed-allocation calls remain closed and are not extended or reseeded.

## Repository and evidence

At 2026-10-26T20:32:21.877375+00:00, [main ff5036af checks](https://github.com/skulitom/Nestbolt/actions/runs/40393931732):
4 of six checks pass; preserve the remaining live checks before the next push. The preceding 09091745 checkpoint remains queued locally. Production,
READMEs and upstream heads/releases are unchanged. All 22 reserved H2 vectors
remain unopened, and no new release is qualified.

[Checks](h5-allocation-aware-geometry-20261026/checks.json), [independent geometry](h5-allocation-aware-geometry-20261026/geometry-checks.json),
[variants](h5-allocation-aware-geometry-20261026/variants.json), [stock domains](h5-allocation-aware-geometry-20261026/domains.json),
[all allocations](h5-allocation-aware-geometry-20261026/allowed-allocations.json), [scope](h5-allocation-aware-geometry-20261026/scope.json),
[next step](h5-allocation-aware-geometry-20261026/next-step.json) and [raw manifest](h5-allocation-aware-geometry-20261026/raw-manifest.json).
The archive verifies 24 canonical files and
2 identical-content aliases by bytes, SHA-256 and CRC.
