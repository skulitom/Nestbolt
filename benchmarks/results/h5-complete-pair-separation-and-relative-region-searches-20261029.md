# H5: complete pair separation and relative-region searches

Date: 2026-10-29. Evidence and documentation only. H2/H5 remain open at
60% completed milestone weight. No new release qualifies.

Three distinct fixed-orientation construction models reach their declared
**128-node limits without an assignment**. All calls are closed. These are
unresolved bounded searches, not infeasibility proofs. **No allocation is
excluded**; the 440-candidate frontier and valid 64-part layout are preserved.
There is no new valid eleven-part or complete 66-part layout.

## Complete convex-piece separation

The [previous checkpoint](h5-axis-choice-rejection-and-exact-source-partition-20261029.md)
independently verified the exact 21-piece cog decomposition. The first new model
uses all 56 pieces from five brackets, four inserts and two cogs. Every one of
the **1,115 inter-original piece pairs** offers both signs of every source edge
normal. Directions are rounded to twelve decimals and renormalized; this finite
axis choice and the fixed modes/phases limit negative conclusions.

The [model audit](h5-complete-pair-separation-and-relative-region-searches-20261029/all-pair-model-audit.json) checks 22,880 edge/sign
references, 18,594 exact support inequalities and 18,594 domain classifications.
Stock bounds make 148 piece pairs safe without constraints and rule out 1,736
directions. The remaining 967 groups use 15,226 binary selectors, for
**15,248 variables / 16,193 rows**. Every matrix row is verified. The minimum
active projected gap is above 0.225000099 mm, and inactive rows are relaxed over
the complete stock domains. All 22 translations are free. All eleven short-sheet
and 55 mandatory first-sheet identities are retained.

## Certified whole-part free regions

For each of the 55 pairs of originals, the next preparation unions the convex
Minkowski differences, inflates the forbidden set conservatively, and subtracts
it from the relative translation rectangle. Constrained triangulation produces
890 triangles. Exactly area-preserving convex merges reduce these to **695
regions**. Boolean operations and triangulation use floating geometry; their
scope is recorded rather than treated as an exact completeness theorem.

The [independent region audit](h5-complete-pair-separation-and-relative-region-searches-20261029/free-region-audit.json) proves safety of
every entire region with **21,960 exact rational source-support inequalities**,
independent of floating collision verdicts. Minimum certified gap is
**0.22546063934742305 mm**, exceeding the 0.225 mm construction target.
All relative domains and identities match. The union of the saved convex regions
has zero measured symmetric-difference area against the constructed free space.

The second model selects one region per pair. The [matrix audit](h5-complete-pair-separation-and-relative-region-searches-20261029/region-model-audit.json)
verifies **717 variables / 2,328 rows**, including 695 region selectors and
2,273 edge planes. Each plane is tightened by its complete coordinate-rounding
error plus 1e-7 mm. Exact checks prove each active plane implies the original
certified region boundary, and every inactive plane is harmless over the full
stock domains.

The third model uses a distinct convex-combination formulation. For each region,
nonnegative vertex weights sum to its binary selector; two equalities per part
pair express their relative translation as the weighted sum. This removes all
deactivation constants. The [audit](h5-complete-pair-separation-and-relative-region-searches-20261029/convex-hull-model-audit.json) verifies
**2,990 variables / 860 rows**, with 695 binary selectors and 2,273 continuous
weights. It repeats all **21,960 exact source-support proofs** after rounding
region vertices to nine decimals. The certified gap remains above 0.225460639 mm.

## Three closed calls and their limits

Each formulation has one independently audited model, one declared call, a
60-second algorithm allowance, a 90-second shared allowance, a 128-node cap and
a three-second source-readback reserve. Preparation is charged to each call.

| Formulation | Solve seconds | Algorithm incl. preparation | Shared incl. preparation | Nodes | Assignment |
|---|---:|---:|---:|---:|---|
| All convex-piece directions | 42.760214 | 44.384345 | 44.478354 | 128 | None |
| Whole-part region planes | 1.670821 | 3.911584 | 3.998491 | 128 | None |
| Region convex combinations | 3.170081 | 5.386526 | 5.457279 | 128 | None |

These are observed construction-call times, not a passing quality benchmark.
The response audits for [piece pairs](h5-complete-pair-separation-and-relative-region-searches-20261029/all-pair-response-audit.json),
[region planes](h5-complete-pair-separation-and-relative-region-searches-20261029/region-response-audit.json) and
[convex combinations](h5-complete-pair-separation-and-relative-region-searches-20261029/convex-hull-response-audit.json) verify respectively
5,129, 5,159 and 5,180 recursive input bindings. No budget overrun or dropped
tiny coefficient is reported. The raw HiGHS label is **“Solution limit reached”**
and the SciPy status is **4**; the logs show 128 nodes and no incumbent. The
installed wrapper maps the requested node cap to `mip_max_nodes`. None of these
statuses proves infeasibility. No call is retried, extended or reseeded.

A separate [horizontal-slice diagnostic](h5-complete-pair-separation-and-relative-region-searches-20261029/slice-capacity-diagnostic.json)
derives exact piecewise-linear lower bounds for each outline over its full Y
domain at nine declared heights. The strongest sampled bound is
**1,481.2088423828 mm at Y=220 mm**, against 1,486.95 mm available. This leaves
5.7411576172 mm before inter-part gaps and coupling between heights. It finds
no capacity contradiction and does not prove that the fixed modes are feasible.

## Next construction and publication

The [next orientation preparation](h5-complete-pair-separation-and-relative-region-searches-20261029/all-mode-preflight.json) broadens
each bracket to all eight legal quarter-turn/mirror combinations and each insert
to all four legal quarter-turns. All **58 instance-mode options** fit individually.
An eleven-entry filled-geometry library shares equivalent outer shapes while
preserving distinct source transforms and original holes for readback. Both
cogs retain the declared 7-degree phase. The [next step](h5-complete-pair-separation-and-relative-region-searches-20261029/next-step.json)
requires independent mode and pair-mode region audits, correct coupling between
each region and both owners' modes, and a full model audit before any call.
**No model or search with variable orientations has opened.** First55, complete
source/native/material validation, production integration and the H5 matrix remain.

[All six checks](h5-complete-pair-separation-and-relative-region-searches-20261029/main-ci-snapshot.json) on main **8c434a2b** have passed
in [run 40811474503](https://github.com/skulitom/Nestbolt/actions/runs/40811474503).
The [prior push receipt](h5-complete-pair-separation-and-relative-region-searches-20261029/prior-main-push-receipt.json) preserves the normal
atomic publication of the preceding two checkpoints. The
[publication review](h5-complete-pair-separation-and-relative-region-searches-20261029/publication-review.json) confirms unchanged production
source, READMEs, upstream heads/releases and both Nestbolt release versions.
H2 keeps its original gate and all 22 reserved vectors remain unopened.

The [manifest](h5-complete-pair-separation-and-relative-region-searches-20261029/raw-manifest.json) retains **4478 canonical files** and
**877 identical aliases** in **34130619 archive bytes**, including the three
models, exact support certificates, raw solver statuses/logs, all timing, the
inconclusive diagnostic and the next preparation. Independent ZIP/hash/alias/
source-binding/JSON/link verification is stored in `archive-checks.json`.
