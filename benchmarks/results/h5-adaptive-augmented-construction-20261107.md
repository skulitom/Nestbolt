# Adaptive augmented construction — 2026-11-07

The bounded adaptive pipeline closes after **two distinct calls** and a third
selection round that correctly stops without opening a call. Independent replay
verifies every evaluation, both complete runtime selection rounds and all six
full-source winner outputs. Its best original-overlap candidate still fails
**50 source pairs**, with **29,249.033408 mm²** overlap. It improves those two
measures against the preceding fixed-weight augmented construction, but remains
worse than the earlier area-only adaptive result (46 failed pairs and
28,414.189788 mm²). No packing validity or allocation exclusion is claimed.
H2/H5 remain open at **60% completed milestone weight**.

## Source-only initialization and deadline controls

[The source pool is independently re-ranked](h5-adaptive-augmented-construction-20261107/source-ranking-controls.json)
against nine closed keys using all 2,854 previously audited full-score readbacks.
The 6,396 original center trials remain unchanged and fully charged; only the
newly closed proposal's exclusion flag changes. A fresh model reconstructs
owners 15 and 17 in mode 2 from the original A/W source coordinates and their
raw proposal centers. Its augmented score is 216,774.908067 mm², below the best
single's 229,308.162672 and source baseline 244,577.060782. Its original overlap
is still 76,322.315097 mm². No optimized ancestor supplies an initializer.

[Model controls](h5-adaptive-augmented-construction-20261107/selected-model-controls.json) independently verify all
81 coordinates, 528 weighted original/clearance pairs and 15 coefficient-1
auxiliary bracket terms. All legal hard domains and continuous cog angles stay
intact. The selected score agrees exactly with the scalar reference; 152
directed gradient terms differ by at most 5.685e-14 mm. Existing contact and
nearest-feature conventions remain explicit, without a smoothness claim.

[The deadline-aware selector](h5-adaptive-augmented-construction-20261107/deadline-controls.json) reproduces the
entire original audited pool exactly. Six injected expiration points cover
before initialization, after one complete mode, before proposals, after one
proposal, after 1,441 proposals and after the complete 2,854-proposal pool.
Every stop preserves the exact completed prefix and returns no selected
proposal. A real 0.05 s deadline stops after 82 center trials; the observed
cooperative overrun is 0.015768 s and the full control returns in 0.070894 s.
One in-progress geometry batch may overrun; the Windows Job remains the outer
time, memory and process bound. No validation output seeds the search.

[The earlier adaptive pipeline is reconciled](h5-adaptive-augmented-construction-20261107/adaptive-history-controls.json)
as a code and validation reference. Both 528-coefficient historical updates
reproduce independently rounded exact-rational arithmetic. [Two additional
validation-only update vectors](h5-adaptive-augmented-construction-20261107/weight-update-controls.json), both clamp
limits and the all-zero-loss case also pass. Updated models and scalar
gradients retain every term; auxiliary coefficients do not change.

Full source preparation is **17.623198 s**, including the preceding 16.974380 s
pool and the complete new 0.648818 s preparation wrapper. The independent
preflight wrapper takes 24.366325 s and closes all descendants. A text-extraction
error in the first search-code generator occurs before any generated runner or
search exists; [the original failure and helper](h5-adaptive-augmented-construction-20261107/preserved-generator-failure.json)
are preserved. Version 2 corrects only its newline delimiter.

## Finite search and complete replay

The frozen controller permits at most three 8 s L-BFGS-B calls, a selection
deadline at 52 s and a source-check boundary at 54 s inside the preparation-
inclusive 60/90 s limits. Later rounds update the fixed positive bounded weights
using only the preceding augmented winner's area losses. The full augmented
objective scores every center and proposal. A joint must beat both the current
state and the best admissible single by more than 1e-6 mm².

