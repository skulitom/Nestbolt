# Full mixed-part source relaxation and band diagnosis — 2026-10-28

The smaller model keeps **all 25 remaining originals mandatory** around the
updated 41 fixed parts. Its first bounded call returns **UNKNOWN without a
candidate**, so the whole sequence stops. The subsequent finite band diagnosis
finds **no capacity contradiction**. Neither result proves feasibility or
infeasibility. H2/H5 remain open at **60% completed milestone weight**.

The initial model uses fresh fixed-owner free regions and necessary capacities
from rectangles contained in the original filled polygons. It has **342 variables,
4,017 constraints, 50 independent anchor coordinates, 1,471 rectangle options
and 205 partial hints**. It has no mover-pair collision constraints initially;
the planned generation loop would add those only after full source readback
exposed a collision. All holes remain reserved. The declared constructive modes
are one 7° cog orientation, eight bracket quarter/mirror choices and two insert
orientations, with no free-angle or complete-orientation claim.

Geometry readback checks **77 domains, 1,138 convex cells and 4,129 integer
halfplanes**, including 286 fixed-neighbour checks and 13,299 independently
constructed Minkowski hulls. Only intrinsic mode-pair domains are reused;
the fixed-owner regions correspond to the updated mixed26 core. The source56
control passes 925 pairs, 224 stock edges and 74 holes / 8,074 hole vertices.

The preliminary fixed rectangles remain preserved. A separately named copy
insets each edge by 2 µm for strict source containment. Independent exact
Fraction segment checks verify **139 contained rectangles against 7,592 source
edges**, plus 4,197 same-owner rectangle pairs. The source56 control passes
both cumulative capacities, with 132,524 µm and 7,024 µm slack.

The serialized model reader verifies every field and all 25 mandatory
constraints. A separate partial-control copy disables exactly ten mandatory
presences; restoring those ten domains reproduces the real model. The partial
control fails those ten requirements in the actual full66 target. A no-solve
preflight exercises all six family pairings, all 66 intrinsic mode domains and
the reversed displacement convention: **1,708 variables / 9,221 constraints**,
95 mode-pair groups, unchanged base prefix and a valid partial control.
This verifies the pair builder but is not a runtime generated-cut result.

The frozen sequence allowed at most eight distinct solves, each at most
15 seconds, within **one 60-second total algorithm budget and 90-second shared
limit**. Search starts at **0.44 s** and the first call returns UNKNOWN after
**15.038662 s returned / 15.037422 s solver time**. Total algorithm time is
**15.235108 s**, shared time **15.948386 s**. The **0.038662 s solve soft overrun**
is preserved. Its response reports 107,154 branches and 20,353 conflicts for
the returned worker, not an aggregate portfolio count. There are no assignments,
incumbents, source candidates, runtime generated cuts or native calls.
The stop-after-no-candidate rule is obeyed; unused time is not a new budget.

A separate read-only diagnosis freezes 93 horizontal boundaries and checks
all **4,278 bands**. For each mandatory part it minimizes the area of its
contained rectangles in each band over conservative anchor-Y intervals and
all permitted modes. These are exact integer piecewise-linear minima at
interval endpoints or rectangle/band breakpoints. Summing the independent
minima and fixed occupied area is a necessary lower bound only.

An independent event-slope implementation verifies all 4,278 results through
**143,421 slope events**, and checks the valid partial control against every
band. It finds **zero overloads**; 486 bands have a positive mover lower bound.
This finite check excludes no fixed-core construction and supplies no full
layout. Contained rectangles cover only part of each original, and X, mode
and inter-part couplings were deliberately relaxed in this diagnosis.

The next formulation will test collision generation before imposing the large
cumulative system. It must still require all66 originals, use the fresh owner
regions, reject every failing source candidate and add complete pair-mode
constraints for exposed collisions. Its complete diagnostic reconstruction,
serialized model and one total time budget must be audited before execution.
No closed solve is restarted or extended. Any successful source construction
still requires native, material and full H5 validation before integration.

[Main CI 40748909850](https://github.com/skulitom/Nestbolt/actions/runs/40748909850)
now passes all six jobs on b699d1c1. The prior outer-cover and this checkpoint
are ready for a normal atomic push after fresh remote guards. Production,
READMEs and upstream heads/releases are unchanged. The valid64 frontier,
444 necessary allocations, original H2 gate and 22 unopened reserved vectors
remain preserved. No new release qualifies.

Evidence: [geometry audit](h5-mixed25-lazy-source-20261028/geometry-audit.json),
[contained-capacity audit](h5-mixed25-lazy-source-20261028/capacity-audit.json),
[base-model reader](h5-mixed25-lazy-source-20261028/base-model-audit.json),
[pair preflight](h5-mixed25-lazy-source-20261028/pair-preflight.json),
[closed response](h5-mixed25-lazy-source-20261028/response-audit.json),
[independent band audit](h5-mixed25-lazy-source-20261028/band-audit.json),
[next step](h5-mixed25-lazy-source-20261028/next-step.json),
[raw manifest](h5-mixed25-lazy-source-20261028/raw-manifest.json).
The archive preserves 281 canonical files and
269 identical-byte aliases in 809,752
compressed bytes, including all bound inputs, helpers, model fields, control,
solver response/logs, every band and publication snapshot.
