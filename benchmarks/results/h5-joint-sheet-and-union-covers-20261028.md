# Movable first sheet and tighter cog-row covers — 2026-10-28

The whole-first-sheet hull-cover search closed **UNKNOWN without a candidate**.
Its complete model and response are independently audited. A subsequent
geometry study produces smaller covers and a valid **56-part partial control**,
providing the next concrete construction. It does not complete the 66-part job.
H2/H5 remain open at **60% completed milestone weight**.

The model allows **all 51 first-sheet originals** to move: 18 frames, six
brackets, 12 inserts and three rigid rows of five cogs. The short-sheet 15 stay
fixed. All **39 blocks are mandatory**, with 78 independent anchor coordinates,
111 legal mode choices, 330 cover component options and 35 symmetry orders.
Independent reading verifies all **228 variables and 998 constraints**. Complete
cover separation applies in every mode. No old rectangular core is fixed.

Source stock checks use a **13 µm guard** inside the original boundary. A
clearance cover may extend at most 114 µm outside its source bounding box, so
the cover envelope is `[6399, 6399, 1493601, 2993601]` µm. This avoids an extra
restriction that would require the clearance covers inside the original stock.
The earlier exact section weights are checked against **9,130 patterns** for
this envelope: the hull-cover height lower bound remains **2,978.159551 mm**,
leaving **9.042449 mm**. This necessary bound does not establish feasibility.

The positive control contains 26 orthogonal originals and two cog rows, plus
the short sheet: **51 originals**, 735 source pair checks, 69 holes and 7,074
hole vertices. Its 145 cover rectangles pass all **10,440 pair checks**. The
control fails exactly the **11 missing-block requirements** of the actual
target. Changing only those requirements in a separate audit copy makes the
control assignment pass every constraint. The target model remains mandatory.

A complete negative control has all 66 originals in legal stock positions
but **825 source collisions and 4,149 cover collisions**. It fails exactly the
NoOverlap2D constraint and both cumulative constraints. Independent source
reconstruction binds both controls to their model poses, with maximum transform
difference about **2.27e-13 mm**. Two early reader errors—treating a collision
count as a list and omitting one section-family label—are preserved with their
partial outputs. The separate corrected audit completes successfully.

One frozen **60-second algorithm / 90-second shared** budget includes process
startup, input checks, solve and any candidate source readback. The solver gets
**59.304176 s** after setup, with four workers, seed zero and `fj` disabled.
Search starts at the logged **0.26 s**. No incumbent or final assignment is
returned. The reported worker counters are **75,563 branches and 64,797
conflicts**; they are not a sum over all four workers.

The call returns after **59.375588 s**, preserving a **0.071413 s solve soft
overrun**. Total algorithm time is **60.076083 s**, including a **0.076083 s
overrun**, and shared time is **60.146931 s**. The response reader rechecks every
model field, runtime parameter, saved hash and reported counter. The single
call is closed. UNKNOWN is not an infeasibility proof; there is no source-valid
full layout, native validation or H5 timing/material credit.

The next study keeps the original five-cog rows and replaces each convex-hull
cover with a slab cover of the **union of the square-expanded filled original
cogs**. Internal cutouts remain reserved. At the same 5 mm slab width, this
requires **523 rectangles per row**, up from 58, but reduces each row's cover
area from **352,775.805050 to 264,914.057960 mm²**. Across three rows it removes
**263,585.241270 mm²** of artificial occupied area. The first-sheet cover area
becomes **4,112,088.300216 mm²**. Smaller area does not prove the job fits.

An initially assumed exact subset relation fails: floating reconstruction of
the original row shifts the first slab boundary by **1 µm**, putting
**0.209406 mm²** of the new cover outside the old slab cover. The failed assertion
and diagnosis are preserved. The new cover is assessed independently; no
original geometry or clearance margin is relaxed. Its full source expansion,
required clearance discs and **390 independently constructed triangle-square
hulls** are covered, and its rectangle interiors are disjoint.

For the predetermined row X offsets of **0 / 80 / 0 mm**, exact rectangle
comparisons derive a safe adjacent Y separation of **269.756 mm**. This places
all three rows above the previous 26-part core as a stronger partial control:
**56 originals, 925 source pair checks, 74 holes and 8,074 hole vertices** pass.
All **1,276,003 pairs** among its 1,598 cover rectangles also pass. The remaining
ten originals are still required in the future target model. This is geometry
preparation only; no union-cover packing model or solve has been created.

Next build and audit that new complete movable-sheet model, using a copy of
the existing reader and honest partial controls. The old hull-cover search
and its hash-bound helpers stay closed. The old section-height certificate
does not automatically apply to the new row shape. Any candidate must pass
original 66-part, native and material checks before production integration;
the full unchanged H5 matrix remains required. Common-line part-in-hole stays
off. The valid 64-part layout, 444 necessary allocations, original H2 gate and
22 unopened vectors remain preserved.

The previous rational checkpoint was pushed normally and atomically to main
and the working branch at **75ee537c** after all six checks passed.
[CI 40764537562](https://github.com/skulitom/Nestbolt/actions/runs/40764537562)
has three successful and three running jobs in this snapshot. This checkpoint
waits for all six before a fresh guarded push. Production, READMEs and upstream
heads/releases are unchanged. No new release qualifies.

Evidence: [geometry and controls](h5-joint-sheet-and-union-covers-20261028/geometry-audit.json),
[complete model audit](h5-joint-sheet-and-union-covers-20261028/model-audit.json),
[independent source bridge](h5-joint-sheet-and-union-covers-20261028/source-bridge-audit.json),
[closed response](h5-joint-sheet-and-union-covers-20261028/response-audit.json),
[tighter row-cover study](h5-joint-sheet-and-union-covers-20261028/union-cover-audit.json),
[preserved subset failure](h5-joint-sheet-and-union-covers-20261028/union-subset-failure.json),
[next step](h5-joint-sheet-and-union-covers-20261028/next-step.json), [raw manifest](h5-joint-sheet-and-union-covers-20261028/raw-manifest.json).
The verified archive contains 356 canonical files and 377
identical-byte aliases in 1,546,307 compressed bytes, including all failed
audits, inputs, controls, geometry, model, solver output and source proofs.
