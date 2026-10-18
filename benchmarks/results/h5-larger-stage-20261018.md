# Larger-return sampling, timing and repair observations — 2026-10-18

**All four diagnostic layouts validate.** The observer records which
original part types are available and move between sheets, requested repair
time, elapsed duration, rejection stages and immediate
material/last-sheet extent. These are new observations, not a reconstruction
of the failed 72-outcome pilot or a quality comparison.

[The committed plan](h5-larger-stage-20261018/plan.json) uses the two
mechanical development jobs, kerfs 0.2 and 1.5 mm, seed zero, 60 seconds
and serial physical CCD0 CPU 8. All original algorithm settings remain.
Instrumentation can perturb wall timing. Production stays unchanged.

| Job | Kerf mm | Attempts | Accepted pairs | Same-inventory accepted | Outcomes |
| --- | ---: | ---: | ---: | ---: | --- |
| m-mechanical-large-plates | 0.2 | 1 | 1 | 0 | accepted: 1 |
| m-mechanical-large-plates | 1.5 | 7 | 0 | 0 | source_repair_failed: 6, accepted: 1 |
| m-mechanical-panel-hardware | 0.2 | 8 | 0 | 0 | neutral_inventory_rejected: 4, source_repair_failed: 4 |
| m-mechanical-panel-hardware | 1.5 | 7 | 0 | 0 | neutral_inventory_rejected: 3, source_repair_failed: 4 |

Of 2 accepted exchanges, 0 return the same original
part types and quantities as they take. This preserves inventory, not
necessarily positions or orientations. Immediate validated material
decreases in 2 accepted exchanges; last-sheet occupied
extent decreases in 2. These observations do not establish
a later benefit or harm from rearrangement.

There are 42 retained proposals across the observed calls;
12 preserve inventory. Retained proposals are not necessarily
attempted, and these counts are not all sampled configurations.

The session took 4.054 minutes. All archive CRCs/member hashes,
trace references, solver counters, original quantities, public exports and
independently recomputed metrics pass. Source, input and binary guards match.
[Every attempt](h5-larger-stage-20261018/observed-exchanges.json) and
[verification](h5-larger-stage-20261018/verification.json) are retained.

No original failed result, gate, production implementation or held-out file
is changed. **H2/H5 remain open; completed weight stays 60%.**

## Source choices and repair time

| Job | Kerf mm | Source inventory by original item ID | Pair choices by item ID | Neutral rejections | Source failures / repairs | Requested source time range, s | Total source time, s |
| --- | ---: | --- | --- | ---: | ---: | --- | ---: |
| m-mechanical-large-plates | 0.2 | [{1: 1, 0: 12, 3: 6}] | [[[0, 0], [1, 0], [3, 3], [1, 0], [0, 0], [1, 0], [3, 3], [0, 3], [0, 0], [0, 3], [3, 3], [0, 3]]] | 0 | 0 / 1 | [0.2390175249999995, 0.2390175249999995] | 0.112091 |
| m-mechanical-large-plates | 1.5 | [{1: 1, 0: 12, 3: 6}] | [[[0, 0], [1, 0], [3, 3], [1, 0], [0, 0], [1, 0], [3, 3], [0, 3], [0, 0], [0, 3], [3, 3], [0, 3]]] | 0 | 6 / 7 | [0.0005516624999994946, 0.2987496750000007] | 0.498155 |
| m-mechanical-panel-hardware | 0.2 | [{2: 2, 1: 42, 0: 17, 3: 41}] | [[[2, 2], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1], [3, 3], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1]]] | 4 | 4 / 8 | [0.010320025000000399, 0.2729090249999997] | 0.548180 |
| m-mechanical-panel-hardware | 1.5 | [{2: 2, 1: 42, 0: 17, 3: 41}] | [[[2, 2], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1], [3, 3], [2, 1], [1, 1], [2, 1], [0, 0], [2, 1]]] | 3 | 4 / 7 | [0.007431925000000561, 0.3001644749999999] | 0.591157 |

Item IDs denote original model items; repeated IDs represent interchangeable
copies. Retained choices are not necessarily attempted. Requested remaining
time is logged immediately before each separator call and can be negative.
Elapsed time can slightly overrun a checked deadline. These observations
do not prove the minimum time needed or feasibility of failed assignments.

## Paired sample rejection partition

