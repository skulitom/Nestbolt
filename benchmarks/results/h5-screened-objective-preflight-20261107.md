# Complete screened-objective preflight — 2026-11-07

The complete objective now uses exact boundary clipping after excluding only
strictly disjoint edge/polygon boxes. It preserves every old result field and
all gradient coordinates in **363 comparisons**.
This is a validation checkpoint with **no optimizer call**. The latest packing
candidate still fails 54 source pairs; H2/H5 remain open at **60% completed weight**.

Only the weighted/augmented import chain changes. The original mathematical
identity, model compilation and closure keys remain identical; all nine original
identity code hashes remain verified and the new implementation hashes are bound
separately. All **23 closed problem keys** stay closed. Arrays retain directed-pair
order, integration pivots and the half-weight shared-boundary convention. Touching
boxes and nonfinite bounds remain included. There is no coordinate rounding or
cache reused across changed inputs.

[Complete objective controls](h5-screened-objective-preflight-20261107/complete-objective-controls.json) compare
original/clearance/weighted/auxiliary/augmented scores, all 81 gradient coordinates,
all 528 pair losses, positive terms, clipped-segment counts, coincident lengths and
auxiliary records. Detailed and plain evaluation, score and pair-loss interfaces
are checked. [All 147 source owner/mode cases](h5-screened-objective-preflight-20261107/source-mode-controls.json)
retain their independent source scores. Original, latest-source, historical flat
and two fixed interior controls are also included.

[Runtime replay](h5-screened-objective-preflight-20261107/runtime-winner-controls.json) covers every one of **211
records from five closed calls**, with **167 saved points**
and all fifteen strict winner streams. Each runtime record now receives independent
scalar reconstruction of all 81 gradient coordinates. Including the five source/
interior/contact cases, **216 complete scalar-gradient
cases** pass. Maximum independent score error is
5.960e-08 mm² and gradient error is
2.910e-11 mm. Three distinct winners in
the latest second epoch remain distinct. No closed output is used as an initializer.

The [original 324 central samples](h5-screened-objective-preflight-20261107/preserved-original-central-controls.json)
retain all fourteen failed finite-step checks. Their [fourteen one-sided controls](h5-screened-objective-preflight-20261107/touching-one-sided-controls.json)
reproduce the same selected gradient and finite slopes; they establish finite
enclosures only, not unique derivatives at contact. The two fixed historical
interior models pass [324 central samples](h5-screened-objective-preflight-20261107/central-controls.json) with
unchanged steps and tolerances. No contact result is relabelled smooth.

[Eight boundary cases](h5-screened-objective-preflight-20261107/boundary-policy-controls.json) cover empty groups,
empty edges, identical, contained, disjoint, corner-touching, shared-edge and
zero-length-edge geometry. Available scalar gradients, clipped counts and shared
lengths agree. Deliberately dropping touching edges is detected by the counts and
coincident lengths of identical squares. [Nine model corruptions](h5-screened-objective-preflight-20261107/negative-controls.json)
remain rejected by independent model readback.

[Complete evaluation timings](h5-screened-objective-preflight-20261107/timings.json), in seconds:

| Labelled context | Original mean | Screened mean | Observed saving |
| --- | ---: | ---: | ---: |
| source_initializer | 0.041671 | 0.037982 | 0.003689 |
| closed_flat_validation_only | 0.079706 | 0.070875 | 0.008831 |
| latest_source_initializer | 0.053117 | 0.043973 | 0.009144 |
| interior-0 | 0.048290 | 0.045517 | 0.002773 |
| interior-1 | 0.053750 | 0.051844 | 0.001906 |
| latest-epoch-0-initial | 0.050558 | 0.045754 | 0.004804 |
| latest-epoch-0-augmented | 0.071681 | 0.078615 | -0.006934 |
| latest-epoch-0-original | 0.079170 | 0.062186 | 0.016984 |
| latest-epoch-0-unweighted | 0.085624 | 0.078220 | 0.007404 |
| latest-epoch-1-initial | 0.082088 | 0.073296 | 0.008792 |
| latest-epoch-1-augmented | 0.084246 | 0.075747 | 0.008499 |
| latest-epoch-1-original | 0.076244 | 0.074758 | 0.001485 |
| latest-epoch-1-unweighted | 0.086185 | 0.071142 | 0.015042 |

The fixed order is old/screened/screened/old, with two samples per variant in each
labelled context. Labels include duplicate states where winner streams coincide
or an epoch starts at its source initializer. Each evaluation includes geometry,
area calculations, all gradients, auxiliary calculations and detailed output.
Object construction is measured separately in the [summary](h5-screened-objective-preflight-20261107/timing-summary.json).
Serialization, source validation and optimizer orchestration are outside these
measurements. These observations do not establish stable runtime, statistical
significance or a packing gain.

The single-call timings include variability and one slowdown; that result stays
preserved. A separate [full-trajectory measurement](h5-screened-objective-preflight-20261107/trajectory-checks.json)
uses each latest closed epoch's complete saved sequence in fixed old/screened/
screened/old batch order. All **392 detailed evaluations** across eight batches
match exactly; their [per-evaluation output hashes](h5-screened-objective-preflight-20261107/trajectory-exact-output-controls.json)
remain recorded. Each batch constructs one objective, then evaluates all 54 or 44
points. Reading inputs and checking the outputs are outside the timed interval.

| Saved epoch | Original mean | Screened mean | Observed saving |
| --- | ---: | ---: | ---: |
| 0 | 4.142659 | 3.717614 | 0.425045 |
| 1 | 3.738695 | 3.372735 | 0.365960 |

These are saved-trajectory evaluation costs, not optimizer executions or evidence
that a future trajectory will match. The separate [batch process](h5-screened-objective-preflight-20261107/trajectory-process.json)
closes in 30.515868 s under its 120 s / 2 GiB cap.

The [bounded audit](h5-screened-objective-preflight-20261107/preflight-process.json) closes in
**253.732413 s**, with peak committed memory
49,770,496 bytes under its 900 s / 2 GiB cap.
All 3 processes close. This validation process
does not create a new search initializer or consume an optimizer call.

[Next](h5-screened-objective-preflight-20261107/next-step.json), prepare a fresh original-source model under all
twenty-three closures, retaining **39.049161 s** preparation plus every new source
cost. Independently verify the full model/source output and complete budget before
freezing another finite attempt. Four arrangements and all 440 allocation candidates
remain unresolved; full66 validity, native/material evidence and the original H5
matrix are still required.

Main is **ddf2310d**. The [last ordinary push receipt](h5-screened-objective-preflight-20261107/prior-main-push-receipt.json)
preserves 52 files and the preceding CI gate. [Current CI](h5-screened-objective-preflight-20261107/main-ci-at-review.json)
has 5 passed and 1 live jobs at review. Product code, README and releases
are unchanged. This checkpoint awaits the next ordinary push gate.

[Archive checks](h5-screened-objective-preflight-20261107/archive-checks.json), [raw manifest](h5-screened-objective-preflight-20261107/raw-manifest.json),
[source bindings](h5-screened-objective-preflight-20261107/source-bindings.json), [historical evidence](h5-screened-objective-preflight-20261107/external-evidence.json)
and [runtime pins](h5-screened-objective-preflight-20261107/runtime-bindings.json) retain the complete evidence graph.
