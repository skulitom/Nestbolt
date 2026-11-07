# Weighted conditional-relocation construction — 2026-11-07

The conditional-relocation model passes independent checks and closes three
new weighted calls. It still has no valid full layout: the final candidate
fails **46 source pairs**, with **28,414.189788 mm²** overlap. It has fewer
failing pairs than the preceding weighted result but a worse overlap-area
score. H2/H5 remain open at **60% completed milestone weight**.

## Fixed-grid relocation and preserved ranking failure

The [model audit](h5-weighted-relocated-construction-20261107/model-audit.json) verifies **6,396 nominal center
trials** over 78 changed owner modes, retaining 32 exact-coordinate aliases and
6,364 unique centers. The existing 9-by-9 source grid and clamped-center control
are frozen before scoring. Each trial considers all 32 other originals already
present, unlike sequential greedy initialization. The 78 old clamped scores
reproduce exactly. The [same complete enumeration](h5-weighted-relocated-construction-20261107/enumeration-controls.json)
then scores the current vector, 78 single-owner and 2,775 two-owner alternatives
using all 528 original/clearance pair losses.

[The best joint proposal](h5-weighted-relocated-construction-20261107/initial-selection.json) moves inserts 10 and 20
(owners 16 and 17) into mode 2. Its weighted score is 216,054.847421 mm² versus
229,297.518758 mm² for the best single, an improvement of **13,242.671337 mm²**.
It also improves the original 244,566.416868 mm² initializer. Independent source
transforms reproduce every center/proposal score; the selected model passes
148 scalar boundary terms and 162 central samples, with maximum central error
0.000103 under the unchanged tolerance.

The [original audit failure](h5-weighted-relocated-construction-20261107/preserved-failed-audit-process.json) remains
preserved. It demanded identical winners from NumPy dot-product scores and a
sequential scalar sum. One owner-mode has a binary64 near-tie where the
reduction orders disagree. [Independent exact-product controls](h5-weighted-relocated-construction-20261107/rounding-diagnostic.json)
cover all 89 near-best vectors across 78 modes, reproducing every recorded score.
[The one ranking difference](h5-weighted-relocated-construction-20261107/rounding-ranking-differences.json) is on
the order of 1e-11 mm². Version2 independently reconstructs every pair vector
for the specified score ordering and separately checks sequential sums within
the unchanged 1e-6 tolerance. Model, weights, geometry, trials and selected
centers remain unchanged. The failed wrapper takes 86.431769 s; the passing
[versioned audit wrapper](h5-weighted-relocated-construction-20261107/model-audit-process.json) takes 194.258318 s.
No optimizer precedes the passing audit.

## Three distinct closed calls and complete accounting

The new pipeline starts from the audited unoptimized source-grid selection.
It excludes all four previous weighted coefficient/mode keys. At each later
epoch it updates bounded positive coefficients, repeats the frozen conditional
center calculation, and admits a new joint choice only if it beats both the
current point and the best admissible single choice. No grid refinement occurs.
The contract permits at most three ten-second calls within preparation-inclusive
60/90-second limits, shortening a call at the source-check reserve boundary.

[Response replay](h5-weighted-relocated-construction-20261107/response-audit.json) verifies **12,792 runtime center
trials**, **5,708 complete proposals**, **1,056 updated coefficients** and
**206 retained points**, reconciling 246 function evaluations. It independently
reconstructs both full66 winners after each call: six checks of 1,380 same-sheet
pairs, 264 stock edges, 90 holes and 10,026 hole vertices. The weighted/unweighted
winner positions coincide in these three epochs; both streams remain explicit.
All fixed-part and stock checks pass. [Epoch outcomes](h5-weighted-relocated-construction-20261107/epoch-reconciliation.json)
retain 55, 52 and 46 failing pairs.

Complete preparation is **15.046673 s**: the original 9.437444 s, the consumed
negative joint-selection stage 1.517851 s and the new relocation wrapper 4.091379 s.
Validation-only audits are separately retained. The first two calls receive 10 s;
the third receives 5.458502 s. Algorithm/shared totals are
**56.586553/56.748614 s**. Slice overruns of 0.074402, 0.034575 and 0.039643 s are
preserved. The pipeline stops after its final source check. All five
[search processes close](h5-weighted-relocated-construction-20261107/closed-process.json), with 114,229,248 bytes peak
aggregate committed memory, below 2 GiB. None of the seven combined weighted
problems may resume. The response-audit wrapper closes in 384.974831 s.

The [46 final failures](h5-weighted-relocated-construction-20261107/source-failures.json) comprise 40 positive
intersections and six clearance-only failures. [Comparison with the preceding
weighted result](h5-weighted-relocated-construction-20261107/prior-result-comparison.json) shows the tradeoff:
three fewer failing pairs, but 206.434815 mm² more original overlap and
297.328738 mm² more unweighted original-plus-clearance penalty. Neither result
is a valid full layout; no material-quality improvement is claimed.

## A verified flat crossed-arm collision

[Failure composition](h5-weighted-relocated-construction-20261107/outcome-diagnostic.json) finds 21 companion/cog
failures totaling 11,466.537157 mm² overlap, 16 cog/cog failures totaling
9,441.760037 mm², and failures between companions. Three cogs have lower-y
bounds active with their local negative weighted gradient blocked. These are
candidate observations, not a global packing exclusion.

A [separate fixed-probe diagnostic](h5-weighted-relocated-construction-20261107/pair-plateau-diagnostic.json)
checks all 47 positive original/clearance pairs. Brackets 7 and 8 have a
**5,625 mm²** crossed-arm overlap, with neither strictly containing the other.
Their combined original/clearance term is 11,284.552900 mm². Every available
pair-coordinate gradient is zero within 1e-7. All **26 feasible translations**
at the predeclared ±0.001, 0.1, 1 and 5 mm steps leave that pair term unchanged.
[Every probe is retained](h5-weighted-relocated-construction-20261107/flat-pair-probes.json). Increasing a constant
positive coefficient cannot provide a direction for a zero-gradient term.
No probe modifies the saved candidate or seeds an optimizer.

[The next preflight](h5-weighted-relocated-construction-20261107/next-step.json) therefore assesses a supplementary
squared distance-to-exit loss for a source-derived bracket collision translation
region. The original L can be decomposed into two rectangles. The proposal
needs independent source, configuration-space, boundary and derivative proofs,
including deterministic ties and floating-transform reconciliation. It must
retain every exact original/clearance term and all existing acceptance rules.
The saved flat pair is validation-only. No auxiliary kernel, new objective
model or successor optimizer is prepared here.

## Repository and evidence

The three preceding checkpoints 0af0c522, f03aadc1 and c7e4b305 reached main
normally after all six previous checks passed, preserving 52 remote files.
[The push receipt](h5-weighted-relocated-construction-20261107/prior-main-push-receipt.json) records both branch
updates and fresh CI 42369490349. [At review](h5-weighted-relocated-construction-20261107/main-ci-at-review.json),
4 jobs pass and 2 remain live. This checkpoint awaits the ordinary
push gate. Product code, README claims and releases remain unchanged. Four
earlier fixed arrangements and 440 allocations remain unresolved.

[Manifest](h5-weighted-relocated-construction-20261107/raw-manifest.json), [source bindings](h5-weighted-relocated-construction-20261107/source-bindings.json),
[historical references](h5-weighted-relocated-construction-20261107/external-evidence.json) and
[runtime pins](h5-weighted-relocated-construction-20261107/runtime-bindings.json) preserve the failures, correction,
all trials, closed calls and readbacks.
