# Weighted mixed-row construction — 2026-11-07

The new weighted original-geometry model passes independent checks and closes
its finite four-epoch search. It still has no valid full layout: the best
unweighted candidate fails **49 original pairs**, with **28,207.754973 mm²**
overlap. Fixed-part and stock checks pass. H2/H5 remain open at **60%**
completed milestone weight; no native call or allocation exclusion follows.

## Positive weights preserve the original conditions

The source geometry, hard domains, 33 moving originals, 81 parameters and all
528 moving pairs are unchanged from the [mixed-row model](h5-mixed-rows-continuous-construction-20261107.md).
Only its unoptimized initializer is consumed; its complete preparation is
charged. No optimized ancestor or closed uniform-weight call is reopened.

Each pair has one coefficient multiplying both original-outline and certified
clearance-outline overlap and every corresponding gradient contribution.
Coefficients stay in **[1, 64]**. The frozen update multiplies colliding terms
by `1.2 + 0.8 × (loss / maximum loss)` and decays noncolliding terms by 0.95,
with the stated floor and ceiling. An initial update gives 33 nonunit weights,
between 1 and 2. [The positive-coefficient proof](h5-weighted-mixed-rows-construction-20261107/zero-equivalence-proof.json)
establishes `unweighted ≤ weighted ≤ 64 × unweighted`, so zero weighted overlap
cannot hide a nonzero term. Original-source acceptance remains separate.

[Independent model checks](h5-weighted-mixed-rows-construction-20261107/model-audit.json) reconstruct all 528
coefficients, 147 mode/full-score controls, 132 scalar gradient terms and
**324 central samples over 162 coordinates**. [Both derivative steps pass](h5-weighted-mixed-rows-construction-20261107/derivative-controls.json),
including a control using weights up to 64. Fifteen update cases verify
**7,920 coefficients**, including floor, ceiling and extreme finite losses.
All 528 isolated positive terms remain detectable, and thirteen corrupted
models are rejected. The original unoptimized initializer is byte-equivalent
in geometry and coordinates. Complete consumed preparation is **9.437444 s**.

## Preserved verifier failure and exact rounding correction

The [first audit failed](h5-weighted-mixed-rows-construction-20261107/preserved-failed-audit-process.json) because
its algebraically equivalent update formula multiplied the loss by 0.8 before
dividing by the maximum, while the model normalizes first. A
[separate diagnostic](h5-weighted-mixed-rows-construction-20261107/rounding-diagnostic.json) finds 79 coefficient
differences, at most two binary64 steps, over all 7,920 controls. It reconstructs
each specified operation from exact rational values and reproduces every actual
coefficient. The versioned audit uses that independent rounding oracle.
The original failure, checker and process remain preserved; model, weights
and initializer are unchanged. No optimization preceded the passing audit.

## Four closed weighted problems and two progress measures

The declared pipeline permits four ten-second calls within preparation-inclusive
60/90-second limits. Each later epoch updates coefficients from the previous
weighted winner, then scores the current physical mode vector and every
distinct single-owner neighbor. Weighted-objective and full-vector ordering
select the next unseen coefficient/mode problem. The first change affects
bracket8, the second insert8; the final epoch retains its modes with different
coefficients. These are four distinct weighted problems, not four distinct
physical mode vectors.

Every evaluation tracks weighted and unweighted progress independently. Every
improvement of either measure is retained. [Response replay](h5-weighted-mixed-rows-construction-20261107/response-audit.json)
verifies **237 proposal scores, 1,584 runtime weight updates and 388 retained
points**, reconciling 455 recorded function evaluations. The two winners differ
in two epochs. All **eight full66 source readbacks** reconstruct 1,380 same-sheet
pairs, 264 stock edges, 90 holes and 10,026 hole vertices; fixed-part and stock
checks pass throughout. The unweighted winners fail 51, 54, 49 and 49 pairs.

The best unweighted objective is 57,660.128728 mm². Its
[49 source failures](h5-weighted-mixed-rows-construction-20261107/source-failures.json) comprise 44 positive
intersections and five clearance-only failures. The final weighted winner is
retained separately: it fails 51 pairs and has 28,330.845832 mm² original
overlap. [Both measures and every epoch](h5-weighted-mixed-rows-construction-20261107/epoch-reconciliation.json)
remain explicit; lower penalty is not material savings or validity.

The declared epoch limit closes the whole search. Algorithm/shared totals are
**54.481227/54.556267 s**, including complete preparation. Slice overruns of
0.069841, 0.005191, 0.073293 and 0.060825 s are preserved. All five
[search processes close](h5-weighted-mixed-rows-construction-20261107/closed-process.json), with 94,785,536 bytes
peak aggregate committed memory. None of these calls may resume.

## Next numerical preflight and repository state

[The next preflight](h5-weighted-mixed-rows-construction-20261107/next-step.json) assesses batching the exact
boundary integral across active pair interactions. The existing kernel already
vectorizes edges within each interaction; the proposed distinction is batching
across those interactions. Every edge/owner/weight mapping and shared-boundary
convention needs independent checks before alternating timings on frozen cases.
This is a numerical/performance review only: no new kernel or optimizer is
prepared, and a faster evaluator alone does not authorize a closed-call restart.

[The two prior checkpoints reached main](h5-weighted-mixed-rows-construction-20261107/prior-main-push-receipt.json)
at d8aa6a90 after all six preceding CI jobs passed, preserving all 52 protected
remote files. Fresh main CI42366837555 is queued at that receipt. This checkpoint
awaits its ordinary push gate. Four earlier fixed arrangements and 440
allocations remain unresolved. Full66 source/native/material validity,
production parity and the unchanged H5 matrix remain required. H2 retains its
original gate and reserved vectors. Product code, README and releases are unchanged.

[Raw evidence](h5-weighted-mixed-rows-construction-20261107/raw-manifest.json), [source bindings](h5-weighted-mixed-rows-construction-20261107/source-bindings.json)
and [pinned runtime files](h5-weighted-mixed-rows-construction-20261107/runtime-bindings.json) preserve the failure,
correction, exact model and closed outcomes.
