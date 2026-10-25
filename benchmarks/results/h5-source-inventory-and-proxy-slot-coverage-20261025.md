# H5: source orientation inventory and exact proxy-slot coverage — 2026-10-25

**The finite all-parts-movable construction remains `UNKNOWN`. A separate exact
check proves the 64-part starting arrangement has no place for even one extra
bracket in the simplified proxy model while every existing position stays
fixed.** Existing parts must move. The conclusion is conditional on those
fixed poses; it does not establish unrestricted packing impossibility.
H2/H5 remain open at **60%** completed milestone weight.

## Source-derived orientation inventory

This construction uses the committed 64-part target layout's orientations:
18 horizontal frames; eight horizontal and thirteen vertical inserts; ten
brackets in five recorded orientation/mirror groups; and all 15 cogs. Two
additional mandatory brackets retain every original orientation/mirror option.
All positions and permitted sheet assignments remain free. The same material
cap, original area charges and five-piece inner cog proxies are retained.

Independent source and group auditing matches nine inputs to committed
evidence, checks all 1,521 same-sheet original polygon pairs and all 6,186 proxy
component pairs, both partial area bounds and four complete sweep profiles.
Minimum source gap is 0.20010000000002037 mm. No new native-margin qualification
is inferred. The 64 poses become nonbinding hints only.

There are ten interchangeable orientation-option groups, **142** per-copy
modes and **56** within-group ordering constraints. Ordering never compares
copies with unequal fixed-orientation option sets. Every source part is
represented exactly once; the two additional brackets remain required and
unhinted. This is a finite orientation inventory for construction, not a
necessary relaxation of every original arrangement.

Preparation takes 0.012657 seconds and the independent source/group audit
takes 0.082611 seconds. Every field of **1,486 variables and 2,178 constraints**
is independently reconstructed, including all 1,406 nonbinding hinted values,
138 coupled inner rectangles, 552 optional intervals, two NoOverlap2D
constraints, four cumulative profiles and both original-area bounds. Model
construction takes 0.036492 seconds and encoding audit 0.024289 seconds.

One declared 60-second, eight-worker, seed-zero call starts search at
**0.07 seconds**. Its presolved hint covers 174 of 292 nonfixed variables.
The call returns **`UNKNOWN` in 60.111765 seconds**, with 532,358
branches, 116,192 conflicts and no incumbent. The small soft-limit overrun is
preserved. It is not repeated, extended or called an infeasibility proof.

## Direct exact check of the two missing slots

Keep all 64 source proxy poses fixed only for this diagnostic. The two missing
brackets retain all eight orientation/reflection cases on both sheets. Their
coupled rectangle components and the 134 fixed inner components have exact
integer coordinates at 100 units/mm.

Two axis-aligned components overlap only when both coordinate intervals
overlap strictly. For an integer moving anchor, the forbidden x interval is
`[fixed_min_x - moving_max_x + 1, fixed_max_x - moving_min_x - 1]`, with the
same rule for y. Clip these inclusive integer rectangles to the unchanged
mode domain. Sweep every critical x slab and complement the merged forbidden
y intervals. This includes boundary touching and isolated one-grid-coordinate
rows or columns; no sampled candidate list stands in for complete coverage.

All **16** queries finish in **0.039943 seconds**, within the declared
120-second construction limit and 200,000-cell cap, with nothing pending.
Every query has **zero** free integer anchors. The bounded two-slot selector
therefore examines zero cell pairs and is fully exhausted without hitting a
cap. It makes no additional solver call.

An independent audit reconstructs all **1,950** forbidden rectangles and uses
per-owner two-dimensional prefix-sum arrays over every critical x/y cell.
This is separate from the construction's interval-merging sweep. Exact integer
widths times heights count **266,545,630,376 mode/anchor pairs** across
**145,251** critical cells. Every one is covered by at least one fixed part.
The independent audit takes **0.060711 seconds** and confirms zero free anchors,
including touching/degenerate-grid cases. Thus even one extra bracket requires
changing an existing position in this proxy model.

## Single-part release census

Coverage is counted by original part, with all components of one part unioned
before counting owners. Cells covered by exactly one owner identify precisely
which bracket anchors become available if that entire part is removed
temporarily. All 64 possible single-part releases are recorded, including all
**33** frame/cog releases. Each core release exposes at least one bracket anchor.

These are counts of possible placements across orientation modes, not physical
free area, and they do not show that two brackets plus the removed part fit.
The next investigation must restore the released part: 63 fixed originals plus
that original part and two new bracket copies totals the required **66**.
No deletion, partial inventory or relaxed native requirement is accepted.

The source-orientation construction call is complete and UNKNOWN; do not rerun it or extend time. The independent integer coverage audit proves no extra bracket slot with all64 proxy poses fixed, so stop attempts that only append the missing brackets. Investigate exact small relocation neighborhoods that change a frame/cog position. For each of the33 original core parts, remove its proxy obstacles temporarily and construct complete integer free-anchor regions for that same part and two additional mandatory brackets around the remaining63 original poses. Keep every original part:63 fixed plus the released part restored plus two brackets equals66. Use the existing source orientation inventory for a finite construction test, both allowed sheets, original material cap and original-area charges. First derive an outward union of reachable occupied proxy regions and compare it to the required proxy areas to reject only certified impossible neighborhoods; do not confuse an anchor-count ranking with physical free area. Only then consider a separately declared bounded three-part feasibility model for the surviving neighborhoods, with complete independent geometry/model checks. Preserve all33 release cases, caps and pending work. A negative is conditional on that neighborhood/inventory; a positive remains a proxy and needs full cog shapes/angles, original clearance/native guards, production budget and all13jobs/two kerfs. H2 stays open; no reserved-vector access, gate reduction or new release. Poll main CI40233299884 and push further evidence normally after it is terminal.

## Repository and evidence

Engine source, all three accurate READMEs and release versions are unchanged.
Main 247e823a's existing run **40233299884** is captured as `in_progress` /
`pending`. The previous exact-alias checkpoint remains
local at source head 1cc63504 while this hosted run finishes. No unfinished
run is called a pass. No native packing, production-budget run, full H5 matrix
or held-out evaluation occurs. No new release is qualified.

Evidence: [inventory plan](h5-source-inventory-and-proxy-slot-coverage-20261025/inventory-plan.json),
[source/group audit](h5-source-inventory-and-proxy-slot-coverage-20261025/inventory-audit.json), [model audit](h5-source-inventory-and-proxy-slot-coverage-20261025/inventory-model-audit.json),
[bounded result](h5-source-inventory-and-proxy-slot-coverage-20261025/inventory-solver.json), [slot plan](h5-source-inventory-and-proxy-slot-coverage-20261025/slots-plan.json),
[independent coverage](h5-source-inventory-and-proxy-slot-coverage-20261025/slots-audit.json), [all query counts](h5-source-inventory-and-proxy-slot-coverage-20261025/slots-coverage.json),
[core-release census](h5-source-inventory-and-proxy-slot-coverage-20261025/core-release-census.json), [source review](h5-source-inventory-and-proxy-slot-coverage-20261025/source-review.json),
[raw archive](h5-source-inventory-and-proxy-slot-coverage-20261025/raw-001.zip) and [manifest](h5-source-inventory-and-proxy-slot-coverage-20261025/raw-manifest.json).
All 72 canonical members and 23
aliases retain exact bytes with CRC and SHA-256 checks, including the complete
model/log, every forbidden rectangle, source hints, coverage and release census.
