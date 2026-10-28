# Separate cog edge contacts — 2026-10-28

The contact correction permits 80 valid moves, but the packet becomes only
**0.236005 mm shorter while growing 9.392841 mm wider**. It does not solve the
mechanical material requirement. This isolated height search is closed; the
next formulation must place the missing mixed parts. H2/H5 remain open at
**60% completed milestone weight**.

The model retains separate distances from original cog vertices to original
edges, instead of differentiating a single minimum-distance function. Original
stock vertices are also kept separate. Every point's motion is bounded by
translation norm plus radius times angle change, rounded upward in 0.000001 mm increments.
The maximum initial point displacement is 3.439293 mm; the pair-feature window
is 7.102607 mm. This covers every feature that could approach the construction
clearance within the declared step. Linearized constraints still propose moves
only; full original polygons decide acceptance.

The preflight checks 238 initial rows (36 stock / 202 pair), all 1,344,000
vertex-edge distances and 6,000 stock-vertex distances, 1,335 active derivative
entries, objective, bounds and the feasible zero step. The source control
passes all 105 pairs, 60 edges, 15 holes and 3,000 hole vertices. For the saved
unsafe direction from the preceding experiment, the new model predicts a
−0.000350522 mm residual; the original source check confirms it. Maximum feature
prediction error for that check is 4.92e-8 mm.

The sole predeclared sequence stops at **80 iterations**, after 232 backtracking
trials and 233 full source-acceptance evaluations. These counts exclude the
separate feature enumerations used to build each LP. Search takes **8.964570 s**
and shared time **12.407827 s**, within the 60/90-second limits. No restart or
extension occurs. The preserved SciPy warning reports that the one-thread option
is forwarded to HiGHS.

Independent readback checks every one of the **81 accepted states**, including
the initial control, and all **232 trials**. It reconstructs all 80 feature
windows and LPs, performing **107,520,000 vertex-edge distance checks** and
**57,283 active derivative checks**. Maximum derivative discrepancy is 1.15e-8.
Every accepted state retains all original holes. The 152 rejected trials that
meet the looser physical source threshold remain rejected under the frozen,
stricter proposal rules.

| Best final packet | Value |
| --- | ---: |
| Actual height | 771.963626616 mm |
| Actual width | 1,445.843185057 mm |
| Height gain from control | 0.236004500 mm |
| Width cost | 9.392840842 mm |
| Minimum source gap | 0.224014009 mm |
| Minimum extra stock clearance | 0.013020174 mm |
| Angle range | 6.273079°–7.324893° |

Top decreases by 0.237464431 mm, including translation; physical height gain is
only 0.236004500 mm. No optimum or full66 result is claimed. The other 51
originals remain required, and this wider packet is not transplanted into the
previous valid64 layout.

The next investigation uses conservative outer rectangle covers and a different
NoOverlap2D formulation for **all 25 remaining originals together** around the
verified mixed26 core and short15. Covers must contain the complete expanded
source polygon; the previously audited *contained* capacity rectangles cannot
serve as outer covers. Coverage, partitioning, integer rounding, stock domains
and all placement links must pass independent checks. A 56-original control
may validate geometry and constraints, but the actual target must retain all
25 movers and account for all 66 originals. This is a new constructive subset,
not a restart of the closed no-fit-cell call. Full original-source, native and
material validation remain prerequisites for integration and the H5 matrix.

Main remains 8713c6e1. Five jobs pass in
[CI 40742366525](https://github.com/skulitom/Nestbolt/actions/runs/40742366525);
Windows checks are live. Queued verified checkpoints wait for all six jobs and
fresh remote guards before normal push. Production, READMEs and upstream heads
and releases are unchanged. The previous valid64, 444 necessary allocations,
original H2 gate and 22 unopened reserved vectors are preserved. No release
qualifies.

Evidence: [preflight](h5-cog-feature-source-20261028/preflight-audit.json),
[saved unsafe-direction check](h5-cog-feature-source-20261028/rejected-direction-check.json),
[all source/model audits](h5-cog-feature-source-20261028/source-audit.json),
[accepted source states](h5-cog-feature-source-20261028/accepted-source-states.json),
[next step](h5-cog-feature-source-20261028/next-step.json),
[raw manifest](h5-cog-feature-source-20261028/raw-manifest.json).
The archive preserves 533 canonical files and
361 identical-byte aliases in 2,807,235
compressed bytes, including every source readback, proposal, trial and input.
