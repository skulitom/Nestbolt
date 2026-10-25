# H5: original-core search and complete second-sheet cog pairs — 2026-10-25

**The full original-core master finishes UNKNOWN without a candidate. A separate
two-cog analysis now completely classifies the second-sheet domain pairs.** Five
combinations have verified placements; the remaining 1,019 are excluded. This
strengthens the next full search but does not qualify a 66-part target layout.
H2/H5 remain open at **60%**.

## Closed full original-core search

The staged master retains all nine mandatory moving originals, the fixed 57,
all 9,776 domain options, both original-area limits, existing conflict/occupancy
constraints and the 130 new guarded exclusions from the previous checkpoint.
Those exclusions add 1,950 physical clauses across all 15 cog pairs. All six cog
anchors use the 71 complete original collision-core pieces, 352 necessary outside
directions per pair, with 5,280 direction variables in total. Exact four-corner
checks cover 2,816 projections. Positive core placements still require the full
guarded-coordinate model; this preliminary relaxation never changes acceptance.

The independent model reconstruction passes **18,530 variables / 34,068 constraints**.
Construction takes **1.082123s**, audit
**0.484307s**. The only master call has a 45-second soft cap,
eight workers and seed zero, inside a shared 60-second pipeline with a two-second
shutdown reserve. It returns **UNKNOWN in 45.305899s**, with no
incumbent. The soft cap overshoots by **0.305899s**;
that overshoot is retained explicitly. Shared elapsed time is
**47.844358s**, within 60 seconds. No selected-coordinate or native
follow-up is opened. The call is closed; no feasibility or impossibility follows.

## Complete second-sheet pair classification

The existing guarded table and earlier exact interval proofs leave 15 of the
32×32 ordered domain pairs unresolved. Each receives a separate, independently
reconstructed two-cog model using its complete inward domains and all 61 full
guarded original collision pieces. At most one two-second call per pair is
allowed, with all construction/audits/solves sharing a60-second diagnostic budget.
This is a separate subproblem, not additional time for the closed full search.

All 15 calls finish in a combined **0.725417s** including preparation:
five feasible and ten infeasible; no UNKNOWN or pending pair. The five feasible
ordered domain pairs are **[1,1], [1,12], [1,17], [12,1], [17,1]**. Independent
integer witness checks verify 32 inward inequalities and 305 full forbidden-piece
clauses. Thus the previously certified at-most-two capacity is attainable in
this fixed-source subproblem; an at-most-one restriction would be incorrect.

The ten solver-negative results are not used as unsupported exclusions. A
separate exact proof procedure applies integer interval deductions, then bisects
a remaining interval when propagation stalls. Every split covers its entire
parent interval. In **0.346853s**, it produces **74 nodes, 540 exact
bound events, 32 binary splits and 42 contradictory leaves**. Independent replay
rebuilds every source rule, verifies every rational floor/ceiling deduction and
unit clause, checks all split coverage, and visits every node without omissions.
All ten trees close. These yield **150 new clauses** across all 15 physical cog
pairs, beyond the exclusions already included in the closed master.

Together, the earlier certificates, ten new proof trees and five positive
witnesses classify **all 1,024 pairs: 1,019 excluded and five feasible**. Negative
scope remains the declared source-angle, inward-domain, guarded integer
construction. No unrestricted packing impossibility is claimed.

## Original-shape and clearance read-back

Each positive pair is rebuilt from the original 80-vertex cog polygon and source
rotation, then checked against the unchanged fixed obstacles and stock. All
**75 same-sheet pair checks** and **40 moving stock-edge checks** pass.
The minimum original separation is **0.212738561201mm**,
above the native requirement **0.211708672510mm**.
The minimum extra stock margin is **0.014296996700mm**,
above the native guard **0.011444091797mm**.
Maximum profile reconstruction error is **2.48e-13mm**.
Every mutual offset also lies outside the full raw and guarded no-fit regions.

The first geometry audit stopped with `KeyError: 'item'` while recording an
original identity; source metadata uses `index`. Its original script, plan and
observed failure are preserved. Correcting that output-field lookup in a separate
audit directory completes the read-back; no witness, guard or solver record changes.

These witnesses contain **only two moving originals against the fixed 57**.
The other seven moving originals remain required. No partial layout is presented
as a full target, and no native validator is called on it.

## Next search and repository state

Use the complete second-sheet classification and 150 new certified clauses in a
distinct full 66-original staged model. The verified pair coordinates may provide
optional hints for interchangeable copies; they must not fix those placements
or remove other mandatory parts. Retain the shared 60-second budget, 45-second
master cap, shutdown reserve, original material target and all validation gates.
Any positive still needs the full guarded-coordinate and 66-original/native
checks, production-budget integration and unchanged 13-job/two-kerf H5 matrix.

Main 61359456 and the offcut documentation remain preserved. Its own
[CI40242602102](https://github.com/skulitom/Nestbolt/actions/runs/40242602102) is **in_progress**, with **5/6** successful jobs
at the saved snapshot; unfinished checks are not counted as passes. This
checkpoint is local. A normal push should follow terminal CI, preserving any
newer remote work and avoiding cancellation of unfinished native checks.

Production source and all three accurate READMEs are unchanged. Preview
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged; no release is qualified.
No native packing, quality run or reserved H2 vector evaluation is performed.
Artem's unchanged H2 gate remains in force, with 22 reserved vectors untouched.

Evidence: [full search audit](h5-original-core-search-20261025/search-audit.json),
[pair/model/proof audit](h5-original-core-search-20261025/pair-audit.json),
[complete classification](h5-original-core-search-20261025/complete-pair-classification.json),
[original-geometry audit](h5-original-core-search-20261025/pair-geometry-audit.json),
[raw archive](h5-original-core-search-20261025/raw-001.zip) and [manifest](h5-original-core-search-20261025/raw-manifest.json).
The archive preserves **406** canonical files and
**209** exact-content aliases, including original inputs,
models, actual parameters, logs, witnesses, full proof trees and failed audit.
Every stored byte length, SHA-256 and ZIP CRC is verified.