| Job | Kerf | Pair kind | Calls | Visited / total | Invalid pose | Boundary | Empty | Over 3 | Returned area | Eligible | Retained | Truncated calls |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| m-mechanical-large-plates | 0.2 | same | 1 | 175 / 175 | 0 | 12 | 0 | 86 | 0 | 77 | 6 | 0 |
| m-mechanical-large-plates | 0.2 | mixed | 0 | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| m-mechanical-large-plates | 1.5 | same | 1 | 175 / 175 | 0 | 12 | 0 | 87 | 0 | 76 | 6 | 0 |
| m-mechanical-large-plates | 1.5 | mixed | 0 | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| m-mechanical-panel-hardware | 0.2 | same | 1 | 204 / 204 | 0 | 21 | 0 | 141 | 0 | 42 | 6 | 0 |
| m-mechanical-panel-hardware | 0.2 | mixed | 0 | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| m-mechanical-panel-hardware | 1.5 | same | 1 | 204 / 204 | 0 | 21 | 0 | 142 | 0 | 41 | 6 | 0 |
| m-mechanical-panel-hardware | 1.5 | mixed | 0 | 0 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Reasons partition visited samples in the displayed order. Boundary collisions
take precedence when an oversized set also occurs. An empty set needs no exchange
and is skipped by this proposal routine. Retained proposals may never be attempted
when the phase expires. Counts do not establish causality or global infeasibility.


## Observed phase costs and intermediate geometry

All four final layouts and four intermediate layouts independently validate. Filled-outer audits check 23,542 same-sheet pairs with the unchanged 1e-7 mm clearance tolerance.

| Job | Kerf mm | Invocation s | Initial validation s | Choice construction s | Pair generation s | Attempt setup s | Source repair s | Trial validation s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 0.210094 | 0.044761 | 0.000748 | 0.001730 | 0.001798 | 0.112091 | 0.043423 |
| m-mechanical-large-plates | 1.5 | 0.621304 | 0.047883 | 0.001425 | 0.001685 | 0.011946 | 0.498155 | 0.046021 |
| m-mechanical-panel-hardware | 0.2 | 1.082615 | 0.093182 | 0.002909 | 0.001267 | 0.014386 | 0.548180 | 0.366622 |
| m-mechanical-panel-hardware | 1.5 | 1.058919 | 0.101830 | 0.003112 | 0.001281 | 0.012687 | 0.591157 | 0.298668 |

The [complete timing record](h5-larger-stage-20261018/phase-timings.json) also retains receiver repair, trial reconstruction and unassigned/observation overhead. Recorded scopes are disjoint and reconcile with each invocation duration.

| Kerf mm | Before exchange, mm2 | After exchange, mm2 | After fill, mm2 | Remaining after fill, s |
| --- | ---: | ---: | ---: | ---: |
| 0.2 | 5419041.9645 | 5418955.5465 | 5418955.5465 | 0.9653642 |
| 1.5 | 5419041.9150 | 5419001.6415 | 5419001.6415 | 0.5524092 |

[Every saved intermediate layout and independent check](h5-larger-stage-20261018/intermediate-layout-checks.json) is retained. Material change during filling was measured without assuming nonincrease.

Panel hardware retains six proposals for the first same-item pair at each
kerf. Seven attempted paired proposals have zero initial repair loss, repair
durations below 0.0001 seconds, and unchanged inventory/material. Their full
validations cost 0.3666222 and 0.2986677 seconds in aggregate. The group phase
then has insufficient reserved time for the later pair choices; no mixed pair
is generated. Later single proposals spend 0.5481800 and 0.5911573 seconds in
failed source repairs. Construction and paired sampling each take only a few
milliseconds here. These are observed durations with logging, not minimum
time requirements or speed comparisons.

The next narrow check is whether any expensive neutral trial is exactly the
same physical state as its validated incumbent: the same original item index,
full transform (including reflection), multiplicity and sheet location. Same
inventory or equal material alone is insufficient. First observe exact state
equivalence on these rejected trials and cover key-order changes, distinct
original identities, changed poses and duplicate counts in authored tests.
Only a proven identical state could be rejected before repeated validation;
every changed state and every accepted exchange must retain the full original
geometry/material checks. Do not use geometric tolerances, rounded poses or
an unchecked material estimate to bypass those checks.

Large-plate acceptances leave 0.9653642 and 0.5524092 seconds of their original
exchange opportunity after filling, while immediate material improves by only
86.4180 and 40.2735 mm2. Filling does not change those material totals. This
identifies unused time after acceptance, but does not prove another useful
swap exists. Any later consecutive-exchange experiment must retain the shared
budget, valid incumbent and cycle protection. The original five failed pilot
material comparisons remain authoritative; neither observation is a quality
gain or justification for integration.

[Source review and next check](h5-larger-stage-20261018/source-review.json). H2/H5 remain open at 60%.
