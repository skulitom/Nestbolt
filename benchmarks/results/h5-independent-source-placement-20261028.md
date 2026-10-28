# Independent source placement — 2026-10-28

The new construction model lets all **23 remaining originals move
independently**, with no lattice or fixed cog coordinates. Its sole bounded
search returns **UNKNOWN** without a complete layout. This is not an
infeasibility result. The earlier source-valid64 remains the best partial
layout; H2/H5 remain open at **60% completed milestone weight**.

## Original-source geometry and conservative cells

The 7/7 short-sheet allocation retains 43 originals: 29 first-sheet frames and
side inserts, plus the 14 short-sheet originals. The remaining 15 cogs, five
brackets and three inserts are all mandatory. Cogs use the legal constructive
phase 7°; brackets have all eight legal modes and inserts use 0°/90°.
No claim covers every possible cog angle.

The original 11 source modes, 66 forbidden-displacement polygons and 11
fixed-neighbour free regions are reused because their source shapes, guards
and 29 fixed first-sheet poses are unchanged. This does not resume any earlier
local search. Preparation decomposes the 77 domains into **1,124 convex cells**
with **4,079 integer halfplanes**, in 8.712509 shared seconds.

An independent reader reconstructs original modes, verifies 141 source convex
pieces, and builds **12,627 independent Minkowski hulls**. All 66 stored
obstacles cover the original-source required-clearance obstacles; all 319
fixed-neighbour checks and stock guards pass. Every convex-cell union is read
back. Exact rational arithmetic bounds coefficient-rounding error, proving
that the integer halfplanes describe subsets of the safe cells on a 1 µm grid.
This conservative construction may miss real placements.

## Partial source control and complete model audit

The first partial control at 258.88 mm cog pitch is preserved as a failure:
its 0.222662845 mm source gap exceeds the required acceptance gap, but is below
the existing conservative obstacle buffer of 0.224308673 mm. Tooth-edge slope
means pitch and clearance increments are not equal.

A separately recorded deterministic control uses 258.90 mm pitch, rounds moving
anchors to 1 µm and relabels identical copies for X ordering. All 43 fixed
originals remain exact. Its **62 original parts** pass 1,219 source pairs and
248 stock edges, with minimum pair gap 0.224800281 mm and minimum extra stock
clearance 0.024800286 mm. All 19 occupied fixed-neighbour cells and 171 occupied
relative cells pass. Four missing bracket positions remain unhinted.

The independent serialized-model reader checks **58,151 variables and 210,518
constraints**, including all 46 independent coordinates, 253 unordered mover
pairs, 1,687 mode-pair groups and 24,203 hint values. Every part is mandatory.
Mode and cell choices, relative-displacement signs, source halfplanes and
identical-copy X ordering are checked exhaustively. The partial control
satisfies its 2,111 active constraints; 83,687 are inactive and 124,720 involve
unplaced parts. No objective, lattice or fixed position is introduced.

## Closed search and next construction

The sole predeclared call uses four workers, seed0, a 60-second solver setting
and a 90-second shared limit. It returns **UNKNOWN**, with **143,475 branches
and 4,080 conflicts**, in 60.129179 solver seconds, 60.151582 returned seconds
and 61.636477 shared seconds. The **0.151582-second returned soft overrun** is
retained. No assignment or native call exists. The independent response reader
verifies hashes, parameters, protobuf status, log rounding and timing.

This result changes none of the 444 necessary count allocations. The call is
closed. Next derive and independently audit rectangles contained in the
original filled modes, then use them for necessary cumulative sheet-capacity
constraints in a separately declared model. Such constraints can improve
propagation while retaining independent positions and every mandatory part.
Any full layout still requires all66 original-source, native and unchanged
material-target checks before integration or a full H5 rerun.

All six jobs pass in
[main CI 40723142543](https://github.com/skulitom/Nestbolt/actions/runs/40723142543).
The preceding normal push receipt is archived. Production, READMEs and upstream
heads/releases are unchanged; all22 reserved H2 vectors remain unopened.
No new release qualifies.

[Source geometry audit](h5-independent-source-placement-20261028/geometry-audit.json),
[retained failed control](h5-independent-source-placement-20261028/initial-control-failure.json),
[valid partial control](h5-independent-source-placement-20261028/partial-control-audit.json),
[complete model audit](h5-independent-source-placement-20261028/model-audit.json),
[response audit](h5-independent-source-placement-20261028/response-audit.json),
[next work](h5-independent-source-placement-20261028/next-step.json),
[raw manifest](h5-independent-source-placement-20261028/raw-manifest.json).
The archive preserves 226 canonical files and
166 identical-byte aliases in 7,391,285
compressed bytes, including all source inputs, cells, halfplanes, model,
mapping, hints, failures, control, logs, response and independent readers.
