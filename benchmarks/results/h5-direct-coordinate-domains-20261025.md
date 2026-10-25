# H5: checked direct-coordinate domains — 2026-10-25

**Continuous placement regions are verified; packing has not been solved.**
The next model requires all 12 brackets and 21 inserts around the unchanged
18-frame/15-cog core 0. Original quantities, stock/material target and native
requirements remain. H2/H5 are open at **60%** completed weight.

## A different representation of the remaining placement problem

Earlier searches chose among finite saved poses or whole macro rectangles.
This construction instead permits each small part to move on a 0.01 mm
coordinate grid within independently checked convex translation regions.
Source-exact quarter turns and reflections turn the L bracket into its two
coupled rectangular arms. The insert is one rectangle. All twelve permitted
orientation/reflection cases map to ten distinct normalized shapes; equivalent
insert quarter turns are explicitly recorded. The normalized original floating
transforms differ by at most 5.68e-14 mm.
Holes remain reserved. No arbitrary part contour or inventory is substituted.

Core 0 is selected because the previous census finds it alone passes both
conservative pair and stock screens. This still requires actual native
transformed-collision validation. New-part regions use **0.22 mm** separation
plus an explicit construction margin, and **0.02 mm** additional stock margin.

## Construction and exact inward rounding

All **20** orientation/sheet queries complete in
**3.562328 seconds**, within 120 seconds, with no pending query.
Exactly covering convex-piece Minkowski sums build the fixed-part obstacles.
Their union is expanded with an explicitly circumscribed 128-sided clearance
polygon at 0.22 + 0.0001 mm. Original stock domains are reduced by the declared
extra margin. Constrained triangulation covers the safe regions exactly;
only convex adjacent unions merge. All unmerged faces remain.

The first independent audit verifies 20 cached obstacles from 396 convex-piece
vertex sums, every complete safe region, 3,884 convex faces and 12,865 rational
halfspaces. Edge coefficients are derived from exact rational representations
of the stored binary-float vertices. Their integer bounds subtract the full
worst-case rounding error over the bounded coordinate domain, plus one unit.
Exact rational clipping verifies **16,455** vertices against the original face
edges. Twelve domains have empty rational intersections or empty integer
bounding intervals; 3,872 remain, implying 58,434 per-copy alternatives.
Removing these empty domains loses no feasible point from this grid model.

## Certified domain consolidation

A separate predeclared 60-second/200,000-attempt consolidation completes in
**5.396297 seconds** after 36,810 merge attempts. Every source
face remains represented exactly once in a recorded lineage. A convex hull
may replace adjacent faces only if the entire hull lies in a separately
reconstructed safe region with the same **0.22 mm** gap and an additional
0.00001 mm construction margin. A hull can add translation space but remains
inside that checked region; its area is not packed material or a quality score.
No part count, required gap or stock domain is reduced.

The independent consolidation audit rebuilds every clearance envelope and
stock domain, verifies all source-face coverage and all hull containment,
and checks **12,655** rational halfspaces and **16,191** resulting vertices.
It retains **3,703** grid domains: 2,419 bracket and 1,284 insert domains.
Twelve proven-empty domains are retained as explicit exclusions. The total
per-copy alternative count falls to **55,992**. Every merge queue finishes;
neither construction phase is repeated or extended.

The resulting domains are conservative feasible subsets. Their inability to
pack would not prove the unrestricted original geometry impossible. No
solver, complete layout, native qualification or production-quality result
has been produced by this work.

## Next exact-count model

Construct and independently check one exact-count coordinate model from consolidated/audit/integer-domains.json. Use one anchor x/y pair, permitted orientation and sheet choice per physical small part. Require all12 brackets and21 inserts; keep core0 unchanged. Connect each piecewise-convex domain to its orientation and sheet with all inward-rounded inequalities and bounds. Model each bracket as two coupled original rectangular arms; enforce at least0.22mm directional separation only between rectangles belonging to different physical parts, including all cross-arm pairs. All original stock bounds,0.02mm additional new-part stock margin and fixed-part safe domains remain. Symmetry ordering may only permute identical copies. The remaining55992 per-copy domain alternatives motivate certified containment removal or factoring before encoding; any removed domain must map to a retained same-sheet/same-orientation superset with independently checked rational halfspace certificates. No lost feasible grid point or arbitrary candidate pruning is allowed. Preserve all source regions and baselines. Verify every model and parameter field before exactly one predeclared60-second/eight-worker/seed-zero solver call. UNKNOWN is not infeasibility and the call must not be extended or repeated. Any full witness requires original geometry and CLI checks, actual native collision checks, original production budget and all13 jobs at both kerfs. No renewed capped pose generation, acceptance weakening, reserved-file access or new release is authorized by this diagnostic.

## Repository and evidence

Both earlier audit checkpoints are pushed to main as **8f941426**. Its hosted
checks are captured as `in_progress` / `pending`.
Previous main 55835d7c's run is `cancelled`;
the repository's CI workflow cancels an older in-progress run on the same
branch when a newer push starts. Its earlier successful jobs remain recorded.
Engine source, all three accurate READMEs and published releases are unchanged.
No native packing, H5 quality matrix or held-out evaluation occurs.

Evidence: [construction plan](h5-direct-coordinate-domains-20261025/plan.json), [generation](h5-direct-coordinate-domains-20261025/generation.json),
[first audit](h5-direct-coordinate-domains-20261025/audit.json), [consolidation plan](h5-direct-coordinate-domains-20261025/consolidation-plan.json),
[consolidation result](h5-direct-coordinate-domains-20261025/consolidation.json),
[independent consolidation audit](h5-direct-coordinate-domains-20261025/consolidation-audit.json),
[source review](h5-direct-coordinate-domains-20261025/source-review.json), [raw archive](h5-direct-coordinate-domains-20261025/raw-001.zip)
and [manifest](h5-direct-coordinate-domains-20261025/raw-manifest.json). All 86 canonical
members and 13 aliases pass exact byte, SHA-256 and CRC
checks. Original input hashes, every source face, empty-domain reason and
orientation alias are preserved.
