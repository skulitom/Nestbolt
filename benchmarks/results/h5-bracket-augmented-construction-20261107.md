# Augmented bracket-depth construction — 2026-11-07

The complete augmented objective passes its independent model audit and closes
one bounded optimizer call. Its final candidate still has **44 source-pair
failures** and **33,707.125558 mm²** original overlap. All three recorded winner
streams select the same point. Compared with the preceding conditional search,
it has fewer failing pairs but more overlap area; **no packing improvement or
valid full layout is claimed**. H2/H5 remain open at **60%**.

## Full objective and independent model checks

The model retains 33 movers, 81 coordinates, all 528 positively weighted original
and clearance-area pair losses, and every hard stock/fixed-part domain. It adds
the 15 unweighted bracket collision-depth terms at the previously frozen
coefficient 1. Source initializer, legal modes and original weights are unchanged.
The objective identity binds the full policy, region bytes and nine executing
source modules. [Closure controls](h5-bracket-augmented-construction-20261107/closure-controls.json) distinguish the
new objective from the already closed area-only problem on the same physical
mode/weight vector. None of the seven earlier weighted calls resumes.

[Model preflight](h5-bracket-augmented-construction-20261107/model-audit.json) checks every field and all **147**
legal owner-mode full scores, with maximum scalar score error 1.165e-10 mm².
It independently accumulates 306 directed source-boundary terms and 162 combined
gradient coordinates at the original initializer and the saved flat case;
maximum discrepancy is 1.528e-13 mm. [Nine corruptions](h5-bracket-augmented-construction-20261107/negative-controls.json)
of identities, coefficients, bounds, pivots, initial coordinates or terms are
rejected. The saved optimized case is validation only and never seeds the run.

## Contact derivatives: preserved failures and limited claims

The [first audit](h5-bracket-augmented-construction-20261107/preserved-failed-audit-process.json) stops when a central
sample at the exact initializer disagrees with the selected area-boundary
convention. A diagnostic retains all **324** original-case central samples,
including **14 failures**: eight at the initializer and six at the saved
candidate. [Pair-level decomposition](h5-bracket-augmented-construction-20261107/contact-pair-causes.json) locates
the discrepancies in source-area contact/near-transition terms. It does not
establish the initial zero-area-contact hypothesis; that false diagnostic
flag remains explicit. The new auxiliary finite differences remain small.

The diagnostic's first output write also fails on a NumPy boolean.
[That serialization failure](h5-bracket-augmented-construction-20261107/preserved-serialization-failure.json),
the original helper and its incomplete JSON bytes remain preserved; the raw
archive stores those incomplete bytes under a `.partial.txt` member while the
record retains their original path and hash. Version 2 changes only output
serialization and output location, preserving all numerical controls.

[The versioned model audit](h5-bracket-augmented-construction-20261107/audit-correction.json) retains the original
samples and their failures. It checks independent scalar gradients at those
same points and [one-sided finite-slope enclosures](h5-bracket-augmented-construction-20261107/touching-controls.json)
for all 14 failing coordinates. These are finite controls, **not a unique
derivative or a global generalized-gradient certificate**. Separately it checks
324 central samples at the exact two deterministic interior controls already
used by the earlier weighted-model audit. Those points have no shared boundary
and unique auxiliary nearest features; they remain validation only. All pass
the unchanged 0.02+3e-6×|gradient| tolerance, including maximum absolute
error 0.026538 for the higher-weight control. Model, kernel, actual initializer,
weights and tolerances do not change. The passing model-audit wrapper takes
21.856198s; the first failed wrapper takes 6.712762s. All artifacts remain.

## One finite call and complete replay

The new problem opens once, with a 36 s L-BFGS-B slice inside preparation-inclusive
60/90 s algorithm/shared limits and a 2 GiB process-tree limit. There are no mode
changes, coefficient updates or retries. Existing area-boundary and nearest
feature rules are explicitly treated as nonsmooth search conventions; full
source geometry remains the acceptance test.