[The result](h5-adaptive-augmented-construction-20261107/closed-search-result.json) opens only two new keys. Epoch 0
has 113 optimizer evaluations and 101 retained improvements; all three winner
streams coincide at 53 failed pairs and 39,731.032334 mm² overlap. Epoch 1 has
104 evaluations and 94 retained points. Its original-overlap winner differs
from the shared augmented/unweighted winner:

| Epoch 1 winner | Failed source pairs | Original overlap (mm²) | Unweighted area sum (mm²) |
| --- | ---: | ---: | ---: |
| Original overlap | 50 | 29,249.033408 | 59,731.770000 |
| Augmented / unweighted | 51 | 29,249.898618 | 59,717.242440 |

[Independent response replay](h5-adaptive-augmented-construction-20261107/response-audit.json) checks all
**219 evaluation records**, **195
retained points**, 1,056 runtime weight coefficients, **12,792 center trials**
and **5,708 full proposals**. Every runtime selection score is independently
reconstructed, including the final stopping round. All six full66 source
readbacks cover 1,380 same-sheet pairs, 264 stock edges, 90 holes and 10,026 hole
vertices each. Fixed-part and stock checks pass. No winner is valid.

Preparation-inclusive algorithm/shared totals are **46.232997/46.308978 s**.
The two solve-slice overruns remain recorded in the response audit.
[All five search processes close](h5-adaptive-augmented-construction-20261107/closed-search-process.json), with
121,110,528 bytes peak aggregate committed memory. [The initial key](h5-adaptive-augmented-construction-20261107/closed-problem-00.json)
and [the adaptive key](h5-adaptive-augmented-construction-20261107/closed-problem-01.json) are permanently closed.
All nine prior keys remain closed as well; no native call or third optimizer
call follows the stopping condition.

## Why the next round stopped

[The final selection](h5-adaptive-augmented-construction-20261107/selection-stop-diagnostic.json) has baseline
130,033.415542 mm², best single 124,973.258351 mm² and best joint
127,189.937793 mm². The single changes owner 11 to mode 0. The joint adds
owner 2 in mode 2; it is 2,216.679442 mm² worse than the single. Both improve
the baseline, but the frozen joint-only prerequisite correctly rejects the
joint and ends the whole pipeline. The unused candidates are diagnostic only.

[Source-failure diagnosis](h5-adaptive-augmented-construction-20261107/outcome-diagnostic.json) records
53 positive area terms, 0
flat available pair gradients, 0 bracket/bracket
failures and 4 cogs with lower-y descent blocked.
[Family failures](h5-adaptive-augmented-construction-20261107/family-failures.json) and [prior comparisons](h5-adaptive-augmented-construction-20261107/prior-comparisons.json)
retain the complete composition and the worse result against the earlier
area-only adaptive construction.

[Next](h5-adaptive-augmented-construction-20261107/next-step.json), independently preflight a separately specified
rule accepting the best strict-improving admissible single **or** joint choice.
Reconcile it against the saved complete score readbacks, then build a fresh
original-source initializer with all eleven closed keys excluded and all
preparation charged. No revised rule, successor state or call is prepared.
This pipeline, its optimized winners and unused stopping candidates cannot
be continued or reused as a successor seed. Four earlier arrangements and
440 allocation candidates remain unresolved.

[At review](h5-adaptive-augmented-construction-20261107/main-ci-at-review.json), main 193660c4 has 6 passed
jobs and 0 live jobs; the workflow aggregate also passed at review.
The preceding 760d2ee6 checkpoint and this one are ready for the ordinary
commit/push checks. Product code, README claims and releases are unchanged.

[Archive verification](h5-adaptive-augmented-construction-20261107/archive-checks.json),
[manifest](h5-adaptive-augmented-construction-20261107/raw-manifest.json), [source bindings](h5-adaptive-augmented-construction-20261107/source-bindings.json),
[historical references](h5-adaptive-augmented-construction-20261107/external-evidence.json) and
[runtime pins](h5-adaptive-augmented-construction-20261107/runtime-bindings.json) preserve the complete evidence.
