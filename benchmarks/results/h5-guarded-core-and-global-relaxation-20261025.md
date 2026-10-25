# H5: guarded-core exclusion and all-parts-movable relaxation — 2026-10-25

**The guarded alternative cannot complete the inventory while its 33 frame/cog
placements stay fixed, within the audited outer geometry model. A new model
allowing all 66 parts to move is unresolved.** Neither result completes H5.
H2/H5 remain open at **60%** completed milestone weight.

## Guarded alternative: complete continuous regions

The preceding checkpoint moved one cog in saved core 5 by
(+0.0125, -0.0125) mm and independently checked all original fixed-part distances
and stock margins. Here all 24 zero-clearance forbidden unions and translation
regions are rebuilt for that changed arrangement. Only 36 hash-bound **local**
Minkowski obstacles are reused; their global translations and complete unions
are recomputed. All 12 permitted small-part orientation/reflection cases and
both original stock domains remain, including continuous unsampled positions.

Construction finishes in 1.075203 seconds within its declared 120 seconds,
with no pending queries. The independent 7.389211-second audit checks:

- 73 input/template/cache matches against committed manifests;
- 36 local obstacles from 860 convex-piece vertex sums and all 12 translated
  obstacles for the moved cog (maximum Hausdorff difference 1.28e-13 mm);
- all 24 new unions, subset exclusions and stock regions;
- 864 complete outer cells/domains, 18,724 required quantization vertices,
  and 4,681 outward rational halfspaces/expanded vertices;
- 33,720 saved small-part poses, 804,591 original fixed-pair distances and
  33,720 union-distance crosschecks.

All **12,860** saved original poses compatible with this core have encoded
floor-grid representatives. Compatible portions of four old baselines total
61, 61, 58 and 58 parts, including the 33 fixed parts; these remain partial.
Their 1,642 cross-part rectangle relations also check. As with core 0, the
0.001 mm subset exclusion, expanded stock, outward quantization and allowed
one-grid-unit overlap deliberately enlarge the diagnostic feasible space.
They are never acceptable production settings.

The model mandates all 12 brackets and 21 inserts in addition to 33 fixed parts.
Every field of its **20,907 variables and 121,531 constraints** is reconstructed
independently. It retains 15,795 domain choices, 360 orientation/sheet modes,
and all 978 cross-part component pairs with coupled bracket arms.

One declared 60-second call reaches search at 1.83 seconds and reports
`#Done 9.78s no_lp`, with total elapsed **9.923168 seconds**.
Status is `INFEASIBLE`, with 112,187 branches, 16,457 conflicts and no incumbent.
The conditional exclusion depends on the full coverage/model audits; there is
no separately verified LRAT proof. Other frame/cog arrangements remain open.
This completed call is not retried or extended.

## All parts movable: a new necessary relaxation

The next investigation removes the fixed arrangement entirely. All original
18 frames, 12 brackets, 21 inserts and 15 cogs choose positions across the same
two original sheet domains and material-height cap. Every permitted non-cog
orientation/reflection remains. No fixed frame set, finite pose list, hint,
objective or missing-part variable is used; only interchangeable-copy ordering
removes symmetry. Holes remain reserved, as required by the original plan.

The earlier exact-rational cog certificate proves a disk of radius
**109.1157 mm** lies strictly inside every filled cog outline, for every cog
rotation. Each cog is represented here by the same fixed-axis convex 16-gon
strictly inside that disk, with a freely moving center. This is a necessary
relaxation, not a substitute for the original cog outline in an accepted layout.
The three other part families retain exact original rectangular components;
the two bracket arms share one orientation and position.

An independent rational audit rechecks all 80 cog boundary distances and the
interior center, all 16 polygon vertices, all 16 non-cog orientation/reflection
cases and their complete rectangle decompositions. It independently constructs
1,792 Minkowski vertex sums, verifies every required separating normal and
all **496** outward separation thresholds. The 28 non-cog sheet/orientation
modes and two cog-center stock domains are rounded outward. Flooring positions
to 0.01 mm changes a relative coordinate by less than one grid unit per axis;
the exact integer inequalities explicitly allow that entire error. Positive
clearance is dropped only in this diagnostic relaxation.

