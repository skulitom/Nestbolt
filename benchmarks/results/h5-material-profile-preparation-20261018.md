# Exact material-profile rejection — preparation, 2026-10-18

The [preceding pilot](h5-exact-reject-pilot-20261018.md) validates all 72
outcomes but fails six of eight material comparisons. Exact-state rejection
skips only three of 41 neutral trials. Read-only review of six saved panel
pairs finds identical per-sheet highest original coordinates in every pair,
including five with changed poses. No new geometry or search was used.

This isolated candidate uses the unchanged validator's original-geometry
footprints, transforms, units and grid. Equal profiles require the same
immutable job, sheet-to-stock assignments, exact highest-coordinate bits
and original copy identities. These are sufficient inputs for the existing
charged-material calculation, including outlined stock, margins and defects.
Only same-inventory trials are eligible. Equality rejects a non-improving
trial; it never establishes collision freedom or permits acceptance.
Every accepted exchange still passes the full geometry and strict material
guards. The baseline profile is cached lazily; footprint work is charged
using the existing validated-vertex coefficient. Budgets and coefficients
are unchanged. Public layout conversion is extracted once and reused.

All 123 optimized core tests pass: 117 prior tests unchanged and six new
tests. Before installing the branch, five proof tests pass and the actual
branch regression fails as intended. The original source, executable and
failure log remain. The initial preparation failure also remains preserved.
Twenty-three valid before/after pairs cover saved panel layouts, units,
transforms, outlines, defects, grid boundaries and real improvements.
Forty-seven frozen-CLI checks confirm all witness metrics exactly and reject
the authored overlapping layout despite its equal profile. Twelve actual
branch outcomes pass another 24 frozen-CLI checks, preserving the canonical
incumbent for active, disabled and expired calls across four seeds.

Strict lint/build, ten public outcomes, four CLI comparisons and five pilot
harness tests pass. Normal results and deterministic common replays match
exactly except wall time. Reconstructing and formatting the recorded runtime
substitutions reproduces every candidate source byte. Validator sources match
production; the statistics file adds only one counter.

The planned 72-outcome comparison retains four jobs, two kerfs, three seeds,
rotating sequential three-arm blocks, eight physical CCD0 cores and 60-second
budgets. Block, case, scoring and measurement functions remain AST-identical
to the preceding pilot. The plan is committed before measurement. This is
qualification, not evidence that the material gate passes. The full 13-job
gate stays closed until the smaller pilot succeeds.

All six hosted checks on earlier main `924336a` passed. Production, frozen
inputs, published preview and three READMEs remain unchanged. No integration
or new release is justified by these experimental checks. H2/H5 remain open
and completed milestone weight is 60%.

[Checks](h5-material-profile-preparation-20261018/checks.json),
[proof witnesses](h5-material-profile-preparation-20261018/profile-checks.json),
[branch outcomes](h5-material-profile-preparation-20261018/branch-checks.json),
[source reconstruction](h5-material-profile-preparation-20261018/source-reconstruction.json),
[archive integrity](h5-material-profile-preparation-20261018/integrity.json).
