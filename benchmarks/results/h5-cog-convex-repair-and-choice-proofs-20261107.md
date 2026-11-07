# Convex repair and exact choice conflicts — 2026-11-07

The one-call continuous repair is **infeasible for its selected safe regions**.
An exact source proof explains why: six choices require a **1,288.21 mm**
horizontal span, while their selected-mode stock bounds permit **1,186.94 mm**.
At least one of those choices must change. A distinct bounded choice search
then verifies **256 further contradictory combinations** and stops at its
frozen node limit. Neither result excludes the original continuous domain,
another mode set or any whole allocation. Four fixed arrangements and all
440 allocations remain; H2/H5 stay open at **60% completed milestone weight**.

## Complete model and pinned solver controls

[Independent field readback](h5-cog-convex-repair-and-choice-proofs-20261107/model-audit.json) verifies all **112 variables,
1,730 constraints and 3,952 nonzero coefficients**. The model retains all
28 selected legal modes, all 56 original translation coordinates and stock
bounds, 1,339 source-region rows for all 258 cog interactions, 268 orthogonal
component separators, the 11 required cog X-order constraints, and 112
absolute-motion rows. Its objective minimizes total absolute translation.
Every one of **5,682 coefficient/RHS values** is exactly representable after
power-of-two scaling; six deliberately corrupted models are rejected.

[Solver controls](h5-cog-convex-repair-and-choice-proofs-20261107/solver-controls.json) verify a synthetic feasible and
infeasible LP, then load and read back the entire actual model without solving
it. Every option, bound, objective and sparse matrix entry is checked.
[Tool provenance](h5-cog-convex-repair-and-choice-proofs-20261107/tool-provenance.json) pins installed SciPy 1.17.1 and
embedded HiGHS 1.12.0, with binary hashes and the MIT/BSD license records.
The call uses dual simplex, one thread, seed zero and presolve.

The first preflight stopped before any solver call because its reader expected
row storage after HiGHS had normalized the matrix to columns. The preserved
failure and corrected v2 reader verify mathematical entries in either storage
order. Complete model preparation is **0.231523 s**; the failed verification
takes 2.126282 s and corrected verification 2.367949 s. Neither changes or
repeats the prepared model. One-thread BLAS also reduces import memory.

## Closed response and exact explanation

[Response reconciliation](h5-cog-convex-repair-and-choice-proofs-20261107/response-audit.json) verifies exactly one
source-model LP call. It reports infeasible during presolve after **0.001151 s**,
with 24.871619 s allocated, zero simplex iterations and no assignment.
There is no solve or algorithm overrun. Preparation-inclusive algorithm/shared
totals are **31.130687 / 31.200950 s**; charged preparation is 30.153657 s.
[The Windows Job](h5-cog-convex-repair-and-choice-proofs-20261107/closed-lp-process.json) closes all five processes,
with zero active descendants and **62,181,376 bytes** peak committed memory.
No source candidate or native validation follows.

[Exact interval replay](h5-cog-convex-repair-and-choice-proofs-20261107/interval-proof-audit.json) verifies 163 bound
deductions, rounded outward so they remain valid for continuous coordinates.
Its contradiction depends on only six source rows and five prior deductions.
[Independent summation of those six rows](h5-cog-convex-repair-and-choice-proofs-20261107/six-region-chain.json) gives
the span contradiction above: **101.27 mm** more than the allowed range.
This explanation does not depend on trusting floating-point infeasibility.
It refutes only these selected region choices under their current modes.

## Closed proof-guided choice search

The new search reuses that proved root and changes region choices jointly.
It orders distinct combinations by total source-region rank, with deterministic
ties; each exact contradiction branches only on choices in its dependency
core. Every node retains all original modes, stock bounds, orthogonal
separators and cog ordering. There are no numerical LP calls in this search.

[The frozen 256-node search](h5-cog-convex-repair-and-choice-proofs-20261107/choice-search.json) stops normally after
**2.173843 s**, below its eight-second internal cap. Its [complete process](h5-cog-convex-repair-and-choice-proofs-20261107/choice-process.json)
takes **2.702245 s**, closes both processes and peaks at 137,736,192 bytes.
All 256 combinations have exact contradictions. **1,350 queued states remain
unsearched**, with minimum pending rank sum four; no larger-domain conclusion
is justified and this search will not be extended.

[Independent replay](h5-cog-convex-repair-and-choice-proofs-20261107/choice-audit.json) verifies **47,804 exact bound
deductions**, 308 used pair/region choices and 1,618 independently reconstructed
source planes, plus every branch, tie, deduplication and terminal contradiction.
[The 256 resulting choice conflicts](h5-cog-convex-repair-and-choice-proofs-20261107/certified-choice-nogoods.json),
along with the original six-choice conflict, provide 257 constraints for a
different model that chooses all source-safe regions together.

## Next construction and unchanged gates

[The next specification](h5-cog-convex-repair-and-choice-proofs-20261107/next-step.json) first clips every candidate
region against its exact selected-mode relative stock bounds. It then proposes
joint region selectors coupled to the original 56 coordinates, complete source
planes and all 257 certified choice conflicts. Every field and tool control
still requires independent review before one newly frozen call. No such model
or call is prepared in this checkpoint.

[The complete charge before new geometry/model building](h5-cog-convex-repair-and-choice-proofs-20261107/next-preparation-charges.json)
is **34.464716 s**: the entire consumed convex process, the conservatively
charged complete proof command, and complete choice preparation. The original
candidate/projection/model costs are already inside that process and must not
be counted twice. [The proof command charge](h5-cog-convex-repair-and-choice-proofs-20261107/interval-proof-complete-charge.json)
includes its separate audit conservatively; this standard-library command used
internal limits and was not a Windows Job run. Other verification is separate.

Full66 original-source checks, native/material checks, production integration
and UI/CLI/MCP parity, and the full unchanged H5 matrix remain required. H2
retains its original gate and unopened reserved vectors. No release or README
change is warranted by these research results. [All six current-main CI jobs
pass](h5-cog-convex-repair-and-choice-proofs-20261107/main-ci-at-review.json); these evidence commits can now undergo the
ordinary guarded fast-forward push. No live run is cancelled.

A checkpoint packaging reader also stopped on a top-level JSON list. Its
partial charge records and source bytes are retained; v2 checks object inputs
and hashes list documents without repeating any construction or search.

[Raw evidence](h5-cog-convex-repair-and-choice-proofs-20261107/raw-manifest.json) contains 85
canonical members and 1,785,115 ZIP bytes. [Historical references](h5-cog-convex-repair-and-choice-proofs-20261107/external-evidence.json)
and [source bindings](h5-cog-convex-repair-and-choice-proofs-20261107/source-bindings.json) retain every consumed input,
including earlier frozen failures. Independent archive verification is required
before commit.