The first preparation failed before producing geometry because an integral
source coordinate remained a floating value at a rational constructor. Its
original helper, plan and failure record are preserved. The corrected helper
checks integrality and converts to exact integers before transformation, in a
separate output directory. It completes in 0.004456 seconds; the independent
geometry audit completes in 0.060897 seconds. No solver had run in the failed
preparation, and no completed phase or capped search was resumed.

## Global encoding and bounded result

All **31,467 variables and 37,061 constraints** are independently reconstructed
from the audited geometry before execution. The model contains 462 modes,
all 2,145 physical-part pairs, 1,941 rectangle/rectangle component pairs,
945 disk/rectangle pairs and 105 disk/disk pairs. Every separating disjunction,
conditional sheet relation, component offset, coordinate bound, copy-order
constraint and solver parameter checks. Construction takes 1.021424 seconds;
the independent encoding audit takes 0.322366 seconds, both within declared
120-second caps.

One declared 60-second, eight-worker, seed-zero call reaches search at
1.62 seconds. It returns **`UNKNOWN`** in **60.152007 seconds**, retaining
the solver's small soft-limit overrun. There is no incumbent after 758,223
branches and 75,218 conflicts. This is unresolved, not an infeasibility proof.
No original layout is manufactured from this outcome, and the call is neither
extended nor repeated.

A separate sanity check maps the preserved original 64-part layout into this
new model. All stock domains and all 1,898 same-sheet component relations check;
the maximum quarter-turn transform difference is 5.69e-14 mm. It still lacks
two brackets and is never a solution to the mandatory 66-part model or a solver
hint. The global relaxation remains open even though the two previously tested
fixed arrangements have conditional negative results.

## Next investigation and repository state

Do not retry or extend either completed call, or revisit small pose sampling with either excluded fixed core. Investigate propagation for the all-parts-movable necessary relaxation. First derive and independently audit original filled-area lower bounds and outward usable-sheet capacity bounds, preserving the actual cog areas even though the geometric model uses smaller inscribed polygons. Then derive optional inner rectangles for every original non-cog component and a rotation-invariant inner square for each cog; their floor-grid placement must remain a subset of every valid original placement. These support global NoOverlap2D/cumulative propagation across all parts without choosing a fixed frame/cog arrangement. Keep all original orientations and both original stock domains, all66 counts, original material target and no part-in-hole. Declare new limits before any strengthened model construction or single solver call, independently reconstruct the full encoding, and retain UNKNOWN/caps. Do not simply change the seed or extend time on the completed model. A positive relaxation still needs original cog shapes/angles, original clearance, native guards, the production budget and all13jobs at both kerfs. H2 remains open by explicit instruction; do not evaluate the22 reserved vectors or ask the same denominator question again.

Engine source, all three accurate READMEs and release versions are unchanged.
Main 8f941426's hosted checks are captured as `in_progress` /
`pending`; no unfinished hosted run is called a pass.
The three newer evidence commits remain local at source head 56678ee9 while
that main run completes, avoiding cancellation by another push. No production
tests are rerun for evidence-only changes. There are no native packing calls,
quality runs, held-out evaluations or newly qualified releases here.

Evidence: [guarded coverage](h5-guarded-core-and-global-relaxation-20261025/guarded-coverage-audit.json),
[guarded model](h5-guarded-core-and-global-relaxation-20261025/guarded-model-audit.json), [guarded result](h5-guarded-core-and-global-relaxation-20261025/guarded-solver.json),
[global plan](h5-guarded-core-and-global-relaxation-20261025/global-plan.json), [global geometry](h5-guarded-core-and-global-relaxation-20261025/global-geometry-audit.json),
[global model](h5-guarded-core-and-global-relaxation-20261025/global-model-audit.json), [global result](h5-guarded-core-and-global-relaxation-20261025/global-solver.json),
[partial baseline check](h5-guarded-core-and-global-relaxation-20261025/global-baseline-audit.json),
[interpretation](h5-guarded-core-and-global-relaxation-20261025/interpretation.json), [source review](h5-guarded-core-and-global-relaxation-20261025/source-review.json),
[raw archive](h5-guarded-core-and-global-relaxation-20261025/raw-001.zip) and [manifest](h5-guarded-core-and-global-relaxation-20261025/raw-manifest.json).
All 168 canonical members and 23
aliases retain exact bytes with CRC and SHA-256 checks, including both complete
models/logs, all guarded regions, global geometry and the failed preparation.
