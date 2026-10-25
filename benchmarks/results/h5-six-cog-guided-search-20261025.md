# H5: guided candidate and exact selected-domain rejection — 2026-10-25

**The verified six-cog hints let the full domain master find a candidate in
11.009201s. The original-coordinate follow-up rejects that selected
combination; a separate exact proof independently certifies the rejection.**
No complete target layout is found. H2/H5 remain open at **60%**.

## Closed guided search

All 66 original parts remain mandatory: nine movable and 57 fixed at their
verified source placements. Every one of the 9,776 domain choices, both original
area limits, all existing exclusions and the full guarded cog cells remain.
The new model adds **9,204 exact conditional domain box bounds** and **79
advisory values** from the previously verified six-cog construction. The hints
fix no placements. Independent reconstruction checks **16,775 variables /
55,587 constraints**, every hint membership and every selected cell condition.
Construction takes **1.272953s** and model audit
**0.597032s**.

The single 45-second-cap, eight-worker, seed-zero call returns a candidate
(`OPTIMAL` is the satisfaction-solver status). Both brackets select query 0,
domain row 190; the insert selects query 17, row 0. The six cogs retain the hinted
domain rows 3, 31, 72, 734 on the first sheet and 1, 1 on the second. Independent
selection checks confirm all nine identities, original area charges, existing
pair exclusions, regional capacities, and all 427 full guarded cog clauses.
These necessary checks do not prove the remaining parts can be placed.

The full selected-coordinate model contains **2,255 variables / 2,341
constraints**, with all 18 same-sheet pairs and 712 original forbidden faces.
Only exact complete-box proofs remove always-separated faces or impossible
directions. Its sole call returns **INFEASIBLE in 0.225323s**.
The complete three-stage pipeline takes **15.872994s**,
within the shared 60-second limit; neither call exceeds its own cap. Both calls
are closed. No native validator or quality run is opened on the rejected candidate.

The raw runner plan's phrase `all66 originals movable/mandatory` is imprecise:
the actual model has nine movable and 57 fixed originals, all mandatory.
[The explicit wording correction](h5-six-cog-guided-search-20261025/plan-wording-correction.json) preserves
the original record; it changes no model, result or scope.

## Exact rejection proof

A separate interval diagnosis checks all 18 same-sheet pairs and the complete
nine-domain selection. All **19 traces reach fixed points**, with **1,104
integer bound deductions** and no contradiction. Exact rational replay checks
every deduction and confirms no further unit-clause or inward-bound deduction
is available. A fixed point is not a feasible placement.

A new bounded proof tree therefore branches on unresolved original separation
clauses. Every branch includes **all remaining possible source edges**; each
child enforces one edge's original inequality. Children may overlap, but their
union covers all possible solutions of their parent. Every original part and
domain stays in scope. The tree completes in **56.946915s**, inside its
separate 60-second proof budget, with **1,316 nodes, 415 branch nodes, 901
contradictory leaves and 4,851 events**. There are no pending or open leaves.
This proof procedure invokes no solver and does not extend the completed search.

Independent rational read-back takes **17.411535s** and reconstructs
source rules, verifies every bound update and unit clause, checks inherited
assumptions, and proves complete coverage of all branches with no orphan node.
The [certified exclusion](h5-six-cog-guided-search-20261025/certified-selection-exclusion.json) applies only
to **these nine selected inward domains with their original source angles,
fixed 57 placements and guarded clauses**. It does not exclude other domains,
other placements or unrestricted packing.

An early read-back started before the proof process wrote its terminal files
and failed with `FileNotFoundError`. Its script, plan and failure record remain
preserved. The separate completed read-back ran after the original process
exited. No proof or solver call was restarted and no failed record overwritten.

## Next structural step and repository state

The remaining bracket/insert coordinates need to participate in the same
guarded placement search as the cog coordinates. Prepare compact guarded
displacement representations for the remaining original profile pairs, prove
whole-cell safety independently, and preserve every allowed domain and original
constraint before another bounded full search. The certified selection can be
excluded where applicable. Repeating the same hinted master is not the next step.
Any complete positive still needs all 66 original geometry checks, native
validation, production-budget integration and the original 13-job/two-kerf H5
matrix. The first-sheet cog representation's extra 0.010 mm constructive
restriction remains explicit and is not an acceptance-guard relaxation.

Main 61359456 now has **all six jobs successful** in
[CI 40242602102](https://github.com/skulitom/Nestbolt/actions/runs/40242602102). Its offcut documentation is preserved. This
checkpoint is prepared for a normal push after reconciling any newer remote
changes; success of the future pushed commit's own CI is not claimed here.
Production source and all three accurate READMEs are unchanged. Preview
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged; no new release is
qualified. H2 keeps its original gate and all 22 reserved vectors untouched.

Evidence: [master audit](h5-six-cog-guided-search-20261025/master-model-audit.json),
[search timing audit](h5-six-cog-guided-search-20261025/search-audit.json),
[proof audit](h5-six-cog-guided-search-20261025/conflict-proof-audit.json),
[source review](h5-six-cog-guided-search-20261025/source-review.json), [archive](h5-six-cog-guided-search-20261025/raw-001.zip), and
[manifest](h5-six-cog-guided-search-20261025/raw-manifest.json). The archive preserves **400
canonical files and 95 exact-content aliases**, including
full models, parameters, logs, every proof node and source input, with verified
size, SHA-256 and CRC.
