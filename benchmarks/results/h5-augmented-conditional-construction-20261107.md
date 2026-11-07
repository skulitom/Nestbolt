# Augmented conditional construction — 2026-11-07

The complete source selector and one bounded search pass independent replay.
The three winner streams choose different candidates, but each still fails
**55 source-pair checks**. The best original-overlap candidate has
**36,097.586688 mm²** overlap, worse than the preceding augmented result's
33,707.125558 mm² and 44 failed pairs. No packing improvement, full-layout
validity or allocation exclusion is established. H2/H5 remain open at **60%**.

## Complete source selection

The model retains 33 movers, 81 coordinates, all 528 weighted original/clearance
area pairs, 15 unweighted bracket-depth terms at coefficient 1, and every hard
stock/fixed-part domain. Original source coordinates, nonunit source weights
and legal modes are unchanged. Cogs retain their continuous angles. Earlier
joint/relocated selector modules are code references only; their computed
scores, centers and optimized states are not consumed.

Every changed physical bracket/insert mode is tested on the frozen 9-by-9
source grid plus its clamped center against all 32 other owners. The
[independent preflight](h5-augmented-conditional-construction-20261107/model-audit.json) reconstructs **6,396 nominal
center trials** (6,364 unique centers and 32 exact aliases), all 147 legal
mode/domain bindings and **2,854 full proposals**: current, 78 singles and
2,775 joints. Joint families comprise 1,215 bracket/bracket, 1,296
bracket/insert and 264 insert/insert choices. Each mutual area and auxiliary
interaction is replaced exactly once.

[All 9,250 full scores replay](h5-augmented-conditional-construction-20261107/selection-replay.json) using independently
reconstructed source polygons, scalar binary64 depth projections and an
additional exact-rational boundary check. Maximum component-score and scalar
reduction errors are 1.165e-10 mm²; maximum rational auxiliary error is
3.638e-12 mm². The ranking policy and 1e-6 score-verification tolerance were
frozen before measurements. [No numerical ranking disagrees](h5-augmented-conditional-construction-20261107/near-tie-rankings.json),
so no tolerance fallback is used. Eight prior closed keys are retained;
one current proposal is excluded by that ledger.

The [chosen joint](h5-augmented-conditional-construction-20261107/selection.json) changes original inserts 10 and 20
(owners 16 and 17) to physical mode 2, with source centers
(1094.2374985, 2620.04999925) and (577.88125075, 2336.6250015).
Its augmented score is **216,065.491335 mm²**, compared with
229,308.162672 for the best single and 244,577.060782 for the current source
state. The joint improves the best single by 13,242.671337 mm².
[Selected-model controls](h5-augmented-conditional-construction-20261107/selected-model-controls.json) verify all
81 coordinates and 148 directed scalar gradient terms, with maximum gradient
error 5.685e-14 mm. The selected initializer still has 75,955.600891 mm²
original overlap; an improved weighted score is not a valid packing.
Existing contact/nearest-feature gradient conventions and their nonsmooth
limitations are retained.

The full selector preparation wrapper takes **5.285699 s**, bringing consumed
source preparation to **16.974380 s**. The independent exhaustive audit wrapper
takes 196.090574 s under its separate frozen 600 s validation limit.
All monitored descendants close within the 2 GiB memory bound.

## Sole closed search and complete response replay

One L-BFGS-B call uses the selected source joint with modes and weights held
fixed. Its 28 s slice returns at **28.064511 s**; the **0.064511 s overrun**
is preserved. Preparation-inclusive algorithm/shared totals are
**48.649513/48.735274 s**, within the frozen 60/90 s overall limits.
[The search process tree closes](h5-augmented-conditional-construction-20261107/closed-search-process.json), with
five processes and 101,482,496 bytes peak aggregate committed memory.