[Complete response replay](h5-bracket-augmented-construction-20261107/response-audit.json) verifies **237 evaluation
records**: the initial point and 236 optimizer evaluations. It recomputes every
score and gradient, independently reconstructs every scalar source-area and
rational auxiliary score, and checks all **212** retained improvements. The
largest independent score discrepancy is 2.329e-10 mm². It separately reconstructs
strict winners for augmented score, original overlap area and unweighted
original-plus-clearance sum; [all three select evaluation 236](h5-bracket-augmented-construction-20261107/winner-reconciliation.json).
Each winner receives a full 66 source readback covering 1,380 same-sheet pairs,
264 stock edges, 90 holes and 10,026 hole vertices. Every fixed-part and stock
check passes. The response-audit wrapper closes in 32.861542s.

The 36 s slice returns at **36.071821s**; its **0.071821s overrun** is retained.
Complete source preparation is **11.688681s**: the previously charged 11.002683s
plus the full new 0.685998s model-preparation wrapper. Algorithm/shared totals
are **52.962365/53.493153s**. [The process tree closes](h5-bracket-augmented-construction-20261107/closed-search-process.json)
with 100,876,288 bytes peak aggregate committed memory. This
[new objective key is permanently closed](h5-bracket-augmented-construction-20261107/closed-problem.json); no
native call or allocation exclusion follows.

## Remaining geometry and next preflight

The [44 source failures](h5-bracket-augmented-construction-20261107/source-failures.json) all have positive original
intersection. Their [family composition](h5-bracket-augmented-construction-20261107/family-failures.json) is:

| Families | Failing pairs | Original overlap (mm²) |
| --- | ---: | ---: |
| Bracket / insert | 3 | 9,566.315981 |
| Bracket / cog | 8 | 5,202.561575 |
| Cog / insert | 14 | 10,113.822169 |
| Cog / cog | 19 | 8,824.425832 |

The [read-only diagnostic](h5-bracket-augmented-construction-20261107/outcome-diagnostic.json) finds no bracket/bracket
source failure and zero auxiliary loss at this candidate. All 45 positive
original/clearance pair terms have a nonzero available pair gradient; no flat
pair probe is triggered. Four cogs have lower-y descent blocked by hard bounds.
These observations do not prove a global packing obstruction.
[Prior comparisons](h5-bracket-augmented-construction-20261107/prior-comparisons.json) preserve both worse overlap
and the different experimental choices; no causal improvement is attributed
to the added term.

[Next](h5-bracket-augmented-construction-20261107/next-step.json), assess legal conditional mode/center choices using
the complete augmented score, starting only from the original unoptimized
source state. Reconcile the earlier weighted selectors, retain the frozen 9-by-9
grid, independently replay all single/joint scores and account for every
consumed preparation stage before any new finite search. The current augmented
key and seven older weighted keys remain closed. No new selector or successor
call exists. Four earlier fixed arrangements and 440 allocations remain unresolved.

The preceding two checkpoints reached main cbc49d2c after all six earlier checks
passed, preserving 52 protected files. [The receipt](h5-bracket-augmented-construction-20261107/prior-main-push-receipt.json)
records the ordinary atomic push. [At this review](h5-bracket-augmented-construction-20261107/main-ci-at-review.json),
4 fresh CI jobs pass and 2 native jobs remain live, so this checkpoint
awaits the ordinary push gate. Product code, README claims and releases are unchanged.

[Archive verification](h5-bracket-augmented-construction-20261107/archive-checks.json),
[manifest](h5-bracket-augmented-construction-20261107/raw-manifest.json), [source bindings](h5-bracket-augmented-construction-20261107/source-bindings.json),
[historical references](h5-bracket-augmented-construction-20261107/external-evidence.json) and
[runtime pins](h5-bracket-augmented-construction-20261107/runtime-bindings.json) preserve the complete evidence.
