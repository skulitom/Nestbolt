# H5: full cog geometry and a smaller original-outline model — 2026-10-25

**The complete guarded cog model finishes UNKNOWN without a candidate. The
recorded run exceeds its declared time allowance.** A separate complete pair
check certifies more exclusions, and an independently audited representation
of the original collision core prepares a substantially smaller necessary
model. H2/H5 remain open at **60%**; no complete target layout is found.

## Complete guarded original-cog search

All previous domain choices, nine moving originals, fixed57 source, area limits,
whole-domain exclusions and occupancy limits remain present. Every one of the
six cog anchors is bound to its selected original domain. The full original
cog/cog collision region has **61 convex pieces / 2,720 outside directions**.

Exact integer projection bounds over both complete same-sheet anchor ranges
prove two pieces already separated. The remaining **59 complete disjunctions**
retain **2,636 directions per physical pair**. Independent four-corner extrema
checks cover **21,760 projections**. Forty-eight explicit query-box constraints
make the bound reductions directly implied by the model.

The independently reconstructed model has **52,790 variables / 66,018 constraints**,
including **39,540 original-cog direction variables**, **1,770 sheet-gated piece
clauses**, and all **16,170** conditional inward cog-domain halfplanes. Construction
takes **1.694459 seconds**, the full model audit
**0.713208 seconds**.

Its only call receives **56.540469 seconds** remaining
from the declared shared60-second allowance, with eight workers and seed zero.
It returns **UNKNOWN without an incumbent in 57.452234 seconds**.
Actual end-to-end elapsed time is **60.870843 seconds**:
the shared allowance overruns by **0.870843 seconds**,
and the solver's soft limit by **0.911765 seconds**.
The audit records both overruns explicitly; neither is counted as a budget pass.
No selected-domain, coordinate or native follow-up call is opened. The run stays
closed and establishes neither feasibility nor impossibility.

## Complete guarded cog-pair refinement

The existing raw-original tables leave **200,309** pairs unmarked across the
735 first-sheet and32 second-sheet domains. A separate bounded geometric pass
checks every pair using the complete convex difference of its actual inward
faces, padded outward by0.00001 mm. A new exclusion requires that whole hull
strictly inside a0.0001 mm inset of the full guarded original collision region.
The whole core is covered by the original model's61 forbidden pieces.

The check finishes in **11.197049 seconds**, with no pending pairs:
**126** additional first-sheet and **20** second-sheet raw-table exclusions.
The independent audit reconstructs exact-rational outward nanometre vertex boxes,
checks all146 complete difference enclosures, all2,695 source vertices, every
old bit, domain order, packed hash/length/padding and whole guarded-core coverage.

Sixteen of the20 second-sheet pairs were already excluded by earlier exact
interval proofs. Therefore **130 ordered pairs are new to the prior master**,
giving **1,950** physical pair clauses across all15 cog pairs. They are not
double-counted. These are restrictions of the declared guarded construction;
an unmarked pair remains unproved, and no global packing impossibility is claimed.

## Smaller complete original collision-core representation

The large model's directions mostly come from the finely polygonized clearance
envelope. The next prepared necessary model uses the complete previously certified
raw-original collision core instead of a circular or convex-hull substitute.
It retains the original source-angle tooth geometry and concavities.

That core decomposes into **71 convex pieces with352 outside edges**. Their union
equals the entire committed core; every whole piece lies strictly inside the
actual original cog/cog collision polygon, with minimum boundary margin
**0.000100000000 mm**. This needs at most
**5,280 physical directions**, versus39,540 in the guarded model.

The rounding is intentionally **necessary**, with exact coefficient-error bounds:
`integer_bound = floor(exact_edge_bound - coefficient_error)`. For any true
outside point, the rounded projection remains at least this bound. This differs
from the stricter constructive rounding used by final guarded separation.
Independent read-back checks verify all71 pieces, all352 inequalities and3,024
exact rational convexity relations, full core equality and strict raw containment.

This is ready for a distinct, independently audited staged model, retaining all
original counts, area/occupancy constraints and the130 new pair exclusions.
It is a necessary search relaxation: **a positive still requires the complete
guarded original-coordinate model, all66 original polygon/stock checks and native
validation**. Moving-pair clearance is omitted only from this preliminary core
test, never from acceptance, production-budget integration or the unchanged
13-job/two-kerf H5 matrix. The new model has not been run in this checkpoint.
Future shared-budget calls should reserve explicit margin for solver overshoot.

## Repository and evidence

Main61359456 and its scrap/offcut documentation remain preserved in the local
merge. Its own [CI40242602102](https://github.com/skulitom/Nestbolt/actions/runs/40242602102) is **in_progress**, with **4/6** jobs
successful in the saved snapshot. No result is inferred for unfinished jobs.
Production source and all three accurate READMEs are unchanged. Preview release
v0.2.0-alpha.1 and stable Latest v0.1.0 remain unchanged; no release is qualified.
No native packing, quality or held-out evaluation is run. All22 reserved H2
vectors remain untouched under Artem's unchanged-gate decision.

Evidence: [complete model audit](h5-full-cog-coordinates-20261025/model-audit.json),
[terminal result and budget audit](h5-full-cog-coordinates-20261025/search-audit.json),
[guarded pair audit](h5-full-cog-coordinates-20261025/guarded-pair-audit.json),
[overlap accounting](h5-full-cog-coordinates-20261025/guarded-pair-overlap.json),
[original-core audit](h5-full-cog-coordinates-20261025/core-relaxation-audit.json),
[archive](h5-full-cog-coordinates-20261025/raw-001.zip) and [manifest](h5-full-cog-coordinates-20261025/raw-manifest.json).
The archive retains **284** canonical files and
**43** identical-content aliases with exact length,
SHA-256 and CRC verification, including complete sources, models, parameters,
logs, pair matrices, negative/non-proof results and all new certificate pieces.