[Response replay](h5-augmented-conditional-construction-20261107/response-audit.json) verifies all **310 evaluation
records**, including 309 optimizer evaluations, and all **274 retained
improving points**. Independent full-score error is at most 2.329e-10 mm²,
original-area error 5.821e-11 mm² and winner scalar-gradient error
1.049e-13 mm. [The three distinct winner streams](h5-augmented-conditional-construction-20261107/winner-reconciliation.json)
are all retained:

| Winner metric | Evaluation | Original overlap (mm²) | Unweighted area sum (mm²) | Augmented score (mm²) | Failed source pairs |
| --- | ---: | ---: | ---: | ---: | ---: |
| Augmented | 309 | 36,112.738571 | 73,538.912801 | 89,201.639437 | 55 |
| Original overlap | 290 | 36,097.586688 | 73,538.314646 | 89,275.475931 | 55 |
| Unweighted area | 302 | 36,105.023349 | 73,528.687948 | 89,227.349054 | 55 |

Each winner receives a full 66-part original-source readback covering 1,380
same-sheet pairs, 264 stock edges, 90 holes and 10,026 hole vertices. Fixed-part
and stock checks pass in all three; none is valid. The independent response
audit wrapper takes 32.959490 s and closes all descendants. The
[new key is permanently closed](h5-augmented-conditional-construction-20261107/closed-problem.json), alongside the
earlier augmented key and seven area-only weighted keys. No native call follows.

## Remaining failures and next preflight

The [best-original source check](h5-augmented-conditional-construction-20261107/source-failures.json) has 52 positive
intersections and three clearance-only failures. Its [family composition](h5-augmented-conditional-construction-20261107/family-failures.json)
is:

| Families | Failing pairs | Original overlap (mm²) |
| --- | ---: | ---: |
| Bracket / insert | 6 | 5,243.233725 |
| Bracket / cog | 9 | 6,092.334134 |
| Insert / insert | 3 | 3.048438 |
| Cog / insert | 20 | 16,895.464987 |
| Cog / cog | 17 | 7,863.505404 |

The [read-only diagnostic](h5-augmented-conditional-construction-20261107/outcome-diagnostic.json) finds no flat
available pair gradient among 55 positive original/clearance area terms.
There is no bracket/bracket failure and auxiliary bracket loss is zero.
Four cogs have negative-gradient descent blocked at their lower-y bounds.
No flat-pair probe is triggered and no candidate changes.
[Comparisons](h5-augmented-conditional-construction-20261107/prior-comparisons.json) preserve the worse result against
the preceding augmented and earlier weighted constructions.

[The next preflight](h5-augmented-conditional-construction-20261107/next-step.json) will assess a bounded adaptive
augmented pipeline after reconciling the older area-only adaptive implementation.
It must start from an independently selected, admissible original-source
proposal; test deadline-aware selector stops; audit every weight and dynamic
model; retain full preparation accounting and freeze its finite contract
before any search. No successor model, pipeline or call exists yet. Current
and prior optimized winners are not successor initializers. Four earlier
fixed arrangements and all 440 allocation candidates remain unresolved.

The previous checkpoint reached main **193660c4** after all six preceding
checks passed, preserving 52 protected files. [The ordinary atomic push receipt](h5-augmented-conditional-construction-20261107/prior-main-push-receipt.json)
is retained. [At sealing](h5-augmented-conditional-construction-20261107/main-ci-at-seal.json), 5 jobs on its
fresh CI run pass and 1 remains live. This checkpoint awaits the ordinary
push gate. Product code, README claims and releases are unchanged.

[Archive verification](h5-augmented-conditional-construction-20261107/archive-checks.json),
[manifest](h5-augmented-conditional-construction-20261107/raw-manifest.json), [source bindings](h5-augmented-conditional-construction-20261107/source-bindings.json),
[historical references](h5-augmented-conditional-construction-20261107/external-evidence.json) and
[runtime pins](h5-augmented-conditional-construction-20261107/runtime-bindings.json) preserve the complete evidence.
