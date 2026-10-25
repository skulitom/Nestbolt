# H5: exact-count direct-coordinate selection — 2026-10-25

**CP-SAT reports `INFEASIBLE` for the checked grid model with fixed core 0.**
It returns no layout. This closes this particular inner-domain search, but
does not prove the original continuous placement problem or another fixed
arrangement impossible. H2/H5 remain open at **60%** completed milestone weight.

## Certified removal of redundant domains

The previous independently checked domains remain preserved. Exact rational
clipping reconstructs all 3,703 domains. One predeclared 30-second/500,000-check
containment phase takes **1.082580 seconds** and
7,268 comparisons. It removes **26** domains only when a retained domain in
the same orientation and sheet contains their entire bounded rational region.
All **3,677** retained domains remain eligible: 2,412 for brackets and 1,265
for inserts, giving **55,509** per-copy alternatives for the exact inventory.
No limit is reached and no incomplete comparison phase is resumed.

A separate boundary-line intersection oracle reconstructs every removed
source domain, independently of the clipping routine. It verifies 121 vertices
against 1,166 target inequalities. Each removal preserves every allowed grid
coordinate, orientation and sheet assignment. No arbitrary pose pruning occurs.

## Complete model verification

The model contains **60,537 variables** and **306,319 constraints**. It fixes
the original 18 frames and 15 cogs from core 0 and requires all **12 brackets
and 21 inserts**, with no objective or unplaced-part variable. Every physical
small part has shared anchor coordinates and exactly one orientation/sheet
mode. Its active mode selects one of the certified convex domains and applies
every inward-rounded halfspace and stock bound.

Each L bracket uses its exact two rectangular arms; their offsets share the
same mode and anchor. The model includes all **528** distinct physical-part
pairs and all **978** cross-part rectangle-component pairs. Same-sheet pairs
must have at least 0.22 mm separation along one axis. The arms belonging to the
same bracket are never separated from one another. Thirty-one ordering
constraints only permute identical copies by sheet/y/x. All permitted original
orientation/reflection aliases remain accounted for.

An independent protobuf reconstruction checks every variable, constraint and
parameter, including all 55,509 domain-choice booleans and 276 orientation/sheet
modes. No additional model fields or hidden objective are present. Model
preparation and that complete comparison take **4.669777 seconds**.

## One bounded search and its actual scope

Exactly one 60-second, eight-worker, seed-zero call is made. Ordinary presolve
is enabled; presolve probing and automatic symmetry discovery are disabled.
The normal worker portfolio still includes a probing search worker. The log
reaches search at **10.09 seconds** and records `#Done 59.73s no_lp` before
returning `INFEASIBLE`. Actual elapsed time is **60.354444 seconds**;
the soft overrun is preserved, without a retry or extension. The response
records 218,662 branches and 22,653 conflicts. There is no returned incumbent.
No separately checked LRAT proof is present; this is the solver's result for
the independently checked model.

This model is a conservative subset of original placements: it uses a 0.01 mm
grid, inward-rounded safe domains, 0.22 mm new-part gap, 0.02 mm additional
stock margin and axis-wise component separation. Original required part gap
is 0.2 mm. Those construction restrictions can exclude valid continuous
placements. Therefore the result does not establish that core 0 must move,
that the original target is impossible, or that H5 can be relaxed.

## Next continuous-coverage question

Investigate an independently checked outer coordinate relaxation for fixed core 0 before changing the fixed arrangement or repeating inner-domain search. Keep the full original 12-bracket/21-insert inventory and all 18 frames/15 cogs. Construct outer translation domains covering every original permitted continuous placement, with explicit allowances for grid quantization and numerical geometry, rather than reusing inward-safe domains as if exhaustive. For cross-part axis-aligned rectangle components, drop positive clearance and allow the grid-rounding displacement needed to cover every continuous nonoverlap; those are relaxation parameters only and can never qualify a cutting layout. Verify all orientation/reflection aliases, unchanged stock accounting, complete region coverage, every rounded inequality and every known original compatible placement. Declare a fresh construction and one solver limit before execution. A feasible relaxed solution is only diagnostic and must not be accepted as a layout. Any negative claim must be conditional on the recorded fixed core and full outward-coverage audit. Preserve the completed inner model and its infeasibility, the original counts, native guard and production budget; do not rerun or extend this solve, infer unrestricted impossibility, resume capped pose lists or change H2. Original geometry, actual native qualification and the full 13-job/two-kerf H5 matrix remain required for completion.

## Repository and evidence

The domain checkpoint 7fa9fc18 is preserved locally; earlier audits are pushed
to main 8f941426. Main's hosted checks are captured as
`in_progress` / `pending`. Engine source, accurate
READMEs and releases are unchanged. No new release is qualified. No original
geometry acceptance run, native packing, production-budget trial, full H5
quality matrix or held-out evaluation occurs because no layout was returned.
The original 66-part inventory, material target, native guard, production
budget and all 13 jobs at both kerfs remain required.

Evidence: [reduction](h5-direct-coordinate-selection-20261025/reduction.json), [independent containment audit](h5-direct-coordinate-selection-20261025/reduction-audit.json),
[model plan](h5-direct-coordinate-selection-20261025/plan.json), [complete model audit](h5-direct-coordinate-selection-20261025/model-audit.json),
[solver result](h5-direct-coordinate-selection-20261025/solver.json), [precise interpretation](h5-direct-coordinate-selection-20261025/interpretation.json),
[source review](h5-direct-coordinate-selection-20261025/source-review.json), [raw archive](h5-direct-coordinate-selection-20261025/raw-001.zip)
and [manifest](h5-direct-coordinate-selection-20261025/raw-manifest.json). All 41 canonical
members and 6 aliases retain exact bytes with
CRC and SHA-256 verification, including the binary model and complete solver log.
