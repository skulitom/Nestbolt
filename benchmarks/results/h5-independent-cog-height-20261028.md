# Independent cog-height optimization — 2026-10-28

The source-valid cog packet becomes only **0.126980 mm shorter** than the packet
in the earlier source64 layout, while becoming **41.066861 mm wider**. This does
not solve the material requirement. The sole fixed-angle call is closed and
not a proven optimum. H2/H5 remain open at **60% completed milestone weight**.

This model differs from the closed triangular phase table, oblique construction
and finite-pool cover: every one of the 15 cog positions is independent within
the full usable stock width, and the objective is the maximum source top.
There is no fixed lattice, pitch, row count or cog position. The angle remains
the audited 7° constructive subset; no free-angle coverage is claimed.

The complete guarded control uses 258.90 mm horizontal pitch, 80 mm alternate
offset and 246.25 mm row pitch. It passes all **105 original source pairs, 60
stock edges, 15 holes / 3,000 hole vertices**, and every occupied pair cell.
Its actual height is 772.448399 mm. This avoids treating the older source-valid
but less conservative clearance as a valid rounded hint for the no-fit model.

The independent geometry audit checks 6,084 source Minkowski hulls, 124 convex
relative cells, 430 conservative integer halfplanes and 92 source-contained
rectangles, with 7,360 exact source-edge and 4,186 same-owner rectangle checks.
Stock domains and the exact source-area lower bound are reconstructed. Necessary
X/Y capacities use 1,380 contained components and add no bounding-box exclusion.

The serialized model audit checks **13,051 variables, 48,046 constraints, 30
independent coordinates, all 105 source pairs, 13,020 cell choices and every
value of the complete feasible hint**. Its top objective is explicitly audited.
The sole 60-second, four-worker call returns **FEASIBLE**, with five incumbents.
Solver time is 60.049336 s, returned time 60.057713 s and shared time 61.047461 s.
The returned soft overrun of **0.057713 s** is preserved. The top objective is
778.717 mm and solver bound 511.526 mm, so no optimum is established. Zero
returned branch/conflict counters do not establish that the worker portfolio
performed no search.

Every incumbent and the final assignment pass the independent saved-model reader.
Every incumbent also passes original-source geometry, stock, angle and hole
readback. Final minimum source gap is **0.224621810 mm** and extra stock clearance
**0.013800281 mm**. The final actual bounds are approximately
(6.513800, 6.513800)–(1,442.961200, 778.716200) mm.

| Source packet | Actual width | Actual height |
| --- | ---: | ---: |
| Earlier valid64 cog packet | 1,395.380539 mm | 772.329379 mm |
| Guarded positive control | 1,395.548399 mm | 772.448399 mm |
| New independently positioned packet | 1,436.447399 mm | 772.202399 mm |

The model top decreases by 0.258 mm, but 0.012 mm comes from translation toward
the stock edge. Actual height decreases only **0.246 mm** from the guarded
control. Relative to the earlier valid64, the 0.126980 mm height gain costs
41.066861 mm of width. The packet is not transplanted into that layout; doing so
would require checking every other original neighbour. All 51 non-cog originals
remain obligations, and no native, full66 or H5 result is claimed.

The next investigation changes the angle variables as well as positions. It must
construct polygons directly from original source vertices for every changed
angle; the fixed-angle no-fit cells and contained rectangles cannot simply be
reused. Start from the newly valid source packet, audit the objective and all
pair/stock/top constraints, scale numerical variables explicitly, and declare a
single bounded nonlinear call only after the positive control passes. A failed
local solve will not justify restarts or an impossibility claim. Any useful
packet still needs all complementary originals and full source/native/material
validation before integration or the H5 matrix.

Main remains **2adfa569**. At this review CI 40735870933 has five passing jobs;
Windows checks remain live. The verified mixed-core commit **05a7232c** and this
checkpoint wait for all six jobs and fresh remote guards before a normal push.
Production and all READMEs are unchanged. Sparrow remains 6f7b9d35 / v0.3.0;
Studio remains c0bb9e86 without a release. No stop rule fires. The previous
valid64, 444-count frontier, original H2 gate and all 22 unopened reserved vectors
remain preserved. No release qualifies.

Evidence: [source geometry](h5-independent-cog-height-20261028/source-geometry-audit.json),
[complete model](h5-independent-cog-height-20261028/model-audit.json),
[response](h5-independent-cog-height-20261028/response-audit.json),
[source extents and tradeoff](h5-independent-cog-height-20261028/source-audit.json),
[every source incumbent](h5-independent-cog-height-20261028/source-incumbents.json),
[next step](h5-independent-cog-height-20261028/next-step.json),
[raw manifest](h5-independent-cog-height-20261028/raw-manifest.json).
The archive contains 75 canonical files and
45 identical-byte aliases in 1,492,993
compressed bytes, including all models, incumbent assignments, source readbacks,
inputs and closed-call records.
