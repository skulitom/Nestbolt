# H5: direct capacities, independent component blocks and the shared five-part construction — 2026-10-29

Direct regeneration recovers the previously verified **18 site choices and 42
count distributions**, without consuming the saved cut list. It also permits
removal of 1,876 impossible unary choices from the placement model. The resulting
model's sole bounded call returned `UNKNOWN`, without a placement.

A separate geometric audit proves that **23 distributions across eight choices
split into independent blocks**. Three choices share the same two-bracket,
three-insert block. Its much smaller audited grid model reports `INFEASIBLE`,
but that is not an independently certified continuous-source exclusion.
Continuous pair and subset-capacity checks remove 102,322 necessary option
combinations and retain 36,802. The full count domain therefore remains unchanged.

H5 is open. No full66 placement, source-check call or native validation was
produced. The 440 overall allocation candidates and complete H5 matrix remain
open; milestone completion is still **60%**.

## Direct regeneration and the global placement call

Starting from the original 29 component tables and 132 counts, direct fine-area
construction takes **2.0645063 s**, generates 50 exact subset certificates and
retains 22 choices / 47 counts. The [area audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/direct-area-audit.json)
checks 14,714 source vertices and 196,029 exact polygon-band clippings. Direct
fine-strip construction then takes **1.8462460 s** and generates four certificates
that remove five more counts and four choices. Its
[independent audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/direct-strip-audit.json) verifies 52 exact breakpoint
evaluations and 5,266 polygon-clipping operations.

The [filtered-source audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/filtered-count-audit.json) confirms byte-for-byte
equality with the previous 18-choice, 42-distribution source table, including all
4,501 mode attributions and 2,957 unique family/geometry/region assignments.
Filtering takes 0.0324599 s. The new direct construction replaces only the
superseded preparation steps; all earlier required source preparation remains
charged.

For each original unary region, the new model checks whether its required empty
cog sites fit any of the 18 retained choices. Exactly 1,876 owner-region choices
cannot satisfy that condition and are removed. All 13 moving original parts and
80 modes remain represented. The [exhaustive model audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/model-audit.json)
verifies all **6,520 variables and 32,928 constraints**, 5,527 retained unary
selectors, 22,439 source planes, 7,935 site-mask implications, 20 rigid rectangles,
544 mode-coordinate equalities and all 183 different-owner rectangle pairs.
It also checks all 42 count selections, 234 canonical component equalities and
373 within-component orders, including the validity of copy relabelling.

Model construction takes 1.1480179 s; total charged preparation is
**40.1912943 s**. The [closed-call audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/response-audit.json) records:

| Measurement | Result |
|---|---:|
| Solver status | `UNKNOWN` |
| Allocated solve slice | 15.0897205 s |
| Returned solve time | 15.1541049 s |
| Solve-slice overrun, preserved | 0.0643844 s |
| Algorithm time, including preparation | 56.0778434 s |
| Shared time, including preparation | 56.1527840 s |
| Branches / conflicts | 39,749 / 51 |
| Assignments / source calls / native calls | 0 / 0 / 0 |

The 60/90-second overall limits pass. This call remains closed; it proves no
infeasibility. Raw LP diagnostics are preserved with the response.

## Independent component blocks

Each model rectangle lies within a 0.15 mm expansion of its independently verified
contained source rectangle. A conservative graph joins component groups whenever
their swept support covers are within 0.6 mm in the maximum-coordinate distance.
Groups in different graph components are therefore separated enough to preserve
the model's 0.3 mm axis clearance after both rectangle expansions.

The [factorization audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/factorization-audit.json) checks all 20 rectangle
extension bounds and **7,856,737 support-rectangle pairs** across 116 group pairs.
It verifies 70 noninteracting group pairs. Eight site choices, covering 23 count
distributions, split into independent blocks. Their largest blocks have 8–11
copies, rather than all 13. This proves independence, not the existence of a
placement in any block.

## Shared five-part block and continuous-domain checks

The same two-bracket/three-insert block occurs in site choices `[0,11]`, `[0,12]`
and `[0,13]`. All 81 original mode/geometry/region options match exactly across
these uses. Its [model audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/shared-block-model-audit.json) verifies every
one of 259 variables and 708 constraints: five original copies, 16 mode selectors,
129 unary selectors, seven rigid rectangles and all 19 different-owner rectangle
pairs. The companion blocks would contain five brackets and three inserts.

The [shared-block call audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/shared-block-response-audit.json) records
`INFEASIBLE` in 0.0531151 s, with 59 branches and 17 conflicts. Total charged
preparation is 39.1142117 s; algorithm/shared time is 39.8688959 / 39.9359431 s.
No assignment, source check, native call or overrun occurred. This is a solver
report about the audited conservative **0.1 mm grid model**; no independent
unsatisfiability certificate is available. It does not exclude the original
continuous source domain or any overall allocation.

To investigate that distinction, a separate necessary-domain construction uses
the **original continuous source hulls**. The required Euclidean gap implies at
least 0.149 mm separation in one coordinate because twice that margin squared is
strictly below the required gap squared. Exact extrema of contained source
rectangles rule out 835 source-option pairs. Complete enumeration, including
repeated options when self-compatible, leaves 139,124 five-option multisets.

For every visited option subset, exact required material is compared with its
original conservative 10 mm support-cell union. The
[independent domain audit](h5-direct-capacities-component-factorization-and-shared-block-20261029/shared-domain-audit.json) verifies **90,422 exact
subset certificates** and independently enumerates the complete pair-compatible
domain. They remove **102,322** five-option multisets; **36,802 remain**.
Those remaining multisets are necessary possibilities, not placements. No whole
block, count distribution or site choice is excluded by this diagnostic.

## Evidence and next work

The [next step](h5-direct-capacities-component-factorization-and-shared-block-20261029/next-step.json) uses the finer, already audited source
supports for the remaining continuous-domain combinations. Every prior solver
call remains closed. Native work still requires full66 original-source validation.

The [raw manifest](h5-direct-capacities-component-factorization-and-shared-block-20261029/raw-manifest.json) records 4917 canonical files and
939 byte-identical aliases in multipart archives totalling 64480165 bytes.
It preserves both complete models and calls, all source bindings, proof tables,
domain enumerations and construction/audit helpers.

The [publication review](h5-direct-capacities-component-factorization-and-shared-block-20261029/publication-review.json) confirms unchanged
production and README digests, upstream heads/releases, stable v0.1.0 and preview
v0.2.0-alpha.1. All six checks on main `cf2c4d7d` passed in
[run 40846115291](https://github.com/skulitom/Nestbolt/actions/runs/40846115291).
No new release qualifies. H2's original gate remains open and no reserved import
vectors were evaluated.
