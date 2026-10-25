# H5: nine-part conflict-owner neighborhood — 2026-10-25

**The broader search finds all 66 required parts in its necessary geometric
model, but the original-outline trial fails.** Independent checks identify five
cog-pair conflicts that no angle can repair at the selected anchors. Stronger
whole-circle and sheet-boundary conditions are now certified for the next model.
H2/H5 remain open at **60%** completed milestone weight.

## Fresh complete geometry

The released originals are items **50, 54, 57, 58, 62, 64 and 65**: one vertical
insert and six cogs. With both missing brackets, the model moves nine mandatory
parts and preserves 57 original source transforms. Counts remain 18 frames,
12 brackets, 21 inserts and 15 cogs. Every allowed orientation and sheet from
the recorded source inventory remains available.

All **20 mode/sheet queries** start from full original stock anchor bounds.
None uses the earlier two-core free cells. The construction reuses 100 immutable
collision-cache entries and adds 10 for the vertical insert. Only strict
interior collision regions are excluded. Complete free regions, including
boundary cases, receive outward padding before complete convex decomposition
and rational outward inequality rounding.

Construction takes **1.200935 seconds**, producing **199 convex
domains** without pending work or caps. Independent verification takes
**1.042923 seconds** and checks:

- 112 inputs against committed evidence, all 57 fixed transforms and all counts.
- 16 exact insert floor-error corner tests and 106 independently built triangle
  collision hulls for its 10 new cache entries.
- Whole-stock coverage for every query, **3,638 outward halfplanes** and
  **82,650 rational vertex tests**.
- All seven released source poses, and **361 exact component Minkowski hulls**
  with all **2,032 facets** represented by the 20-normal separation basis.

The minimum new exclusion margin is 0.000995184727 mm;
the nominal 0.001 mm erosion is not claimed as its exact realized margin.

## One bounded search and a rejected original trial

The joint model contains **1,871 variables and 10,774 constraints**: 46 mode
choices, 482 complete per-part domain choices, 8,283 reified halfplanes,
36 physical pairs and 53 convex-component pairs. All 1,060 exact projection
separation choices are present. Original area charges and original outward
stock bounds remain. There is no objective, hint, copy ordering or optional
original part. A separate protobuf oracle checks every variable, constraint
and solver parameter before search.

One declared 60-second, eight-worker, seed-zero call returns **OPTIMAL in
1.133719 seconds**, with an incumbent at
1.082739 seconds. Here OPTIMAL means a feasible
necessary-model arrangement; there is no packing objective. The completed call
is not retried or extended.

An independent solution audit verifies all 66 copies, nine selected domains,
25 same-sheet moving-component separations and original area charges of
**4,091,952,616 / 389,788,154** units across the two sheets (1,000 units/mm²).
The outward fixed-obstacle relaxation permits two tiny proxy intersections;
these are recorded explicitly, not described as physical feasibility.

The full original-outline trial preserves all 57 fixed transforms, uses the
selected bracket/insert orientations and each restored cog's source angle.
Checking all **1,585 original pairs** finds **17 clearance failures** and
**three stock-boundary failures**. Its three largest stock overruns are about
28.97, 30.87 and 23.12 mm. The rejected file and every failure remain preserved.
It is not sent to native packing as an accepted candidate.

## Stronger cog conditions, independently certified

The original cog contains a disk of radius **109.1157 mm** at every angle.
A whole circle of radius **109.1 mm** about its floored center remains inside
that disk for every floor error: in 0.0001 mm units,
`(1091157 − 1091000)² > 2 × 100²`. Exact circle distances reject three selected
moving-cog pairs; rational point-to-original distances reject two further
moving-cog/fixed-original pairs. These account for all five robust conflicts.

Separately, the original's convex hull has **40 vertices**. All 3,200 original
point/halfplane checks establish a centered hull disk with radius
**139.2707 mm**. This supplies a necessary minimum stock-boundary support at
every angle. It is used **only for sheet boundaries**, never as a filled
collision proxy for the concave cog.

The stronger stock-center bounds are `[14576, 14576, 135424, 285424]` and
`[14576, 14576, 135424, 18017]` in 0.01 mm units. They preserve **all 15 known
valid source cog centers** and reject all three out-of-bounds selected cog
anchors at every angle. Preparation and independent verification take
0.119874 and
0.121689 seconds respectively. No further solver call occurs in
this checkpoint.

Next, strengthen the nine-part model using these certified conditions while
preserving its complete original counts, material cap and allowed modes. Any
linear approximation of the whole circle must be identified and audited as
such. A positive still needs actual original outlines and angles, clearance
and native guards, the production budget and the full 13-job/two-kerf matrix.
Neither this rejected trial nor a conditional negative proves unrestricted
packing impossibility.

## Repository and evidence

The previous six checkpoints were normally pushed to main **51fe56c0**, and
the remote head was verified. New [CI 40237436741](https://github.com/skulitom/Nestbolt/actions/runs/40237436741) is
**in_progress**, with **2/6** jobs successful in the saved snapshot.
Its status is separate from the older six-job successful run. Production source,
all three accurate READMEs and release versions remain unchanged. There is no
held-out evaluation, full quality rerun, native acceptance or new release.

Evidence: [domain audit](h5-conflict-owner-neighborhood-20261025/domain-audit.json),
[model audit](h5-conflict-owner-neighborhood-20261025/model-audit.json), [bounded result](h5-conflict-owner-neighborhood-20261025/solver-result.json),
[solution audit](h5-conflict-owner-neighborhood-20261025/solution-audit.json),
[stronger certificate](h5-conflict-owner-neighborhood-20261025/stronger-cog-certificate.json),
[independent certificate audit](h5-conflict-owner-neighborhood-20261025/stronger-cog-audit.json),
[push receipt](h5-conflict-owner-neighborhood-20261025/main-push-receipt.json),
[raw archive](h5-conflict-owner-neighborhood-20261025/raw-001.zip) and [manifest](h5-conflict-owner-neighborhood-20261025/raw-manifest.json).
All **214** canonical members and
**60** identical-content aliases retain exact bytes
with CRC/SHA-256 verification, including all domains, model/log, rejected trial,
source inputs, certificates and executed helpers.
