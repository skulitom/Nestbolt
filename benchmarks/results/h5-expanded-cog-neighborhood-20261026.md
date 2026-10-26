# H5: expanded cog neighborhood — 2026-10-26

**Fresh geometry for 12 mandatory movers and 54 fixed originals is verified.**
This releases neighboring original cogs **53, 56 and 61** in addition to the
previous nine movers. All 66 originals remain required. No new solver call,
complete target or native acceptance occurs. H2/H5 stay open at **60%**.

## Fresh regions and preserved inventory

The three released cogs already use the same source angle and original profile
as the six previously moving cogs. All ten profiles and 100 independently
certified fixed-style collision obstacles therefore remain reusable unchanged.
Recompute all 20 free regions using only the retained 54 original placements:
47 on sheet 1 and seven on sheet 2. Their transforms remain unchanged.
The moving inventory is two brackets, one insert and nine cogs.

Fixed area charges are recomputed to **3,681,713,590 / 249,662,718** units of
0.001 mm². The material target, native guards, 0.2125 mm construction clearance,
clearance-envelope margin and stock margins remain unchanged. No old fixed57
domain table, regional capacity, occupancy/no-good or source-area exclusion is
transferred to the expanded search space.

An independent audit reconstructs every new region by sequentially subtracting
the cached obstacles in reverse order. Its maximum Hausdorff difference from
the producer's union-subtraction result is zero. All 1,102 retained fixed-pair
checks pass. The old regions have zero recorded lost area. Exact containment
reports true for 19 queries and false for the first-sheet cog query; that
numerical boundary discrepancy remains recorded, without an exhaustive
containment claim. Sheet 2 is unchanged.

## Explicit repair of a prior partial anchor

The previous **63-original partial** is still geometrically valid under the
original native guards. But original cog 53's continuous source anchor and
nearest grid point lie outside the stronger moving-construction free region.
That original exclusion is preserved.

For each newly released cog, enumerate exactly the nine nearest-grid points
offset by −1, 0 or +1 micrometre in each direction. Keep the six prior witness
cog positions fixed for this diagnostic. Check all **27 points**, **358 source
pair cases**, **973,760 integer inequalities** and **729 triples**. Exactly
**54 triples** pass. Independently verify every result and the exact rational
minimum-shift ranking. The selected changes move an anchor axis by at most
**0.001428556 mm**, including rounding from the original continuous pose.

Reconstruct all 63 actual original outlines and their **83 cutouts / 9,172
cutout vertices**. All **1,467** same-sheet pair checks and **252** stock-edge
checks pass; minimum pair gap is **0.212500 mm**, above the unchanged native
guarded requirement **0.211709 mm**. All 22 selected moving-cog pair relations
pass the full original source clauses. The 54 fixed transforms and six earlier
witness positions remain unchanged. This remains a partial missing brackets
**28/29** and insert **50**; it is not a cutting layout or H5 result.

## Complete inward-domain preparation

The new regions produce **3,718 raw convex faces**, **3,716 inward integer
domains**, two explicitly recorded discards and **12,631 inward halfplanes**.
No merge/time/face cap fires and no positive-area raw coverage gap is recorded.
Every inset, discard, bound and rational coefficient-error rounding is independently
checked. All nine repaired partial anchors belong to at least one new domain.

The 82 original mutual profile-pair files are reused byte-for-byte, with their
committed independent geometry proof and all **27,256** outside-plane rounding
checks verified again. The fresh inventory covers **66 physical pairs** and
**538 same-sheet query-pair modes**. These are constructive finite-angle/grid
domains, not an unrestricted packing proof.

Next build and independently audit a fresh 12-original coordinate model from
these domains. Recompute all difference-bound reductions and any additional
capacity certificates; require all three missing originals. Use the checked
partial only as advisory hints. Full 66-original geometry/native validation,
production integration and the complete 13-job/two-kerf matrix remain necessary.
All earlier solver calls remain closed.

The prior two-checkpoint push to **d1645404** is retained with its receipt.
At 02:08 UTC, [its CI 40256286467](https://github.com/skulitom/Nestbolt/actions/runs/40256286467)
is running with four jobs passed. Preserve that run before another normal push.
Upstream state, production and READMEs are unchanged. No new release is qualified;
preview v0.2.0-alpha.1 and stable v0.1.0 remain appropriate. H2 retains its original
gate and all 22 reserved vectors remain untouched.

Evidence: [region audit](h5-expanded-cog-neighborhood-20261026/region-audit.json),
[complete local-census audit](h5-expanded-cog-neighborhood-20261026/anchor-census-audit.json),
[three small shifts](h5-expanded-cog-neighborhood-20261026/verified-anchor-shifts.json),
[joint-domain audit](h5-expanded-cog-neighborhood-20261026/joint-domain-audit.json),
[checks](h5-expanded-cog-neighborhood-20261026/checks.json), and [raw manifest](h5-expanded-cog-neighborhood-20261026/raw-manifest.json).
**331** canonical files and **250**
exact-content aliases are size/SHA-256/CRC verified in **1**
independently readable archive part(s).
