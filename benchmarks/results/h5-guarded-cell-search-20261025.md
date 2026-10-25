# H5: guarded full search and a verified six-cog construction — 2026-10-25

**The full guarded-cell master remains UNKNOWN. A smaller diagnostic finds four
first-sheet cog placements, giving a verified six-cog construction with the
known second-sheet pair.** Together with the fixed 57, all 63 placed originals
clear the original native guards. Two brackets and one insert remain required.
No full target layout is claimed; H2/H5 remain open at **60%**.

## Full guarded-cell search, closed

The master retains all 66 originals, all 9,776 domain options, both original-area
limits and every existing occupancy/pair exclusion. It replaces the necessary
raw-core cog conditions with the independently proved 229+4 guarded displacement
cells. Every same-sheet pair chooses one cell for that sheet; different-sheet
pairs activate none. Independent reconstruction verifies all 16,775 variables /
46,383 constraints, including 30 sheet-activation flags, 3,495 cell flags, 6,990
chosen-cell box bounds, 12,465 cell halfplanes and 16 advisory hints. Boolean
activation truth tables are exhausted. No hint fixes a placement or removes a part.

Construction takes **1.253357s**, model audit
**0.560022s**. The single 45-second/eight-worker/seed-zero call
returns **UNKNOWN in 45.666246s** without an incumbent. Its soft-cap
overshoot is **0.666246s**, explicitly retained.
Shared pipeline time **48.579203s** stays within 60 seconds.
No full-coordinate or native follow-up is opened. This closed call proves neither
feasibility nor impossibility. The extra 0.010 mm first-sheet construction
restriction from the cell preparation remains explicit.

## Four first-sheet cogs and six-cog read-back

The existing exact second-sheet capacity is at most two cogs. A full placement
of six moving cogs therefore needs at least four on the first sheet. A separate
diagnostic keeps **four mandatory original cogs, all 735 first-sheet domains per
cog, every domain's integer box and inward halfplanes, applicable regional
limits, the global three-region exclusion and all 229 guarded pair cells**.
The other five moving originals are absent only from this subproblem and remain
mandatory for the full job. No partial acceptance or objective is introduced.

Its independent oracle verifies **4,329 variables / 23,991 constraints**, with
no hints. The sole 45-second-cap call returns a feasible assignment (`OPTIMAL`
is the satisfaction-solver status) in **7.753828s**; complete
elapsed time is **8.201210s**, inside the separate 60-second budget.
The call is closed. The four domain rows are **3, 31, 72, 734**; every chosen domain,
cell, regional bound and original guarded inequality passes read-back.

Combining those positions with the previous second-sheet [1,1] witness assigns
all six interchangeable original copies without changing their source angle.
All **seven same-sheet cog pairs / 427 complete original guarded clauses** pass.
The six positions are available as advisory hints; they are not fixed in the
next full search.

## Original geometry and failed sampled completion

Rebuilding the six cogs and all 57 fixed originals from actual job polygons
verifies **63 distinct original identities**, **1,467 same-sheet pair checks**
and **252 stock-edge checks**. Minimum original separation is
**0.212500000000mm**, above the native requirement
**0.211708672510mm**. Minimum extra stock margin is
**0.012500000000mm**, above the native guard
**0.011444091797mm**. Maximum reconstruction error is
**5.08e-13mm**. Missing items
**28, 29, 50** (two brackets and one insert) are recorded explicitly; no native
validator is called on the partial layout.

A separate deterministic completion sample tests all 18 allowed bracket/insert
queries. Rational vertex-to-mean interpolation and floor/ceil micrometre
neighbours generate **162,863 points**, yielding **103,036 unique source-valid
poses**. Every point is tested against all fixed cogs on its sheet using the full
guarded original inequalities. **Zero bracket poses and eight insert poses**
survive. The sampler finishes in **2.016014s**, with no pending query.

Independent read-back regenerates the complete declared sample and supplies a
failed source-clause certificate for every one of the **103,028 rejected poses**.
It verifies **4,858,271 failed inequalities with arbitrary-precision integers**,
and all **672** full clauses for the eight accepted poses. This proves the
finite sample cannot complete the fixed six-cog arrangement. It does **not**
exclude unsampled positions, other cog arrangements or unrestricted packing.

Next keep all six cogs movable and use the verified positions only as hints.
Add explicit selected-domain integer boxes for all 6×767 cog-domain choices,
as in the successful smaller diagnostic: 9,204 redundant conditional bounds.
These bounds preserve every allowed integer position. Independently audit the
new full model and hints before a distinct bounded call. All 66 originals, the
material target, native guards, full-coordinate follow-up and complete H5
requirements remain unchanged. A positive must still reach production-budget
integration and the original 13-job/two-kerf matrix.

## Repository and evidence

Main 61359456 and its offcut documentation remain preserved. Its own
[CI40242602102](https://github.com/skulitom/Nestbolt/actions/runs/40242602102) is **in_progress**, with **5/6** successful jobs
at the saved snapshot. This checkpoint remains local pending terminal CI, so
the Windows check is not cancelled by a push. Production source, all three
accurate READMEs, preview v0.2.0-alpha.1 and stable Latest v0.1.0 are unchanged.
No new release is qualified. No native packing, quality run or held-out
evaluation occurs; all 22 reserved H2 vectors remain untouched.

Evidence: [full model audit](h5-guarded-cell-search-20261025/model-audit.json),
[terminal budget audit](h5-guarded-cell-search-20261025/search-audit.json), [four-cog audit](h5-guarded-cell-search-20261025/four-cog-audit.json),
[63-original geometry audit](h5-guarded-cell-search-20261025/original63-geometry-audit.json),
[sample audit](h5-guarded-cell-search-20261025/completion-sample-audit.json), [archive](h5-guarded-cell-search-20261025/raw-001.zip)
and [manifest](h5-guarded-cell-search-20261025/raw-manifest.json). The archive retains
**333** canonical files and **68**
exact-content aliases, including complete models, parameters, logs, original
layouts, every sampled point and rejection certificate, with size/SHA-256/CRC verification.
