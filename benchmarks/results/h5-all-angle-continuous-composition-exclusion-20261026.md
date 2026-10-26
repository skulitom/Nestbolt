# H5: all-angle continuous composition exclusion — 2026-10-26

**Four brackets and four cogs cannot fit the current short-sheet target,
even with arbitrary cog rotations, continuous positions and stock enlarged
outward by 0.020 mm. Adding an insert or more parts cannot fix that subset.
For this two-sheet target, the first sheet must contain at least nine brackets
or twelve cogs. Other compositions remain open; H2/H5 remain open at 60%.**

## Rotation-independent geometry and continuous positions

Reconstruct the original 80-vertex, 20-tooth cog from the frozen job. Exact
rational distances to every edge, together with an exact origin winding check,
prove a centered disk of radius **109.115 mm** lies in its filled outer.
The disk is preserved under every real rotation; this uses no angle sample.
Part-in-part remains disabled, so holes do not reduce the occupied filled outer.

Floor each continuous anchor coordinate to the micrometre grid. Its displacement
is less than sqrt(2) micrometres. Reduce the common disk radius by 2 micrometres
to **109.113 mm**, then inscribe a rational 128-gon. Every vertex's squared norm
is checked exactly. The shifted polygon remains inside the original shape at
every rotation and continuous position. Likewise, rebuild all 26 bracket/insert
inner rectangles with **2-micrometre insets**, whose whole-boundary margins
exceed the possible anchor displacement.

A separate exact convex-hull proof checks all 40 hull edges and every original
vertex. Its centered **139.270 mm** disk establishes necessary stock support in
every direction. This larger disk is used only for stock bounds, not collisions.
Relax the original usable stock outward by **0.020 mm** on every side and floor
the resulting necessary anchor bounds. The mapping covers continuous source
positions; the proxy grid does not restrict source positions. Old sampled-angle
stock padding, angle flags and exclusions are not transferred.

For each of ten non-cog profiles against the common cog polygon, and for the
cog pair, construct exact integer-coordinate Minkowski hulls. Independently
verify hull convexity, every hull vertex's provenance and containment of all
**21,505** generated sum points. Prove each complete central forbidden rectangle,
expanded by **0.1 micrometre**, is covered by its hull union using exact rational
polygon subtraction. No sample-only containment inference is used. This yields
necessary left/right disjunctions and a common cog X gap of **215.446 mm**.

## Fresh area and complete model checks

Recompute all area bounds from the rational inner subsets and the new stock
domains. Exact slice integration includes every translated vertex breakpoint
and interior quadratic minimum. A separate edge-integral implementation checks
all **42,525 coefficients**, **675 complete vertical cells**, and **63 bands**.
No finite-angle coefficient is reused. Disjoint mapped inner subsets obey
these band capacities, so the inequalities remain necessary for original
continuous placements.

The nine-original model has **1,768 variables / 2,374 constraints**. It retains
all eight bracket choices independently, both insert profiles, the common cog
proxy, complete stock and cell constraints, necessary side/order bounds, and
98 optional inner rectangles. The audit reconstructs every field, checks
106,596 physical cell-band coefficients, verifies copy/profile relabelling and
round-trips the model through the actual solver importer.

Its sole 20-second, four-worker, seed-0 call returns **INFEASIBLE** after
**3.816914 solver / 4.592091 shared seconds**.
The declared 30-second shared limit is honored without a soft overrun.

Removing the insert from the short-sheet inventory is a distinct composition;
insert37 remains mandatory on the first sheet alongside brackets28/29. The
eight-original model contains **1,424 variables / 2,008 constraints**, including
96 optional inner rectangles. Every field and import is independently checked.
Its sole call also returns **INFEASIBLE**, after
**3.932667 solver / 4.690825 shared seconds**,
again within its 20/30-second limits. Both calls are closed and independently
read back; neither is retried, reseeded or extended.

## Consequence for the complete job

The job defines identical copies within each family. Any valid larger short-sheet
arrangement containing at least four brackets and four cogs would contain a valid
eight-part subset, contradicting the necessary-model result. Therefore:

**Short sheet: brackets <= 3 OR cogs <= 3.**

With all 12 brackets and 15 cogs required in this two-sheet target, the equivalent
first-sheet condition is **brackets >= 9 OR cogs >= 12**. This does not claim the
surviving compositions fit, or exclude another sheet/material target.

The checked first-sheet partial contains **55 originals**: 18 frames, six
brackets, 20 inserts and 11 cogs. All **11** remaining originals are still
mandatory: **21/22/25/26/28/29/37/53/63/64/65** (six brackets, one insert, four cogs).
Thus continuing that partial requires adding at least three brackets or one cog
to the first sheet. Exact enumeration covers all **70** remaining family-count
allocations; the new subset cut excludes **six**, leaving **64 unproved**.
Every one of the 66 identities is accounted for exactly once.

Next prepare a complete necessary composition selector over these remaining
originals. A part unselected for the short sheet must remain an explicit
first-sheet obligation. Audit presence-conditional geometry and any new area
bound before another bounded call. A selected composition still needs actual
original geometry on both sheets, complete native/material validation,
production integration within 60 seconds and the full H5 matrix.

## Repository and evidence

At **2026-10-26T09:36:31.860151+00:00**, local HEAD and main are **6246967c**. The previous two
checkpoints were pushed normally after all six checks on 7271cc8b passed.
[Current CI40298314725](https://github.com/skulitom/Nestbolt/actions/runs/40298314725)
has five successful jobs and Windows checks remain live. Queue this checkpoint
until the existing run completes successfully; do not cancel it with a push.
Production, READMEs, upstream stop-rule state and all 22 reserved H2 vectors
remain unchanged. H2 retains its original gate and no new release is qualified.

All **seven audits pass**. [Checks](h5-all-angle-continuous-composition-exclusion-20261026/checks.json),
[closed calls](h5-all-angle-continuous-composition-exclusion-20261026/closed-calls.json), [scope](h5-all-angle-continuous-composition-exclusion-20261026/scope.json),
[composition cut](h5-all-angle-continuous-composition-exclusion-20261026/composition-cut.json), [next step](h5-all-angle-continuous-composition-exclusion-20261026/next-step.json),
[raw manifest](h5-all-angle-continuous-composition-exclusion-20261026/raw-manifest.json). All 139
canonical files and 112 aliases are byte/SHA-256/CRC
verified across 1 archive parts.
