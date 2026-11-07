# One-/three-turned cog-transfer capacity — 2026-11-07

**Nineteen source-valid 44-part partials cannot extend to 66 parts.** Even
changing every bracket/insert allocation cannot rescue these exact first-sheet
frame/cog cores while the short-sheet cog stays fixed. Eleven cores also fail
when that last cog is free. No whole allocation or orientation class is excluded.
H2/H5 remain open at **60% completed milestone weight**; the valid 64-part result remains best.

[The source construction](h5-one-three-transfer-capacity-20261107/source-plan.json) reuses the exact earlier
one-/three-turned upper-frame pools and puts original cog14 on the independently
verified short sheet. It screens all **135** choices of fourteen first-sheet
cog sites: fifteen choices from the one-turned pool and 120 from the three-turned
pool. All pool contacts are recomputed from original polygons.

[Independent replay](h5-one-three-transfer-capacity-20261107/source-audit.json) verifies **783 pool contacts**.
The three-turned pool has precisely two disjoint collided pairs, [3,14] and
[7,15]. Of 120 choices,116 retain at least one witnessed collision. The four
surviving omission pairs are [3,7], [3,15], [7,14] and [14,15]. All fifteen
one-turned choices survive. Complete checks of the nineteen original 44-part
partials verify **10,678 same-sheet pairs and 1,064 original holes**. Every
remaining identity is retained: six brackets and sixteen inserts still need
placement. The 116 negatives are preserved with their specific witnesses.

[New covers](h5-one-three-transfer-capacity-20261107/cover-plan.json) rebuild every world obstacle and all 24
full mode masks, including the eight one-turned bracket modes that could have
been reused after equality checks. Rebuilding keeps this proof self-contained.
Only audited local cog inner rectangles and source parameters are reused.
Each pool includes all eight quarter-turn/mirror bracket modes and four
quarter-turn insert modes in the full physical stock domain. Point/interval
classes allow one empty cog bit for the one-turned pool and two for the
three-turned pool, with no fixed-frame conflict.

[Independent exact readback](h5-one-three-transfer-capacity-20261107/cover-audit.json) verifies **2,423 source
inner rectangles, 20 component bounds, 24 masks and 49,247,076 continuous
classes**. Every retained class is covered exactly once. Original L-component
and insert sweeps, outward stock clipping and subtraction of definitely
occupied source interiors give **57** independently checked union-difference
areas. Boundary, duplicate-obstacle and area-rounding controls pass.

| Upper turned frames | Valid partials | Largest available companion area (mm²) | Required (mm²) |
|---|---:|---:|---:|
| One | 15 | 456,755.775318 | 556,778 |
| Three | 4 | 495,456.515617 | 556,778 |

[All nineteen fixed 44-part layouts are excluded](h5-one-three-transfer-capacity-20261107/fixed44-capacities.json).
These proofs apply to the exact selected frames/cogs and short-sheet rows,
without running an optimizer.

[The inventory extension](h5-one-three-transfer-capacity-20261107/inventory-plan.json) first keeps only the
eighteen frames and fourteen cogs on the first sheet, releasing all remaining
originals. The previous material proof bounds the entire other sheet by
465,326.048858 mm². Combined area and bracket-count bounds exclude eleven of
the nineteen cores even when the last cog is ignored. Eight remain unexcluded
under that broader relaxation; a surviving necessary bound is not feasibility.

The second scope additionally fixes original cog14 at its verified short-sheet
pose, but releases every bracket and insert on both sheets. [Rational source
area readback](h5-one-three-transfer-capacity-20261107/fixed-short-cog-area.json) certifies at least **50,061 mm²**
for that cog's filled outer polygon, including a conservative 80-vertex rounding
allowance. At most **415,265.048858 mm²** then remains for short-sheet companions.
Original holes stay preserved and are not nesting space.

[Every whole-part split](h5-one-three-transfer-capacity-20261107/whole-part-splits.json) is checked. The largest
fitting bracket/insert inventory lower bound is only **399,990 mm²**, so the
first sheet must hold at least **495,777 mm²** of companion bodies. The largest
available first-sheet region is **495,456.515617 mm²**: a deficit of at least
**320.484383 mm²**. [Independent division-based inventory enumeration](h5-one-three-transfer-capacity-20261107/inventory-audit.json)
verifies **5,434 split checks**, including every family and combined-area reason.
[All nineteen fixed first 32 parts plus short-cog cases are excluded](h5-one-three-transfer-capacity-20261107/fixed32-capacities.json),
regardless of which brackets and inserts go on each sheet. This second result
does not cover moving the last cog onto the first sheet or changing fixed poses.

| Bounded stage | Complete preparation (s) | Separate audit (s) |
|---|---:|---:|
| Source subsets and partials | 0.919201 | 1.199101 |
| Fresh covers and occupied area | 9.630416 | 12.924171 |
| Whole-part inventory | 0.384811 | 0.413790 |

The [source](h5-one-three-transfer-capacity-20261107/transfers-process.json), [cover](h5-one-three-transfer-capacity-20261107/covers-process.json)
and [inventory](h5-one-three-transfer-capacity-20261107/inventory-process.json) preparations retain all inherited
work for **40.936341 s** total if consumed by a successor. Their separate
[source](h5-one-three-transfer-capacity-20261107/transfers-audit-process.json), [cover](h5-one-three-transfer-capacity-20261107/covers-audit-process.json)
and [inventory](h5-one-three-transfer-capacity-20261107/inventory-audit-process.json) audits pass. All six Job
Objects close three processes within their caps, 2 GiB, CCD1 and single-thread
controls. No optimizer or closed call is reopened.

[Next](h5-one-three-transfer-capacity-20261107/next-step.json), test the original one-turned all 15-cog first-sheet
core under arbitrary companion splits using zero-empty covers. Restoring the
missing site yields one common first 33-part core, not four separate searches. The
three-turned pool cannot restore either removed cog without reviving a known
collision, so any further source construction must change an actual pose.
Four earlier fixed arrangements and 440 whole-job allocations remain. Full66
source/native/material checks, integration, parity and the H5 matrix remain open.

[Main 66192d0d includes the preceding ordinary push](h5-one-three-transfer-capacity-20261107/prior-main-push-receipt.json).
[CI at review](h5-one-three-transfer-capacity-20261107/main-ci-at-review.json) records **5 passed / 1
live jobs**. This checkpoint and the five-/six-turned proof await the next
ordinary push gate. No product, README or release changes are warranted by
these research exclusions.

[Archive checks](h5-one-three-transfer-capacity-20261107/archive-checks.json), [manifest](h5-one-three-transfer-capacity-20261107/raw-manifest.json),
[source bindings](h5-one-three-transfer-capacity-20261107/source-bindings.json), [historical references](h5-one-three-transfer-capacity-20261107/external-evidence.json)
and [runtime pins](h5-one-three-transfer-capacity-20261107/runtime-bindings.json) retain the complete evidence.
