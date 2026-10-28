# Union-cover resolution and short-sheet transfer — 2026-10-28

Two distinct complete-layout trials closed **UNKNOWN without a candidate**.
The 10 mm cover substantially reduces setup cost, but neither trial proves
that all 66 originals fit or that they cannot fit. The next construction uses
an existing, independently revalidated short sheet containing one cog, allowing
a different first-sheet arrangement. H2/H5 remain open at **60% milestone weight**.

Both models keep **all 51 first-sheet originals movable** as 39 mandatory
blocks, plus the fixed short-sheet 15. All 228 variables, 111 mode choices,
35 conditional symmetry orders, source bounds and cover constraints are
independently read from the saved protobufs. Source clearance and all original
identities/holes are retained. A valid 56-part control fails exactly the ten
missing-part requirements in each actual target model. A separate audit copy
changing only those requirements passes every constraint. Complete negative
controls correctly fail with **825 original-source collisions**, while retaining
90 holes and 10,026 hole vertices. Their cover collision counts are 15,138 and
8,226; NoOverlap2D and both cumulative constraints reject them.

| Complete model | 5 mm vertical cover | 10 mm vertical cover |
|---|---:|---:|
| Rectangles per cog row | 523 | 253 |
| Component options / constraints | 1,725 / 3,788 | 915 / 2,168 |
| Search begins in solver log | 18.87 s | 3.16 s |
| Allocated solve time after setup | 59.218313 s | 59.348857 s |
| Returned solve time | 59.261779 s | 59.371190 s |
| Solve soft overrun | 0.043466 s | 0.022333 s |
| Total algorithm / shared time | 60.048065 / 60.115243 s | 60.026304 / 60.081107 s |
| Returned worker branches / conflicts | 1,248 / 38 | 11,409 / 659 |
| Complete candidates | 0 | 0 |

Each call has its own predeclared **one-call, 60-second algorithm / 90-second
shared** budget, four workers, seed zero and `fj` disabled. Startup, input
checking and any candidate source readback count in the algorithm budget.
The **0.048065 s and 0.026304 s algorithm overruns** are preserved. Worker
counters are not totals across workers. Every saved response, runtime parameter
and model field is audited. Both calls are closed; no unused time is reassigned.
No original-source infeasibility or H5 runtime/material claim follows.

The 10 mm trial follows a finite, frozen **four-variant geometry study**, not
another run of the same model. The selection rule requires a source-valid
56-part control, no cover collisions and at most 20,000 mm² added cover area
per row, then selects the fewest rectangles. All four variants preserve the
full square-expanded original source; independent coverage checks include
390 triangle-square hulls per variant.

| Variant | Rectangles per row | Added area per row | Control / selection |
|---|---:|---:|---|
| Vertical, 10 mm | 253 | +12,304.401160 mm² | Valid; selected |
| Vertical, 20 mm | 114 | +29,933.534936 mm² | Valid; exceeds study's area policy |
| Horizontal, 5 mm | 556 | −1,171.681210 mm² | Valid; more components |
| Horizontal, 10 mm | 278 | +9,164.158790 mm² | Five stock-check failures |

The failed horizontal control and all unselected variants remain preserved.
Their outcomes concern these controls and the declared selection policy, not
global packing feasibility. The selected vertical control uses **270.980 mm**
row spacing and passes **310,078 cover pairs** and all 925 original-source pairs.
Its model retains all ten missing originals as mandatory. The earlier convex-
hull height certificate is not reused for these different row shapes.

The next direction changes the allocation using a previously verified short
sheet: **seven brackets, four inserts and one cog** in their exact saved poses.
Fresh original-source readback passes **66 pairs, 48 stock edges, 26 holes and
3,250 hole vertices**, with minimum gap **0.224308673 mm** and minimum extra
stock clearance **0.0126 mm**. The unchanged first/short stock bounds and material
target are retained. A summary-field typo is preserved; a separate independent
reader completes the source and identity audit.

That short sheet leaves **18 frames, five brackets, 17 inserts and 14 cogs**
mandatory on the first sheet. The preflight accounts for all 66 originals
exactly once and identifies the existing unexcluded frontier entry. The count
of 444 necessary allocations is unchanged. A prospective construction has
**43 movable blocks**: 40 orthogonal originals and cog rows of **5 / 5 / 4**.
No new first-sheet placement, row geometry or packing model is claimed yet.

The next model must distinguish four-cog and five-cog modes and apply symmetry
only to identical rows. Every first-sheet original remains movable; the old
26-part core may supply partial-control hints only. A complete candidate still
requires original 66-part validation, native checks and material accounting,
then production integration and the full unchanged H5 matrix. Common-line
part-in-hole stays off. The valid 64-part layout and 22 unopened H2 vectors
remain preserved; the original H2 gate is unchanged.

Main remains **75ee537c**. The previous checkpoint **b0468c71** is queued behind
[CI 40764537562](https://github.com/skulitom/Nestbolt/actions/runs/40764537562),
which has five successful jobs and Windows checks running in this snapshot.
Both queued checkpoints require all six jobs and fresh remote checks before a
normal atomic push. Production, READMEs and upstream heads/releases are unchanged.
No new release qualifies.

Evidence: [5 mm model audit](h5-union-cover-resolution-and-transfer-20261028/union5-model-audit.json),
[5 mm closed response](h5-union-cover-resolution-and-transfer-20261028/union5-response-audit.json),
[four-variant geometry audit](h5-union-cover-resolution-and-transfer-20261028/axis-study-audit.json),
[10 mm model audit](h5-union-cover-resolution-and-transfer-20261028/slab10-model-audit.json),
[10 mm closed response](h5-union-cover-resolution-and-transfer-20261028/slab10-response-audit.json),
[short12 transfer audit](h5-union-cover-resolution-and-transfer-20261028/transfer-preflight-audit.json),
[next step](h5-union-cover-resolution-and-transfer-20261028/next-step.json), [raw manifest](h5-union-cover-resolution-and-transfer-20261028/raw-manifest.json).
The verified archive contains 461 canonical files and 484
identical-byte aliases in 1,982,239 compressed bytes, including complete
models, controls, failures, closed responses, geometry studies and source inputs.
