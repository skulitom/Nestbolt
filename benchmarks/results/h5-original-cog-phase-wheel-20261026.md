# H5: original-cog phases and a finite seven-cog obstruction — 2026-10-26

**The declared 15-cog triangular-grid construction is infeasible at all five
tested pitches and 36 tested angles.** An independent enumeration explains
the result with seven cogs: their contact constraints cannot all hold together.
This closes one finite construction, not the full placement problem. All six
remaining brackets and three inserts still require placement. H2/H5 remain
open at **60%** by completed milestone weights.

## Declared construction and source geometry

Keep the checked 27 first-sheet originals and fifteen short-sheet originals.
Require all fifteen remaining cogs in three staggered rows of five. Test
pitches 260, 262, 264, 266 and 268 mm, with each cog independently choosing an
actual original rotation from 0° through 17.5° in 0.5° increments. No exact
tooth symmetry is assumed. This phase-only preparation excludes all nine
remaining non-cogs from the model; they remain mandatory before any full-layout
claim. No old owner-dependent domains are reused.

The constructor computes **19,440 original-outline pair distances** across
fifteen pitch/direction tables. The independent audit rebuilds the actual source
vertex transforms for **194,400 near-pair angle combinations**, covering all
thirty near neighbors at all five pitches. The largest difference caused by
translating those reconstructed shapes is below 9 × 10⁻¹³ mm. The other 75
pairs have center separation greater than twice the verified 140.001 mm source
radius plus the construction clearance. All 105 cog pairs are accounted for.

The construction uses 0.225 mm clearance. No saved distance falls between the
required native guard clearance and 0.225 mm, so changing between these two
thresholds would not change these finite compatibility tables.

## One call and an independently checked explanation

The model has **16 variables and 30 compatibility constraints**: one pitch and
fifteen independent angles. A separate protobuf reconstruction verifies every
variable domain and allowed tuple, with no objective or hint.

The sole call closes **INFEASIBLE** during presolve. Internal solver time is
**0.169084 seconds**, returned-call time
**0.170663 seconds**, and shared-process time
**1.124359 seconds**. The declared limits are
20 solver seconds and 30 shared seconds; neither is exceeded. No retry,
reseed or extension is permitted for this closed construction.

A single triangle admits respectively **0, 0, 8, 28 and 124** phase assignments
at the five pitches. Pair or triangle feasibility therefore does not establish
feasibility of a repeated grid. For the seven-cog wheel centered on lattice node
6, every pitch has zero closing assignments. A dynamic-programming certificate
contains **458** reachability records. An independent depth-first enumeration
of **618** prefixes reproduces every record exactly and finds zero complete
wheel assignments. This also explains the 15-cog model's negative result
without relying solely on its solver status.

The certificate covers only the declared positions and finite angles. It does
not exclude continuous rotation, independent center shifts, a different contact
graph, or the fixed27 neighborhood. No original layout, native validation,
material improvement or production-budget qualification follows from it.

## Next work and repository checkpoint

The next construction must allow different cog contacts and couple them to all
six remaining brackets and three inserts. Use fresh current-owner geometry.
The 42-original core and earlier 64-original partial remain preserved. Full66
source/native/material validation, production integration and the complete H5
matrix remain required. The older wide-frame grid and eleven-insert side strip
already have retained finite-search evidence; they must not be presented as new.

Commit **6c5bf878** is verified on `main`, pushed normally after all six jobs in
[the preceding CI run](https://github.com/skulitom/Nestbolt/actions/runs/40336537934)
passed. At 2026-10-26T15:01:48.011030+00:00, its
[new CI run](https://github.com/skulitom/Nestbolt/actions/runs/40343656177)
is in_progress, with 4 successful jobs.
Queue this new evidence checkpoint until that run finishes successfully.
Production and README digests are unchanged; no new release is qualified.
H2 retains its original gate and all 22 reserved vectors remain untouched.

All four audits pass. [Checks](h5-original-cog-phase-wheel-20261026/checks.json),
[geometry](h5-original-cog-phase-wheel-20261026/geometry-audit-checks.json),
[model](h5-original-cog-phase-wheel-20261026/model-checks.json),
[response](h5-original-cog-phase-wheel-20261026/response-audit-checks.json),
[independent wheel enumeration](h5-original-cog-phase-wheel-20261026/wheel-audit-checks.json),
[scope](h5-original-cog-phase-wheel-20261026/scope.json), [next step](h5-original-cog-phase-wheel-20261026/next-step.json), and
[raw manifest](h5-original-cog-phase-wheel-20261026/raw-manifest.json). The archive verifies
44 canonical files and 12
aliases by exact bytes, SHA-256 and CRC.
