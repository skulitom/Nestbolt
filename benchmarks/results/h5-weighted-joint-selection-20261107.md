# Weighted joint-selection preflight — 2026-11-07

The exhaustive two-owner mode comparison **does not meet its improvement
prerequisite**. The best joint choice scores 613.576416 mm² worse than the best
single choice; both score worse than the unoptimized initializer. No selected
model or optimizer is opened. This closes this proposed selection path without
changing any packing result. H2/H5 remain open at **60% completed milestone weight**.

## Complete physical-mode enumeration and full scores

The [frozen preflight](h5-weighted-joint-selection-20261107/frozen-plan.json) uses the unchanged 33-owner,
81-parameter original/clearance model and its audited initial pair weights.
It consumes only the preserved unoptimized source initializer. For a changed
mode, the owner center moves only as far as necessary to enter that mode's
hard bounds. Every other center and all 15 actual cog angles stay fixed.

[Independent exact rational class reconstruction](h5-weighted-joint-selection-20261107/enumeration-controls.json)
checks all 147 owner/mode bindings. Brackets have 10 physical choices, inserts
have 3 choices represented by 6 nominal modes, and cogs have one continuous-angle
mode. The exhaustive comparison includes the current vector, **78 single-owner
choices** and **2,775 two-owner choices**: 1,215 bracket/bracket, 1,296
bracket/insert and 264 insert/insert. Equivalent current modes and aliases stay
explicit; no distinct full physical vector is duplicated.

The new selector caches exact intersections for each changed owner, replaces
the two changed owners' mutual interaction once, and sums **all 528 weighted
pair losses** for every proposal. Each loss includes original and clearance
geometry. It uses no subtractive delta or partial-score ranking.
[Independent replay](h5-weighted-joint-selection-20261107/selection-audit.json) transforms every source ring
and directly recomputes every complete score, without the cache. All **2,854
scores** agree within **1.74623e-10 mm²**, below the frozen 1e-6 tolerance.
Independent full-score ordering reproduces both best choices.

[All four closed weighted coefficient/physical-mode keys](h5-weighted-joint-selection-20261107/closed-weighted-problems.json)
are reconstructed from their preserved models and responses. The current
initializer's problem is excluded; the other three old coefficient vectors
differ from the initial weights. Exclusion and physical alias checks apply
before ranking. Earlier weighted and unweighted calls remain closed.

## The improvement condition fails

| Choice | Weighted objective | Difference from initializer |
|---|---:|---:|
| Preserved initializer (closed problem) | 244,566.416868 mm² | — |
| Best admissible single change | 244,973.051779 mm² | +406.634911 mm² |
| Best admissible two-owner change | 245,586.628194 mm² | +1,020.211327 mm² |

[The best single](h5-weighted-joint-selection-20261107/selection.json) changes insert 7 (owner 13) to mode 2;
the best joint changes inserts 7 and 8 (owners 13 and 14) to mode 2. These are
diagnostic alternatives, not accepted placements. The joint score is
**613.576416 mm² worse** than the single score. The declared prerequisite
required a joint improvement greater than 1e-6 mm², so no selected-state/model
file or search directory is created. Conditional scalar/central model checks
are not run because no model is selected. No source-validity claim follows.

The [complete preparation wrapper](h5-weighted-joint-selection-20261107/preparation-process.json) takes
**1.517851s**. With the entire consumed 9.437444s original preparation, the
recorded preparation total is **10.955294s**. The separate
[validation wrapper](h5-weighted-joint-selection-20261107/audit-process.json) takes 48.647537s. Both bounded
Windows jobs close with no active processes, within their 20/180s limits and
2GiB memory limits. The audit's peak committed memory is 38,617,088 bytes.
No optimizer, native call, allocation exclusion or source mutation occurs.

## Next geometry question and current state

The negative result applies to nearest-bound clamping. It does not establish
that those physical modes are worse at other centers inside their hard cells.
[The next preflight](h5-weighted-joint-selection-20261107/next-step.json) assesses conditional center moves
on the existing fixed 9-by9 source grid plus the clamped-center control, scoring
each changed owner against all other 32 originals. Unlike the sequential source
initializer, all other original positions are already present during this
comparison. The grid may not be refined after viewing results. Any resulting
joint proposal must still beat the best single proposal and pass an independent
model/finite-accounting preflight before an optimizer could open.
No successor selector or optimizer is prepared in this checkpoint.

The preceding weighted search remains invalid, with 49 source-pair failures
and 28,207.754973 mm² overlap. Four earlier fixed arrangements and 440 allocations
remain unresolved. Product code, README claims and releases are unchanged.
[Main CI at review](h5-weighted-joint-selection-20261107/main-ci-at-review.json) has five passed jobs and
Windows native checks running on d8aa6a90. Pending 0af0c522, f03aadc1 and this
checkpoint await the ordinary push gate.

[Raw evidence manifest](h5-weighted-joint-selection-20261107/raw-manifest.json),
[historical references](h5-weighted-joint-selection-20261107/external-evidence.json),
[source bindings](h5-weighted-joint-selection-20261107/source-bindings.json) and unchanged
[runtime pins](h5-weighted-joint-selection-20261107/runtime-bindings.json) preserve all proposals, scores,
exclusions, scripts and closed processes. Runtime pins are checked at sealing;
this does not claim an additional before-run runtime check.
