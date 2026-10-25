# H5: stronger two-core relocation exclusion — 2026-10-25

**The stronger joint model returns INFEASIBLE for all 207 remaining two-core
cases and 286 sheet allocations.** With the earlier 299 area exclusions and
22 empty-role exclusions, all **528 recorded two-core neighborhoods** are now
closed. This is conditional on the source poses and finite orientation
inventory; it does not prove unrestricted packing impossibility. H2/H5 remain
open at **60%** completed milestone weight.

## Complete convex domains

All eligible modes of the 207 cases produce **2,206 queries**. The domain
source is the previously audited outward region cover, including all original
grid anchors and boundary cases. Each positive-area component is triangulated;
only convex adjacent unions are merged, with every unmerged face retained.
Each face expands by a 0.001 mm square, and the complete expanded union must
cover the whole input region. This is a necessary outer cover, not accepted
cutting geometry. No extra floor-anchor shift or sampled pose set is introduced.

The first phase writes 40 complete query outputs, then an empty input region
triggers a guard failure: GEOS `covers(empty, empty)` returns false even though
empty-set coverage is vacuously satisfied. The failure and original code are
preserved. Its observed plan-to-failure interval is
**0.706075 seconds**. Recovery charges 60
seconds to that phase and uses at most the remaining 60 seconds of the original
120-second budget. It reuses all 40 query files and the support atlas byte for
byte, changes only the empty-region guard, and computes 2,166 unfinished queries.

The recovered phase completes in **25.216528 seconds**, with
**32,626 convex domains**, no pending queries and no domain, merge or time cap.
Each normalized rational edge is rounded at coefficient scale 10⁷. The exact
worst-case coefficient error over the complete coordinate range is added,
plus one unit, before ceiling the upper bound. Integer bounding intervals also
round outward. This preserves every source integer anchor.

Independent verification takes **24.394219 seconds**. It checks
all **165,640 outward halfplanes** with **960,962 exact rational vertex tests**,
complete whole-region coverage, all 2,206 source-cover hashes against committed
evidence, six other source matches and **398** original source-pose integer
memberships. Three selected false anchors remain rejected after rounding.

## Exact stronger collision conditions

The moving cog uses the complete floor-safe 16-gon, already proved inside every
rotated original cog across all coordinate-floor errors. Brackets retain two
coupled rectangle components and restored horizontal frames one rectangle.
An exact integer support atlas contains **18 convex component types** and
**20 common edge normals**. An independent integer monotone-chain oracle
reconstructs all **324 ordered component Minkowski hulls**, verifies all support
values, and confirms all **1,852 hull facets** use normals in that basis.

Coordinates use 0.01 mm units and shape vertices 0.0001 mm units. For every
cross-part convex-component pair on the same sheet, some normal must satisfy
`100 × n·(anchorB − anchorA) ≥ supportA(n) + supportB(−n)`.
Every term is integer, so no projection rounding is needed. Touching is allowed
in this necessary diagnostic. Both bracket arms share the same part position
and mode; no same-part separation is imposed. The old five-rectangle cog check
is not used as a substitute for the stronger polygon.

## Fully audited bounded search

One model retains all 207 cases and 286 allocations, with 62 original source
poses fixed per selected case and four movable parts mandatory. It contains:

| Model element | Count |
| --- | ---: |
| Variables / constraints | 56,046 / 356,662 |
| Role/mode choices | 3,958 |
| Complete per-part convex-domain choices | 51,197 |
| Reified outward domain halfplanes | 248,866 |
| Physical part pairs / component pairs | 6 / 13 |
| Exact projection separation choices | 260 |
| Component support variables | 120 |

Original area charges and sheet-allocation links remain. There are no optional
original parts, objectives, hints or copy-order restrictions. Construction takes
**4.140012 seconds** and a separate protobuf oracle
reconstructs every variable, constraint, support value, sheet-XOR truth table
and solver parameter in **1.964401 seconds**.

One declared 60-second, eight-worker, seed-zero call starts search at 4.70
seconds and records `#Done 20.57s no_lp`. It returns **INFEASIBLE in
20.878256 seconds**, with 29,266 branches, 7,458 conflicts and no
incumbent. The solver reports `LRAT_status: NA`; no separate formal LRAT proof
is claimed. The completed call is neither retried nor extended.

## Broader construction prepared from actual conflicts

The previous false arrangement moved cogs 58 and 65. Its certified fixed-owner
collision list contains items **50, 54, 57, 62 and 64**. The next census releases
all of them together: one vertical insert (class 13, modes 22/23) and six cogs,
plus both mandatory missing brackets. That gives **57 fixed originals + 9
mandatory movable originals = 66**, with no deletion or partial-count objective.
All source orientations and permitted sheets are recorded. This is preparation,
not a search or feasibility claim. Fresh domains must start at the full original
stock bounds; the narrower two-core domains must not restrict the larger move.

Before searching this broader neighborhood, independently certify the moving
insert proxy and its new collision-cache entries against fixed originals, while
reusing immutable existing caches. Build complete domains under a declared budget
and audit their coverage and exact mutual convex-component separation. Preserve
original area charges, the material cap, the finite source orientation inventory
and cog containment at every angle. Completed searches must not be retried or
extended.

A positive result would still need actual cog outlines and angles, original
clearance and native guards, the production budget, and all 13 jobs at both kerfs.
H2 stays open, with no further held-out access or new release at this checkpoint.

## Repository and evidence

All six jobs in main 247e823a's existing **CI40233299884** now pass. The snapshot
is terminal success, not a restarted run or inferred pass. The accumulated
checkpoints are ready for the next authorized normal push after this evidence
is committed. This source checkpoint starts at 8528180d; a new post-push run
must be tracked separately. Production source, all three accurate READMEs and
release versions remain unchanged. No native packing, quality matrix, held-out
evaluation or new release occurs; H5 is not qualified by this diagnostic.

Evidence: [domain plan](h5-strong-pair-relocation-exclusion-20261025/domain-plan.json), [domain audit](h5-strong-pair-relocation-exclusion-20261025/domain-audit.json),
[support atlas](h5-strong-pair-relocation-exclusion-20261025/support-atlas.json), [full model audit](h5-strong-pair-relocation-exclusion-20261025/model-audit.json),
[bounded result](h5-strong-pair-relocation-exclusion-20261025/solver-result.json), [next neighborhood](h5-strong-pair-relocation-exclusion-20261025/next-neighborhood.json),
[completed main CI](h5-strong-pair-relocation-exclusion-20261025/completed-main-ci.json), [raw archive](h5-strong-pair-relocation-exclusion-20261025/raw-001.zip)
and [manifest](h5-strong-pair-relocation-exclusion-20261025/raw-manifest.json). All **4666**
canonical members and **58** identical-content aliases
retain exact bytes with CRC/SHA-256 checks, including the initial guard failure,
all domains/rounding data, full model/log, source inputs and executed helpers.
