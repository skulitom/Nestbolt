# Source capacity and core-height limits — 2026-10-28

The source-capacity search closes **UNKNOWN**. A separate search that moves all
18 frames and 11 side inserts lowers their top by only **0.017 mm**. More
usefully, a new exact source bound proves that this same core can be shortened
by at most another **5.443429 mm**, even with arbitrary positions and all legal
quarter turns. The next construction will change the core composition.
H2/H5 remain open at **60% completed milestone weight**; no full layout exists.

## Necessary source-capacity constraints

The phase7 cog has 92 disjoint contained rectangles, covering 88.223258% of its
filled area. All bracket and insert modes and the 29 fixed first-sheet originals
also have contained rectangles. Independent exact-rational edge checks verify
**139 local/fixed rectangles, 7,580 source-edge checks and 4,194 internal pair
checks**. Integrating disjoint sections proves the two stock-capacity constraints
are necessary for any valid source placement. No extra spacing is demanded.

The model preserves all **58,151 prior variables, 210,518 constraints and 24,203
hints exactly**, then adds 2,990 optional intervals and two cumulative capacities.
All 23 movers remain mandatory and independently positioned. Every addition,
presence literal, demand and capacity is read back. The positive partial control
passes with 1,414 active components and both cumulative sweeps.

The first geometry audit's timer was accidentally overwritten by an interval
coordinate; its negative elapsed duration is invalid and retained with an
erratum. The corrected reader repeats the checks into a separate folder and
records 0.113605 seconds. No solver call is repeated for this repair.

The sole 60-second, four-worker capacity call returns **UNKNOWN**, with 95,682
returned branches and 2,890 conflicts. Solver time is 60.084770 s; returned time
60.104726 s; shared time 61.620649 s. The 0.104726-second returned soft overrun is
preserved. No assignment or infeasibility claim follows.

## Independent frame/insert core compaction

Existing records already contain fixed mixed-row and staggered frame patterns.
This new model instead moves every one of the 18 frames and 11 side inserts
independently, allows 0°/90° orientations and minimizes their maximum upper Y.
All original filled outers are rectangular. Padding each model rectangle by
112 µm guarantees at least 0.2239 mm actual source separation, accounting for
the recorded source-bound tolerance. Stock and native guards remain unchanged.

All **117 variables, 291 constraints and the complete valid control** are
independently audited, including 406 expanded rectangle pairs. The sole bounded
call returns **FEASIBLE**, retaining nine incumbents, in 60.040218 solver seconds
and 60.853029 shared seconds. Its returned soft overrun is 0.041680 s. Every
incumbent and final assignment passes the saved-model evaluator. The result is
not an optimum; its solver bound remains 2,061.659 mm.

The new actual core top is **2,107.633 mm**, only **0.017 mm** below the previous
2,107.65 mm. All frames stay unturned and all eleven inserts stay at 90°.
Combined with the unchanged short14, the source43 readback verifies **497 pairs,
172 stock edges and 57 holes / 4,830 hole vertices**. Minimum pair clearance is
0.224 mm and minimum extra stock clearance is 0.013 mm. All 23 remaining originals
are explicitly unplaced. The earlier valid64 remains the best partial layout.

## Exact bound on further height reduction

For each frame/insert quarter turn, take a rectangle inset 2 µm per side.
The independent reader proves containment using 128 exact source halfplane
tests across all eight modes. At a horizontal section, inner widths
449,996 / 349,996 / 179,996 / 109,996 µm receive weights **9 / 7 / 2 / 1**.
Every one of the **214 feasible section-count patterns** fitting the original
1,487,000 µm usable width has total weight at most 28. A separate nested-loop
enumeration verifies the complete pattern set and all quantity caps.

Integrating these section weights over height yields a core-span lower bound
of **14,669,827 / 7 µm**, or **2,095.689571 mm**. Adding the conservative stock
bottom gives an original-core-top lower bound of **2,102.189571 mm**. Relative
to the newly verified top, at most **5.443429 mm** of further height reduction
is possible. This bound covers arbitrary independent positions and all legal
quarter turns of this same 18-frame/11-insert core. It is not a full66 exclusion
and does not rule out beneficial changes to the shape of the remaining space.

Another height-only call is not justified by these results. The next step is
to revalidate the previously source-valid staggered core with brackets embedded
beside frames, then use a new independent-coordinate formulation for all its
25 remaining originals. Its old 2,000-pose finite-pool exclusion stays closed;
owner-dependent geometry must be rebuilt. All 444 necessary short-count
candidates, original quantities, material target and guards remain unchanged.

At publication review, five jobs pass and the Windows check is still running in
[main CI 40728382102](https://github.com/skulitom/Nestbolt/actions/runs/40728382102).
A normal push waits for all six plus fresh remote guards. Production, READMEs
and upstream heads/releases are unchanged. All 22 reserved H2 vectors remain
unopened. No new release qualifies.

[Capacity necessity](h5-source-capacity-and-core-height-20261028/capacity-necessity-proof.json),
[capacity response](h5-source-capacity-and-core-height-20261028/capacity-response-audit.json),
[core response](h5-source-capacity-and-core-height-20261028/core-response-audit.json),
[source readback](h5-source-capacity-and-core-height-20261028/core-source-audit.json),
[exact height bound](h5-source-capacity-and-core-height-20261028/height-bound-audit.json),
[next construction](h5-source-capacity-and-core-height-20261028/next-step.json),
[raw manifest](h5-source-capacity-and-core-height-20261028/raw-manifest.json).
The archive preserves 299 canonical files and
134 identical-byte aliases in 13,695,690
compressed bytes, including both closed calls, every incumbent, the invalid
timer record, corrected checks, source inputs, complete models and all patterns.
