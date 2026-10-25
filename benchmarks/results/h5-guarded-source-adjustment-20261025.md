# H5: corrected source clearances and original-outline regions — 2026-10-25

**The 57-original starting arrangement now clears the unchanged native
conservative distance and stock guards in independent geometry checks.** Fifteen
parts move by at most **0.023 mm per axis**. Complete clearance regions for all
nine remaining mandatory originals are built from their actual outlines,
including every cog tooth. No full 66-part target layout is claimed; H2/H5 remain
open at **60%** completed milestone weight.

## Small, bounded source adjustment

Every source part keeps its original shape, copy, orientation and sheet. Axis
offsets are bounded to ±0.05 mm on a 0.0001 mm grid. Stock bounds round inward
and require 0.0125 mm beyond the original stock clearances. The pair-gap target
is 0.2125 mm, above the native conservative 0.211708672510 mm requirement.

All **1,246** same-sheet pairs are examined. For 92 near pairs, all **60,404**
boundary-segment pairs are checked, producing **467** projection constraints.
Integer normals, exact rational segment projections and ceiling bounds preserve
the intended gap. These constraints propose a candidate; the subsequent full
original-geometry audit decides whether it is usable.

Preparation takes **0.253857 seconds** and its independent audit
**0.219100 seconds**. A separate protobuf oracle checks every variable,
constraint, objective and parameter in the **228-variable/695-constraint** model.
One declared 10-second, eight-worker, seed-zero call returns **OPTIMAL in
0.027011 seconds**, minimizing the total absolute axis translation
on this bounded grid. All three incumbent records are preserved.

The final total absolute axis translation is **0.2563 mm** across 15 parts:
one frame, five brackets and nine inserts. No cog changes position. The maximum
single-axis change is **0.023 mm**, below the declared 0.05 mm limit.

## Independent full-original checks

Every adjusted polygon is reconstructed from the source job and new transform,
with maximum disagreement of **5.68e-14 mm**
against an independent translation of the original polygon. All identities,
orientations, mirror flags, sheets and area charges remain unchanged.

All **1,246 original pairs** have zero intersection area and meet the requested
gap. The minimum gap is **0.212500000000 mm**, exceeding the
native conservative distance by **0.000791327490 mm**.
All **228 stock-edge checks** pass: the minimum extra margin is
**0.012500000000 mm**, exceeding the conversion guard
by **0.001055908203 mm**. All nine prior pair
shortfalls and all four prior stock shortfalls are resolved.

The preserved partial layout still contains only 57 originals. Its independent
geometry checks do not claim a native full-job validation or a completed target.
The other nine originals remain mandatory, so final counts stay 18 frames,
12 brackets, 21 inserts and 15 cogs. Fixed-original area charges remain
3,831,901,744 / 249,662,718 units across the sheets (1,000 units/mm²).

## Complete full-original clearance regions

All ten moving profiles use actual outer polygons. Both brackets retain every
recorded orientation, the insert remains vertical, and all six cogs use their
known source angle with all **80 original vertices** preserved. This finite
construction inventory does not exhaust all possible cog angles.

All **100** fixed-style/moving-profile collision obstacles are rebuilt. Each
zero-clearance Minkowski obstacle receives an explicit circumscribed 128-gon
clearance envelope, assembled from boundary-segment sums rather than a rounded
buffer substitute. The nominal envelope support is 0.2126 mm; exact rational
halfplane checks certify that it contains the required 0.2125 mm disk.

Each of the **20** mode/sheet queries starts from inward 1-micrometre anchor
bounds with 0.0125 mm extra stock margin, and subtracts every applicable adjusted
fixed-original obstacle. Whole free geometries are retained with **no outward
padding or sampled pose list**. All queries are nonempty. Construction takes
**1.788203 seconds**, with no pending cases or caps and
**4,861** output vertices.

The independent audit takes **9.834698 seconds**. It reconstructs raw
obstacles from **11,872 unmerged triangle-pair hulls**, then checks positive
clearance using a different decomposition: **2,491 raw-obstacle triangles**
Minkowski-summed with the complete envelope. It verifies all 128 rational support
lines and 16,384 convexity checks. Maximum raw/expanded obstacle disagreement is
**1.48e-10 / 5.55e-11 mm**;
maximum free-region disagreement is **2.27e-13 mm**.
Every whole-stock partition is checked against all applicable fixed originals.

Next, construct full-original mutual collision conditions and a joint model for
all nine mandatory moving parts. Allowed-region rounding must stay conservative
inward for this constructive search; the older outward necessary-relaxation
rounding is not a substitute. Every resulting 66-part candidate still needs
original-pair/stock checks, native validation, production-budget implementation
and the full 13-job/two-kerf H5 matrix. Previous completed solver calls stay closed.

## Repository and evidence

Main **51fe56c0** contains the six previously pushed checkpoints and has no new
remote commits after this checkpoint's fetch. [CI 40237436741](https://github.com/skulitom/Nestbolt/actions/runs/40237436741) is
**in_progress**, with **5/6** jobs successful in the saved snapshot.
Production source, all three accurate READMEs and release versions remain
unchanged. There is no held-out evaluation, full-job native acceptance or release.

Evidence: [source changes](h5-guarded-source-adjustment-20261025/changes.json),
[original-geometry audit](h5-guarded-source-adjustment-20261025/original-geometry-audit.json),
[model audit](h5-guarded-source-adjustment-20261025/model-audit.json), [bounded result](h5-guarded-source-adjustment-20261025/solver-result.json),
[original-region audit](h5-guarded-source-adjustment-20261025/original-region-audit.json),
[query summary](h5-guarded-source-adjustment-20261025/original-query-summary.json),
[raw archive](h5-guarded-source-adjustment-20261025/raw-001.zip) and [manifest](h5-guarded-source-adjustment-20261025/raw-manifest.json).
All **182** canonical members and
**153** identical-content aliases retain exact bytes
with CRC/SHA-256 verification, including all source transforms, proposals,
pair/stock checks, full-original obstacles, free regions and executed helpers.
